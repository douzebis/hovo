__package__ = 'hovo'

from hovo.colors import Rgb
from hovo.const import StageKey
from hovo.const import StageVal
from hovo.row import retrieve_row
from hovo import glob
from hovo import state
from hovo.fixer import Fixer
from hovo.warning import warning

def retrieve_stage(rows):

    try:
        key, val = retrieve_row(rows, StageKey, StageVal)
    except StopIteration as e:
        warning(str(e))
        return

    # Provision buganizer imports and cosmetic updates
    url = None if glob.stagesHeadingId == None \
        else f"#heading={glob.stagesHeadingId}"
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
    color = Rgb.RED if val['value'] == None else Rgb.BLACK
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
    
    state.stage_key = key
    state.stage_val = val