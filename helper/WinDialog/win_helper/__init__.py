"""
Win32 Helper Utilities

This module provides Win32 API functions, structures, and common shared control classes and enums.
It serves as a utility module to facilitate interaction with the WinDialog module.

Note:
    For detailed usage instructions and examples, please refer to the
    MS documentation at https://learn.microsoft.com/en-us/windows/win32/api
"""

import ctypes
from ctypes import POINTER
from ctypes.wintypes import (
	HWND, UINT, WPARAM, LPARAM, INT, BOOL,
    MSG, HINSTANCE, RECT, HMODULE, LPCWSTR,
    POINT
)
from enum import IntEnum

WM_USER = 1024

INT_PTR = LONG_PTR = ctypes.c_ssize_t  # signed pointer sized integer
UINT_PTR = ctypes.c_size_t  # unsigned pointer sized integer
DWORD_PTR = ctypes.c_size_t # unsigned pointer sized integer


user32 = ctypes.WinDLL('user32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
comctl32 = ctypes.WinDLL('comctl32', use_last_error=True)

LRESULT = LPARAM
DIALOGPROC = ctypes.WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)

SendMessage = user32.SendMessageW
SendMessage.restype = LRESULT
SendMessage.argtypes = [HWND, UINT, WPARAM, LPARAM]

PostMessage = user32.PostMessageW
PostMessage.restype = BOOL
PostMessage.argtypes = [HWND, UINT, WPARAM, LPARAM]

DialogBoxIndirectParam = user32.DialogBoxIndirectParamW
DialogBoxIndirectParam.restype = INT_PTR
DialogBoxIndirectParam.argtypes = [HINSTANCE, POINTER(ctypes.c_ubyte), HWND, DIALOGPROC, LPARAM]

CreateDialogIndirectParam = user32.CreateDialogIndirectParamW #DialogBoxParamW
CreateDialogIndirectParam.argtypes = [HINSTANCE, POINTER(ctypes.c_ubyte), HWND, DIALOGPROC, LPARAM] #
CreateDialogIndirectParam.restype = HWND

GetDlgItem = user32.GetDlgItem
GetDlgItem.restype = HWND
GetDlgItem.argtypes = [HWND, INT]

GetDlgItemText = user32.GetDlgItemTextW
GetDlgItemText.restype = UINT
GetDlgItemText.argtypes = [HWND, INT, LPCWSTR, INT]

EndDialog = user32.EndDialog
EndDialog.restype = BOOL
EndDialog.argtypes = [HWND, INT_PTR]

ShowWindow = user32.ShowWindow
ShowWindow.restype = BOOL
ShowWindow.argtypes = [HWND, INT]

UpdateWindow = user32.UpdateWindow
UpdateWindow.restype = BOOL
UpdateWindow.argtypes = [HWND]

DestroyWindow = user32.DestroyWindow
DestroyWindow.restype = BOOL
DestroyWindow.argtypes = [HWND]

IsWindowVisible = user32.IsWindowVisible
IsWindowVisible.argtypes = [HWND]
IsWindowVisible.restype = BOOL

GetMessage = user32.GetMessageW
GetMessage.restype  = BOOL
GetMessage.argtypes = [POINTER(MSG), HWND, UINT, UINT]

TranslateMessage = user32.TranslateMessage
TranslateMessage.restype  = BOOL
TranslateMessage.argtypes = [POINTER(MSG)]

DispatchMessage = user32.DispatchMessageW
DispatchMessage.restype  = LRESULT
DispatchMessage.argtypes = [POINTER(MSG)]

IsDialogMessage = user32.IsDialogMessageW
IsDialogMessage.restype  = BOOL
IsDialogMessage.argtypes = [HWND, POINTER(MSG)]

GetWindowRect = user32.GetWindowRect
GetWindowRect.restype  = BOOL
GetWindowRect.argtypes = [HWND, POINTER(RECT)]

OffsetRect = user32.OffsetRect
OffsetRect.restype  = BOOL
OffsetRect.argtypes = [POINTER(RECT), INT, INT]

CopyRect = user32.CopyRect
CopyRect.restype  = BOOL
CopyRect.argtypes = [POINTER(RECT), POINTER(RECT)]

SetWindowPos = user32.SetWindowPos
SetWindowPos.restype  = BOOL
SetWindowPos.argtypes = [HWND, HWND, INT, INT, INT, INT, UINT]

