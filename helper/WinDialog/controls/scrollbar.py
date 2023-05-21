""" Dialog SCROLLBAR control implementation """
from dataclasses import dataclass
from .__control_template import Control

@dataclass
class ScrollBar(Control):
    window_class: str = 'SCROLLBAR'