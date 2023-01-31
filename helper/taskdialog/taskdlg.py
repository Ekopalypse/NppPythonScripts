from ctypes import *
from ctypes.wintypes import *
import platform


LRESULT = LONG_PTR = LONG if platform.architecture()[0] == '32bit' else LARGE_INTEGER
HRESULT =  LONG
TASKDIALOGCALLBACK = WINFUNCTYPE(HRESULT, HWND, UINT, WPARAM, LPARAM, LONG_PTR)

class _TDM:
    # task dialog messages
    NAVIGATE_PAGE                       = 1125  # wParam = 0, lParam addressof new config structure
    CLICK_BUTTON                        = 1126  # wParam = Button ID
    SET_MARQUEE_PROGRESS_BAR            = 1127  # wParam = 0 (nonMarque) wParam != 0 (Marquee)
    SET_PROGRESS_BAR_STATE              = 1128  # wParam = new progress state
    SET_PROGRESS_BAR_RANGE              = 1129  # lParam = MAKELPARAM(nMinRange, nMaxRange)
    SET_PROGRESS_BAR_POS                = 1130  # wParam = new position
    SET_PROGRESS_BAR_MARQUEE            = 1131  # wParam = 0 (stop marquee), wParam != 0 (start marquee), lparam = speed (milliseconds between repaints)
    SET_ELEMENT_TEXT                    = 1132  # wParam = element (TASKDIALOG_ELEMENTS), lParam = new element text (LPCWSTR)
    CLICK_RADIO_BUTTON                  = 1134  # wParam = Radio Button ID
    ENABLE_BUTTON                       = 1135  # lParam = 0 (disable), lParam != 0 (enable), wParam = Button ID
    ENABLE_RADIO_BUTTON                 = 1136  # lParam = 0 (disable), lParam != 0 (enable), wParam = Radio Button ID
    CLICK_VERIFICATION                  = 1137  # wParam = 0 (unchecked), 1 (checked), lParam = 1 (set key focus)
    UPDATE_ELEMENT_TEXT                 = 1138  # wParam = element (TASKDIALOG_ELEMENTS), lParam = new element text (LPCWSTR)
    SET_BUTTON_ELEVATION_REQUIRED_STATE = 1139  # wParam = Button ID, lParam = 0 (elevation not required), lParam != 0 (elevation required)
    UPDATE_ICON                         = 1140  # wParam = icon element (TASKDIALOG_ICON_ELEMENTS), lParam = new icon (hIcon if TDF_USE_HICON_* was set, PCWSTR otherwise)


class _TDN:
    # task dialog notifications
    CREATED                 = 0
    NAVIGATED               = 1
    BUTTON_CLICKED          = 2   # wParam = Button ID
    HYPERLINK_CLICKED       = 3   # lParam = (LPCWSTR)pszHREF
    TIMER                   = 4   # wParam = Milliseconds since dialog created or timer reset
    DESTROYED               = 5
    RADIO_BUTTON_CLICKED    = 6   # wParam = Radio Button ID
    DIALOG_CONSTRUCTED      = 7
    VERIFICATION_CLICKED    = 8   # wParam = 1 if checkbox checked, 0 if not, lParam is unused and always 0
    HELP                    = 9
    EXPANDO_BUTTON_CLICKED  = 10  # wParam = 0 (dialog is now collapsed), wParam != 0 (dialog is now expanded)


class _TDF:
    # task dialog flags
    ENABLE_HYPERLINKS           = 0x1
    USE_HICON_MAIN              = 0x2
    USE_HICON_FOOTER            = 0x4
    ALLOW_DIALOG_CANCELLATION   = 0x8
    USE_COMMAND_LINKS           = 0x10
    USE_COMMAND_LINKS_NO_ICON   = 0x20
    EXPAND_FOOTER_AREA          = 0x40
    EXPANDED_BY_DEFAULT         = 0x80
    VERIFICATION_FLAG_CHECKED   = 0x100
    SHOW_PROGRESS_BAR           = 0x200
    SHOW_MARQUEE_PROGRESS_BAR   = 0x400
    CALLBACK_TIMER              = 0x800
    POSITION_RELATIVE_TO_WINDOW = 0x1000
    RTL_LAYOUT                  = 0x2000
    NO_DEFAULT_RADIO_BUTTON     = 0x4000
    CAN_BE_MINIMIZED            = 0x8000
# if (NTDDI_VERSION >= NTDDI_WIN8)
    NO_SET_FOREGROUND           = 0x10000,  # Don't call SetForegroundWindow() when activating the dialog
