"""
SYSLISTVIEW32 Control Implementations

Example Usage:
    from WinDialog import ListView

    # Create a list view control
    listview = ListView('', (180, 200), (0,0))
    listview.columns = ['Col{}'.format(x) for x in range(2)]
    listview.rows = [('{}'.format(x),'{}'.format(pow(x,x))) for x in range(100)]

For detailed documentation, refer to their respective docstrings.
"""
from dataclasses import dataclass
from .__control_template import Control
from enum import IntEnum
from ..win_helper import (
    SendMessage, NM, WM_NotifyDelegator, MAKELPARAM, NMHDR, CCM, MAKELONG
)

import ctypes
from ctypes.wintypes import (
    UINT, LPARAM, INT, LPCWSTR, PUINT, PINT, POINT, ULONG, DWORD, SIZE, RECT, HBITMAP, WORD, WCHAR
)

PFNLVCOMPARE = ctypes.WINFUNCTYPE(INT, LPARAM, LPARAM, LPARAM)
PFNLVGROUPCOMPARE = ctypes.WINFUNCTYPE(INT, INT, INT, ctypes.c_void_p)

class LVS(IntEnum):
    ICON = 0x0000
    REPORT = 0x0001
    SMALLICON = 0x0002
    LIST = 0x0003
    TYPEMASK = 0x0003
    SINGLESEL = 0x0004
    SHOWSELALWAYS = 0x0008
    SORTASCENDING = 0x0010
    SORTDESCENDING = 0x0020
    SHAREIMAGELISTS = 0x0040
    NOLABELWRAP = 0x0080
    AUTOARRANGE = 0x0100
    EDITLABELS = 0x0200
    OWNERDATA = 0x1000
    NOSCROLL = 0x2000
    TYPESTYLEMASK = 0xfc00
    ALIGNTOP = 0x0000
    ALIGNLEFT = 0x0800
    ALIGNMASK = 0x0c00
    OWNERDRAWFIXED = 0x0400
    NOCOLUMNHEADER = 0x4000
    NOSORTHEADER = 0x8000

class LVSIL(IntEnum):
    NORMAL = 0
    SMALL = 1
    STATE = 2
    GROUPHEADER = 3

class LVIF(IntEnum):
    TEXT = 0x00000001
    IMAGE = 0x00000002
    PARAM = 0x00000004
    STATE = 0x00000008
    INDENT = 0x00000010
    NORECOMPUTE = 0x00000800
    GROUPID = 0x00000100
    COLUMNS = 0x00000200
    COLFMT = 0x00010000

class LVIS(IntEnum):
    FOCUSED = 0x0001
    SELECTED = 0x0002
    CUT = 0x0004
    DROPHILITED = 0x0008
    GLOW = 0x0010
    ACTIVATING = 0x0020
    OVERLAYMASK = 0x0F00
    STATEIMAGEMASK = 0xF000

class LVNI(IntEnum):
    ALL = 0x0000
    FOCUSED = 0x0001
    SELECTED = 0x0002
    CUT = 0x0004
    DROPHILITED = 0x0008
    STATEMASK = FOCUSED | SELECTED | CUT | DROPHILITED
    VISIBLEORDER = 0x0010
    PREVIOUS = 0x0020
    VISIBLEONLY = 0x0040
    SAMEGROUPONLY = 0x0080
    ABOVE = 0x0100
    BELOW = 0x0200
    TOLEFT = 0x0400
    TORIGHT = 0x0800
    DIRECTIONMASK = ABOVE | BELOW | TOLEFT | TORIGHT

class LVFI(IntEnum):
    PARAM = 0x0001
    STRING = 0x0002
    SUBSTRING = 0x0004
    PARTIAL = 0x0008
    WRAP = 0x0020
    NEARESTXY = 0x0040

class LVIR(IntEnum):
    BOUNDS = 0
    ICON = 1
    LABEL = 2
    SELECTBOUNDS = 3

class LVHT(IntEnum):
    NOWHERE = 0x00000001
    ONITEMICON = 0x00000002
    ONITEMLABEL = 0x00000004
    ONITEMSTATEICON = 0x00000008
    ONITEM = ONITEMICON | ONITEMLABEL | ONITEMSTATEICON
    ABOVE = 0x00000008
    BELOW = 0x00000010
    TORIGHT = 0x00000020
    TOLEFT = 0x00000040

class LVHTEX(IntEnum):
    GROUPHEADER = 0x10000000
    GROUPFOOTER = 0x20000000
    GROUPCOLLAPSE = 0x40000000
    GROUPBACKGROUND = 0x80000000
    GROUPSTATEICON = 0x01000000
    GROUPSUBSETLINK = 0x02000000
    GROUP = GROUPBACKGROUND | GROUPCOLLAPSE | GROUPFOOTER | GROUPHEADER | GROUPSTATEICON | GROUPSUBSETLINK
    ONCONTENTS = 0x04000000
    FOOTER = 0x08000000

class LVA(IntEnum):
    DEFAULT = 0x0000
    ALIGNLEFT = 0x0001
    ALIGNTOP = 0x0002
    SNAPTOGRID = 0x0005

class LVCF(IntEnum):
    FMT = 0x0001
    WIDTH = 0x0002
    TEXT = 0x0004
    SUBITEM = 0x0008
    IMAGE = 0x0010
    ORDER = 0x0020
    MINWIDTH = 0x0040
    DEFAULTWIDTH = 0x0080
    IDEALWIDTH = 0x0100

class LVCFMT(IntEnum):
    LEFT = 0x0000
    RIGHT = 0x0001
    CENTER = 0x0002
    JUSTIFYMASK = 0x0003
    IMAGE = 0x0800
    BITMAPONRIGHT = 0x1000
    COLHASIMAGES = 0x8000

    FIXEDWIDTH = 0x00100
    NODPISCALE = 0x40000
    FIXEDRATIO = 0x80000
    LINEBREAK = 0x100000
    FILL = 0x200000
    WRAP = 0x400000
    NOTITLE = 0x800000
    TILEPLACEMENTMASK = LINEBREAK | FILL
    SPLITBUTTON = 0x1000000

class LVSCW(IntEnum):
    AUTOSIZE = -1
    AUTOSIZEUSEHEADER = -2

class LVSICF(IntEnum):
    NOINVALIDATEALL = 0x00000001
    NOSCROLL = 0x00000002

class LVS_EX(IntEnum):
    GRIDLINES = 0x00000001
    SUBITEMIMAGES = 0x00000002
    CHECKBOXES = 0x00000004
    TRACKSELECT = 0x00000008
    HEADERDRAGDROP = 0x00000010
    FULLROWSELECT = 0x00000020
    ONECLICKACTIVATE = 0x00000040
    TWOCLICKACTIVATE = 0x00000080
    FLATSB = 0x00000100
    REGIONAL = 0x00000200
    INFOTIP = 0x00000400
    UNDERLINEHOT = 0x00000800
    UNDERLINECOLD = 0x00001000
    MULTIWORKAREAS = 0x00002000
    LABELTIP = 0x00004000
    BORDERSELECT = 0x00008000
    DOUBLEBUFFER = 0x00010000
    HIDELABELS = 0x00020000
    SINGLEROW = 0x00040000
    SNAPTOGRID = 0x00080000
    SIMPLESELECT = 0x00100000
    JUSTIFYCOLUMNS = 0x00200000
    TRANSPARENTBKGND = 0x00400000
    TRANSPARENTSHADOWTEXT = 0x00800000
    AUTOAUTOARRANGE = 0x01000000
    HEADERINALLVIEWS = 0x02000000
    AUTOCHECKSELECT = 0x08000000
    AUTOSIZECOLUMNS = 0x10000000
    COLUMNSNAPPOINTS = 0x40000000
    COLUMNOVERFLOW = 0x80000000

class LVBKIF(IntEnum):
    SOURCENONE = 0x00000000
    SOURCEHBITMAP = 0x00000001
    SOURCEURL = 0x00000002
    SOURCEMASK = 0x00000003
    STYLENORMAL = 0x00000000
    STYLETILE = 0x00000010
    STYLEMASK = 0x00000010
    FLAGTILEOFFSET = 0x00000100
    TYPEWATERMARK = 0x10000000
    FLAGALPHABLEND = 0x20000000

class LV(IntEnum):
    VIEWICON = 0x0000
    VIEWDETAILS = 0x0001
    VIEWSMALLICON = 0x0002
    VIEWLIST = 0x0003
    VIEWTILE = 0x0004
    VIEWMAX = 0x0004

