from Npp import console
from WinDialog import (
    Dialog,
    Button, CheckBoxButton, GroupBox, CommandButton, RadioButton,
    SimpleLabel, TruncatedLabel, BlackFramedLabel, CenteredLabel, RigthAlignedLabel,
    ComboBox,
)

console.show()

class ButtonDialog(Dialog):
    def __init__(self, title='Some buttons dialog'):
        super().__init__(title)

        _button1 = CheckBoxButton('Simple', (90,14), (10, 10))
        _button1.on_click = self.on_click
        _button2 = CheckBoxButton('Three state check box', (90,14), (10, 30), three_state=True)
        _button2.on_click = self.on_click

        _button3 = GroupBox('Group Box 1', (160, 30), (10, 50))
        # _button3a starts a new group of radio buttons,
        # all following radio buttons are part of this group
        # unless they start a new group
        _button3a = RadioButton('Radio button 1', (60,14), (20, 60), group=True)
        _button3b = RadioButton('Radio button 2', (60,14), (90, 60))
        # new group started by _button4a
        _button4 = GroupBox('Group Box 2', (160, 30), (10, 90))
        _button4a = RadioButton('Radio button 1', (60,14), (20, 100), group=True)
        _button4b = RadioButton('Radio button 2', (60,14), (90, 100))

        _button5 = Button('Close dialog', (80,22), (10,130))
        _button5.on_click = self.on_close

        _button6 = Button('Default push button', (80,22), (90,130))
        _button6.set_default()
        _button6.on_click = self.on_click

        _button7 = CommandButton('Command link', (100,26), (10,160))

        self.add_controls([
               _button1, _button2,
               _button3, _button3a, _button3b,
               _button4, _button4a, _button4b,
               _button5, _button6,
               _button7,
               ])
        self.show()

    def on_close(self):
        self.terminate()

    def on_click(self):
        print("button clicked")


class LabelDialog(Dialog):
    def __init__(self, title='test dialog'):
        super().__init__(title)

        _label1 = SimpleLabel('Simple label', (90, 14), (10, 10))
        _label2 = TruncatedLabel('Simple label with truncates text', (80, 14), (10, 30))
        _label3 = BlackFramedLabel('', (90, 30), (10, 50))
        _label4 = SimpleLabel('Label within black frame', (90,14), (15, 60))
        _label6 = CenteredLabel('Centered label', (90, 14), (10, 90))
        _label7 = RigthAlignedLabel('Right alligned label', (90, 14), (10, 110))

        self.add_controls([ _label1, _label2, _label3, _label4,  _label6, _label7 ])
        self.show()

class ComboBoxDialog(Dialog):
    def __init__(self, title='test dialog'):
        super().__init__(title)
        self.size = (110, 120)
        self.cb1 = ComboBox((80,10), (10,10))
        self.cb1.items = ['Item1', 'Item2', 'Item3',]
        self.cb1.on_selchange = self.on_selchange

        self.cb2 = ComboBox((80,10), (10,60))
        self.cb2.items = []
        self.cb2.on_selchange = self.on_selchange2

        self.add_controls([self.cb1, self.cb2])
        self.show()

    def on_selchange(self):
        match self.cb1.get_selected_item():
            case 0:
                self.cb2.update(['100', '101', '102',])
            case 1:
                self.cb2.update(['200', '201', '202',])
            case _:
                self.cb2.update(['301', '301', '302',])

    def on_selchange2(self):
        print(self.cb1.items[self.cb1.get_selected_item()])


ButtonDialog()
LabelDialog()
ComboBoxDialog()
