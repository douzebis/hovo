__package__ = 'hovo'

import json
import sys

import click

from hovo import glob, option
from hovo.areas import retrieve_areas
from hovo.colors import Ansi, Rgb
from hovo.fixer import Fixer
from hovo.duration import retrieve_duration
from hovo.effort import retrieve_effort
from hovo.google_duration import retrieve_google_duration
from hovo.google_owner import retrieve_google_owner
from hovo.leader import retrieve_leader
from hovo.maturity import retrieve_maturity
from hovo.s3ns_owner import retrieve_s3ns_owner
from hovo.stage import retrieve_stage
from hovo.structural import rse
from hovo.warning import warning
from hovo import state
from hovo.const import BugidVal
from hovo.const import InterVal
from hovo.const import TitleVal
from hovo import googleapi

def parse_table(element):

    #bugid = {}
    #inter = {}
    #title = {}

    # The text in table cells are in nested Structural Elements and tables
    # may be nested.
    table = element.get('table')
    rows = table.get('tableRows')
    # Too many rows indicate that this is not actually a step
    if len(rows) < 9 or len(rows) > 15:return

    row = rows[0]
    cells = row.get('tableCells')
    # Not exactly two cells indicate that this is not actually a step
    if len(cells) != 2:
        return
    
    # Is this maybe our description?
    content = cells[0].get('content')[0]
    #text = rse(content)
    if (not BugidVal.matches(content)
        or not TitleVal.matches(content)):
        return  # Patterns did not match: this is not our step

    # At this point we decide the table is our step template
    state.bugid = BugidVal.extract(content)
    state.inter = InterVal.extract(content)
    state.title = TitleVal.extract(content)
    if state.mode != state.MODE.ENGAGED:
        warning(f"Likely missing heading 2 for step {state.bugid['value']}")

