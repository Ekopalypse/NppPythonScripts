import lspclient
from Npp import console
try:
    lspclient.goto_definition()
except Exception as e:
    console.writeError(f'error while going to definition position: {e}')
