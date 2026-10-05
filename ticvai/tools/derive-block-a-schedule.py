# -*- coding: utf-8 -*-
"""Derive the schedule of every block from the plan: a start day, an owner and a sprint for every task.

    python tools/derive-block-a-schedule.py [--rebalance]   # writes handoff/service-docs/block-a-schedule.json

The name and the output file are kept from Block A's schedule (op-release.py, op-release-server.sh and
op-descriptions.py read it); since the replan of 1 October it covers Blocks A to D in two-week sprints.

**Why derived** (30 September). The schedule was reconstructed by hand on 27 September from ticket text, and
the re-derive of 30 September added 242 tasks it did not know. A schedule that has to be patched by hand after
every re-derive is one that is wrong after every re-derive.

A list scheduler over working days from Monday 5 October 2026 (tools/sprint_plan.py, shared with
build-service-docs.py so the owners it gave and the dates here agree):
- tasks in the plan's build order (`sequence` in plan-tasks.csv: block, app-module, phase, wave, chain, track);
- each on its owner, at the plan's pace (Block A as sized: 3,018 points, 35 days, 9 developers) times that
  person's pace in docs/active/team.json (`pace`, Surendra 0.6);
- never before every task it depends on (`dependsOn`) has ended, **except a front-end task on a back-end
  one**: screens build against the generated client and the mock server (SETUP-CLIENTS, SETUP-SEED), so the
  screen may start first and only its end waits for the back end it wires to;
- **soft platform waits** (30 September, Chinmay): a backend task may start before the platform kernel,
  idempotency and the outbox are finished, because it is written against their interfaces, which are
  published by day INTERFACES_DAY; the kernel may start before sign-in setup for the same reason; and a
  read-only or report task may start before the services whose data it reads, building against the seeded
  data. In each case only its end waits. Setup, migrations and the AI engine's setup stay hard;
- **a person who is waiting takes the next ticket that is ready**: each task goes in its owner's first free gap
  that starts after it is ready;
- AI engine tasks carry no points: their length is the engineer-days in block-a-extra-tasks.json (Block A) or
  plan-tasks.csv `days` (the AI review's capabilities, later blocks), never before the review's sprint for them;
- client tasks start on day 0 and hold no one.

**Owners** come from the plan (build-service-docs.py), which keeps a pushed ticket's owner from release
`sprintPlan.stableOwners.since` on (plan item L2) unless run with --rebalance. This script only times them; a
task the plan left without an owner is given one here the same way (whoever in its pool can start it first).

Output (working days from Monday 5 October 2026): start, end, assign, sprint (of its start), endSprint, block,
and the calendar: sprints with dates, blocks with their end and target, holidays.
"""
import csv
import io
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sprint_plan as sp  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"


