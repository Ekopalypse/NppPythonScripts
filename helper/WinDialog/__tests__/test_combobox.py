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
    selected_item = dlg.comboboxex32_0.get_selected_item()
    if selected_item == 0:
        dlg.combobox_0.update(['100', '101', '102',])
    elif selected_item == 1:
        dlg.combobox_0.update(['200', '201', '202',])
    else:
        dlg.combobox_0.update(['300', '301', '302',])

def on_selchange2():
    print(dlg.comboboxex32_0.items[dlg.comboboxex32_0.get_selected_item()])

def on_init():
    dlg.comboboxex32_0.insert_items(['Item1', 'Item2', 'Item3',])

def on_insertitem(args): print('on_insertitem', args._fields_)
def on_deleteitem(args): print('on_deleteitem', args._fields_)
def on_beginedit(args): print('on_beginedit', args._fields_)
def on_endedit(args): print('on_endedit', args._fields_)
def on_getdispinfo(args): print('on_getdispinfo', args._fields_)
def on_dragbegin(args): print('on_dragbegin', args._fields_)

dlg = create_dialog_from_rc(rc_code=rc)
dlg.center = True
dlg.comboboxex32_0.on_selchange = on_selchange
dlg.comboboxex32_0.on_insertitem = on_insertitem
dlg.comboboxex32_0.on_deleteitem = on_deleteitem
dlg.comboboxex32_0.on_beginedit = on_beginedit
dlg.comboboxex32_0.on_endedit = on_endedit
dlg.comboboxex32_0.on_getdispinfo = on_getdispinfo
dlg.comboboxex32_0.on_dragbegin = on_dragbegin


dlg.combobox_0.items = []
dlg.combobox_0.on_selchange = on_selchange2

dlg.initialize = on_init
dlg.show()

class ComboBoxDialog(Dialog):
    def __init__(self, title='test dialog'):
        super().__init__(title)
        self.size = (250, 125)
        self.center = True
        self.cb1 = ComboBoxEx('', (80,100), (10,10))
        self.cb1.on_selchange = self.on_selchange

        self.cb2 = ComboBox('', (80,100), (10,60))
        self.cb2.on_selchange = self.on_selchange2

        self.initialize = self.on_init
        self.show()

    def on_init(self):
        self.cb1.insert_items(['Item1', 'Item2', 'Item3',])

    def on_selchange(self):
        selected_item = self.cb1.get_selected_item()
        if selected_item == 0:
            self.cb2.update(['100', '101', '102',])
        elif selected_item == 1:
            self.cb2.update(['200', '201', '202',])
        else:
            self.cb2.update(['300', '301', '302',])

    def on_selchange2(self):
        print(self.cb1.items[self.cb1.get_selected_item()])

ComboBoxDialog()