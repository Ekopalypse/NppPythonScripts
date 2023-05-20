
from WinDialog import (
    Dialog, create_dialog_from_rc,
    ListView,
    Button

)

rc = '''
1 DIALOGEX 0, 0, 250, 125
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "TextBox Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "", 0, "SysListView32", LVS_REPORT | WS_CHILD | WS_VISIBLE | WS_BORDER | WS_TABSTOP, 5, 5, 240, 76 , LVS_EX_CHECKBOXES // listview
   CONTROL "Get selected rows", 0, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 84, 100, 87, 14
}
'''

def get_selected_rows():
    print('get_selected_rows')

def init_listview():
    print('init list view')

dlg = create_dialog_from_rc(rc_code=rc)
dlg.center = True
dlg.listview.columns = ['Col{}'.format(x) for x in range(2)]
dlg.listview.rows = [('{}'.format(x),'{}'.format(pow(x,x))) for x in range(100)]
dlg.listview.show_headers = True
dlg.listview.fit_last_column = False
dlg.button_0.on_click = get_selected_rows
dlg.initialize = init_listview
dlg.show()

class ListViewDialog(Dialog):
    def __init__(self, title='test dialog'):
        super().__init__(title)
        self.listview = ListView('', (180, 200), (0,0))
        self.listview.columns = ['Col{}'.format(x) for x in range(2)]
        self.listview.rows = [('{}'.format(x),'{}'.format(pow(x,x))) for x in range(100)]
        self.show()

