__package__ = 'hovo'

import json
import re
import sys
import textwrap
from datetime import datetime
from venv import create

from tzlocal import get_localzone

import click
from bs4 import BeautifulSoup
from flask import cli

from hovo import dot_google, glob, option
from hovo.colors import Ansi
from hovo.const import BugidVal, TitleVal
from hovo.persons import Persons


def name_to_person(txt):
    gotcha = Persons.extract({
        'startIndex': 0,
        'textRun': {
            'content': txt,
        },
    })
    if len(gotcha) != 1 or not gotcha[0]['is_person']:
        Ansi.warning(f"Cannot idendify person '{txt}'")
        return txt
    else:
        return gotcha[0]

def get_comments():
    text = textwrap.dedent("""
        ## HOVO assignees
          
        ### Assignees status
    """)
    # Our sources of information regarding comments include:
    # - glob.html => HTML
    # - glob.comments => json
    # - glob.raw => HTML
    # - glob.doc => HTML

    # -- Retrieve comments assignee information from `glob.html` ---------------
    comments_html = []
    comments_count = 0
    ep = 0

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(glob.html, 'html.parser')
    # Find all tags with id matching the pattern 'cmnt\d*'
    target_tags = soup.find_all(
        lambda tag: (
            tag.name == 'h2'
            or tag.has_attr('id') and tag['id'].startswith('cmnt')))
    current_comments = []
    orphan_comments = []
#    step = None
    step_id = None
    for tag in target_tags:
        if tag.name == 'h2':
            # New heading 2, this might be a step specification
            if not BugidVal.matches(tag.text) or not TitleVal.matches(tag.text):
                step_id = None
#                step = None
            else:
                step_id = BugidVal.extract(tag.text)['value']
                # The following statement is really an assert
                next(step for step in glob.steps
                     if step['bugid']['value'] == step_id)
            continue
        elif tag.name == 'a':
            # This might be about a comment
            if not tag.has_attr('id'):
                continue
            elif re.search('^cmnt_ref(\d*)$', tag['id']):
                c_ref = re.sub('^cmnt_ref(\d*)$', r'\1', tag['id'])
                parent_sup = tag.find_parent('sup')
                if not parent_sup:
                    raise Exception("Internal error")
                sp = parent_sup.sourcepos
                if sp != ep:
                    comments_count += 1
#                    is_reply = False
                else:
                    # FIXME: Could be 'is_reply = True'
                    pass
#                    is_reply = False
                ep = sp + len(str(parent_sup))
                #print(f"\n*** REFERENCE {tag.text}")
                #print(f"sourceline: {parent_sup.sourceline}")
                #print(f"sourcepos: {parent_sup.sourcepos}")
                #print(f"endpos: {parent_sup.sourcepos + len(str(parent_sup))}")
                comments_html.append({
                    'ref': c_ref,
                    'tag': tag.text,
                    'serial': comments_count,
                    'sp': parent_sup.sourcepos,
                    'ep': parent_sup.sourcepos + len(str(parent_sup)),
                    # FIXME
                    'is_reply': False,
                    #'is_reply': is_reply,
                    'stepId': step_id,
#                    'step': step
                    'assignee': None,
                })
                continue
            elif re.search('^cmnt(\d*)$', tag['id']):
                c_ref = re.sub('^cmnt(\d*)$', r'\1', tag['id'])
                comment = next(c for c in comments_html if c['ref'] == c_ref)
                parent_div = tag.find_parent('div')
                #print(parent_div.prettify())
                if not parent_div:
                    raise Exception("Internal error")
                #print("\n*** COMMENT SUBSTANCE")
                #print(f"sourceline: {parent_div.sourceline}")
                #print(f"sourcepos: {parent_div.sourcepos}")
                #print(parent_div.prettify())
                # Find all <p> tags within the <div>
                p_tags = parent_div.select('div p')
                p_count = len(p_tags)
                if p_count > 1:
                    pass
                if p_count == 0:
                    raise Exception("Internal error")
                content = ""
                for i in range(p_count):
                    p_spans = p_tags[i]('span')
                    if i == p_count - 1 and len(p_spans) == 1:
                        pragma = p_spans[0].text
                        assignee = re.sub(
                            r'^_(Assigned|Reassigned) to ([^ ]*)_$',
                            r'\2', p_tags[i].text)
                        if assignee != p_tags[i].text:
                            comment['assignee'] = name_to_person(assignee)
                            break
                        if re.search(r'^_Marked as done_$', pragma): break
                        if re.search(r'^_Re-opened_$', pragma): break
                    if i != 0:
                        content += "\n"
                    for s in p_spans:
                        content += s.text
                comment['content'] = re.sub('\xa0', ' ', content)
                # FIXME Remove this debug statement
                # 'PTAL @tony.cerqueira@s3ns.io & @mickael.roger@s3ns.io as this is dependent on the networking layer working OK. And the capability for TUP to reach our IDP.'
                continue
    
    comments_assigned = []
    prev_comment = None
    for comment in comments_html:
        if comment['is_reply']:
            prev_comment['replies'].append(comment)
        else:
            if prev_comment != None:
                comments_assigned.append(prev_comment)
            prev_comment = comment
            prev_comment['replies'] = []
    if prev_comment != None:
        comments_assigned.append(prev_comment)
    comments_assigned = [c for c in comments_assigned if c['assignee'] != None]


