""" Dialog RICHEDIT control implementation """
from dataclasses import dataclass
from .__control_template import Control

@dataclass
class RichEdit(Control):
    windowClass: str = 'RICHEDIT'

# richedit20w and richedit50w