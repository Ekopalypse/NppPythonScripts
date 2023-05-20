""" Dialog SYSLISTVIEW32 control implementation """
from dataclasses import dataclass
from .__control_template import Control
from enum import IntEnum
from ..win_helper import SendMessage

import ctypes
from ctypes.wintypes import (
	UINT, LPARAM, INT, LPCWSTR,PUINT
)

class LVCOLUMN(ctypes.Structure):
    """ implementation of a LVCOLUMN structure """
    _fields_ = [('mask',        UINT),
                ('fmt',         INT),
                ('cx',          INT),
                ('pszText',     LPCWSTR),
                ('cchTextMax',  INT),
                ('iSubItem',    INT),
                ('iImage',      INT),
                ('iOrder',      INT),
                ('cxMin',       INT),
                ('cxDefault',   INT),
                ('cxIdeal',     INT),
                ]

class LVITEM(ctypes.Structure):
    """ implementation of a LVITEM structure """
    _fields_ = [('mask',       UINT),
                ('iItem',      INT),
                ('iSubItem',   INT),
                ('state',      UINT),
                ('stateMask',  UINT),
                ('pszText',    LPCWSTR),
                ('cchTextMax', INT),
                ('iImage',     INT),
                ('lParam',     LPARAM),
                ('iIndent',    INT),
                ('iGroupId',   INT),
                ('cColumns',   UINT),
                ('puColumns',  PUINT),
                ('piColFmt',   INT),
                ('iGroup',     INT),
                ]

class LVS(IntEnum):
    ICON = 0x0
    REPORT = 0x1
    SMALLICON = 0x2
    LIST = 0x3
    TYPEMASK = 0x3
    SINGLESEL = 0x4
    SHOWSELALWAYS = 0x8
    SORTASCENDING = 0x10
    SORTDESCENDING = 0x20
    SHAREIMAGELISTS = 0x40
    NOLABELWRAP = 0x80
    AUTOARRANGE = 0x100
    EDITLABELS = 0x200
    OWNERDATA = 0x1000
    NOSCROLL = 0x2000
    TYPESTYLEMASK = 0xFC00
    ALIGNTOP = 0x0
    ALIGNLEFT = 0x800
    ALIGNMASK = 0xC00
    OWNERDRAWFIXED = 0x400
    NOCOLUMNHEADER = 0x4000
    NOSORTHEADER = 0x8000

class LVS_EX(IntEnum):
    GRIDLINES        = 0x00000001
    SUBITEMIMAGES    = 0x00000002
    CHECKBOXES       = 0x00000004
    TRACKSELECT      = 0x00000008
    HEADERDRAGDROP   = 0x00000010
    FULLROWSELECT    = 0x00000020 # applies to report mode only
    ONECLICKACTIVATE = 0x00000040
    TWOCLICKACTIVATE = 0x00000080
    FLATSB           = 0x00000100
    REGIONAL         = 0x00000200
    INFOTIP          = 0x00000400 # listview does InfoTips for you
    UNDERLINEHOT     = 0x00000800
    UNDERLINECOLD    = 0x00001000
    MULTIWORKAREAS   = 0x00002000
    LABELTIP         = 0x00004000 # listview unfolds partly hidden labels if it does not have infotip text
    BORDERSELECT     = 0x00008000 # border selection style instead of highlight
    # if (NTDDI_VERSION >= NTDDI_WINXP)
    DOUBLEBUFFER     = 0x00010000
    HIDELABELS       = 0x00020000
    SINGLEROW        = 0x00040000
    SNAPTOGRID       = 0x00080000  # Icons automatically snap to grid.
    SIMPLESELECT     = 0x00100000  # Also changes overlay rendering to top right for icon mode.
    # endif
    # if (NTDDI_VERSION >= NTDDI_VISTA)
    JUSTIFYCOLUMNS   = 0x00200000  # Icons are lined up in columns that use up the whole view area.
    TRANSPARENTBKGND = 0x00400000  # Background is painted by the parent via WM_PRINTCLIENT
    TRANSPARENTSHADOWTEXT = 0x00800000  # Enable shadow text on transparent backgrounds only (useful with bitmaps)
    AUTOAUTOARRANGE  = 0x01000000  # Icons automatically arrange if no icon positions have been set
    HEADERINALLVIEWS = 0x02000000  # Display column header in all view modes
    AUTOCHECKSELECT  = 0x08000000
    AUTOSIZECOLUMNS  = 0x10000000
    COLUMNSNAPPOINTS = 0x40000000
    COLUMNOVERFLOW   = 0x80000000

