"""
COMBOBOX Control Implementations

This module provides the `ComboBox` class, which is an implementation of a combobox control
and `ComboBoxEx` class, which is an implementation of a comboboxex control

The combobox controls are implemented as data classes that inherit from the `Control` class defined in the `__control_template` module.
Each combobox control class includes attributes for configuring the control's appearance, position, and behavior.

Example Usage:
    from WinDialog import ComboBox

    # Create a combo box control
    combo_box = ComboBox('', (80,100), (10,60))
    combo_box_ex = ComboBoxEx('', (80,100), (10,60))

For detailed documentation on each combobox control class, refer to their respective docstrings.
"""
from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    WindowStyle as WS,
    WM_CommandDelegator, WM_NotifyDelegator,
    CCM,
    SendMessage, NMHDR, WM_USER, INT_PTR, LPNMHDR
)
import ctypes
from ctypes.wintypes import (
    UINT, LPARAM, INT, BOOL, WCHAR, LPWSTR
)

class CBS(IntEnum):
    SIMPLE = 1
    DROPDOWN = 2
    DROPDOWNLIST = 3
    OWNERDRAWFIXED = 16
    OWNERDRAWVARIABLE = 32
    AUTOHSCROLL = 64
    OEMCONVERT = 128
    SORT = 256
    HASSTRINGS = 512
    NOINTEGRALHEIGHT = 1024
    DISABLENOSCROLL = 2048
    UPPERCASE = 8192
    LOWERCASE = 16384

class CB(IntEnum):
    OKAY = 0
    GETEDITSEL = 320
    LIMITTEXT = 321
    SETEDITSEL = 322
    ADDSTRING = 323
    DELETESTRING = 324
    DIR = 325
    GETCOUNT = 326
    GETCURSEL = 327
    GETLBTEXT = 328
    GETLBTEXTLEN = 329
    INSERTSTRING = 330
    RESETCONTENT = 331
    FINDSTRING = 332
    SELECTSTRING = 333
    SETCURSEL = 334
    SHOWDROPDOWN = 335
    GETITEMDATA = 336
    SETITEMDATA = 337
    GETDROPPEDCONTROLRECT = 338
    SETITEMHEIGHT = 339
    GETITEMHEIGHT = 340
    SETEXTENDEDUI = 341
    GETEXTENDEDUI = 342
    GETDROPPEDSTATE = 343
    FINDSTRINGEXACT = 344
    SETLOCALE = 345
    GETLOCALE = 346
    GETTOPINDEX = 347
    SETTOPINDEX = 348
    GETHORIZONTALEXTENT = 349
    SETHORIZONTALEXTENT = 350
    GETDROPPEDWIDTH = 351
    SETDROPPEDWIDTH = 352
    INITSTORAGE = 353
    MSGMAX = 354
    ERR = -1
    ERRSPACE = -2

class CBN(IntEnum):
    SELCHANGE = 1
    DBLCLK = 2
    SETFOCUS = 3
    KILLFOCUS = 4
    EDITCHANGE = 5
    EDITUPDATE = 6
    DROPDOWN = 7
    CLOSEUP = 8
    SELENDOK = 9
    SELENDCANCEL = 10


