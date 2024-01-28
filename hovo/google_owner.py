__package__ = 'hovo'

from hovo.colors import Rgb
from hovo.const import GoogleOwnerKey
from hovo.const import GoogleOwnerVal
from hovo.row import retrieve_row
from hovo import glob
from hovo import state
from hovo.fixer import Fixer
from hovo.warning import warning


def retrieve_google_owner(rows):

    try:
        key, val = retrieve_row(rows, GoogleOwnerKey, GoogleOwnerVal)
    except StopIteration as e:
        warning(str(e))
        return

    # Provision buganizer imports and cosmetic updates
    url = None if glob.googleownersHeadingId == None \
        else f"#heading={glob.googleownersHeadingId}"
    Fixer.update_style(
        key['start'],
        key['end'],
        font_size=None,
        url=url,
    )
    if key['text'] != key['target']:
        Fixer.replace(
            key['target'],
            key['start'],
            key['end'],
        )
    
    state.googleowner_key = key
    state.googleowner_val = val