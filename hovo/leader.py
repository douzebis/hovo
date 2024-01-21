__package__ = 'hovo'

import json

import click

from hovo.const import LEADER_KEY
from hovo.const import RAW_LABEL
from hovo.const import LEADERS
from hovo.const import TRIMMER
from hovo.glob import S
from hovo.structural import rse
from hovo.warning import warning

def retrieve_leader(rows):
    global S

    # Find the stage row
    row = next(
        (r for r in rows
         if LEADER_KEY.parse.search(rse(r.get('tableCells')[0].get('content')))),
        None)
    # Check the integrity of the "leader" row
    if row == None:
        warning(f"Cannot find leader row")
        return
    cells = row.get('tableCells')
    if len(cells) != 2:
        raise click.ClickException(f"Leader row should have exactly two cells: {rse([row])}")
    content = cells[0].get('content')
    startIndex = content[0]['startIndex']
    text = rse(content)
    #leader_k = LEADER_KEY.parse.sub(LEADER_KEY.MATCH, text)
    #if not leader_k != text:
    #    leader_k = TRIMMER.parse.sub(TRIMMER.MATCH, leader_k)
    #    raise click.ClickException(f"'{leader_k}' should be '{RAW_LABEL.LEADER}' in leader row")
    
    # Retrieve the "leader" data
    S.Step['leaderKeyStart'] = startIndex + len(LEADER_KEY.parse.sub(LEADER_KEY.START, text))
    S.Step['leaderKeyEnd'] = startIndex + len(LEADER_KEY.parse.sub(LEADER_KEY.END, text))
    content = cells[1].get('content')
    text = rse(content)
    leader = TRIMMER.parse.sub(TRIMMER.MATCH, text)
    if leader not in LEADERS:
        warning(f"Unknown leader value: compare\n- {leader}\n- {LEADERS}")
    S.Step['leader'] = leader
