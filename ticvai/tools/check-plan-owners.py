#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module test is never tested by its app-module's main builder, phase 2 of the AI engine has no owner, and every
migration is the migration owner's.

**6 October 2026, CHG-R4-005 and CHG-R4-006.** The test strategy (docs/active/block-test-strategy.md, 1 October) gives
each app-module's module test to "a peer in its stack who is not its main builder"; the scheduler skipped the main
builder only for a test with no owner yet, so a pinned or planned owner went through: TEST-AM-APPROVALS-P08-BLOCK-A was
Hrushikant Patkar's and TEST-AM-AI-ENGINE-A2 Kalpita Mejari's, each the main builder of what they tested. And phase 2
of the AI engine (docs/active/ai-phase-plan.json, CHG-AIPH-001: "starts after 2 April, has no owner") still had its
three module tests and its app-modules assigned in the schedule.

**What fails** (handoff/service-docs/plan-tasks.csv, handoff/service-docs/block-a-schedule.json,
docs/active/ai-phase-plan.json):

  O-SELF-TEST      a module test (TEST-AM-*) owned, in the plan or the schedule, by its app-module's main builder (the
                   most points; an AI task counts its days at the plan's pace)
  O-PHASE2-OWNED   an AI unit, a module test or the app-module of a phase 2 module of the AI engine has an owner, in the
                   plan or the schedule
  O-MIG-OWNER      a migration task (team.json `migrations`: its key pattern, ^MIG- since CHG-R5-001 on 7 October) owned,
                   in the plan or the schedule, by anyone but the migration owner, or team.json has no such rule. Its
                   table sub-tasks take their task's owner (op-release.py), so the task is the one checked.
  O-NO-CHECKER     a module test (TEST-AM-*) owned, in the plan or the schedule, by someone team.json `neverTests` names
                   (Hrushikant Patkar, never a checker; CHG-R5-004)
  O-MOVE           a task block-a-extra-tasks.json `ownerMoves` moves (CHG-R5-003) still owned, in the plan or the
                   schedule, by the person it leaves, or by anyone but the person it goes to

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-plan-owners.py [--all]
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
import sprint_plan as sp  # noqa: E402
import ticket_done as td  # noqa: E402

RULES = {
    "O-SELF-TEST": "a module test owned by its app-module's main builder (block-test-strategy; CHG-R4-005)",
    "O-PHASE2-OWNED": "phase 2 of the AI engine has an owner, against ai-phase-plan.json (CHG-AIPH-001; CHG-R4-006)",
    "O-MIG-OWNER": "a migration task not owned by the migration owner of team.json (CHG-R5-001)",
    "O-MOVE": "a task the lead's ownerMoves moves not owned by the person it goes to (CHG-R5-003)",
    "O-NO-CHECKER": "a module test owned by someone who never tests (team.json neverTests; CHG-R5-004)",
}
SD = Path("handoff") / "service-docs"


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-plan-owners", RULES)
    plan = g.ROOT / SD / "plan-tasks.csv"
    if not plan.exists():
        guard.note("plan-tasks.csv missing: run tools/build-service-docs.py")
        return guard.finish()
    with plan.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    sched = g.load_json(g.ROOT / SD / "block-a-schedule.json", {}) or {}
    assign = sched.get("assign") or {}
    kids = defaultdict(list)
    for r in rows:
        kids[r["parent"]].append(r)
    team = g.load_json(g.ROOT / "docs" / "active" / "team.json", {}) or {}
    ai_lead = ((team.get("ai") or {}).get("who") or [""])[0]
    extra = g.load_json(g.ROOT / "docs" / "active" / "block-a-extra-tasks.json", {}) or {}
    days_of = {t["key"]: float(t["days"]) for t in extra.get("tasks") or [] if t.get("days")}
    phase = g.load_json(g.ROOT / "docs" / "active" / "ai-phase-plan.json", {}) or {}
    phase2 = {m["key"] for m in phase.get("modules") or [] if m.get("phase") == 2 and m.get("key")}
    n_tests = 0
    for r in rows:
        k = r["key"]
        if k.startswith("TEST-AM-") and r["parent"] not in phase2:
            n_tests += 1
            builder = td.main_builder([x for x in kids[r["parent"]] if x["type"] == "Task"], sp.PLAN_PACE,
                                     ai_lead, days_of)
            for where, who in (("plan", r["assignee"]), ("schedule", assign.get(k))):
                if builder and who == builder:
                    guard.add("O-SELF-TEST", f"{k}:{where}", f"{k}: {who} tests in the {where} what they built most of "
                              f"({r['parent']})")
        if r["parent"] in phase2 and r["track"] in ("AI", "Test") or k in phase2:
            for where, who in (("plan", r["assignee"]), ("schedule", assign.get(k))):
                if who:
                    guard.add("O-PHASE2-OWNED", f"{k}:{where}", f"{k} (phase 2 of the AI engine) is {who}'s in the {where}")
    # **Every migration is one person's** (CHG-R5-001, 7 October: "shift all the migration tickets to Hrushikant"):
    # the owner a pushed ticket keeps from the last release does not hold against it.
    mig_owner, mig_rx = sp.migration_owner(team)
    n_mig = 0
    if not mig_owner:
        guard.add("O-MIG-OWNER", "team.json", "docs/active/team.json has no `migrations` owner (CHG-R5-001)")
    else:
        for r in rows:
            if r["type"] != "Task" or not sp.is_migration_of(mig_rx, r["key"]):
                continue
            n_mig += 1
            for where, who in (("plan", r["assignee"]), ("schedule", assign.get(r["key"]))):
                if who != mig_owner:
                    guard.add("O-MIG-OWNER", f"{r['key']}:{where}",
                              f"{r['key']} is {who or 'nobody'}'s in the {where}, not {mig_owner}'s (CHG-R5-001)")
    # **The lead's owner moves hold** (CHG-R5-003, 7 October): the rebalance that keeps Block A's r2 dates once the
    # migrations are one person's.
    by_key = {r["key"]: r for r in rows}
    moves = sp.owner_moves(extra)
    for k, (frm, to) in sorted(moves.items()):
        r = by_key.get(k)
        if r is None:
            guard.note(f"ownerMoves names {k}, which is not in the plan")
            continue
        for where, who in (("plan", r["assignee"]), ("schedule", assign.get(k))):
            if who != to:
                guard.add("O-MOVE", f"{k}:{where}", f"{k} is {who or 'nobody'}'s in the {where}; ownerMoves gives it "
                                                    f"to {to} (from {frm}, CHG-R5-003)")
    guard.note(f"{len(moves)} owner moves")
    # **Never a checker** (CHG-R5-004, 7 October: Hrushikant Patkar tests no module): team.json `neverTests`.
    never = sp.never_testers(team)
    for r in rows:
        if r["type"] == "Task" and r["key"].startswith("TEST-AM-"):
            for where, who in (("plan", r["assignee"]), ("schedule", assign.get(r["key"]))):
                if who in never:
                    guard.add("O-NO-CHECKER", f"{r['key']}:{where}",
                              f"{r['key']} is {who}'s in the {where}, who never tests (neverTests, CHG-R5-004)")
    guard.note(f"{n_tests} module tests, {len(phase2)} phase 2 app-modules of the AI engine, "
               f"{n_mig} migration tasks ({mig_owner or 'no owner'}'s)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
