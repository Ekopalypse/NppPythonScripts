'''
SYSTREEVIEW32 Control Implementations

Example Usage:
    from WinDialog import TreeView

    # Create a tree view control
    treeview = TreeView('',(100, 10), (10, 10))

For detailed documentation, refer to their respective docstrings.
'''
import ctypes
from ctypes.wintypes import INT, UINT, HWND, LPCWSTR, LPARAM, POINT, LONG, WORD
from dataclasses import dataclass
from enum import IntEnum
from .__control_template import Control
from ..win_helper import (
    SendMessage, MAKELPARAM,
    NMHDR, NM, CCM, WindowStyle as WS,
    WM_NotifyDelegator
)


class TVS(IntEnum):
    HASBUTTONS = 0x0001
    HASLINES = 0x0002
    LINESATROOT = 0x0004
    EDITLABELS = 0x0008
    DISABLEDRAGDROP = 0x0010
    SHOWSELALWAYS = 0x0020
    RTLREADING = 0x0040
    NOTOOLTIPS = 0x0080
    CHECKBOXES = 0x0100
    TRACKSELECT = 0x0200
    SINGLEEXPAND = 0x0400
    INFOTIP = 0x0800
    FULLROWSELECT = 0x1000
    NOSCROLL = 0x2000
    NONEVENHEIGHT = 0x4000
    NOHSCROLL = 0x8000


class TVS_EX(IntEnum):
    NOSINGLECOLLAPSE = 0x0001
    MULTISELECT = 0x0002
    DOUBLEBUFFER = 0x0004
    NOINDENTSTATE = 0x0008
    RICHTOOLTIP = 0x0010
    AUTOHSCROLL = 0x0020
    FADEINOUTEXPANDOS = 0x0040
    PARTIALCHECKBOXES = 0x0080
    EXCLUSIONCHECKBOXES = 0x0100
    DIMMEDCHECKBOXES = 0x0200
    DRAWIMAGEASYNC = 0x0400


HTREEITEM = ctypes.c_void_p
HRESULT = LONG

class TVIF(IntEnum):
    TEXT = 0x0001
    IMAGE = 0x0002
    PARAM = 0x0004
    STATE = 0x0008
    HANDLE = 0x0010
    SELECTEDIMAGE = 0x0020
    CHILDREN = 0x0040
    INTEGRAL = 0x0080
    STATEEX = 0x0100
    EXPANDEDIMAGE = 0x0200


class TVIS(IntEnum):
    SELECTED = 0x0002
    CUT = 0x0004
    DROPHILITED = 0x0008
    BOLD = 0x0010
    EXPANDED = 0x0020
    EXPANDEDONCE = 0x0040
    EXPANDPARTIAL = 0x0080
    OVERLAYMASK = 0x0F00
    STATEIMAGEMASK = 0xF000
    USERMASK = 0xF000


class TVIS_EX(IntEnum):
    FLAT = 0x0001
    DISABLED = 0x0002
    ALL = 0x0002


# Structure for TreeView's NM_TVSTATEIMAGECHANGING notification
class NMTVSTATEIMAGECHANGING(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('hti', HTREEITEM),
        ('iOldStateImageIndex', INT),
        ('iNewStateImageIndex', INT),
    ]


I_CHILDRENCALLBACK = -1
I_CHILDRENAUTO     = -2


class TVITEM(ctypes.Structure):
    _fields_ = [
        ('mask', UINT),
        ('hItem', HTREEITEM),
        ('state', UINT),
        ('stateMask', UINT),
        ('pszText', LPCWSTR),
        ('cchTextMax', INT),
        ('iImage', INT),
        ('iSelectedImage', INT),
        ('cChildren', INT),
        ('lParam', LPARAM),
    ]


# only used for Get and Set messages.  no notifies
class TVITEMEX(ctypes.Structure):
    _fields_ = [
        ('mask', UINT),
        ('hItem', HTREEITEM),
        ('state', UINT),
        ('stateMask', UINT),
        ('pszText', LPCWSTR),
        ('cchTextMax', INT),
        ('iImage', INT),
        ('iSelectedImage', INT),
        ('cChildren', INT),
        ('lParam', LPARAM),
        ('iIntegral', INT),
        ('uStateEx', UINT),
        ('hwnd', HWND),
        ('iExpandedImage', INT),
        ('iReserved', INT),
    ]


class TVI(IntEnum):
    ROOT = -0x10000  # ((HTREEITEM)(ULONG_PTR)-0x10000)
    FIRST = -0x0FFFF  # ((HTREEITEM)(ULONG_PTR)-0x0FFFF)
    LAST = -0x0FFFE  # ((HTREEITEM)(ULONG_PTR)-0x0FFFE)
    SORT = -0x0FFFD  # ((HTREEITEM)(ULONG_PTR)-0x0FFFD)

