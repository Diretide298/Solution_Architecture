#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every Tier A device class of ADR-0015 is built by a planned task, or says why not.

**5 October 2026, CHG-R4-002.** ADR-0015 (13 August) put about nine device classes in Tier A: "build to the
standard, now, at full quality". Its actions gave the Tier A drivers to the back end. Seven weeks later the client
confirmed BOCA and sent its FGL programming guide, and nothing in the plan built the ticket printer, or any other Tier
A driver: an accepted decision with no task is a decision nobody delivers.

**What fails** (docs/adr/0015-standards-first-device-drivers.md, docs/active/block-a-extra-tasks.json,
handoff/service-docs/plan-tasks.csv):

  D-TIER-A-UNPLANNED  a class in ADR-0015's Tier A table is named by no task's `deviceClasses` in
                      block-a-extra-tasks.json and by no `deviceClassesDeferred` entry (class -> why, the lead's)
  D-TASK-NOT-PLANNED  a task that names a device class is not in the plan (plan-tasks.csv)

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py): the Tier A classes still
unplanned when this guard was written are its baseline, and each leaves it when a task or a deferral names it.

    python3 tools/check-device-tiers.py [--all] [--update-baseline]
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "D-TIER-A-UNPLANNED": "an ADR-0015 Tier A device class no planned task builds and no deferral explains (CHG-R4-002)",
    "D-TASK-NOT-PLANNED": "a task naming a device class is not in the plan (CHG-R4-002)",
}
ADR = Path("docs") / "adr" / "0015-standards-first-device-drivers.md"
PLAN = Path("handoff") / "service-docs" / "plan-tasks.csv"


def tier_a(text: str) -> list:
    """The class names of the Tier A table: the first cell of each row between '### Tier A' and the next heading."""
    m = re.search(r"^### Tier A\b.*?$(.*?)^###? ", text, re.M | re.S)
    out = []
    for line in (m.group(1) if m else "").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] and not set(cells[0]) <= set("-: ") and cells[0] != "Class":
            out.append(re.sub(r"\*", "", cells[0]).strip())
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-device-tiers", RULES)
    adr = g.ROOT / ADR
    if not adr.exists():
        guard.note(f"{ADR.as_posix()} missing: nothing to check")
        return guard.finish()
    classes = tier_a(adr.read_text(encoding="utf-8"))
    extra = g.load_json(g.ROOT / "docs" / "active" / "block-a-extra-tasks.json", {}) or {}
    named = {}
    for t in extra.get("tasks") or []:
        for c in t.get("deviceClasses") or []:
            named.setdefault(c, []).append(t["key"])
    deferred = extra.get("deviceClassesDeferred") or {}
    planned = set()
    if (g.ROOT / PLAN).exists():
        with (g.ROOT / PLAN).open(encoding="utf-8", newline="") as fh:
            planned = {r["key"] for r in csv.DictReader(fh)}
    else:
        guard.note(f"{PLAN.as_posix()} missing: D-TASK-NOT-PLANNED not run")
    for c in classes:
        if c in named:
            for k in named[c]:
                if planned and k not in planned:
                    guard.add("D-TASK-NOT-PLANNED", f"{c}:{k}", f"{k} names the Tier A class {c!r} and is not in the plan")
            continue
        if c in deferred:
            guard.note(f"deferred: {c} - {deferred[c]}")
            continue
        guard.add("D-TIER-A-UNPLANNED", c, f"ADR-0015 Tier A class {c!r}: no task in block-a-extra-tasks.json names it "
                  "(`deviceClasses`) and no `deviceClassesDeferred` entry says why")
    for c in sorted(set(named) - set(classes)):
        guard.note(f"a task names {c!r}, which is not a Tier A class of ADR-0015 ({', '.join(named[c])})")
    guard.note(f"{len(classes)} Tier A classes in ADR-0015; {sum(1 for c in classes if c in named)} built by a task, "
               f"{sum(1 for c in classes if c in deferred and c not in named)} deferred")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
