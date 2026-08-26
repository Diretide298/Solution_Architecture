# Infrastructure Runtime

Terraform + Kubernetes. One `cell` module instance = one tenant in one jurisdiction.

## Cell rules

- **Verify the hyperscaler has a region in the jurisdiction** before applying. Gulf coverage
  is uneven. Where there is none, `tier = "client_hosted"` is the mechanism, not a workaround
- **Check `geo_redundant_backup_enabled` against the paired region.** Default pairing may sit
  outside the jurisdiction, moving personal data across the boundary via the backup path
- Size `database_sku` against **tenant aggregate** load, not per-venue. Venue peaks within a
  tenant are correlated — Eid, National Day, school holidays
- `prevent_destroy` on databases and key vaults
- Key vault per cell — a compromise is contained to one tenant

## Placement

Region carries `shared` | `dedicated:{cloud}:{region}` | `client_hosted:{endpoint}`.
A tenant may be **mixed** across regions.

## Migration rollout

Every migration runs **once per cell**. Errors multiply by tenant count.

Canary cell -> 10% -> remainder, gated on health. Version skew between cells is expected;
contracts tolerate N-3 minor versions.

**Rollback tested before merge, not after.**

## Style

Modules parameterised, never copy-pasted per cell · no inline secrets · variables carry
`description` and `validation` — validation catches jurisdiction typos at plan time ·
`fmt` and `validate` blocking in CI · state remote, locked, per environment.

## What is not here

Cross-tenant analytics. The warehouse is fed by per-cell event export of **aggregated,
pseudonymised** data only. Cells are never queried directly.
