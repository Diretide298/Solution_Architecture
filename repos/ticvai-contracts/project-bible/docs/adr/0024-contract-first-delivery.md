# ADR-0024 — The contract is the deliverable, and it is written before anything else

**Status:** Accepted · 17 August 2026, recording a decision already implemented
**Relates to:** every other ADR

---

## Why this is written late

**It is the decision the whole package rests on and it was never stated.** As of 17 August:
**776 operations, 287 tables, 376 screens, 80 state models, 29 events — and no SQL in this
package.**

That is not an accident of scheduling. It is a method, applied for seven weeks, that nobody had
written down — so a new joiner would have found a package with no database and drawn the wrong
conclusion about why.

---

## Decision

**Nothing is built until the contract that describes it exists, is validated, and traces to a
requirement.**

The order is fixed:

**Requirement → contract → schema → screen → flow → build.**

And the constraint that gives it teeth: **an artefact may not reference something that does not
exist.** A screen may not name an operation no contract defines. A flow may not name a screen no
platform declares. A state model may not emit an event with no definition. **Seven validators
enforce this**, and they are the reason the package can be trusted at all.

## Why no SQL in this package

**Corrected 17 August.** This ADR said *zero lines of SQL* and an external audit found six
migrations, 1,822 lines and 39 `CREATE TABLE` statements in the build workspace. **Both are true
and the sentence was wrong**: the design package carries no DDL, and the build repository has
begun generating it.

That is the intended direction — DDL is generated from the schema once the design stops moving —
but **an ADR claiming zero while migrations exist is the kind of statement that makes the whole
document untrustworthy**, and it was written the same day the migrations appeared.

**The rule that still holds: no migration is authored by hand against a moving schema.**

**SQL was written and then deliberately removed once before.** The design was still moving, and a migration
written against a moving schema is a migration rewritten — three times, in our case, before the
removal.

`handoff/storage-design.md` holds the reasoning, and the Excel reference holds 279 tables and
2,025 columns derived from the contracts. **The schema exists; the DDL does not**, and the DDL is
generated when the design stops moving rather than maintained while it does.

**This is the part most likely to be misread as being behind.** It is a deliberate deferral of
the cheapest artefact to produce and the most expensive to keep correct.

## What the method has actually caught

The argument for contract-first is usually theoretical. Here it is not:

**A cart that did not exist.** `createOrder` took a whole basket at once — correct for a till,
and it looked enough like a cart that nine requirements went unnoticed until the vocabulary was
swept.

**A gift card that could be issued and blocked and never activated or redeemed.** Found by
writing the state model, not by testing a screen.

**An inter-entity obligation that could be listed and never settled.** Same.

**`updateWorkOrder` doing six different jobs**, so no audit could say which action caused which
state change.

**None of these would have been found cheaply after the code existed**, and all of them were
found by writing the artefact that describes the thing rather than the thing.

## The cost, stated honestly

**Seven weeks and nothing runs.** Design at roughly 93%, build at zero, and every number in this
package is an assertion until something executes against real infrastructure.

**That is the risk of the method and it is real.** A contract can be internally consistent,
validated by seven checkers, and wrong about the world — and the only thing that finds that is
running it.

`venue-scanner` is the smallest slice that would: 16 screens, fully specified, offline-mandatory,
one flow with eight branches, and it exercises the schema derivation, RLS, the offline bundle,
leases, sync reconciliation and the event catalogue in one pass.

## Consequences

**A defect found in a contract costs a text edit.** The same defect found in code costs a
migration, a client change and a redeploy across cells.

**The client can review scope without reading code.** Every conflict in the register points at a
contract, a screen or an ADR, and 76 of them have been closed by editing text.

**Drift between contract and implementation becomes the main risk once building starts**, which
is why `test-and-acceptance.md` puts contract conformance first — it is generated from the
OpenAPI and catches exactly that class.

**The method must stop being the whole activity.** It has produced a complete design and no
evidence, and the value of the next artefact written is now lower than the value of the first
thing that runs.
