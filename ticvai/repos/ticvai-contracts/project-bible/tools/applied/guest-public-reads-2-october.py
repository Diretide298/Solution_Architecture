#!/usr/bin/env python3
"""Let a guest call what the contracts already say a guest may call, and let a visitor browse before signing in.

**Decided by Chinmay on 2 October 2026: fix before any Block A ticket starts** (GFIX-5, CHG-GST-005). The
typed check of the council of 2 October (`tools/check-audience-match.py`, rule AM-GUEST-SECURITY) found 84
operations whose `x-ticvai-audience` includes guests while their effective `security` admits only a staff
bearer token: most declared no `security` of their own and fell back to their contract's `bearerAuth`. A
guest screen calling one is refused. Its sister check (`tools/check-preauth-session.py`) found 200 loads on
the 125 guest screens a visitor reaches before signing in that need a session, led by `listProducts` (25
screens), `getWaitTimes` (14), `listPerformances` (9) and `getAvailability` (9). Browsing the storefront
before sign-in must work.

Two kinds of fix, both **widening only**: every alternative an operation accepted is kept, so a client built
against r1 with a bearer token still works (tools/check-contract-compat.py counts a security change that only
adds alternatives as additive, 2 October).

  PUBLIC  the published, non-personal reads a first-time visitor needs (the catalogue, availability,
          performances, seats, offers, the shop, queues, programmes and rewards on offer, consent purposes,
          recommendations for an anonymous visitor):  `security: [{}, guestAuth, bearerAuth]`. The `{}`
          alternative makes the credential optional (header, ADR-0025: a guest call resolves to published
          data; a staff token keeps its permission).
  GUEST   everything else that declares a guest audience (the guest's own records and the actions a guest
          takes): `security: [guestAuth, bearerAuth]`. Personal reads stay behind sign-in.

Operations whose only non-staff audience is `public` (an external reviewer or a TICVAI prospect signing in
with a bearer token: decideApprovalRequest, listApprovalRequests, listVenueTypeTemplates,
submitOnboardingApplication) are not guest operations and are left for the lead.

Text edits, so every comment and quote in the contracts survives. Idempotent.

    python tools/applied/guest-public-reads-2-october.py [--apply]
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

PUBLIC = {
    # catalogue: what is on sale, when, and whether there is room
    "listProducts", "getProduct", "listProductCategories", "listProductVariants", "searchCatalogue",
    "listPerformances", "getPerformance", "getAvailability", "getProductEligibilityRule",
    "listCatalogueBundles", "listGroupPackages", "getGroupPackageDefinition", "listMembershipProgrammes",
    "listMembershipBenefits", "getPlanBenefits",
    # offers, seats, the shop and the queues a visitor looks at
    "listPromotions", "getPromotion", "getBundle", "getSeatAvailability", "listMerchandise",
    "lookupMerchandise", "listQueues",
    # programmes and rewards on offer, and what a visitor is asked to consent to
    "listLoyaltyProgrammes", "listRewards", "listBadges", "listConsentPurposes",
    # declared anonymous already: a visitor's recommendation slot and its events
    "decideRecommendations", "recordRecommendationEvents",
    # the module catalogue a prospect reads before an account exists
    "listModuleCatalogue",
}
# **The second pass: published reads that admitted a guest token but no visitor** (check-preauth-session
# PS-LOAD-NEEDS-SESSION after the first pass): wait times, the guest menu and dining, the venue map, transport
# timetables and fares, parking facilities, the tender exchange rates and the analytics tags the storefront
# loads after consent. Each keeps its alternatives and gains `{}`.
PUBLIC_EXTRA = {
    "getWaitTimes", "getGuestMenu", "listModifierGroups", "listDiningOutlets", "listDeliveryLocations",
    "getFnbDeliveryPolicy", "listFulfilmentSlots", "getVenueMap", "getVenueMapGraph", "listBookableVenueMaps",
    "getMapResourceAvailability", "listTransportStations", "searchTransportDepartures", "getTransportRoute",
    "getTransportRouteMap", "getTransportFareTable", "listTransportPassOffers", "listParkingFacilities",
    "listFxRates", "listAnalyticsProviders",
}
PUBLIC |= PUBLIC_EXTRA
NOT_GUEST = {"decideApprovalRequest", "listApprovalRequests", "listVenueTypeTemplates",
             "submitOnboardingApplication"}
COMMENT_PUBLIC = ("      # Public, with an optional token (decided 2 October, GFIX-5): a visitor browses before "
                  "signing in; a guest\n      # or staff token is still accepted. `{}` makes the credential "
                  "optional.\n")




def guest_ops() -> dict:
    """operationId -> contract file, for every operation whose audience includes guests and whose effective
    security admits no guest."""
    out = {}
    for f in sorted((ROOT / "contracts").glob("*/*.yaml")):
        if f.parent.name not in ("spine", "satellite"):
            continue
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        default = d.get("security")
        for item in (d.get("paths") or {}).values():
            if not isinstance(item, dict):
                continue
            for op in item.values():
                if not isinstance(op, dict) or not op.get("operationId"):
                    continue
                aud = set(op.get("x-ticvai-audience") or [])
                if not aud & {"guest", "anonymous"}:
                    continue
                sec = op.get("security", default)
                if sec == [] or any(isinstance(x, dict) and not x for x in sec or []):
                    continue
                if op["operationId"] in PUBLIC or not any(isinstance(x, dict) and "guestAuth" in x
                                                          for x in sec or []):
                    out[op["operationId"]] = (f, sec or [])
    return out
    return out


def block_for(op: str, sec: list) -> str:
    """The new security: the alternatives it had, and what this pass adds, in the contracts' order."""
    alts = [x for x in sec if isinstance(x, dict) and x]
    names = [next(iter(x)) for x in alts]
    if "guestAuth" not in names:
        names.insert(0, "guestAuth")
    if "bearerAuth" not in names and op not in PUBLIC_EXTRA:
        names.append("bearerAuth")
    body = ["      security:"] + (["      - {}"] if op in PUBLIC else []) + [f"      - {n}: []" for n in names]
    return (COMMENT_PUBLIC if op in PUBLIC else "") + "\n".join(body) + "\n"


