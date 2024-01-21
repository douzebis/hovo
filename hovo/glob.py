__package__ = 'hovo'

from hovo.const import MODE

class C: # Short for Credentials
    Cookies = ''

class D: # Short for Document
    Docs = None
    Warnings = 0
    StagesHeadingId = None
    AreasHeadingId = None
    LeadersHeadingId = None
    MaturityHeadingId = None
    EffortsHeadingId = None
    Steps = []
    Bugs = []
    Cmnts = []

class S: # Short for State-machine
    Step = {}
    Buganizer = {}
    Seen = set()
    Mode = MODE.DISENGAGED



#class G_NO_LONGER_USED: # Short for Globals
#    Bugs = []
#    Cmnts = []
#    Steps = []
#    Step = {}
#    Seen = set()
#    Mode = MODE.DISENGAGED
#    StagesHeadingId = None
#    AreasHeadingId = None
#    LeadersHeadingId = None
#    MaturityHeadingId = None
#    EffortsHeadingId = None
