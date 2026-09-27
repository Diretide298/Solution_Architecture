#!/usr/bin/env python3
"""Correct `trigger: onLoad` on operations that write, or that need an input the screen lacks (audit R268).

`derive-task-linkage.py` is a one-time generator (refresh.sh excludes it), and it was never the
only source of triggers: `from page inventory` and `From the flow it appears in` came from the
pack importers, and the verb rule *a read is onLoad* was copied into them. Fixing the generator
therefore changes nothing already on disk. This applies the generator's corrected rule,
`load_trigger`, to every `apis` entry the screens already declare:

* an operation that **writes** (anything beyond the idempotency cache) is never `onLoad`:
  `joinQueue`, `submitReview`, `setSubscription`, `recordConsent`, `registerGuest`,
  `requestGuestOtp`, `claimLocationSession` become `onAction`. One only a device calls
  (`recordDeviceHeartbeat`) becomes `background`;
* a **read that needs a value the screen does not arrive with** becomes `onAction`: a typed
  query (`searchCatalogue` needs `q`, `resolveProductByCode` needs `code`), a `lookup*`, or a
  get-by-id whose id is not handed over by `session` or an upstream screen -- or only by a
  deep link on a screen that also loads a list, where the id is the row the user picks
  (`getSupplierPerformance` on `BO-083`, `getBillingStatement`, `diffConfigVersion`).

**Only `onLoad` is ever changed**, and only to a less eager trigger: `onInterval`, `onScan`,
`background` and `onAction` are left as they are, and nothing is promoted to `onLoad`. POSTs that
write nothing (`simulateCommercialPackage`, `quoteRentalPrice`) and reads bounded by a required
date range are left alone: whether they run on open is a product decision this does not make.

Edits are made line by line on the one `trigger:` line of the item, so comments, key order and
the rest of the file are unchanged. Operation ids, screen ids and paths are not touched.
Idempotent: a second run finds nothing to change.

Run: `python tools/fix-audit-load-triggers.py [--apply] [--verbose]`
Without `--apply` it prints what it would change and writes nothing.
"""
from __future__ import annotations

import argparse
import collections
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_spec = importlib.util.spec_from_file_location("derive_task_linkage",
                                               ROOT / "tools" / "derive-task-linkage.py")
dtl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dtl)

SCREEN_RE = re.compile(r"^- id:\s*['\"]?([^'\"\s]+)")
APIS_RE = re.compile(r"^(\s*)apis:\s*$")
TRIGGER_RE = re.compile(r"^(\s*)(-\s+)?trigger:\s*['\"]?onLoad['\"]?(\s*(#.*)?)$")


def plan(files, inputs, lineage, screen_ids):
    """{path: {screen id: {item index: (operationId, new trigger, reason)}}}"""
    out = {}
    for f in files:
        d = yaml.safe_load(io.open(f, encoding="utf8")) or {}
        per = {}
        for s in d.get("screens") or []:
            for i, a in enumerate(s.get("apis") or []):
                if not isinstance(a, dict) or a.get("trigger") != "onLoad":
                    continue
                oid = a.get("operationId")
                if not oid or (oid not in inputs and oid not in lineage):
                    continue
                trig, why = dtl.load_trigger(oid, s, inputs, lineage, screen_ids, skip_index=i)
                if trig != "onLoad":
                    per.setdefault(s["id"], {})[i] = (oid, trig, why)
        if per:
            out[f] = per
    return out


def rewrite(path, per_screen):
    """Change the planned `trigger:` lines. Returns (new text, count, not found)."""
    # newline="" keeps the CRLF endings the screens are stored with; `\s*` in TRIGGER_RE
    # carries the `\r` through to the rewritten line.
    lines = io.open(path, encoding="utf8", newline="").read().split("\n")
    done = 0
    found = set()
    sid = None
    apis_ind = None
    idx = -1
    op_ind = None
    for n, line in enumerate(lines):
        m = SCREEN_RE.match(line)
        if m:
            sid, apis_ind, idx = m.group(1), None, -1
            continue
        if sid is None or sid not in per_screen:
            continue
        m = APIS_RE.match(line)
        if m and apis_ind is None:
            apis_ind, idx = len(m.group(1)), -1
            continue
        if apis_ind is None or not line.strip():
            continue
        ind = len(line) - len(line.lstrip(" "))
        if ind < apis_ind or (ind == apis_ind and not line.lstrip().startswith("- ")):
            apis_ind = None          # the apis block has ended
            continue
        if ind == apis_ind and line.lstrip().startswith("- "):
            idx += 1
            op_ind = ind + 2
        want = per_screen[sid].get(idx)
        if not want:
            continue
        t = TRIGGER_RE.match(line)
        if not t:
            continue
        key_ind = len(t.group(1)) + (len(t.group(2)) if t.group(2) else 0)
        if key_ind != op_ind:
            continue
        lines[n] = "%s%strigger: %s%s" % (t.group(1), t.group(2) or "", want[1], t.group(3) or "")
        found.add((sid, idx))
        done += 1
    missing = [(s, i) for s, items in per_screen.items() for i in items if (s, i) not in found]
    return "\n".join(lines), done, missing


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true", help="write the changes")
    ap.add_argument("--verbose", action="store_true", help="print every change")
    args = ap.parse_args()

    files = sorted(SCREENS.glob("P*.yaml"))
    inputs = dtl.operation_inputs()
    lineage = json.load(io.open(dtl.LINEAGE, encoding="utf8"))
    screen_ids = set()
    for f in files:
        for s in (yaml.safe_load(io.open(f, encoding="utf8")) or {}).get("screens") or []:
            if s.get("id"):
                screen_ids.add(s["id"])

    todo = plan(files, inputs, lineage, screen_ids)
    kinds = collections.Counter()
    total = 0
    problems = []
    for f, per in todo.items():
        text, n, missing = rewrite(f, per)
        total += n
        for sid, items in sorted(per.items()):
            for i, (oid, trig, why) in sorted(items.items()):
                kinds["%s (%s)" % (trig, "writes" if why.startswith("it writes") or why.startswith("it is a")
                                  else "device" if "device" in why else "needs input")] += 1
                if args.verbose or not args.apply:
                    print("  %-9s %-34s onLoad -> %-10s %s" % (sid, oid, trig, why))
        for sid, i in missing:
            problems.append("%s: %s apis[%d] not found in the text" % (f.name, sid, i))
        if args.apply and n:
            io.open(f, "w", encoding="utf8", newline="").write(text)
            print("  -> %s (%d)" % (f.relative_to(ROOT), n))

    print()
    for k, v in kinds.most_common():
        print("  %-28s %d" % (k, v))
    print("%d trigger(s) %s across %d file(s)"
          % (total, "changed" if args.apply else "would change", len(todo)))
    for p in problems:
        print("  WARNING " + p)
    if not args.apply:
        print("nothing written -- pass --apply")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
