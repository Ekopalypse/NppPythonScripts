"""
MSCTLS_PROGRESS32 Control Implementations

The `ProgressBar` class represents a msctls_progress32 control that displays the progress of a task or operation.
It allows setting the range, stepping the progress, retrieving the step value, and getting or setting the position
of the progress bar.

Example:
    from WinDialog import ProgressBar

    # Create a progress bar control
    progress_bar = ProgressBar('', (122, 20), (31, 18))

"""
from dataclasses import dataclass
from enum import IntEnum
from typing import Union, Tuple
from .__control_template import Control
from ..win_helper import (
    SendMessage, WM_USER, CCM, LOWORD, HIWORD
)
import ctypes
from ctypes.wintypes import INT

class PBRANGE(ctypes.Structure):
    _fields_ = [('iLow',  INT),
                ('iHigh', INT),
                ]

class PBM(IntEnum):
    SETRANGE = WM_USER + 1
    SETPOS = WM_USER + 2
    DELTAPOS = WM_USER + 3
    SETSTEP = WM_USER + 4
    STEPIT = WM_USER + 5
    SETRANGE32 = WM_USER + 6
    GETRANGE = WM_USER + 7
    GETPOS = WM_USER + 8
    SETBARCOLOR = WM_USER + 9
    SETMARQUEE = WM_USER + 10
    SETBKCOLOR = CCM.SETBKCOLOR
    GETSTEP = WM_USER + 13
    GETBKCOLOR = WM_USER + 14
    GETBARCOLOR = WM_USER + 15
    SETSTATE = WM_USER + 16
    GETSTATE = WM_USER + 17

class PBS(IntEnum):
    SMOOTH = 0x01
    VERTICAL = 0x04
    MARQUEE = 0x08
    SETMARQUEE = WM_USER + 10
    SMOOTHREVERSE = 0x10

