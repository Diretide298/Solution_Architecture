# Cells & Tenancy

> **Purpose:** The deployment model  
> **Owner:** Dinesh  
> **Status:** Settled


## Cell = Tenant × Jurisdiction

One isolated deployment cell per tenant per jurisdiction. Splitting at **Region** is mandatory, not load-driven — a venue operating in a jurisdiction expects infrastructure there.

the reference tenant runs **two cells minimum** — `ref-north` (Abu Dhabi + Dubai) and `ref-offshore` (Venue Beta-2) — because Brand Beta spans UAE and Oman.

## Why cells

| Problem | How cells solve it |
|---|---|
| Noisy neighbour | Structurally impossible across tenants |
| Blast radius | A bad migration takes one tenant, not the platform |
| Data residency | Cell placed in the required jurisdiction |
| Client-hosted tenants | Same topology, different owner. No special code path |
| Per-tenant scaling | Each cell sized to its own load |
| Connection exhaustion | Bounded per cell rather than tenants × services × pods |

Cells scale by **replication**, not decomposition — which is why 6–8 services suffice rather than one per bounded context.

## Placement is a Region attribute

```
Region {
  id, name, country
  currency, decimals, timezone, date_format, fiscal_year_start
  placement: shared | dedicated:{cloud}:{region} | client_hosted:{endpoint}
}
```

A tenant may be **mixed**: Abu Dhabi and Dubai on a shared UAE cell, Oman dedicated or client-hosted. Placement is not a tenant-level property.

## Tiers

| Tier | Topology | Fits |
|---|---|---|
| Shared | Shared cell, DB per tenant | Single-venue, low concurrency |
| Dedicated | Own cell, own cluster | Multi-venue |
| Isolated | Own cell, own region, own key management | Residency or contractual isolation |
| Client-hosted | Client's own subscription | Full physical separation, or jurisdictions with no hyperscaler region |

Same code, same migrations, different placement. Tier is a Control Plane attribute.

## Brand is not a boundary

**Region is.** Brand Beta spans UAE and Oman in the client's own example, so brand-level separation does not align with jurisdiction. Region owns currency, decimals, time zone, fiscal year and tax regime — everything jurisdiction-shaped.

## Venue isolation — partitioning, not separate databases

One database per tenant (10 Aug 2026). Venues are isolated by **Postgres list partitioning on `venue_id`**, not by separate databases.

| | Partitioning | Separate DBs |
|---|---|---|
| Physical data separation | Yes | Yes |
| Partition pruning | Yes | Yes |
| Independent archival and vacuum | Yes | Yes |
| **Single transaction across venues** | **Yes** | No |
| **One guest-app identity, one wallet** | **Yes** | No |
| Migration targets | 1 per tenant | 1 per venue |

Five features cross venue boundaries inside one transaction and would need distributed transactions otherwise: multi-venue passes with revenue split (12 Aug §16) · memberships across venues · wallet balances · consistent guest-app identity (the stated reason for one DB) · consolidated brand reporting (12 Aug §14).

Partition the hot tables — orders, order lines, tickets, scan events, payments, ledger entries, F&B orders. Leave shared reference data unpartitioned: guests, products, price lists, roles, entitlement definitions. Those must be visible across venues.

## Load

Sizing is against **tenant aggregate with correlated peaks**, not per-venue. Venues within a tenant peak on the same days — Eid, National Day, school holidays — so the averaging assumption behind per-venue sizing does not apply.

| Scope | Sustained writes/s | Rows/s |
|---|---|---|
| One venue at 10k concurrent | 20–40 | 200–500 |
| 8-venue tenant | 160–320 | 1,600–4,000 |
| Same, correlated burst | ~1,600 | ~15,000 |

Gate scans are absorbed at the venue edge and never reach the primary in real time — the highest-frequency operation on a busy day, removed from the database entirely.

## Escape hatch

A venue outgrowing its cell can be **promoted** to its own cell: provision, logical replication of that venue's partitions, cutover, registry update. Cross-venue features then federate through the API.

Promotion is an exception path, not the default topology.

## What crosses a border

| Level | May cross |
|---|---|
| Above Venue | **Aggregate only** — revenue by venue, product, period, currency |
| Venue and below | **Never.** Stays in-cell |

Cross-tenant and cross-region reporting is served from a central warehouse fed by per-cell event export of aggregated, pseudonymised data. **Cells are never queried directly.**

See compliance/data-residency.