GetModuleHandle = kernel32.GetModuleHandleW
GetModuleHandle.restype  = HMODULE
GetModuleHandle.argtypes = [LPCWSTR]

# https://learn.microsoft.com/en-us/windows/win32/controls/subclassing-overview#subclassing-controls-using-comctl32dll-version-6
SUBCLASSPROC = ctypes.WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM, UINT_PTR, DWORD_PTR)

SetWindowSubclass = comctl32.SetWindowSubclass
SetWindowSubclass.restype  = BOOL
SetWindowSubclass.argtypes = [HWND, SUBCLASSPROC, UINT_PTR, DWORD_PTR]

GetWindowSubclass = comctl32.GetWindowSubclass
GetWindowSubclass.restype  = BOOL
GetWindowSubclass.argtypes = [HWND, SUBCLASSPROC, UINT_PTR, POINTER(DWORD_PTR)]

RemoveWindowSubclass = comctl32.RemoveWindowSubclass
RemoveWindowSubclass.restype  = BOOL
RemoveWindowSubclass.argtypes = [HWND, SUBCLASSPROC, UINT_PTR]

DefSubclassProc = comctl32.DefSubclassProc
DefSubclassProc.restype  = LRESULT
DefSubclassProc.argtypes = [HWND, UINT, WPARAM, LPARAM]

SetWindowText = user32.SetWindowTextW
SetWindowText.restype = BOOL
SetWindowText.argtypes = [HWND, LPCWSTR]

GetWindowText = user32.GetWindowTextW
GetWindowText.restype = INT
GetWindowText.argtypes = [HWND, LPCWSTR, INT]

GetWindowTextLength = user32.GetWindowTextLengthW
GetWindowTextLength.restype = INT
GetWindowTextLength.argtypes = [HWND]

GetWindowLong = user32.GetWindowLongPtrW
GetWindowLong.restype = LONG_PTR
GetWindowLong.argtypes = [HWND, INT]

SetWindowLong = user32.SetWindowLongPtrW
SetWindowLong.restype = LONG_PTR
SetWindowLong.argtypes = [HWND, INT, LONG_PTR]

FindWindow = user32.FindWindowW
FindWindow.restype = HWND
FindWindow.argtypes = [LPCWSTR, LPCWSTR]

FindWindowEx = user32.FindWindowExW
FindWindowEx.restype = HWND
FindWindowEx.argtypes = [HWND, HWND, LPCWSTR, LPCWSTR]

SetFocus = user32.SetFocus
SetFocus.restype = HWND
SetFocus.argtypes = [HWND]
# GetDialogBaseUnits = user32.GetDialogBaseUnits
# GetDialogBaseUnits.restype = LONG
# GetDialogBaseUnits.argtypes = []

# MulDiv = kernel32.MulDiv
# MulDiv.restype = INT
# MulDiv.argtypes = [INT, INT, INT]

# MapDialogRect = user32.MapDialogRect
# MapDialogRect.restype = BOOL
# MapDialogRect.argtypes = [HWND, POINTER(RECT)]

SWP_NOSIZE = 1

class GWL(IntEnum):
    WNDPROC        = -4
    HINSTANCE      = -6
    HWNDPARENT     = -8
    STYLE          = -16
    EXSTYLE        = -20
    USERDATA       = -21
    ID             = -12

