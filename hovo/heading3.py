__package__ = 'hovo'

#from hovo.structural import get_text
from hovo.const import KnownH3
from hovo import state
from hovo.structural import rse

def parse_h3(element):             # This may be a dependency specification

    text = rse([element])
    if state.mode == state.MODE.ENGAGED:
        if text == KnownH3.DEPENDS_ON:
            state.mode = state.MODE.DEPENDS_ON
        elif text == KnownH3.UNLOCKS:
            state.mode = state.MODE.UNLOCKS
    elif state.mode == state.MODE.DEPENDS_ON:
        if text == KnownH3.UNLOCKS:
            state.mode = state.MODE.UNLOCKS
        else:
            state.mode = state.MODE.DISENGAGED
    else:
        state.mode = state.MODE.DISENGAGED