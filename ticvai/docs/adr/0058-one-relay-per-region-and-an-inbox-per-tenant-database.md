# ADR-0058: One relay per region reads every tenant's outbox, and every consumer has an inbox

**Status:** Accepted · 30 September 2026 · Chinmay Parab · **amended 1 October 2026** (relay throughput, the two publishing interfaces, republish from the outbox: see the amendment at the end)
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
- **Each poll is one short transaction:** select up to 200 rows (a configurable batch size since the 1 October amendment: 1,000 in the burst environment) `WHERE published_at IS NULL ORDER BY created_at, id FOR UPDATE SKIP LOCKED`, publish them as a batch with the ordering key = aggregate id (ADR-0057: the Kafka partition key, or the RabbitMQ single-active-consumer or consistent-hash routing key), set `published_at`, commit. The relay publishes through the kernel's broker-side interface (`IBrokerPublisher` since the 1 October amendment; modules enqueue through `IOutbox`), never a broker SDK, so it is the same code whichever broker the client chooses.
- **Adaptive polling:** every 100 ms while rows are found, backing off to 2 s when idle. **Amended 1 October: a full batch polls again at once.** An idle tenant costs one indexed query every 2 seconds.
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

---

## Amendment — relay throughput, the two publishing interfaces, and republish from the outbox, 1 October 2026

**Status unchanged: Accepted.** Source: the broker decision pack (`docs/active/broker-decision-pack.md`,
appendix sections B, C and D, risks R3 and R8). All three hold whichever broker the client chooses.

### 1. The relay drains a full batch, and the batch size is per environment

