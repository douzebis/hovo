__package__ = 'hovo'

import json
import re

import click

from hovo.area import retrieve_area
from hovo.const import ACOL
from hovo.const import COLOR
#from hovo.const import LABEL_ROW
from hovo.const import MODE
from hovo.const import STEP
from hovo.const import BUGID
from hovo.const import TITLE
from hovo.duration import retrieve_duration
from hovo.gduration import retrieve_gduration
from hovo.effort import retrieve_effort
from hovo.glob import S
from hovo.glob import D
from hovo.options import O
from hovo.googleowner import retrieve_googleowner
from hovo.leader import retrieve_leader
from hovo.maturity import retrieve_maturity
from hovo.s3nsowner import retrieve_s3nsowner
from hovo.stage import retrieve_stage
from hovo.structural import rse
from hovo.warning import warning
from hovo.doc import DOC

def parse_table(element):
    global S

    bugid = {}
    title = {}

    # The text in table cells are in nested Structural Elements and tables may be
    # nested.
    table = element.get('table')
    rows = table.get('tableRows')
    # Too many rows indicate that this is not actually a step
    if len(rows) < 9 or len(rows) > 15:return

    row = rows[0]
    cells = row.get('tableCells')
    # Not exactly two cells indicate that this is not actually a step
    if len(cells) != 2:
        return

    # Locate and record the bugid for the step
    content = cells[0].get('content')
    text = rse(content)
    if not STEP.parse.search(text):
        return  # Pattern did not match: this is not a step

#    content = cells[0].get('content')
#    startIndex = content[0]['startIndex']
#    endIndex = content[0]['endIndex']
#    text = rse(content)
#    bugid = STEP.parse.sub(STEP.BUGID, text)
#    title = STEP.parse.sub(STEP.TITLE, text)
#    if  not bugid != text or not title != text:
#        return  # Pattern did not match: this is not a bugid

    # At this point we decide the table is a step template
    if S.Mode != MODE.ENGAGED:
        warning(f"Likely missing heading 2 for step {bugid}")

    # Locate and record the data for the step bugid
    bugid['start'] = content[0]['startIndex']
    bugid['end'] = bugid['start'] + len(STEP.parse.sub(STEP.PART1, text))
    bugid['text'] = STEP.parse.sub(STEP.PART1, text)
    if O.import_buganizer:
        bugid['target'] = S.Buganizer['bugid']
    else:
        bugid['target'] = BUGID.parse.sub(BUGID.MATCH, bugid['text'])

    # Locate and record the data for the step title
    title['start'] = bugid['end'] + 1
    title['end'] = content[0]['endIndex'] - 1
    title['text'] = STEP.parse.sub(STEP.PART2, text)
    if O.import_buganizer:
        title['target'] = S.Buganizer['title']
    else:
        title['target'] = TITLE.parse.sub(TITLE.MATCH, title['text'])

    # Check if step ID is consistent with Heading 2
    if bugid['target'] != S.Step['bugid']:
        warning(f"Step bugId is different from Heading 2: compare\n- {bugid['target']}\n- {S.Step['bugid']}")
            
    # Check is step Title is consistent with Heading 2
    if title['target'] != S.Step['title']:
        warning(f"Step title is different from Heading 2: compare\n- {title['target']}\n- {S.Step['title']}")

    if O.check_buganizer:
        if bugid['target'] != S.Buganizer['bugid']:
            warning(
                f"Bugid in Doc and Buganizer do not match: compare\n- {bugid['target']}\n- {S.Buganizer['bugid']}")
        if title['target'] != S.Buganizer['title']:
            warning(
                f"Title in Doc and Buganizer do not match: compare\n- {title['target']}\n- {S.Buganizer['title']}")

    DOC.color_text(COLOR.BLACK, title['start'], title['end'])
    if title['text'] != title['target']:
        DOC.replace(
            title['target'],
            title['start'],
            title['end']
        )
    DOC.color_text(COLOR.BLACK, bugid['start'], bugid['end'])
    if bugid['text'] != bugid['target']:
        DOC.replace(
            bugid['target'],
            bugid['start'],
            bugid['end']
        )

    print(json.dumps(DOC.get_inplace_requests(), indent=2))
    print(json.dumps(DOC.get_moving_requests(), indent=2))
    
    S.Step['bugid'] = bugid
    S.Step['title'] = title




    
    
#    # Retrieve Indexes
#    S.Step['startIndex'] = element['startIndex']
#    S.Step['bugidStart'] = startIndex + len(STEP.parse.sub(STEP.BUGID_START, text))
#    S.Step['bugidEnd'] = startIndex + len(STEP.parse.sub(STEP.BUGID_END, text))
#    S.Step['titleStart'] = startIndex + len(STEP.parse.sub(STEP.TITLE_START, text))
#    S.Step['titleEnd'] = startIndex + len(STEP.parse.sub(STEP.TITLE_END, text))

    # Retrieve Stage
    retrieve_stage(rows)

    # Retrieve Area
    retrieve_area(rows)

    # Retrieve Leader
    retrieve_leader(rows)

    # Retrieve S3NS owner
    retrieve_s3nsowner(rows)

    # Retrieve Google owner
    retrieve_googleowner(rows)

    # Retrieve Maturity
    retrieve_maturity(rows)

    # Retrieve Effort
    retrieve_effort(rows)

    # Retrieve Duration
    retrieve_duration(rows)

    # Retrieve Google Duration
    retrieve_gduration(rows)

    # Retrieve the startIndex of the first cell of the nine's row
    S.Step['forcedStart'] = rows[9]['tableCells'][0]['startIndex']
    S.Step['forcedEnd'] = rows[9]['tableCells'][0]['endIndex']



    #if (S.Step['leader'] in [ 'S3NS', 'joint']
    #    and S.Step['maturity'] != 3):
    #    S.Step['assignees'] = { S.Step['s3ns_email'] }
    #else:
    #    S.Step['assignees'] = { }