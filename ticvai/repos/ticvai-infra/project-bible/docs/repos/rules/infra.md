# Infrastructure Runtime

Terraform + Kubernetes. One `cell` module instance = one cell of one environment: a region of one jurisdiction
holding a database per tenant (ADR-0038, ADR-0040). Tenants are rows in the control database (ADR-0039), never
module inputs; a tenant is placed on a cell (r8 cause FOUNDATION-AI-C55, 20 October 2026).

**Environments** (the lead, 20 October 2026, FOUNDATION-AI-C52 and C23): dev runs on laptops with docker compose
and has no cell; `staging` is one shared pre-production environment in the Softlabs Azure subscription
(`terraform/environments/staging`, state in a storage account there, `backend.hcl.example`); `production` is hosted
by the client later (`terraform/environments/production/<cell>.tfvars`). The environment is part of every resource
name (`stg-ae1`, `prd-ae1`), and staging turns the heavy parts down with the module's switches
(`system_min_nodes`, `nat_gateway_enabled`, `ai_gpu_enabled`, no replicas, no high availability).

## Cell rules

- **Verify the hyperscaler has a region in the jurisdiction** before applying. Gulf coverage
  is uneven. Where there is none, `tier = "client_hosted"` is the mechanism, not a workaround
- **Check `geo_redundant_backup_enabled` against the paired region.** Default pairing may sit
  outside the jurisdiction, moving personal data across the boundary via the backup path
- Size `database_sku` against **tenant aggregate** load, not per-venue. Venue peaks within a
  tenant are correlated — Eid, National Day, school holidays
- `prevent_destroy` on databases and key vaults
- Key vault per cell. A cell holds many tenants (ADR-0038), so the field keys inside it are per tenant
  (ADR-0063): a compromise of one tenant's data key is contained to that tenant

## Placement

A cell's tier is `shared`, `dedicated`, `isolated` or `clientHosted` (`control.cell.tier`). A tenant's database
sits on one instance of one cell (`control.cell_tenant`, ADR-0042) and is never split (ADR-0040); a tenant may
have a database in more than one cell, one row each.

## Migration rollout

Every migration runs **once per tenant database** (ADR-0039): the fan-out unit is a tenant database and the
canary is a tenant, then waves, gated on health. Version skew between databases is expected while a run is in
flight; contracts tolerate N-3 minor versions.

**Rollback tested before merge, not after.**

## Style

Modules parameterised, never copy-pasted per cell · no inline secrets · variables carry
`description` and `validation` — validation catches jurisdiction typos at plan time ·
`fmt` and `validate` blocking in CI · state remote, locked, per environment.

## What is not here

Cross-tenant analytics. The warehouse is fed by per-cell event export of **aggregated,
pseudonymised** data only. Cells are never queried directly.
