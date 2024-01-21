__package__ = 'hovo'

import json

import click

from hovo.const import EFFORT_KEY
from hovo.const import EFFORT_VAL
from hovo.const import RAW_LABEL
from hovo.const import TRIMMER
from hovo.glob import S
from hovo.structural import rse
from hovo.warning import warning

def retrieve_effort(rows):
    global S

    # Find the stage row
    row = next(
        (r for r in rows
         if EFFORT_KEY.parse.search(rse(r.get('tableCells')[0].get('content')))),
        None)
    # Check the integrity of the effort row
    if row == None:
        warning(f"Cannot find effort row")
        return
    cells = row.get('tableCells')
    if len(cells) != 2:
        warning(f"Effort row should have exactly two cells: {rse([row])}")
        return
    content = cells[0].get('content')
    startIndex = content[0]['startIndex']
    text = rse(content)
    #effort_k = EFFORT_KEY.parse.sub(EFFORT_KEY.MATCH, text)
    #if not effort_k != text:
    #    effort_k = TRIMMER.parse.sub(TRIMMER.MATCH, effort_k)
    #    raise click.ClickException(f"'{effort_k}' should be '{RAW_LABEL.EFFORT}' in effort row")
    
    # Retrieve the "effort" data
    S.Step['effortKeyStart'] = startIndex + len(EFFORT_KEY.parse.sub(EFFORT_KEY.START, text))
    S.Step['effortKeyEnd'] = startIndex + len(EFFORT_KEY.parse.sub(EFFORT_KEY.END, text))
    content = cells[1].get('content')
    text = rse(content)
    effort = TRIMMER.parse.sub(TRIMMER.MATCH, text)
    S.Step['effortValStart'] = startIndex + len(TRIMMER.parse.sub(TRIMMER.START, text))
    S.Step['effortValEnd'] = startIndex + len(TRIMMER.parse.sub(TRIMMER.END, text))
    try:
        S.Step['effort'] = float(effort)
    except:
        S.Step['effort'] = 0.