# endif # (NTDDI_VERSION >= NTDDI_WIN8)
    SIZE_TO_CONTENT             = 0x1000000   # used by ShellMessageBox to emulate MessageBox sizing behavior    


class _TASKDIALOG_BUTTON(Structure):
    _pack_ = 1
    _fields_ = [
        ('nButtonID', INT),
        ('pszButtonText', LPCWSTR)
    ]


class _TASKDIALOGCONFIG(Structure):
    _pack_ = 1
    _fields_ = [
        ('cbSize',                  UINT),
        ('hwndParent',              HWND),
        ('hInstance',               HINSTANCE),
        ('dwFlags',                 UINT),  # TASKDIALOG_FLAGS),
        ('dwCommonButtons',         UINT),  # TASKDIALOG_COMMON_BUTTON_FLAGS),
        ('pszWindowTitle',          LPCWSTR),
        ('hMainIcon',               HICON),
        ('pszMainInstruction',      LPCWSTR),
        ('pszContent',              LPCWSTR),
        ('cButtons',                UINT),
        ('pButtons',                POINTER(_TASKDIALOG_BUTTON)),
        ('nDefaultButton',          INT),
        ('cRadioButtons',           UINT),
        ('pRadioButtons',           POINTER(_TASKDIALOG_BUTTON)),
        ('nDefaultRadioButton',     INT),
        ('pszVerificationText',     LPCWSTR),
        ('pszExpandedInformation',  LPCWSTR),
        ('pszExpandedControlText',  LPCWSTR),
        ('pszCollapsedControlText', LPCWSTR),
        ('hFooterIcon',             HICON),
        ('pszFooter',               LPCWSTR),
        ('pfCallback',              TASKDIALOGCALLBACK),
        ('lpCallbackData',          LONG_PTR),
        ('cxWidth',                 UINT),
    ]

    def __init__(self):
        self.cbSize = sizeof(self)


TaskDialogIndirect = WinDLL('comctl32').TaskDialogIndirect
TaskDialogIndirect.argtypes = [POINTER(_TASKDIALOGCONFIG), 
                               POINTER(INT), 
                               POINTER(INT), 
                               POINTER(BOOL)]
TaskDialogIndirect.restype = HRESULT

SendMessage = WinDLL('user32').SendMessageW
SendMessage.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessage.restype = LRESULT

FindWindow = WinDLL('user32').FindWindowW
FindWindow.argtypes = [LPCWSTR, LPCWSTR]
FindWindow.restype = HWND

ShellExecute = WinDLL('shell32').ShellExecuteW
ShellExecute.argtypes = [HWND, LPCWSTR, LPCWSTR, LPCWSTR, LPCWSTR, INT]
ShellExecute.restype = HINSTANCE

