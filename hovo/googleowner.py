__package__ = 'hovo'

import json

import click

from hovo.const import GOOGLEOWNER_KEY
from hovo.const import RAW_LABEL
from hovo.const import TRIMMER
from hovo.glob import S
from hovo.structural import rse
from hovo.warning import warning

def retrieve_googleowner(rows):
    global S

    # Find the Google owner row
    row = next(
        (r for r in rows
         if GOOGLEOWNER_KEY.parse.search(rse(r.get('tableCells')[0].get('content')))),
        None)
    # Check the integrity of the Google owner row
    if row == None:
        warning(f"Cannot find Google owner row")
        return
    cells = row.get('tableCells')
    if len(cells) != 2:
        warning(f"Google owner row should have exactly two cells: {rse([row])}")
        return
    content = cells[0].get('content')
    startIndex = content[0]['startIndex']
    text = rse(content)
    #googleowner_k = GOOGLEOWNER_KEY.parse.sub(GOOGLEOWNER_KEY.MATCH, text)
    #if not googleowner_k != text:
    #    googleowner_k = TRIMMER.parse.sub(TRIMMER.MATCH, googleowner_k)
    #    raise click.ClickException(f"'{googleowner_k}' should be '{RAW_LABEL.GOOGLEOWNER}' in googleowner row")

    # Retrieve the "googleowner" data
    try:
        owner = cells[1].get('content')[0]['paragraph']['elements'][0]
    except:
        warning(f"Bad formatting in Google owner row: {rse([row])}")
    try:
        name = owner['person']['personProperties']['name']
    except:
        name = ''
    S.Step['google_owner'] = name