__package__ = 'hovo'

import json

import click

from hovo.const import AREA_KEY
from hovo.const import RAW_LABEL
from hovo.const import AREAS
from hovo.const import TRIMMER
from hovo.glob import S
from hovo.structural import rse
from hovo.warning import warning


def retrieve_area(rows):
    global S

    # Find the stage row
    row = next(
        (r for r in rows
         if AREA_KEY.parse.search(rse(r.get('tableCells')[0].get('content')))),
        None)
    # Check the integrity of the "area" row
    cells = row.get('tableCells')
    if len(cells) != 2:
        warning(f"area row should have exactly two cells: {rse([row])}")
        return
    content = cells[0].get('content')
    startIndex = content[0]['startIndex']
    text = rse(content)
    #area_k = AREA_KEY.parse.sub(AREA_KEY.MATCH, text)
    #if not area_k != text:
    #    area_k = TRIMMER.parse.sub(TRIMMER.MATCH, area_k)
    #    raise click.ClickException(f"'{area_k}' should be '{RAW_LABEL.AREA}' in area row")
    
    # Retrieve the "area" data
    S.Step['areaKeyStart'] = startIndex + len(AREA_KEY.parse.sub(AREA_KEY.START, text))
    S.Step['areaKeyEnd'] = startIndex + len(AREA_KEY.parse.sub(AREA_KEY.END, text))
    content = cells[1].get('content')
    text = rse(content)
    area = TRIMMER.parse.sub(TRIMMER.MATCH, text)
    if area not in AREAS:
        warning(f"Unknown area value: compare\n- {area}'\n- {AREAS}")
    S.Step['area'] = area
