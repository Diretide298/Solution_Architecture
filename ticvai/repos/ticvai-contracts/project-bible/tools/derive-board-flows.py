#!/usr/bin/env python3
"""One process flow per client board, routed through the navigation the screens actually declare.

**The client gave us 73 boards and the package described none of them.** Measured 10 September:
728 screens carry a `source.pack`, and not one appeared in any of the 95 flows. The two halves of
the package -- what the client specified and what we said happens -- did not touch anywhere.

**Why this can be derived at all.** Each board is a hub and nine spokes: the hub declares an exit
to every spoke and each spoke declares one back. That is a real navigation graph, so a route
through a board is not invented, it is read. The client's own ordering survives too, in
`source.number` ("8.1.1", "8.1.2"), so the steps run in the order the board was written.

**What is derived and what is not.**

- *Derived*: the route, the operations each screen declares, the wave, the contracts touched, and
  the branches -- which come from the `states` each screen declares, not from imagination.
- *Not derived, and deliberately absent*: **why anyone walks the journey.** A derived flow knows
  the order of the screens and nothing about the reason. `purpose` is quoted from the screen
  rather than paraphrased, so no sentence here claims more than the screen already claimed.

**These are scaffolding and say so.** Every file carries `provenance: derived-from-board`, and
`check-board-flows.py` counts them apart from authored flows for exactly that reason: a generator
that could mark all 73 boards covered in one run would otherwise report the work finished on the
day it started.

**Single apply, not part of refresh.** Flows get hand-edited -- the authored ones carry dated
corrections -- and a generator in `refresh.sh` would overwrite that work every run. It writes only
files that do not exist, so a flow someone has since authored is never touched.

    python3 tools/derive-board-flows.py [--apply]
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
FLOWS = ROOT / "flows"

# The actor a board's screens belong to, by the platform they live on. Taken from the vocabulary
# the authored flows already use, so a reader is not asked to learn a second set of words.
ACTOR = {
    "P01": "guest", "P02": "guest", "P05": "guest",
    "P04": "cashier", "P15": "cashier",
    "P06": "supervisor", "P07": "gateOperator",
    "P08": "venueManager", "P12": "venueManager", "P13": "venueManager", "P16": "venueManager",
    "P09": "platformAdmin", "P10": "partner", "P11": "platformAdmin", "P14": "platformAdmin",
}


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def module_of(pack: str) -> str:
    """Stripped exactly as `derive-wireframes.ws_map` strips it, or the codes would disagree."""
    s = re.sub(r"\.pdf$", "", pack, flags=re.I)
    s = re.sub(r"[_ ]*Reference$", "", s, flags=re.I)
    s = re.sub(r"[_ ]*Module$", "", s, flags=re.I)
    return s.replace("_", " ").strip() or pack


def numkey(n) -> tuple:
    """'8.1.10' sorts after '8.1.2'. String order would put the client's tenth screen third."""
    out = []
    for part in str(n or "").split("."):
        out.append(int(part) if part.isdigit() else 0)
    return tuple(out)


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:60].rstrip("-")