class LVM(IntEnum):
    FIRST = 0x1000

    # ListView Messages
    GETBKCOLOR = FIRST + 0
    SETBKCOLOR = FIRST + 1
    GETIMAGELIST = FIRST + 2
    SETIMAGELIST = FIRST + 3
    GETITEMCOUNT = FIRST + 4

    DELETEITEM = FIRST + 8
    DELETEALLITEMS = FIRST + 9
    GETCALLBACKMASK = FIRST + 10
    SETCALLBACKMASK = FIRST + 11
    GETNEXTITEM = FIRST + 12

    SETITEMPOSITION = FIRST + 15
    GETITEMPOSITION = FIRST + 16

    HITTEST = FIRST + 18
    ENSUREVISIBLE = FIRST + 19
    SCROLL = FIRST + 20
    REDRAWITEMS = FIRST + 21
    ARRANGE = FIRST + 22

    GETEDITCONTROL = FIRST + 24

    DELETECOLUMN = FIRST + 28
    GETCOLUMNWIDTH = FIRST + 29
    SETCOLUMNWIDTH = FIRST + 30

    GETHEADER = FIRST + 31

    CREATEDRAGIMAGE = FIRST + 33
    GETVIEWRECT = FIRST + 34
    GETTEXTCOLOR = FIRST + 35
    SETTEXTCOLOR = FIRST + 36
    GETTEXTBKCOLOR = FIRST + 37
    SETTEXTBKCOLOR = FIRST + 38
    GETTOPINDEX = FIRST + 39
    GETCOUNTPERPAGE = FIRST + 40
    GETORIGIN = FIRST + 41
    UPDATE = FIRST + 42
    SETITEMSTATE = FIRST + 43
    GETITEMSTATE = FIRST + 44
    SETITEMCOUNT = FIRST + 47
    SORTITEMS = FIRST + 48
    SETITEMPOSITION32 = FIRST + 49
    GETSELECTEDCOUNT = FIRST + 50
    GETITEMSPACING = FIRST + 51

    SETICONSPACING = FIRST + 53
    SETEXTENDEDLISTVIEWSTYLE = FIRST + 54
    GETEXTENDEDLISTVIEWSTYLE = FIRST + 55
    GETSUBITEMRECT = FIRST + 56
    SUBITEMHITTEST = FIRST + 57
    SETCOLUMNORDERARRAY = FIRST + 58
    GETCOLUMNORDERARRAY = FIRST + 59
    SETHOTITEM = FIRST + 60
    GETHOTITEM = FIRST + 61
    SETHOTCURSOR = FIRST + 62
    GETHOTCURSOR = FIRST + 63
    APPROXIMATEVIEWRECT = FIRST + 64
    SETWORKAREA = FIRST + 65
    GETSELECTIONMARK = FIRST + 66
    SETSELECTIONMARK = FIRST + 67
    GETWORKAREA = FIRST + 70
    SETHOVERTIME = FIRST + 71
    GETHOVERTIME = FIRST + 72

    GETITEM = FIRST + 75
    SETITEM = FIRST + 76
    INSERTITEMW = FIRST + 77
    INSERTITEM = INSERTITEMW
    FINDITEMW = FIRST + 83
    FINDITEM = FINDITEMW
    GETSTRINGWIDTHW = FIRST + 87
    GETSTRINGWIDTH = GETSTRINGWIDTHW
    EDITLABELW = FIRST + 118
    EDITLABEL = EDITLABELW
    GETCOLUMNW = FIRST + 95
    GETCOLUMN = GETCOLUMNW
    SETCOLUMNW = FIRST + 96
    SETCOLUMN = SETCOLUMNW
    INSERTCOLUMNW = FIRST + 97
    INSERTCOLUMN = INSERTCOLUMNW
    GETITEMTEXTW = FIRST + 115
    GETITEMTEXT = GETITEMTEXTW
    SETITEMTEXTW = FIRST + 116
    SETITEMTEXT = SETITEMTEXTW
    GETISEARCHSTRINGW = FIRST + 117
    GETISEARCHSTRING = GETISEARCHSTRINGW
    GETBKIMAGEW = FIRST + 139
    SETBKIMAGEW = FIRST + 138
    # LVBKIMAGE = LVBKIMAGEW
    # LPLVBKIMAGE = LPLVBKIMAGEW
    SETBKIMAGE = SETBKIMAGEW
    GETBKIMAGE = GETBKIMAGEW

