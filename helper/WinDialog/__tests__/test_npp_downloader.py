
from WinDialog import create_dialog_from_rc

rc = '''
1 DIALOGEX 0, 0, 366, 230
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "Npp Downloader"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "SEGOE UI"
{
    CONTROL "Download multiple files", 1 , BUTTON              , BS_GROUPBOX | WS_CHILD | WS_VISIBLE                     , 3 , 73 , 360, 136
    CONTROL "Link to new release"    , 2 , BUTTON              , BS_GROUPBOX | WS_CHILD | WS_VISIBLE                     , 3 , 3  , 360, 60
    CONTROL "Url"                    , 3 , STATIC              , SS_LEFT | WS_CHILD | WS_VISIBLE | WS_GROUP              , 10, 17 , 18 , 9
    CONTROL ""                       , 4 , EDIT                , ES_LEFT | WS_CHILD | WS_VISIBLE | WS_BORDER | WS_TABSTOP, 30, 14 , 328, 14
    CONTROL "Download"               , 5 , BUTTON              , BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP      , 6 , 39 , 72 , 14
    CONTROL "Download"               , 6 , BUTTON              , BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP      , 6 , 189, 72 , 14
    CONTROL ""                       , 7 , "msctls_progress32" , WS_CHILD                                                , 90, 42 , 268, 8
    CONTROL ""                       , 8 , "msctls_progress32" , WS_CHILD                                                , 90, 192, 268, 8
    CONTROL ""                       , 9 , "ComboBoxEx32"      , WS_CHILD | WS_VISIBLE | WS_TABSTOP                      , 6 , 85 , 72 , 90
    CONTROL ""                       , 10, LISTBOX             , LBS_STANDARD | WS_CHILD | WS_VISIBLE | WS_TABSTOP       , 90, 85 , 268, 100
    CONTROL ""                       , 11, "msctls_statusbar32", SBARS_SIZEGRIP | WS_CHILD | WS_VISIBLE                  , 0 , 212, 366, 15
}
'''

dlg = create_dialog_from_rc(rc_code=rc)
dlg.center = True
dlg.show()