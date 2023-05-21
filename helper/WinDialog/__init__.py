# -*- coding: utf-8 -*-
"""
A simple Windows dialog wrapper module.

This module provides a set of classes and enums that wrap around the Windows dialog controls and API.
It allows developers to easily create and interact with dialogs and their controls in a simplified manner.

Currently the following classes and enums are supported and tested:
(Note that only basic functionality has been implemented so far).
- Dialog: Represents a dialog window.
- Button: The standard button control and base class for various other types of buttons.
    DefaultButton, CheckBoxButton, GroupBox, CommandButton, RadioButton, SplitButton
- Label: Represents a static control and base class for various other types of labels.
    TruncatedLabel, BlackFramedLabel, CenteredLabel, RightAlignedLabel
- ComboBox: Represents a combobox control.
- ComboBoxEx: Represents an comboboxex control.
- ListBox: Represents a listbox control.
- TextBox: Represents a edit control.
- ListView: Represents a syslistview32 control.
- ProgressBar: Represents a progress bar control.
- StatusBar: Represents a status bar control.
- UpDown: Represents an up-down control.
- Scintilla: Represents a Scintilla control.
- TreeView: Represents a systreeview32 control.

Enums:
- BS: Button control styles.
- SS: Static control styles.
- CBS: ComboBox control styles.
- CBES_EX: ComboBoxEx control styles.
- LBS: ListBox control styles.
- ES: Edit control styles.
- LVS: ListView control styles.
- LVS_EX: Extended ListView control styles.
- PBS: ProgressBar control styles.
- SBARS: StatusBar control styles.
- UDS: Up-down control styles.

For more documentation on each class, refer to their respective docstrings.

Classes that are missing and for which there are currently no plans to include are:
- HotKey
- TrackBar
- ReBarWindow
- RichEdit
- ScrollBar
- Animate
- Header
- IPAddress
- Link
- Pager
- TabControl
- ToolBar
"""

__all__ = ['Dialog',
           'Button', 'DefaultButton', 'CheckBoxButton', 'GroupBox', 'CommandButton', 'RadioButton', 'SplitButton', 'BS',
           'Label', 'TruncatedLabel', 'BlackFramedLabel', 'CenteredLabel', 'RigthAlignedLabel', 'SS',
           'ComboBox', 'ComboBoxEx', 'CBS', 'CBES_EX',
           'ListBox', 'LBS',
           'TextBox', 'ES',
           'ListView', 'LVS', 'LVS_EX',
           'ProgressBar', 'PBS',
           'StatusBar', 'SBARS',
           'UpDown', 'UDS',
           'Scintilla',
           'TreeView'
           ]
__version__ = '0.2'
__author__ = 'ekopalypse'

from .win_helper import (
    SWP_NOSIZE,
    DIALOGPROC, DialogBoxIndirectParam, LPNMHDR,
    GetDlgItem, EndDialog,
    GetWindowRect, CopyRect, OffsetRect, SetWindowPos, GetModuleHandle,
    WinMessages as WM,
    WindowStyle as WS,
    DialogBoxStyles as DS
)
from .controls.__control_template import Control
from .controls.button import Button, DefaultButton, CheckBoxButton, GroupBox, CommandButton, RadioButton, SplitButton, BS
from .controls.static import Label, TruncatedLabel, BlackFramedLabel, CenteredLabel, RigthAlignedLabel, SS
from .controls.combobox import ComboBox, ComboBoxEx, CBS, CBES_EX
from .controls.listbox import ListBox, LBS
from .controls.edit import TextBox, ES
from .controls.syslistview32 import ListView, LVS, LVS_EX
from .controls.msctls_progress32 import ProgressBar, PBS
from .controls.msctls_statusbar32 import StatusBar, SBARS
from .controls.msctls_updown32 import UpDown, UDS
from .controls.scintilla import Scintilla
from .controls.systreeview32 import TreeView

# from .controls.richedit import ...
# from .controls.msctls_hotkey32 import ...
# from .controls.msctls_trackbar32 import ...
# from .controls.rebarwindow32 import ...
# from .controls.scrollbar import ...
# from .controls.sysanimate import ...
# from .controls.sysheader import ...
# from .controls.sysipaddress import ...
# from .controls.syslink import ...
# from .controls.syspager import ...
# from .controls.systabcontrol32 import ...
# from .controls.toolbarwindow32 import ...

from .resource_parser import parser

