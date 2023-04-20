""" Provides the implementation of a dialog control.
    It is not intended to be created/instantiated by user code,
    but rather to serve as a base class for the dialog and its controls such as buttons, labels....
"""
from ctypes import create_unicode_buffer
from ctypes.wintypes import DWORD, WORD, SHORT, BYTE
from .win_helper import (
    WindowStyle as WS, WindowClassStyles as CS,
    ExtendedWindowStyles as WS_EX, DialogBoxStyles as DS,
    ShowWindowCommands as SW,
    ShowWindow, UpdateWindow
)

class Control:
    """ Implementation of a control template structure """
    def __init__(self, name, size, position):
        self._array = bytearray()
        self.helpID = 0
        self.exStyle = 0
        self.style = WS.VISIBLE | WS.CHILD
        self.x = position[0]
        self.y = position[1]
        self.cx = size[0]
        self.cy = size[1]
        self.id = 0
        self.windowClass = ''
        self.title = name
        self.extraCount = 0
        self.hwnd = None
        self.intialize_needed = False

    def create(self):
        """ create the control template structure """
        self._array += DWORD(self.helpID)
        self._array += DWORD(self.exStyle)
        self._array += DWORD(self.style)
        self._array += SHORT(self.x)
        self._array += SHORT(self.y)
        self._array += SHORT(self.cx)
        self._array += SHORT(self.cy)
        self._array += DWORD(self.id)
        self._array += create_unicode_buffer(self.windowClass)
        self._array += create_unicode_buffer(self.title)
        self._array += WORD(self.extraCount)
        return self._array

    def show(self):
        ShowWindow(self.hwnd, SW.NORMAL)

    def hide(self):
        ShowWindow(self.hwnd, SW.HIDE)

    def update(self):
        UpdateWindow(self.hwnd)


class Window:
    """ Implementation of a dialog template structure """
    def __init__(self, name, size, position=(0, 0), resizable=False, itemCount=None):
        self._array = bytearray()
        self.dlgVer = 1
        self.signature = 0xFFFF
        self.helpID = 0
        self.exStyle = WS_EX.TOOLWINDOW

        _style = WS.SYSMENU | CS.HREDRAW | CS.VREDRAW | DS.SETFONT
        if resizable:
            _style |= WS.SIZEBOX
        self.style = _style
        self.cDlgItems = itemCount
        self.x = position[0]
        self.y = position[1]
        self.cx = size[0]
        self.cy = size[1]
        self.menu = 0
        self.windowClass = 0
        self.title = name

    def create(self):
        """ create the window template structure """
        self._array += WORD(self.dlgVer)
        self._array += WORD(self.signature)
        self._array += DWORD(self.helpID)
        self._array += DWORD(self.exStyle)
        self._array += DWORD(self.style)
        self._array += WORD(self.cDlgItems)
        self._array += SHORT(self.x)
        self._array += SHORT(self.y)
        self._array += SHORT(self.cx)
        self._array += SHORT(self.cy)
        self._array += WORD(self.menu)
        if isinstance(self.windowClass, str):
            windowClass = create_unicode_buffer(self.windowClass)
        elif isinstance(self.windowClass, int):
            windowClass = WORD(self.windowClass)
        self._array += windowClass
        self._array += create_unicode_buffer(self.title)
        # currently hard coded
        self._array += WORD(8)                                # pointsize
        self._array += WORD(400)                              # weight
        self._array += BYTE(0)                                # italic
        self._array += BYTE(0x1)                              # charset
        self._array += create_unicode_buffer('MS Shell Dlg')  # typeface

        return self._array