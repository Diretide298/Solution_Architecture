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

# **The digit run spans a thousands separator.** `\d+` against "1,032 operations" matched the
# "032" alone and wrote "1,1032" — a pattern that half-matches corrupts rather than skips.
PHRASES = [
    (r"\b[\d,]+ operations\b", "{operations} operations"),
    (r"\b[\d,]+ tables\b", "{tables} tables"),
    (r"\b[\d,]+ screens\b", "{screens} screens"),
    (r"\b[\d,]+ state models\b", "{states} state models"),
    (r"\b[\d,]+ events\b", "{events} events"),
    (r"\b[\d,]+ flows\b", "{flows} flows"),
    (r"\b[\d,]+ ADRs\b", "{adrs} ADRs"),
    (r"\b[\d,]+ contracts\b", "{contracts} contracts"),
    (r"\b[\d,]+ relationships\b", "{relationships} relationships"),
    (r"\b[\d,]+ platforms\b", "{platforms} platforms"),
    # **Three counts that drifted because no phrase watched them.** MANIFEST.md read "12 apps"
    # after the five shipped apps were decided on 10 September, and "83 boards" after 65 of them
    # were archived the same day. `apps` is now the shipped unit and `frontends` the build unit;
    # both are real and the documents have to say which they mean.
    (r"\b[\d,]+ apps\b", "{apps} apps"),
    (r"\b[\d,]+ frontends\b", "{frontends} frontends"),
    (r"\b[\d,]+ boards\b", "{boards} boards"),
    # **Both quoted from memory in three places and wrong in all of them.** They change on
    # every generation of the DDL, which is exactly the kind of number nobody re-reads.
    (r"\b[\d,]+ foreign keys\b", "{foreignKeys} foreign keys"),
    (r"\b[\d,]+ indexes\b", "{indexes} indexes"),
]


# **A markdown table cell is a count with no noun next to it**, so `PHRASES` above cannot see one.
# `COVERAGE.md`'s "What exists" table was still reading 753 operations, 278 tables, 364 screens,
# 76 state models, 23 flows and 24 ADRs on 3 September — **every figure frozen around 17 August**,
# in the one document whose whole purpose is to say what exists.
#
# Matched on the row label instead. A row whose label is not here is left exactly as it is.
ROWS = {
    "API operations": "operations",
    "Tables designed": "tables",
    "Tables written as DDL": "tables",
    "Relationships": "relationships",
    "Screens defined": "screens",
    "State models": "states",
    "Domain events": "events",
    "User flows": "flows",
    "ADRs": "adrs",
}


def _sync_rows(text: str, c: dict) -> str:
    """Rewrite the first numeric cell of any table row whose label is in ROWS.

    **Split on the pipe rather than matching a pattern.** A markdown row has known structure, and a
    regex over it has to encode the bold markers, the cell padding and the separator line as well —
    three more things to get wrong in service of one substitution.

    **Bold survives.** These rows carry `**278**` and a reader uses the emphasis to find the line
    that matters; stripping it to update a number would be the worse outcome of the two.
    """
    out = []
    for line in text.split("\n"):
        parts = line.split("|")
        # `set(...) - set("- :")` skips the `|---|---|` separator without matching it by shape.
        if len(parts) >= 4 and set(parts[1].strip()) - set("- :"):
            key = ROWS.get(parts[1].strip().strip("*").strip())
            cell = parts[2].strip() if key else ""
            if key and cell.strip("*").replace(",", "").isdigit():
                bold = "**" if cell.startswith("**") else ""
                parts[2] = f" {bold}{c[key]:,}{bold} "
                line = "|".join(parts)
        out.append(line)
    return "\n".join(out)


def main() -> int:
    if not STATUS.exists():
        raise SystemExit("run `python3 tools/build-status.py` first")
    s = json.loads(STATUS.read_text(encoding="utf-8"))
    c = dict(s["counts"])
    c["conflicts"] = s["conflicts"]["closed"] + s["conflicts"]["open"] + s["conflicts"]["withdrawn"]

    # **Four more documents, because the two below were never the only ones carrying a count.**
    # On 3 September five different table totals were in circulation — 383 in README, OVERVIEW,
    # COVERAGE and MANIFEST's headline, 373 in MANIFEST's layout block and backend/README, 369 in
    # services/README, against 374 actually emitted. **This tool ran on every refresh and saw two
    # of the six.**
    #
    # `deploy/*.yml` is deliberately not here. Its prose carries load arithmetic — "60,000 seats
    # over two hours is 1,045 RPS" — and every pattern in `PHRASES` below is a bare digit run
    # against a noun, which is broad enough to rewrite a sentence that was never a count of anything.
    # **Those two figures are corrected by hand.**
    total = 0
    for name in ("README.md", "COVERAGE.md", "OVERVIEW.md", "MANIFEST.md",
                 "backend/README.md", "services/README.md"):
        p = ROOT / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        before = text
        for pattern, template in PHRASES:
            text = re.sub(pattern, template.format(**c), text)
        text = _sync_rows(text, c)
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
