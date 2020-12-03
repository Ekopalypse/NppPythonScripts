import lspclient
from Npp import console
try:
    lspclient.format_document()
except Exception as e:
    console.writeError(f'error while formatting document: {e}')
