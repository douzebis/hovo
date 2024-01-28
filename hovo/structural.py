__package__ = 'hovo'

import json
import re

#from hovo.const import Token

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def rse(piece): # read_structural_elements
    """Recurses through a list of Structural Elements to parse a document's
       tables where tables may be in nested elements.

        Args:
            elements: a Structural Element or a list thereof.
    """
    text = ''
    if isinstance(piece, list):
        for element in piece:
            text += rse(element)
    elif 'paragraph' in piece:
        elems = piece.get('paragraph').get('elements')
        for elem in elems:
            text += read_paragraph_element(elem)
    elif 'table' in piece:
        # The text in table cells are in nested Structural Elements and tables may be
        # nested.
        table = piece.get('table')
        for row in table.get('tableRows'):
            cells = row.get('tableCells')
            for cell in cells:
                text += rse(cell.get('content'))
    elif 'tableCells' in piece:
#            print("IN TABLECELLS")
        # The text in table cells are in nested Structural Elements and tables may be
        # nested.
        cells = piece.get('tableCells')
        for cell in cells:
            text += rse(cell.get('content'))
    elif 'tableOfContents' in piece:
        # The text in the TOC is also in a Structural Element.
        toc = piece.get('tableOfContents')
        text += rse(toc.get('content'))
    return text

#def get_text(elements):
#    text = rse(elements)
#    text = re.sub(f"{Token.SPACENL}*$", "", text, 1, flags=re.S)
#    text = re.sub(f"^{Token.SPACENL}*", "", text, 1, flags=re.S)
#    return text
