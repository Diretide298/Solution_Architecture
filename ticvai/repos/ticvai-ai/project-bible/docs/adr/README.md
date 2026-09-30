# ADR

> **Purpose:** Architecture Decision Records  
> **Owner:** Chinmay  
> **Status:** Living

One file per decision: `NNNN-short-title.md`. Format: Context · Decision · Status · Consequences · Alternatives.

**A closed conflict becomes an ADR.** The [conflicts register](../registers/conflicts.md) tracks the question; the ADR records the answer and why — so that in a year nobody reconstructs the reasoning from seven MoM documents.


**The principles beneath these are in [../principles.md](../principles.md)**, which is shorter
and usually enough to predict what an ADR says.
| # | Decision | Status | Closes |
|---|---|---|---|
| [0001](0001-cell-architecture-one-tenant-per-jurisdiction.md) | Cell architecture — one tenant per jurisdiction | **Superseded** by 0014 and 0017 | — |
| [0002](0002-authorisation-is-user-driven-not-workstation-driven.md) | Authorisation is user-driven, not workstation-driven | Accepted | CF-03 |
| [0003](0003-conditional-role-selection-at-login.md) | Conditional role selection at login | Accepted | CF-01 |
| [0004](0004-single-session-per-user.md) | Single session per user | Accepted | CF-02, CF-28 |
| [0005](0005-venue-isolation-by-partitioning-not-separate-databases.md) | Venue isolation by partitioning, not separate databases | Accepted — confirmed by 0038; **amended by 0056**: release 1 isolates by RLS and composite keys, venue partitions later | — |
| [0006](0006-tiered-guest-app-distribution.md) | Tiered guest-app app distribution | Accepted | CF-13 |
| [0007](0007-hybrid-repository-topology.md) | Hybrid repository topology | Accepted | — |
| [0008](0008-money-carries-per-region-scale.md) | Money carries per-region scale | Accepted | — |
| [0009](0009-ai-data-residency.md) | AI data residency — architectural, not storage-location | Accepted — section 2 **amended by 0049** (Qdrant on every tier, a collection per tenant) | **CF-20** |
| [0010](0010-cross-jurisdiction-entitlements.md) | Cross-jurisdiction entitlements — home-cell ownership with delegated redemption | Accepted | **CF-31** |
| [0011](0011-hierarchy-is-binding.md) | The hierarchy is binding — seven levels confirmed | Accepted | **CF-34, CF-27** |
| [0012](0012-queue-integration-adaptor-first.md) | Queue integration — adaptor-first, vendor deferred | Accepted (partial) | **CF-33** |
| [0013](0013-local-first-point-of-sale.md) | Local-first point of sale — one read path, leases, local journal | Accepted | **CF-15** |
| [0014](0014-cell-per-region.md) | **Cell per region** — supersedes the jurisdiction-only split | **Superseded** by 0038 | **CF-32** |
| [0015](0015-standards-first-device-drivers.md) | Standards-first device drivers — ESC/POS, UnifiedPOS, OSDP | Accepted | — |
| [0016](0016-read-write-separation.md) | Read and write paths are separated, routing declared per operation | Accepted | — |
| [0017](0017-deployment-models.md) | Deployment models — shared, dedicated, additional region, on-premise | Accepted — amended by 0038 | — |
| [0018](0018-configuration-scope.md) | Configuration scope — three levels, nearest ancestor wins, venue is the floor | Accepted | — |
| [0019](0019-dynamic-bundle-pricing.md) | A dynamic bundle has a fixed price and a variable allocation | Proposed | — |
| [0020](0020-ai-isolation-boundary.md) | Where AI runs, and what it is isolated from | Accepted 30 September — **amended by 0049** (Qdrant, a collection and a scoped token per tenant) | — |
| [0021](0021-qdrant-partitioning.md) | Qdrant — one collection per embedding model, tenant is the shard, scope is the filter | Accepted in part 30 September — **amended by 0049**: a collection per tenant replaces the shard | — |
| [0022](0022-conflict-policy.md) | Conflict policy is declared per operation, from a closed set of four | Accepted | — |
| [0023](0023-pii-separation.md) | Personal data lives apart from the append-only ledger | Accepted | — |
| [0024](0024-contract-first-delivery.md) | The contract is the deliverable, written before anything else | Accepted | — |
| [0025](0025-one-audience-field.md) | One field says who may call an operation | Accepted | — |
| [0026](0026-public-api-versioning.md) | Public API versioning, scopes and deprecation | Accepted | — |
| [0027](0027-payment-links.md) | A payment link is a credential, and payment converts the reservation | Accepted | BL-072 |
| [0028](0028-service-decomposition.md) | Seventeen modules, and the data boundary decides where they split | Accepted — **amended by 0055**: deployed as five units; ownership rule rewritten | — |
| [0029](0029-outlet-configuration-scope.md) | Outlet configuration is outlet-scoped, and the path is the evidence | Accepted | — |
| [0030](0030-deep-link-cold-entry.md) | A deep link is a pointer, not authorisation | Accepted | — |
| [0031](0031-contention-and-locking.md) | Contention is leased, not locked — and where a lock is unavoidable it is named | Accepted | — |
| [0032](0032-load-shedding-and-pooling.md) | A service refuses early or fails late — pooling, backpressure and breakers | Accepted — pooling amended by 0038 | — |
| [0033](0033-outbox-and-dead-letters.md) | Every asynchronous handoff has an outbox and a place to fail | Accepted — **amended by 0058** (relay per region, inbox); broker per 0057 | — |
| [0034](0034-ai-retrieval-and-cost.md) | The cheapest AI call is the one that never reaches a provider | Accepted | — |
| [0035](0035-burst-environments.md) | A flash sale gets its own environment, and it cannot be deleted until it has been reconciled | Accepted — amended 3 September | — |
| [0036](0036-burst-cell-database-segregation.md) | The burst cell shares one Postgres instance with a database per service | **Superseded** by 0038 | — |
| [0037](0037-what-may-be-inside-a-lock.md) | A lock holds one statement, not a transaction | Accepted | — |
| [0038](0038-cell-is-a-region-database-per-tenant.md) | **A cell is a region, and a database per tenant inside it** | Accepted | **CF-161** |
| [0039](0039-control-plane-and-tenant-database-lifecycle.md) | The control plane is a database of its own, and a tenant database is the unit | Accepted | — raises **CF-167** |
| [0040](0040-a-cell-may-hold-more-than-one-instance.md) | A cell is a region; a region may need more than one instance | Accepted | — amends 0038 |
| [0041](0041-a-command-centre-is-a-saved-dashboard.md) | A command centre is a saved dashboard, not a screen | Accepted | — raises **CF-169** |
| [0042](0042-when-a-region-grows-and-where-a-tenant-lands.md) | When a region grows, and where a tenant lands | Accepted — one number pending sign-off | **CF-168** |
| [0043](0043-the-control-plane-splits-on-personal-data.md) | The control plane splits on personal data | Accepted | **CF-167** |
| [0044](0044-which-tables-partition-by-venue.md) | Which tables partition by venue | Accepted 18 September — **amended by 0056**: venue partitioning deferred, not cancelled | — completes 0005 |
| [0045](0045-every-order-carries-a-proven-contact.md) | **Every order carries a proven contact, and the gate is the checkout page** | Accepted | **CF-172** |
| [0046](0046-on-premise-has-two-configurations.md) | **On-premise has two configurations, and the difference is a control channel** | Accepted | **CF-61** — amends 0017, closes the AI question in 0020 |
| [0047](0047-how-long-data-is-kept-and-where-it-goes-next.md) | **How long data is kept, and where it goes next** | Accepted — one number pending | **CF-64** (closed), **CF-165** — amends 0042 |
| [0048](0048-guest-recurring-billing-is-commerce.md) | **Guest recurring billing is commerce, not the Control Plane** | Accepted | **BL-100** — relates to 0039, 0043, 0028 |
| [0049](0049-vectors-live-in-qdrant-one-collection-per-tenant.md) | **Vectors live in Qdrant from day one, one collection per tenant, each with its own token** | Accepted 30 September | SD-060 — amends 0009, 0020, 0021 |
| [0050](0050-one-autonomy-scale.md) | One autonomy scale; the approval tier is not an autonomy level | Accepted 30 September (records AI-D04) | SD-060 |
| [0051](0051-ai-ships-on-a-baseline-and-learns-per-tenant.md) | Every AI function ships on a baseline and learns per tenant | Accepted 30 September | SD-060, SD-061 |
| [0055](0055-a-modular-monolith-deployed-as-five-units.md) | **A modular monolith, deployed as five units** | Accepted 30 September | **SD-001**, SD-002, SD-006 — amends 0028 |
| [0056](0056-one-id-type-and-time-partitioning-before-the-first-migration.md) | **One id type (UUIDv7), and time partitioning first** | Accepted 30 September | **SD-010**, SD-012, SD-009 — amends 0044, 0005 |
| [0057](0057-events-travel-on-rabbitmq-or-kafka.md) | Events travel on RabbitMQ or Kafka, behind one kernel interface | **Proposed** — waiting on the client's choice between RabbitMQ and Kafka | **SD-032** — completes 0033 |
| [0058](0058-one-relay-per-region-and-an-inbox-per-tenant-database.md) | One relay per region, and an inbox per tenant database | Accepted 30 September | SD-031, SD-030 — amends 0033 |
| [0059](0059-ai-phasing-against-the-six-month-plan.md) | AI phasing against the six-month plan | Accepted 30 September | SD-062, CF-57, CF-14 |

