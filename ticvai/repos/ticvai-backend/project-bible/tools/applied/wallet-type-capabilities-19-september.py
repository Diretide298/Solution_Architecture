#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make `WalletType` say what a wallet may do, and `CreditType` cover the client's library.

## The thirteen client wallet types were never thirteen kinds

*Wallet Configuration Backend Structure*, board 1.2, says administrators may create types
"**such as**" — then lists Guest, Registered Customer, Family, Parent, Child, Corporate,
School, Employee, Membership, Event, Resort, Cashless Venue and Closed-Loop. Read as an
enum that is thirteen kinds and five of them do not fit `ownerKind`. Read as presets it
is four dimensions we already have:

    WalletType = ownerKind x allowedCreditTypeIds x scopePath x channels

    Membership, Closed-Loop   differ by CREDIT TYPE
    Event, Resort, Cashless   differ by SCOPE
    the other eight          differ by OWNER

**So no enum values are added.** Putting Resort into `ownerKind` would encode a scope
choice as identity, which is what stops a configurable model being configurable.

## What is genuinely missing

Board 1.2 configures per type: stored-value, transfer, top-up and refund capability; gift
card, voucher, membership-credit and wearable support; and online, POS, mobile-app and
API usage. **None of that is on `WalletType`.** The channel half exists, but on
`WalletFundingRules.allowedChannels` and `WalletChannelRules.allowedChannels` — two other
objects — so the capability and the thing it describes live apart.

That gap is also the answer to "how do three callers share one operation": they all call
`topUpWallet`, and the wallet type says whether this channel may. A service boundary was
never the right instrument.

## CreditType

The client's balance-type library is Gift Card, Membership, Loyalty, Ride, Attraction,
**Redemption Ticket**, **F&B / Meal**, **Retail**, **Parking**, **Event**, Promotional,
Refund and Custom. Our enum has ten of thirteen. The five missing matter: redemption
credits are earned by gameplay score and spent only on prizes — 2,450 of them on a
customer's own balance view — and `loyalty` is the wrong home, because loyalty points
accrue on completed orders.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import re
import sys

CONTRACT = "contracts/satellite/wallet.yaml"

# Board 1.2, "Each wallet type can configure". Defaults are false because a capability
# nobody enabled should not be silently on — the restriction screens in the same pack
# ("Disable top-ups", "Disable online payments") only make sense against an explicit flag.
CAPABILITIES = """        storedValueCapability:
          type: boolean
          default: true
          description: 'Board 1.2. Whether this wallet holds a balance at all. A pure
            entitlement wallet — passes and vouchers, no money — does not.

            '
        topUpCapability:
          type: boolean
          default: false
        transferCapability:
          type: boolean
          default: false
        refundCapability:
          type: boolean
          default: false
        giftCardSupport:
          type: boolean
          default: false
        voucherSupport:
          type: boolean
          default: false
        membershipCreditSupport:
          type: boolean
          default: false
        wearableSupport:
          type: boolean
          default: false
        usageChannels:
          type: array
          description: '**Where this wallet may be used, declared on the type itself.**
            Board 1.2 configures online, POS, mobile-app and API usage per wallet type,
            and this is what lets one `topUpWallet` serve every caller: the operation is
            shared and the type says which channel may reach it. `WalletChannelRules`
            still governs the per-credential detail — PIN thresholds, offline floor
            limits — and this governs whether the channel is open at all.

            '
          items:
            type: string
            enum:
            - online
            - pos
            - mobileApp
            - api
            - kiosk
            - reader
        presetName:
          type: string
          description: '**The client''s own name for this composition** — "Resort Wallet",
            "Cashless Venue Wallet", "Closed-Loop Wallet". Board 1.2 lists thirteen such
            names as examples, not as kinds: they are combinations of `ownerKind`,
            `allowedCreditTypeIds` and `scopePath`. Naming the preset keeps the client''s
            vocabulary without hard-coding it into an enum.

            '
"""

NEW_CREDIT_CATEGORIES = ["redemption", "fnb", "retail", "parking", "event"]


def main():
    apply = "--apply" in sys.argv
    t = io.open(CONTRACT, encoding="utf-8").read()
    before = t
    notes = []

    # --- WalletType capabilities, inserted before `holderMayDifferFromOwner` ---
    if "topUpCapability" in t:
        notes.append("WalletType already has the capability flags")
    else:
        anchor = "        holderMayDifferFromOwner:"
        i = t.index("    WalletType:")
        j = t.index(anchor, i)
        t = t[:j] + CAPABILITIES + t[j:]
        notes.append("WalletType += 9 capability/channel field(s) + presetName")

    # --- CreditType.category enum ---
    i = t.index("    CreditType:")
    seg = t[i:i + 2600]
    m = re.search(r"(        category:\n          type: string\n          enum:\n)((?:          - \w+\n)+)",
                  seg)
    if not m:
        raise SystemExit("could not find CreditType.category enum")
    have = re.findall(r"- (\w+)", m.group(2))
    add = [c for c in NEW_CREDIT_CATEGORIES if c not in have]
    if not add:
        notes.append("CreditType.category already complete")
    else:
        # `other` stays last: it is the escape hatch, and a reader scanning the list
        # should not have to step over it to reach a real category.
        body = [c for c in have if c != "other"] + add + (["other"] if "other" in have else [])
        new = m.group(1) + "".join("          - %s\n" % c for c in body)
        t = t[:i] + seg.replace(m.group(0), new, 1) + t[i + 2600:]
        notes.append("CreditType.category += %s (now %d)" % (", ".join(add), len(body)))

    for n in notes:
        print("  %s" % n)
    if t == before:
        print("\nnothing to do")
        return
    if not apply:
        print("\n  nothing written — pass --apply")
        return
    io.open(CONTRACT, "w", encoding="utf-8", newline="\n").write(t)
    print("  -> %s" % CONTRACT)


if __name__ == "__main__":
    main()
