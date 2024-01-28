__package__ = 'hovo'

import click

from hovo import cookies, option
from hovo.buganizer import B7rCache, get_b7r_xsrf_token
from hovo.cli_buganizer.cli_buganizer import buganizer_cli
from hovo.cli_row import row_cli
from hovo.cookies import get_cookies
from hovo.process import process_hovo

@click.command(
    name='check',
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
    '--update-buganizer',
    is_flag=True,
    default=False,
    help="""
        Export some Step fields back to Buganizer:
        - maturity
    """,
)
def check_cli(
    import_buganizer,
    check_buganizer,
    update_buganizer,
):
    option.import_buganizer = import_buganizer
    option.check_buganizer = check_buganizer
    if update_buganizer:
        option.export_maturity = True

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