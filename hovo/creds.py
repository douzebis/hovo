__package__ = 'hovo'

import sys

from oauth2client import client, file, tools

from hovo import googleapi

#DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
#DISCOVERY_DRIVE = 'https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

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
        # Stash sys.argv while running the oauth flow
        # (Modules click and oauth2client seem to conflict together)
        reg = sys.argv
        sys.argv = [ reg[0] ]
        credentials = tools.run_flow(flow, store)
        sys.argv = reg
    return credentials
