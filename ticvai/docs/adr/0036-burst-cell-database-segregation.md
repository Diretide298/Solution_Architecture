# ADR-0036: The burst cell shares one Postgres instance with a database per service

**Status:** Superseded by [ADR-0038](0038-cell-is-a-region-database-per-tenant.md), on the trigger
this ADR named itself: CF-161 resolved, so the exception is restated against the new decision rather
than inherited from this one. A burst cell is one tenant, therefore one database.
**Date:** 31 August 2026
**Related:** [ADR-0005](0005-venue-isolation-by-partitioning-not-separate-databases.md) · [ADR-0028](0028-service-decomposition.md) · [ADR-0031](0031-contention-and-locking.md) · [ADR-0032](0032-load-shedding-and-pooling.md) · [ADR-0035](0035-burst-environments.md) · **CF-161**

---

## Context

**`deploy/c-flash-sale.yml` ran one Postgres instance holding one database with 26 schemas.** That
is the shared-schema model from ADR-0005, and it contradicts the position Dinesh put to the client
on 24 August: **databases segregated from day one.**

**It was not written as an exception. It was written without noticing**, which is worse — a silent
deviation reads as a decision nobody remembers making.

**Dinesh's reasoning is sound and it is specifically about time**: splitting a centralised database
after two or three years in production is significantly harder than starting isolated and merging
later. **The asymmetry is real and it is why CF-161 is a serious question.**

---

## Decision

**In a burst cell: one Postgres instance, one database per service, no cross-database joins.**

**In the permanent platform: CF-161 decides, and this ADR does not touch it.**

### Why the exception holds

**The reasoning behind day-one segregation does not reach this environment**, because it is entirely
about what happens after two or three years and **a burst cell lives for one on-sale.**

**Single tenant. Single event. Destroyed after reconciliation** (ADR-0035). There is no *"two years
later"* to protect against — the environment is gone before the first migration would have been
needed.

### What segregation would cost here, specifically

**Three connection pools instead of one**, in an environment where the pooler is already the thing
standing between 640 client connections and a primary that will not want them.

**Cross-service reads over the network on the hold path.** `acquireInventoryHold` reads
`catalogue.performance` and writes `catalogue.inventory_hold`; a hold that crosses a database
boundary adds a round trip **inside the lock**, and ADR-0031 already establishes that the lease
duration is the ceiling. **A 6 ms lease becoming 8 ms drops the per-row ceiling by a quarter.**

**Slower provisioning**, in an environment whose entire purpose is standing up before a sale opens.

### One instance is not one database

**Dinesh confirmed on 24 August that multiple databases on a single server instance satisfies
segregation.** So this decision is `POSTGRES_DB` per service on one `postgres-hot`, not three
servers — **which is why the cost of the exception is smaller than it looks, and why taking it is a
judgement rather than a shortcut.**

---

## Consequences

**🔴 This does not resolve CF-161. It carves a bounded exception out of it.**

**CF-161 goes to the internal session with Dinesh on its own terms**, and that session must not
proceed with the MoM's answer assumed — the conflict between ADR-0028 and a client-facing
recommendation is the thing to settle, and **a burst-cell carve-out settles none of it.**

**ADR-0028 still reads Accepted while contradicting what the client was told.** That remains open.

**The scope of this exception is named and narrow**: `CellKind: burst` only. A `shared`, `dedicated`
or `onPremise` cell gets whatever CF-161 decides, and **an exception that is not named is an
exception that spreads.**

---

## When this exception is reopened

**A bounded exception with no condition for reopening becomes permanent by inertia**, so the
triggers are named rather than left to somebody noticing.

**A fourth service enters the burst cell.** Three databases on one instance is a judgement about a
small, fixed set. **Four is the point at which "one instance, a database each" starts being an
argument for the general case** rather than an exception to it, and the reasoning here does not
stretch that far.

**A burst environment lives longer than 24 hours.** The whole justification is lifetime — *there is
no two years later to protect against*. **An environment that persists across days has one**, and
the exception should be re-argued rather than assumed.

**CF-161 resolves toward full per-service segregation.** The exception survives that resolution —
its reasoning is independent — **but it must be restated against the new decision rather than
inherited from this one.** An exception carved out of a question that has since been answered is an
exception nobody can defend from the document that created it.

**A burst environment is reused for a second on-sale.** Reuse breaks single-event, which is half of
the justification, and **reuse is the likely optimisation somebody proposes to save provisioning
time.**

---

## Alternatives considered

**Full segregation in the burst cell too.** Rejected on the cost above — three pools, a network hop
inside the lock, slower standup — **in the one environment where all three matter most.**

**Say nothing and leave the compose file as it was.** Rejected because that is what produced this
ADR: a silent deviation that reads as a decision nobody remembers making, in a file somebody would
eventually cite as precedent.

**Wait for CF-161.** Rejected because the burst environment can be built and benchmarked now, and
**the answer for a fifty-second environment does not depend on the answer for a permanent one.**
