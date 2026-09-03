# ADR-0038: A cell is a region, and a database per tenant inside it

**Status:** Accepted
**Date:** 3 September 2026
**Supersedes:** [ADR-0014](0014-cell-per-region.md) — a cell held one tenant · [ADR-0036](0036-burst-cell-database-segregation.md) — a burst cell held a database per service
**Closes:** **CF-161**
**Amends:** [ADR-0028](0028-service-decomposition.md), whose decomposition is unchanged · [ADR-0017](0017-deployment-models.md), whose placement table is amended to describe instances rather than cells
**Confirms:** [ADR-0005](0005-venue-isolation-by-partitioning-not-separate-databases.md)

---

## Context

**CF-161 has been open since 24 August and it has blocked two ADRs by sitting under them.** Dinesh
recommended segregating databases from the start, because splitting a centralised database after
two or three years in production is significantly harder than starting isolated and merging later.
ADR-0028 and ADR-0005, written the same day, say one Postgres per cell with 26 schemas inside it —
tenancy as a partition key rather than a deployment boundary. **Neither position is wrong and they
cannot both hold.**

**The asymmetry in Dinesh's argument is real, and the question it leaves unanswered is *split along
which line*.** Per service is one answer. Per tenant is another, and it is the split anybody is
actually going to be asked for: a client outgrowing the shared platform, a client buying isolation,
a client leaving. Nobody has ever been asked to extract OrderService from a running venue.

**Meanwhile nothing in the package implements any of the three positions.** Measured on 3
September, across the whole of `backend/` and all seven deployment configurations:

| | |
|---|---|
| `CREATE SCHEMA` | **26** |
| `CREATE DATABASE` | **0** |
| `PARTITION BY` | **0** — ADR-0005's decision of 12 August has never been generated |
| row-level security policies | **0** |
| configs provisioning per tenant | **0 of 7** — a, b and d point every service at one `ticvai`; c and its variants at three databases named per *service* |

`venue_id` and `tenant_id` are ordinary columns. **Whatever gets decided here, it is being decided
against artefacts that implement none of the alternatives**, which is the one piece of good news:
there is no migration, because there is nothing to migrate.

---

## Decision

**One Postgres instance per region. The instance is the cell. One database per tenant inside it.**

```
postgres instance  ·  region  ·  the cell
  ├── db: acme            26 schemas → tables → venue_id partitions
  ├── db: globex          26 schemas
  └── db: initech         26 schemas

services   shared across tenants, scaled on traffic,
           routed per request to a tenant database by tenant id
```

**The 26 schemas stay as they are, inside each tenant database.** ADR-0028's decomposition is
untouched: no service spans a schema it does not own, and no schema is written by two. What changes
is where those schemas live — one set per tenant rather than one set for everybody.

**Venues remain list partitions on `venue_id` within the tenant database.** ADR-0005 is confirmed,
not superseded, and it is now owed its implementation.

**A cell holds many tenants.** This is the part that supersedes ADR-0014, which set
`Cell = Tenant × Region` and gave every cell exactly one tenant. A cell is now a region and nothing
else.

### Why one instance per region rather than one instance holding several

**Residency stops being a policy and becomes a fact about where a file is.** Postgres has no
construct between an instance and a database, so "a cell inside an instance" would be a naming
convention — and a naming convention is the wrong thing to be holding a data-residency commitment.
With one instance per region, a tenant's data can only sit in the instance its region owns, and the
question *"is this row in the UAE"* is answered by which host it is on rather than by a prefix
somebody could get wrong.

### Why per tenant rather than per service

**The costs of segregation land where they hurt most on the service line and least on the tenant
line.** ADR-0036 itemised them for the burst cell: three connection pools instead of one, a
cross-service read over the network **inside the lease lock**, slower provisioning. Per tenant, a
purchase never leaves its database — `acquireInventoryHold` reads `catalogue.performance` and
writes `catalogue.inventory_hold` in the same transaction it always did — and the pools are per
tenant, which is a capacity question rather than a correctness one.

**And the operational cost the package objected to changes shape.** Sixteen databases to migrate,
back up, monitor and keep in step is sixteen different schemas. Two hundred tenant databases is
**one** schema applied two hundred times: a fan-out with a known shape, which is a job rather than
an architecture.

---

## Consequences

**🔴 The control plane is not a schema in a tenant database.** `control.*` is 41 tables — the cell
registry, placement, licences, migration runs, onboarding applications, the Guest Link Registry of
ADR-0010 — and every one of them is *about* tenants rather than *inside* one. A cell registry that
exists two hundred times is two hundred registries. **`control` moves out of the tenant template
and into a home of its own**, and that home is the next ADR.

