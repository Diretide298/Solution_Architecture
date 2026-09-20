#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The operation that revalues foreign balances never reads a balance.

`runFxRevaluation` says what it does and has said it for a long time:

    "Restates open inter-entity obligations **and any foreign-denominated balance** at the
     closing rate, posting the movement to FX gain and loss."

**Its lineage reads `ledger.inter_entity_obligation` and nothing else that holds a balance.**
An inter-entity obligation is one legal entity owing another; it is not the general ledger. A
venue in Dubai keeping a EUR bank account under an AED entity has a foreign-denominated balance
that this operation claims to restate and cannot see.

    ledger.account.currency          the account's denomination
    ledger.legal_entity.currency     the functional currency it reports in
                                     **different means foreign, and there is no third source**

Nothing else in the package revalues an account. Fourteen operations touch `ledger.fx_rate` and
every one of them converts a single transaction — a payment, a tender, a settlement, a
commission. **Conversion at transaction time and revaluation at close are different acts**: the
first picks a rate for an amount, the second restates an amount that was already converted
because the rate has since moved. Only the second produces an unrealised gain, and only this
operation was ever supposed to do it.

**`FxRatePurpose.revaluation` already exists in the enum.** The contract anticipated this; the
operation just never grew the other half.

## What this changes

    FxRevaluationResult   +accountsRevalued, +byAccount    the obligation half already reported
                                                           `obligationsRevalued` and `byEntity`,
                                                           and the account half reported nothing
    lineage               +ledger.account, +ledger.legal_entity as reads

**`ledger.account` is not added as a write, deliberately.** Ten operations post to the ledger and
none of them lists `ledger.account` in `writes` — `balance` follows from `ledger.posting` in this
package, and only `createAccount` and `updateAccount` write the row. Adding a write here because
a balance moves would make this the one posting operation that claims otherwise. **Deviating from
a convention without saying so is what produced the `fnb.order` duplicate**; if the balance
maintenance is wrong it is wrong for all ten and belongs in one change, not this one.

    python3 tools/applied/fx-revaluation-reads-accounts-20-september.py --apply
"""
import io
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIN = os.path.join(ROOT, "contracts", "spine", "finance.yaml")
LIN = os.path.join(ROOT, "handoff", "api-data-lineage.json")

OLD = """        byEntity:
          type: array
          items:
            type: object
            properties:
              legalEntityId:
                type: string
                format: uuid
              openBalance:
                $ref: ../shared/common.yaml#/components/schemas/Money
              movement:
                $ref: ../shared/common.yaml#/components/schemas/Money
"""

NEW = """        accountsRevalued:
          type: integer
          description: >
            **Foreign-denominated ledger accounts restated, which is the other half of what this
            operation has always claimed to do.** An account is foreign when its `currency`
            differs from the `currency` of the legal entity it belongs to; there is no third
            source for that judgement. Until 20 September this operation read only
            `ledger.inter_entity_obligation` and reported only `obligationsRevalued`, so a EUR
            bank account under an AED entity was never restated and nothing said so.
        byEntity:
          type: array
          items:
            type: object
            properties:
              legalEntityId:
                type: string
                format: uuid
              openBalance:
                $ref: ../shared/common.yaml#/components/schemas/Money
              movement:
                $ref: ../shared/common.yaml#/components/schemas/Money
        byAccount:
          type: array
          description: >
            One row per account restated. **A net movement by entity cannot be explained to an
            auditor** — the question at close is which account moved and at what rate, and an
            entity total is the sum of answers rather than an answer.
          items:
            type: object
            properties:
              accountId:
                type: string
                format: uuid
              accountCode:
                type: string
              currency:
                type: string
                pattern: ^[A-Z]{3}$
              functionalCurrency:
                type: string
                pattern: ^[A-Z]{3}$
              openBalance:
                $ref: ../shared/common.yaml#/components/schemas/Money
              closingRate:
                type: number
                description: >
                  The `revaluation`-purpose rate applied. **Recorded on the result and not
                  looked up again** — a rate row can be superseded, and a close that cannot be
                  re-explained at the rate it actually used is not a close.
              movement:
                $ref: ../shared/common.yaml#/components/schemas/Money
"""

# The description already promised this. It is the reads that were short, so the summary line
# gains the sentence that says which balances, rather than a new claim.
DESC_OLD = """      description: 'Restates open inter-entity obligations and any foreign-denominated balance at the
        closing rate, posting the movement to FX gain and loss.
"""
DESC_NEW = """      description: 'Restates open inter-entity obligations and any foreign-denominated balance at the
        closing rate, posting the movement to FX gain and loss.

        A ledger account is foreign-denominated when its currency differs from the functional currency
        of its legal entity, which is the only test the schema supports and the one used here.

"""

ADD_READS = ["ledger.account", "ledger.legal_entity"]


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(FIN, encoding="utf-8").read()

    if "accountsRevalued" in s:
        print("  finance.yaml already amended")
    else:
        if s.count(OLD) != 1:
            print("  !! byEntity block matched %d times, expected 1" % s.count(OLD))
            return 1
        s = s.replace(OLD, NEW)
        print("    FxRevaluationResult  +accountsRevalued, +byAccount")
        if s.count(DESC_OLD) == 1:
            s = s.replace(DESC_OLD, DESC_NEW)
            print("    runFxRevaluation     description says which balances are foreign")
        else:
            print("    !! description block not matched — left alone")

    try:
        yaml.safe_load(s)
    except Exception as e:
        print("  !! finance.yaml would not parse: %s" % str(e)[:160])
        return 1
    print("    finance.yaml parses")

    # **This entry is hand-mapped, and `derive-lineage.py` only ever adds.** An operation already
    # present is left exactly as it is, by design, so a derivation run will never repair this —
    # the file is the authored input and the edit belongs here.
    L = json.load(io.open(LIN, encoding="utf-8"))
    e = L.get("runFxRevaluation")
    if e is None:
        print("  !! runFxRevaluation not in the lineage")
        return 1
    added = [t for t in ADD_READS if t not in e["reads"]]
    if added:
        e["reads"] = sorted(set(e["reads"]) | set(ADD_READS))
        print("    lineage              +%s" % ", +".join(added))
    else:
        print("    lineage              already reads both")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(FIN, "w", encoding="utf-8", newline="\n").write(s)
    io.open(LIN, "w", encoding="utf-8", newline="\n").write(
        json.dumps(L, indent=1, ensure_ascii=False))
    print("  -> contracts/spine/finance.yaml, handoff/api-data-lineage.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
