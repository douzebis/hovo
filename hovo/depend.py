__package__ = 'hovo'

import sys

import click

from hovo import glob, state
from hovo.bugref import register_dependency
from hovo.const import BugidVal
from hovo.const import InterVal
from hovo.const import TitleVal

def parse_depend(elems):             # This may be a dependency specification

# Is this maybe a new step description?
    if BugidVal.matches(elems) and TitleVal.matches(elems):
        bugid = BugidVal.extract(elems)
        inter = InterVal.extract(elems)
        title = TitleVal.extract(elems)

        register_dependency(bugid, inter, title)
        match state.mode:
            case state.ParsingMode.DEPENDS_ON:
                state.depends_on.append(bugid)
            case state.ParsingMode.UNLOCKS:
                state.unlocks.append(bugid)
            case _:
                raise click.ClickException('internal exception')