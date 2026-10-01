# The event broker: RabbitMQ or Kafka

> **Date:** 1 October 2026 · **For:** the client (page 1), then the engineers (the appendix)
> **Decision needed by:** Monday 12 October 2026, so the first purchase is proven end to end by 23 October
> **Records:** ADR-0057 (proposed; amended 1 October with this analysis). Builds on ADR-0033 (outbox and dead
> letters), ADR-0055 (five deployables), ADR-0056 (ids and partitions), ADR-0058 (relay and inbox), ADR-0013 and
> ADR-0046 (venues and on-premise)
> **Prices:** Azure UAE North pay-as-you-go and vendor list prices, read 30 September 2026
> (`docs/active/infra-answers-30-september.md` section 3). US dollars a month, 730 hours

---

## Decision summary

**We recommend RabbitMQ, run for us by CloudAMQP in Azure UAE North: a three-node cluster with a private
connection, about $400–700 a month.**

**What the broker does.** Every sale reaches ticketing, the ledger and stock through it. `order.paid` alone
has six consumers, three of them critical. The broker must keep each order's events in sequence, retry
failures with a delay, set aside messages that keep failing so a person can replay them, and keep the data
in the UAE.

**Why RabbitMQ.**

1. **It is a queue, and ours is a queue problem.** Retries with a delay and dead letters are built in. Kafka
   is a log. With Kafka, retries and dead letters are code we write and test ourselves.
2. **One broker everywhere.** Venues on their own premises run RabbitMQ whichever cloud broker you choose
   (it fits a small venue server). With RabbitMQ in the cloud too, there is one broker to learn, one
   adapter to test and one runbook.
3. **It fits the team.** Nobody on the team has run either broker. RabbitMQ has fewer new ideas to learn,
   and a managed service removes the running of it.
4. **It carries the peak.** A 60,000-seat on-sale sold in 20 minutes produces about 2,900 events and 7,400
   deliveries a second at its peak. A three-node RabbitMQ cluster handles that. We will load-test the
   chosen plan at 10,000 deliveries a second before the first on-sale.
5. **Nothing is locked in.** Our code talks to one interface, never to the broker. Moving to Kafka later is
   one adapter and a staged cut-over, with no change to any module.

**What each choice means for you**

| | **RabbitMQ (recommended)** | **Kafka** |
|---|---|---|
| Where it runs | CloudAMQP in Azure UAE North, private connection. Fallback: we run it in your Azure cluster | Azure Event Hubs with the Kafka endpoint, in UAE North. Confluent Cloud only if you already hold a Confluent contract |
| Production cost a month | **$396** (smaller plan) **to $696** (larger plan), private link included. The load test picks the plan | **Event Hubs Standard: $60–130**, plus about $1 an hour while a big on-sale runs. **Premium: about $1,070.** Confluent (private): $1,280–1,640 plus usage |
| Running it | The provider patches, upgrades and monitors the broker | Microsoft runs Event Hubs. We build and run the retry and dead-letter handling |
| At your venues | The same broker as the cloud | RabbitMQ at the venue, Kafka in the cloud: two brokers to test and support |
| Replaying past events from the broker | A replayable stream can be added to RabbitMQ later if you want one. Replay today comes from our own event store in the database | 7 days on Standard, 90 days on Premium |
| Data in the UAE | Messages stay on servers in UAE North. **CloudAMQP's control plane is outside the UAE**: we get it in writing that backups, settings and logs stay in UAE North before signing, or we run it ourselves | Everything stays in Azure UAE North |
| Effect on the plan | None. We are already building on RabbitMQ | The first purchase is still proven on 23 October, on RabbitMQ in development. The Kafka adapter and its retry handling follow in sprint 2 |

**When Kafka is the better answer.** Choose Kafka if you want your own teams or partners to read and re-read
the live event stream from the broker itself, over days or weeks. If so, tell us how far back and for whom.
Even then, we would recommend RabbitMQ for the sale path and a stream alongside it, not a swap.

