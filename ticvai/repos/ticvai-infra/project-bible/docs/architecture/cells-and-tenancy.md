# Cells & Tenancy

> **Purpose:** The deployment model, restated from the accepted ADRs
> **Owner:** Dinesh
> **Status:** Restates ADR-0038 (as amended by ADR-0040), ADR-0039, ADR-0042, ADR-0043, ADR-0017 (as amended),
> ADR-0005 (as amended by ADR-0056), ADR-0056 and ADR-0064. Where this page and an ADR disagree, the ADR wins.

**Rewritten 3 November 2026** (r13 system review A-07, CHG-R14J-051). The page taught ADR-0001's
`Cell = Tenant × Jurisdiction`, one tenant per cell, which ADR-0014 replaced and ADR-0038 superseded in turn
(ADR-0001 and ADR-0014 are both superseded; their live successor is ADR-0038).

## A cell is a region, holding a database per tenant

**A cell is a region and nothing else** (ADR-0038). It is served by one Postgres instance, and by more than one
when one is not enough (ADR-0040): the instance is something a cell *has*, not something it *is*.

**A cell holds many tenants, each in its own database** (ADR-0038). Every tenant database gets the same
template: every schema except `control` (ADR-0039 1). **A tenant database is never split across instances**
(ADR-0040); it sits whole inside exactly one instance of its region's cell.

**A tenant with venues in two regions has two cells and two databases** (ADR-0039 4): one row per tenant per
cell in `control.cell_tenant`, which replaced `control.cell.tenant_id`.

```
cell  ·  a region (UAE, Oman, ...)
  ├── instance 1                 control.cell_instance (live · draining · retired)
  │     ├── db: acme             the tenant template -> tables
  │     └── db: globex           the same template
  └── instance 2                 added when the region needs it (ADR-0040, ADR-0042)
        └── db: initech

services   shared across tenants, five deployables (ADR-0055),
           routed per request to a tenant database by tenant id
```

## The tenant database is the unit of the lifecycle

A tenant database is the unit of **provisioning, migration, backup and destruction** (ADR-0039 2). It is named
from the tenant's stable slug and does not encode the region: the instance already is the region.

- **Provisioning** follows verification, never the application, and registers the database in
  `control.cell_tenant` with its cell and its instance (ADR-0042: `instance_id` is required from the first row).
- **Migrations fan out per tenant database, and the canary is a tenant** inside the canary cell, not the cell
  (ADR-0039 3): one `control.migration_run_tenant` row per tenant per run, rolled up per cell in
  `control.migration_run_cell`. A wave is a set of tenants and may be part of one cell.
- **Restore is per tenant**, and **destruction is a database drop and a row** (ADR-0039).

## Where a new tenant lands, and when a region grows

**The address is the cell and the instance** (ADR-0042 1). **A new tenant goes to the `live` instance in its cell
with the most headroom**, measured as peak concurrent server connections over the trailing 7 days as a fraction of
that instance's own `max_connections`, never as a count of databases. **A pinned tenant is placed by hand** and the
balancer leaves it alone; a pin is what a dedicated client buys (ADR-0042 2). The growth trigger and its threshold
are ADR-0042 3's.

## Tiers

The deployment models are ADR-0017's, amended by ADR-0038 so that its placement table describes instances, and by
ADR-0046 (on-premise is two configurations).

| Tier | What it is |
|---|---|
| Shared | A tenant database on a shared instance of its region's cell; isolation is logical (row security by scope) |
| Dedicated | The tenant's database pinned to an instance of its own (ADR-0042) |
| Additional region | A cell in another region, built on demand, in-jurisdiction |
| On-premise | The client's hardware: `onPremiseIsolated` or `onPremiseConnected` (ADR-0046) |

A burst environment for an on-sale is one tenant and one event, one instance holding one database (ADR-0035 as
restated by ADR-0038).

## Region is the boundary, not brand

**Region is.** Brand Beta spans UAE and Oman in the client's own example, so brand-level separation does not align
with jurisdiction. Region owns currency, decimals, time zone, fiscal year and tax regime: everything
jurisdiction-shaped. **Residency is a fact about which host a file is on** (ADR-0038), and with several instances
every one of them is still in that region (ADR-0040).

## The control plane

`control` is a database of its own, not a schema in a tenant database (ADR-0039 1). **It splits on personal data**
(ADR-0043): one global control database holding no natural person, and one regional control database per region
for what names a person. The rule: a table goes regional when its subject is a natural person; otherwise it stays
global and the column that names a person is extracted.

## Tenants share a cell, so a busy one is limited

**Tenants on a shared instance can affect each other**, and ADR-0064 is the answer: a token bucket per tenant and
audience in every request-serving host, a cap on one tenant's share of a replica's in-flight work when the replica
is busy, the per-tenant connection pool cap, and on-sales in a burst environment behind the waiting room.

## Venues inside a tenant database

Venues are rows of one tenant database, not databases of their own (ADR-0005). **In release 1 venue isolation
comes from row security by scope; venue partitioning is deferred, not cancelled** (ADR-0056, amending ADR-0005 and
ADR-0044). The time-driven, append-only tables are range-partitioned by month instead (ADR-0056 2).

Five features cross venue boundaries inside one transaction, which is why venues share a database: multi-venue
passes with revenue split (12 Aug 16) · memberships across venues · wallet balances · one guest-app identity ·
consolidated brand reporting (12 Aug 14).

**The old escape hatch, a venue promoted to a cell of its own, no longer fits**: a tenant database is never split
(ADR-0040). An existing tenant moves whole, and only by `planTenantMigration` and `executeTenantMigration`,
operator-initiated; rebalancing is deliberately not automatic (ADR-0042).

## Load

Sizing is against **tenant aggregate with correlated peaks**, not per-venue. Venues within a tenant peak on the same
days (Eid, National Day, school holidays), so the averaging assumption behind per-venue sizing does not apply.

| Scope | Sustained writes/s | Rows/s |
|---|---|---|
| One venue at 10k concurrent | 20-40 | 200-500 |
| 8-venue tenant | 160-320 | 1,600-4,000 |
| Same, correlated burst | ~1,600 | ~15,000 |

Gate scans are absorbed at the venue edge and never reach the primary in real time (ADR-0013).

## What crosses a border

| Level | May cross |
|---|---|
| Above Venue | **Aggregate only**: revenue by venue, product, period, currency |
| Venue and below | **Never.** Stays in-cell |

Cross-tenant and cross-region reporting is served from a central warehouse fed by per-cell event export of
aggregated, pseudonymised data. **Cells are never queried directly.** Entitlements that cross cells follow
ADR-0010.

See compliance/data-residency.
