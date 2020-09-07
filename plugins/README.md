
Proof of concept of using pthon together with either
cython or cffi to create a notepad++ plugin

To create the cffi based plugin edit test_cffi.py and modify PLUGIN_NAME and NPP_DIR to your needs 
and then run python.exe test_cffi.py.
If everything goes well the plugin got created and copied to notepad++ plugins directory.

To create the cython based plugin edit setup.py and modify PLUGIN_NAME, MODULE_NAME and NPP_DIR 
and in plugin.pxy modify LOG_FILE to your needs.
Then run python.exe setup.py build_ext -i
If there is no error the plugin will be created and copied to the notepad++ plugins directory.

Tested on Windows 7 x64 with
    Python 3.8.5
    cffi 1.14.2 (pip install cffi)
    cython 3.0a6 (pip install --pre cython)
    Visual Studio 2017 Community Edition
