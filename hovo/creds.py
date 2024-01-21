__package__ = 'hovo'

import sys

from oauth2client import client, file, tools

from hovo.const import SCOPES

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth 2.0 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    store = file.Storage('token.json')
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        # Stash sys.argv while running the oauth flow (click and oauth2client conflict)
        reg = sys.argv
        sys.argv = [ reg[0] ]
        credentials = tools.run_flow(flow, store)
        sys.argv = reg
    return credentials