**What we need from you by Monday 12 October**

1. **The choice:** RabbitMQ or Kafka.
2. **If RabbitMQ:** your consent to CloudAMQP (84codes) as a data sub-processor, once they confirm in writing
   that messages, backups, settings and logs stay in UAE North. If your data protection officer will not
   accept a control plane outside the UAE, say so and we run RabbitMQ in your Azure cluster instead (about
   $330 a month plus our engineers' time).
3. **Who holds the contract and pays:** your Azure subscription or a direct contract with the provider.
4. **Replay:** whether anyone needs to replay events from the broker itself, how many days back, and who.
5. **The budget line:** approval for the monthly figure above, per production region.
6. **Availability:** whether the broker falls under the 99.99% commitment we asked you about (item 3 of our
   30 September email). The provider's service level has to match it.

If we have not heard by 12 October, we proceed on the recommendation: RabbitMQ, and a RabbitMQ we run in
the development environment until the contract is signed.

---

## Engineering appendix

### A. Requirements

**Functional**

| # | Requirement | Source |
|---|---|---|
| F1 | Carry 77 events (the catalogue under `events/`) from the outbox of every tenant database to 198 consumer entries in 24 consuming contexts | `events/*.yaml`, 1 October count |
| F2 | Keep one aggregate's events in order. No order across aggregates | `events/_schema.yaml`, ADR-0058 |
| F3 | At-least-once delivery. Each consumer has a durable inbox and states its idempotency key | ADR-0058, `_schema.yaml` |
| F4 | Five attempts, exponential from 1 s, jittered, then dead-letter. 103 consumer entries are `retryThenDeadLetter`, 94 `retry` | ADR-0033 |
| F5 | Dead letters drain into `platform.dead_letter`, where `replayDeadLetter` works. Financial postings and DSARs halt and alert instead | ADR-0033, ADR-0057 |
| F6 | .NET consumers (`commerce`, `access`, `operations`, `workers`) and Python consumers (`ticvai-ai`) | ADR-0055 |
| F7 | An on-premise equivalent that runs on a venue server. Venue-local profile: 1 CPU, 1 GB for the broker | ADR-0046, `deploy/d-venue-local-offline.yml` |

**Non-functional**

| # | Requirement | Number |
|---|---|---|
| N1 | Peak throughput (section C) | 2,900 events/s published, 7,400 deliveries/s; test at 10,000 deliveries/s |
| N2 | Residency | Messages, backups and logs in Azure UAE North (ADR-0038, amended by ADR-0040; LLD: every store in the UAE) |
| N3 | No public endpoints | Private Link or in-cluster only (LLD) |
| N4 | Availability | Three nodes across zones 1–3 (LLD). The outbox is the record: a rebuilt broker loses nothing if we can republish (see risk R8) |
| N5 | Latency | Relay polls every 100 ms when busy, 2 s when idle (ADR-0058). The broker adds milliseconds. Not a differentiator |
| N6 | Run by this team | See section F |

**Constraints.** Block A starts Monday 5 October. The relay, adapter and inbox are proven on
`order.paid` → entitlement issuance → `entitlement.issued` by 23 October. The client chooses by 12 October.
Azure Service Bus is ruled out (ADR-0057, Option C).

### B. The design both brokers sit behind

```
 tenant database (one per tenant)                     workers deployable            consumers
 ┌─────────────────────────────┐   poll, lease per   ┌──────────────┐   publish    ┌────────────────────────┐
 │ state change + outbox row   │   tenant database   │ relay        │   ordering   │ consumer wrapper       │
 │ (one transaction)           ├────────────────────►│ (ADR-0058)   ├──key = ─────►│ 1 check sequence       │
 │ platform.outbox, monthly    │   200 rows a batch  │ via broker   │  aggregateId │ 2 insert inbox row     │
 │ partitions (ADR-0056)       │                     │ adapter      │              │   + effect, one tx     │
 └─────────────────────────────┘                     └──────────────┘   BROKER     │ 3 settle: ack / retry  │
                                                                                   │   later / dead-letter  │
 platform.dead_letter ◄──── drain worker ◄──── broker dead-letter place ◄──────────┤   / halt               │
 (replayDeadLetter)                                                                └────────────────────────┘
```

**Exactly-once effect, whichever broker.** The outbox row commits with the state change (ADR-0033). The relay
publishes at least once. The consumer inserts `kernel.inbox (consumer, event_id)` with `ON CONFLICT DO
NOTHING` in the same transaction as its effect (ADR-0058). So every database effect happens once. This holds
on either broker and depends on neither.

Kafka's own exactly-once (idempotent producer plus transactions) covers Kafka-to-Kafka read-process-write
only. It does not cover a Postgres effect. So it adds nothing here. Effects outside the database (email, SMS,
webhooks through `public-api`, payment-provider calls) stay at-least-once on both brokers and rely on the
downstream idempotency key (`marketing.message_dispatch`, the provider's idempotency header).

**Order, and why retries do not break it.** The consumer checks `sequence` per aggregate. If event *n* fails
and goes to a delayed retry, event *n+1* of the same aggregate arrives, sees the gap, and is also sent to
retry. When *n* succeeds, *n+1* follows. So a retry can leave the ordered lane without breaking order, on
either broker. A gap that never closes dead-letters and a person sees it.

**How each broker gives per-aggregate order**

```
RabbitMQ                                               Kafka (Event Hubs)
─────────                                              ──────────────────
relay ─► topic exchange "ticvai.events"                relay ─► topic, key = aggregateId
          │ binding per consumer, by event name                  │ partition = hash(key) mod P
          ▼                                                      ▼
   consistent-hash exchange per consumer               P partitions (Standard: up to 32, fixed at creation)
          │ hash(aggregateId) → shard                           │
          ▼                                                     ▼
   16 quorum queues per consumer,                      one consumer group per consumer;
   single active consumer each                         one reader per partition
          │ nack → DLX → delay queue (TTL) → back               │ failure → retry topic → dead-letter topic
          │ x-delivery-limit → dead-letter queue                │ (consumer wrapper code: ours)
          ▼                                                     ▼
   drain worker → platform.dead_letter                 drain worker → platform.dead_letter
```

In both, parallelism per consumer is fixed up front: shard count on RabbitMQ, partition count on Kafka.
Changing it re-hashes keys, so it is done with the consumer drained, and the sequence check covers the
cut-over. We start at 16 shards (section C).

**Finding: the kernel has two jobs under one name.** In the starter repository,
`Ticvai.Shared.Kernel/Abstractions/IIntegrationEvent.cs` defines `IEventPublisher.PublishAsync` as *"enqueues
onto the outbox within the caller's transaction"*. ADR-0058 has the relay publish to the broker "through the
kernel's `IEventPublisher`". Those are two contracts: modules enqueue to the outbox, and the relay sends to
the broker. We propose keeping `IEventPublisher` for modules and naming the broker side separately (for
example `IEventTransport`: `PublishBatchAsync(envelopes)` with the ordering key, and `Subscribe(consumerName,
eventNames, handler)` where the handler returns `Ack`, `RetryLater`, `DeadLetter` or `Halt`). The starter's
`IIntegrationEvent` also lacks `aggregateId`, `sequence` and `scopePath` from the ADR-0058 envelope. Both are
for the PLATFORM-OUTBOX ticket, not this decision.

### C. Throughput at flash-sale peaks

**Source figures.** `handoff/sizing.json` (from `tools/derive-sizing.py`), `handoff/burst-scope.json`, the
burst simulator (`handoff/burst-model.js`) and ADR-0035. A flash sale runs in its own burst environment with
one database. The design load is **5,000 requests a second**. The documents' own sale: **60,000 seats, 95%
buying, 22 calls a buyer**: 1,045 requests a second at peak over two hours, **6,270** if sold in twenty
minutes. The shared cell's large-cell peak is 7,036 requests a second, mostly reads.

**Events per buyer (our estimate from the catalogue).** One seat per buyer, as the burst model assumes.

| Event | Per buyer | Consumers | Deliveries |
|---|---:|---:|---:|
| `seat.held` (`createSeatHold`, 2 calls) | 2 | 1 | 2 |
| `order.created` | 1 | 3 | 3 |
| `payment.captured` | 1 | 2 | 2 |
| `order.paid` | 1 | 6 | 6 |
| `seat.sold` | 1 | 3 | 3 |
| `entitlement.issued` | 1 | 5 | 5 |
| `order.completed` | 1 | 3 | 3 |
| `storefront.sessionEvent` (batches of up to 50 interactions) | 2 | 1 | 2 |
| **Total** | **10** | | **26** |

**Load on the broker**

| Scenario | Requests/s | Buyers/s | Events published/s | Deliveries/s |
|---|---:|---:|---:|---:|
| Shared cell, large, normal peak | 7,036 | — | hundreds (ADR-0057) | under 2,000 (2.6 consumers an event on average) |
| On-sale over 2 hours, peak | 1,045 | 48 | 480 | 1,240 |
| Burst design load | 5,000 | 227 | 2,270 | 5,900 |
| **On-sale in 20 minutes, peak** | **6,270** | **285** | **2,850** | **7,400** |
| **Load-test target** | | | **3,500** | **10,000** |

Message size: an envelope of about 400 bytes plus the payload, so 1–1.5 KB for `order.paid` with lines
(assumption; to be measured).

**RabbitMQ at 10,000 deliveries a second.** Each delivery is a quorum-queue message replicated to three nodes:
about 30,000 replicated writes a second, 30–45 MB/s across the cluster. RabbitMQ's published quorum-queue
benchmarks reach tens of thousands of small messages a second on adequately sized nodes, so this is inside the
envelope but not by a factor of ten.
**We do not size the CloudAMQP plan on paper.** The load test in sprint 2 decides between the $297 and the $597
plan, and between them is $300 a month.

**Event Hubs Standard at the same peak.** A throughput unit carries 1 MB/s or 1,000 events/s in, and 2 MB/s or
4,096 events/s out. Two constraints bite together:

- **10 event hubs (topics) per namespace** forces coarse topics: one per publishing deployable plus retry and
  dead-letter topics. The `commerce` topic then carries 40 of the 77 events and has **17 consuming contexts**,
  close to Standard's **20 consumer groups per event hub**. A consumer that owns two handlers on the same topic
  needs its own group, so the limit is near.
- **Every consumer group reads every commerce event** and discards what it does not handle. At the 20-minute
  peak that is about 2,000 commerce events/s × 17 groups ≈ 34,000 reads/s, 34–51 MB/s: **17–26 TUs of egress**
  out of the namespace's 40.

It works, at about $0.70–1.05 an hour while scaled up, but only if the namespace is **scaled up before the
sale** (auto-inflate raises TUs and never lowers them, so scaling down is a job we write), and the headroom is
thin. Premium (100 event hubs per PU) removes the coarse-topic problem.

**Kafka's genuine advantage here is fan-out.** Consumers read one log, so adding consumers costs egress but
not writes. RabbitMQ copies each message into every bound queue. At 26 deliveries per buyer we are well
inside what that costs. If fan-out grew by ten times (for example many external subscribers on the live
stream), that would be a reason to revisit (section I).

**Finding: the relay, not the broker, is the first ceiling in a flash sale.** ADR-0058 gives one polling loop
per tenant database, 200 rows a poll, a poll every 100 ms while rows are found. That is at most **2,000
events a second per tenant database**, less the publish time. A flash sale is one tenant in one database and
produces **2,270–2,850** a second. This holds on either broker. Proposal for the ADR-0058 owner: poll again at
once when a batch comes back full, allow a larger batch in the burst environment, and measure relay lag in the
same load test. It needs no change to ADR-0058's design, only to two of its parameters.

**Consumer side.** With 16 shards per consumer, `access.issueOrderEntitlements` handles about 18 orders a
second per shard at the 20-minute peak, so each issuance transaction (inbox row included) must finish in
under about 55 ms. The same arithmetic applies to Kafka partitions. The load test measures it.

### D. Dead letters, retries and replay

| Need | RabbitMQ | Kafka (Event Hubs) |
|---|---|---|
| Delayed retry | Dead-letter exchange into a delay queue with a TTL, routed back to the shard. Configuration | Retry topic and a consumer that waits. Code. On Standard the retry topic is shared across consumers (10-topic limit), so it carries a header naming the consumer |
| Retry budget | `x-delivery-limit` on quorum queues (RabbitMQ 4 defaults it to 20; we set 5) | Counted by our wrapper in a header |
| Dead letters | Dead-letter queue per consumer, drained to `platform.dead_letter` | Dead-letter topic written by our wrapper, drained to `platform.dead_letter` |
| Halt and alert (ledger, DSAR) | Stop settling the shard: that shard's queue backs up and pages. 1 in 16 orders waits, the rest flow | Pause the partition: the same effect on 1 in P |
| Poison message | Delivery limit, then dead letter | Must be moved off the partition by our wrapper, or the partition stops |

**Replay: what is actually needed, and where it comes from**

| Need | What it replays | Where it comes from | Does the broker matter? |
|---|---|---|---|
| Dead-letter replay | One failed delivery | `platform.dead_letter` → `replayDeadLetter` (ADR-0033) | No |
| Audit | What happened, provably | `platform.audit_record`, `ledger.journal_line`, `ai.decision_record` with its hash chain. None of them comes from the broker | No |
| Reporting read-model rebuild | All events of a kind since a date | The source tables, or the outbox's monthly partitions (hot for the retention period, then archived to Blob, ADR-0047/0056) | No |
| A new AI feature over history | Months of orders, scans, interactions | Training snapshots in Blob and the outbox archive (ai-system-design 3.4) | No. Event Hubs Standard keeps 7 days, Premium 90: too short for training anyway |
| Broker lost or rebuilt | Everything unconsumed | Republish from the outbox by time range (risk R8) | No |
| The client's own live subscribers re-reading the stream | Days to weeks | The broker | **Yes: Kafka's case** |

**Replay is Kafka's real advantage, and we need it in one place only: live subscribers re-reading the stream.**
Nobody has asked for that. If they do, RabbitMQ has streams (an append-only, replayable queue type with a .NET
and a Python client, and super streams for partitioning), and the relay can feed one alongside the queues. So
the need does not force a broker change.

### E. Multi-region, residency and venues

**One broker per region.** A cell is a region (ADR-0038). Events never cross regions through the broker.
Cross-region entitlements go through the CrossRegion module's contract and reconciliation (ADR-0010), not by
mirroring a broker. So no Shovel, Federation, MirrorMaker or Cluster Linking. This is the same for both
brokers, and it is what residency wants.

**Disaster recovery.** The broker is not geo-paired (ADR-0060, proposed). In a failover to UAE Central the
broker there starts empty, the relay re-publishes from the promoted tenant databases' outboxes, and the inbox
absorbs duplicates. Same for both brokers. It needs the republish tool in risk R8.

| Option | Residency |
|---|---|
| RabbitMQ on our AKS | Strongest. Everything is in our cluster in UAE North |
| Event Hubs | Strong. An Azure regional service in UAE North. Do not enable Geo-DR pairing outside the UAE |
| **CloudAMQP** | Message data is on nodes in UAE North. **The control plane is outside the UAE.** Needs 84codes' written statement that backups, definitions and logs stay in UAE North. Fallback: our AKS |
| Confluent Cloud | Cluster in `uaenorth`. Control plane and metrics outside the UAE. The same written check would be needed |

Event payloads carry ids, not names or contact details (`subjectId`, `venueId`, lines). They are still tenant
data, so the written check stands.

**Venues on premises.** The venue-local profile runs RabbitMQ in 1 CPU and 1 GB, whichever cloud broker is
chosen. A single-node Kafka in KRaft mode fits there only just, and it would still leave retries to us.

**Store-and-forward is not the broker's job in this design.** A venue that loses its connection journals
locally and syncs on reconnect through `syncOrders`, and **the server re-prices every line on ingest**
(ADR-0013, step 4). The rejection path (`sync.rejection`) is application logic that a broker bridge cannot do.
So no event crosses the WAN broker-to-broker. If one ever needs to (for example venue telemetry into the
cloud), RabbitMQ's Shovel is built-in store-and-forward over an unreliable link. The Kafka equivalent is
MirrorMaker 2 or Cluster Linking, both heavier than a venue server should carry. **This favours RabbitMQ
but does not decide the question**, because the design does not rely on it.

### F. Operations and skills

**The team, from the developers' skills matrix** (ten developers rated, of a team of 14; ratings 0–4):

| Skill | What the matrix shows |
|---|---|
| RabbitMQ, Kafka, any messaging | **Not in the matrix. Nobody is rated** |
| Kubernetes | Highest rating 2 (one person); most unrated or 0. Team average 0.3 |
| Azure | Highest 3 (one person), then 2 and 1. Team average 1.0 |
| Docker | Highest 3. Team average 2.0 |
| .NET / C# | Two at 4, two at 3 |
| Python (FastAPI) | One at 4 |
| PostgreSQL | Highest 3. Team average 2.0 |

Two AI engineers join from 5 October, for `ticvai-ai`'s Python consumers.

**What each option asks of this team**

| Option | Broker operations | Consumer code | Verdict for this team |
|---|---|---|---|
| **CloudAMQP** | The provider: patching, upgrades, disk and memory alarms, backups. We keep topology as code and alert on queue depth and dead letters | Ack, nack, retry by configuration. The concepts map onto the outbox and dead-letter tables the team already knows | **Lowest total burden** |
| RabbitMQ Cluster Operator on AKS | Ours: upgrades, quorum membership, disk alarms, node loss, with Kubernetes skill at 2 at most. Our estimate: 2–4 engineer-days a month, more in an incident | As above | Fine technically, heavy for this team. The fallback only |
| Event Hubs Standard or Premium | Microsoft's | Ours: offsets and checkpoints, rebalances, retry and dead-letter topics, the coarse-topic filter, pre-scaling TUs before a sale. Plus RabbitMQ at venues: two adapters, two contract-test suites | Low broker burden, high code burden in an area where newcomers make the classic mistakes (committing an offset before the effect, a poison message stopping a partition, rebalance storms) |
| Confluent Cloud | Confluent's | As Event Hubs, without the 10-topic limit | As Event Hubs, plus a second vendor contract |

### G. Cost in UAE North (production, one region, a month)

| Option | Monthly | What is included | What it adds |
|---|---:|---|---|
| **RabbitMQ, CloudAMQP 3-node Big Bunny + PrivateLink** | **$396** | Managed 3-node cluster, private connection | Nothing |
| **RabbitMQ, CloudAMQP 3-node Happy Hare + PrivateLink** | **$696** | As above, larger nodes | Taken only if the load test needs it |
| RabbitMQ, Cluster Operator on our AKS | $329 | 3 × D2s v5 ($258) + 3 × P10 ($65), corrected workbook line | 2–4 engineer-days a month (our estimate) |
| Kafka, Event Hubs Standard | $60–130 | 2 TUs ($58); the "Standard Kafka Endpoint" meter (≈ $66) may or may not be billed on top (unconfirmed) | ≈ $0.70–1.05 an hour while pre-scaled for a sale; the retry and dead-letter build; RabbitMQ still at venues |
| Kafka, Event Hubs Premium | ≈ $1,072 | 1 PU, 100 event hubs, 90 days' retention | More PUs for large sales, scaled by hand |
| Kafka, Confluent Enterprise (private) | $1,280–1,640 | Private networking | $0.02–0.05/GB throughput, $0.08/GB-month storage, a second contract |

**Pre-production** runs a single-node RabbitMQ in the pre-production cluster (about $110, the workbook line)
whichever option is chosen. With Kafka it also needs an Event Hubs Standard namespace (about $30 for one TU).

**In proportion.** The HA production month in the cost workbook is about $8,050 (corrected 30 September). The
recommended broker is 5–9% of it. Every option except Confluent is within $700 a month of every other, so cost
does not decide this. Correctness, the team and the venues do.

### H. Lock-in, the one interface and the migration path

**The interface is the lock-in control.** Modules call `IEventPublisher`, which enqueues to the outbox. They
never see the broker. The relay and the consumer wrapper use the broker-side interface (section B), and only
the adapter behind it knows the broker. To keep that true:

- The interface exposes only what both brokers can do: publish a batch with an ordering key, subscribe by
  consumer name and event names, and settle as `Ack`, `RetryLater`, `DeadLetter` or `Halt`. No priorities, no
  per-message TTL, no request-reply, no broker-side replay through it.
- One broker-agnostic contract-test suite (order per key, redelivery absorbed by the inbox, retry budget, dead
  letter reaches `platform.dead_letter`, halt stops one shard only) runs against every adapter in CI.
- No MassTransit: version 9 moved to a commercial licence. A thin adapter over the official RabbitMQ .NET
  client, and `aio-pika` or `pika` for Python, is enough for 77 events.

**Vendor lock-in.** CloudAMQP is standard RabbitMQ over AMQP 0-9-1. Topology exports as a definitions file, so
moving to our own cluster, or to another RabbitMQ provider, is configuration. Event Hubs speaks the Kafka
protocol, but its topic limits, consumer-group limits and TU model shape the topology. Leaving it means
redesigning topics, not only moving them.

**If they pick RabbitMQ and later need Kafka**

1. Build the Kafka adapter and its retry and dead-letter wrapper. Pass the same contract tests.
2. Stand up Kafka. The relay publishes every batch to both brokers. The outbox is the single source and the
   inbox absorbs duplicates, so dual publishing is safe.
3. Move one consumer at a time. Point it at Kafka from the time its RabbitMQ queues are empty. Anything it sees
   twice, the inbox skips. The sequence check covers order across the switch.
4. When no consumer reads RabbitMQ in the cloud, stop publishing there. Venues keep RabbitMQ.
5. Rollback at any step: point the consumer back.

About two sprints of platform work, and no module code changes. **If they pick Kafka and later want
RabbitMQ**, the same steps in reverse, shorter, because the RabbitMQ adapter already exists for development
and venues.

**If only replay is wanted**, not a swap: the relay feeds a RabbitMQ stream, or an Event Hubs namespace, with
the chosen event families alongside the queues. The sale path does not change.

### I. Decision matrix

Scores 1 (poor) to 5 (best). Weights sum to 100. Scores are ours, reasoned in sections B to H.

| Criterion | Weight | CloudAMQP | RabbitMQ on AKS | Event Hubs Std | Event Hubs Prem | Confluent Ent |
|---|---:|---:|---:|---:|---:|---:|
| Ordering, retries and dead letters (B, D) | 20 | 5 | 5 | 3 | 3 | 3 |
| Operations and skills (F) | 20 | 4 | 2 | 4 | 4 | 4 |
| Time to the 23 October proof (A) | 15 | 5 | 4 | 3 | 3 | 2 |
| Residency (E) | 10 | 3 | 5 | 5 | 5 | 4 |
| One broker with the venues (E) | 10 | 5 | 5 | 2 | 2 | 2 |
| Cost (G) | 10 | 4 | 4 | 5 | 2 | 1 |
| Flash-sale headroom (C) | 5 | 4 | 4 | 3 | 5 | 5 |
| Replay from the broker (D) | 5 | 3 | 3 | 3 | 4 | 5 |
| Lock-in and migration (H) | 5 | 5 | 5 | 3 | 4 | 4 |
| **Weighted (out of 5)** | 100 | **4.35** | **4.00** | **3.50** | **3.40** | **3.10** |

**Sensitivity.** Double the weight on replay (take it from time to the proof): CloudAMQP 4.25, Event Hubs
Premium 3.45, Confluent 3.25. Drop the venue criterion entirely (move its weight to cost): CloudAMQP 4.25,
RabbitMQ on AKS 3.90, Event Hubs Standard 3.80. RabbitMQ stays first in both. Kafka wins only if live broker replay for outside
subscribers becomes the leading requirement **and** on-premise consistency stops mattering.

CloudAMQP's residency score (3) rests on the written confirmation. If 84codes cannot give it, the answer is
RabbitMQ on our AKS (4.00), still ahead of every Kafka option.

### J. Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | CloudAMQP cannot confirm backups, definitions and logs stay in UAE North | Medium | High | Ask before signing. Fallback: Cluster Operator on AKS, priced at $329 plus time |
| R2 | The chosen plan does not carry 10,000 deliveries/s | Low–medium | High on a sale day | Load-test in sprint 2 at the target. Happy Hare if Big Bunny fails. Retest before the first large on-sale |
| R3 | The relay tops out near 2,000 events/s per tenant database (section C) | High in a 20-minute sale | Relay lag, late tickets and ledger | Poll again at once on a full batch; a larger batch in the burst environment; alert on lag (ADR-0058 action 5) |
| R4 | Nobody on the team has run a broker | Certain | Medium | Managed service; runbook; broker-agnostic contract tests; a load test the team runs itself |
| R5 | A halted critical consumer (ledger) blocks its shard | By design | 1 in 16 orders waits | Pages at once; `Halt` only on ADR-0033's two cases |
| R6 | Changing the shard or partition count later | Low | Order breaks during the change | Drain first; the sequence check catches the rest; start at 16 |
| R7 | The interface leaks broker features | Medium over time | Lock-in | Narrow interface; code review; one contract suite across adapters |
| R8 | Broker lost, or a DR failover, after the relay marked rows published | Low | Events never delivered | **A republish-from-outbox tool by tenant and time range.** It is not in the plan yet. Both brokers need it; ADR-0060's DR failover assumes it; it is also the replay path |
| R9 | The provider's SLA is below the availability promised to the client | Medium | Contractual | Read the SLA against the answer to email item 3 before signing |
| R10 | If Kafka on Event Hubs Standard: 10 topics, 20 consumer groups, manual scale-down | Certain if chosen | Medium | Coarse topics, pre-scaling in the burst environment's warming state, or Premium |

### K. What we would revisit, and when

- **A client or partner wants to re-read the live stream:** add a RabbitMQ stream or a Kafka side feed from the
  relay. Not a broker swap.
- **Sustained deliveries above about 25,000 a second, or fan-out grows by ten times:** Kafka through the
  migration path in section H.
- **A region passes about 200 tenant databases, or relay lag p95 exceeds 2 s:** logical decoding on the outbox
  (ADR-0058, Option C).
- **After three months of production metrics:** the CloudAMQP plan size, and the shard count per consumer.
- **If we end up self-running and it costs more than four engineer-days a month:** move to CloudAMQP. The
  protocol and the definitions file are the same.

### L. What this pack did not check

- CloudAMQP's rated throughput per plan, its SLA, and whether it sells through the Azure Marketplace.
- Whether Event Hubs bills the Standard Kafka Endpoint meter on top of TUs (carried from 30 September).
- Message sizes and consumer processing times. Section C uses estimates until the load test measures them.
- Events per buyer. Section C derives 10 from the catalogue, with one seat per buyer.