class LVGF(IntEnum):
    NONE = 0x00000000
    HEADER = 0x00000001
    FOOTER = 0x00000002
    STATE = 0x00000004
    ALIGN = 0x00000008
    GROUPID = 0x00000010
    SUBTITLE = 0x00000100
    TASK = 0x00000200
    DESCRIPTIONTOP = 0x00000400
    DESCRIPTIONBOTTOM = 0x00000800
    TITLEIMAGE = 0x00001000
    EXTENDEDIMAGE = 0x00002000
    ITEMS = 0x00004000
    SUBSET = 0x00008000
    SUBSETITEMS = 0x00010000

class LVGS(IntEnum):
    NORMAL = 0x00000000
    COLLAPSED = 0x00000001
    HIDDEN = 0x00000002
    NOHEADER = 0x00000004
    COLLAPSIBLE = 0x00000008
    FOCUSED = 0x00000010
    SELECTED = 0x00000020
    SUBSETED = 0x00000040
    SUBSETLINKFOCUSED = 0x00000080

class LVGA(IntEnum):
    HEADERLEFT = 0x00000001
    HEADERCENTER = 0x00000002
    HEADERRIGHT = 0x00000004
    FOOTERLEFT = 0x00000008
    FOOTERCENTER = 0x00000010
    FOOTERRIGHT = 0x00000020

class LVGGR(IntEnum):
    GROUP = 0
    HEADER = 1
    LABEL = 2
    SUBSETLINK = 3
class LVGMF(IntEnum):
    NONE = 0x00000000
    BORDERSIZE = 0x00000001
    BORDERCOLOR = 0x00000002
    TEXTCOLOR = 0x00000004

class LVTVIF(IntEnum):
    AUTOSIZE = 0x00000000
    FIXEDWIDTH = 0x00000001
    FIXEDHEIGHT = 0x00000002
    FIXEDSIZE = 0x00000003
    EXTENDED = 0x00000004

class LVTVIM(IntEnum):
    TILESIZE = 0x00000001
    COLUMNS = 0x00000002
    LABELMARGIN = 0x00000004

class LVFF(IntEnum):
    ITEMCOUNT = 0x00000001

class LVFIF(IntEnum):
    TEXT = 0x00000001
    STATE = 0x00000002

class LVFIS(IntEnum):
    FOCUSED = 0x0001

class LVKF(IntEnum):
    ALT = 0x0001
    CONTROL = 0x0002
    SHIFT = 0x0004

class LVCDI(IntEnum):
    ITEM = 0x00000000
    GROUP = 0x00000001
    ITEMSLIST = 0x00000002

class LVCDRF(IntEnum):
    NOSELECT = 0x00010000
    NOGROUPFRAME = 0x00020000

class LVN(IntEnum):
    FIRST = -100
    ITEMCHANGING = FIRST-0
    ITEMCHANGED = FIRST-1
    INSERTITEM = FIRST-2
    DELETEITEM = FIRST-3
    DELETEALLITEMS = FIRST-4
    BEGINLABELEDITA = FIRST-5
    BEGINLABELEDITW = FIRST-75
    ENDLABELEDITA = FIRST-6
    ENDLABELEDITW = FIRST-76
    COLUMNCLICK = FIRST-8
    BEGINDRAG = FIRST-9
    BEGINRDRAG = FIRST-11
    ODCACHEHINT = FIRST-13
    ODFINDITEMA = FIRST-52
    ODFINDITEMW = FIRST-79
    ITEMACTIVATE = FIRST-14
    ODSTATECHANGED = FIRST-15
    ODFINDITEM = ODFINDITEMW
    HOTTRACK = FIRST-21
    GETDISPINFOA = FIRST-50
    GETDISPINFOW = FIRST-77
    SETDISPINFOA = FIRST-51
    SETDISPINFOW = FIRST-78
    BEGINLABELEDIT = BEGINLABELEDITW
    ENDLABELEDIT = ENDLABELEDITW
    GETDISPINFO = GETDISPINFOW
    SETDISPINFO = SETDISPINFOW
    KEYDOWN = FIRST-55
    MARQUEEBEGIN = FIRST-56
    GETINFOTIPA = FIRST-57
    GETINFOTIPW = FIRST-58
    GETINFOTIP = GETINFOTIPW
    INCREMENTALSEARCHA = FIRST-62
    INCREMENTALSEARCHW = FIRST-63
    INCREMENTALSEARCH = INCREMENTALSEARCHW
    COLUMNDROPDOWN = FIRST-64
    COLUMNOVERFLOWCLICK = FIRST-66
    BEGINSCROLL = FIRST-80
    ENDSCROLL = FIRST-81
    LINKCLICK = FIRST-84
    GETEMPTYMARKUP = FIRST-87

# class LVIF(IntEnum):
    # DISETITEM = 0x1000

class LVGIT(IntEnum):
    UNFOLDED = 0x0001
#
#  LVN_INCREMENTALSEARCH gives the app the opportunity to customize
#  incremental search.  For example, if the items are numeric,
#  the app can do numerical search instead of string search.
#
#  ListView notifies the app with NMLVFINDITEM.
#  The app sets pnmfi->lvfi.lParam to the result of the incremental search,
#  or to LVNSCH_DEFAULT if ListView should do the default search,
#  or to LVNSCH_ERROR to fail the search and just beep,
#  or to LVNSCH_IGNORE to stop all ListView processing.
#
#  The return value is not used.

class LVNSCH(IntEnum):
    DEFAULT = -1
    ERROR = -2
    IGNORE = -3

class EMF(IntEnum):
    CENTERED = 0x00000001


#define INDEXTOSTATEIMAGEMASK(i) ((i) << 12)

#define I_INDENTCALLBACK        (-1)

#define I_GROUPIDCALLBACK   (-1)
#define I_GROUPIDNONE       (-2)

class LVITEM(ctypes.Structure):
    _fields_ = [
        ('mask', UINT),
        ('iItem', INT),
        ('iSubItem', INT),
        ('state', UINT),
        ('stateMask', UINT),
        ('pszText', LPCWSTR),
        ('cchTextMax', INT),
        ('iImage', INT),
        ('lParam', LPARAM),
        ('iIndent', INT),
        ('iGroupId', INT),
        ('cColumns', UINT),
        ('puColumns', PUINT),
        ('piColFmt', PINT),
        ('iGroup', INT),
    ]

#define LPSTR_TEXTCALLBACKW     ((LPCWSTR)-1L)
#define LPSTR_TEXTCALLBACKA     ((LPSTR)-1L)

#define I_IMAGECALLBACK         (-1)
#define I_IMAGENONE             (-2)

#define I_COLUMNSCALLBACK       ((UINT)-1)

class LVFINDINFO(ctypes.Structure):
    _fields_ = [
        ('flags', UINT),
        ('psz', LPCWSTR),
        ('lParam', LPARAM),
        ('pt', POINT),
        ('vkDirection', UINT),
    ]

class LVHITTESTINFO(ctypes.Structure):
    _fields_ = [
        ('pt', POINT),
        ('flags', UINT),
        ('iItem', INT),
        ('iSubItem', INT),
        ('iGroup', INT),
    ]

class LVCOLUMN(ctypes.Structure):
    _fields_ = [
        ('mask', UINT),
        ('fmt', INT),
        ('cx', INT),
        ('pszText', LPCWSTR),
        ('cchTextMax', INT),
        ('iSubItem', INT),
        ('iImage', INT),
        ('iOrder', INT),
        ('cxMin', INT),
        ('cxDefault', INT),
        ('cxIdeal', INT),
    ]

# LVCFMT_ flags up to FFFF are shared with the header control (HDF_ flags).
# Flags above FFFF are listview-specific.

# these flags only apply to LVS_OWNERDATA listviews in report or list mode
#define LV_MAX_WORKAREAS         16

class LVBKIMAGE(ctypes.Structure):
    _fields_ = [
        ('ulFlags', ULONG),
        ('hbm', HBITMAP),
        ('pszImage', LPCWSTR),
        ('cchImageMax', UINT),
        ('xOffsetPercent', INT),
        ('yOffsetPercent', INT),
    ]

class LVGROUP(ctypes.Structure):
    _fields_ = [
        ('cbSize', UINT),
        ('mask', UINT),
        ('pszHeader', LPCWSTR),
        ('cchHeader', INT),
        ('pszFooter', LPCWSTR),
        ('cchFooter', INT),
        ('iGroupId', INT),
        ('stateMask', UINT),
        ('state', UINT),
        ('uAlign', UINT),
        ('pszSubtitle', LPCWSTR),
        ('cchSubtitle', UINT),
        ('pszTask', LPCWSTR),
        ('cchTask', UINT),
        ('pszDescriptionTop', LPCWSTR),
        ('cchDescriptionTop', UINT),
        ('pszDescriptionBottom', LPCWSTR),
        ('cchDescriptionBottom', UINT),
        ('iTitleImage', INT),
        ('iExtendedImage', INT),
        ('iFirstItem', INT),
        ('cItems', UINT),
        ('pszSubsetTitle', LPCWSTR),
        ('cchSubsetTitle', UINT),
    ]


