# ticvai-backend

.NET 8 services for a single TICVAI cell. One deployment of this repo serves one
tenant in one jurisdiction (Project Direction §3.3.1).

## Module boundaries are enforced, not encouraged

`tests/Ticvai.ArchitectureTests` fails the build if any module references another
module's internals. Modules communicate through contracts in
`Ticvai.Shared.Kernel.Abstractions` and through the event bus. Without automated
enforcement these boundaries decay within weeks, and extraction later becomes a
rewrite rather than a week's work.

`Ticvai.Shared.Kernel` holds primitives only — tenant context, money, IDs, result
types. The moment domain logic lands there the boundaries are gone.

## Schema-per-module, database-per-tenant

One database per tenant (10 Aug 2026). Each module owns a Postgres schema and
connects with a role granted access only to that schema. This is normally a
microservice anti-pattern; it is correct here because the tenancy decision
outranks it and because order → payment → entitlement → ledger must be atomic.

## Non-negotiables

| Concern | Rule |
|---|---|
| Tenant scope | Enforced at the data layer via RLS, not only in services |
| Sessions | Redis registry; JWT `sid` validated per request |
| Money | `numeric(18,4)` + explicit currency scale. OMR is 3dp |
| Connections | PgBouncer transaction mode, per-service pool caps |
| Venue isolation | List partitioning on `venue_id` for hot tables |
| Reads | Replicas by default; access validation reads the primary |

## Run locally

    docker compose up -d
    dotnet run --project src/Ticvai.Api
