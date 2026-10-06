#!/usr/bin/env python3
"""A plan change must never again make a second OpenProject ticket for work that already has one.

**30 September 2026.** Work moved between key prefixes -- a Venue Management screen became a Block A setup
screen (VM-BO-005 -> APP-SETUP-BO-005), operations moved between SVC- and VM-, a schema's migration moved
from VM-MIG- to MIG- -- and the push made 25 second tickets for work that had one (closed afterwards by
tools/op-retire.py). A split re-numbered SVC-WALLET-RETAIL-1, so its ticket was matched to the wrong half.
`build-service-docs.py` now reconciles every key against pms-map.json (`reconcile_keys`); this checks it.

**A pushed key is the ticket's identity and is never renamed** (council of 1 October, plan item 1C, C4):
a move between module prefixes (VM- / SVC- / APP-SETUP- / MIG-) is metadata, and the generator keeps the
pushed key for the moved work. **A rename is therefore a reconciliation that failed, and it blocks.**

Reads handoff/service-docs/tasks.csv and pms-map.json and fails on:

  renamed     a pushed key that has left the plan, is not closed and is not retired in op-retire.py, whose
              work -- the screen id, an operation, a table -- now appears under a different planned key.
              With a new key, pushing it would make the second ticket (the 25 duplicates of 30 September);
              with a key that already has a ticket, the old ticket is left open carrying work that is
              built elsewhere. Either way the planned key differs from the pushed key for the same work.
  unstable    a planned key the generator's own reconciliation would write differently: tasks.csv is
              older than the generator, or was edited by hand.

and reports without failing: a new key whose work sits on a sub-task of a ticket still in the plan (a split:
the new key is new work linked to its parent, and a person moves the sub-task), or on a ticket op-retire
closed. A ticket op-retire retires (merged or deferred, with its reason) has left the plan on purpose.

Then it proves the reconciliation on copies of the plan and the map, in memory: a screen moved between
prefixes, a split that re-numbered its parts, a migration and operations moved between Block A and Venue
Management, a genuinely new group, and a closed ticket that must not be reopened. **And it proves the
block**: a plan written with a renamed key, and a plan that moved a ticket's work into another ticket
without retiring it, must both fail; the same prefix move written under the pushed key must pass.

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


def retired_keys(mp) -> frozenset:
    """Pushed keys tools/op-retire.py takes out of the plan with a reason: every key it names (merged or
    deferred), and every key of a screen it defers or merges. Such a ticket left the plan on purpose."""
    try:
        spec = importlib.util.spec_from_file_location("op_retire", ROOT / "tools" / "op-retire.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception:
        return frozenset()
    sids = list(mod.DEFERRED) + list(mod.MERGED)
    out = set(mod.OTHER)
    # A ticket replaced by another (op-retire.py REPLACED, r2; CHG-CLN-002) is retired too: its work was removed
    # from the contract, so it is not "renamed" whatever key now builds the record.
    out |= set(getattr(mod, "REPLACED", {})) | set(getattr(mod, "MERGED_R2", {}))
    for k in mp:
        if "#" not in k and any(re.search(rf"-{re.escape(s)}$", k) for s in sids):
            out.add(k)
    return frozenset(out)


def overlap(kind, fam, work_k, p, pitems):
    ident = gen.key_identity(p)
    if not ident or ident[0] != kind:
        return set()
    if kind == "screen":
        return {fam} if ident[1] == fam else set()
    same = work_k & pitems[p]
    if kind == "tables" and ident[1] == fam:
        same = same or {f"schema {fam}"}
    return same


def check(rows, mp, closed, retired=frozenset()):
    """(errors, notes) for one plan and one map."""
    planned = {r["key"] for r in rows}
    work = plan_work(rows)
    pitems = gen.pushed_items(mp)
    errors, notes = [], []
    # **A pushed ticket whose work is now under another key that already has a ticket.** The loop below
    # only looks at new keys; this is the other half of a rename: the old ticket is left open, carrying
    # work somebody builds under a different ticket, with nothing in the plan saying so.
    for p in sorted(set(pitems) - planned):
        if p in closed or p in retired or not gen.key_identity(p):
            continue
        for k in sorted(planned & set(pitems)):
            if k not in work:
                continue
            kind, fam = gen.key_identity(k)
            same = overlap(kind, fam, work[k], p, pitems)
            if same:
                what = ", ".join(sorted(same)[:4]) + (" ..." if len(same) > 4 else "")
                errors.append(f"renamed    #{mp[p]} {p} left the plan, and its work {what} is now under {k}: "
                              f"keep {p} for that work (moves are metadata), or retire {p} in op-retire.py "
                              "with the reason")
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
            if (p in closed or p in retired) and p not in planned and kind != "screen" and pitems[p] == work[k]:
                # CHG-R4-010 (6 October): op-retire.py closes keys for the work they had before the fresh r1; one
                # pushed again for exactly this work is the same ticket, not a closed one (SVC-CATALOGUE-DRAFTED-3).
                errors.append(f"renamed    {k} is new, but its work {what} is exactly #{mp[p]} {p}, which op-retire "
                              f"closes for older work: {p} is the key for it (pushing {k} makes a second ticket)")
            elif p in closed:
                notes.append(f"{k}: {what} was on #{mp[p]} {p}, closed by op-retire; a new ticket is right")
            elif p in planned:
                notes.append(f"{k}: {what} is a sub-task of #{mp[p]} {p}, still in the plan; move the sub-task")
            else:
                errors.append(f"renamed    {k} is new, but {what} is already on #{mp[p]} {p}, which left the "
                              f"plan: {p} is the key for that work (pushing {k} makes a second ticket)")
    fixed = planned - set(work)
    final, _ = gen.reconcile_keys(work, fixed, mp, closed)
    for k, v in sorted(final.items()):
        if k != v:
            errors.append(f"unstable   {k} would be written as {v} ("
                          + (f"ticket #{mp[v]}" if v in mp else "no ticket yet") + "): re-run build-service-docs.py")
    return errors, notes


def self_test(rows, mp, closed=frozenset(), retired=frozenset()):
    """Each case edits copies of today's plan and map into a state the plan has been in, and asserts the key
    the reconciliation gives. Returns [(case, ok, detail)]."""
    work = plan_work(rows)
    fixed = {r["key"] for r in rows} - set(work)
    if not gen.pushed_items(mp):
        # **A fresh start pushes nothing yet** (Chinmay, 3 October, CHG-GTR-001): r1 goes into a new OpenProject
        # project and pms-map.json starts empty (project 153's map is in service-docs/archive/). The cases
        # below edit a map of pushed tickets, so they run on today's plan as if all of it had been pushed: every
        # task with an id, and an ops or tables task's work as its KEY#item sub-tasks, as push-openproject.py
        # records them. Case 2 used to read the real map and died on a KeyError with an empty one.
        mp, n = {}, 0
        for r in rows:
            n += 1
            mp[r["key"]] = n
            if r["key"] in work and gen.key_identity(r["key"])[0] != "screen":
                for item in sorted(work[r["key"]]):
                    n += 1
                    mp[f"{r['key']}#{item}"] = n

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
        # the next number nobody pushed and no other planned task holds (more planned work can hold 4 already)
        n = 4
        while f"SVC-WALLET-RETAIL-{n}" in m or f"SVC-WALLET-RETAIL-{n}" in w or f"SVC-WALLET-RETAIL-{n}" in fixed:
            n += 1
        case("new group avoids a number pushed for other work", f["SVC-WALLET-RETAIL-3"], f"SVC-WALLET-RETAIL-{n}")
    # 6. Today's plan against today's map moves nothing -- with the keys op-retire closes, as the generator runs it
    # (a key closed as replaced, CHG-CLN-002, is never handed to other work).
    f = run(work, mp, closed)
    case("today's plan keeps every key", sum(1 for k, v in f.items() if k != v), 0)

    # 8-12. **The block** (C4, 1 October): these run check() itself, on a plan and a map edited in memory.
    # Each picks its ticket from today's plan, so it does not depend on one key surviving the next plan.
    def other_prefix(k):
        for a, b in (("SVC-", "VM-"), ("VM-", "SVC-"), ("APP-SETUP-", "VM-")):
            if k.startswith(a):
                return b + k[len(a):]
        return None

    def rekey(m, old, new):
        return {(new + k[len(old):] if k == old or k.startswith(old + "#") else k): v for k, v in m.items()}

    def rows_with(rs, old, new):
        return [dict(r, key=new) if r["key"] == old else r for r in rs]

    planned = {r["key"] for r in rows}
    pit = gen.pushed_items(mp)
    renamed = [k for k in sorted(work) if k in pit and gen.key_identity(k)[0] in ("ops", "screen")
               and (gen.key_identity(k)[0] == "screen" or pit[k] & work[k])
               and other_prefix(k) and other_prefix(k) not in mp and other_prefix(k) not in planned
               and gen.key_identity(other_prefix(k)) == gen.key_identity(k)]
    for kind in ("ops", "screen"):
        k = next((x for x in renamed if gen.key_identity(x)[0] == kind), None)
        if not k:
            continue
        nk = other_prefix(k)
        # 8. tasks.csv written with the work under a new prefix, the pushed key dropped: blocked.
        errs, _ = check(rows_with(rows, k, nk), mp, closed, retired)
        case(f"{kind} renamed {k} -> {nk} is blocked", any(e.startswith("renamed") and k in e for e in errs), True)
        # 9. The same move, pushed under the other prefix and written under the pushed key: metadata, passes.
        m = rekey(mp, k, nk)
        errs, _ = check(rows_with(rows, k, nk), m, closed, retired)
        case(f"{kind} moved {k} -> {nk} under its pushed key passes", errs, [])
        # 10. ...because the generator gives the natural key (the new prefix) the pushed one.
        case(f"{kind} moved: reconciliation writes {k} as pushed {nk}", run(work, m).get(k), nk)
    # 11. A ticket's operations folded into another planned ticket, the first dropped from the plan without
    # op-retire saying why: blocked. 12. ...and with op-retire's reason, it passes.
    # The one moved has a single operation and the one receiving it several, so the receiving ticket keeps
    # its key under the reconciliation and only the dropped one is at stake.
    # (keys op-retire already names are left out: their leaving the plan has a reason, so it cannot be the case)
    ops = [x for x in sorted(work) if x in pit and gen.key_identity(x)[0] == "ops" and x not in retired]
    a = next((x for x in ops if len(pit[x] & work[x]) == 1), None)
    b = next((x for x in ops if x != a and len(pit[x] & work[x]) >= 2), None)
    if a and b:
        moved = sorted(work[a] | work[b])
        rs = []
        for r in rows:
            if r["key"] == a:
                continue
            if r["key"] == b:
                r = dict(r, description=f"Operations: {', '.join(moved)}. Spec: test.")
            rs.append(r)
        errs, _ = check(rs, mp, closed, retired)
        case(f"work of {a} moved into {b} without a reason is blocked",
             any(e.startswith("renamed") and a in e for e in errs), True)
        # retired as merged into b, which closes the ticket (op-retire's merge = Rejected), so it is closed here too
        errs, _ = check(rs, mp, closed | {a}, retired | {a})
        case(f"work of {a} moved into {b}, retired in op-retire, passes", errs, [])
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
    errors, notes = check(rows, mp, closed, retired_keys(mp))
    planned = {r["key"] for r in rows}
    pushed = set(gen.pushed_items(mp))
    print(f"plan {len(planned)} keys, {len(planned & pushed)} with a ticket, {len(planned - pushed)} new; "
          f"{len(pushed - planned)} pushed keys out of the plan")
    for n in notes:
        print(f"  note       {n}")
    for e in errors:
        print(f"  {e}")
    tests = self_test(rows, mp, closed, retired_keys(mp))
    for name, ok, detail in tests:
        print(f"  test {'ok  ' if ok else 'FAIL'} {name}" + ("" if ok else f": {detail}"))
    failed = [t for t in tests if not t[1]]
    if errors or failed:
        print(f"FAIL: {len(errors)} pushed key(s) renamed or unstable (a rename blocks: keep the pushed key), "
              f"{len(failed)} self-test(s) failed")
        return 1
    print(f"PASS: no pushed key renamed, no new key's work already on a pushed ticket; {len(tests)} tests pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
