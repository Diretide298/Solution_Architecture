# AI Runtime

Python 3.12 / FastAPI. Separate from the .NET core by design — different runtime, scaling
profile, compliance boundary and dependency lifecycle.

## Non-negotiables

| Rule | Why |
|---|---|
| **Never writes to the transactional database.** Read-only, scoped by the caller's resolved permission set | An AI capability must not become a permission bypass |
| **Tenant isolation is partition-level, never filter-level** | A forgotten filter is a cross-client breach; a missing collection is a loud failure |
| **All AI data stays in-jurisdiction** — vector stores, prompt logs, indices | Residency |
| **No provider SDK calls in capability code** | Provider swap must be configuration |
| Every response carries trace ID, model version, token count, retrieval sources | Cost attribution and grounding audit |
| **No capability ships without an eval baseline**, regression-gated in CI | Hallucination in a pricing path is a financial defect |
| Anything affecting price, refund, entitlement or financial state is **recommendation-only** until a human approves | AI-62 |
| PII scrubbed on ingress and egress, audited | 10 Aug 2026 |

## Phase 1 scope — 15 of 67 applications

Everything else needs operating history that does not exist before launch.

| Group | IDs |
|---|---|
| Conversational | AI-01 to AI-08. **AI-01 is the substrate** — the rest are configurations |
| Reporting | AI-57 natural-language reporting. **AI-58 forecasting is excluded** |
| Governance | AI-61 to AI-66. **Preconditions, not features.** Nothing ships before them |

Full rationale: `ticvai-docs/plan/ai-phasing.md`.

## Vector store

Two implementations behind one interface — Qdrant and `pgvector`. The residency decision
is a config change, not a rewrite.

Isolation is by **separate collection per tenant**: `t_{tenant_hex}__{namespace}`. There is
no shared collection to accidentally span.

## Tooling

Ruff (`E,F,I,N,UP,B,A,C4,PT,SIM,ARG,PL,RUF,ASYNC,S`) and mypy `strict`, both blocking.
Type hints everywhere · `async def` throughout · `@dataclass(frozen=True, slots=True)` for
value objects · Pydantic at the boundary only · structlog, never f-string log messages.