class WindowClassStyles(IntEnum):
    # Aligns the window's client area on a byte boundary (in the x direction).
    # This style affects the width of the window and its horizontal placement on the display.
    BYTEALIGNCLIENT = 0x1000
    # Aligns the window on a byte boundary (in the x direction).
    # This style affects the width of the window and its horizontal placement on the display.
    BYTEALIGNWINDOW = 0x2000
    # Allocates one device context to be shared by all windows in the class.
    # Because window classes are process specific, it is possible for multiple threads of an application to create a window of the same class.
    # It is also possible for the threads to attempt to use the device context simultaneously.
    # When this happens, the system allows only one thread to successfully finish its drawing operation.
    CLASSDC = 0x0040
    # Sends a double-click message to the window procedure when the user double-clicks the mouse
    # while the cursor is within a window belonging to the class.
    DBLCLKS = 0x0008
    # Enables the drop shadow effect on a window. The effect is turned on and off through SPI_SETDROPSHADOW.
    # Typically, this is enabled for small, short-lived windows such as menus to emphasize their Z-order relationship to other windows.
    # Windows created from a class with this style must be top-level windows; they may not be child windows.
    DROPSHADOW = 0x00020000
    # Indicates that the window class is an application global class.
    # For more information, see the "Application Global Classes" section of About Window Classes.
    GLOBALCLASS = 0x4000
    # Redraws the entire window if a movement or size adjustment changes the width of the client area.
    HREDRAW = 0x0002
    # Disables Close on the window menu.
    NOCLOSE = 0x0200
    # Allocates a unique device context for each window in the class.
    OWNDC = 0x0020
    # Sets the clipping rectangle of the child window to that of the parent window so that the child can draw on the parent.
    # A window with the PARENTDC style bit receives a regular device context from the system's cache of device contexts.
    # It does not give the child the parent's device context or device context settings. Specifying PARENTDC enhances an application's performance.
    PARENTDC = 0x0080
    # Saves, as a bitmap, the portion of the screen image obscured by a window of this class. When the window is removed,
    # the system uses the saved bitmap to restore the screen image, including other windows that were obscured.
    # Therefore, the system does not send WM_PAINT messages to windows that were obscured if the memory used by the bitmap has not been discarded
    # and if other screen actions have not invalidated the stored image.
    # This style is useful for small windows (for example, menus or dialog boxes) that are displayed briefly
    # and then removed before other screen activity takes place.
    # This style increases the time required to display the window, because the system must first allocate memory to store the bitmap.
    SAVEBITS = 0x0800
    # Redraws the entire window if a movement or size adjustment changes the height of the client area.
    VREDRAW = 0x0001

class WindowStyle(IntEnum):
    # The window has a thin-line border
    BORDER = 0x00800000
    # The window has a title bar (includes the WS_BORDER style).
    CAPTION = 0x00C00000
    # The window is a child window. A window with this style cannot have a menu bar. This style cannot be used with the WS_POPUP style.
    CHILD = 0x40000000
    # Same as the WS_CHILD style.
    CHILDWINDOW = 0x40000000
    # Excludes the area occupied by child windows when drawing occurs within the parent window. This style is used when creating the parent window.
    CLIPCHILDREN = 0x02000000
    # Clips child windows relative to each other; that is, when a particular child window receives a WM_PAINT message,
    # the WS_CLIPSIBLINGS style clips all other overlapping child windows out of the region of the child window to be updated.
    # If WS_CLIPSIBLINGS is not specified and child windows overlap, it is possible, when drawing within the client area of a child window,
    #to draw within the client area of a neighboring child window.
    CLIPSIBLINGS = 0x04000000
    # The window is initially disabled. A disabled window cannot receive input from the user.
    # To change this after a window has been created, use the EnableWindow function.
    DISABLED = 0x08000000
    # The window has a border of a style typically used with dialog boxes. A window with this style cannot have a title bar.
    DLGFRAME = 0x00400000
    # The window is the first control of a group of controls. The group consists of this first control and all controls defined after it,
    # up to the next control with the WS_GROUP style.
    # The first control in each group usually has the WS_TABSTOP style so that the user can move from group to group.
    # The user can subsequently change the keyboard focus from one control in the group to the next control in the group by using the direction keys.
    # You can turn this style on and off to change dialog box navigation.
    # To change this style after a window has been created, use the SetWindowLong function.
    GROUP = 0x00020000
    # The window has a horizontal scroll bar.
    HSCROLL = 0x00100000
    # The window is initially minimized. Same as the WS_MINIMIZE style.
    ICONIC = 0x20000000
    # The window is initially maximized.
    MAXIMIZE = 0x01000000
    # The window has a maximize button. Cannot be combined with the WS_EX_CONTEXTHELP style. The WS_SYSMENU style must also be specified.
    MAXIMIZEBOX = 0x00010000
    # The window is initially minimized. Same as the WS_ICONIC style.
    MINIMIZE = 0x20000000
    # The window has a minimize button. Cannot be combined with the WS_EX_CONTEXTHELP style. The WS_SYSMENU style must also be specified.
    MINIMIZEBOX = 0x00020000
    # The window is an overlapped window. An overlapped window has a title bar and a border. Same as the WS_TILED style.
    OVERLAPPED = 0x00000000
    # The window is a pop-up window. This style cannot be used with the WS_CHILD style.
    POPUP = 0x80000000
    # The window has a sizing border. Same as the WS_THICKFRAME style.
    SIZEBOX = 0x00040000
    # The window has a window menu on its title bar. The WS_CAPTION style must also be specified.
    SYSMENU = 0x00080000
    # The window is a control that can receive the keyboard focus when the user presses the TAB key.
    # Pressing the TAB key changes the keyboard focus to the next control with the WS_TABSTOP style.
    # You can turn this style on and off to change dialog box navigation. To change this style after a window has been created,
    # use the SetWindowLong function. For user-created windows and modeless dialogs to work with tab stops,
    # alter the message loop to call the IsDialogMessage function.
    TABSTOP = 0x00010000
    # The window has a sizing border. Same as the WS_SIZEBOX style.
    THICKFRAME = 0x00040000
    # The window is an overlapped window. An overlapped window has a title bar and a border. Same as the WS_OVERLAPPED style.
    TILED = 0x00000000
    # The window is initially visible. This style can be turned on and off by using the ShowWindow or SetWindowPos function.
    VISIBLE = 0x10000000
    # The window has a vertical scroll bar.
    VSCROLL = 0x00200000

    # The window is an overlapped window. Same as the WS_OVERLAPPEDWINDOW style.
    TILEDWINDOW =(OVERLAPPED | CAPTION | SYSMENU | THICKFRAME | MINIMIZEBOX | MAXIMIZEBOX)
    # The window is an overlapped window. Same as the TILEDWINDOW style.
    OVERLAPPEDWINDOW =(OVERLAPPED | CAPTION | SYSMENU | THICKFRAME | MINIMIZEBOX | MAXIMIZEBOX)
    # The window is a pop-up window. The CAPTION and POPUPWINDOW styles must be combined to make the window menu visible.
    POPUPWINDOW =(POPUP | BORDER | SYSMENU)