**🔴 `control.cell` loses `tenant_id`.** It is a column today, which was correct while a cell had
one tenant. A cell now has many, so it becomes a relation — and until it does, the schema asserts
the rule this ADR just replaced.

**🔴 `control.migration_run_cell` can no longer say what happened.** One row per cell per migration
was per tenant while a cell was a tenant. Under this decision a fan-out that succeeds for 180
tenants and fails for 20 has nowhere to record it, and **that is the failure that happens at two in
the morning.** A per-tenant migration row is not optional.

**ADR-0036 is superseded rather than amended.** A burst cell is one tenant and one event, so under
this rule it is one instance holding one database — and the three-databases-per-service arrangement
loses the reason it was carved out for. Its own reopening triggers named this: *"CF-161 resolves…
it must be restated against the new decision rather than inherited from this one."* The costs it
listed disappear with it, which is the outcome it would have preferred.

**ADR-0032's pooling arithmetic is redone per database, and the number it needs does not exist.**
Pools are per database, so *"four hundred client connections share forty server ones"* is now a
statement about one tenant. **At 40 server connections a database, `max_connections = 500` supports
about 25 tenants transacting concurrently** — 200 tenants is comfortable, 200 tenants busy together
is not, and a Saturday evening is exactly when venues are busy together. **The figure to size
against is concurrent tenants and the package has never stated one.** It is a client question, and
it should be asked before the instance is specified rather than after.

**`tenant_id` inside a tenant database is redundant.** 51 occurrences across `backend/`. Most are
harmless and some are load-bearing on the control-plane side; they need reading rather than
deleting, and a column that says which tenant you are while you are inside that tenant's database
is a column that will eventually disagree with the database it is in.

**`CellKind` survives with its meaning intact.** `shared` is a regional instance with many tenant
databases; `dedicated` is a regional instance with one; `onPremise` is a regional instance the
Control Plane may not be able to reach; `burst` is a regional instance stood up for one sale and
destroyed after reconciliation. ADR-0017's placement table describes instances now rather than
cells, which is an amendment to its wording and not to its decision.

**Cross-cell machinery (ADR-0010) is unchanged in mechanism and wider in scope.** It already
crosses regions. It now also describes two tenants who happen to share an instance, which is a
cheaper hop and the same code path.

**All seven deployment configurations regenerate**, and `tools/derive-ddl.py` gains two jobs: emit
one tenant template rather than one database's worth of DDL, and emit the `PARTITION BY venue_id`
that ADR-0005 has been owed since 12 August.

**This ADR decides the shape and implements none of it.** Every artefact named above still says
something else today.

---

## When this is reopened

**A tenant outgrows the instance its region owns.** The exit is already specified —
`planTenantMigration` and `executeTenantMigration`, and moving one database is the cheapest version
of that operation this architecture has ever had. But the *trigger* wants a threshold rather than a
complaint.

**Concurrent tenants exceed what one primary's connections allow.** The arithmetic above puts that
at roughly 25 at the current pool size. Passing it is a reason to re-argue the topology, not only to
raise `max_connections`.

**A jurisdiction requires separation below the region.** One instance per region answers residency
at the country level. A rule that says two tenants in the same country may not share a host is a
different decision and this one does not reach it.

---

## Alternatives considered

**A database per service, as recommended on 24 August.** Rejected. The asymmetry argument is
correct and it does not select this line: the split that gets asked for is a tenant, not a service.
The costs are concentrated on the hold path — a network hop inside the lease lock, where ADR-0031
establishes that lease duration is the ceiling — and sixteen distinct schemas must be kept in step
before a single table is written.

**One shared database with tenancy as a partition key, as ADR-0028 was written.** Rejected on the
asymmetry, which is the half of Dinesh's argument that survives. Extracting one tenant from a
two-hundred-tenant database after two years in production is the operation this platform will
actually be asked to perform, and it is the one this arrangement makes hardest.

**Cell stays `Tenant × Region`, with a database per cell.** Rejected. It reaches the same physical
arrangement and makes *cell* mean two different things depending on placement — under `shared` it
would be a database, under `dedicated` an instance. **A word that changes referent with
configuration is a word that will be wrong in half the documents that use it.**

**A schema per tenant inside one database.** Rejected. 26 schemas × 200 tenants is 5,200 schemas in
one catalogue, and it buys none of the isolation: one `max_connections`, one WAL, one restore, and
a single bad migration reaches every tenant.
