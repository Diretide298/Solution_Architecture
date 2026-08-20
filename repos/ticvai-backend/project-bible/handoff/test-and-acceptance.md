# Test and acceptance

**40 requirements, and the artefact audit said we had permission vectors and nothing else.**
That was true. It was also the wrong place to start, because **the test cases are already
written — they are the refusals, the guards and the branches.**

## What is derivable today

| Source | Cases | What each asserts |
|---|---|---|
| Refusal rules | **194** | The operation refuses, with that status, for that reason (`validation-rules.md`) |
| State transitions | **327** | The legal move succeeds; **and every illegal move is refused** |
| Flow branches | **93** | The unhappy path behaves as the flow says. The highest-value cases in the set |
| Screen states | **1456** | Loading, empty, error and offline render, across 364 specified screens |
| Events | **25** | Published once per state change, and idempotent for each consumer |
| Operations | **707** | Contract conformance — request and response match the schema |

**The illegal transitions are the ones worth writing first.** A state model with 327 legal moves
implies far more illegal ones, and *can a completed work order be started again* is the
question a test answers and a reviewer does not.

## The four layers

**Contract conformance.** Generated from the OpenAPI. Every operation, request and response
shape. Cheap, and it catches the class of defect this project has produced most — a contract
and an implementation drifting.

**State machine.** For each model, assert every legal transition and **assert the refusal of
every illegal one**. Generated from `states/`.

**Flow acceptance.** Each flow, each branch. **Written by hand and worth it** — twelve flows have
found one missing screen, one missing contract and sixteen missing operations between them, and
a test that runs them keeps finding things.

**Permission matrix.** Every operation against every role: permitted, refused, or out of scope.
Generated from `x-ticvai-permission` and the role definitions. **The one that catches a scope
widening**, which is the defect nobody sees in review.

## Acceptance criteria the client signs

Different from the above, and currently absent. **A capability is accepted when its flow
completes and its branches behave**, not when its operations return 200.

The twelve flows are the natural unit: each names an actor, a trigger, an outcome and the
failures. **A flow is a paragraph a client can read and agree to**; a list of 737 operations is
not.

## What is missing

| | |
|---|---|
| **The generators** | Everything above is derivable and nothing derives it. Four generators, and they are small |
| **Test data** | A seeded venue with a catalogue, a rota, an open shift. **Needed before any of this runs**, and it is the same seeding job as the report register |
| **48 flows unwritten** | The flow layer covers twelve of sixty |
| **Performance targets** | CF — no latency budget stated, so there is nothing to assert |
