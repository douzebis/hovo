__package__ = 'hovo'

import copy
import re

import click

from hovo.structural import rbe, rpe, rse

# == WELL-KNOWN HEADERS ========================================================

class KnownH2:
    STAGES = 'Handoff stages'
    AREAS = 'Handoff areas'
    LEADERS = 'Step leaders'
    S3NS_OWNERS = 'S3ns owners'
    GOOGLE_OWNERS = 'Google owners'
    MATURITY = 'SOW maturity'
    EFFORT = 'Efforts and durations'
    DURATION = 'Efforts and durations'

class KnownH3:
    DEPENDS_ON = 'Depends on:'
    UNLOCKS = 'Unlocks:'

#class STEP:
#    REGEX = f'^(({Tok.SPACENL}*{Tok.BUGID}){Tok.SPACENL})({Tok.SPACENL}*.*{Tok.NOSPACE}{Tok.SPACENL}*)\n$'
#    #PART1_START = r'\5'
#    #PART1_END = r'\3'
#    PART1 = r'\2'
#    PART2_START = r'\1'
#    #PART2_END = r'\1'
#    PART2 = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class BUGID:
#    REGEX = f'^(({Tok.SPACENL}*)({Tok.BUGID}))$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class TITLE:
#    REGEX = f'^(({Tok.SPACENL}*)(.*{Tok.NOSPACE})){Tok.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class Trimmer:
#    REGEX = f'^(({Tok.SPACENL}*)(.*{Tok.NOSPACE})){Tok.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    PARSE = re.compile(REGEX, flags=re.S)
#
#    @classmethod
#    def matches(cls, text):
#        return cls.PARSE.search(text)
#    
#    @classmethod
#    def get_match(cls, text):
#        return cls.PARSE.sub(cls.MATCH, text)
#
#class SPACES:
#    REGEX = f'^(()({Tok.SPACENL}*))$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)

# == AUXILIARY TOKENS ==========================================================

SPACE = f'[ \xa0\t]'
LETTER = f'[^ \xa0\t\r\n]'

#class Tok:  # FIXME REMOVE ME
#    MISSINGBUG = '000000000'
#    BUGID = '\d\d\d\d\d\d\d\d\d'
#    SPACE = '[ \xa0\t]'
#    SPACENL = '[ \xa0\n\r\t]'
#    NOSPACE = '[^ \xa0\n\r\t]'
#    NEWLINE = '[\n\r]'

# == PARSING BUGID, INTER, AND TITLE DATA ======================================

BUGID = f'\d\d\d\d\d\d\d\d\d'
INTER = f'{SPACE}+'
TITLE = f'{LETTER}(({SPACE}|{LETTER})*{LETTER}|)'
BUGID_AND_TITLE = \
    f"^"\
    f"(?P<prolog>({SPACE})*)"\
    f"(?P<bugid>{BUGID})"\
    f"(?P<inter>{INTER})"\
    f"(?P<title>{TITLE})"\
    f"(?P<epilog>({SPACE})*)"\
    f"$"

