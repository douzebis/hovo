__package__ = 'hovo'

import sys

from hovo.colors import Ansi
from hovo.const import KnownH2
from hovo.const import BUGID
from hovo.const import TITLE
from hovo import option
from hovo.structural import rpe, rse
from hovo.buganizer import get_b7r_fields
from hovo.const import BugidVal
from hovo.const import InterVal
from hovo.const import TitleVal
from hovo import glob
from hovo import state

def parse_h2(element):
    try:
        headingId = element['paragraph']['paragraphStyle']['headingId']
    except:
        headingId = ''
    elems = element.get('paragraph').get('elements')
    text = rpe(elems)
    if headingId != '':
        # Let's look for well-known sections (definition of stages, etc.)
        wellknown = text.strip()
        match wellknown:
            case KnownH2.STAGES:
                Ansi.info(f"{wellknown}'s heading is '{headingId}'")
                glob.stagesHeadingId = headingId
                return
            case KnownH2.AREAS:
                Ansi.info(f"{wellknown}'s heading is '{headingId}'")
                glob.areasHeadingId = headingId
                return
            case KnownH2.LEADERS:
                Ansi.info(f"{wellknown}'s heading is '{headingId}'")
                glob.leadersHeadingId = headingId
                return
            case KnownH2.S3NS_OWNERS:
                Ansi.info(f"{wellknown}'s heading is '{headingId}'")
                glob.s3nsownersHeadingId = headingId
                return
            case KnownH2.GOOGLE_OWNERS:
                Ansi.info(f"{wellknown}'s heading is '{headingId}'")
                glob.googleownersHeadingId = headingId
                return
            case KnownH2.MATURITY:
                Ansi.info(f"{wellknown}'s heading is '{headingId}'")
                glob.maturityHeadingId = headingId
                return
            case KnownH2.EFFORT:
                Ansi.info(f"{wellknown}'s heading is '{headingId}'")
                glob.effortHeadingId = headingId
                glob.durationHeadingId = headingId
                return

    # Is this maybe a new step description?
    t1 = BugidVal.matches(elems)
    t2 = TitleVal.matches(elems)
    if t1 and t2:
        state.mode = state.ParsingMode.ENGAGED

        state.bugid0 = BugidVal.extract(elems)
        state.inter0 = InterVal.extract(elems)
        state.title0 = TitleVal.extract(elems)
        state.bugid = None
        state.inter = None
        state.title = None
        state.headingId = headingId
        state.cmnts = []
        state.depends_on = []
        state.unlocks = []
    
        Ansi.note(f"[{state.bugid0['start']}] "\
                  f"Parsing {state.bugid0['target']} "\
                  f"{state.title0['target']}...")
        if option.check_buganizer or option.import_buganizer \
            or option.export_maturity:
            state.Buganizer = get_b7r_fields(state.bugid0['value'])
