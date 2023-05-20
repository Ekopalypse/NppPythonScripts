'''
BUTTON Control Implementations

Provides classes for creating various types of button controls for dialogs.
The button controls include standard buttons, default buttons, command buttons, checkbox buttons, radio buttons, split buttons, and group boxes.

The button controls are implemented as data classes that inherit from the `Control` class defined in the `__control_template` module.
Each button control class includes attributes for configuring the control's appearance, position, and behavior.

Example Usage:
    from WinDialog import Button, DefaultButton

    # Create a standard button control
    button = Button(title="Click Me", size=(80, 25), position=(10, 10))

    # Create a default button control
    default_button = DefaultButton(title="OK", size=(80, 25), position=(10, 50))

For detailed documentation on each button control class, refer to their respective docstrings.

Note: This module requires the `__control_template` module and the `win_helper` module.

'''

from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    WindowStyle as WS,
    WM_CommandDelegator
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


class BN(IntEnum):
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


class BCM(IntEnum):
    FIRST = 0x1600
    GETIDEALSIZE = FIRST + 0x0001
    SETIMAGELIST = FIRST + 0x0002
    GETIMAGELIST = FIRST + 0x0003
    SETTEXTMARGIN = FIRST + 0x0004
    GETTEXTMARGIN = FIRST + 0x0005
    SETDROPDOWNSTATE = FIRST + 0x0006
    SETSPLITINFO = FIRST + 0x0007
    GETSPLITINFO = FIRST + 0x0008
    SETNOTE = FIRST + 0x0009
    GETNOTE = FIRST + 0x000A
    GETNOTELENGTH = FIRST + 0x000B
    SETSHIELD = FIRST + 0x000C


class BM(IntEnum):
    GETCHECK = 0x00F0
    SETCHECK = 0x00F1
    GETSTATE = 0x00F2
    SETSTATE = 0x00F3
    SETSTYLE = 0x00F4
    CLICK = 0x00F5
    GETIMAGE = 0x00F6
    SETIMAGE = 0x00F7
    SETDONTCLICK = 0x00F8


class BST(IntEnum):
    UNCHECKED = 0x0000
    CHECKED = 0x0001
    INDETERMINATE = 0x0002
    PUSHED = 0x0004
    FOCUS = 0x0008


@dataclass
class Button(Control):
    '''
    Represents a standard button control.

    The DefaultButton class inherits from the Control class.

    Attributes:
        Inherited Attributes:
            See :class:`Control`
        on_click (WM_CommandDelegator): Handler for the BN.CLICKED notification.
        on_paint (WM_CommandDelegator): Handler for the BN.PAINT notification.
        on_hilite (WM_CommandDelegator): Handler for the BN.HILITE notification.
        on_unhilite (WM_CommandDelegator): Handler for the BN.UNHILITE notification.
        on_disable (WM_CommandDelegator): Handler for the BN.DISABLE notification.
        on_doubleclicked (WM_CommandDelegator): Handler for the BN.DOUBLECLICKED notification.
        on_setfocus (WM_CommandDelegator): Handler for the BN.SETFOCUS notification.
        on_killfocus (WM_CommandDelegator): Handler for the BN.KILLFOCUS notification.
    '''
    size: (int, int) = (50, 11)
    style: int = Control.style | WS.TABSTOP | BS.CENTER | BS.PUSHLIKE | BS.FLAT
    window_class: str = 'Button'

    # button notification callbacks
    on_click         = WM_CommandDelegator(BN.CLICKED)
    on_paint         = WM_CommandDelegator(BN.PAINT)
    on_hilite        = WM_CommandDelegator(BN.HILITE)
    on_unhilite      = WM_CommandDelegator(BN.UNHILITE)
    on_disable       = WM_CommandDelegator(BN.DISABLE)
    on_doubleclicked = WM_CommandDelegator(BN.DOUBLECLICKED)
    on_setfocus      = WM_CommandDelegator(BN.SETFOCUS)
    on_killfocus     = WM_CommandDelegator(BN.KILLFOCUS)


@dataclass
class DefaultButton(Button):
    style: int = Control.style | WS.TABSTOP | BS.DEFPUSHBUTTON
    '''
    Represents a default button control.

    The DefaultButton class inherits from the Button class.

    Attributes:
        Inherited Attributes:
            See :class:`Button`

    Example Usage:
        from dialog_controls import DefaultButton

        # Create a default button control
        default = DefaultButton(title="Enable Option", size=(120, 20), position=(10, 10))

    Note:
        The DefaultButton class inherits the on_click, on_paint, on_hilite, on_unhilite,
        on_disable, on_doubleclicked, on_setfocus, and on_killfocus attributes from the Button class.
    '''

