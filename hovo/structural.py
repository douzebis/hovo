__package__ = 'hovo'

import json
import re

from hovo.const import P

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def rse(elements): # read_structural_elements
    """Recurses through a list of Structural Elements to parse a document's tables where tables may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for element in elements:
#        print(f"\nIN RSE\n{json.dumps(element, indent=2)}")
        if 'paragraph' in element:
            elems = element.get('paragraph').get('elements')
            for elem in elems:
                text += read_paragraph_element(elem)
        elif 'table' in element:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = element.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += rse(cell.get('content'))
        elif 'tableCells' in element:
#            print("IN TABLECELLS")
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            cells = element.get('tableCells')
            for cell in cells:
                text += rse(cell.get('content'))
        elif 'tableOfContents' in element:
            # The text in the TOC is also in a Structural Element.
            toc = element.get('tableOfContents')
            text += rse(toc.get('content'))
    return text

def get_text(elements):
    text = rse(elements)
    text = re.sub(f"{P.SPACE}*$", "", text, 1, flags=re.S)
    text = re.sub(f"^{P.SPACE}*", "", text, 1, flags=re.S)
    return text