@dataclass
class ComboBox(Control):
    """
    A class representing a combobox control.

    Combobox is a control that combines the functionality of a text box and a drop-down list.
    It allows users to select an item from a predefined list or enter a custom value.

    Attributes:
        style (int): The style of the combobox control.
        windowClass (str): The window class associated with the combobox control.
        __items (list): The list of items to be displayed in the combobox.

    Combobox Notification Callbacks:
        - onSelChange: Triggered when the selection in the combobox changes.
        - onDblClk: Triggered when the user double-clicks an item in the combobox.
        - onSetFocus: Triggered when the combobox receives focus.
        - onKillFocus: Triggered when the combobox loses focus.
        - onEditChange: Triggered when the user changes the text in the combobox's edit control.
        - onEditUpdate: Triggered when the combobox's edit control is about to display altered text.
        - onDropDown: Triggered when the combobox's dropdown list is about to be displayed.
        - onCloseUp: Triggered when the combobox's dropdown list is about to be closed.
        - onSelEndOk: Triggered when the user selects an item and closes the combobox's dropdown list.
        - onSelEndCancel: Triggered when the user cancels the selection and closes the combobox's dropdown list.

    Methods:
        getSelectedItem() -> int:
            Get the index of the currently selected item in the combobox.

        getSelectedItemText() -> str:
            This method retrieves the text of the selected item in a combo box.

        clear() -> None:
            Clear the combobox by removing all items.

        set(new_list_of_items: List[str]) -> None:
            Update the combobox by replacing the current list of items with a new list.

        append(list_of_items: List[str]) -> None:
            Insert items from the 'items' attribute into the combobox.

    """
    style: int = WS.CHILD | WS.VISIBLE | CBS.HASSTRINGS | CBS.DROPDOWNLIST
    windowClass: str = 'Combobox'
    __items: list = None

    def __post_init__(self):
        """
        Perform post-initialization tasks for the ComboBox object.

        This method is automatically called after the initialization of the ComboBox object.
        It ensures that the '__items' attribute is initialized properly.

        Args:
            None.

        Returns:
            None.
        """
        if self.__items is None:
            self.__items = []

    # combobox notification callbacks
    onSelChange    = WM_CommandDelegator(CBN.SELCHANGE)
    onDblClk       = WM_CommandDelegator(CBN.DBLCLK)
    onSetFocus     = WM_CommandDelegator(CBN.SETFOCUS)
    onKillFocus    = WM_CommandDelegator(CBN.KILLFOCUS)
    onEditChange   = WM_CommandDelegator(CBN.EDITCHANGE)
    onEditUpdate   = WM_CommandDelegator(CBN.EDITUPDATE)
    onDropDown     = WM_CommandDelegator(CBN.DROPDOWN)
    onCloseUp      = WM_CommandDelegator(CBN.CLOSEUP)
    onSelEndOk     = WM_CommandDelegator(CBN.SELENDOK)
    onSelEndCancel = WM_CommandDelegator(CBN.SELENDCANCEL)

    def getSelectedItem(self):
        """
        Get the index of the currently selected item in the combobox.

        Returns:
            int: The index of the selected item.
        """
        return SendMessage(self.hwnd, CB.GETCURSEL, 0, 0)

    def getSelectedItemText(self):
        """
        Get the text of the currently selected item in the combobox.

        Returns:
            str: The text of the selected item.
        """
        index = SendMessage(self.hwnd, CB.GETCURSEL, 0, 0)
        return self.__items[index].value

    def clear(self):
        """
        Clear the combobox by removing all items.

        Returns:
            None.
        """
        self.__items.clear()
        SendMessage(self.hwnd, CB.RESETCONTENT, 0, 0)

    def set(self, new_list_of_items):
        """
        Update the combobox by replacing the current list of items with a new list.

        Args:
            new_list_of_items (list): The new list of items to be displayed in the combobox.

        Returns:
            None.
        """
        self.clear()
        self.append(new_list_of_items)

    def append(self, list_of_items):
        """
        Append new items to the combobox.

        Returns:
            None.
        """
        try:
            for item in list_of_items:
                self.__items.append(ctypes.create_unicode_buffer(item))
                lp_item = ctypes.addressof(self.__items[-1])
                SendMessage(self.hwnd, CB.ADDSTRING, 0, lp_item)
            SendMessage(self.hwnd, CB.SETCURSEL, 0, 0)
        except Exception as e:
            print(f'append Exceptions:{e}')

# ComboBoxEx

class CBEIF(IntEnum):
    TEXT          = 0x00000001
    IMAGE         = 0x00000002
    SELECTEDIMAGE = 0x00000004
    OVERLAY       = 0x00000008
    INDENT        = 0x00000010
    LPARAM        = 0x00000020
    DI_SETITEM    = 0x10000000

class COMBOBOXEXITEM(ctypes.Structure):
    _fields_ = [
        ("mask", UINT),
        ("iItem", INT_PTR),
        ("pszText", LPWSTR),
        ("cchTextMax", INT),
        ("iImage", INT),
        ("iSelectedImage", INT),
        ("iOverlay", INT),
        ("iIndent", INT),
        ("lParam", LPARAM),
    ]

class CBEM(IntEnum):
    SETIMAGELIST     = WM_USER + 2
    GETIMAGELIST     = WM_USER + 3
    DELETEITEM       = CB.DELETESTRING
    GETCOMBOCONTROL  = WM_USER + 6
    GETEDITCONTROL   = WM_USER + 7
    SETEXSTYLE       = WM_USER + 8  # use  SETEXTENDEDSTYLE instead
    SETEXTENDEDSTYLE = WM_USER + 14   # lparam == new style, wParam (optional) == mask
    GETEXSTYLE       = WM_USER + 9 # use GETEXTENDEDSTYLE instead
    GETEXTENDEDSTYLE = WM_USER + 9
    SETUNICODEFORMAT = CCM.SETUNICODEFORMAT
    GETUNICODEFORMAT = CCM.GETUNICODEFORMAT
    HASEDITCHANGED   = WM_USER + 10
    INSERTITEM       = WM_USER + 11
    SETITEM          = WM_USER + 12
    GETITEM          = WM_USER + 13
    SETWINDOWTHEME   = CCM.SETWINDOWTHEME

