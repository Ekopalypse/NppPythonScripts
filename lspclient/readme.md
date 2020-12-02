
Proof of concept for creating an lsp-client for notepad++ with Python

***WARNING: is still work in progress***
Even if some LSP messages have already been created, they are not yet sufficient tested, so CAUTION!

Requirement: installed PythonScript plugin version 3.X

Setup:
	- copy lsp_server_config.json to ...\plugins\Config
	- create a directory ...\plugins\Config\PythonScript\lib
	- and copy the file Npp.pyi there
	- create a directory ...\plugins\Config\PythonScript\lib\lspclient
	- copy the following files there
		- client.py
		- io_handler.py
		- \_\_init\_\_.py
		- lsp_protocol.py
	- the remaining files are copied to ...\plugins\Config\PythonScript\scripts
		- lspclient_start.py
		- lspclient_stop.py

	- modify the file lsp_server_config according to your needs
	
	- start Npp and the lsp-client via the lspclient_start.py
	- Done.
	
Note: use the console, because diagnostic information are currently being displayed there.
The lsp-client is currently configured with logging by default. If you have problems ... take a look into it.
