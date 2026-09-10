#!/usr/bin/env python3
"""Put the 3 August UI/UX workshop's decisions into the screens, where they were never recorded.

**The minute was mined for decisions and its interaction design was not.** `sources/mom` has been
read for what was agreed about entities, pricing and infrastructure; the session on 3 August was
about how the point of sale behaves, and five of the things confirmed that day reached nothing in
the package. Four of them are visible as component kinds nobody uses:

| Confirmed 3 August | State before this ran |
|---|---|
| A slide-in drawer for ticket detail, date/time and seat selection, **in place of full-page navigation** | `drawer` on 1 screen of 1,231, and not on the POS |
| An embedded AI assistant the cashier can query directly | no component kind existed for it at all |
| Always-visible "hot function" buttons beside the search-driven magic banner | nothing |
| A payment flow the cashier can inquire into | `paymentTerminal` on 0 screens, on a platform with a POS |
| Four ticket flows — admission, dated, timed, seated | `seatMap` on 1 screen, and not on either seat-selection screen |

## Why a tool and not an edit

Everything here cites the minute, so **the generators carry it** — both refuse to overwrite a
component whose `provenance` is not their own. That was already true of components and was *not*
true of overlays, which both generators rebuilt from scratch from the destructive actions they
found; the drawer added by hand would have survived until the next rebuild and then vanished. Both
now carry, and this file is the thing that would have caught it: run it twice and the second run
reports nothing to do.

## What it does not do

**It does not resolve what the drawer replaces.** `POS-003 Sell — Timed Entry` and `POS-004 Sell —
Seat Map` are separate screens reached by leaving the catalogue, which is the full-page navigation
the workshop replaced. Deleting them is not this tool's decision — a seat map may still be wanted
full-screen on a tablet, and a screen id is never reissued. Each gets a gap saying what it now
overlaps and who has to decide.

Run: python tools/apply-uiux-workshop-decisions.py [--apply]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[2]
SCREENS = ROOT / "screens"

# **The citation, and it is the whole warrant for every field below.** `provenance` already admits
# a minute; nothing had used it. The section names are the digest's own headings, so a reader can
# find the paragraph rather than take this file's word for what was said.
WALKTHROUGH = "minute 2026-08-03 §Point-of-Sale (Cashier) UI Walkthrough"
APPROACH = "minute 2026-08-03 §UX Design Approach Discussion"
VARIANTS = "minute 2026-08-03 §Ticket Flow Variations by Product Type"

# ---- 1. the drawer ------------------------------------------------------------------------------
# **Three steps, one drawer, and the order is the minute's.** "Selecting a ticket opens a drawer
# showing inclusions and rules/restrictions, followed by date/time selection and, where relevant,
# seat selection." Each step is its own overlay because each renders as its own frame, and a
# reviewer judging this flow needs to see the catalogue behind all three — that the cashier never
# left it is the entire decision.
DRAWERS = [
    {"id": "drawerTicketDetail", "component": "drawer", "trigger": "Select a ticket",
     "bindsTo": "Product",
     "body": "**What this ticket includes and what it does not.** Inclusions, and the rules and "
             "restrictions that apply — the things a cashier is asked at the counter and "
             "currently has to know. The catalogue stays behind it: nothing is lost by closing "
             "this, because nothing has been added to the cart yet.",
     "provenance": WALKTHROUGH},
    {"id": "drawerDateAndSession", "component": "drawer", "trigger": "Continue from ticket detail",
     "bindsTo": "Availability",
     "body": "**Date, then session, for the flows that need them.** An admission ticket skips "
             "this and goes to quantity; a dated ticket asks the date; a timed ticket asks the "
             "date and then the time. Which of the three is not a property of this drawer — it "
             "is the product type, and the drawer shows the steps that type requires.",
     "provenance": VARIANTS},
    {"id": "drawerSeatSelection", "component": "drawer", "trigger": "Continue from date and session",
     "bindsTo": "SeatAvailability",
     "body": "**Seats, for a seated product only.** Carries the seating rules the venue "
             "configured — a group whose seats must stay together cannot be split here, and the "
             "map says so at the point of selection rather than at payment.",
     "provenance": VARIANTS},
]

# ---- 2, 3. the assistant and the hot functions ---------------------------------------------------
ASSISTANT = {
    "kind": "assistantPanel", "label": "Ask about this sale",
    "notes": "**The cashier asks in their own words and stays on the screen.** The minute's own "
             "examples are finding today's promo code, processing a refund and switching to the "
             "night theme — one of those is a question, one is an action needing a permission and "
             "a confirmation, and one is a preference. The panel answers all three; it performs "
             "none of them differently from the button that already does.",
    "provenance": WALKTHROUGH,
}

# **Beside the search, not instead of it.** Allam proposed the hybrid and asked Softlabs for the
# recommendation on the balance; Qossai agreed a combination might be ideal. So the three named
# high-frequency actions are here and the search stays — what is *not* settled is how many, and
# that is recorded as a gap rather than guessed at.
HOT_FUNCTIONS = [
    {"kind": "secondaryButton", "label": "Refund", "provenance": APPROACH},
    {"kind": "secondaryButton", "label": "Check transaction", "provenance": APPROACH},
    {"kind": "secondaryButton", "label": "Print last receipt", "provenance": APPROACH},
]

# ---- 4. the payment terminal ---------------------------------------------------------------------
# **Not authored — the contract and the component library already agree.** `POS-005` declares
# `inquirePaymentStatus`, and `paymentTerminal`'s own note says the `unknown` state is why that
# operation exists: "a terminal that charged a card and never returned a response is the normal
# failure, not the exotic one — the screen must offer inquiry, not a retry that double-charges."
# The screen had the operation and no component that could reach it.
TERMINAL = {
    "kind": "paymentTerminal", "label": "Card payment",
    "operation": "createPayment",
    "notes": "**`unknown` is the state this screen exists to handle.** Where the terminal charged "
             "the card and returned nothing, the cashier inquires with `inquirePaymentStatus` — "
             "the screen must not offer a retry, which double-charges a guest standing at the "
             "counter.",
    # **The library is named first because `contract ` is a reserved prefix.** The contracts
    # generator treats any provenance beginning `contract ` as its own and rewrites over it, so
    # the first version of this line — which opened with the endpoint — was deleted on the next
    # rebuild of P04. A citation is not free text: the leading token decides who owns the field.
    "provenance": "component library _components.yaml paymentTerminal · the screen's own "
                  "inquirePaymentStatus, from contract payments",
}

# ---- 5. the seat map -----------------------------------------------------------------------------
SEATMAP = {
    "kind": "seatMap", "label": "Choose seats",
    "notes": "**A seat selection screen with no seat map.** `noGeometry` is the state that "
             "matters: a map imported from a manifest alone can be sold from a list and not "
             "rendered, and the screen has to say which it is rather than showing an empty "
             "frame.",
    "provenance": VARIANTS,
}

PLAN: dict[str, dict] = {
    "POS-002": {"overlays": DRAWERS,
                "components": [("contextPanel", "assistant", [ASSISTANT]),
                               ("actionBar", "hotFunctions", HOT_FUNCTIONS)],
                "gap": {"why": "**How many hot functions, and which, is not settled.** Allam "
                               "proposed the hybrid on 3 August and asked Softlabs for the "
                               "recommendation on the balance between always-visible buttons and "
                               "the search-driven magic banner; Qossai agreed a combination might "
                               "be ideal and deferred. The three here are the three the minute "
                               "names — they are not a recommendation.",
                        "source": APPROACH}},
    "POS-005": {"components": [("contentBody", "payment", [TERMINAL])]},
    "POS-004": {"gap": {"why": "**This screen is the full-page navigation the 3 August workshop "
                               "replaced.** Seat selection is now step three of the drawer on "
                               "`POS-002`, which is where the cashier stays. Whether this "
                               "survives as a screen of its own is a decision nobody has made: a "
                               "seat map may still be wanted full-screen on a tablet, and a "
                               "screen id is never reissued, so it is recorded rather than "
                               "deleted.",
                        "source": WALKTHROUGH}},
    "POS-003": {"gap": {"why": "**This screen is the full-page navigation the 3 August workshop "
                               "replaced.** Date and session selection is now step two of the "
                               "drawer on `POS-002`. Same decision as `POS-004`, same reason for "
                               "recording it rather than acting on it.",
                        "source": WALKTHROUGH}},
    "WEB-007": {"components": [("contentBody", "selection", [SEATMAP])]},
    "GST-049": {"components": [("contentBody", "selection", [SEATMAP])]},
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the screen files")
    a = ap.parse_args()

    changed: dict[str, list[str]] = {}
    files: dict[Path, dict] = {}
    seen = set()

    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        touched = False
        for s in doc["screens"]:
            plan = PLAN.get(s["id"])
            if not plan:
                continue
            seen.add(s["id"])
            notes: list[str] = []

            have = {o.get("id") for o in (s.get("overlays") or [])}
            for ov in plan.get("overlays") or []:
                if ov["id"] in have:
                    continue
                s.setdefault("overlays", []).append(dict(ov))
                notes.append(f"overlay {ov['id']}")

            regions = (s.setdefault("layout", {}).setdefault("regions", []))
            for region, slot, comps in plan.get("components") or []:
                # **Matched on the label, not the kind.** A screen may legitimately carry two
                # buttons; it may not carry `Refund` twice, and re-running this must not add one.
                present = {str(c.get("label")) for r in regions for c in r.get("components") or []}
                add = [dict(c) for c in comps if str(c.get("label")) not in present]
                if not add:
                    continue
                target = next((r for r in regions
                               if r.get("name") == region and r.get("slot") == slot), None)
                if target is None:
                    target = {"name": region, "slot": slot, "components": []}
                    regions.append(target)
                target.setdefault("components", []).extend(add)
                notes.append(f"{len(add)} × {region}/{slot}")

            if (g := plan.get("gap")):
                if not any(str(x.get("source")) == g["source"] for x in (s.get("gaps") or [])):
                    s.setdefault("gaps", []).append(dict(g))
                    notes.append("gap")

            if notes:
                changed[s["id"]] = notes
                touched = True
        if touched:
            files[f] = doc

    for sid in sorted(set(PLAN) - seen):
        print(f"  {sid} is in the plan and not in the package — nothing applied")

    if not changed:
        print("nothing to do — every decision is already recorded")
        return 0

    for sid in sorted(changed):
        print(f"  {sid:8} {', '.join(changed[sid])}")

    if not a.apply:
        print("\n  nothing written — pass --apply")
        return 0

    for f, doc in files.items():
        f.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                     encoding="utf-8")
        print(f"  -> {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
