import lspclient
from Npp import console
try:
    lspclient.references()
except Exception as e:
    console.writeError(f'error while trying to find references: {e}')
