from Npp import console
from WinDialog import (
    Dialog, create_dialog_from_rc,
    ListBox,
    Button
)

console.show()

rc = '''
1 DIALOGEX 0, 0, 250, 125
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "ListBox Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "", 0, LISTBOX, LBS_STANDARD | LBS_HASSTRINGS | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 5, 5, 240, 60
   CONTROL "Get Selected Items", 0, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 50, 68, 150, 25
}
'''

def get_selected_items():
    index = dlg.listbox_0.getSelectedItem()
    if index >= 0:
        print(dlg.some_items[index])

def on_init():
    dlg.listbox_0.addStrings(dlg.some_items)
    dlg.some_items.append('Item4')
    dlg.listbox_0.addString(dlg.some_items[-1])

dlg = create_dialog_from_rc(rc_code=rc)
dlg.button_0.onClick = get_selected_items
dlg.center = True
dlg.some_items = ['Item1', 'Item2', 'Item3',]
dlg.initialize = on_init
dlg.show()

class ListBoxDialog(Dialog):
    def __init__(self, title='ListBox Dialog'):
        super().__init__(title)
        self.size = (250, 125)
        self.center = True
        self.lb1 = ListBox('', (240, 60), (5, 5))
        # self.lb1.addStrings(['Item1', 'Item2', 'Item3',])
        self.lb1.on_selchange = self.on_selchange

        self.button = Button('Get Selected Items', (150, 25), (50, 68))
        self.button.onClick = self.on_click
        self.initialize = self.on_init

        self.some_items = ['Item1', 'Item2', 'Item3',]
        self.show()

    def on_init(self):
        self.lb1.addStrings(self.some_items)
        self.some_items.append('Item4')
        self.lb1.addString(self.some_items[-1])

    def on_selchange(self):
        print('changed')

    def on_click(self):
        index = self.lb1.getSelectedItem()
        if index >= 0:
            print(self.some_items[index])


ListBoxDialog()