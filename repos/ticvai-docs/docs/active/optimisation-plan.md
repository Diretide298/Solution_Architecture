# Optimisation adoption plan

**Deferred by decision, 17 August 2026.** Seven of fourteen techniques adopted, sequenced against
one hard dependency. Nothing built yet.

---

## The dependency that sets the order

**Nothing here happens before the embedding model is chosen**, because hybrid retrieval and both
chunking changes interact with it, and all three change what is stored.

    benchmark (ADR-0021 addendum)
      └─▶ model chosen
            └─▶ storage-shaping work  ← must land BEFORE any tenant is indexed
                  └─▶ index
                        └─▶ caches    ← can land any time after
                              └─▶ rerank, cheaper synthesis model

**Doing the caches first would work. Doing the chunking last would not.**

---

## Stage A — before any tenant is indexed

Retrofitting any of these means a full rebuild per tenant, through the shadow swap in
`states/ai-index-job.yaml`.

| | What changes |
|---|---|
| **Hybrid retrieval** | `KnowledgeCollection` gains sparse vector config — **a collection created dense-only cannot gain a sparse index without a rebuild**. `semanticSearch` gains a mode. **ADR-0021 gains the `idf` scoping rule**, because with payload partitioning BM25 statistics are computed shard-wide and a term common at one venue gets one IDF for both |
| **Parent-child retrieval** | `IndexSource.chunkStrategy` gains a value; `ai.index_entry` gains a parent reference. **Fixes a failure we would otherwise hit** — a refund policy paragraph retrieved without its section heading answers the wrong question confidently |
| **Semantic chunking** | Another `chunkStrategy` value. Fixed-token splitting cuts a rule in half, and policies and FAQs are where that shows |
| **Embedding cache** | `ai.index_entry` gains a content hash; a cache store appears in the schema. **A tenant editing fifty of twenty thousand chunks re-embeds fifty, not twenty thousand** |

**Why hybrid is first among these:** it is not an optimisation. A venue corpus is full of proper
nouns — "Yas Waterworld", "Bronze Annual Pass", menu item names — and dense retrieval is good at
meaning and poor at exact tokens. Half our queries are exact tokens.

## Stage B — before the guest concierge ships

These change CF-14's economics enough that **setting the cap without them would set it wrong.**

| | What changes |
|---|---|
| **Query result cache** | A cache store. `AiPolicy` gains a TTL and an enable flag. The nine invalidating events gain a cache consumer. **Scope is part of the key** — a cache keyed on the question alone is a cross-venue leak wearing a performance hat |
| **Provider prompt caching** | Nothing structural. A constraint on prompt assembly order, and a note in `ai-platform.md`. **A prompt assembled in the wrong order silently loses the discount** |
| **Cheaper synthesis model for guests** | Nothing. `AiProvider.capability` already allows a different provider per capability — **the contract supports it and nobody has decided it** |

**Why the query cache is the largest item on this page:** staff queries are diverse; kiosk queries
are extraordinarily repetitive. Forty questions, thousands of times a day. At per-token billing
that is a larger lever than every other technique combined.

**And the risk is symmetrical.** A cached answer that outlives a price change has misled a guest
at a kiosk on the venue's behalf.

## Stage C — any time

| | What changes |
|---|---|
| **Reranking, top 10–30 to 5** | **`AiProvider.capability` already carried `rerank`** — proposed here as an addition, and it was in the enum before this was written. Only `AiPolicy`'s top-K pair was new. **Reduces cost as well as improving quality**, which is unusual. **The catch is a second model with its own residency question** (ADR-0009) and its own key (CF-14) — a cross-encoder calling a US endpoint from a UAE cell is the same breach as the main model, and it would be easy to add without noticing |

---

## Declined, with reasons

**Context compression.** Reranking to five already cuts the context, and compression is **another
model call per query** — precisely the thing per-token billing makes expensive. Revisit only if
reranking proves insufficient.

**Query rewriting.** The cache handles kiosk repetition, which is where the volume is. The value
is on staff analytical queries, and it is prompt-layer work that can be added later without
rework.

## Already have, undeclared

**Metadata pre-filtering** — `scope_path` filtering is pre-filtering and it is already the design.
What is missing is the declaration that it happens *before* the vector search, which is the
difference between fast and very fast.

**Small top-K** — `limit` on `semanticSearch`.

**Local vector DB** — ADR-0020, Qdrant in-cell.

## Gated elsewhere

**Smaller embedding model** — the benchmark decides. Already open in ADR-0021's addendum.

## Implementation only

**Batch embeddings** — indexer detail, no contract surface.

---

# Independent of AI, and larger

These came out of the same assessment and have nothing to do with RAG.

| | |
|---|---|
| ✅ **Read routing — retracted** | Claimed as 63% unimplemented on 17 August. **Wrong: all 285 GETs declare routing**, and the 485 are writes, which ADR-0016 says are not declared. The error was counting operations rather than reads. **Routing is complete** |
| 🟡 **No cache tier anywhere** | Three stores, none a cache. Candidates are read on every request and change rarely: scope resolution, permission resolution (`resolvePermissions` reads five tables on every authorised call), tenant configuration, price lists. **`getOfflinePackage` is the sharpest — a bundle identical for every scanner at a venue, rebuilt per device** |
| 🟡 **Idempotency keys have no declared store** | Every write carries one as of 17 August and **nothing says where seen keys live or how long they are kept.** A key store that forgets too early lets a replay through, which is the defect the key exists to prevent |
| 🟡 **No performance targets exist** | A known blocked artefact class rather than an oversight, but **376 screens with no budget will produce some slow ones** |
| 🟡 **Wave-based code splitting available and unstated** | The manifests carry `byWave`. A Wave 1 build does not need Wave 2 and 3 routes. **`guest-app` is the case that matters** — 80 screens across two platforms, 21 in Wave 1, and it is the app a guest downloads on hotel wifi |
| 🟡 **Offline bundle size undeclared** | `venue-scanner` is offline-mandatory and its bundle is the whole gate operation. No stated size, build time or staleness limit, and F06 depends on it |

**Item one was retracted.** What remains — the cache tier, the idempotency key store, the frontend
items — is real but smaller than the AI work, and none of it is on the critical path.
