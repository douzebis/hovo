__package__ = 'hovo'

import click

from hovo.const import P
from hovo.glob import D

def bug_register(bugid, bugidStart, bugidEnd,
                 title, titleStart, titleEnd):
    global G
    
    bug = next((bug for bug in D.Bugs if bug['bugid'] == bugid), None)
    if bug != None:
        if (title != bug['title']
            and bugid != P.MISSINGBUG):
            raise click.ClickException(
                f'bug titles for Bug ID {bugid} do not match:\n' +
                f"{title} versus {bug['title']}")
    D.Bugs.append(
        {
            'bugid': bugid,
            'title': title,
            'bugidStart': bugidStart,
            'bugidEnd': bugidEnd,
            'titleStart': titleStart,
            'titleEnd': titleEnd
        }
    )