class LVGROUPMETRICS(ctypes.Structure):
    _fields_ = [
        ('cbSize', UINT),
        ('mask', UINT),
        ('Left', UINT),
        ('Top', UINT),
        ('Right', UINT),
        ('Bottom', UINT),
        ('crLeft', INT),
        ('crTop', INT),
        ('crRight', INT),
        ('crBottom', INT),
        ('crHeader', INT),
        ('crFooter', INT),
    ]

class LVINSERTGROUPSORTED(ctypes.Structure):
    _fields_ = [
        ('pfnGroupCompare', PFNLVGROUPCOMPARE),
        ('pvData', ctypes.c_void_p),
        ('lvGroup', LVGROUP),
    ]

class LVTILEVIEWINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', UINT),
        ('dwMask', DWORD),
        ('dwFlags', DWORD),
        ('sizeTile', SIZE),
        ('cLines', INT),
        ('rcLabelMargin', RECT),
    ]

class LVTILEINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', UINT),
        ('iItem', INT),
        ('cColumns', UINT),
        ('puColumns', PUINT),
        ('piColFmt', PINT),
    ]

#define LVTILEINFO_V5_SIZE CCSIZEOF_STRUCT(LVTILEINFO, puColumns)
class LVINSERTMARK(ctypes.Structure):
    _fields_ = [
        ('cbSize', UINT),
        ('dwFlags', DWORD),
        ('iItem', INT),
        ('dwReserved', DWORD),
    ]

#define LVIM_AFTER      0x00000001 # TRUE = insert After iItem, otherwise before

class LVSETINFOTIP(ctypes.Structure):
    _fields_ = [
        ('cbSize', UINT),
        ('dwFlags', DWORD),
        ('pszText', LPCWSTR),
        ('iItem', INT),
        ('iSubItem', INT),
    ]

#define  LVM_SETINFOTIP         (LVM_FIRST + 173)
# These next to methods make it easy to identify an item that can be repositioned
# within listview. For example: Many developers use the lParam to store an identifier that is
# unique. Unfortunatly, in order to find this item, they have to iterate through all of the items
# in the listview. Listview will maintain a unique identifier.  The upper bound is the size of a DWORD.

class LVFOOTERINFO(ctypes.Structure):
    _fields_ = [
        ('mask', UINT),
        ('pszText', LPCWSTR),
        ('cchTextMax', INT),
        ('cItems', UINT),
    ]

class LVFOOTERITEM(ctypes.Structure):
    _fields_ = [
        ('mask', UINT),
        ('iItem', INT),
        ('pszText', LPCWSTR),
        ('cchTextMax', INT),
        ('state', UINT),
        ('stateMask', UINT),
    ]

class LVITEMINDEX(ctypes.Structure):
    _fields_ = [
        ('iItem', INT),
        ('iGroup', INT),
    ]

class NMLISTVIEW(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('iItem', INT),
        ('iSubItem', INT),
        ('uNewState', UINT),
        ('uOldState', UINT),
        ('uChanged', UINT),
        ('ptAction', POINT),
        ('lParam', LPARAM),
    ]

# NMITEMACTIVATE is used instead of NMLISTVIEW in IE >= 0x400
# therefore all the fields are the same except for extra uKeyFlags
# they are used to store key flags at the time of the single click with
# delayed activation - because by the time the timer goes off a user may
# not hold the keys (shift, ctrl) any more
class NMITEMACTIVATE(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('iItem', INT),
        ('iSubItem', INT),
        ('uNewState', UINT),
        ('uOldState', UINT),
        ('uChanged', UINT),
        ('ptAction', POINT),
        ('lParam', LPARAM),
        ('uKeyFlags', UINT),
    ]

# key flags stored in uKeyFlags
#define NMLVCUSTOMDRAW_V3_SIZE CCSIZEOF_STRUCT(NMLVCUSTOMDRAW, clrTextBk)
# class NMLVCUSTOMDRAW(ctypes.Structure):
    # _fields_ = [
        # ('nmcd', NMCUSTOMDRAW),
        # ('clrText', INT),
        # ('clrTextBk', INT),
        # ('iSubItem', INT),
        # ('dwItemType', DWORD),
        # # Item
        # ('clrFace', INT),
        # ('iIconEffect', INT),
        # ('iIconPhase', INT),
        # ('iPartId', INT),
        # ('iStateId', INT),
        # # Group
        # ('rcText', RECT),
        # ('uAlign', UINT),
    # ]

# dwItemType
# ListView custom draw return values
class NMLVCACHEHINT(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('iFrom', INT),
        ('iTo', INT),
    ]


class NMLVFINDITEM(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('iStart', INT),
        ('lvfi', LVFINDINFO),
    ]

class NMLVODSTATECHANGE(ctypes.Structure):
    _fields_ = [
            ('hdr', NMHDR),
        ('iFrom', INT),
        ('iTo', INT),
        ('uNewState', UINT),
        ('uOldState', UINT),
    ]

class LVDISPINFO(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('item', LVITEM),
    ]

class LVKEYDOWN(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('hdr', NMHDR),
        ('wVKey', WORD),
        ('flags', UINT),
    ]

# class NMLVLINK(ctypes.Structure):
    # _fields_ = [
        # ('hdr', NMHDR),
        # ('link', LITEM),
        # ('iItem', INT),
        # ('iSubItem', INT),
    # ]


class NMLVGETINFOTIP(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('dwFlags', DWORD),
        ('pszText', LPCWSTR),
        ('cchTextMax', INT),
        ('iItem', INT),
        ('iSubItem', INT),
        ('lParam', LPARAM),
    ]

class NMLVSCROLL(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('dx', INT),
        ('dy', INT),
    ]

L_MAX_URL_LENGTH = 2048 + 32 + len("://")
class NMLVEMPTYMARKUP(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        # out
        ('dwFlags', DWORD),
        ('szMarkup', WCHAR * L_MAX_URL_LENGTH),
    ]

# class LVS(IntEnum):
    # ICON = 0x0
    # REPORT = 0x1
    # SMALLICON = 0x2
    # LIST = 0x3
    # TYPEMASK = 0x3
    # SINGLESEL = 0x4
    # SHOWSELALWAYS = 0x8
    # SORTASCENDING = 0x10
    # SORTDESCENDING = 0x20
    # SHAREIMAGELISTS = 0x40
    # NOLABELWRAP = 0x80
    # AUTOARRANGE = 0x100
    # EDITLABELS = 0x200
    # OWNERDATA = 0x1000
    # NOSCROLL = 0x2000
    # TYPESTYLEMASK = 0xFC00
    # ALIGNTOP = 0x0
    # ALIGNLEFT = 0x800
    # ALIGNMASK = 0xC00
    # OWNERDRAWFIXED = 0x400
    # NOCOLUMNHEADER = 0x4000
    # NOSORTHEADER = 0x8000

# class LVS_EX(IntEnum):
    # GRIDLINES        = 0x00000001
    # SUBITEMIMAGES    = 0x00000002
    # CHECKBOXES       = 0x00000004
    # TRACKSELECT      = 0x00000008
    # HEADERDRAGDROP   = 0x00000010
    # FULLROWSELECT    = 0x00000020 # applies to report mode only
    # ONECLICKACTIVATE = 0x00000040
    # TWOCLICKACTIVATE = 0x00000080
    # FLATSB           = 0x00000100
    # REGIONAL         = 0x00000200
    # INFOTIP          = 0x00000400 # listview does InfoTips for you
    # UNDERLINEHOT     = 0x00000800
    # UNDERLINECOLD    = 0x00001000
    # MULTIWORKAREAS   = 0x00002000
    # LABELTIP         = 0x00004000 # listview unfolds partly hidden labels if it does not have infotip text
    # BORDERSELECT     = 0x00008000 # border selection style instead of highlight
    # # if (NTDDI_VERSION >= NTDDI_WINXP)
    # DOUBLEBUFFER     = 0x00010000
    # HIDELABELS       = 0x00020000
    # SINGLEROW        = 0x00040000
    # SNAPTOGRID       = 0x00080000  # Icons automatically snap to grid.
    # SIMPLESELECT     = 0x00100000  # Also changes overlay rendering to top right for icon mode.
    # # endif
    # # if (NTDDI_VERSION >= NTDDI_VISTA)
    # JUSTIFYCOLUMNS   = 0x00200000  # Icons are lined up in columns that use up the whole view area.
    # TRANSPARENTBKGND = 0x00400000  # Background is painted by the parent via WM_PRINTCLIENT
    # TRANSPARENTSHADOWTEXT = 0x00800000  # Enable shadow text on transparent backgrounds only (useful with bitmaps)
    # AUTOAUTOARRANGE  = 0x01000000  # Icons automatically arrange if no icon positions have been set
    # HEADERINALLVIEWS = 0x02000000  # Display column header in all view modes
    # AUTOCHECKSELECT  = 0x08000000
    # AUTOSIZECOLUMNS  = 0x10000000
    # COLUMNSNAPPOINTS = 0x40000000
    # COLUMNOVERFLOW   = 0x80000000

