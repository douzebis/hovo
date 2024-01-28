__package__ = 'hovo'

import json
from datetime import datetime

import click
from bs4 import BeautifulSoup
from js2py import EvalJs

from hovo import cookies
from hovo.colors import Ansi
from hovo.googleapi import BUGANIZER_URL
from hovo.warning import warning

#class M: # Short for Magic
#    PRIMARY = 0
#    EXTENDED = 1
#    COMPONENT_ID = 1425125

class B7r:
    # Magic constants
    PRIMARY = 0
    EXTENDED = 1
    COMPONENT_ID = 1425125
    # Buganizer fields of interest
    AREA = {
        'nickname': "areas",
        'b7r_name': "TPC Capability/ Category",
        'type': EXTENDED,
        'code': 1147073,
    }
    ASSIGNEE = {
        'nickname': "assignee",
        'b7r_name': "Assignee",
        'type': PRIMARY,
        'path': [0, 0, 1, 21, 9, 2, 0],
    }
    DURATION = {
        'nickname': "duration",
        'b7r_name': "Duration",
        'type': EXTENDED,
        'code': 1215114,
    }
    GOOGLE_DURATION = {
        'nickname': "gduration",
        'b7r_name': "Google Estimate (Days)",
        'type': EXTENDED,
        'code': 1215505,
    }
    GOOGLE_OWNER = {
        'nickname': "google_owner",
        'b7r_name': "Google Owner",
        'type': EXTENDED,
        'code': 1211695,
    }
    LEADER = {
        'nickname': "leader",
        'b7r_name': "Assignee Company",
        'type': EXTENDED,
        'code': 1148316,
    }
    MATURITY = {
        'nickname': "maturity",
        'b7r_name': "SOW Maturity",
        'type': EXTENDED,
        'code': 1242910,
        'val_to_b7r': lambda x: {0: '0 - Void', 1: '1 - Draft', \
                                 2: '2 - Developing', 3: '3 - Mature'}[x]
    }
    S3NS_OWNER = {
        'nickname': "s3ns_owner",
        'b7r_name': "S3NS Owner",
        'type': EXTENDED,
        'code': 1201498,
    }
    STAGE = {
        'nickname': "stage",
        'b7r_name': "Handoff Stage",
        'type': EXTENDED,
        'code': 1201497,
    }
    TITLE = {
        'nickname': "title",
        'b7r_name': "Title",
        'type': PRIMARY,
        'path': [0, 0, 1, 21, 5],
    }

FIELDS = [getattr(B7r, attr) for attr in dir(B7r) \
          if (not callable(getattr(B7r, attr))
              and not attr.startswith("__")
              and not attr in {'PRIMARY', 'EXTENDED', 'COMPONENT_ID'})]

class B7rCache:
    BUGS_FILE = 'bugs.json'
    bugs = []
    @staticmethod
    def load():
        try:
            with open(B7rCache.BUGS_FILE, 'r') as file:
                # Deserialize the JSON list and assign it to the static field
                B7rCache.bugs = json.load(file)
        except FileNotFoundError:
            pass
    def dump():
        with open(B7rCache.BUGS_FILE, 'w') as file:
            json.dump(B7rCache.bugs, file)

# The commented functions below have teen used to reverse engineer the Buganizer
# format.

#def prints(*args, **kwargs):
#    # Create an in-memory buffer
#    output_buffer = io.StringIO()
#    # Redirect the standard output to the buffer
#    sys.stdout = output_buffer
#    try:
#        # Call the function that performs print statements
#        print(*args, **kwargs)
#        # Get the content of the buffer
#        result = output_buffer.getvalue()
#    finally:
#        # Reset the standard output
#        sys.stdout = sys.__stdout__
#    return result
#
#def LOOKFOR(target, jspb, path):
#    if isinstance(jspb, list):
#        i = 0
#        for item in jspb:
#            LOOKFOR(target, item, path + f"[{i}]")
#            i += 1
#    else:
#        if str(jspb) == str(target):
#            print(f"*** {path}: {jspb}")
#
#def lookfor(target, jspb, path, jspb0):
#    try:
#        if jspb[0] ==  target:
#            print(f"\nDEF {path}:")
#            print(jspb)
#            if jspb[1] != None:
#                LOOKFOR(jspb[1], jspb0, "")
#            return
#    except:
#        pass
#    try:
#        if jspb[4] ==  target:
#            print(f"\nDEC {path}:")
#            print(jspb)
#            if jspb[1] != None:
#                LOOKFOR(jspb[1], jspb0, "")
#            return
#    except:
#        pass
#    if isinstance(jspb, list):
#        i = 0
#        for item in jspb:
#            lookfor(target, item, path + f"[{i}]", jspb0)
#            i += 1
#    else:
#        if str(jspb) == str(target):
#            print(f"{path}: {jspb}")
#    
# for i in {0..50}; do echo -n "$i "; jq ".[0][0][1][5][$i]" titi.html | grep -c '1215506'; done | grep -v ' 0$'
            
def get_value_by_path(tree, path):
    current_node = tree
    try:
        for index in path:
            current_node = current_node[index]
        return current_node
    except (IndexError, TypeError):
        # Handle invalid paths or indices
        return None

