__package__ = 'hovo'

import click

from hovo.bugref import bug_register
from hovo.const import MODE
from hovo.const import SPACES
from hovo.const import STEP
from hovo.const import BUGID
from hovo.const import TITLE
from hovo.const import TRIMMER
from hovo.glob import S
from hovo.structural import rse

def parse_depend(element):             # This may be a dependency specification
    global S

    bugid = {}
    title = {}

    text = rse([element])
    if SPACES.parse.search(text):
            return
    trimmed = TRIMMER.parse.sub(TRIMMER.MATCH, text)
    #bugid = STEP.parse.sub(STEP.BUGID, text)
    #bid = BUGID.parse.sub(BUGID.MATCH, STEP.parse.sub(STEP.PART1, text))
    if (not STEP.parse.search(text)  # there was no match: there is no bugid
    #if (not bugid != text # there was no match: there is no bugid
        and trimmed != 'None' and trimmed != 'None.'):
        # there was no match: there should be a bugid
        match S.Mode:
            case MODE.DEPENDS_ON:
                #S.Step['depends_on'].append(bid)  # ???
                raise click.ClickException(
                    f"missing bugid for 'depends on': {text}")
            case MODE.UNLOCKS:
                #S.Step['unlocks'].append(bid)  # ???
                raise click.ClickException(
                    f"missing bugid for 'unlocks': {text}")
            case _:
                raise click.ClickException('internal exception')
    #if bugid != text:
    if STEP.parse.search(text):
        # Locate and record the data for the bugid
        bugid['start'] = element['startIndex']
        bugid['end'] = bugid['start'] + len(STEP.parse.sub(STEP.PART1, text))
        bugid['text'] = STEP.parse.sub(STEP.PART1, text)
        bugid['target'] = BUGID.parse.sub(BUGID.MATCH, bugid['text'])

        # Locate and record the data for the step title
        title['start'] = bugid['end'] + 1
        title['end'] = element['endIndex'] - 1
        title['text'] = STEP.parse.sub(STEP.PART2, text)
        title['target'] = TITLE.parse.sub(TITLE.MATCH, title['text'])

        bug_register(bugid['target'], bugid['start'], bugid['end'],
                     title['target'], title['start'], title['end'])
        match S.Mode:
            case MODE.DEPENDS_ON:
                S.Step['depends_on'].append(bugid)
            case MODE.UNLOCKS:
                S.Step['unlocks'].append(bugid)
            case _:
                raise click.ClickException('internal exception')