class LVM(IntEnum):
    FIRST = 0x1000
    SETUNICODEFORMAT = CCM.SETUNICODEFORMAT
    GETUNICODEFORMAT = CCM.GETUNICODEFORMAT
    GETBKCOLOR = FIRST+0
    SETBKCOLOR = FIRST+1
    GETIMAGELIST = FIRST+2
    SETIMAGELIST = FIRST+3
    GETITEMCOUNT = FIRST+4
    GETITEMA = FIRST+5
    GETITEMW = FIRST+75
    GETITEM = GETITEMW
    SETITEMA = FIRST+6
    SETITEMW = FIRST+76
    SETITEM = SETITEMW
    INSERTITEMA = FIRST+7
    INSERTITEMW = FIRST+77
    INSERTITEM = INSERTITEMW
    DELETEITEM = FIRST+8
    DELETEALLITEMS = FIRST+9
    GETCALLBACKMASK = FIRST+10
    SETCALLBACKMASK = FIRST+11
    GETNEXTITEM = FIRST+12
    FINDITEMA = FIRST+13
    FINDITEMW = FIRST+83
    GETITEMRECT = FIRST+14
    SETITEMPOSITION = FIRST+15
    GETITEMPOSITION = FIRST+16
    GETSTRINGWIDTHA = FIRST+17
    GETSTRINGWIDTHW = FIRST+87
    HITTEST = FIRST+18
    ENSUREVISIBLE = FIRST+19
    SCROLL = FIRST+20
    REDRAWITEMS = FIRST+21
    ARRANGE = FIRST+22
    EDITLABELA = FIRST+23
    EDITLABELW = FIRST+118
    GETEDITCONTROL = FIRST+24
    GETCOLUMNA = FIRST+25
    GETCOLUMNW = FIRST+95
    SETCOLUMNA = FIRST+26
    SETCOLUMNW = FIRST+96
    INSERTCOLUMNA = FIRST+27
    INSERTCOLUMNW = FIRST+97
    DELETECOLUMN = FIRST+28
    GETCOLUMNWIDTH = FIRST+29
    SETCOLUMNWIDTH = FIRST+30
    GETHEADER = FIRST+31
    CREATEDRAGIMAGE = FIRST+33
    GETVIEWRECT = FIRST+34
    GETTEXTCOLOR = FIRST+35
    SETTEXTCOLOR = FIRST+36
    GETTEXTBKCOLOR = FIRST+37
    SETTEXTBKCOLOR = FIRST+38
    GETTOPINDEX = FIRST+39
    GETCOUNTPERPAGE = FIRST+40
    GETORIGIN = FIRST+41
    UPDATE = FIRST+42
    SETITEMSTATE = FIRST+43
    GETITEMSTATE = FIRST+44
    GETITEMTEXTA = FIRST+45
    GETITEMTEXTW = FIRST+115
    SETITEMTEXTA = FIRST+46
    SETITEMTEXTW = FIRST+116
    SETITEMCOUNT = FIRST+47
    SORTITEMS = FIRST+48
    SETITEMPOSITION32 = FIRST+49
    GETSELECTEDCOUNT = FIRST+50
    GETITEMSPACING = FIRST+51
    GETISEARCHSTRINGA = FIRST+52
    GETISEARCHSTRINGW = FIRST+117
    SETICONSPACING = FIRST+53
    SETEXTENDEDLISTVIEWSTYLE = FIRST+54
    GETEXTENDEDLISTVIEWSTYLE = FIRST+55
    GETSUBITEMRECT = FIRST+56
    SUBITEMHITTEST = FIRST+57
    SETCOLUMNORDERARRAY = FIRST+58
    GETCOLUMNORDERARRAY = FIRST+59
    SETHOTITEM = FIRST+60
    GETHOTITEM = FIRST+61
    SETHOTCURSOR = FIRST+62
    GETHOTCURSOR = FIRST+63
    APPROXIMATEVIEWRECT = FIRST+64
    SETWORKAREAS = FIRST+65
    GETWORKAREAS = FIRST+70
    GETNUMBEROFWORKAREAS = FIRST+73
    GETSELECTIONMARK = FIRST+66
    SETSELECTIONMARK = FIRST+67
    SETHOVERTIME = FIRST+71
    GETHOVERTIME = FIRST+72
    SETTOOLTIPS = FIRST+74
    GETTOOLTIPS = FIRST+78
    SORTITEMSEX = FIRST+81
    SETBKIMAGEA = FIRST+68
    SETBKIMAGEW = FIRST+138
    GETBKIMAGEA = FIRST+69
    GETBKIMAGEW = FIRST+139
    SETSELECTEDCOLUMN = FIRST+140
    SETVIEW = FIRST+142
    GETVIEW = FIRST+143
    INSERTGROUP = FIRST+145
    SETGROUPINFO = FIRST+147
    GETGROUPINFO = FIRST+149
    REMOVEGROUP = FIRST+150
    MOVEGROUP = FIRST+151
    GETGROUPCOUNT = FIRST+152
    GETGROUPINFOBYINDEX = FIRST+153
    MOVEITEMTOGROUP = FIRST+154
    GETGROUPRECT = FIRST+98
    SETGROUPMETRICS = FIRST+155
    GETGROUPMETRICS = FIRST+156
    ENABLEGROUPVIEW = FIRST+157
    SORTGROUPS = FIRST+158
    INSERTGROUPSORTED = FIRST+159
    REMOVEALLGROUPS = FIRST+160
    HASGROUP = FIRST+161
    GETGROUPSTATE = FIRST+92
    GETFOCUSEDGROUP = FIRST+93
    SETTILEVIEWINFO = FIRST+162
    GETTILEVIEWINFO = FIRST+163
    SETTILEINFO = FIRST+164
    GETTILEINFO = FIRST+165
    SETINSERTMARK = FIRST+166
    GETINSERTMARK = FIRST+167
    INSERTMARKHITTEST = FIRST+168
    GETINSERTMARKRECT = FIRST+169
    SETINSERTMARKCOLOR = FIRST+170
    GETINSERTMARKCOLOR = FIRST+171
    GETSELECTEDCOLUMN = FIRST+174
    ISGROUPVIEWENABLED = FIRST+175
    GETOUTLINECOLOR = FIRST+176
    SETOUTLINECOLOR = FIRST+177
    CANCELEDITLABEL = FIRST+179
    MAPINDEXTOID = FIRST+180
    MAPIDTOINDEX = FIRST+181
    ISITEMVISIBLE = FIRST+182
    GETEMPTYTEXT = FIRST+204
    GETFOOTERRECT = FIRST+205
    GETFOOTERINFO = FIRST+206
    GETFOOTERITEMRECT = FIRST+207
    GETFOOTERITEM = FIRST+208
    GETITEMINDEXRECT = FIRST+209
    SETITEMINDEXSTATE = FIRST+210
    GETNEXTITEMINDEX = FIRST+211

# class LVCF(IntEnum):
    # FMT          = 0x0001
    # WIDTH        = 0x0002
    # TEXT         = 0x0004
    # SUBITEM      = 0x0008
    # IMAGE        = 0x0010
    # ORDER        = 0x0020
    # MINWIDTH     = 0x0040
    # DEFAULTWIDTH = 0x0080
    # IDEALWIDTH   = 0x0100

# class LVCFMT(IntEnum):
    # LEFT               = 0x0000
    # RIGHT              = 0x0001
    # CENTER             = 0x0002
    # JUSTIFYMASK        = 0x0003

    # IMAGE              = 0x0800
    # BITMAP_ON_RIGHT    = 0x1000
    # COL_HAS_IMAGES     = 0x8000

    # FIXED_WIDTH        = 0x00100
    # NO_DPI_SCALE       = 0x40000
    # FIXED_RATIO        = 0x80000

    # # The following flags
    # LINE_BREAK         = 0x100000
    # FILL               = 0x200000
    # WRAP               = 0x400000
    # NO_TITLE           = 0x800000
    # TILE_PLACEMENTMASK = LINE_BREAK | FILL

    # SPLITBUTTON        = 0x1000000

