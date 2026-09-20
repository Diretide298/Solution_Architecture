#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 3b: the nine currency columns their workbook brought, sorted into two kinds.

**ADR-0018 says currency is region-scoped and resolves from the scope walk**, so a table stores
it only where it genuinely differs from its region. Their workbook stores `currency_code` on
nine of the tables we accepted, and `check-package` caught all nine — which is the checker doing
exactly its job on a schema that had never seen our ADR.

Seven of them genuinely differ, and two do not:

    a selector, not a copy      payments.fee_rule, eligibility_rule and method_config carry a
                                currency to say WHICH currency the rule applies to. That is a
                                condition on the row, not a denormalised copy of the region's
                                answer, and dropping it would make the rule unconditional
    money that is really other  inventory.supplier_contract prices in an overseas supplier's own
                                currency and orders.deposit is money actually taken. Their
                                siblings inventory.supplier and orders.payment are already
                                exempt for this reason
    a denominated balance       wallet.balance and wallet.hold. wallet.wallet is already exempt
                                because "a stored-value balance is denominated and the
                                denomination is part of the balance" - a hold on that balance
                                carries the same denomination
    the denormalisation         fnb.price_list and retail.price_list. Our catalogue.price_list
                                does NOT store it: `currency` there is x-ticvai-persisted: false
                                with the ADR quoted on it. An F&B price list is the same kind of
                                object, and storing it would let a price list disagree with its
                                own region

**This is worth reporting to them as a finding rather than a fix.** A generated schema puts a
currency column on anything holding money, because that is what money tables usually look like.
It cannot know that a region owns the answer here.

    python3 tools/applied/schema-merge-phase-3b-currency-20-september.py --apply
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EXEMPT = [
    ("payments.fee_rule",
     "the currency the fee applies TO, not the currency it is in - a selector on the rule"),
    ("payments.eligibility_rule",
     "same: a condition saying which currency this method is allowed for"),
    ("payments.method_config",
     "which currency a method is enabled for, per scope and channel"),
    ("inventory.supplier_contract",
     "an overseas supplier contracts in its own currency; inventory.supplier is already exempt "
     "for this reason"),
    ("orders.deposit",
     "money actually taken, like orders.payment.tender_currency beside it"),
    ("wallet.balance",
     "a stored-value balance is denominated, the same reason wallet.wallet is exempt"),
    ("wallet.hold",
     "a hold on a denominated balance carries the balance's denomination"),
]

# schema name -> contract, for the two that are the denormalisation ADR-0018 forbids
NOT_PERSISTED = [
    ("FnbPriceList", "satellite/fnb.yaml"),
    ("RetailPriceList", "satellite/retail.yaml"),
]

NOTE = (
    '          x-ticvai-persisted: false\n'
    '          description: \'**Resolved from the region, not stored** (ADR-0018). The same rule\n'
    '            catalogue.price_list already follows: a price list in a UAE region is AED and\n'
    \
    '            cannot be anything else, so the column would hold millions of copies of one\n'
    '            region-owned answer and would let a price list disagree with its own region.\n'
    '            **Kept on the wire, removed from the table.** Taken from the backend workbook,\n'
    '            which stored it.\'\n'
)


def main():
    apply = "--apply" in sys.argv[1:]

    # ── the two that must not persist ────────────────────────────────────────
    for schema, rel in NOT_PERSISTED:
        p = os.path.join(ROOT, "contracts", rel)
        s = io.open(p, encoding="utf-8").read()
        m = re.search(r"^    %s:\n" % re.escape(schema), s, re.M)
        if not m:
            print("    !! %s not found in %s" % (schema, rel))
            continue
        nxt = re.search(r"^    [A-Za-z]", s[m.end():], re.M)
        end = m.end() + (nxt.start() if nxt else len(s) - m.end())
        block = s[m.end():end]
        if "x-ticvai-persisted: false" in block:
            print("    %-18s %s already marked" % (schema, rel))
            continue
        blk = re.sub(r"(        currencyCode:\n(?:          [^\n]*\n)+)",
                     lambda mm: mm.group(1) + NOTE, block, count=1)
        if blk == block:
            print("    !! %s has no currencyCode property" % schema)
            continue
        print("    %-18s %s  currencyCode marked not persisted" % (schema, rel))
        if apply:
            io.open(p, "w", encoding="utf-8", newline="\n").write(s[:m.end()] + blk + s[end:])

    # ── the seven that genuinely differ ──────────────────────────────────────
    cp = os.path.join(ROOT, "tools", "check-package.py")
    s = io.open(cp, encoding="utf-8").read()
    if "payments.fee_rule" in s:
        print("    check-package.py already carries the new exemptions")
        if not apply:
            print("\n  nothing written - pass --apply")
        return 0
    anchor = '        "wallet.wallet",\n    }'
    if anchor not in s:
        print("    !! check-package.py: CURRENCY_OK anchor not found")
        return 1
    lines = [
        '        # **Seven more from the backend workbook, 20 September.** Their schema stores a\n'
        '        # currency on anything holding money, which is what a money table usually looks\n'
        '        # like; it cannot know a region owns the answer here. These seven genuinely\n'
        '        # differ. The two that did not - fnb.price_list and retail.price_list - carry\n'
        '        # `x-ticvai-persisted: false` instead, the same as catalogue.price_list.\n'
    ]
    for table, why in EXEMPT:
        lines.append('        "%s",%s# %s\n'
                     % (table, " " * max(1, 34 - len(table)), why))
    print("\n    check-package.py: %d exemption(s) added" % len(EXEMPT))
    for table, why in EXEMPT:
        print("      %-32s %s" % (table, why[:70]))
    if apply:
        io.open(cp, "w", encoding="utf-8", newline="\n").write(
            s.replace(anchor, '        "wallet.wallet",\n' + "".join(lines) + "    }", 1))
    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    print("\n  Re-run derive-schema.py then check-package.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
