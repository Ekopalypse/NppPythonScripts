from windowsapi cimport *


cdef extern from "Notepad_plus_msgs.h":
    #include <windows.h>
    #include <tchar.h>

    cdef enum LangType:
        L_TEXT, L_PHP , L_C, L_CPP, L_CS, L_OBJC, L_JAVA, L_RC,\
        L_HTML, L_XML, L_MAKEFILE, L_PASCAL, L_BATCH, L_INI, L_ASCII, L_USER,\
        L_ASP, L_SQL, L_VB, L_JS, L_CSS, L_PERL, L_PYTHON, L_LUA, \
        L_TEX, L_FORTRAN, L_BASH, L_FLASH, L_NSIS, L_TCL, L_LISP, L_SCHEME,\
        L_ASM, L_DIFF, L_PROPS, L_PS, L_RUBY, L_SMALLTALK, L_VHDL, L_KIX, L_AU3,\
        L_CAML, L_ADA, L_VERILOG, L_MATLAB, L_HASKELL, L_INNO, L_SEARCHRESULT,\
        L_CMAKE, L_YAML, L_COBOL, L_GUI4CLI, L_D, L_POWERSHELL, L_R, L_JSP,\
        L_COFFEESCRIPT, L_JSON, L_JAVASCRIPT, L_FORTRAN_77, L_BAANC, L_SREC,\
        L_IHEX, L_TEHEX, L_SWIFT,\
        L_ASN1, L_AVS, L_BLITZBASIC, L_PUREBASIC, L_FREEBASIC, \
        L_CSOUND, L_ERLANG, L_ESCRIPT, L_FORTH, L_LATEX, \
        L_MMIXAL, L_NIMROD, L_NNCRONTAB, L_OSCRIPT, L_REBOL, \
        L_REGISTRY, L_RUST, L_SPICE, L_TXT2TAGS, L_VISUALPROLOG,\
        # Don't use L_JS, use L_JAVASCRIPT instead
        # The end of enumated language type, so it should be always at the end
        L_EXTERNAL

    cdef enum winVer:
        WV_UNKNOWN, WV_WIN32S, WV_95, WV_98, WV_ME, WV_NT, WV_W2K, WV_XP, WV_S2003, \
        WV_XPX64, WV_VISTA, WV_WIN7, WV_WIN8, WV_WIN81, WV_WIN10

    cdef enum Platform:
        PF_UNKNOWN, PF_X86, PF_X64, PF_IA64

    cdef struct sessionInfo:
        LPCWSTR sessionFilePathName
        int nbFile
        LPCWSTR *files

    cdef struct toolbarIcons:
        HBITMAP hToolbarBmp
        HICON hToolbarIcon

    cdef struct CommunicationInfo:
        long internalMsg
        LPCWSTR srcModuleName
        void* info

    int NPPMSG

    int NPPM_GETCURRENTSCINTILLA
    int NPPM_GETCURRENTLANGTYPE
    int NPPM_SETCURRENTLANGTYPE

    int NPPM_GETNBOPENFILES
    int ALL_OPEN_FILES
    int PRIMARY_VIEW
    int SECOND_VIEW

    int NPPM_GETOPENFILENAMES


    int NPPM_MODELESSDIALOG
    int MODELESSDIALOGADD
    int MODELESSDIALOGREMOVE

    int NPPM_GETNBSESSIONFILES
    int NPPM_GETSESSIONFILES
    int NPPM_SAVESESSION
    int NPPM_SAVECURRENTSESSION

        # struct sessionInfo {
            # TCHAR* sessionFilePathName;
            # int nbFile;
            # TCHAR** files;
        # };

    int NPPM_GETOPENFILENAMESPRIMARY
    int NPPM_GETOPENFILENAMESSECOND

    int NPPM_CREATESCINTILLAHANDLE
    int NPPM_DESTROYSCINTILLAHANDLE
    int NPPM_GETNBUSERLANG

    int NPPM_GETCURRENTDOCINDEX
    int MAIN_VIEW
    int SUB_VIEW

    int NPPM_SETSTATUSBAR
    int STATUSBAR_DOC_TYPE
    int STATUSBAR_DOC_SIZE
    int STATUSBAR_CUR_POS
    int STATUSBAR_EOF_FORMAT
    int STATUSBAR_UNICODE_TYPE
    int STATUSBAR_TYPING_MODE

    int NPPM_GETMENUHANDLE
    int NPPPLUGINMENU
    int NPPMAINMENU
    # int NPPM_GETMENUHANDLE(INT menuChoice, 0)
    # Return: menu handle (HMENU) of choice (plugin menu handle or Notepad++ main menu handle)

    int NPPM_ENCODESCI
    #ascii file to unicode
    #int NPPM_ENCODESCI(MAIN_VIEW/SUB_VIEW, 0)
    #return new unicodeMode

    int NPPM_DECODESCI
    #unicode file to ascii
    #int NPPM_DECODESCI(MAIN_VIEW/SUB_VIEW, 0)
    #return old unicodeMode

    int NPPM_ACTIVATEDOC
    #void NPPM_ACTIVATEDOC(int view, int index2Activate)

    int NPPM_LAUNCHFINDINFILESDLG
    #void NPPM_LAUNCHFINDINFILESDLG(TCHAR * dir2Search, TCHAR * filtre)

    int NPPM_DMMSHOW
    #void NPPM_DMMSHOW(0, tTbData->hClient)

    int NPPM_DMMHIDE
    #void NPPM_DMMHIDE(0, tTbData->hClient)

    int NPPM_DMMUPDATEDISPINFO
    #void NPPM_DMMUPDATEDISPINFO(0, tTbData->hClient)

    int NPPM_DMMREGASDCKDLG
    #void NPPM_DMMREGASDCKDLG(0, &tTbData)

    int NPPM_LOADSESSION
    #void NPPM_LOADSESSION(0, int TCHAR* file name)

    int NPPM_DMMVIEWOTHERTAB
    #void WM_DMM_VIEWOTHERTAB(0, tTbData->pszName)

    int NPPM_RELOADFILE
    #BOOL NPPM_RELOADFILE(BOOL withAlert, TCHAR *filePathName2Reload)

    int NPPM_SWITCHTOFILE
    #BOOL NPPM_SWITCHTOFILE(0, TCHAR *filePathName2switch)

    int NPPM_SAVECURRENTFILE
    #BOOL NPPM_SAVECURRENTFILE(0, 0)

    int NPPM_SAVEALLFILES
    #BOOL NPPM_SAVEALLFILES(0, 0)

    int NPPM_SETMENUITEMCHECK
    #void WM_PIMENU_CHECK(UINT funcItem[X]._cmdID, TRUE/FALSE)

    int NPPM_ADDTOOLBARICON
    #void WM_ADDTOOLBARICON(UINT funcItem[X]._cmdID, toolbarIcons icon)
        # struct toolbarIcons {
            # HBITMAP hToolbarBmp;
            # HICON   hToolbarIcon;
        # };

    int NPPM_GETWINDOWSVERSION
    #winVer NPPM_GETWINDOWSVERSION(0, 0)

    int NPPM_DMMGETPLUGINHWNDBYNAME
    #HWND WM_DMM_GETPLUGINHWNDBYNAME(int TCHAR *windowName, int TCHAR *moduleName)
    # if moduleName is NULL, then return value is NULL
    # if windowName is NULL, then the first found window handle which matches with the moduleName will be returned

    int NPPM_MAKECURRENTBUFFERDIRTY
    #BOOL NPPM_MAKECURRENTBUFFERDIRTY(0, 0)

    int NPPM_GETENABLETHEMETEXTUREFUNC
    #BOOL NPPM_GETENABLETHEMETEXTUREFUNC(0, 0)

    int NPPM_GETPLUGINSCONFIGDIR
    #int NPPM_GETPLUGINSCONFIGDIR(int strLen, TCHAR *str)
    # Get user's plugin config directory path. It's useful if plugins want to save/load parameters for the current user
    # Returns the number of TCHAR copied/to copy.
    # Users should call it with "str" be NULL to get the required number of TCHAR (not including the terminating nul character),
    # allocate "str" buffer with the return value + 1, then call it again to get the path.

    int NPPM_MSGTOPLUGIN
    #BOOL NPPM_MSGTOPLUGIN(TCHAR *destModuleName, CommunicationInfo *info)
    # return value is TRUE when the message arrive to the destination plugins.
    # if destModule or info is NULL, then return value is FALSE
        # struct CommunicationInfo {
            # long internalMsg;
            # int TCHAR * srcModuleName;
            # void * info; # defined by plugin
        # };

    int NPPM_MENUCOMMAND
    #void NPPM_MENUCOMMAND(0, int cmdID)
    # uncomment ##include "menuCmdID.h"
    # in the beginning of this file then use the command symbols defined in "menuCmdID.h" file
    # to access all the Notepad++ menu command items

    int NPPM_TRIGGERTABBARCONTEXTMENU
    #void NPPM_TRIGGERTABBARCONTEXTMENU(int view, int index2Activate)

    int NPPM_GETNPPVERSION
    # int NPPM_GETNPPVERSION(0, 0)
    # return version
    # ex : v4.6
    # HIWORD(version) == 4
    # LOWORD(version) == 6

    int NPPM_HIDETABBAR
    # BOOL NPPM_HIDETABBAR(0, BOOL hideOrNot)
    # if hideOrNot is set as TRUE then tab bar will be hidden
    # otherwise it'll be shown.
    # return value : the old status value

    int NPPM_ISTABBARHIDDEN
    # BOOL NPPM_ISTABBARHIDDEN(0, 0)
    # returned value : TRUE if tab bar is hidden, otherwise FALSE

    int NPPM_GETPOSFROMBUFFERID
    # int NPPM_GETPOSFROMBUFFERID(UINT_PTR bufferID, INT priorityView)
    # Return VIEW|INDEX from a buffer ID. -1 if the bufferID non existing
    # if priorityView set to SUB_VIEW, then SUB_VIEW will be search firstly
    #
    # VIEW takes 2 highest bits and INDEX (0 based) takes the rest (30 bits)
    # Here's the values for the view :
    #  MAIN_VIEW 0
    #  SUB_VIEW  1

    int NPPM_GETFULLPATHFROMBUFFERID
    # int NPPM_GETFULLPATHFROMBUFFERID(UINT_PTR bufferID, TCHAR *fullFilePath)
    # Get full path file name from a bufferID.
    # Return -1 if the bufferID non existing, otherwise the number of TCHAR copied/to copy
    # User should call it with fullFilePath be NULL to get the number of TCHAR (not including the nul character),
    # allocate fullFilePath with the return values + 1, then call it again to get full path file name

    int NPPM_GETBUFFERIDFROMPOS
    # LRESULT NPPM_GETBUFFERIDFROMPOS(INT index, INT iView)
    # wParam: Position of document
    # lParam: View to use, 0 = Main, 1 = Secondary
    # Returns 0 if invalid

    int NPPM_GETCURRENTBUFFERID
    # LRESULT NPPM_GETCURRENTBUFFERID(0, 0)
    # Returns active Buffer

    int NPPM_RELOADBUFFERID
    # VOID NPPM_RELOADBUFFERID(UINT_PTR bufferID, BOOL alert)
    # Reloads Buffer
    # wParam: Buffer to reload
    # lParam: 0 if no alert, else alert


    int NPPM_GETBUFFERLANGTYPE
    # int NPPM_GETBUFFERLANGTYPE(UINT_PTR bufferID, 0)
    # wParam: BufferID to get LangType from
    # lParam: 0
    # Returns as int, see LangType. -1 on error

    int NPPM_SETBUFFERLANGTYPE
    # BOOL NPPM_SETBUFFERLANGTYPE(UINT_PTR bufferID, INT langType)
    # wParam: BufferID to set LangType of
    # lParam: LangType
    # Returns TRUE on success, FALSE otherwise
    # use int, see LangType for possible values
    # L_USER and L_EXTERNAL are not supported

    int NPPM_GETBUFFERENCODING
    # int NPPM_GETBUFFERENCODING(UINT_PTR bufferID, 0)
    # wParam: BufferID to get encoding from
    # lParam: 0
    # returns as int, see UniMode. -1 on error

    int NPPM_SETBUFFERENCODING
    # BOOL NPPM_SETBUFFERENCODING(UINT_PTR bufferID, INT encoding)
    # wParam: BufferID to set encoding of
    # lParam: encoding
    # Returns TRUE on success, FALSE otherwise
    # use int, see UniMode
    # Can only be done on new, unedited files

    int NPPM_GETBUFFERFORMAT
    # int NPPM_GETBUFFERFORMAT(UINT_PTR bufferID, 0)
    # wParam: BufferID to get EolType format from
    # lParam: 0
    # returns as int, see EolType format. -1 on error

    int NPPM_SETBUFFERFORMAT
    # BOOL NPPM_SETBUFFERFORMAT(UINT_PTR bufferID, INT format)
    # wParam: BufferID to set EolType format of
    # lParam: format
    # Returns TRUE on success, FALSE otherwise
    # use int, see EolType format


    int NPPM_HIDETOOLBAR
    # BOOL NPPM_HIDETOOLBAR(0, BOOL hideOrNot)
    # if hideOrNot is set as TRUE then tool bar will be hidden
    # otherwise it'll be shown.
    # return value : the old status value

    int NPPM_ISTOOLBARHIDDEN
    # BOOL NPPM_ISTOOLBARHIDDEN(0, 0)
    # returned value : TRUE if tool bar is hidden, otherwise FALSE

    int NPPM_HIDEMENU
    # BOOL NPPM_HIDEMENU(0, BOOL hideOrNot)
    # if hideOrNot is set as TRUE then menu will be hidden
    # otherwise it'll be shown.
    # return value : the old status value

    int NPPM_ISMENUHIDDEN
    # BOOL NPPM_ISMENUHIDDEN(0, 0)
    # returned value : TRUE if menu is hidden, otherwise FALSE

    int NPPM_HIDESTATUSBAR
    # BOOL NPPM_HIDESTATUSBAR(0, BOOL hideOrNot)
    # if hideOrNot is set as TRUE then STATUSBAR will be hidden
    # otherwise it'll be shown.
    # return value : the old status value

    int NPPM_ISSTATUSBARHIDDEN
    # BOOL NPPM_ISSTATUSBARHIDDEN(0, 0)
    # returned value : TRUE if STATUSBAR is hidden, otherwise FALSE

    int NPPM_GETSHORTCUTBYCMDID
    # BOOL NPPM_GETSHORTCUTBYCMDID(int cmdID, ShortcutKey *sk)
    # get your plugin command current mapped shortcut into sk via cmdID
    # You may need it after getting NPPN_READY notification
    # returned value : TRUE if this function call is successful and shortcut is enable, otherwise FALSE

    int NPPM_DOOPEN
    # BOOL NPPM_DOOPEN(0, int TCHAR *fullPathName2Open)
    # fullPathName2Open indicates the full file path name to be opened.
    # The return value is TRUE (1) if the operation is successful, otherwise FALSE (0).

    int NPPM_SAVECURRENTFILEAS
    # BOOL NPPM_SAVECURRENTFILEAS (BOOL asCopy, int TCHAR* filename)

    int NPPM_GETCURRENTNATIVELANGENCODING
    # int NPPM_GETCURRENTNATIVELANGENCODING(0, 0)
    # returned value : the current native language encoding

    int NPPM_ALLOCATESUPPORTED
    # returns TRUE if NPPM_ALLOCATECMDID is supported
    # Use to identify if subclassing is necessary

    int NPPM_ALLOCATECMDID
    # BOOL NPPM_ALLOCATECMDID(int numberRequested, int* startNumber)
    # sets startNumber to the initial command ID if successful
    # Returns: TRUE if successful, FALSE otherwise. startNumber will also be set to 0 if unsuccessful

    int NPPM_ALLOCATEMARKER
    # BOOL NPPM_ALLOCATEMARKER(int numberRequested, int* startNumber)
    # sets startNumber to the initial command ID if successful
    # Allocates a marker number to a plugin
    # Returns: TRUE if successful, FALSE otherwise. startNumber will also be set to 0 if unsuccessful

    int NPPM_GETLANGUAGENAME
    # int NPPM_GETLANGUAGENAME(int langType, TCHAR *langName)
    # Get programming language name from the given language type (LangType)
    # Return value is the number of copied character / number of character to copy (\0 is not included)
    # You should call this function 2 times - the first time you pass langName as NULL to get the number of characters to copy.
    # You allocate a buffer of the length of (the number of characters + 1) then call NPPM_GETLANGUAGENAME function the 2nd time
    # by passing allocated buffer as argument langName

    int NPPM_GETLANGUAGEDESC
    # int NPPM_GETLANGUAGEDESC(int langType, TCHAR *langDesc)
    # Get programming language short description from the given language type (LangType)
    # Return value is the number of copied character / number of character to copy (\0 is not included)
    # You should call this function 2 times - the first time you pass langDesc as NULL to get the number of characters to copy.
    # You allocate a buffer of the length of (the number of characters + 1) then call NPPM_GETLANGUAGEDESC function the 2nd time
    # by passing allocated buffer as argument langDesc

    int NPPM_SHOWDOCSWITCHER
    # VOID NPPM_ISDOCSWITCHERSHOWN(0, BOOL toShowOrNot)
    # Send this message to show or hide doc switcher.
    # if toShowOrNot is TRUE then show doc switcher, otherwise hide it.

    int NPPM_ISDOCSWITCHERSHOWN
    # BOOL NPPM_ISDOCSWITCHERSHOWN(0, 0)
    # Check to see if doc switcher is shown.

    int NPPM_GETAPPDATAPLUGINSALLOWED
    # BOOL NPPM_GETAPPDATAPLUGINSALLOWED(0, 0)
    # Check to see if loading plugins from "%APPDATA%\..\Local\Notepad++\plugins" is allowed.

    int NPPM_GETCURRENTVIEW
    # int NPPM_GETCURRENTVIEW(0, 0)
    # Return: current edit view of Notepad++. Only 2 possible values: 0 = Main, 1 = Secondary

    int NPPM_DOCSWITCHERDISABLECOLUMN
    # VOID NPPM_DOCSWITCHERDISABLECOLUMN(0, BOOL disableOrNot)
    # Disable or enable extension column of doc switcher

    int NPPM_GETEDITORDEFAULTFOREGROUNDCOLOR
    # int NPPM_GETEDITORDEFAULTFOREGROUNDCOLOR(0, 0)
    # Return: current editor default foreground color. You should convert the returned value in COLORREF

    int NPPM_GETEDITORDEFAULTBACKGROUNDCOLOR
    # int NPPM_GETEDITORDEFAULTBACKGROUNDCOLOR(0, 0)
    # Return: current editor default background color. You should convert the returned value in COLORREF

    int NPPM_SETSMOOTHFONT
    # VOID NPPM_SETSMOOTHFONT(0, BOOL setSmoothFontOrNot)

    int NPPM_SETEDITORBORDEREDGE
    # VOID NPPM_SETEDITORBORDEREDGE(0, BOOL withEditorBorderEdgeOrNot)

    int NPPM_SAVEFILE
    # VOID NPPM_SAVEFILE(0, int TCHAR *fileNameToSave)

    int NPPM_DISABLEAUTOUPDATE
    # VOID NPPM_DISABLEAUTOUPDATE(0, 0)

    int NPPM_REMOVESHORTCUTBYCMDID
    # BOOL NPPM_REMOVESHORTCUTASSIGNMENT(int cmdID)
    # removes the assigned shortcut mapped to cmdID
    # returned value : TRUE if function call is successful, otherwise FALSE

    int NPPM_GETPLUGINHOMEPATH
    # int NPPM_GETPLUGINHOMEPATH(int strLen, TCHAR *pluginRootPath)
    # Get plugin home root path. It's useful if plugins want to get its own path
    # by appending <pluginFolderName> which is the name of plugin without extension part.
    # Returns the number of TCHAR copied/to copy.
    # Users should call it with pluginRootPath be NULL to get the required number of TCHAR (not including the terminating nul character),
    # allocate pluginRootPath buffer with the return value + 1, then call it again to get the path.

    int RUNCOMMAND_USER
    int VAR_NOT_RECOGNIZED
    int FULL_CURRENT_PATH
    int CURRENT_DIRECTORY
    int FILE_NAME
    int NAME_PART
    int EXT_PART
    int CURRENT_WORD
    int NPP_DIRECTORY
    int CURRENT_LINE
    int CURRENT_COLUMN
    int NPP_FULL_FILE_PATH
    int GETFILENAMEATCURSOR

    int NPPM_GETFULLCURRENTPATH
    int NPPM_GETCURRENTDIRECTORY
    int NPPM_GETFILENAME
    int NPPM_GETNAMEPART
    int NPPM_GETEXTPART
    int NPPM_GETCURRENTWORD
    int NPPM_GETNPPDIRECTORY
    int NPPM_GETFILENAMEATCURSOR
    # BOOL NPPM_GETXXXXXXXXXXXXXXXX(int strLen, TCHAR *str)
    # where str is the allocated TCHAR array,
    #       strLen is the allocated array size
    # The return value is TRUE when get generic_string operation success
    # Otherwise (allocated array size is too small) FALSE

    int NPPM_GETCURRENTLINE
    # int NPPM_GETCURRENTLINE(0, 0)
    # return the caret current position line
    int NPPM_GETCURRENTCOLUMN
    # int NPPM_GETCURRENTCOLUMN(0, 0)
    # return the caret current position column

    int NPPM_GETNPPFULLFILEPATH




    # Notification code
    int NPPN_FIRST
    int NPPN_READY
    #scnNotification->nmhdr.code = NPPN_READY;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = 0;

    int NPPN_TBMODIFICATION
    #scnNotification->nmhdr.code = NPPN_TB_MODIFICATION;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = 0;

    int NPPN_FILEBEFORECLOSE
    #scnNotification->nmhdr.code = NPPN_FILEBEFORECLOSE;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_FILEOPENED
    #scnNotification->nmhdr.code = NPPN_FILEOPENED;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_FILECLOSED
    #scnNotification->nmhdr.code = NPPN_FILECLOSED;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_FILEBEFOREOPEN
    #scnNotification->nmhdr.code = NPPN_FILEBEFOREOPEN;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_FILEBEFORESAVE
    #scnNotification->nmhdr.code = NPPN_FILEBEFOREOPEN;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_FILESAVED
    #scnNotification->nmhdr.code = NPPN_FILESAVED;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_SHUTDOWN
    #scnNotification->nmhdr.code = NPPN_SHUTDOWN;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = 0;

    int NPPN_BUFFERACTIVATED
    #scnNotification->nmhdr.code = NPPN_BUFFERACTIVATED;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = activatedBufferID;

    int NPPN_LANGCHANGED
    #scnNotification->nmhdr.code = NPPN_LANGCHANGED;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = currentBufferID;

    int NPPN_WORDSTYLESUPDATED
    #scnNotification->nmhdr.code = NPPN_WORDSTYLESUPDATED;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = currentBufferID;

    int NPPN_SHORTCUTREMAPPED
    #scnNotification->nmhdr.code = NPPN_SHORTCUTSREMAPPED;
    #scnNotification->nmhdr.hwndFrom = ShortcutKeyStructurePointer;
    #scnNotification->nmhdr.idFrom = cmdID;
        #where ShortcutKeyStructurePointer is pointer of struct ShortcutKey:
        #struct ShortcutKey {
        #  bool _isCtrl;
        #  bool _isAlt;
        #  bool _isShift;
        #  UCHAR _key;
        #};

    int NPPN_FILEBEFORELOAD
    #scnNotification->nmhdr.code = NPPN_FILEBEFOREOPEN;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = NULL;

    int NPPN_FILELOADFAILED
    #scnNotification->nmhdr.code = NPPN_FILEOPENFAILED;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_READONLYCHANGED
    int DOCSTATUS_READONLY
    int DOCSTATUS_BUFFERDIRTY
    #scnNotification->nmhdr.code = NPPN_READONLYCHANGED;
    #scnNotification->nmhdr.hwndFrom = bufferID;
    #scnNotification->nmhdr.idFrom = docStatus;
        # where bufferID is BufferID
        #       docStatus can be combined by DOCSTATUS_READONLY and DOCSTATUS_BUFFERDIRTY


    int NPPN_DOCORDERCHANGED
    #scnNotification->nmhdr.code = NPPN_DOCORDERCHANGED;
    #scnNotification->nmhdr.hwndFrom = newIndex;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_SNAPSHOTDIRTYFILELOADED
    #scnNotification->nmhdr.code = NPPN_SNAPSHOTDIRTYFILELOADED;
    #scnNotification->nmhdr.hwndFrom = NULL;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_BEFORESHUTDOWN
    #scnNotification->nmhdr.code = NPPN_BEFORESHUTDOWN;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = 0;

    int NPPN_CANCELSHUTDOWN
    #scnNotification->nmhdr.code = NPPN_CANCELSHUTDOWN;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = 0;

    int NPPN_FILEBEFORERENAME
    #scnNotification->nmhdr.code = NPPN_FILEBEFORERENAME;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_FILERENAMECANCEL
    #scnNotification->nmhdr.code = NPPN_FILERENAMECANCEL;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_FILERENAMED
    #scnNotification->nmhdr.code = NPPN_FILERENAMED;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_FILEBEFOREDELETE
    #scnNotification->nmhdr.code = NPPN_FILEBEFOREDELETE;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_FILEDELETEFAILED
    #scnNotification->nmhdr.code = NPPN_FILEDELETEFAILED;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

    int NPPN_FILEDELETED
    #scnNotification->nmhdr.code = NPPN_FILEDELETED;
    #scnNotification->nmhdr.hwndFrom = hwndNpp;
    #scnNotification->nmhdr.idFrom = BufferID;

