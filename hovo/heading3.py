__package__ = 'hovo'

from hovo.structural import get_text
from hovo.const import HEADING3
from hovo.const import MODE
from hovo.glob import S

def parse_heading3(element):             # This may be a dependency specification
    global S

    text = get_text([element])
    if S.Mode == MODE.ENGAGED:
        if text == HEADING3.DEPENDS_ON:
            S.Mode = MODE.DEPENDS_ON
        elif text == HEADING3.UNLOCKS:
            S.Mode = MODE.UNLOCKS
    elif S.Mode == MODE.DEPENDS_ON:
        if text == HEADING3.UNLOCKS:
            S.Mode = MODE.UNLOCKS
        else:
            S.Mode = MODE.DISENGAGED
    else:
        S.Mode = MODE.DISENGAGED