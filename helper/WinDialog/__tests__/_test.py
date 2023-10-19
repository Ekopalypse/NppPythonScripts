from Npp import console
from WinDialog import  Dialog, create_dialog_from_rc

console.show()

rc = '''
1 DIALOGEX 0, 0, 250, 100
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "Test Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
'''

def on_close():
    print(f'closing: {dlg.size=} {dlg.position=}')

try:
    print("trying")
    dlg
except NameError:
    print('initializing')
    dlg = create_dialog_from_rc(rc_code=rc)
    dlg.center = False
    dlg.onClose = on_close
    dlg.useLastDialogPos = True
    dlg.show()
else:
    print(f'show it:{dlg.size=} {dlg.position=}')
    dlg.show()