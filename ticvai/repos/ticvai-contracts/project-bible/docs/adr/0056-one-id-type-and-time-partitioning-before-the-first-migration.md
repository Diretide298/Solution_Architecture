# ADR-0056: One id type, and time partitioning first, fixed before the first migration

**Status:** Accepted · 30 September 2026 · Chinmay Parab
**Date:** 2026-09-30 · **Deciders:** Chinmay Parab
**Finding:** SD-010 (high), with SD-012 and SD-009
**Amends:** ADR-0044 (which tables partition by venue, amended by this ADR) — venue partitioning is deferred, not cancelled · ADR-0005 (venue isolation, amended by this ADR) — isolation in release 1 comes from RLS, not partitions
**Related:** ADR-0047 (retention) · ADR-0033 (outbox) · ADR-0058 (relay and inbox)

---

## Context

**Primary keys are cheap to change before data exists and expensive after.** The MIG tickets
(MIG-BASELINE and 33 `MIG-*` tickets in `handoff/service-docs/tasks.csv`) generate tables from
`tools/derive-ddl.py`. Whatever shape they have on 5 October is the shape the data lands in.

**ADR-0044 is accepted and not implemented.**

- Signed off 18 September: `venue_id NOT NULL` implies `PARTITION BY LIST (venue_id)`, `venue_id` leading the primary key, and composite foreign keys into it. 85 tables partition and **74 tables gain a `venue_id` column**.
- `backend/tenant/*.sql`: **0 occurrences of `PARTITION BY`**. `930-partitioning.sql` lines 4–7 say *"the tables declare their own partitioning where they are created"*. They do not.

**The tables that grow, grow with time, not with venues.** None of them has an inbound foreign key
(`900-foreign-keys.sql`: 0 references to each):

| Table | Where | Id today | Time column |
|---|---|---|---|
| `access.scan_event` | `010-access.sql:1497` | `text` | `recorded_at` |
| `platform.outbox` | `010-platform.sql:200` | `uuid` | `created_at` |
| `platform.dead_letter` | `010-platform.sql:99` | `uuid` | `created_at` |
| `platform.audit_record` | `010-platform.sql:18` | `uuid` | `occurred_at` |
| `ledger.journal_line` | `010-ledger.sql:252` | `uuid` | **none** |
| `marketing.message_dispatch` | `010-marketing.sql:1312` | `text` | `queued_at` |

List-by-venue does nothing for any of these. A range partition by month does, and it needs no
composite keys because nothing points at them.

**Id types are mixed** (SD-012): 980 `uuid`, 79 `text` and 9 `jsonb` primary keys. `orders.sales_order.id`
is `text` (`010-orders.sql:1288`), but `platform.outbox.aggregate_id` is `uuid`, so the outbox cannot
record an order. Transport ids are `jsonb PRIMARY KEY` (SD-009). `data-model.md:56` says *"ULID `char(26)`
for edge-created entities; UUID for configuration"*. The starter kernel's `UlidGenerator` returns a
26-character string.

---

## Decision

**Decided 30 September 2026: one id type and time partitioning first.** This changes what Chinmay
signed on 18 September (ADR-0044, now amended), and he accepted that change.

**Why the team matters here.** The decision was checked against the developers' skills matrix
(`docs/active/team.json`): PostgreSQL ratings top out at 3 and most are 2. Composite keys on 85
partitioned tables touch every query in 17 modules, and that is work for people rated 4 or 5. With
this team, composite keys everywhere is the riskier path; plain range partitions and one id type are
not.

### 1. Every id column is `uuid`. New ids are UUIDv7.

- UUIDv7 (RFC 9562) starts with a millisecond timestamp, like a ULID. It sorts by time and keeps index inserts local.
- It is 16 bytes in a native type, against 26+ bytes of `text`.
- It is generated in one place: a kernel `Id.New()`. Offline clients (POS, scanner, guest app) generate the same format.
- Where a person reads or types an id, show a separate human code (`order_number`, ticket code). Never the raw id.
- The 79 `text` and 9 `jsonb` id columns, and every foreign key to them, become `uuid`.

A ULID stored in a `uuid` column would work equally well; the bits are the same. UUIDv7 is preferred
because the tooling already speaks it: Postgres 18 has `uuidv7()`, .NET 9 and later have
`Guid.CreateVersion7()`, and the `uuid` npm package has `v7`. **The part that is not negotiable is one
type.**

### 2. Release 1 partitions the time-driven tables by month.

