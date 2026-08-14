# ticvai-ai

Python / FastAPI. Separate from the .NET core from day one — different runtime,
different scaling profile, different compliance boundary (CF-20), different
dependency lifecycle.

## Non-negotiables

| Rule | Why |
|---|---|
| Never writes to the transactional database | An AI capability must not become a permission bypass |
| Read-only, scoped by the caller's permission set | The same set the backend resolved at login |
| Tenant isolation is partition-level, never filter-level | A forgotten filter is a cross-client breach; a missing collection is a loud failure |
| No provider SDK calls in capability code | Provider swap must be config, not a rewrite |
| Every response carries trace id, model version, token count, sources | Required for cost attribution (CF-14) and for grounding audits |
| No capability ships without an eval baseline | Regression-gated in CI |

## Wave 1 is infrastructure, not features

Nothing user-facing ships in the vertical slice. Wave 1 delivers the service
skeleton, model abstraction, vector abstraction with tenant partitioning, PII
scrubbing, token accounting, guardrails, caching and the eval harness.

Capabilities (concierge, POS assistant, upsell, approval summaries, support
first-line, financial assistant) land in Wave 2+.

## Vector store

Two implementations behind one interface. Qdrant proposed 12 Aug 2026, pending
UAE residency confirmation. pgvector is the fallback and inherits the cell's
existing residency posture, backups and pooling. The decision is a config change.

## Layout

    api/           FastAPI routers, dependency wiring
    capabilities/  one module per capability; depends only on core + retrieval
    retrieval/     vector store abstraction, chunking, reranking
    guardrails/    PII scrubbing, prompt-injection defence, grounding checks
    evals/         golden sets, scoring, CI regression gate
    core/          settings, model abstraction, token accounting, tracing
