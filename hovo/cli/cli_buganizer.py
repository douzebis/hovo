__package__ = 'hovo'

import ast
import json
import sys

import js2py
import click
from hovo import dot_google, dot_user, glob
from hovo import buganizer

import hovo.cookies as cookies
from hovo.buganizer import B7rCache, get_b7r_xsrf_token, get_defrosted_resources_jspb, set_b7r_description
from numpy import isin


def show_paths(target, jspb, path):
    if isinstance(jspb, str):
        if target in jspb:
            print(f"FOUND {path} => {jspb}")
    elif isinstance(jspb, int):
        if target == jspb:
            print(f"FOUND {path} => {jspb}")
    elif isinstance(jspb, list):
        i = 0
        for item in jspb:
            show_paths(target, item, path + f"[{i}]")
            i += 1
    elif isinstance(jspb, dict):
        for i in jspb:
            show_paths(target, jspb[i], path + f"['{i}']")
    elif jspb == None:
        return
    else:
        print(f"DEADEND?? {path} => {str(jspb)}")

def get_value_by_path(tree, path):
    current_node = tree
    try:
        for index in path:
            current_node = current_node[index]
        return current_node
    except (IndexError, TypeError):
        # Handle invalid paths or indices
        return None


@click.command(
        name='buganizer',
)
@click.option(
    '--add-comment',
    help="""Add a comment to an Partner Issue Tracker bug"""
)
@click.option(
    '--bugid',
    default='304809981',
    help="""Specifies the Partner Issue Tracker bug id"""
)
@click.option(
    '--get-defrosted-resources',
    is_flag=True,
    default=False,
    help="""Get defrostedResourcesJspb information""",
)
@click.option(
    '--get-prop',
    is_flag=True,
    default=False,
    help="""Get property from Partner Issue Tracker bug""",
)
@click.option(
    '--locate',
    help="""Specifies a string to locate in a Partner Issue Tracker bug"""
)
@click.option(
    '--path',
    help="""Specifies a path in a Partner Issue Tracker bug"""
)
@click.option(
    '--set-prop',
    help="""Set property for Partner Issue Tracker bug"""
)
@click.option(
    '--show-xsrf-token',
    is_flag=True,
    default=False,
    help="""Prints the x-xrsf-token for the Buganizer session""",
)
def buganizer_cli(
    add_comment,
    bugid,
    get_defrosted_resources,
    get_prop,
    locate,
    path,
    set_prop,
    show_xsrf_token,
):
    B7rCache.load()
    #glob.b7r_session = cookies.get_cookies(
    #    dot_user.B7R_COOKIES_PATH, "https://partnerissuetracker.corp.google.com/issues/304809981")
    glob.b7r_session = cookies.get_cookies(
        dot_user.B7R_COOKIES_PATH, dot_google.ISSUETRACKER_URL)
    
    if show_xsrf_token:
        print(f"{get_b7r_xsrf_token()}")
        return
    
    if get_defrosted_resources and bugid != None:
#        def prints(*args, **kwargs):
#            # Create an in-memory buffer
#            output_buffer = io.StringIO()
#            # Redirect the standard output to the buffer
#            sys.stdout = output_buffer
#            try:
#                # Call the function that performs print statements
#                print(*args, **kwargs)
#                # Get the content of the buffer
#                result = output_buffer.getvalue()
#            finally:
#                # Reset the standard output
#                sys.stdout = sys.__stdout__
#            return result
        jspb = get_defrosted_resources_jspb(bugid, force=True)
        jspb = ast.literal_eval(str(jspb))
        #toto = ast.literal_eval(jspb)
        #print(json.dumps(toto, indent=2))
        print(json.dumps(jspb, indent=2))
        return
    
    if locate != None and bugid != None:
        jspb = get_defrosted_resources_jspb(bugid, force=True)
        jspb = ast.literal_eval(str(jspb))
        result = show_paths(locate, jspb, '.')
        return
    
    if get_prop and path != None and bugid != None:
        jspb = get_defrosted_resources_jspb(bugid, force=True)
        jspb = ast.literal_eval(str(jspb))
        match path:
            case 'description':
                extended_path = [0,0,1,15,19,0]
            case 'description2':
                extended_path = [0,0,1,15,19,15,1,0,1]
            case 'description3':
                extended_path = [0,0,5,6,19,0]
            case 'description4':
                extended_path = [0,0,5,6,19,15,1,0,1]
            case _:
                extended_path = json.loads(path)
        print(json.dumps(get_value_by_path(jspb, extended_path)))
        return
    
    if set_prop != None and path != None and bugid != None:
        set_b7r_description(bugid, set_prop)
        return
    
    if add_comment != None and path != None and bugid != None:
        # Payload retrieved from chrome "inspect" tab
        # Look for "Payload", "view source"
        # Convert to python with, e.g.
        # import json
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(json.loads(r'[null,null,null,null,["304809981",["Adding a comment for test, please disregard.",null,null,null,null,null,null,null,2]]]'))
        payload = \
            [   None,
                None,
                None,
                None,
                [   bugid,
                    [   add_comment,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        2]]]
        url=f"{dot_google.ISSUETRACKER_URL}/action/issues/{bugid}/comment"
        headers = {
            'X-XSRF-Token': get_b7r_xsrf_token(),
            'Content-Type': 'application/json',
        }
        json_payload = json.dumps(payload)

        # Make the POST request with the JSON payload and X-XSRF-Token
        response = glob.b7r_session.post(url, data=json_payload, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print(response.text)
        else:
            raise click.ClickException(f"{response.status_code}")
        return




# The following code (commented out) is a test for modifying the 'SOW Maturity'
# of a real buganizer (successful and requires setting the x-xsrf-token).
#    url = 'https://partnerissuetracker.corp.google.com/action/issues/304809707'
#    payload = json.loads('["304809707",[["customField",null,1,null,[null,null,null,null,null,null,null,null,null,null,null,null,[1242910,null,null,"0 - Void"]]]]]')
#    headers = {
#        'Content-Type': "application/json",
#        'X-XSRF-Token': cookies.x_xsrf_token,
#    }
#    # Update the session headers with the defined headers
#    cookies.session.headers.update(headers)
#    
#    response = cookies.session.post(url, json=payload)
#
#    # Check the response
#    if response.status_code == 200:
#        print("POST request successful")
#        print("Response:", response.text)
#    else:
#        print(f"POST request failed with status code {response.status_code}")
#        print("Response:", response.text)