cdef extern from "menuCmdID.h":
    int IDM
    int IDM_FILE
    # IMPORTANT: If list below is modified, you have to change the value of IDM_FILEMENU_LASTONE and IDM_FILEMENU_EXISTCMDPOSITION
    int IDM_FILE_NEW
    int IDM_FILE_OPEN
    int IDM_FILE_CLOSE
    int IDM_FILE_CLOSEALL
    int IDM_FILE_CLOSEALL_BUT_CURRENT
    int IDM_FILE_SAVE
    int IDM_FILE_SAVEALL
    int IDM_FILE_SAVEAS
    int IDM_FILE_CLOSEALL_TOLEFT
    int IDM_FILE_PRINT
    int IDM_FILE_PRINTNOW
    int IDM_FILE_EXIT
    int IDM_FILE_LOADSESSION
    int IDM_FILE_SAVESESSION
    int IDM_FILE_RELOAD
    int IDM_FILE_SAVECOPYAS
    int IDM_FILE_DELETE
    int IDM_FILE_RENAME
    int IDM_FILE_CLOSEALL_TORIGHT
    int IDM_FILE_OPEN_FOLDER
    int IDM_FILE_OPEN_CMD
    int IDM_FILE_RESTORELASTCLOSEDFILE
    int IDM_FILE_OPENFOLDERASWORSPACE
    int IDM_FILE_OPEN_DEFAULT_VIEWER
    int IDM_FILE_CLOSEALL_UNCHANGED
    # IMPORTANT: If list above is modified, you have to change the following values:

    # To be updated if new menu item(s) is (are) added in menu "File"
    int IDM_FILEMENU_LASTONE

    # 0 based position of command "Exit" including the bars in the file menu
    # and without counting "Recent files history" items

    # 0  New
    # 1  Open...
    # 2  Open Containing Folder
    # 3  Open Folder as Workspace
    # 4  Open in Default Viewer
    # 5  Reload from Disk
    # 6  Save
    # 7  Save As...
    # 8  Save a Copy As...
    # 9  Save All
    #10  Rename...
    #11  Close
    #12  Close All
    #13  Close More
    #14  Move to Recycle Bin
    #15  --------
    #16  Load Session...
    #17  Save Session...
    #18  --------
    #19  Print...
    #20  Prsize_t Now
    #21  --------
    #22  Exit
    int IDM_FILEMENU_EXISTCMDPOSITION


    int IDM_EDIT
    int IDM_EDIT_CUT
    int IDM_EDIT_COPY
    int IDM_EDIT_UNDO
    int IDM_EDIT_REDO
    int IDM_EDIT_PASTE
    int IDM_EDIT_DELETE
    int IDM_EDIT_SELECTALL
    int IDM_EDIT_BEGINENDSELECT

    int IDM_EDIT_INS_TAB
    int IDM_EDIT_RMV_TAB
    int IDM_EDIT_DUP_LINE
    int IDM_EDIT_REMOVE_DUP_LINES
    int IDM_EDIT_TRANSPOSE_LINE
    int IDM_EDIT_SPLIT_LINES
    int IDM_EDIT_JOIN_LINES
    int IDM_EDIT_LINE_UP
    int IDM_EDIT_LINE_DOWN
    int IDM_EDIT_UPPERCASE
    int IDM_EDIT_LOWERCASE
    int IDM_EDIT_PROPERCASE_FORCE
    int IDM_EDIT_PROPERCASE_BLEND
    int IDM_EDIT_SENTENCECASE_FORCE
    int IDM_EDIT_SENTENCECASE_BLEND
    int IDM_EDIT_INVERTCASE
    int IDM_EDIT_RANDOMCASE
    int IDM_EDIT_REMOVEEMPTYLINES
    int IDM_EDIT_REMOVEEMPTYLINESWITHBLANK
    int IDM_EDIT_BLANKLINEABOVECURRENT
    int IDM_EDIT_BLANKLINEBELOWCURRENT
    int IDM_EDIT_SORTLINES_LEXICOGRAPHIC_ASCENDING
    int IDM_EDIT_SORTLINES_LEXICOGRAPHIC_DESCENDING
    int IDM_EDIT_SORTLINES_INTEGER_ASCENDING
    int IDM_EDIT_SORTLINES_INTEGER_DESCENDING
    int IDM_EDIT_SORTLINES_DECIMALCOMMA_ASCENDING
    int IDM_EDIT_SORTLINES_DECIMALCOMMA_DESCENDING
    int IDM_EDIT_SORTLINES_DECIMALDOT_ASCENDING
    int IDM_EDIT_SORTLINES_DECIMALDOT_DESCENDING

    int IDM_EDIT_OPENASFILE
    int IDM_EDIT_OPENINFOLDER
    int IDM_EDIT_SEARCHONINTERNET
    int IDM_EDIT_CHANGESEARCHENGINE

    # Menu macro
    int IDM_MACRO_STARTRECORDINGMACRO
    int IDM_MACRO_STOPRECORDINGMACRO
    int IDM_MACRO_PLAYBACKRECORDEDMACRO
    #-----------

    int IDM_EDIT_BLOCK_COMMENT
    int IDM_EDIT_STREAM_COMMENT
    int IDM_EDIT_TRIMTRAILING
    int IDM_EDIT_TRIMLINEHEAD
    int IDM_EDIT_TRIM_BOTH
    int IDM_EDIT_EOL2WS
    int IDM_EDIT_TRIMALL
    int IDM_EDIT_TAB2SW
    int IDM_EDIT_SW2TAB_LEADING
    int IDM_EDIT_SW2TAB_ALL
    int IDM_EDIT_STREAM_UNCOMMENT

    # Menu macro
    int IDM_MACRO_SAVECURRENTMACRO
    #-----------

    int IDM_EDIT_RTL
    int IDM_EDIT_LTR
    int IDM_EDIT_SETREADONLY
    int IDM_EDIT_FULLPATHTOCLIP
    int IDM_EDIT_FILENAMETOCLIP
    int IDM_EDIT_CURRENTDIRTOCLIP

    # Menu macro
    int IDM_MACRO_RUNMULTIMACRODLG
    #-----------

    int IDM_EDIT_CLEARREADONLY
    int IDM_EDIT_COLUMNMODE
    int IDM_EDIT_BLOCK_COMMENT_SET
    int IDM_EDIT_BLOCK_UNCOMMENT
    int IDM_EDIT_COLUMNMODETIP
    int IDM_EDIT_PASTE_AS_HTML
    int IDM_EDIT_PASTE_AS_RTF
    int IDM_EDIT_COPY_BINARY
    int IDM_EDIT_CUT_BINARY
    int IDM_EDIT_PASTE_BINARY
    int IDM_EDIT_CHAR_PANEL
    int IDM_EDIT_CLIPBOARDHISTORY_PANEL

    int IDM_EDIT_AUTOCOMPLETE
    int IDM_EDIT_AUTOCOMPLETE_CURRENTFILE
    int IDM_EDIT_FUNCCALLTIP
    int IDM_EDIT_AUTOCOMPLETE_PATH

    #Belong to MENU FILE
    int IDM_OPEN_ALL_RECENT_FILE
    int IDM_CLEAN_RECENT_FILE_LIST

    int IDM_SEARCH
    int IDM_SEARCH_FIND
    int IDM_SEARCH_FINDNEXT
    int IDM_SEARCH_REPLACE
    int IDM_SEARCH_GOTOLINE
    int IDM_SEARCH_TOGGLE_BOOKMARK
    int IDM_SEARCH_NEXT_BOOKMARK
    int IDM_SEARCH_PREV_BOOKMARK
    int IDM_SEARCH_CLEAR_BOOKMARKS
    int IDM_SEARCH_GOTOMATCHINGBRACE
    int IDM_SEARCH_FINDPREV
    int IDM_SEARCH_FINDINCREMENT
    int IDM_SEARCH_FINDINFILES
    int IDM_SEARCH_VOLATILE_FINDNEXT
    int IDM_SEARCH_VOLATILE_FINDPREV
    int IDM_SEARCH_CUTMARKEDLINES
    int IDM_SEARCH_COPYMARKEDLINES
    int IDM_SEARCH_PASTEMARKEDLINES
    int IDM_SEARCH_DELETEMARKEDLINES
    int IDM_SEARCH_MARKALLEXT1
    int IDM_SEARCH_UNMARKALLEXT1
    int IDM_SEARCH_MARKALLEXT2
    int IDM_SEARCH_UNMARKALLEXT2
    int IDM_SEARCH_MARKALLEXT3
    int IDM_SEARCH_UNMARKALLEXT3
    int IDM_SEARCH_MARKALLEXT4
    int IDM_SEARCH_UNMARKALLEXT4
    int IDM_SEARCH_MARKALLEXT5
    int IDM_SEARCH_UNMARKALLEXT5
    int IDM_SEARCH_CLEARALLMARKS

    int IDM_SEARCH_GOPREVMARKER1
    int IDM_SEARCH_GOPREVMARKER2
    int IDM_SEARCH_GOPREVMARKER3
    int IDM_SEARCH_GOPREVMARKER4
    int IDM_SEARCH_GOPREVMARKER5
    int IDM_SEARCH_GOPREVMARKER_DEF

    int IDM_SEARCH_GONEXTMARKER1
    int IDM_SEARCH_GONEXTMARKER2
    int IDM_SEARCH_GONEXTMARKER3
    int IDM_SEARCH_GONEXTMARKER4
    int IDM_SEARCH_GONEXTMARKER5
    int IDM_SEARCH_GONEXTMARKER_DEF

    int IDM_FOCUS_ON_FOUND_RESULTS
    int IDM_SEARCH_GOTONEXTFOUND
    int IDM_SEARCH_GOTOPREVFOUND

    int IDM_SEARCH_SETANDFINDNEXT
    int IDM_SEARCH_SETANDFINDPREV
    int IDM_SEARCH_INVERSEMARKS
    int IDM_SEARCH_DELETEUNMARKEDLINES
    int IDM_SEARCH_FINDCHARINRANGE
    int IDM_SEARCH_SELECTMATCHINGBRACES
    int IDM_SEARCH_MARK

    int IDM_MISC
    int IDM_FILESWITCHER_FILESCLOSE
    int IDM_FILESWITCHER_FILESCLOSEOTHERS


    int IDM_VIEW
    # int IDM_VIEW_TOOLBAR_HIDE
    int IDM_VIEW_TOOLBAR_REDUCE
    int IDM_VIEW_TOOLBAR_ENLARGE
    int IDM_VIEW_TOOLBAR_STANDARD
    int IDM_VIEW_REDUCETABBAR
    int IDM_VIEW_LOCKTABBAR
    int IDM_VIEW_DRAWTABBAR_TOPBAR
    int IDM_VIEW_DRAWTABBAR_INACIVETAB
    int IDM_VIEW_POSTIT
    int IDM_VIEW_TOGGLE_FOLDALL
    # int IDM_VIEW_USER_DLG
    int IDM_VIEW_LINENUMBER
    int IDM_VIEW_SYMBOLMARGIN
    int IDM_VIEW_FOLDERMAGIN
    int IDM_VIEW_FOLDERMAGIN_SIMPLE
    int IDM_VIEW_FOLDERMAGIN_ARROW
    int IDM_VIEW_FOLDERMAGIN_CIRCLE
    int IDM_VIEW_FOLDERMAGIN_BOX
    int IDM_VIEW_ALL_CHARACTERS
    int IDM_VIEW_INDENT_GUIDE
    int IDM_VIEW_CURLINE_HILITING
    int IDM_VIEW_WRAP
    int IDM_VIEW_ZOOMIN
    int IDM_VIEW_ZOOMOUT
    int IDM_VIEW_TAB_SPACE
    int IDM_VIEW_EOL
    int IDM_VIEW_EDGELINE
    int IDM_VIEW_EDGEBACKGROUND
    int IDM_VIEW_TOGGLE_UNFOLDALL
    int IDM_VIEW_FOLD_CURRENT
    int IDM_VIEW_UNFOLD_CURRENT
    int IDM_VIEW_FULLSCREENTOGGLE
    int IDM_VIEW_ZOOMRESTORE
    int IDM_VIEW_ALWAYSONTOP
    int IDM_VIEW_SYNSCROLLV
    int IDM_VIEW_SYNSCROLLH
    int IDM_VIEW_EDGENONE
    int IDM_VIEW_DRAWTABBAR_CLOSEBOTTUN
    int IDM_VIEW_DRAWTABBAR_DBCLK2CLOSE
    int IDM_VIEW_REFRESHTABAR
    int IDM_VIEW_WRAP_SYMBOL
    int IDM_VIEW_HIDELINES
    int IDM_VIEW_DRAWTABBAR_VERTICAL
    int IDM_VIEW_DRAWTABBAR_MULTILINE
    int IDM_VIEW_DOCCHANGEMARGIN
    int IDM_VIEW_LWDEF
    int IDM_VIEW_LWALIGN
    int IDM_VIEW_LWINDENT
    int IDM_VIEW_SUMMARY

    int IDM_VIEW_FOLD
    int IDM_VIEW_FOLD_1
    int IDM_VIEW_FOLD_2
    int IDM_VIEW_FOLD_3
    int IDM_VIEW_FOLD_4
    int IDM_VIEW_FOLD_5
    int IDM_VIEW_FOLD_6
    int IDM_VIEW_FOLD_7
    int IDM_VIEW_FOLD_8

    int IDM_VIEW_UNFOLD
    int IDM_VIEW_UNFOLD_1
    int IDM_VIEW_UNFOLD_2
    int IDM_VIEW_UNFOLD_3
    int IDM_VIEW_UNFOLD_4
    int IDM_VIEW_UNFOLD_5
    int IDM_VIEW_UNFOLD_6
    int IDM_VIEW_UNFOLD_7
    int IDM_VIEW_UNFOLD_8

    int IDM_VIEW_FILESWITCHER_PANEL
    int IDM_VIEW_SWITCHTO_OTHER_VIEW
    int IDM_EXPORT_FUNC_LIST_AND_QUIT

    int IDM_VIEW_DOC_MAP

    int IDM_VIEW_PROJECT_PANEL_1
    int IDM_VIEW_PROJECT_PANEL_2
    int IDM_VIEW_PROJECT_PANEL_3

    int IDM_VIEW_FUNC_LIST
    int IDM_VIEW_FILEBROWSER

    int IDM_VIEW_TAB1
    int IDM_VIEW_TAB2
    int IDM_VIEW_TAB3
    int IDM_VIEW_TAB4
    int IDM_VIEW_TAB5
    int IDM_VIEW_TAB6
    int IDM_VIEW_TAB7
    int IDM_VIEW_TAB8
    int IDM_VIEW_TAB9
    int IDM_VIEW_TAB_NEXT
    int IDM_VIEW_TAB_PREV
    int IDM_VIEW_MONITORING
    int IDM_VIEW_TAB_MOVEFORWARD
    int IDM_VIEW_TAB_MOVEBACKWARD
    int IDM_VIEW_IN_FIREFOX
    int IDM_VIEW_IN_CHROME
    int IDM_VIEW_IN_EDGE
    int IDM_VIEW_IN_IE

    int IDM_VIEW_GOTO_ANOTHER_VIEW
    int IDM_VIEW_CLONE_TO_ANOTHER_VIEW
    int IDM_VIEW_GOTO_NEW_INSTANCE
    int IDM_VIEW_LOAD_IN_NEW_INSTANCE

    int IDM_FORMAT
    int IDM_FORMAT_TODOS
    int IDM_FORMAT_TOUNIX
    int IDM_FORMAT_TOMAC
    int IDM_FORMAT_ANSI
    int IDM_FORMAT_UTF_8
    int IDM_FORMAT_UCS_2BE
    int IDM_FORMAT_UCS_2LE
    int IDM_FORMAT_AS_UTF_8
    int IDM_FORMAT_CONV2_ANSI
    int IDM_FORMAT_CONV2_AS_UTF_8
    int IDM_FORMAT_CONV2_UTF_8
    int IDM_FORMAT_CONV2_UCS_2BE
    int IDM_FORMAT_CONV2_UCS_2LE

    int IDM_FORMAT_ENCODE
    int IDM_FORMAT_WIN_1250
    int IDM_FORMAT_WIN_1251
    int IDM_FORMAT_WIN_1252
    int IDM_FORMAT_WIN_1253
    int IDM_FORMAT_WIN_1254
    int IDM_FORMAT_WIN_1255
    int IDM_FORMAT_WIN_1256
    int IDM_FORMAT_WIN_1257
    int IDM_FORMAT_WIN_1258
    int IDM_FORMAT_ISO_8859_1
    int IDM_FORMAT_ISO_8859_2
    int IDM_FORMAT_ISO_8859_3
    int IDM_FORMAT_ISO_8859_4
    int IDM_FORMAT_ISO_8859_5
    int IDM_FORMAT_ISO_8859_6
    int IDM_FORMAT_ISO_8859_7
    int IDM_FORMAT_ISO_8859_8
    int IDM_FORMAT_ISO_8859_9
    # int IDM_FORMAT_ISO_8859_10
    # int IDM_FORMAT_ISO_8859_11
    int IDM_FORMAT_ISO_8859_13
    int IDM_FORMAT_ISO_8859_14
    int IDM_FORMAT_ISO_8859_15
    # int IDM_FORMAT_ISO_8859_16
    int IDM_FORMAT_DOS_437
    int IDM_FORMAT_DOS_720
    int IDM_FORMAT_DOS_737
    int IDM_FORMAT_DOS_775
    int IDM_FORMAT_DOS_850
    int IDM_FORMAT_DOS_852
    int IDM_FORMAT_DOS_855
    int IDM_FORMAT_DOS_857
    int IDM_FORMAT_DOS_858
    int IDM_FORMAT_DOS_860
    int IDM_FORMAT_DOS_861
    int IDM_FORMAT_DOS_862
    int IDM_FORMAT_DOS_863
    int IDM_FORMAT_DOS_865
    int IDM_FORMAT_DOS_866
    int IDM_FORMAT_DOS_869
    int IDM_FORMAT_BIG5
    int IDM_FORMAT_GB2312
    int IDM_FORMAT_SHIFT_JIS
    int IDM_FORMAT_KOREAN_WIN
    int IDM_FORMAT_EUC_KR
    int IDM_FORMAT_TIS_620
    int IDM_FORMAT_MAC_CYRILLIC
    int IDM_FORMAT_KOI8U_CYRILLIC
    int IDM_FORMAT_KOI8R_CYRILLIC
    int IDM_FORMAT_ENCODE_END

    # int IDM_FORMAT_CONVERT

    int IDM_LANG
    int IDM_LANGSTYLE_CONFIG_DLG
    int IDM_LANG_C
    int IDM_LANG_CPP
    int IDM_LANG_JAVA
    int IDM_LANG_HTML
    int IDM_LANG_XML
    int IDM_LANG_JS
    int IDM_LANG_PHP
    int IDM_LANG_ASP
    int IDM_LANG_CSS
    int IDM_LANG_PASCAL
    int IDM_LANG_PYTHON
    int IDM_LANG_PERL
    int IDM_LANG_OBJC
    int IDM_LANG_ASCII
    int IDM_LANG_TEXT
    int IDM_LANG_RC
    int IDM_LANG_MAKEFILE
    int IDM_LANG_INI
    int IDM_LANG_SQL
    int IDM_LANG_VB
    int IDM_LANG_BATCH
    int IDM_LANG_CS
    int IDM_LANG_LUA
    int IDM_LANG_TEX
    int IDM_LANG_FORTRAN
    int IDM_LANG_BASH
    int IDM_LANG_FLASH
    int IDM_LANG_NSIS
    int IDM_LANG_TCL
    int IDM_LANG_LISP
    int IDM_LANG_SCHEME
    int IDM_LANG_ASM
    int IDM_LANG_DIFF
    int IDM_LANG_PROPS
    int IDM_LANG_PS
    int IDM_LANG_RUBY
    int IDM_LANG_SMALLTALK
    int IDM_LANG_VHDL
    int IDM_LANG_CAML
    int IDM_LANG_KIX
    int IDM_LANG_ADA
    int IDM_LANG_VERILOG
    int IDM_LANG_AU3
    int IDM_LANG_MATLAB
    int IDM_LANG_HASKELL
    int IDM_LANG_INNO
    int IDM_LANG_CMAKE
    int IDM_LANG_YAML
    int IDM_LANG_COBOL
    int IDM_LANG_D
    int IDM_LANG_GUI4CLI
    int IDM_LANG_POWERSHELL
    int IDM_LANG_R
    int IDM_LANG_JSP
    int IDM_LANG_COFFEESCRIPT
    int IDM_LANG_JSON
    int IDM_LANG_FORTRAN_77
    int IDM_LANG_BAANC
    int IDM_LANG_SREC
    int IDM_LANG_IHEX
    int IDM_LANG_TEHEX
    int IDM_LANG_SWIFT
    int IDM_LANG_ASN1
    int IDM_LANG_AVS
    int IDM_LANG_BLITZBASIC
    int IDM_LANG_PUREBASIC
    int IDM_LANG_FREEBASIC
    int IDM_LANG_CSOUND
    int IDM_LANG_ERLANG
    int IDM_LANG_ESCRIPT
    int IDM_LANG_FORTH
    int IDM_LANG_LATEX
    int IDM_LANG_MMIXAL
    int IDM_LANG_NIMROD
    int IDM_LANG_NNCRONTAB
    int IDM_LANG_OSCRIPT
    int IDM_LANG_REBOL
    int IDM_LANG_REGISTRY
    int IDM_LANG_RUST
    int IDM_LANG_SPICE
    int IDM_LANG_TXT2TAGS
    int IDM_LANG_VISUALPROLOG

    int IDM_LANG_EXTERNAL
    int IDM_LANG_EXTERNAL_LIMIT

    int IDM_LANG_USER
    int IDM_LANG_USER_LIMIT
    int IDM_LANG_USER_DLG

    int IDM_ABOUT
    int IDM_HOMESWEETHOME
    int IDM_PROJECTPAGE
    int IDM_ONLINEHELP
    int IDM_FORUM
    # int IDM_PLUGINSHOME
    int IDM_UPDATE_NPP
    int IDM_WIKIFAQ
    int IDM_HELP
    int IDM_CONFUPDATERPROXY
    int IDM_CMDLINEARGUMENTS
    int IDM_ONLINESUPPORT
    int IDM_DEBUGINFO

    int IDM_SETTING
    # int IDM_SETTING_TAB_SIZE
    # int IDM_SETTING_TAB_REPLCESPACE
    # int IDM_SETTING_HISTORY_SIZE
    # int IDM_SETTING_EDGE_SIZE
    int IDM_SETTING_IMPORTPLUGIN
    int IDM_SETTING_IMPORTSTYLETHEMS
    int IDM_SETTING_TRAYICON
    int IDM_SETTING_SHORTCUT_MAPPER
    int IDM_SETTING_REMEMBER_LAST_SESSION
    int IDM_SETTING_PREFERENCE
    int IDM_SETTING_OPENPLUGINSDIR
    int IDM_SETTING_PLUGINADM
    int IDM_SETTING_SHORTCUT_MAPPER_MACRO
    int IDM_SETTING_SHORTCUT_MAPPER_RUN
    int IDM_SETTING_EDITCONTEXTMENU

    int IDM_TOOL
    int IDM_TOOL_MD5_GENERATE
    int IDM_TOOL_MD5_GENERATEFROMFILE
    int IDM_TOOL_MD5_GENERATEINTOCLIPBOARD
    int IDM_TOOL_SHA256_GENERATE
    int IDM_TOOL_SHA256_GENERATEFROMFILE
    int IDM_TOOL_SHA256_GENERATEINTOCLIPBOARD

    int IDM_EXECUTE

    int IDM_SYSTRAYPOPUP
    int IDM_SYSTRAYPOPUP_ACTIVATE
    int IDM_SYSTRAYPOPUP_NEWDOC
    int IDM_SYSTRAYPOPUP_NEW_AND_PASTE
    int IDM_SYSTRAYPOPUP_OPENFILE
    int IDM_SYSTRAYPOPUP_CLOSE

    #endif #MENUCMDID_H