class PBST(IntEnum):
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

    Attributes:
        windowClass (str): The window class name for the progress bar control.
        step_value (int): The step value used when stepping the progress bar. Default is 10.

    Methods:
        step() -> None:
            Advance the progress bar by one step.

        getStepValue() -> int:
            Get the current step value.

        setStepValue(value: int) -> None:
            Set the step value of the progress bar.

        getPosition() -> int:
            Get the current position of the progress bar.

        setPosition(value: int) -> None:
            Set the position of the progress bar.

        deltaPos(advance_by_value: int) -> int:
            Advances the current position of a progress bar by a specified increment.

        getRange(value: bool=False, both: bool=False) -> Union[int, Tuple[int, int]]:
            Retrieves information about the current high and low limits of a given progress bar control.

        setRange(min_value: int, max_value: int) -> None:
            Set the range of the progress bar control.

        setRange32(min_val: int, max_val: int) -> int:
            Sets the minimum and maximum values for a progress bar to 32-bit values.

        getBarColor() -> int:
            Gets the background color of the progress bar.

        setBarColor(color: int) -> None:
            Sets the color of the progress indicator bar in the progress bar control.

        setMarquee(turn_on: bool=False, anmiation_time: int=0) -> None:
            Sets the progress bar to marquee mode.

        getBkColor() -> int:
            Gets the background color of the progress bar.

        setBkColor(color: int) -> None:
            Sets the background color in the progress bar.

        getState() -> PBST:
            Gets the state of the progress bar.

        setState(value: PBST) -> PBST:
            Sets the state of the progress bar.
    """

    windowClass: str = 'msctls_progress32'
    step_value:int = 10

    def step(self) -> None:
        """
        Advance the progress bar by one step.

        Args:
            None

        Returns:
            None
        """
        SendMessage(self.hwnd, PBM.STEPIT, 0, 0)

    def getStepValue(self) -> int:
        """
        Get the current step value.

        Args:
            None

        Returns:
            int: The current step value.
        """
        return SendMessage(self.hwnd, PBM.GETSTEP, 0, 0)

    def setStepValue(self, value: int) -> None:
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

    def getPosition(self) -> int:
        """
        Get the current position of the progress bar.

        Args:
            None

        Returns:
            int: The current position of the progress bar.
        """
        return SendMessage(self.hwnd, PBM.GETPOS, 0, 0)

    def setPosition(self, value: int) -> None:
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

    def deltaPos(self, advance_by_value: int) -> int:
        """
        Advances the current position of a progress bar by a specified increment.

        Args:
            advance_by_value (int): The position value to set.

        Returns:
            int: the previous position
        """
        return SendMessage(self.hwnd, PBM.DELTAPOS, advance_by_value, 0)

    def getRange(self, value: bool=False, both: bool=False) -> Union[int, Tuple[int, int]]:
        """
        Retrieves information about the current high and low limits of a given progress bar control.

        Args:
            value (bool): Specifies which limit value is to be used as the return value of the function.
                          - True: Return the low limit.
                          - False: Return the high limit.
                          (default=False)
            both (bool):  Specifies whether both limits should be returned.
                          - True: Return both limits as a tuple of two integers.
                          - False: Return only the specified limit.
                          (default=False)

        Returns:
            int/(int, int): The specified limit(s).
        """
        if both:
            pbrange = PBRANGE()
            SendMessage(self.hwnd, PBM.GETRANGE, value, ctypes.addressof(pbrange))
            return (pbrange.iLow, pbrange.iHigh)
        else:
            return SendMessage(self.hwnd, PBM.GETRANGE, value, 0)

    def setRange(self, min_value: int, max_value: int) -> None:
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

    def setRange32(self, min_val: int, max_val: int) -> Tuple[int, int]:
        """
        Sets the minimum and maximum values for a progress bar to 32-bit values.

        Args:
            min_val (int): The minimum value to set.
            max_val (int): The minimum value to set.

        Returns:
            (int, int): The previous 16-bit low and 16-bit high limits.
                 If the previous ranges were 32-bit values, the return value consists of the LOWORDs of both 32-bit limits.
        """
        ret_val = SendMessage(self.hwnd, PBM.SETRANGE32, min_val, max_val)
        return LOWORD(ret_val), HIWORD(ret_val)

    def getBarColor(self) -> int:
        """
        Gets the background color of the progress bar.

        Args:
            None

        Returns:
            int: The color of the progress bar.
        """
        return SendMessage(self.hwnd, PBM.GETBARCOLOR, 0, 0)

    def setBarColor(self, color: int) -> None:
        """
        Sets the color of the progress indicator bar in the progress bar control.

        Args:
            color (int): The value that specifies the new progress indicator bar color.

        Returns:
            None
        """
        return SendMessage(self.hwnd, PBM.SETBARCOLOR, 0, color)

    def setMarquee(self, turn_on: bool=False, anmiation_time: int=0) -> None:
        """
        Sets the progress bar to marquee mode.

        Args:
            turn_on (bool): Indicates whether to turn the marquee mode on or off.
            anmiation_time (int): Time, in milliseconds, between marquee animation updates.
                                  If this parameter is zero, the marquee animation is updated every 30 milliseconds.
        Returns:
            None
        """
        SendMessage(self.hwnd, PBM.SETMARQUEE, turn_on, anmiation_time)

    def getBkColor(self) -> int:
        """
        Gets the background color of the progress bar.

        Args:
            None

        Returns:
            int: The progress background color.
        """
        return SendMessage(self.hwnd, PBM.GETBKCOLOR, 0, 0)

    def setBkColor(self, color: int) -> None:
        """
        Sets the background color in the progress bar.

        Args:
            color (int): The value that specifies the new progress background color.

        Returns:
            None
        """
        return SendMessage(self.hwnd, PBM.SETBKCOLOR, 0, color)

    def getState(self) -> PBST:
        """
        Gets the state of the progress bar.

        Args:
            None

        Returns:
            PBST: Returns the current state.
        """
        return PBST(SendMessage(self.hwnd, PBM.GETSTATE, 0, 0))

    def setState(self, value: PBST) -> PBST:
        """
        Sets the state of the progress bar.

        Args:
            value (PBST): State of the progress bar that is being set.

        Raises:
            ValueError: If the provided values are not within the valid range.

        Returns:
            PBST: Returns the previous state.
        """
        return PBST(SendMessage(self.hwnd, PBM.SETSTATE, PBST(value).value, 0))
