# Restore Drill

> **Purpose:** Monthly, automated  
> **Owner:** Dinesh  
> **Status:** **Monthly**


Failure raises a **P2**. An untested backup is not a backup.

1. Select a cell on rotation.
2. Provision a scratch Postgres instance **in the same jurisdiction**. Restoring into a convenient nearby region moves personal data across the boundary.
3. PITR-restore to a timestamp roughly 24 hours old.
4. Assert `platform.schema_version` max matches the cell's recorded version.
5. Assert row counts on `orders.sales_order` and `access.scan_event` are within tolerance of the source at that timestamp.
6. **Assert RLS is enforced.** Connect as `ticvai_reporting` without setting `ticvai.scope_paths`; confirm queries return **zero rows**, not everything. This is the check that catches a missing `FORCE ROW LEVEL SECURITY`.
7. Assert money precision: an OMR row round-trips at 3 decimal places.
8. Record RTO actual against target. Destroy the scratch instance.

## Single-tenant restore

A single-tenant restore must not disturb other tenants on the cell. Restore to a scratch instance, then logically copy the tenant schema back.
