
Proof of concept for creating an lsp-client for notepad++ with Python

***WARNING: is still work in progress, still aplha phase***  
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
	- lspclient_clear_peek_definition.py
	- lspclient_find_references.py
	- lspclient_goto_definition.py
	- lspclient_range_format_document.py
	- lspclient_rename.py

-   modify the file lsp_server_config according to your needs  
-   add additional flush method to ConsoleError object to startup.py
~~~py
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
-  V 0.5
    - fixed a crash because formatting target received a negative position.
    - enhanced formatting and range formatting requests

-  V 0.4
    - added additional setup info
    - multiple new language features added
    - added more logging calls, again.
    
-  V 0.3
    - added additional env (environment variables) to lsp_server_config.json
    - made sure that no other messages are sent if initilize_result from server is pending  
    - removed dynamic registration capabilities from initialize request as those aren't supported yet.  
    - added more logging calls  
    - sucessfully tested basic functionality with non-python lsp servers  
    
-  V 0.2
    - added additional setup info
    - reformatted code to satisfy pyls linter
    - output formatted diags to console to be able to jump to line of interest
    - make format request working
    - make peek request working
    - added more logging calls  
  
### General
- [x] `initialize`
- [x] `initialized`
- [x] `shutdown`
- [x] `exit`
- [ ] `$/cancelRequest`
- [x] `$/progress` (window/progress only atm)
### Window
- [ ] `showMessage`
- [ ] `showMessageRequest`
- [ ] `logMessage`
- [ ] `progress/create`
- [ ] `progress/cancel`
### Telemetry
- [x] `event`
### Client
- [ ] `registerCapability`
- [ ] `unregisterCapability`
### Workspace
- [ ] `workspaceFolders`
- [ ] `didChangeWorkspaceFolder`
- [ ] `didChangeConfiguration`
- [ ] `configuration`
- [ ] `didChangeWatchedFiles`
- [ ] `symbol`
- [ ] `executeCommand`
- [ ] `applyEdit`
### Text Synchronization
- [x] `didOpen`
- [x] `didChange`
- [x] `willSave`
- [ ] `willSaveWaitUntil`
- [x] `didSave`
- [x] `didClose`
### Diagnostics
- [x] `publishDiagnostics`
### Language Features
- [x] `completion`
- [ ] `completion resolve`
- [x] `hover`
- [x] `signatureHelp`
- [ ] `declaration`
- [x] `definition`
- [ ] `typeDefinition`
- [ ] `implementation`
- [x] `references`
- [ ] `documentHighlight`
- [x] `documentSymbol`
- [ ] `codeAction`
- [ ] `codeLens`
- [ ] `codeLens resolve`
- [ ] `documentLink`
- [ ] `documentLink resolve`
- [ ] `documentColor`
- [ ] `colorPresentation`
- [x] `formatting`
- [x] `rangeFormatting`
- [ ] `onTypeFormatting`
- [x] `rename`
- [ ] `prepareRename`
- [ ] `foldingRange`
- [ ] `selectionRange`

