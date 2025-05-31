from WinDialog import FileOpenDialog, DirectoryPicker, FileSaveDialog
from WinDialog.com_dialogs import FOS

def test_dlgs():

    answer = notepad.messageBox('About to demo a file-open dialog where you can select multiple items -- proceed?', '', MESSAGEBOXFLAGS.YESNOCANCEL)
    if answer == MESSAGEBOXFLAGS.RESULTCANCEL: return
    if answer == MESSAGEBOXFLAGS.RESULTYES:
        open_dlg = FileOpenDialog()
        open_dlg.setOptions(FOS.ALLOWMULTISELECT)
        result = open_dlg.show()
        if len(result) > 0: notepad.messageBox(str(result), 'Result')

    answer = notepad.messageBox('About to demo a file-open dialog where you can only select 1 item -- proceed?', '', MESSAGEBOXFLAGS.YESNOCANCEL)
    if answer == MESSAGEBOXFLAGS.RESULTCANCEL: return
    if answer == MESSAGEBOXFLAGS.RESULTYES:
        open_dlg = FileOpenDialog()
        open_options = open_dlg.getOptions()
        open_options &= ~FOS.ALLOWMULTISELECT
        open_dlg.setOptions(open_options)
        result = open_dlg.show()
        if len(result) > 0: notepad.messageBox(str(result), 'Result')

    answer = notepad.messageBox('About to demo a file-save dialog -- proceed?', '', MESSAGEBOXFLAGS.YESNOCANCEL)
    if answer == MESSAGEBOXFLAGS.RESULTCANCEL: return
    if answer == MESSAGEBOXFLAGS.RESULTYES:
        save_dlg = FileSaveDialog()
        save_dlg.setFolder(r'c:')
        save_dlg.setFileTypes([['All files', '*.*'], ['Text Files', '*.txt'], ['Log Files', '*.log']])
        save_options = save_dlg.getOptions()
        save_options |= FOS.OVERWRITEPROMPT
        save_dlg.setOptions(save_options)
        result = save_dlg.show()
        if len(result) > 0: notepad.messageBox(str(result), 'Result')

    answer = notepad.messageBox('About to demo a directory-picker dialog -- proceed?', '', MESSAGEBOXFLAGS.YESNOCANCEL)
    if answer == MESSAGEBOXFLAGS.RESULTCANCEL: return
    if answer == MESSAGEBOXFLAGS.RESULTYES:
        dir_pick_dlg = DirectoryPicker()
        result = dir_pick_dlg.show()
        if len(result) > 0: notepad.messageBox(str(result), 'Result')

test_dlgs()