class ExtendedWindowStyles(IntEnum):
    # The window accepts drag-drop files.
    ACCEPTFILES = 0x00000010
    # Forces a top-level window onto the taskbar when the window is visible.
    APPWINDOW = 0x00040000
    # The window has a border with a sunken edge.
    CLIENTEDGE = 0x00000200
    # Paints all descendants of a window in bottom-to-top painting order using double-buffering.
    # Bottom-to-top painting order allows a descendent window to have translucency (alpha) and transparency (color-key) effects,
    # but only if the descendent window also has the TRANSPARENT bit set.
    # Double-buffering allows the window and its descendents to be painted without flicker.
    # This cannot be used if the window has a class style of either OWNDC or CLASSDC.
    # Windows 2000: This style is not supported.
    COMPOSITED = 0x02000000
    # The title bar of the window includes a question mark.
    # When the user clicks the question mark, the cursor changes to a question mark with a pointer.
    # If the user then clicks a child window, the child receives a WM_HELP message.
    # The child window should pass the message to the parent window procedure, which should call the WinHelp function using the HELP_WM_HELP command.
    # The Help application displays a pop-up window that typically contains help for the child window.
    # CONTEXTHELP cannot be used with the MAXIMIZEBOX or MINIMIZEBOX styles.
    CONTEXTHELP = 0x00000400
    # The window itself contains child windows that should take part in dialog box navigation.
    # If this style is specified, the dialog manager recurses into children of this window when performing navigation operations
    #vsuch as handling the TAB key, an arrow key, or a keyboard mnemonic.
    CONTROLPARENT = 0x00010000
    # The window has a double border; the window can, optionally,
    # be created with a title bar by specifying the CAPTION style in the dwStyle parameter.
    DLGMODALFRAME = 0x00000001
    # The window is a layered window. This style cannot be used if the window has a class style of either OWNDC or CLASSDC.
    # Windows 8: The LAYERED style is supported for top-level windows and child windows.
    # Previous Windows versions support LAYERED only for top-level windows.
    LAYERED = 0x00080000
    # If the shell language is Hebrew, Arabic, or another language that supports reading order alignment,
    # the horizontal origin of the window is on the right edge. Increasing horizontal values advance to the left.
    LAYOUTRTL = 0x00400000
    # The window has generic left-aligned properties. This is the default.
    LEFT = 0x00000000
    # If the shell language is Hebrew, Arabic, or another language that supports reading order alignment,
    # the vertical scroll bar (if present) is to the left of the client area. For other languages, the style is ignored.
    LEFTSCROLLBAR = 0x00004000
    # The window text is displayed using left-to-right reading-order properties. This is the default.
    LTRREADING = 0x00000000
    # The window is a MDI child window.
    MDICHILD = 0x00000040
    # A top-level window created with this style does not become the foreground window when the user clicks it.
    # The system does not bring this window to the foreground when the user minimizes or closes the foreground window.
    # The window should not be activated through programmatic access or via keyboard navigation by accessible technology, such as Narrator.
    # To activate the window, use the SetActiveWindow or SetForegroundWindow function.
    # The window does not appear on the taskbar by default. To force the window to appear on the taskbar, use the APPWINDOW style.
    NOACTIVATE = 0x08000000
    # The window does not pass its window layout to its child windows.
    NOINHERITLAYOUT = 0x00100000
    # The child window created with this style does not send the WM_PARENTNOTIFY message to its parent window when it is created or destroyed.
    NOPARENTNOTIFY = 0x00000004
    # The window does not render to a redirection surface.
    # This is for windows that do not have visible content or that use mechanisms other than surfaces to provide their visual.
    NOREDIRECTIONBITMAP = 0x00200000
    # The window has generic "right-aligned" properties. This depends on the window class.
    # This style has an effect only if the shell language is Hebrew, Arabic, or another language that supports reading-order alignment;
    # otherwise, the style is ignored.
    # Using the RIGHT style for static or edit controls has the same effect as using the SS_RIGHT or ES_RIGHT style, respectively.
    # Using this style with button controls has the same effect as using BS_RIGHT and BS_RIGHTBUTTON styles.
    RIGHT = 0x00001000
    # The vertical scroll bar (if present) is to the right of the client area. This is the default.
    RIGHTSCROLLBAR = 0x00000000
    # If the shell language is Hebrew, Arabic, or another language that supports reading-order alignment,
    # the window text is displayed using right-to-left reading-order properties.
    # For other languages, the style is ignored.
    RTLREADING = 0x00002000
    # The window has a three-dimensional border style intended to be used for items that do not accept user input.
    STATICEDGE = 0x00020000
    # The window is intended to be used as a floating toolbar. A tool window has a title bar that is shorter than a normal title bar,
    # and the window title is drawn using a smaller font.
    # A tool window does not appear in the taskbar or in the dialog that appears when the user presses ALT+TAB.
    # If a tool window has a system menu, its icon is not displayed on the title bar.
    # However, you can display the system menu by right-clicking or by typing ALT+SPACE.
    TOOLWINDOW = 0x00000080
    # The window should be placed above all non-topmost windows and should stay above them, even when the window is deactivated.
    # To add or remove this style, use the SetWindowPos function.
    TOPMOST = 0x00000008
    # The window should not be painted until siblings beneath the window (that were created by the same thread) have been painted.
    # The window appears transparent because the bits of underlying sibling windows have already been painted.
    # To achieve transparency without these restrictions, use the SetWindowRgn function.
    TRANSPARENT = 0x00000020
    # The window has a border with a raised edge.
    WINDOWEDGE = 0x00000100
    # The window is an overlapped window.
    OVERLAPPEDWINDOW = (WINDOWEDGE | CLIENTEDGE)
    # The window is palette window, which is a modeless dialog box that presents an array of commands.
    PALETTEWINDOW = (WINDOWEDGE | TOOLWINDOW | TOPMOST)

