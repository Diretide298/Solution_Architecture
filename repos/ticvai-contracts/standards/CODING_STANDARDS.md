# TICVAI — Coding Standards

**Version:** 1.0
**Scope:** All five repositories. Binding.
**Companion:** `NOMENCLATURE.md`, `API_DESIGN.md`, `AI_AUTHORSHIP.md`

---

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

## 3. C# / .NET 8

### 3.1 Enforced at compile time

`Directory.Build.props` sets `TreatWarningsAsErrors`, `Nullable=enable`,
`EnforceCodeStyleInBuild`, and wires `BannedApiAnalyzers`.

| Banned | Use instead | Why |
|---|---|---|
| `System.DateTime` | `DateTimeOffset` | Venues span time zones within one tenant |
| `DateTime.Now` / `.Today` | `DateTimeOffset.UtcNow` | Server-local time is meaningless |
| `decimal` for money | `Money` | Raw decimal loses the per-region currency scale |
| `Guid.NewGuid()` for entity IDs | `UlidGenerator.NewUlid()` | Offline generation; index locality |

### 3.2 Structure

- **Module boundaries are enforced by `Ticvai.ArchitectureTests`, not by convention.**
  A module referencing another module's internals fails the build.
- `Ticvai.Shared.Kernel` holds primitives only. Domain logic there means the boundaries
  are gone.
- Domain layer is persistence-ignorant — no EF, Npgsql, Redis or ASP.NET references.
- API layer returns contract DTOs, never domain entities.

### 3.3 Style

```csharp
// File-scoped namespaces. Primary constructors where they read well.
namespace Ticvai.Modules.Orders.Application;

public sealed class RefundAuthoriser(
    IOrderRepository orders,
    IPermissionEvaluator permissions,
    ILogger<RefundAuthoriser> logger)
{
    // Expected failures return Result<T>. Exceptions are for the unexpected.
    public async Task<Result<RefundAuthorisation>> AuthoriseAsync(
        RefundRequest request,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(request);

        // Guard clauses first, happy path unindented.
        if (request.Amount.IsNegative)
        {
            return Result<RefundAuthorisation>.Failure(
                Error.Validation("amount", "Refund amount must be positive."));
        }

        // ...
    }
}
```

| Rule | Detail |
|---|---|
| `sealed` by default | Unseal deliberately |
| `readonly record struct` for value objects | `Money`, `ScopeNode` |
| `Result<T>` for expected failures | Exceptions for the genuinely unexpected |
| `CancellationToken` on every async method | Threaded through, never ignored |
| `.ConfigureAwait(false)` in library code | Not in the API layer |
| Constructor injection only | No service locator, no static access to DI |
| One public type per file | File named for the type |

### 3.4 Data access

- Every query runs with `ticvai.scope_paths` set. RLS is defence in depth, not the only line.
- Parameterised always. String-concatenated SQL is a build-blocking review finding.
- Explicit transaction boundaries. Order + payment + entitlement + ledger is **one**
  transaction.
- No lazy loading. Fetch what you need.

---

## 4. TypeScript / React / React Native

### 4.1 Compiler

`tsconfig.base.json` sets `strict`, `noUncheckedIndexedAccess`,
`exactOptionalPropertyTypes`, `noImplicitOverride`, `verbatimModuleSyntax`.

`any` is prohibited. Use `unknown` and narrow.

### 4.2 Enforced boundaries

ESLint `@nx/enforce-module-boundaries` blocks:

| Blocked | Why |
|---|---|
| Apps importing a SQLite driver directly | Everything goes through `offline-core`. Six sync engines is six divergent bug surfaces |
| Packages importing apps | Dependencies point one way |
| Local permission computation | Clients consume `effectivePermissions`. Client-side authz is a security hole and a divergence source |
| `localStorage` / `sessionStorage` in artefacts | Unsupported in the target runtime |

### 4.3 Style

```typescript
// Named exports. Default exports only where a framework demands one.
export function useShiftState(workstationId: string): ShiftState {
  // Hooks at the top, unconditional.
  const [state, setState] = useState<ShiftState>(initialShiftState);

  // Effects declare their dependencies honestly. No lying to the linter.
  useEffect(() => {
    // ...
  }, [workstationId]);

  return state;
}
```

