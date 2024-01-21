__package__ = 'hovo'

import json

import click

from hovo.const import S3NSOWNER_KEY
from hovo.const import RAW_LABEL
#from hovo.const import LABEL_ROW
from hovo.const import STAGES
from hovo.const import TRIMMER
from hovo.glob import S
from hovo.structural import rse
from hovo.warning import warning

def retrieve_s3nsowner(rows):
    global S

    # Find the S3NS owner row
    row = next(
        (r for r in rows
         if S3NSOWNER_KEY.parse.search(rse(r.get('tableCells')[0].get('content')))),
        None)
    # Check the integrity of the S3NS owner row
    if row == None:
        warning(f"Cannot find S3NS owner row")
        return
    cells = row.get('tableCells')
    if len(cells) != 2:
        warning(f"S3NS owner row should have exactly two cells: {rse([row])}")
        return
    content = cells[0].get('content')
    startIndex = content[0]['startIndex']
    text = rse(content)
    #s3nsowner_k = S3NSOWNER_KEY.parse.sub(S3NSOWNER_KEY.MATCH, text)
    #if not s3nsowner_k != text:
    #    s3nsowner_k = TRIMMER.parse.sub(TRIMMER.MATCH, s3nsowner_k)
    #    raise click.ClickException(f"'{s3nsowner_k}' should be '{RAW_LABEL.S3NSOWNER}' in S3NS owner row")
    
    # Retrieve the "s3nsowner" data
    try:
        owner = cells[1].get('content')[0]['paragraph']['elements'][0]
    except:
        warning(f"Bad formatting in SENS owner row: {rse([row])}")
        return
    try:
        name = owner['person']['personProperties']['name']
        email = owner['person']['personProperties']['email']
    except:
        if S.Step['leader'] != 'Google':
            warning(f"Missing S3NS owner in SENS owner row: {rse([row])}")
        else:
            name = ''
            email = ''
    S.Step['s3ns_owner'] = name
    S.Step['s3ns_email'] = email