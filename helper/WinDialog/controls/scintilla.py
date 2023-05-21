'''
SCINTILLA Control Implementations

Example Usage:

For detailed documentation, refer to their respective docstrings.
'''

from dataclasses import dataclass
from .__control_template import Control

@dataclass
class Scintilla(Control):
    window_class: str = 'Scintilla'