def get_b7r_field(jspb, field):
    # Perform some integrity checks
    if jspb[0][0][1][21][0] != B7r.COMPONENT_ID:
        raise click.ClickException(
            f"Buganizer Component ID: expected "\
                f"{B7r.COMPONENT_ID} got {node[13][1]}")

    match field['type']:
        case B7r.PRIMARY:
            return get_value_by_path(jspb, field['path'])
        case B7r.EXTENDED:
            # Fetch property declaration in Buganizer
            node = next((
                n for n in jspb[0][0][1][14] if n[13][0] == field['code']
            ), None)
            if node == None: return None
            # Perform some integrity checks
            if node[13][4] != field['b7r_name']:
                raise click.ClickException(
                    f"Buganizer Code {field['code']}: expected "\
                        f"{field['b7r_name']} got {node[13][4]}")
            # Fetch property value in Buganizer
            node = next((
                n for n in jspb[0][0][1][21][14] if n[0] == field['code']
            ), None)
            if node == None:
                return None
            else:
                return node[9]
        case _:
            raise click.ClickException(f"Internal error in buganizer.py")

#def node_label(bugid):
#    if bugid in state.Seen:
#        return ""
#    state.Seen.add(bugid)
#    node = next((s for s in state.Steps if s['bugid'] == bugid), None)
#    if node == None:
#        return ""
#    node_title = node['title']
#    node_label = f"[\"{bugid}\\n{node_title[:14]}\\n{node_title[14:28]}\\n{node_title[28:42]}\"]"
#    return node_label 

def get_b7r_xsrf_token():
    # Fetch buganizer page
    response = cookies.session.get(
        f"https://partnerissuetracker.corp.google.com/issues")

    # Check if the request to the protected page was successful
    if response.status_code != 200:
        raise click.ClickException(
            f"Error accessing: {response.status_code}")
    
    # Parse the HTML content using BeautifulSoup
    buganizer = BeautifulSoup(response.text, 'html.parser')

    # Find all script tags
    tags = buganizer.find_all('script')
    
    # Find buganizerSessionJspb where the meat is
    # (Evaluate JavaScript code using js2py)
    context = EvalJs({})
    context.execute(tags[2].string)
    jspb = context.buganizerSessionJspb
    return jspb[2]

def set_b7r_field(bugid, nickname, value):
    field = next(f for f in FIELDS if f['nickname'] == nickname)
    newvalue = field['val_to_b7r'](value)
    bug = get_b7r_fields(bugid, force=(cookies.x_xsrf_token == ""))
    Ansi.note(f"Updating B7R maturity: "
                f"'{bug[nickname]}' to '{newvalue}'...")
    if field['type'] != B7r.EXTENDED:
        raise click.ClickException("Cannot only set EXTENDED fields")
    payload = [
      bugid,
      [
        [
          "customField",
          None,
          1,
          None,
          [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            [
              field['code'],
              None,
              None,
              newvalue
            ]
          ]
        ]
      ]
    ]
    url=f"{BUGANIZER_URL}/action/issues/{bugid}"
    headers = {
        'X-XSRF-Token': cookies.x_xsrf_token,
        'Content-Type': 'application/json',
    }
    json_payload = json.dumps(payload)

    # Make the POST request with the JSON payload and X-XSRF-Token
    response = cookies.session.post(url, data=json_payload, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        pass
    else:
        raise click.ClickException(f"{response.status_code}")

def get_b7r_fields(bugid, force=False):
    global FIELDS

    if not force:
        bug = next((b for b in B7rCache.bugs if b['bugid'] == bugid), None)
        if bug != None:
            return bug
    bug = {
        'bugid': bugid,
        'issued_at': int(datetime.utcnow().timestamp()),
    }

    # Fetch buganizer page
    url=f"{BUGANIZER_URL}/issues/{bugid}"
    response = cookies.session.get(url)

    # Check if the request to the protected page was successful
    if response.status_code != 200:
        raise click.ClickException(
            f"Error accessing: {response.status_code}")
    
    # Parse the HTML content using BeautifulSoup
    buganizer = BeautifulSoup(response.text, 'html.parser')

    # Find all script tags
    tags = buganizer.find_all('script')

    # Retrieve the xsrf-token if not already the case
    if cookies.x_xsrf_token == "":
        context = EvalJs({})
        context.execute(tags[2].string)
        jspb = context.buganizerSessionJspb
        cookies.x_xsrf_token = jspb[2]
    
    # Find defrostedResourcesJspb where the meat is
    if False:  # Assuming we know nothing...
        jspb = None
        for tag in tags:
            content = tag.string
            if content:
                # Evaluate JavaScript code using js2py
                context = EvalJs({})
                context.execute(content)
                try:
                    jspb = context.defrostedResourcesJspb
                    break
                except Exception as e:
                    if str(e) != "ReferenceError: "\
                        "defrostedResourcesJspb is not defined":
                        raise e 
                        continue
    else:  # ...but in fact we know where defrostedResourcesJspb resides
        context = EvalJs({})
        context.execute(tags[2].string)
        jspb = context.defrostedResourcesJspb

    if jspb == None:
        warning(f"Cannot find jspb!")
        return None
    
    for prop in FIELDS:
        value = get_b7r_field(jspb, prop)
        bug[prop['nickname']] = value
        #ACOL.print(f"{bugid}: {prop['b7r_name']} == {value}", color=ACOL.GRAY)
    B7rCache.bugs.append(bug)
    # Persist the updated buganizer cache to disk.
    B7rCache.dump()
    return bug