#    print('\n*** glob.html')
#    print(json.dumps(comments_assigned, indent=2))

    # -- Retrieve reference comments information from `glob.comments` ----------

    comments_aux = []
    for c in glob.comments:
        if c['kind'] == "drive#comment" and not c['deleted']:
            # FIXME: why do resolved comment stay visible in the doc?
            # What does it mean for a comment to be resolved??
            if 'resolved' in c and c['resolved']:
                continue
            comment = {
                'id': c['id'],
                'anchor': c['anchor'],
                'serial': 0,
                'createdTime': c['createdTime'],
                'modifiedTime': c['modifiedTime'],
                'author': name_to_person(c['author']['displayName']),
                'quotedFileContent': c['quotedFileContent']['value'] \
                    if 'quotedFileContent' in c else "",
                'content': re.sub('\xa0', ' ', c['content']),
                'assignee': None,
                'isOff': False,
                'replies': [],
            }
            for r in c['replies']:
                if r['deleted']:
                    continue
                comment['replies'].append({
                    'id': r['id'],
                    'createdTime': r['createdTime'],
                    'modifiedTime': r['modifiedTime'],
                    'author': name_to_person(r['author']['displayName']),
                    'content': re.sub('\xa0', ' ', r['content']),
                    'assignee': None,
                    'isOff': False,
                })
            comments_aux.append(comment)

    # -- Match with anchor information from `glob.raw` -------------------------
    # kix.dv3gwsedtuv4
    # \{"ty":"as","st":"doco_anchor","si":(\d+),"ei":(\d+),"sm":\{"das_a":\{"cv":\{"op":"set","opValue":\[("kix.[^"]+"(,"kix.[^"]+")*)\]\}\}\}\}
    magic = rf'\{{"ty":"as","st":"doco_anchor","si":(\d+),"ei":(\d+),' \
            rf'"sm":\{{"das_a":\{{"cv":\{{"op":"set",' \
            rf'"opValue":\[("kix.[^"]+"(,"kix.[^"]+")*)\]\}}\}}\}}\}}'
    #print(magic)
    matches = re.finditer(magic, glob.raw)
    for match in matches:
        sp = match.start()
        ep = match.end()
        si = match.group(1)
        ei = match.group(2)
        anchors = match.group(3)
        #print("****")
        #print("si:", si)
        #print("ei:", ei)
        #print("anchors:", anchors)
        kixes = re.finditer('"(kix.[^"]+)"', anchors)
        for kix in kixes:
            anchor = kix.group(1)
            #print("kix:", anchor)
            comment = next((c for c in comments_aux if anchor == c['anchor']), None)
            if comment == None:
                continue
            #print(f"found {anchor}")
            comment['si'] = si
            comment['ei'] = ei

    # Here we want to list comments that are not reachable from the doc
    for comment in comments_aux:
        if 'si' not in comment:
            Ansi.note(f"Deleting unreachable comment {dot_google.DOCS_RAD}/"
                      f"{option.doc_id}/edit?disco={comment['id']}")
            # Replacing deletion with resolution, since it does not seem
            # possible to delete others' comments.
            #
            #response = dot_google.drive.comments().delete(
            #    fileId=option.doc_id, commentId=comment['id'],
            #    ).execute()
            dot_google.drive.replies().create(
                fileId=option.doc_id, commentId=comment['id'],
                body = {
                    'content': "Resolving the comment as it does not seem "\
                        "to be reachable from the document.",
                    'action': "resolve",
                },
                fields = "content,action",
            ).execute()
            

#    print('\n*** glob.comments unredacted')
#    print(json.dumps(comments_aux, indent=2))
    
    comments = [c for c in comments_aux if 'si' in c]
    comments = sorted(comments, key=lambda x: x['si'])

