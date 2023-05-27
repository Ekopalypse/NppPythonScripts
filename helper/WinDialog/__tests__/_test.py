from Npp import console
from WinDialog import (
    Dialog, create_dialog_from_rc,
    Button
)
from WinDialog.controls.button import BST

console.show()

rc = '''
1 DIALOGEX 0, 0, 250, 100
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "Test Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "btn_3", 2, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP,  31, 18, 30, 20
   CONTROL "btn_0", 4, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP,  91, 18, 30, 20
   CONTROL "btn_4", 0, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP,  61, 18, 30, 20
   CONTROL "btn_1", 1, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 121, 18, 30, 20
   CONTROL "btn_2", 3, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 151, 18, 30, 20
}
'''
def on_init():
    dlg.button_1.setCheckState(BST.CHECKED)
    print(dlg.button_0.getCheckState())
    print(dlg.button_1.getCheckState())

dlg = create_dialog_from_rc(rc_code=rc)
dlg.initialize = on_init
dlg.center = True
dlg.show()