def patch(text: str, op: str, sec: list) -> str:
    lines = text.split("\n")
    i = next(n for n, ln in enumerate(lines) if re.match(r"^      operationId: " + re.escape(op) + r"\s*$", ln))
    end = i + 1
    while end < len(lines) and (lines[end].startswith("       ") or lines[end].startswith("      ")
                                or not lines[end].strip()):
        end += 1
    block = block_for(op, sec)
    s = next((n for n in range(i, end) if lines[n] == "      security:"), None)
    if s is not None:
        e = s + 1
        while e < end and re.match(r"^ {6,}- ", lines[e]):
            e += 1
        lines[s:e] = block.rstrip("\n").split("\n")
    else:
        lines[i + 1:i + 1] = block.rstrip("\n").split("\n")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    found = {op: v for op, v in guest_ops().items() if op not in NOT_GUEST}
    todo = {op: v[0] for op, v in found.items()}
    by_file = {}
    for op, f in todo.items():
        by_file.setdefault(f, []).append(op)
    for f, ops in sorted(by_file.items()):
        text = f.read_text(encoding="utf-8")
        for op in sorted(ops):
            text = patch(text, op, found[op][1])
        yaml.safe_load(text)
        pub = sorted(o for o in ops if o in PUBLIC)
        print(f"{f.relative_to(ROOT)}: {len(pub)} public, {len(ops) - len(pub)} guest-session"
              f"  public={', '.join(pub)}")
        if a.apply:
            with open(f, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
    print(f"{len(todo)} operation(s): {sum(1 for o in todo if o in PUBLIC)} public, "
          f"{sum(1 for o in todo if o not in PUBLIC)} guest-session" if todo else "nothing to do")
    if todo and not a.apply:
        print("nothing written - pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
