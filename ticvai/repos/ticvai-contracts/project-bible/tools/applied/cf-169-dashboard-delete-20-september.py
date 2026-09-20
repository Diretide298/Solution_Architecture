#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The half of CF-169 that is a contract decision rather than a screen.

CF-169 names three places where a data model was built and no screen written. **Two of them are
design work** — dashboard authoring screens, and `seatp`'s 130 screens of seat-map authoring with
no package counterpart. The third is a contract question and it is answerable now:

    "there is no `deleteDashboard` — list, create, get, update and nothing else — so a soft or
     hard delete has to be chosen where `is_shared` is true"

Confirmed: four operations on `/dashboards`, no delete.

## Soft, and the deciding column is `is_shared`

| | |
|---|---|
| **Maintainability** | a soft delete costs an `archived_at` column and a predicate on every list. Small, and it is the only version that can be undone |
| **Readability** | `archivedAt` says what happened; a missing row says nothing |
| **Optimised access** | one predicate on a list of tens of rows per venue |
| **DB strain** | negligible either way — dashboards are few and `tiles` is capped at 24 |
| **Cross-cell** | none. A dashboard belongs to the venue whose data it reads |

**`is_shared` is what settles it.** A shared dashboard is on other people's screens, and hard
deletion makes their saved view vanish with no way to say what it was. `dashboard_tile` cascades
too, so a hard delete takes the tile configuration — `visualisation`, `parameters`,
`refresh_seconds` — that somebody spent an afternoon on.

**Archiving a shared dashboard is refused.** Un-sharing first is one extra call and it puts the
owner in front of the fact that other people are using it, which a confirmation dialog cannot do
because nothing reaches the people who are.

    python3 tools/applied/cf-169-dashboard-delete-20-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REP = os.path.join(ROOT, "contracts", "satellite", "reporting.yaml")

ARCHIVED = """          archivedAt:
            type: string
            format: date-time
            nullable: true
            readOnly: true
            description: >
              **Set by `deleteDashboard`, which archives rather than removes.** A dashboard's
              tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody
              configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an
              afternoon's work with it and leaves nothing to say what was there.

              Archived dashboards are excluded from `listDashboards` unless asked for.
"""

DELETE_OP = """    delete:
      operationId: deleteDashboard
      summary: Archive a dashboard
      description: 'CF-169. **Archives rather than removes, and refuses while `isShared` is true.**

        A shared dashboard is on other people''s screens. Deleting one makes their saved view vanish
        with no way to say what it was, and a confirmation dialog cannot help because nothing in it
        reaches the people who are using it — **un-sharing first is one extra call and it puts the
        owner in front of that fact.**

        The tiles go with it and come back with it. `reporting.dashboard_tile` carries
        `visualisation`, `parameters` and `refresh_seconds` per tile, which is the configuration
        work rather than the dashboard.

        '
      tags:
      - reporting
      x-ticvai-permission: REPORT_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      responses:
        '204':
          description: Archived
        '409':
          description: The dashboard is shared. Un-share it first.
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
"""


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(REP, encoding="utf-8").read()

    if "operationId: deleteDashboard" in s:
        print("  already applied")
        return 0

    i = s.find("      x-ticvai-persistence: reporting.dashboard + reporting.dashboard_tile\n")
    if i < 0:
        print("  !! Dashboard schema not found")
        return 1
    j = s.find("          createdAt:\n", i)
    if j < 0:
        print("  !! Dashboard.createdAt anchor not found")
        return 1
    s = s[:j] + ARCHIVED + s[j:]
    print("    Dashboard        +archivedAt")

    # Into the existing `/dashboards/{dashboardId}` path, after its last verb.
    h = s.find("  /dashboards/{dashboardId}:\n")
    if h < 0:
        print("  !! path not found")
        return 1
    nxt = re.search(r"^  /", s[h + 30:], re.M)
    end = h + 30 + (nxt.start() if nxt else 0)
    if not nxt:
        c = re.search(r"^components:", s[h:], re.M)
        end = h + c.start()
    s = s[:end] + DELETE_OP + s[end:]
    print("    /dashboards/{dashboardId}  +deleteDashboard")

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! would not parse: %s" % str(e)[:180])
        return 1
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (doc.get("paths") or {}).values() for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("  !! %d operationId lines, %d parsed" % (text_n, parsed_n))
        return 1
    verbs = list((doc["paths"]["/dashboards/{dashboardId}"] or {}))
    print("    parses · %d operations · path verbs: %s" % (parsed_n, verbs))

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(REP, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> contracts/satellite/reporting.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
