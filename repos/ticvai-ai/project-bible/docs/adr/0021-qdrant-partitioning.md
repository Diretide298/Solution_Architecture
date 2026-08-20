# ADR-0021 — Qdrant: one collection per embedding model, tenant is the shard, scope is the filter

**Status:** Proposed · 17 August 2026
**Supersedes:** the "tenant isolation is partition-level, never filter-level" rule as it applied to Qdrant
**Relates to:** ADR-0001 (cells — **superseded in part by ADR-0014**), ADR-0014 (cell per region),
ADR-0017 (placement), ADR-0020 (AI isolation), CF-97

---

## Decision

Three rules, and none of them is conditional on anything.

**One collection per embedding model.** Not per tenant, not per purpose, not per venue — because
**a collection is the only container that can hold a different vector configuration, and a shard
cannot.** A tenant forced onto a local model by residency therefore gets its own collection; every
other tenant shares.

**Tenant is the shard key. Always.** One shard per tenant, on every placement.

**Scope is an indexed payload filter the caller cannot supply** — `scope_path`, sourced from the
resolved session.

    qdrant
      └── knowledge                     one collection
            ├── shard: tenant_a         ← the isolation boundary
            ├── shard: tenant_b
            └── shard: tenant_c
                  payload: scope_path, source, entity_id, locale, content_kind, updated_at

---

## Why uniform, rather than following placement

This took two corrections to get right, and the correction matters more than the original.

**Placement is not a property of the platform. It is a property of a tenant, and it changes.** A
tenant starts on `shared`, grows, and moves to `dedicated`. ADR-0017 makes that a normal
commercial event rather than a re-architecture.

**A Qdrant shape that follows placement changes shape when a tenant upgrades.** That turns a
billing change into a data migration, and it puts a conditional in the retrieval client that
every future query has to be right about.

**Shard-per-tenant costs nothing on dedicated placement** — a single-tenant cell has one shard,
which is what an unsharded collection is anyway. And **a tenant moving from shared to dedicated
moves a shard**, which is a Qdrant primitive rather than an export and reimport.

So the uniform rule is free on the placement where it does nothing, and correct on the placement
where it matters.

---

## What decides a collection, and it is not the tenant

**A collection is Qdrant's only top-level container — there is no database above it — and each one
carries its own vector configuration, indexing parameters and sharding configuration.** A shard
does not: **shards inherit the collection's vector config.**

That single fact decides the whole question. **Vectors from two different embedding models are
not comparable**, so they cannot share a collection — and they cannot be separated by a shard
either, because a shard cannot have a different vector size or distance metric.

**So the split criterion is the embedding model, and nothing else.** Qdrant says so directly:
*create multiple collections only when your data is not homogenous, or when users' vectors are
created by different embedding models.*

### What this means for us, concretely

**Collection count equals the number of distinct embedding models in an installation.** That is
one, or two if catalogue and knowledge diverge — not one per tenant.

**But it is not always one.** ADR-0009 and ADR-0020 mean **a tenant in a region with no adequacy
finding, or on-premise, gets a locally hosted model.** Its vectors are a different size in a
different space, so **that tenant has its own collection whether we like it or not.** That is
forced by the model, not chosen for isolation — and it is the case where the naive
collection-per-tenant answer happens to be right for a reason nobody stated.

### And the shard is Qdrant's own second tier

This is not a workaround. Qdrant describes exactly this shape: **collection-based isolation is
the entry level, and a scaled setup moves to payload-based isolation plus resource-based
isolation from sharding — one collection, queried on both `group_id` and `shard_key_selector`,
giving two additional levels of isolation.**

**Yes, a server can hold thousands of collections.** It is also the thing their scaling guidance
tells you not to do, citing a deployment that hit the 1000-collection limit after a year and had
to migrate. **The capability is real and the advice against using it that way is theirs, not
mine.**

---

## Why not the two obvious alternatives

### Collection per tenant

The original design, and it was wrong twice.

**The vendor documents it as a failure mode.** Qdrant's guidance is a single collection per
embedding model with payload-based partitioning for tenants and use cases. Their scaling material
is blunter: do not create one collection per tenant, because it does not scale past a few hundred
and wastes resources — one company hit the 1000-collection limit after a year and had to migrate.

**And it described an isolation we never had.** A tenant has venues; a steward at one venue must
not retrieve another venue's document. **So every query filters by `scope_path` regardless** — we
had partition-by-tenant *and* filter-by-scope, and called it partition-only.

