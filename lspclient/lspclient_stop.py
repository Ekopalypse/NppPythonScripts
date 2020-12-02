import lspclient
from Npp import console
try:
    lspclient.stop()
except Exception as e:
    console.writeError(f'error stoping lspclient: {e}')
