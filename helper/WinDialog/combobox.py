""" Dialog combobox control implementation
"""

from enum import IntEnum
from .dialog_template import Control
from .win_helper import (
    WindowStyle as WS,
    SendMessage, HIWORD
)
import ctypes

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

class ComboBox(Control):
    """ Implementations of the combobox control """

    def __init__(self, size=None, position=None):
        super().__init__('', size, position)
        self.windowClass = 'Combobox'
        self.style = WS.CHILD | WS.VISIBLE | CBS.HASSTRINGS | CBS.DROPDOWNLIST
        self.size = size
        self.position = position
        self.intialize_needed = True
        self.items = []
        self.on_selchange = lambda: None

    def get_selected_item(self):
        return SendMessage(self.hwnd, CB.GETCURSEL, 0, 0)

    def callback(self, wparam, lparam):
        match HIWORD(wparam):
            case CBN.SELCHANGE:
                self.on_selchange()
            case _:
                return

    def clear(self):
        self.items.clear()
        SendMessage(self.hwnd, CB.RESETCONTENT, 0, 0)

    def update(self, new_list_of_items):
        self.clear()
        self.items.extend(new_list_of_items)
        self.insert_items()

    def initialize(self):
        self.insert_items()

    def insert_items(self):
        try:
            for item in self.items:
                lp_item = ctypes.addressof(ctypes.create_unicode_buffer(item))
                SendMessage(self.hwnd, CB.ADDSTRING, 0, lp_item)
            SendMessage(self.hwnd, CB.SETCURSEL, 0, 0)
        except Exception as e:
            print(f'insert_items Exceptions:{e}')