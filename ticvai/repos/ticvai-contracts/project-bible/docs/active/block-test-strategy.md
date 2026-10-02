# Test strategy: every block tested end to end at its sprint boundary

> Decided 1 October 2026, after the PM call: two-week sprints, blocks made of complete app-modules, "each block can be completely tested". This is how. Read with the sprint plan (`TICVAI - Sprint Plan.xlsx`) and the build plan (`TICVAI - Build Plan.docx`).

## The units

| Unit | What it is | Tested by | When |
|---|---|---|---|
| **Ticket** | One task in OpenProject (an operation, a table, a screen) | Its maker (unit tests), then a peer tester in the same stack (ADAM enforces tester ≠ maker) | Before it moves to Ready for QA → Closed |
| **App-module** | A business module in one app, e.g. *Ticketing · POS*, with the back end it needs | The module test task, owned by a peer who did not build most of it | In the sprint the module's last ticket closes |
| **Block** | A set of complete app-modules (A, B, C, D), ending on a sprint boundary | The block test: its flows end to end, on the integration environment, then the client's acceptance | The last three working days of the block's final sprint |

## Test levels, and the tool each one uses (all in the starters)

| Level | What it covers | Tool | Where it runs |
|---|---|---|---|
| Unit | Business rules in a handler, a reducer, a component | xUnit (.NET), Jest / Vitest (front ends) | Every commit, CI |
| Contract | Each operation against its OpenAPI contract in `contracts/`; each app's calls against the provider | Pact (consumer-driven), plus the contract schema check | Every commit, CI; a provider change that breaks a consumer fails the build |
| Integration | A service with its real PostgreSQL schema (the migrations, RLS per tenant), its outbox and the broker | xUnit integration tests against a real database from the migrations | Every merge to main, CI |
| Module | The app-module's screens with the real back end: every state the screen YAML lists (loading, empty, error and the named ones), its navigation, its permissions | Component and interaction tests in the app; API tests for the module's operations | Integration environment, when the module completes |
| Flow (end to end) | A journey from `flows/F*.yaml` across apps and services, step by step | Scripted journeys (web and mobile); the flow's steps are the test case | Integration environment, at the block test |
| Offline | POS, scanner and staff app: the flow's `offlineBehaviour`: sell offline, queue, reconcile on reconnect, refuse configuration offline | Network-cut runs of the flow on a device | Integration environment, at the module test and the block test |
| Load | Purchase and admission paths (99.99% target), on-sale waiting room, the event relay | k6 | Pre-production, once per block that adds a purchase or admission path |

## Done, for each unit

**A ticket is done when:**
- its unit tests pass and cover the rules its task lists;
- its contract test passes (operations) or its screen's states are each reachable (screens);
- a peer in the same stack reviewed and tested it;
- it is merged and green on CI.

**An app-module is done when:**
- every ticket in it is done;
- the module test passed on the integration environment: every screen state, every navigation link, every permission (an allowed and a refused user), every operation's error responses;
- for an offline app, the module's offline behaviour passed with the network cut;
- no open defect of severity 1 or 2 is left on it.

**A block is done when:**
- every app-module in it is done;
- **every flow the block claims passes end to end.** A block claims a flow when all the flow's platforms, screens and operations are built in this block or an earlier one. A flow that needs a later block is listed as "partly testable" with the steps that can run;
- load tests pass where the block adds a purchase or admission path;
- the client has run the block's acceptance session on the integration environment and signed off, or listed what is open;
- the release that carries it is tagged.

## How the testing lands in the sprints

1. **Inside each ticket.** The task's points include its unit and contract tests; there is no separate ticket for them. The front-end [FE] tickets keep their wire, build and test sub-tasks.
2. **One module test task per app-module.** It is about 10% of the module's points (at least 2), assigned to a peer in the module's stack who is not its main builder, and scheduled right after the module's last ticket. It is a real ticket in OpenProject, in the same sprint.
3. **One block test per block.** It covers the block's claimed flows, the offline runs and the load run. It is assigned to a pair (one back end, one front end, rotating per block) and led by Chinmay, in the last three working days of the block's final sprint.
4. **No new feature work starts in those three days.** Developers not on the block test fix the defects it finds, or take ready work from the next block that does not touch the block under test.
5. **Client acceptance.** The block is demonstrated in the sprint review at the block's end. The client tests on the integration environment in the following week, while the next sprint runs.

## The same-numbers test (2 October)

Decided by Chinmay on 2 October (DEC-559; CHG-DOC-022), as the prevention CHG-FIN-006 lacked: the till, the
back-office reports and Analytics are windows onto one reporting area, so they must show the same numbers.
**A frontend comparison test** reads the same figure (takings, gross sales excluding VAT, refunds) for one scope,
one period and one as-of time on the till (POS-008), the back office (BO-058, BO-059) and Analytics (P16), and
fails on any difference. It is a real ticket in the block that first ships all three, run in the module test and
again in the block test.

## Environments

| Environment | Used for | Data |
|---|---|---|
| Developer machine (starter) | Unit, contract, integration tests | Throw-away database from the migrations |
| CI | Every commit and merge | The same, per build |
| Integration (the pre-production tier in the HLD, about $1,535 a month) | Module tests, block tests, client acceptance | Two seeded demo tenants (a theme park and a venue with F&B), rebuilt at each release tag |
| Pre-production at production size | Load tests | Generated volume, never real guest data |

## Defects

- **Severity 1:** the flow cannot complete. **Severity 2:** it completes wrongly. **Severity 3:** a workaround exists. **Severity 4:** cosmetic.
- Severity 1 and 2 block the module or the block from being done. Severity 3 and 4 go into the next sprint.
- Each defect is a bug ticket on the module's epic in OpenProject, linked to the ticket it was found on. A defect that turns out to be a spec gap becomes a change request through ADAM.

## What the sprint plan must show

- The module test task for every app-module, in the sprint it lands.
- The block test window, the last three working days of each block's final sprint.
- For each block, the flows it claims (fully testable) and the flows that are only partly testable until a later block.
- The same-numbers comparison test, in the block that first ships the till, back-office and Analytics figures.
