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
    index = dlg.listbox_0.get_selected_item()
    if index >= 0:
        print(dlg.some_items[index])

def on_init():
    dlg.listbox_0.add_strings(dlg.some_items)

dlg = create_dialog_from_rc(rc_code=rc)
dlg.button_0.on_click = get_selected_items
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
        self.lb1.add_strings(['Item1', 'Item2', 'Item3',])
        self.lb1.on_selchange = self.on_selchange

        self.button = Button('Get Selected Items', (150, 25), (50, 68))
        self.button.on_click = self.on_click
        self.initialize = self.on_init

        self.some_items = ['Item1', 'Item2', 'Item3',]
        self.show()

    def on_init(self):
        self.lb1.add_strings(self.some_items)

    def on_selchange(self):
        print('changed')

    def on_click(self):
        index = self.lb1.get_selected_item()
        if index >= 0:
            print(self.some_items[index])


ListBoxDialog()