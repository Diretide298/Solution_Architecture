#!/usr/bin/env python3
"""Attach the September pack boards to the graph they were ingested beside.

**140 screens arrived in September with no navigation at all** — no `exitTo`, no `entryFrom`, no
operations, all wave 3 — from two packs: `Approval_Workflows_and_Governance` (80 across P08 and
P09) and `Unified_BI_Reporting_and_AI_Analytics` (60 on P16). They are not screens that lost their
links. They are headings that were never wired to anything, and every reachability warning in the
package traces to them.

**There is no navigation in the packs to derive from.** A pack entry carries `board`, `area`,
`number`, `page`, `purpose`, `acceptance` and `terms` — and no edges at all. So this is a
structural decision, recorded as one, not a derivation dressed up as evidence:

- **The board is the unit.** The 140 fall into fourteen board groups of ten, each led by a Command
  Center, a Library or a Workspace — the screen the board was drawn around. That screen is the hub.
  Board numbers repeat across the two packs, so the group is (platform, board), not board alone.
- **The hub hangs off the platform's home screen** — `BO-100 Venue Home`, `ADM-002 Platform
  Dashboard`, `ANL-001 Executive Command Center`. A new product area is reachable from the home
  screen; nothing else in the package is a more honest guess, and a guess dressed as a flow
  citation would be worse than one labelled as what it is.
- **Children hang off the hub and go back to it.** Two edges, so the board is navigable rather
  than a one-way list.
- **Both edges are labelled**, because on a command centre the control genuinely is a tile
  bearing the screen's name, and on a child the way back is a named return. `provenance` leads
  with `structural ` so no reader mistakes it for something observed in a flow or on a board.
  What is *not* claimed: no `carries`, because nothing is known to travel, and no `control`,
  because these screens lay out no components yet.

**`ANL-011` is not wired — it is collapsed.** It is name-identical to `ANL-001`, which is P16's
entry point and already carries 4 operations, 9 exits and the domain filter; `ANL-011` carries
none of those. The BI pack redrew a screen the platform already had. Its 9 siblings attach to
`ANL-001` instead, and its `purpose` and its gap are carried onto `ANL-001` rather than deleted —
the same carry rule the generators follow.

`ADM-321 Visual Workflow Designer` is also a duplicate, of `ADM-241`. It is **left in place and
reported**: unlike `ANL-011` it is a child rather than a hub, and which of the two survives is a
question about the workflow designer, not about navigation.

Idempotent. Run with no arguments to see what it would do; `--apply` to write.
"""

from __future__ import annotations
import collections
import glob
import io
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
HOME = {"P08": "BO-100", "P09": "ADM-002", "P16": "ANL-001"}
COLLAPSE = {"ANL-011": "ANL-001"}
PACKS = {"Approval_Workflows_and_Governance_Reference.pdf",
         "Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf"}


def add(seq: list, v: str) -> bool:
    if v in seq:
        return False
    seq.append(v)
    seq.sort()
    return True


def label(nav: dict, to: str, trigger: str, board, back: bool = False) -> None:
    """Say how the move is made, and be explicit that it is structure rather than observation."""
    tr = nav.setdefault("transitions", [])
    if any(str(t.get("to", "")).partition("#")[0] == to for t in tr):
        return
    entry = {"to": to, "trigger": trigger,
             "provenance": f"structural — pack board {board} wiring, 9 September 2026"}
    if back:
        entry["back"] = True
    tr.append(entry)


