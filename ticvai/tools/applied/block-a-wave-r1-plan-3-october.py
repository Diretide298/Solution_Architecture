#!/usr/bin/env python3
"""Every screen a Block A task builds is wave 1 (CHG-RONEP-005, 3 October 2026). A one-off; a second run does nothing.

CHG-SPF-006 made every Block A screen wave 1, reading Block A from op-release.json, where a four-digit screen id
(BO-1065, BO-1094 ...) built no screen (the three-digit pattern fixed by CHG-GTR-002). So the fourteen Block A
setup screens with four-digit ids kept wave 2 or 3, and BO-1065, which Chinmay decided on 3 October is drawn and
built in Block A with its AI residency section, was not drawn in Block A. This reads Block A -- both drops, A1 and A2
(CHG-RONEP-007) -- from the plan (handoff/service-docs/plan-tasks.csv, run tools/build-service-docs.py first) and edits
only the `wave:` line of each such screen, so nothing else in a file moves. A screen an earlier run made wave 1 that
the plan no longer builds in Block A (the command centres lever A left out, CHG-RONEP-007) gets back the wave it had
at 3044d8b0. tools/check-screen-patterns.py (P8) keeps it so.

    python3 tools/applied/block-a-wave-r1-plan-3-october.py [--dry-run]
"""
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import sprint_plan as sp  # noqa: E402
import ticket_done as td  # noqa: E402

BEFORE = "3044d8b0"          # the commit before this one-off first ran


def waves(text):
    out, sid = {}, None
    for ln in text.split("\n"):
        m = re.match(r"^- id: ([A-Z]+-\d+[A-Z]?)\s*$", ln)
        if m:
            sid = m.group(1)
            continue
        m = re.match(r"^  wave: (\d+)\s*$", ln)
        if m and sid:
            out[sid] = m.group(1)
    return out


def main() -> int:
    plan = ROOT / "handoff" / "service-docs" / "plan-tasks.csv"
    a = set()
    for r in csv.DictReader(plan.open(encoding="utf-8")):
        if r["type"] == "Task" and (r.get("block") or "A") in sp.BLOCK_A_FAMILY and r.get("track") != "Test":
            a |= {b.split(" ", 1)[1] for b in td.builds_of(r, "", {}) if b.startswith("screen ")}
    changed = []
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        old = subprocess.run(["git", "show", f"{BEFORE}:./screens/{f.name}"], cwd=ROOT, capture_output=True,
                             text=True, encoding="utf-8", errors="replace").stdout
        before = waves(old)
        lines = f.read_text(encoding="utf-8").split("\n")
        sid, hit = None, False
        for i, ln in enumerate(lines):
            m = re.match(r"^- id: ([A-Z]+-\d+[A-Z]?)\s*$", ln)
            if m:
                sid = m.group(1)
                continue
            m = re.match(r"^  wave: (\d+)\s*$", ln)
            if not m or not sid:
                continue
            if sid in a and m.group(1) != "1":
                changed.append(f"{sid} ({f.name}): wave {m.group(1)} -> 1")
                lines[i] = "  wave: 1"
                hit = True
            elif sid not in a and m.group(1) == "1" and before.get(sid, "1") != "1":
                changed.append(f"{sid} ({f.name}): wave 1 -> {before[sid]} (no longer in Block A)")
                lines[i] = f"  wave: {before[sid]}"
                hit = True
        if hit and "--dry-run" not in sys.argv:
            f.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(changed) if changed else "nothing to do: every Block A screen is wave 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
