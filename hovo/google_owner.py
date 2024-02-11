__package__ = 'hovo'

import json
from hovo.colors import Ansi, Rgb
from hovo.const import GoogleOwnerKey
from hovo.const import GoogleOwnerVal
from hovo.persons import Persons
from hovo.row import retrieve_row
from hovo import glob, option
from hovo import state
from hovo.fixer import Fixer
from hovo.warning import warning


def retrieve_google_owner(rows):

    try:
        key, val = retrieve_row(rows, GoogleOwnerKey, GoogleOwnerVal, skip_buganizer=True)
    except StopIteration as e:
        warning(str(e))
        return

    # Provision buganizer imports and cosmetic updates
    url = None if glob.googleownersHeadingId == None \
        else f"#heading={glob.googleownersHeadingId}"
    Fixer.update_style(
        key['start'],
        key['end'],
        font_size=None,
        url=url,
    )
    if key['text'] != key['target']:
        Fixer.replace(
            key['target'],
            key['start'],
            key['end'],
        )

    findees = []
    for element in val['target']:
        if 'paragraph' not in element:
            Ansi.warning(f"expected a paragraph instead of:\n"
                         f"{json.dumps(element, indent=2)}")
            continue
        for elem in element['paragraph']['elements']:
            if 'person' in elem:
                findees.append(elem['person']['personProperties'])
                continue
            elif not 'textRun' in elem:
                Ansi.warning(f"expected a textRun instead of:\n"
                            f"{json.dumps(elem, indent=2)}")
                continue
            elem['replaceWith'] = Persons.extract(elem)
            for item in elem['replaceWith']:
                if item['is_person']:
                    findees.append(item)
                    Fixer.replace(
                        item['name'],
                        item['startIndex'],
                        item['endIndex'],
                        url=f"mailto:{item['email']}",
                    )
                else:
                    Fixer.update_style(
                        item['startIndex'],
                        item['endIndex'],
                        fg_color=Rgb.RED,
                        font_size=None,
                        url=url,
                    )

#    print(json.dumps(state.Buganizer, indent=2))
#    print(f"Findees are {json.dumps(findees)}")  

    b7r_findees = []
    b7r_missing = []
    if option.check_b7r_google_owner or option.import_b7r_google_owner:
        try:
            b7r_value = state.Buganizer[GoogleOwnerVal.NICKNAME]
        except KeyError:
            Ansi.warning(f"Cannot find the step's '{GoogleOwnerVal.NICKNAME}'")
            b7r_value = None
        if b7r_value != None:
            for item in Persons.extract({
                    'startIndex': 0,
                    'textRun': {
                        'content': b7r_value,
                    },
                }):
                if item['is_person']:
                    b7r_findees.append(item)
        for item in b7r_findees:
            n = next((i for i in findees if i['email'] == item['email']), None)
            if n == None:
                b7r_missing.append(item)
    
    if option.check_b7r_google_owner:
        if len(b7r_missing) != 0:
            Ansi.warning(
                f"Missing '{GoogleOwnerVal.NICKNAME}'s from Buganizer:\n"
                f"- {json.dumps([i['email'] for i in b7r_missing])}")
    
    if option.import_b7r_google_owner:
        if len(b7r_missing) != 0:
            Ansi.note(
                f"Adding '{GoogleOwnerVal.NICKNAME}'s from Buganizer:\n"
                f"- {json.dumps([i['email'] for i in b7r_missing])}")
            for item in b7r_missing:
                Fixer.replace(
                    item['name'],
                    val['end'] - 1,
                    val['end'] - 1,
                    url=f"mailto:{item['email']}",
                )
                Fixer.replace(
                    ' ',
                    val['end'] - 1,
                    val['end'] - 1,
                )
        

    state.googleowner_key = key
    state.googleowner_val = val