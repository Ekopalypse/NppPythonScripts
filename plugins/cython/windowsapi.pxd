from libc.stdint cimport int64_t, uint64_t

IF UNAME_MACHINE == 'AMD64':
    DEF _WIN64 = True
ELSE:
    DEF _WIN64 = False
# DEF _M_IX86 = False
# DEF UNICODE = True

cdef extern from "Windows.h" nogil:
    # ctypedef Py_UNICODE WCHAR
    # ctypedef unsigned short WORD
    # ctypedef int BOOL
    # ctypedef unsigned char BYTE
    # ctypedef char CCHAR
    # ctypedef char CHAR
    # ctypedef unsigned long DWORD
    # ctypedef uint64_t DWORDLONG
    # ctypedef unsigned int DWORD32
    # ctypedef uint64_t DWORD64
    # ctypedef float FLOAT
    # ctypedef void *PVOID
    # ctypedef const void *LPCVOID
    # ctypedef const WCHAR *LPCWSTR
    # ctypedef WCHAR *LPWSTR
    
    # IF _M_IX86:
        # ctypedef double ULONGLONG
        # ctypedef double LONGLONG
    # ELSE:
        # ctypedef uint64_t ULONGLONG
        # ctypedef int64_t LONGLONG 

    # IF _WIN64:
        # ctypedef uint64_t ULONG_PTR
        # ctypedef int HALF_PTR
        # ctypedef int64_t INT_PTR 
        # ctypedef int64_t LONG_PTR 
        # ctypedef HALF_PTR *PHALF_PTR
        # ctypedef unsigned int UHALF_PTR
        # ctypedef UHALF_PTR *PUHALF_PTR
        # ctypedef uint64_t UINT_PTR
    # ELSE:
        # ctypedef unsigned long ULONG_PTR
        # ctypedef short HALF_PTR
        # ctypedef int INT_PTR
        # ctypedef long LONG_PTR
        # ctypedef HALF_PTR *PHALF_PTR
        # ctypedef unsigned short UHALF_PTR
        # ctypedef UHALF_PTR *PUHALF_PTR
        # ctypedef unsigned int UINT_PTR

    # IF UNICODE:
        # ctypedef LPCWSTR LPCTSTR 
        # ctypedef LPWSTR LPTSTR
        # ctypedef LPCWSTR PCTSTR
        # ctypedef LPWSTR PTSTR
        # ctypedef WCHAR TBYTE
        # ctypedef WCHAR TCHAR
    # ELSE:
        # ctypedef LPCSTR LPCTSTR
        # ctypedef LPSTR LPTSTR
        # ctypedef LPCSTR PCTSTR
        # ctypedef LPSTR PTSTR
        # ctypedef unsigned char TBYTE
        # ctypedef char TCHAR

    # ctypedef WORD ATOM
    # ctypedef BYTE BOOLEAN
    # ctypedef DWORD COLORREF
    # ctypedef ULONG_PTR DWORD_PTR
    # ctypedef PVOID HANDLE
    # ctypedef HANDLE HACCEL

    # ctypedef HANDLE HBITMAP
    # ctypedef HANDLE HBRUSH
    # ctypedef HANDLE HCOLORSPACE
    # ctypedef HANDLE HCONV
    # ctypedef HANDLE HCONVLIST
    # ctypedef HANDLE HICON
    # ctypedef HICON HCURSOR
    # ctypedef HANDLE HDC
    # ctypedef HANDLE HDDEDATA
    # ctypedef HANDLE HDESK
    # ctypedef HANDLE HDROP
    # ctypedef HANDLE HDWP
    # ctypedef HANDLE HENHMETAFILE
    # ctypedef int HFILE
    # ctypedef HANDLE HFONT
    # ctypedef HANDLE HGDIOBJ
    # ctypedef HANDLE HGLOBAL
    # ctypedef HANDLE HHOOK
    # ctypedef HANDLE HINSTANCE
    # ctypedef HANDLE HKEY
    # ctypedef HANDLE HKL
    # ctypedef HANDLE HLOCAL
    # ctypedef HANDLE HMENU
    # ctypedef HANDLE HMETAFILE
    # ctypedef HINSTANCE HMODULE
    # ctypedef HANDLE HPALETTE
    # ctypedef HANDLE HPEN
    # ctypedef long LONG
    # ctypedef LONG HRESULT
    # ctypedef HANDLE HRGN
    # ctypedef HANDLE HRSRC
    # ctypedef HANDLE HSZ
    # ctypedef HANDLE WINSTA
    # ctypedef HANDLE HWND
    # ctypedef int INT

    # ctypedef signed char INT8
    # ctypedef signed short INT16
    # ctypedef signed int INT32
    # ctypedef int64_t INT64
    # ctypedef WORD LANGID
    # ctypedef DWORD LCID
    # ctypedef DWORD LCTYPE
    # ctypedef DWORD LGRPID

    # ctypedef signed int LONG32
    # ctypedef int64_t LONG64
    # ctypedef LONG_PTR LPARAM
