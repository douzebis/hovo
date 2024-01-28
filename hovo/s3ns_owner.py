__package__ = 'hovo'

from hovo.colors import Rgb
from hovo.const import S3nsOwnerKey
from hovo.const import S3nsOwnerVal
from hovo.row import retrieve_row
from hovo import glob
from hovo import state
from hovo.fixer import Fixer
from hovo.warning import warning

def retrieve_s3ns_owner(rows):

    try:
        key, val = retrieve_row(rows, S3nsOwnerKey, S3nsOwnerVal)
    except StopIteration as e:
        warning(str(e))
        return

    # Provision buganizer imports and cosmetic updates
    url = None if glob.s3nsownersHeadingId == None \
        else f"#heading={glob.s3nsownersHeadingId}"
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
    
    state.s3nsowner_key = key
    state.s3nsowner_val = val