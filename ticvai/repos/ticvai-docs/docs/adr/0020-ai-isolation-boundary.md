# ADR-0020 — Where AI runs, and what it is isolated from

**Status:** Accepted · 30 September 2026 · Chinmay Parab — amended by [ADR-0049](0049-vectors-live-in-qdrant-one-collection-per-tenant.md): Qdrant per tenant on every tier (a collection and a scoped token per tenant); the analytical store is the AI log database. Proposed 17 August 2026 · section 2 amended 2 October 2026 (Chinmay): **every LLM call is scrubbed offline first, and an in-cell guard model reads both ways**, whatever the tenant's residency class · amended 3 October 2026 (Chinmay): **the guard is the provider's content-safety service, not a model we host**; the Presidio scrubber stays in our worker
**Relates to:** ADR-0001 (cells — **superseded in part by ADR-0014**), ADR-0009 (residency),
ADR-0016 (read routing), CF-64 (retention)

---

## The question ADR-0009 did not answer

ADR-0009 settled the **legal** question: UAE law does not mandate domestic storage, so a
third-party LLM API is not automatically non-compliant, subject to a transfer risk assessment.

It said nothing about **where the AI service runs**, and that is a different question with an
operational answer rather than a legal one. The contract exists, the tables exist, and nobody
has decided whether AI lives inside a cell or outside it.

**This matters now** because `ai.interaction` is currently specified to sit in the same
PostgreSQL instance as `access.scan_event`, and those two tables have nothing in common except
a connection pool.

---

## What is wrong today

**Every AI table is in the transactional database.** `ai.interaction` records a row per prompt
with its response, sources, tokens and cost. `ai.message` records the same content again as
conversation history.

Three consequences, none of them intended:

**An audit table with no retention grows forever** (CF-64). It is the fastest-growing table in
the platform and the only one nobody reads operationally.

**A runaway AI workload competes with a gate scan for connections.** `validateAccess` runs tens
of thousands of times a day and must not queue behind a report-generation prompt. ADR-0016
already separates analytical reads onto a replica for exactly this reason; AI writes were never
considered.

**Prompt content is personal data in the transactional store.** A guest's question contains
whatever they typed. Putting it beside `pii.subject` is defensible; putting it there
*accidentally*, with no retention and no erasure path, is not.

---

## Amended 4 October 2026: the embedding model, its reranker and the scrubber run on our GPU node pool; no LLM

**Decided by Chinmay, 4 October 2026** (change entry CHG-R11-001, reversing CHG-R1S-026): *"we have to host for
embeddings only not for LLM"*; *"its a sdk we can host it wihtin our embeddings server cant we ? also the arabic
NER"*; *"Naaa dont keep AI CPU node at all"*.