> **0026 to 0037 were added on 30 September** (SD-053): they had been on disk since August and
> missing from this table. **0049–0051 and 0055–0059 were added the same day**, from the system-design
> review. Numbers 0052–0054 and 0060–0068 are held by review drafts that are not decided yet; they join
> this table when they are.

## Still needed

One remains, and it is blocked rather than unwritten:

**The embedding model** — gated on the benchmark run in ADR-0021's addendum (0021 is amended by
0049, and the benchmark still applies), then on real tenant content. The architecture does
not wait on it.

**AI phasing** was here until 30 September. It is closed by 0059.

**The cloud event broker** is written (0057) and waits on the client's choice between RabbitMQ and
Kafka.

## Status vocabulary

Four values, and a status must **lead** with its state rather than bury it.

| | |
|---|---|
| **Accepted** | In force |
| **Accepted in part** | In force with a named carve-out, and the carve-out says which |
| **Proposed** | Written and not yet reviewed by anyone but its author |
| **Superseded** | Replaced. **Do not cite its Decision section** |

`check-package.py` enforces the set, and fails any ADR citing a superseded one without naming
the supersession. **Both rules exist because of CF-97**: ADR-0001 (retired — see ADR-0014 and ADR-0017)'s status read
*"Accepted — split rule superseded by ADR-0014"*, and a careful reader took the first word and
built a cross-tenant isolation defect on it.
