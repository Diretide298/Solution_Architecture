#!/usr/bin/env python3
"""Prepare the build-order sync for the OpenProject server: renumber every ticket, and find the links the plan dropped.

When the plan changes, tickets already in OpenProject keep yesterday's build-order number (the Priority_No.
field) and yesterday's "follows" links. op-bulk-links adds the new links but never removes one, and nothing
renumbered a ticket once it was made. This writes handoff/service-docs/op-order.json for op-order-sync.rb:

  - "priority": every ticket's OpenProject id -> its build order now (a sub-task takes its task's number)
  - "edges":    every "waits on" pair in the plan, unreduced, as OpenProject ids [task, what it waits on];
                the server keeps a direct link only if the plan still orders that pair, directly or through a chain

Run after tools/refresh.sh and after new tickets are made and merged into pms-map.json (op-created-merge.py):

  python3 tools/op-order-sync.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
PRIORITY_NO = "customField9"   # the "Priority_No." field on project 153, as push-openproject.py writes it


def main() -> int:
    rows = list(csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8")))
    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    seq = {r["key"]: int(r["sequence"]) for r in rows if r["sequence"]}
    missing = sorted(k for k in seq if k not in mp)
    if missing:
        print(f"{len(missing)} plan keys have no OpenProject id yet (make them first: op-create.rb, then "
              f"op-created-merge.py): {', '.join(missing[:15])}{' ...' if len(missing) > 15 else ''}")
        return 1
    priority = {}
    for k, wp in mp.items():
        if k.startswith(("_", "VERSION-")) or not isinstance(wp, int):
            continue
        base = k.split("#", 1)[0]
        if base in seq:
            priority[str(wp)] = seq[base]
    edges = sorted({(mp[r["key"]], mp[d]) for r in rows if r["type"] == "Task"
                    for d in r["dependsOn"].split() if d in mp})
    out = {"field": PRIORITY_NO, "priority": priority, "edges": edges,
           "tasks": sorted(mp[r["key"]] for r in rows if r["type"] == "Task")}
    (DOCS / "op-order.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"op-order.json: {len(priority)} tickets to number, {len(edges)} plan links over "
          f"{len(out['tasks'])} tasks -> {DOCS / 'op-order.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
