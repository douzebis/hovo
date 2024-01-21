__package__ = 'hovo'

import json

import click

from hovo.const import DURATION_KEY
from hovo.const import DURATION_VAL
from hovo.const import RAW_LABEL
from hovo.const import TRIMMER
from hovo.glob import S
from hovo.structural import rse
from hovo.warning import warning

def retrieve_duration(rows):
    global S

    # Find the stage row
    row = next(
        (r for r in rows
         if DURATION_KEY.parse.search(rse(r.get('tableCells')[0].get('content')))),
        None)
    # Check the integrity of the duration row
    if row == None:
        warning(f"Cannot find duration row")
        return
    cells = row.get('tableCells')
    if len(cells) != 2:
        warning(f"Duration row should have exactly two cells: {rse([row])}")
        return
    content = cells[0].get('content')
    startIndex = content[0]['startIndex']
    text = rse(content)
    #duration_k = DURATION_KEY.parse.sub(DURATION_KEY.MATCH, text)
    #if not duration_k != text:
    #    duration_k = TRIMMER.parse.sub(TRIMMER.MATCH, duration_k)
    #    raise click.ClickException(f"'{duration_k}' should be '{RAW_LABEL.DURATION}' in duration row")
    
    # Retrieve the "duration" data
    S.Step['durationKeyStart'] = startIndex + len(DURATION_KEY.parse.sub(DURATION_KEY.START, text))
    S.Step['durationKeyEnd'] = startIndex + len(DURATION_KEY.parse.sub(DURATION_KEY.END, text))
    content = cells[1].get('content')
    text = rse(content)
    duration = TRIMMER.parse.sub(TRIMMER.MATCH, text)
    S.Step['durationValStart'] = startIndex + len(TRIMMER.parse.sub(TRIMMER.START, text))
    S.Step['durationValEnd'] = startIndex + len(TRIMMER.parse.sub(TRIMMER.END, text))
    try:
        S.Step['duration'] = float(duration)
    except:
        S.Step['duration'] = 0.