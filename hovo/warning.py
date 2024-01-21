__package__ = 'hovo'

import click

from hovo.const import ACOL
from hovo.options import O
from hovo.glob import D

def warning(message):
    ACOL.print(message, color=ACOL.BRIGHT_YELLOW)
    if O.stop_on_warning:
        raise click.ClickException("Stopping on warning")
    else:
        D.Warnings += 1