#!/usr/bin/env python3
"""Section homes link to the Block A screens they lead to (lever A, CHG-RONEP-007, 3 October 2026). A one-off.

Chinmay, 3 October ("Block A size and embeddings"; docs/active/decisions/answers-3-october-r1-plan.md): pull in app
homes only, not the 42 command centres; the section homes link to their setup screens. The plan's navigation closure
(tools/build-service-docs.py nav_hubs) now pulls into Block A only an app's entry and the homes block-a-extra-tasks.json
names (`navHomes`: BO-101 to BO-108, EMP-003). A Block A screen whose only way in passed a command centre (BO-010
through ADM-138, ADM-037 through ADM-519 ...) gets a link from its section home -- the Venue Management section of its
module, else its app's entry or home -- written as tools/check-navigation.py expects: the home's `navigation.exitTo`
and a `transitions` entry, and the screen's `entryFrom` where it keeps one (N-ENTRY-MIRROR).

Reads Block A (A1 and A2) from handoff/service-docs/plan-tasks.csv: run tools/build-service-docs.py first. Only the
screens it links change, spliced back at their file's dump width (tools/applied/spec-screen-patterns-3-october.py
ScreenFiles). A second run says there is nothing to link. tools/check-plan-closure.py (C-REACH) keeps it so.

    python3 tools/applied/nav-homes-r1-plan-3-october.py [--dry-run]
"""
import csv
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import sprint_plan as sp  # noqa: E402
import ticket_done as td  # noqa: E402

PROV = ("CHG-RONEP-007: the section home links to the Block A screen it leads to (lever A, Chinmay, 3 October 2026); "
        "its command centre is not in Block A")
# Venue Management sections by screen module; a module with no section of its own opens from Venue Home (BO-100)
SECTION = {"Orders & Money": "BO-101", "Sell": "BO-102", "Commercial": "BO-102", "Access & Venue": "BO-103",
           "Food & Beverage": "BO-104", "Stock & Supply": "BO-105", "People & Access Rights": "BO-106",
           "Access & Identity": "BO-106", "Guests & Marketing": "BO-107", "Engagement & Support": "BO-107",
           "Venue Operations": "BO-108", "Rentals": "BO-108", "Transport": "BO-108", "Games & Rides": "BO-108"}


def main() -> int:
    spec = importlib.util.spec_from_file_location("ssp", ROOT / "tools" / "applied" / "spec-screen-patterns-3-october.py")
    ssp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ssp)
    sf = ssp.ScreenFiles()
    scr = sf.screens
    extra = json.loads((ROOT / "docs" / "active" / "block-a-extra-tasks.json").read_text(encoding="utf-8"))
    homes = set(extra.get("navHomes") or {})
    blk = {}
    for r in csv.DictReader((ROOT / "handoff" / "service-docs" / "plan-tasks.csv").open(encoding="utf-8")):
        if r["type"] == "Task" and r.get("track") != "Test":
            for b in td.builds_of(r, "", {}):
                if b.startswith("screen "):
                    sid = b.split(" ", 1)[1]
                    if sid not in blk or sp.BLOCKS.index(r["block"]) < sp.BLOCKS.index(blk[sid]):
                        blk[sid] = r["block"]
    fam = {sid for sid, b in blk.items() if b in sp.BLOCK_A_FAMILY}
    plat = {sid: s["_plat"] for sid, s in scr.items()}
    links = []
    for pf in sorted({plat[s] for s in fam if s in scr}):
        app = {sid: s for sid, s in scr.items() if plat[sid] == pf}
        entries = sorted(sid for sid, s in app.items() if sp.is_entry(s))
        ok = fam | homes | set(entries)
        for t, path in sorted(sp.nav_paths(app, ok, {s for s in fam if plat.get(s) == pf}).items()):
            if all(x in ok for x in path):
                continue
            home = SECTION.get(scr[t].get("module")) if pf == "P08" else None
            if not home or home not in app:
                home = next((x for x in reversed(path) if x in homes or x in entries), entries[0] if entries else None)
            if not home or home == t:
                continue
            links.append((home, t))
    for home, t in links:
        nav = scr[home].setdefault("navigation", {})
        ex = nav.setdefault("exitTo", [])
        if t not in ex:
            ex.append(t)
        tr = nav.setdefault("transitions", [])
        if not any(isinstance(x, dict) and x.get("to") == t for x in tr):
            tr.append({"to": t, "trigger": f"Opens {scr[t].get('name')}", "provenance": PROV})
        sf.dirty.add(home)
        tnav = scr[t].get("navigation") or {}
        if isinstance(tnav.get("entryFrom"), list) and home not in tnav["entryFrom"]:
            tnav["entryFrom"].append(home)
            sf.dirty.add(t)
    for home, t in links:
        print(f"{home} -> {t} ({scr[t].get('name')})")
    if not links:
        print("nothing to link: every Block A screen is reached through Block A screens and app homes")
        return 0
    if "--dry-run" not in sys.argv:
        print("written:", ", ".join(sf.write()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
