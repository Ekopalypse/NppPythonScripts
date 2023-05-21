""" Dialog COMBOBOX control implementation """
from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    WindowStyle as WS,
    WM_CommandDelegator, WM_NotifyDelegator,
    CCM,
    SendMessage, NMHDR, WM_USER, INT_PTR, LPNMHDR,
    GetDlgItemText
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
    """ Implementations of the combobox control """
    style: int = WS.CHILD | WS.VISIBLE | CBS.HASSTRINGS | CBS.DROPDOWNLIST
    window_class: str = 'Combobox'
    items: list = None

    def __post_init__(self):
        if self.items is None:
            self.items = []

    # combobox notification callbacks
    on_selchange    = WM_CommandDelegator(CBN.SELCHANGE)
    on_dblclk       = WM_CommandDelegator(CBN.DBLCLK)
    on_setfocus     = WM_CommandDelegator(CBN.SETFOCUS)
    on_killfocus    = WM_CommandDelegator(CBN.KILLFOCUS)
    on_editchange   = WM_CommandDelegator(CBN.EDITCHANGE)
    on_editupdate   = WM_CommandDelegator(CBN.EDITUPDATE)
    on_dropdown     = WM_CommandDelegator(CBN.DROPDOWN)
    on_closeup      = WM_CommandDelegator(CBN.CLOSEUP)
    on_selendok     = WM_CommandDelegator(CBN.SELENDOK)
    on_selendcancel = WM_CommandDelegator(CBN.SELENDCANCEL)

    def get_selected_item(self):
        return SendMessage(self.hwnd, CB.GETCURSEL, 0, 0)

    def clear(self):
        self.items.clear()
        SendMessage(self.hwnd, CB.RESETCONTENT, 0, 0)

    def update(self, new_list_of_items):
        self.clear()
        self.items.extend(new_list_of_items)
        self.insert_items()

    def insert_items(self):
        try:
            for item in self.items:
                lp_item = ctypes.addressof(ctypes.create_unicode_buffer(item))
                SendMessage(self.hwnd, CB.ADDSTRING, 0, lp_item)
            SendMessage(self.hwnd, CB.SETCURSEL, 0, 0)
        except Exception as e:
            print(f'insert_items Exceptions:{e}')

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
    """ implementation of a COMBOBOXEXITEM structure """
    # _pack_ = 1
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
    style: int = Control.style | CBS.DROPDOWN
    window_class: str = 'ComboBoxEx32'
    __items: list = None

    def __post_init__(self):
        if self.__items is None:
            self.__items = []

    # comboboxex notification callbacks
    # on_getdispinfoa = WM_NotifyDelegator(CBEN.GETDISPINFOA, None)
    on_insertitem = WM_NotifyDelegator(CBEN.INSERTITEM, PNMCOMBOBOXEX)
    on_deleteitem = WM_NotifyDelegator(CBEN.DELETEITEM, PNMCOMBOBOXEX)
    on_beginedit = WM_NotifyDelegator(CBEN.BEGINEDIT, LPNMHDR)
    # on_endedita = WM_NotifyDelegator(CBEN.ENDEDITA, PNMCBEENDEDIT)
    on_endedit = WM_NotifyDelegator(CBEN.ENDEDITW, PNMCBEENDEDIT)
    on_getdispinfo = WM_NotifyDelegator(CBEN.GETDISPINFOW, PNMCOMBOBOXEX)
    # on_dragbegina = WM_NotifyDelegator(CBEN.DRAGBEGINA, None)
    on_dragbegin = WM_NotifyDelegator(CBEN.DRAGBEGINW, PNMCBEDRAGBEGIN)

    # combobox notification callbacks
    on_selchange    = WM_CommandDelegator(CBN.SELCHANGE)
    on_dblclk       = WM_CommandDelegator(CBN.DBLCLK)
    on_setfocus     = WM_CommandDelegator(CBN.SETFOCUS)
    on_killfocus    = WM_CommandDelegator(CBN.KILLFOCUS)
    on_editchange   = WM_CommandDelegator(CBN.EDITCHANGE)
    on_editupdate   = WM_CommandDelegator(CBN.EDITUPDATE)
    on_dropdown     = WM_CommandDelegator(CBN.DROPDOWN)
    on_closeup      = WM_CommandDelegator(CBN.CLOSEUP)
    on_selendok     = WM_CommandDelegator(CBN.SELENDOK)
    on_selendcancel = WM_CommandDelegator(CBN.SELENDCANCEL)

    def get_selected_item(self):
        return SendMessage(self.hwnd, CB.GETCURSEL, 0, 0)

    def clear(self):
        self.__items.clear()
        SendMessage(self.hwnd, CB.RESETCONTENT, 0, 0)

    def update(self, new_list_of_items):
        self.clear()
        self.__items.extend(new_list_of_items)
        self.insert_items()

    def insert_items(self, items):
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
            print(f'insert_items Exceptions:{e}')

    def get_text(self, buffer_length):
        buffer = ctypes.create_unicode_buffer(buffer_length)
        res = GetDlgItemText(self.hwnd, self.id, buffer, buffer_length)
        if res != 0:
            return buffer.value
        return None

    def get_combo_control(self):
        self.child_combo_hwnd = SendMessage(self.hwnd, CBEM.GETCOMBOCONTROL, 0, 0)

    # def set_dropdown_visibility(self, show=False):
        # self.child_combo_hwnd = SendMessage(self.hwnd, CBEM.GETCOMBOCONTROL, 0, 0)
        # SendMessage(self.child_combo_hwnd, CB.SHOWDROPDOWN, 1 if show else 0, 0)

    # def get_edit_control(self):
        # hwnd = SendMessage(self.hwnd, CBEM.GETEDITCONTROL, 0, 0)
        # if hwnd == 0:
            # combo_hwnd = FindWindowEx(self.hwnd, None, 'Combobox', None)
            # combo_l_hwnd = FindWindowEx(combo_hwnd, None, 'ComboLbox', None)
            # hwnd = FindWindowEx(combo_hwnd, combo_l_hwnd, 'Edit', None)

        # print('get_edit_control', hwnd)