- `PARTITION BY RANGE` on the time column, monthly, for the six tables above, plus `kernel.inbox` (ADR-0058).
- `ledger.journal_line` gains `posted_at`, copied from its journal entry.
- The primary key becomes `(id, <time column>)`. No foreign key changes, because nothing references these tables.
- A kernel job creates partitions three months ahead. Retention (ADR-0047) detaches and archives whole partitions instead of deleting rows.
- The rule lives in `derive-ddl.py` and is read from the schema: **append-only, has a time column, no inbound foreign key → range partition by month.** Like ADR-0044's rule, it cannot drift from the schema.

### 3. Venue list partitioning is deferred, not cancelled.

- `venue_id NOT NULL` stays where it is. The 74 extra columns are not added now.
- Where a child table already carries `venue_id` (25 tables), add the composite foreign key now. The parent needs only `UNIQUE (venue_id, id)`, which is cheap. This keeps most of ADR-0044's cross-venue guarantee.
- Venue isolation on reads comes from RLS (ADR-0005's other half).
- **Revisit trigger:** a tenant with more than 100 venues, or one venue that needs its own vacuum or archive. Because each tenant has its own database, a later move is a table rewrite in one tenant's maintenance window, not a platform migration.

---

## Options Considered

### Option A: Implement ADR-0044 in full now

| Dimension | Assessment |
|---|---|
| Complexity | High. 85 partitioned tables, 74 new columns, composite keys everywhere |
| Cost | Most of a sprint of generator and migration work before any feature |
| Scalability | Venue pruning. Does nothing for the tables that grow with time |
| Team familiarity | Low. Composite keys touch every query in 17 modules |
| Time to Block A | Slows MIG and every service ticket that writes those tables |

**Pros:** Database-enforced cross-venue integrity everywhere. Honours the 18 September sign-off.
**Cons:** Largest cost, smallest effect on growth. Every partitioned table needs a DEFAULT partition.

### Option B: Time partitioning first, one id type, venue partitioning later (recommended)

| Dimension | Assessment |
|---|---|
| Complexity | Low. Six tables plus the inbox, no foreign key changes |
| Cost | About 3 points of generator work, 3 points for the partition job |
| Scalability | Partitions where the growth is. Retention drops partitions |
| Team familiarity | High. Plain range partitions, one id type |
| Time to Block A | Fits before 5 October |

**Pros:** Cheap. Directly serves retention and the outbox. Fixes the id mismatch.
**Cons:** Cross-venue integrity is partly enforced by the application until venue partitioning comes.

### Option C: No partitioning in release 1; fix only the id type

| Dimension | Assessment |
|---|---|
| Complexity | Lowest |
| Cost | Lowest now; a rewrite of the big tables later |
| Scalability | Deletes instead of partition drops; vacuum pressure on `scan_event` and `outbox` |
| Team familiarity | High |
| Time to Block A | Fastest |

**Pros:** Nothing to build.
**Cons:** The tables that need partitions are exactly the ones that are painful to convert once full.

---

## Trade-off Analysis

A buys a correctness property (no cross-venue references) at a cost paid by every table and query.
B buys the performance and retention property that matters in the first year and keeps most of the
correctness with composite keys where `venue_id` already exists. C saves three points now and costs
a rewrite of the busiest tables later.

On ids, the choice between ULID-in-uuid and UUIDv7 is small. The choice between one type and three
is not: mixed types already broke the outbox.

---

## Consequences

**Easier**

- The outbox can reference every aggregate.
- Retention is a partition detach, not a mass delete.
- Ids sort by time everywhere, online and offline.

**Harder**

- `data-model.md:56` and the offline-core generator change from ULID strings to UUIDv7.
- A cross-venue reference between tables without `venue_id` is caught by the application, not the database, until venue partitioning.

**Revisit**

- Venue partitioning at the trigger above.
- The 37 nullable-`venue_id` tables stay unpartitioned under any option (ADR-0044's own reasoning).

---

## Action Items

**Before Monday 5 October 2026** (the MIG tickets depend on it)

1. [x] Chinmay's yes, including the change to what was signed on 18 September (30 September 2026).
2. [ ] `derive-ddl.py`: every id column `uuid`; the range-partition rule; `journal_line.posted_at`; composite keys where `venue_id` already exists; header of `930-partitioning.sql`. Re-derive in `tools/refresh.sh` order, then mirrors, then `check-package`. (3 pts)
3. [x] Amend ADR-0044's status line and ADR-0005's consequences; update `data-model.md:56` (30 September 2026).
4. [ ] Fix transport keys (SD-009) and `outbox.aggregate_id` in the same regeneration.

**Sprint 1**

5. [ ] **KERNEL-ID**: replace `UlidGenerator` with `Id.New()` (UUIDv7, big-endian into `Guid` so Postgres order is time order); same generator in `offline-core`. (2 pts)
6. [ ] **MIG-PARTITIONS**: the job that creates monthly partitions ahead and detaches expired ones per ADR-0047. (3 pts)
