'''
SCINTILLA Control Implementations

Example Usage:
    from WinDialog import Scintilla

    # Create a scintilla control

For detailed documentation, refer to their respective docstrings.
'''

from dataclasses import dataclass
from .__control_template import Control

@dataclass
class Scintilla(Control):
    windowClass: str = 'Scintilla'
