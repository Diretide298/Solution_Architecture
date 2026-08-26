#!/usr/bin/env python3
"""Render the contract backlog as a register a person can read.

    python3 tools/build-backlog-index.py

`handoff/contract-backlog.json` is the machine copy and nothing reads JSON by choice. This
writes `docs/registers/contract-backlog.md` beside `conflicts.md`, in the same shape, so a
queued edit is as visible as a conflict.

**Why this exists rather than one CF per gap.** Every gap the walk finds could be raised as a
conflict, and at three per section across 146 sections the register would end near 450 entries.
A conflict register is where a decision lives — *two sources disagree, or a decision is required
and absent.* A missing operation we have already decided to build is work, not a conflict, and
mixing the two makes the twenty open decisions harder to see rather than easier. So: **anything
carrying a decision or a cost gets a CF, everything else gets a row here**, and every row names
its CF where it has one.

Nothing in this file is hand-maintained. Run it after editing the backlog.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# A cp1252 console cannot encode the arrows and dashes this tool prints, and the
# failure lands *after* the work is done — so the output is written, the summary
# line raises UnicodeEncodeError, and a correct run exits 1. Reconfiguring at
# import means anything importing this module gets it too, refresh.sh included.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:      # a captured stream may not be reconfigurable; harmless
    pass


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "handoff" / "contract-backlog.json"
INDEX = ROOT / "docs" / "registers" / "contract-backlog.md"
if not INDEX.parent.exists():
    INDEX = ROOT / "registers" / "contract-backlog.md"

LANES = [
    ("decision", "Needs a decision — tracked as a conflict",
     "Each of these has a CF. The register holds the reasoning; this is the index."),
    ("deferred", "Deferred — waiting on a section",
     "Crosses contracts, or has no precedent to copy. Deciding now would design it in the "
     "wrong contract. Each names what unblocks it."),
    ("settled", "Settled — made at section close",
     "One contract, and that contract already shows how it should look."),
]


def main() -> int:
    if not SOURCE.exists():
        print("no backlog to render")
        return 0

    doc = json.loads(SOURCE.read_text(encoding="utf-8"))
    entries = doc.get("entries") or []
    open_ = [e for e in entries if e.get("status") == "open"]
    done = [e for e in entries if e.get("status") == "done"]
    withdrawn = [e for e in entries if e.get("status") == "withdrawn"]

    out = [
        "# Contract backlog — index\n",
        f"**{len(entries)} edits raised by the requirement walk — {len(open_)} open, "
        f"{len(done)} done, {len(withdrawn)} withdrawn.**\n",
        "Generated from `handoff/contract-backlog.json` by `tools/build-backlog-index.py`.",
        "Every gap the walk finds lands here. **The ones carrying a decision or a cost also "
        "carry a CF** and are in `conflicts.md`; the rest are work rather than conflict, and "
        "putting them in the conflict register would bury the open decisions among them.\n",
        "| Lane | Open |", "|---|---|",
    ]
    for key, title, _ in LANES:
        out.append(f"| {title.split(' — ')[0]} | **{sum(1 for e in open_ if e.get('lane') == key)}** |")
    out.append(f"| **Total open** | **{len(open_)}** |\n")

    for key, title, blurb in LANES:
        sel = [e for e in open_ if e.get("lane") == key]
        if not sel:
            continue
        out += [f"\n## {title} — {len(sel)}\n", blurb + "\n",
                "| ID | Section | Refs | What | Contracts | Blocked on | CF |",
                "|---|---|---|---|---|---|---|"]
        for e in sel:
            refs = ", ".join(e.get("refs") or [])
            if len(refs) > 46:
                refs = refs[:43] + "…"
            cons = ", ".join(e.get("contracts") or e.get("candidateHomes") or [])
            out.append(
                f"| **{e['id']}** | {e.get('section','')} | {refs} | "
                f"{' '.join(str(e.get('what','')).split())} | `{cons}` | "
                f"{e.get('blockedOn') or '—'} | {e.get('cf') or '—'} |")

    if done or withdrawn:
        out += ["\n## Closed\n",
                "| ID | Section | What | Resolution |", "|---|---|---|---|"]
        for e in done + withdrawn:
            state = "**Done.** " if e.get("status") == "done" else "**Withdrawn.** "
            out.append(f"| **{e['id']}** | {e.get('section','')} | "
                       f"{' '.join(str(e.get('what','')).split())} | "
                       f"{state}{e.get('closedBy') or e.get('why','')} |")

    out += ["\n## Why an edit is deferred rather than made\n",
            "The test is applied, not judged: **does this edit touch only the contract being "
            "walked, and does that contract already contain a precedent for how it should "
            "look?** Both yes is settled. Anything else is deferred.\n",
            "It was written as a test because judgement got it wrong the first time it was "
            "used. **BL-002 — the missing footer — looks like an obvious mirror of the "
            "header** until you notice a header is chrome and a footer is a link surface "
            "pointing at policy records the CMS may already compose. Instinct said build it; "
            "the test said wait.\n"]

    INDEX.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{INDEX.relative_to(ROOT)}: {len(entries)} entries · {len(open_)} open")
    for key, title, _ in LANES:
        print(f"  {sum(1 for e in open_ if e.get('lane') == key):>4}  {key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
