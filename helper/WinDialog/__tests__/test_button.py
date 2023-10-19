from Npp import console
console.show()
from WinDialog import (
    Dialog, create_dialog_from_rc,
    Button, DefaultButton, CheckBoxButton, GroupBox, CommandButton, RadioButton,
)

rc = '''
1 DIALOGEX 0, 0, 250, 200
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "Button Dialog"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
   CONTROL "Simple",                1 , BUTTON, BS_AUTOCHECKBOX | WS_CHILD | WS_VISIBLE | WS_TABSTOP,    10, 10, 90, 14
   CONTROL "Three state check box", 2 , BUTTON, BS_AUTO3STATE | WS_CHILD | WS_VISIBLE | WS_TABSTOP,      10, 30, 90, 14
   CONTROL "Group Box 1",           3 , BUTTON, BS_GROUPBOX | WS_GROUP | WS_CHILD | WS_VISIBLE,          10, 50, 160, 30
   CONTROL "Radio button 1",        4 , BUTTON, BS_AUTORADIOBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 20, 60, 60, 14
   CONTROL "Radio button 2",        5 , BUTTON, BS_AUTORADIOBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 90, 60, 60, 14
   CONTROL "Group Box 2",           6 , BUTTON, BS_GROUPBOX | WS_GROUP | WS_CHILD | WS_VISIBLE,          10, 90, 160, 30
   CONTROL "Radio button 1",        7 , BUTTON, BS_AUTORADIOBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 20, 100, 60, 14
   CONTROL "Radio button 2",        8 , BUTTON, BS_AUTORADIOBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 90, 100, 60, 14
   CONTROL "Close Dialog",          9 , BUTTON, BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP,      10, 130, 80, 22
   CONTROL "Default push button",   10, BUTTON, BS_DEFPUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP,   90, 130, 80, 22
   CONTROL "Command Link",          11, BUTTON, BS_COMMANDLINK | WS_CHILD | WS_VISIBLE | WS_TABSTOP,     10, 160, 100, 26
}
'''

dlg = create_dialog_from_rc(rc_code=rc)
dlg.center = True
dlg.button_1.onClick = lambda: print('button_1 on_click')
dlg.button_2.onClick = lambda: print('three state button clicked')
dlg.button_9.onClick = dlg.terminate
dlg.button_10.onClick = lambda: print('button_10 on_click')
dlg.onClose = lambda: print('Dialog is going to close')
dlg.show()

class ButtonDialog(Dialog):
    def __init__(self, title='Some buttons dialog'):
        super().__init__(title)
        self.size = (250, 200)
        self.center = True
        self.btn1 = CheckBoxButton(title='Simple', size=(90,14), position=(10, 10))
        self.btn1.onClick = lambda: print('btn1 on_click')
        self.btn2 = CheckBoxButton(title='Three state check box', size=(90,14), position=(10, 30))
        self.btn2.setThreeState()
        self.btn2.onClick = self.three_state_btn_click

        # A new group of radio buttons,
        # all following radio buttons are part of this group
        # unless a new group starts
        self.btn3 = GroupBox('Group Box 1', (160, 30), (10, 50))
        self.btn3a = RadioButton('Radio button 1', (60,14), (20, 60))
        self.btn3b = RadioButton('Radio button 2', (60,14), (90, 60))
        # new group started
        self.btn4 = GroupBox('Group Box 2', (160, 30), (10, 90))
        self.btn4a = RadioButton('Radio button 1', (60,14), (20, 100))
        self.btn4b = RadioButton('Radio button 2', (60,14), (90, 100))

        self.btn5 = DefaultButton(title='Close dialog', size=(80,22), position=(10,130))
        self.btn5.onClick = self.terminate

        self.btn6 = Button('Normal push button', (80,22), (90,130))
        self.btn6.onClick = self.on_click

        self.btn7 = CommandButton('Command link', (100,26), (10,160))

        self.show()

    def initialize(self):
        self.btn3a.setCheck()

    def onClose(self):
        print("Dialog is going to close")

    def three_state_btn_click(self):
        print("three state button clicked")
        
    def on_click(self):
        for control in self.controlList:
            if isinstance(control, CheckBoxButton) or isinstance(control, RadioButton):
                print(f'{control.title} is checked: {control.isChecked()}')

ButtonDialog()
