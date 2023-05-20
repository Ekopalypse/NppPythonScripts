""" Dialog SYSHEADER32 control implementation """
from dataclasses import dataclass
from .__control_template import Control
from ..win_helper import (
    WindowStyle as WS,
)
# SysHeader32, WS_CHILD | WS_VISIBLE, 31, 70, 60, 12
@dataclass
class Header(Control):
    window_class: str = 'SysHeader32'