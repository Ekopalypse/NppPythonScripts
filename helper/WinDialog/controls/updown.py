"""
UPDOWN control implementation

The `UpDown` class represents a msctls_updown32 control.

The UpDown controls is implemented as data class that inherit from the `Control` class defined in the `__control_template` module.
The class includes attributes for configuring the control's appearance, position, and behavior.

Example:
    from WinDialog import UpDown

    # Create a updown control
    up_down = UpDown('', (10, 14), (19, 18))

"""
from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    WM_NotifyDelegator,
    SendMessage, WM_USER, CCM, NMHDR
)
import ctypes
from ctypes.wintypes import (
	UINT, INT, BOOL
)

UD_MAXVAL = 0x7fff
UD_MINVAL = -UD_MAXVAL

class UDACCEL(ctypes.Structure):
    """ implementation of a UDACCEL structure """
    _fields_ = [('nSec', UINT),
                ('nInc', UINT),
                ]

class NMUPDOWN(ctypes.Structure):
    """ implementation of a NMUPDOWN structure """
    _fields_ = [('hdr', NMHDR),
                ('iPos', INT),
                ('iDelta', INT),
                ]
PNMUPDOWN = ctypes.POINTER(NMUPDOWN)

class UDS(IntEnum):
    WRAP = 0x0001
    SETBUDDYINT = 0x0002
    ALIGNRIGHT = 0x0004
    ALIGNLEFT = 0x0008
    AUTOBUDDY = 0x0010
    ARROWKEYS = 0x0020
    HORZ = 0x0040
    NOTHOUSANDS = 0x0080
    HOTTRACK = 0x0100


class UDM(IntEnum):
    SETRANGE = WM_USER + 101
    GETRANGE = WM_USER + 102
    SETPOS = WM_USER + 103
    GETPOS = WM_USER + 104
    SETBUDDY = WM_USER + 105
    GETBUDDY = WM_USER + 106
    SETACCEL = WM_USER + 107
    GETACCEL = WM_USER + 108
    SETBASE = WM_USER + 109
    GETBASE = WM_USER + 110
    SETRANGE32 = WM_USER + 111
    GETRANGE32 = WM_USER + 112 # wParam & lParam are LPINT
    SETUNICODEFORMAT = CCM.SETUNICODEFORMAT
    GETUNICODEFORMAT = CCM.GETUNICODEFORMAT
    SETPOS32 = WM_USER + 113
    GETPOS32 = WM_USER + 114


class UDN(IntEnum):
    FIRST = 0xFFFFFD2E
    DELTAPOS = FIRST

@dataclass
class UpDown(Control):
    """
    Implementation of an up-down control.

    The UpDown class represents an up-down control, which is typically used to increment or decrement a value.
    It provides methods to set the range of values, get and set the current value, and handles up-down control notifications.

    Attributes:
        windowClass (str): The window class of the up-down control.
        nmupdown (NMUPDOWN): An instance of the NMUPDOWN structure for handling up-down control notifications.

    updown notification callbacks:
        on_deltapos (WM_NotifyDelegator): Sent when the user changes the position of the up-down control.

    Methods:
        setRange(min_value: int, max_value: int) -> None:
            Set the range of the up-down control.
        getValue() -> int:
            Get the current value of the up-down control.
        setValue(value: int) -> None:
            Set the value of the up-down control.

    Note:
        The valid range for the min_value and max_value parameters in the set_range method is between UD_MINVAL and UD_MAXVAL.
    """

    windowClass: str = 'msctls_updown32'
    nmupdown: NMUPDOWN = NMUPDOWN()
    # updown notification callbacks
    onDeltaPos = WM_NotifyDelegator(UDN.DELTAPOS, PNMUPDOWN)

    def setRange(self, min_value, max_value):
        """
        Set the range of the up-down control.

        Args:
            min_value (int): The minimum value of the range.
            max_value (int): The maximum value of the range.

        Raises:
            ValueError: If the provided values are not within the valid range.

        Note:
            The valid range for min_value and max_value is between UD_MINVAL(-0x7fff) and UD_MAXVAL(0x7fff).

        """
        if (not (UD_MINVAL <= min_value <= UD_MAXVAL)) or (not (UD_MINVAL <= max_value <= UD_MAXVAL)):
            raise ValueError(f'Valid values are in range of {UD_MINVAL} to {UD_MAXVAL}')
        SendMessage(self.hwnd, UDM.SETRANGE, 0, ((min_value << 16) & 0xFFFF0000) + (max_value & 0xFFFF))

    def getValue(self):
        """
        Get the current value of the up-down control.

        Returns:
            int: The current value of the up-down control, or None if no value is set.

        """
        ret_val = BOOL(0)
        res = SendMessage(self.hwnd, UDM.GETPOS32, 0, ctypes.addressof(ret_val))
        if not ret_val:
            return None
        return res

    def setValue(self, value):
        """
        Set the value of the up-down control.

        Args:
            value (int): The value to set.

        """
        SendMessage(self.hwnd, UDM.SETPOS32, 0, value)