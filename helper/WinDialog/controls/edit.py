"""
EDIT Control Implementations

Provides a class for creating a edit control for dialogs.

The edit control is implemented as data class that inherit from the `Control` class defined in the `__control_template` module.
It includes attributes for configuring the control's appearance, position, and behavior.

Example Usage:


For detailed documentation, refer to the respective docstrings.
"""
from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    WindowStyle as WS,
    WM_CommandDelegator,
    SetWindowText, GetWindowTextLength, GetWindowText, SetFocus
)
import ctypes

class ES(IntEnum):
    LEFT        = 0x0000
    CENTER      = 0x0001
    RIGHT       = 0x0002
    MULTILINE   = 0x0004
    UPPERCASE   = 0x0008
    LOWERCASE   = 0x0010
    PASSWORD    = 0x0020
    AUTOVSCROLL = 0x0040
    AUTOHSCROLL = 0x0080
    NOHIDESEL   = 0x0100
    OEMCONVERT  = 0x0400
    READONLY    = 0x0800
    WANTRETURN  = 0x1000
    NUMBER      = 0x2000

class EM(IntEnum):
    GETSEL              = 0x00B0
    SETSEL              = 0x00B1
    GETRECT             = 0x00B2
    SETRECT             = 0x00B3
    SETRECTNP           = 0x00B4
    SCROLL              = 0x00B5
    LINESCROLL          = 0x00B6
    SCROLLCARET         = 0x00B7
    GETMODIFY           = 0x00B8
    SETMODIFY           = 0x00B9
    GETLINECOUNT        = 0x00BA
    LINEINDEX           = 0x00BB
    SETHANDLE           = 0x00BC
    GETHANDLE           = 0x00BD
    GETTHUMB            = 0x00BE
    LINELENGTH          = 0x00C1
    REPLACESEL          = 0x00C2
    GETLINE             = 0x00C4
    LIMITTEXT           = 0x00C5
    CANUNDO             = 0x00C6
    UNDO                = 0x00C7
    FMTLINES            = 0x00C8
    LINEFROMCHAR        = 0x00C9
    SETTABSTOPS         = 0x00CB
    SETPASSWORDCHAR     = 0x00CC
    EMPTYUNDOBUFFER     = 0x00CD
    GETFIRSTVISIBLELINE = 0x00CE
    SETREADONLY         = 0x00CF
    SETWORDBREAKPROC    = 0x00D0
    GETWORDBREAKPROC    = 0x00D1
    GETPASSWORDCHAR     = 0x00D2
    SETMARGINS          = 0x00D3
    GETMARGINS          = 0x00D4
    SETLIMITTEXT        = LIMITTEXT
    GETLIMITTEXT        = 0x00D5
    POSFROMCHAR         = 0x00D6
    CHARFROMPOS         = 0x00D7
    SETIMESTATUS        = 0x00D8
    GETIMESTATUS        = 0x00D9
    ENABLEFEATURE       = 0x00DA

class EN(IntEnum):
    SETFOCUS     = 0x0100
    KILLFOCUS    = 0x0200
    CHANGE       = 0x0300
    UPDATE       = 0x0400
    ERRSPACE     = 0x0500
    MAXTEXT      = 0x0501
    HSCROLL      = 0x0601
    VSCROLL      = 0x0602
    ALIGN_LTR_EC = 0x0700
    ALIGN_RTL_EC = 0x0701
    BEFORE_PASTE = 0x0800
    AFTER_PASTE  = 0x0801

@dataclass
class TextBox(Control):
    """
    Represents an edit control.

    Args:
        style (int): The style of the text box control. Defaults to a combination of styles that include
                     child, visible, border, tab stop, left alignment, multiline, and want return.
        window_class (str): The window class name of the text box control. Defaults to 'Edit'.

    Attributes:
        hwnd (int): The handle of the text box control.

    Notifications:
        The following notification callbacks can be assigned to handle specific events:
        - on_setfocus: Sent when the text box control receives the keyboard focus.
        - on_killfocus: Sent when the text box control loses the keyboard focus.
        - on_change: Sent when the user has taken an action that may have altered the text in the text box control.
        - on_update: Sent when the text box control is about to redraw itself.
        - on_errspace: Sent when the text box control cannot allocate enough memory to meet a specific request.
        - on_maxtext: Sent when the current text insertion has exceeded the specified maximum number of characters.
        - on_hscroll: Sent when the user clicks the horizontal scroll bar of the text box control.
        - on_vscroll: Sent when the user clicks the vertical scroll bar of the text box control.
        - on_align_ltr_ec: Sent when the user has changed the text box control direction to left-to-right.
        - on_align_rtl_ec: Sent when the user has changed the text box control direction to right-to-left.

    Methods:
        set_text(text: str) -> None:
            Sets the text of the text box control.

        get_text() -> str:
            Retrieves the text from the text box control.

        grab_focus() -> None:
            Sets the keyboard focus to the text box control.
    """
    style: int = WS.CHILD | WS.VISIBLE | WS.BORDER | WS.TABSTOP | ES.LEFT | ES.MULTILINE | ES.WANTRETURN
    window_class: str = 'Edit'

    # edit notification callbacks
    on_setfocus = WM_CommandDelegator(EN.SETFOCUS)          # Sent when an edit control receives the keyboard focus.
    on_killfocus = WM_CommandDelegator(EN.KILLFOCUS)        # Sent when an edit control loses the keyboard focus.
    on_change = WM_CommandDelegator(EN.CHANGE)              # Sent when the user has taken an action that may have altered text in an edit control.
    on_update = WM_CommandDelegator(EN.UPDATE)              # Sent when an edit control is about to redraw itself
    on_errspace = WM_CommandDelegator(EN.ERRSPACE)          # Sent when an edit control cannot allocate enough memory to meet a specific request.
    on_maxtext = WM_CommandDelegator(EN.MAXTEXT)            # Sent when the current text insertion has exceeded
    on_hscroll = WM_CommandDelegator(EN.HSCROLL)            # Sent when the user clicks an edit control's horizontal scroll bar.
    on_vscroll = WM_CommandDelegator(EN.VSCROLL)            # Sent when the user clicks an edit control's vertical  scroll bar.
    on_align_ltr_ec = WM_CommandDelegator(EN.ALIGN_LTR_EC)  # Sent when the user has changed the edit control direction to left-to-right.
    on_align_rtl_ec = WM_CommandDelegator(EN.ALIGN_RTL_EC)  # Sent when the user has changed the edit control direction to right-to-left.

    # These notifications are not mentioned in "https://learn.microsoft.com/en-us/windows/win32/controls/bumper-edit-control-reference-notifications".

    # on_before_paste = WM_CommandDelegator(EN.BEFORE_PASTE)  #
    # on_after_paste = WM_CommandDelegator(EN.AFTER_PASTE)    #

    def set_text(self, text):
        """
        Sets the text of the text box control.

        Args:
            text (str): The text to be set in the text box control.

        Returns:
            None
        """
        SetWindowText(self.hwnd, text)

    def get_text(self):
        """
        Retrieves the text from the text box control.

        Returns:
            str: The text contained in the text box control.
        """
        length = GetWindowTextLength(self.hwnd) + 1
        buffer = ctypes.create_unicode_buffer(length)
        GetWindowText(self.hwnd, buffer, length)
        return buffer.value

    def grab_focus(self):
        """
        Sets the keyboard focus to the text box control.

        Returns:
            None
        """
        SetFocus(self.hwnd)