#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The three binding counts the design-handoff generator measures may only go down.

**Council of 2 October 2026, "the one thing to do first"** (`docs/active/council/council-report-2026-10-02-opus.html`): the
per-screen design-handoff generator (`tools/design_spec.py`, 1 October) resolves every screen against
the contracts and found, mechanically and at no AI cost,

    unbound-control      a control with no schema field behind it: an authored label only   (5,613 then)
    undefined-operation  a form that calls an operation no contract defines                   (55)
    unknown-field        a bound field (`Schema.path`) that is not in the contracts           (42)

Those are failing checks, not audit findings: a screen could be merged that did not resolve against its
contract, and that is the root of most of the week's churn. Fixing them all before Monday is impossible,
so this is a **ratchet**: today's counts per app, block and kind are the baseline
(`checks/baseline.json`), and the run fails if any count rises. A fix lowers a count; the lead then
records the lower number with `--update-baseline` in a reviewed commit, so the ceiling only falls.

**Much of the first count is legitimate static text** (a heading, a hint), and 1,683 of the 26 September
findings were false or only partly real. So a person may allowlist an item in `checks/allowlist.yaml`,
with a reason, an approver and an expiry **no more than 14 days** after it was added. An allowlisted item
is left out of the counts; an expired entry fails the run, so an exception is a decision with a date,
never a silent hole.

The counts are computed by the generator's own `render_screen` (the same function every BUNDLE.md is
written by), with the two sections that cannot affect them (the requirements matrix and the tracker
rows) stubbed out for speed. `--from-coverage FILE` reads the per-screen coverage that
`export-design-batch.py --all --coverage FILE` wrote instead of recomputing.

    python3 tools/check-binding-ratchet.py                      # compare with checks/baseline.json
    python3 tools/check-binding-ratchet.py --update-baseline    # record today's counts (reviewed commit)
    python3 tools/check-binding-ratchet.py --from-coverage F    # use a coverage file
    python3 tools/check-binding-ratchet.py --self-test          # the rules only, on made-up counts

**The baseline in this commit was recorded on the change-rules branch, before r2.** Re-record it on main
at r2 (`--update-baseline`) before this gate blocks any audit fix.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import importlib.util
import json
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASELINE = ROOT / "checks" / "baseline.json"
ALLOWLIST = ROOT / "checks" / "allowlist.yaml"
MAX_DAYS = 14
KINDS = ("unbound-control", "undefined-operation", "unknown-field")


def _utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def kind_of(reason: str) -> str:
    """The generator's reason text -> the kind (the same split as export-design-batch's summary)."""
    if reason.startswith("no schema field"):
        return "unbound-control"
    if "not found" in reason:
        return "unknown-field"
    if "no contract" in reason:
        return "undefined-operation"
    return "other"