# class LVIF(IntEnum):
    # TEXT               = 0x00000001
    # IMAGE              = 0x00000002
    # PARAM              = 0x00000004
    # STATE              = 0x00000008
    # INDENT             = 0x00000010
    # NORECOMPUTE        = 0x00000800
    # GROUPID            = 0x00000100
    # COLUMNS            = 0x00000200
    # COLFMT             = 0x00010000  # The piColFmt member is valid in addition to puColumns

# class LVIS(IntEnum):
    # FOCUSED            = 0x0001
    # SELECTED           = 0x0002
    # CUT                = 0x0004
    # DROPHILITED        = 0x0008
    # GLOW               = 0x0010
    # ACTIVATING         = 0x0020

    # OVERLAYMASK        = 0x0F00
    # STATEIMAGEMASK     = 0xF000
    # # STATEIMAGEMASK = 0x3000

    # UNCHECKED          = 0x1000
    # CHECKED            = 0x2000


@dataclass
class ListView(Control):
    """
    A class representing a list view control.

    Attributes:
        style (int): The style of the list view control.
        windowClass (str): The window class associated with the list view control.
        __columns (list): The list of headers in the list view control.
        __rows (list): The list of rows in the list view control.

    Notification:
        onClick (WM_NotifyDelegator): Handler for the NM.CLICK notification.
        onCustomDraw (WM_NotifyDelegator): Handler for the NM.CUSTOMDRAW notification.
        onDblClk (WM_NotifyDelegator): Handler for the NM.DBLCLK notification.
        onKillFocus (WM_NotifyDelegator): Handler for the NM.KILLFOCUS notification.
        onRClick (WM_NotifyDelegator): Handler for the NM.RCLICK notification.
        onRDblClk (WM_NotifyDelegator): Handler for the NM.RDBLCLK notification.
        onReturn (WM_NotifyDelegator): Handler for the NM.RETURN notification.
        onSetCursor (WM_NotifyDelegator): Handler for the NM.SETCURSOR notification.
        onSetFocus (WM_NotifyDelegator): Handler for the NM.SETFOCUS notification.
        onHover (WM_NotifyDelegator): Handler for the NM.HOVER notification.
        onReleasedCapture (WM_NotifyDelegator): Handler for the NM.RELEASEDCAPTURE notification.

        onItemChanging (WM_NotifyDelegator): Handler for the LVN.ITEMCHANGING notification.
        onItemChanged (WM_NotifyDelegator): Handler for the LVN.ITEMCHANGED notification.
        onInsertItem (WM_NotifyDelegator): Handler for the LVN.INSERTITEM notification.
        onDeleteItem (WM_NotifyDelegator): Handler for the LVN.DELETEITEM notification.
        onDeleteAllItems (WM_NotifyDelegator): Handler for the LVN.DELETEALLITEMS notification.
        onBeginLabelEdit (WM_NotifyDelegator): Handler for the LVN.BEGINLABELEDIT notification.
        onEndLabelEdit (WM_NotifyDelegator): Handler for the LVN.ENDLABELEDIT notification.
        onColumnClick (WM_NotifyDelegator): Handler for the LVN.COLUMNCLICK notification.
        onBeginDrag (WM_NotifyDelegator): Handler for the LVN.BEGINDRAG notification.
        onBeginrDrag (WM_NotifyDelegator): Handler for the LVN.BEGINRDRAG notification.
        onOdCacheHint (WM_NotifyDelegator): Handler for the LVN.ODCACHEHINT notification.
        onItemActivate (WM_NotifyDelegator): Handler for the LVN.ITEMACTIVATE notification.
        onOdStateChanged (WM_NotifyDelegator): Handler for the LVN.ODSTATECHANGED notification.
        onOdFindItem (WM_NotifyDelegator): Handler for the LVN.ODFINDITEM notification.
        onHotTrack (WM_NotifyDelegator): Handler for the LVN.HOTTRACK notification.
        onGetDispInfo (WM_NotifyDelegator): Handler for the LVN.GETDISPINFO notification.
        onSetDispInfo (WM_NotifyDelegator): Handler for the LVN.SETDISPINFO notification.
        onKeyDown (WM_NotifyDelegator): Handler for the LVN.KEYDOWN notification.
        onMarqueeBegin (WM_NotifyDelegator): Handler for the LVN.MARQUEEBEGIN notification.
        onGetInfoTip (WM_NotifyDelegator): Handler for the LVN.GETINFOTIP notification.
        onIncrementalSearch (WM_NotifyDelegator): Handler for the LVN.INCREMENTALSEARCH notification.
        onColumnDropDown (WM_NotifyDelegator): Handler for the LVN.COLUMNDROPDOWN notification.
        onColumnOverflowClick (WM_NotifyDelegator): Handler for the LVN.COLUMNOVERFLOWCLICK notification.
        onBeginScroll (WM_NotifyDelegator): Handler for the LVN.BEGINSCROLL notification.
        onEndScroll (WM_NotifyDelegator): Handler for the LVN.ENDSCROLL notification.
        onLinkClick (WM_NotifyDelegator): Handler for the LVN.LINKCLICK notification.
        onGetEmptyMarkup (WM_NotifyDelegator): Handler for the LVN.GETEMPTYMARKUP notification.

    Methods:
        clear() -> None:
            Clear the list view by removing all items.

        addColumn() -> None:
        addColumns() -> None:

        addRow() -> None:
        addRows() -> None:

        getSelectedColumns() -> List[List[str]]:
        getSelectedRows() -> Dict[str: List[str]]:

    """
    style: int = Control.style | LVS.REPORT
    windowClass: str = 'SysListView32'
    __columns: list = None
    __rows: list = None
    show_headers: bool = False
    fit_last_column: bool = False

    onClick = WM_NotifyDelegator(NM.CLICK, None)
    onCustomDraw = WM_NotifyDelegator(NM.CUSTOMDRAW, None)
    onDblClk = WM_NotifyDelegator(NM.DBLCLK, None)
    onKillFocus = WM_NotifyDelegator(NM.KILLFOCUS, None)
    onRClick = WM_NotifyDelegator(NM.RCLICK, None)
    onRDblClk = WM_NotifyDelegator(NM.RDBLCLK, None)
    onReturn = WM_NotifyDelegator(NM.RETURN, None)
    onSetCursor = WM_NotifyDelegator(NM.SETCURSOR, None)
    onSetFocus = WM_NotifyDelegator(NM.SETFOCUS, None)
    onHover = WM_NotifyDelegator(NM.HOVER, None)
    onReleasedCapture = WM_NotifyDelegator(NM.RELEASEDCAPTURE, None)

    onItemChanging = WM_NotifyDelegator(LVN.ITEMCHANGING, None)
    onItemChanged = WM_NotifyDelegator(LVN.ITEMCHANGED, None)
    onInsertItem = WM_NotifyDelegator(LVN.INSERTITEM, None)
    onDeleteItem = WM_NotifyDelegator(LVN.DELETEITEM, None)
    onDeleteAllItems = WM_NotifyDelegator(LVN.DELETEALLITEMS, None)
    onBeginLabelEdit = WM_NotifyDelegator(LVN.BEGINLABELEDIT, None)
    onEndLabelEdit = WM_NotifyDelegator(LVN.ENDLABELEDIT, None)
    onColumnClick = WM_NotifyDelegator(LVN.COLUMNCLICK, None)
    onBeginDrag = WM_NotifyDelegator(LVN.BEGINDRAG, None)
    onBeginrDrag = WM_NotifyDelegator(LVN.BEGINRDRAG, None)
    onOdCacheHint = WM_NotifyDelegator(LVN.ODCACHEHINT, None)
    onItemActivate = WM_NotifyDelegator(LVN.ITEMACTIVATE, None)
    onOdStateChanged = WM_NotifyDelegator(LVN.ODSTATECHANGED, None)
    onOdFindItem = WM_NotifyDelegator(LVN.ODFINDITEM, None)
    onHotTrack = WM_NotifyDelegator(LVN.HOTTRACK, None)
    onGetDispInfo = WM_NotifyDelegator(LVN.GETDISPINFO, None)
    onSetDispInfo = WM_NotifyDelegator(LVN.SETDISPINFO, None)
    onKeyDown = WM_NotifyDelegator(LVN.KEYDOWN, None)
    onMarqueeBegin = WM_NotifyDelegator(LVN.MARQUEEBEGIN, None)
    onGetInfoTip = WM_NotifyDelegator(LVN.GETINFOTIP, None)
    onIncrementalSearch = WM_NotifyDelegator(LVN.INCREMENTALSEARCH, None)
    onColumnDropDown = WM_NotifyDelegator(LVN.COLUMNDROPDOWN, None)
    onColumnOverflowClick = WM_NotifyDelegator(LVN.COLUMNOVERFLOWCLICK, None)
    onBeginScroll = WM_NotifyDelegator(LVN.BEGINSCROLL, None)
    onEndScroll = WM_NotifyDelegator(LVN.ENDSCROLL, None)
    onLinkClick = WM_NotifyDelegator(LVN.LINKCLICK, None)
    onGetEmptyMarkup = WM_NotifyDelegator(LVN.GETEMPTYMARKUP, None)


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

    def insertItems(self):
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
            SendMessage(self.hwnd, LVM.SETCOLUMNWIDTH, i, LVSCW.AUTOSIZE)


    def clear(self):
        SendMessage(self.hwnd, LVM.DELETEALLITEMS, 0, 0)

    def addColumns(self):
        self.column_count = len(self.columns)
        for i in range(self.column_count):
            self.insertColumn(i, self.columns[i])
        SendMessage(self.hwnd, LVM.SETEXTENDEDLISTVIEWSTYLE, LVS_EX.CHECKBOXES, LVS_EX.CHECKBOXES)

    def getSelectedRows(self):
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

    # def DeleteColumns(self):
    #     for i in range(self.column_number):
    #         self.DeleteColumn(0)

    # *************************************************************************
    # generated

    def setUnicodeFormat(self, fUnicode):
        return SendMessage(self.hwnd, LVM.SETUNICODEFORMAT, fUnicode, 0)  # BOOL

    def getUnicodeFormat(self):
        return SendMessage(self.hwnd, LVM.GETUNICODEFORMAT, 0, 0)  # BOOL

    def getBkColor(self):
        return SendMessage(self.hwnd, LVM.GETBKCOLOR, 0, 0)  # INT

    def setBkColor(self, clrBk):
        return SendMessage(self.hwnd, LVM.SETBKCOLOR, 0, INT(clrBk))  # BOOL

    def getImageList(self, iImageList):
        return SendMessage(self.hwnd, LVM.GETIMAGELIST, INT(iImageList), 0)  # HIMAGELIST

    # def setImageList(self, himl, iImageList):
        # return SendMessage(self.hwnd, LVM.SETIMAGELIST, iImageList, HIMAGELIST(himl))  # HIMAGELIST

    def getItemCount(self):
        return SendMessage(self.hwnd, LVM.GETITEMCOUNT, 0, 0)  # int

    # def getItem(self, pitem):
        # return SendMessage(self.hwnd, LVM.GETITEM, 0, (LPARAM)(LV_ITEM *)(pitem))  # BOOL

    # def setItem(self, pitem):
        # return SendMessage(self.hwnd, LVM.SETITEM, 0, (LPARAM)(const LV_ITEM *)(pitem))  # BOOL

    # def insertItem(self, pitem):
        # return SendMessage(self.hwnd, LVM.INSERTITEM, 0, (LPARAM)(const LV_ITEM *)(pitem))  # int

    def deleteItem(self, i):
        return SendMessage(self.hwnd, LVM.DELETEITEM, int(i), 0)  # BOOL

    def deleteAllItems(self):
        return SendMessage(self.hwnd, LVM.DELETEALLITEMS, 0, 0)  # BOOL

    def getCallbackMask(self):
        return SendMessage(self.hwnd, LVM.GETCALLBACKMASK, 0, 0)  # BOOL

    def setCallbackMask(self, mask):
        return SendMessage(self.hwnd, LVM.SETCALLBACKMASK, UINT(mask), 0)  # BOOL

    def getNextItem(self, i, flags):
        return SendMessage(self.hwnd, LVM.GETNEXTITEM, int(i), MAKELPARAM((flags), 0))  # int

    # def findItem(iStart, plvfi):
        # return SendMessage(self.hwnd, LVM.FINDITEM, int(iStart), (LPARAM)(const LV_FINDINFO *)(plvfi))  # int

    # def getItemRect(i, prc, code):
        # return SendMessage(self.hwnd,
                           # LVM.GETITEMRECT,
                           # i,
                           # ((prc) ? (((RECT *)(prc))->left = (code),(LPARAM)(RECT *)(prc)): (LPARAM)(RECT *)NULL))  # BOOL

    def setItemPosition(self, i, x, y):
        return SendMessage(self.hwnd, LVM.SETITEMPOSITION, int(i), MAKELPARAM((x), (y)))  # BOOL

    # def getItemPosition(i, ppt):
        # return SendMessage(self.hwnd, LVM.GETITEMPOSITION, int(i), (LPARAM)(POINT *)(ppt))  # BOOL

    def getStringWidth(self, psz):
        return SendMessage(self.hwnd, LVM.GETSTRINGWIDTH, 0, LPCWSTR(psz))  # int

    # def hitTest(self, pinfo):
        # return SendMessage(self.hwnd, LVM.HITTEST, 0, (LPARAM)(LV_HITTESTINFO *)(pinfo))  # int

    # def hitTestEx(self, pinfo):
        # return SendMessage(self.hwnd, LVM.HITTEST, (WPARAM)-1, (LPARAM)(LV_HITTESTINFO *)(pinfo))  # int

    def ensureVisible(self, i, fPartialOK):
        return SendMessage(self.hwnd, LVM.ENSUREVISIBLE, int(i), MAKELPARAM((fPartialOK), 0))  # BOOL

    def scroll(self, dx, dy):
        return SendMessage(self.hwnd, LVM.SCROLL, int(dx), int(dy))  # BOOL

    def redrawItems(self, iFirst, iLast):
        return SendMessage(self.hwnd, LVM.REDRAWITEMS, int(iFirst), int(iLast))  # BOOL

    def arrange(self, code):
        return SendMessage(self.hwnd, LVM.ARRANGE, UINT(code), 0)  # BOOL

    def editLabel(self, i):
        return SendMessage(self.hwnd, LVM.EDITLABEL, int(i), 0)  # HWND

    def getEditControl(self):
        return SendMessage(self.hwnd, LVM.GETEDITCONTROL, 0, 0)  # HWND

    # def getColumn(column_index, pcol):
        # return SendMessage(self.hwnd, LVM.GETCOLUMN, int(column_index), (LPARAM)(LV_COLUMN *)(pcol))  # BOOL

    # def setColumn(column_index, pcol):
        # return SendMessage(self.hwnd, LVM.SETCOLUMN, int(column_index), (LPARAM)(const LV_COLUMN *)(pcol))  # BOOL

    def insertColumn(self, index, name):
        item = LVCOLUMN()
        item.mask = LVCF.TEXT | LVCF.FMT # | LVCF.SUBITEM
        item.fmt = LVCFMT.LEFT
        item.cx = 50
        item.pszText = name
        item.cchTextMax = len(name)
        return SendMessage(self.hwnd, LVM.INSERTCOLUMN, index, ctypes.addressof(item))  # int

    def deleteColumn(self, column_index):
        return SendMessage(self.hwnd, LVM.DELETECOLUMN, int(column_index), 0)  # BOOL

    def getColumnWidth(self, column_index):
        return SendMessage(self.hwnd, LVM.GETCOLUMNWIDTH, int(column_index), 0)  # int

    def setColumnWidth(self, column_index, cx):
        return SendMessage(self.hwnd, LVM.SETCOLUMNWIDTH, int(column_index), MAKELPARAM((cx), 0))  # BOOL
    def GetHeader(self):
        return SendMessage(self.hwnd, LVM.GETHEADER, 0, 0)  # HWND

    # def createDragImage(self, i, lpptUpLeft):
        # return SendMessage(self.hwnd, LVM.CREATEDRAGIMAGE, int(i), LPPOINT(lpptUpLeft))  # HIMAGELIST

    # def getViewRect(self, prc):
        # return SendMessage(self.hwnd, LVM.GETVIEWRECT, 0, (LPARAM)(RECT *)(prc))  # BOOL

    def getTextColor(self):
        return SendMessage(self.hwnd, LVM.GETTEXTCOLOR, 0, 0)  # INT

    def setTextColor(self, clrText):
        return SendMessage(self.hwnd, LVM.SETTEXTCOLOR, 0, INT(clrText))  # BOOL

    def getTextBkColor(self):
        return SendMessage(self.hwnd, LVM.GETTEXTBKCOLOR, 0, 0)  # INT

    def setTextBkColor(self, clrTextBk):
        return SendMessage(self.hwnd, LVM.SETTEXTBKCOLOR, 0, INT(clrTextBk))  # BOOL

    def getTopIndex(self):
        return SendMessage(self.hwnd, LVM.GETTOPINDEX, 0, 0)  # int

    def getCountPerPage(self):
        return SendMessage(self.hwnd, LVM.GETCOUNTPERPAGE, 0, 0)  # int

    # def getOrigin(self, ppt):
        # return SendMessage(self.hwnd, LVM.GETORIGIN, 0, (LPARAM)(POINT *)(ppt))  # BOOL

    def update(self, i):
        return SendMessage(self.hwnd, LVM.UPDATE, i, 0)  # BOOL

    # def setItemState(i, data, mask):
        # LV_ITEM _macro_lvi;  _macro_lvi.stateMask = (mask);  _macro_lvi.state = (data)
        # SendMessage(self.hwnd, LVM.SETITEMSTATE, i, (LPARAM)(LV_ITEM *)&_macro_lvi)

    # def setCheckState(i, fCheck):
        # ListView_SetItemState(i, INDEXTOSTATEIMAGEMASK((fCheck)?2:1), LVIS_STATEIMAGEMASK)

    def getItemState(self, i, mask):
        return SendMessage(self.hwnd, LVM.GETITEMSTATE, i, mask)  # UINT

    # def getCheckState(self, i):
       # ((((UINT)(SendMessage(self.hwnd, LVM.GETITEMSTATE, i, LVIS_STATEIMAGEMASK))) >> 12) -1)

    # def getItemText(i, iSubItem_, pszText_, cchTextMax_):
        # LV_ITEM _macro_lvi;  _macro_lvi.iSubItem = (iSubItem_);  _macro_lvi.cchTextMax = (cchTextMax_);  _macro_lvi.pszText = (pszText_)
        # SendMessage(self.hwnd, LVM.GETITEMTEXT, i, (LPARAM)(LV_ITEM *)&_macro_lvi)

    # def setItemText(i, iSubItem_, pszText_):
        # LV_ITEM _macro_lvi;  _macro_lvi.iSubItem = (iSubItem_);  _macro_lvi.pszText = (pszText_)
        # SendMessage(self.hwnd, LVM.SETITEMTEXT, i, (LPARAM)(LV_ITEM *)&_macro_lvi)

    def setItemCount(self, cItems):
        SendMessage(self.hwnd, LVM.SETITEMCOUNT, cItems, 0)

    def setItemCountEx(self, cItems, dwFlags):
        SendMessage(self.hwnd, LVM.SETITEMCOUNT, cItems, dwFlags)

    def sortItems(self, _pfnCompare, _lPrm):
        return SendMessage(self.hwnd, LVM.SORTITEMS, LPARAM(_lPrm),   PFNLVCOMPARE(_pfnCompare))  # BOOL

    # def setItemPosition32(i, x0, y0):
        # POINT ptNewPos;     ptNewPos.x = (x0); ptNewPos.y = (y0)
        # SendMessage(self.hwnd, LVM.SETITEMPOSITION32, int(i), (LPARAM)&ptNewPos)

    def getSelectedCount(self):
        return SendMessage(self.hwnd, LVM.GETSELECTEDCOUNT, 0, 0)  # UINT

    def getItemSpacing(self, fSmall):
        return SendMessage(self.hwnd, LVM.GETITEMSPACING, fSmall, 0)  # DWORD

    def getISearchString(self, lpsz):
        return SendMessage(self.hwnd, LVM.GETISEARCHSTRING, 0, LPCWSTR(lpsz))  # BOOL

    def setIconSpacing(self, cx, cy):
        return SendMessage(self.hwnd, LVM.SETICONSPACING, 0, MAKELONG(cx,cy))  # DWORD

    def SetExtendedListViewStyle(self, dw):
        return SendMessage(self.hwnd, LVM.SETEXTENDEDLISTVIEWSTYLE, 0, dw)  # DWORD

    def SetExtendedListViewStyleEx(self, dwMask, dw):
        return SendMessage(self.hwnd, LVM.SETEXTENDEDLISTVIEWSTYLE, dwMask, dw)  # DWORD

    def GetExtendedListViewStyle(self):
        return SendMessage(self.hwnd, LVM.GETEXTENDEDLISTVIEWSTYLE, 0, 0)  # DWORD

    # def getSubItemRect(iItem, iSubItem, code, prc):
        # return SendMessage(self.hwnd,
                           # LVM.GETSUBITEMRECT, int(iItem),
                           # ((prc) ? ((((LPRECT)(prc))->top = (iSubItem)), (((LPRECT)(prc))->left = (code)), prc): LPRECTNULL))  # BOOL

    # def subItemHitTest(self, plvhti):
        # return SendMessage(self.hwnd, LVM.SUBITEMHITTEST, 0, LPLVHITTESTINFO(plvhti))  # int

    # def subItemHitTestEx(self, plvhti):
        # return SendMessage(self.hwnd, LVM.SUBITEMHITTEST, -1, LPLVHITTESTINFO(plvhti))  # int

    # def setColumnOrderArray(iCount, pi):
        # return SendMessage(self.hwnd, LVM.SETCOLUMNORDERARRAY, iCount, LPINT(pi))  # BOOL

    # def getColumnOrderArray(iCount, pi):
        # return SendMessage(self.hwnd, LVM.GETCOLUMNORDERARRAY, iCount, LPINT(pi))  # BOOL

    def setHotItem(self, i):
        return SendMessage(self.hwnd, LVM.SETHOTITEM, i, 0)  # int

    def getHotItem(self):
        return SendMessage(self.hwnd, LVM.GETHOTITEM, 0, 0)  # int

    def setHotCursor(self, hcur):
        return SendMessage(self.hwnd, LVM.SETHOTCURSOR, 0, hcur)  # HCURSOR

    def getHotCursor(self):
        return SendMessage(self.hwnd, LVM.GETHOTCURSOR, 0, 0)  # HCURSOR

    def approximateViewRect(self, iWidth, iHeight, iCount):
        return SendMessage(self.hwnd, LVM.APPROXIMATEVIEWRECT, iCount, MAKELPARAM(iWidth, iHeight))  # DWORD

    # def setWorkAreas(nWorkAreas, prc):
        # return SendMessage(self.hwnd, LVM.SETWORKAREAS, int(nWorkAreas), (LPARAM)(RECT *)(prc))  # BOOL

    # def getWorkAreas(nWorkAreas, prc):
        # return SendMessage(self.hwnd, LVM.GETWORKAREAS, int(nWorkAreas), (LPARAM)(RECT *)(prc))  # BOOL

    # def getNumberOfWorkAreas(self, pnWorkAreas):
        # return SendMessage(self.hwnd, LVM.GETNUMBEROFWORKAREAS, 0, (LPARAM)(UINT *)(pnWorkAreas))  # BOOL

    def getSelectionMark(self):
        return SendMessage(self.hwnd, LVM.GETSELECTIONMARK, 0, 0)  # int

    def setSelectionMark(self, i):
        return SendMessage(self.hwnd, LVM.SETSELECTIONMARK, 0, i)  # int

    def SetHoverTime(self, dwHoverTimeMs):
        return SendMessage(self.hwnd, LVM.SETHOVERTIME, 0, dwHoverTimeMs)  # DWORD

    def GetHoverTime(self):
        return SendMessage(self.hwnd, LVM.GETHOVERTIME, 0, 0)  # DWORD

    def SetToolTips(self, hwndNewHwnd):
        return SendMessage(self.hwnd, LVM.SETTOOLTIPS, hwndNewHwnd, 0)  # HWND

    def GetToolTips(self):
        return SendMessage(self.hwnd, LVM.GETTOOLTIPS, 0, 0)  # HWND

    def sortItemsEx(self, _pfnCompare, _lPrm):
        return SendMessage(self.hwnd, LVM.SORTITEMSEX, LPARAM(_lPrm), PFNLVCOMPARE(_pfnCompare))  # BOOL

    def setSelectedColumn(self, column_index):
        SendMessage(self.hwnd, LVM.SETSELECTEDCOLUMN, column_index, 0)

    def setView(self, iView):
        return SendMessage(self.hwnd, LVM.SETVIEW, DWORD(iView), 0)  # DWORD

    def getView(self):
        return SendMessage(self.hwnd, LVM.GETVIEW, 0, 0)  # DWORD

    def insertGroup(self, index, pgrp):
        SendMessage(self.hwnd, LVM.INSERTGROUP, index, pgrp)

    def setGroupInfo(self, iGroupId, pgrp):
        SendMessage(self.hwnd, LVM.SETGROUPINFO, iGroupId, pgrp)

    def getGroupInfo(self, iGroupId, pgrp):
        SendMessage(self.hwnd, LVM.GETGROUPINFO, iGroupId, pgrp)

    def removeGroup(self, iGroupId):
        SendMessage(self.hwnd, LVM.REMOVEGROUP, iGroupId, 0)

    def moveGroup(self, iGroupId, toIndex):
        SendMessage(self.hwnd, LVM.MOVEGROUP, iGroupId, toIndex)

    def getGroupCount(self):
        SendMessage(self.hwnd, LVM.GETGROUPCOUNT, 0, 0)

    def getGroupInfoByIndex(self, iIndex, pgrp):
        SendMessage(self.hwnd, LVM.GETGROUPINFOBYINDEX, iIndex, pgrp)

    def moveItemToGroup(self, idItemFrom, idGroupTo):
        SendMessage(self.hwnd, LVM.MOVEITEMTOGROUP, idItemFrom, idGroupTo)

    # def getGroupRect(iGroupId, type, prc):
        # SendMessage(self.hwnd, LVM.GETGROUPRECT, iGroupId, ((prc) ? (((RECT*)(prc))->top = (type)), (LPARAM)(RECT*)(prc): (LPARAM)(RECT*)NULL))

    def setGroupMetrics(self, pGroupMetrics):
        SendMessage(self.hwnd, LVM.SETGROUPMETRICS, 0, pGroupMetrics)

    def getGroupMetrics(self, pGroupMetrics):
        SendMessage(self.hwnd, LVM.GETGROUPMETRICS, 0, pGroupMetrics)

    def enableGroupView(self, fEnable):
        SendMessage(self.hwnd, LVM.ENABLEGROUPVIEW, fEnable, 0)

    def sortGroups(self, _pfnGroupCompate, _plv):
        SendMessage(self.hwnd, LVM.SORTGROUPS, _pfnGroupCompate, _plv)

    def insertGroupSorted(self, structInsert):
        SendMessage(self.hwnd, LVM.INSERTGROUPSORTED, structInsert, 0)

    def removeAllGroups(self):
        SendMessage(self.hwnd, LVM.REMOVEALLGROUPS, 0, 0)

    def hasGroup(self, dwGroupId):
        SendMessage(self.hwnd, LVM.HASGROUP, dwGroupId, 0)

    # def setGroupState(dwGroupId, dwMask, dwState):
        # LVGROUP _macro_lvg
        # _macro_lvg.cbSize = sizeof(_macro_lvg)
        # _macro_lvg.mask = LVGF_STATE
        # _macro_lvg.stateMask = dwMask
        # _macro_lvg.state = dwState
        # SendMessage(self.hwnd, LVM.SETGROUPINFO, dwGroupId, (LPARAM)(LVGROUP *)&_macro_lvg)

    def getGroupState(self, dwGroupId, dwMask):
        return SendMessage(self.hwnd, LVM.GETGROUPSTATE, dwGroupId, dwMask)  # uint

    def getFocusedGroup(self):
        SendMessage(self.hwnd, LVM.GETFOCUSEDGROUP, 0, 0)

    def setTileViewInfo(self, ptvi):
        SendMessage(self.hwnd, LVM.SETTILEVIEWINFO, 0, ptvi)

    def getTileViewInfo(self, ptvi):
        SendMessage(self.hwnd, LVM.GETTILEVIEWINFO, 0, ptvi)

    def setTileInfo(self, pti):
        SendMessage(self.hwnd, LVM.SETTILEINFO, 0, pti)

    def getTileInfo(self, pti):
        SendMessage(self.hwnd, LVM.GETTILEINFO, 0, pti)

    def setInsertMark(self, lvim):
        return SendMessage(self.hwnd, LVM.SETINSERTMARK, 0, (LPARAM) (lvim))  # BOOL

    def getInsertMark(self, lvim):
        return SendMessage(self.hwnd, LVM.GETINSERTMARK, 0, (LPARAM) (lvim))  # BOOL

    # def insertMarkHitTest(self, point, lvim):
        # return SendMessage(self.hwnd, LVM.INSERTMARKHITTEST, LPPOINT(point), LPLVINSERTMARK(lvim))  # int

    # def getInsertMarkRect(self, rc):
        # return SendMessage(self.hwnd, LVM.GETINSERTMARKRECT, 0, LPRECT(rc))  # int

    def setInsertMarkColor(self, color):
        return SendMessage(self.hwnd, LVM.SETINSERTMARKCOLOR, 0, INT(color))  # INT

    def getInsertMarkColor(self):
        return SendMessage(self.hwnd, LVM.GETINSERTMARKCOLOR, 0, 0)  # INT

    def SetInfoTip(self, plvInfoTip):
        return SendMessage(self.hwnd, LVM.SETINFOTIP, 0, plvInfoTip)  # BOOL

    def getSelectedColumn(self):
        return SendMessage(self.hwnd, LVM.GETSELECTEDCOLUMN, 0, 0)  # UINT

    def isGroupViewEnabled(self):
        return SendMessage(self.hwnd, LVM.ISGROUPVIEWENABLED, 0, 0)  # BOOL

    def getOutlineColor(self):
        return SendMessage(self.hwnd, LVM.GETOUTLINECOLOR, 0, 0)  # INT

    def setOutlineColor(self, color):
        return SendMessage(self.hwnd, LVM.SETOUTLINECOLOR, 0, INT(color))  # INT

    def cancelEditLabel(self):
        SendMessage(self.hwnd, LVM.CANCELEDITLABEL, 0, 0)

    def mapIndexToID(self, index):
        return SendMessage(self.hwnd, LVM.MAPINDEXTOID, index, 0)  # UINT

    def mapIDToIndex(self, id):
        return SendMessage(self.hwnd, LVM.MAPIDTOINDEX, id, 0)  # UINT

    def isItemVisible(self, index):
        return SendMessage(self.hwnd, LVM.ISITEMVISIBLE, index, 0)  # UINT

    # def setGroupHeaderImageList(self, himl):
        # return SendMessage(self.hwnd, LVM.SETIMAGELIST, (WPARAM)LVSIL_GROUPHEADER, HIMAGELIST(himl))  # HIMAGELIST

    # def getGroupHeaderImageList(self):
        # return SendMessage(self.hwnd, LVM.GETIMAGELIST, (WPARAM)LVSIL_GROUPHEADER, 0)  # HIMAGELIST

    def getEmptyText(self, pszText, cchText):
        return SendMessage(self.hwnd, LVM.GETEMPTYTEXT, cchText, pszText)  # BOOL

    def getFooterRect(self, prc):
        return SendMessage(self.hwnd, LVM.GETFOOTERRECT, 0, prc)  # BOOL

    def getFooterInfo(self, plvfi):
        return SendMessage(self.hwnd, LVM.GETFOOTERINFO, 0, plvfi)  # BOOL

    def getFooterItemRect(self, iItem, prc):
        return SendMessage(self.hwnd, LVM.GETFOOTERITEMRECT, iItem, prc)  # BOOL

    def getFooterItem(self, iItem, pfi):
        return SendMessage(self.hwnd, LVM.GETFOOTERITEM, iItem, pfi)  # BOOL

    # def getItemIndexRect(plvii, iSubItem, code, prc):
        # return SendMessage(self.hwnd,
                           # LVM.GETITEMINDEXRECT,
                           # (WPARAM)(LVITEMINDEX*)(plvii),
                           # ((prc) ? ((((LPRECT)(prc))->top = (iSubItem)), (((LPRECT)(prc))->left = (code)), prc): LPRECTNULL))  # BOOL

    # def setItemIndexState(plvii, data, mask):
        # LV_ITEM _macro_lvi;  _macro_lvi.stateMask = (mask);  _macro_lvi.state = (data)
        # SendMessage(self.hwnd, LVM.SETITEMINDEXSTATE, (WPARAM)(LVITEMINDEX*)(plvii), (LPARAM)(LV_ITEM *)&_macro_lvi)

    # def getNextItemIndex(plvii, flags):
        # return SendMessage(self.hwnd, LVM.GETNEXTITEMINDEX, (WPARAM)(LVITEMINDEX*)(plvii), MAKELPARAM((flags), 0))  # BOOL

    def setBkImage(self, plvbki):
        return SendMessage(self.hwnd, LVM.SETBKIMAGE, 0, plvbki)  # BOOL

    def getBkImage(self, plvbki):
        return SendMessage(self.hwnd, LVM.GETBKIMAGE, 0, plvbki)  # BOOL

