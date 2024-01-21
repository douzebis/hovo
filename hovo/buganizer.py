__package__ = 'hovo'

import inspect
import io
import json
import re
import requests
import sys
import zipfile

import click

from bs4 import BeautifulSoup
from js2py import EvalJs

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from hovo.bugref import bug_register
from hovo.cleanup import cleanup
from hovo.creds import get_credentials
from hovo.depend import parse_depend
from hovo.const import ACOL
from hovo.const import AREA_KEY
from hovo.const import LEADER_KEY
from hovo.const import AREAS
from hovo.const import STAGE_KEY
from hovo.const import COLOR
from hovo.const import DISCOVERY_DOC
from hovo.const import DISCOVERY_DRIVE
from hovo.const import HEADING2
from hovo.const import HEADING3
from hovo.const import LABEL
from hovo.const import LEADERS
from hovo.const import P
from hovo.const import MODE
from hovo.const import RAW_LABEL
from hovo.const import STAGE
from hovo.const import STAGES
from hovo.const import STAR
from hovo.const import STEP
from hovo.const import TRIMMER
from hovo.glob import C
from hovo.glob import D
from hovo.glob import S
from hovo.heading3 import parse_heading3
from hovo.options import O
from hovo.structural import get_text
from hovo.structural import rse
from hovo.cookies import get_cookies
from hovo.table import parse_table
from hovo.warning import warning

def get_value_by_path(tree, path):
    current_node = tree
    try:
        for index in path:
            current_node = current_node[index]
        return current_node
    except (IndexError, TypeError):
        # Handle invalid paths or indices
        return None


class M: # Short for Magic
    PRIMARY = 0
    EXTENDED = 1
    COMPONENT_ID = 1425125

class P:
    AREA = {
        'name': "TPC Capability/ Category",
        'nickname': "area",
        'type': M.EXTENDED,
        'code': 1147073,
    }
    ASSIGNEE = {
        'name': "Assignee",
        'nickname': "assignee",
        'type': M.PRIMARY,
        'path': [0, 0, 1, 21, 9, 2, 0],
    }
    GDURATION = {
        'name': "Google Estimate (Days)",
        'nickname': "gduration",
        'type': M.EXTENDED,
        'code': 1215505,
    }
    MATURITY = {
        'name': "SOW Maturity",
        'nickname': "maturity",
        'type': M.EXTENDED,
        'code': 1242910,
    }
    TITLE = {
        'name': "Title",
        'nickname': "title",
        'type': M.PRIMARY,
        'path': [0, 0, 1, 21, 5],
    }

PROPS = [getattr(P, attr) for attr in dir(P) if not callable(getattr(P, attr)) and not attr.startswith("__")]

    
def prints(*args, **kwargs):
    # Create an in-memory buffer
    output_buffer = io.StringIO()
    # Redirect the standard output to the buffer
    sys.stdout = output_buffer
    try:
        # Call the function that performs print statements
        print(*args, **kwargs)
        # Get the content of the buffer
        result = output_buffer.getvalue()
    finally:
        # Reset the standard output
        sys.stdout = sys.__stdout__
    return result

def LOOKFOR(target, jspb, path):
    if isinstance(jspb, list):
        i = 0
        for item in jspb:
            LOOKFOR(target, item, path + f"[{i}]")
            i += 1
    else:
        if str(jspb) == str(target):
            print(f"*** {path}: {jspb}")

def lookfor(target, jspb, path, jspb0):
    try:
        if jspb[0] ==  target:
            print(f"\nDEF {path}:")
            print(jspb)
            if jspb[1] != None:
                LOOKFOR(jspb[1], jspb0, "")
            return
    except:
        pass
    try:
        if jspb[4] ==  target:
            print(f"\nDEC {path}:")
            print(jspb)
            if jspb[1] != None:
                LOOKFOR(jspb[1], jspb0, "")
            return
    except:
        pass
    if isinstance(jspb, list):
        i = 0
        for item in jspb:
            lookfor(target, item, path + f"[{i}]", jspb0)
            i += 1
    else:
        if str(jspb) == str(target):
            print(f"{path}: {jspb}")
    

# for i in {0..50}; do echo -n "$i "; jq ".[0][0][1][5][$i]" titi.html | grep -c '1215506'; done | grep -v ' 0$'
def get_buganizer_prop(jspb, prop):
    # Perform some integrity checks
    if jspb[0][0][1][21][0] != M.COMPONENT_ID:
        raise click.ClickException(
            f"Buganizer Component ID: expected {M.COMPONENT_ID} got {node[13][1]}")

    match prop['type']:
        case M.PRIMARY:
            return get_value_by_path(jspb, prop['path'])
        case M.EXTENDED:
            # Fetch property declaration in Buganizer
            node = next((
                n for n in jspb[0][0][1][14] if n[13][0] == prop['code']
            ), None)
            if node == None: return None
            # Perform some integrity checks
            if node[13][4] != prop['name']:
                raise click.ClickException(
                    f"Buganizer Code {prop['code']}: expected {prop['name']} got {node[13][4]}")
            # Fetch property value in Buganizer
            node = next((
                n for n in jspb[0][0][1][21][14] if n[0] == prop['code']
            ), None)
            if node == None:
                return None
            else:
                return node[9]
        case _:
            raise click.ClickException(f"Internal error in buganizer.py")

def node_label(bugid):
    if bugid in S.Seen:
        return ""
    S.Seen.add(bugid)
    node = next((s for s in S.Steps if s['bugid'] == bugid), None)
    if node == None:
        return ""
    node_title = node['title']
    node_label = f"[\"{bugid}\\n{node_title[:14]}\\n{node_title[14:28]}\\n{node_title[28:42]}\"]"
    return node_label 

def get_buganizer(bugid):
    global PROPS

    # Fetch buganizer page
    buganizer_response = requests.get(
        f"https://partnerissuetracker.corp.google.com/issues/{bugid}",
        headers={'Cookie': C.Cookies})

    # Check if the request to the protected page was successful
    if buganizer_response.status_code != 200:
        raise click.ClickException(
            f"Error accessing: {buganizer_response.status_code}")
    
    # Parse the HTML content using BeautifulSoup
    buganizer = BeautifulSoup(buganizer_response.text, 'html.parser')

    # Find all script tags
    tags = buganizer.find_all('script')
    
    # Find defrostedResourcesJspb where the meat is
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
                if str(e) != "ReferenceError: defrostedResourcesJspb is not defined":
                  raise e 
                continue
    if jspb == None:
        warning(f"Cannot find jspb!")
        return None

    bug = {
        'bugid': bugid,        
    }
    for prop in PROPS:
        value = get_buganizer_prop(jspb, prop)
        bug[prop['nickname']] = value
        #ACOL.print(f"{bugid}: {prop['name']} == {value}", color=ACOL.GRAY)
    return bug