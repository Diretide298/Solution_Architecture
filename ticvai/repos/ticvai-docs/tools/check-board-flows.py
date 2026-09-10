#!/usr/bin/env python3
"""Which client boards have a process flow, and which screens the flows name that do not exist.

**The client gave us 73 boards; the flows describe a different package.** Measured 10 September:
728 screens carry a `source.pack`, and not one of them appears in any flow — not as a step, not as
an entry screen, not as a bare string. The 95 flows reference 283 screen ids of which 271 are
non-pack screens. The two halves of the package do not touch.

That is worth a checker rather than a one-off count, because it is the kind of gap that closes
slowly and silently: a flow written today covers one board, and nothing would otherwise say
whether it was the seventy-third or the first.

**Two questions, one pass.**

1. **Coverage** — for each client board, how many of its screens any flow reaches. A board with
   zero is a board the client specified and no one has described the process for.
2. **Dangling references** — screen ids a flow names that match no screen in the package. A flow
   step pointing at nothing is a step nobody can build, and it reads as covered until you look.

Reports; never writes. Exit is 0 unless a flow names a screen that does not exist — an absent flow
is work not yet done, but a flow pointing at a missing screen is a defect in what we have.

    python3 tools/check-board-flows.py [--verbose]
"""

from __future__ import annotations

import collections
import glob
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCREEN_ID = re.compile(r"\b[A-Z]{2,4}-\d{3}\b")


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def module_of(pack: str) -> str:
    """The module name, stripped exactly as `derive-wireframes.ws_map` strips it.

    The two must agree or a board would carry one code on the wireframes and another here, which
    is worse than having no code at all.
    """
    s = re.sub(r"\.pdf$", "", pack, flags=re.I)
    s = re.sub(r"[_ ]*Reference$", "", s, flags=re.I)
    s = re.sub(r"[_ ]*Module$", "", s, flags=re.I)
    return s.replace("_", " ").strip() or pack


def main() -> int:
    _utf8()
    verbose = "--verbose" in sys.argv

    board_screens: dict = collections.defaultdict(set)
    screen_board: dict = {}
    all_ids: set = set()
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for sc in (doc.get("screens") or []):
            all_ids.add(sc["id"])
            src = sc.get("source") or {}
            if src.get("pack") and src.get("board") is not None:
                key = (module_of(src["pack"]), int(src["board"]))
                board_screens[key].add(sc["id"])
                screen_board[sc["id"]] = key

    keys = sorted(board_screens)
    ws = {k: "WS%02d" % i for i, k in enumerate(keys, 1)}

    # **Every screen id a flow names, however it names it.** Reading only `steps[].screen` missed
    # entry screens and the ids that appear in prose, and a checker that undercounts coverage is
    # one that manufactures work.
    # **Only ids whose prefix names a real screen family.** The first pass reported `CF-101` and
    # `BL-127` as missing screens; they are a conflict id and a backlog id quoted in prose. A
    # checker that cries wolf on registries it does not know about gets muted, and then the four
    # real ones underneath go unread with it.
    prefixes = {i.split("-")[0] for i in all_ids}

    named: set = set()
    derived_named: set = set()
    flows_of: dict = collections.defaultdict(set)
    derived_of: dict = collections.defaultdict(set)
    # **`_schema.yaml` is not a flow.** Globbing `*.yaml` counted it and reported 169 where
    # `build-status` reported 168, and two tools disagreeing about how many flows exist is exactly
    # the drift these checkers are here to catch.
    flow_files = sorted(glob.glob(str(ROOT / "flows" / "F*.yaml")))
    for path in flow_files:
        text = pathlib.Path(path).read_text(encoding="utf-8")
        doc = yaml.safe_load(text) or {}
        fid = doc.get("id") or pathlib.Path(path).stem
        # **A derived flow is scaffolding, not coverage.** The generator can put a flow against
        # all 73 boards in one run, and if that counted the same as an authored one this checker
        # would report the job finished on the day it started. They are counted apart, and the
        # authored number is the one that means anything.
        derived = str(doc.get("provenance", "")).startswith("derived")
        for sid in SCREEN_ID.findall(text):
            if sid.split("-")[0] not in prefixes:
                continue
            named.add(sid)
            if derived:
                derived_named.add(sid)
            if sid in screen_board:
                (derived_of if derived else flows_of)[screen_board[sid]].add(fid)

    covered = [k for k in keys if board_screens[k] & (named - derived_named)]
    scaffolded = [k for k in keys if k not in covered and board_screens[k] & derived_named]
    bare = [k for k in keys if not (board_screens[k] & named)]
    dangling = sorted(named - all_ids)

    pack_total = sum(len(v) for v in board_screens.values())
    pack_named = len(set().union(*board_screens.values()) & named) if board_screens else 0

    print(f"{len(flow_files)} flow(s) · {len(keys)} client board(s) · {pack_total} board screen(s)")
    print(f"  boards with an authored flow  : {len(covered)}")
    print(f"  boards with only a derived one: {len(scaffolded)}")
    print(f"  boards with no flow at all    : {len(bare)}")
    print(f"  board screens named by a flow: {pack_named}/{pack_total}")

    if verbose and bare:
        print("\n  no flow describes these boards:")
        for k in bare:
            print(f"    {ws[k]}  {k[0][:44]:46} board {k[1]:>2}  {len(board_screens[k]):>3} screens")
    if covered:
        print("\n  covered:")
        for k in covered:
            n = len(board_screens[k] & named)
            print(f"    {ws[k]}  {k[0][:34]:36} b{k[1]:<3} {n:>2}/{len(board_screens[k]):<3} "
                  f"{', '.join(sorted(flows_of[k]))}")

    if dangling:
        print(f"\n  {len(dangling)} screen id(s) named by a flow that no screen file defines —")
        print("  a step pointing at nothing reads as covered until you look:")
        for sid in dangling:
            who = sorted(f for f in flow_files
                         if sid in pathlib.Path(f).read_text(encoding="utf-8"))
            print(f"    {sid}  named by {', '.join(pathlib.Path(w).stem[:3] for w in who)}")

    if bare:
        print(f"\n**{len(bare)} of {len(keys)} client boards have no process flow.** The client "
              "specified these; nothing in the package describes how they are used.")
    if scaffolded:
        print(f"**{len(scaffolded)} board(s) carry a derived flow and no authored one.** A derived "
              "flow routes the screens and names the operations they declare; it does not know why "
              "anyone walks the journey. It is a place to write, not a thing that is written.")
    print("\nFAIL" if dangling else "\nPASS", f"— {len(dangling)} dangling reference(s)")
    return 1 if dangling else 0


if __name__ == "__main__":
    sys.exit(main())
