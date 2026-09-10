# ADR-0005: Venue isolation by partitioning, not separate databases

**Status:** Accepted — **confirmed by [ADR-0038](0038-cell-is-a-region-database-per-tenant.md)**
(itself amended by ADR-0040 on instance count, which does not touch this confirmation),
which settles what *the tenant database* is. **Not yet implemented:** `backend/` contains no
`PARTITION BY`, so `venue_id` is an ordinary column and this decision is owed its DDL.
**[ADR-0044](0044-which-tables-partition-by-venue.md) proposes the rule** — partition where
`venue_id` is `NOT NULL` — and is waiting on sign-off, because it carries a `venue_id` onto 74
referencing tables.
**Date:** 12 August 2026

## Context

10 Aug 2026 settled one database per tenant, with all channels connecting to it, so that guest-app identity and session stay consistent across channels. The question was whether venues within a tenant warrant separate databases.

## Decision

**Venues are isolated by Postgres list partitioning on `venue_id`**, within the tenant database. Not separate databases.

## Consequences

- Multi-venue passes with revenue split (12 Aug §16), memberships, wallets, guest-app identity and consolidated brand reporting all remain single-transaction
- Partition pruning gives per-venue query isolation; independent archival and vacuum per venue
- Migration and backup targets stay at one per tenant rather than one per venue
- **Partitioning gives data isolation, not resource isolation** — venues share a primary. Mitigated by capacity-counter sharding, per-venue rate limits and reserved connection minimums
- A venue that outgrows its cell can be **promoted** to its own cell as an exception path
- **Nothing in the schema enforces the isolation today.** `orders.order_line` references
  `orders.sales_order` by `sales_order_id` alone, so a line in one venue may reference an order in
  another and satisfy every constraint. Pruning makes that unlikely; only a composite key makes it
  impossible, which is what ADR-0044 decides

## Alternatives

| Rejected | Why |
|---|---|
| Database per venue | Five cross-venue features become distributed transactions |
| No isolation | Loses per-venue archival, pruning and query locality |
