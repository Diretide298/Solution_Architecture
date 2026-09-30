#!/usr/bin/env python3
"""Prepare the assignee and week sync for the OpenProject server: who does each ticket, who is accountable, which
Block A week it is planned in.

A ticket gets its assignee, accountable and week ("Block A · Week n" version) when it is made, and nothing changed
them afterwards. On 30 September 307 of the 515 tasks read back from OpenProject still named the person from an
older plan, so a developer's board showed someone else's work. This writes handoff/service-docs/op-assign.json for
op-assign-sync.rb, with every value worked out exactly as push-openproject.py does when it makes a ticket:

  - task:      assignee from the Block A schedule (else tasks.csv), accountable by track, week from its start day
  - sub-task:  the same as its task
  - epic, feature: assignee and accountable; the week is left alone (they have none)

Run after tools/refresh.sh and after new tickets are merged into pms-map.json:

  python3 tools/op-assign-sync.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
sys.path.insert(0, str(Path(__file__).parent))
LEAD = __import__("push-openproject").LEAD


def main() -> int:
    rows = list(csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8")))
    by_key = {r["key"]: r for r in rows}
    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    sched = json.loads((DOCS / "block-a-schedule.json").read_text(encoding="utf-8"))
    who = sched["assign"]
    week = {k: min(int(v // 5), 6) + 1 for k, v in sched["start"].items()}
    svc_owner = {r["service"]: r["assignee"] for r in rows if r["type"] == "Epic" and r["key"].startswith("SVC-")}

    def accountable(r):
        if r["track"] in ("Backend", "Database"):
            return svc_owner.get(r["service"]) or LEAD["devops"]
        return LEAD.get(r["area"]) or r["assignee"]

    tickets, people = {}, set()
    for key, wp in mp.items():
        if key.startswith(("_", "VERSION-")) or not isinstance(wp, int):
            continue
        base = key.split("#", 1)[0]
        r = by_key.get(base)
        if not r:
            continue                                    # out of the plan: op-retire.py handles it
        if r["type"] == "Task":
            assignee = who.get(base) or r["assignee"] or None
            wk = week.get(base)
            version = mp.get(f"VERSION-W{wk}") if wk else None
        else:
            assignee, version = r["assignee"] or None, None
        acct = accountable(r)
        tickets[str(wp)] = {"key": key, "assignee": assignee, "responsible": acct, "version": version,
                            "setVersion": r["type"] == "Task"}
        people.update(p for p in (assignee, acct) if p)
    out = {"project": 153, "people": sorted(people), "tickets": tickets}
    (DOCS / "op-assign.json").write_text(json.dumps(out), encoding="utf-8")
    print(f"op-assign.json: {len(tickets)} tickets, {len(people)} people -> {DOCS / 'op-assign.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
