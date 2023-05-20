from Npp import console
from WinDialog import (
    Dialog, create_dialog_from_rc,
    Button, UpDown
)

console.show()

rc = '''
1 DIALOGEX 0, 0, 250, 100
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "StatusBar Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "", 0, "msctls_updown32", WS_CHILD | WS_VISIBLE | WS_TABSTOP, 19, 18, 10, 20
   CONTROL "Get value", 0, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 31, 18, 69, 20
   CONTROL "Set Range", 1, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 102, 18, 69, 20
}
'''

def get_value():
    print(dlg.msctls_updown32_0.get_value())

def set_range():
    print(dlg.msctls_updown32_0.set_range(-5, 5))


dlg = create_dialog_from_rc(rc_code=rc)
dlg.msctls_updown32_0.set_range(0, 5)
dlg.button_0.on_click = get_value
dlg.button_1.on_click = set_range
dlg.center = True
dlg.show()

class UpDownDialog(Dialog):
    def __init__(self, title='UpDown Dialog'):
        super().__init__(title)
        self.size = (250, 100)
        self.center = True
        self.btn0 = Button('Get value', (69, 20), (31, 18))
        self.btn1 = Button('Set Range', (69, 20), (102, 18))
        self.up_down = UpDown('', (10, 20), (19, 18))
        self.btn0.on_click = self.get_value
        self.btn1.on_click = self.set_range
        self.show()

    def get_value(self):
        print(self.up_down.get_value())

    def set_range(self):
        self.up_down.set_range(-5, 5)

UpDownDialog()

# class ScintillaDialog(Dialog):
    # def __init__(self, title='Scintilla Dialog'):
        # super().__init__(title)
        # self.size = (250, 125)
        # self.center = True
        # self.sci = Scintilla('', (247, 122), (1, 1))
        # self.show()

# ScintillaDialog()