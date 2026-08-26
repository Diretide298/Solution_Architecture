# Schema

> **Purpose:** Tables, keys, indexes, partitioning and RLS  
> **Owner:** Backend + Dinesh  
> **Status:** Baseline applied · spine ERD in progress

One third of the build handoff. See [api-list](api-list.md) and [page-inventory](page-inventory.md).

---

## Universal rules

Every table follows these. They are not per-table decisions.

| Rule | Detail |
|---|---|
| **Schema per module** | `platform` `identity` `catalogue` `orders` `access` `sync` `ledger` `pii`. Each service connects with a role granted only its own schema |
| **Money** | `numeric(18,4)` + `currency_code char(3)` + `currency_scale smallint`. **Never `decimal(18,2)`** — some currencies use 3dp |
| **IDs — edge-created** | `char(26)` ULID, client-generated. Doubles as the idempotency key |
| **IDs — configuration** | `uuid` |
| **Never on a partitioned table** | `bigserial`. A shared sequence is a contention point |
| **Scope** | `scope_path ltree` + denormalised `venue_id`, `region_id`, `brand_id` |
| **Partitioning** | `PARTITION BY LIST (venue_id)` on hot tables. Partition key must be in the PK |
| **RLS** | `ENABLE` **and** `FORCE ROW LEVEL SECURITY`. Without FORCE the owner bypasses every policy |
| **Time** | `timestamptz` UTC. Distinguish `created_at` / `recorded_at` / `synced_at` |
| **Booleans** | `is_`, `has_`, `can_`, `requires_` prefix |

---

## Partitioned vs not

| Partition on `venue_id` | Leave unpartitioned |
|---|---|
| `orders.sales_order` | `catalogue.product` |
| `orders.order_line` | `catalogue.price_list` |
| `orders.payment` | `catalogue.event` |
| `orders.refund` | `identity.principal` |
| `orders.shift`, `orders.cash_movement` | `identity.role`, `identity.grant` |
| `access.scan_event` | `platform.scope_node` |
| `ledger.journal_entry` | `pii.subject` |
| `fnb.order`, `retail.order` | `access.access_point` |

**Reference data stays unpartitioned because it must be visible across venues.** Products,
prices, guests and entitlement definitions are shared; transactions are not.

---

## Applied — `V0001__baseline.sql`

| Object | Purpose |
|---|---|
| Extensions | `ltree` `pgcrypto` `pg_stat_statements` `vector` |
| Schemas | 8, with per-module roles and default privileges |
| `platform.scope_node` | 7-level tree, GiST index on `path` |
| `platform.region_settings` | Country, currency, **scale**, timezone, fiscal year, placement |
| `platform.in_scope(ltree)` | RLS predicate — target at or beneath a granted path |
| `platform.outbox` | Publication atomic with the state change |
| `platform.schema_version` | Per-cell register the orchestrator reads |
| `orders.sales_order` | Partitioned, ULID PK, RLS + FORCE, idempotency unique index |
| `access.scan_event` | Partitioned, ULID PK, RLS + FORCE |
| `pii` schema | Separately erasable. Ledger references opaque `subject_id` |

**The `pii` split is what reconciles an append-only ledger with erasure obligations.**
Erasure deletes the `pii` row; the ledger keeps its integrity with an orphaned but valid
reference.

---

## To design — spine

| Module | Tables | Notes |
|---|---|---|
| `identity` | `principal` `role` `principal_role` `grant` `session_audit` `password_policy` | `grant` = `(principal_id, permission, scope_path, effect)`. GiST on `scope_path` |
| `catalogue` | `product` `component` `attribute` `attribute_value` `product_variant` `price_list` `price` `event` `performance` `envelope` `data_mask_field` `data_mask_value` | **`product_variant` is materialised**, regenerated on axis change |
| `catalogue` | `bundle` `bundle_delta` | **C102.** Version, signature, content hash |
| `catalogue` | `lease` `lease_unit` | **C103.** TTL, holder, sub-lease parent |
| `orders` | `sales_order` `order_line` `payment` `refund` `void` `reservation` `shift` `deposit_box` `cash_movement` | All partitioned |
| `access` | `access_point` `admission_profile` `scan_event` `blacklist` `offline_package` | |
| `ledger` | `account` `journal_entry` `journal_line` `tax_code` `recognition_schedule` `allocation_split` `legal_entity` `fiscal_period` `settlement` `price_variance` | `price_variance` pending **CF-38** |
| `platform` | `guest_link` `redemption_right` `wallet_allocation` | **Cross-cell. Wave 1 per ADR-0014** |
| `pii` | `subject` `subject_contact` `subject_document` `consent` | Erasable |

---

## Two decisions that shape the schema

### Data mask — `JSONB` + registry, never dynamic DDL

```sql
CREATE TABLE catalogue.data_mask_field (
    id            uuid PRIMARY KEY,
    scope_kind    text NOT NULL,        -- account | event | ticket | metric_cell
    code          text NOT NULL,
    data_type     text NOT NULL,
    labels        jsonb NOT NULL,       -- multi-language
    validation    jsonb,
    value_set_id  uuid,
    is_queryable  boolean NOT NULL DEFAULT false
);
```

Values live in a `JSONB` column on the owning entity. **GIN index only on paths declared
`is_queryable`.** Dynamic DDL per tenant field makes migrations unrunnable at N cells.

### Component / attribute — materialised variants

Template + axes + a materialised `product_variant` table, regenerated on axis change.
A static product table cannot express it; pure runtime expansion kills pricing queries.

---

## Index strategy

| Pattern | Example |
|---|---|
| Partition-local lookup | `(venue_id, created_at DESC)` |
| Idempotency | `UNIQUE (venue_id, idempotency_key)` |
| Scope containment | `USING gist (scope_path)` |
| Data mask queryable paths | `USING gin ((mask_values -> 'path'))` |
| Foreign keys | **Every FK indexed** |
| Ledger period close | `(fiscal_period_id, account_id)` |

---

## Migration rules

- Forward-only, numbered, checksummed, per-cell version register
- **Test rollback before merge**, not after
- `CREATE INDEX CONCURRENTLY` where available
- Resumable — an interrupted migration must be safe to re-run
- Canary cell → 10% → remainder, gated on health
- **Every migration runs once per region.** Errors multiply by cell count

---

## Files

`ticvai-backend/src/Ticvai.Migrations/Scripts/` — `V0001__baseline.sql` applied.
