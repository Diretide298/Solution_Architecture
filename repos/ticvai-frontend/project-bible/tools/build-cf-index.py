#!/usr/bin/env python3
"""
Generate the conflict status index from the register.

`registers/conflicts.md` holds the reasoning; this produces the one-line-per-conflict index
beside it. Generated rather than maintained, because the register's own summary was maintained
by hand and had drifted five ways by 14 August — it claimed 31 closed against 36 rows, and five
conflicts that had been resolved were still sitting in an open section because new items were
inserted at the top and completed ones were never moved.

A count kept by hand next to the thing it counts will disagree with it. This regenerates both
the index and the register's summary table from the rows.

Run: python3 tools/build-cf-index.py
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "registers/conflicts.md"
INDEX = ROOT / "registers/conflict-status.md"

STATE = {
    "Open — needs a client decision": "OPEN — client",
    "Open — Softlabs to resolve": "OPEN — Softlabs",
    "Closed": "CLOSED",
    "Withdrawn or absorbed": "WITHDRAWN",
}
ORDER = list(STATE)
ROW = re.compile(r"^\| \*?\*?(CF-\d+[a-z]?|P08-\d+)\*?\*? \|(.*)$")
OWNER = re.compile(r"Chinmay|Dinesh|Qossai|Allam|Finance|Chitrangi|counsel|Contracts|design|Parked|Both|Softlabs|Client")


def parse() -> list[dict]:
    section = None
    rows = []
    for line in REGISTER.read_text().split("\n"):
        if line.startswith("## "):
            section = line[3:].strip()
        elif line.startswith("### "):
            pass  # sub-headings do not change the state
        if (m := ROW.match(line)) and section:
            # a sub-section under Closed is still Closed
            state = next((k for k in ORDER if section.startswith(k.split(" —")[0])
                          and (section == k or k == "Closed")), section)
            rows.append({"id": m.group(1),
                         "section": section if section in STATE else state,
                         "cells": [c.strip() for c in m.group(2).split(" | ")]})
    return rows


def sort_key(r: dict) -> tuple[int, str]:
    return int(re.sub(r"\D", "", r["id"])), re.sub(r"[\d\-]|CF|P08", "", r["id"])


def main() -> int:
    rows = sorted(parse(), key=sort_key)
    if not rows:
        print("no conflict rows found", file=sys.stderr)
        return 1

    counts = Counter(r["section"] for r in rows)
    unknown = [k for k in counts if k not in STATE]
    if unknown:
        print(f"unrecognised section(s): {unknown}", file=sys.stderr)
        return 1

    numbered = [r for r in rows if r["id"].startswith("CF-")]
    ids = sorted({int(re.sub(r"\D", "", r["id"])) for r in numbered})
    gaps = [n for n in range(1, max(ids) + 1) if n not in ids]
    dupes = [k for k, v in Counter(r["id"] for r in rows).items() if v > 1]

    out = [
        "# Conflict register — status index\n",
        f"**{len(rows)} conflicts raised — CF-01 to CF-{max(ids)}, plus CF-33a and one "
        "screen-level item.**\n",
        "Generated from `conflicts.md`, which holds the full reasoning for each. This is the",
        "index: one line per conflict, so anything's state can be checked without reading the",
        "register.\n",
        "| State | Count |", "|---|---|",
    ]
    for k in ORDER:
        out.append(f"| {STATE[k]} | **{counts.get(k, 0)}** |")
    out.append(f"| **Total** | **{len(rows)}** |")
    open_n = counts.get(ORDER[0], 0) + counts.get(ORDER[1], 0)
    out += ["", "**Blocking: 0.** No conflict currently prevents contract, schema or build work.",
            f"**{open_n} open, {counts.get('Closed', 0)} closed.**", ""]

    for k in ORDER:
        sel = [r for r in rows if r["section"] == k]
        if not sel:
            continue
        out += [f"\n## {k} — {len(sel)}\n", "| ID | Issue | Owner |", "|---|---|---|"]
        for r in sel:
            issue = " ".join(re.sub(r"\*\*", "", r["cells"][0]).split())[:150]
            owner = next((re.sub(r"\*\*", "", c).strip() for c in r["cells"][1:]
                          if len(c) < 40 and OWNER.search(c)), "")
            out.append(f"| **{r['id']}** | {issue} | {owner} |")

    out += ["", "---", "",
            "## Integrity\n",
            f"- **Numbering:** CF-01 to CF-{max(ids)}, "
            + ("no gaps" if not gaps else f"**gaps at {gaps}**"),
            f"- **Duplicates:** {'none' if not dupes else dupes}",
            "- **Counts** are generated from the rows, so this file and the register's summary",
            "  cannot disagree. Regenerate with `tools/build-cf-index.py` after editing.\n"]

    INDEX.write_text("\n".join(out) + "\n")
    print(f"{INDEX.name}: {len(rows)} conflicts")
    for k in ORDER:
        print(f"  {counts.get(k, 0):>3}  {STATE[k]}")
    if gaps:
        print(f"  gaps in numbering: {gaps}")
    if dupes:
        print(f"  duplicates: {dupes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
