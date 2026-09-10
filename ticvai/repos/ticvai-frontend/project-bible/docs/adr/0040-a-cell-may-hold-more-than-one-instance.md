# ADR-0040: A cell is a region; a region may need more than one instance

**Status:** Accepted
**Date:** 7 September 2026
**Amends:** [ADR-0038](0038-cell-is-a-region-database-per-tenant.md) — its decision read *"One Postgres instance per region. The instance is the cell."* The first sentence becomes *one or more*, and the second no longer holds
**Amends:** [ADR-0032](0032-load-shedding-and-pooling.md), whose pool cap is a per-tenant limit and not a reservation
**Raises:** **CF-168** — when a second instance is added, and who decides. **Decided 8 September by [ADR-0042](0042-when-a-region-grows-and-where-a-tenant-lands.md)**

---

## Context

**ADR-0038 made the cell, the region and the Postgres instance one thing, and that made a region's
capacity one machine.** It was the right simplification for the question it was answering — where
does a tenant's data live — and it quietly answered a second one it was not asked: how much can a
region hold.

**The arithmetic surfaced it four days later.** `default_pool_size` caps server connections per
database, so ten tenants plus `control` is 440 of `max_connections = 500`. That was written up as
*"the ceiling is eleven tenants and the configuration runs out one client after launch"*, which is
**wrong in a way worth recording**:

| | |
|---|---|
| `MIN_POOL_SIZE` | **not set in any configuration** — pgbouncer defaults to 0 |
| So a provisioned tenant holds | **nothing** until it transacts, and releases at idle timeout |
| So 440 is | the case where all ten peak **simultaneously at full depth** |
| And 11 is | a monitoring threshold, not a capacity limit |

**Connections scale with concurrent transactions, not with tenants and not with people.** A client
with fifty venues and a client with two both get a pool of forty. **The package already sizes
against load everywhere else** — `derive-burst-scope.py` computes
`connectionsAtFloor = floor × POOL_MAX_PER_REPLICA` where the floor comes from RPS. The tenant
pools are the only place capacity is a function of *how many tenants exist* rather than *how much
work they do.*

**ADR-0038's own reopening trigger named this exactly**, and it is being taken up rather than
worked around:

> *"Concurrent tenants exceed what one primary's connections allow… Passing it is a reason to
> re-argue the topology, not only to raise `max_connections`."*

---

## Decision

**A cell is a region. A region is served by one instance, and by more than one when it needs
more.** Both directions are available and neither is preferred in the abstract:

**Scale the instance up** where the work is not yet more than one machine should do. It keeps one
`max_connections`, one WAL, one restore and one thing to reason about, and it is the cheaper answer
whenever it is available.

**Add an instance and spread tenants across it** where it is not. This is what removes the ceiling:
capacity per region stops being one machine's and becomes a number of machines, and a tenant
database still sits whole inside exactly one of them.

**A tenant database is never split across instances.** Everything ADR-0038 and ADR-0039 rest on —
per-tenant restore, a bounded drop, one migration applied N times — depends on a tenant being one
database in one place, and that is unchanged.

### What this costs, and it is the reason ADR-0038 chose otherwise

**"The instance is the cell" stops being true, and that sentence was doing work.** ADR-0038 rejected
`Cell = Tenant × Region` on the grounds that **a word that changes referent with configuration is a
word that will be wrong in half the documents that use it** — and a cell that is sometimes one
instance and sometimes three is that same hazard, arriving from the other side.

**It is accepted here because the alternative is worse and the fix is cheap:** the cell stays the
region, exactly and always, and the instance becomes a thing a cell *has* rather than a thing it
*is*. `CellKind` is unaffected — `shared`, `dedicated`, `onPremise` and `burst` describe a region's
arrangement, not a host count.

**Residency is unaffected.** ADR-0038's argument was that with one instance per region a row can
only sit in the instance its region owns. With several, every one of them is still in that region,
so the property that mattered — *"is this row in the UAE"* is answered by which host it is on —
holds without change.

---

## Consequences

**🔴 `control.cell_tenant` no longer says enough to route a request.** It carries `cell_id`,
`tenant_id` and `database_name`, which was a complete address while a cell had one instance.
**With several, a database name without a host is not an address**, and the service that resolves a
tenant would have to guess. A `control.cell_instance` table and an `instance_id` on `cell_tenant`
are required before a second instance can exist.

**This ADR does not make that change.** It is named here so that the gap is a decision rather than
an omission — and so nobody adds an instance believing the control plane can already find it.
[ADR-0042](0042-when-a-region-grows-and-where-a-tenant-lands.md) makes it: `control.cell_instance`
exists and `cell_tenant.instance_id` is required from the first row.

**Placement becomes a real choice on provisioning.** ADR-0039 said provisioning is *apply the
template, record the tenant's membership of the cell, seed nothing.* It now also picks an instance.
**A rule is needed and this ADR does not set one** — fullest-first, emptiest-first and pinned all
behave differently on the day a tenant grows, which is CF-168. **ADR-0042 sets it: emptiest-first by
trailing-week peak connections, with a pin.**

**Migration fan-out is unchanged in mechanism and wider in one dimension.**
`control.migration_run_tenant` is per tenant database and does not care which host it is on. What
gains meaning is `migration_run_cell` as a rollup: a region is now several machines, and *"how is
the UAE doing"* may have to distinguish them.

**ADR-0032's pool cap is a limit, not a reservation, and it is deliberately oversubscribed.** The
sum of per-database caps may exceed `max_connections`, because tenants do not all peak together and
`min_pool_size = 0` means idle ones cost nothing. **What is monitored is concurrent server
connections against the primary's own limit** — not the tenant count, which says nothing about
load. A sustained approach to that limit is the signal to scale, and this ADR gives two ways to.

**Backups, upgrades and failover multiply per region.** One instance per region meant one of each.
This is the operational cost, and it is the ordinary kind — more of a thing already being done,
rather than a new thing.

---

## When this is reopened

**A tenant outgrows the instance it sits on.** Already specified — `planTenantMigration` and
`executeTenantMigration` — and moving one database between two instances in the same region is the
cheapest form that operation has ever had. What is missing is a threshold rather than a complaint —
**ADR-0042 supplies one for adding an instance**, and leaves the per-tenant outgrowing threshold open.

**Instances per region reach a number where placement wants a scheduler.** Two or three is a column
on a table. Ten is a component nobody has designed, and the point at which this decision should be
re-argued rather than extended.

---

## Alternatives considered

**Raise `max_connections` alone.** Rejected as the *only* answer, kept as one of two. Every backend
is a process with a memory cost whether or not it is used, so this buys headroom on a curve that
flattens — and it leaves the region's capacity as one machine's, which is the thing being fixed.

**Lower `default_pool_size` alone.** Rejected for the same reason and one more: halving it to twenty
doubles the tenants that fit and halves what a single busy tenant can ever get. **It trades a
platform limit for a per-tenant one**, which is the wrong direction on the exact day it matters — a
sale, in one venue, in one tenant.

**A read replica instead of a second primary.** Rejected as a substitute, not as a practice.
ADR-0016 already routes reads to replicas, and that is worth doing on its own; but a replica takes
no writes, and the connections in question are held by the write path.

**Shard a tenant's database across instances.** Rejected. It breaks the single property every
decision since ADR-0038 has been built on — that a tenant is one database, so it can be restored,
migrated and dropped as one thing.