def load():
    screens, board, plat_of = {}, {}, {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        code = f.name.split("-")[0]
        pl = doc.get("platform") or {}
        for sc in (doc.get("screens") or []):
            screens[sc["id"]] = sc
            plat_of[sc["id"]] = (code, pl.get("shortName") or pl.get("name") or code)
            src = sc.get("source") or {}
            if src.get("pack") and src.get("board") is not None:
                board[sc["id"]] = (module_of(src["pack"]), int(src["board"]))
    return screens, board, plat_of


def ops_of(sc: dict) -> list:
    return [a["operationId"] for a in (sc.get("apis") or []) if isinstance(a, dict)]


def contracts_of(sc: dict) -> set:
    return {a.get("contract") for a in (sc.get("apis") or [])
            if isinstance(a, dict) and a.get("contract")}


def build(key, ids, screens, plat_of, fid):
    module, bnum = key
    ordered = sorted(ids, key=lambda i: numkey((screens[i].get("source") or {}).get("number")))

    # **The hub is the screen the others exit to**, not the first by number -- on some boards those
    # are different screens, and routing from the wrong one produces a flow whose every step is a
    # link that does not exist.
    same = {i: [e for e in ((screens[i].get("navigation") or {}).get("exitTo") or []) if e in ids]
            for i in ids}
    hub = max(ordered, key=lambda i: len(same[i]))
    spokes = [i for i in ordered
              if i != hub and (hub in same.get(i, []) or i in same.get(hub, []))]
    if not spokes:
        return None

    code, short = plat_of[hub]
    wave = max((screens[i].get("wave") or 1) for i in ([hub] + spokes))
    joined = set()
    for i in [hub] + spokes:
        joined |= contracts_of(screens[i])
    contracts = sorted(joined) or ["unknown"]

    steps = []
    n = 1
    steps.append({
        "step": n, "screen": hub,
        "action": "Opens " + str(screens[hub].get("name")),
        "operations": ops_of(screens[hub])[:4],
        "outcome": (screens[hub].get("purpose") or "").strip() or "The board's landing screen",
    })
    for sp in spokes:
        n += 1
        steps.append({
            "step": n, "screen": sp,
            "action": "Works in " + str(screens[sp].get("name")),
            "operations": ops_of(screens[sp])[:4],
            "outcome": (screens[sp].get("purpose") or "").strip() or "As the board specifies",
        })
        if sp != spokes[-1]:
            n += 1
            steps.append({
                "step": n, "screen": hub,
                "action": "Returns to the board's landing screen",
                "operations": ops_of(screens[hub])[:1],
                "outcome": "Ready for the next screen on this board",
            })

    # **Branches from declared states, never from invention.** A screen that declares
    # `emptyNoAccess` has already said this journey can be stopped by permission; a screen that
    # does not has said nothing, and this tool must not say it for them.
    branches = []
    hub_states = list((screens[hub].get("states") or {}).keys())
    if "emptyFirstRun" in hub_states:
        branches.append({
            "at": 1,
            "condition": "Nothing has been set up on " + str(screens[hub].get("name")) + " yet",
            "behaviour": ("The screen declares `emptyFirstRun`. **On a new tenant this is the "
                          "expected state**, and it is a different situation from an empty result "
                          "on an established one."),
            "severity": "expected", "resolvedBy": "Automatic",
        })
    noaccess = None
    for st in steps:
        if "emptyNoAccess" in (screens[st["screen"]].get("states") or {}):
            noaccess = st
            break
    if noaccess:
        branches.append({
            "at": noaccess["step"],
            "condition": "The operator does not hold the permission this screen requires",
            "behaviour": ("The screen declares `emptyNoAccess`. **The journey stops here rather "
                          "than failing later**, which is the right shape -- but the permission "
                          "that would satisfy it is not granted by any role in `roles.yaml`."),
            "severity": "requiresStaff", "resolvedBy": "Unresolved -- see the permission join",
        })
    if not branches:
        branches.append({
            "at": 1,
            "condition": "The board's screens declare no failure state",
            "behaviour": ("**Nothing here says what happens when this goes wrong.** That is a gap "
                          "in the screens rather than in the journey, and it is recorded as a "
                          "branch so it is not mistaken for a journey that cannot fail."),
            "severity": "requiresStaff", "resolvedBy": "Unresolved -- the screens are silent",
        })

    return {
        "id": fid,
        "name": module + " board " + str(bnum) + ": " + str(screens[hub].get("name")),
        "actor": ACTOR.get(code, "venueManager"),
        "wave": wave,
        "frequency": "routine",
        "criticality": "operational",
        "platforms": [code + " " + str(short)],
        "provenance": "derived-from-board",
        "offlineBehaviour": ("Not stated by the board. **The client's reference does not say**, "
                             "and this flow will not guess."),
        "trigger": {
            "description": ("The work the client grouped as " + module + " board " + str(bnum) +
                            ". **This route is read from the screens' own navigation**, and the "
                            "reason anyone walks it has still to be written."),
            "entryScreen": hub,
            "entryPoints": ["Arrives at " + str(screens[hub].get("name"))],
        },
        "steps": steps,
        "branches": branches,
        "exitStates": [
            {"state": "completed",
             "description": "Every screen on " + module + " board " + str(bnum) + " visited"},
        ],
        "primaryContract": contracts[0],
        "contracts": contracts,
    }


def main() -> int:
    _utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    screens, board, plat_of = load()
    by_board = collections.defaultdict(set)
    for sid, key in board.items():
        by_board[key].add(sid)

    used = set()
    authored_screens = set()
    for f in FLOWS.glob("*.yaml"):
        m = re.match(r"F(\d+)", f.name)
        if m:
            used.add(int(m.group(1)))
        text = f.read_text(encoding="utf-8")
        doc = yaml.safe_load(text) or {}
        # A board an authored flow already reaches is left alone.
        if not str(doc.get("provenance", "")).startswith("derived"):
            authored_screens |= set(re.findall(r"\b[A-Z]{2,4}-\d{3}\b", text))
    nxt = max(used) + 1 if used else 1

    written, skipped = [], []
    for key in sorted(by_board):
        ids = by_board[key]
        if ids & authored_screens:
            skipped.append((key, "an authored flow already reaches it"))
            continue
        fid = "F%d" % nxt
        doc = build(key, ids, screens, plat_of, fid)
        if not doc:
            skipped.append((key, "no hub-and-spoke route in the navigation"))
            continue
        path = FLOWS / (fid + "-" + slug(doc["name"]) + ".yaml")
        if path.exists():
            skipped.append((key, path.name + " exists"))
            continue
        written.append((path, doc))
        nxt += 1

    for path, doc in written:
        print("  %-6s %-58s %2d steps" % (doc["id"], doc["name"][:58], len(doc["steps"])))
    for key, why in skipped:
        print("  skip   %-36s board %-3s %s" % (key[0][:34], key[1], why))

    print("\n%d flow(s) to write, %d skipped" % (len(written), len(skipped)))
    if not a.apply:
        print("run with --apply to write")
        return 0

    for path, doc in written:
        path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                        encoding="utf-8")
    print("written to %s/" % FLOWS.relative_to(ROOT))
    print("run tools/check-flows.py and tools/check-board-flows.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
