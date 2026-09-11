#!/usr/bin/env python3
"""Turn the workshop pack into screen definitions, and register what they still need.

**770 screens across 77 boards**, from `sources/workshop/pack.json`. Adds the ones no screen
claims to the existing `screens/P*.yaml` files and prints the contract gap.

## It adds; it does not rebuild

The first version dropped every screen carrying `source.pack` and wrote it again, and that was
idempotent for exactly as long as this tool was the only thing that had ever touched those screens.
`generate-screens-from-pack.py` and `generate-screens-from-contracts.py` have since rebuilt all
1,091 with their components, provenance, patterns, overlays and gaps. **Re-running the old version
today would have replaced 590 of them with `searchField` / `dataTable` / `detailPanel` — the exact
regression the September rebuild was undoing** — and its docstring would have said it was safe.

So a pack entry a screen already claims is skipped, and ids for new ones come from
`screens/_id-register.yaml`, not from the highest id present in the file.

## What this does not do

**It does not invent operations.** A generated screen declares `apis: []`.

The 500 screens already in the package carry 2,569 operation references at about five apiece, so
these 590 imply roughly three thousand more — against 1,032 operations that exist. **Authoring
three thousand endpoints from a PDF is not derivation, it is fabricating an API surface**, and
every downstream artefact in this package — the lineage, the DDL, the sizing, the burst scope —
would then rest on it while reading as though the contracts had said so.

So the screens land with what the documents actually specify: a name, a purpose, the fields and
KPIs each one names, its board and its page in the source. What each screen needs from the
contracts is written to `docs/active/workshop-contract-gap.md` as a register, per board, for a
person to work through. **A gap somebody can see is worth more than a number that looks complete.**

## Placement

The user's decision was to split by owning platform rather than invent a configuration platform.
`P08` takes venue-operated configuration and `P09` platform-level commercial configuration, which
is the ownership line the two consoles already draw — otherwise P08 alone would go from 143 screens
to 563 and stop being one team's file.

Run: `python3 tools/derive-pack-screens.py [--apply]`
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "sources" / "workshop" / "pack.json"
SCREENS = ROOT / "screens"
GAP = ROOT / "docs" / "active" / "workshop-contract-gap.md"

# module -> (platform code, licensed module, navigation section)
PLACEMENT = {
    "Access Control Module": ("P08", "access", "Access & Venue"),
    "Order   Reservation Management": ("P08", "ticketing", "Orders & Money"),
    "Ticket Media   Credential Management": ("P08", "access", "Access & Venue"),
    "Group Sales   Corporate Booking Management": ("P08", "ticketing", "Sell"),
    "Membership   Annual Pass Management": ("P08", "membership", "Sell"),

    "Pricing   Revenue Management": ("P09", "ticketing", "Commercial"),
    "Promotions   Bundles Management": ("P09", "marketing", "Commercial"),
    "Product Lifecycle   Catalogue Governance": ("P09", "ticketing", "Catalogue"),
    "Sales Channel Management": ("P09", "ticketing", "Commercial"),
    "Rules  Workflow  Approval   Automation Engine": ("P09", "core", "Platform"),
    "Communication & Notification Platform Services": ("P09", "marketing", "Platform"),
    "Ticket Upgrade, Exchange & Conversion": ("P09", "ticketing", "Commercial"),
    "Ticket Resale Marketplace": ("P09", "ticketing", "Commercial"),

    # The 9 September books. Both are placed by board rather than whole — see `BOARD_PLACEMENT`.
    "Approval Workflows and Governance": ("P09", "core", "Platform"),
    "Unified BI Reporting and AI Analytics Platform": ("P16", "analytics", "Analytics"),

    "B2B, Reseller & OTA Partner Management": ("P10", "partner", "Partners"),
    "Customer Service": ("P12", "marketing", "Support"),
    "Privacy  Consent   Preference Management": ("P13", "core", "Policy"),
    "Waiver, Consent & Digital Form Management": ("P13", "core", "Policy"),

    # **The 11 September books, placed where the package already puts their domain.** None of
    # this is new vocabulary: every licensed module is in `LicencePosition.licensedModules`.
    #   DAM — `CMS-010 Media Library` is on P13, and `assets.yaml` serves every guest surface, so
    #   a tenant without a media library is not a tenant: `core`.
    #   Game & Ride — reader and RFID configuration already live on P08 (`BO-180`, `BO-199`).
    #   Rental — venue-operated, and `resources.yaml` is exactly this entity: "a specific object
    #   checked out to a named guest and returned". Boards 6–8 are also on P06, decided 11
    #   September; those copies carry `source.sameAs`, not `source.pack`, so this entry stays the
    #   one claimant — see `applied/apply-rental-staff-app.py`.
    #   Subscription — `subscription.yaml` runs on the control plane and names P09 as its only
    #   consumer, beside `ADM-008` and `ADM-011`. **Placed by who works each screen, 11 September**:
    #   boards 7, 8 and screen 6.10 are the new customer's own admin and are P08's (`BOARD_PLACEMENT`,
    #   `SCREEN_PLACEMENT`); boards 2, 4 and 5 stay here for the operator-led sale and are copied to
    #   P17 Sign-up for the prospect by `applied/apply-subscription-placement.py`.
    "Digital Asset Management DAM": ("P13", "core", "Media Library"),
    "Game and Ride Module": ("P08", "games", "Games & Rides"),
    "Rental Management": ("P08", "resources", "Rentals"),
    "Subscription Licensing AI Self Service": ("P09", "core", "Tenants & Licensing"),
}

# (module, board) -> placement, or None for a board that is not drawn as screens of its own.
# **Two of the 9 September books do not belong to one platform each**, and placing them by module
# would have put a venue approver's inbox in the platform console and reversed a decision P16 had
# already recorded.
#
#   **Approval Workflows & Governance splits on the line P08 and P09 already draw.** Boards 2, 3,
#   6, 7 and 8 configure and measure the approval engine centrally; boards 1, 4 and 5 are worked
#   by whoever approves — an inbox, a decision workspace, an escalation desk — and those are
#   venue-operated.
#
#   **Unified BI's boards 5 to 8 are the same four screens under four domain names.** Sales,
#   Finance, Operations and Customer each get a command centre, an analytics set and an AI
#   screen. P16's platform note already settled this shape once: *"a domain is a filter on an
#   analytics screen, not a copy of it"*, when 26 board screens became nine. Drawing all forty
#   would build the duplication that note describes removing, so they stay in `pack.json` and are
#   listed in `docs/active/bi-domain-boards-9-september.md` against the domain filter that covers
#   them. **Recorded, not dropped** — a screen nobody can find again has been lost, whatever the
#   commit message says.
BOARD_PLACEMENT: dict[tuple[str, str], tuple[str, str, str] | None] = {
    **{("Approval Workflows and Governance", b): ("P08", "core", "Venue Operations")
       for b in ("1", "4", "5")},
    **{("Unified BI Reporting and AI Analytics Platform", b): None
       for b in ("5", "6", "7", "8")},
    **{("Subscription Licensing AI Self Service", b): ("P08", "core", "Setup & Go-Live")
       for b in ("7", "8")},
}

# (module, board, number) -> placement, for the one screen a board does not share. Subscription 6.10
# *Your TICVAI Environment Is Ready* speaks to the customer and "hands the customer directly to
# Board 7"; the rest of board 6 is TICVAI watching provisioning. Decided 11 September.
SCREEN_PLACEMENT: dict[tuple[str, str, str], tuple[str, str, str]] = {
    ("Subscription Licensing AI Self Service", "6", "10"): ("P08", "core", "Setup & Go-Live"),
}

# (pack, number, page) -> the screen it was collapsed into. **A deletion this tool cannot see is a
# screen it will add back.** Both are recorded where they were decided:
#   `ADM-321` into `ADM-241` -- tools/applied/README.md, `apply-naming-and-navsets.py`, 9 September.
#   `ANL-011` into `ANL-001` -- docs/active/pack-board-wiring-9-september.md, "removed, not wired".
COLLAPSED: dict[tuple[str, str, str], str] = {
    ("Approval_Workflows_and_Governance_Reference.pdf", "3", "13"): "ADM-241",
    ("Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf", "1", "3"): "ANL-001",
}


# **A word in a title that says what the screen is.** Used only to choose components, so a
# command centre gets tiles and a directory gets a table — not to decide what a screen means.
ARCHETYPE = [
    ("command center", "dashboard"), ("dashboard", "dashboard"), ("analytic", "dashboard"),
    ("intelligence", "dashboard"), ("monitor", "dashboard"), ("forecast", "dashboard"),
    ("builder", "editor"), ("designer", "editor"), ("workspace", "editor"),
    ("studio", "editor"), ("configuration", "editor"), ("setup", "editor"),
    ("directory", "list"), ("register", "list"), ("registry", "list"),
    ("explorer", "list"), ("library", "list"), ("inbox", "list"),
    ("audit", "history"), ("history", "history"), ("log", "history"),
    ("simulation", "editor"), ("approval", "list"), ("publication", "editor"),
]


def slug(text: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def archetype(title: str) -> str:
    low = title.lower()
    for word, kind in ARCHETYPE:
        if word in low:
            return kind
    return "list"


def pascal(text: str) -> str:
    return "".join(w.capitalize() for w in re.findall(r"[A-Za-z0-9]+", text))[:48] or "Screen"


def impl(app: str, section: str, title: str, sid: str) -> dict:
    """The implementation block, to the convention `check-frontend` enforces.

    `component` must sit under `apps/<app>/src/routes/` and end `.tsx`, and a route must be
    absolute and unique within its app — **the screen id goes in the route** because two modules
    can name a screen the same thing and a silent collision would put two screens on one URL.
    """
    folder = slug(section)
    return {
        "app": app,
        "route": f"/{folder}/{slug(title)[:56]}-{sid.lower()}",
        "component": f"apps/{app}/src/routes/{folder}/{pascal(title)}.tsx",
        "status": "notStarted",
    }


def layout_for(kind: str, rec: dict) -> dict:
    """Regions and components, from what the document says is on the screen.

    Only the component vocabulary in `screens/_components.yaml` is used — an unknown `kind` is an
    error in `check-screens`, and inventing one to fit a PDF heading would trade a real check for
    a tidier-looking file.
    """
    kpis = [t for t in rec.get("sections", {}).get("Display", [])][:6]
    comps: list = []
    if kind == "dashboard":
        comps += [{"kind": "metricTile", "notes": k} for k in (kpis or ["Headline figure"])[:6]]
        comps.append({"kind": "dataTable", "notes": "The records behind the figures"})
    elif kind == "editor":
        comps += [{"kind": "detailPanel", "notes": "The configuration being edited"},
                  {"kind": "selectField", "notes": "Scope this applies at"},
                  {"kind": "toggle", "notes": "Active"}]
    elif kind == "history":
        comps += [{"kind": "timeline", "notes": "What changed, when, and by whom"},
                  {"kind": "searchField", "notes": "Find a change"}]
    else:
        comps += [{"kind": "searchField", "notes": "Find a record"},
                  {"kind": "dataTable", "notes": "Every record with its status"},
                  {"kind": "detailPanel", "notes": "The selected record"}]
    return {"template": "split" if kind in ("editor", "list") else "dashboard",
            "regions": [{"name": "contentBody", "components": comps}]}


def states_for(rec: dict, kind: str) -> dict:
    what = rec["title"]
    return {
        "loading": "Skeleton while the configuration loads",
        "emptyFirstRun": f"**Nothing configured yet.** The action is to create the first "
                         f"{what.split()[0].lower()} entry, and this state carries it",
        "emptyNoResults": "**Nothing matched.** The filter or the scope narrowed it — naming "
                          "which is what stops somebody concluding the record does not exist",
        "emptyNoAccess": "**Says which permission is missing, and never renders as an empty "
                         "list.** An empty table reads as *there is no data* and sends somebody "
                         "to support with the wrong question",
        "error": "Configuration service unavailable. Says what is unaffected",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the screen files")
    a = ap.parse_args()

    if not PACK.exists():
        print("no sources/workshop/pack.json — run tools/parse-workshop-pack.py --apply")
        return 1
    pack = json.loads(PACK.read_text(encoding="utf-8"))

    unplaced = sorted({r["module"] for r in pack} - set(PLACEMENT))
    if unplaced:
        print("  no placement for: " + ", ".join(unplaced))
        return 1

    # **Ids come from `screens/_id-register.yaml`, not from the highest id in the file.** The
    # register is the high-water mark including retired numbers, and taking max+1 of what is
    # present is how ADM-038 was issued twice on 4 September.
    register = yaml.safe_load((SCREENS / "_id-register.yaml").read_text(encoding="utf-8"))
    docs, prefix, nextnum, held = {}, {}, {}, {}
    by_id: dict = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = d["platform"]["code"]
        docs[code] = (f, d)
        # **Incremental, not rebuilt.** This used to drop every screen carrying `source.pack` and
        # write it again, which was idempotent while this tool was the only thing that had ever
        # touched them. It is not any more: `generate-screens-from-pack.py` and
        # `generate-screens-from-contracts.py` have since rebuilt all 1,091 with their components,
        # provenance, patterns, overlays and gaps, and the rebuild here would have replaced 590 of
        # those with `searchField` / `dataTable` / `detailPanel` again — **the exact regression the
        # September rebuild was undoing**, applied by a tool whose docstring calls it safe.
        #
        # So a pack screen is now left alone, and only a pack entry no screen claims is added.
        prefix[code] = d["screens"][0]["id"].split("-")[0]
        for s in d["screens"]:
            src = s.get("source") or {}
            if src.get("pack"):
                held[(src["pack"], str(src.get("number")), str(src.get("page")))] = (code, s)
        by_id.update({s["id"]: (code, s) for s in d["screens"]})

    # **A collapsed screen is claimed by the one it was collapsed into.** Found on 11 September:
    # adding four books re-ran this over all 1,110 entries, and it would have brought back both
    # screens deleted on 9 September, because nothing but prose remembered they had gone.
    for key, survivor in COLLAPSED.items():
        if key not in held and survivor in by_id:
            held[key] = by_id[survivor]

    for code, pre in prefix.items():
        nextnum[code] = int((register["prefixes"].get(pre) or {}).get("nextFree") or 1)

    added = defaultdict(list)
    gap = defaultdict(list)
    not_drawn: list[dict] = []
    claimed = 0
    for rec in pack:
        if (existing := held.get((rec["source"], str(rec["number"]), str(rec["page"])))):
            claimed += 1
            # **The register is every pack screen still waiting on an operation, not only the
            # ones added today.** Rebuilding it from the newly added screens alone would have
            # shrunk it from 590 rows to 140 and read as though 450 questions had been answered.
            if not (existing[1].get("apis") or []):
                gap[(rec["module"], rec["board"])].append(
                    (existing[1]["id"], rec["title"], rec.get("terms") or []))
            continue
        place = SCREEN_PLACEMENT.get(
            (rec["module"], str(rec["board"]), str(rec["number"])),
            BOARD_PLACEMENT.get((rec["module"], rec["board"]), PLACEMENT[rec["module"]]))
        if place is None:
            not_drawn.append(rec)
            continue
        code, licensed, section = place
        kind = archetype(rec["title"])
        sid = f"{prefix[code]}-{nextnum[code]:03d}"
        nextnum[code] += 1
        screen = {
            "id": sid,
            "name": rec["title"],
            "module": section,
            "requiresModule": licensed,
            "purpose": (rec.get("purpose") or rec["title"])[:240],
            "wave": 3,
            "density": "compact",
            "layout": layout_for(kind, rec),
            "states": states_for(rec, kind),
            "apis": [],
            "implementation": impl(docs[code][1]["platform"]["app"], section, rec["title"], sid),
            # The board is generated by `derive-wireframes.py` from these very screens, so the
            # anchor is predictable — and a screen that does not name one is reported by
            # `check-wireframes` as having no board at all.
            "wireframe": {"status": "notStarted",
                          "board": f"{docs[code][1]['platform']['wireframeBoard']}#{sid.lower()}"},
            "source": {"pack": rec["source"], "board": rec["board"],
                       "number": rec["number"], "page": rec["page"]},
        }
        added[code].append(screen)
        gap[(rec["module"], rec["board"])].append((sid, rec["title"], rec.get("terms") or []))

    print(f"{len(pack)} pack entries: {claimed} already have a screen, "
          f"{sum(len(v) for v in added.values())} would be added, "
          f"{len(not_drawn)} covered by a filter on another screen\n")
    print(f"  {'platform':6} {'was':>5} {'added':>7} {'now':>6}")
    for code in sorted(added):
        f, d = docs[code]
        print(f"  {code:6} {len(d['screens']):>5} {len(added[code]):>7} "
              f"{len(d['screens']) + len(added[code]):>6}")

    still_open = sum(len(v) for v in gap.values())
    print(f"  {still_open} pack screens carry no operation yet")

    if not added:
        print("\n  every pack entry already has a screen — nothing to add")
        return 0

    if not a.apply:
        print("\n  nothing written — pass --apply")
        return 0

    for code, screens in added.items():
        f, d = docs[code]
        d["screens"].extend(screens)
        d["platform"]["screenCount"] = len(d["screens"])
        f.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100),
                     encoding="utf-8")
        print(f"  -> {f.relative_to(ROOT)}")
    print("  ids issued — run `tools/derive-id-register.py --apply` and commit it in this change")

    # ---- the register ----------------------------------------------------------------------
    lines = [
        "# Workshop pack — what the new screens need from the contracts",
        "",
        f"**{still_open} of the {len(pack)} pack screens still carry `apis: []`.** Generated by "
        "`tools/derive-pack-screens.py`; regenerate rather than editing.",
        "",
        "The 500 screens already in the package carry 2,569 operation references, about five "
        "apiece. These imply roughly three thousand more against the 1,032 that exist. "
        "**Authoring those from a PDF would be fabricating an API surface**, and the lineage, the "
        "DDL, the sizing and the burst scope would all then rest on it while reading as though the "
        "contracts had said so.",
        "",
        "So each board is listed with the vocabulary its screens actually name. That is the input "
        "to writing operations — not a substitute for it.",
        "",
        "## Why this is not automated",
        "",
        "Matching each screen's vocabulary against all 1,032 existing operations — their ids, "
        "summaries, paths and the tables they touch — was tried and it does not work. **Eight "
        "unrelated screens all matched `listScans` at 0.75**, among them *Group & B2B Admission "
        "Profile Builder* and *Policy Approval, Audit, Analytics & AI Optimization*. An operation "
        "with a small vocabulary wins on any containment measure, and 260 of the 590 screens got "
        "no candidate at all.",
        "",
        "**The documents say what a screen shows, not what serves it.** A field list is not an "
        "endpoint, and nothing in these PDFs names one. Wiring them by similarity would pass "
        "`check-screens` — it only tests that an `operationId` exists, never that it is the right "
        "one — and produce a package that looks finished and is wrong in three thousand places.",
        "",
    ]
    for (module, board), rows in sorted(gap.items()):
        terms = sorted({t for _, _, ts in rows for t in ts})
        lines += [f"## {module} — board {board}", "",
                  f"{len(rows)} screens · {len(terms)} distinct terms", "",
                  "| Screen | Name |", "|---|---|"]
        lines += [f"| `{sid}` | {name} |" for sid, name, _ in rows]
        lines += ["", "**Vocabulary** — " + ", ".join(terms[:60])
                  + (" …" if len(terms) > 60 else ""), ""]
    GAP.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> {GAP.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
