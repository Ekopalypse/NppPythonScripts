from Npp import notepad
from pathlib import Path
from pprint import pformat

from WinDialog import (
    Dialog, create_dialog_from_rc,
    Button, UpDown
)

rc = '''
1 DIALOGEX 0, 0, 250, 108
STYLE DS_SETFONT | WS_BORDER
CAPTION "Command Center"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "SEGOE UI"
{
  CONTROL "", 0, EDIT, ES_LEFT | WS_CHILD | WS_VISIBLE | WS_BORDER | WS_TABSTOP, 1, 0, 240, 14
  CONTROL "", 0, LISTBOX, LBS_STANDARD | WS_CHILD | WS_VISIBLE | WS_TABSTOP, 1, 14, 240, 80
  CONTROL "", 0, BUTTON, BS_DEFPUSHBUTTON | WS_CHILD | WS_TABSTOP, 100, 92, 50, 7
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
    dlg.listbox_0.add_strings(filtered_list)
    dlg.edit_0.grab_focus()

def on_click():
    exec(open(files[filtered_list[0]], 'r').read())
    dlg.terminate()

def on_change():
    global filtered_list
    text = dlg.edit_0.get_text()
    dlg.listbox_0.clear()
    if text:
        filtered_list = list(filter_files(files, text))
        dlg.listbox_0.add_strings(filtered_list)
    else:
        dlg.listbox_0.add_strings(files)


dlg.edit_0.on_change = on_change
dlg.button_0.on_click = on_click
dlg.initialize = on_init
dlg.center = True
dlg.show()
