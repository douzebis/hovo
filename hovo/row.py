__package__ = 'hovo'

import json
import click

from hovo import option
from hovo.const import GoogleOwnerVal
from hovo.structural import rse
from hovo.warning import warning
from hovo import state

def retrieve_row(rows, key_class, val_class, skip_buganizer=False):
    """
        May raise StopIteration, IndexError
    """
    global S

    # Find the row that corresponds to key_pattern
    try:
        row = next(
            r for r in rows
            if key_class.matches(
                r.get('tableCells')[0].get('content')))
    except StopIteration:
        raise StopIteration(f"Cannot find row '{val_class.NICKNAME}'\n"
                            f"  (Was looking for '{key_class.REGEX}')")
    cells = row.get('tableCells')
    if len(cells) != 2:
        raise IndexError(f"Row '{val_class.NICKNAME}' should have exactly two cells: "
                         f"{rse([row])}")
    
    # Retrieve the row's key and value
    key = key_class.extract(cells[0].get('content'))
    # FIXME: remove this debug statement
    if val_class == GoogleOwnerVal:
        pass
    val = val_class.extract(cells[1].get('content'))
#    content = cells[0].get('content')
#    key['start'] = content[0]['startIndex']
#    key['text'] = rse(content)[:-1]
#    key['end'] = key['start'] + len(key['text'])
#
#    # Locate and record the row value
#    content = cells[1].get('content')
#    val['start'] = content[0]['startIndex']
#    val['text'] = rse(content)[:-1]
#    val['end'] = key['start'] + len(val['text'])
    
#    try:
#        is_match = val_class.matches(val['text'])

    if not skip_buganizer:
        if option.import_buganizer or option.check_buganizer \
            or option.update_b7r_maturity:
            try:
                if val_class.NICKNAME in state.Buganizer:
                    b7r_check = val_class.b7r_to_val(
                        state.Buganizer[val_class.NICKNAME])
                    val['b7r'] = b7r_check
                else:
                    b7r_check = None
            except Exception as e:
                raise click.ClickException(f"Internal error: {e}")

    if not val_class.matches(cells[1].get('content')):
        warning(
            f"Value '{val_class.NICKNAME}' "
            f"does not match template: compare\n"
            f"- {val['text'].strip()}\n"
            f"- {val_class.REGEX}")

    if not skip_buganizer:
        if (option.import_buganizer
            and b7r_check != None and val['value'] != b7r_check):
            val['target'] = val_class.val_to_text(b7r_check)
            val['value'] = b7r_check

        if (option.check_buganizer
            and b7r_check != None and val['value'] != b7r_check):
                warning(f"Values of '{val_class.NICKNAME}' in Doc and "
                        f"Buganizer do not match: compare\n"
                        f"- {val['target']}\n"
                        f"- {val_class.val_to_text(b7r_check)}")
            
    return key, val