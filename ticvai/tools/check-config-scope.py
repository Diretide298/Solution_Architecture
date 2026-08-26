#!/usr/bin/env python3
"""
Validate configuration scope against ADR-0018.

The matrix says "configurable" 321 times and 263 of those do not say at what level. ADR-0018
settles it with a rule rather than 263 answers: three levels, nearest ancestor wins, venue is
the floor.

This checks that the contracts hold to it:

  1. Every configuration operation declares `x-ticvai-config-scope`.
  2. The declared scope is one of tenant, region or venue. **Nothing configures below venue** —
     a workstation is assigned a profile the venue defined, not configured itself. Forty
     workstations configured individually is forty things that drift.
  3. `x-ticvai-config-scope` never sits below `x-ticvai-scope-level`. An operation a venue
     manager may call cannot set a tenant-wide value.
  4. The four settled categories are not contradicted — money and ledger stay at region, brand
     and identity stay at tenant. Those are law, store rules and contract, not preference.

Run: python3 tools/check-config-scope.py
"""
import re
import sys
from pathlib import Path

import yaml

# A cp1252 console cannot encode the arrows and dashes this tool prints, and the
# failure lands *after* the work is done — so the output is written, the summary
# line raises UnicodeEncodeError, and a correct run exits 1. Reconfiguring at
# import means anything importing this module gets it too, refresh.sh included.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:      # a captured stream may not be reconfigurable; harmless
    pass


ROOT = Path(__file__).resolve().parents[1]
# The shipped `contracts/` is authoritative. Until 17 August these pointed at a sibling repo
# outside the package, so every validator passed for whoever had that repo checked out and read
# nothing for anyone working from the zip — which is the worst failure a checker can have, because
# it is silent and it looks like success.
CONTRACTS = ROOT / "contracts"
if not CONTRACTS.exists():
    CONTRACTS = ROOT.parent / "ticvai" / "ticvai-contracts" / "openapi"

ERRORS: list[str] = []
WARNINGS: list[str] = []

#  joined on 18 August (CF-138). **Restricted to F&B and retail** — the client decided
# their configuration belongs at outlet, and no other domain trades from a place inside a venue.
VALID = ("tenant", "region", "venue")
OUTLET_DOMAINS = ("fnb", "retail")
# Outlet sits below venue on the commercial branch, beside department on the organisational one.
# Both are depth 3; neither is an ancestor of the other.
RANK = {"tenant": 0, "region": 1, "venue": 2, "department": 3, "outlet": 3, "sub_department": 4, "workstation": 5}

# Settled and not open to preference. ADR-0018, and ADR-0008 / ADR-0006 before it.
MUST_BE_REGION = re.compile(
    r"RegionSettings|FxRate|AccountMapping|Settlement|TaxCode|Denomination", re.I)
MUST_BE_TENANT = re.compile(
    r"BrandIdentity|Theme|AppIcon|Font|Sso|ConsentPurpose|Subscription|ModuleEnablement", re.I)

# An operation is configuration if it writes a **rule**, not a record.
#
# "Profile" means two things here and the distinction matters: an AdmissionProfile is a rule
# that applies to many scans; a GuestProfile is one person's record. Matching both made a
# cashier updating an email address look like a venue setting a tenant-wide default.
IS_CONFIG = re.compile(
    # **A keyword whitelist misses configuration that is not named after a noun on the list.**
    # 24 operations carried an `x-ticvai-config-scope` the checker never examined — including
    # `createMenu` and `updateMenu`, the two cited in review as correctly scoped. Their tags were
    # never actually read.
    #
    # **Widened 24 August** to cover the nouns the package settled on since: a menu, a provider, a
    # matrix, a quota, a facility, a domain. **The tag itself is now the stronger signal** — the
    # skip branch reports anything tagged that these rules still miss, so a gap announces itself
    # rather than passing quietly.
    r"Config|Setting|Policy|Rule|Template|Toggle|Enablement|Mapping|Threshold|"
    r"AdmissionProfile|WorkstationProfile|"
    r"Layout|Board|Denomination|Programme|Definition|Dashboard|"
    # **Narrowed back on the same day it was widened.** `Campaign`, `Collection`, `Category` and
    # `Resource` caught content and records rather than configuration — a marketing campaign is a
    # thing a venue *makes*, not a setting it *holds*, and demanding a config scope on one is
    # asking the wrong question.
    #
    # **The distinction that survives: configuration is what a venue sets once and everything else
    # resolves against.** A menu, a provider, an approval matrix, a quota, an SLA. A campaign is
    # authored, published and retired on its own lifecycle.
    # **Widened 24 August, then narrowed the same day.** The first cut added `Campaign`,
    # `Collection`, `Category` and `Resource` and caught content rather than configuration — a
    # marketing campaign is a thing a venue *makes*, not a setting it *holds*.
    #
    # **Then I dropped `create` from the verb list and made it worse**: 22 operations that
    # legitimately carry a scope tag stopped being examined, including `createMenu` and
    # `createAdmissionProfile`. **Reverted.** The verb is not the discriminator; the noun is, and
    # the skip branch now reports anything tagged that these rules still miss — so a gap
    # announces itself rather than passing quietly.
    r"Menu|Provider|Matrix|Quota|Licensing|Facility|CustomDomain|Footer|"
    r"Sla|Combination|ReaderProfile|ProductCategories|IndexSource|FxRate|"
    r"MessageTrigger|DailyCount|KnowledgeCollection|CustomDomain",
    re.I)