class LVCF(IntEnum):
    FMT          = 0x0001
    WIDTH        = 0x0002
    TEXT         = 0x0004
    SUBITEM      = 0x0008
    IMAGE        = 0x0010
    ORDER        = 0x0020
    MINWIDTH     = 0x0040
    DEFAULTWIDTH = 0x0080
    IDEALWIDTH   = 0x0100

class LVCFMT(IntEnum):
    LEFT               = 0x0000
    RIGHT              = 0x0001
    CENTER             = 0x0002
    JUSTIFYMASK        = 0x0003

    IMAGE              = 0x0800
    BITMAP_ON_RIGHT    = 0x1000
    COL_HAS_IMAGES     = 0x8000

    FIXED_WIDTH        = 0x00100
    NO_DPI_SCALE       = 0x40000
    FIXED_RATIO        = 0x80000

    # The following flags
    LINE_BREAK         = 0x100000
    FILL               = 0x200000
    WRAP               = 0x400000
    NO_TITLE           = 0x800000
    TILE_PLACEMENTMASK = LINE_BREAK | FILL

    SPLITBUTTON        = 0x1000000

class LVIF(IntEnum):
    TEXT               = 0x00000001
    IMAGE              = 0x00000002
    PARAM              = 0x00000004
    STATE              = 0x00000008
    INDENT             = 0x00000010
    NORECOMPUTE        = 0x00000800
    # if (NTDDI_VERSION >= NTDDI_WINXP)
    GROUPID            = 0x00000100
    COLUMNS            = 0x00000200
    # endif
    #if (NTDDI_VERSION >= NTDDI_VISTA)
    COLFMT             = 0x00010000  # The piColFmt member is valid in addition to puColumns
    #endif

class LVIS(IntEnum):
    FOCUSED            = 0x0001
    SELECTED           = 0x0002
    CUT                = 0x0004
    DROPHILITED        = 0x0008
    GLOW               = 0x0010
    ACTIVATING         = 0x0020

    OVERLAYMASK        = 0x0F00
    STATEIMAGEMASK     = 0xF000
    # STATEIMAGEMASK = 0x3000

    UNCHECKED          = 0x1000
    CHECKED            = 0x2000

LVSCW_AUTOSIZE = -1
LVSCW_AUTOSIZE_USEHEADER = -2

