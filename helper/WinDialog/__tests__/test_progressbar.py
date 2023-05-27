from Npp import console
from WinDialog import (
    Dialog, create_dialog_from_rc,
    Button, ProgressBar
)
from WinDialog.controls.progressbar import PBST

console.show()

rc = '''
1 DIALOGEX 0, 0, 250, 100
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "ProgressBar Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "", 0, "msctls_progress32", WS_CHILD | WS_VISIBLE, 31, 18, 122, 20
   CONTROL "Step", 0, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 163, 18, 50, 20
   CONTROL "Re-initialize ProgressBar", 1, BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 31, 43, 122, 14
}
'''

def do_test():
    assert(dlg.msctls_progress32_0.getStepValue() == 10)
    assert(dlg.msctls_progress32_0.step() is None)
    assert(dlg.msctls_progress32_0.step() is None)
    assert(dlg.msctls_progress32_0.getPosition() == 20)
    assert(dlg.msctls_progress32_0.setStepValue(42) is None)
    assert(dlg.msctls_progress32_0.getStepValue() == 42)
    assert(dlg.msctls_progress32_0.setPosition(13) == 20)
    assert(dlg.msctls_progress32_0.getPosition() == 13)
    assert(dlg.msctls_progress32_0.deltaPos(2) == 13)
    assert(dlg.msctls_progress32_0.getPosition() == 15)
    assert(dlg.msctls_progress32_0.setRange(0, 150) is None)
    assert(dlg.msctls_progress32_0.getRange(False, both=True) == (0, 150))
    assert(dlg.msctls_progress32_0.setRange32(0, 0xfffffe) == (0, 150))
    assert(dlg.msctls_progress32_0.setRange32(0, 0xffffff) == (0, 65534))
    assert(dlg.msctls_progress32_0.getRange(False, both=True) == (0, 16777215))
    assert(dlg.msctls_progress32_0.setBarColor(0xc2b656) == 4278190080)
    assert(dlg.msctls_progress32_0.getBarColor() == 12760662)
    assert(dlg.msctls_progress32_0.setMarquee(turn_on=True, anmiation_time=1000) is None)
    assert(dlg.msctls_progress32_0.setBkColor(0x756ce0) == 4278190080)
    assert(dlg.msctls_progress32_0.getBkColor() == 7695584)
    assert(dlg.msctls_progress32_0.setState(PBST.ERROR) == PBST.NORMAL)
    assert(dlg.msctls_progress32_0.getState() == PBST.ERROR)
    print('done')

def do_step():
    dlg.msctls_progress32_0.step()
    print(dlg.msctls_progress32_0.getPosition())

def init_progressbar():
    dlg.msctls_progress32_0.setPosition(0)
    dlg.msctls_progress32_0.setStepValue(13)
    dlg.msctls_progress32_0.setRange(0, 65)
    dlg.msctls_progress32_0.setBarColor(0xc2b656)
    dlg.msctls_progress32_0.setMarquee(turn_on=True, anmiation_time=1000)
    dlg.msctls_progress32_0.setBkColor(0x756ce0)

dlg = create_dialog_from_rc(rc_code=rc)
dlg.button_0.onClick = do_step
dlg.button_1.onClick = init_progressbar
dlg.center = True
dlg.show()


class ProgressBarDialog(Dialog):
    def __init__(self, title='ProgressBar Dialog'):
        super().__init__(title)
        self.size = (250, 100)
        self.center = True
        self.btn_step = Button('Step', (50, 20), (163, 18))
        self.btn_reinit = Button('Re-initialize ProgressBar', (122, 14), (31, 43))
        self.progress_bar = ProgressBar('', (122, 20), (31, 18))
        self.btn_step.onClick = self.do_step
        self.btn_reinit.onClick = self.reinit_progressbar
        self.show()

    def do_step(self):
        self.progress_bar.step()
        print(self.progress_bar.getPosition())

    def reinit_progressbar(self):
        self.progress_bar.setPosition(0)
        self.progress_bar.setStepValue(13)
        self.progress_bar.setRange(0, 65)

ProgressBarDialog()
