# ADR-0060: Availability targets per tier, and how they are met

**Status:** Proposed · waiting on the client (which services the 99.99% agreed on 31 July covers, and whether it accepts an SLO per tier and the cost of zone-redundant HA) (Chinmay decided 1 October: production PostgreSQL is **zone-redundant on every tier**, the shared cell included; the Terraform follows)
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab and the client (99.99% was agreed with the client on 31 July) · **Consulted:** Dinesh (infrastructure)
**Finding:** SD-045 (high)
**Related:** ADR-0047 (RPO floor, decided 21 September) · ADR-0013 (local-first POS) · ADR-0038, amended by ADR-0040 · ADR-0042 (pinned instances) · ADR-0057 (broker: RabbitMQ or Kafka, the client's choice) · ADR-0058 (relay and inbox) · ADR-0049 (Qdrant) · ADR-0061 (replica floors) · ADR-0032 (Redis product, amended 30 September: Azure Managed Redis)

---

## What is open, and who answers

| Question | Who | Where it is asked |
|---|---|---|
| Which services does the 99.99% commitment cover? Does the client accept the SLO per tier below (99.99% for venue operations locally, 99.95% for cloud commerce)? | The client | Drafted in the client email of 30 September, item 3. **Not yet in the Decisions Register** |
| Does the client accept the cost of zone-redundant HA for every tenant (the cost workbook's HA sheet, about $8,050 a month for a production cell, against about $4,530 without HA)? | The client | Not yet in the Decisions Register |
| One production HA mode for PostgreSQL: the Terraform sets `SameZone` for the shared tier and `ZoneRedundant` only for dedicated and isolated tiers; the LLD promises zone-redundant for production. This ADR proposes zone-redundant for every production tenant | Chinmay | LLD open point (`docs/active/infra-answers-30-september.md` section 2) |
| Access to UAE Central for the DR module (access-restricted; needs a support request) | Dinesh, with Azure support | — |

Everything else below is our design and does not wait.

---

## Context

**A target was agreed; nothing says how it is met.**

- `docs/active/deployment-and-scaling-brief.md:70`: *"Target uptime 99.99%"*, agreed 31 July. Line 73: *"DR is a tenant-selectable module, not a default."* High availability is separate from DR.
- `docs/active/deployment-architecture-analysis.md:189`: *"99.99% was agreed on 31 July and a single cell does not deliver it."*
- ADR-0047 decided the RPO floor: asynchronous replication with a several-minute RPO by default; synchronous, near-zero RPO only on a pinned instance. It left RTO out on purpose: *"it belongs in the SOW beside the runbook"* (line 216).
- The only RTO and RPO numbers in the package are AI's: RTO 4 h, RPO 15 min (`ai-system-design.md` section 4.3).
- No ADR covers zone-redundant HA, point-in-time restore per tenant database, or a DR region.

**99.99% is 4.3 minutes of downtime a month.** A guest purchase in the cloud passes through the edge,
the container platform, Redis, the database and the broker in series. Each has its own published
SLA; the product of serial SLAs is lower than the smallest one. For example, 99.99% × 99.95% ×
99.99% × 99.9% is about 99.83%. (Illustrative. Check current Azure SLA figures for the chosen SKUs.)
Only an active-active, two-region design reaches 99.99% for the whole cloud path.

**What the region offers** (`docs/active/infra-answers-30-september.md` section 2, read 30 September):

- **UAE North** has zone-redundant HA for PostgreSQL Flexible Server, same-zone HA and geo-redundant backup.
- **UAE Central** is access-restricted (a support request is needed) and has no zone-redundant HA, but it has geo-redundant backup. UAE North's geo-backup pair is therefore in the same country, and `geo_redundant_backup_enabled = true` is compatible with residency once access to UAE Central is granted.

**One fact about the database changes the restore story.** Azure Database for PostgreSQL Flexible
Server restores a whole server to a new server. It does not restore one database. With a database
per tenant on a shared instance (ADR-0038, amended by ADR-0040), restoring one tenant needs an extra
step.

---

## Decision

**Proposed: an SLO per tier, zone-redundant HA for everyone in-region, DR as the tenant-selectable
module agreed on 31 July, and an honest statement to the client about what 99.99% would take.**

### SLOs per tier (monthly)

| Tier | SLO | How it is measured |
|---|---|---|
| **Venue operations: gate, POS, KDS** (local-first, ADR-0013) | **99.99%** of scans and sales complete locally | At the device and edge node. The cloud being down does not count against it |
| **Commerce in the cloud** (guest purchase, sync, payments) | **99.95%** (about 22 minutes a month) | Synthetic purchase every minute, per region |
| **Back office and operations** | **99.9%** | Synthetic sign-in and key reads |
| **AI and engagement** | **99.5%**; RTO 4 h, RPO 15 min (AI design 4.3) | Gateway health |

This is where 99.99% can honestly be offered: the venue keeps selling and scanning with the WAN down.

### High availability (every tenant, in-region)

- **PostgreSQL Flexible Server with zone-redundant HA** in UAE North. A synchronous standby in another zone: RPO zero on a zone loss, automatic failover in about one to two minutes (check the current figure). The NSG rules zone-redundant HA needs (5432 inside `snet-postgres`, outbound to the `Storage` service tag) are in the Terraform cell module's network plan.
- Every deployable runs at least two replicas across zones; `commerce` runs three (ADR-0061).
- **Redis: Azure Managed Redis**, zone-redundant by default (ADR-0032, amended 30 September; Azure Cache for Redis is retiring).
- **The event broker is zone-spread, whichever the client chooses** (ADR-0057). Modules see only the kernel interface, so HA is a property of the broker's deployment, not of the code:
  - RabbitMQ on CloudAMQP: a 3-node dedicated cluster; RabbitMQ on the Cluster Operator in our AKS: 3 nodes, one per zone, quorum queues on persistent disks.
  - Kafka on Event Hubs: the namespace's zone redundancy in UAE North (confirm for the chosen tier).
  - **The outbox is the record** (ADR-0058, partitions per ADR-0056). A broker outage delays delivery; it loses nothing, because the relay re-publishes what is not yet relayed and consumers de-duplicate through the inbox.
- **Qdrant: 3 nodes, one per zone, replication factor 2** (ADR-0049).
- pgbouncer as a pair.

### Backup and restore

- Automated backups with point-in-time restore, retention 35 days.
- **Geo-redundant backup to UAE Central** once access is granted (in-country, so residency holds).
- **A nightly logical dump per tenant database** to Blob in UAE North. This gives single-tenant restore and tenant extraction without restoring a whole server.
- **Single-tenant restore runbook:** restore the instance to a new server at the point in time, dump the one tenant database, restore it in place or repoint the tenant in the control plane. Target: 4 hours.
- **Qdrant:** a snapshot per collection, copied to Blob in UAE North by the Kubernetes CronJob of ADR-0049 (Qdrant cannot write to Blob itself). A tenant's vectors are restored from its collection snapshot; the tenant database keeps the chunk text and point references, so a collection can also be re-embedded.

### Disaster recovery (the tenant-selectable module)

- **With DR:** an asynchronous cross-region read replica in UAE Central (access-restricted: see the open questions). RPO minutes (ADR-0047's asynchronous default). RTO 4 hours with a rehearsed runbook.
- **Without DR:** geo-restore from backup. RPO about an hour, RTO up to 24 hours, best effort.
- **The broker is not geo-paired.** In a DR failover the broker in the DR region starts empty; the relay re-publishes from the promoted tenant database's outbox, and the inbox absorbs duplicates (ADR-0058). This holds for RabbitMQ and Kafka alike.
- **Qdrant in DR:** the tenant's collection snapshots are restored into the DR region's cluster, in the UAE only (ADR-0049's hosting condition).

### Drills

A restore drill each block (A, B1, B2, B3): one tenant from point-in-time restore, one from a logical
dump, one Qdrant collection from its snapshot. Measure and record the RTO.

---

## Options Considered

### Option A: 99.99% for everything, active-active in two regions

| Dimension | Assessment |
|---|---|
| Complexity | Very high. Multi-region writes or fast promotion, global routing, data conflicts |
| Cost | Roughly double the infrastructure, plus engineering beyond the six months |
| Scalability | High |
| Team familiarity | Low |
| Time to Block A | Not feasible in the programme |

**Pros:** Meets the agreed number literally.
**Cons:** Cannot be built by April 2027 by this team. The second UAE region is access-restricted and has no zone-redundant HA.

### Option B: SLO per tier, zone-redundant HA, DR as a module (proposed)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. Managed HA, runbooks, drills |
| Cost | Zone-redundant HA roughly doubles database compute (the workbook's HA sheet); DR only for tenants who buy it |
| Scalability | Per tenant; DR per tenant |
| Team familiarity | Medium. Managed features plus a runbook |
| Time to Block A | Terraform flags in SETUP-ENV; production built before the first live tenant |

**Pros:** Honest numbers that can be tested. Venue operations keep 99.99% locally.
**Cons:** The cloud commerce number is 99.95%, not 99.99%. Needs the client's agreement.

### Option C: Single zone, no HA

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Cost | Lowest |
| Scalability | Same |
| Team familiarity | High |
| Time to Block A | Fastest |

**Pros:** Cheap.
**Cons:** About 99.9% at best. A zone loss is an outage with data loss up to the last backup.

---

## Trade-off Analysis

A meets the words of the agreement and nothing else: it cannot be built in time. C is cheap and
breaks the agreement badly. B keeps 99.99% where the client's guests actually feel it (the gate and
the till, which are local-first by design) and states 99.95% for the cloud purchase path. The
conversation with the client is the real cost of B, and it is better held now than after an outage.

---

## Consequences

**Easier:** targets that can be tested; restore that works for one tenant; a broker choice that does not change the HA story.
**Harder:** the client conversation; the nightly per-tenant dump job; a Qdrant restore path beside the database's; drills every block.
**Revisit:** if a client buys 99.99% for cloud commerce, price Option A as a separate offer.

---

## Action Items

**Before Monday 5 October 2026**

1. [ ] None blocking. SETUP-ENV should expose zone-redundancy and HA flags in the `cell` Terraform module from the start. (1 pt)

**By the 23 October checkpoint**

2. [ ] Chinmay: one production HA mode for PostgreSQL (this ADR proposes zone-redundant for every production tenant); align the Terraform and the LLD.
3. [ ] The client: which services the 99.99% covers, the SLO per tier, and the cost of zone-redundant HA (add both to the Decisions Register).
4. [x] ~~Dinesh~~: Flexible Server zone-redundant HA and geo-backup in UAE North. **Answered 30 September** (`infra-answers-30-september.md` section 2): both available; the geo-backup pair is UAE Central.
5. [ ] Dinesh: request access to UAE Central for the DR module.
6. [ ] Write the RTO and RPO per tier into the SOW (ADR-0047 puts RTO there).

**Before the first production tenant**

7. [ ] **OPS-BACKUP**: nightly logical dump per tenant database, retention, restore script. (3 pts)
8. [ ] **OPS-RESTORE-DRILL**: first drill in Block A; runbook for single-tenant restore, including a Qdrant collection. (2 pts)
9. [ ] **OBS-SLO**: synthetic purchase and SLO dashboards per tier. (2 pts)
