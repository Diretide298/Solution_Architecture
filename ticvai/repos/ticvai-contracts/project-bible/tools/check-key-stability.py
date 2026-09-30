#!/usr/bin/env python3
"""A plan change must never again make a second OpenProject ticket for work that already has one.

**30 September 2026.** Work moved between key prefixes -- a Venue Management screen became a Block A setup
screen (VM-BO-005 -> APP-SETUP-BO-005), operations moved between SVC- and VM-, a schema's migration moved
from VM-MIG- to MIG- -- and the push made 25 second tickets for work that had one (closed afterwards by
tools/op-retire.py). A split re-numbered SVC-WALLET-RETAIL-1, so its ticket was matched to the wrong half.
`build-service-docs.py` now reconciles every key against pms-map.json (`reconcile_keys`); this checks it.

Reads handoff/service-docs/tasks.csv and pms-map.json and fails on:

  duplicate   a planned key with no ticket whose work -- the screen id, an operation, a table -- is
              already on a pushed ticket that has left the plan and is not closed. Pushing it would
              make the second ticket.
  unstable    a planned key the generator's own reconciliation would write differently: tasks.csv is
              older than the generator, or was edited by hand.

and reports without failing: a new key whose work sits on a sub-task of a ticket still in the plan (the
work moved between two live tickets, which a person moves), or on a ticket op-retire closed.

Then it proves the reconciliation on copies of the plan and the map, in memory: a screen moved between
prefixes, a split that re-numbered its parts, a migration and operations moved between Block A and Venue
Management, a genuinely new group, and a closed ticket that must not be reopened.

    python3 tools/check-key-stability.py [--tasks PATH] [--map PATH]   (defaults: the files above)
"""
import argparse
import csv
import importlib.util
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"

_spec = importlib.util.spec_from_file_location("build_service_docs", ROOT / "tools" / "build-service-docs.py")
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)


def plan_work(rows):
    """natural key -> its work, read back from tasks.csv the way the generator formed it."""
    work = {}
    for r in rows:
        k, ident = r["key"], gen.key_identity(r["key"])
        if r["type"] != "Task" or not ident:
            continue
        if ident[0] == "screen":
            work[k] = {ident[1]}
        elif ident[0] == "ops":
            m = re.search(r"Operations(?: beyond the first release)?: ([^.]+)\.", r["description"])
            if m:
                work[k] = {o.strip() for o in m.group(1).split(",")}
        elif ident[0] == "tables":
            m = re.search(r"Tables: (.+?)\. Source", r["description"])
            if m:
                work[k] = {t.strip() for t in m.group(1).split(",")}
    return work


def check(rows, mp, closed):
    """(errors, notes) for one plan and one map."""
    planned = {r["key"] for r in rows}
    work = plan_work(rows)
    pitems = gen.pushed_items(mp)
    errors, notes = [], []
    for k in sorted(planned - set(pitems)):
        if k not in work:
            continue
        kind, fam = gen.key_identity(k)
        for p in sorted(pitems):
            ident = gen.key_identity(p)
            if not ident or ident[0] != kind:
                continue
            same = work[k] & pitems[p] if kind != "screen" else ({fam} if ident[1] == fam else set())
            if kind == "tables" and ident[1] == fam and p not in planned:
                same = same or {f"schema {fam}"}
            if not same:
                continue
            what = ", ".join(sorted(same)[:4]) + (" ..." if len(same) > 4 else "")
            if p in closed:
                notes.append(f"{k}: {what} was on #{mp[p]} {p}, closed by op-retire; a new ticket is right")
            elif p in planned:
                notes.append(f"{k}: {what} is a sub-task of #{mp[p]} {p}, still in the plan; move the sub-task")
            else:
                errors.append(f"duplicate  {k} is new, but {what} is already on #{mp[p]} {p}, which left the plan")
    fixed = planned - set(work)
    final, _ = gen.reconcile_keys(work, fixed, mp, closed)
    for k, v in sorted(final.items()):
        if k != v:
            errors.append(f"unstable   {k} would be written as {v} ("
                          + (f"ticket #{mp[v]}" if v in mp else "no ticket yet") + "): re-run build-service-docs.py")
    return errors, notes