### Payload filter alone, no shard

The correction made first, reasoning from ADR-0001 (retired — see ADR-0014 and ADR-0017)'s *Cell = Tenant × Jurisdiction*: a cell holds
one tenant, so `tenant_id` names nothing.

**True for dedicated placement, false for the default.** ADR-0017: *"Shared — the default. One
TICVAI installation in the UAE serves every tenant that does not need otherwise. Isolation is
`FORCE` row-level security on a scope path, and nothing else."*

**And ADR-0001 had already said so itself.** Eight lines below the sentence I quoted it points at
ADR-0014 as the operative model, and ADR-0014 states plainly that *"a cell holds exactly one
tenant is no longer true"*. **The ADRs do not contradict each other — I followed the wrong one and
did not follow its own pointer.**

**Postgres enforces RLS. Qdrant enforces nothing.** On shared Postgres a careless join returns no
rows because the database stops you. On shared Qdrant a query missing its filter returns every
tenant's vectors, and **nothing in the database will stop it.**

That is the entire argument for a shard: **it is the only boundary in Qdrant that does not depend
on a query being written correctly.**

---

## The threshold that would change this

**Shard-per-tenant works because our tenant count is low.** Qdrant's own framing is that
shard-based multitenancy suits a smaller number of larger tenants, and payload-based suits a large
number of small ones.

We are Miral-class operators in the UAE and Oman — **tens of tenants, not thousands** — and every
one is large enough to justify a shard.

**If a shared installation passes roughly one hundred tenants this must be revisited**, and the
answer then is tiered multitenancy: a shared fallback shard for small tenants, dedicated shards
for large ones, within the same collection. Qdrant supports it natively and the migration is a
promotion rather than a rebuild.

**Nobody has stated the expected tenant count.** It is not in ADR-0001 or ADR-0017, and it is the
single number that decides whether this ADR holds. Raised with CF-97.

---

## What still has to be true in the code

**Sharding routes. It does not authorise.**

A query is directed to a shard by `tenant_id` and filtered within it by `scope_path`, and **both
come from the resolved session, never from a caller parameter.**

**This must be enforced by a single retrieval client that has no parameter for scope.** Not a
convention, not a review checklist — a function that takes a session and a question and offers no
way to ask about somebody else's data.

The difference between this and Postgres RLS is exactly that Postgres does not need anyone to
remember. Since Qdrant does, **the remembering happens in one place rather than in every query.**

---

## Consequences

**One collection, created at cell provisioning.** Not created on demand per tenant, which removes
a class of race and a class of orphan.

**A tenant's data can be moved, exported or dropped as a shard.** Offboarding or a contract ending
is a shard drop rather than a filtered delete across a shared index — which matters for CF-64 and
for PDPL.

**`reindexSource` has a larger blast radius on shared placement.** A shadow-swap now affects a
shard rather than a purpose-specific collection. The atomic swap in `states/ai-index-job.yaml` is
what keeps that safe.

**`removeIndexEntry` must filter on `entity_id` and `scope_path` within the tenant's shard.**
Deleting by `entity_id` alone was safe when a collection held one tenant. It is not now, and
erasure runs through this path.

**Residency is unchanged.** The cell places the data and Qdrant sits inside it — the part of the
original design that was always right.

**Hybrid retrieval needs a scoped IDF, and this is where that bites.** Qdrant computes BM25 and
IDF statistics **shard-wide**, so a term's rarity is measured against everything in the shard.
Shard-per-tenant handles the cross-tenant case — a term common at one tenant does not distort
another's scores. **Inside a dedicated cell the shard is the whole tenant and its venues share
it**, so a term common at one venue and rare at another gets one score for both.

`KnowledgeCollection.idfScope` defaults to `tenant` and narrows to `venue` where a tenant's venues
differ enough for it to matter — a theme park and a museum under one operator, where "queue" means
something at one and nothing at the other.

**This is a decision, not a default to leave alone.** A sparse index scoring against the wrong
population retrieves confidently and wrongly, which is the failure mode hardest to notice.

---

## Open

**The embedding model**, which decides how many collections exist. Two if catalogue and knowledge
diverge; **one more for every tenant that residency forces onto a local model** (ADR-0009,
ADR-0020, CF-61). Nobody has said whether any tenant is in that position — it is a residency
question with a storage consequence.

