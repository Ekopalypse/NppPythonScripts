""" Dialog LISTBOX control implementation """
from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    WM_CommandDelegator,
    WindowStyle as WS,
    SendMessage
)
import ctypes

class LBS(IntEnum):
    NOTIFY            = 0x0001
    SORT              = 0x0002
    NOREDRAW          = 0x0004
    MULTIPLESEL       = 0x0008
    OWNERDRAWFIXED    = 0x0010
    OWNERDRAWVARIABLE = 0x0020
    HASSTRINGS        = 0x0040
    USETABSTOPS       = 0x0080
    NOINTEGRALHEIGHT  = 0x0100
    MULTICOLUMN       = 0x0200
    WANTKEYBOARDINPUT = 0x0400
    EXTENDEDSEL       = 0x0800
    DISABLENOSCROLL   = 0x1000
    NODATA            = 0x2000
    NOSEL             = 0x4000
    COMBOBOX          = 0x8000
    STANDARD          = NOTIFY | SORT | WS.VSCROLL | WS.BORDER

class LBN(IntEnum):
    ERRSPACE        = (-2)
    SELCHANGE       = 1
    DBLCLK          = 2
    SELCANCEL       = 3
    SETFOCUS        = 4
    KILLFOCUS       = 5

class LB(IntEnum):
    ADDSTRING            = 0x0180
    INSERTSTRING         = 0x0181
    DELETESTRING         = 0x0182
    SELITEMRANGEEX       = 0x0183
    RESETCONTENT         = 0x0184
    SETSEL               = 0x0185
    SETCURSEL            = 0x0186
    GETSEL               = 0x0187
    GETCURSEL            = 0x0188
    GETTEXT              = 0x0189
    GETTEXTLEN           = 0x018A
    GETCOUNT             = 0x018B
    SELECTSTRING         = 0x018C
    DIR                  = 0x018D
    GETTOPINDEX          = 0x018E
    FINDSTRING           = 0x018F
    GETSELCOUNT          = 0x0190
    GETSELITEMS          = 0x0191
    SETTABSTOPS          = 0x0192
    GETHORIZONTALEXTENT  = 0x0193
    SETHORIZONTALEXTENT  = 0x0194
    SETCOLUMNWIDTH       = 0x0195
    ADDFILE              = 0x0196
    SETTOPINDEX          = 0x0197
    GETITEMRECT          = 0x0198
    GETITEMDATA          = 0x0199
    SETITEMDATA          = 0x019A
    SELITEMRANGE         = 0x019B
    SETANCHORINDEX       = 0x019C
    GETANCHORINDEX       = 0x019D
    SETCARETINDEX        = 0x019E
    GETCARETINDEX        = 0x019F
    SETITEMHEIGHT        = 0x01A0
    GETITEMHEIGHT        = 0x01A1
    FINDSTRINGEXACT      = 0x01A2
    SETLOCALE            = 0x01A5
    GETLOCALE            = 0x01A6
    SETCOUNT             = 0x01A7
    INITSTORAGE          = 0x01A8
    ITEMFROMPOINT        = 0x01A9

@dataclass
class ListBox(Control):
    """ Implementations of a listbox control """
    style: int = WS.CHILD | WS.VISIBLE | LBS.HASSTRINGS | LBS.STANDARD
    window_class: str = 'Listbox'
    __items: list = None

    def __post_init__(self):
        if self.__items is None:
            self.__items = []

    # listbox notification callbacks
    on_errspace = WM_CommandDelegator(LBN.ERRSPACE)
    on_selchange = WM_CommandDelegator(LBN.SELCHANGE)
    on_dblclk = WM_CommandDelegator(LBN.DBLCLK)
    on_selcancel = WM_CommandDelegator(LBN.SELCANCEL)
    on_setfocus = WM_CommandDelegator(LBN.SETFOCUS)
    on_killfocus = WM_CommandDelegator(LBN.KILLFOCUS)

    def clear(self):
        self.__items.clear()
        SendMessage(self.hwnd, LB.RESETCONTENT, 0, 0)

    def add_strings(self, items):
        '''
            Adds a list of strings to the listbox
        '''
        if not all(isinstance(item, str) for item in items):
            raise ValueError('Not all items are of type string')
        self.__items = []
        for i, item in enumerate(items):
            self.__items.append(ctypes.create_unicode_buffer(item))
            lp_item = ctypes.addressof(self.__items[i])
            SendMessage(self.hwnd, LB.ADDSTRING, 0, lp_item)

    def add_string(self, item):
        '''
            Adds a string to the listbox
        '''
        if not isinstance(item, str):
            raise ValueError('Item is not of type string')

        lp_item = ctypes.addressof(ctypes.create_unicode_buffer(item))
        SendMessage(self.hwnd, LB.ADDSTRING, 0, lp_item)


    def get_selected_item(self):
        '''
            In a single-selection list box, the return value is the
            zero-based index of the currently selected item.
            If there is no selection, the return value is LB_ERR.
        '''
        return SendMessage(self.hwnd, LB.GETCURSEL, 0, 0)