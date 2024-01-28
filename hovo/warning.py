__package__ = 'hovo'

import click

from hovo import glob
from hovo import option
from hovo.colors import Ansi


def warning(message):
    Ansi.warning(message)
    if option.stop_on_warning:
        raise click.ClickException("Stopping on warning")
    else:
        glob.warnings += 1