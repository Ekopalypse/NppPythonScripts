""" Dialog REBARWINDOW32 control implementation """
from dataclasses import dataclass
from .__control_template import Control


@dataclass
class ReBarWindow(Control):
    window_class: str = 'ReBarWindow32'