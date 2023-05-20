""" Dialog SCROLLBAR control implementation """
from dataclasses import dataclass
from .__control_template import Control
from ..win_helper import WindowStyle as WS

@dataclass
class ScrollBar(Control):
    window_class: str = 'SCROLLBAR'