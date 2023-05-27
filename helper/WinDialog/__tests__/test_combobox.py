from Npp import console
from WinDialog import (
    Dialog, create_dialog_from_rc,
    ComboBox, ComboBoxEx,
)

console.show()

rc = '''
1 DIALOGEX 0, 0, 250, 125
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "ComboBox Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "", 0, "ComboBoxEx32", CBS_DROPDOWN | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 10, 10, 80, 100
   CONTROL "", 0, COMBOBOX, CBS_DROPDOWN | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 10, 60, 80, 100
}
'''

def on_selchange():
    selected_item = dlg.comboboxex32_0.getSelectedItem()
    if selected_item == 0:
        dlg.combobox_0.set(['100', '101', '102',])
    elif selected_item == 1:
        dlg.combobox_0.set(['200', '201', '202',])
    else:
        dlg.combobox_0.set(['300', '301', '302',])

def on_selchange2():
    print(dlg.combobox_0.getSelectedItem())

def on_init():
    dlg.comboboxex32_0.append(['Item1', 'Item2', 'Item3',])

dlg = create_dialog_from_rc(rc_code=rc)
dlg.center = True
dlg.comboboxex32_0.onSelChange = on_selchange
dlg.combobox_0.items = []
dlg.combobox_0.onSelChange = on_selchange2
dlg.initialize = on_init
dlg.show()

class ComboBoxDialog(Dialog):
    def __init__(self, title='test dialog'):
        super().__init__(title)
        self.size = (250, 125)
        self.center = True
        self.cb1 = ComboBoxEx('', (80,100), (10,10))
        self.cb1.onSelChange = self.on_selchange

        self.cb2 = ComboBox('', (80,100), (10,60))
        self.cb2.onSelChange = self.on_selchange2

        self.initialize = self.on_init
        self.show()

    def on_init(self):
        self.cb1.append(['Item1', 'Item2', 'Item3',])

    def on_selchange(self):
        selected_item = self.cb1.getSelectedItem()
        if selected_item == 0:
            self.cb2.set(['100', '101', '102',])
        elif selected_item == 1:
            self.cb2.set(['200', '201', '202',])
        else:
            self.cb2.set(['300', '301', '302',])

    def on_selchange2(self):
        print(self.cb2.getSelectedItem())

ComboBoxDialog()