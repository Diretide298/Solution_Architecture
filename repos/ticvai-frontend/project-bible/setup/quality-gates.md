# Coding Standards — shared

**Binding across all five repositories.**
Language-specific rules: [backend-patterns](backend-patterns.md) · [frontend-patterns](frontend-patterns.md) · [data-and-storage](data-and-storage.md)

## 1. Principles

| # | Principle | Consequence |
|---|---|---|
| 1 | **Readable over clever** | The person debugging a gate outage at 2am is not you |
| 2 | **Explicit over implicit** | No hidden conventions, no magic strings, no ambient behaviour |
| 3 | **Fail loudly** | A silent failure in a multi-tenant system is a data leak waiting to be noticed |
| 4 | **Enforce in CI, not in review** | A rule a human must remember is a rule that decays |
| 5 | **Tenant scope is never optional** | Every data path proves its scope |
| 6 | **Errors are part of the design** | Recovery paths matter more than happy paths in payments and sync |

---

## 2. Universal Rules

Apply in every language.

| Rule | Reason |
|---|---|
| No secrets, credentials, connection strings or tenant IDs in source | Key vault per cell |
| No `TODO` without an issue reference — `TODO(TICV-123):` | Unreferenced TODOs are never done |
| No commented-out code | Git remembers. Delete it |
| No swallowed exceptions | `catch { }` is prohibited. Log, wrap, or rethrow |
| No magic numbers or strings | Named constant, config value, or enum |
| Public API surface documented | Doc comments on anything crossing a module boundary |
| Async all the way down | No sync-over-async. It deadlocks under load |
| Log with structure, never string concatenation | Queryable across cells |
| Every log and span carries `tenant_id`, `region_id`, `venue_id` | *"The tenant is slow"* is otherwise unactionable |
| Timeouts on every outbound call | An unbounded call is an outage waiting for a slow dependency |
| Idempotency key on every mutating operation | Offline clients replay their outbox |

---

## 8. Testing

| Layer | Scope | Gate |
|---|---|---|
| Unit | Domain logic, pure functions, money arithmetic | Every commit |
| Architecture | Module boundaries, layering | **Every commit, blocking** |
| Contract | Both directions against OpenAPI | Every commit |
| Integration | Real Postgres, real Redis, RLS enforcement | Every commit |
| Permission matrix | Every permission × every scope level | Per release |
| Offline | Network severed mid-transaction, replay, dedupe | Per release |
| Load | Tenant-aggregate with correlated venue peaks | Per release |
| Device | Simulators in CI, hardware lab nightly | Nightly |

**Every test runs against the reference fixture** — two brands, three regions across
two countries, AED and OMR. Never a single-venue simplification. A team that develops
against one venue and one currency ships code that breaks the moment a second region
appears, and finds out at UAT.

Tests assert behaviour, not implementation. Name them for what they prove:
`Refund_below_threshold_requires_second_user_authorisation`.

---

## 9. Code Review

Every change reviewed. Elevated-review areas per `AI_AUTHORSHIP.md` §5 need a second
reviewer with domain knowledge.

**Reviewer checklist:**

- [ ] Tenant scope enforced on every data path
- [ ] Permission checked at the right scope level
- [ ] Money uses `Money`, correct currency scale
- [ ] Timestamps distinguish `recorded_at` from `synced_at` where offline applies
- [ ] Errors handled; nothing swallowed
- [ ] Idempotency key on mutations
- [ ] Naming conforms to `NOMENCLATURE.md`
- [ ] Tests assert behaviour and cover failure paths
- [ ] No secrets, no PII in logs
- [ ] External API references verified against real documentation
- [ ] Comments explain *why*, citing the decision where non-obvious

---

