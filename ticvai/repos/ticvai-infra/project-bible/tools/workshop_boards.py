"""The `WS##` code of every client workshop board, issued once and never renumbered.

**A `WS` code used to be a position, not a name.** Three tools — `derive-design-manifest`,
`derive-wireframes` and `check-board-flows` — each numbered the boards by enumerating them in sorted
order. They agreed with one another, and every one of them renumbered the moment a book arrived
whose name sorted early. On 11 September `Digital Asset Management` and `Game and Ride` did exactly
that: 47 of the 73 boards moved, `WS27` stopped meaning `Group Sales board 1` and started meaning
`Digital Asset Management board 1`, and 47 design bundles on disk named a board they no longer held.

Nothing had been drawn against a `WS` code yet, which is the only reason it cost nothing. A code
that ends up in a queue, a batch log, `wireframes/incoming/<BATCH-ID>/` and a client conversation
has to mean one board for good, the way a screen id does.

So codes live in `screens/_workshop-boards.yaml`, beside the screen id register. **A board that has
a code keeps it; a new board gets the next number**, in sorted order within the arrivals of one run
so that two people running the same refresh issue the same codes. A board that disappears keeps its
code in the file, unissued, rather than freeing it for reuse.

The first 73 were seeded from the manifest committed before the 11 September intake, so every code
that existed before that day still names the board it named then.
"""
from __future__ import annotations

import os
from collections import Counter
from pathlib import Path

import yaml

REGISTER = Path(__file__).resolve().parents[1] / "screens" / "_workshop-boards.yaml"


def label(module: str, board: int) -> str:
    return "%s board %d" % (module, int(board))


def codes(keys, write: bool = False) -> dict:
    """`(module, board)` -> `WS##` for every key, issuing codes for boards the register lacks.

    `write=False` issues them in memory only — a checker must not be the thing that changes the
    register, but it still has to be able to name a board a refresh has not yet recorded.
    """
    doc = {}
    if REGISTER.exists():
        doc = yaml.safe_load(REGISTER.read_text(encoding="utf-8")) or {}
    boards: dict = dict(doc.get("boards") or {})
    by_label = {v: k for k, v in boards.items()}
    nxt = max((int(c[2:]) for c in boards), default=0) + 1

    # Sorted by module and then board *number* — as strings, `board 10` issues before `board 2`.
    fresh = [label(m, b) for m, b in sorted({(m, int(b)) for m, b in keys})
             if label(m, b) not in by_label]
    for lab in fresh:
        code = "WS%02d" % nxt
        boards[code] = lab
        by_label[lab] = code
        nxt += 1

    if fresh and write:
        doc["boards"] = dict(sorted(boards.items(), key=lambda kv: int(kv[0][2:])))
        tmp = REGISTER.with_name(REGISTER.name + ".tmp")
        tmp.write_text(
            "# Issued by tools/workshop_boards.py. A code is never renumbered or reused — see there.\n"
            + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8")
        os.replace(tmp, REGISTER)

    return {(m, int(b)): by_label[label(m, b)] for m, b in keys}


def sort_key(code: str) -> int:
    """`WS100` after `WS99` — as text, WS100–WS107 sort before WS11."""
    return int(code[2:])


def home_platforms(rows) -> dict:
    """`(module, board)` -> the one platform a workshop board is drawn on.

    `rows` is `(key, platform, number)` for every pack screen. **The majority wins, and a tie goes
    to the platform of the board's first screen** — its hub — rather than to whichever file loaded
    first. Found 11 September: Subscription 6.10 moved to P08 while 6.1–6.9 stayed on P09, and
    `derive-design-manifest.py` and `derive-wireframes.py` must agree on where the board lives or
    a screen is tagged `WS103` on one board and batched somewhere else.
    """
    counts: dict = {}
    first: dict = {}
    for key, platform, number in rows:
        counts.setdefault(key, Counter())[platform] += 1
        try:
            n = tuple(int(p) for p in str(number).split("."))
        except ValueError:
            n = (10 ** 6,)
        if key not in first or n < first[key][0]:
            first[key] = (n, platform)
    out = {}
    for key, c in counts.items():
        top = max(c.values())
        leaders = {p for p, v in c.items() if v == top}
        out[key] = first[key][1] if first[key][1] in leaders else sorted(leaders)[0]
    return out
