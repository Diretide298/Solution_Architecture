#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ADAM CR-084 (ticket 30654): what deleteGuestAccount and exportSubjectData read and write (14 October 2026, CHG-GDL-001..002).

**The lineage said Identity read nothing it needed and wrote a table it cannot.** deleteGuestAccount refuses with 409
while open orders or a live entitlement remain, and its lineage read only `pii.subject`; exportSubjectData read
`access.entitlement` and `orders.sales_order` raw, though Identity is Foundation and reads nothing above it (ADR-0028)
and Access is another deployable (ADR-0055 rule 4). Both listed `platform.dsar_request` as an unconditional write,
though `dsar_request.guest_link_id` is NOT NULL and a guest who never transacted across regions has no link.

Chinmay decided on 14 October 2026 (the r6 settlement of CR-084):

  - both read Identity's own projection `identity.subject_holding` (contract schema `SubjectHolding`), fed by the
    order and entitlement events, instead of the orders and access tables; the owners' rules are declared as
    `orders#openOrdersForSubject` and `access#liveEntitlementsForSubject` and named in `x-ticvai-read-via`;
  - the request is an `approvals.request`, raised through Approvals' in-process `createApprovalRequest`
    (ADR-0055 rule 3: Approvals is in the Tenancy module, in `commerce` with Identity);
  - `platform.dsar_request` is no longer Identity's write: the job calls cross-region `createDsarRequest`
    (serviceAuth) only for a guest linked across cells, and that operation writes it. This takes Identity out of
    XDW-011 (docs/active/cross-deployable-writes.yaml).

`derive-lineage --apply` never updates an entry it already has, so the change is made here, as
`contracts-s12-4-october.py` made CHG-FXC-004. A second run reports nothing to do.

    python tools/applied/r6-cr084-delete-guest-account.py [--apply]
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "handoff", "api-data-lineage.json")

# op: (reads to add, reads to remove, writes to add, writes to remove, fixNote)
LINEAGE = {
    "deleteGuestAccount": (
        ["identity.subject_holding"], [],
        ["approvals.request"], ["platform.dsar_request"],
        "14 October 2026 (ADAM CR-084, CHG-GDL-001): the 409's open orders and live entitlements are read from "
        "Identity's projection identity.subject_holding (read-via orders#openOrdersForSubject and "
        "access#liveEntitlementsForSubject, route projection); requestId is the approvals.request raised through "
        "Approvals' in-process createApprovalRequest; the job tombstones pii.subject for every guest and calls "
        "cross-region createDsarRequest (serviceAuth), which writes platform.dsar_request, only when guestLinkId is set"),
    "exportSubjectData": (
        ["identity.subject_holding"], ["access.entitlement", "orders.sales_order"],
        ["approvals.request"], ["platform.dsar_request"],
        "14 October 2026 (ADAM CR-084, CHG-GDL-002): the orders and entitlements it lists come from Identity's "
        "projection identity.subject_holding, not access.entitlement or orders.sales_order (ADR-0028); requestId is "
        "the approvals.request raised through createApprovalRequest; cross-region createDsarRequest, which writes "
        "platform.dsar_request, is called only when guestLinkId is set"),
}


def main() -> int:
    apply = "--apply" in sys.argv[1:]
    lin = json.load(io.open(PATH, encoding="utf-8"))
    changed = []
    for op, (r_add, r_del, w_add, w_del, why) in LINEAGE.items():
        e = lin.get(op)
        if e is None:
            print("missing from the lineage: %s (run derive-lineage --apply first)" % op)
            return 1
        reads = sorted((set(e.get("reads") or []) | set(r_add)) - set(r_del))
        writes = sorted((set(e.get("writes") or []) | set(w_add)) - set(w_del))
        if reads != e.get("reads") or writes != e.get("writes") or e.get("fixNote") != why:
            e["reads"], e["writes"], e["fixNote"] = reads, writes, why
            changed.append(op)
    if not changed:
        print("nothing to do: both entries already read the projection and raise an approvals request")
        return 0
    print("%s: %s" % ("changed" if apply else "would change (pass --apply)", ", ".join(changed)))
    if apply:
        io.open(PATH, "w", encoding="utf-8").write(json.dumps(lin, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
