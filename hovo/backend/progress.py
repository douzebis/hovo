__package__ = 'hovo'

import copy
from datetime import datetime
import inspect
import sys
import textwrap

from tzlocal import get_localzone
from hovo import glob
from hovo.colors import Ansi
from hovo.const import STAGE, STAGES


def get_progress():
#    Ansi.print("\nHOVO Maturity...", color=Ansi.GRAY, file=sys.stderr)
#    Ansi.print("\nPlease paste this markdown in the mog",
#               color=Ansi.GREEN, file=sys.stderr)
#    Ansi.print("```", color=Ansi.GREEN, file=sys.stderr)
    text = textwrap.dedent("""
        ## HOVO progress
          
        ### Progress indicator
                           
        \  | # steps | eng·days | maturity % | effort % | duration %
        ---|--------:|---------:|-----------:|---------:|----------:
    """)

    count = {
        getattr(STAGE, key): 0
        for key in dir(STAGE)
        if not key.startswith("__") and not inspect.ismethod(getattr(STAGE, key))
    }
    total_m = copy.deepcopy(count)  # Maturity %
    total_ce = copy.deepcopy(count)  # Cumulative effort
    total_e = copy.deepcopy(count)  # % of steps with an effort estimate
    total_d = copy.deepcopy(count)  # % of steps with a duration estimate
    
    # Iterate through steps
    for step in glob.steps:
        # Skip milestones
        if step['duration_val']['value'] == 0:
            continue
        stage = step['stage_val']['value']
        count[stage] += 1
        total_m[stage] += step['maturity_val']['value']
        if step['effort_val']['value'] != 'TBD':
            total_ce[stage] += step['effort_val']['value']
            total_e[stage] += 1
        if step['duration_val']['value'] != 'TBD':
            total_d[stage] += 1
    total_count = sum(count.values())
    grand_total_m = sum(total_m.values())
    grand_total_ce = sum(total_ce.values())
    grand_total_e = sum(total_e.values())
    grand_total_d = sum(total_d.values())
    if total_count == 0:
        maturity = 'NA'
        cum_effort = 'NA'
        effort = 'NA'
        duration = 'NA'
    else:
        maturity = str(round(100*grand_total_m/(3*total_count))) + "%"
        cum_effort = str(round(grand_total_ce))
        effort = str(round(100*grand_total_e/total_count)) + "%"
        duration = str(round(100*grand_total_d/total_count)) + "%"
    text += f"Total | {total_count} | {cum_effort} | {maturity}" \
        f"| {effort} | {duration}\n"
    for stage in STAGES:
        if count[stage] == 0:
            maturity = 'NA'
            cum_effort = 'NA'
            effort = 'NA'
            duration = 'NA'
        else:
            maturity = str(round(100*total_m[stage]/(3*count[stage]))) + "%"
            cum_effort = str(round(total_ce[stage]))
            effort = str(round(100*total_e[stage]/count[stage])) + "%"
            duration = str(round(100*total_d[stage]/count[stage])) + "%"
        text += f"{stage} | {count[stage]} | {cum_effort} | {maturity}" \
            f"| {effort} | {duration}\n"

    # Print the current date and time in local timezone
    local_timezone = get_localzone()
    current_local_date = datetime.now(local_timezone)
    text += f"\n"
    text += f"Last computed on " \
          f"{current_local_date.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"

    # Add a explanatory epilog
    text += textwrap.dedent("""
        ### Meaning of the HOVO progress indicator

        The HOVO maturity indicator represents the level of maturity of the
        descriptions of the steps to be performed during TPC hand-off. It is
        based on the maturity stars in the HOVO:
          
        - ☆☆☆: 0%
        - ★☆☆: 33%
        - ★★☆: 67%
        - ★★★: 100%

        The maturity is consolidated by hand-off stage.

        Note: we recently decided to exclude milestones (i.e. zero duration
        steps) from the consolidation - with a temporarily negative effect
        on the indicator.
    """)
#    Ansi.print("```", color=Ansi.GREEN, file=sys.stderr)
    return text
