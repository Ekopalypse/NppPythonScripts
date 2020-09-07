# distutils: language=c++

from windowsapi cimport *
from plugininterface cimport *
from npp cimport *
from libcpp.vector cimport vector
from libcpp cimport bool 

import logging
from logging.handlers import RotatingFileHandler
LOG_FILE = r'D:\cython_plugin.log'
FORMAT = '%(relativeCreated)10d %(name)-20s %(thread)-5d %(funcName)-32s  %(message)s'
logging.basicConfig(
    handlers=[RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=5)],
    level=logging.INFO,
    format=FORMAT,
    )
logger = logging.getLogger(__name__)
log = logger.info
log('Initialized')

cdef HWND npp_hwnd
cdef HWND sci1_hwnd
cdef HWND sci2_hwnd

notif_map = {}


cdef open_doc():
    log(f'SendMessageW({<size_t>npp_hwnd}, {NPPM_MENUCOMMAND}, 0, {IDM_FILE_NEW})')
    result = SendMessageW(npp_hwnd, NPPM_MENUCOMMAND, 0, IDM_FILE_NEW)
    log(f'npp SendMessageW returned:{result}')

    SCI_ADDTEXT = 2001
    SCI_GETSTATUS = 2383

    message = 'this text is copyright protected by cython ;-)'.encode('utf8')
    
    log(f'SendMessageW({<size_t>sci1_hwnd}, {SCI_ADDTEXT}, {len(message)}, {message})')
    result = SendMessageW(sci1_hwnd, SCI_ADDTEXT, <WPARAM>(len(message)), <LPARAM><char*>message)
    log(f'sci SendMessageW returned:{result}')
    
    log(f'SendMessageW({<size_t>sci1_hwnd}, {SCI_GETSTATUS}, 0, 0)')
    result = SendMessageW(sci1_hwnd, SCI_GETSTATUS, 0, 0)
    log(f'sci SendMessageW returned:{result}')


cdef close_doc():
    log(f'SendMessageW({<size_t>npp_hwnd}, {NPPM_MENUCOMMAND}, 0, {IDM_FILE_CLOSE})')
    result = SendMessageW(npp_hwnd, NPPM_MENUCOMMAND, 0, IDM_FILE_CLOSE)
    log(f'npp SendMessageW returned:{result}')


cdef vector[FuncItem] *vfi = new vector[FuncItem]()
cdef void create_funcitem_array():

    cdef FuncItem menuItem
    menuItem._itemName = <LPCWSTR>'&Open customized new document'
    menuItem._pFunc = &open_doc
    menuItem._cmdID = 0
    menuItem._init2Check = False
    menuItem._pShKey = NULL
    vfi.push_back(menuItem)

    menuItem._itemName = <LPCWSTR>'&Close active document'
    menuItem._pFunc = &close_doc
    menuItem._cmdID = 0
    menuItem._init2Check = False
    menuItem._pShKey = NULL
    vfi.push_back(menuItem)
    

cdef extern FuncItem* getFuncsArray(int *nbF):
    log('npp asks for the function/menu items')
    create_funcitem_array()
    nbF[0] = <int>vfi.size() 
    return <FuncItem*>vfi.data()


cdef extern void setInfo(NppData notepadPlusData):
    log('npp informs us about some window handles')
    nppData = notepadPlusData
    global npp_hwnd
    global sci1_hwnd
    global sci2_hwnd
    
    npp_hwnd = nppData._nppHandle
    sci1_hwnd = nppData._scintillaMainHandle
    sci2_hwnd = nppData._scintillaSecondHandle
    
    notif_map.update({<size_t>npp_hwnd: 'npp',
                      <size_t>sci1_hwnd: 'editor1',
                      <size_t>sci2_hwnd: 'editor2'})

    log(f'npp  hwnd is {<size_t>npp_hwnd}')
    log(f'sci1 hwnd is {<size_t>sci1_hwnd}')
    log(f'sci2 hwnd is {<size_t>sci2_hwnd}')


cdef extern LPCWSTR getName():
    log('npp asks for the plugin name - give it to it')
    return 'CYTHON_PLUGIN'
    
    
cdef extern void beNotified(SCNotification *notifyCode):
    _hwndFrom = <size_t>notifyCode.nmhdr.hwndFrom
    _code = <size_t>notifyCode.nmhdr.code
    _idFrom = <size_t>notifyCode.nmhdr.idFrom
    if _hwndFrom in notif_map:
        log(f'notification received from {notif_map[_hwndFrom]}')

    
cdef extern LRESULT messageProc(UINT Message, WPARAM wParam, LPARAM lParam):
    return True

    
cdef extern bool isUnicode():
    log('npp checks if this is a unicode build - always return true')
    return True