class BugidVal:
    NICKNAME = 'bugid'
    PARSER = re.compile(BUGID_AND_TITLE, flags=re.S)

    @classmethod
    def matches(cls, elems):
        text = elems if isinstance(elems, str) else rbe(elems)[:-1]
        res = cls.PARSER.search(text)
        return res
    
    @classmethod
    def extract(cls, elems):
        #if not isinstance(elems, list):
        #    raise click.ClickException("not a structured element")
        text = elems if isinstance(elems, str) else rbe(elems)[:-1]
        start = 0 if isinstance(elems, str) else elems[0]['startIndex']
        bugid = cls.PARSER.sub(rf"\g<prolog>\g<bugid>", text)
        end = start + len(bugid)
        target = cls.PARSER.sub(rf"\g<bugid>", text)
        value = cls.text_to_val(target)
        return {
            'text': bugid,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text
    
    @classmethod
    def val_to_text(cls, text):
        return text
    
    @classmethod
    def b7r_to_value(cls, text):
        return text

class InterVal:
    NICKNAME = 'inter'
    PARSER = re.compile(BUGID_AND_TITLE, flags=re.S)

    @classmethod
    def matches(cls, elems):
        return cls.PARSER.search(rbe(elems)[:-1])
    
    @classmethod
    def extract(cls, elems):
        text = rbe(elems)[:-1]
        start = elems[0]['startIndex'] \
            + len(cls.PARSER.sub(rf"\g<prolog>\g<bugid>", text))
        inter = cls.PARSER.sub(rf"\g<inter>", text)
        end = start + len(inter)
        target = " "
        value = cls.text_to_val(target)
        return {
            'text': inter,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text
    
    @classmethod
    def val_to_text(cls, text):
        return text


class TitleVal:
    NICKNAME = 'title'
    PARSER = re.compile(BUGID_AND_TITLE, flags=re.S)

    @classmethod
    def matches(cls, elems):
#        print("*** matches: ", elems)
        text = elems if isinstance(elems, str) else rbe(elems)[:-1]
#        if text.startswith("322845751"):
#            pass
        return cls.PARSER.search(text)
    
    @classmethod
    def extract(cls, elems):
#        print("*** extract: ", elems)
        text = elems if isinstance(elems, str) else rbe(elems)[:-1]
        start = 0 if isinstance(elems, str) else elems[0]['startIndex'] \
            + len(cls.PARSER.sub(rf"\g<prolog>\g<bugid>\g<inter>", text))
        title = cls.PARSER.sub(rf"\g<title>\g<epilog>", text)
        end = start + len(title)
        target = cls.PARSER.sub(rf"\g<title>", text)
        value = cls.text_to_val(target)
        return {
            'text': title,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text
    
    @classmethod
    def val_to_text(cls, text):
        return text
    
    @classmethod
    def b7r_to_value(cls, text):
        return text

# ==============================================================================

#class LABEL:
#    STAGE = 'Stage'
#    #AREAS = 'Area'
#    LEADER = 'Leader'
#    S3NSOWNER = 'S3NS owner'
#    GOOGLEOWNER = 'Google co-owners'
#    MATURITY = 'SOW maturity'
#    MATURITY_VAL = '\u2606\u2606\u2606|\u2605\u2606\u2606|\u2605\u2605\u2606|\u2605\u2605\u2605'
#    EFFORT = 'Effort \\(eng days\\)'
#    EFFORT_VAL = '\d+[.]\d*'
#    DURATION = 'Duration \\(cal days\\)'
#    DURATION_VAL = '\d+[.]\d*'
#    GDURATION = 'Google duration'
#    GDURATION_VAL = '\d+[.]\d*'

# == PARSING STAGE DATA ========================================================

class StageKey:
    REGEX = rf'Stage'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        target = cls.PARSER.sub(rf"\g<payload>", text)
        value = cls.text_to_val(target)
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text.strip()
    
    @classmethod
    def val_to_text(cls, text):
        return text
    
class StageVal:
    NICKNAME = 'stage'
    REGEX = rf'Prerequisites|Preparation|Handover|Takeover|Control|Hypercare'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        if cls.matches(content):
            target = cls.PARSER.sub(rf"\g<payload>", text)
            value = cls.text_to_val(target)
        else:
            target = text.strip()
            value = None
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text
    
    @classmethod
    def val_to_text(cls, text):
        return text
    
    @classmethod
    def b7r_to_val(cls, text):
        return text

# == PARSING AREAS DATA ========================================================

class AreasKey:
    REGEX = rf'Areas'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        target = cls.PARSER.sub(rf"\g<payload>", text)
        value = cls.text_to_val(target)
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text.strip()
    
    @classmethod
    def val_to_text(cls, text):
        return text

class AreasVal:
    NICKNAME = 'areas'
    TOKEN = rf'Security|Datacenter|Partner Integrations|Base Networking|'\
            rf'Cloud Networking|Operations|Contracts & Compliance|Testing|'\
            rf'Program Mgt.|GCP Horizontal Services|TPC IaaC'
    REGEX = rf'({TOKEN})(({SPACE})*,({SPACE})*({TOKEN}))*'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        if cls.matches(content):
            target = cls.PARSER.sub(rf"\g<payload>", text)
            value = cls.text_to_val(target)
        else:
            target = text.strip()
            value = None
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        # Split the string into tokens
        tokens = [token.strip() for token in text.split(',')]
        # Remove empty tokens
        tokens = [token for token in tokens if token]
        # Sort the tokens lexicographically
        tokens.sort()
        # Deduplicate the tokens
        unique_tokens = list(set(tokens))
        # Join the tokens with a comma and a space
        result = ', '.join(unique_tokens)
        return result
    
    @classmethod
    def val_to_text(cls, text):
        return text
    
    @classmethod
    def b7r_to_val(cls, text):
        return text

# == PARSING LEADER DATA =======================================================

class LeaderKey:
    REGEX = rf'Leader'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        target = cls.PARSER.sub(rf"\g<payload>", text)
        value = cls.text_to_val(target)
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text.strip()
    
    @classmethod
    def val_to_text(cls, text):
        return text

class LeaderVal:
    NICKNAME = 'leader'
    REGEX = rf'S3NS|Google|Joint'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        if cls.matches(content):
            target = cls.PARSER.sub(rf"\g<payload>", text)
            value = cls.text_to_val(target)
        else:
            target = text.strip()
            value = None
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text
    
    @classmethod
    def val_to_text(cls, text):
        return text
    
    @classmethod
    def b7r_to_val(cls, text):
        return text


# == PARSING S3NS OWNER DATA ===================================================
    
class S3nsOwnerKey:
    REGEX = rf'S3ns owners'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        target = cls.PARSER.sub(rf"\g<payload>", text)
        value = cls.text_to_val(target)
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text.strip()
    
    @classmethod
    def val_to_text(cls, text):
        return text

class S3nsOwnerVal:
    NICKNAME = 's3ns_owner'

    @classmethod
    def matches(cls, content):
        try:
            S3nsOwnerVal.extract(content)
            return True
        except ValueError:
            return False

    @classmethod
    def extract(cls, content):
        try:
            owner = content[0]['paragraph']['elements'][0]\
                    ['person']['personProperties']
        except:
            #raise ValueError("<PERSON>")
            owner = { 'name': None, 'email': None }
        return {
            'text': '',
            'start': content[0]['startIndex'],
            'end': content[0]['startIndex'],
            'target': '',
            'value': owner['name'],
            'name': owner['name'],
            'email': owner['email'],
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text
    
    @classmethod
    def val_to_text(cls, text):
        return text
    
    @classmethod
    def b7r_to_val(cls, text):
        return text

# == PARSING GOOGLE OWNER DATA =================================================

class GoogleOwnerKey:
    REGEX = rf'Google owners'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        target = cls.PARSER.sub(rf"\g<payload>", text)
        value = cls.text_to_val(target)
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text.strip()
    
    @classmethod
    def val_to_text(cls, text):
        return text

class GoogleOwnerVal:
    NICKNAME = 'google_owner'

    @classmethod
    def matches(cls, content):
        try:
            GoogleOwnerVal.extract(content)
            return True
        except ValueError:
            return False

    @classmethod
    def extract(cls, content):
        if len(content) == 0: raise Exception
        start = content[0]['startIndex']
        end = content[-1]['endIndex']
        text = rse(content)
        value = content
        target = copy.deepcopy(content)
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text
    
    @classmethod
    def val_to_text(cls, text):
        return text
    
    @classmethod
    def b7r_to_val(cls, text):
        return text

# == PARSING MATURITY DATA =====================================================

class MaturityKey:
    REGEX = rf'SOW maturity'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        target = cls.PARSER.sub(rf"\g<payload>", text)
        value = cls.text_to_val(target)
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text.strip()
    
    @classmethod
    def val_to_text(cls, text):
        return text

class MaturityVal:
    NICKNAME = 'maturity'
    REGEX = rf'☆☆☆|★☆☆|★★☆|★★★'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        if cls.matches(content):
            target = cls.PARSER.sub(rf"\g<payload>", text)
            value = cls.text_to_val(target)
        else:
            target = text.strip()
            value = None
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        match text:
            case '☆☆☆':
                return 0
            case '★☆☆':
                return 1
            case '★★☆':
                return 2
            case '★★★':
                return 3
            case _:
                return None
    
    @classmethod
    def val_to_text(cls, val):
        match val:
            case None:
                return None
            case 0:
                return '☆☆☆'
            case 1:
                return '★☆☆'
            case 2:
                return '★★☆'
            case 3:
                return '★★★'
            case _:
                raise Exception("Internal error")
    
    @classmethod
    def b7r_to_val(cls, b7r):
        if not isinstance(b7r, int):
            return None
        b7r = int(b7r)
        return b7r if b7r >= 0 and b7r <= 3 else None

# == PARSING EFFORT DATA =======================================================

class EffortKey:
    REGEX = rf'S3ns effort - engineers·days'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        target = cls.PARSER.sub(rf"\g<payload>", text)
        value = cls.text_to_val(target)
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text.strip()
    
    @classmethod
    def val_to_text(cls, text):
        return text
    
class EffortVal:
    NICKNAME = 'effort'
    REGEX = rf'(\d+[.]?\d*|[?]+|TBD)'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        if cls.matches(content):
            target = cls.PARSER.sub(rf"\g<payload>", text)
            try:
                value = float(target)
            except ValueError:
                target = 'TBD'
                value = target
        else:
            target = text.strip()
            value = None
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        try:
            return float(text)
        except ValueError:
            return'TBD'
    
    @classmethod
    def val_to_text(cls, text):
        return str(text)
    
    @classmethod
    def b7r_to_val(cls, text):
        return None

# == PARSING DURATION DATA =======================================================

class DurationKey:
    REGEX = rf'Duration - calendar days'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        target = cls.PARSER.sub(rf"\g<payload>", text)
        value = cls.text_to_val(target)
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        return text.strip()
    
    @classmethod
    def val_to_text(cls, text):
        return text
    
class DurationVal:
    NICKNAME = 'duration'
    REGEX = rf'(\d+[.]?\d*|[?]+|TBD)'
    PARSER = re.compile(
        rf"^(?P<prolog>{SPACE}*)"
        rf"(?P<payload>{REGEX})"
        rf"(?P<epilog>{SPACE}*)$",
        flags=re.S)

    @classmethod
    def matches(cls, content):
        return cls.PARSER.search(rse(content)[:-1])
    
    @classmethod
    def extract(cls, content):
        if not isinstance(content, list):
            raise click.ClickException("Internal error")
        text = rse(content)[:-1]
        start = content[0]['startIndex']
        end = start + len(text)
        if cls.matches(content):
            target = cls.PARSER.sub(rf"\g<payload>", text)
            try:
                value = float(target)
            except ValueError:
                target = 'TBD'
                value = target
        else:
            target = text.strip()
            value = None
        return {
            'text': text,
            'start': start,
            'end': end,
            'target': target,
            'value': value,
        }
    
    @classmethod
    def text_to_val(cls, text):
        try:
            return float(text)
        except ValueError:
            return'TBD'
    
    @classmethod
    def val_to_text(cls, text):
        return str(text)
    
    @classmethod
    def b7r_to_val(cls, text):
        return None

# ------------------------------------------------------------------------------

#class LEADER_KEY:
#    REGEX = f'^(({Token.SPACENL}*)({LABEL.LEADER})){Token.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class S3NSOWNER_KEY:
#    REGEX = f'^(({Token.SPACENL}*)({LABEL.S3NSOWNER})){Token.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class GOOGLEOWNER_KEY:
#    REGEX = f'^(({Token.SPACENL}*)({LABEL.GOOGLEOWNER})){Token.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class MATURITY_KEY:
#    REGEX = f'^(({Token.SPACENL}*)({LABEL.MATURITY})){Token.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class MATURITY_VAL:
#    REGEX = f'^(({Token.SPACENL}*)({LABEL.MATURITY_VAL})){Token.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)

#class EFFORT_KEY:
#    REGEX = f'^(({Tok.SPACENL}*)({LABEL.EFFORT})){Tok.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class EFFORT_VAL:
#    REGEX = f'^(({Tok.SPACENL}*)({LABEL.EFFORT_VAL})){Tok.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class DURATION_KEY:
#    REGEX = f'^(({Tok.SPACENL}*)({LABEL.DURATION})){Tok.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class DURATION_VAL:
#    REGEX = f'^(({Tok.SPACENL}*)({LABEL.DURATION_VAL})){Tok.SPACENL}*$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class GDURATION_KEY:
#    REGEX = f'^(({Tok.SPACENL}*)({LABEL.GDURATION})){Tok.SPACENL}*\n$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)
#
#class GDURATION_VAL:
#    REGEX = f'^(({Tok.SPACENL}*)({LABEL.GDURATION_VAL})){Tok.SPACENL}*\n$'
#    START = r'\2'
#    END = r'\1'
#    MATCH = r'\3'
#    parse = re.compile(REGEX, flags=re.S)

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