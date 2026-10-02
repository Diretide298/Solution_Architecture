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
| [0009](0009-ai-data-residency.md) | AI data residency — architectural, not storage-location | Accepted — section 2 **amended by 0049** (Qdrant on every tier, a collection per tenant); sections 1 and 3 **amended 2 October** (a residency class per tenant, UAE-only by default through Core42 Compass) | **CF-20** |
| [0010](0010-cross-jurisdiction-entitlements.md) | Cross-jurisdiction entitlements — home-cell ownership with delegated redemption | Accepted | **CF-31** |
| [0011](0011-hierarchy-is-binding.md) | The hierarchy is binding — seven levels confirmed | Accepted | **CF-34, CF-27** |
| [0012](0012-queue-integration-adaptor-first.md) | Queue integration — adaptor-first, vendor deferred | Accepted in part — **Q2 amended by 0066** (the waiting room has its own endpoints and an admission token) | **CF-33** |
| [0013](0013-local-first-point-of-sale.md) | Local-first point of sale — one read path, leases, local journal | Accepted | **CF-15** |
| [0014](0014-cell-per-region.md) | **Cell per region** — supersedes the jurisdiction-only split | **Superseded** by 0038 | **CF-32** |
| [0015](0015-standards-first-device-drivers.md) | Standards-first device drivers — ESC/POS, UnifiedPOS, OSDP | Accepted — **amended by 0067** (one device register) | — |
| [0016](0016-read-write-separation.md) | Read and write paths are separated, routing declared per operation | Accepted | — |
| [0017](0017-deployment-models.md) | Deployment models — shared, dedicated, additional region, on-premise | Accepted — amended by 0038 | — |
| [0018](0018-configuration-scope.md) | Configuration scope — three levels, nearest ancestor wins, venue is the floor | Accepted | — |
| [0019](0019-dynamic-bundle-pricing.md) | A dynamic bundle has a fixed price and a variable allocation | Proposed | — |
| [0020](0020-ai-isolation-boundary.md) | Where AI runs, and what it is isolated from | Accepted 30 September — **amended by 0049** (Qdrant, a collection and a scoped token per tenant); section 2 **amended 2 October** (mandatory offline PII scrubbing and an in-cell guard model on every LLM call) | — |
| [0021](0021-qdrant-partitioning.md) | Qdrant — one collection per embedding model, tenant is the shard, scope is the filter | Accepted in part 30 September — **amended by 0049**: a collection per tenant replaces the shard | — |
| [0022](0022-conflict-policy.md) | Conflict policy is declared per operation, from a closed set of four | Accepted | — |
| [0023](0023-pii-separation.md) | Personal data lives apart from the append-only ledger | Accepted | — |
| [0024](0024-contract-first-delivery.md) | The contract is the deliverable, written before anything else | Accepted | — |
| [0025](0025-one-audience-field.md) | One field says who may call an operation | Accepted | — |
| [0026](0026-public-api-versioning.md) | Public API versioning, scopes and deprecation | Accepted | — |
| [0027](0027-payment-links.md) | A payment link is a credential, and payment converts the reservation | Accepted | BL-072 |
| [0028](0028-service-decomposition.md) | Seventeen modules, and the data boundary decides where they split | Accepted — **amended by 0055**: deployed as five units; ownership rule rewritten; **amended 2 October**: F&B owns its own catalogue so ticketing scales on its own | — |
| [0029](0029-outlet-configuration-scope.md) | Outlet configuration is outlet-scoped, and the path is the evidence | Accepted — extended 2 October with the outlet settings decided that day (payment timing, inside the venue or standalone, type and department, till layout, producing outlet, default station) | — |
| [0030](0030-deep-link-cold-entry.md) | A deep link is a pointer, not authorisation | Accepted | — |
| [0031](0031-contention-and-locking.md) | Contention is leased, not locked — and where a lock is unavoidable it is named | Accepted | — |
| [0032](0032-load-shedding-and-pooling.md) | A service refuses early or fails late — pooling, backpressure and breakers | Accepted — pooling amended by 0038; the per-tenant rate limit it deferred is decided by **0064** | — |
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
| [0047](0047-how-long-data-is-kept-and-where-it-goes-next.md) | **How long data is kept, and where it goes next** | Accepted — one number pending; retention per data category and region waits on research (2 October) | **CF-64** (closed), **CF-165** — amends 0042 |
| [0048](0048-guest-recurring-billing-is-commerce.md) | **Guest recurring billing is commerce, not the Control Plane** | Accepted | **BL-100** — relates to 0039, 0043, 0028 |
| [0049](0049-vectors-live-in-qdrant-one-collection-per-tenant.md) | **Vectors live in Qdrant from day one, one collection per tenant, each with its own token** | Accepted 30 September | SD-060 — amends 0009, 0020, 0021 |
| [0050](0050-one-autonomy-scale.md) | One autonomy scale; the approval tier is not an autonomy level | Accepted 30 September (records AI-D04) | SD-060 |
| [0051](0051-ai-ships-on-a-baseline-and-learns-per-tenant.md) | Every AI function ships on a baseline and learns per tenant | Accepted 30 September | SD-060, SD-061 |
| [0052](0052-one-recommendation-engine.md) | One recommendation engine; runtime in AI, configuration in Promotions | Accepted 1 October (records AI-D07–D09) | SD-060 |
| [0053](0053-risk-layer-ownership.md) | Owners keep their deterministic rules; AI owns cross-entity risk, alerts and cases | Accepted 1 October (records AI-D06) | SD-060 |
| [0054](0054-natural-language-analytics-goes-through-the-semantic-layer.md) | Natural-language analytics goes through the semantic layer | Accepted 1 October (records AI-D13, AI-D15) | SD-060 |
| [0055](0055-a-modular-monolith-deployed-as-five-units.md) | **A modular monolith, deployed as five units** | Accepted 30 September | **SD-001**, SD-002, SD-006 — amends 0028 |
| [0056](0056-one-id-type-and-time-partitioning-before-the-first-migration.md) | **One id type (UUIDv7), and time partitioning first** | Accepted 30 September | **SD-010**, SD-012, SD-009 — amends 0044, 0005 |
| [0057](0057-events-travel-on-rabbitmq-or-kafka.md) | Events travel on RabbitMQ or Kafka, behind one kernel interface | **Proposed** — waiting on the client's choice between RabbitMQ and Kafka | **SD-032** — completes 0033 |
| [0058](0058-one-relay-per-region-and-an-inbox-per-tenant-database.md) | One relay per region, and an inbox per tenant database | Accepted 30 September | SD-031, SD-030 — amends 0033 |
| [0059](0059-ai-phasing-against-the-six-month-plan.md) | AI phasing against the six-month plan | Accepted 30 September | SD-062, CF-57, CF-14 |
| [0060](0060-availability-targets-high-availability-and-disaster-recovery.md) | Availability targets per tier, and how they are met | **Proposed** — waiting on the client (what the 99.99% covers; SLO per tier; HA cost) and on Chinmay (one production HA mode) | **SD-045** |
| [0061](0061-replica-floors-per-deployable.md) | Replica floors are set per deployable and per zone | Accepted 1 October | SD-044 |
| [0062](0062-e-invoicing-through-a-provider-adapter.md) | E-invoicing goes through a provider adapter, and a rejection stops for a person | **Proposed** — waiting on the client (provider, mandate date, B2C scope, VAT 201 layout) | **SD-035**, CF-133 |
| [0063](0063-encryption-keys-and-biometric-templates.md) | Encryption and keys; biometric templates stay with the biometric vendor | **Accepted in part** — the biometric consent, enrolment-channel, minors, image-viewing and face-matching rules decided 2 October; the rest waits on the client's DPO (template location, retention floor) and the facial-reader vendor | SD-058, CF-35 |
| [0064](0064-per-tenant-limits.md) | Every tenant has a request budget, and a busy tenant cannot starve the others | Accepted 1 October | SD-042, SD-043 — amends 0032 |
| [0065](0065-on-sale-availability-is-read-from-a-short-cache.md) | Browse availability is read from a one-second cache; the hold decides | **Proposed** — waiting on Chinmay: it reverses F01/F07's "never cached" | **SD-038** |
| [0066](0066-the-on-sale-waiting-room-is-separate-from-the-ride-queue.md) | The on-sale waiting room sits at the edge, apart from the ride queue | Accepted 1 October | **SD-039** — amends 0012 |
| [0067](0067-one-device-register.md) | One device register; Access keeps only where a device is placed | Accepted 1 October | SD-004 — amends 0015 |
| [0068](0068-guest-admission-policy-lives-in-access-only.md) | Guest admission policy lives in Access only, and the offline package carries it | Accepted 1 October | SD-005, SD-052 |
| [0069](0069-in-park-3d-navigation-is-built-natively.md) | **In-park 3D navigation is built natively**, from a venue GLB model, a pathway and location file, and GPS | Accepted 30 September (client meeting, MoM 4.8) | — builds on the venue-map contract (19.2.55–19.2.60) |
| [0070](0070-configuration-moves-as-a-versioned-package.md) | **Configuration moves to production as a versioned package; the schema only moves forward** | Accepted 2 October (DEC-168, ADM-122) | — relates to 0039 |

> **0026 to 0037 were added on 30 September** (SD-053): they had been on disk since August and
> missing from this table. **0049–0051 and 0055–0059 were added the same day**, from the system-design
> review. **0069 was added the same day** from the client meeting of 30 September; it took the next
> number after the review drafts so none of them had to be renumbered.
> **0052–0054 and 0060–0068 joined on 1 October** (plan item 2.5), moved from the review drafts in
> `audit/ticvai/steps/SD/adr-drafts/` and brought in line with 0049 and 0055–0058 (the broker is RabbitMQ
> or Kafka per 0057, never Service Bus; Redis is Azure Managed Redis). Eight are Accepted. Four are
> Proposed with the open question and who answers in their status line: 0060, 0062 and 0063 wait on the
> client, and 0065 on Chinmay.
> **2 October:** Chinmay's decisions on the open questions amend 0009, 0020 and 0028, extend 0029, add a
> pending item to 0047, move 0063 to Accepted in part, and add **0070**
> (`docs/registers/decisions-2-october.md` lists each decision).

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
