from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Compiler import Options

Options.annotate = True

PLUGIN_NAME = 'CythonPlugin'
MODULE_NAME = 'CythonPlugin'
NPP_DIR = r'D:\PortableApps\Npp'

cpp_init_code = f'''#include <Python.h>
#include "PluginInterface.h"

PyMODINIT_FUNC PyInit_{MODULE_NAME}(void);

BOOL APIENTRY DllMain( HANDLE hModule,
                       DWORD  reasonForCall,
                       LPVOID /* lpReserved */ )
{{
    switch ( reasonForCall )
    {{
        case DLL_PROCESS_ATTACH:
            if (!Py_IsInitialized())
            {{
                PyImport_AppendInittab("{MODULE_NAME}", &PyInit_{MODULE_NAME});
                Py_InitializeEx(0);
                PyEval_InitThreads();
            }}
            PyImport_ImportModule("{MODULE_NAME}");
            break;
        case DLL_PROCESS_DETACH:
            Py_Finalize();
            break;

        case DLL_THREAD_ATTACH:
            break;

        case DLL_THREAD_DETACH:
            break;
    }}

    return TRUE;
}}'''

with open("plugininit.cpp", "w") as f:
    f.write(cpp_init_code)

extensions = [
    Extension("CYTHON_PLUGIN", 
              ["CYTHON_PLUGIN.pyx", "plugininit.cpp"], 
              export_symbols = [
                'setInfo',
                'getName',
                'getFuncsArray',
                'beNotified',
                'messageProc',
                'isUnicode',
              ],
              libraries=["user32"])
]

extensions = [
    Extension(MODULE_NAME, 
              ["plugin.pyx", "plugininit.cpp"],
              export_symbols = [
                'setInfo',
                'getName',
                'getFuncsArray',
                'beNotified',
                'messageProc',
                'isUnicode',
              ],
              libraries=["user32"])
]


setup(
    name=f"{PLUGIN_NAME}",
    ext_modules=cythonize(extensions, 
                          compiler_directives={'language_level' : "3", 
                                               'embedsignature': True},
                          ), 
    requires=['Cython'],
)


def copy_and_rename():
    import sys
    import platform
    from pathlib import Path
    from shutil import copyfile
    
    v = platform.python_version_tuple()
    max_min_version = f'{v[0]}{v[1]}'
    if platform.architecture()[0] == '32bit':
        pyd = Path(f'{MODULE_NAME}.cp{max_min_version}-win32.pyd')
    else:
        pyd = Path(f'{MODULE_NAME}.cp{max_min_version}-win_amd64.pyd')
            

    target_dir = Path(NPP_DIR)
    
    if pyd.exists():
        plugins_dir = target_dir.joinpath('plugins', f'{PLUGIN_NAME}')
        if not plugins_dir.exists():
            plugins_dir.mkdir()
        print(f'copying {pyd.absolute()} to {plugins_dir}')        
        copyfile(pyd.absolute(), plugins_dir.joinpath(f'{PLUGIN_NAME}.dll'))
                
        py_dll = 'python{}{}.dll'.format(*sys.version_info[:2])
        python_path = Path(sys.prefix)
        full_py_dll_path = python_path.joinpath(py_dll)
        print(f'copying {full_py_dll_path} to {plugins_dir}')
        copyfile(full_py_dll_path, plugins_dir.joinpath(py_dll))

copy_and_rename()
