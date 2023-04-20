""" Dialog button control implementation
"""

from enum import IntEnum
from .dialog_template import Control
from .win_helper import (
    HIWORD,
    WindowStyle as WS
)

class BS(IntEnum):
    PUSHBUTTON = 0
    SOLID = 0
    TEXT = 0
    DEFPUSHBUTTON = 1
    HOLLOW = 1
    NULL = 1
    CHECKBOX = 2
    HATCHED = 2
    AUTOCHECKBOX = 3
    PATTERN = 3
    RADIOBUTTON = 4
    INDEXED = 4
    THREE_STATE = 5
    DIBPATTERN = 5
    AUTO3STATE = 6
    DIBPATTERNPT = 6
    GROUPBOX = 7
    PATTERN8X8 = 7
    USERBUTTON = 8
    DIBPATTERN8X8 = 8
    AUTORADIOBUTTON = 9
    OWNERDRAW = 11
    SPLITBUTTON = 12
    DEFSPLITBUTTON = 13
    COMMANDLINK = 14
    RIGHTBUTTON = 32
    LEFTTEXT = 32
    ICON = 64
    BITMAP = 128
    LEFT = 256
    RIGHT = 512
    CENTER = 768
    TOP = 1024
    BOTTOM = 2048
    VCENTER = 3072
    PUSHLIKE = 4096
    MULTILINE = 8192
    NOTIFY = 16384
    FLAT = 32768

class BN:
    CLICKED = 0
    PAINT = 1
    HILITE = 2
    UNHILITE = 3
    DISABLE = 4
    DOUBLECLICKED = 5
    # PUSHED = HILITE
    # UNPUSHED = UNHILITE
    # DBLCLK = DOUBLECLICKED
    SETFOCUS = 6
    KILLFOCUS = 7

class Button(Control):
    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.style = WS.CHILD | WS.VISIBLE | BS.CENTER | BS.PUSHLIKE | BS.FLAT

        self.windowClass = 'Button'
        self.name = name
        self.size = size
        self.position = position
        self.on_click = lambda: None

    def set_default(self):
        self.style |= BS.DEFPUSHBUTTON

    def callback(self, wparam, lparam):
        match HIWORD(wparam):
            case BN.CLICKED:
                self.on_click()
            case BN.PAINT:
                pass
            case BN.HILITE:
                pass
            case BN.UNHILITE:
                pass
            case BN.DISABLE:
                pass
            case BN.DOUBLECLICKED:
                pass
            case BN.SETFOCUS:
                pass
            case BN.KILLFOCUS:
                pass
            case _:
                return

class CommandButton(Button):
    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.style = WS.VISIBLE | WS.CHILD | BS.COMMANDLINK

class CheckBoxButton(Button):
    def __init__(self, name=None, size=None, position=None, three_state=False):
        super().__init__(name, size, position)
        self.style = WS.VISIBLE | WS.CHILD | BS.AUTOCHECKBOX | BS.FLAT
        if three_state:
            self.style -= BS.AUTOCHECKBOX
            self.style |=BS.AUTO3STATE


class RadioButton(Button):
    def __init__(self, name=None, size=None, position=None, group=False):
        super().__init__(name, size, position)
        self.style = WS.VISIBLE | WS.CHILD | BS.AUTORADIOBUTTON | BS.FLAT
        if group:
            self.style |= WS.GROUP

class SplitButton(Button):
    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.style = WS.VISIBLE | WS.CHILD | BS.SPLITBUTTON

# GroupBox does not inherit from Button as it is not clickable
class GroupBox(Control):
    def __init__(self, name=None, size=None, position=None):
        super().__init__(name, size, position)
        self.style = WS.VISIBLE | WS.CHILD | BS.GROUPBOX
        self.windowClass = 'Button'
        self.name = name
        self.size = size
        self.position = position