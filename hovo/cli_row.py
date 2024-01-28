__package__ = 'hovo'

import click
from hovo import glob, option
from hovo.colors import Ansi
from hovo.process import process_hovo

@click.command(
    name='row',
)
@click.option(
    '--remove',
    'remove_row',
    is_flag=True,
    default=False,
    help="""Removes a row from the Step tables""",
)
@click.option(
    '--relabel',
    'relabel_row',
    default=None,
    type=str,
    help="""Relabels a row in the Step tables""",
)
@click.argument(
    'row',
    type=click.IntRange(1, None),
)
def row_cli(
    remove_row,
    relabel_row,
    row,
):
    option.remove_row = remove_row
    option.relabel_row = relabel_row
    option.row = row

    # Check the consistency of provided options
    # (nothing yet)
    row_count = 0
    if remove_row: row_count += 1
    if relabel_row != None: row_count += 1
    if row_count > 1:
        raise click.BadParameter(
            f"Only one of --add-row, --remove-row, "
            f"--relabel_row can be specified")

    if remove_row:
        Ansi.info(f"Removing row {row}...")
        glob.mission = glob.Mission.ROW_MISSION
    elif relabel_row != None:
        Ansi.info(f"Relabeling row {row}: '{relabel_row}'...")
        glob.mission = glob.Mission.ROW_MISSION

    process_hovo()