def main():
    team = json.loads((ROOT / "docs" / "active" / "team.json").read_text(encoding="utf-8"))
    people, caps, _ = sp.load_team(team)
    settings = sp.sprint_settings(team)
    extra = json.loads((ROOT / "docs" / "active" / "block-a-extra-tasks.json").read_text(encoding="utf-8"))
    days_of = {t["key"]: float(t["days"]) for t in extra["tasks"] if t.get("days")}
    src = DOCS / "plan-tasks.csv"
    if not src.exists():
        src = DOCS / "tasks.csv"
    rows = [r for r in csv.DictReader(io.open(src, encoding="utf-8")) if r["type"] == "Task"]
    rows.sort(key=lambda r: (int(r["sequence"] or 0), r["key"]))
    pins, note = sp.pinned_owners(team, rebalance="--rebalance" in sys.argv[1:])
    # a service's owner: whoever carries most of its first-release back end (only used for a task with no owner)
    owners = Counter()
    for r in rows:
        if r["track"] == "Backend" and r["service"] and r.get("block", "A") == "A" and r["assignee"]:
            owners[(r["service"], r["assignee"])] += int(r["points"] or 0)
    svc_owner = {}
    for (svc, who), _ in sorted(owners.items(), key=lambda x: (-x[1], x[0])):
        svc_owner.setdefault(svc, who)

    def pool_of(r):
        if r["track"] == "AI":
            return "ai"
        if r["track"] == "Frontend":
            return {"POS": "pos", "MOB": "mob", "P05": "mob", "P06": "mob", "P07": "mob"}.get(r["area"], "web")
        return "web" if r["track"] == "Onboarding" else "be"

    # **The block-test windows** (docs/active/block-test-strategy.md): the last working days of each block's final
    # sprint, where the block test sits (TEST-BLOCK-<block>-BE/FE, placed by build-service-docs.py) and no new
    # feature work starts.
    freeze = {}
    for r in rows:
        if r["key"].startswith("TEST-BLOCK-") and r.get("notBefore"):
            w0 = float(r["notBefore"])
            freeze[r["block"]] = (w0, w0 + float(r.get("days") or sp.BLOCK_TEST_DAYS))
    # the tasks of a decided app-module scheduled after a block do not re-pace the pushed work (CHG-R4-003)
    late_ams = {a["key"] for a in extra.get("appModules") or [] if a.get("scheduleAfter")}
    items = [{"key": r["key"], "who": pins.get(r["key"]) or r["assignee"] or None, "pool": pool_of(r),
              "paceExclude": r.get("parent") in late_ams,
              "track": r["track"], "service": r["service"], "points": int(r["points"] or 0),
              "days": float(r.get("days") or 0) or days_of.get(r["key"]),
              "notBefore": float(r.get("notBefore") or 0), "deps": (r["dependsOn"] or "").split(),
              "client": r["area"] == "client", "block": r.get("block") or "A"} for r in rows]
    pace_at, pace_line, _ = sp.pace_model(team, items)
    res = sp.schedule(items, people, caps=caps, svc_owner=svc_owner,
                      backend_owners=(team.get("areas") or {}).get("backend") or [],
                      helper_share=team.get("helperShare") or {}, freeze=freeze,
                      open_blocks=settings["fixed"], pace_at=pace_at)
    # **AI engine tasks past 2 April stay unassigned** (Chinmay, 1 October): they are timed here like any task,
    # but the plan left them without an owner, so the schedule gives them none either
    unowned_ai = {r["key"] for r in rows if r["track"] == "AI" and not r["assignee"] and not pins.get(r["key"])}
    block = {r["key"]: r.get("block") or "A" for r in rows}
    ai_engine = {r["key"] for r in rows if r["track"] == "AI" and r["block"] != "A"}
    placed = {k: v for k, v in res.items() if v["who"]}
    assigned = {k: v["who"] for k, v in placed.items() if k not in unowned_ai}
    b_end, b_ai = defaultdict(float), defaultdict(float)
    for k, v in placed.items():
        if k.startswith("TEST-BLOCK-"):
            continue
        if k in ai_engine or (k.startswith("TEST-AM-AI-ENGINE-") and block[k] != "A"):
            b_ai[block[k]] = max(b_ai[block[k]], v["end"])
        else:
            b_end[block[k]] = max(b_end[block[k]], v["end"])
    blocks = {}
    for b in sp.BLOCKS:
        if b not in b_end and b not in b_ai:
            continue
        if b not in b_end:            # a block of AI engine work only (A2 since CHG-RONEP-010): it ends on its target
            b_end[b] = float(sp.window_of(settings["targets"][b])[0])
        t = settings["targets"][b]
        w = freeze.get(b)
        # the block's final sprint: the one its test window is in (build-service-docs.py placed it after the work)
        n = sp.sprint_of_index(w[0]) if w else sp.final_sprint(b_end[b])
        normal = sp.final_sprint(b_end[b], sp.BLOCK_TEST_DAYS, at_least=1)       # where it would end at normal hours
        bt = [v for k, v in placed.items() if k.startswith(f"TEST-BLOCK-{b}-")]
        blocks[b] = {"lastDay": sp.day(max(b_end[b] - 1e-6, 0.0)).isoformat(), "endSprint": n,
                     "endsOn": sp.SPRINTS_ALL[n - 1]["end"].isoformat(), "targetSprint": t,
                     "targetEndsOn": sp.SPRINTS_ALL[t - 1]["end"].isoformat(),
                     "testFrom": sp.day(w[0]).isoformat() if w else "", "testTo": sp.day(w[1] - 1).isoformat() if w else "",
                     "testEnds": sp.day(max(max((v["end"] for v in bt), default=0.0) - 1e-6, 0)).isoformat() if bt else "",
                     "aiEngineLastDay": sp.day(max(b_ai[b] - 1e-6, 0.0)).isoformat() if b in b_ai else "",
                     "fixed": b in settings["fixed"], "normalEndSprint": max(normal, n if b not in settings["fixed"] else 1),
                     "normalEndsOn": sp.SPRINTS_ALL[max(normal, n if b not in settings["fixed"] else 1) - 1]["end"].isoformat()}
    out = {"note": ("Derived by tools/derive-block-a-schedule.py from plan-tasks.csv (the sprint plan of 1 October): "
                    "build order, dependencies, each person's pace, two-week sprints. start and end = working days "
                    "from Monday 5 October 2026; sprint = the sprint a task starts in (Sprint 1 = 5-16 Oct 2026, "
                    "Sprint 13 = 22 Mar-2 Apr 2027; a sprint past 13 is past the six months). " + note),
           "start": {k: round(v["start"], 2) for k, v in res.items()},
           "end": {k: round(v["end"], 2) for k, v in res.items()},
           "assign": assigned,
           "duration": {k: round(v.get("dur") or 0.0, 3) for k, v in placed.items()},
           "pace": pace_line,
           "sprint": {k: sp.sprint_of_index(v["start"]) for k, v in placed.items()},
           "endSprint": {k: sp.sprint_of_index(max(v["end"] - 1e-6, 0.0)) for k, v in placed.items()},
           "block": block,
           "sprints": [{"n": s_["n"], "name": s_["name"], "start": s_["start"].isoformat(),
                        "end": s_["end"].isoformat(), "days": s_["days"]} for s_ in sp.SPRINTS],
           "blocks": blocks, "freeze": {b: list(w) for b, w in freeze.items()},
           "holidays": {d.isoformat(): n for d, n in sp.HOLIDAYS.items()}}
    (DOCS / "block-a-schedule.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    last = {}
    for k, v in placed.items():
        last[v["who"]] = max(last.get(v["who"], 0), v["end"])
    for w in sorted(last, key=lambda x: -last[x]):
        lw = max(last[w] - 1e-6, 0)
        print(f"  {w:28} last day {sp.day(lw).isoformat()} (Sprint {sp.sprint_of_index(lw)})")
    for b, x in blocks.items():
        print(f"  Block {b}: ends {x['endsOn']} (Sprint {x['endSprint']}; target Sprint {x['targetSprint']}, "
              f"{x['targetEndsOn']}); last work {x['lastDay']}; block test {x['testFrom']} to {x['testTo']}"
              + (f" (it ends {x['testEnds']})" if x['testEnds'] and x['testEnds'] > x['testTo'] else "")
              + (f"; AI engine to {x['aiEngineLastDay']}" if x['aiEngineLastDay'] else ""))
    print(f"  owners: {note}")
    print(f"  {len(res)} tasks -> handoff/service-docs/block-a-schedule.json")


if __name__ == "__main__":
    main()
