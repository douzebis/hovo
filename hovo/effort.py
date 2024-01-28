__package__ = 'hovo'

from hovo.colors import Rgb
from hovo.const import EffortKey
from hovo.const import EffortVal
from hovo.row import retrieve_row
from hovo import glob
from hovo import state
from hovo.fixer import Fixer
from hovo.warning import warning

def retrieve_effort(rows):

    try:
        key, val = retrieve_row(rows, EffortKey, EffortVal)
    except StopIteration as e:
        warning(str(e))
        return

    # Provision buganizer imports and cosmetic updates
    url = None if glob.effortHeadingId == None \
        else f"#heading={glob.effortHeadingId}"
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
    color = Rgb.RED if val['value'] == None or val['value'] == 'TBD' \
        else Rgb.BLACK
    Fixer.update_style(
        val['start'],
        val['end'],
        fg_color=color,
        font_size=None,
        url=None,
    )
    if val['text'] != val['target']:
        Fixer.replace(
            val['target'],
            val['start'],
            val['end'],
        )
    
    state.effort_key = key
    state.effort_val = val