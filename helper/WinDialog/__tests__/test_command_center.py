from Npp import notepad
from pathlib import Path

from WinDialog import create_dialog_from_rc

rc = '''
1 DIALOGEX 0, 0, 250, 108
STYLE DS_SETFONT | WS_BORDER
CAPTION "Command Center"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "SEGOE UI"
{
  CONTROL "", 0, EDIT, ES_LEFT | WS_CHILD | WS_VISIBLE | WS_BORDER | WS_TABSTOP, 1, 0, 240, 14
  CONTROL "", 0, LISTBOX, LBS_STANDARD | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 1, 14, 240, 80
}
'''

def filter_files(files, text):
    for file_ in files:
        if file_.startswith(text):
            yield file_

config_dir = Path(notepad.getPluginConfigDir())
script_path = config_dir.joinpath("PythonScript\\scripts")
files = dict((x.parts[-1][:-3], x) for x in script_path.iterdir() if x.suffix == '.py')
filtered_list = list(files.keys())
dlg = create_dialog_from_rc(rc_code=rc)

def on_init():
    dlg.listbox_0.addStrings(filtered_list)
    dlg.edit_0.grabFocus()

def on_idok():
    index = dlg.listbox_0.getSelectedItem()
    if index > -1:
        print(files[filtered_list[index]])
    else:
        print(files[filtered_list[0]])

def on_change():
    global filtered_list
    text = dlg.edit_0.getText()
    dlg.listbox_0.clear()
    if text:
        filtered_list = list(filter_files(files, text))
        dlg.listbox_0.addStrings(filtered_list)
    else:
        dlg.listbox_0.addStrings(files)


dlg.edit_0.onChange = on_change
dlg.onIdOk = on_idok
dlg.initialize = on_init
dlg.center = True
dlg.show()
