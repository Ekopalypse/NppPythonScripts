from Npp import console
from WinDialog import (
    Dialog, create_dialog_from_rc,
    Label, TruncatedLabel, BlackFramedLabel, CenteredLabel, RigthAlignedLabel,
)

console.show()

rc = '''
1 DIALOGEX 0, 0, 250, 100
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "Label Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "Simple label",         0, STATIC, SS_SIMPLE | WS_CHILD | WS_VISIBLE | WS_GROUP,                  5,  4,  50, 10
   CONTROL "Truncated text label", 1, STATIC, SS_LEFT | SS_WORDELLIPSIS | WS_CHILD | WS_VISIBLE | WS_GROUP,  5, 15,  50, 10
   CONTROL "",                     2, STATIC, SS_BLACKFRAME | WS_CHILD | WS_VISIBLE | WS_GROUP,              5, 30, 130, 40
   CONTROL "Blackframed labels",   3, STATIC, SS_SIMPLE | WS_CHILD | WS_VISIBLE | WS_GROUP,                 10, 35, 120, 10
   CONTROL "Centered",             4, STATIC, SS_CENTER | WS_CHILD | WS_VISIBLE | WS_GROUP,                 10, 45, 120, 10
   CONTROL "Right aligned",        5, STATIC, SS_RIGHT | WS_CHILD | WS_VISIBLE | WS_GROUP,                  10, 55, 120, 10
}
'''

dlg = create_dialog_from_rc(rc_code=rc)
dlg.center = True
dlg.show()


class LabelDialog(Dialog):
    def __init__(self, title='Label Dialog'):
        super().__init__(title)
        self.center = True
        self.size = (250, 100)
        self.label1 = Label('Simple label', (50, 10), (5, 4))
        self.label2 = TruncatedLabel('Truncated text label', (50, 10), (5, 15))
        self.label3 = BlackFramedLabel('', (130, 40), (5, 30))
        self.label4 = Label('Blackframed labels', (120, 10), (10, 35))
        self.label6 = CenteredLabel('Centered', (120, 10), (10, 45))
        self.label7 = RigthAlignedLabel('Right aligned', (120, 10), (10, 55))
        self.show()
LabelDialog()