def self_test(rows, mp):
    """Each case edits copies of today's plan and map into a state the plan has been in, and asserts the key
    the reconciliation gives. Returns [(case, ok, detail)]."""
    work = plan_work(rows)
    fixed = {r["key"] for r in rows} - set(work)

    def without(m, *keys):
        return {k: v for k, v in m.items() if k.partition("#")[0] not in keys}

    def run(w, m, closed=frozenset()):
        return gen.reconcile_keys(w, fixed, m, closed)[0]

    out = []

    def case(name, got, want):
        out.append((name, got == want, f"got {got}, want {want}"))

    # 1. A Venue Management screen becomes a Block A setup screen: the plan forms APP-SETUP-BO-005, and the
    # map holds the ticket pushed as VM-BO-005 (open, as it was before op-retire closed it).
    if "APP-SETUP-BO-005" in work and "VM-BO-005" in mp:
        f = run(work, without(mp, "APP-SETUP-BO-005"))
        case("screen moved VM -> APP-SETUP keeps its ticket", f["APP-SETUP-BO-005"], "VM-BO-005")
        # 7. ...unless that ticket was closed: a Rejected ticket is not reopened for the work.
        f = run(work, without(mp, "APP-SETUP-BO-005"), frozenset({"VM-BO-005"}))
        case("closed ticket is not reused", f["APP-SETUP-BO-005"], "APP-SETUP-BO-005")
    # 2. A split re-numbers its parts: the map as it was before the split, SVC-WALLET-RETAIL-1 carrying
    # transferWalletBalance; the plan now puts four other operations in -1 and transferWalletBalance in -2.
    a, b = "SVC-WALLET-RETAIL-1", "SVC-WALLET-RETAIL-2"
    if a in work and b in work and "transferWalletBalance" in work[b]:
        m = without(mp, a, b)
        m[a], m[a + "#transferWalletBalance"] = mp[a], mp.get(b + "#transferWalletBalance", 1)
        f = run(work, m)
        case("split: transferWalletBalance keeps SVC-WALLET-RETAIL-1", f[b], a)
        case("split: the new half takes a number nobody pushed", f[a], b)
    # 3. A schema's migration moves from Venue Management to Block A: MIG-SEATING is formed, VM-MIG-SEATING
    # was pushed (open).
    if "MIG-SEATING" in work and "VM-MIG-SEATING" in mp:
        f = run(work, without(mp, "MIG-SEATING"))
        case("migration moved VM-MIG -> MIG keeps its ticket", f["MIG-SEATING"], "VM-MIG-SEATING")
    # 4. Operations move from Block A to Venue Management: VM-CATALOGUE-UPSELL-1 is formed, the upsell
    # operations were pushed as SVC-CATALOGUE-UPSELL-1 (open).
    if "VM-CATALOGUE-UPSELL-1" in work and "SVC-CATALOGUE-UPSELL-1" in mp:
        f = run(work, without(mp, "VM-CATALOGUE-UPSELL-1"))
        case("operations moved SVC -> VM keep their ticket", f["VM-CATALOGUE-UPSELL-1"], "SVC-CATALOGUE-UPSELL-1")
    # 5. A genuinely new group whose natural number was pushed for operations that have left the plan: it
    # is new work, so it takes a fresh number, and the old ticket is left for op-retire to explain.
    if b in work:
        w = dict(work)
        w["SVC-WALLET-RETAIL-3"] = {"brandNewOperation"}
        m = dict(mp)
        m["SVC-WALLET-RETAIL-3"], m["SVC-WALLET-RETAIL-3#retiredOperation"] = 1, 2
        f = run(w, m)
        case("new group avoids a number pushed for other work", f["SVC-WALLET-RETAIL-3"], "SVC-WALLET-RETAIL-4")
    # 6. Today's plan against today's map moves nothing.
    f = run(work, mp)
    case("today's plan keeps every key", sum(1 for k, v in f.items() if k != v), 0)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default=str(DOCS / "tasks.csv"))
    ap.add_argument("--map", default=str(DOCS / "pms-map.json"))
    a = ap.parse_args()
    with open(a.tasks, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    mp = json.loads(Path(a.map).read_text(encoding="utf-8"))
    closed = gen.closed_keys()
    errors, notes = check(rows, mp, closed)
    planned = {r["key"] for r in rows}
    pushed = set(gen.pushed_items(mp))
    print(f"plan {len(planned)} keys, {len(planned & pushed)} with a ticket, {len(planned - pushed)} new; "
          f"{len(pushed - planned)} pushed keys out of the plan")
    for n in notes:
        print(f"  note       {n}")
    for e in errors:
        print(f"  {e}")
    tests = self_test(rows, mp)
    for name, ok, detail in tests:
        print(f"  test {'ok  ' if ok else 'FAIL'} {name}" + ("" if ok else f": {detail}"))
    failed = [t for t in tests if not t[1]]
    if errors or failed:
        print(f"FAIL: {len(errors)} key(s) would duplicate or move a ticket, {len(failed)} self-test(s) failed")
        return 1
    print(f"PASS: no new key's work is already on a pushed ticket; {len(tests)} reconciliation tests pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
