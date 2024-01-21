__package__ = 'hovo'

import json

import click

from hovo.const import GDURATION_KEY
from hovo.const import GDURATION_VAL
from hovo.const import RAW_LABEL
from hovo.const import TRIMMER
from hovo.glob import S
from hovo.glob import D
from hovo.options import O
from hovo.structural import rse
from hovo.warning import warning
from hovo.doc import DOC

def retrieve_gduration(rows):
    global S

    gduration_key = {}
    gduration_val = {}

    # Find the stage row
    row = next(
        (r for r in rows
         if GDURATION_KEY.parse.search(rse(r.get('tableCells')[0].get('content')))),
        None)
    # Check the integrity of the gduration row
    if row == None:
        warning(f"Cannot find Google duration row")
        return
    cells = row.get('tableCells')
    if len(cells) != 2:
        warning(f"Google duration row should have exactly two cells: {rse([row])}")
        return
    
    # Locate and record the key for the Google duration estimate
    content = cells[0].get('content')
    gduration_key['start'] = content[0]['startIndex']
    gduration_key['end'] = content[0]['endIndex'] - 1
    gduration_key['text'] = rse(content)

    # Locate and record the value for the Google duration estimate
    content = cells[1].get('content')
    gduration_val['start'] = content[0]['startIndex']
    gduration_val['end'] = content[0]['endIndex'] - 1
    gduration_val['text'] = rse(content)
    if O.import_buganizer:
        gduration_val['target'] = str(float(S.Buganizer['gduration']))
    else:
        try:
            gduration_val['target'] = str(float(gduration_val['text']))
        except:
            gduration_val['target'] = str(0.)
    
    if gduration_val['text'] != gduration_val['target']:
        DOC.replace(
            gduration_val['target'],
            gduration_val['start'],
            gduration_val['end']
        )

    if O.check_buganizer:
        if gduration_val['target'] != S.Buganizer['gduration']:
            warning(
                f"Google duration in Doc and Buganizer do not match: compare\n- {gduration_val['target']}\n- {S.Buganizer['gduration']}")
    
    S.Step['gduration_key'] = gduration_key
    S.Step['gduration_val'] = gduration_val