# #     ctypedef BOOL far *LPBOOL
# #     ctypedef BYTE far *LPBYTE
    # ctypedef DWORD *LPCOLORREF
    # ctypedef const CHAR *LPCSTR


    # ctypedef DWORD *LPDWORD
    # ctypedef HANDLE *LPHANDLE
    # ctypedef int *LPINT
    # ctypedef long *LPLONG
    # ctypedef CHAR *LPSTR

    # ctypedef void *LPVOID
    # ctypedef WORD *LPWORD

    # ctypedef LONG_PTR LRESULT
    # ctypedef BOOL *PBOOL
    # ctypedef BOOLEAN *PBOOLEAN
    # ctypedef BYTE *PBYTE
    # ctypedef CHAR *PCHAR
    # ctypedef const CHAR *PCSTR

    # ctypedef const WCHAR *PCWSTR
    # ctypedef DWORD *PDWORD
    # ctypedef DWORDLONG *PDWORDLONG
    # ctypedef DWORD_PTR *PDWORD_PTR
    # ctypedef DWORD32 *PDWORD32
    # ctypedef DWORD64 *PDWORD64
    # ctypedef FLOAT *PFLOAT

    # ctypedef HANDLE *PHANDLE
    # ctypedef HKEY *PHKEY
    # ctypedef int *PINT
    # ctypedef INT_PTR *PINT_PTR
    # ctypedef INT8 *PINT8
    # ctypedef INT16 *PINT16
    # ctypedef INT32 *PINT32
    # ctypedef INT64 *PINT64
    # ctypedef PDWORD PLCID
    # ctypedef LONG *PLONG
    # ctypedef LONGLONG *PLONGLONG
    # ctypedef LONG_PTR *PLONG_PTR
    # ctypedef LONG32 *PLONG32
    # ctypedef LONG64 *PLONG64

    # ctypedef short SHORT
    # ctypedef SHORT *PSHORT
    # ctypedef ULONG_PTR SIZE_T
    # ctypedef LONG_PTR SSIZE_T    
    # ctypedef SIZE_T *PSIZE_T
    # ctypedef SSIZE_T *PSSIZE_T
    # ctypedef CHAR *PSTR
    # ctypedef TBYTE *PTBYTE
    # ctypedef TCHAR *PTCHAR

    # ctypedef unsigned char UCHAR
    # ctypedef UCHAR *PUCHAR

    # ctypedef unsigned int UINT
    # ctypedef UINT *PUINT
    # ctypedef UINT_PTR *PUINT_PTR
    # ctypedef unsigned char UINT8
    # ctypedef unsigned short UINT16
    # ctypedef unsigned int UINT32
    # ctypedef uint64_t UINT64
    # ctypedef unsigned long ULONG
    # ctypedef unsigned int ULONG32
    # ctypedef uint64_t ULONG64
    # ctypedef UINT8 *PUINT8
    # ctypedef UINT16 *PUINT16
    # ctypedef UINT32 *PUINT32
    # ctypedef UINT64 *PUINT64
    # ctypedef ULONG *PULONG
    # ctypedef ULONGLONG *PULONGLONG
    # ctypedef ULONG_PTR *PULONG_PTR
    # ctypedef ULONG32 *PULONG32
    # ctypedef ULONG64 *PULONG64
    # ctypedef unsigned short USHORT
    # ctypedef USHORT *PUSHORT

    # ctypedef WCHAR *PWCHAR
    # ctypedef WORD *PWORD
    # ctypedef WCHAR *PWSTR
    # ctypedef uint64_t QWORD
    # ctypedef HANDLE SC_HANDLE
    # ctypedef LPVOID SC_LOCK
    # ctypedef HANDLE SERVICE_STATUS_HANDLE

    # ctypedef struct UNICODE_STRING:
        # USHORT Length
        # USHORT MaximumLength
        # PWSTR Buffer
    # ctypedef UNICODE_STRING *PUNICODE_STRING
    # ctypedef const UNICODE_STRING *PCUNICODE_STRING

    # ctypedef UINT_PTR WPARAM    
    # ctypedef unsigned int* uptr_t
    # ctypedef int* sptr_t
    
    IF _WIN64:
        ctypedef int64_t LONG_PTR 
        ctypedef uint64_t UINT_PTR
    ELSE:
        ctypedef long LONG_PTR
        ctypedef unsigned int UINT_PTR

    ctypedef Py_UNICODE WCHAR
    ctypedef WCHAR TCHAR
    ctypedef WCHAR* LPCWSTR
    ctypedef unsigned int* uptr_t
    ctypedef int* sptr_t    
    ctypedef void* HANDLE
    ctypedef HANDLE HWND
    ctypedef HANDLE HBITMAP
    ctypedef HANDLE HICON
    
    ctypedef unsigned int UINT
    ctypedef UINT_PTR WPARAM
    ctypedef LONG_PTR LPARAM
    ctypedef LONG_PTR LRESULT
    
    cdef LRESULT SendMessageW(HWND   hWnd,
                              UINT   Msg,
                              WPARAM wParam,
                              LPARAM lParam)


cdef extern from "stddef.h":
    ctypedef ptrdiff_t Sci_Position    
