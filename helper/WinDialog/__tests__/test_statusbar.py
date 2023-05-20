from Npp import console
from WinDialog import (
    Dialog, create_dialog_from_rc,
    Button, StatusBar, SBARS
)

console.show()

rc = '''
1 DIALOGEX 0, 0, 250, 100
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "StatusBar Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "", 0, "msctls_statusbar32", SBARS_SIZEGRIP | WS_CHILD | WS_VISIBLE, 0, 88, 249, 12
   CONTROL "Set statusbar text", 0, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 31, 43, 122, 14
}
'''

def set_message():
    dlg.msctls_statusbar32_0.set_text('Some message to display')

dlg = create_dialog_from_rc(rc_code=rc)
dlg.button_0.on_click = set_message
dlg.center = True
dlg.show()

class StatusBarDialog(Dialog):
    def __init__(self, title='StatusBar Dialog'):
        super().__init__(title)
        self.size = (250, 100)
        self.center = True
        self.btn_set_msg = Button('Set statusbar text', (122, 14), (31, 43))
        self.status_bar = StatusBar('', (249, 12), (0, 88))
        self.status_bar.style += SBARS.SIZEGRIP
        self.btn_set_msg.on_click = self.set_message
        self.show()

    def set_message(self):
        self.status_bar.set_text('Some message to display')
StatusBarDialog()