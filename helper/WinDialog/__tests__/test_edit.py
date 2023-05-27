from Npp import console
from WinDialog import (
    Dialog, create_dialog_from_rc,
    TextBox,
    Button

)

console.show()

rc = '''
1 DIALOGEX 0, 0, 250, 100
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "TextBox Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "123", 0, EDIT, ES_LEFT | WS_CHILD | WS_VISIBLE | WS_BORDER | WS_TABSTOP, 5, 5, 240, 12
   CONTROL "Get Text", 0, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 100, 35, 50, 14
   CONTROL "Set Text", 1, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 100, 55, 50, 14
}
'''

def get_text():
    print(dlg.edit_0.getText())

def set_text():
    dlg.edit_0.setText('1234567890')

dlg = create_dialog_from_rc(rc_code=rc)
dlg.center = True
dlg.edit_0.on_change = get_text
dlg.button_0.onClick = get_text
dlg.button_1.onClick = set_text
dlg.show()


class TextBoxDialog(Dialog):
    def __init__(self, title='TextBox Dialog'):
        super().__init__(title)
        self.size = (250, 100)
        self.center = True
        self.textbox = TextBox('123', (240, 12), (5, 5))
        self.textbox.on_change = self.get_text
        self.button = Button('Get Text', (50, 14), (100, 35))
        self.button.onClick = self.get_text
        self.button2 = Button('Set Text', (50, 14), (100, 55))
        self.button2.onClick = self.set_text

        self.show()

    def get_text(self):
        print(self.textbox.getText())

    def set_text(self):
        self.textbox.setText('1234567890')

TextBoxDialog()