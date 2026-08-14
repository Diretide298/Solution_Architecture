# Monthly restore drill

Automated. Failure raises a P2 — an untested backup is not a backup.

1. Select a cell on rotation.
2. Provision a scratch Postgres instance **in the same jurisdiction**. Restoring
   into a convenient nearby region moves personal data across the boundary.
3. PITR-restore to a timestamp ~24h old.
4. Assert `platform.schema_version` max matches the cell's recorded version.
5. Assert row counts on `orders.sales_order` and `access.scan_event` are within
   tolerance of the source at that timestamp.
6. Assert RLS is enforced: connect as `ticvai_reporting` without setting
   `ticvai.scope_paths` and confirm queries return zero rows rather than
   everything. This is the check that would have caught a missing
   `FORCE ROW LEVEL SECURITY`.
7. Record RTO actual against target. Destroy the scratch instance.
