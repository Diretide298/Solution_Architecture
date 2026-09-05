# ADR-0034: The cheapest AI call is the one that never reaches a provider

**Status:** Accepted
**Date:** 31 August 2026
**Related:** [ADR-0020](0020-ai-isolation-boundary.md) · [ADR-0021](0021-qdrant-partitioning.md) · [ADR-0032](0032-load-shedding-and-pooling.md) · BL-151

---

## Context

**Tokens are billed to the tenant.** `setAiProvider` takes a `credentialRef` that lives in the
secret store, `monthlyTokenCeiling` caps consumption, and `AiProviderError` has `quotaExceeded` and
`residencyRefused` as first-class outcomes. **BYOK is settled.**

**Which makes provider spend a commercial argument rather than an infrastructure one.** A tenant
whose AI Concierge costs more than it earns switches it off, and the workshop committed on 30 July
and never held is where that conversation was going to happen.

**`cache:answer` already exists and its note names the lever**: *forty questions repeat thousands of
times a day at a kiosk.* **It is keyed on question, scope and locale — exact match.** "What time do
you close?" and "when do you shut?" are two misses and two provider calls.

---

## Decision

### Retrieval, in the order a request meets them

**1 · Semantic cache before exact cache.** Embed the question, search `cache:answer` at a similarity
threshold, and serve on a hit. **An embedding costs a fraction of a completion**, so the trade is
favourable even when it misses.

**Threshold is per capability, not global.** A factual venue question tolerates 0.95; a
recommendation does not tolerate anything, and **`ai.policy` carries the threshold** so a tenant who
finds it wrong can move it.

**2 · Negative caching.** *No answer found* costs a full retrieval and a completion. **Cache the
miss** with a shorter TTL than a hit — the answer may exist tomorrow because somebody indexed it.

**3 · Single-flight.** Two hundred people ask the same thing when a ride breaks. **One provider
call, two hundred responses.** Same mechanism as ADR-0032 and the same reasoning — batching, not the pooling arithmetic ADR-0038 amended.

**4 · Two-stage retrieval.** Vector recall wide and cheap, then rerank narrow. `AiProviderCapability`
already has `rerank` — **this makes it a declared stage rather than an available option.**

**5 · Model cascade.** A small model answers, and escalates only when its confidence is below
threshold. `ai.suggestion.confidence` exists and nothing routes on it. **`ai.policy.cascade` names
the small model, the large one and the threshold between them.**

### Embedding and indexing

**Batch embedding.** `ingestKnowledgeDocument` embeds per document. **One provider call per N
chunks is an order of magnitude cheaper** and every provider supports it.

**`cache:embedding` already handles the incremental case** — content hash and model to a vector, so
editing fifty of twenty thousand chunks re-embeds fifty.

**Chunk size and overlap are declared per collection**, not global. **The single biggest lever on
retrieval quality** and currently nowhere: a venue FAQ and a maintenance manual do not chunk the
same way.

**Quantisation is declared and it is a decision.** `scalar` int8 is roughly four times smaller — 49
GB becomes 12 — **and it costs recall.** `binary` is smaller again and needs rescoring against full
vectors to be usable.

**Never a default.** A tenant whose search quality drops after an infrastructure change should be
able to find the line that did it.

**HNSW `m` and `ef_construct` per collection.** Defaults are tuned for neither our recall nor our
latency, and a collection built with the wrong ones needs a rebuild — **which is why this is a
creation decision, like the sparse index.**

### Cost and containment

**A per-request token budget**, not only a monthly ceiling. **One runaway conversation can spend a
tenant's month**, and the monthly cap discovers that after it has happened.

**Prompt prefix caching.** The system prompt and tenant policy are identical across every call in a
tenant and providers charge less for a cached prefix. **Order the prompt so the stable part comes
first** — otherwise the discount is unavailable regardless of provider support.

**Guardrail short-circuit.** A refusal a rule can decide never reaches a model. **Cheaper, faster,
and more consistent than asking a model to refuse.**

**Provider fallback with a breaker.** BL-151 named it. **Breaker opens, traffic moves to the
secondary, and `residencyRefused` is never retried elsewhere** — a residency refusal is a correct
answer and failing over would defeat it.

### Streaming is a different product

**Time-to-first-token and total latency are separate targets on a chat surface.** A concierge that
starts answering in 300 ms and finishes in 4 seconds is better than one that says nothing for 2.

**Declared per capability**: `chat` streams, `generateConfiguration` does not — nobody watches a
config draft assemble.

---

## Consequences

**`ai.policy` gains eight fields** — semantic threshold, cascade, chunking, quantisation, HNSW
parameters, per-request budget, streaming, fallback. **A tenant can now get their AI badly wrong**,
which is the cost of letting them get it right.

**The semantic cache changes what a cache hit means.** An exact hit is provably the same question;
a semantic hit is a judgement. **`ai.interaction` records which kind served the answer**, because
the first complaint about a wrong answer will be about a semantic hit and nobody will be able to
tell.

**Quantisation and HNSW are creation decisions.** Changing them means a rebuild, and a rebuild is
`shadow_collection` — **which already exists, and this is what it is for.**

---

## Alternatives considered

**Fine-tuning per tenant instead of retrieval.** Rejected for now: it moves cost from inference to
training, needs per-tenant data volumes nobody has, and **a fine-tune cannot be corrected by
editing a document** — retrieval can.

**One global embedding model.** Rejected because ADR-0021 already handles the case where residency
forces a local one, and pretending otherwise would break the tenant it was written for.

**Caching at the provider only.** Rejected: it saves tokens and not latency, and **the latency is
what a guest at a kiosk experiences.**