class _U(ctypes.Union):
    _fields_ = [
        ('itemex', TVITEMEX),
        ('item', TVITEM),
    ]

class TVINSERTSTRUCT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ('hParent', HTREEITEM),
        ('hInsertAfter', HTREEITEM),
        ("u", _U),
    ]


class TVE(IntEnum):
    COLLAPSE = 0x0001
    EXPAND = 0x0002
    TOGGLE = 0x0003
    EXPANDPARTIAL = 0x4000
    COLLAPSERESET = 0x8000


class TVSIL(IntEnum):
    NORMAL = 0
    STATE = 2


class TVSI(IntEnum):
    ROOT = 0x0000
    NEXT = 0x0001
    PREVIOUS = 0x0002
    PARENT = 0x0003
    CHILD = 0x0004
    FIRSTVISIBLE = 0x0005
    NEXTVISIBLE = 0x0006
    PREVIOUSVISIBLE = 0x0007
    DROPHILITE = 0x0008
    CARET = 0x0009
    LASTVISIBLE = 0x000A
    NEXTSELECTED = 0x000B
    NOSINGLEEXPAND = 0x8000


class TVHITTESTINFO(ctypes.Structure):
    _fields_ = [
        ('pt', POINT),
        ('flags', UINT),
        ('hItem', HTREEITEM),
    ]


class TVHT(IntEnum):
    NOWHERE = 0x0001
    ONITEMICON = 0x0002
    ONITEMLABEL = 0x0004
    ONITEMINDENT = 0x0008
    ONITEMBUTTON = 0x0010
    ONITEMRIGHT = 0x0020
    ONITEMSTATEICON = 0x0040
    ONITEM = ONITEMICON | ONITEMLABEL | ONITEMSTATEICON
    ABOVE = 0x0100
    BELOW = 0x0200
    TORIGHT = 0x0400
    TOLEFT = 0x0800


class TVSBF(IntEnum):
    XBORDER = 0x00000001
    YBORDER = 0x00000002


# class TVITEMPART(IntEnum):
    # TVGIPR_BUTTON = 0x0001


# class TVGETITEMPARTRECTINFO(ctypes.Structure):
    # _fields_ = [
        # ('hti', HTREEITEM),
        # ('prc', ctypes.POINTER(RECT)),
        # ('partID', TVITEMPART),
    # ]


PFNTVCOMPARE = ctypes.WINFUNCTYPE(INT, LPARAM, LPARAM, LPARAM)

class TVSORTCB(ctypes.Structure):
    _fields_ = [
        ('hParent', HTREEITEM),
        ('lpfnCompare', PFNTVCOMPARE),
        ('lParam', LPARAM),
    ]


class NMTREEVIEW(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('action', UINT),
        ('itemOld', TVITEM),
        ('itemNew', TVITEM),
        ('ptDrag', POINT),
    ]


class TVC(IntEnum):
    UNKNOWN = 0x0000
    BYMOUSE = 0x0001
    BYKEYBOARD = 0x0002


class TVIFDI(IntEnum):
    SETITEM = 0x1000


class TVDISPINFO(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('item', TVITEM),
    ]


class TVDISPINFOEX(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('item', TVITEMEX),
    ]


class TVNRET(IntEnum):
    DEFAULT = 0
    SKIPOLD = 1
    SKIPNEW = 2


class TVKEYDOWN(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('hdr', NMHDR),
        ('wVKey', WORD),
        ('flags', UINT),
    ]


# class NMTVCUSTOMDRAW(ctypes.Structure):
    # _fields_ = [
        # ('nmcd', NMCUSTOMDRAW),
        # ('clrText', INT),
        # ('clrTextBk', INT),
        # ('iLevel', INT),
    # ]


# for tooltips
class NMTVGETINFOTIP(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('pszText', LPCWSTR),
        ('cchTextMax', INT),
        ('hItem', HTREEITEM),
        ('lParam', LPARAM),
    ]


# treeview's customdraw return meaning don't draw images.  valid on CDRF_NOTIFYITEMPREPAINT
class TVCDRF(IntEnum):
    NOIMAGES = 0x00010000


class TVITEMCHANGE(ctypes.Structure):
    _fields_ = [
        ('hdr', NMHDR),
        ('uChanged', UINT),
        ('hItem', HTREEITEM),
        ('uStateNew', UINT),
        ('uStateOld', UINT),
        ('lParam', LPARAM),
    ]


