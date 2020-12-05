import lspclient
from Npp import console
try:
    lspclient.clear_peek_definition()
except Exception as e:
    console.writeError(f'error while clearing peek annotation: {e}')
