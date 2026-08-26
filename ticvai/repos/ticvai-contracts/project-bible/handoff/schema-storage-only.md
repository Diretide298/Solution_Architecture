# Tables that exist only in storage

**Twelve tables are in the migrations and not in the schema reference.** Every one is correct.
They are recorded here so the difference reads as a decision rather than an omission.

The schema reference derives from the API contracts. A table with no API representation
cannot appear there — and some tables should have no API representation.

| Table | Why it has no contract schema |
|---|---|
| `platform.schema_version` | The migration runner's own bookkeeping. Exposing it would let a tenant read platform internals |
| `platform.outbox` | Transactional outbox. Published events have contracts; the outbox row does not |
| `platform.venue_settings` | Venue configuration is read through `tenancy` operations that return a composed view, not this row |
| `platform.sale_board_page`, `platform.sale_board_tile` | Child tables of `sale_board`, which the API returns as one nested object. The split is a storage decision |
| `platform.device_heartbeat` | High-volume, short-lived. The API returns current status; the history is operational and trimmed |
| `identity.principal_credential` | **Deliberately absent from every API.** A credential hash has no response it belongs in |
| `identity.role_permission` | Child of `role`, returned nested |
| `identity.mfa_recovery_code` | Hashed and single-use. Returned once at enrolment and never retrievable — a recovery code that can be re-read is a second password |
| `identity.authz_audit` | Written by the platform, read through reporting. No direct API |
| `orders.sales_order_unassigned`, `access.scan_event_unassigned` | **Default partitions.** Not tables in the modelling sense — they catch rows whose `venue_id` matches no configured partition, so a misconfiguration is loud rather than silently lossy |

## The general rule

Three kinds of table legitimately have no contract schema:

**Child tables the API returns nested.** One API object, several tables. The reference records
the parent; the children are a normalisation decision.

**Tables nothing may read over HTTP.** Credential hashes, recovery codes, the outbox. Absence
from the API is the security control.

**Infrastructure.** Default partitions, version bookkeeping, heartbeat history.

**A table appearing here that fits none of the three is a gap, not a decision.** All twelve
currently fit.
