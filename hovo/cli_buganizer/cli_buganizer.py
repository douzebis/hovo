__package__ = 'hovo'

import click

import hovo.cookies as cookies
from hovo.buganizer import get_b7r_xsrf_token


@click.command(
        name='buganizer',
)
@click.option(
    '--get-xsrf-token',
    is_flag=True,
    default=False,
    help="""Prints the x-xrsf-token for the Buganizer session""",
)
def buganizer_cli(
    get_xsrf_token,
):

    cookies.get_cookies()
    print(f"{get_b7r_xsrf_token()}")
    # cookies.x_xsrf_token = get_b7r_xsrf_token()

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