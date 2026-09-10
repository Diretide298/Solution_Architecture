#!/usr/bin/env python3
"""Label P04's transitions from the POS board delivered 9 September 2026.

**Phase 1 of the navigable-board rebuild, and it is a test rather than a migration.**

The question was whether `navigation.transitions[]` can hold what a working prototype does. The
only way to find out is to encode one platform by hand against a prototype that exists, before the
vocabulary is applied to 1,231 screens. That prototype is `TICVAI POS Terminal (1) 1.html`; this is
P04 encoded against it, in the vocabulary settled in `docs/active/interactive-wireframes-plan.md`
§2.1.

## The rule this script follows

**Nothing is labelled that cannot be cited.** Every transition below carries a `provenance` naming
the board handler and its line in the decoded template, or the flow and step it comes from. A
transition the board does not demonstrate is **left as a bare string** rather than given a plausible
trigger, because a guessed guard is worse than an absent one — it reads as a decision.

That is also the measurement. After this runs, `audit-transitions.py` counts how much of P04's
graph the board actually proves, and the remainder is the honest size of the authoring job on every
other platform.

## What it does not do

**It does not touch `exitTo`.** The graph stays exactly as it is — `check-screens.py`,
`screen-index.json`, `board-data.js` and the reachability check all join on those ids.
`transitions[]` is written alongside, and a screen with an unlabelled edge simply has no entry
for it.

Idempotent: re-running replaces the labels rather than compounding them.
"""

from __future__ import annotations
import pathlib
import sys

import yaml

SCREENS = pathlib.Path(__file__).resolve().parent.parent / "screens" / "P04-point-of-sale.yaml"