#    bugid['start'] = content[0]['startIndex']
#    bugid['end'] = bugid['start'] + len(STEP.parse.sub(STEP.PART1, text))
#    bugid['text'] = STEP.parse.sub(STEP.PART1, text)
#    if option.import_buganizer:
#        bugid['target'] = state.Buganizer['bugid']
#    else:
#        bugid['target'] = BUGID.parse.sub(BUGID.MATCH, bugid['text'])
#
#    # Locate and record the data for the step title
#    title['start'] = bugid['end'] + 1
#    title['end'] = content[0]['endIndex'] - 1
#    title['text'] = STEP.parse.sub(STEP.PART2, text)
#    if option.import_buganizer:
#        title['target'] = state.Buganizer['title']
#    else:
#        title['target'] = TITLE.parse.sub(TITLE.MATCH, title['text'])

    # Check if step ID is consistent with Heading 2
    if state.bugid['value'] != state.bugid0['value']:
        warning(f"Step 'bugId' values in Table and Heading 2 do not match: "
                f"compare\n"
                f"- {state.bugid['value']}\n"
                f"- {state.bugid0['value']}")
            
    # Check is step Title is consistent with Heading 2
    if state.title['value'] != state.title0['value']:
        warning(f"Step 'title' values in Table and Heading 2 do not match: "
                f"compare\n"
                f"- {state.title['value']}\n"
                f"- {state.title0['value']}")

    if option.check_buganizer:
        if state.bugid['value'] \
            != BugidVal.b7r_to_value(state.Buganizer['bugid']):
            warning(
                f"Step 'bugid' values in Doc and Buganizer do not match: "
                f"compare\n"
                f"- {state.bugid['target']}\n"
                f"- {state.Buganizer['bugid']}")
        if state.title['value'] \
            != TitleVal.b7r_to_value(state.Buganizer['title']):
            warning(
                f"Step 'title' values in Doc and Buganizer do not match: "
                f"compare\n"
                f"- {state.title['target']}\n"
                f"- {state.Buganizer['title']}")

    # Provision buganizer imports and cosmetic updates
            
    Fixer.update_style(
        state.bugid0['start'],
        state.bugid0['end'],
        font_size=None,
        url=f"{googleapi.BUGANIZER_URL}/issues/{state.bugid0['value']}",
    )
    if state.bugid0['text'] != state.bugid0['target']:
        Fixer.replace(
            state.bugid0['target'],
            state.bugid0['start'],
            state.bugid0['end'],
        )
    Fixer.update_style(
        state.inter0['start'],
        state.inter0['end'],
        font_size=16,
        url=f"",
    )
    if state.inter0['text'] != state.inter0['target']:
        Fixer.replace(
            state.inter0['target'],
            state.inter0['start'],
            state.inter0['end'],
        )
    Fixer.update_style(
        state.title0['start'],
        state.title0['end'],
        font_size=16,
    )
    if state.title0['text'] != state.title0['target']:
        Fixer.replace(
            state.title0['target'],
            state.title0['start'],
            state.title0['end'],
        )
    Fixer.update_style(
        state.bugid['start'],
        state.bugid['end'],
        url=f"{googleapi.BUGANIZER_URL}/issues/{state.bugid0['value']}",
    )
    if state.bugid['text'] != state.bugid['target']:
        Fixer.replace(
            state.bugid['target'],
            state.bugid['start'],
            state.bugid['end']
        )
    Fixer.update_style(
        state.inter['start'],
        state.inter['end'],
        url=f"",
    )
    if state.inter['text'] != state.inter['target']:
        Fixer.replace(
            state.inter['target'],
            state.inter['start'],
            state.inter['end'],
        )
    Fixer.update_style(
        state.title['start'],
        state.title['end'],
        #url=f"{googleapi.DOCS_URL}/{option.doc_id}#heading={state.headingId}",
        url=f"#heading={state.headingId}",
    )
    if state.title['text'] != state.title['target']:
        Fixer.replace(
            state.title['target'],
            state.title['start'],
            state.title['end'],
        )
    
    # Are we on a special mission?
    match glob.mission:
        case None:
            pass
        case glob.Mission.ROW_MISSION:
            if option.remove_row:
                Fixer.remove_row(
                    option.row,
                    element['startIndex'],
                )
            elif option.relabel_row != None:
                cell = rows[option.row].get('tableCells')[0]
                Fixer.replace(option.relabel_row, cell['startIndex'] + 1,
                              cell['endIndex'] - 1)
        case _:
            raise click.ClickException(f"unknown mission: {glob.mission}")

    if option.traces:
        Ansi.flash("*** DUMPING DOC.get_inplace_requests()...")
        Ansi.flash(json.dumps(Fixer.get_inplace_requests(), indent=2))
        Ansi.flash("***")
        Ansi.flash("*** DUMPING DOC.get_moving_requests()...")
        Ansi.flash(json.dumps(Fixer.get_moving_requests(), indent=2))
    
    # Retrieve Stage
    retrieve_stage(rows)

    # Retrieve Area
    retrieve_areas(rows)

    # Retrieve Leader
    retrieve_leader(rows)

    # Retrieve S3NS owner
    retrieve_s3ns_owner(rows)

    # Retrieve Google owner
    retrieve_google_owner(rows)

    # Retrieve Maturity
    retrieve_maturity(rows)

    # Retrieve Effort
    retrieve_effort(rows)

    # Retrieve Duration
    retrieve_duration(rows)

    return

    # Retrieve Google Duration
    retrieve_google_duration(rows)

    # Retrieve the startIndex of the first cell of the nine's row
    state.Step['forcedStart'] = rows[9]['tableCells'][0]['startIndex']
    state.Step['forcedEnd'] = rows[9]['tableCells'][0]['endIndex']



    #if (state.Step['leader'] in [ 'S3NS', 'joint']
    #    and state.Step['maturity'] != 3):
    #    state.Step['assignees'] = { state.Step['s3ns_email'] }
    #else:
    #    state.Step['assignees'] = { }