def _spec():
    spec = importlib.util.spec_from_file_location("design_spec", ROOT / "tools" / "design_spec.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def findings(coverage: str | None = None) -> tuple[list[tuple], dict]:
    """([(screen, app, block, kind, item)], {screens, fully_resolved})."""
    ds = _spec()
    pkg = ds.PKG
    stats_by = {}
    if coverage:
        stats_by = json.loads(pathlib.Path(coverage).read_text(encoding="utf-8"))
    else:
        # Display-only sections: they never append to `unresolved` and cost most of the run.
        ds.tracker_for = lambda s, plat: []
        ds.requirements_for = lambda s: []
        for sid, (s, plat) in pkg.screens.items():
            st: dict = {}
            ds.render_screen(s, plat, st)
            stats_by[sid] = st
    out, full = [], 0
    for sid, st in stats_by.items():
        s, plat = pkg.screens.get(sid, ({}, {}))
        app = (plat.get("targetApp") or {}).get("app") or plat.get("code") or "?"
        blk = pkg.blocks.get(sid)
        block = blk[0] if blk else "-"
        if st.get("inputs", 0) == st.get("inputs_resolved", 0) and st.get("outputs", 0) == st.get("outputs_resolved", 0):
            full += 1
        for _sid, label, reason in st.get("unresolved") or []:
            k = kind_of(str(reason))
            item = str(label or "")
            if k == "undefined-operation":
                item = str(reason).split("`")[1] if "`" in str(reason) else item
            elif k == "unknown-field":
                item = str(reason).split(" not found")[0]
            out.append((sid, app, block, k, item))
    src = "plan-tasks.csv" if ds.PLAN_TASKS.exists() else "tasks.csv"
    return out, {"screens": len(stats_by), "fully_resolved": full, "block_source": src}


# ------------------------------------------------------------------------------------- allowlist
def load_allowlist(path=ALLOWLIST) -> list[dict]:
    if not pathlib.Path(path).exists():
        return []
    doc = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8")) or {}
    return list(doc.get("entries") or [])


def _date(x):
    if isinstance(x, datetime.date):
        return x
    try:
        return datetime.date.fromisoformat(str(x))
    except Exception:
        return None


def check_allowlist(entries: list[dict], today: datetime.date) -> list[str]:
    errs = []
    for i, e in enumerate(entries, 1):
        tag = f"allowlist entry {i} ({e.get('screen')} {e.get('kind')} {e.get('item', '*')})"
        miss = [f for f in ("screen", "kind", "reason", "added", "expires", "approved_by") if not e.get(f)]
        if miss:
            errs.append(f"{tag}: missing {', '.join(miss)}")
            continue
        if e["kind"] not in KINDS:
            errs.append(f"{tag}: kind must be one of {', '.join(KINDS)}")
        a, x = _date(e["added"]), _date(e["expires"])
        if not a or not x:
            errs.append(f"{tag}: added and expires must be YYYY-MM-DD")
            continue
        if (x - a).days > MAX_DAYS or x < a:
            errs.append(f"{tag}: expires {x} is more than {MAX_DAYS} days after added {a}")
        if today > x:
            errs.append(f"{tag}: EXPIRED on {x}: fix the screen, or renew it with a new decision")
    return errs


def allowed(f: tuple, entries: list[dict], today: datetime.date) -> bool:
    sid, _app, _blk, kind, item = f
    for e in entries:
        x = _date(e.get("expires"))
        if not x or today > x:
            continue
        if e.get("screen") == sid and e.get("kind") == kind and (not e.get("item") or str(e["item"]) == item):
            return True
    return False


# ----------------------------------------------------------------------------------------- ratchet
def counts(fs: list[tuple]) -> dict:
    c = collections.Counter(f"{app}|{blk}|{kind}" for _sid, app, blk, kind, _item in fs)
    return dict(sorted(c.items()))


def compare(base: dict, cur: dict) -> tuple[list[tuple], list[tuple]]:
    """([(key, was, now)] risen, [(key, was, now)] fallen)."""
    up, down = [], []
    for k in sorted(set(base) | set(cur)):
        b, n = int(base.get(k, 0)), int(cur.get(k, 0))
        if n > b:
            up.append((k, b, n))
        elif n < b:
            down.append((k, b, n))
    return up, down


def self_test() -> list[tuple[str, bool]]:
    t = datetime.date(2026, 10, 2)
    fs = [("WEB-001", "guest", "A", "unbound-control", "Hero"), ("WEB-001", "guest", "A", "unbound-control", "Tagline"),
          ("POS-002", "venue-pos", "A", "undefined-operation", "voidLine")]
    base = counts(fs)
    out = []
    up, _ = compare(base, counts(fs))
    out.append(("same counts pass", not up))
    up, _ = compare(base, counts(fs + [("WEB-002", "guest", "A", "unknown-field", "Cart.total")]))
    out.append(("a new unknown field fails", [k for k, *_ in up] == ["guest|A|unknown-field"]))
    up, down = compare(base, counts(fs[1:]))
    out.append(("a fix lowers a count and passes", not up and down == [("guest|A|unbound-control", 2, 1)]))
    # a swap inside one app/block/kind keeps the count: the ratchet is on counts, as the council asked
    up, _ = compare(base, counts([fs[0], ("WEB-003", "guest", "A", "unbound-control", "x"), fs[2]]))
    out.append(("a swap within one count passes", not up))
    allow = [{"screen": "WEB-002", "kind": "unknown-field", "item": "Cart.total", "reason": "static",
              "added": "2026-10-01", "expires": "2026-10-10", "approved_by": "Chinmay"}]
    new = fs + [("WEB-002", "guest", "A", "unknown-field", "Cart.total")]
    up, _ = compare(base, counts([f for f in new if not allowed(f, allow, t)]))
    out.append(("an allowlisted item is left out of the counts", not up and not check_allowlist(allow, t)))
    out.append(("an expired allowlist entry fails", bool(check_allowlist(allow, datetime.date(2026, 10, 11)))))
    up, _ = compare(base, counts([f for f in new if not allowed(f, allow, datetime.date(2026, 10, 11))]))
    out.append(("an expired entry stops excusing its item", bool(up)))
    long_ = [dict(allow[0], expires="2026-10-20")]
    out.append(("an entry longer than 14 days fails", bool(check_allowlist(long_, t))))
    out.append(("an entry without an approver fails", bool(check_allowlist([dict(allow[0], approved_by="")], t))))
    return out


def head() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True).stdout.strip()
    except Exception:
        return ""


