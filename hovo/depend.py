__package__ = 'hovo'

import sys

import click

from hovo import glob
from hovo.bugref import bug_register
from hovo.const import BugidVal
from hovo.const import InterVal
from hovo.const import TitleVal

def parse_depend(element):             # This may be a dependency specification

    bugid = BugidVal.extract(element)
    inter = InterVal.extract(element)
    title = TitleVal.extract(element)
    sys.exit(0)

#    text = rse([element])
#    if SPACES.parse.search(text):
#            return
#    trimmed = Trimmer.PARSE.sub(Trimmer.MATCH, text)
#    #bugid = STEP.parse.sub(STEP.BUGID, text)
#    #bid = BUGID.parse.sub(BUGID.MATCH, STEP.parse.sub(STEP.PART1, text))
#    if (not STEP.parse.search(text)  # there was no match: there is no bugid
#    #if (not bugid != text # there was no match: there is no bugid
#        and trimmed != 'None' and trimmed != 'None.'):
#        # there was no match: there should be a bugid
#        match state.mode:
#            case state.MODE.DEPENDS_ON:
#                #state.Step['depends_on'].append(bid)  # ???
#                raise click.ClickException(
#                    f"missing bugid for 'depends on': {text}")
#            case state.MODE.UNLOCKS:
#                #state.Step['unlocks'].append(bid)  # ???
#                raise click.ClickException(
#                    f"missing bugid for 'unlocks': {text}")
#            case _:
#                raise click.ClickException('internal exception')
#    #if bugid != text:
#    if STEP.parse.search(text):
#        # Locate and record the data for the bugid
#        bugid['start'] = element['startIndex']
#        bugid['end'] = bugid['start'] + len(STEP.parse.sub(STEP.PART1, text))
#        bugid['text'] = STEP.parse.sub(STEP.PART1, text)
#        bugid['target'] = BUGID.parse.sub(BUGID.MATCH, bugid['text'])
#
#        # Locate and record the data for the step title
#        title['start'] = bugid['end'] + 1
#        title['end'] = element['endIndex'] - 1
#        title['text'] = STEP.parse.sub(STEP.PART2, text)
#        title['target'] = TITLE.parse.sub(TITLE.MATCH, title['text'])
#
#        bug_register(bugid['target'], bugid['start'], bugid['end'],
#                     title['target'], title['start'], title['end'])
#        match state.mode:
#            case state.MODE.DEPENDS_ON:
#                state.step['depends_on'].append(bugid)
#            case state.MODE.UNLOCKS:
#                state.step['unlocks'].append(bugid)
#            case _:
#                raise click.ClickException('internal exception')