@dataclass
class CommandButton(Button):
    style: int = Control.style | WS.TABSTOP | BS.COMMANDLINK
    '''
    Represents a command button control.

    The CommandButton class inherits from the Button class.

    Attributes:
        Inherited Attributes:
            See :class:`Button`

    Example Usage:
        from dialog_controls import CommandButton

        # Create a command button control
        command = CommandButton(title="Enable Option", size=(120, 20), position=(10, 10))

    Note:
        The CommandButton class inherits the on_click, on_paint, on_hilite, on_unhilite,
        on_disable, on_doubleclicked, on_setfocus, and on_killfocus attributes from the Button class.
    '''

@dataclass
class CheckBoxButton(Button):
    '''
    Represents a checkbox button control.

    The CheckBoxButton class inherits from the Button class and
    adds a specific method for configuring a checkbox button control.

    Attributes:
        Inherited Attributes:
            See :class:`Button`

    Example Usage:
        from dialog_controls import CheckBoxButton

        # Create a checkbox button control
        checkbox = CheckBoxButton(title="Enable Option", size=(120, 20), position=(10, 10))

        # Set the checkbox to a three-state mode
        checkbox.set_three_state()

    Note:
        The CheckBoxButton class inherits the on_click, on_paint, on_hilite, on_unhilite,
        on_disable, on_doubleclicked, on_setfocus, and on_killfocus attributes from the Button class.
    '''
    style: int = Control.style | WS.TABSTOP | BS.AUTOCHECKBOX | BS.FLAT
    def set_three_state(self):
        '''
        Sets the checkbox button control to a three-state mode.

        By default, the checkbox button control is in a two-state mode (checked or unchecked).
        This method modifies the style of the control to enable a three-state mode, allowing
        an indeterminate state in addition to checked and unchecked states.
        '''
        self.style -= BS.AUTOCHECKBOX
        self.style |=BS.AUTO3STATE


@dataclass
class RadioButton(Button):
    style: int = Control.style | WS.TABSTOP | BS.AUTORADIOBUTTON | BS.FLAT
    '''
    Represents a radio button control.

    The RadioButton class inherits from the Button class.

    Attributes:
        Inherited Attributes:
            See :class:`Button`

    Example Usage:
        from dialog_controls import RadioButton

        # Create a radio button control
        radio = RadioButton(title="Enable Option", size=(120, 20), position=(10, 10))

    Note:
        The RadioButton class inherits the on_click, on_paint, on_hilite, on_unhilite,
        on_disable, on_doubleclicked, on_setfocus, and on_killfocus attributes from the Button class.
    '''

@dataclass
class SplitButton(Button):
    style: int = Control.style | WS.TABSTOP | BS.SPLITBUTTON
    '''
    Represents a split button control.

    The SplitButton class inherits from the Button class.

    Attributes:
        Inherited Attributes:
            See :class:`Button`

    Example Usage:
        from dialog_controls import SplitButton

        # Create a split button control
        split = SplitButton(title="Enable Option", size=(120, 20), position=(10, 10))

    Note:
        The SplitButton class inherits the on_click, on_paint, on_hilite, on_unhilite,
        on_disable, on_doubleclicked, on_setfocus, and on_killfocus attributes from the Button class.
    '''

# GroupBox does not inherit from Button as it is not clickable
@dataclass
class GroupBox(Control):
    '''
    Represents a group box control.

    The GroupBox class inherits from the Control class and NOT from the Button base class.

    Attributes:
        title (str): The title or label displayed on the group box.
        size (tuple[int, int]): The width and height of the group box control.
        position (tuple[int, int]): The x and y coordinates of the group box control.
        style (int): The style flags for the group box control.
        ex_style (int): The extended style flags for the group box control.
        window_class (str): The window class name for the group box control.

    Example Usage:
        from WinDialog import GroupBox, RadioButton

        # Create a group box control
        group_box = GroupBox(title="Options", size=(180, 120), position=(10, 10))

        # Create buttons inside the group box
        button1 = RadioButton(title="Button 1", size=(80, 25), position=(20, 40))
        button2 = RadioButton(title="Button 2", size=(80, 25), position=(20, 80))

    Note:
        The GroupBox class does not inherit any event handler attributes from the Control class
        as it is not a clickable control. It is used as a container for grouping related controls.
    '''
    # title: str = ''
    # size: (int, int) = (50, 11)
    # position: (int, int) = (0, 0)
    style: int = Control.style | BS.GROUPBOX | WS.GROUP
    # ex_style: int = 0
    window_class: str = 'Button'
