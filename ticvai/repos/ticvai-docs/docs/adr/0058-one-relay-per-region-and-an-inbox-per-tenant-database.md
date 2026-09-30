# ADR-0058: One relay per region reads every tenant's outbox, and every consumer has an inbox

**Status:** Accepted · 30 September 2026 · Chinmay Parab
**Date:** 2026-09-30 · **Deciders:** Chinmay Parab
**Finding:** SD-031 (high), with SD-030
**Amends:** ADR-0033 (outbox and dead letters, amended by this ADR) — "a relay process per cell" becomes a relay per region that iterates tenant databases
**Related:** ADR-0038, amended by ADR-0040 (database per tenant) · ADR-0032, pooling amended by ADR-0038 · ADR-0057 (broker, proposed: RabbitMQ or Kafka, the client's choice) · ADR-0056 (partitions)

---

## Context

**The relay was designed before the database-per-tenant decision.**

- ADR-0033 line 81: *"A relay process per cell"*. Written 31 August.
- ADR-0038 (5 September, amended by ADR-0040 on instance count): one database per tenant, 10 at go-live and growing. So there are as many outboxes as tenants.
- A single poller per cell must hold connections to every tenant database. Nothing says how.

**Consumers have nowhere durable to de-duplicate.**

- `events/_schema.yaml:21`: events are delivered at least once and every consumer states its idempotency key.
- `backend/`: no inbox or processed-event table.
- Idempotency today lives only in Redis (SD-024). A Redis loss means duplicate effects.

**The outbox table is not ready to be polled** (SD-030).

- `platform.outbox` (`010-platform.sql:200`) has `published_at` but no index on unpublished rows.
- 68 of 69 events lack `sequence`, so a consumer cannot detect order gaps.
- `aggregate_id` is `uuid` while some aggregate ids are `text` (fixed by ADR-0056).

**Pooling limits the tools.** pgbouncer runs in transaction mode (ADR-0032, pooling amended by
ADR-0038). That forbids `LISTEN/NOTIFY` across transactions and session advisory locks.

---

## Decision

### The relay

- **One logical relay per region**, running in the `workers` deployable (ADR-0055).
- It reads the list of tenant databases in the region from the control plane and runs **one polling loop per tenant database**.
- **A lease per tenant database** (a row in the regional control database, renewed every few seconds) gives each loop to exactly one worker replica. So one publisher per tenant at a time, and order within a tenant holds. If a replica dies, its leases expire and another replica takes them.
- **Each poll is one short transaction:** select up to 200 rows `WHERE published_at IS NULL ORDER BY created_at, id FOR UPDATE SKIP LOCKED`, publish them as a batch with the ordering key = aggregate id (ADR-0057: the Kafka partition key, or the RabbitMQ single-active-consumer or consistent-hash routing key), set `published_at`, commit. The relay publishes through the kernel's `IEventPublisher`, never a broker SDK, so it is the same code whichever broker the client chooses.
- **Adaptive polling:** every 100 ms while rows are found, backing off to 2 s when idle. An idle tenant costs one indexed query every 2 seconds.
- Failures back off and jitter as ADR-0033 says. A tenant database that is down does not stop the others; its loop backs off alone.

### The envelope

Every event carries `eventId` (= the outbox row id, UUIDv7), `eventName`, `aggregateType`,
`aggregateId`, **`sequence` per aggregate** (assigned in the writing transaction), `tenantId`,
`scopePath`, `occurredAt` and `payload`.

### The inbox

- **`kernel.inbox (consumer text, event_id uuid, processed_at timestamptz, PRIMARY KEY (consumer, event_id))`** in every tenant database, range-partitioned by month (ADR-0056).
- The consumer inserts its inbox row **in the same transaction as its effect**, with `ON CONFLICT DO NOTHING`. No row inserted means already processed: skip and acknowledge.
- AI consumers write `ai.inbox` instead, because only AI writes AI tables (ADR-0020, amended by ADR-0049 on where vectors live; this rule is unchanged).
- Retention: 30 days, longer than any redelivery window.

### Order

The broker keeps an aggregate's events in order through the ordering key: one Kafka partition per key,
or one active consumer per RabbitMQ queue shard (ADR-0057). The consumer also checks `sequence`, so
order does not rest on the broker alone. On a gap it
abandons the message for a later retry; a gap that never closes ends in the dead letters, drained
into `platform.dead_letter`, where a person sees it.

**The inbox is the guarantee whichever broker is chosen.** Kafka and RabbitMQ both deliver at least
once; neither one's de-duplication is relied on.

### Outbox housekeeping

- A partial index on `platform.outbox (created_at, id) WHERE published_at IS NULL`.
- Published rows leave with their monthly partition (ADR-0056, ADR-0047).

---

## Options Considered

### Option A: One relay per region, a loop per tenant database, leases (recommended)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. A lease table and a loop manager |
| Cost | Two worker replicas cover a region |
| Scalability | Comfortable to about 200 tenant databases per region, then see Option C |
| Team familiarity | High. Plain SQL and a background service in .NET |
| Time to Block A | Fits sprint 1 weeks 1–2 |

**Pros:** Works through pgbouncer. Keeps per-tenant order. One thing to deploy.
**Cons:** Polling adds latency (up to 2 s after an idle period, about 100 ms when busy).

### Option B: A relay process per tenant database

| Dimension | Assessment |
|---|---|
| Complexity | Low per relay, high in total: one process per tenant to deploy and watch |
| Cost | Grows with tenant count, not load |
| Scalability | Poor. Hundreds of mostly idle processes |
| Team familiarity | High |
| Time to Block A | Fast for 10 tenants |

**Pros:** Simplest code.
**Cons:** Tenant onboarding now deploys a process. Cost follows tenancy, which ADR-0032 already warns against.

### Option C: Logical decoding (change data capture) on the outbox table

| Dimension | Assessment |
|---|---|
| Complexity | High. A replication slot per tenant database; slots retain WAL if the reader stops |
| Cost | Low compute; operational risk on disk |
| Scalability | Best at high tenant counts and volumes |
| Team familiarity | Low |
| Time to Block A | Too slow for sprint 1 |

**Pros:** No polling, lowest latency.
**Cons:** A stalled slot fills the disk of a shared instance. Note: ADR-0033 rejected CDC because it
publishes *what changed, not what happened*. CDC on the **outbox table** publishes what happened, so
that objection does not apply to this option. Kept as the growth path.

### Option D: Each deployable publishes its own outbox rows after commit

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Cost | None extra |
| Scalability | Fine |
| Team familiarity | High |
| Time to Block A | Fast |

**Pros:** Lowest latency. No separate process.
**Cons:** Several publishers per tenant break per-tenant order. A crash after commit leaves rows that still need a sweeper, which is Option A again.

---

## Trade-off Analysis

A and B differ in whether cost follows load or tenancy. A wins. A and C differ in latency and
operational risk; C is the right answer at a scale we do not have, and a stalled replication slot on
a shared instance is a platform outage. D looks cheaper but ends up needing A's sweeper anyway.

The inbox is not optional under any option. At-least-once delivery without a durable inbox is
duplicate tickets and duplicate postings the first time Redis restarts.

---

## Consequences

**Easier**

- One place to watch relay lag per tenant.
- Consumers de-duplicate in the database, in the same transaction as the effect.

**Harder**

- One inbox insert per consumed event.
- The lease table lives in the regional control plane, which is not generated yet (SD-020).

**Revisit**

- Move to Option C when a region passes about 200 tenant databases, or relay lag p95 exceeds 2 s.

---

## Action Items

**Before Monday 5 October 2026** (these change tables the MIG tickets create)

1. [x] Chinmay's yes (30 September 2026).
2. [ ] Package: add `kernel.inbox` (and `ai.inbox`), `sequence` on the outbox, the partial index, and the lease table in the regional control schema; amend ADR-0033's consequences line. Re-derive, mirrors, check. (2 pts)
3. [ ] Package: `x-ticvai-emits` and `sequence` on every event (SD-030, SD-033 are package items; list them as a dependency).

**Sprint 1, weeks 1–2**

4. [ ] **KERNEL-RELAY**: the loop manager, leases, adaptive polling, batch publish. **KERNEL-INBOX**: the consumer wrapper that inserts the inbox row in the effect's transaction. Together with ADR-0057's adapter (built on a local RabbitMQ until the client chooses): 8 pts.
5. [ ] Dashboard and alert: relay lag per tenant database; unpublished rows older than 60 s. (1 pt)