- **The AI pool is a GPU node pool:** one AI GPU node pool: Azure NV6ads A10 v5 in UAE North (6 vCPU, 55 GB, a sixth of an A10 with 4 GB), one node without high availability and two with it, one per zone; on AWS (me-central-1, UAE) a g6.2xlarge-class node (one L4, 8 vCPU), its price and regional availability to confirm. It is still tainted and isolated as this ADR says; it
  runs the `ticvai-ai` pods (floors as ADR-0061: real-time 2, interactive 1, batch 0, about 1 vCPU a pod, since
  they mostly wait on the provider's streamed answer), Presidio's recognisers on its CPU, and on its GPU at fp16
  BGE-M3, its reranker and the Arabic NER. There is no separate AI CPU pool and no separate Presidio pool.
- **Sizing is an assumption** until the Sprint 2 benchmark; the step up is NV12ads A10 v5 (12 vCPU, 8 GB of GPU
  memory), taken on CPU saturation or GPU memory pressure.
- **Scrubbing stays mandatory and fails closed:** with the GPU node down the scrubber is down, and the LLM call is
  refused `503 scrubber-unavailable`, never sent raw.
- **Embeddings never leave the cell:** hybrid retrieval is our BGE-M3 dense vectors with Qdrant's BM25 sparse
  index, reranked by our reranker; the vectors stay in our Qdrant (ADR-0049).
- **Still no LLM of ours:** LLM calls stay with the providers and the guard stays the provider's content-safety
  service. In the 3 October amendment below, the scrubber "inside our own worker", "No GPU pool" and "Embeddings
  too" are superseded.

---

## Amended 3 October 2026: the guard is the provider's content-safety service; we host no model

**Decided by Chinmay, 3 October 2026** (`docs/active/decisions/answers-3-october-gate-and-hosting.md`; change
entry CHG-R1S-002): *"We are not hosting anything unless client asks it."* A guard model is itself an LLM and
needs a GPU host, so item 3 of the amendment above changes; items 1, 2, 4 and 5 stand.

- **Item 3 now reads:** the guard on input and output is **the provider's content-safety service**: Azure AI
  Content Safety in UAE North for a `uaeOnly` tenant, the provider's own moderation for BYOK and
  `globalAllowed`. Qwen3Guard is not hosted; a self-hosted guard comes back only if a client asks for
  self-hosting (Chinmay may drop the guard altogether). The Arabic gap the 2 October text names is covered by
  the golden set: Arabic harmful prompts run against the safety service before each release.
- **[Where it runs superseded 4 October, CHG-R11-001: on the AI GPU node pool.]** **The scrubber stays, unchanged:** Microsoft Presidio and the Arabic NER model are **a CPU library inside our
  own worker**, not a hosted model, and scrubbing is mandatory in every residency class.
- **Still fails closed:** with the scrubber or the safety service down the call is refused
  (`503 scrubber-unavailable`), never sent raw; a blocked message or reply is `422 guard-refused`.
- **[Superseded 4 October, CHG-R11-001: the AI pool is a GPU node pool, still with no LLM.]** **No GPU pool, no in-cell model.** The cell runs no LLM; the AI goes through providers (Core42 Compass by
  default, OpenAI UAE as fallback, BYOK), ADR-0009 as amended the same day.
- **[Superseded 4 October, CHG-R11-001: BGE-M3 and its reranker are ours, in the cell.]** **Embeddings too** (later the same evening, CHG-R1S-026): the provider's embedding model on the UAE route
  (OpenAI UAE `text-embedding-3-large` or Core42), through the scrubber and the residency class like any call;
  no embedding model and no CPU embeddings in the cell. The vectors stay in our Qdrant (ADR-0049).

---

## Amended 2 October 2026: mandatory offline scrubbing, and a guard model both ways

**Decided by Chinmay, 2 October 2026:** *"we may need to scrub personal info no matter what: an offline
NLP-based scrubber or censorship"* (DEC-542 and DEC-543 in `docs/registers/decisions-2-october.md`; change
entry CHG-DOC-005). Research: `docs/active/research/ai-ml-model-selection-2-october.md`, tasks T12 and T13.

Section 2 said the prompt is the only thing that leaves, governed by `ai.policy.maskedFields`. Masking by
field covers the data the platform puts in a prompt; it does not cover what a guest or a member of staff
types (a phone number in a question, an Emirates ID pasted into a chat). So, **for every LLM call, whatever
the tenant's residency class** (ADR-0009, amended the same day):

1. **Detection, offline, inside the cell.** Microsoft Presidio, with custom recognisers for Emirates ID
   numbers, UAE phone numbers, passport numbers, IBANs, Luhn-checked card numbers and email addresses, plus
   an Arabic named-entity model (for example CAMeL Tools) for Arabic names and places. Field masking from
   the schema (`maskedFields`) stays the first control; the scrubber is the second, for free text.
2. **Reversible placeholders.** Detected values are replaced by placeholders (`[GUEST_1]`, `[PHONE_1]`).
   The map from placeholder to value stays in the cell and never travels with the prompt; the reply is
   re-filled before it reaches the user.
