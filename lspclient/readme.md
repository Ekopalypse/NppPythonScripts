
Proof of concept for creating an lsp-client for notepad++ with Python

***WARNING: is still work in progress***  
Even if some LSP messages have already been created, they are not yet sufficient tested, so CAUTION!

Requirement: installed PythonScript plugin version 3.X

## Setup:  
-   copy lsp_server_config.json to ...\plugins\Config  
-   create a directory ...\plugins\Config\PythonScript\lib  
-   and copy the file Npp.pyi there  
-   create a directory ...\plugins\Config\PythonScript\lib\lspclient  
-   copy the following files there  
	- client.py  
	- io_handler.py  
	- \_\_init\_\_.py  
	- lsp_protocol.py  
-   the remaining files are copied to ...\plugins\Config\PythonScript\scripts  
	- lspclient_start.py  
	- lspclient_stop.py
	- lspclient_format_document.py
	- lspclient_peek_definition.py

-   modify the file lsp_server_config according to your needs  
-   add additional flush method to ConsoleError object to startup.py
~~~
class ConsoleError:
    def __init__(self):
        global console
        self._console = console;

    def write(self, text):
        self._console.writeError(text);

    def flush(self):
        pass
~~~
  
- start Npp and the lsp-client via the lspclient_start.py  
- Done.  
	
Note: use the console, because diagnostic information are currently being displayed there.  
The lsp-client is currently configured with logging by default. If you have problems ... take a look into it.

## Changes  
-  V 0.2
    - added additional setup info
    - reformatted code to satisfy pyls linter
    - output formatted diags to console to be able to jump to line of interest
    - make format request working
    - make peek request working
    - added more logging calls
