import lspclient
from Npp import console
try:
    lspclient.rename()
except Exception as e:
    console.writeError(f'error calling rename: {e}')
