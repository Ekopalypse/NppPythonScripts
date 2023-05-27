""" Dialog MSCTLS_HOTKEY32 control implementation """
from dataclasses import dataclass
from .__control_template import Control

@dataclass
class HotKey(Control):
    windowClass: str = 'msctls_hotkey32'