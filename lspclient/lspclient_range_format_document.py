import lspclient
from Npp import console
try:
    lspclient.range_format_document()
except Exception as e:
    console.writeError(f'error while formatting range of document: {e}')