**The problem.** The decision above reads up to 200 rows a poll and polls every 100 ms while rows are
found. That caps one tenant database at **200 / 0.1 s = 2,000 events a second, less the publish time**
(about 1,500–1,700 once a cycle's own 20–35 ms is added). A flash sale is one tenant in one database
(ADR-0035) and publishes **2,270 events a second at the burst design load and 2,850 at the 20-minute
on-sale peak** (the pack, section C: 10 events a buyer at 227–285 buyers a second). The relay, not the
broker, would be the first ceiling.

**Decision.**

- **Drain loop.** When a poll returns a full batch, the loop polls again **at once**. A partial batch
  waits the busy interval (100 ms). An empty poll backs off, doubling, to the idle interval (2 s).
  Unchanged: one loop per tenant database under its lease, so one publisher per tenant, and order holds.
- **The batch size is configuration, not code**: `Relay:BatchSize`, **200 in the shared cells, 1,000 in
  the flash-sale burst environment** (set in the burst environment's warming state, ADR-0035), at most
  5,000. The intervals are `Relay:BusyInterval` and `Relay:IdleInterval`. The starter carries the rule
  as `RelayOptions` and `RelayPacing` (`TICVAI.Infrastructure/Messaging`), with tests.
- **The broker adapter awaits confirms for the batch together**, not one round trip per message
  (`IBrokerPublisher.PublishBatchAsync`). A batch that is not wholly confirmed stays unpublished and is
  sent again; the inbox absorbs the duplicates.

**The resulting ceiling, and how it was estimated.** A drained loop runs cycles back to back, so its
ceiling is batch size ÷ cycle time. One cycle is select → publish and await confirms → set
`published_at` → commit, modelled as a fixed cost per cycle plus a cost per row:

- **Fixed, 10–15 ms:** the select through pgbouncer on the partial index (1–2 ms), the broker's confirm
  round trip for the batch across zones (5–10 ms on three-node quorum queues), the update and commit
  (2–4 ms with a zone-redundant standby).
- **Per row, 50–100 µs:** reading and serialising about 1.2 KB, sending it, its share of the confirm,
  and updating the row out of the partial index.

These are planning figures from typical PostgreSQL and RabbitMQ latencies inside one Azure region, not
measurements.

| Relay | Batch | Cycle | Ceiling per tenant database |
|---|---:|---:|---:|
| As decided on 30 September (100 ms wait after every batch) | 200 | 100 ms + 20–35 ms | **1,500–1,700/s** (2,000 at most) |
| Drained | 200 | 20–35 ms | **5,700–10,000/s** |
| **Drained, burst environment** | **1,000** | **60–115 ms** | **8,700–16,700/s** |
| Drained, broker confirms slowed to 50 ms under load | 200 | 65–75 ms | 2,700–3,100/s |
| Drained, broker confirms slowed to 50 ms under load | 1,000 | 105–155 ms | 6,500–9,500/s |

**Against the need:** 2,270–2,850 events/s at the peak, and **3,500/s in the load test**. Draining alone
clears the peak while the broker is healthy. The larger batch keeps the margin when the broker is the
slow part: with confirms at 50 ms a 200-row batch sits at the peak, a 1,000-row batch at two to three
times it. **Plan on 8,700 events/s per tenant database in the burst environment** (the low end), about
three times the 20-minute peak.

**What the larger batch costs.** One transaction holds locks on up to 1,000 outbox rows for about
100 ms. Writers only insert outbox rows, and one loop per tenant takes them (`SKIP LOCKED`), so nothing
waits on those locks. A failed batch re-sends up to 1,000 rows, which the inboxes skip. Event latency
in a drained burst is about two cycles, 0.1–0.25 s.

**Measured, not assumed:** the sprint-2 load test runs one tenant at 3,500 events/s published and
records relay cycle time, batch fill and relay lag (age of the oldest unpublished row). If lag p95
passes 2 s at that rate, the trigger to revisit (Option C) is met early.

### 2. Two interfaces, not one

The decision above has the relay publish "through the kernel's `IEventPublisher`", while the starter's
`IEventPublisher` enqueued to the outbox inside the caller's transaction. Those are two contracts, now
two interfaces (in the starter, `TICVAI.Application/Abstractions/Messaging`):

| Interface | Caller | Does |
|---|---|---|
| `IOutbox.EnqueueAsync(IIntegrationEvent)` | modules | writes `platform.outbox` in the caller's transaction; never talks to the broker |
| `IBrokerPublisher.PublishBatchAsync(IReadOnlyList<EventEnvelope>)` | the relay only (and the republish below) | sends a batch keyed by aggregate id and returns when the broker has confirmed all of it; one adapter per broker |

`IIntegrationEvent` now carries the whole envelope above: `EventId`, `EventName`, `EventVersion`,
`AggregateType`, **`AggregateId`, `Sequence`, `ScopePath`**, `TenantId`, `OccurredAt`. The consumer
side (subscribe by consumer name and event names; settle as `Ack`, `RetryLater`, `DeadLetter` or
`Halt`) is PLATFORM-OUTBOX's to add, in the same folder. The name `IEventPublisher` is retired.

### 3. Republish from the outbox, by tenant and time range

**Why.** The relay marks a row published once the broker confirms it. If the broker is then lost or
rebuilt, or a DR failover starts an empty broker in the other region (ADR-0060, which assumes this
capability), every message the broker held but no consumer had settled is gone, and nothing would send
it again (the pack's risk R8). The outbox still has every row. The same tool recovers a queue purged by
mistake.

**What it does.** A person asks for one tenant database's outbox rows with `created_at` in
`[from, to)`, optionally only some event names. The relay loop that holds that tenant's lease reads them
in `(created_at, id)` order, in batches of `Relay:BatchSize`, with a keyset cursor, and publishes them
through `IBrokerPublisher`, **whether or not they were published before**. Every consumer's inbox skips
what it already handled; what it never saw arrives in sequence order.

- **It does not touch `published_at`.** The first publication stays on record, and the hot partition is
  not rewritten, so the partial index of unpublished rows stays small.
- **Live events come first.** The loop alternates one republish batch with each live batch, so a
  republish never holds up today's tickets. A live event whose aggregate still has older events waiting
  in the republish range sees a sequence gap at its consumer, is retried later, and goes through once
  the republish reaches the older one. So **`from` must be early enough**: the moment the oldest message
  still held by the lost broker was published. When that is unknown, the time of the loss minus one
  hour, or the start of any consumer halt then in progress, whichever is earlier. Too early costs
  duplicates the inboxes absorb; too late loses events.
- **One republish per tenant at a time.** A second request for a tenant with one queued or running is
  refused. A cancelled or failed job keeps its cursor, so a new request can start where it stopped.
- **Only the hot outbox.** Rows whose monthly partition is archived to Blob (ADR-0047, ADR-0056) are
  outside it; a range reaching into them is refused. Republishing from the archive is not built.
- **Recorded.** The job row in the regional control database (`control.outbox_republish`, beside the
  lease table `control.outbox_relay`) holds tenant, range, event names, reason, requester, status,
  cursor and rows published; the request also goes to the audit trail.
- **DR runbook.** After a failover, one request per promoted tenant database, `from` as above and `to`
  the time of the request. The inboxes came over with the databases, so duplicates are skipped there
  too.

**The contract operations are not added yet**: the contracts are being edited in parallel. The proposal
is action item 10.

### What it changes in the action items

Actions 1–5 stand. Action 4's KERNEL-RELAY takes the drain loop and the batch size. Added:

**Sprint 1, weeks 1–2**

6. [x] Starter kernel: `IOutbox` and `IBrokerPublisher` (the split of `IEventPublisher`), the envelope on
   `IIntegrationEvent`, `RelayOptions` and `RelayPacing` with tests, and `backend-patterns` 3.5
   (1 October 2026).
7. [ ] Package: retire the name `IEventPublisher` where it still stands (ADR-0033 and ADR-0057 were
   changed with this amendment): the comment in the four `deploy/*.yml`, the PLATFORM-OUTBOX task
   text (`docs/active/block-a-extra-tasks.json`, which feeds `handoff/service-docs/tasks.csv`), and
   `repos/ticvai-backend/src/Ticvai.Shared.Kernel/Abstractions/IIntegrationEvent.cs` (that older
   scaffold does not build today: 22 analyzer errors). Re-derive, mirrors, check.
8. [ ] Burst environment: `Relay__BatchSize=1000` on the `workers` host in the burst environment's
   configuration (Terraform or Helm values; `deploy/c-flash-sale.yml` has no `workers` service yet).

**Sprint 2**

9. [ ] Load test: one tenant at 3,500 events/s published; record relay cycle time, batch fill and lag
   p95. Alert when a tenant's batches come back full for more than 60 s running: the relay is at its
   ceiling. (Inside the load-test ticket.)

**Before the first DR drill (ADR-0060)**

10. [ ] Package, **platform-ops contract** (served by the `operations` host; carried out by the relay in
    `workers`): add the republish operations below, the `control.outbox_republish` table derived from
    them, and a task in the development plan, **PLATFORM-REPUBLISH, 3 pts**, after KERNEL-RELAY.
    **Authored 1 October**: the four operations and `OutboxRepublish`/`OutboxRepublishRequest` in
    `contracts/satellite/platform-ops.yaml`, on P09 ADM-318 until republish has a screen of its own, the state
    model `states/outbox-republish.yaml`, and hand-mapped lineage; `control.outbox_republish` is derived at the
    next refresh.

    | Operation | Method and path | Permission | Notes |
    |---|---|---|---|
    | `republishOutbox` | `POST /outbox-republishes` | `PLATFORM_CELL_MANAGE` | Body `OutboxRepublishRequest`: `tenantId` (uuid, required), `from` and `to` (date-time, required, `from` < `to` ≤ now), `eventNames` (string[], catalogue names, optional: every event when absent), `reason` (string, required, up to 500). `Idempotency-Key` required. `202` with `OutboxRepublish` and `X-Consistency-Token`. Own errors: `409` `republish-in-progress` (the tenant has one queued or running); `422` `outbox-range-archived` (`from` is older than the oldest hot outbox partition). An unknown event name is the shared `400` `validation`. Scope level `platform`, audience `staff`, offline `false`, conflict policy `append`. Consumed by P09 ADM-318 Dead Letters until it has a screen of its own |
    | `listOutboxRepublishes` | `GET /outbox-republishes` | `PLATFORM_CELL_VIEW` | Filters `tenantId`, `status`; `PageSize` and `PageCursor`; read routing `replica`; newest first |
    | `getOutboxRepublish` | `GET /outbox-republishes/{republishId}` | `PLATFORM_CELL_VIEW` | Progress: `status`, `cursorAt`, `rowsPublished` |
    | `cancelOutboxRepublish` | `POST /outbox-republishes/{republishId}/cancel` | `PLATFORM_CELL_MANAGE` | Stops after the current batch and keeps the cursor. `Idempotency-Key` required. `409` `republish-finished` when it has already completed, failed or been cancelled. Conflict policy `serverWins` |

    `OutboxRepublish` (`x-ticvai-persistence: control.outbox_republish`): `id` (uuid), `tenantId`,
    `from`, `to`, `eventNames`, `reason`, `status` (`queued`, `running`, `completed`, `failed`,
    `cancelled`), `cursorAt` (date-time, how far it has got), `rowsPublished` (integer), `lastError`,
    `requestedBy` (the principal), `requestedAt`, `startedAt`, `finishedAt`. Both permissions exist in
    `shared/permissions.yaml`; they are the ones `listDeadLetters` and `replayDeadLetter` use.