def main() -> int:
    apply = "--apply" in sys.argv

    docs, screens, plat = {}, {}, {}
    for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml"))):
        d = yaml.safe_load(open(f, encoding="utf-8")) or {}
        docs[f] = d
        for s in d.get("screens") or []:
            screens[s["id"]] = s
            plat[s["id"]] = d["platform"]["code"]

    # **Selected by which pack they came from, not by whether they are wired.** Selecting on
    # "has no navigation" worked once and then reported nothing to do on the second run, because
    # the first run had wired them — a tool that cannot see its own output cannot maintain it.
    stranded = [i for i, s in screens.items()
                if plat[i] in HOME
                and str((s.get("source") or {}).get("pack") if isinstance(s.get("source"), dict)
                        else "") in PACKS]

    pack = json.load(io.open(ROOT / "sources" / "workshop" / "pack.json", encoding="utf-8"))
    by_title = {}
    for e in pack:
        by_title.setdefault(str(e.get("title", "")).strip().lower(), e)

    groups: dict = collections.defaultdict(list)
    for i in stranded:
        e = by_title.get(screens[i]["name"].strip().lower()) or {}
        groups[(plat[i], e.get("board", "?"))].append((e.get("number"), i))

    todo, edges = [], 0
    for (code, board), rows in sorted(groups.items()):
        rows.sort(key=lambda r: (r[0] is None, r[0], r[1]))
        ids = [i for _, i in rows]

        hub = ids[0]
        if hub in COLLAPSE:
            # The hub is a duplicate of a screen that already exists and already works.
            target = COLLAPSE[hub]
            todo.append(f"collapse {hub} into {target}; its {len(ids) - 1} sibling(s) attach there")
            if apply:
                keep, drop = screens[target], screens[hub]
                if drop.get("purpose") and drop["purpose"] != keep.get("purpose"):
                    keep.setdefault("purposeNote", drop["purpose"])
                for g in (drop.get("gaps") or []):
                    keep.setdefault("gaps", []).append(g)
                for d in docs.values():
                    before = len(d["screens"])
                    d["screens"] = [s for s in d["screens"] if s["id"] != hub]
                    # **Removing a screen means the platform's own count is now wrong.**
                    # `check-package` compares them and fails, which is the check working.
                    if len(d["screens"]) != before and "screenCount" in d["platform"]:
                        d["platform"]["screenCount"] = len(d["screens"])
            hub, ids = target, ids[1:]

        home = HOME[code]
        if hub != home:
            hn = screens[hub].setdefault("navigation", {})
            hm = screens[home].setdefault("navigation", {})
            hub_labelled = any(str(t.get("to", "")).partition("#")[0] == hub
                               for t in (hm.get("transitions") or []))
            if (home not in (hn.get("entryFrom") or []) or hub not in (hm.get("exitTo") or [])
                    or not hub_labelled):
                todo.append(f"{home} → {hub}  (hub of board {board}, {len(ids)} screen(s))")
                edges += 1
                if apply:
                    add(hm.setdefault("exitTo", []), hub)
                    add(hn.setdefault("entryFrom", []), home)
                    add(hn.setdefault("exitTo", []), home)
                    label(hm, hub, screens[hub]["name"], board)
                    label(hn, home, f"Back to {screens[home]['name']}", board, back=True)

        for child in ids:
            if child == hub:
                continue
            cn = screens[child].setdefault("navigation", {})
            hn = screens[hub].setdefault("navigation", {})
            wired = child in (hn.get("exitTo") or [])
            labelled = any(str(t.get("to", "")).partition("#")[0] == child
                           for t in (hn.get("transitions") or []))
            if wired and labelled:
                continue
            edges += 1
            if apply:
                add(hn.setdefault("exitTo", []), child)
                add(cn.setdefault("entryFrom", []), hub)
                add(cn.setdefault("exitTo", []), hub)
                label(hn, child, screens[child]["name"], board)
                label(cn, hub, f"Back to {screens[hub]['name']}", board, back=True)

    if not todo and not edges:
        print("nothing to do — every pack board is already attached")
        return 0

    print(f"{len(groups)} board group(s), {len(stranded)} stranded screen(s)")
    for t in todo:
        print(f"  {t}")
    print(f"\n{edges} edge(s) {'written' if apply else 'pending (run with --apply)'}")

    if apply:
        for f, d in docs.items():
            pathlib.Path(f).write_text(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100),
                encoding="utf-8")
        print(f"written to {len(docs)} platform file(s)")

    dupes = [i for i in screens
             if i != "ANL-011"
             and any(j != i and screens[j]["name"].strip().lower() == screens[i]["name"].strip().lower()
                     and plat[j] == plat[i] for j in screens)]
    if dupes:
        print(f"\nStill duplicated by name, left for a person: {', '.join(sorted(dupes)[:8])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
