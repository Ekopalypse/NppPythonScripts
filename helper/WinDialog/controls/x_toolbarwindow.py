""" Dialog TOOLBARWINDOW32 control implementation """
from dataclasses import dataclass
from .__control_template import Control

@dataclass
class ToolBar(Control):
    windowClass: str = 'ToolbarWindow32'