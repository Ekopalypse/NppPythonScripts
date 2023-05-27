""" Dialog SYSHEADER32 control implementation """
from dataclasses import dataclass
from .__control_template import Control

@dataclass
class Header(Control):
    windowClass: str = 'SysHeader32'