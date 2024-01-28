__package__ = 'hovo'

import json

import click

from hovo.colors import Ansi
from hovo.colors import Rgb
from hovo import glob

def cleanup(docs, doc_id):
    global G

#    updateRequests = [
#        {
#            'insertText': {
#                'location': {
#                    'index': 5,
#                },
#                'text': 'Hello',
#            },
#        },
#        {
#            'insertText': {
#                'location': {
#                    'index': 6 + len('Hello'),
#                },
#                'text': 'HIHI',
#            },
#        },
#    ]
#
#    docs.documents().batchUpdate(
#        documentId=doc_id,
#        body={'requests': updateRequests}
#    ).execute()
#    return

    updateRequests = []

    Ansi.print('Highlighting missing BugIds in the document...', color=Ansi.GRAY)
#    for bug in G.Bugs:
#        updateRequests.append(
#            {
#                'updateTextStyle': {
#                    'range': {
#                        'startIndex': bug['bugidStart'],
#                        'endIndex': bug['bugidEnd']
#                    },
#                    'textStyle': {
#                        'link':  {
#                            'url': f"https://partnerissuetracker.corp.google.com/issues/{bug['bugid']}"
#                        }
#                    },
#                    'fields': 'link'
#                }
#            }
#        )
#        if bug['bugid'] == P.MISSINGBUG:
#            updateRequests.append(
#                {
#                    'updateTextStyle': {
#                        'range': {
#                            'startIndex': bug['bugidStart'],
#                            'endIndex': bug['bugidEnd']
#                        },
#                        'textStyle': {
#                            'foregroundColor': {
#                                'color': {
#                                    'rgbColor': COLOR.RED
#                                }
#                            }
#                        },
#                        'fields': 'foregroundColor'
#                    }
#                }
#            )
#        step = next((step for step in hovo.Steps if step['bugid'] == bug['bugid']), None)
#        if step != None:
#            if (step['title'] != bug['title']
#                and step['bugid'] != P.MISSINGBUG):
#                raise click.ClickException(
#                    f"bug and step titles for Bug ID {bug['bugid']} do not match:\n" +
#                    f"{bug['title']} versus {step['title']}")
#            updateRequests.append(
#                {
#                    'updateTextStyle': {
#                        'range': {
#                            'startIndex': bug['titleStart'],
#                            'endIndex': bug['titleEnd']
#                        },
#                        'textStyle': {
#                            'link':  {
#                                'url': f"https://docs.google.com/document/d/{doc_id}/edit#heading={step['headingId']}"
#                            }
#                        },
#                        'fields': 'link'
#                    }
#                }
#            )

    Ansi.print('Fixing table keys in the document...', color=Ansi.GRAY)
    for step in glob.steps:
        if G.add_row == 'True':
            updateRequests.append(
                {
                    'insertTableRow': {
                        'tableCellLocation': {
                            'tableStartLocation': {
                                'index': step['startIndex'],
                            },
                            'rowIndex': 8,
                            'columnIndex': 1,
                        },
                        'insertBelow': 'true'
                    },
                },
            )
        if G.force_label != '':
            updateRequests.append(
                {
                    'insertText': {
                        'location': {
                            'index': step['forcedStart'] + 1,
                        },
                        'text': G.force_label,
                    },
                },
            )
            if step['forcedStart'] + 1 < step['forcedEnd'] - 1:
                updateRequests.append(
                    {
                        'deleteContentRange': {
                            'range': {
                                'startIndex': step['forcedStart'] + 1,
                                'endIndex': step['forcedEnd'] - 1,
                            },
                        },
                    },
                )
        updateRequests.extend([
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': step['bugidStart'],
                        'endIndex': step['bugidEnd']
                    },
                    'textStyle': {
                        'link':  {
                            'url': f"https://partnerissuetracker.corp.google.com/issues/{step['bugid']}"
                        }
                    },
                    'fields': 'link'
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': step['titleStart'],
                        'endIndex': step['titleEnd']
                    },
                    'textStyle': {
                        'link':  None
                    },
                    'fields': 'link'
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': step['stageKeyStart'],
                        'endIndex': step['stageKeyEnd']
                    },
                    'textStyle': {
                        'link':  {
                            'url': f"https://docs.google.com/document/d/{doc_id}/edit#heading={G.StagesHeadingId}"
                        }
                    },
                    'fields': 'link'
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': step['areaKeyStart'],
                        'endIndex': step['areaKeyEnd']
                    },
                    'textStyle': {
                        'link':  {
                            'url': f"https://docs.google.com/document/d/{doc_id}/edit#heading={G.AreasHeadingId}"
                        }
                    },
                    'fields': 'link'
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': step['leaderKeyStart'],
                        'endIndex': step['leaderKeyEnd']
                    },
                    'textStyle': {
                        'link':  {
                            'url': f"https://docs.google.com/document/d/{doc_id}/edit#heading={G.LeadersHeadingId}"
                        }
                    },
                    'fields': 'link'
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': step['maturityKeyStart'],
                        'endIndex': step['maturityKeyEnd']
                    },
                    'textStyle': {
                        'link':  {
                            'url': f"https://docs.google.com/document/d/{doc_id}/edit#heading={G.MaturityHeadingId}"
                        }
                    },
                    'fields': 'link'
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': step['maturityValStart'],
                        'endIndex': step['maturityValEnd']
                    },
                    'textStyle': {
                        'foregroundColor': {
                            'color': {
                                'rgbColor': Rgb.LIGHTNING_YELLOW
                            }
                        }
                    },
                    'fields': 'foregroundColor'
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': step['effortValStart'],
                        'endIndex': step['effortValEnd']
                    },
                    'textStyle': {
                        'link':  {
                            'url': f"https://docs.google.com/document/d/{doc_id}/edit#heading={G.EffortsHeadingId}"
                        }
                    },
                    'fields': 'link'
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': step['durationValStart'],
                        'endIndex': step['durationValEnd']
                    },
                    'textStyle': {
                        'link':  {
                            'url': f"https://docs.google.com/document/d/{doc_id}/edit#heading={G.EffortsHeadingId}"
                        }
                    },
                    'fields': 'link'
                }
            },
        ])

    #print(updateRequests)
    updateRequests.reverse()
    print(json.dumps(updateRequests, indent=2))
    docs.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': updateRequests}
    ).execute()

    #for step in reversed(hovo.Steps):
    #    print(step['startIndex'])
    #    updateRequests.append([
    #        {
    #            'insertTableRow': {
    #                'tableCellLocation': {
    #                    'tableStartLocation': {
    #                        'index': step['startIndex'],
    #                    },
    #                    'rowIndex': 8,
    #                    'columnIndex': 1,
    #                },
    #                'insertBelow': 'true'
    #            },
    #        },
    #    ])
    #    docs.documents().batchUpdate(
    #        documentId=doc_id,
    #        body={'requests': updateRequests}
    #    ).execute()