from Npp import notepad
import ctypes
from ctypes import wintypes, create_unicode_buffer
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Dialog:
    '''
    Dialog Class

    Represents a Windows dialog window.

    The Dialog class provides a template for creating and managing dialog windows.
    It encapsulates properties and behaviors common to dialog windows, such as
    title, size, position, styles, and controls.

    Attributes:
        title (str): The title of the dialog window.
        size ((int, int)): The width and height of the dialog window.
        position ((int, int)): The x and y coordinates of the dialog window.
        styles (int): The style flags for the dialog window.
        ex_styles (int): The extended style flags for the dialog window.
        pointsize (int): The font size for the dialog window.
        typeface (str): The font typeface for the dialog window.
        weight (int): The font weight for the dialog window.
        italic (int): The font italicization for the dialog window.
        charset (int): The character set for the dialog window.

        parent (int): The handle of the parent window for the dialog.
        center (bool): Indicates whether the dialog should be centered on the screen.
        control_list (List): A list of control instances to be added to the dialog.
        control_start_id (int): The starting identifier for controls in the dialog.
        hwnd (int): The handle of the dialog window.
        registered_commands (Dict): A dictionary of registered command messages and their associated handlers.
        registered_notifications (Dict): A dictionary of registered notification messages and their associated handlers.
        initialize (Callable): A callback function called during the initialization of the dialog.

    Note:
        The Dialog class is intended to be subclassed for specific dialog implementations.
        It provides a base template and common functionality for creating dialog windows.
    '''
    title: str                     = ''
    size: (int, int)               = (300, 400)
    position: (int, int)           = (0, 0)
    style: int                     = DS.SETFONT | DS.MODALFRAME | WS.POPUP | WS.CAPTION | WS.SYSMENU
    ex_style: int                  = 0
    pointsize: int                 = 9
    typeface: str                  = 'Segoe UI'
    weight: int                    = 0
    italic: int                    = 0
    charset: int                   = 0

    parent: int                    = notepad.hwnd
    center: bool                   = False
    control_list: List             = field(default_factory=list)
    control_start_id: int          = 1025
    hwnd: int                      = 0
    registered_commands: Dict      = field(default_factory=dict)
    registered_notifications: Dict = field(default_factory=dict)

    def __post_init__(self):
        """
        Perform post-initialization tasks for the Dialog object.

        This method is automatically called after the initialization of the Dialog object.
        It initializes the control_list, registered_commands, and registered_notifications attributes.

        Parameters:
            None.

        Returns:
            None.
        """
        self.control_list = []
        self.registered_commands = {}
        self.registered_notifications = {}

    def initialize(self):
        '''
        Initializes the dialog and its controls at runtime.

        This method is intended to be overridden by a concrete class.
        It is executed after all controls have been created but before the dialog is displayed.
        Concrete implementations should provide custom logic to set up initial values, states, and configurations of the controls.

        Parameters:
            None.

        Returns:
            None

        '''

        pass

    def __create_dialog_window(self):
        '''
        Create the dialog template structure.

        Parameters:
            None.

        Returns:
            bytearray: The byte array representing the dialog template structure.

        '''
        # https://learn.microsoft.com/en-us/windows/win32/dlgbox/dlgtemplateex
        self.windowClass = 0
        _array = bytearray()
        _array += wintypes.WORD(1)  # dlgVer
        _array += wintypes.WORD(0xFFFF)  # signature
        _array += wintypes.DWORD(0)  # helpID
        _array += wintypes.DWORD(self.ex_style)
        _array += wintypes.DWORD(self.style)
        _array += wintypes.WORD(self.dialog_items or 0)  # cDlgItems
        _array += wintypes.SHORT(self.position[0])  # x
        _array += wintypes.SHORT(self.position[1])  # y
        _array += wintypes.SHORT(self.size[0])  # width
        _array += wintypes.SHORT(self.size[1])  # height
        _array += wintypes.WORD(0)  # menu
        _array += wintypes.WORD(0)  # windowClass
        _array += create_unicode_buffer(self.title)
        _array += wintypes.WORD(self.pointsize)
        _array += wintypes.WORD(self.weight)
        _array += wintypes.BYTE(self.italic)
        _array += wintypes.BYTE(self.charset)
        _array += create_unicode_buffer(self.typeface)
        return _array

    def __default_dialog_proc(self, hwnd, msg, wparam, lparam):
        """
        Default Window Procedure Callback

        It handles messages sent to a window that are not explicitly processed by a custom window procedure.

        Parameters:
            hwnd: The handle to the window receiving the message.
            msg: The message identifier.
            wparam: Additional message-specific information.
            lparam: Additional message-specific information.

        Returns:
            The result of the message processing.

        Note: Custom window procedures should call this function when they do not handle a particular message.

        """
        if msg == WM.INITDIALOG:
                self.hwnd = hwnd
                for i, control in enumerate(self.control_list):
                    self.control_list[i].hwnd = GetDlgItem(hwnd, control.id)

                self.initialize()

                if self.center:
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
                    SetWindowPos(hwnd, 0, center_x, center_y, 0, 0, SWP_NOSIZE)

                return True

        elif msg == WM.CLOSE:
                EndDialog(hwnd, 0)  # this is executed by clicking the X in the upper right corner

        elif msg == WM.COMMAND:
                if wparam in self.registered_commands:
                    self.registered_commands[wparam]()
                    return True

        elif msg == WM.NOTIFY:
                lpnmhdr = ctypes.cast(lparam, LPNMHDR)
                notif_key = (lpnmhdr.contents.code, lpnmhdr.contents.idFrom)
                if notif_key in self.registered_notifications:
                    args = ctypes.cast(lparam, self.registered_notifications[notif_key][1])
                    self.registered_notifications[notif_key][0](args.contents)
                    return True
        return False

    def show(self):
        '''
        This method displays the dialog on the screen and starts its message loop,
        allowing user interaction with the controls. The method blocks until the
        dialog is closed.

        Parameters:
            None.

        Returns:
            None
        '''
        for item in dir(self):
            obj = getattr(self, item)
            if isinstance(obj, Control):
                self.control_list.append(obj)
        self.__create_dialog()

    def terminate(self):
        '''
        This method terminates the dialog and closes its window.

        Parameters:
            None.

        Returns:
            None
        '''
        if self.hwnd:
            EndDialog(self.hwnd, 0)

    def __align_struct(self, tmp):
        '''
        Aligns the template structure to the size of a DWORD.

        Parameters:
            tmp: The template structure to be aligned.

        Returns:
            The aligned template structure.
        '''
        dword_size = ctypes.sizeof(wintypes.DWORD)
        align = dword_size - len(tmp) % dword_size
        if align < dword_size:
            tmp += bytearray(align)
        return tmp

    def __create_dialog(self):
        """
        Create the dialog window and its controls.

        This method constructs the dialog window by creating its controls and setting up event handling.
        It iterates over the control_list, assigns unique IDs to the controls, creates control structures,
        aligns them to match memory requirements, and registers event handlers for commands and notifications.

        Parameters:
            None.

        Returns:
            None.

        Raises:
            TypeError: If a control in control_list is not an instance of Control.

        Notes:
            - This method is called internally during the creation of the Dialog object.
            - It utilizes the __align_struct method to ensure proper memory alignment.
            - The created dialog is displayed using the DialogBoxIndirectParam function.
        """
        controls = bytearray()
        for i, control in enumerate(self.control_list):
            if not isinstance(control, Control):
                raise TypeError(f"{control} is not an instance of Control")
            control.id = self.control_start_id + i
            control_struct = control.create()
            controls += self.__align_struct(control_struct)
            for event, func in control.registered_commands.items():
                # mimicking what MS does internally allows us to directly use wparam in __default_dialog_proc
                self.registered_commands[(event << 16) + control.id] = func

            for event, func in control.registered_notifications.items():
                self.registered_notifications[(event, control.id)] = func


        self.dialog_items = len(self.control_list)
        dlg_window = self.__create_dialog_window()
        dlg_window = self.__align_struct(dlg_window)
        dialog = dlg_window + controls
        # print(' ,'.join(f'0x{x:>02X}' for x in dialog))
        raw_bytes = (ctypes.c_ubyte * len(dialog)).from_buffer_copy(dialog)
        hinstance = GetModuleHandle(None)
        DialogBoxIndirectParam(hinstance,
                               raw_bytes,
                               self.parent,
                               DIALOGPROC(self.__default_dialog_proc),
                               0)


