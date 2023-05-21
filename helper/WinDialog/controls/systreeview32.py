'''
SYSTREEVIEW32 Control Implementations

Example Usage:

For detailed documentation, refer to their respective docstrings.
'''
from dataclasses import dataclass
from .__control_template import Control
from ..win_helper import WindowStyle as WS

@dataclass
class TreeView(Control):
    style: int = Control.style | WS.BORDER
    window_class: str = 'SysTreeView32'