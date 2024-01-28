__package__ = 'hovo'

import click

from hovo import glob, googleapi
from hovo.fixer import Fixer

NO_BUG_ID = '000000000'

def register_dependency(bugid, inter, title):
    id = bugid['value']
    ref0 = next((r for r in glob.dependencies
                 if r['bugid']['value'] == id), None)
    if ref0 != None:
        if (title['value'] != ref0['title']['value']
            and id != NO_BUG_ID):
            raise click.ClickException(
                f"Titles for bugid '{id}' do not match: compare\n"
                f"- {title['value']}\n"
                f"- {ref0['title']['value']}")
    glob.dependencies.append(
        {
            'bugid': bugid,
            'title': title,
        })      
    Fixer.update_style(
        bugid['start'],
        bugid['end'],
        font_size=11,
        url=f"{googleapi.BUGANIZER_URL}/issues/{bugid['value']}",
    )
    if bugid['text'] != bugid['target']:
        Fixer.replace(
            bugid['target'],
            bugid['start'],
            bugid['end'],
        )
    Fixer.update_style(
        inter['start'],
        inter['end'],
        url=f"",
    )
    if inter['text'] != inter['target']:
        Fixer.replace(
            inter['target'],
            inter['start'],
            inter['end'],
        )
    if title['text'] != title['target']:
        Fixer.replace(
            title['target'],
            title['start'],
            title['end'],
        )
