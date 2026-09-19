#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Twelve actions that belong on a screen which already exists.

**Not a gap in the design — a gap in the wiring.** Each of these operates on a noun a
screen already shows, on a screen that already receives the identifier the operation
needs, for an audience that already uses that platform. `ANL-039` previews and validates a
report execution and could not cancel one; `BO-077` shows FX rates and variances and could
not pull rates from the provider; `EMP-059` is *Table Order, Bill & Payment* and had no way
for the party to ask for the bill.

## What is deliberately not here

**Twenty-one others look like the same problem and are not.** `suspendWallet`, `closeWallet`,
`updateAccessPolicy`, `updateReportSchedule` and eighteen more have no screen that both
receives their identifier and makes sense of the verb. Matching on the parameter alone
produces `cancelSubscription` on *Integrations*, `redeemWaitingGuest` on *Journal Entries*
and `reinstateEntitlement` on *Receipt & Reprint* — plausible, wrong, and exactly the
title-matching failure this run has been about. Those need a screen or a decision, and are
listed in the run report rather than guessed at here.

**`cloneProduct` and `evaluateAccess` are left out for the same reason.** `cloneProduct`
matched a sell screen rather than the product directory, and `evaluateAccess` — "decide,
now, and say why" — matched a footfall report. Both need a person.

Every target was checked for three things before it went in the list below: it is not a
`source.sameAs` twin, its platform matches the operation's audience, and its `entryState`
already declares the parameters the operation's path requires.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# screen id -> (operationId, contract, purpose, trigger)
WIRING = {
    "ANL-039": [("cancelReportExecution", "reporting",
                 "Stop a run that is going to be wrong anyway", "onAction")],
    "BO-077": [("ingestFxRates", "finance",
                "Pull today's rates from the configured provider", "onAction")],
    "BO-076": [("validateRecognitionSchedules", "finance",
                "Find product kinds claimed by more than one schedule", "onAction")],
    "BO-097": [("captureStoredValue", "orders",
                "Take some or all of the held balance", "onAction")],
    "BO-1125": [("redeemGiftCard", "wallet", "Spend against a card", "onAction")],
    "BO-396": [("createGame", "games", "Register a game on this attraction", "onAction")],
    "BO-1066": [("simulateAccessPolicy", "identity",
                 "What this policy would decide, before it decides anything", "onAction")],
    "WEB-010": [("createCart", "orders", "Start a cart", "onLoad")],
    "EMP-058": [("getTableVisit", "fnb", "Read a visit with all its orders", "onAction")],
    "EMP-059": [("requestBill", "fnb", "The party asked to pay", "onAction")],
    "EMP-034": [("splitOrder", "orders",
                 "Break one order into independent orders", "onAction")],
    "POS-002": [("transferGameCard", "games",
                 "Move balances to another card", "onAction")],
}

# `createCart` is the only read-shaped one here and it still invalidates nothing; the rest
# change something a sibling on the same screen displays.
INVALIDATES = {
    "cancelReportExecution": ["listReportExecutions"],
    "ingestFxRates": ["listFxRates"],
    "captureStoredValue": ["getStoredValueAuthorisation"],
    "redeemGiftCard": ["getGiftCard"],
    "createGame": ["listGames"],
    "splitOrder": ["getOrder"],
    "transferGameCard": ["getGameCard"],
    "requestBill": ["getTableVisit"],
}


def main():
    apply = "--apply" in sys.argv
    added = skipped = 0
    for f in sorted(os.listdir(os.path.join(ROOT, "screens"))):
        if not (f.startswith("P") and f.endswith(".yaml")):
            continue
        path = os.path.join(ROOT, "screens", f)
        d = yaml.safe_load(io.open(path, encoding="utf-8")) or {}
        changed = False
        for s in (d.get("screens") or []):
            if s["id"] not in WIRING:
                continue
            # **Never write a twin.** Tripped three times in this run already.
            if (s.get("source") or {}).get("sameAs"):
                print("  %-9s is a twin of %s — edit the master"
                      % (s["id"], s["source"]["sameAs"]))
                skipped += 1
                continue
            have = {a.get("operationId") for a in (s.get("apis") or [])}
            new = []
            for oid, contract, purpose, trigger in WIRING[s["id"]]:
                if oid in have:
                    continue
                entry = {"operationId": oid, "contract": contract, "purpose": purpose,
                         "trigger": trigger,
                         "provenance": "wiring gap, 19 September 2026 — the screen showed the "
                                       "noun and could not act on it"}
                if INVALIDATES.get(oid):
                    entry["invalidates"] = INVALIDATES[oid]
                new.append(entry)
            if new:
                s.setdefault("apis", []).extend(new)
                added += len(new)
                changed = True
                print("  %-9s %-38s + %s" % (s["id"], s["name"][:38],
                                             ", ".join(n["operationId"] for n in new)))
        if changed and apply:
            io.open(path, "w", encoding="utf-8", newline="\n").write(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
            print("  -> screens/%s" % f)

    print("\n%d reference(s) added, %d skipped" % (added, skipped))
    if not apply:
        print("\n  nothing written — pass --apply")


if __name__ == "__main__":
    main()
