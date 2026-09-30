# -*- coding: utf-8 -*-
"""Derive the Block A schedule from the task sheet: a start day and an assignee for every task.

    python tools/derive-block-a-schedule.py        # writes handoff/service-docs/block-a-schedule.json

**Why derived** (30 September). The schedule was reconstructed by hand on 27 September from ticket text, and
the re-derive of 30 September added 242 tasks it did not know. A schedule that has to be patched by hand after
every re-derive is one that is wrong after every re-derive.

A list scheduler over working days from Monday 5 October 2026:
- tasks in the sheet's build order (`sequence`, which already puts database before back end before front end);
- each on its assignee, at the plan's pace (Block A as sized: 3,018 points, 35 days, 9 developers) times
  that person's pace in docs/active/team.json (`pace`, Surendra 0.6);
- never before every task it depends on (`dependsOn`) has ended, **except a front-end task on a back-end
  one**: screens build against the generated client and the mock server (SETUP-CLIENTS, SETUP-SEED), so the
  screen may start first and only its end waits for the back end it wires to;
- **soft platform waits** (30 September, Chinmay): a backend task may start before the platform kernel,
  idempotency and the outbox are finished, because it is written against their interfaces, which are
  published by day INTERFACES_DAY; the kernel may start before sign-in setup for the same reason; and a
  read-only or report task may start before the services whose data it reads, building against the seeded
  data. In each case only its end waits. Setup, migrations and the AI engine's setup stay hard;
- AI engine tasks carry no points: their length is the engineer-days named in
  docs/active/block-a-extra-tasks.json;
- client tasks start on day 0 and hold no one.

A start past day 34 is Block A's tail in B1, and the ticket says so (op-descriptions.py).
"""
import csv, io, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
PACE = 3018 / 35 / 9
# The platform interfaces (ITenantContext, the current user, the idempotency filter, the outbox writer) are
# published in week 1; a backend task written against them can start from here.
INTERFACES_DAY = 3.0
SOFT_PLATFORM = {"PLATFORM-KERNEL", "PLATFORM-IDEMPOTENCY", "PLATFORM-OUTBOX"}


def main():
    team = json.loads((ROOT / "docs" / "active" / "team.json").read_text(encoding="utf-8"))
    pace_of = team.get("pace") or {}
    extra = json.loads((ROOT / "docs" / "active" / "block-a-extra-tasks.json").read_text(encoding="utf-8"))
    days_of = {t["key"]: float(t["days"]) for t in extra["tasks"] if t.get("days")}
    rows = [r for r in csv.DictReader(io.open(DOCS / "tasks.csv", encoding="utf-8")) if r["type"] == "Task"]
    rows.sort(key=lambda r: (int(r["sequence"] or 0), r["key"]))
    track = {r["key"]: r["track"] for r in rows}
    service = {r["key"]: r["service"] for r in rows}

    def is_soft(r, d):
        if r["track"] == "Frontend":
            return track.get(d) in ("Backend", "Database")
        if r["track"] == "Backend":
            if d in SOFT_PLATFORM:
                return True
            # another service's task: the data this one reads or reports on
            return (track.get(d) == "Backend" and service.get(d) and service.get(d) != r["service"]
                    and not d.startswith(("PLATFORM-", "KERNEL-", "SETUP-", "MIG-")))
        return r["key"] == "PLATFORM-KERNEL" and d == "SETUP-AUTH"

    cursor, end, start, assign, busy = {}, {}, {}, {}, {}
    for r in rows:
        k, who = r["key"], r["assignee"]
        deps = [d for d in (r["dependsOn"] or "").split() if d in end]
        hard = [d for d in deps if not is_soft(r, d)]
        ready = max([end[d] for d in hard] or [0.0])
        if len(hard) < len(deps) and r["track"] != "Frontend":
            ready = max(ready, INTERFACES_DAY)
        wire = max([end[d] for d in deps if d not in hard] or [0.0])
        if not who or r["area"] == "client":
            start[k], end[k] = 0.0, 0.0
            continue
        if k in days_of:
            dur = days_of[k]
        else:
            dur = float(r["points"] or 0) / (PACE * float(pace_of.get(who, 1.0))) if r["points"] else 0.25
        # **A person who is waiting takes the next ticket that is ready** (30 September). Tasks are placed in
        # build order, each in its person's first free gap that starts after it is ready, so a ticket waiting on
        # somebody else no longer leaves its owner idle: the next ready ticket fills the gap, as it does on
        # ADAM's board ("the first ticket in that order that is not blocked").
        slots = busy.setdefault(who, [])
        s = ready
        for b0, b1 in slots:
            if s + dur <= b0 + 1e-9:
                break
            if s < b1:
                s = b1
        slots.append((s, s + dur))
        slots.sort()
        start[k], end[k] = s, max(s + dur, wire)
        cursor[who] = max(cursor.get(who, 0.0), s + dur)
        assign[k] = who
    out = {"note": ("Derived by tools/derive-block-a-schedule.py from tasks.csv (30 September 2026): build order, "
                    "dependencies, each person's pace. start = working days from Monday 5 October 2026; a start of 35 "
                    "or more is Block A's tail in B1."),
           "start": {k: round(v, 2) for k, v in start.items()}, "assign": assign}
    (DOCS / "block-a-schedule.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    tail = {}
    for k, v in start.items():
        if v >= 35 and assign.get(k):
            tail[assign[k]] = tail.get(assign[k], 0) + 1
    last = {}
    for k, v in end.items():
        if assign.get(k):
            last[assign[k]] = max(last.get(assign[k], 0), v)
    for w in sorted(last, key=lambda x: -last[x]):
        print(f"  {w:28} last day {last[w]:5.1f}  tasks starting after day 35: {tail.get(w, 0)}")
    print(f"  {len(start)} tasks -> handoff/service-docs/block-a-schedule.json")


if __name__ == "__main__":
    main()
