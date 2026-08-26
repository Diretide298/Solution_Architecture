#!/usr/bin/env python3
"""Rewrite the counts in README.md and COVERAGE.md from handoff/status.json.

Counts were typed by hand until 17 August. **README.md carried two different operation totals in
one file** — 737 and 753 — and neither was current, while COVERAGE.md disagreed with both. Found
by an external audit rather than by any checker here.

Numbers between the markers below are replaced on every run. Anything outside them is prose and is
left alone.

    <!-- counts:start --> … <!-- counts:end -->

Where a document has no markers, the known stale phrases are matched and updated in place, and a
line is printed so the drift is visible rather than silent.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "handoff" / "status.json"

PHRASES = [
    (r"\b\d+ operations\b", "{operations} operations"),
    (r"\b\d+ tables\b", "{tables} tables"),
    (r"\b\d+ screens\b", "{screens} screens"),
    (r"\b\d+ state models\b", "{states} state models"),
    (r"\b\d+ events\b", "{events} events"),
    (r"\b\d+ flows\b", "{flows} flows"),
    (r"\b\d+ ADRs\b", "{adrs} ADRs"),
    (r"\b\d+ contracts\b", "{contracts} contracts"),
    (r"\b\d+ relationships\b", "{relationships} relationships"),
    (r"\b\d+ platforms\b", "{platforms} platforms"),
]


def main() -> int:
    if not STATUS.exists():
        raise SystemExit("run `python3 tools/build-status.py` first")
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    c = dict(s["counts"])
    c["conflicts"] = s["conflicts"]["closed"] + s["conflicts"]["open"] + s["conflicts"]["withdrawn"]

    total = 0
    for name in ("README.md", "COVERAGE.md"):
        p = ROOT / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        before = text
        for pattern, template in PHRASES:
            text = re.sub(pattern, template.format(**c), text)
        # the conflict register line, which uses a different shape
        text = re.sub(r"\b\d+ closed · \d+ client", f"{s['conflicts']['closed']} closed · "
                      f"{s['conflicts']['open']} client", text)
        if text != before:
            p.write_text(text, encoding="utf-8")
            changed = sum(1 for a, b in zip(before.split("\n"), text.split("\n")) if a != b)
            print(f"  {name}: {changed} line(s) updated")
            total += changed
    print(f"{total} line(s) synced from status.json" if total else "counts already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
