__package__ = 'hovo'

import inspect
import io
import json
import re
import sys
import zipfile

import click
from bs4 import BeautifulSoup
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from hovo import glob, googleapi, option, state
from hovo.cleanup import cleanup
from hovo.colors import Ansi
from hovo.const import STAGE, STAGES
from hovo.depend import parse_depend
from hovo.fixer import Fixer
from hovo.heading2 import parse_h2
from hovo.heading3 import parse_h3
from hovo.table import parse_table


def parse_steps(elements):
    """Recurses through a list of Structural Elements to retrieve Hovo steps
        specifications and dependencies between steps.

        Args:
            elements: a list of Structural Elements.
    """

    for element in elements:
        if 'paragraph' in element:  
            elems = element.get('paragraph').get('elements')
            try:
                style = element['paragraph']['paragraphStyle']['namedStyleType']
                if style == 'HEADING_1':
                    glob.commit_step()
                    continue
                elif style == 'HEADING_2':
                    glob.commit_step()
                    parse_h2(element)
                    continue
                elif style == 'HEADING_3':
                    parse_h3(element)
                    continue
            except:
                pass
            if (state.mode == state.ParsingMode.DEPENDS_ON
                or state.mode == state.ParsingMode.UNLOCKS):
                parse_depend(elems)
            #for elem in elems:
            #    parse_steps(elem)
        #if (state.mode == state.ParsingMode.DEPENDS_ON
        #    or state.mode == state.ParsingMode.UNLOCKS):
        #    parse_depend(element)

        elif 'table' in element:
            parse_table(element)

        elif 'tableOfContents' in element:
            # The text in the TOC is also in a Structural Element.
            toc = element.get('tableOfContents')
            parse_steps(toc.get('content'))