3. **A guard model on input and output.** An offline guard model, **Qwen3Guard** (it covers Arabic; Azure
   AI Content Safety's harm models were not trained on Arabic), checks the prompt before it leaves and the
   answer before it is shown (the streaming variant for streamed answers).
4. **Mandatory, not tied to residency.** A UAE-only tenant is scrubbed as well: in-country inference
   changes where the data goes, not whether the model should see it. A scrubbed prompt is still
   pseudonymised personal data under PDPL, so scrubbing reduces the transfer, it does not remove the
   transfer duties of ADR-0009 section 3.
5. **Fails closed.** If the scrubber or the guard is unavailable, the call is refused, exactly as an unset
   masking list sends nothing rather than everything. No LLM call is made around them.

**What proves it** (the prevention, CHG-DOC-005, open until it exists): a gateway test corpus in Arabic and
English with Emirates IDs, phone numbers, IBANs and card numbers, in which no raw value may appear in an
outbound prompt, and a test that a scrubber or guard outage refuses the call. The AI gateway contract
(`contracts/satellite/ai.yaml`) states scrubbing as mandatory, and the gateway task carries the scrubber and
the guard; both are owned outside this ADR.

---

## Amended 30 September 2026

**Accepted with two corrections from ADR-0049** (and the AI system design, section 8):

1. **Retrieval runs on Qdrant per tenant, on every tier.** Section 1's "Qdrant runs per cell" stands as
   the cluster, but inside it each tenant has its own collection (per embedding model, behind the alias
   `tenant_<tenantId>`) and its own JWT scoped to that collection. The tenant boundary is enforced by
   Qdrant, not by a filter; venue scope inside a tenant is a payload filter the retrieval client always
   adds. Self-hosted in Azure UAE North, 3-node HA; a single node in the venue-local profile (ADR-0046).
2. **"The analytical store" in section 3 is the AI log database**, not a general analytical replica.

Sections 2 and 3's boundaries (the prompt is the only thing that leaves; AI's logs move off the
transactional primary) stand. The AI deployable's Postgres role stays read-only on the transactional
schemas (ADR-0055).

---

## Decision

**Three isolation boundaries, each drawn for a different reason.**

### 1. Retrieval and the index stay in the cell

Qdrant runs per cell. **Embeddings are derived from tenant data and are tenant data** — a vector
of a guest's support case is not anonymous because it is a vector.

This also makes residency automatic rather than argued: a cell in a jurisdiction keeps its
index in that jurisdiction, and ADR-0001 (retired — the split rule is now ADR-0038, which supersedes ADR-0014 and amends ADR-0017)'s boundary does the work without a second mechanism.

**ADR-0001 is superseded in part by ADR-0014** — a shared cell holds several tenants — so the cell
is a residency boundary here and not a tenant one. ADR-0021 carries the tenant boundary.

### 2. Inference is a call out, and the prompt is the only thing that leaves

