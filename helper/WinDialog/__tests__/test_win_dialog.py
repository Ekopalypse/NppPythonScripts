from Npp import console
from WinDialog import (
    Dialog, Button, DefaultButton
)

console.show()

class AllControlsDialog(Dialog):
    def __init__(self, title='Dialog using Comic Sans MS font'):
        super().__init__(title)
        self.size = (367, 167)
        self.pointsize = 10
        self.typeface = "Comic Sans MS"
        self.btn1 = Button(title='&OK', size=(50, 11), position=(130, 78))
        self.btn1.onClick = lambda: print('ok')
        self.btn2 = DefaultButton(title='&Cancel', size=(50, 11), position=(187, 78))
        self.btn2.on_click = self.on_close
        self.center = True
        self.show()

    def on_close(self):
        self.terminate()

AllControlsDialog()
