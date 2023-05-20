""" Dialog STATIC control implementation """
from dataclasses import dataclass
from .__control_template import Control

from enum import IntEnum
from ..win_helper import (
    WindowStyle as WS
)

class SS(IntEnum):
    LEFT             = 0x00000000
    CENTER           = 0x00000001
    RIGHT            = 0x00000002
    ICON             = 0x00000003
    BLACKRECT        = 0x00000004
    GRAYRECT         = 0x00000005
    WHITERECT        = 0x00000006
    BLACKFRAME       = 0x00000007
    GRAYFRAME        = 0x00000008
    WHITEFRAME       = 0x00000009
    USERITEM         = 0x0000000A
    SIMPLE           = 0x0000000B
    LEFTNOWORDWRAP   = 0x0000000C
    OWNERDRAW        = 0x0000000D
    BITMAP           = 0x0000000E
    ENHMETAFILE      = 0x0000000F
    ETCHEDHORZ       = 0x00000010
    ETCHEDVERT       = 0x00000011
    ETCHEDFRAME      = 0x00000012
    TYPEMASK         = 0x0000001F
    REALSIZECONTROL  = 0x00000040
    NOPREFIX         = 0x00000080  # Don't do "&" character translation
    NOTIFY           = 0x00000100
    CENTERIMAGE      = 0x00000200
    RIGHTJUST        = 0x00000400
    REALSIZEIMAGE    = 0x00000800
    SUNKEN           = 0x00001000
    EDITCONTROL      = 0x00002000
    ENDELLIPSIS      = 0x00004000
    PATHELLIPSIS     = 0x00008000
    WORDELLIPSIS     = 0x0000C000
    ELLIPSISMASK     = 0x0000C000

@dataclass
class Label(Control):
    """Implementation for a simple label control"""
    style: int = SS.SIMPLE | WS.CHILD | WS.VISIBLE
    window_class: str = 'Static'

@dataclass
class RigthAlignedLabel(Label):
    """ Implementation of a right aligned label control """
    def __post_init__(self):
        self.style = SS.RIGHT | WS.CHILD | WS.VISIBLE

@dataclass
class CenteredLabel(Label):
    """ Implementation of a centered label control """
    def __post_init__(self):
        self.style = SS.CENTER | WS.CHILD | WS.VISIBLE

@dataclass
class TruncatedLabel(Label):
    """ Implementation of a truncated label control """
    def __post_init__(self):
        self.style = SS.LEFT | SS.WORDELLIPSIS | WS.CHILD | WS.VISIBLE

@dataclass
class BlackFramedLabel(Label):
    """ Implementation of a black framed label control """
    def __post_init__(self):
        self.style = SS.LEFT | SS.BLACKFRAME | WS.CHILD | WS.VISIBLE