def check_hovo():
    Ansi.print("Parsing the document...", color=Ansi.GRAY, file=sys.stderr)
    parse_steps(glob.contents)
    # Commit the last (possibly pending) step
    glob.commit_step()

    # Walk the dependencies one more time to add links to the corresponding
    # headings if possible (i.e., when the bugid corresponds to a step)
    for ref in glob.dependencies:
        step = next((s for s in glob.steps
                     if s['bugid']['value'] == ref['bugid']['value']), None)
        url = f"" if step == None else f"#heading={step['headingId']}"
        Fixer.update_style(
            ref['title']['start'],
            ref['title']['end'],
            url=url,
        )

    if option.traces:
        Ansi.flash("\n*** DUMPING HOVO STEPS...")
        Ansi.flash(json.dumps(glob.steps, indent=2))
        Ansi.flash("\n*** DUMPING HOVO DEPENDENCIES...")
        Ansi.flash(json.dumps(glob.dependencies, indent=2))

    if option.traces:
        Ansi.flash("\n*** DUMPING DOC.get_inplace_requests()...")
        Ansi.flash(json.dumps(Fixer.get_inplace_requests(), indent=2))
        Ansi.flash("\n*** DUMPING DOC.get_moving_requests()...")
        Ansi.flash(json.dumps(Fixer.get_moving_requests(), indent=2))
        
    if not option.dry_run:
        googleapi.docs.documents().batchUpdate(
            documentId=option.doc_id,
            body={'requests': Fixer.get_inplace_requests() \
                + Fixer.get_moving_requests()}
        ).execute()

    return

    Ansi.print("\nHOVO Maturity...", color=Ansi.GRAY, file=sys.stderr)
    count = {
        getattr(STAGE, key): 0
        for key in dir(STAGE)
        if not key.startswith("__") and not inspect.ismethod(getattr(STAGE, key))
    }
    sigma = {
        getattr(STAGE, key): 0
        for key in dir(STAGE)
        if not key.startswith("__") and not inspect.ismethod(getattr(STAGE, key))
    }
    # Iterate through steps
    for step in G.Steps:
        stage = step['stage']
        count[stage] += 1
        sigma[stage] += step['maturity']
    Count = sum(count.values())
    Sigma = sum(sigma.values())
    Ansi.print(
        f"Global maturity: {round(100*Sigma/(3*Count)) if Count > 0 else 'NaN'}%",
        color=Ansi.GREEN)
    for stage in STAGES:
        Ansi.print(
            f"- {stage}: {round(100*sigma[stage]/(3*count[stage])) if count[stage] > 0 else 'NaN'}%",
            color=Ansi.GREEN)

    Ansi.print("\nCHECKING THE CONSISTENCY OF DEPENDENCIES", color=Ansi.GRAY, file=sys.stderr)
    for step in G.Steps:
        step_id = step['bugid']
        missing_depends = []
        missing_unlocks = []
        for sibling in G.Steps:
            sibling_id = sibling['bugid']
            if sibling_id == step_id:
                continue
            if step_id in sibling['unlocks'] and not sibling_id in step['depends_on']:
                missing_depends.append(sibling)
            if step_id in sibling['depends_on'] and not sibling_id in step['unlocks']:
                missing_unlocks.append(sibling)
        if len(missing_depends) == 0 and len(missing_unlocks) == 0:
            #ACOL.print(f"{step_id}: OK", color=ACOL.GRAY)
            continue
        Ansi.print(f"{step_id}: {step['title']}...", color=Ansi.BRIGHT_YELLOW)
        if len(missing_depends) > 0:
            Ansi.print(f"- Missing 'depends on':", color=Ansi.BRIGHT_YELLOW)
            for sibling in missing_depends:
                Ansi.print(f"{sibling['bugid']} {sibling['title']}", color=Ansi.YELLOW)
        if len(missing_unlocks) > 0:
            Ansi.print(f"- Missing 'unlocks':", color=Ansi.BRIGHT_YELLOW)
            for sibling in missing_unlocks:
                Ansi.print(f"{sibling['bugid']} {sibling['title']}", color=Ansi.YELLOW)

    Ansi.print("\nOUTPUTING DEPENDENCY GRAPH", color=Ansi.GRAY, file=sys.stderr)
    Ansi.print(f"graph TD;", color=Ansi.GREEN)
    G.Seen = set()
    for step in G.Steps:
        step_id = step['bugid']
        for sibling_id in step['unlocks']:
            sibling_label = node_label(sibling_id)
            step_label = node_label(step_id) # /!\ Don't move this line up. We want a label only the 1st time
            Ansi.print(f"  {step_id}{step_label} --> {sibling_id}{sibling_label};", color=Ansi.GREEN)

    Ansi.print("\nOUTPUTING GANTT CHART", color=Ansi.GRAY, file=sys.stderr)
    Ansi.print(f"gantt", color=Ansi.GREEN)
    Ansi.print(f"  title HOVO Gantt", color=Ansi.GREEN)
    Ansi.print(f"  dateFormat  YYYY-MM-DD", color=Ansi.GREEN)
    Ansi.print(f"  excludes  Saturday Sunday", color=Ansi.GREEN)
    Ansi.print(f"  start :start, 2024-01-01, 0d", color=Ansi.GREEN)
    prev_stage = None
    for step in G.Steps:
        stage = step['stage']
        if stage != prev_stage:
            Ansi.print(f"  section {stage}", color=Ansi.GREEN)
            prev_stage = stage
        step_id = step['bugid']
        #for sibling_id in G.Steps:
        #    if not sibl
        #    step['unlocks']:
        #    sibling_label = node_label(sibling_id)
        #    step_label = node_label(step_id)
        task = f"{step_id} :{step_id}, after start"
        for sibling_id in step['depends_on']:
            task += f" {sibling_id}"
        task += ", 1d"
        Ansi.print(f"  {task}", color=Ansi.GREEN)
    
