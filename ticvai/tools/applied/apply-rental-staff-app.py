#!/usr/bin/env python3
"""Put Rental's frontline boards on the staff app as well as on venue management.

**Decided 11 September 2026:** Rental Management boards 6, 7 and 8 — *Rental Checkout & Equipment
Assignment*, *Active Rental Operations & Monitoring*, *Rental Return, Damage Assessment &
Settlement* — "can go to staff app and also in venue management". They were placed on P08 alone
when `Latest Docs.zip` was ingested, which took P08 to 593 screens and put the work of handing a
guest a paddleboard at a desktop.

**Both, not a move.** A supervisor still watches active rentals and settles a damage dispute from
the back office; the attendant at the rental counter does the handover and the return on a device
they carry. So the thirty P08 screens stay, and P06 gets thirty of its own.

## Why a P06 screen does not claim the pack entry

Each P06 screen carries `source.sameAs` — the P08 screen it is the staff-app form of — and
**not** `source.pack`. Three tools key on `source.pack`, and each would do the wrong thing with a
second claimant: `derive-design-manifest` would put desktop and handheld screens in one `WS` batch
under one brief with one form factor, `derive-board-flows` would route one board through two
platforms, and `derive-pack-screens` would stop being able to say which screen *is* the entry. The
book is still cited: every component keeps the provenance it was generated with.

## What is copied, and what is not

Copied from the twin: `purpose`, `pattern` and its reason, `layout`, `states`, `gaps`,
`overlays`, `apis`, `apisNote`, `entryState` — everything `generate-screens-from-pack.py` builds
from the book. **Re-running this re-copies them**, so when the P08 screen is regenerated the P06
one follows rather than drifting.

Not copied: the id, the route, the density — a handheld is `comfortable` — and the navigation,
which is P06's own: a hub per board off `EMP-003 Home — on duty`, children to the hub and back.

**The offline state is `TODO`, on purpose.** P06 is offline-capable, so `check-screens` requires
one. The book does not say what a counter does when the connection drops, and no minute has
decided it; writing "keeps working" would be a promise with no operation behind it, which is the
exact failure `check-screens` exists to catch. `TODO` is reported as a warning, which is true.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations
import collections
import glob
import os
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACK = "Rental_Management.pdf"
BOARDS = ("6", "7", "8")
HOME = "EMP-003"
COPIED = ("purpose", "pattern", "patternReason", "layout", "states", "gaps", "overlays",
          "apis", "apisNote", "entryState")
OFFLINE = ("TODO — not decided. Rental Management does not say what a staff device does here "
           "without a connection, and no minute has decided it.")
PROVENANCE = "structural — Rental board {board} on the staff app, 11 September 2026"


def slug(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def pascal(text: str) -> str:
    return "".join(w.capitalize() for w in re.findall(r"[A-Za-z0-9]+", text))[:48] or "Screen"


def number(s: dict) -> tuple:
    return tuple(int(p) for p in str((s.get("source") or {}).get("number") or "999").split("."))


def link(a: dict, b: dict, board: str, back: bool) -> None:
    na, nb = a.setdefault("navigation", {}), b.setdefault("navigation", {})
    for seq, v in ((na.setdefault("exitTo", []), b["id"]), (nb.setdefault("entryFrom", []), a["id"])):
        if v not in seq:
            seq.append(v)
            seq.sort()
    tr = na.setdefault("transitions", [])
    if not any(str(t.get("to", "")).partition("#")[0] == b["id"] for t in tr):
        entry = {"to": b["id"], "trigger": f"Back to {b['name']}" if back else b["name"],
                 "provenance": PROVENANCE.format(board=board)}
        if back:
            entry["back"] = True
        tr.append(entry)


def main() -> int:
    apply = "--apply" in sys.argv
    files = {pathlib.Path(f).name: f for f in glob.glob(str(ROOT / "screens" / "P*.yaml"))}
    p08f = next(f for n, f in files.items() if n.startswith("P08-"))
    p06f = next(f for n, f in files.items() if n.startswith("P06-"))
    p08 = yaml.safe_load(open(p08f, encoding="utf-8"))
    p06 = yaml.safe_load(open(p06f, encoding="utf-8"))
    reg_path = ROOT / "screens" / "_id-register.yaml"
    register = yaml.safe_load(open(reg_path, encoding="utf-8"))
    app = p06["platform"]["app"]

    twins = [s for s in p08["screens"]
             if (s.get("source") or {}).get("pack") == PACK
             and str((s.get("source") or {}).get("board")) in BOARDS]
    by_twin = {(s.get("source") or {}).get("sameAs"): s for s in p06["screens"]
               if (s.get("source") or {}).get("sameAs")}
    p06_ids = {s["id"]: s for s in p06["screens"]}
    nxt = int(register["prefixes"]["EMP"]["nextFree"])
    nxt = max(nxt, max(int(i.split("-")[1]) for i in p06_ids) + 1)

    created, synced = [], 0
    for t in sorted(twins, key=lambda s: (int(s["source"]["board"]), number(s))):
        mine = by_twin.get(t["id"])
        if mine is None:
            sid = "EMP-%03d" % nxt
            nxt += 1
            mine = {
                "id": sid, "name": t["name"], "module": "Rentals",
                "requiresModule": t.get("requiresModule", "resources"), "wave": t.get("wave"),
                "source": {"sameAs": t["id"], "book": PACK, "board": t["source"]["board"],
                           "number": t["source"]["number"], "page": t["source"]["page"]},
                "implementation": {
                    "app": app,
                    "route": f"/rentals/{slug(t['name'])[:56]}-{sid.lower()}",
                    "component": f"apps/{app}/src/routes/rentals/{pascal(t['name'])}.tsx",
                    "status": "notStarted"},
                "density": "comfortable",
                "notes": (f"The staff-app form of `{t['id']}`, for the attendant at the rental "
                          "counter. Decided 11 September 2026 that Rental boards 6–8 live on both "
                          "platforms; `tools/applied/apply-rental-staff-app.py` keeps the two in step."),
            }
            p06["screens"].append(mine)
            p06_ids[sid] = mine
            by_twin[t["id"]] = mine
            created.append(sid)
        before = yaml.safe_dump({k: mine.get(k) for k in COPIED}, sort_keys=True)
        for k in COPIED:
            if k in t:
                mine[k] = yaml.safe_load(yaml.safe_dump(t[k], allow_unicode=True))
            else:
                mine.pop(k, None)
        mine.setdefault("states", {})["offline"] = mine["states"].get("offline") or OFFLINE
        if "offline" not in (t.get("states") or {}):
            mine["states"]["offline"] = OFFLINE
        synced += before != yaml.safe_dump({k: mine.get(k) for k in COPIED}, sort_keys=True)

    groups = collections.defaultdict(list)
    for t in twins:
        groups[t["source"]["board"]].append(by_twin[t["id"]])
    for board, rows in sorted(groups.items()):
        rows.sort(key=number)
        hub = rows[0]
        link(p06_ids[HOME], hub, board, back=False)
        link(hub, p06_ids[HOME], board, back=True)
        for child in rows[1:]:
            link(hub, child, board, back=False)
            link(child, hub, board, back=True)

    print(f"{len(twins)} Rental screen(s) on boards {', '.join(BOARDS)} of P08")
    print(f"  {len(created)} created on P06{': ' + created[0] + '…' + created[-1] if created else ''}")
    print(f"  {synced} re-synced from their P08 twin")
    for board, rows in sorted(groups.items()):
        print(f"  board {board}: {HOME} → {rows[0]['id']} {rows[0]['name']} ({len(rows)} screens)")
    if not apply:
        print("\npreview only — run with --apply")
        return 0

    p06["platform"]["screenCount"] = len(p06["screens"])
    path = pathlib.Path(p06f)
    if yaml.safe_load(path.read_text(encoding="utf-8")) == p06:
        print(f"unchanged: {path.name} — {len(p06['screens'])} screens")
        return 0
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(yaml.safe_dump(p06, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    os.replace(tmp, path)
    print(f"written: {path.name} — {len(p06['screens'])} screens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
