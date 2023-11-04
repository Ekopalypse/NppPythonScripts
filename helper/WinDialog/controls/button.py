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
'''

from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    WindowStyle as WS,
    WM_CommandDelegator, SendMessage
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

        isChecked (bool): Indicates if a radio or checkbox button is checked.
            Returns True if the current radio or checkbox button is checked, False otherwise

    Notifications:
        onClick (WM_CommandDelegator): Handler for the BN.CLICKED notification.
        onPaint (WM_CommandDelegator): Handler for the BN.PAINT notification.
        onHilite (WM_CommandDelegator): Handler for the BN.HILITE notification.
        onUnhilite (WM_CommandDelegator): Handler for the BN.UNHILITE notification.
        onDisable (WM_CommandDelegator): Handler for the BN.DISABLE notification.
        onDoubleClicked (WM_CommandDelegator): Handler for the BN.DOUBLECLICKED notification.
        onSetFocus (WM_CommandDelegator): Handler for the BN.SETFOCUS notification.
        onKillFocus (WM_CommandDelegator): Handler for the BN.KILLFOCUS notification.
    '''
    size: (int, int) = (50, 11)
    style: int = Control.style | WS.TABSTOP | BS.CENTER | BS.PUSHLIKE | BS.FLAT
    windowClass: str = 'Button'

    onClick         = WM_CommandDelegator(BN.CLICKED)
    onPaint         = WM_CommandDelegator(BN.PAINT)
    onHilite        = WM_CommandDelegator(BN.HILITE)
    onUnhilite      = WM_CommandDelegator(BN.UNHILITE)
    onDisable       = WM_CommandDelegator(BN.DISABLE)
    onDoubleClicked = WM_CommandDelegator(BN.DOUBLECLICKED)
    onSetFocus      = WM_CommandDelegator(BN.SETFOCUS)
    onKillFocus     = WM_CommandDelegator(BN.KILLFOCUS)

    def getCheckState(self):
        '''
        Gets the checkbox button check state.

        Args:
            None

        Returns:
            BST: The current check value.
        '''
        return BST(SendMessage(self.hwnd, BM.GETCHECK, 0, 0))

    def setCheckState(self, value):
        '''
        Sets the checkbox button check state.

        Args:
            value (BST enum): One of the BST enumeration values

        Returns:
            None
        '''
        SendMessage(self.hwnd, BM.SETCHECK, value, 0)

    @property
    def isChecked(self) -> bool :
        if isinstance(self, CheckBoxButton) or isinstance(self, RadioButton):
            return self.getCheckState() == BST.CHECKED
        else:
            return False

    def setCheck(self, checked: bool = True):
        '''
        Helper function that either sets BST.CHECKED (True) or BST.UNCHECKED (False). (defaults to True).

        Args:
            checked (bool) Indicates whether to check or uncheck radio or checkbox buttons.
                If this parameter is True, the button is checked.
                If the parameter is False, the button is unchecked.

        Returns:
            None
        '''

        self.setCheckState(BST.CHECKED if checked else BST.UNCHECKED)


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
        The DefaultButton class inherits the onClick, onPaint, onHilite, onUnhilite,
        onDisable, onDoubleClicked, onSetFocus, and onKillFocus attributes from the Button class.
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
        The CommandButton class inherits the onClick, onPaint, onHilite, onUnhilite,
        onDisable, onDoubleClicked, onSetFocus, and onKillFocus attributes from the Button class.
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

    Methods:
        setThreeState() -> None:
            Sets the checkbox button control to a three-state mode.

        getCheckState() -> BST:
            Gets the state of the checkbox button control.

        setCheckState():
            Sets the state of the checkbox button control.

    Example Usage:
        from dialog_controls import CheckBoxButton

        # Create a checkbox button control
        checkbox = CheckBoxButton(title="Enable Option", size=(120, 20), position=(10, 10))

        # Set the checkbox to a three-state mode
        checkbox.setThreeState()

    Note:
        The CheckBoxButton class inherits the onClick, onPaint, onHilite, onUnhilite,
        onDisable, onDoubleClicked, onSetFocus, and onKillFocus attributes from the Button class.
    '''
    style: int = Control.style | WS.TABSTOP | BS.AUTOCHECKBOX | BS.FLAT

    def setThreeState(self):
        '''
        Sets the checkbox button control to a three-state mode.

        By default, the checkbox button control is in a two-state mode (checked or unchecked).
        This method modifies the style of the control to enable a three-state mode, allowing
        an indeterminate state in addition to checked and unchecked states.

        Args:
            None.

        Returns:
            None.
        '''
        self.style -= BS.AUTOCHECKBOX
        self.style |=BS.AUTO3STATE


@dataclass
class RadioButton(Button):
    '''
    Represents a radio button control.

    The RadioButton class inherits from the Button class.

    Attributes:
        Inherited Attributes:
            See :class:`Button`

    Methods:
        getCheckState() -> BST:
            Gets the state of the radio button control.

        setCheckState():
            Sets the state of the radio button control.

    Example Usage:
        from dialog_controls import RadioButton

        # Create a radio button control
        radio = RadioButton(title="Enable Option", size=(120, 20), position=(10, 10))

    Note:
        The RadioButton class inherits the onClick, onPaint, onHilite, onUnhilite,
        onDisable, onDoubleClicked, onSetFocus, and onKillFocus attributes from the Button class.
    '''
    style: int = Control.style | WS.TABSTOP | BS.AUTORADIOBUTTON | BS.FLAT


@dataclass
class RadioPushButton(Button):
    '''
    Represents a radio button control with a pushbutton-like appearance.

    The RadioPushButton class inherits from the Button class.

    Attributes:
        Inherited Attributes:
            See :class:`Button`

    Methods:
        getCheckState() -> BST:
            Gets the state of the radio pushbutton control.

        setCheckState():
            Sets the state of the radio pushbutton control.

    Example Usage:
        from dialog_controls import RadioPushButton

        # Create a radio button control with a pushbutton appearance
        radio = RadioPushButton(title="Enable Option", size=(120, 20), position=(10, 10))

    Note:
        The RadioPushButton class inherits the onClick, onPaint, onHilite, onUnhilite,
        onDisable, onDoubleClicked, onSetFocus, and onKillFocus attributes from the Button class.
    '''
    style: int = Control.style | WS.TABSTOP | BS.AUTORADIOBUTTON | BS.FLAT | BS.PUSHLIKE


@dataclass
class SplitButton(Button):
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
        The SplitButton class inherits the onClick, onPaint, onHilite, onUnhilite,
        onDisable, onDoubleClicked, onSetFocus, and onKillFocus attributes from the Button class.
    '''
    style: int = Control.style | WS.TABSTOP | BS.SPLITBUTTON


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
        exStyle (int): The extended style flags for the group box control.
        windowClass (str): The window class name for the group box control.

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
    style: int = Control.style | BS.GROUPBOX | WS.GROUP
    windowClass: str = 'Button'