############
# ASSIGNEES
    try:
        request = drive.files().export_media(
            fileId=doc_id, mimeType="application/zip"
        )
        zip_file = io.BytesIO()
        downloader = MediaIoBaseDownload(zip_file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
    except HttpError as error:
        raise click.ClickException(f"An error occurred: {error}")

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        # We extract the first file in the zip
        html_content = zip_ref.read(zip_ref.namelist()[0])
        
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tags with id matching the pattern 'cmnt\d*'
    target_tags = soup.find_all(
        lambda tag: (
            tag.name == 'h2'
            or tag.has_attr('id') and tag['id'].startswith('cmnt')))

    # Print the contents of the enclosing <div> for each matching tag
    G.Cmnts = []
    current_bugid = None
    for tag in target_tags:
        if tag.name == 'h2':
            if current_bugid != None:
                step = next(step for step in G.Steps if step['bugid'] == current_bugid)
                step['cmnts'] = current_cmnts
            bugid = STEP.parse.sub(STEP.BUGID, tag.text)
            if not bugid != tag.text:
                current_bugid = None
                continue
            title  = STEP.parse.sub(STEP.TITLE, tag.text)
            current_bugid = bugid
            current_cmnts = []
        elif tag.name == 'a':
            if not tag.has_attr('id'):
                continue
            cmnt = re.sub('cmnt_ref(\d*)', r'\1', tag['id'])
            if cmnt != tag['id']:
                if current_bugid != None:
                    current_cmnts.append(cmnt)
                    continue
            cmnt = re.sub('cmnt(\d*)', r'\1', tag['id'])
            if cmnt != tag['id']:
                enclosing_div = tag.find_parent('div')
                if not enclosing_div:
                    continue
                text = enclosing_div.text.strip()
                assignee = re.sub(r'.*_Assigned to ([^ ]*)_$', r'\1', text, flags=re.S)
                if not assignee != text:
                    G.Cmnts.append({'cmnt': cmnt})
                else:
                    G.Cmnts.append({'cmnt': cmnt, 'assignee': assignee})
                continue
    if current_bugid != None:
        step = next(step for step in G.Steps if step['bugid'] == current_bugid)
        step['cmnts'] = current_cmnts

    Ansi.print("\nBUGIDS PER ASSIGNEE", color=Ansi.GRAY, file=sys.stderr)
    assignee_bugids = {}
    # Iterate through bugids
    for step in G.Steps:
        bugid = step["bugid"]
        if (step['leader'] != 'Google'
            and step['maturity'] != 3):
                assignee = step['s3ns_email']
                if assignee not in assignee_bugids:
                    assignee_bugids[assignee] = set()
                assignee_bugids[assignee].add(bugid)
        for cmntid in step["cmnts"]:
            cmnt = next((cmnt for cmnt in G.Cmnts if cmnt["cmnt"] == cmntid), None)
            if "assignee" in cmnt:
                assignee = cmnt["assignee"]
                # Add bugid to the assignee_bugids dictionary
                if assignee not in assignee_bugids:
                    assignee_bugids[assignee] = set()
                assignee_bugids[assignee].add(bugid)
    # Display the result
                
    for assignee, assigned_bugids in sorted(assignee_bugids.items()):
        Ansi.print(f"{assignee}: {sorted(assigned_bugids)}", color=Ansi.YELLOW)
    
    Ansi.print("\nASSIGNEES PER BUGID", color=Ansi.GRAY, file=sys.stderr)
    bugid_comments = {}
    # Iterate through bugids
    for step in G.Steps:
        bugid = step["bugid"]
        comments_with_assignee = []
        # Iterate through comments for the current bugid
        for cmntid in step["cmnts"]:
            cmnt = next(c for c in G.Cmnts if c['cmnt'] == cmntid)
            if cmnt and 'assignee' in cmnt:
                comments_with_assignee.append(cmnt['assignee'])
        # Add bugid and corresponding comments with assignee to the dictionary
        if comments_with_assignee:
            bugid_comments[bugid] = comments_with_assignee
    # Display the result
    for bugid, comments_with_assignee in bugid_comments.items():
        Ansi.print(f"{bugid}: {comments_with_assignee}", color=Ansi.YELLOW)

    Ansi.print("\nCLEANING UP BUGIDS FORMATTING IN THE DOCUMENT", color=Ansi.GRAY, file=sys.stderr)
    cleanup(docs, doc_id)

# hovo() is the entry point for shell completion
#def hovo():
#    print("BEFORE OPTIONS")
#    get_options()
#    print("BEFORE PROCESS")
#    process()
#    print("AFTER PROCESS")

#if __name__ == 'main__':
##    hovo()
#    print("AT THE END")


"""
    for bugid in [
        306596328,
        306596329,
        306596461,
        306596467,
        306596468,
        306596469,
        306600147,
        306600720,
        306600904,
        306600905,
        306600906,
        306600908,
        306601151,
        306601152,
        306601646,
        306601647,
        306601648,
        306601663,
        306601664,
        306602238,
        306602239,
        306602241,
        306603096,
        306603097,
        306603917,
        306603953,
        306603954,
        306603955,
        306603959,
        306606613,
        306606614,
    ]:
        # Fetch buganizer page
        buganizer_response = requests.get(
            f"https://partnerissuetracker.corp.google.com/issues/{bugid}",
            headers={'Cookie': cookie})

        # Check if the request to the protected page was successful
        if buganizer_response.status_code != 200:
            raise click.ClickException(
                f"Error accessing: {buganizer_response.status_code}")
        
        # Parse the HTML content using BeautifulSoup
        buganizer = BeautifulSoup(buganizer_response.text, 'html.parser')

        # Find all script tags
        buganizer_tags = buganizer.find_all('script')
        duration = 99
        duration = get_buganizer_prop(buganizer_tags, PROP.GOOGLE_DURATION)
        ACOL.print(f"{bugid}: {duration}", color=ACOL.GREEN)
    return
"""