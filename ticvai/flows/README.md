# User flows

**23 written.** Every contract is touched by at least one, and every platform appears in at
least one. That is the coverage measure worth having — the earlier target of sixty was invented.

| | Flow | Actor | Steps | Branches | Criticality |
|---|---|---|---|---|---|
| F01 | Guest buys a ticket online | guest | 8 | **7** | revenue |
| F02 | Guest buys seated tickets | guest | 5 | **5** | revenue |
| F03 | Partner books on credit | partner | 4 | **3** | revenue |
| F04 | Platform admin ships a release | platformAdmin | 4 | **4** | operational |
| F05 | Agent resolves a guest complaint | agent | 3 | **3** | operational |
| F06 | Guest enters the venue | gateOperator | 6 | **8** | revenue |
| F07 | Guest buys at a kiosk | guest | 8 | **7** | revenue |
| F08 | Steward works a shift on the employee app | supervisor | 8 | **7** | operational |
| F09 | Event is cancelled and refunded | venueManager | 5 | **8** | revenue |
| F10 | Partner books, uses and settles | partner | 6 | **7** | revenue |
| F11 | Guest orders food to a lounger | guest | 7 | **7** | convenience |
| F12 | Asset fails and closes a queue | technician | 5 | **7** | safety |
| F13 | Month end closes | financeController | 6 | **7** | financial |
| F14 | A discount needs a manager | cashier | 5 | **6** | financial |
| F15 | A part is needed and ordered | technician | 5 | **7** | operational |
| F16 | A venue opens for the first time | platformAdmin | 7 | **5** | operational |
| F17 | A guest buys merchandise and collects later | guest | 5 | **5** | revenue |
| F18 | A guest plays an arcade game | guest | 4 | **4** | convenience |
| F19 | A membership works in another country | guest | 5 | **6** | revenue |
| F20 | A manager asks a question and gets an answer | venueManager | 3 | **6** | operational |
| F21 | A ride queue fills and a guest is redirected | guest | 5 | **6** | convenience |
| F22 | A tenant rebrands their app | venueManager | 6 | **6** | operational |
| F23 | A contractor gets a badge and uses it | contractor | 5 | **6** | safety |
| | | | **125** | **137** | |

## Why the branches matter more than the steps

`check-flows.py` fails a flow with no branches, because a flow with only a happy path describes
a demo. **Between them these have found one missing screen, two missing contracts, twenty-odd
missing operations and a cart** — and every one of those was invisible to a checker, because a
checker verifies what exists and cannot notice what was never named.

## Coverage

| | |
|---|---|
| Contracts touched | **25 of 25** |
| Platforms appearing | **12 of 12** |
| Operations named in a step | 129 |

**Operations named in a step is deliberately low.** A flow names the operation that carries the
step, not every call the screen makes — a flow listing forty operations is a call graph, and
nobody reviews a call graph.

## What is not written

The remaining journeys are variations rather than new territory: refunds by channel, membership
renewal and freeze, group bookings, stock counts with a variance, DSAR end to end. **Each would
find something**, and none covers a contract or a platform that has nothing.

**A flow is cheap and finds expensive things.** That has held for twenty-three of them.