def create_dialog_from_rc(rc_code):
    '''
    Create a dialog object from resource code.

    This function parses the given resource code and creates a `Dialog` object
    along with its associated controls based on the provided code.
    The control types defined in the resource code are mapped to their corresponding control classes.

    Parameters:
        rc_code (str): The resource code defining the dialog and its controls.

    Returns:
        Dialog: A `Dialog` object representing the parsed dialog and its controls.

    Raises:
        NotImplementedError: If a requested control type is not implemented yet.

    Note that currently only resource code generated by ResourceHacker is supported.
    '''
    control_type_map = {
        'button': Button,
        'edit': TextBox,
        'static': Label,
        'combobox': ComboBox,
        'comboboxex32': ComboBoxEx,
        'syslistview32': ListView,
        'listbox': ListBox,
        'msctls_progress32': ProgressBar,
        'msctls_statusbar32': StatusBar,
        'msctls_updown32': UpDown,
    }

    _dialog = parser(rc_code)
    dialog = Dialog(title=_dialog.title,
                    size=_dialog.size,
                    position=_dialog.position,
                    style=_dialog.styles,
                    ex_style=_dialog.ex_styles,
                    pointsize=_dialog.font.pointsize,
                    typeface=_dialog.font.typeface,
                    weight=_dialog.font.weight,
                    italic=_dialog.font.italic,
                    charset=_dialog.font.charset)

    for rc in _dialog.controls:
        base_instance = control_type_map.get(rc.control_class, None)
        if base_instance is None:
            raise NotImplementedError(f'The requested control "{rc.control_class}" is not implemented yet!')
            # console.show()
        _control = type(rc.control_class, (base_instance,), {})
        control_instance = _control(
            title=rc.title,
            size=rc.size,
            position=rc.position,
            style=rc.style,
            ex_style=rc.ex_style,
        )
        control_name =  rc.name if rc.name else f"{rc.control_class}_{rc.id_}"
        setattr(dialog, control_name, control_instance)

    return dialog
