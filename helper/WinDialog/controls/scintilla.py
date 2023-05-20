""" Dialog RICHEDIT control implementation """
from dataclasses import dataclass
from .__control_template import Control

@dataclass
class Scintilla(Control):
    window_class: str = 'Scintilla'
