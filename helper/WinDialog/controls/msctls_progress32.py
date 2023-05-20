""" Dialog MSCTLS_PROGRESS32 control implementation """
from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    WindowStyle as WS,
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
    window_class: str = 'msctls_progress32'
    step_value:int = 10

    def set_range(self, min_value, max_value):
        if (not (0 <= min_value)) or (not (min_value < max_value <= 0xFFFF)):
            raise ValueError(f'Valid values are in range of 0 to {0xFFFF}')
        SendMessage(self.hwnd, PBM.SETRANGE, 0, ((max_value << 16) & 0xFFFF0000) + (min_value & 0xFFFF))

    def step(self):
        SendMessage(self.hwnd, PBM.STEPIT, 0, 0)

    def get_step_value(self):
        return SendMessage(self.hwnd, PBM.GETSTEP, 0, 0)

    def set_step_value(self, value):
        if not (0 <= value <= 0xFFFF):
            raise ValueError(f'Valid values are in range of 0 to {0xFFFF}')
        SendMessage(self.hwnd, PBM.SETSTEP, value, 0)

    def get_position(self):
        return SendMessage(self.hwnd, PBM.GETPOS, 0, 0)

    def set_position(self, value):
        if not (0 <= value <= 0xFFFF):
            raise ValueError(f'Valid values are in range of 0 to {0xFFFF}')
        return SendMessage(self.hwnd, PBM.SETPOS, value, 0)
