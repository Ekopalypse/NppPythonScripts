# -*- coding: utf-8 -*-
r'''
This is a simple wrapper around the MS Dialog API
See https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-dialogboxindirectparamw for more information.

The workflow is like this

1. Import the module
2. Create a dialog instance
3. Create the controls
4. Add the controls to the dialog
5. Show the dialog

Checkout the test_win_dialog.py script for examples.
'''

__all__ = ['Dialog',
           'Button', 'CheckBoxButton', 'GroupBox', 'CommandButton', 'RadioButton', 'SplitButton',
           'SimpleLabel', 'TruncatedLabel', 'BlackFramedLabel', 'CenteredLabel', 'RigthAlignedLabel',
           'ComboBox'
           ]
__version__ = '0.1'
__author__ = 'ekopalypse'

from .dialog_template import Window, Control
from .win_helper import (
    LOWORD, DIALOGPROC, DialogBoxIndirectParam,
    GetDlgItem, EndDialog,
    GetWindowRect, CopyRect, OffsetRect, SetWindowPos, GetModuleHandle,
    WinMessages as WM,
)
from .button import Button, CheckBoxButton, GroupBox, CommandButton, RadioButton, SplitButton
from .label import SimpleLabel, TruncatedLabel, BlackFramedLabel, CenteredLabel, RigthAlignedLabel
from .combobox import ComboBox

from Npp import notepad
import ctypes
from ctypes import wintypes

class Dialog():
    def __init__(self, title=None, parent=None, size=None, resizable=False):
        if not title:
            raise ValueError('Dialog class is missing mandatory parameter: title')
        self.title = title
        self.parent = parent or notepad.hwnd
        self.size = size or (190, 210)
        self.resizable=resizable
        self.control_list = []
        self.control_callbacks = {}
        self.control_start_id = 1025
        self.hwnd = 0

    def __default_dialog_proc(self, hwnd, msg, wparam, lparam):
        """ window procedure callback """

        if msg == WM.INITDIALOG:
            self.hwnd = hwnd
            for i, control in enumerate(self.control_list):
                self.control_list[i].hwnd = GetDlgItem(hwnd, control.id)
                if control.intialize_needed:
                    control.initialize()

            rcOwner = wintypes.RECT()
            rcDlg = wintypes.RECT()
            rc = wintypes.RECT()

            GetWindowRect(self.parent, ctypes.byref(rcOwner))
            GetWindowRect(hwnd, ctypes.byref(rcDlg))
            CopyRect(ctypes.byref(rc), ctypes.byref(rcOwner))

            OffsetRect(ctypes.byref(rcDlg), -rcDlg.left, -rcDlg.top)
            OffsetRect(ctypes.byref(rc), -rc.left, -rc.top)
            OffsetRect(ctypes.byref(rc), -rcDlg.right, -rcDlg.bottom)

            center_x = rcOwner.left + (rc.right // 2)
            center_y = rcOwner.top + (rc.bottom // 2)
            SetWindowPos(hwnd, 0, center_x, center_y, 0, 0, 1)  # 1 = SWP_NOSIZE, retains the current size (ignores the cx and cy parameters).

            return True

        elif msg == WM.CLOSE:
            EndDialog(hwnd, 0)  # this is executed by clicking the X in the upper right corner

        elif msg == WM.COMMAND:
            control_id = LOWORD(wparam)
            if control_id in self.control_callbacks:
                control = self.control_callbacks[control_id]
                control.callback(wparam, lparam)
            return True

        return False

    def add_controls(self, controls=[]):
        self.control_list = controls

    def show(self):
        self.__create_dialog()

    def terminate(self):
        if self.hwnd:
            EndDialog(self.hwnd, 0)

    def __align_struct(self, tmp):
        # align template structure to dword size
        dword_size = ctypes.sizeof(wintypes.DWORD)
        align = dword_size - len(tmp) % dword_size
        if align < dword_size:
            tmp += bytearray(align)
        return tmp

    def __create_dialog(self):
        controls = bytearray()
        for i, control in enumerate(self.control_list):
            if not isinstance(control, Control):
                raise TypeError(f"{control} is not an instance of Control")
            control.id = self.control_start_id + i
            control_struct = control.create()
            controls += self.__align_struct(control_struct)
            self.control_callbacks[control.id] = control

        dlgwindow = Window(self.title,
                           self.size,
                           (0, 0),
                           self.resizable,
                           len(self.control_list)).create()
        dlgwindow = self.__align_struct(dlgwindow)

        _window = dlgwindow + controls
        raw_bytes = (ctypes.c_ubyte * len(_window)).from_buffer_copy(_window)
        hinstance = GetModuleHandle(None)
        DialogBoxIndirectParam(hinstance,
                               raw_bytes,
                               self.parent,
                               DIALOGPROC(self.__default_dialog_proc),
                               0)

        if self.hwnd == 0:
            raise WindowsError(f'Failed to create dialog, error:{ctypes.WinError()}')
