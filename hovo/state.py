__package__ = 'hovo'

class ParsingMode:
    DISENGAGED = 0
    ENGAGED = 1
    DEPENDS_ON = 2
    UNLOCKS = 3

mode = ParsingMode.DISENGAGED

headingId = ''
bugid0 = None
inter0 = None
title0 = None
bugid = None
inter = None
title = None

stage_key = None
stage_val = None
areas_key = None
areas_val = None
leader_key = None
leader_val = None
s3nsowner_key = None
s3nsowner_val = None
googleowner_key = None
googleowner_val = None
maturity_key = None
maturity_val = None
effort_key = None
effort_val = None
duration_key = None
duration_val = None

depends_on = []
unlocks = []
cmnts = []

def init_step(*,
    bugid0,
    inter0,
    title0,
    bugid,
    inter,
    title,
    headingId,
    cmnts,
    depends_on,
    unlocks,
):
    # This is a trick from https://stackoverflow.com/a/17603590
    def trick(
        _bugid0,
        _inter0,
        _title0,
        _bugid,
        _inter,
        _title,
        _headingId,
        _cmnts,
        _depends_on,
        _unlocks,
    ):
        global bugid0
        global inter0
        global title0
        global bugid
        global inter
        global title
        global headingId
        global cmnts
        global depends_on
        global unlocks
        bugid0 = _bugid0
        inter0 = _inter0
        title0 = _title0
        bugid = _bugid
        inter = _inter
        title = _title
        headingId = _headingId
        cmnts = _cmnts
        depends_on = _depends_on
        unlocks = _unlocks
    trick(
        bugid0,
        inter0,
        title0,
        bugid,
        inter,
        title,
        headingId,
        cmnts,
        depends_on,
        unlocks,
    )

Buganizer = {}
Seen = set()