class CBES_EX(IntEnum):
    NOEDITIMAGE       = 0x00000001
    NOEDITIMAGEINDENT = 0x00000002
    PATHWORDBREAKPROC = 0x00000004
    NOSIZELIMIT       = 0x00000008
    CASESENSITIVE     = 0x00000010
    TEXTENDELLIPSIS   = 0x00000020

class NMCOMBOBOXEX(ctypes.Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("ceItem", COMBOBOXEXITEM),
    ]
PNMCOMBOBOXEX = ctypes.POINTER(NMCOMBOBOXEX)

CBEMAXSTRLEN = 260

# CBEN_DRAGBEGIN sends this information ...
class NMCBEDRAGBEGIN(ctypes.Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("iItemid", INT),
        ("szText", (WCHAR * CBEMAXSTRLEN)),
    ]
PNMCBEDRAGBEGIN = ctypes.POINTER(NMCBEDRAGBEGIN)

# CBEN_ENDEDIT sends this information...
# fChanged if the user actually did anything
# iNewSelection gives what would be the new selection unless the notify is failed
#                      iNewSelection may be CB_ERR if there's no match
class NMCBEENDEDIT(ctypes.Structure):
    _fields_ = [
        ("hdr", NMHDR),
        ("fChanged", BOOL),
        ("iNewSelection", INT),
        ("szText", (WCHAR * CBEMAXSTRLEN)),
        ("iWhy", INT),
    ]
PNMCBEENDEDIT = ctypes.POINTER(NMCBEENDEDIT)

class CBEN(IntEnum):
    FIRST = 0xFFFFFCE0
    GETDISPINFOA = FIRST - 0
    INSERTITEM   = FIRST - 1
    DELETEITEM   = FIRST - 2
    BEGINEDIT    = FIRST - 4
    ENDEDITA     = FIRST - 5
    ENDEDITW     = FIRST - 6
    GETDISPINFOW = FIRST - 7
    DRAGBEGINA   = FIRST - 8
    DRAGBEGINW   = FIRST - 9

class CBENF(IntEnum):
    KILLFOCUS = 1
    RETURN    = 2
    ESCAPE    = 3
    DROPDOWN  = 4

