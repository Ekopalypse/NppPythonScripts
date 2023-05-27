""" Dialog SYSLINK control implementation """
from dataclasses import dataclass
from .__control_template import Control


@dataclass
class Link(Control):
    windowClass: str = 'SysLink'