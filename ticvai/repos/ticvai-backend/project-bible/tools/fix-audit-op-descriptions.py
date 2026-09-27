#!/usr/bin/env python3
"""Bring handoff/service-docs/op-descriptions.json up to what tools/op-descriptions.py now writes.

op-descriptions.py is not part of refresh.sh: it is run by hand (and by push-openproject.py for new tickets), so its
fixes for audit roots R067, R071, R072, R084, R085, R121 and R157 reach nothing already generated until this runs.

It rebuilds every description the file already holds from the package as it stands, with the Block A schedule, and
reports what would change. Idempotent: a second run after --apply finds nothing to change. Dry run by default.

  python3 tools/fix-audit-op-descriptions.py [--schedule handoff/service-docs/block-a-schedule.json] [--show N] [--apply]

After --apply the text is only in the local file. OpenProject still shows the old descriptions until
tools/op-descriptions.rb applies the file on the server (see the header of that script).
"""
from __future__ import annotations

import argparse
import difflib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
TARGET = DOCS / "op-descriptions.json"

# What each audit root changes in the text, so the report says which roots a changed description carries.
MARKERS = {
    "R071/R084/R121 done-when": "Reads and writes at least the tables listed",
    "R071 reads label": "Reads (from the lineage, at least)",
    "R084 money": "- **Money:** currency and scale",
    "R157 emits": "- **Emits (through `platform.outbox`",
    "R072 guest rule": "a guest caller needs no permission",
    "R072 guest screen": "not reachable on a guest screen",
}


def load_generator():
    spec = importlib.util.spec_from_file_location("op_descriptions", ROOT / "tools" / "op-descriptions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schedule", default=str(DOCS / "block-a-schedule.json"))
    ap.add_argument("--show", type=int, default=2, help="print a diff for this many changed descriptions")
    ap.add_argument("--apply", action="store_true", help="write the file (default: dry run)")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")     # a Windows console is not UTF-8

    gen = load_generator()
    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    old = json.loads(TARGET.read_text(encoding="utf-8"))
    keys = [k for k in mp if not k.startswith(("_", "VERSION")) and str(mp[k]) in old]
    texts = gen.build(a.schedule, keys)
    new = dict(old)
    for k, t in texts.items():
        new[str(mp[k])] = t

    changed = [i for i in old if old[i] != new[i]]
    print(f"{len(old)} descriptions in {TARGET.relative_to(ROOT)}; {len(changed)} would change")
    for label, mark in MARKERS.items():
        n = sum(1 for i in changed if mark in new[i] and mark not in old[i])
        print(f"  {label}: {n}")
    stale = sum(1 for i in changed if "'; 429" in old[i] or "\n; " in old[i])
    print(f"  R085 split response lines removed: {stale}")
    others = [i for i in changed if not any(m in new[i] and m not in old[i] for m in MARKERS.values())]
    if others:
        print(f"  {len(others)} change for other reasons (the package moved since the file was written)")
    for i in changed[: a.show]:
        print(f"\n--- #{i}")
        sys.stdout.writelines(difflib.unified_diff(old[i].splitlines(True), new[i].splitlines(True), "old", "new", n=0))

    if not changed:
        print("nothing to do")
        return 0
    if not a.apply:
        print("\ndry run: nothing written; --apply writes the file")
        return 0
    TARGET.write_text(json.dumps(new, indent=0, ensure_ascii=False), encoding="utf-8")
    print(f"\nwritten: {TARGET}. Apply it on the OpenProject server with tools/op-descriptions.rb.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