# The state vocabulary P04 transitions carry. Names follow the board's own store so the two can be
# read side by side; `cart` is the line collection, `cartHoldExpiresAt` the lease that makes a
# recalled sale different from a re-keyed one.
#
# key: (source screen, destination screen) -> the labels for that transition
T: dict[tuple[str, str], dict] = {

    # ── POS-001 Begin Shift ──────────────────────────────────────────────────────────────
    # The board splits this across two steps — a PIN pad and a float count — and the package
    # holds it as one screen. Both steps are gates on the same transition, so they are one.
    ("POS-001", "POS-002"): dict(
        trigger="Open shift, after the four-digit PIN and the float count",
        control="primaryButton#openShift",
        precondition="pin.length == 4 and openingFloat.counted",
        guard="sale.create",
        carries=["shiftId", "operatorId", "operatorRole", "openingFloat",
                 "workstationId", "outletId", "catalogueBundleVersion"],
        onFailure=[dict(when="networkLost", to="POS-001#offline",
                     note="**Opening does not work offline** (F32) — a float declared offline is a "
                          "float nobody can reconcile against the safe.")],
        provenance="board TICVAI POS Terminal · submit (4867) + openShift (4885); flow F32 steps 1-2",
    ),
    ("POS-001", "POS-007"): dict(
        trigger="Close shift",
        control="iconButton#closeShift",
        precondition="shift.status == 'open'",
        guard="shift.reopen",
        escalatable=True,
        carries=["shiftId", "expectedCash", "cashMovements"],
        provenance="board TICVAI POS Terminal · goClose (4891); flow F32 step 6",
    ),

    # ── POS-002 Sell · Ticket Catalogue ──────────────────────────────────────────────────
    ("POS-002", "POS-003"): dict(
        trigger="Choose a date and session for a timed product",
        control="drawer#drawerDateAndSession",
        precondition="product.timed",
        carries=["productId", "visitDate", "sessionTime", "quantityByVariant"],
        returnsTo="POS-002",
        discards=["drawerSelection"],
        provenance="board TICVAI POS Terminal · openDrawer (4082) + dGo/pickShowTime (4276-4278)",
    ),
    ("POS-002", "POS-004"): dict(
        trigger="Select seats on the plan",
        control="drawer#drawerSeatSelection",
        precondition="product.seats or product.evt",
        carries=["productId", "performanceId", "seatPicks", "zoneId", "holdExpiresAt"],
        returnsTo="POS-002",
        discards=["seatPicks"],
        onFailure=[dict(when="soldOut", to="POS-004#zoneUnavailable",
                     note="The board refuses the zone rather than the sale — `evPickZone` (4269)."),
                dict(when="overSelectionLimit", to="POS-004",
                     note="**Ten seats is the per-sale maximum** — `toggleSeat` (4106).")],
        provenance="board TICVAI POS Terminal · toggleSeat (4106) + drawerConfirm (4118); "
                   "seats are held for 8 minutes",
    ),
    ("POS-002", "POS-006"): dict(
        trigger="Recall held",
        control="iconButton#recallHeld",
        guard="sale.resume",
        provenance="board TICVAI POS Terminal · hold (3992) — hot key F2",
    ),
    ("POS-002", "POS-005"): dict(
        trigger="Charge, or swipe the pay control",
        control="primaryButton#charge",
        precondition="cart.lineCount > 0",
        guard="payment.take",
        carries=["cart", "guest", "discount", "orderType", "table", "taxTotals"],
        returnsTo="POS-002",
        discards=[],
        onFailure=[
            dict(when="declined", to="POS-005#paymentFailed",
                 note="Retry reuses the same idempotency key and transaction id — "
                      "`retryPayment` (4645). A retry is never a new transaction."),
            dict(when="timeout", to="POS-005#paymentFailed"),
            dict(when="networkLost", to="POS-005#paymentUnknown",
                 note="**The branch that matters.** A card authorisation interrupted mid-flight has "
                      "an outcome nobody knows yet. The board resolves it against the gateway "
                      "(`checkPaymentStatus`, 4670) rather than guessing. `states/payment.yaml` has "
                      "no `unknown` and should."),
        ],
        provenance="board TICVAI POS Terminal · goCheckout (5157) + launchPayment (4597)",
    ),

    # ── POS-003 / POS-004 back to the catalogue ──────────────────────────────────────────
    ("POS-003", "POS-002"): dict(
        trigger="Back",
        control="secondaryButton#backToDetail",
        returnsTo="POS-002",
        discards=["sessionTime", "quantityByVariant"],
        provenance="board TICVAI POS Terminal · backToDetail (5309)",
    ),
    ("POS-004", "POS-002"): dict(
        trigger="Back",
        control="secondaryButton#backToDetail",
        returnsTo="POS-002",
        discards=["seatPicks"],
        provenance="board TICVAI POS Terminal · backToDetail (5309)",
    ),
    ("POS-003", "POS-005"): dict(
        trigger="Add to sale, then charge",
        precondition="cart.lineCount > 0",
        guard="payment.take",
        carries=["cart", "guest", "discount", "visitDate", "sessionTime"],
        provenance="board TICVAI POS Terminal · drawerConfirm (4118) then goCheckout (5157)",
    ),
    ("POS-004", "POS-005"): dict(
        trigger="Add seats to sale, then charge",
        precondition="cart.lineCount > 0",
        guard="payment.take",
        carries=["cart", "seatPicks", "holdExpiresAt", "guest", "discount"],
        provenance="board TICVAI POS Terminal · drawerConfirm (4118) then goCheckout (5157)",
    ),

    # ── POS-005 Payment ──────────────────────────────────────────────────────────────────
    ("POS-005", "POS-002"): dict(
        trigger="Back to sale",
        control="secondaryButton#backToSale",
        returnsTo="POS-002",
        discards=["tendered", "splitParts"],
        carries=["cart", "guest", "discount", "orderType"],
        provenance="board TICVAI POS Terminal · backToSale (5506). **The cart survives.** "
                   "`cancelPaymentTxn` (4655) is the other path and it clears the cart — raised as "
                   "POS-BOARD-AUDIT.md C-6, because a declined card is not an abandoned sale.",
    ),

    # ── POS-006 Held Orders ──────────────────────────────────────────────────────────────
    # The reference example for `carries`, and the reason the field exists.
    ("POS-006", "POS-002"): dict(
        trigger="Recall this held sale",
        control="dataTable#heldList",
        guard="sale.resume",
        carries=["cart", "cartHoldExpiresAt", "guest", "discount", "table", "orderType"],
        returnsTo="POS-006",
        provenance="board TICVAI POS Terminal · recall (4000). **The hold clock travels with the "
                   "cart** — a destination that re-fetches the lines has lost the lease, and the "
                   "guest's seats go back on sale while they are standing at the till.",
    ),

    # ── POS-007 Close Shift ──────────────────────────────────────────────────────────────
    ("POS-007", "POS-001"): dict(
        trigger="Close and sign out",
        control="primaryButton#lockShift",
        precondition="closeStep == 'summary'",
        guard="cash.variance.approve",
        escalatable=True,
        carries=["shiftId", "countedCash", "variance", "approverPrincipalId"],
        discards=["cart", "guest", "table", "discount"],
        onFailure=[dict(when="varianceOutOfTolerance", to="POS-007#awaitingApproval",
                     note="Variance beyond tolerance holds the close until a Duty Manager PIN is "
                          "captured — `pinConfirm` case 'shift' (4348). The expected figure is "
                          "never shown before the count (blindCount).")],
        provenance="board TICVAI POS Terminal · signOut (5641) + lockShift (5687); flow F32 step 6",
    ),

    # ── POS-013 Offline / Sync ───────────────────────────────────────────────────────────
    ("POS-013", "POS-020"): dict(
        trigger="Open a queued transaction that needs attention",
        control="dataTable#syncQueue",
        precondition="syncQueue.any(status in ['CONFLICT','FAILED','REQUIRES_ATTENTION'])",
        guard="inventory.conflict.resolve",
        escalatable=True,
        carries=["localTxnId", "conflictReason", "productId"],
        provenance="board TICVAI POS Terminal · openConflict (4770) + resolveConflict (4776)",
    ),
    ("POS-013", "POS-002"): dict(
        trigger="Back to sale",
        carries=["cart", "guest", "discount"],
        provenance="board TICVAI POS Terminal · navigation rail; **selling continues offline** "
                   "(ADR-0013) and the queue drains on reconnect — `toggleNet` (4750).",
    ),

    # ── POS-021 / POS-022 / POS-023 — the other sell surfaces ────────────────────────────
    ("POS-021", "POS-005"): dict(
        trigger="Charge",
        control="primaryButton#charge",
        precondition="cart.lineCount > 0",
        guard="payment.take",
        carries=["cart", "guest", "discount", "orderType", "table", "taxTotals"],
        returnsTo="POS-021",
        provenance="board TICVAI POS Terminal · goCheckout (5157) from the `fnb` screen",
    ),
    ("POS-022", "POS-005"): dict(
        trigger="Send to kitchen, then charge",
        precondition="order.lineCount > 0",
        guard="payment.take",
        carries=["orderId", "tableLabel", "courses", "cart"],
        provenance="board TICVAI POS Terminal · queue STAGES (3483) — **the kitchen fires on "
                   "payment** for quick service and on send for dine-in.",
    ),
    ("POS-023", "POS-005"): dict(
        trigger="Charge",
        control="primaryButton#charge",
        precondition="cart.lineCount > 0",
        guard="payment.take",
        carries=["cart", "guest", "discount", "taxTotals"],
        returnsTo="POS-023",
        onFailure=[dict(when="outOfStock", to="POS-023#stockConflict",
                     note="Reserve-on-add means the shortfall is found before payment — "
                          "`reserveStock` (4025). Offline, the sale proceeds on policy and the "
                          "conflict is raised at sync.")],
        provenance="board TICVAI POS Terminal · goCheckout (5157) from the `retail` screen",
    ),
}

