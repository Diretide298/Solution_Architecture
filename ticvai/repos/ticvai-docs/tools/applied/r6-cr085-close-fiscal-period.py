#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ADAM CR-085 (ticket 28411): what closeFiscalPeriod reads and writes (14 October 2026, CHG-FIN-012).

**The lineage said the close touched only Ledger's tables, and the contract said it asked three other modules.**
`closeFiscalPeriod`'s `noOpenShifts` check was "asked of `orders.listShifts`", its `walletChecks` came from Wallet's
pre-close checks, and its 202 raised `approvals.createApprovalRequest`; the lineage listed none of it, so neither the
plan nor the checks saw the dependencies, and the ticket was scheduled before the Wallet operation it needs.

Chinmay decided on 14 October 2026 (the r6 settlement of CR-085) that each question is asked of its owner by a
declared query (the ADR-0055 amendment of that day). Ledger, Orders, Wallet and Approvals are all in `commerce`, so:

  - `noOpenShifts` asks `shift#unclosedShiftsInPeriod`, `walletChecks` / `walletRollForward` ask
    `wallet#periodCloseChecks`, and the approval asks `approvals#approvalRequirement`, all in process
    (`x-ticvai-read-via`, copied into the lineage as `readVia` by derive-lineage);
  - the request is an `approvals.request`, raised through Approvals' in-process `createApprovalRequest` in the close's
    transaction (ADR-0055 rule 3; within one deployable, so no `x-ticvai-write-via`, as CR-084's deleteGuestAccount);
  - the queries are asked for the period's legal entity, so the close reads `ledger.legal_entity` for its scope path;
  - the owners' tables those queries read in the close's transaction are listed (`orders.pos_shift`, `wallet.balance`,
    `approvals.rule`), covered by the readVia, as CHG-TEN-004 lists `orders.pos_shift` for configureWorkstation, so the
    board sees the migrations the close waits on;
  - `reopenPeriod`, the period's other approved step, takes the same approval route (the class of the CR).

`derive-lineage --apply` never updates an entry it already has, so the change is made here, as
`r6-cr084-delete-guest-account.py` made CHG-GDL-001. A second run reports nothing to do.

    python tools/applied/r6-cr085-close-fiscal-period.py [--apply]
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "handoff", "api-data-lineage.json")

# op: (reads to add, reads to remove, writes to add, writes to remove, fixNote)
LINEAGE = {
    "closeFiscalPeriod": (
        ["ledger.legal_entity", "orders.pos_shift", "wallet.balance", "approvals.rule"], [],
        ["approvals.request"], [],
        "14 October 2026 (ADAM CR-085, CHG-FIN-012): noOpenShifts asks Orders' shift#unclosedShiftsInPeriod, "
        "walletChecks and walletRollForward ask wallet#periodCloseChecks, and the approval asks "
        "approvals#approvalRequirement, all in process (readVia); the 202's approvalRequestId is the approvals.request "
        "raised through Approvals' in-process createApprovalRequest; the owners' tables those queries read in the close's "
        "transaction are orders.pos_shift, wallet.balance and approvals.rule (as CHG-TEN-004 lists orders.pos_shift for "
        "configureWorkstation); ledger.legal_entity gives the scope path the queries are asked for; "
        "recognitionRunComplete is runRecognition's computation run dry (4 October, CHG-FXC-004: the close checks and "
        "the run record)"),
    # The same approval route on the period's other approved step (the class of CR-085).
    "reopenPeriod": (
        ["approvals.rule"], [],
        ["approvals.request"], [],
        "14 October 2026 (ADAM CR-085, CHG-FIN-012): the approval asks approvals#approvalRequirement in process "
        "(readVia, reading approvals.rule in the reopen's transaction); the 202's approvalRequestId is the "
        "approvals.request raised through Approvals' in-process createApprovalRequest (kind periodReopen)"),
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
        print("nothing to do: every entry already carries its CR-085 change")
        return 0
    print("%s: %s" % ("changed" if apply else "would change (pass --apply)", ", ".join(changed)))
    if apply:
        io.open(PATH, "w", encoding="utf-8").write(json.dumps(lin, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
