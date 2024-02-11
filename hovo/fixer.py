__package__ = 'hovo'

from hovo.colors import Rgb

class Fixer:
    Requests = []

    def reset():
        Fixer.Requests = []

    def get_inplace_requests():
        inplace_requests = [d for d in Fixer.Requests if d['index'] == None]
        deflat = []
        for d in inplace_requests:
            deflat.extend(d['requests'])
        return deflat

    def get_moving_requests():
        sortable_requests = [d for d in Fixer.Requests if d['index'] != None]
        sorted_requests = sorted(
            sortable_requests,
            key=lambda x: x['index'],
            reverse=True)
        deflat = []
        for d in sorted_requests:
            deflat.extend(d['requests'])
        return deflat
    
    def update_style(
        start,
        end,
        fg_color=Rgb.BLACK,
        bg_color={},
        font_size=11,
        url='',
    ):
        text_style = {
            'foregroundColor': {} if fg_color ==  {} else {'color': fg_color},
            'backgroundColor': {} if bg_color ==  {} else {'color': bg_color},
            'fontSize': {'magnitude': font_size, 'unit': 'PT'},
            'link': None if url == '' else {'url': url},
        }
        fields = ''
        if fg_color != None: fields += 'foregroundColor,'
        if bg_color != None: fields += 'backgroundColor,'
        if font_size != None: fields += 'fontSize,'
        if url != None: fields += 'link,'
        Fixer.Requests.append(
            {
                'index': None,
                'requests': [{
                    'updateTextStyle': {
                        'range': {
                            'startIndex': start,
                            'endIndex': end,
                        },
                        'textStyle': text_style,
                        'fields': fields[:-1]
                    }
                }]
            }
        )

    # https://developers.google.com/docs/api/reference/rest/v1/documents/request#request
    def remove_row(row, start):
        Fixer.Requests.append(
            {
                'index': start,
                'requests': [{
                    'deleteTableRow': {
                        'tableCellLocation': {
                            'tableStartLocation': {
                                'index': start
                            },
                            "rowIndex": row,
                        },
                    },
                }]
            }
        )

    # https://developers.google.com/docs/api/reference/rest/v1/documents/request#updatetablecellstylerequest
    def row_style(
        row,
        start,
        bg_color={},
    ):
        style = {
            'backgroundColor': {} if bg_color ==  {} else {'color': bg_color},
        }
        fields = ''
        if bg_color != None: fields += 'backgroundColor,'
        Fixer.Requests.append(
            {
                'index': None,
                'requests': [{
                    'updateTableCellStyle': {
                        'tableCellStyle': style,
                        'fields': fields[:-1],
                        'tableRange': {
                            "tableCellLocation": {
                                "tableStartLocation": {
                                    'index': start,
                                },
                                "rowIndex": row,
                                "columnIndex": 0
                            },
                            "rowSpan": 1,
                            "columnSpan": 2
                        },
                    },
                }]
            }
        )

    def insert(text, start):
        Fixer.Requests.append(
            {
                'index': start,
                'requests': [{
                    'insertText': {
                        'location': {
                            'index': start,
                        },
                        'text': text,
                    },

                }]
            }
        )
    
    # https://developers.google.com/docs/api/how-tos/tables
    def replace(text, start, end, url=None):
        requests = []
        if start < end:
            requests.append(
                {
                    'deleteContentRange': {
                        'range': {
                            'startIndex': start,
                            'endIndex': end,
                        },
                    },
                }
            )
        requests.append(
            {
                'insertText': {
                    'location': {
                        'index': start,
                    },
                    'text': text,
                },
            }
        )
        if url != None:
            requests.append(
                {
                    'updateTextStyle' : {
                        'textStyle': {
                            "link": {
                                "url": url,
                            }
                        },
                        'fields': 'link,',
                        'range': {
                            'startIndex': start,
                            'endIndex': start + len(text)
                        }
                    }
                }
            )
        Fixer.Requests.append(
            {
                'index': start,
                'requests': requests,
            }
        )