# Screens that live inside the application shell and therefore take part in the primary rail.
# The board's `onApp` list, mapped to package ids.
USES_RAIL = ["POS-002", "POS-005", "POS-007", "POS-008", "POS-009", "POS-011",
             "POS-012", "POS-013", "POS-015", "POS-016", "POS-021", "POS-023"]

# Screens that can hold a cart and therefore share the charge transition.
USES_CHARGE = ["POS-002", "POS-003", "POS-004", "POS-010", "POS-021", "POS-022", "POS-023"]

# **A guarded transition and a `denied` state are one decision written in two places.** Declaring
# the first without the second is how `denied` came to stand at 3 screens out of 1,231 — the gate
# was recorded on the control and the consequence was recorded nowhere.
#
# Escalatable and refused are different sentences. Where a supervisor PIN unlocks the action the
# screen says so and stays; where it does not, it says who to fetch.
DENIED = {
 "POS-001": "Sign-in succeeds and the shift will not open — the operator's role does not hold "
            "`sale.create` on this terminal. The float count is kept, not discarded, and a "
            "supervisor can open the shift against the same count.",
 "POS-002": "The catalogue reads normally and **Charge is refused** without `payment.take`. The "
            "cart is held, not cleared, so a permitted operator can complete the same sale.",
 "POS-003": "Session and date selection are readable; adding to a sale needs `payment.take` to "
            "complete. The hold is not taken until the sale can be charged.",
 "POS-004": "Seats can be viewed but not held without `payment.take` — an unchargeable hold takes "
            "capacity off sale for eight minutes and returns it unsold.",
 "POS-006": "Held sales are listed and cannot be recalled without `sale.resume`. **The list is "
            "still shown**, because a cashier who cannot see the held sale fetches a supervisor to "
            "the wrong screen.",
 "POS-007": "The count is accepted and the close is held. A variance beyond tolerance needs "
            "`cash.variance.approve` — a supervisor PIN is captured in place and the shift closes "
            "against the same count, rather than the cashier counting twice.",
 "POS-013": "The sync queue is readable by anyone on shift. Resolving a conflict changes stock and "
            "needs `inventory.conflict.resolve`; a supervisor PIN unlocks it in place.",
 "POS-021": "Ordering is refused without `payment.take`. The kitchen is not fired, so nothing is "
            "cooked against a sale that cannot be paid for.",
 "POS-022": "The rail is readable and **Send to kitchen is refused** without `payment.take`. "
            "Tickets already fired are unaffected.",
 "POS-023": "Merchandise scans and prices normally; charging needs `payment.take`. Stock reserved "
            "on add is released rather than held against a sale that cannot complete.",
}


