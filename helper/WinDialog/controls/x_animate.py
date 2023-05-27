""" Dialog SYSANIMATE32 control implementation """
from dataclasses import dataclass
from .__control_template import Control

@dataclass
class Animate(Control):
    windowClass: str = 'SysAnimate32'