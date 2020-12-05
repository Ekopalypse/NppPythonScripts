import lspclient
from Npp import notepad, console
try:
    lspclient.start(notepad.getPluginConfigDir()+'\\lsp_server_config.json')
except Exception as e:
    console.writeError(f'error starting lspclient: {e}')
    lspclient.stop()
