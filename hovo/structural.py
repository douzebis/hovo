__package__ = 'hovo'

import json
import re

import click

#from hovo.const import Token

def rpe(elems):  # read_paragraph_elements
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text = ''
    for elem in elems:
        if 'textRun' in elem:
            text += elem['textRun']['content']
        elif 'pageBreak' in elem:
            text += '\n' * (elem['endIndex'] - elem['startIndex'])
        elif 'footnoteReference' in elem:
            text += ' ' * (elem['endIndex'] - elem['startIndex'])
        elif 'richLink' in elem:
            text += ' ' * (elem['endIndex'] - elem['startIndex'])
        elif 'inlineObjectElement' in elem:
            text += ' ' * (elem['endIndex'] - elem['startIndex'])
        elif 'person' in elem:
            text += ' ' * (elem['endIndex'] - elem['startIndex'])
        else:
            raise click.ClickException("Internal error")
    return text

def rse(elements):  # read_structural_elements
    """Recurses through a list of Structural Elements to parse a document's
       tables where tables may be in nested elements.

        Args:
            elements: a Structural Element or a list thereof.
    """
    text = ''
    if not isinstance(elements, list):
        raise click.ClickException("not a structured element")
    for element in elements:
        #text += rse(element)
        if 'paragraph' in element:
            elems = element.get('paragraph').get('elements')
            text += rpe(elems)
        elif 'table' in element:
            # The text in table cells are in nested Structural Elements and
            # tables may be nested.
            table = element.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += rse(cell.get('content'))
        elif 'tableOfContents' in element:
            # The text in the TOC is also in a Structural Element.
            toc = element.get('tableOfContents')
            text += rse(toc.get('content'))
    return text

def rbe(es):  # behave as either rse or rpe
    e = es[0]
    if ('paragraph' in e
        or 'table' in e
        or 'tableOfContents' in e):
        return rse(es)
    else:
        return rpe(es)