@dataclass
class ComboBoxEx(Control):
    """
    A class representing a ComboBoxEx control.

    Attributes:
        style (int): The style of the combo box control.
        windowClass (str): The window class of the combo box control.
        __items (list): The list of items in the combo box control.

    Methods:
        __post_init__() -> None:
            Initializes the ComboBoxEx object after its creation.

        getSelectedItem() -> int:
            Get the index of the currently selected item in the combo box.

        getSelectedItemText() -> str:
            This method retrieves the text of the selected item in a combo box.

        clear() -> None:
            Clear the items in the combo box.

        set(new_list_of_items) -> None:
            Update the items in the combo box with a new list.

        append(items) -> None:
            This method appends the specified items into the combo box.

        getComboControl() -> None:
            This method retrieves the handle of the underlying combo control associated
            with the ComboBoxEx control and sets it as the `child_combo_hwnd` attribute.

    Notification Callbacks:
        The following notification callbacks are available for the ComboBoxEx class:
        - onInsertItem: Triggered when an item is inserted into the combo box.
        - onDeleteItem: Triggered when an item is deleted from the combo box.
        - onBeginEdit: Triggered when the combo box enters edit mode.
        - onEndEdit: Triggered when the combo box finishes editing.
        - onGetDispInfo: Triggered to retrieve display information for an item.
        - onDragBegin: Triggered when dragging begins in the combo box.

    Combobox Notification Callbacks:
        The following notification callbacks inherited from the Control class are also available for the ComboBoxEx class:
        - onSelChange: Triggered when the selection in the combo box changes.
        - onDblClk: Triggered when the combo box is double-clicked.
        - onSetFocus: Triggered when the combo box receives focus.
        - onKillFocus: Triggered when the combo box loses focus.
        - onEditChange: Triggered when the content of the combo box edit control changes.
        - onEditUpdate: Triggered when the combo box edit control is updated.
        - onDropDown: Triggered when the combo box dropdown list is shown.
        - onCloseUp: Triggered when the combo box dropdown list is closed.
        - onSelEndOk: Triggered when the combo box selection is completed.
        - onSelEndCancel: Triggered when the combo box selection is canceled.

    """
    style: int = Control.style | CBS.DROPDOWN
    windowClass: str = 'ComboBoxEx32'
    __items: list = None

    def __post_init__(self):
        """
        This method is automatically called after the initialization of the ComboBoxEx object.
        It initializes the __items attribute if it is not set.

        Args:
            None

        Returns:
            None
        """
        if self.__items is None:
            self.__items = []

    # comboboxex notification callbacks
    onInsertItem = WM_NotifyDelegator(CBEN.INSERTITEM, PNMCOMBOBOXEX)
    onDeleteItem = WM_NotifyDelegator(CBEN.DELETEITEM, PNMCOMBOBOXEX)
    onBeginEdit = WM_NotifyDelegator(CBEN.BEGINEDIT, LPNMHDR)
    onEndEdit = WM_NotifyDelegator(CBEN.ENDEDITW, PNMCBEENDEDIT)
    onGetDispInfo = WM_NotifyDelegator(CBEN.GETDISPINFOW, PNMCOMBOBOXEX)
    onDragBegin = WM_NotifyDelegator(CBEN.DRAGBEGINW, PNMCBEDRAGBEGIN)

    # combobox notification callbacks
    onSelChange    = WM_CommandDelegator(CBN.SELCHANGE)
    onDblClk       = WM_CommandDelegator(CBN.DBLCLK)
    onSetFocus     = WM_CommandDelegator(CBN.SETFOCUS)
    onKillFocus    = WM_CommandDelegator(CBN.KILLFOCUS)
    onEditChange   = WM_CommandDelegator(CBN.EDITCHANGE)
    onEditUpdate   = WM_CommandDelegator(CBN.EDITUPDATE)
    onDropDown     = WM_CommandDelegator(CBN.DROPDOWN)
    onCloseUp      = WM_CommandDelegator(CBN.CLOSEUP)
    onSelEndOk     = WM_CommandDelegator(CBN.SELENDOK)
    onSelEndCancel = WM_CommandDelegator(CBN.SELENDCANCEL)

    def getSelectedItem(self):
        """
        Get the index of the currently selected item in the combo box.

        Returns:
            int: The index of the selected item.
        """
        return SendMessage(self.hwnd, CB.GETCURSEL, 0, 0)

    def getSelectedItemText(self):
        """
        Get the text of the currently selected item in the combo box.

        Returns:
            str: The text of the selected item.
        """
        index = SendMessage(self.hwnd, CB.GETCURSEL, 0, 0)
        return self.__items[index].value

    def clear(self):
        """
        Clear the items in the combo box.

        Returns:
            None
        """
        self.__items.clear()
        SendMessage(self.hwnd, CB.RESETCONTENT, 0, 0)

    def set(self, new_list_of_items):
        """
        Update the items in the combo box with a new list.

        Args:
            new_list_of_items (list): The new list of items.

        Returns:
            None
        """
        self.clear()
        self.append(new_list_of_items)

    def append(self, items):
        """
        This method inserts the specified items into the combo box.

        Args:
            items (list): The list of items to be inserted.

        Returns:
            None
        """
        self.__items = []
        try:
            cb_item = COMBOBOXEXITEM()
            cb_item.mask = CBEIF.TEXT
            for i, item in enumerate(items):
                self.__items.append(ctypes.create_unicode_buffer(item))
                cb_item.iItem          = i
                cb_item.pszText        = ctypes.addressof(self.__items[i])
                cb_item.cchTextMax     = len(self.__items[i])
                cb_item.iImage         = 0
                cb_item.iSelectedImage = 0
                cb_item.iIndent        = 0
                SendMessage(self.hwnd, CBEM.INSERTITEM, 0, ctypes.addressof(cb_item))
            # SendMessage(self.hwnd, CB.SETCURSEL, 0, 0)
        except Exception as e:
            print(f'append Exceptions:{e}')

    def getComboControl(self):
        """
        This method retrieves the handle of the underlying combo control associated
        with the ComboBoxEx control and sets it as the `child_combo_hwnd` attribute.

        Returns:
            None
        """
        self.child_combo_hwnd = SendMessage(self.hwnd, CBEM.GETCOMBOCONTROL, 0, 0)
