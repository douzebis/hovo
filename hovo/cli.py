__package__ = 'hovo'

import click

from hovo.process import process
from hovo.options import O


# See https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration
# for details about shell completion
def complete_doc_id(ctx, param, incomplete):
    return [
        k for k in [
            '1m1NpM7xI-HPQ8eUArkrdEcyhezcG846flTSE2yl5WRk', # api-tests
            '175sF91-CZ3fJ4tlKSiWedHHUcaNlS5ECq-drhRozPsY' # real hovo doc
        ]
        if k.startswith(incomplete)]

@click.command()
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
    '--import-buganizer',
    is_flag=True,
    default=False,
    help="""
        Import some of the Hovo data from Buganizer
    """,
)
@click.option(
    '--check-buganizer',
    is_flag=True,
    default=False,
    help="""
        Check the consistency of the Hovo file with Buganizer
    """,
)
@click.option(
    '--row',
    type=click.IntRange(0, None),
    default=0,
    help="""
        Add a row in the Hovo tables
    """,
)
@click.option(
    '--add-row',
    is_flag=True,
    default=False,
    help="""
        Add a row in the Hovo tables, before a give row
    """,
)
@click.option(
    '--remove-row',
    is_flag=True,
    default=False,
    help="""
        Remove a row from the Hovo tables
    """,
)
@click.option(
    '--label-row',
    type=str,
    default='',
    help="""
        Set a new label for a row in the Hovo tables
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
def cli(
    doc_id,
    import_buganizer,
    check_buganizer,
    row,
    add_row,
    remove_row,
    label_row,
    stop_on_warning,
):
    global O

    O.doc_id = doc_id
    O.import_buganizer = import_buganizer
    O.check_buganizer = check_buganizer
    O.add_row = add_row
    O.row = row
    O.add_row = add_row
    O.remove_row = remove_row
    O.label_row = label_row
    O.stop_on_warning = stop_on_warning

    row_count = 0
    if add_row: row_count += 1
    if remove_row: row_count += 1
    if label_row != '': row_count += 1
    if row_count > 1:
        raise click.BadParameter(
            f"Only one of --add-row, --remove-row, label_row can be specified")
    if row_count > 0 and row == 0:
        raise click.BadParameter(
            f"--add-row, --remove-row, label_row require a --row to be specified")
    if row_count == 0 and row > 0:
        raise click.BadParameter(
            f"--row requires one of --add-row, --remove-row, label_row to be specified")
    process()



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