# class NMTVASYNCDRAW(ctypes.Structure):
    # _fields_ = [
        # ('hdr', NMHDR),
        # ('pimldp', IMAGELISTDRAWPARAMS),  # the draw that failed
        # ('hr', HRESULT),                  # why it failed
        # ('hItem', HTREEITEM),             # item that failed to draw icon
        # ('lParam', LPARAM),               # its data
        # # Out Params
        # ('dwRetFlags', DWORD),            # What listview should do on return
        # ('iRetImageIndex', INT),          # used if ADRF_DRAWIMAGE is returned
    # ]

class TVN(IntEnum):
    FIRST = -400
    SELCHANGING = FIRST-50
    SELCHANGED = FIRST-51
    GETDISPINFO = FIRST-52
    SETDISPINFO = FIRST-53
    ITEMEXPANDING = FIRST-54
    ITEMEXPANDED = FIRST-55
    BEGINDRAG = FIRST-56
    BEGINRDRAG = FIRST-57
    DELETEITEM = FIRST-58
    BEGINLABELEDIT = FIRST-59
    ENDLABELEDIT = FIRST-60
    KEYDOWN = FIRST-12
    GETINFOTIP = FIRST-14
    SINGLEEXPAND = FIRST-15
    ITEMCHANGING = FIRST-17
    ITEMCHANGED = FIRST-19
    ASYNCDRAW = FIRST-20


class TVM(IntEnum):
    FIRST = 0x1100
    INSERTITEM = FIRST+50
    DELETEITEM = FIRST+1
    EXPAND = FIRST+2
    GETITEMRECT = FIRST+4
    GETCOUNT = FIRST+5
    GETINDENT = FIRST+6
    SETINDENT = FIRST+7
    GETIMAGELIST = FIRST+8
    SETIMAGELIST = FIRST+9
    GETNEXTITEM = FIRST+10
    SELECTITEM = FIRST+11
    GETITEM = FIRST+62
    SETITEM = FIRST+63
    EDITLABEL = FIRST+65
    GETEDITCONTROL = FIRST+15
    GETVISIBLECOUNT = FIRST+16
    HITTEST = FIRST+17
    CREATEDRAGIMAGE = FIRST+18
    SORTCHILDREN = FIRST+19
    ENSUREVISIBLE = FIRST+20
    SORTCHILDRENCB = FIRST+21
    ENDEDITLABELNOW = FIRST+22
    GETISEARCHSTRING = FIRST+64
    SETTOOLTIPS = FIRST+24
    GETTOOLTIPS = FIRST+25
    SETINSERTMARK = FIRST+26
    SETUNICODEFORMAT = CCM.SETUNICODEFORMAT
    GETUNICODEFORMAT = CCM.GETUNICODEFORMAT
    SETITEMHEIGHT = FIRST+27
    GETITEMHEIGHT = FIRST+28
    SETBKCOLOR = FIRST+29
    SETTEXTCOLOR = FIRST+30
    GETBKCOLOR = FIRST+31
    GETTEXTCOLOR = FIRST+32
    SETSCROLLTIME = FIRST+33
    GETSCROLLTIME = FIRST+34
    SETINSERTMARKCOLOR = FIRST+37
    GETINSERTMARKCOLOR = FIRST+38
    SETBORDER = FIRST+35
    GETITEMSTATE = FIRST+39
    SETLINECOLOR = FIRST+40
    GETLINECOLOR = FIRST+41
    MAPACCIDTOHTREEITEM = FIRST+42
    MAPHTREEITEMTOACCID = FIRST+43
    SETEXTENDEDSTYLE = FIRST+44
    GETEXTENDEDSTYLE = FIRST+45
    SETAUTOSCROLLINFO = FIRST+59
    SETHOT = FIRST+58
    GETSELECTEDCOUNT = FIRST+70
    SHOWINFOTIP = FIRST+71
    GETITEMPARTRECT = FIRST+72

