# ADR-0005: Venue isolation by partitioning, not separate databases

**Status:** Accepted  
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

## Alternatives

| Rejected | Why |
|---|---|
| Database per venue | Five cross-venue features become distributed transactions |
| No isolation | Loses per-venue archival, pruning and query locality |
