#!/usr/bin/env python3
"""Attach the four 11 September books to the graph, the way the September boards were attached.

**340 screens arrived from `Latest Docs.zip` with no navigation at all** — Digital Asset
Management (40, P13), Game & Ride (100, P08), Rental Management (100, P08) and Subscription
Licensing & AI Self-Service (100, P09). `derive-board-flows.py` skipped all 34 of their boards:
*"no hub-and-spoke route in the navigation"*.

**The rule is `wire-pack-boards.py`'s, unchanged.** Screen 1 of a board is its hub; the hub hangs
off the platform's home screen; every other screen hangs off the hub and goes back to it; both
edges are labelled and the provenance leads with `structural`. See that file for why that is the
honest guess and not a derivation.

**Why a sibling and not a re-run of that file.**

- **It groups by `(platform, board)`.** Game & Ride and Rental both have boards 1–10 on P08, so
  each pair would have merged into one twenty-screen board with one hub. This groups by
  `(platform, source.pack, source.board)`, read from the screen's own `source` block rather than
  by looking its title up in the pack, which is ambiguous when titles repeat across books.
- **Its collapse path is a one-off that already ran.** `ANL-011` is gone, so re-running it over
  the September packs would promote a different screen to hub and write edges nobody decided.

**What is not claimed**, as before: no `carries`, because nothing is known to travel, and no
`control`, because these screens lay out no components yet.

Idempotent — it adds an edge only where one is missing and never rewrites one that exists.
Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations
import collections
import glob
import os
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACKS = {"Digital Asset Management DAM.pdf", "Game_and_Ride_Module.pdf",
         "Rental_Management.pdf", "Subscription_Licensing_AI_Self_Service.pdf"}
PROVENANCE = "structural — pack board {board} wiring, 11 September 2026"


def add(seq: list, v: str) -> bool:
    if v in seq:
        return False
    seq.append(v)
    seq.sort()
    return True


def label(nav: dict, to: str, trigger: str, board: str, back: bool = False) -> None:
    tr = nav.setdefault("transitions", [])
    if any(str(t.get("to", "")).partition("#")[0] == to for t in tr):
        return
    entry = {"to": to, "trigger": trigger, "provenance": PROVENANCE.format(board=board)}
    if back:
        entry["back"] = True
    tr.append(entry)


def number(s: dict) -> tuple:
    return tuple(int(p) for p in str((s.get("source") or {}).get("number") or "999").split("."))


def main() -> int:
    apply = "--apply" in sys.argv

    docs, screens, plat, home = {}, {}, {}, {}
    for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml"))):
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        docs[f] = d
        code = d["platform"]["code"]
        for s in d.get("screens") or []:
            screens[s["id"]] = s
            plat[s["id"]] = code
            if (s.get("navigation") or {}).get("isEntryPoint"):
                home[code] = s["id"]

    groups: dict = collections.defaultdict(list)
    for i, s in screens.items():
        src = s.get("source") or {}
        if src.get("pack") in PACKS:
            groups[(plat[i], src["pack"], str(src.get("board")))].append(s)

    edges, hubs = 0, []
    for (code, pack, board), rows in sorted(groups.items()):
        if code not in home:
            print(f"  {code} declares no entry point — {pack} board {board} left unwired")
            continue
        rows.sort(key=lambda s: (number(s), s["id"]))
        hub, homeid = rows[0], home[code]
        hubs.append(f"{homeid} → {hub['id']}  {pack[:28]} board {board} ({len(rows)} screens)")

        hn = hub.setdefault("navigation", {})
        hm = screens[homeid].setdefault("navigation", {})
        if hub["id"] not in (hm.get("exitTo") or []) or homeid not in (hn.get("entryFrom") or []):
            edges += 1
        if apply:
            add(hm.setdefault("exitTo", []), hub["id"])
            add(hn.setdefault("entryFrom", []), homeid)
            add(hn.setdefault("exitTo", []), homeid)
            label(hm, hub["id"], hub["name"], board)
            label(hn, homeid, f"Back to {screens[homeid]['name']}", board, back=True)

        for child in rows[1:]:
            cn = child.setdefault("navigation", {})
            if child["id"] in (hn.get("exitTo") or []) and hub["id"] in (cn.get("exitTo") or []):
                continue
            edges += 1
            if apply:
                add(hn.setdefault("exitTo", []), child["id"])
                add(cn.setdefault("entryFrom", []), hub["id"])
                add(cn.setdefault("exitTo", []), hub["id"])
                label(hn, child["id"], child["name"], board)
                label(cn, hub["id"], f"Back to {hub['name']}", board, back=True)

    sizes = collections.Counter(len(v) for v in groups.values())
    print(f"{len(groups)} board group(s), {sum(len(v) for v in groups.values())} screen(s), "
          f"board sizes {dict(sizes)}")
    for h in hubs:
        print(f"  {h}")
    if not edges:
        print("nothing to do — every board is already attached")
        return 0
    print(f"\n{edges} screen(s) {'wired' if apply else 'to wire (run with --apply)'}")

    if apply:
        # Only the files whose content changed, and through a temporary file: a failed write on
        # the target truncates it, and rewriting untouched files buries the real diff.
        written = 0
        for f, d in docs.items():
            path = pathlib.Path(f)
            text = yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100)
            if yaml.safe_load(path.read_text(encoding="utf-8")) == d:
                continue
            tmp = path.with_name(path.name + ".tmp")
            tmp.write_text(text, encoding="utf-8")
            os.replace(tmp, path)
            written += 1
        print(f"written to {written} platform file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
