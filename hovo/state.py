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

Buganizer = {}
Seen = set()