from Npp import console
from WinDialog import Dialog, Button, create_dialog_from_rc

console.show()

# these two functions are used by 1st and 2nd dialog
def on_close():
    dlg.terminate()

def on_ok():
    print('ok')

# 1st dialog
rc = '''
1 DIALOGEX 0, 0, 250, 100
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "Created from RC code"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "&OK", 1, BUTTON, BS_DEFPUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 130, 78, 50, 11
   CONTROL "&Close", 2, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 187, 78, 50, 11       //             close_btn
}
'''
dlg = create_dialog_from_rc(rc_code=rc)
dlg.center = True
dlg.button_1.onClick = on_ok
dlg.close_btn.onClick = on_close
dlg.show()
print(id(dlg))
del(dlg)

# 2nd dialog
dlg = Dialog(title='Created by direct use of the Dialog class')
dlg.size = (250, 100)
dlg.center = True
ok_btn = Button(title='&OK', size=(50, 11), position=(130, 78))
ok_btn.onClick = on_ok
close_btn = Button(title='&Close', size=(50, 11), position=(187, 78))
close_btn.onClick = on_close
dlg.controlList = [ok_btn, close_btn]
dlg.show()
print(id(dlg))
del(dlg)

# 3rd dialog
class TestDialog(Dialog):
    def __init__(self, title='Created through inheritance from Dialog'):
        super().__init__(title)
        self.size = (250, 100)
        self.center = True

        self.ok_btn = Button(title='&OK', size=(50, 11), position=(130, 78))
        self.ok_btn.onClick = self.on_ok

        self.close_btn = Button(title='&Close', size=(50, 11), position=(187, 78))
        self.close_btn.onClick = self.on_close

        self.show()

    def on_close(self):
        self.terminate()

    def on_ok(self):
        print('ok')

dlg = TestDialog()
print(id(dlg))
del(dlg)
