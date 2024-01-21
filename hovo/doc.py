__package__ = 'hovo'

class DOC:
    Requests = []

    def reset():
        DOC.Requests = []

    def get_inplace_requests():
        inplace_requests = [d for d in DOC.Requests if d['index'] == None]
        deflat = []
        for d in inplace_requests:
            deflat.extend(d['requests'])
        return deflat

    def get_moving_requests():
        sortable_requests = [d for d in DOC.Requests if d['index'] != None]
        sorted_requests = sorted(
            sortable_requests,
            key=lambda x: x['index'],
            reverse=True)
        deflat = []
        for d in sorted_requests:
            deflat.extend(d['requests'])
        return deflat
    
    def color_text(color, start, end):
        DOC.Requests.append(
            {
                'index': None,
                'requests': [{
                    'updateTextStyle': {
                        'range': {
                            'startIndex': start,
                            'endIndex': end,
                        },
                        'textStyle': {
                            'foregroundColor': {
                                'color': {
                                    'rgbColor': color
                                }
                            }
                        },
                        'fields': 'foregroundColor'
                    }
                }]
            }
        )

    def insert(text, start):
        DOC.Requests.append(
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
    
    def replace(text, start, end):
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
        DOC.Requests.append(
            {
                'index': start,
                'requests': requests,
            }
        )