The provider is called from inside the cell. **What crosses a border is the prompt and the
retrieved context, never the store**, and `ai.policy.maskedFields` is what governs it — failing
closed, so an unset masking list sends nothing rather than everything. *(Amended 2 October 2026:
every prompt is also scrubbed offline and checked by a guard, both failing closed; see the amendments
above: since 3 October the guard is the provider's content-safety service.)*

`x-ticvai-scope-level: region` on `setAiProvider` is what makes this enforceable: which
providers a region may use is a residency decision, and a region with no adequacy finding gets a
locally hosted model or no assistant.

### 3. AI's own tables move off the transactional primary

**`ai.interaction`, `ai.message` and `ai.conversation` are append-only logs with an analytical
read pattern**, and they belong with the analytical store rather than beside `orders.payment`.

`ai.policy`, `ai.provider`, `ai.index_source` and `ai.knowledge_collection` stay on the primary
— they are small, they are configuration, and they are read on the hot path of every AI call.

**The dividing line is the same one ADR-0016 already draws**: configuration and current state on
the primary, history on the replica.

---

## What this does not decide

**Whether a shared cell can share an AI deployment.** Several small tenants in one cell already
share a database with logical isolation, and sharing a Qdrant instance with per-tenant
collections is the same trade. **It is a cost decision, and the collection boundary already
provides the isolation** — this ADR does not force one instance per tenant.

**Whether the on-premise model gets AI at all** (CF-61). **Closed by
[ADR-0046](0046-on-premise-has-two-configurations.md), and the answer is four-way rather than the
two it looks like.** The line is not connectivity, it is data egress: **AI inference is data
traffic, not control traffic**, so a connected site does not get the assistant merely by being
connected.

| configuration | AI |
|---|---|
| `onPremiseIsolated`, no model shipped | **none** — the honest default, said in the contract rather than discovered at install |
| `onPremiseIsolated` + client-hosted local model | **yes, locally.** Its own Qdrant collection, forced by vector dimensionality — see [ADR-0021](0021-qdrant-partitioning.md) |
| `onPremiseConnected`, control channel only | **none.** The channel is PII-free by construction ([ADR-0043](0043-the-control-plane-splits-on-personal-data.md)); inference is not |
| `onPremiseConnected` + explicit inference-egress consent | **yes, hosted.** A separate consent, subject to [ADR-0009](0009-ai-data-residency.md) |

**An isolated site with its own GPU gets a better assistant than a connected site whose client will
not let content leave.** Counter-intuitive, and correct.

---

## Consequences

**Retention becomes urgent rather than theoretical.** Moving the logs does not stop them
growing; it stops them growing *in the wrong place*. CF-64 still has to answer how long a prompt
is kept, and prompts may contain personal data.

**Erasure has a second home.** `pii.erase_subject` must reach `ai.interaction` and the Qdrant
payload, and `removeIndexEntry` exists for the second. **A knowledge base still answering from
an erased subject is an erasure that did not happen** — already stated in the RAG source
register, and this ADR is where it becomes a storage requirement.

**A cell without Qdrant has no AI.** That is a provisioning consequence: `provisionCell` must
know whether the tenant bought AI, and a cell provisioned without it cannot gain the assistant
by configuration alone.

**Cost is per cell, not per platform.** A vector store in every cell is more expensive than one
centrally, and that is the price of the residency answer being automatic rather than argued.
Worth stating in the commercial model rather than discovering it in an invoice.

---

## Addendum — the rule was already being broken

**17 August, same day.** An isolation sweep run immediately after this ADR was written found two
operations that contradicted it. Both had passed every validator, because **every operation
existed and resolved to a real table** — which is precisely the class of defect a checker cannot
see.

### `generateVenueLayout` wrote into `seating.import_job`

**AI writing directly into a transactional contract.** It would have let a generated seat layout
reach a real seat map without a person looking at it, which is the one thing the read-only rule
exists to prevent — and a seat manifest is always wrong the first time in a way only a person
notices.

Corrected: it writes `ai.layout_draft` and stops at `previewReady`. The draft enters
`seating.import_job` at that contract's existing human commit step, so the review gate is the
one seating already has rather than a second one invented for AI.

### `askReportingQuestion` wrote no `ai.interaction`

The reporting contract was brought under AI governance earlier the same day — provider
resolution, masking list, audit record. **The lineage was never updated to match**, so
requirement 8.3.55 was satisfied in the contract and not in the data.

**A governance rule stated in prose and absent from the lineage is a rule nobody can verify**,
and this is the second time today that gap has appeared.

### What this says about the rule

The four rules in `ai-platform.md` are stated as principles and were being checked by nobody.
**The sweep that found these is not automated and probably cannot be**, because it asks whether
a write crosses a boundary that only a reader knows about.

What is now checkable, and is: **no non-AI contract writes an AI table, and no AI operation
writes outside its own stores.** That is a lineage query, and it would have caught both.

**The rule has two stated exceptions and neither is a loophole.**

`askReportingQuestion` and `saveNaturalLanguageQuery` live in `reporting` and write `ai.interaction`
— **that is the governance record, and requiring it is the opposite of a bypass.** They were
brought under AI governance rather than being allowed to escape it, and the alternative was a
model call with no audit trail.

Every `cache:*` table is exempt from the outward rule. **A cache is derived from something already
read, invalidated by an event already consumed, and losable without consequence** — nothing treats
one as a source of truth, which is what the read-only rule is protecting.

**Both exceptions are in `check-package.py` and this ADR now says so.** An absolute rule with an
undocumented allowlist is worse than a rule with two stated exceptions, because the first invites
a third that nobody argues for.

### The rule extended to the AI tables of 29 September

**Added 30 September** (the 29 September pass, AI2 baseline). The day-one baseline added five
AI-owned tables: `ai.venue_settings` (the venue AI profile, `setAiVenueSettings`),
`ai.history_import` and `ai.history_observation` (a venue's own history brought in by
`importVenueHistory`), `ai.capability_maturity` (where each capability stands between baseline and
learned) and `ai.training_run` (each per-tenant training run). **They are inside the boundary and
the lineage rule covers them like every other `ai.*` table**: only AI operations write them, no
non-AI contract writes them, and the operations that write them write nothing outside `ai.*`,
`qdrant*` or `cache:*`. A history import reads the tenant's platform tables through their owners'
read APIs and copies what it needs into `ai.history_observation`; it never writes back.