**The tenant-count assumption**, above.

**Whether shared remains the default placement**, given it is the only model where a missing filter
is a cross-client breach rather than a cross-venue one. That is CF-97, and it is not an AI
question.

---

# Addendum — the embedding model

**17 August 2026.** The ADR above left one question open: one collection or two, which is decided
by whether catalogue and knowledge content use the same embedding model.

## The answer is one model, multilingual

**One collection, one multilingual model, no translation anywhere.** An Arabic query matches
Arabic content and English content; an English query does the same in reverse.

Candidates, all of which cover every language a UAE venue plausibly needs: **BGE-M3**
(open, 100+ languages), **Cohere embed-v4** (hosted, 256 languages), **Gemini Embedding 2**
(hosted, strongest reported cross-lingual retrieval), **Swan-Large** (open, Arabic-centric,
outperforms Multilingual-E5-large on most Arabic tasks).

## Why not translate to English and keep one index

This was proposed as the cheaper option and the instinct is right about one index being cheaper
than two. **It inverts where the cost sits.**

**Embedding is a one-off cost per document. Translation at query time is a cost per query,
forever.**

| | Calls, year one | Growth |
|---|---|---|
| Embed ~20,000 chunks | **20,000** | Only on change |
| Translate query in and answer out | **~350,000** | Every year, rising |

At fifty staff asking ten questions a day, translate-at-query is roughly **seventeen times the
calls in year one** and the gap widens with usage. It also adds two model round trips before
the answer starts — noticeable at a desk, decisive at a kiosk.

**And the decisive argument is in our own package.** `CMS-011 Translations` exists: *"Fill in
what every language is missing."* Eight of the eleven RAG sources are tenant-authored content,
**so the Arabic already exists and the tenant chose those words.** Translating from English
would duplicate work they have done and answer guests in an approximation of their own
terminology — a venue that calls a wristband سوار in their CMS should not get a translator's
alternative back from the assistant.

Translating at **index** time rather than query time is the good version of the idea, and it is
the right pattern for a corpus that is genuinely English-only with occasional other-language
documents. Ours is not that corpus.

## Adding languages later is free; changing the model is not

**Adding a language:** the tenant publishes content in it, the indexer embeds it, done. No
reindex of what exists, no schema change, no new collection. **This matters for a UAE venue
specifically** — the visitor mix is not English and Arabic, it is English, Arabic, Hindi, Urdu,
Russian, Chinese and Tagalog, and which of those matter will change with the market.

**Changing the model:** every chunk re-embedded and the collection rebuilt, because vectors from
different models are not comparable. `states/ai-index-job.yaml` has the shadow-collection swap
that makes this survivable rather than catastrophic, but it is a full pass per tenant.

**So the decision is not which languages to support. It is picking a model whose coverage we
will not outgrow** — and all four candidates clear that bar, which makes this less risky than it
sounds.

## The evaluation, in two stages

### Stage 1 — public benchmarks. Runnable now, no client content

| | |
|---|---|
| **Dialectal ArabicMTEB** | **The closest fit.** Nineteen datasets, of which five are retrieval covering Gulf dialects. Content is authored in Modern Standard Arabic; a guest types Gulf colloquial, and this is the only public suite that measures that gap |
| **ArabicMTEB** | 94 datasets, eight tasks. Its **Cross-lingual Retrieval** task is the Arabic-query-against-English-document case we will hit constantly |
| **MIRACL** | Multilingual retrieval across 18 languages — the reference for languages we may add later |

**One result complicates the choice and is worth stating.** Swan-Large wins on Arabic tasks and
is Arabic-centric, built on an Arabic LLM. **A model that wins ArabicMTEB may be the wrong
choice for a corpus that is half English**, and no public benchmark measures "one index, both
directions, equally well," which is exactly our requirement.

### Stage 2 — 30 to 50 real queries against real venue content

**This is the stage that decides**, and it blocks on a tenant's corpus existing.

Public benchmarks test news and encyclopaedia text. **Nothing in them resembles a wristband
policy, an allergen list or a refund window.** And none covers **code-mixing** — an Arabic query
containing "Yas Waterworld" and "annual pass" in English, which is not an edge case here but the
normal case.

## Sequencing

**Stage 1 can run this week. Stage 2 blocks on the first tenant's content.**

