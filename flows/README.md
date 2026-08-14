# User flows

**8 written of roughly 60.** Each is validated end to end: every step names a screen that
exists and an operation that exists, and the step sequence is compared against the navigation
graph.

| | Flow | Actor | Steps | Branches | Criticality | Platforms |
|---|---|---|---|---|---|---|
| F01 | Guest buys a ticket online | guest | 8 | **7** | revenue | P01 |
| F02 | Guest buys seated tickets | guest | 5 | **5** | revenue | P01 |
| F03 | Partner books on credit | partner | 4 | **3** | revenue | P10 |
| F04 | Platform admin ships a release | platformAdmin | 4 | **4** | operational | P09 |
| F05 | Agent resolves a guest complaint | agent | 3 | **3** | operational | P12 |
| F06 | Guest enters the venue | gateOperator | 6 | **8** | revenue | P07 |
| F07 | Guest buys at a kiosk | guest | 8 | **7** | revenue | P05 |
| F08 | Steward works a shift on the employee app | supervisor | 8 | **7** | operational | P06 |

## Why the branches matter more than the steps

`check-flows.py` fails a flow with no branches, because a flow with only a happy path
describes a demo. Every flow written so far has found something: F02 was missing a screen
entirely, and F08 found that **a task has no contract** — four of its eight steps name no
operation, and the employee app is fifty screens built around them (CF-71).

## What is not written

Roughly fifty-two. The ones worth doing next, in order:

| | Why |
|---|---|
| **Event cancellation and refund** | Touches order, entitlement, seat, ledger and notification at once. It will expose more than any other single flow |
| **Partner bulk booking to settlement** | Allocation, voucher, usage, reconciliation — the B2B lifecycle nobody has traced |
| **Shop-and-drop collection** | 4.4.7, contracted on 14 August and never walked through |
| **Guest orders food to a lounger** | The one the client described in detail on 14 August |
| **Membership purchase and cross-venue use** | CF-31. Crosses cells, which nothing else does |
| **Stock count with a variance** | Freezes movements, blind count, recount or accept |
| **Asset fails and closes a queue** | Maintenance to queue to guest app, the cascade in ADR-0015 |

**A flow is cheap and finds expensive things.** Eight have produced one missing screen, one
missing contract and four missing operations between them.
