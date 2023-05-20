""" Dialog MSCTLS_TRACKBAR32 control implementation """
from dataclasses import dataclass
from .__control_template import Control

@dataclass
class TrackBar(Control):
    window_class: str = 'msctls_trackbar32'