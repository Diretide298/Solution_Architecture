# AI Platform Rules

> Distinct from setup/llm-conventions, which covers using AI to *write* code. This page covers building AI *features*.

### 5.3 AI service rules

| Rule | Why |
|---|---|
| No provider SDK calls in capability code | Provider swap must be configuration |
| **Tenant isolation is the cell where a cell holds one tenant, and a dedicated Qdrant shard where it does not** | **Corrected twice on 17 August.** The original rule — never filter-level — was right about shared placement for the wrong stated reason. The first correction dismissed it on ADR-0001 (retired — see ADR-0014 and ADR-0017)'s *Cell = Tenant × Jurisdiction*, **without checking ADR-0017, where shared placement puts every tenant in one installation behind RLS**. Postgres enforces RLS; **Qdrant enforces nothing**, so on shared placement the boundary must be a shard. See ADR-0021 |
| Read-only against the transactional core | An AI capability must not become a permission bypass |
| Every response carries trace ID, model version, token count, sources | Cost attribution and grounding audit |
| No capability ships without an eval baseline | Regression-gated in CI |

---

---

## Prompt assembly order

**Providers cache a stable prefix and charge less for it. A prompt assembled in the wrong order
silently loses that**, with no error and no signal other than a bill that is larger than it should
be.

The order is fixed, most stable first:

    1. system prompt          identical for every request in a capability
    2. tenant instructions    changes when a tenant edits its assistant configuration
    3. retrieved context      changes per question
    4. conversation history   changes per turn
    5. the question           changes always

**Anything that varies per request must not appear above something that does not.** A trace ID or
a timestamp in the system prompt invalidates the whole cached prefix for every request that
follows, which is the failure worth naming because it looks harmless.

**This is not an optimisation with a quality trade.** The output is identical; only the price
differs.

---

## One provider per capability, and the guest case

`AiProvider.capability` already allows a different provider per capability, and **the obvious
split has not been made: a cheaper model for guest synthesis, a stronger one for staff analysis.**

A kiosk answering *what time do you close* from retrieved context does not need the largest model
available. A manager asking why last Tuesday's revenue was down does.

**This matters more since 17 August**, when guest AI became a Phase 1 commitment charged per token
(CF-14). Guest volume is bounded by footfall and staff volume by headcount, so **the cheaper model
serves the traffic the venue cannot control.**

**Nothing needs building** — the contract expresses it. What is missing is the decision and a
default in the provider seed.

---

## Reranking crosses the same borders as the model

A reranker is **its own model, with its own residency question and its own key.**

`AiCapability` already carries `rerank`, so a rerank provider is configured, scoped and credentialled
exactly like a chat provider. **A cross-encoder calling a US endpoint from a UAE cell is the same
breach as the main model calling one** — and it would be easy to add without noticing, because a
reranker feels like infrastructure rather than a model.

`AiPolicy.retrieveTopK` and `rerankTopK` control it. **Null `rerankTopK` disables reranking**, and a
venue with no rerank provider configured runs without it rather than failing — the same posture as
the assistant itself under CF-61.
