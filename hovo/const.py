__package__ = 'hovo'

import random
import re

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
DISCOVERY_DRIVE = 'https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'

class HEADING2:
    STAGES = 'Handoff stages'
    AREAS = 'Handoff areas'
    LEADERS = 'Step leaders'
    MATURITY = 'SOW maturity'
    EFFORTS = 'Efforts and durations'

class COLOR:
    def rgb(hex_color):
        return {
            'red':   int(hex_color[1:3], 16)/255.,
            'green': int(hex_color[3:5], 16)/255.,
            'blue':  int(hex_color[5:7], 16)/255.,
        }

    RANDOM = {'red': random.random(), 'green': random.random(), 'blue': random.random()}
    ACID_GREEN = rgb('#8FFE09')
    BLACK = {'red': 0., 'green': 0., 'blue': 0.}
    GOLD = {'red': 241./255., 'green': 194./255., 'blue': 49./255.}
    RED = {'red': 1., 'green': 0., 'blue': 0.}

# ANSI escape codes for text colors
class ACOL:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    @staticmethod
    def print(message, color=RESET, **kwargs):
        print(color + message + ACOL.RESET, **kwargs)


class MODE:
    DISENGAGED = 0
    ENGAGED = 1
    DEPENDS_ON = 2
    UNLOCKS = 3

class HEADING3:
    DEPENDS_ON = 'Depends on:'
    UNLOCKS = 'Unlocks:'

class P: # short for PATTERN
    MISSINGBUG = '000000000'
    BUGID = '\d\d\d\d\d\d\d\d\d'
    SPACE = '[ \xa0\n\r\t]'
    NOSPACE = '[^ \xa0\n\r\t]'
    NEWLINE = '[\n\r]'

class STEP:
    REGEX = f'^(({P.SPACE}*{P.BUGID}){P.SPACE})({P.SPACE}*.*{P.NOSPACE}{P.SPACE}*)\n$'
    #PART1_START = r'\5'
    #PART1_END = r'\3'
    PART1 = r'\2'
    PART2_START = r'\1'
    #PART2_END = r'\1'
    PART2 = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class BUGID:
    REGEX = f'^(({P.SPACE}*)({P.BUGID}))$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class TITLE:
    REGEX = f'^(({P.SPACE}*)(.*{P.NOSPACE})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class TRIMMER:
    REGEX = f'^(({P.SPACE}*)(.*{P.NOSPACE})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class SPACES:
    REGEX = f'^(()({P.SPACE}*))$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class LABEL:
    STAGE = 'Stage'
    AREA = 'Area'
    LEADER = 'Leader'
    S3NSOWNER = 'S3NS owner'
    GOOGLEOWNER = 'Google co-owners'
    MATURITY = 'SOW maturity'
    MATURITY_VAL = '\u2606\u2606\u2606|\u2605\u2606\u2606|\u2605\u2605\u2606|\u2605\u2605\u2605'
    EFFORT = 'Effort \\(eng days\\)'
    EFFORT_VAL = '\d+[.]\d*'
    DURATION = 'Duration \\(cal days\\)'
    DURATION_VAL = '\d+[.]\d*'
    GDURATION = 'Google duration'
    GDURATION_VAL = '\d+[.]\d*'

class STAGE_KEY:
    REGEX = f'^(({P.SPACE}*)({LABEL.STAGE})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class AREA_KEY:
    REGEX = f'^(({P.SPACE}*)({LABEL.AREA})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class LEADER_KEY:
    REGEX = f'^(({P.SPACE}*)({LABEL.LEADER})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class S3NSOWNER_KEY:
    REGEX = f'^(({P.SPACE}*)({LABEL.S3NSOWNER})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class GOOGLEOWNER_KEY:
    REGEX = f'^(({P.SPACE}*)({LABEL.GOOGLEOWNER})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class MATURITY_KEY:
    REGEX = f'^(({P.SPACE}*)({LABEL.MATURITY})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class MATURITY_VAL:
    REGEX = f'^(({P.SPACE}*)({LABEL.MATURITY_VAL})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class EFFORT_KEY:
    REGEX = f'^(({P.SPACE}*)({LABEL.EFFORT})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class EFFORT_VAL:
    REGEX = f'^(({P.SPACE}*)({LABEL.EFFORT_VAL})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class DURATION_KEY:
    REGEX = f'^(({P.SPACE}*)({LABEL.DURATION})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class DURATION_VAL:
    REGEX = f'^(({P.SPACE}*)({LABEL.DURATION_VAL})){P.SPACE}*$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class GDURATION_KEY:
    REGEX = f'^(({P.SPACE}*)({LABEL.GDURATION})){P.SPACE}*\n$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class GDURATION_VAL:
    REGEX = f'^(({P.SPACE}*)({LABEL.GDURATION_VAL})){P.SPACE}*\n$'
    START = r'\2'
    END = r'\1'
    MATCH = r'\3'
    parse = re.compile(REGEX, flags=re.S)

class RAW_LABEL:
    STAGE = 'Stage'
    AREA = 'Area'
    LEADER = 'Leader'
    S3NSOWNER = 'S3NS owner'
    GOOGLEOWNER = 'Google co-owners'
    MATURITY = 'SOW maturity'
    EFFORT = 'Effort (eng days)'
    DURATION = 'Duration (cal days)'
    GDURATION = 'Google duration'

#class LABEL_ROW:
#    STAGE = 1
#    AREA = 2
#    LEADER = 3
#    S3NSOWNER = 4
#    GOOGLEOWNER = 5
#    MATURITY = 6
#    EFFORT = 7
#    DURATION = 8
#    GDURATION = 8

class STAGE:
    PREREQUISITES = 'Prerequisites'
    PREPARATION = 'Preparation'
    HANDOVER = 'Handover'
    TAKEOEVER = 'Takeover'
    CONTROL = 'Control'
    HYPERCARE = 'Hypercare'

STAGES = [
    STAGE.PREREQUISITES,
    STAGE.PREPARATION,
    STAGE.HANDOVER,
    STAGE.TAKEOEVER,
    STAGE.CONTROL,
    STAGE.HYPERCARE
]

class AREA:
    SECURITY = 'Security'
    DATACENTER = 'Datacenter'
    PARTNERINT = 'Partner Integrations'
    BASENET = 'Base Networking'
    CLOUDNET = 'Cloud Networking'
    OPERATIONS = 'Operations'
    CONTRACTS = 'Contracts & Compliance'
    TESTING = 'Testing'
    MANAGEMENT = 'Program Mgt.'
    HORIZONTAL = 'GCP Horizontal Services'
    TPCIAAC = 'TPC IaaC'

AREAS = [
    AREA.SECURITY,
    AREA.DATACENTER,
    AREA.PARTNERINT,
    AREA.BASENET,
    AREA.CLOUDNET,
    AREA.OPERATIONS,
    AREA.CONTRACTS,
    AREA.TESTING,
    AREA.MANAGEMENT,
    AREA.HORIZONTAL,
    AREA.TPCIAAC
]

class LEADER:
    S3NS = 'S3NS'
    GOOGLE = 'Google'
    JOINT = 'Joint'

LEADERS = [
    LEADER.S3NS,
    LEADER.GOOGLE,
    LEADER.JOINT
]

class STAR:
    ZERO = '\u2606\u2606\u2606'
    ONE = '\u2605\u2606\u2606'
    TWO = '\u2605\u2605\u2606'
    THREE = '\u2605\u2605\u2605'

STARS = [
    STAR.ZERO,
    STAR.ONE,
    STAR.TWO,
    STAR.THREE
]