# **Authoring, not configuring.** A bookable resource, a venue map and a donation campaign are
# records a venue creates and retires on their own lifecycle — they resolve *against* configuration
# rather than being it, and demanding a scope on one is asking the wrong question.
NOT_CONFIG = re.compile(r"GuestProfile|createResource|createVenueMap|createDonationCampaign", re.I)
WRITES = ("put", "post", "patch")


def main() -> int:
    files = sorted(list((CONTRACTS / "spine").glob("*.yaml")) +
                   list((CONTRACTS / "satellite").glob("*.yaml")))
    total = tagged = 0
    by_scope: dict[str, int] = {}

    for f in files:
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for verb, op in item.items():
                if verb not in WRITES or not isinstance(op, dict):
                    continue
                oid = op.get("operationId", "")
                if NOT_CONFIG.search(oid):
                    continue
                # **An operation the naming rules do not reach is never examined at all.**
                # `setKitchenSla` and `setTableCombinations` carried a config scope and were
                # skipped, so their tags were never checked — a silent exemption is worse than a
                # missing one, because nothing reports it.
                reached = IS_CONFIG.search(oid) and re.match(
                    r"^(set|configure|update|publish|create|schedule|claim)", oid)
                if not reached:
                    if op.get("x-ticvai-config-scope"):
                        ERRORS.append(
                            f"{f.stem}.{oid}: declares a config scope but the naming rules do not "
                            "reach it, so its scope was never checked. Rename it or widen "
                            "IS_CONFIG — an unexamined tag is worse than an absent one")
                    continue
                total += 1
                scope = op.get("x-ticvai-config-scope")

                # **The path is evidence and it was never read.** Four F&B operations declared
                # `venue` on `/outlets/{outletId}/...` — `setSectionLayout` beside `setTableLayout`
                # on the same resource with the opposite scope. The check passed because `venue` is
                # unconditionally valid, so the one thing that could have caught it went unexamined.
                #
                # **A path that names an outlet is configuration at that outlet.** If it were not,
                # the outlet in the path is decoration.
                if "{outletId}" in path and scope and scope != "outlet":
                    ERRORS.append(
                        f"{f.stem}.{oid}: declares scope '{scope}' on {path} — a path that names "
                        "an outlet configures at that outlet (CF-138, ADR-0018). Either the scope "
                        "is wrong or the outlet in the path is decoration")

                if not scope:
                    ERRORS.append(f"{f.stem}.{oid}: no x-ticvai-config-scope. Every "
                                  "configuration operation declares its level (ADR-0018)")
                    continue
                tagged += 1
                by_scope[scope] = by_scope.get(scope, 0) + 1

                # `outlet` is valid only in F&B and retail. Those two trade from a place inside
                # a venue — a restaurant has its own menu and a shop its own range — and the
                # client moved their configuration there on 18 August (CF-138). **Everywhere else
                # venue is still the floor**, because the argument that produced that rule was
                # about workstations, and a workstation is a device rather than a business.
                allowed = VALID + (("outlet",) if f.stem in OUTLET_DOMAINS else ())
                if scope not in allowed:
                    if scope == "outlet":
                        ERRORS.append(f"{f.stem}.{oid}: config scope 'outlet' outside F&B and "
                                      "retail. An outlet is where those two trade; no other "
                                      "domain has one (ADR-0018, amended 18 August)")
                    else:
                        ERRORS.append(f"{f.stem}.{oid}: config scope '{scope}' — tenant, region "
                                      "and venue configure, and outlet configures in F&B and "
                                      "retail. Below that you assign a profile, you do not "
                                      "configure one")
                    continue

                caller = op.get("x-ticvai-scope-level")
                if caller in RANK and RANK[scope] < RANK[caller]:
                    ERRORS.append(
                        f"{f.stem}.{oid}: callable at '{caller}' but sets a '{scope}'-wide "
                        "value — a venue manager cannot set a tenant default")

                if MUST_BE_REGION.search(oid) and scope != "region":
                    ERRORS.append(f"{f.stem}.{oid}: must be region. Money, tax and "
                                  "denominations are law, not preference (ADR-0008)")
                if MUST_BE_TENANT.search(oid) and scope != "tenant":
                    ERRORS.append(f"{f.stem}.{oid}: must be tenant. Brand and identity are "
                                  "one app and one directory (ADR-0006)")

    print(f"configuration operations: {total}, tagged {tagged}")
    for k in VALID + ("outlet",):
        if by_scope.get(k):
            print(f"  {k:10}{by_scope[k]}")
    print()
    for w in WARNINGS:
        print(f"  WARN  {w}")
    for e in ERRORS:
        print(f"  FAIL  {e}")
    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
