#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close BL-110, and record that most of it had already been built.

Written to a file rather than a shell — backticks in `bash -c` ate two closure notes yesterday.
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "handoff", "contract-backlog.json")

CLOSED_BY = (
    "**Closed 21 September, and most of it was already built when the walk measured it.**\n\n"
    "The 20 September walk reduced 48 requirements to *\"one schema change and one small new "
    "rule\"*. **Both were done.** The schema change is `AccessPolicy` and `AccessCondition` — "
    "twenty-six attributes covering 3.3.2 through 3.3.21, deny-wins combining, versions, "
    "templates, `simulateAccessPolicy` and a signed offline `AccessPolicyBundle` — landed in "
    "*\"Phase 2: the forty-two identity rows were one gap, and it was ABAC\"*. The new rule is "
    "`SegregationRule` and `setSegregationRules`, **built by BL-147**, checked at grant time with "
    "`allowWithCompensatingControl` for the small venue that cannot separate duties.\n\n"
    "**This is the fifth stale measurement in two days and this one was mine.** I searched "
    "`contracts/` for `segregat`, piped it through `head -10`, saw `approvals`, `access`, "
    "`workforce` and `permissions`, and concluded `identity` had none. **The identity rows were "
    "lines 11 to 14 of a list truncated to 10.** Same failure as concluding no operation retires "
    "a device because no operationId contains *retire* — a conclusion drawn from an absence that "
    "was an artefact of how I looked.\n\n"
    "**Three real holes were found and closed, all smaller than what the entry carried:**\n\n"
    "**`setSegregationRules` was a PUT with no GET.** `P09 ADM-340 Segregation of Duties Policy "
    "Manager` is a screen that manages rules and had nothing to load them with, and nobody could "
    "audit a tenant's controls without database access. `listSegregationRules` added — **rules are "
    "evidence as much as configuration.**\n\n"
    "**Nothing listed who already violates a rule.** BL-147 was right that grant-time beats "
    "use-time — *discovering the conflict when somebody exercises it means the conflict already "
    "existed* — but **a rule added today had said nothing about the grants made yesterday**, so a "
    "venue held the control and not the finding. `listSegregationViolations` is deliberately a "
    "report rather than an action: revoking on rule creation strands a venue mid-shift, doing "
    "nothing leaves real exposure unreported, and a person decides between them. Compensating-"
    "control cases are flagged rather than filtered, because a queue that hides what has been "
    "excused stops measuring the thing it exists to measure.\n\n"
    "**Scope was not part of the conflict, and `scopePath` is not it** — that one is the partition "
    "key and says where the rule row lives (ADR-0005), not where the conflict applies. "
    "`ACCREDITATION_ISSUE` at Yas Island beside `ACCREDITATION_MANAGE` at Warner Bros read as a "
    "toxic pair when it is two jobs at two sites, and **the first thing a venue does with a "
    "control that cries wolf is switch it off.** `scopeSensitive` defaults true and walks "
    "`scopePath` prefixes the way `resolvePermissions` already does.\n\n"
    "**`approvals.yaml` described a model that was never built.** Its "
    "`listApprovalControlPolicies` said *\"`identity.setSegregationRules` says which **roles** one "
    "person may not hold at once\"*; the operation has always been over permission pairs. "
    "Corrected — and a rule over roles would be the weaker control anyway, defeated by adding "
    "`ORDER_REFUND_APPROVE` to a third role while still reporting compliant.\n\n"
    "**Not rebuilt: the exception path.** `allowWithCompensatingControl` already covers it and "
    "covers it better than a separate object would.\n\n"
    "**Still open and not closed by this: one sentence from the client.** 3.3.27 asks for "
    "*\"real-time authorization\"*. Read literally it contradicts resolving permissions once at "
    "login and would put a policy engine on the hot path of all 2,056 operations; read as *\"a "
    "revoked permission takes effect promptly\"* it is session invalidation, which `forceLogout` "
    "already answers. **That is a question rather than a blocker** — everything else in 3.3 is "
    "built either way, which is why this closes."
)


def main():
    apply = "--apply" in sys.argv[1:]
    B = json.load(io.open(PATH, encoding="utf-8"))
    e = next(x for x in B["entries"] if x["id"] == "BL-110")
    if e.get("closedBy") == CLOSED_BY and e.get("status") == "done":
        print("  already applied")
        return 0
    e["status"] = "done"
    e["lane"] = "settled"
    e["closed"] = "2026-09-21"
    e["closedBy"] = CLOSED_BY
    print("    BL-110  -> done · settled · 2026-09-21 · %d chars" % len(CLOSED_BY))
    o = sum(1 for x in B["entries"] if x.get("status") != "done")
    print("    open backlog entries after this: %d" % o)
    for x in B["entries"]:
        if x.get("status") != "done":
            print("      %s  %-9s %s" % (x["id"], x.get("lane"), (x.get("what") or "")[:70]))
    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(PATH, "w", encoding="utf-8", newline="\n").write(
        json.dumps(B, indent=1, ensure_ascii=False))
    print("  -> handoff/contract-backlog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
