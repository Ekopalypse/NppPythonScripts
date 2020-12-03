import lspclient
from Npp import console
try:
    lspclient.peek_definition()
except Exception as e:
    console.writeError(f'error while peeking: {e}')