class DialogBoxStyles(IntEnum):
    ABSALIGN = 0x01
    SYSMODAL = 0x02
    LOCALEDIT = 0x20
    SETFONT = 0x40
    MODALFRAME = 0x80
    NOIDLEMSG = 0x100
    SETFOREGROUND = 0x200
    THREE_DLOOK = 0x0004
    FIXEDSYS = 0x0008
    NOFAILCREATE = 0x0010
    CONTROL = 0x0400
    CENTER = 0x0800
    CENTERMOUSE = 0x1000
    CONTEXTHELP = 0x2000
    SHELLFONT = (SETFONT | FIXEDSYS)

class WinMessages(IntEnum):
    CLOSE = 16
    COMMAND = 273
    INITDIALOG = 272
    NOTIFY = 78
    PAINT = 15
    SIZE = 5

class ShowWindowCommands(IntEnum):
    HIDE = 0
    # SHOWNORMAL = 1
    NORMAL = 1
    SHOWMINIMIZED = 2
    # SHOWMAXIMIZED = 3
    MAXIMIZE = 3
    SHOWNOACTIVATE = 4
    SHOW = 5
    MINIMIZE = 6
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    RESTORE = 9
    SHOWDEFAULT = 10
    # FORCEMINIMIZE = 11
    MAX = 11

class NMHDR(ctypes.Structure):
    _fields_ = [('hwndFrom', HWND),
                ('idFrom',   UINT_PTR),
                ('code',     UINT)]
