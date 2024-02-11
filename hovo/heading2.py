__package__ = 'hovo'

import sys

from hovo import glob, option, state
from hovo.buganizer import get_b7r_fields
from hovo.colors import Ansi
from hovo.const import BUGID, TITLE, BugidVal, InterVal, KnownH2, TitleVal
from hovo.structural import rpe, rse


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

        state.init_step(
            bugid0=BugidVal.extract(elems),
            inter0=InterVal.extract(elems),
            title0=TitleVal.extract(elems),
            bugid=None,
            inter=None,
            title=None,
            headingId=headingId,
            cmnts=[],
            depends_on=[],
            unlocks=[],
        )

        # Kill the previous "Parsing..." message if it was uneventful
        # in order to decrease the need for viewer "attention span"
        kill_line = glob.msgs_count == Ansi.msgs_count()
        Ansi.note(f"[{state.bugid0['start']}] "\
                  f"Parsing {state.bugid0['target']} "\
                  f"{state.title0['target']}...",
                  kill_line=kill_line)
        glob.msgs_count = Ansi.msgs_count()
        if option.check_buganizer or option.import_buganizer \
            or option.update_b7r_maturity:
            try:
                state.Buganizer = get_b7r_fields(state.bugid0['value'])
            except Exception as e:
                raise e
            pass

