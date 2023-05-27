from Npp import console
from WinDialog import (
    Dialog, create_dialog_from_rc,
    Button, UpDown, TextBox
)

console.show()

rc = '''
1 DIALOGEX 0, 0, 250, 100
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "StatusBar Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "", 0, "msctls_updown32", WS_CHILD | WS_VISIBLE | WS_TABSTOP, 19, 18, 10, 14
   CONTROL "Set Range", 0, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 57, 18, 69, 14
   CONTROL "", 0, EDIT, ES_LEFT | WS_CHILD | WS_VISIBLE | WS_BORDER | WS_TABSTOP, 32, 18, 22, 14
}
'''

def set_range():
    dlg.msctls_updown32_0.setRange(-8, 2)

def on_deltapos(args):
    dlg.edit_0.setText(f"{args.iPos}")

def initialize():
    dlg.msctls_updown32_0.setRange(-5, 5)

dlg = create_dialog_from_rc(rc_code=rc)
dlg.msctls_updown32_0.setRange(0, 5)
dlg.msctls_updown32_0.onDeltaPos = on_deltapos
dlg.button_0.on_click = set_range
dlg.center = True
dlg.initialize = initialize
dlg.show()

class UpDownDialog(Dialog):
    def __init__(self, title='UpDown Dialog'):
        super().__init__(title)
        self.size = (250, 100)
        self.center = True
        self.btn0 = Button('Set Range', (69, 14), (57, 18))
        self.up_down = UpDown('', (10, 14), (19, 18))
        self.up_down.onDeltaPos = self.on_deltapos
        self.edit = TextBox('', (22, 14), (32, 18))
        self.btn0.onClick = self.set_range
        # self.initialize = self.on_init
        self.show()

    def on_init(self):
        self.up_down.setRange(-5, 5)

    def on_deltapos(self, args):
        self.edit.setText(f"{args.iPos}")

    def get_value(self):
        print(self.up_down.getValue())

    def set_range(self):
        self.up_down.setRange(-8, 2)

UpDownDialog()
