# ADR-0016 — Read and write paths are separated, and routing is declared per operation

**Status:** Accepted
**Date:** 14 August 2026
**Supersedes:** nothing. **Amends:** ADR-0005 (resource isolation), ADR-0014 (cell boundary)

---

## Context

ADR-0005 chose partitioning over separate databases and named the cost plainly:

> Partitioning gives data isolation, not resource isolation — venues share a primary.

That cost has been sitting unaddressed. Meanwhile the contracts have been accumulating an
implicit read model in prose:

- Reporting "reads the reporting replica, never the primary" — stated on 23 operations
- Access validation "reads the primary unconditionally" — because a revoked entitlement that
  admits a guest-app is worse than a slow gate
- Financial reports are "served from the reporting replica" — because a month-end report
  against the transactional database during a venue spike is the single most likely cause of
  an outage this platform has
- POS reads the local bundle and does not touch the database at all (ADR-0013)

Four different routing rules, expressed as English in descriptions, enforced by nothing.

A rule that lives only in prose gets followed until the first person in a hurry. The specific
failure mode is well understood: someone adds a dashboard query to a hot path, it works in
staging where nothing else is running, and it takes the primary down on a Saturday.

## Decision

**Every operation declares which database it reads, in `x-ticvai-read-routing`.** Three
values, and the routing layer refuses to serve an operation whose declaration it cannot
satisfy.

| Value | Reads | Lag tolerated | Use |
|---|---|---|---|
| `primary` | The write primary, always | None | Correctness depends on this instant |
| `replica` | A hot streaming replica, primary on failover | Seconds, bounded and enforced | Operational reads where a second of staleness is invisible |
| `analytical` | The reporting replica, never the primary | Minutes | Aggregations, exports, dashboards |

**All writes go to the primary.** That is not a routing decision and is not declared.

### What must be `primary`

Correctness-critical reads, where a stale answer is a wrong answer rather than an old one:

- **Access validation.** A revoked entitlement, a blacklisted guest-app, an expired pass. Replica
  lag here admits someone who should be refused, and the guest-app is already through the gate by
  the time it resolves
- **Capacity, envelopes, channel allocations and leases.** Overselling is not recoverable by
  waiting
- **Seat availability and holds.** Same reason, sharper — two guests in the same seat
- **Payment and order state during a transaction**
- **Session validation and permission resolution at login.** A revoked grant must not survive
  replica lag
- **Shift state and cash position**
- **Stock on hand where a sale depletes it** — retail, recipe-linked F&B, prize redemption

### What may be `replica`

Operational reads where a second of staleness is invisible to the person reading:

Catalogue browsing, product and price listing, guest-app profile reads, case and work order
queues, asset lookups, menu reads, inventory listings, configuration reads.

### What must be `analytical`

Anything aggregating, exporting or spanning a date range: every reporting operation, financial
reports, trial balance, settlement matching, usage metering, campaign performance, natural
language query.

**Never the primary, under any load condition.** This is the rule ADR-0005's known cost most
needs.

## Horizontal scaling

Two axes, and they solve different problems.

### Within a cell — read replicas

A cell is one Postgres primary plus replicas. Scaling reads is adding replicas, which is
cheap and requires no application change once routing is declared.

**This does not scale writes**, and writes are where a venue spike actually lands: scans,
orders, payments. Mitigations from ADR-0005 stand — capacity-counter sharding, per-venue rate
limits, reserved connection minimums — with one addition:

**Access validation gets a reserved connection pool.** A gate must not queue behind a report.
This is the concrete form of "venues share a primary" being an accepted risk rather than an
ignored one.

### Beyond a cell — launch another cluster

Amended 14 August. **Capacity is driven by traffic and concurrent users, not by tenant count.**
Forty quiet tenants may load a cell less than three busy ones.

Scaling out is **launching another identical cluster** and placing or moving tenants onto it —
same shape, same tier, same schema version, copied from a model cell rather than specified. A
cluster at a different version is not capacity; it is a second thing to maintain.

`getCellCapacity` reports per dimension — concurrent users, transactions, scans, connections,
storage, replication lag — because the response differs by which one is short.

A tenant already on a hot cell moves with `planTenantMigration`, which is the same machinery
that upgrades a tenant from shared to dedicated infrastructure.

### Beyond a cell — split the cell

**The cell is the shard boundary** (ADR-0014). A tenant-region that outgrows one primary is
split by region, or a region is split, and the existing cell machinery handles it — because
cross-cell was already built for jurisdiction rather than for load.

**Venues are not shards.** Splitting a venue out of its cell breaks the single-transaction
guarantee ADR-0005 exists to preserve: multi-venue passes, revenue splits, memberships and
consolidated reporting all assume one database. That guarantee is worth more than the
elasticity.

### Where the analytical store lives

The reporting replica is **in-cell** and in-region. It is a replica of that cell's primary,
not a central warehouse.

Cross-cell and cross-tenant reporting comes from the central warehouse, which receives
aggregates only and never personal data (ADR-0009, ADR-0010). **A cell is never queried by
another cell for reporting.** That constraint is data residency, not performance, and it does
not bend under load.

## Consequences

**Every operation declares its routing.** 581 operations, validated in CI alongside the four
existing extensions. An operation with no declaration does not build.

**The routing layer enforces the declaration** rather than trusting it. An operation declared
`analytical` cannot be served from the primary even if a replica is unavailable — it fails
instead, because a failed report is recoverable and a downed primary during trading is not.

**Replica lag is measured and bounded.** `replica` reads carry a maximum tolerated lag; beyond
it the router falls back to the primary and emits a warning. `analytical` has no such
fallback, deliberately.

**Results say how fresh they are.** `ReportResult.dataAsOf` already carries the replica
position. That field exists precisely so nobody argues about a figure that moved between two
people running the same report.

**Connection pools are separate per class.** Sharing one pool means an analytical query can
exhaust the connections a gate needs, which reintroduces the problem this ADR exists to
prevent.

### Costs accepted

| | |
|---|---|
| Replica cost per cell | Real, and multiplied by the number of cells under ADR-0014 |
| Routing is a decision per operation | 581 declarations. Mechanical, but each one is a judgement someone must make correctly |
| A wrong `replica` declaration is a subtle bug | It works in test where lag is zero. Mitigated by defaulting new operations to `primary` — the safe direction |
| Write scaling is unsolved within a cell | Accepted. The answer is splitting the cell, and the machinery already exists |

## Alternatives considered

**Route by verb — reads to replica, writes to primary.** Simple, and wrong in exactly the
place it matters: access validation is a read that must never be stale.

**One replica, all reads.** Puts a month-end aggregation and a turnstile scan on the same
connection pool. The report wins, because it got there first.

**CQRS with separate read models.** Genuinely better for reporting and genuinely more machinery
than a platform with no production traffic should carry. The `analytical` class leaves the door
open — a materialised read model is an implementation of it, not a change to it.

**Venue-level sharding.** Rejected above. It breaks the single-transaction guarantee that
ADR-0005 chose partitioning to preserve.
