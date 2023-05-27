"""
MSCTLS_STATUSBAR32 control implementation

The `StatusBar` class represents a msctls_statusbar32 control that displays text at the bottom of a dialog.

Example:


"""
from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    WM_NotifyDelegator,
    SendMessage, WM_USER, CCM, LPNMHDR
)

import ctypes

class SBARS(IntEnum):
    SIZEGRIP = 0x0100
    TOOLTIPS = 0x0800

class SBT(IntEnum):
    TOOLTIPS = 0x0800  # this is a status bar flag, preference to SBARS_TOOLTIPS
    OWNERDRAW = 0x1000
    NOBORDERS = 0x0100
    POPOUT = 0x0200
    RTLREADING = 0x0400
    NOTABPARSING = 0x0800

class SB(IntEnum):
    SETTEXTA = WM_USER+1
    SETTEXTW = WM_USER+11
    GETTEXTA = WM_USER+2
    GETTEXTW = WM_USER+13
    GETTEXTLENGTHA = WM_USER+3
    GETTEXTLENGTHW = WM_USER+12
    SETPARTS = WM_USER+4
    GETPARTS = WM_USER+6
    GETBORDERS = WM_USER+7
    SETMINHEIGHT = WM_USER+8
    SIMPLE = WM_USER+9
    GETRECT = WM_USER+10
    ISSIMPLE = WM_USER+14
    SETICON = WM_USER+15
    SETTIPTEXTA = WM_USER+16
    SETTIPTEXTW = WM_USER+17
    GETTIPTEXTA = WM_USER+18
    GETTIPTEXTW = WM_USER+19
    GETICON = WM_USER+20
    SETUNICODEFORMAT = CCM.SETUNICODEFORMAT
    GETUNICODEFORMAT = CCM.GETUNICODEFORMAT
    SETBKCOLOR = CCM.SETBKCOLOR  # lParam = bkColor
    SIMPLEID = 0x00ff # refers to the data saved for simple mode

class SBN(IntEnum):
    FIRST = 0xfffffc8f
    SIMPLEMODECHANGE = FIRST - 0

@dataclass
class StatusBar(Control):
    """
    Implementation of a status bar control.

    The `StatusBar` class represents a status bar control that displays status information to the user.
    It provides methods to set the text displayed in the status bar.

    Attributes:
        windowClass (str): The window class name for the status bar control. Default is 'msctls_statusbar32'.

    Notifications:
        on_simplemodechange (WM_NotifyDelegator): Sent when the status bar enters or exits simple mode.

    Methods:
        setText(message: str) -> None:
            Updates the text displayed in the status bar.

    """
    windowClass: str = 'msctls_statusbar32'

    # statusbar notification callbacks
    onSimpleModeChange = WM_NotifyDelegator(SBN.SIMPLEMODECHANGE, LPNMHDR)

    def setText(self, message):
        """
        Set the text displayed in the status bar.

        Args:
            message (str): The text message to be displayed in the status bar.

        Returns:
            None
        """
        msg = ctypes.create_unicode_buffer(message)
        SendMessage(self.hwnd, SB.SETTEXTW, SBT.NOBORDERS, ctypes.addressof(msg))