@dataclass
class TreeView(Control):
    """
    A class representing a tree view control.

    Attributes:
        style (INT): The style of the tree view control.
        windowClass (str): The window class associated with the tree view control.
        __nodes (dict): The nodes in a tree view control.


    Notification:
        - ...

    Methods:
        clear() -> None:
            Clear the list view by removing all items.

        addNode(parent) -> None:
        addNodes(parent) -> None:

    """
    style: INT = Control.style | WS.BORDER
    windowClass: str = 'SysTreeView32'

    onClick = WM_NotifyDelegator(NM.CLICK, None)
    onCustomDraw = WM_NotifyDelegator(NM.CUSTOMDRAW, None)
    onDblClk = WM_NotifyDelegator(NM.DBLCLK, None)
    onKillFocus = WM_NotifyDelegator(NM.KILLFOCUS, None)
    onRClick = WM_NotifyDelegator(NM.RCLICK, None)
    onRDblClk = WM_NotifyDelegator(NM.RDBLCLK, None)
    onReturn = WM_NotifyDelegator(NM.RETURN, None)
    onSetCursor = WM_NotifyDelegator(NM.SETCURSOR, None)
    onSetFocus = WM_NotifyDelegator(NM.SETFOCUS, None)
    onAsyncDraw = WM_NotifyDelegator(TVN.ASYNCDRAW, None)
    onBeginDrag = WM_NotifyDelegator(TVN.BEGINDRAG, None)
    onBeginLabelEdit = WM_NotifyDelegator(TVN.BEGINLABELEDIT, None)
    onBeginrDrag = WM_NotifyDelegator(TVN.BEGINRDRAG, None)
    onDeleteItem = WM_NotifyDelegator(TVN.DELETEITEM, None)
    onEndLabelEdit = WM_NotifyDelegator(TVN.ENDLABELEDIT, None)
    onGetDispInfo = WM_NotifyDelegator(TVN.GETDISPINFO, None)
    onGetInfoTip = WM_NotifyDelegator(TVN.GETINFOTIP, None)
    onItemChanged = WM_NotifyDelegator(TVN.ITEMCHANGED, None)
    onItemChanging = WM_NotifyDelegator(TVN.ITEMCHANGING, None)
    onItemExpanded = WM_NotifyDelegator(TVN.ITEMEXPANDED, None)
    onItemExpanding = WM_NotifyDelegator(TVN.ITEMEXPANDING, None)
    onKeyDown = WM_NotifyDelegator(TVN.KEYDOWN, None)
    onSelChanged = WM_NotifyDelegator(TVN.SELCHANGED, None)
    onSelChanging = WM_NotifyDelegator(TVN.SELCHANGING, None)
    onSetDispInfo = WM_NotifyDelegator(TVN.SETDISPINFO, None)
    onSingleExpand = WM_NotifyDelegator(TVN.SINGLEEXPAND, None)

    def insertItem(self, lpis):
        """
        Inserts an item into a tree-view control.

        Args:
            lpis: The structure containing information about the item to insert.

        Returns:
            HTREEITEM: The handle to the newly inserted item.
        """
        return SendMessage(self.hwnd, TVM.INSERTITEM, 0, ctypes.addressof(lpis))  # return (HTREEITEM) LPTV_INSERTSTRUCT(lpis)

    def deleteItem(self, hitem):
        """
        Deletes an item from a tree-view control.

        Args:
            hitem: The handle to the item to delete.

        Returns:
            BOOL: True if the item is successfully deleted, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.DELETEITEM, 0, HTREEITEM(hitem))  # return (BOOL)

    def deleteAllItems(self, hwnd):
        """
        Deletes all items from a tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            BOOL: True if all items are successfully deleted, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.DELETEITEM, 0, TVI.ROOT)  # return (BOOL)

    def expand(self, hitem, code):
        """
        Expands or collapses a tree-view item.

        Args:
            hitem: The handle to the item to expand or collapse.
            code: The code indicating the action to perform. (TVE_COLLAPSE, TVE_COLLAPSERESET, TVE_EXPAND, TVE_TOGGLE)

        Returns:
            BOOL: True if the item is successfully expanded or collapsed, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.EXPAND, code, HTREEITEM(hitem))  # return (BOOL)

    def getItemRect(self, hitem, p_rect, code):
        """
        Retrieves the bounding rectangle for a specified tree-view item.

        Args:
            hitem: The handle to the item.
            p_rect: The pointer to a RECT structure that receives the bounding rectangle.
            code: The code indicating the type of rectangle to retrieve. (TVIR_BOUNDS, TVIR_ICON, TVIR_LABEL)

        Returns:
            BOOL: True if the bounding rectangle is successfully retrieved, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.GETITEMRECT, code, ctypes.addressof(p_rect)) #     (*(HTREEITEM *)(prc) = (hitem) , return (BOOL)

    def getCount(self, hwnd):
        """
        Retrieves the number of items in a tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            UINT: The number of items in the tree-view control.
        """
        return SendMessage(self.hwnd, TVM.GETCOUNT, 0, 0)  # return (UINT)

    def getIndent(self, hwnd):
        """
        Retrieves the amount of indentation for items in a tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            UINT: The amount of indentation, in pixels.
        """
        return SendMessage(self.hwnd, TVM.GETINDENT, 0, 0)  # return (UINT)

    def setIndent(self, indent):
        """
        Sets the amount of indentation for items in a tree-view control.

        Args:
            indent: The amount of indentation to set, in pixels.

        Returns:
            BOOL: True if the indentation is successfully set, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.SETINDENT, indent, 0)  # return (BOOL)

    def getImageList(self, iImage):
        """
        Retrieves the handle to the image list used for drawing icons in a tree-view control.

        Args:
            iImage: The identifier of the image list to retrieve. (TVSIL_NORMAL, TVSIL_STATE)

        Returns:
            HIMAGELIST: The handle to the image list.
        """
        return SendMessage(self.hwnd, TVM.GETIMAGELIST, iImage, 0)  # return (HIMAGELIST)

    def setImageList(self, himl, iImage):
        """
        Sets the image list for a tree-view control.

        Args:
            himl: The handle to the image list.
            iImage: The identifier of the image list to set. (TVSIL_NORMAL, TVSIL_STATE)

        Returns:
            HIMAGELIST: The previous handle to the image list, or None if no previous image list was set.
        """
        return SendMessage(self.hwnd, TVM.SETIMAGELIST, iImage, himl)  # return (HIMAGELIST)  HIMAGELIST(himl)

    def getNextItem(self, hitem, code):
        """
        Retrieves the next item in a tree-view control based on the specified relationship.

        Args:
            hitem: The handle to the reference item.
            code: The code indicating the relationship between the reference item and the item to retrieve.
                  Possible values: TVGN_CHILD, TVGN_NEXT, TVGN_PARENT, TVGN_PREVIOUS, TVGN_ROOT.

        Returns:
            HTREEITEM: The handle to the next item in the specified relationship.
        """
        return SendMessage(self.hwnd, TVM.GETNEXTITEM, code, HTREEITEM(hitem))  # return (HTREEITEM)

    def select(self, hitem, code):
        """
        Selects or deselects a tree-view item in a tree-view control.

        Args:
            hitem: The handle to the item to select or deselect.
            code: The code indicating the selection action to perform.
                  Possible values:
                    TVGN_CARET, TVGN_DROPHILITE, TVGN_FIRSTVISIBLE, TVGN_LASTVISIBLE,
                    TVGN_NEXTSELECTED, TVGN_NEXTVISIBLE, TVGN_PARENT, TVGN_PREVIOUSSELECTED,
                    TVGN_PREVIOUSVISIBLE, TVGN_ROOT

        Returns:
            BOOL: True if the selection action is successful, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.SELECTITEM, code, HTREEITEM(hitem))  # return (BOOL)

    def getItem(self, item):
        """
        Retrieves information about a tree-view item in a tree-view control.

        Args:
            pitem: The pointer to a TV_ITEM structure that receives the item information.

        Returns:
            BOOL: True if the item information is successfully retrieved, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.GETITEM, 0, ctypes.addressof(item))  # return (BOOL)

    def setItem(self, item):
        """
        Sets information about a tree-view item in a tree-view control.

        Args:
            pitem: The pointer to a TV_ITEM structure that contains the item information to set.

        Returns:
            BOOL: True if the item information is successfully set, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.SETITEM, 0, ctypes.addressof(item))  # return (BOOL)

    def editLabel(self, hitem):
        """
        Initiates in-place editing of the label text of a tree-view item.

        Args:
            hitem: The handle to the item to edit.

        Returns:
            HWND: The handle to the edit control used for editing the label text.
        """
        return SendMessage(self.hwnd, TVM.EDITLABEL, 0, HTREEITEM(hitem))  # return (HWND)

    def getEditControl(self, hwnd):
        """
        Retrieves the handle to the edit control used for editing a tree-view item's label.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            HWND: The handle to the edit control, or None if no edit control is associated.
        """
        return SendMessage(self.hwnd, TVM.GETEDITCONTROL, 0, 0)  # return (HWND)

    def getVisibleCount(self, hwnd):
        """
        Retrieves the number of visible items in a tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            UINT: The number of visible items in the tree-view control.
        """
        return SendMessage(self.hwnd, TVM.GETVISIBLECOUNT, 0, 0)  # return (UINT)

    def hitTest(self, lpht):
        """
        Determines which item is at a specified position in a tree-view control.

        Args:
            lpht: The pointer to a TV_HITTESTINFO structure that contains the position information.

        Returns:
            HTREEITEM: The handle to the item at the specified position.
        """
        return SendMessage(self.hwnd, TVM.HITTEST, 0, ctypes.addressof(lpht))  # return (HTREEITEM)

    def createDragImage(self, hitem):
        """
        Creates a drag image for the specified tree-view item.

        Args:
            hitem: The handle to the tree-view item.

        Returns:
            HIMAGELIST: The handle to the drag image, or None if an error occurs.
        """
        return SendMessage(self.hwnd, TVM.CREATEDRAGIMAGE, 0, HTREEITEM(hitem))  # return (HIMAGELIST)

    def sortChildren(self, hitem, recurse):
        """
        Sorts the child items of a specified tree-view item.

        Args:
            hitem: The handle to the parent item whose children will be sorted.
            recurse: Specifies whether to recursively sort the child items of the parent item.

        Returns:
            BOOL: True if the sort operation is successful, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.SORTCHILDREN, recurse, HTREEITEM(hitem))  # return (BOOL)

    def ensureVisible(self, hitem):
        """
        Ensures that a tree-view item is visible, scrolling the tree-view control if necessary.

        Args:
            hitem: The handle to the item to make visible.

        Returns:
            BOOL: True if the item is successfully made visible, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.ENSUREVISIBLE, 0, HTREEITEM(hitem))  # return (BOOL)

    def sortChildrenCB(self, psort, recurse):
        """
        Sorts the child items of a specified tree-view item using a comparison callback function.

        Args:
            psort: The pointer to a TV_SORTCB structure that contains the sort information.
            recurse: Specifies whether to recursively sort the child items of the parent item.

        Returns:
            BOOL: True if the sort operation is successful, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.SORTCHILDRENCB, recurse, ctypes.addressof(psort))  # return (BOOL)  LPTV_SORTCB(psort)

    def endEditLabelNow(self, fCancel):
        """
        Ends the in-place editing of a tree-view item's label.

        Args:
            fCancel: Specifies whether to cancel the label edit or accept the changes.

        Returns:
            BOOL: True if the label editing is successfully ended, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.ENDEDITLABELNOW, fCancel, 0)  # return (BOOL)

    def setToolTips(self, hwndTT):
        """
        Associates a tooltip control with a tree-view control.

        Args:
            hwndTT: The handle to the tooltip control.

        Returns:
            HWND: The handle to the previous tooltip control, or None if no tooltip control was associated.
        """
        return SendMessage(self.hwnd, TVM.SETTOOLTIPS, hwndTT, 0)  # return (HWND)

    def getToolTips(self, hwnd):
        """
        Retrieves the handle to the tooltip control associated with a tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            HWND: The handle to the tooltip control, or None if no tooltip control is associated.
        """
        return SendMessage(self.hwnd, TVM.GETTOOLTIPS, 0, 0)  # return (HWND)

    def getISearchString(self, hwndTV, lpsz):
        """
        Retrieves the incremental search string of a tree-view control.

        Args:
            hwndTV: The handle to the tree-view control.
            lpsz: The pointer to a buffer that receives the incremental search string.

        Returns:
            BOOL: True if the incremental search string is successfully retrieved, False otherwise.
        """
        return SendMessage((hwndTV), TVM.GETISEARCHSTRING, 0, LPCWSTR(lpsz))  # return (BOOL)

    def setInsertMark(self, item, after):
        """
        Sets the insertion mark in a tree-view control.

        Args:
            hItem: The handle to the tree-view item.
            fAfter: Specifies whether the insertion mark should appear after the item.

        Returns:
            BOOL: True if the insertion mark is successfully set, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.SETINSERTMARK, after, item)  # return (BOOL)

    def setUnicodeFormat(self, fUnicode):
        """
        Sets the Unicode character format flag for a tree-view control.

        Args:
            fUnicode: Specifies whether to set the Unicode character format flag.

        Returns:
            BOOL: True if the Unicode format is successfully set, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.SETUNICODEFORMAT, fUnicode, 0)  # return (BOOL)

    def getUnicodeFormat(self, hwnd):
        """
        Retrieves the Unicode character format flag of a tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            BOOL: True if the Unicode format flag is set, False otherwise.
        """
        return SendMessage(self.hwnd, TVM.GETUNICODEFORMAT, 0, 0)  # return (BOOL)

    def setItemHeight(self,  iHeight):
        """
        Sets the height of the items in the tree-view control.

        Args:
            iHeight: The new height of the items.

        Returns:
            INT: The previous height of the items.
        """
        return SendMessage(self.hwnd, TVM.SETITEMHEIGHT, iHeight, 0)  # return (INT)

    def getItemHeight(self, hwnd):
        """
        Retrieves the current height of the items in the tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            INT: The height of the items.
        """
        return SendMessage(self.hwnd, TVM.GETITEMHEIGHT, 0, 0)  # return (INT)

    def setBkColor(self, clr):
        """
        Sets the background color of the tree-view control.

        Args:
            clr: The new background color.

        Returns:
            INT: The previous background color.
        """
        return SendMessage(self.hwnd, TVM.SETBKCOLOR, 0, clr)  # return (INT)

    def setTextColor(self, clr):
        """
        Sets the text color of the tree-view control.

        Args:
            clr: The new text color.

        Returns:
            INT: The previous text color.
        """
        return SendMessage(self.hwnd, TVM.SETTEXTCOLOR, 0, clr)  # return (INT)

    def getBkColor(self, hwnd):
        """
        Retrieves the current background color of the tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            INT: The background color.
        """
        return SendMessage(self.hwnd, TVM.GETBKCOLOR, 0, 0)  # return (INT)

    def getTextColor(self, hwnd):
        """
        Retrieves the current text color of the tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            INT: The text color.
        """
        return SendMessage(self.hwnd, TVM.GETTEXTCOLOR, 0, 0)  # return (INT)

    def setScrollTime(self, uTime):
        """
        Sets the scroll time of the tree-view control.

        Args:
            uTime: The new scroll time, in milliseconds.

        Returns:
            UINT: The previous scroll time.
        """
        return SendMessage(self.hwnd, TVM.SETSCROLLTIME, uTime, 0)  # return (UINT)

    def getScrollTime(self, hwnd):
        """
        Retrieves the current scroll time of the tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            UINT: The scroll time, in milliseconds.
        """
        return SendMessage(self.hwnd, TVM.GETSCROLLTIME, 0, 0)  # return (UINT)

    def setInsertMarkColor(self, clr):
        """
        Sets the color of the insertion mark in the tree-view control.

        Args:
            clr: The new color of the insertion mark.

        Returns:
            INT: The previous color of the insertion mark.
        """
        return SendMessage(self.hwnd, TVM.SETINSERTMARKCOLOR, 0, clr)  # return (INT)

    def getInsertMarkColor(self, hwnd):
        """
        Retrieves the current color of the insertion mark in the tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            INT: The color of the insertion mark.
        """
        return SendMessage(self.hwnd, TVM.GETINSERTMARKCOLOR, 0, 0)  # return (INT)

    def setBorder(self,  dwFlags, xBorder, yBorder):
        """
        Sets the border of the tree-view control.

        Args:
            dwFlags: The border flags.
            xBorder: The new width of the border, in pixels.
            yBorder: The new height of the border, in pixels.

        Returns:
            INT: The previous border width and height, packed in a single value.
        """
        return SendMessage(self.hwnd, TVM.SETBORDER, dwFlags, MAKELPARAM(xBorder, yBorder))  # return (INT)

    def getItemState(self, hti, mask):
        """
        Retrieves the state of a tree-view item.

        Args:
            hti: The handle to the tree-view item.
            mask: The mask that specifies which item state flags to retrieve.

        Returns:
            UINT: The item state flags.
        """
        return SendMessage(self.hwnd, TVM.GETITEMSTATE, hti, mask)  # return (UINT)

    def getCheckState(self, hti):
        """
        Retrieves the check state of a tree-view item.

        Args:
            hti: The handle to the tree-view item.

        Returns:
            INT: The check state of the item. Possible values:
                -1: The item is unchecked.
                 0: The item is partially checked.
                 1: The item is checked.
    """
        return (((SendMessage(self.hwnd, TVM.GETITEMSTATE, hti, TVIS.STATEIMAGEMASK))) >> 12) -1  # return ((((UINT)(

    def setLineColor(self, clr):
        """
        Sets the line color of the tree-view control.

        Args:
            clr: The new line color.

        Returns:
            INT: The previous line color.
        """
        return SendMessage(self.hwnd, TVM.SETLINECOLOR, 0, clr)  # return (INT)

    def getLineColor(self, hwnd):
        """
        Retrieves the current line color of the tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            INT: The line color.
        """
        return SendMessage(self.hwnd, TVM.GETLINECOLOR, 0, 0)  # return (INT)

    def mapAccIDToHTREEITEM(self, id):
        """
        Maps an accessibility ID to the corresponding tree-view item.

        Args:
            id: The accessibility ID to map.

        Returns:
            HTREEITEM: The handle to the corresponding tree-view item.
        """
        return SendMessage(self.hwnd, TVM.MAPACCIDTOHTREEITEM, id, 0)  # return (HTREEITEM)

    def mapHTREEITEMToAccID(self, htreeitem):
        """
        Maps a tree-view item to the corresponding accessibility ID.

        Args:
            htreeitem: The handle to the tree-view item.

        Returns:
            UINT: The corresponding accessibility ID.
        """
        return SendMessage(self.hwnd, TVM.MAPHTREEITEMTOACCID, htreeitem, 0)  # return (UINT)

    def setExtendedStyle(self, dw, mask):
        """
        Sets the extended styles of the tree-view control.

        Args:
            dw: The new extended styles.
            mask: The mask that specifies which extended styles to set.

        Returns:
            DWORD: The previous extended styles.
        """
        return SendMessage(self.hwnd, TVM.SETEXTENDEDSTYLE, mask, dw)  # return (DWORD)

    def getExtendedStyle(self, hwnd):
        """
        Retrieves the current extended styles of the tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            DWORD: The extended styles.
        """
        return SendMessage(self.hwnd, TVM.GETEXTENDEDSTYLE, 0, 0)  # return (DWORD)

    def setAutoScrollInfo(self, uPixPerSec, uUpdateTime):
        """
        Sets the auto-scroll information for the tree-view control.

        Args:
            uPixPerSec: The scrolling speed, in pixels per second.
            uUpdateTime: The time interval between updates, in milliseconds.

        Returns:
            None
        """
        return SendMessage(self.hwnd, TVM.SETAUTOSCROLLINFO, uPixPerSec, uUpdateTime)  # return (VOID)

    def setHot(self, hitem):
        """
        Sets the "hot" tree-view item, which is the item that has the mouse over it.

        Args:
            hitem: The handle to the "hot" item.

        Returns:
            None
        """
        return SendMessage(self.hwnd, TVM.SETHOT, 0, hitem)  # return (VOID)

    def getSelectedCount(self, hwnd):
        """
        Retrieves the count of selected items in the tree-view control.

        Args:
            hwnd: The handle to the tree-view control.

        Returns:
            DWORD: The count of selected items.
        """
        return SendMessage(self.hwnd, TVM.GETSELECTEDCOUNT, 0, 0)  # return (DWORD)

    def showInfoTip(self, hitem):
        """
        Shows the info tip for a tree-view item.

        Args:
            hitem: The handle to the tree-view item.

        Returns:
            DWORD: The result of the operation.
        """
        return SendMessage(self.hwnd, TVM.SHOWINFOTIP, 0, hitem)  # return (DWORD)


