#!/usr/bin/env python3
"""Every screen a Block A task builds is wave 1 (CHG-RONEP-005, 3 October 2026). A one-off; a second run does nothing.

CHG-SPF-006 made every Block A screen wave 1, reading Block A from op-release.json, where a four-digit screen id
(BO-1065, BO-1094 ...) built no screen (the three-digit pattern fixed by CHG-GTR-002). So the fourteen Block A
setup screens with four-digit ids kept wave 2 or 3, and BO-1065, which Chinmay decided on 3 October is drawn and
built in Block A with its AI residency section, was not drawn in Block A. This reads Block A from the plan
(handoff/service-docs/plan-tasks.csv, run tools/build-service-docs.py first) and edits only the `wave:` line of
each such screen, so nothing else in a file moves. tools/check-screen-patterns.py (P8) keeps it so.

    python3 tools/applied/block-a-wave-r1-plan-3-october.py [--dry-run]
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import ticket_done as td  # noqa: E402


def main() -> int:
    plan = ROOT / "handoff" / "service-docs" / "plan-tasks.csv"
    a = set()
    for r in csv.DictReader(plan.open(encoding="utf-8")):
        if r["type"] == "Task" and (r.get("block") or "A") == "A" and r.get("track") != "Test":
            a |= {b.split(" ", 1)[1] for b in td.builds_of(r, "", {}) if b.startswith("screen ")}
    changed = []
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        lines = f.read_text(encoding="utf-8").split("\n")
        sid, hit = None, False
        for i, ln in enumerate(lines):
            m = re.match(r"^- id: ([A-Z]+-\d+[A-Z]?)\s*$", ln)
            if m:
                sid = m.group(1)
                continue
            m = re.match(r"^  wave: (\d+)\s*$", ln)
            if m and sid in a and m.group(1) != "1":
                changed.append(f"{sid} ({f.name}): wave {m.group(1)} -> 1")
                lines[i] = "  wave: 1"
                hit = True
        if hit and "--dry-run" not in sys.argv:
            f.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(changed) if changed else "nothing to do: every Block A screen is wave 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
