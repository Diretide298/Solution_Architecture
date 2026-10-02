#!/usr/bin/env python3
"""Say which guest screens are behind sign-in, and which loads on a public screen wait for one.

**Decided by Chinmay on 2 October 2026: fix before any Block A ticket starts** (GFIX-6, CHG-GST-006). After
the published reads were opened to visitors (tools/applied/guest-public-reads-2-october.py, GFIX-5),
`tools/check-preauth-session.py` still found guest screens a visitor can reach that load the guest's own
records (PS-UNDECLARED-SIGNIN) or a personal read that needs a session (PS-LOAD-NEEDS-SESSION). Personal reads
stay behind sign-in; the screens say so. Three cases:

  ACCOUNT   the screen is the guest's own record (tickets, orders, wallet, memberships, reservations, cases,
            notifications, loyalty, wishlist, the virtual-queue place, saved routes): it declares
            `entryState.params` `subjectId` `from: session`, so it is behind sign-in and a visitor who opens
            it is sent to sign in and brought back (GFIX-4's no-access state).
  SIGNED_IN a public screen with one load that runs only for a signed-in guest (Home's tickets, the plans'
            own memberships, help's own cases): the `apis` purpose says so.
  CART      a booking, basket or kiosk screen that reads the cart, hold or order of the guest session the
            device already holds: signed in, or the anonymous cart session every visitor gets when a first
            line is added (ADR-0045, `createCart`). The purpose says which session it rides on.

Idempotent.

    python tools/applied/guest-signin-declarations-2-october.py [--apply]
"""
import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
FILES = [ROOT / "screens" / n for n in ("P01-guest-web-storefront.yaml", "P02-guest-mobile-app.yaml",
                                        "P05-guest-kiosk.yaml")]
WHEN = "decided 2 October 2026 by Chinmay, fix before Block A starts (GFIX-6)"

ACCOUNT = {
    "WEB-018", "GST-012", "GST-013", "GST-055",              # tickets
    "WEB-019", "GST-019", "WEB-030", "GST-014",              # orders and transfers
    "GST-011",                                               # wallet
    "WEB-023", "GST-015",                                    # membership management
    "WEB-031", "GST-016", "GST-017",                         # reservations
    "WEB-034", "GST-034",                                    # lost and found cases
    "WEB-046", "GST-030",                                    # notifications
    "WEB-043", "GST-036",                                    # loyalty position
    "GST-020",                                               # wishlist
    "WEB-040", "GST-023",                                    # the guest's place in a virtual queue
    "GST-079",                                               # saved routes
    "WEB-038",                                               # tracking the guest's own F&B order
}
SIGNED_IN = {
    ("WEB-022", "getMyMemberships"), ("GST-040", "listMyCases"), ("WEB-025", "listCases"),
    ("WEB-044", "listAiConversations"), ("WEB-049", "listMyFavouriteRoutes"),
    ("WEB-050", "getVisitPlan"), ("GST-053", "getVisitPlan"), ("GST-054", "getVisitPlan"),
    ("GST-059", "getVisitPlan"), ("GST-054", "createAiConversation"),
    ("WEB-036", "getGuestOrderStatus"), ("GST-024", "getGuestOrderStatus"), ("GST-032", "getGuestOrderStatus"),
    ("WEB-016", "getGuestSession"), ("GST-042", "getGuestSession"),
}
CART = {
    ("WEB-010", "getCart"), ("WEB-010", "createCart"), ("WEB-010", "getCouponCode"), ("WEB-010", "getResourceHold"),
    ("GST-041", "getCart"), ("GST-041", "getResourceHold"), ("GST-009", "getCart"), ("GST-032", "getCart"),
    ("GST-053", "getCart"), ("KSK-006", "getCart"), ("WEB-047", "getResourceHold"), ("GST-074", "getResourceHold"),
    ("WEB-012", "getOrder"), ("WEB-013", "getOrder"), ("GST-010", "getOrder"), ("GST-028", "getOrder"),
    ("KSK-009", "getOrder"), ("KSK-011", "getOrder"),
}
SAY_SIGNED_IN = " Only when signed in (" + WHEN + ")."
SAY_CART = (" With the guest session the device already holds: signed in, or the anonymous cart session a "
            "visitor gets with the first line (ADR-0045) (" + WHEN + ").")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    log = []
    for f in FILES:
        text = f.read_text(encoding="utf-8")
        doc = yaml.safe_load(text)
        for s in doc["screens"]:
            sid = s["id"]
            if sid in ACCOUNT:
                es = s.setdefault("entryState", {})
                params = es.setdefault("params", [])
                if not any(isinstance(p, dict) and p.get("name") == "subjectId" for p in params):
                    params.insert(0, {"name": "subjectId", "from": "session"})
                    log.append(f"{sid}: behind sign-in (subjectId from session)")
                else:
                    for p in params:
                        if p.get("name") == "subjectId" and p.get("from") != "session":
                            log.append(f"{sid}: subjectId from {p.get('from')} -> session")
                            p["from"] = "session"
            for api in s.get("apis") or []:
                key = (sid, api.get("operationId"))
                add = SAY_SIGNED_IN if key in SIGNED_IN else SAY_CART if key in CART else None
                if add and "(GFIX-6)" not in str(api.get("purpose") or ""):
                    api["purpose"] = str(api.get("purpose") or "").rstrip() + add
                    log.append(f"{sid}: {key[1]} purpose says {'signed in' if key in SIGNED_IN else 'cart session'}")
        out = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)
        if out != text:
            log.append(f"{f.name}: {'written' if a.apply else 'would change'}")
            if a.apply:
                with open(f, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(out)
    print("\n".join(log) if log else "nothing to do")
    return 0


if __name__ == "__main__":
    sys.exit(main())