# #define TreeView_GetItemPartRect(hwnd, hitem, prc, partid) \
# { TVGETITEMPARTRECTINFO info \
  # info.hti = (hitem); \
  # info.prc = (prc); \
  # info.partID = (partid); \
  # (BOOL)SNDMSG((hwnd), TVM_GETITEMPARTRECT, 0, (LPARAM)&info); \
# }

# # tvm_?etitemstate only uses mask, state and stateMask.
# # so unicode or ansi is irrelevant.
# #define TreeView_SetItemState(hwndTV, hti, data, _mask) \
# { TVITEM _ms_TVi;\
  # _ms_TVi.mask = TVIF_STATE \
  # _ms_TVi.hItem = (hti); \
  # _ms_TVi.stateMask = (_mask);\
  # _ms_TVi.state = (data);\
  # SNDMSG((hwndTV), TVM_SETITEM, 0, (LPARAM)(TV_ITEM *)&_ms_TVi);\
# }

# #define TreeView_SetCheckState(hwndTV, hti, fCheck) \
  # TreeView_SetItemState(hwndTV, hti, INDEXTOSTATEIMAGEMASK((fCheck)?2:1), TVIS_STATEIMAGEMASK)


#define TreeView_GetChild(hwnd, hitem)          TreeView_GetNextItem(hwnd, hitem, TVGN_CHILD)
#define TreeView_GetNextSibling(hwnd, hitem)    TreeView_GetNextItem(hwnd, hitem, TVGN_NEXT)
#define TreeView_GetPrevSibling(hwnd, hitem)    TreeView_GetNextItem(hwnd, hitem, TVGN_PREVIOUS)
#define TreeView_GetParent(hwnd, hitem)         TreeView_GetNextItem(hwnd, hitem, TVGN_PARENT)
#define TreeView_GetFirstVisible(hwnd)          TreeView_GetNextItem(hwnd, NULL,  TVGN_FIRSTVISIBLE)
#define TreeView_GetNextVisible(hwnd, hitem)    TreeView_GetNextItem(hwnd, hitem, TVGN_NEXTVISIBLE)
#define TreeView_GetPrevVisible(hwnd, hitem)    TreeView_GetNextItem(hwnd, hitem, TVGN_PREVIOUSVISIBLE)
#define TreeView_GetSelection(hwnd)             TreeView_GetNextItem(hwnd, NULL,  TVGN_CARET)
#define TreeView_GetDropHilight(hwnd)           TreeView_GetNextItem(hwnd, NULL,  TVGN_DROPHILITE)
#define TreeView_GetRoot(hwnd)                  TreeView_GetNextItem(hwnd, NULL,  TVGN_ROOT)
#define TreeView_GetLastVisible(hwnd)           TreeView_GetNextItem(hwnd, NULL,  TVGN_LASTVISIBLE)
#if (_WIN32_IE >= 0x0600)
#define TreeView_GetNextSelected(hwnd, hitem)   TreeView_GetNextItem(hwnd, hitem,  TVGN_NEXTSELECTED)
#endif



#define TreeView_SelectItem(hwnd, hitem)            TreeView_Select(hwnd, hitem, TVGN_CARET)
#define TreeView_SelectDropTarget(hwnd, hitem)      TreeView_Select(hwnd, hitem, TVGN_DROPHILITE)
#define TreeView_SelectSetFirstVisible(hwnd, hitem) TreeView_Select(hwnd, hitem, TVGN_FIRSTVISIBLE)