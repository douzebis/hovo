__package__ = 'hovo'

import colorsys
import json
from math import sqrt
import re
import textwrap
from hovo import dot_google, glob, option
from hovo.colors import Ansi

from hovo.const import STAGE, STAGES


def hsv_to_rgb(h, s, v):
    """
    Convert HSV (Hue, Saturation, Value) color to RGB (Red, Green, Blue) color.
    h: float, Hue component (0.0 - 1.0)
    s: float, Saturation component (0.0 - 1.0)
    v: float, Value component (0.0 - 1.0)
    Returns: tuple, (r, g, b) where r, g, b are RGB components (0 - 255)
    """
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    #l = 0.2126 * r + 0.7152 * g + 0.0722 * b
    l = sqrt(0.299*r*r + 0.587*g*g + 0.114*b*b)
    if l > 0:
        r = r * v / l
        g = g * v / l
        b = b * v / l
    if r > 1: r = 1
    if g > 1: g = 1
    if b > 1: b = 1
    # Convert RGB color to hexadecimal color code
    hex_color = '#{:02x}{:02x}{:02x}'.format(
        int(r * 255),
        int(g * 255),
        int(b * 255)
    )
    return hex_color

def get_dependency_graphs():
    text = textwrap.dedent(f"""
        ## HOVO dependency graphs
    """)

    for stage in STAGES:
        text += textwrap.dedent(f"""

            ### HOVO Dependency graph for stage '{stage}'
                               
            ```mermaid
            flowchart TD
        """)
        seen_nodes = set()
        def is_dejavu_node(bugid):
            if bugid in seen_nodes:
                return True
            seen_nodes.add(bugid)
            return False

        seen_arrows = set()
        def is_dejavu_arrow(from_id, to_id):
            arrow = f"{from_id}-{to_id}"
            if arrow in seen_arrows:
                return True
            seen_arrows.add(arrow)
            return False
        
        labels = {}
        leaders = {}
        areas = {
            'Security': [],
            'Datacenter': [],
            'Partner_Integrations': [],
            'Base_Networking': [],
            'Cloud_Networking': [],
            'Operations': [],
            'Contract___Compliance': [],
            'Testing': [],
            'Program_Mgt_': [],
            'GCP_Horizontal_Services': [],
            'TPC_IaaC': [],
        }

        fills = {}
        def decorate(bugid):
            if bugid not in seen_nodes:
                seen_nodes.add(bugid)
            if bugid in labels: return
            step = next((s for s in glob.steps
                         if s['bugid']['value'] == bugid), None)
            if step == None: return
            node_title = step['title']['value']
            node_label = (
                f'"{bugid}\\n'
                f'{node_title[:14]}\\n'
                f'{node_title[14:28]}\\n'
                f'{node_title[28:42]}\\n'
                f'{node_title[42:46]}"')
            labels[bugid] = node_label
            node_leader = step['leader_val']['value']
            node_leader = re.sub(r'[ .,;&]', '_', node_leader.strip())
            if step['stage_val']['value'] != stage:
                node_leader = 'not_this_stage'
            if node_leader not in leaders:
                leaders[node_leader] = []
            leaders[node_leader].append(bugid)
            node_area = step['areas_val']['value']
            node_area = re.sub(r',.*', '', node_area.strip())
            node_area = re.sub(r'[ .,;&]', '_', node_area)
            if node_area not in fills:
                fills[node_area] = None
            #if step['stage_val']['value'] != stage:
            #    node_area = 'pale_' + node_area
            if node_area not in areas:
                areas[node_area] = [bugid]
            else:
                areas[node_area].append(bugid)
            return node_label 

        for step in glob.steps:
            step_id = step['bugid']['value']

            for s in step['unlocks']:
                sibling_id = s['value']
                if is_dejavu_arrow(step_id, sibling_id):
                    continue
                sibling = next(
                    (s for s in glob.steps if s['bugid']['value'] == sibling_id),
                    None)
                if (step['stage_val']['value'] != stage and
                    (sibling == None or sibling['stage_val']['value'] != stage)):
                    continue
                decorate(step_id)
                decorate(sibling_id)
                text += f"\n{step_id} --> {sibling_id}"

            for s in step['depends_on']:
                sibling_id = s['value']
                if is_dejavu_arrow(sibling_id, step_id):
                    continue
                sibling = next(
                    (s for s in glob.steps if s['bugid']['value'] == sibling_id),
                    None)
                if (step['stage_val']['value'] != stage and
                    (sibling == None or sibling['stage_val']['value'] != stage)):
                    continue
                decorate(step_id)
                decorate(sibling_id)
                text += f"\n{sibling_id} --> {step_id}"
        
        text += f"\n"
        for bugid in labels:
            text += f"\n{bugid}[{labels[bugid]}]"
        
        text += f"\n"
        for leader in leaders:
            text += f"\nclass "
            for bugid in leaders[leader]:
                text += f"{bugid},"
            text += f" {leader}"
        
        text += f"\n"
        for area in areas:
            if len(areas[area]) == 0: continue
            text += f"\nclass "
            for bugid in areas[area]:
                text += f"{bugid},"
            text += f" {area}"
        
        text += f"\n"
        text += f"\nclassDef S3NS stroke:#0060FF,stroke-width:6px"
        text += f"\nclassDef Google stroke:#FF0000,stroke-width:6px"
        text += f"\nclassDef Joint stroke:#C08000,stroke-width:6px"
        text += f"\nclassDef not_this_stage stroke:#000000,stroke-width:6px"
        
        text += f"\n"
        sorted_fills = sorted([f for f in fills])
        count_fills = len(sorted_fills)
        for i in range(count_fills):
            fill = sorted_fills[i]
            saturated = hsv_to_rgb(i/count_fills, 1, 0.4)
            unsaturated = hsv_to_rgb(i/count_fills, 0.2, 0.4)
            text += f"\nclassDef {fill} fill:{saturated},color:white"
            text += f"\nclassDef pale_{fill} fill:{unsaturated},color:white"
        
        text += f"\n"
        for bugid in seen_nodes:
            step = next((s for s in glob.steps
                         if s['bugid']['value'] == bugid), None)
            if step == None:
                bug_link = f"{dot_google.ISSUETRACKER_URL}/issues/{bugid}"
                text += f'\nclick {bugid} "{bug_link}"'
            else:
                doc_link = f"{dot_google.DOCS_RAD}/{option.doc_id}"
                heading_link = f"{doc_link}/edit#heading={step['headingId']}"
                text += f'\nclick {bugid} "{heading_link}"'

        text += f"\n```\n"

    return text


#classDef Security fill:#f96

