__package__ = 'hovo'

import json

import click

from hovo.const import MATURITY_KEY
from hovo.const import MATURITY_VAL
from hovo.const import RAW_LABEL
from hovo.const import TRIMMER
from hovo.const import STAR
from hovo.const import STARS
from hovo.glob import S
from hovo.structural import rse
from hovo.warning import warning

def retrieve_maturity(rows):
    global S

    # Find the stage row
    row = next(
        (r for r in rows
         if MATURITY_KEY.parse.search(rse(r.get('tableCells')[0].get('content')))),
        None)
    # Check the integrity of the maturity row
    if row == None:
        warning(f"Cannot find maturity row")
        return
    cells = row.get('tableCells')
    if len(cells) != 2:
        warning(f"maturity row have exactly two cells: {rse([row])}")
        return
    content = cells[0].get('content')
    startIndex = content[0]['startIndex']
    text = rse(content)
    #maturity_k = MATURITY_KEY.parse.sub(MATURITY_KEY.MATCH, text)
    #if not maturity_k != text:
    #    maturity_k = TRIMMER.parse.sub(TRIMMER.MATCH, maturity_k)
    #    raise click.ClickException(f"'{maturity_k}' should be '{RAW_LABEL.MATURITY}' in maturity row")
    
    # Retrieve the "maturity" data
    S.Step['maturityKeyStart'] = startIndex + len(MATURITY_KEY.parse.sub(MATURITY_KEY.START, text))
    S.Step['maturityKeyEnd'] = startIndex + len(MATURITY_KEY.parse.sub(MATURITY_KEY.END, text))
    content = cells[1].get('content')
    startIndex = content[0]['startIndex']
    text = rse(content)
    if not MATURITY_VAL.parse.search(text):
        maturity = TRIMMER.parse.sub(TRIMMER.MATCH, text)
        warning(f"Unknown maturity: compare\n- {maturity}\n- {STARS}")
        return
    maturity = MATURITY_VAL.parse.sub(MATURITY_VAL.MATCH, text)
    match maturity:
        case STAR.ZERO:
            S.Step['maturity'] = 0
        case STAR.ONE:
            S.Step['maturity'] = 1
        case STAR.TWO:
            S.Step['maturity'] = 2
        case STAR.THREE:
            S.Step['maturity'] = 3
        case _:
            raise click.ClickException(
                f"internal error while parsing Maturity row")
    S.Step['maturityValStart'] = startIndex + len(MATURITY_VAL.parse.sub(MATURITY_VAL.START, text))
    S.Step['maturityValEnd'] = startIndex + len(MATURITY_VAL.parse.sub(MATURITY_VAL.END, text))