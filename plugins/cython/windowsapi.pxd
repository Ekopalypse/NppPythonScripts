from libc.stdint cimport int64_t, uint64_t

IF UNAME_MACHINE == 'AMD64':
    DEF _WIN64 = True
ELSE:
    DEF _WIN64 = False

cdef extern from "Windows.h" nogil:
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
