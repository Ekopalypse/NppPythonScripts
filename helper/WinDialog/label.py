""" Dialog label control implementation
"""

from enum import IntEnum
from .dialog_template import Control
from .win_helper import (
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


class Label(Control):
    """Implementation for a standard label control"""
    # https://docs.microsoft.com/en-us/windows/desktop/Controls/static-control-styles



    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.windowClass = 'Static'
        self.style = WS.CHILD | WS.VISIBLE
        self.name = name
        self.size = size
        self.position = position


class SimpleLabel(Label):
    """ Implementation of a simple label control """
    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.style = WS.CHILD | WS.VISIBLE | SS.SIMPLE


class RigthAlignedLabel(Label):
    """ Implementation of a right aligned label control """
    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.style = WS.CHILD | WS.VISIBLE | SS.RIGHT


class CenteredLabel(Label):
    """ Implementation of a centered label control """
    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.style = WS.CHILD | WS.VISIBLE | SS.CENTER


class TruncatedLabel(Label):
    """ Implementation of a truncated label control """
    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.style = WS.CHILD | WS.VISIBLE | SS.WORDELLIPSIS


class BlackFramedLabel(Label):
    """ Implementation of a black framed label control """
    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.style = WS.CHILD | WS.VISIBLE | SS.BLACKFRAME
