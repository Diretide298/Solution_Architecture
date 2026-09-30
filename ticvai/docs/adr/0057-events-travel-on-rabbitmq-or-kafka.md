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
3. [x] ~~Dinesh~~: check a managed RabbitMQ in Azure UAE North (and, if the client leans to Kafka, Event Hubs' Kafka endpoint or Confluent Cloud there), with prices. **Done 30 September**: see the amendment below.
4. [x] Package: name the broker question in ADR-0033; add RabbitMQ to the four `deploy/*.yml` as the local and venue-local broker, with the cloud broker left as the client's choice. (1 pt)

**Sprint 1, weeks 1–2**

5. [ ] **SETUP-ENV**: the chosen broker for dev and staging in Terraform, once the client answers; a RabbitMQ container until then. (2 pts)
6. [ ] **PLATFORM-OUTBOX** (kernel events): `IEventPublisher` and `IEventSubscriber`, the envelope, the RabbitMQ adapter, the dead-letter drain into `platform.dead_letter`. With the relay and inbox of ADR-0058, 8 points together (review 7.3).
7. [ ] Prove it on `order.paid` → entitlement issuance → `entitlement.issued` by 23 October.

**After the client answers**

8. [ ] If Kafka: the Kafka adapter behind the same interface, with the same contract tests, and the consumer-side retry and dead-letter topic. (3 pts)

---

## Amendment — the options in UAE North, with prices, 30 September 2026

**Status unchanged: Proposed; the choice is still the client's. Our recommendation is unchanged: RabbitMQ.**
Source: `docs/active/infra-answers-30-september.md` section 3. Azure prices from the Azure Retail Prices API
(`uaenorth`, pay as you go, 730 hours), vendor list prices from the vendors' pages, both read 30 September 2026.

**Azure has no first-party RabbitMQ** (no RabbitMQ product in the Azure price list). Service Bus speaks AMQP
1.0, not RabbitMQ's AMQP 0-9-1, and stays ruled out (Option C).

### If the client picks RabbitMQ

| Option | UAE North | Small production price (USD / month) | Notes |
|---|---|---|---|
| **CloudAMQP, dedicated (recommended)** | Yes (in their Azure region list since 21 October 2019) | 3-node **Big Bunny $297** or **Happy Hare $597**, plus **$99** for VPC peering or PrivateLink: **about $400–700** | Managed by 84codes; their control plane is outside the UAE. **Get it in writing that backups, definitions and logs stay in UAE North before signing** |
| RabbitMQ Cluster Operator on our AKS (fallback) | Yes (our cluster) | 3 × D2s v5 ($258) + 3 × P10 disks ($65): **about $320**, plus our time | Cluster Operator and Messaging Topology Operator are MPL 2.0 and use the official image. **Not the Bitnami chart**: its images moved behind a paid subscription on 29 September 2025. This is what the cost workbook prices today |
| Azure Service Bus | Yes | Standard $10 + operations; Premium 1 MU about $715 | Not RabbitMQ; ruled out |

### If the client picks Kafka

| Option | UAE North | Small production price (USD / month) | Notes |
|---|---|---|---|
| **Event Hubs Standard + Kafka endpoint** | Yes | 2 TUs ≈ $58 + ingress events (a few dollars); a "Standard Kafka Endpoint" meter ($0.09/h, ≈ $66) may be billed on top (unconfirmed): **budget $60–130** | Private Link available. **At most 10 event hubs (topics) per namespace** and 7 days' retention |
| Event Hubs Premium | Yes | 1 PU ≈ **$1,072** | 100 event hubs per PU, 90 days' retention, resource isolation |
| Confluent Cloud on Azure | Yes (`uaenorth`; UAE Central not listed) | Standard ≈ $550 but public endpoints only; **Enterprise (private networking) ≈ $1,280–1,640** + $0.02–0.05/GB throughput + $0.08/GB-month storage | A second vendor contract. Public endpoints conflict with the LLD's "no public endpoints", so in practice Enterprise |

**Kafka on Event Hubs Standard: design topics per deployable, not per event.** With 69 events plus dead-letter
topics, the 10-topic limit forces a few coarse topics (for example one per deployable) or a second namespace.
Otherwise Premium. Confluent only if the client already has a Confluent contract.

### What it changes

- **Recommendation to the client, restated with prices:** RabbitMQ on **CloudAMQP, 3-node, with PrivateLink,
  in UAE North, about $400–700 a month.** It meets "managed, if one exists there", costs about the same as
  running it ourselves once our time is counted, and nobody on the team has run RabbitMQ.
- **Infrastructure:** a managed broker removes the `broker` node pool from `snet-aks-data`
  (`broker_self_hosted = false` in the Terraform cell module) and adds a private endpoint in
  `snet-private-endpoints`. The cost workbook prices the self-run cluster (VMs and P10 disks) until the client
  answers.

---

## Amendment — the decision pack: analysis and recommendation, 1 October 2026

**Status unchanged: Proposed until the client answers (by Monday 12 October). Recommendation unchanged and now
argued in full: RabbitMQ on CloudAMQP, three nodes with PrivateLink, in Azure UAE North, $396–696 a month.**
Source: `docs/active/broker-decision-pack.md` (a one-page summary for the client, then an engineering appendix).

### What the analysis found

- **Ordering and exactly-once effect do not separate the brokers.** Both give per-aggregate order through the
  ordering key; the consumer's `sequence` check makes a delayed retry safe on either; the outbox and the inbox
  (ADR-0058) give a once-only database effect on either. Kafka's own exactly-once covers Kafka-to-Kafka only
  and adds nothing for a Postgres effect.
- **Retries and dead letters do.** RabbitMQ does them by configuration (dead-letter exchange, delay queue,
  `x-delivery-limit` on quorum queues). On Kafka they are our consumer-wrapper code, and on Event Hubs
  Standard the 10-topic limit forces one shared retry topic.
- **Flash-sale peak, from the package's own figures** (`sizing.json`, `burst-scope.json`, the burst model):
  60,000 seats sold in 20 minutes is 6,270 requests/s, about 285 buyers/s, **about 2,850 events/s published
  and 7,400 deliveries/s** (10 events and 26 deliveries a buyer, derived from the catalogue). This is more
  than this ADR's "low thousands", because of fan-out. **Load-test target: 10,000 deliveries/s**, which also
  picks the CloudAMQP plan ($297 or $597, plus $99 PrivateLink).
- **Event Hubs Standard at that peak:** coarse topics give the `commerce` topic 17 consuming contexts (limit
  20 consumer groups), each reading every commerce event: about 34,000 reads/s, **17–26 TUs of egress out of
  40**, pre-scaled before the sale and scaled down by our own job. Workable, with thin headroom. Premium
  removes the limit at about $1,072.
- **Finding, independent of the broker: the relay is the first ceiling.** ADR-0058's one loop per tenant
  database at 200 rows every 100 ms tops out near **2,000 events/s**, below the 2,270–2,850 a single-tenant
  flash sale produces. Proposed to the ADR-0058 owner: poll again at once on a full batch, a larger batch in
  the burst environment, and relay lag measured in the same load test.
- **Replay** is Kafka's real advantage, and it is needed in one place only: outside subscribers re-reading the
  live stream. Nobody has asked for that. Audit, reporting rebuilds, AI training and dead-letter replay come
  from the database, the outbox's monthly partitions and Blob. Event Hubs keeps 7 days (Standard) or 90
  (Premium) anyway. If live replay is wanted later, a RabbitMQ stream or a Kafka side feed from the relay
  gives it without a broker swap.
- **Multi-region:** one broker per region. Nothing crosses regions through the broker (ADR-0010's contract
  does). **Venues:** RabbitMQ in 1 CPU and 1 GB whichever cloud broker is chosen. Store-and-forward is
  `syncOrders` with server-side re-pricing (ADR-0013), not a broker bridge.
- **Residency:** RabbitMQ on our AKS and Event Hubs keep everything in UAE North. CloudAMQP's control plane is
  outside the UAE: its score depends on 84codes' written confirmation that backups, definitions and logs stay
  in UAE North. Without it, RabbitMQ on our AKS.
- **Skills:** the skills matrix has no messaging column (nobody rated), Kubernetes at 2 at most (team average
  0.3), Azure at 3 at most. This favours a managed broker, and the one with fewer new concepts.
- **Cost:** every option but Confluent is within $700 a month of the others, 5–9% of the HA production month
  (about $8,050). Cost does not decide it.

### Decision matrix (weights sum to 100; scores 1–5; weighted out of 5)

| CloudAMQP | RabbitMQ on AKS | Event Hubs Standard | Event Hubs Premium | Confluent Enterprise |
|---:|---:|---:|---:|---:|
| **4.35** | 4.00 | 3.50 | 3.40 | 3.10 |

Criteria and weights: ordering, retries and dead letters 20; operations and skills 20; time to the 23 October
proof 15; residency 10; one broker with the venues 10; cost 10; flash-sale headroom 5; replay 5; lock-in 5.
RabbitMQ stays first when replay's weight is doubled and when the venue criterion is dropped. Kafka leads only
if live broker replay for outside subscribers becomes the leading requirement and on-premise consistency
stops mattering.

### Additions to the decision above

- **The kernel interface has two roles under one name.** The starter's `IEventPublisher` enqueues to the outbox
  inside the caller's transaction; this ADR and ADR-0058 also have the relay publish to the broker through it.
  Modules keep `IEventPublisher`. The relay and the consumer wrapper use a separate broker-side interface
  (publish a batch with an ordering key; subscribe by consumer name and event names; settle as `Ack`,
  `RetryLater`, `DeadLetter` or `Halt`), and only its adapter knows the broker. The starter's
  `IIntegrationEvent` still lacks `aggregateId`, `sequence` and `scopePath`. For PLATFORM-OUTBOX.
- **One broker-agnostic contract-test suite** runs against every adapter in CI.
- **16 shards per consumer** on RabbitMQ (or 16 partitions on Kafka) to start. Change only with the consumer
  drained.
- **A republish-from-outbox tool** (by tenant and time range) is needed on either broker, to recover a lost
  broker and to replay. It is not in the plan yet.
- **Migration path, if the other broker is needed later:** the second adapter behind the same contract tests;
  the relay publishes to both; consumers move one at a time, with the inbox absorbing duplicates and the
  sequence check covering order; stop the old publisher; roll back by re-pointing a consumer. About two
  sprints of platform work, and no module changes.

### What we need from the client by 12 October

The choice; if RabbitMQ, consent to CloudAMQP as a sub-processor subject to the residency confirmation (or
RabbitMQ on our AKS); who holds the contract; whether anyone needs replay from the broker, how far back and
for whom; the monthly budget line; and whether the broker falls under the 99.99% commitment (client email of
30 September, item 3). Without an answer by 12 October we proceed on the recommendation.

### Revisit

Outside subscribers want live replay (add a stream, not a swap). Sustained deliveries above about 25,000/s or
ten times the fan-out (Kafka through the migration path). CloudAMQP plan and shard count after three months of
production metrics. Self-running costs more than four engineer-days a month (move to CloudAMQP).
