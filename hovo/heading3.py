__package__ = 'hovo'

#from hovo.structural import get_text
from hovo.const import KnownH3
from hovo import glob, state
from hovo.structural import rpe, rse

def parse_h3(element):             # This may be a dependency specification

    text = rpe(element.get('paragraph').get('elements')).strip()
    if state.mode == state.ParsingMode.ENGAGED:
        if text == KnownH3.DEPENDS_ON:
            state.mode = state.ParsingMode.DEPENDS_ON
        elif text == KnownH3.UNLOCKS:
            state.mode = state.ParsingMode.UNLOCKS
    elif state.mode == state.ParsingMode.DEPENDS_ON:
        if text == KnownH3.UNLOCKS:
            state.mode = state.ParsingMode.UNLOCKS
        else:
            glob.commit_step()