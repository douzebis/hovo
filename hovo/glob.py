__package__ = 'hovo'

from hovo import state

from enum import Enum

docs_session = None
b7r_session = None
b7r_xsrf_token=""

indicators = ''

class Mission(Enum):
    ROW_MISSION = 1
mission = None

# This is the Google drive zip-export for the HOVO. We retrieve it first:
html = None
# This is the Google drive comments-export for the HOVO. We retrieve it second:
comments = None
# This is raw (curl-retrievable) HTML-version of the HOVO. We retrieve it third:
raw = None
# This is the Google docs version of the HOVO. We retrieve it last:
doc = None
contents = None

warnings = 0
steps = []
dependencies = []
comments = []
msgs_count = 0

areasHeadingId = None
durationHeadingId = None
effortHeadingId = None
googleownersHeadingId = None
leadersHeadingId = None
maturityHeadingId = None
s3nsownersHeadingId = None
stagesHeadingId = None


def commit_step():
    global steps
    
    if state.mode != state.ParsingMode.DISENGAGED:
        steps.append({
            'headingId':  state.headingId,
            'bugid0':     state.bugid0,
            'inter0':     state.inter0,
            'title0':     state.title0,
            'bugid':      state.bugid,
            'inter':      state.inter,
            'title':      state.title,

            'stage_key': state.stage_key,
            'stage_val': state.stage_val,
            'areas_key': state.areas_key,
            'areas_val': state.areas_val,
            'leader_key': state.leader_key,
            'leader_val': state.leader_val,
            's3nsowner_key': state.s3nsowner_key,
            's3nsowner_val': state.s3nsowner_val,
            'googleowner_key': state.googleowner_key,
            'googleowner_val': state.googleowner_val,
            'maturity_key': state.maturity_key,
            'maturity_val': state.maturity_val,
            'effort_key': state.effort_key,
            'effort_val': state.effort_val,
            'duration_key': state.duration_key,
            'duration_val': state.duration_val,

            'depends_on': state.depends_on,
            'unlocks':    state.unlocks,
            'cmnts':      state.cmnts,
        })
        state.headingId = ''
        state.bugid0 = None
        state.inter0 = None
        state.title0 = None
        state.bugid = None
        state.inter = None
        state.title = None

        state.stage_key = None
        state.stage_val = None
        state.areas_key = None
        state.areas_val = None
        state.leader_key = None
        state.leader_val = None
        state.s3nsowner_key = None
        state.s3nsowner_val = None
        state.googleowner_key = None
        state.googleowner_val = None
        state.maturity_key = None
        state.maturity_val = None
        state.maturity_key = None
        state.effort_key = None
        state.effort_val = None
        state.duration_key = None
        state.duration_val = None

        state.depends_on = []
        state.unlocks = []
        state.cmnts = []

        state.mode = state.ParsingMode.DISENGAGED