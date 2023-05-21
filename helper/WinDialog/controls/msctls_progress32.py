"""
MSCTLS_PROGRESS32 Control Implementations

The `ProgressBar` class represents a msctls_progress32 control that displays the progress of a task or operation.
It allows setting the range, stepping the progress, retrieving the step value, and getting or setting the position
of the progress bar.

Example:


"""
from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    SendMessage, WM_USER, CCM
)
import ctypes
from ctypes.wintypes import INT

class PBRANGE(ctypes.Structure):
    """ implementation of a PBRANGE structure """
    _fields_ = [('iLow',  INT),
                ('iHigh', INT),
                ]

class PBM(IntEnum):
    SETRANGE = WM_USER + 1
    SETPOS = WM_USER + 2
    DELTAPOS = WM_USER + 3
    SETSTEP = WM_USER + 4
    STEPIT = WM_USER + 5
    SETRANGE32 = WM_USER + 6        # lParam = high, wParam = low
    GETRANGE = WM_USER + 7          # wParam = return (TRUE ? low : high). lParam = PPBRANGE or NULL
    GETPOS = WM_USER + 8
    SETBARCOLOR = WM_USER + 9       # lParam = bar color
    SETMARQUEE = WM_USER + 10
    SETBKCOLOR = CCM.SETBKCOLOR     #lParam = bkColor
    GETSTEP = WM_USER + 13
    GETBKCOLOR = WM_USER + 14
    GETBARCOLOR = WM_USER + 15
    SETSTATE = WM_USER + 16         # wParam = PBST_[State] (NORMAL, ERROR, PAUSED)
    GETSTATE = WM_USER + 17

class PBS(IntEnum):
    SMOOTH = 0x01
    VERTICAL = 0x04
    MARQUEE = 0x08
    SETMARQUEE = WM_USER + 10
    SMOOTHREVERSE = 0x10

class PBST(IntEnum):  # used by SetState message as wparam value only
    NORMAL = 0x0001
    ERROR = 0x0002
    PAUSED = 0x0003


@dataclass
class ProgressBar(Control):
    """
    Implementation of a progress bar control.

    This class represents a progress bar control that displays the progress of a task
    or operation. It provides methods for setting the range, stepping the progress,
    retrieving the step value, getting and setting the position of the progress bar.

    Args:
        window_class (str): The window class name for the progress bar control.
        step_value (int): The step value used when stepping the progress bar. Default is 10.

    Methods:
        set_range(min_value: int, max_value: int) -> None:
            Set the range of the progress bar control.

        step() -> None:
            Advance the progress bar by one step.

        get_step_value() -> int:
            Get the current step value.

        set_step_value(value: int) -> None:
            Set the step value of the progress bar.

        get_position() -> int:
            Get the current position of the progress bar.

        set_position(value: int) -> None:
            Set the position of the progress bar.

    Note:
        - The values passed to the progress bar methods should be within the range of 0 to 65535 (0xFFFF).
    """
    window_class: str = 'msctls_progress32'
    step_value:int = 10

    def set_range(self, min_value, max_value):
        """
        Set the range of the progress bar control.

        Args:
            min_value (int): The minimum value of the progress bar range.
            max_value (int): The maximum value of the progress bar range.

        Raises:
            ValueError: If the provided values are not within the valid range.

        Returns:
            None
        """
        if (not (0 <= min_value)) or (not (min_value < max_value <= 0xFFFF)):
            raise ValueError(f'Valid values are in range of 0 to {0xFFFF}')
        SendMessage(self.hwnd, PBM.SETRANGE, 0, ((max_value << 16) & 0xFFFF0000) + (min_value & 0xFFFF))

    def step(self):
        """
        Advance the progress bar by one step.

        Returns:
            None
        """
        SendMessage(self.hwnd, PBM.STEPIT, 0, 0)

    def get_step_value(self):
        """
        Get the current step value.

        Returns:
            int: The current step value.
        """
        return SendMessage(self.hwnd, PBM.GETSTEP, 0, 0)

    def set_step_value(self, value):
        """
        Set the step value of the progress bar.

        Args:
            value (int): The step value to set.

        Raises:
            ValueError: If the provided value is not within the valid range.

        Returns:
            None
        """
        if not (0 <= value <= 0xFFFF):
            raise ValueError(f'Valid values are in range of 0 to {0xFFFF}')
        SendMessage(self.hwnd, PBM.SETSTEP, value, 0)

    def get_position(self):
        """
        Get the current position of the progress bar.

        Returns:
            int: The current position of the progress bar.
        """
        return SendMessage(self.hwnd, PBM.GETPOS, 0, 0)

    def set_position(self, value):
        """
        Set the position of the progress bar.

        Args:
            value (int): The position value to set.

        Raises:
            ValueError: If the provided value is not within the valid range.

        Returns:
            None
        """
        if not (0 <= value <= 0xFFFF):
            raise ValueError(f'Valid values are in range of 0 to {0xFFFF}')
        return SendMessage(self.hwnd, PBM.SETPOS, value, 0)