Choosing before stage 2 risks a rebuild. **Committing to the architecture does not** — one
collection per embedding model per cell holds whichever model wins, and the model choice is a
configuration value in `ai.provider`.

## Can this be automated

Partly, and the boundary is worth knowing before someone starts.

**What works:** `mteb` installs cleanly from PyPI — version 2.19.3 was verified on 17 August. It
carries a task registry, an evaluation loop and result serialisation, and hosted models
(Cohere, Gemini) need only an API key and a small budget.

**What needs checking first, not assuming:** **ArabicMTEB does not appear to ship inside the
`mteb` package.** Inspecting the 2.19.3 wheel found Arabic classification, sentiment and
reranking tasks but not the ArabicMTEB retrieval suite. The paper states the benchmark is
publicly released, so it is likely a separate dataset release to load as custom tasks — **the
first job is to confirm where it lives, not to write the harness.**

**What needs real hardware:** BGE-M3 runs on CPU for a benchmark subset and wants a GPU for the
full suite. **Swan-Large is built on a 7B-class Arabic LLM and needs a GPU**, so if it is on the
shortlist the environment has to allow for that.

**A realistic shape for the run:** confirm ArabicMTEB availability, register it as custom tasks,
evaluate the four candidates on retrieval and cross-lingual retrieval plus the Gulf dialectal
retrieval sets, and produce one table of nDCG@10 by model by task. **A day of work, and it
eliminates any candidate that fails on Gulf Arabic before a line of platform code depends on
it.**

## Status of the benchmark run

**A prompt for Claude Code was written on 17 August** covering stage 1: four candidates against
the ArabicMTEB retrieval and cross-lingual tasks, the Gulf dialectal retrieval sets, MIRACL
Arabic, and one standard English retrieval task.

**The English column is not optional and is the point of the exercise.** Swan-Large is
Arabic-centric and reportedly wins on Arabic; a model that wins ArabicMTEB may be the wrong shape
for an index that is half English, and no public benchmark measures both directions at once.

Two things the prompt is explicit about, because assuming either would waste the run:

**Confirm where ArabicMTEB actually lives before writing a harness.** Inspecting the `mteb`
2.19.3 wheel on 17 August found Arabic classification, sentiment and reranking tasks but **not
the ArabicMTEB retrieval suite**. The paper states the benchmark is publicly released, so it is
likely a separate dataset release to register as custom tasks — but that is the first job, not
an assumption.

**Swan-Large needs a GPU**, being built on a 7B-class Arabic model. If the environment cannot
run it, it should be dropped and said so rather than silently substituted with a smaller variant.

## What is decided and what is not

| | |
|---|---|
| **Decided** | One collection per embedding model, per cell. `scope_path` as an indexed payload the caller cannot supply. No translation at query time |
| **Decided** | Adding languages later requires no reindex; changing the model requires a full rebuild through the shadow-swap in `states/ai-index-job.yaml` |
| **Not decided** | Which model. Gated on stage 1, then stage 2 against real tenant content |
| **Not decided** | One collection or two — follows from whether catalogue and knowledge share an embedding model, which follows from the above |

**The architecture does not wait on the model.** One collection per embedding model per cell
holds whichever model wins, and the choice is a configuration value in `ai.provider`.

---

# History

**This ADR was rewritten once and corrected twice on 17 August**, and the sequence is worth keeping
because each error was visible without new information.

**First shape: collection per tenant.** Justified by a rule that tenant isolation must never be
filter-level. Wrong against the vendor's documented limit, and wrong about our own design — we
filtered by `scope_path` inside the collection anyway.

**Second shape: payload filter alone, no shard.** Justified by ADR-0001's *Cell = Tenant ×
Jurisdiction*. **Wrong because ADR-0017 says the default placement puts every tenant in one
installation behind RLS**, and the second ADR was not checked before building on the first.

**Third and current: uniform shard-per-tenant.** The correction that mattered was not adding the
shard back — it was noticing that **a shape conditional on placement breaks when a tenant changes
placement**, which they are expected to do.

**The underlying defect is not a contradiction between ADRs.** ADR-0014 had already corrected
ADR-0001 and ADR-0001 points at it. The defect is that ADR-0001 is still titled *one tenant per
jurisdiction*, still reads as operative for eighty-five lines, and has now produced two errors —
this one, and `platform.tenant` written with no RLS on the same ground. **That is CF-97.**