class Dialog(object):

    def __init__(self, modal=True):
        self.event_handler = { 
            _TDN.CREATED: self.__on_created,
            _TDN.NAVIGATED: self.__on_navigated,
            _TDN.BUTTON_CLICKED: self.__on_button_clicked,
            _TDN.HYPERLINK_CLICKED: self.__on_hyperlink_clicked,
            _TDN.TIMER: self.__on_timer,
            _TDN.DESTROYED: self.__on_destroyed,
            _TDN.RADIO_BUTTON_CLICKED: self.__on_radio_button_clicked,
            _TDN.DIALOG_CONSTRUCTED: self.__on_dialog_constructed,
            _TDN.VERIFICATION_CLICKED: self.__on_verification_clicked,
            _TDN.HELP: self.__on_help,
            _TDN.EXPANDO_BUTTON_CLICKED: self.__on_expand_button_clicked,
        }
        
        self.parent = FindWindow(u'Notepad++', None) if modal else None
        self.checked_verification = False
        self.hwnd = None
        self.button_callbacks = {}
        self._init_config()

    def _init_config(self):
        self.config = _TASKDIALOGCONFIG()
        self.config.pfCallback = TASKDIALOGCALLBACK(self._callback)
        self.config.hwndParent = self.parent
        self.config.hInstance = None
        self.config.dwFlags = _TDF.ALLOW_DIALOG_CANCELLATION

    def _callback(self, hwnd, msg, wparam, lparam, lpRefData):
        if msg == _TDN.BUTTON_CLICKED and wparam == 2:  # ensures that the dialog can be cancelled
            return 0        
        if msg in self.event_handler:
            args = {'hwnd': hwnd, 'wparam': wparam, 'lparam': lparam}
            result = self.event_handler[msg](args)
            return 1 if result is None else result
        return 1

    def __on_created(self, args): 
        self.hwnd = args['hwnd']
        return 1

    def __on_button_clicked(self, args):
        callback = self.button_callbacks[args['wparam']]
        if callback is not None:
            res = callback(args['wparam'])
            if res in [0, 1]:
                return res
        return 1

    def __on_radio_button_clicked(self, args): 
        callback = self.button_callbacks[args['wparam']]
        if callback is not None:
            res = callback(args['wparam'])
            if res in [0, 1]:
                return res
        return 1

    def __on_verification_clicked(self, args): 
        self.checked_verification = not self.checked_verification
        if self.checked_verification:
            self.config.dwFlags |= _TDF.VERIFICATION_FLAG_CHECKED
        else:
            self.config.dwFlags &=~ _TDF.VERIFICATION_FLAG_CHECKED
        return 1

    def __on_hyperlink_clicked(self, args):
        ShellExecute(None, u'open', wstring_at(args['lparam']), None, None, 1)
        return 1

    def __on_navigated(self, args): return 1
    def __on_timer(self, args): return 1
    def __on_destroyed(self, args): return 0
    def __on_dialog_constructed(self, args): return 1
    def __on_help(self, args): return 1
    def __on_expand_button_clicked(self, args): return 1

    def __create_buttons(self, list_of_buttons):
        buttons_array = (_TASKDIALOG_BUTTON * len(list_of_buttons))()
        for i, button in enumerate(list_of_buttons):
            buttons_array[i].nButtonID = button[0]
            buttons_array[i].pszButtonText = button[1]
            self.button_callbacks[button[0]] = None if len(button) < 3 else button[2]
        return buttons_array

    def use_hyper_links(self, enable=True):
        '''
        '''
        if enable:
            self.config.dwFlags |= _TDF.ENABLE_HYPERLINKS
        else:
            self.config.dwFlags &=~ _TDF.ENABLE_HYPERLINKS

    def use_command_links(self, enable=True):
        '''
        '''
        if enable:
            self.config.dwFlags |= _TDF.USE_COMMAND_LINKS
        else:
            self.config.dwFlags &=~ _TDF.USE_COMMAND_LINKS
    
    def create_page(self,
                    title=None,
                    main_instruction=None,
                    content=None,
                    default_button=None,
                    push_buttons=None, 
                    default_radio_button=None,
                    radio_buttons=None, 
                    verification_text=None,
                    expanded_information=None,
                    expanded_control_text=None,
                    collapsed_control_text=None,
                    footer=None,
                    width=None):
        ''' Creates a task dialog page. 
            Contains messages, title, verification check box, command links, push buttons, and radio buttons. 
            
            Every subsequent call to create_page will only overwrite/delete the members if they are provided explicitly,
            otherwise the previous value is still used. So in order to, for example, remove the footer text on the next page
            one has to provide `footer=''`.
            
            The buttons needs to be provided as a list of tuples having the following format:
            
                id, name of the button, callback function
                
                For example: 
                push_buttons = [(1000, "Close", self.on_close), (1001, "Next", self.on_next)]
        '''
        
        if title is not None:
            self.config.pszWindowTitle = LPCWSTR(title)

        if main_instruction is not None:
            self.config.pszMainInstruction = LPCWSTR(main_instruction)
            
        if content is not None:
            self.config.pszContent = LPCWSTR(content)
            
        if push_buttons is not None:
            self.config.cButtons = len(push_buttons)
            if self.config.cButtons > 0:
                self.config.pButtons = self.__create_buttons(push_buttons)

        if default_button is not None:
            self.config.nDefaultButton = default_button
        
        if radio_buttons is not None:
            self.config.cRadioButtons = len(radio_buttons)
            if self.config.cRadioButtons > 0:
                self.config.pRadioButtons = self.__create_buttons(radio_buttons)

        if default_radio_button is not None:
            self.config.nDefaultRadioButton = default_radio_button
        
        if verification_text is not None:
            self.config.pszVerificationText = LPCWSTR(verification_text)

        if expanded_information is not None:
            self.config.pszExpandedInformation = LPCWSTR(expanded_information)
        
        if expanded_control_text is not None:
            self.config.pszExpandedControlText = LPCWSTR(expanded_control_text)
        
        if collapsed_control_text is not None:
            self.config.pszCollapsedControlText = LPCWSTR(collapsed_control_text)
        
        if footer is not None:
            self.config.pszFooter = LPCWSTR(footer)

        if width is not None:
            self.config.cxWidth = width

        SendMessage(self.hwnd, _TDM.NAVIGATE_PAGE, 0, addressof(self.config))
       
    def show(self):
        ''' Calls the TaskDialogIndirect to display the dialog.
            pnButton and pnRadioButton are NOT used.
        '''
        TaskDialogIndirect(
            byref(self.config), None, None, byref(BOOL(self.checked_verification))
        )
