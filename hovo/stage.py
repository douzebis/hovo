__package__ = 'hovo'

import json

import click

from hovo.const import STAGE_KEY
from hovo.const import RAW_LABEL
from hovo.const import STAGES
from hovo.const import TRIMMER
from hovo.glob import S
from hovo.structural import rse
from hovo.warning import warning

def retrieve_stage(rows):
    global S

    # Find the stage row
    row = next(
        (r for r in rows
         if STAGE_KEY.parse.search(rse(r.get('tableCells')[0].get('content')))),
        None)
    # Check the integrity of the stage row
    if row == None:
        warning(f"Cannot find stage row")
        return
    cells = row.get('tableCells')
    if len(cells) != 2:
        warning(f"Stage row should have exactly two cells: {rse([row])}")
        return
    content = cells[0].get('content')
    startIndex = content[0]['startIndex']
    text = rse(content)
    #stage_k = STAGE_KEY.parse.sub(STAGE_KEY.MATCH, text)
    #if not stage_k != text:
    #    stage_k = TRIMMER.parse.sub(TRIMMER.MATCH, stage_k)
    #    raise click.ClickException(f"'{stage_k}' should be '{RAW_LABEL.STAGE}' in stage row")
    
    # Retrieve the stage data
    S.Step['stageKeyStart'] = startIndex + len(STAGE_KEY.parse.sub(STAGE_KEY.START, text))
    S.Step['stageKeyEnd'] = startIndex + len(STAGE_KEY.parse.sub(STAGE_KEY.END, text))
    content = cells[1].get('content')
    text = rse(content)
    stage = TRIMMER.parse.sub(TRIMMER.MATCH, text)
    if stage not in STAGES:
        warning(f"Unknown stage value: compare\n- {stage}'\n- {STAGES}")
    S.Step['stage'] = stage
