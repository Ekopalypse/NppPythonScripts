""" Dialog MSCTLS_HOTKEY32 control implementation """
from dataclasses import dataclass
from .__control_template import Control
from ..win_helper import (
    WindowStyle as WS,
)

@dataclass
class HotKey(Control):
    window_class: str = 'msctls_hotkey32'