@dataclass
class ListView(Control):
    """ Implementation of a ListView control """
    style: int = Control.style | LVS.REPORT
    window_class: str = 'SysListView32'
    column_count: int = 0
    columns: list = None
    rows: list = None
    show_headers: bool = False
    fit_last_column: bool = False

    # def initialize(self):
        # # ex_flags = LVS_EX.GRIDLINES | LVS_EX.FULLROWSELECT | LVS_EX.FLATSB
        # # SendMessage(self.hwnd, LVM.SETEXTENDEDLISTVIEWSTYLE, ex_flags, ex_flags)
        # self.create_columns()
        # self.insert_items()

        # if self.fgcolor is not None:
            # self.set_text_foreground_color(self.fgcolor)
        # if self.bgcolor is not None:
            # self.set_text_background_color(self.bgcolor)
            # self.set_window_background_color(self.bgcolor)

    # def _rgb_from_tuple(self, color):
        # return (color[2] << 16) + (color[1] << 8) + color[0]

    # def set_text_foreground_color(self, color):
        # SendMessage(self.hwnd, LVM.SETTEXTCOLOR, 0, self._rgb_from_tuple(color))

    # def set_text_background_color(self, color):
        # SendMessage(self.hwnd, LVM.SETTEXTBKCOLOR, 0, self._rgb_from_tuple(color))

    # def set_window_background_color(self, color):
        # SendMessage(self.hwnd, LVM.SETBKCOLOR, 0, self._rgb_from_tuple(color))

    # def autosize_columns(self):
        # SendMessage(self.hwnd, LVM.SETEXTENDEDLISTVIEWSTYLE, LVS_EX.AUTOSIZECOLUMNS, LVS_EX.AUTOSIZECOLUMNS)

    def insert_items(self):
        lv_item = LVITEM()
        lv_item.mask = LVIF.TEXT
        for i in range(len(self.rows)):
            lv_item.iItem = i
            for j in range(self.column_count):
                try:
                    if j == 0:
                        lv_item.iSubItem = 0
                        lv_item.pszText = self.rows[i][0]
                        SendMessage(self.hwnd, LVM.INSERTITEM, 0, ctypes.addressof(lv_item))
                    else:
                        lv_item.iSubItem = j
                        lv_item.pszText = self.rows[i][j]
                        SendMessage(self.hwnd, LVM.SETITEM, 0, ctypes.addressof(lv_item))
                except IndexError:
                    pass

        for i in range(len(self.rows)):
            SendMessage(self.hwnd, LVM.SETCOLUMNWIDTH, i, LVSCW_AUTOSIZE)


    def delete_all_items(self):
        SendMessage(self.hwnd, LVM.DELETEALLITEMS, 0, 0)

    def create_columns(self):
        self.column_count = len(self.columns)
        for i in range(self.column_count):
            item = LVCOLUMN()
            item.mask = LVCF.TEXT | LVCF.FMT # | LVCF.SUBITEM
            item.fmt = LVCFMT.LEFT
            item.cx = 50
            col_name = self.columns[i]
            item.pszText = col_name
            item.cchTextMax = len(col_name)
            SendMessage(self.hwnd, LVM.INSERTCOLUMN, i, ctypes.addressof(item))
        SendMessage(self.hwnd, LVM.SETEXTENDEDLISTVIEWSTYLE, LVS_EX.CHECKBOXES, LVS_EX.CHECKBOXES)

    def get_checked_items(self):
        lv_item = LVITEM()
        lv_item.mask = LVIF.STATE
        lv_item.stateMask = LVIS.CHECKED
        checked_items = []
        for i in range(len(self.rows)):
            lv_item.iItem = i
            SendMessage(self.hwnd, LVM.GETITEM, 0, ctypes.addressof(lv_item))
            if lv_item.state == LVIS.CHECKED:
                checked_items.append(i)
                # length = SendMessage(self.hwnd, LVM.GETITEMTEXT, i, ctypes.addressof(lv_item))
                # print(length, lv_item.pszText)


        return checked_items

    def delete_column(self, column_index):
        SendMessage(self.hwnd, LVM.DELETECOLUMN, column_index, 0)

    # def DeleteColumns(self):
    #     for i in range(self.column_number):
    #         self.DeleteColumn(0)


