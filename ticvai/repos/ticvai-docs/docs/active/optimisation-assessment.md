# Optimisation assessment — RAG, caching, backend, frontend

**17 August 2026. Assessment only; nothing changed.**

The question was whether standard RAG techniques change what we have already written. **Four of
them do, and one of those is a correctness problem rather than an optimisation.**

---

## What the contracts know today

| | |
|---|---|
| `semanticSearch` accepts | `query`, `kinds`, `limit`. Nothing else |
| `IndexSource.chunkStrategy` | `wholeRecord`, `paragraph`, `fixedTokens`, `section` |
| Mentions of hybrid, sparse, BM25, rerank config, cache, compression, rewriting | **Zero** |
| Cache tier in the platform | **None.** Stores are `postgres`, `postgres-analytical`, `qdrant` |

So the answer to "does this change anything" is yes, because **the contracts currently assume dense
retrieval, one strategy, no reranking and no cache** — and none of that was a decision, it was a
default nobody revisited.

---

## 1. Hybrid retrieval — and the correctness problem underneath it

**This is the one that changes an ADR, and it is not really an optimisation.**

Hybrid means dense vectors plus a sparse signal, usually BM25. It is the technique most likely to
help us specifically, because **a venue's corpus is full of proper nouns a dense model handles
badly** — "Yas Waterworld", "Bronze Annual Pass", a menu item name. Dense retrieval is good at
meaning and poor at exact tokens, and half our queries are exact tokens.

**The problem is what it does to ADR-0021.** Qdrant's own documentation is explicit: with
payload-based partitioning, BM25 and IDF statistics are computed **across the entire shard**, so a
term's rarity is measured against every tenant's vocabulary rather than the tenant's own. Their
`idf` search parameter exists to correct exactly this.

**We chose shard-per-tenant, which mostly handles it** — the statistics are per shard and a shard
is a tenant. **But inside a dedicated cell the shard is the whole tenant and venues share it**, so
a term common at one venue and rare at another gets one IDF for both.

**Not fatal, and not something to discover during a demo.** The fix is a search parameter, and it
needs to be in the contract rather than left to whoever writes the retrieval client.

| | |
|---|---|
| **Changes** | ADR-0021 — a consequence paragraph and the `idf` scoping rule |
| **Changes** | `KnowledgeCollection` — sparse vector configuration is a collection-creation decision, and **a collection created dense-only cannot gain a sparse index without a rebuild** |
| **Changes** | `semanticSearch` — a mode, or a default |
| **Cost** | Low. Sparse indexes are cheap and Qdrant computes them in the same call |
| **Urgency** | **Before the first collection is created**, because retrofitting is a reindex |

---

## 2. Caching — three different caches, and we have none of them

The question asked specifically about not sending the same query to the LLM repeatedly. **There
are three distinct caches and they have different economics, different invalidation and different
owners.**

### 2a. Embedding cache — pure win, no quality cost

Same text, same model, same vector. A product description that has not changed does not need
re-embedding, and **`reindexSource` currently re-embeds a whole source.**

Keyed on a content hash plus the model identifier. **Invalidation is trivial** — the key changes
when the content does.

**Where it matters most:** a tenant with 20,000 chunks who edits fifty of them. Today that is
20,000 embeddings; with a cache it is fifty.

| | |
|---|---|
| **Changes** | `ai.index_entry` gains a content hash. A cache store appears in the schema |
| **Cost** | Low to build, **high savings on reindex** |
| **Quality** | None |

### 2b. Query result cache — the big one, and the guest concierge makes it bigger

**Staff queries are diverse. Guest queries at a kiosk are extraordinarily repetitive** — where are
the toilets, what time do you close, is the water slide open, where do I collect my tickets.

A kiosk in an entrance hall will serve the same forty questions thousands of times a day. **At
per-token billing (CF-14) that is the single largest cost lever available**, and it is larger than
every other technique on the list combined.

**Invalidation is the hard part and we already have the mechanism.** Nine events invalidate the
RAG index; the same events invalidate a cached answer. **A cached answer that outlives a price
change is worse than a slow one** — a guest told an old price at a kiosk has been misled by the
venue.

**Scope is part of the key.** The same question at two venues has two answers, so the key must
carry `scope_path` — and a cache keyed on the question alone is a cross-venue data leak wearing a
performance hat.

| | |
|---|---|
| **Changes** | A cache store. `AiPolicy` gains a TTL and an enable flag. The invalidating events gain a cache consumer |
| **Cost** | Medium to build, **very high savings** |
| **Quality** | None where invalidation is right, **severe where it is wrong** |
| **Note** | This changes CF-14's cap economics materially. Worth modelling before setting the cap |

### 2c. Provider prompt caching — cheapest to adopt

Anthropic and others cache a stable prompt prefix, charging less for the cached portion. **Our
system prompt plus the retrieved context is most of every request**, and the system prompt is
identical across a tenant's traffic.

**Adopting it is mostly a matter of ordering the prompt so the stable part comes first**, which is
a prompt-construction decision, not an architecture one — but it needs stating, because a prompt
assembled in the wrong order silently loses the discount.

| | |
|---|---|
| **Changes** | Nothing structural. A note in `ai-platform.md` and a constraint on prompt assembly |
| **Cost** | Very low to adopt, **material savings** |

---

## 3. Reranking

`AiPolicy` mentions rerank once and nothing configures it.

**Retrieve 30, rerank to 5, send 5.** The retrieval is cheap; the tokens sent to the model are not.
So reranking usually **reduces** cost as well as improving quality, which makes it unusual on this
list.