| Rule | Detail |
|---|---|
| Function components, hooks only | No class components |
| Props typed with an interface, never inline | Reusable, documentable |
| No `React.FC` | Poor generics and children inference |
| Discriminated unions over optional-field soup | `{ status: 'offline' } \| { status: 'syncing'; pending: number }` |
| Errors surface to the user | A swallowed sync failure behind "all synced" is worse than an error |
| No business logic in components | Hooks and packages |

### 4.4 Offline

- Every mutating call goes through the `offline-core` outbox. No direct fetch on a write path.
- Conflict policy is declared per entity at the call site. There is no global default.
- The offline indicator reflects real transport state, never an optimistic guess.

---

## 5. Python / FastAPI

### 5.1 Tooling

Ruff (line length 100, `E,F,I,N,UP,B,A,C4,PT,SIM,ARG,PL,RUF,ASYNC,S`) and mypy `strict`.
Both blocking in CI.

### 5.2 Style

```python
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class TenantScope:
    """Isolation boundary for every operation.

    ``jurisdiction`` is carried because a cell never spans jurisdictions and
    the vector store must not either.
    """

    tenant_id: UUID
    jurisdiction: str
```

| Rule | Detail |
|---|---|
| Type hints everywhere | mypy strict; no untyped defs |
| `async def` throughout | No blocking IO in an async path |
| `@dataclass(frozen=True, slots=True)` for value objects | Immutable, cheap |
| Pydantic at the boundary only | Not as an internal domain model |
| Structured logging via `structlog` | Never f-string log messages |
| Explicit exception types | Never bare `except:` |

### 5.3 AI service rules

| Rule | Why |
|---|---|
| No provider SDK calls in capability code | Provider swap must be configuration |
| Tenant isolation is partition-level, never filter-level | A forgotten filter is a cross-client breach; a missing collection is a loud failure |
| Read-only against the transactional core | An AI capability must not become a permission bypass |
| Every response carries trace ID, model version, token count, sources | Cost attribution and grounding audit |
| No capability ships without an eval baseline | Regression-gated in CI |

---

## 6. SQL & Migrations

| Rule | Detail |
|---|---|
| Forward-only, numbered, checksummed | `V0001__baseline.sql` |
| Every migration is reversible or documented as irreversible | Runs across every cell |
| **Test rollback before merge** | Not after |
| No `SELECT *` | Explicit columns |
| Every foreign key indexed | — |
| `ENABLE` **and** `FORCE ROW LEVEL SECURITY` | Without FORCE the owner bypasses every policy |
| Partition key in the primary key | Required on partitioned tables |
| Comment the non-obvious | `COMMENT ON COLUMN` for anything a newcomer would misread |

Long-running DDL uses `CONCURRENTLY` where available. A migration holding a lock on
`sales_order` during trading is an outage across every venue in the cell.

---

## 7. Terraform

| Rule | Detail |
|---|---|
| Modules parameterised, never copy-pasted per cell | One `cell` module, N tfvars |
| `prevent_destroy` on databases and key vaults | — |
| No inline secrets | Key vault references |
| Variables carry `description` and `validation` | Validation catches jurisdiction typos at plan time |
| `terraform fmt` and `validate` in CI | Blocking |
| State backed remotely, locked, per environment | — |

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

**Every test runs against the Miral reference fixture** — two brands, three regions across
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

## 10. Commits and Branches

**Conventional Commits**, scoped to the context:

```
feat(orders): add dual-authorisation to refund flow
fix(access): correct re-entry count on group media
chore(contracts): bump identity spec to v1.2.0
```

Types: `feat` `fix` `refactor` `perf` `test` `docs` `chore` `build` `ci`

Trailers per `AI_AUTHORSHIP.md`:

```
Refs: C04, 2.12.3
Assisted-By: Claude (Anthropic) <ai@softlabs.example>
```

Branches: `<type>/<context>/<short-description>` — `feat/orders/dual-auth-refund`.

Squash on merge. One logical change per commit on `main`.
