__package__ = 'hovo'

from hovo.buganizer import set_b7r_field
from pyparsing import Opt
import click

from hovo.colors import Ansi, Rgb
from hovo.const import MaturityKey
from hovo.const import MaturityVal
from hovo.row import retrieve_row
from hovo import glob, option
from hovo import state
from hovo.fixer import Fixer
from hovo.warning import warning

def retrieve_maturity(rows):

    try:
        key, val = retrieve_row(rows, MaturityKey, MaturityVal)
    except StopIteration as e:
        warning(str(e))
        return

    # Provision buganizer imports and cosmetic updates
    url = None if glob.maturityHeadingId == None \
        else f"#heading={glob.maturityHeadingId}"
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
    match val['value']:
        case None:
            color = Rgb.RED
        case 0:
            color = Rgb.ZERO_STAR
        case 1:
            color = Rgb.ONE_STAR
        case 2:
            color = Rgb.TWO_STARS
        case 3:
            color = Rgb.THREE_STARS
        case _:
            raise click.ClickException("Internal error")
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
    if not option.dry_run and option.export_maturity:
        if val['value'] != val['b7r']:
            set_b7r_field(state.bugid['value'], 'maturity', val['value'])
    
    state.maturity_key = key
    state.maturity_val = val