**The catch for us is a second model.** A reranker is its own model with its own residency
question (ADR-0009) and its own key (CF-14's per-tenant tokens). **A cross-encoder reranker calling
a US endpoint from a UAE cell is the same residency breach as the main model**, and it would be
easy to add without noticing because it feels like infrastructure.

| | |
|---|---|
| **Changes** | **`AiProvider.capability` already had `rerank`** — this document proposed adding it, and an external audit found it was in the enum before the assessment was written. `AiPolicy` needs the top-K pair |
| **Cost** | Medium |
| **Quality** | Improves |

---

## 4. Chunking — semantic and parent-child

`chunkStrategy` has four values and **neither of the two techniques that most help a corpus like
ours.**

**Parent-child** is the one to look at. Retrieve on a small precise chunk, send the parent section
for context. **A venue's refund policy is a paragraph that only makes sense inside its section**,
and a retrieved paragraph without its heading answers the wrong question confidently.

**Semantic chunking** splits on meaning rather than length, which matters for policies and FAQs
where a fixed-token split cuts a rule in half.

| | |
|---|---|
| **Changes** | `IndexSource.chunkStrategy` gains values. `ai.index_entry` gains a parent reference |
| **Cost** | Low |
| **Quality** | Often improves, and **parent-child specifically fixes a failure mode we will otherwise hit** |
| **Urgency** | Before indexing, since it changes what is stored |

---

## 5. Metadata pre-filtering — already have it, not declared

`scope_path` filtering is pre-filtering and it is already the design. **What is missing is the
declaration that it happens before the vector search rather than after**, which is the difference
between fast and very fast, and between correct and nearly correct.

Qdrant's filterable HNSW does this natively. **No change beyond writing it down.**

---

## 6. Smaller models

Two independent choices we have collapsed into one:

**A smaller embedding model** — decided by the benchmark in ADR-0021's addendum. Already gated.

**A smaller synthesis model** — never discussed. A kiosk answering "what time do you close" from
retrieved context does not need the largest model available. **`AiProvider.capability` already
allows different providers per capability**, so the contract supports it and nobody has decided
it.

**This interacts with the guest cap.** A cheaper model for guest traffic and a stronger one for
staff analysis is the obvious shape, and it is a configuration we can already express.

---

## What does not change anything

**Batch embeddings** — implementation detail of the indexer.
**Local vector DB** — already decided; Qdrant is in-cell (ADR-0020).
**Small top-K** — a parameter, already present as `limit`.
**Query rewriting** — prompt engineering, no contract surface.

---

# Backend, beyond RAG

## Read routing — **retracted, 17 August. There was no gap.**

This section claimed 485 of 773 operations declared no read routing and called it the largest
finding in the assessment. **It was wrong, and the error was mine: I counted operations rather
than reads.**

**All 285 GETs declare routing.** The 485 are writes, and ADR-0016 says plainly: *"All writes go
to the primary. That is not a routing decision and is not declared."* Three POSTs also declare it
— `semanticSearch`, `evaluateApprovalRequirement` and `settleAiUsage` — which are computations
that read, and declaring it there is correct.

**Routing is 100% complete.** The lesson is the one already in `principles.md`: a percentage over
the wrong denominator reads as a defect and is not one.

## There is no cache tier at all

Three stores: `postgres`, `postgres-analytical`, `qdrant`. **No Redis, no in-process cache, nothing
between a request and the database.**

The obvious candidates are the ones read on every request and changed rarely:
**scope resolution and permission resolution** (`resolvePermissions` reads five tables and runs on
every authorised call), **tenant configuration**, **price lists**, **the offline bundle**.

`getOfflinePackage` is the sharpest: **a bundle identical for every scanner at a venue, rebuilt per
device.**

## Idempotency keys have no declared store

Every write now carries one (fixed today) and **nothing says where the record of seen keys lives or
how long it is kept.** That is a cache-shaped problem with a correctness consequence — a key store
that forgets too early lets a replay through.

---

# Frontend

## No performance targets exist anywhere

This is a known blocked artefact class rather than an oversight — **"performance/SLA (no targets)"**
has been on the blocked list since the audit. But it means **no screen has a budget**, and 376
screens with no budget will produce some slow ones.

## Wave-based code splitting is available and unstated

The manifests carry `byWave` per app. **A Wave 1 build does not need Wave 2 and 3 routes**, and the
split is already described in data — nobody has said it should drive the bundle.

`guest-app` is the case that matters: **80 screens across two platforms**, of which 21 are Wave 1,
and it is the app a guest downloads on hotel wifi.

## Offline bundle size is undeclared

`venue-scanner` is offline-mandatory and its bundle is the whole gate operation. **No stated size,
no stated build time, no stated staleness limit.** F06 depends on it and the flow does not say how
big it is.

## Three apps serve two platforms each

`guest-app` runs P02 and P05; `venue-management-web` runs P08 and P13. **A kiosk build does not need
the guest app's account screens**, and nothing says the shells differ.

---

# Recommended order

**Before anything is indexed** — these change stored data and cost a rebuild afterwards:

1. Sparse vector configuration on the collection, and the `idf` scoping rule (hybrid + ADR-0021)
2. Parent-child and semantic chunk strategies
3. Content hash on index entries, for the embedding cache

**Before the guest concierge ships** — these change CF-14's economics:

4. Query result cache with event-driven invalidation
5. Provider prompt caching, via prompt assembly order
6. A separate, cheaper provider for guest synthesis

**Independent of AI, and larger than all of the above:**

7. ~~Read routing on 485 operations~~ — **retracted, there was no gap**
8. A cache tier for scope, permission and configuration resolution
9. A declared store and retention for idempotency keys

**Item 7 was retracted on 17 August.** Routing is complete; the claim counted operations rather
than reads. What remains of the independent work is items 8 and 9.
