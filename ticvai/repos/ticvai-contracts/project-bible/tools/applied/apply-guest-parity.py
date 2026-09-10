#!/usr/bin/env python3
"""Give the guest mobile app the twenty-three operations only guest web could call.

**Decided 10 September 2026: guest web and guest mobile are one product in two shells**, so an
operation on one and not the other is a defect rather than a difference. The tally:

    P01 Guest Web   46 screens · 115 operations
    P02 Guest App   71 screens · 132 operations
    shared 92 · web-only 23 · mobile-only 40

**The mobile app could not complete a purchase.** It calls `checkoutCart` and `createPayment` and
has never called `createOrder` — it could start a checkout and could not produce an order. The
whole cart-editing surface was web-only too: `updateCartLine`, `removeCartLine`, `extendCart`,
`abandonCart`, `claimCart`. A guest on a phone could put things in a basket and not take one out.

**Two of these are worse on mobile than on web.** `registerGuestDevice`, `revokeGuestDevice` and
`listGuestDevices` were web-only — and the phone *is* the device. The app that holds the
credential could not show you which devices hold it.

**The forty mobile-only operations are not touched.** Face pass, waitlists, resale, referrals,
delegation, wallet passes and AI conversations belong on a phone in ways they may not belong on
the web, and deciding that is the client's call, not a symmetry exercise. **This closes the gap
that makes mobile weaker, not the one that makes it different.**

Each operation is placed on the mobile screen that already does that job. Nothing new is invented:
every one of the twenty-three is an operation guest web has been calling all along.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
P02 = ROOT / "screens" / "P02-guest-mobile-app.yaml"

# operation -> (mobile screen that already does this job, contract, why it is on that screen)
PLACE = {
    # the cart a guest could fill and not empty
    "updateCartLine":  ("GST-041", "orders", "Change a quantity before paying"),
    "removeCartLine":  ("GST-041", "orders", "Take a line out of the basket"),
    "extendCart":      ("GST-041", "orders", "Keep the hold alive while the guest decides"),
    "abandonCart":     ("GST-041", "orders", "Give the inventory back"),
    "claimCart":       ("GST-041", "orders", "Pick up a basket started on another device"),
    "listProductVariants": ("GST-041", "catalogue", "Which variant each line is"),

    # the order the app could never create
    "createOrder":          ("GST-009", "orders", "Turn the checked-out cart into an order"),
    "acquireInventoryHold": ("GST-009", "inventory", "Hold the stock while payment is taken"),

    # paying for something somebody else booked
    "getPaymentLink": ("GST-009", "payments", "Open a payment link sent to this guest"),
    "payByLink":      ("GST-009", "payments", "Pay a booking somebody else made"),

    # the phone is the device, and could not see its own registrations
    "listGuestDevices":   ("GST-073", "identity", "Which devices hold this guest's credentials"),
    "registerGuestDevice": ("GST-073", "identity", "Trust this device"),
    "revokeGuestDevice":  ("GST-073", "identity", "Sign a lost device out"),
    "verifyGuestEmail":   ("GST-073", "identity", "Confirm the address before it can recover an account"),

    # profile and marketing consent
    "updateMyProfile":          ("GST-039", "crm", "Change name, contact and preferences"),
    "getMarketingSubscription": ("GST-065", "marketing", "What this guest has opted into"),
    "setMarketingSubscription": ("GST-065", "marketing", "Change it"),

    # money instruments the wallet screen already shows
    "getGiftCard":    ("GST-071", "payments", "Balance on a gift card"),
    "getCouponCode":  ("GST-037", "promotions", "Resolve a code the guest typed"),

    # in-venue surfaces that existed without their read
    "listQueues":        ("GST-023", "queue", "Which virtual queues are running"),
    "lookupMerchandise": ("GST-026", "retail", "Find an item by code or scan"),
    "reserveMerchandise": ("GST-026", "retail", "Hold it for collection"),

    # the shell
    "getTenantConfig": ("GST-001", "tenancy", "Branding, currency and what this venue enables"),
}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    apply = "--apply" in sys.argv
    doc = yaml.safe_load(P02.read_text(encoding="utf-8"))
    by_id = {s["id"]: s for s in doc["screens"]}

    todo = []
    missing_screen = []
    for op, (sid, contract, purpose) in sorted(PLACE.items()):
        s = by_id.get(sid)
        if s is None:
            missing_screen.append((op, sid))
            continue
        have = {a.get("operationId") for a in (s.get("apis") or [])}
        if op in have:
            continue
        todo.append((sid, op))
        if apply:
            s.setdefault("apis", []).append({
                "operationId": op, "contract": contract, "purpose": purpose,
                "trigger": "onAction" if op[:3] in ("cre", "upd", "rem", "set", "pay", "reg",
                                                    "rev", "cla", "aba", "ext", "acq", "res",
                                                    "ver") else "onLoad",
            })

    if missing_screen:
        for op, sid in missing_screen:
            print(f"  ! {sid} does not exist on P02 — {op} has nowhere to go")
    if not todo:
        print("nothing to do — guest mobile calls every operation guest web does")
        return 0

    per = {}
    for sid, op in todo:
        per.setdefault(sid, []).append(op)
    for sid in sorted(per):
        print(f"  {sid} {by_id[sid]['name'][:30]:<32} + {', '.join(sorted(per[sid]))}")
    print(f"\n{len(todo)} operation(s) across {len(per)} screen(s)")

    if not apply:
        print("run with --apply to write")
        return 0
    P02.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                   encoding="utf-8")
    print("written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