def main() -> int:
    _utf8()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--update-baseline", action="store_true")
    ap.add_argument("--from-coverage", metavar="FILE")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--today", help=argparse.SUPPRESS)
    a = ap.parse_args()
    today = _date(a.today) if a.today else datetime.date.today()

    tests = self_test()
    for name, ok in tests:
        if not ok or a.self_test:
            print(f"  test {'ok  ' if ok else 'FAIL'} {name}")
    if a.self_test:
        return 0 if all(ok for _, ok in tests) else 1

    entries = load_allowlist()
    errs = check_allowlist(entries, today)
    fs, meta = findings(a.from_coverage)
    kept = [f for f in fs if not allowed(f, entries, today)]
    cur = counts(kept)
    tot = collections.Counter(f[3] for f in kept)
    print(f"binding ratchet: {meta['screens']} screens, {meta['fully_resolved']} fully resolved; "
          + ", ".join(f"{k} {tot.get(k, 0)}" for k in KINDS)
          + (f" ({len(fs) - len(kept)} allowlisted)" if len(fs) != len(kept) else ""))

    if a.update_baseline:
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps({
            "_about": "Binding counts per app|block|kind that may only fall (tools/check-binding-ratchet.py). "
                      "Written by --update-baseline in a reviewed commit, never by hand.",
            "recorded": today.isoformat(), "commit": head(),
            "totals": {k: tot.get(k, 0) for k in KINDS},
            "screens": meta["screens"], "fully_resolved": meta["fully_resolved"],
            "block_source": meta["block_source"],
            "counts": cur}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"baseline written: {BASELINE.relative_to(ROOT).as_posix()} ({len(cur)} counts)")
        return 0

    if not BASELINE.exists():
        print("FAIL - no checks/baseline.json: record one with --update-baseline")
        return 1
    base = json.loads(BASELINE.read_text(encoding="utf-8"))
    if base.get("block_source", "tasks.csv") == "tasks.csv" and meta["block_source"] == "plan-tasks.csv":
        # **A baseline from before the replan's plan-tasks.csv knew only Block A** ("-" is everything else).
        # Compare like with like until it is re-recorded, rather than failing every B-D count from 0.
        print("  note: the baseline knew only Block A (tasks.csv); B-D are compared as '-'. "
              "Re-record it with --update-baseline.")
        kept = [(sid, app, blk if blk == "A" else "-", kind, item) for sid, app, blk, kind, item in kept]
        cur = counts(kept)
    up, down = compare(base.get("counts") or {}, cur)
    by_key = collections.defaultdict(collections.Counter)
    for sid, app, blk, kind, _item in kept:
        by_key[f"{app}|{blk}|{kind}"][sid] += 1
    for k, b, n in up:
        top = ", ".join(f"{s} ({c})" for s, c in by_key[k].most_common(6))
        print(f"  FAIL {k:<48} {b:>5} -> {n:<5} screens: {top}")
    for k, b, n in down[:20]:
        print(f"  down {k:<48} {b:>5} -> {n}")
    if len(down) > 20:
        print(f"  ... and {len(down) - 20} more fallen")
    for e in errs:
        print(f"  FAIL {e}")
    bad = [t for t in tests if not t[1]]
    if up or errs or bad:
        print(f"FAIL - {len(up)} count(s) rose, {len(errs)} allowlist problem(s), {len(bad)} self-test(s) failed "
              f"(baseline {base.get('recorded')} at {base.get('commit')})")
        return 1
    print(f"PASS - no count rose against the baseline of {base.get('recorded')} ({base.get('commit')})"
          + (f"; {len(down)} fell: run --update-baseline to tighten" if down else "")
          + f"; {len(tests)} self-tests pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
