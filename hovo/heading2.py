__package__ = 'hovo'

import sys

from hovo.const import ACOL
from hovo.const import HEADING2
from hovo.const import MODE
from hovo.const import STEP
from hovo.const import BUGID
from hovo.const import TITLE
from hovo.const import TRIMMER
from hovo.options import O
from hovo.glob import S
from hovo.glob import D
from hovo.structural import rse
from hovo.buganizer import get_buganizer

def parse_heading2(element):
    global D

    # This signals the end of a previous step (if any)
    # Let's flush what we have gathered so far
    if S.Step != {}:
        D.Steps.append(S.Step)
    S.Step = {}
    
    # Let's look for well-known sections (definition of stages, etc.)
    try:
        headingId = element['paragraph']['paragraphStyle']['headingId']
    except:
        headingId = ''
    text = rse([element])
    wellknown = TRIMMER.parse.sub(TRIMMER.MATCH, text)
    match wellknown:
        case HEADING2.STAGES:
            ACOL.print(f"{wellknown}'s heading is '{headingId}'", color=ACOL.GRAY, file=sys.stderr)
            D.StagesHeadingId = headingId
        case HEADING2.AREAS:
            ACOL.print(f"{wellknown}'s heading is '{headingId}'", color=ACOL.GRAY, file=sys.stderr)
            D.AreasHeadingId = headingId
        case HEADING2.LEADERS:
            ACOL.print(f"{wellknown}'s heading is '{headingId}'", color=ACOL.GRAY, file=sys.stderr)
            D.LeadersHeadingId = headingId
        case HEADING2.MATURITY:
            ACOL.print(f"{wellknown}'s heading is '{headingId}'", color=ACOL.GRAY, file=sys.stderr)
            D.MaturityHeadingId = headingId
        case HEADING2.EFFORTS:
            ACOL.print(f"{wellknown}'s heading is '{headingId}'", color=ACOL.GRAY, file=sys.stderr)
            D.EffortsHeadingId = headingId

    # Is this maybe a new step description?
    if STEP.parse.search(text):
        bugid = BUGID.parse.sub(BUGID.MATCH, STEP.parse.sub(STEP.PART1, text))
        title = TITLE.parse.sub(BUGID.MATCH, STEP.parse.sub(STEP.PART2, text))
        S.Step['bugid'] = bugid
        S.Step['title'] = title
        S.Step['headingId'] = headingId
        S.Step['cmnts'] = []
        S.Step['depends_on'] = []
        S.Step['unlocks'] = []
        S.Mode = MODE.ENGAGED
        ACOL.print(f"Parsing {S.Step['bugid']} {S.Step['title']}...", color=ACOL.WHITE, file=sys.stderr)
        if O.check_buganizer or O.import_buganizer:
            S.Buganizer = get_buganizer(bugid)
