__package__ = 'hovo'

import json
import re

from hovo import dot_google, glob, option
from hovo.buganizer import B7r, add_b7r_comment, get_b7r_fields, set_b7r_description
from hovo.colors import Ansi


def get_description(bug):
    if B7r.DESCRIPTION['nickname'] not in bug:
        return None
    else:
        return bug[B7r.DESCRIPTION['nickname']]

def truncate(text, length):
            if len(text) <= length:
                return re.sub("[\n\|]", " ", text)
            else:
                return re.sub("[\n\|]", " ", f"{text[:length-3]}...")
            
def patch_buganizer(comments):
    for step in glob.steps:
        bugid = step['bugid']['value']
        title = step['title']['value']
        doc_link = f"{dot_google.DOCS_RAD}/{option.doc_id}"
        heading_link = f"{doc_link}/edit#heading={step['headingId']}"
        kill_line = glob.msgs_count == Ansi.msgs_count()
        Ansi.info(f"Checking description of step {bugid}...",
                  kill_line=kill_line)
        glob.msgs_count = Ansi.msgs_count()
        def is_good_to_go(description):
            if not isinstance(description, str):
                return False
            if heading_link not in description:
                return False
            for comment in comments:
                if comment['stepId'] != bugid: continue
                if comment['lastCommentUrl'] in description: continue
                return False
            return True

        bug = get_b7r_fields(bugid)
        description = get_description(bug)
        if not is_good_to_go(description) and not bug['is_fresh']:
            bug = get_b7r_fields(bugid, force=True)
            description = get_description(bug)

        if not is_good_to_go(description):
            new_description = (
                f"The **source of truth** for the Handoff step discussed in "
                f"this Partner Issue is **[section _{title.strip()}_]"
                f"({heading_link})** of the **[Handoff Voice Over (HOVO)]"
                f"({doc_link})** document.\n\nPlease [refer to the HOVO]"
                f"({heading_link}) for details about this issue.\n\n"
                f"Please **always update the HOVO** after you come to a "
                f"resolution through exchanges via the Partner Issue Tracker.")
            arm_comments = (
                f"\n\nThe following HOVO comment(s) pertain to this Partner "
                f"Issue and have active assignees:")
            for comment in comments:
                if comment['stepId'] != bugid: continue
                comment_summary = (
                    f"\n- [{truncate(comment['lastContent'], 80)}]"
                    f"({comment['lastCommentUrl']})")
                new_description += arm_comments + comment_summary
                arm_comments = ''
                if comment['lastCommentUrl'] in description: continue
                comment_notify = (
                    f"The [following HOVO comment]"
                    f"({comment['lastCommentUrl']}) "
                    f"pertains to this Partner Issue and was assigned to "
                    f"[{comment['lastAssignee']['name']}]"
                    f"(mailto:{comment['lastAssignee']['email']}) "
                    f"on {comment['lastCreatedTime']}:\n\n--\n\n"
                    f"{comment['lastContent']}")
                Ansi.note(f"Notifying step {bugid} of comment {comment['id']}"
                          f"...")
                add_b7r_comment(bugid, comment_notify)
                
            Ansi.note(f"Updating the description of step {bugid}...")
            set_b7r_description(bugid, new_description)
            bug = get_b7r_fields(bugid, force=True)