
Proof of concept of using pthon together with either
cython or cffi to create a notepad++ plugin

To create the cffi based plugin edit __test_cffi.py__ and modify _PLUGIN_NAME_ and _NPP_DIR_ to your needs  
and then run `python.exe test_cffi.py`.  
If everything goes well the plugin got created and copied to notepad++ plugins directory.

To create the cython based plugin edit __setup.py__ and modify _PLUGIN_NAME_, _MODULE_NAME_ and _NPP_DIR_  
and in __plugin.pxy__ modify _LOG_FILE_ to your needs.  
Then run `python.exe setup.py build_ext -i`  
If there is no error the plugin will be created and copied to the notepad++ plugins directory.  

Tested on Windows 7 x64 with
~~~
    Python 3.8.5
    cffi 1.14.2 (pip install cffi)
    cython 3.0a6 (pip install --pre cython)
    Visual Studio 2017 Community Edition
~~~
