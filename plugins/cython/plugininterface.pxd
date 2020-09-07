
from windowsapi cimport *
from libcpp cimport bool 

cdef extern from "PluginInterface.h":
    # int nbChar = 64
    # ctypedef void (__cdecl * PFUNCPLUGINCMD)()
    ctypedef struct NppData:
        HWND _nppHandle
        HWND _scintillaMainHandle
        HWND _scintillaSecondHandle

    ctypedef struct ShortcutKey:
        bool _isCtrl
        bool _isAlt
        bool _isShift
        unsigned char _key

    ctypedef struct FuncItem:
        WCHAR _itemName[64]
        void* _pFunc
        int _cmdID
        bool _init2Check
        ShortcutKey *_pShKey

    cdef void setInfo(NppData)
    cdef LPCWSTR getName()
    cdef FuncItem * getFuncsArray(int *)
    cdef void beNotified(SCNotification *)
    cdef LRESULT messageProc(UINT Message, WPARAM wParam, LPARAM lParam)
    cdef bool isUnicode()

cdef extern from "scintilla.h":
    ctypedef struct Sci_NotifyHeader:
        void* hwndFrom
        uptr_t idFrom
        unsigned int code
        
    ctypedef struct SCNotification:
        Sci_NotifyHeader nmhdr
        Sci_Position position
        int ch
        int modifiers
        int modificationType
        const char* text
        Sci_Position length
        Sci_Position linesAdded
        int message
        uptr_t wParam
        sptr_t lParam
        Sci_Position line
        int foldLevelNow
        int foldLevelPrev
        int margin
        int listType
        int x
        int y
        int token
        Sci_Position annotationLinesAdded
        int updated
        int listCompletionMethod
