# ADR-0057: Events travel on RabbitMQ or Kafka, behind one kernel interface

**Status:** Proposed · waiting on the client's choice between RabbitMQ and Kafka
**Date:** 2026-09-30 · **Deciders:** Chinmay Parab; the broker itself is the client's choice · **Consulted:** Dinesh (infrastructure)
**Finding:** SD-032 (blocker)
**Completes:** ADR-0033 (outbox and dead letters, amended by ADR-0058), which says the relay publishes "to the broker" and never names one
**Related:** ADR-0058 (relay and inbox) · ADR-0046 (on-premise) · ADR-0055 (deployables)

---

## What is decided and what is not

**Decided 30 September 2026 (Chinmay Parab):**

- The broker is **RabbitMQ or Kafka**. Not Azure Service Bus.
- The **kernel interface** (`IEventPublisher`, `IEventSubscriber`), the envelope, per-aggregate ordering, the dead-letter drain and the inbox. None of these depends on which broker is chosen.
- **Local development runs a RabbitMQ container** until the client answers.

**Not decided:** which of the two runs in the cloud. That question goes to the client. We need the
answer **before sprint 1 week 2 (Monday 12 October)**, so the relay is proven end to end by the
23 October checkpoint. Our recommendation is below: RabbitMQ.

---

## Context

**No broker has been chosen or deployed.**

- ADR-0033 (amended by ADR-0058) line 37: the relay publishes at-least-once *"to the broker"*.
- `deploy/a-independent-tenant.yml`, `b-shared-platform.yml`, `c-flash-sale.yml`, `d-venue-local-offline.yml`: Postgres, Redis, pgbouncer and services. No broker until 30 September.
- No ADR or architecture document named one.

**Block A checkout depends on it.** `order.paid` has three critical consumers: entitlements, ledger
and inventory. The review's pace checkpoint (23 October) asks for one guest-web purchase end to end,
producing a ticket and a ledger entry.

**What the broker must do.**

