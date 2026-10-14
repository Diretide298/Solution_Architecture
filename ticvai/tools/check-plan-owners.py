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
  O-NO-TAKEOVER    a module test the last release gave someone `neverTests` names, now owned, in the plan or the
                   schedule, by someone team.json `noTestTakeover` names (Surendra; CHG-R5-005)
  O-MOVE           a task block-a-extra-tasks.json `ownerMoves` moves (CHG-R5-003) still owned, in the plan or the
                   schedule, by the person it leaves, or by anyone but the person it goes to
  O-LEFT           (15 October 2026, CHG-PPL-001: Tanmay Dukhande left, Narayan Gaonkar took his place) a task owned or
                   accountable, in the plan or the schedule, by someone team.json `successors` says has left; a
                   leaver still in team.json's areas, onboard, pace, people, helpers, serviceOwners or the
                   block-a-extra-tasks.json pins (moduleTestPeers, ownerMoves `to`); or a successor not on the roster
  O-SVC-OWNER      (15 October 2026, CHG-PPL-002: "keep hrushikant" for LedgerService) a back-end, database or setup
                   task of a service team.json `serviceOwners` fixes whose accountable (its reviewing owner) is anyone
                   but that owner

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
    "O-NO-TAKEOVER": "a module test given up by someone who never tests, taken by someone team.json noTestTakeover keeps off it (CHG-R5-005)",
    "O-LEFT": "work or a pin still on someone who left the team (team.json successors; CHG-PPL-001)",
    "O-SVC-OWNER": "a fixed service's back end reviewed by anyone but its fixed owner (team.json serviceOwners; CHG-PPL-002)",
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
    # **Nor to these** (CHG-R5-005, 7 October: Surendra takes none of the module tests Hrushikant gives up). The last
    # release's owners say who gave a test up; once a release pushes the new owners the rule has nothing left to check.
    no_take = sp.no_test_takeover(team)
    pins, _ = sp.pinned_owners(team)
    for r in rows:
        if r["type"] == "Task" and r["key"].startswith("TEST-AM-") and pins.get(r["key"]) in never:
            for where, who in (("plan", r["assignee"]), ("schedule", assign.get(r["key"]))):
                if who in no_take:
                    guard.add("O-NO-TAKEOVER", f"{r['key']}:{where}",
                              f"{r['key']} is {who}'s in the {where}, given up by {pins[r['key']]}; "
                              f"noTestTakeover keeps {who} off it (CHG-R5-005)")
    n_left = check_left(guard, team, extra, rows, assign)
    n_svc = check_service_owners(guard, team, rows)
    guard.note(f"{n_left} people left the team (successors), {n_svc} back-end tasks of fixed services checked")
    guard.note(f"{n_tests} module tests, {len(phase2)} phase 2 app-modules of the AI engine, "
               f"{n_mig} migration tasks ({mig_owner or 'no owner'}'s)")
    return guard.finish()


def check_left(guard, team, extra, rows, assign) -> int:
    """O-LEFT (CHG-PPL-001; Chinmay, 15 October 2026: "tanmay is leaving so shift all tasks to narayan"): nothing stays on
    a person who left, in the plan, the schedule or the inputs that place work."""
    succ = sp.successors(team)
    if not succ:
        return 0
    for r in rows:
        if r["type"] != "Task":
            continue
        for where, field, who in (("plan", "owner", r["assignee"]), ("plan", "accountable", r.get("accountable")),
                                  ("schedule", "owner", assign.get(r["key"]))):
            if who in succ:
                guard.add("O-LEFT", f"{r['key']}:{where}:{field}",
                          f"{r['key']}: {who} is its {field} in the {where} but left; {succ[who]} took their place")
    places = [("areas." + a, set(ws)) for a, ws in (team.get("areas") or {}).items()]
    places += [(f, set(team.get(f) or {})) for f in ("onboard", "pace", "helpers", "backendHelpers", "helperShare",
                                                     "neverTests", "noTestTakeover")]
    places += [("people", {p.get("name") for p in team.get("people") or []}),
               ("serviceOwners", set((team.get("serviceOwners") or {}).values())),
               ("migrations.owner", {(team.get("migrations") or {}).get("owner")}),
               ("venueManagement.who", set((team.get("venueManagement") or {}).get("who") or [])),
               ("ai.who", set((team.get("ai") or {}).get("who") or [])),
               ("block-a-extra-tasks.json moduleTestPeers", set((extra.get("moduleTestPeers") or {}).values())),
               ("block-a-extra-tasks.json ownerMoves to", {to for _, to in sp.owner_moves(extra).values()})]
    roster = {p.get("name") for p in team.get("people") or []}
    for who, new in sorted(succ.items()):
        for name, held in places:
            if who in held:
                guard.add("O-LEFT", f"team:{who}:{name}", f"{who} left (successor {new}) but is still in {name}")
        if new not in roster:
            guard.add("O-LEFT", f"team:{who}:successor", f"{who}'s successor {new} is not in team.json people")
    return len(succ)


def check_service_owners(guard, team, rows) -> int:
    """O-SVC-OWNER (CHG-PPL-002; Chinmay, 15 October 2026: "keep hrushikant"): a service the lead fixed is reviewed by
    its fixed owner, whatever the load balancer would give it."""
    fixed = sp.service_owners(team)
    n = 0
    for r in rows:
        if r["type"] == "Task" and r["service"] in fixed and r["track"] in ("Backend", "Database", "DevOps", "Setup",
                                                                             "Onboarding"):
            n += 1
            if r.get("accountable") != fixed[r["service"]]:
                guard.add("O-SVC-OWNER", r["key"], f"{r['key']} ({r['service']}) is reviewed by "
                          f"{r.get('accountable') or 'nobody'}, not {fixed[r['service']]} (serviceOwners, CHG-PPL-002)")
    return n


if __name__ == "__main__":
    sys.exit(main())
