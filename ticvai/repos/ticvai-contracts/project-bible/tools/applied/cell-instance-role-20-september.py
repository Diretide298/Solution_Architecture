#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ADR-0042 places a new tenant on the emptiest instance, and an archive server is the emptiest
thing in the estate.

**This is a defect in an accepted ADR, not a new feature.** ADR-0042 decided on 8 September that
a new tenant is provisioned onto the instance in its region with the most headroom — peak
concurrent connections over the trailing 7 days as a fraction of that instance's own
`max_connections`. `control.cell_instance` carries `id`, `cell_id`, `name`, `status`,
`max_connections`, `created_at`, `retired_at`, **and nothing saying what an instance is for.**

So the rule is wrong the first time the estate holds an instance that is not a primary, and
ADR-0047 has just decided on two of them:

    archive     ADR-0047 puts archived personal data on a separate instance rather than a
                tablespace. An archive takes almost no connections, so emptiest-first would
                place the NEXT TENANT PROVISIONED onto the archive server
    burst       CF-162's flash-sale environment has NO TRAILING HISTORY AT ALL, so its
                headroom reads as total. Emptiest-first would put the most violent workload
                in the estate onto whichever instance has the least room to absorb it

**`status: draining` is not this.** Draining is a state an instance passes through — *takes no
new tenants and still serves the ones it has* — and it is temporary by construction. A role is
what an instance is for, permanently. Using `draining` to keep tenants off an archive would mean
marking a healthy instance as being emptied forever, and the two questions would then be
impossible to tell apart on the day an archive really was being retired.

## What changes

    role         primary | archive | burst, required, defaulting to primary
    placement    reads it -- only `primary` is a candidate
    metrics      `archive` and `burst` contribute to NO other instance's headroom figure

**The metric exclusion is the half that is easy to miss.** A flash sale that entered the trailing
seven-day average would hold a region's placement hostage for a week after the sale ended — every
tenant provisioned in that week would be pushed away from a host that is, by then, idle.

    python3 tools/applied/cell-instance-role-20-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SUB = os.path.join(ROOT, "contracts", "satellite", "subscription.yaml")

ANCHOR = "            is being retired.'\n"

ROLE = """        role:
          type: string
          enum:
          - primary
          - archive
          - burst
          default: primary
          description: '**What the instance is for, which decides whether a tenant may be placed
            on it.** ADR-0042 provisions a new tenant onto the instance in its region with the
            most headroom, and until this column existed every instance was a candidate.


            **`archive` holds data past its active stage** (ADR-0047) and takes almost no
            connections, so an emptiest-first rule reads it as the best place in the region and
            would put the next tenant provisioned straight onto it.


            **`burst` is CF-162''s flash-sale environment and has no trailing history at all**,
            so its headroom reads as total — emptiest-first would send the most violent workload
            in the estate to whichever host has the least room for it.


            **Only `primary` is placed onto, and `archive` and `burst` enter no other instance''s
            headroom figure.** A sale that joined the trailing seven-day average would push
            tenants away from that host for a week after it had gone quiet.


            **Distinct from `status: draining`.** Draining is a state an instance passes through
            and is temporary; a role is permanent. Marking an archive as draining to keep tenants
            off it would make a healthy instance indistinguishable from one being retired.'
"""


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(SUB, encoding="utf-8").read()

    if "          - burst\n" in s and "role:" in s:
        print("  already applied")
        return 0

    if s.count(ANCHOR) != 1:
        print("  !! status description anchor matched %d times" % s.count(ANCHOR))
        return 1
    s = s.replace(ANCHOR, ANCHOR + ROLE)
    print("    CellInstance  +role: primary | archive | burst")

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! would not parse: %s" % str(e)[:200])
        return 1
    ci = (doc.get("components") or {}).get("schemas", {}).get("CellInstance") or {}
    props = ci.get("properties") or {}
    if "role" not in props or props["role"].get("default") != "primary":
        print("  !! role did not land correctly")
        return 1
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (doc.get("paths") or {}).values() for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("  !! %d operationId lines, %d parsed" % (text_n, parsed_n))
        return 1
    print("    parses · CellInstance has %d properties · %d operations intact"
          % (len(props), parsed_n))
    print("    enum: %s" % ", ".join(props["role"]["enum"]))

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(SUB, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> contracts/satellite/subscription.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
