__package__ = 'hovo'

import click

from hovo.const import Tok
from hovo import glob

def bug_register(bugid, bugidStart, bugidEnd,
                 title, titleStart, titleEnd):
    global G
    
    bug = next((bug for bug in glob.Bugs if bug['bugid'] == bugid), None)
    if bug != None:
        if (title != bug['title']
            and bugid != Tok.MISSINGBUG):
            raise click.ClickException(
                f'bug titles for Bug ID {bugid} do not match:\n' +
                f"{title} versus {bug['title']}")
    glob.Bugs.append(
        {
            'bugid': bugid,
            'title': title,
            'bugidStart': bugidStart,
            'bugidEnd': bugidEnd,
            'titleStart': titleStart,
            'titleEnd': titleEnd
        }
    )
