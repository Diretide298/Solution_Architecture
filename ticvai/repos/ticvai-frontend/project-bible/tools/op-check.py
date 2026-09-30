#!/usr/bin/env python3
"""Prepare the OpenProject health check (tools/op-check.rb): what the plan says each ticket in pms-map.json is.

Writes handoff/service-docs/op-check.json:
  "tickets": id -> {key, type, parent (OpenProject id or null), subject (tasks, features, epics only)}
  "retired": ids of tickets tools/op-retire.py moved out of the plan (closed or on hold), so the check does not
             report them as unknown

    python3 tools/op-check.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
sys.path.insert(0, str(Path(__file__).parent))
TYPES = __import__("push-openproject").TYPES


def main() -> int:
    rows = {r["key"]: r for r in csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8"))}
    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    tickets, retired = {}, []
    for key, wp in mp.items():
        if key.startswith(("_", "VERSION-")) or not isinstance(wp, int):
            continue
        base, _, part = key.partition("#")
        r = rows.get(base)
        if not r:
            retired.append(wp)
            continue
        if part:
            tickets[str(wp)] = {"key": key, "type": TYPES["Sub Task"], "parent": mp.get(base), "subject": None}
        else:
            tickets[str(wp)] = {"key": key, "type": TYPES[r["type"]],
                                "parent": mp.get(r["parent"]) if r["parent"] else None,
                                "subject": r["subject"][:255]}
    out = {"project": 153, "tickets": tickets, "retired": sorted(retired)}
    (DOCS / "op-check.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"op-check.json: {len(tickets)} plan tickets, {len(retired)} retired -> {DOCS / 'op-check.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