#    print('\n*** glob.comments')
#    print(json.dumps(comments, indent=2))

    # -- Match monday `raw` with Tuesday `comments` ----------------------------

    def is_same(c, ca, allow_dejavu=False):
        if c['isOff']: return False
        if c['content'] == ca['content'] and (
            c['assignee'] == None or allow_dejavu) :
            return True
        if c['assignee'] == None: return False
        if c['serial'] != ca['serial']: return False
        for r in c['replies']:
            if r['isOff']: continue
            if r['assignee'] != None and not allow_dejavu: continue
            if r['content'] == ca['content']: return True
        return False

    for comment in comments_assigned:
        # FIXME: remove this debug statement
        #if comment['serial'] == 24:
        #    pass
        # Find match
        try:
            gotcha = next(c for c in comments if is_same(c, comment))
        except StopIteration:
            try:
                gotcha = next(c for c in comments
                              if is_same(c, comment, allow_dejavu=True))
            except StopIteration:
                Ansi.warning(
                    f"Cannot find comment:\n{json.dumps(comment, indent=2)}")
            continue

        # Import assignee information
        if gotcha['assignee'] == None:
            for c in comments:
                if c['ei'] <= gotcha['si']: c['isOff'] = True
                if c['si'] >= gotcha['ei']: break
            gotcha['assignee'] = comment['assignee']
            gotcha['serial'] = comment['serial']
            gotcha['stepId'] = comment['stepId']
            continue
        for r in gotcha['replies']:
            r['isOff'] = True
            if r['assignee'] != None: continue
            if r['content'] != comment['content']: continue
            r['assignee'] = comment['assignee']
            break
    
    # Remove comments that do not have an assignee
    comments = [c for c in comments if c['assignee'] != None]

    # Determine last assignee
    def age(dt):
        #from datetime import datetime, timedelta
        # Convert the string to a datetime object
        before = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Get the current datetime
        now = datetime.utcnow()
        # Calculate the difference between the current datetime and the given datetime
        delta = now - before
        # Extract the number of days from the time difference
        return delta.days

    for comment in comments:
        comment['lastId'] = comment['id']
        comment['lastAssignee'] = comment['assignee']
        comment['lastCreatedTime'] = comment['createdTime']
        comment['lastModifiedTime'] = comment['modifiedTime']
        comment['lastContent'] = comment['content']
        for r in comment['replies']:
            if r['assignee'] != None:
                comment['lastId'] = r['id']
                comment['lastAssignee'] = r['assignee']
                comment['lastCreatedTime'] = r['createdTime']
                comment['lastModifiedTime'] = r['modifiedTime']
                comment['lastContent'] = r['content']

#    dt = datetime.strptime(last_assigned_time, "%Y-%m-%dT%H:%M:%S.%fZ")
#    comment['last_assigned_week'] = \
#        f"{dt.strftime('%Y')}W{dt.strftime('%U').zfill(2)}"

#    print('\n*** glob.comments with assignees')
#    print(json.dumps(comments, indent=2))        

    def dump_comments_table(comments):
        # Sort comments by
        #
        # - Company
        # - Assignee: [Name](mailto)
        # - Age
        # - Stepid: [Bugid](buganizer link), [First letters](header2 link)
        # - Comment: [First letters](comment link)

        def truncate(text, length):
            if len(text) <= length:
                return re.sub("[\n\|]", " ", text)
            else:
                return re.sub("[\n\|]", " ", f"{text[:length-3]}...")
        for c in comments:
            c['lastAge'] = round(age(c['lastCreatedTime']) / 7)
            c['buganizerUrl'] = f"{dot_google.ISSUETRACKER_URL}" \
                                f"/issues/{c['stepId']}"
            step = next(step for step in glob.steps
                        if step['bugid']['value'] == c['stepId'])
            c['shortTitle'] = truncate(step['title']['value'], 35)
            c['stepUrl'] = f"{dot_google.DOCS_RAD}/{option.doc_id}" \
                    f"/edit#heading={step['headingId']}"
            c['shortLastContent'] = truncate(c['lastContent'], 35)
            c['lastCommentUrl'] = f"{dot_google.DOCS_RAD}/{option.doc_id}" \
                                f"/edit?disco={c['lastId']}"
            c['shortQuotedContent'] = truncate(c['quotedFileContent'], 35)
        
        sorted_comments = sorted(comments, key=lambda x: (
            x['lastAssignee']['name'],
            -x['lastAge'],
            x['stepId'],
            x['serial'],
            ))

        text = textwrap.dedent("""
                            
            Assignee | Age | Step ID | Step Title | Excerpt
            ---------|-----|---------|------------|--------
        """)
        for c in sorted_comments:
            text += f"[{truncate(c['lastAssignee']['name'], 20)}]" \
                f"(mailto:{c['lastAssignee']['email']})"
            text += f" | {c['lastAge']}w"
            text += f" | [{c['stepId']}]({c['buganizerUrl']})"
            text += f" | [{c['shortTitle']}]({c['stepUrl']})"
            text += f" | [{c['shortQuotedContent']}]({c['lastCommentUrl']})"
            text += "\n"
            
        # Print the current date and time in local timezone
        local_timezone = get_localzone()
        current_local_date = datetime.now(local_timezone)
        text += f"\n"
        text += f"Last computed on " \
            f"{current_local_date.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        return text
    

    text = textwrap.dedent("""
        ## HOVO pending requests

        ### Pending requests for Google
    """)
    text += dump_comments_table(
        [c for c in comments
         if "@google.com" in c['lastAssignee']['email']])
    text += textwrap.dedent("""
        ### Pending requests for S3NS
    """)
    text += dump_comments_table(
        [c for c in comments
         if "@google.com" not in c['lastAssignee']['email']])

    return text, comments