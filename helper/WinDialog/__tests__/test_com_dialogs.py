from WinDialog import FileOpenDialog, DirectoryPicker
from WinDialog.com_dialogs import FOS

dlg = FileOpenDialog()
dlg.setOptions(FOS.ALLOWMULTISELECT)
print(dlg.show())

print(DirectoryPicker().show())

options = dlg.getOptions()
options &= ~FOS.ALLOWMULTISELECT
dlg.setOptions(options)
print(dlg.show())