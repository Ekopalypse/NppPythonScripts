from Npp import console
from dataclasses import dataclass
from WinDialog import (
    Dialog, Button
)

console.show()

class AllControlsDialog(Dialog):
    def __init__(self, title='Whoa'):
        super().__init__(title)
        self.size = (367, 167)
        self.pointsize = 10
        self.typeface = "CaskaydiaCove Nerd Font Mono"
        self.btn1 = Button(title='&OK', size=(50, 11), position=(130, 78))
        self.btn1.on_click = lambda: print('ok')
        self.btn2 = DefaultButton(title='&Cancel', size=(50, 11), position=(187, 78))
        self.btn2.on_click = self.on_close
        self.center = True
        self.show()

    def on_close(self):
        self.terminate()

AllControlsDialog()
