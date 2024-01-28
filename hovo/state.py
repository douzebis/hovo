__package__ = 'hovo'

#from hovo.const import MODE


class MODE:  # FIXME: rename as ParsingMode
    DISENGAGED = 0
    ENGAGED = 1
    DEPENDS_ON = 2
    UNLOCKS = 3

mode = MODE.DISENGAGED

# Values bugid, inter, title are first discovered when hitting a H2.
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


cmnts = []
depends_on = []
unlocks = []
## Then the full step is discovered when hitting the corresponding table.
#step = {}

Buganizer = {}
Seen = set()