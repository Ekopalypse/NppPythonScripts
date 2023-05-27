""" Dialog SYSTABCONTROL32 control implementation """
from dataclasses import dataclass
from .__control_template import Control

@dataclass
class TabControl(Control):
    style: int = Control.style # | ...  # TCS_TABS | TCS_RAGGEDRIGHT
    windowClass: str = 'SysTabControl32'