- Run in Azure UAE North, or beside it, with data kept in the region (residency, ADR-0038 as amended by ADR-0040).
- Keep order per aggregate (an order's events arrive in sequence).
- At-least-once delivery with dead letters. `events/_schema.yaml:21` already requires every consumer to state its idempotency key.
- Serve .NET and Python (`ticvai-ai`) consumers.
- Have an on-premise equivalent. The venue-local profile (ADR-0046) needs RabbitMQ anyway.
- Be run by the team we have: 14 people, .NET and PostgreSQL, **no dedicated platform engineer**. In the developers' skills matrix **nobody rated Kafka or RabbitMQ**, and Kubernetes tops out at 2.

**Volume is modest.** 69 events. A large cell peaks at about 7,000 rps, mostly reads. Events are a
fraction of writes: hundreds per second at peak, perhaps low thousands during an on-sale in a burst
environment. Both brokers handle that with room to spare.

---

## Decision

### Decided now, whichever broker is chosen

- **One interface in the kernel.** Modules publish and subscribe through `IEventPublisher` and `IEventSubscriber`, never through a broker SDK. The relay (ADR-0058) publishes through the same interface. Swapping the broker is an adapter, not a change to any module.
- **The envelope** is ADR-0058's: `eventId` (UUIDv7, ADR-0056), `eventName`, `aggregateType`, `aggregateId`, `sequence`, `tenantId`, `scopePath`, `occurredAt`, `payload`. Tenant id travels in the envelope and as a header. **No topic or queue per tenant**: tenants grow, and isolation already comes from the tenant database.
- **Per-aggregate order through an ordering key = `aggregateId`.**
  - Kafka: the partition key. One partition keeps one aggregate's events in order.
  - RabbitMQ: a consistent-hash exchange on the key, with **single active consumer** on each shard queue, so one consumer at a time reads a shard in order.
  - Either way the consumer also checks `sequence` (ADR-0058) and does not rely on the broker alone.
- **Dead letters drain into `platform.dead_letter`.** After the retry budget of ADR-0033, a message goes to the broker's dead-letter place (a RabbitMQ dead-letter exchange, or a Kafka dead-letter topic written by the consumer wrapper). A worker drains it into `platform.dead_letter`, where `replayDeadLetter` already works. Financial postings and DSARs halt and alert instead (ADR-0033).
- **The inbox (ADR-0058) is the guarantee.** Both brokers deliver at least once. Duplicate filtering by the broker, where it exists, is a first filter only.
- **Local development and the venue-local profile run RabbitMQ.** A RabbitMQ container is in the local and venue-local deploy configurations now. Until the client answers, the kernel adapter is built and tested against it.

### For the client: RabbitMQ or Kafka in the cloud

**Our recommendation is RabbitMQ**, ideally as a **managed service in Azure UAE North, if one
exists there** (check availability, for example CloudAMQP on Azure, before relying on it). If no
managed offer serves the region, a three-node quorum cluster that we run is the fallback, and that
cost is stated below.

**Kafka only if the client wants replayable event streams**, for example to feed analytics
directly from the broker. The Azure-native way to get the Kafka API is Event Hubs; Confluent Cloud is
the other. Check UAE North availability and the tier that carries the Kafka endpoint for either.

---

## Options Considered

### Option A: RabbitMQ (recommended)

| Dimension | Assessment |
|---|---|
| Complexity | Low to medium. Queues, dead-letter exchanges, retries with delay, single active consumer. A queue problem solved by a queue |
| Cost | Low for a managed plan at our volume. If self-run: a three-node quorum cluster, and the people cost of running it |
| Scalability | Far above our volume (hundreds of events per second, low thousands in an on-sale) |
| Team familiarity | Nobody rated it in the skills matrix. Simpler to learn than Kafka: the concepts map onto what the outbox and dead-letter tables already do |
| Time to Block A | Fast. It is already the local and venue-local broker, so cloud, local and on-premise are one broker and one adapter |

**Pros:** One broker everywhere: cloud, developer machines and the venue-local profile (ADR-0046). Dead letters and delayed retries are built in. Small operational surface.
**Cons:** No first-party managed RabbitMQ in Azure; a managed plan in UAE North must be confirmed. No replay of old messages (the outbox partitions are the record, ADR-0056, so this is acceptable).

### Option B: Kafka (managed: Event Hubs with the Kafka API, or Confluent Cloud)

| Dimension | Assessment |
|---|---|
| Complexity | Medium to high. A log, not a queue: partitions, consumer groups, offsets and checkpoints. No per-message dead letter; retries and dead-letter topics are ours to build |
| Cost | Event Hubs is cheap per throughput unit at our volume; Confluent Cloud is the most expensive option and a second vendor contract |
| Scalability | Highest. Built for telemetry-scale streams we do not have |
| Team familiarity | Low. Nobody rated it; partition and offset semantics are new to the team |
| Time to Block A | Slower. The retry and dead-letter path must be built before `order.paid` is safe |

**Pros:** Replayable streams. Industry standard for event streaming. Event Hubs is Azure-native.
**Cons:** Solves a volume problem we do not have and leaves the retry and dead-letter problem we do have. The venue-local profile still needs RabbitMQ, so there are two brokers and two adapters to test.

### Option C: Azure Service Bus

Recommended in the first draft of this ADR. **Ruled out by Chinmay on 30 September**: the broker is
RabbitMQ or Kafka.

---

## Trade-off Analysis

The workload is business events with per-aggregate order and a strong need for dead letters and
retries. That is a queue problem. RabbitMQ solves it with built-in features; Kafka solves a stream
problem and leaves retries to us.

The team decides the rest. With 14 people, no platform engineer, nobody rated on either broker and
Kubernetes at 2 at most, the broker with fewer moving parts is the safer one. RabbitMQ is also
already required on-premise, so choosing it in the cloud means one broker to learn, one adapter to
test and one runbook.

Kafka's real advantage is replay. The outbox is already partitioned by month (ADR-0056), so
analytics can read history from there. Kafka is worth its cost only if the client wants the broker
itself to be a replayable stream.

A .NET messaging library could implement the interface. Wolverine and MassTransit both support
RabbitMQ and Kafka; MassTransit v9 moved to a commercial licence, so check licence terms before
adopting either. A thin adapter over the official client is also enough for 69 events.

---

## Consequences

**Easier**

- Development starts on 5 October on a local RabbitMQ; nothing waits for the client's answer except the cloud provisioning.
- Modules never see the broker, so the client's answer changes one adapter and the infrastructure code.
- If the client chooses RabbitMQ, cloud and venue-local run the same broker.

**Harder**

- The cloud broker is not provisioned until the client answers. If the answer is late, the 23 October end-to-end proof runs on a RabbitMQ we host in dev.
- If the client chooses Kafka: two brokers to test (Kafka in the cloud, RabbitMQ in the venue-local profile), and the retry and dead-letter path is ours to build.

**Revisit**

- If events need replay for analytics, feed a warehouse from the outbox partitions (ADR-0056), not from the broker.
- If a region passes about 200 tenant databases, see ADR-0058's logical-decoding trigger.

---

## Action Items

**Before Monday 12 October 2026 (sprint 1, week 2)**

1. [x] Chinmay: broker is RabbitMQ or Kafka, not Service Bus; the question goes to the client (30 September).
2. [ ] Client: choose RabbitMQ or Kafka for the cloud event broker (asked in the Decisions Register, "For you to answer").
3. [ ] Dinesh: check a managed RabbitMQ in Azure UAE North (and, if the client leans to Kafka, Event Hubs' Kafka endpoint or Confluent Cloud there), with prices.
4. [x] Package: name the broker question in ADR-0033; add RabbitMQ to the four `deploy/*.yml` as the local and venue-local broker, with the cloud broker left as the client's choice. (1 pt)

**Sprint 1, weeks 1–2**

5. [ ] **SETUP-ENV**: the chosen broker for dev and staging in Terraform, once the client answers; a RabbitMQ container until then. (2 pts)
6. [ ] **PLATFORM-OUTBOX** (kernel events): `IEventPublisher` and `IEventSubscriber`, the envelope, the RabbitMQ adapter, the dead-letter drain into `platform.dead_letter`. With the relay and inbox of ADR-0058, 8 points together (review 7.3).
7. [ ] Prove it on `order.paid` → entitlement issuance → `entitlement.issued` by 23 October.

**After the client answers**

8. [ ] If Kafka: the Kafka adapter behind the same interface, with the same contract tests, and the consumer-side retry and dead-letter topic. (3 pts)
