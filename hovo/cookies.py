__package__ = 'hovo'

import json

from datetime import datetime

import click

from hovo.const import ACOL

def is_cookie_valid(cookie):
    # Extract expiration date from the cookie
    expiration_timestamp = cookie.get("expirationDate", 0)
    # Convert the timestamp to a datetime object
    expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp)
    # Get the current UTC time
    current_datetime = datetime.utcnow()
    # Compare the expiration date with the current date
    return current_datetime < expiration_datetime

def get_cookies():
    """Return valid cookies header for SSO.

    Returns:
        Cookies header, or exception.
    """
    try: 
        with open("cookies.json", 'r') as file:
            content = file.read()
    except Exception as error:
        raise click.ClickException(f"cannot get cookies.json info: {error}")

    cookies = ""
    for cookie in json.loads(content):
        if not is_cookie_valid(cookie):
            if cookie['name'] == "S":
                ACOL.print(
                    f"Warning: cookie 'S' has expired, please refresh your cookies.json",
                    color=ACOL.GRAY)
            else:
                raise click.ClickException(
                    f"Cookie '{cookie['name']}' has expired, please refresh your cookies.json")
        cookies += f"{cookie['name']}={cookie['value']}; "
    return cookies

comment = """

Use extension:
https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
and view Buganizer page:
https://partnerissuetracker.corp.google.com/issues/304809566
__FROM AN INCOGNITO WINDOW__
and export the cookies
__AS JSON_
in
.../hovo/cookies.json
"""