# Gaps the encoding exposed — recorded on the screen, per the schema's own rule that a screen
# naming the thing it is missing has done the thinking.
GAPS = {
    "POS-005": [
        dict(field="navigation.exitTo",
             why="**The success branch has nowhere to go.** `finishPayment` (4636) lands on a "
                 "receipt with a VAT breakdown, a reprint and a 12-second auto-continue back to a "
                 "new sale. P04 declares no receipt screen, so the most-reached screen on the "
                 "platform is undrawn and unspecified.",
             source="POS-BOARD-AUDIT.md §5"),
        dict(field="Order.buyerTrn",
             why="**Above AED 10,000 a simplified tax invoice is not lawful** — a full UAE tax "
                 "invoice needs the buyer's name, address and TRN. The board relabels the receipt "
                 "at the threshold and captures none of the three, and no P04 screen declares the "
                 "capture. See `roles.yaml` thresholds.taxInvoice.",
             source="POS-BOARD-AUDIT.md C-11"),
    ],
    "POS-020": [
        dict(operation="recordNoSale",
             why="**A no-sale with no reason is the single most reliable indicator of till theft** "
                 "(F32 step 5), and nothing in the board or this screen captures one. The board's "
                 "home hot key opens the drawer with no permission check and no audit record.",
             source="POS-BOARD-AUDIT.md C-4, C-5"),
    ],
}


def main() -> int:
    doc = yaml.safe_load(SCREENS.read_text(encoding="utf-8"))
    screens = doc["screens"]
    by_id = {s["id"]: s for s in screens}

    labelled = bare = 0
    for s in screens:
        sid = s["id"]
        nav = s.setdefault("navigation", {})
        # `exitTo` is left exactly as it is — bare screen ids. `check-screens.py`,
        # `screen-index.json`, `board-data.js` and the reachability check all join on it.
        exits = [t if isinstance(t, str) else t.get("to") for t in (nav.get("exitTo") or [])]
        nav["exitTo"] = exits

        trans = []
        for to in exits:
            spec = T.get((sid, to))
            if spec:
                trans.append({"to": to, **spec})
                labelled += 1
            else:
                # No entry. The board does not demonstrate this transition, and a plausible
                # trigger invented here would read as a decision somebody made.
                bare += 1
        if trans:
            nav["transitions"] = trans
        elif "transitions" in nav:
            del nav["transitions"]

        uses = []
        if sid in USES_RAIL:
            uses.append("posPrimaryRail")
        if sid in USES_CHARGE:
            uses.append("posSaleToPayment")
        if uses:
            nav["uses"] = uses
        elif "uses" in nav:
            del nav["uses"]

        st = s.setdefault("states", {})
        if sid in DENIED and not st.get("denied"):
            st["denied"] = DENIED[sid]

        for g in GAPS.get(sid, []):
            existing = s.setdefault("gaps", [])
            if not any(x.get("why") == g["why"] for x in existing):
                existing.append(g)

    SCREENS.write_text(
        yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=98),
        encoding="utf-8")

    total = labelled + bare
    print(f"P04: {total} transitions · {labelled} labelled from the board "
          f"({labelled * 100 // total}%) · {bare} left bare")
    print(f"     rail: {len(USES_RAIL)} screens · charge: {len(USES_CHARGE)} screens")
    print(f"     gaps recorded on: {', '.join(sorted(GAPS))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
