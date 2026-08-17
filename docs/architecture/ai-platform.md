# AI Platform Rules

> Distinct from setup/llm-conventions, which covers using AI to *write* code. This page covers building AI *features*.

### 5.3 AI service rules

| Rule | Why |
|---|---|
| No provider SDK calls in capability code | Provider swap must be configuration |
| Tenant isolation is partition-level, never filter-level | A forgotten filter is a cross-client breach; a missing collection is a loud failure |
| Read-only against the transactional core | An AI capability must not become a permission bypass |
| Every response carries trace ID, model version, token count, sources | Cost attribution and grounding audit |
| No capability ships without an eval baseline | Regression-gated in CI |

---

