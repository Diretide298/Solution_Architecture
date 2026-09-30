# ADR-0049: Vectors live in Qdrant from day one, one collection per tenant, each with its own token

**Status:** Accepted · 30 September 2026 · Chinmay Parab
**Date:** 2026-09-30 · **Deciders:** Chinmay Parab
**Finding:** SD-060 (high), with SD-019
**Source:** `docs/architecture/ai-system-design.md` sections 2.4, 5.8 and 8 (decision AI-D12 of 29 September chose pgvector "for now"; this ADR reverses it)
**Amends:** ADR-0021 (Qdrant partitioning, amended by this ADR) — a collection per tenant replaces the shard per tenant with a scope filter · ADR-0020 (AI isolation, amended by this ADR) and ADR-0009 section 2 (residency, amended by this ADR) — Qdrant per tenant on every tier
**Related:** ADR-0038, amended by ADR-0040 (database per tenant) · ADR-0046 (on-premise) · ADR-0047 (erasure and retention)

---

## Context

**Four positions were on record.**

- CH02 (client book): Qdrant everywhere, with a payload filter.
- ADR-0009 section 2: Qdrant for dedicated cells, pgvector for the shared tier.
- ADR-0020 (then Proposed): *"a cell without Qdrant has no AI"*.
- ADR-0021 (then Proposed): Qdrant, one collection per embedding model, the tenant as the shard, scope as a payload filter. Its central worry: *"Qdrant enforces nothing"*.
- The AI system design (AI-D12, 29 September) then chose pgvector in the tenant database "for now".

**Chinmay decided on 30 September: Qdrant from the start.** Retrieval is a first-release feature
(the guest concierge is in Block A) and it should run on the store it will grow on, not move later.

**A shared collection cannot be enforced by the store.** Qdrant's granular JWT RBAC scopes a token to
collections. The payload-filter RBAC that could once restrict a token to a tenant's points inside a
shared collection was removed in Qdrant 1.16. So in a shared collection, tenant isolation would rest
on the application remembering a filter on every call, which is exactly ADR-0021's worry. A
collection per tenant, with a token that can reach only that collection, makes the store enforce it.

**The package is not ready for either store today.** `ai.chunk_embedding.dense` is `text` (SD-019),
and 30 of the 39 AI operations in the slice are marked store `qdrant` in the lineage, which this
decision confirms.

**The sizes are small.** About 20,000 chunks per tenant, 1024 dimensions (design 5.8). BGE-M3 gives
dense and learned sparse vectors, fused by reciprocal rank; Qdrant holds both as named vectors.

---

## Decision

**Every tenant's vectors live in Qdrant, in collections of its own, from day one and on every tier.**

### One collection per tenant, per embedding model, behind an alias