LPNMHDR = POINTER(NMHDR)

def LOWORD(value):
    """
    Extract the low part of a DWORD (double word).

    Parameters:
        value (int): The DWORD value.

    Returns:
        int: The low word (16 bits) of the DWORD value.
    """
    return value & 0xFFFF


def HIWORD(value):
    """
    Extract the high part of a DWORD (double word).

    Parameters:
        value (int): The DWORD value.

    Returns:
        int: The high word (16 bits) of the DWORD value.
    """
    return (value >>16) & 0xFFFF

def MAKELPARAM(low, high):
    """
    Constructs a LPARAM value from two 16-bit values.

    Args:
        low: The lower 16 bits value.
        high: The upper 16 bits value.

    Returns:
        LPARAM: The combined 32-bit value where low occupies the lower 16 bits
        and high occupies the upper 16 bits.
    """
    return (low & 0xFFFF) | ((high & 0xFFFF) << 16)
MAKELONG = MAKELPARAM

class NMITEMACTIVATE(ctypes.Structure):
    _fields_ = [('hdr',       LPNMHDR),
                ('iItem',     INT),
                ('iSubItem',  INT),
                ('uNewState', UINT),
                ('uOldState', UINT),
                ('uChanged',  UINT),
                ('ptAction',  POINT),
                ('lParam',    LPARAM),
                ('uKeyFlags', UINT)]
LPNMITEMACTIVATE = ctypes.POINTER(NMITEMACTIVATE)


class CCM(IntEnum):
    FIRST               = 0x2000         # Common control shared messages
    LAST                = FIRST + 0x200
    SETBKCOLOR          = FIRST + 1      # lParam is bkColor
    SETCOLORSCHEME      = FIRST + 2      # lParam is color scheme
    GETCOLORSCHEME      = FIRST + 3      # fills in COLORSCHEME pointed to by lParam
    GETDROPTARGET       = FIRST + 4
    SETUNICODEFORMAT    = FIRST + 5
    GETUNICODEFORMAT    = FIRST + 6
    SETVERSION          = FIRST + 0x7
    GETVERSION          = FIRST + 0x8
    SETNOTIFYWINDOW     = FIRST + 0x9    # wParam == hwndParent.
    SETWINDOWTHEME      = FIRST + 0xb
    DPISCALE            = FIRST + 0xc    # wParam == Awareness


class NM(IntEnum):
    FIRST                = 0
    OUTOFMEMORY          = FIRST-1
    CLICK                = FIRST-2    # uses NMCLICK struct
    DBLCLK               = FIRST-3
    RETURN               = FIRST-4
    RCLICK               = FIRST-5    # uses NMCLICK struct
    RDBLCLK              = FIRST-6
    SETFOCUS             = FIRST-7
    KILLFOCUS            = FIRST-8
    CUSTOMDRAW           = FIRST-12
    HOVER                = FIRST-13
    NCHITTEST            = FIRST-14   # uses NMMOUSE struct
    KEYDOWN              = FIRST-15   # uses NMKEY struct
    RELEASEDCAPTURE      = FIRST-16
    SETCURSOR            = FIRST-17   # uses NMMOUSE struct
    CHAR                 = FIRST-18   # uses NMCHAR struct
    TOOLTIPSCREATED      = FIRST-19   # notify of when the tooltips window is create
    LDOWN                = FIRST-20
    RDOWN                = FIRST-21
    THEMECHANGED         = FIRST-22
    FONTCHANGED          = FIRST-23
    CUSTOMTEXT           = FIRST-24   # uses NMCUSTOMTEXT struct
    TVSTATEIMAGECHANGING = FIRST-24   # uses NMTVSTATEIMAGECHANGING struct, defined after HTREEITEM
    LAST                 = FIRST-99


class WM_CommandDelegator:
    '''
        A descriptor class that acts as a delegator for Windows WM_COMMAND notifications.
        Used only internally.
    '''
    def __init__(self, wm_command_id):
        self.id = wm_command_id

    def __set__(self, control, value):
        control.registeredCommands[self.id] = value


class WM_NotifyDelegator:
    '''
        A descriptor class that acts as a delegator for Windows WM_NOTIFY notifications.
        Used only internally.
    '''
    def __init__(self, wm_notify_id, returned_struct):
        self.id = wm_notify_id
        self.returned_struct = returned_struct

    def __set__(self, control, value):
        control.registeredNotifications[self.id] = (value, self.returned_struct)
