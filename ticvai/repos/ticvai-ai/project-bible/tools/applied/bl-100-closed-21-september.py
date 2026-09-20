#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Close BL-100 against the dunning model and ADR-0048.

Written to a file, not a shell — backticks in `bash -c` ate two closure notes on 20 September.
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "handoff", "contract-backlog.json")

CLOSED_BY = (
    "**Closed 21 September.** The entry named eight capabilities and five had arrived without it "
    "noticing — auto-renewal, grace periods, billing cycles, downgrade and mandates. **Three were "
    "genuinely absent from `contracts/` entirely**: dunning, a retry schedule and a billing "
    "statement. `dunning` appeared only inside a state model, which is CF-49's exact shape — a "
    "capability present in states and in no contract.\n\n"
    "**The boundary is decided and recorded: [ADR-0048](../adr/0048-guest-recurring-billing-is-"
    "commerce.md).** The entry's own argument was right — `subscription` is the Control Plane, it "
    "runs outside every cell because it provisions cells, and it bills tenants — and "
    "`subscription.yaml` had drifted across it, carrying seventeen membership operations including "
    "`setRenewalAutoMembership` and `listMembershipRenewalRetention`. **All seventeen are "
    "provisional**, read off a workshop pack and never specified: nobody decided this, a filename "
    "did. **The residency row is the one that is not negotiable** — a guest's payment history in a "
    "control-plane table is personal data outside its jurisdiction, which is what the cell model "
    "exists to prevent.\n\n"
    "**Built where the rest of the billing is.** The policy in `payments.yaml` — `DunningPolicy`, "
    "`DunningCase`, `DeclineClass`, and the queue a venue actually works from, ordered by attempts "
    "remaining rather than by age because the ones about to exhaust are the ones somebody can "
    "still save by calling the guest. The record in `orders.yaml` — `BillingStatement`, computed "
    "rather than stored, because a statement assembled at read time cannot disagree with the "
    "ledger it describes.\n\n"
    "**Dunning retry and gateway retry are different axes and must never share a counter.** "
    "`setPaymentFailoverPolicy` governs retry inside one attempt — seconds, a different provider, "
    "and a decline is final there. Dunning governs retry across days: a fresh authorisation on a "
    "card that may since have been replaced. **Both are called retry, and treating one as the "
    "other is how a guest is charged twice.**\n\n"
    "**A hard decline is never scheduled.** A closed account, a stolen card or a do-not-honour put "
    "on a timetable is how a merchant ID gets flagged by the scheme, and the venue finds out when "
    "its acquirer calls. `retryableDeclineClasses` defaults to `soft` alone, and `unknown` is "
    "treated as hard because guessing soft optimises for one more attempt and risks the thing that "
    "cannot be undone.\n\n"
    "**The attempt spacing is the part that matters, so it is a field rather than a constant.** "
    "`[0, 3, 7, 14]` straddles a payday; retrying at the same hour each day hits the same daily "
    "limit on the same card and tells the venue nothing it did not already know.\n\n"
    "**Dunning cannot revoke admission.** `terminalAction` stops at `suspendBilling` and "
    "`cancelRenewal`; `graceDays` already governs how long a pass keeps working. The case this "
    "protects is concrete — **a guest at a gate on a family day out, refused because a card "
    "expired and a retry ran at 3am.** Ending somebody's access stays a staff decision with a name "
    "attached.\n\n"
    "**A statement is not a tax invoice**, and `isTaxInvoice` is false and read-only rather than "
    "absent. UAE e-invoicing is Peppol five-corner with the FTA as the fifth, PINT AE XML and 51 "
    "mandatory fields; **CF-133 is open and AED 50m+ businesses must appoint an accredited service "
    "provider by 30 October 2026.** A statement implying otherwise would be wrong in the one "
    "direction with a regulator at the end of it.\n\n"
    "**Two things deliberately not done.** The seventeen provisional drafts are **not moved** — "
    "they are unreviewed workshop text awaiting a CF-171 session, and relocating operations nobody "
    "has agreed would assert a home rather than record one; ADR-0048 is the instruction to the "
    "session that reads them. And **the stored-card and PCI scope this entry warned about is still "
    "not re-examined** — it arrived with the mandate model, it is a security review rather than a "
    "contract question, and it is named here rather than quietly closed with the rest."
)


def main():
    apply = "--apply" in sys.argv[1:]
    B = json.load(io.open(PATH, encoding="utf-8"))
    e = next(x for x in B["entries"] if x["id"] == "BL-100")
    if e.get("closedBy") == CLOSED_BY and e.get("status") == "done":
        print("  already applied")
        return 0
    e["status"] = "done"
    e["lane"] = "settled"
    e["closed"] = "2026-09-21"
    e["closedBy"] = CLOSED_BY
    print("    BL-100  -> done · settled · 2026-09-21 · %d chars" % len(CLOSED_BY))
    o = sum(1 for x in B["entries"] if x.get("status") != "done")
    print("    open backlog entries after this: %d" % o)
    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(PATH, "w", encoding="utf-8", newline="\n").write(
        json.dumps(B, indent=1, ensure_ascii=False))
    print("  -> handoff/contract-backlog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