- A tenant gets one collection per embedding model, for example `t_<tenantId>_bge-m3-v1`.
- The retrieval client never names that collection. It reads the **alias `tenant_<tenantId>`**.
- **A model change is a shadow collection plus an alias swap:** re-embed into a new collection in the background, evaluate it (ADR-0021's two-stage evaluation), then point the alias at it and drop the old one. No reader changes.
- The collection is provisioned at tenant onboarding, with the tenant database (ADR-0039).

### Each tenant has its own token, scoped to its collection

- **Qdrant granular JWT RBAC:** each tenant has a JWT that grants access only to its own collections and alias. The retrieval client for a tenant holds only that tenant's token.
- Tokens live in the cell's Key Vault and rotate on a schedule and on demand. The API key that can sign them never reaches the application.
- **So a bug that forgets the tenant cannot read another tenant's vectors:** the store refuses it.

### Venue scope is a payload filter the client always adds

- Inside a tenant, points carry `venue_id` and `scope_path` in their payload, indexed.
- **The single retrieval client has no scope parameter** (ADR-0021's rule). It reads the caller's scope from the request context and always adds the filter. A caller cannot pass a wider one.

### Hosting

- **Self-hosted Qdrant in Azure UAE North** (residency, ADR-0009), a **3-node cluster** with replication for high availability, per cell. Check whether Qdrant Hybrid Cloud on our own AKS is an option; it would keep the data in our cluster with Qdrant managing operations.
- **Venue-local on-premise profile (ADR-0046): a single node.**
- **Backups:** snapshots per collection to storage in the UAE, on the tenant database's schedule, and restore tested per tenant.

### Erasure and offboarding

- **Erasure** deletes points by the guest's or document's payload key.
- **The tenant database keeps the point references** (`ai.chunk_embedding`: point id, collection, source document, guest where there is one). That is what makes erasure provable: the database says which points existed, and the delete is checked against it.
- **Offboarding** deletes the tenant's collections and alias, and revokes its token, with the tenant database (ADR-0047).

### Limits

- Qdrant Cloud's default cap is 1,000 collections per cluster. At 10–200 tenants, with one or two collections each, that is well inside it.
- **Revisit** past about 500 tenants in one region: custom sharding, or a second cluster in the region.

---

## Options Considered

### Option A: pgvector in the tenant database

| Dimension | Assessment |
|---|---|
| Complexity | Low. An extension in a database we already run |
| Cost | Marginal |
| Scalability | Comfortable at 20,000 chunks per tenant |
| Team familiarity | High. PostgreSQL team |
| Time to Block A | Fits |

**Pros:** RLS enforces scope; erasure follows the tenant database; one store fewer.
**Cons:** A move to Qdrant later for scale. **Rejected by Chinmay on 30 September: Qdrant from the start.**

### Option B: Qdrant, one collection per tenant, a token per tenant (decided)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. A third store to run, back up and keep resident; collection and token lifecycle per tenant |
| Cost | About USD 600–700 a month per cell for a 3-node HA cluster (design 5.8) |
| Scalability | High. 1,000 collections per cluster by default; revisit past about 500 tenants per region |
| Team familiarity | Low. Nobody on the team has Qdrant experience (skills matrix) |
| Time to Block A | Fits with the concierge's retrieval work; the cluster is a setup task |

**Pros:** Isolation between tenants is enforced by the store, not by a filter. Built for vector search and hybrid dense-plus-sparse retrieval. No migration later.
**Cons:** A second place tenant data lives: backup, recovery, residency and erasure each need their own path.

### Option C: Qdrant, one shared collection with a tenant filter (ADR-0021 as written)

| Dimension | Assessment |
|---|---|
| Complexity | Low per tenant |
| Cost | Same cluster |
| Scalability | Highest |
| Team familiarity | Low |
| Time to Block A | Same |

**Pros:** Fewest collections.
**Cons:** **Rejected: tenant isolation would be application-enforced only.** With payload-filter RBAC removed in Qdrant 1.16, no token can be limited to one tenant's points.

### Option D: A Qdrant instance per tenant

| Dimension | Assessment |
|---|---|
| Complexity | High. An instance to run per tenant |
| Cost | Grows with tenants, not load: too costly |
| Scalability | Poor to operate |
| Team familiarity | Low |
| Time to Block A | Slow |

**Pros:** Strongest isolation.
**Cons:** Too costly for 10–200 tenants, and cost follows tenancy (ADR-0032, pooling amended by ADR-0038, warns against that).

---

## Trade-off Analysis

B and C run on the same cluster. What separates them is who enforces the tenant boundary: in B the
store refuses a wrong token; in C the application must never forget a filter. B costs more
collections, which the limits above allow. A is cheaper and simpler, and was ruled out by the
decision to run Qdrant from the start. D buys nothing B does not, at a cost per tenant.

---

## Consequences

**Easier**

- Tenant isolation for vectors is enforced by Qdrant, not by convention.
- A model change is a shadow collection and an alias swap.
- No vector-store migration later.

**Harder**

- **A second store to back up, recover and keep resident**, with its own snapshots, restore drill and residency answer.
- **Compliance:** the security approval for Qdrant, outstanding since 12 August, was given on 30 September (Chinmay) on one condition: Qdrant is hosted only on servers in the UAE. That condition binds every tier, including disaster recovery and backups.
- **Skills:** nobody on the team has run Qdrant (skills matrix). The two AI engineers own it with DevOps.
- Erasure has a second home: the tenant database records the point references so a delete can be proven.

**Revisit**

- Past about 500 tenants in one region (custom sharding or a second cluster).
- If a tenant passes about 2 million chunks, or retrieval p95 exceeds 150 ms, look at shards for that tenant's collection.

---

## Action Items

**Before Monday 5 October 2026**

1. [x] Chinmay: Qdrant from day one, a collection per tenant with a collection-scoped token (30 September).
2. [ ] Package: lineage store `qdrant` confirmed on the AI operations; `ai.chunk_embedding` holds the point reference (point id, collection, model, source, guest), not the vector; ADR-0021, ADR-0020 and ADR-0009 amendments (done 30 September). Re-derive, mirrors, check.
3. [x] Security approval for Qdrant: given 30 September, on condition of UAE hosting only (no client question needed).
4. [x] ~~Dinesh~~: check Qdrant Hybrid Cloud on our own AKS in UAE North as an alternative to plain self-hosting. **Closed 30 September: self-hosted chosen**; Hybrid Cloud needs an Enterprise contract and sends collection metadata to `cloud.qdrant.io` (amendment below).

**Sprint 1–2**

5. [ ] **SETUP-QDRANT** (DevOps): the 3-node cluster in dev and staging via Terraform (the `qdrant` node pool) and the official Helm chart, pinned to 1.16 or later; TLS on the service; the snapshot CronJob that copies snapshots to Blob in the UAE; a check that a collection-scoped token works through the alias; monitoring. (3 pts)
6. [ ] **AI-ENGINE-QDRANT** (AI engineers): collection-per-tenant provisioning at onboarding with the alias, per-tenant JWT issuance and rotation, the retrieval client with the mandatory venue filter, erasure and offboarding paths, snapshots. (about 5 days)
7. [ ] C4 retrieval: embedding and reranker in the cell, hybrid retrieval on Qdrant (design section 7).

---

## Amendment — hosting, the token key and backups, 30 September 2026

**Status unchanged: Accepted.** Source: `docs/active/infra-answers-30-september.md` section 1 (Qdrant
documentation and pricing pages, read 30 September 2026).

### Decision: self-host open-source Qdrant on our AKS in UAE North

- **Open-source Qdrant (Apache 2.0), the official Helm chart, on the cell's own AKS in UAE North**: 3 nodes,
  one per zone, replication factor 2, on the tainted data pool (`qdrant` node pool, E4s v5, Premium SSD P15
  256 GB each). No licence fee; the VMs and disks are already in the cost workbook.
- **Pin Qdrant 1.16 or later.** This ADR's reasoning assumes payload-filter RBAC is gone (deprecated in 1.15,
  removed in 1.16).
- **TLS on the Qdrant service** (or a mesh). An API key over plain HTTP is not acceptable.
- The plain Helm chart gives no zero-downtime upgrades, automatic shard rebalancing or cluster backup. Those
  are ours: SETUP-QDRANT and the runbook own them.

### Collection-scoped JWT: how it is signed, and what rotation means

- **JWT RBAC is in open-source Qdrant since v1.9**: set `service.api_key` and `service.jwt_rbac: true`.
- **The token is HS256, signed with the admin API key itself.** The token issuer holds `service.api_key` and
  mints each tenant's token with `{"access":[{"collection":"t_<id>_bge-m3-v1","access":"r"}]}` and an `exp`.
- **Key Vault holds the API key as a *secret*, not an HSM key**: Key Vault keys cannot do HMAC signing. Only
  the issuer reads it; `ticvai-ai` never does (as the Decision above already says). The HSM tier of Key Vault
  is justified by the per-tenant keys, not by Qdrant.
- **Rotating the API key breaks every tenant's token at once**; Qdrant does not migrate tokens. Rotation is
  therefore a **planned procedure**, not a schedule that runs by itself:
  1. Announce a window; put AI retrieval in its degraded mode (no RAG answers, the rest of the platform
     unaffected).
  2. Write the new key to Key Vault as a new secret version.
  3. Roll the Qdrant pods one at a time onto the new `service.api_key`.
  4. The issuer reissues every tenant's token with the new key; the retrieval clients reload them.
  5. Verify one read per tenant; disable the old secret version.
  An urgent rotation after a leak follows the same steps without the announcement. Per-tenant tokens still
  expire and are reissued on their own schedule (`exp`), which needs no rotation of the key.
- **Aliases: test on day one.** The documentation does not say whether a token scoped to the collection works
  through the alias `tenant_<id>`. The `access` claim is a list, so the token can name both the collection and
  the alias if it has to.

### Backups: snapshots do not go straight to Blob

- Qdrant's snapshot storage supports only `local` and `s3`; **Azure Blob is not a native target.**
- **Route:** take each collection's snapshot to local disk, then a **Kubernetes CronJob copies it to the UAE
  North storage account** with azcopy under workload identity, and prunes the local copy. An S3-compatible
  gateway in front of Blob is the alternative if the CronJob proves fragile.
- Azure Disk snapshots of the Qdrant disks are a second line, not a replacement: Qdrant's own snapshot is the
  consistent one.

### Rejected

- **Qdrant Hybrid Cloud (on our AKS, operated by Qdrant's operator).** The data stays in our cluster, but the
  cloud agent keeps an outbound connection to `cloud.qdrant.io` and sends metrics, cluster metadata and
  collection information. Our collection names carry tenant ids, so tenant ids would leave the UAE. It is
  also Enterprise-only, with the price on request, and whether it exposes `jwt_rbac` is not stated.
- **Qdrant Managed Cloud.** Whether Azure UAE North is offered could not be confirmed (no public region list),
  and there are no list prices. Ruled out until Qdrant shows a UAE North region in writing.
- **Qdrant Private Cloud** (Enterprise operator, no connection to Qdrant) fixes Hybrid's metadata problem, at a
  price on request. It stays the fallback if running Qdrant proves too much for the team.

### Sizing check

About 0.2 GB per tenant (20,000 chunks, dense and sparse vectors, HNSW index). At 200 tenants and replication
factor 2 that is under 100 GB of working set across three 32 GB nodes; the 256 GB disks are comfortable.
