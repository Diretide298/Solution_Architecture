# User flows

**A flow is one job a person came to do, traced across screens.**

    _schema.yaml        the meta-schema
    F01…F05.yaml        one file per flow
    ../tools/check-flows.py

## Why flows are separate from screens

A screen is owned by whoever builds it. A flow crosses screens, often crosses apps, and is
owned by nobody unless it is written down.

The failures that cost most are almost never inside a screen. They are in the joins — a hold
that expires while the guest is on the payment page, a payment taken with no response
received, a plan applied against cell state that has since moved. Those live between screens,
so they are recorded between screens.

## The branch rule

**Every flow declares its unhappy paths, and `branches` cannot be empty.** A flow with only a
happy path describes a demo, not a product.

The five flows here carry 21 branches between them. Several are the reason a design decision
exists at all — the payment-taken-no-response branch in F01 is why `createOrder` runs before
`createPayment`, and why the screen offers inquiry rather than retry.

## What the check catches

| | |
|---|---|
| Screen does not exist | |
| Operation does not exist | |
| **A step calls an operation the screen does not declare** | The useful one |
| Branch at a step that does not exist | |
| No branches at all | |

That third check found nine mismatches on first run — every one a case of the **screens being
behind the flows**. The P09 screens were generated before `platform-ops` existed, so they
carried "no contract" against operations that now do exist. The flow was right and the screen
inventory was stale, which is exactly the drift this comparison exists to surface.

## Coverage

| Flow | Actor | Steps | Branches | Criticality |
|---|---|---|---|---|
| **F01** Guest buys a ticket online | guest | 8 | 7 | revenue |
| **F02** Guest buys seated tickets | guest | 4 | 4 | revenue |
| **F03** Partner books on credit | partner | 4 | 3 | revenue |
| **F04** Platform admin ships a release | platformAdmin | 4 | 4 | operational |
| **F05** Agent resolves a guest complaint | agent | 3 | 3 | operational |

**Five of roughly sixty.** These are the five whose screens are specified. The rest —
gate admission, POS sale, offline recovery, shift close-out, stock count, work order — cross
platforms whose screens have no definitions yet, so a flow written now could not be checked
against anything.

Writing an unverifiable flow is how a flow becomes fiction. The remaining fifty-five wait for
their screens.
