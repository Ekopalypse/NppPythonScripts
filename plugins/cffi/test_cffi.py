# -*- coding: utf-8 -*-
import cffi

ffibuilder = cffi.FFI()
ffibuilder.set_unicode(True)

PLUGIN_NAME = 'CFFI_PLUGIN'  # careful - is used below as well
NPP_DIR = r'D:\PortableApps\Npp'     # <<== THIS NEEDS TO BE MODFIED

MODIFIED_PLUGIN_HEADER = 'modified_plugin.h'
with open(MODIFIED_PLUGIN_HEADER) as f:
    # read the modified plugininterface.h and pass it to embedding_api(),
    # manually removing the '#' directives and the CFFI_DLLEXPORT
    data = ''.join([line for line in f if not line.startswith('#')])
    data = data.replace('CFFI_DLLEXPORT', '')
    ffibuilder.embedding_api(data)


# exported python functions which will show up in the menu
ffibuilder.cdef("""
extern "Python" void open_doc();
extern "Python" void close_doc();
""")

ffibuilder.set_source(PLUGIN_NAME, f'''
#include "{MODIFIED_PLUGIN_HEADER}"
''')

ffibuilder.embedding_init_code(
f'from {PLUGIN_NAME} import ffi, lib'  +
"""
import os
import logging
import ctypes

SENDMESSAGE = ctypes.WinDLL('user32', use_last_error=True).SendMessageW

WM_USER = 1024
NPPMSG = WM_USER + 1000
NPPM_MENUCOMMAND = NPPMSG + 48

IDM = 40000
IDM_FILE = IDM + 1000
IDM_FILE_NEW = IDM_FILE + 1
IDM_FILE_CLOSE = IDM_FILE + 3

cur_dir = os.path.abspath(os.path.curdir)
LOG_FILE = os.path.join(cur_dir, r'plugins\{0}', '{0}.log')
FORMAT = '%(asctime)-15s %(threadName)-10s %(thread)-5d %(funcName)-20s  %(message)s'
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format=FORMAT,
                    )
log = logging.info

_keepalive = None  # to keep the c objects alive
notif_map = {{}}
npp_hwnd = None
sci1_hwnd = None
sci2_hwnd = None

# error handler
def _onerror(exception, exc_value, traceback):
    log(f'exception: {{exception}}')
    log(f'exc_value: {{exc_value}}')
    log(f'traceback: {{traceback}}')


@ffi.def_extern(onerror=_onerror)
def isUnicode():
    log('npp checks if this is a unicode build - always return true')
    return True


@ffi.def_extern(onerror=_onerror)
def getName():
    log('npp asks for the plugin name - give it to it')
    return ffi.new('TCHAR []', '{0}')


@ffi.def_extern(onerror=_onerror)
def setInfo(npp_data):
    log('npp informs us about some window handles')
    global npp_hwnd
    global sci1_hwnd
    global sci2_hwnd
    npp_hwnd = int(ffi.cast('intptr_t', npp_data._nppHandle))
    sci1_hwnd = int(ffi.cast('intptr_t', npp_data._scintillaMainHandle))
    sci2_hwnd = int(ffi.cast('intptr_t', npp_data._scintillaSecondHandle))
    notif_map.update({{npp_hwnd : 'npp',
                      sci1_hwnd : 'editor1',
                      sci2_hwnd : 'editor2'}})

    log(f'npp hwnd is {{npp_hwnd}}')
    log(f'sci1 hwnd is {{sci1_hwnd}}')
    log(f'sci2 hwnd is {{sci2_hwnd}}')


@ffi.def_extern(onerror=_onerror)
def beNotified(notification):
    _hwndFrom = int(ffi.cast('intptr_t', notification.nmhdr.hwndFrom))
    _code = int(ffi.cast('uintptr_t', notification.nmhdr.code))
    _idFrom = int(ffi.cast('uintptr_t', notification.nmhdr.idFrom))
    if _hwndFrom in notif_map:
        log(f'from {{notif_map[_hwndFrom]}}')
    # else:
        # log(f'from {{_hwndFrom}}')


@ffi.def_extern(onerror=_onerror)
def messageProc(message, wparam, lparam):
    # log(f'{{message}} {{wparam}} {{lparam}}')
    return True


@ffi.def_extern(onerror=_onerror)
def getFuncsArray(_nbF):
    log('npp asks for the function/menu items')
    _nbF[0] = 2
    funcItem = ffi.new('FuncItem[2]')
    list_of_exported_functions = [(lib.open_doc, 'Open customized new document'),
                                  (lib.close_doc, 'Close active document')]
                                  
    for i, exported_functions in enumerate(list_of_exported_functions):
        funcItem[i]._pFunc = exported_functions[0]
        funcItem[i]._cmdID = 0
        funcItem[i]._itemName = exported_functions[1]
        funcItem[i]._init2Check = False
        funcItem[i]._pShKey = ffi.NULL

    global _keepalive
    _keepalive = funcItem
    return funcItem


@ffi.def_extern(onerror=_onerror)
def open_doc():
    SCI_LEXER = ctypes.WinDLL('SciLexer.dll', use_last_error=True)

    result = SENDMESSAGE(npp_hwnd, NPPM_MENUCOMMAND, 0, IDM_FILE_NEW)
    log(f'npp sendmessage returned:{{result}}')

    sci_direct_function = SCI_LEXER.Scintilla_DirectFunction
    sci_direct_pointer = SENDMESSAGE(sci1_hwnd, 2185, 0, 0)

    SCI_ADDTEXT = 2001
    SCI_GETSTATUS = 2383

    message = 'this text is copyright protected by cffi ;-)'.encode('utf8')
    result = sci_direct_function(sci_direct_pointer, SCI_ADDTEXT, len(message), message)
    error_status = sci_direct_function(sci_direct_pointer, SCI_GETSTATUS, None, None)

    if error_status > 0:
        log(f'-->> ERROR: {{error_status}}')


@ffi.def_extern(onerror=_onerror)
def close_doc():
    result = SENDMESSAGE(npp_hwnd, NPPM_MENUCOMMAND, 0, IDM_FILE_CLOSE)
    log(f'npp sendmessage returned:{{result}}')

""".format(PLUGIN_NAME))

# now this is were the magic happens
ffibuilder.compile(target=f'{PLUGIN_NAME}.dll', verbose=True)

# create the needed plugin directory and copy the plugin.dll into it
if __name__ == '__main__':
    import sys
    import os
    from shutil import copyfile
    
    print('\n')
    
    dll_name = PLUGIN_NAME +'.dll'
    source_dir = os.path.abspath(os.path.curdir)
    source = os.path.join(source_dir, dll_name)
    target_dir = os.path.join(NPP_DIR, f'plugins\\{PLUGIN_NAME}')
    target = os.path.join(target_dir, dll_name)

    if not os.path.exists(target_dir):
        print(f'creating {target_dir}')
        os.makedirs(target_dir)  # create the plugin directory

    if os.path.exists(target):
        print(f'deleting existing {target}')
        os.unlink(target)  # delete an existing version - only possible if not loaded by npp instance

    # copy plugin dll and pythonXX.dll
    print(f'copying {source} to {target}')
    copyfile(source, target)
    
    py_dll = 'python{}{}.dll'.format(*sys.version_info[:2])
    full_py_dll_path = os.path.join(sys.prefix, py_dll)
    print(f'copying {full_py_dll_path} to {target_dir}')
    copyfile(full_py_dll_path, os.path.join(target_dir, py_dll))
