#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Whether every screen has a design a developer can open, and whether drawn frames are linked.

**Audit class A-WIREFRAME (docs/active/root-classes.md), roots R252, R258, R272.** On 26
September most screen tickets said "no wireframe": generated frames `notStarted`, the Claude
Design and client frames archived to the git-ignored `_dump/` and the screens repointed away from
them (R258), redrawn frames sitting in `wireframes/incoming/` that no screen record named, and pack
frames matched to the wrong screen by title (R272). `check-wireframes.py` holds the board anchors
and file references; it cannot say a screen has no design at all, or that a drawn frame exists
and is not linked. This does:

  W-NO-DESIGN          a screen with no design source of any kind: frame not started, and no
                       prototype, workshop board, reference frame or boardFrames (R252)
  W-INCOMING-UNLINKED  a frame for the screen in wireframes/incoming/ that its record never names,
                       while the record still says notStarted (R258)
  W-DUMP-POINTER       a wireframe path into `_dump/`, which is git-ignored and reaches no
                       developer (R258)

The baseline holds today's `W-NO-DESIGN` screens (the Claude Design runs are drawing them); a
screen added after it must arrive with a design source or a recorded one.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-wireframe-coverage.py [--all] [--update-baseline]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "W-NO-DESIGN": "a screen with no design source of any kind (R252)",
    "W-INCOMING-UNLINKED": "a drawn frame in wireframes/incoming/ its screen record never names (R258)",
    "W-DUMP-POINTER": "a wireframe path into the git-ignored _dump/ (R258)",
}


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-wireframe-coverage", RULES)
    incoming = {}
    for f in (g.ROOT / "wireframes" / "incoming").glob("*/*.html"):
        m = re.match(r"([a-z]{2,5}-\d{3,4})", f.stem, re.I)
        if m:
            incoming.setdefault(m.group(1).upper(), []).append(f.relative_to(g.ROOT).as_posix())
    for plat, s in g.screens():
        sid = s["id"]
        w = s.get("wireframe") or {}
        blob = json.dumps({"w": w, "b": s.get("boardFrames")}, default=str)
        started = w.get("status") not in (None, "notStarted")
        sources = [w.get("prototype"), w.get("workshopBoard"), w.get("derivedFrom"), s.get("boardFrames")]
        if not started and not any(sources):
            guard.add("W-NO-DESIGN", sid, f"{sid} ({plat}): frame notStarted and no prototype, workshop board, "
                                          f"reference frame or boardFrames")
        for path in incoming.get(sid, []):
            if not started and path not in blob and "incoming" not in blob:
                guard.add("W-INCOMING-UNLINKED", f"{sid}:{path}", f"{sid}: {path} is drawn and the record "
                                                                   f"still points at a notStarted frame")
        if re.search(r"(^|[\"/ ])_dump/", blob):
            guard.add("W-DUMP-POINTER", sid, f"{sid}: a wireframe path points into _dump/")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
