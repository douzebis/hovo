__package__ = 'hovo'

import click

from hovo.colors import Rgb
from hovo.const import LeaderKey
from hovo.const import LeaderVal
from hovo.row import retrieve_row
from hovo import glob
from hovo import state
from hovo.fixer import Fixer
from hovo.warning import warning

def retrieve_leader(rows):

    try:
        key, val = retrieve_row(rows, LeaderKey, LeaderVal)
    except StopIteration as e:
        warning(str(e))
        return

    # Provision buganizer imports and cosmetic updates
    url = None if glob.leadersHeadingId == None \
        else f"#heading={glob.leadersHeadingId}"
    Fixer.update_style(
        key['start'],
        key['end'],
        font_size=None,
        url=url,
    )
    match val['value']:
        case 'S3NS':
            color = Rgb.S3NS
        case 'Joint':
            color = Rgb.JOINT
        case 'Google':
            color = Rgb.GOOGLE
        case _:
            color = Rgb.RED
    Fixer.row_style(
        0,
        rows[0]['startIndex'] - 1,
        bg_color=color,
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
    
    state.leader_key = key
    state.leader_val = val