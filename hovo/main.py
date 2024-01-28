__package__ = 'hovo'

import json
import sys

import requests
import click

from hovo import cookies, option
from hovo.buganizer import B7rCache, get_b7r_xsrf_token
from hovo.cli_buganizer.cli_buganizer import buganizer_cli
from hovo.cli_row import row_cli
from hovo.colors import Ansi
from hovo.cookies import get_cookies
from hovo.cli_check import check_cli

# See https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
# for details about shell completion
def complete_doc_id(ctx, param, incomplete):
    return [
        k for k in [
            '1m1NpM7xI-HPQ8eUArkrdEcyhezcG846flTSE2yl5WRk', # api-tests
            '175sF91-CZ3fJ4tlKSiWedHHUcaNlS5ECq-drhRozPsY' # real hovo doc
        ]
        if k.startswith(incomplete)]

@click.group(invoke_without_command=True)
@click.option(
    '--doc-id',
    default='1m1NpM7xI-HPQ8eUArkrdEcyhezcG846flTSE2yl5WRk',
    shell_complete=complete_doc_id,
    help="""
    ID the Google doc to parse, as found at `https://docs.google.com/document/d/ID/edit`
    '1m1NpM7xI-HPQ8eUArkrdEcyhezcG846flTSE2yl5WRk' is the ID for the test doc
    """
)
@click.option(
    '--dry-run',
    is_flag=True,
    default=False,
    help="""
        Do not modify the document or Buganizer
    """,
)
@click.option(
    '--stop-on-warning',
    is_flag=True,
    default=False,
    help="""
        Stop as soon as there is a warning
    """,
)
@click.option(
    '--traces',
    is_flag=True,
    default=False,
    help="""
        Display internal traces
    """,
)
@click.option(
    '--show-xsrf-token',
    is_flag=True,
    default=False,
    help="""
        Display Buganizer session x-xsrf-token
    """,
)
def main_cli(
    doc_id,
    dry_run,
    stop_on_warning,
    traces,
    show_xsrf_token,
):
    get_cookies()
    #cookies.x_xsrf_token = get_b7r_xsrf_token()

#    payload = [
#      307023152,
#      [
#        [
#          "customField",
#          None,
#          1,
#          None,
#          [
#            None,
#            None,
#            None,
#            None,
#            None,
#            None,
#            None,
#            None,
#            None,
#            None,
#            None,
#            None,
#            [
#              1242910,
#              None,
#              None,
#              "0 - Void"
#            ]
#          ]
#        ]
#      ]
#    ]
#    # Create a requests session
#    session = requests.Session()
#
#    # Add cookies to the requests session
#    for cookie in cookies.cookies:
#        session.cookies.set(cookie['name'], cookie['value'])
#
#    json_payload = json.dumps(payload)
#    headers = {
#        'X-XSRF-Token': cookies.x_xsrf_token,
#        'Content-Type': 'application/json',
#    }
#
#    # Make the POST request with the JSON payload and X-XSRF-Token
#    response = session.post(
#        'https://partnerissuetracker.corp.google.com/action/issues/307023152',
#        data=json_payload,
#        headers=headers)
#
#    # Check if the request was successful (status code 200)
#    if response.status_code == 200:
#        print("Successfully accessed the protected URL")
#        print(response.text)
#    else:
#        print(f"Failed to access the protected URL: {response.status_code}")
#
#    sys.exit(0)

    if show_xsrf_token:
        Ansi.print(f"{cookies.x_xsrf_token}")
        return

    # Retrieving buganizer fields is slow. We use a cache at least for
    # testing. Remove the cache file ('bugs.json') if you want to clear
    # the cache.
    B7rCache.load()

    option.doc_id = doc_id
    option.dry_run = dry_run
    option.stop_on_warning = stop_on_warning
    option.traces = traces

main_cli.add_command(check_cli)
main_cli.add_command(buganizer_cli)
main_cli.add_command(row_cli)

"""
googleapiclient.errors.HttpError: <HttpError 403 when requesting https://docs.googleapis.com/v1/documents/175sF91-CZ3fJ4tlKSiWedHHUcaNlS5ECq-drhRozPsY?alt=json returned "Google Docs API has not been used in project 187176146673 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/docs.googleapis.com/overview?project=187176146673 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.". Details: "[{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Google developers console API activation', 'url': 'https://console.developers.google.com/apis/api/docs.googleapis.com/overview?project=187176146673'}]}, {'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'SERVICE_DISABLED', 'domain': 'googleapis.com', 'metadata': {'service': 'docs.googleapis.com', 'consumer': 'projects/187176146673'}}]">

https://developers.google.com/docs/api/quickstart/python?hl=fr
Dans la console Google Cloud, accédez à Menu menu > API et services > Identifiants.
Accéder à "Identifiants"

Cliquez sur Créer des identifiants > ID client OAuth.
Cliquez sur Type d'application > Application de bureau.
Dans le champ Name (Nom), saisissez le nom de l'identifiant. Ce nom ne s'affiche que dans la console Google Cloud.
Cliquez sur Créer. L'écran du client OAuth créé s'affiche, affichant le nouvel ID et le nouveau code secret du client.
Cliquez sur OK. Les identifiants nouvellement créés s'affichent sous ID client OAuth 2.0.
Enregistrez le fichier JSON téléchargé sous le nom credentials.json, puis déplacez-le dans votre répertoire de travail.
"""