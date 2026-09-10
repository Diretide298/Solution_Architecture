#!/usr/bin/env python3
"""The other half of guest parity — what the mobile app can do and the website cannot.

`apply-guest-parity.py` closed the twenty-three operations mobile was missing. This asks the
reverse question, and the answer is not "all forty".

**Nothing in the contracts makes any of these mobile-only.** All forty were checked for a channel
or audience restriction and **not one carries either** — the split is accidental, a consequence of
two platforms being specified by different people at different times, not a decision anybody made.

**So the test is device capability, and only one operation passes it.** `enrolFacePass` needs a
camera and a liveness check performed under supervision; that is a phone in a venue, not a desktop
browser. Everything else has no technical reason to be absent from the web — and six of them are
worse than an inconvenience:

    exportSubjectData · deleteGuestAccount · getGuestConsents
    updateGuestPreferences · getWaiverStatus · uploadGuestDocument

**A data-subject request that only works inside an app is a compliance problem.** A guest who
never installed it cannot see their consents, export their data, or ask for their account to be
deleted. Those rights do not depend on which shell somebody happens to use.

**Left on mobile deliberately:** `enrolFacePass` (camera and liveness). Its companions
`getFacePassEnrolment` and `revokeFacePass` come to web anyway — **you should be able to revoke a
face enrolment from a desktop after losing the phone that made it**, which is exactly when you
most need to.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
P01 = ROOT / "screens" / "P01-guest-web-storefront.yaml"

# The one operation that stays on the phone, and why.
PHONE_ONLY = {
    "enrolFacePass": "Camera capture with a liveness check, done in venue. A desktop browser is "
                     "the wrong instrument and an unsupervised enrolment is the wrong process.",
}

# operation -> (web screen that already does this job, contract, why it belongs there)
PLACE = {
    # --- rights a guest holds regardless of which shell they use -------------------------
    "getGuestConsents":      ("WEB-024", "marketing-crm", "What this guest has consented to"),
    "updateGuestPreferences": ("WEB-020", "marketing-crm", "Change contact and consent preferences"),
    "exportSubjectData":     ("WEB-024", "marketing-crm", "Export everything held about this guest"),
    "deleteGuestAccount":    ("WEB-024", "identity", "Ask for the account to be deleted"),
    "getWaiverStatus":       ("WEB-024", "access", "Which waivers are signed and which are due"),
    "uploadGuestDocument":   ("WEB-011", "marketing-crm", "Provide a document a booking requires"),

    # --- security, which is worst on the device you have lost ---------------------------
    "createMfaChallenge":    ("WEB-016", "identity", "Second factor at sign-in"),
    "getMyChallenges":       ("WEB-017", "identity", "Outstanding security challenges"),
    "getFacePassEnrolment":  ("WEB-024", "access", "Whether a face pass is enrolled on this account"),
    "revokeFacePass":        ("WEB-024", "access", "Revoke it after losing the phone that made it"),
    "listDelegations":       ("WEB-024", "identity", "Who may act for this guest"),
    "grantDelegation":       ("WEB-024", "identity", "Let somebody else manage a booking"),

    # --- money -------------------------------------------------------------------------
    "listPaymentTokens":     ("WEB-021", "payments", "Saved cards on this account"),
    "storePaymentToken":     ("WEB-021", "payments", "Save a card for next time"),
    "transferWalletBalance": ("WEB-021", "payments", "Move value between wallets"),
    "redeemLoyaltyPoints":   ("WEB-043", "marketing-crm", "Spend points"),
    "inquirePaymentStatus":  ("WEB-012", "payments", "Ask what happened to a payment that did not answer"),
    "issueWalletPass":       ("WEB-018", "access", "Add the ticket to a phone wallet from the desktop"),

    # --- support and self-service -------------------------------------------------------
    "createCase":            ("WEB-025", "customer-service", "Raise a case"),
    "listCases":             ("WEB-025", "customer-service", "Cases this guest has open"),
    "createRefundRequest":   ("WEB-019", "orders", "Ask for a refund"),
    "createResaleListing":   ("WEB-030", "resale", "List a ticket for resale"),

    # --- catalogue the website simply never read ---------------------------------------
    "getPerformance":        ("WEB-006", "catalogue", "The performance being booked"),
    "getBundle":             ("WEB-008", "catalogue", "A bundle offered as an upsell"),
    "listCatalogueBundles":  ("WEB-008", "catalogue", "Which bundles apply here"),
    "getGameCard":           ("WEB-021", "games", "Balance on a game card"),

    # --- booking things that are not tickets --------------------------------------------
    "bookResource":          ("WEB-031", "resources", "Book a cabana or similar"),
    "getResourceAvailability": ("WEB-031", "resources", "What is free and when"),
    "createTableReservation": ("WEB-036", "fnb", "Reserve a table"),
    "updateTableReservation": ("WEB-031", "fnb", "Change or cancel it"),
    "joinRestaurantWaitlist": ("WEB-036", "fnb", "Join the waitlist when nothing is free"),
    "joinWaitlist":          ("WEB-040", "queue", "Join a virtual queue"),
    "leaveWaitlist":         ("WEB-040", "queue", "Leave it"),

    # --- groups and sharing -------------------------------------------------------------
    "getGroupBooking":       ("WEB-031", "orders", "A group booking this guest belongs to"),
    "respondToInvitation":   ("WEB-017", "orders", "Accept or decline an invitation"),
    "shareEntitlement":      ("WEB-018", "access", "Send a ticket to somebody"),
    "createReferral":        ("WEB-043", "marketing-crm", "Refer a friend"),

    # --- the concierge ------------------------------------------------------------------
    "listAiConversations":   ("WEB-044", "ai", "Earlier conversations"),
    "sendConversationMessage": ("WEB-044", "ai", "Ask the concierge something"),
}

WRITES = ("create", "update", "delete", "set", "store", "transfer", "redeem", "issue", "grant",
          "revoke", "upload", "export", "join", "leave", "book", "respond", "share", "send")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    apply = "--apply" in sys.argv
    doc = yaml.safe_load(P01.read_text(encoding="utf-8"))
    by_id = {s["id"]: s for s in doc["screens"]}

    todo, absent = [], []
    for op, (sid, contract, purpose) in sorted(PLACE.items()):
        s = by_id.get(sid)
        if s is None:
            absent.append((op, sid))
            continue
        if op in {a.get("operationId") for a in (s.get("apis") or [])}:
            continue
        todo.append((sid, op))
        if apply:
            s.setdefault("apis", []).append({
                "operationId": op, "contract": contract, "purpose": purpose,
                "trigger": "onAction" if op.startswith(WRITES) else "onLoad",
            })

    for op, sid in absent:
        print(f"  ! {sid} does not exist on P01 — {op} has nowhere to go")
    if not todo:
        print("nothing to do — guest web calls everything mobile does, bar the camera work")
    else:
        per = {}
        for sid, op in todo:
            per.setdefault(sid, []).append(op)
        for sid in sorted(per):
            print(f"  {sid} {by_id[sid]['name'][:30]:<32} + {', '.join(sorted(per[sid]))}")
        print(f"\n{len(todo)} operation(s) across {len(per)} screen(s)")
    print("\nstaying on the phone: " + ", ".join(PHONE_ONLY))
    for k, v in PHONE_ONLY.items():
        print(f"  {k} — {v}")

    if todo and apply:
        P01.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                       encoding="utf-8")
        print("\nwritten")
    elif todo:
        print("\nrun with --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
