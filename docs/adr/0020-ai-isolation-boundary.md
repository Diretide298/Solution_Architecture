# ADR-0020 — Where AI runs, and what it is isolated from

**Status:** Proposed · 17 August 2026
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

## Decision

**Three isolation boundaries, each drawn for a different reason.**

### 1. Retrieval and the index stay in the cell

Qdrant runs per cell. **Embeddings are derived from tenant data and are tenant data** — a vector
of a guest's support case is not anonymous because it is a vector.

This also makes residency automatic rather than argued: a cell in a jurisdiction keeps its
index in that jurisdiction, and ADR-0001's boundary does the work without a second mechanism.

**ADR-0001 is superseded in part by ADR-0014** — a shared cell holds several tenants — so the cell
is a residency boundary here and not a tenant one. ADR-0021 carries the tenant boundary.

### 2. Inference is a call out, and the prompt is the only thing that leaves

The provider is called from inside the cell. **What crosses a border is the prompt and the
retrieved context, never the store**, and `ai.policy.maskedFields` is what governs it — failing
closed, so an unset masking list sends nothing rather than everything.

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

**Whether the on-premise model gets AI at all** (CF-61). An on-premise venue has no route to a
hosted provider and no local model unless one is shipped. **The honest default is no assistant
on-premise**, and that should be said in the contract rather than discovered at install.

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
