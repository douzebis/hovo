__package__ = 'hovo'

import json
import re
from difflib import get_close_matches

from fuzzywuzzy import fuzz

from hovo.dot_user import PERSONS_PATH

class Persons:
    with open(PERSONS_PATH, 'r') as json_file:
        directory = []
        for i in json.load(json_file):
            directory.extend([i, {'name': i['email'], 'email': i['email']}])
    names = [entry['name'] for entry in directory]

    @classmethod
    def extract(cls, text_run):
        start_index = text_run['startIndex']
        text = text_run['textRun']['content']

        # Split the text into tokens
        tokens = []
        sis = []
        eis = []
        for match in re.finditer('[^ ,;/\xa0\n\r\t]+', text):
            si = match.start()
            ei = match.end()
            token = text[si:ei]
            tokens.append(token)
            sis.append(start_index + si)
            eis.append(start_index + ei)
        #tokens = re.split('(?: | +. *| *. +|,|;|/)+', text)
    
        verdict = []
        l =  len(tokens)
        a = 0
        for a in range(l):
            found = False
            #print('---')
            curr_match = ''
            curr_conf = 0
            b = a + 1
            while b <= a + 4 and b <= l:
                new_cand = ' '.join(word for word in tokens[a: b] if word)
                new_match = get_close_matches(new_cand, Persons.names, n=1, cutoff=0.9)
                new_conf = 0 if len(new_match) == 0 else fuzz.ratio(new_cand, new_match[0])
                #print('???', new_cand, '->', new_conf)
                if new_conf < curr_conf and curr_conf > 60:
                    #print('***', curr_cand, curr_conf)
                    verdict.append({
                        'start': a,
                        'end': b - 1,
                        'name': curr_match[0],
                        'conf': curr_conf,
                    })
                    a = b - 1
                    break
                if new_conf == 100 or new_conf > 60 and (b == a + 4 or b == l):
                    #print('***', new_cand, new_conf)
                    verdict.append({
                        'start': a,
                        'end': b,
                        'name': new_match[0],
                        'conf': new_conf,
                    })
                    a = b
                    break
                curr_match = new_match
                curr_conf = new_conf
                b += 1
        
        # Use a loop to remove the matching dictionary in-place
        for pos in range(l):
            filtered = [i['conf'] for i in verdict if i['start'] <= pos and i['end'] > pos]
            maximum = 101 if len(filtered) == 0 else max(filtered)
            verdict = [i for i in verdict if i['start'] > pos or i['end'] <= pos or i['conf'] >= maximum]

        orphans = []
        for pos in range(l):
            filtered = [i for i in verdict if i['start'] <= pos and i['end'] > pos]
            if len(filtered) == 0: orphans.append(tokens[pos])

        result = []
        pos = 0
        while pos < l:
            found = next((i for i in verdict if i['start'] <= pos and i['end'] > pos), None)
            if found != None:
                email = next(i['email'] for i in Persons.directory
                             if i['name'] == found['name'])
                name = next(i['name'] for i in Persons.directory
                            if i['email'] == email)
                result.append({
                    'startIndex': sis[found['start']],
                    'endIndex': eis[found['end']-1],
                    'is_person': True,
                    'name': name,
                    'email': email,
                })
                pos = found['end']
            else:
                result.append({
                    'startIndex': sis[pos],
                    'endIndex': eis[pos],
                    'is_person': False,
                    'text': tokens[pos],
                })
                pos += 1
        #print(json.dumps(result, indent=2))
        return result

"""
for text in [
    "Adit Sina Ali Zare, Adeteju Enunwa",
    "Adit Sina Ali, Adeteju Enunwa",
    "Adit Sina Ali, zzz Adeteju Enunwa",
    "Christopher Williamson",
    "René Meulman",
    "Michelle Fernandez Bieber",
    "James Buckland/ Michelle Ferenandez Bieber",
    "Jasmine O'Steen",
    "Ali Zaree, Adeteju Enunwa <aenunwa@google.com>"
]:
    persons = Persons.extract(text)
    print()
    print(text)
    print("    =>", end='')
    started=False
    for i in persons:
        if started:
            print(",", end='')
        else:
            started = True
        if i['is_person']:
            print(f" {i['email']}", end='')
        else:
            print(f" \033[91m{i['orphan']}\033[0m", end='')
    print()
"""
