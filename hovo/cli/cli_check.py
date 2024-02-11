__package__ = 'hovo'

import click

from hovo import cookies, option
from hovo.buganizer import B7rCache, get_b7r_xsrf_token
from hovo.cli.cli_buganizer import buganizer_cli
from hovo.cli.cli_row import row_cli
from hovo.cookies import get_cookies
from hovo.process import process_hovo

@click.command(
    name='check',
)
@click.option(
    '--check-b7r-google-owner',
    is_flag=True,
    default=False,
    help="""
        Check Hovo consistency with b7r Google owner field
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
    '--import-b7r-google-owner',
    is_flag=True,
    default=False,
    help="""
        Import some of the Hovo data from Buganizer
    """,
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
    '--resolve-orphan-comments',
    is_flag=True,
    default=False,
    help="""
        Resolve comments that are not accessible from the Google doc
    """,
)
@click.option(
    '--update-b7r-google-owner',
    is_flag=True,
    default=False,
    help="""
        Export some Step fields back to Buganizer:
        - maturity
    """,
)
@click.option(
    '--update-b7r-maturity',
    is_flag=True,
    default=False,
    help="""
        Export some Step fields back to Buganizer:
        - maturity
    """,
)
@click.option(
    '--update-buganizer',
    is_flag=True,
    default=False,
    help="""
        Export some Step fields back to Buganizer:
        - maturity
    """,
)
def check_cli(
    check_b7r_google_owner,
    check_buganizer,
    import_b7r_google_owner,
    import_buganizer,
    resolve_orphan_comments,
    update_b7r_google_owner,
    update_b7r_maturity,
    update_buganizer,
):
    if check_buganizer:
        option.check_buganizer = True
        option.check_b7r_google_owner = True
    else:
        if check_b7r_google_owner:
            option.check_buganizer = True
            option.check_b7r_google_owner = True

    if import_buganizer:
        option.import_buganizer = True
        option.import_b7r_google_owner = True
    else:
        if import_b7r_google_owner:
            option.import_buganizer = True
            option.import_b7r_google_owner = True

    if resolve_orphan_comments:
        option.resolve_orphan_comments = True

    if update_buganizer:
        option.update_buganizer = True
        option.update_b7r_google_owner = True
        option.update_b7r_maturity = True
    else:
        if update_b7r_google_owner:
            option.update_buganizer = True
            option.update_b7r_google_owner = True
        if update_b7r_maturity:
            option.update_buganizer = True
            option.update_b7r_maturity = True
    
    option.load_zip = True
    option.load_comments = True
    option.load_raw = True
    option.load_gdoc = True


    # Check the consistency of provided options
    # (nothing yet)
#    row_count = 0
#    if add_row: row_count += 1
#    if remove_row: row_count += 1
#    if label_row != '': row_count += 1
#    if row_count > 1:
#        raise click.BadParameter(
#            f"Only one of --add-row, --remove-row, label_row can be specified")
#    if row_count > 0 and row == 0:
#        raise click.BadParameter(
#            f"--add-row, --remove-row, label_row require a --row to be specified")
#    if row_count == 0 and row > 0:
#        raise click.BadParameter(
#            f"--row requires one of --add-row, --remove-row, label_row to be specified")
    
    process_hovo()