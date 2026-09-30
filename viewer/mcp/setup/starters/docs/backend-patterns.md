# Backend Patterns — C# / .NET 10

Shared rules: [quality-gates](quality-gates.md). Naming: [naming-and-style](naming-and-style.md).

This describes the backend repository as the setup zip creates it: `TICVAI-Backend.slnx`,
.NET 10, clean architecture in `src/TICVAI.*`. Where a type is named here, it exists there.

## 3. C# / .NET 10

### 3.1 Enforced at compile time

`Directory.Build.props` sets `TreatWarningsAsErrors`, `Nullable=enable`,
`EnforceCodeStyleInBuild`, and wires `BannedApiAnalyzers` over `BannedSymbols.txt`.

| Banned (build error) | Use instead | Why |
|---|---|---|
| `DateTime.Now` / `.Today` / `.UtcNow`, `DateTimeOffset.Now` | `DateTimeOffset.UtcNow` or `TimeProvider` | Venues span time zones within one tenant; server-local time is meaningless |
| `Guid.NewGuid()` | `TICVAI.Domain.Identity.Id.New()` | It mints UUID v4; every new id is UUIDv7 ([naming-and-style](naming-and-style.md) 4) |

| Rule (review) | Use | Why |
|---|---|---|
| No bare `decimal` for money | `TICVAI.Domain.ValueObjects.Money` (amount + ISO 4217 code) | A raw decimal loses the currency and its scale (AED 2, OMR 3) |
| Every id is a `Guid`, stored as `uuid` | `TICVAI.Domain.Identity.Id.New()` (UUIDv7) for a row created on the server; the device's id, unchanged, for one created offline | One id type ([naming-and-style](naming-and-style.md) 4); time-ordered, so indexes stay compact; PostgreSQL 16 has no `uuidv7()`, so the application mints every id |
| Human codes people read or type (order numbers, ticket codes) | a separate column | A code is not the id; it can be reissued or reformatted without touching a key |

`BaseEntity<TId>` takes the id from its caller and never mints one, so a row loaded from the
database or created offline keeps the id it arrived with. Inside an entity its own `Id` property hides
the `Id` class: write `Identity.Id.New()` there.

### 3.2 Structure

| Project | Holds | May reference |
|---|---|---|
| `TICVAI.Domain` | entities, value objects (`Money`), `Id`, domain exceptions | nothing |
| `TICVAI.Contracts` | request, response and event types, named as the contract names them | nothing |
| `TICVAI.Application` | `Features/<Module>/` use cases, `Result`/`Error`, abstractions (`ITenantContext`, `ICurrentPrincipal`, `IIdempotencyStore`) | Domain, Contracts |
| `TICVAI.Infrastructure` | EF Core `DbContext`, repositories, `SqlMigrationRunner`, external services | Application |
| `TICVAI.Api` | controllers, middleware, `Program.cs` | Application, Contracts, Infrastructure |

- **The reference rules are enforced by `TICVAI.ArchitectureTests`, not by convention.** A
  layer referencing one it may not fails the test run.
- A module is a folder under `Application/Features/`, named for the service (`Orders`,
  `Catalogue`). Two modules share only what is in `TICVAI.Domain` or `TICVAI.Contracts`.
- Domain layer is persistence-ignorant — no EF, Npgsql, Redis or ASP.NET references.
- API layer returns contract DTOs, never domain entities.

### 3.3 Style

```csharp
// File-scoped namespaces. Primary constructors where they read well.
namespace TICVAI.Application.Features.Orders;

public sealed class RefundAuthoriser(
    IOrderRepository orders,
    ICurrentPrincipal principal,
    ILogger<RefundAuthoriser> logger)
{
    // Expected failures return Result<T>. Exceptions are for the unexpected.
    public async Task<Result<RefundAuthorisation>> AuthoriseAsync(
        RefundRequest request,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(request);

        // Guard clauses first, happy path unindented.
        if (!principal.Has("ORDER_REFUND"))
        {
            return Result<RefundAuthorisation>.Failure(Error.Forbidden("ORDER_REFUND"));
        }

        if (request.Amount.Amount <= 0)
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

- Every query runs with `ticvai.scope_paths` set from `ITenantContext.ScopePaths`. RLS is
  defence in depth, not the only line.
- **The schema is the package's derived DDL, not EF Core migrations.** `backend/tenant/*.sql`
  and `backend/control/*.sql` (000 schemas, 002 the migration register, 010 per module, 900
  foreign keys, 910 indexes, 920 row-level security) are applied in file order by
  `SqlMigrationRunner`, which records each file and its checksum in `platform.schema_version`.
  A [DB] ticket is done when its file applies to an empty database and a second run applies
  nothing. Never edit an applied file: add a new one.
- A retried mutating request with the same `Idempotency-Key` gets the first answer, from
  `IIdempotencyStore` (in memory in development; Redis in production).
- Parameterised always. String-concatenated SQL is a build-blocking review finding.
- Explicit transaction boundaries. Order + payment + entitlement + ledger is **one**
  transaction.
- No lazy loading. Fetch what you need.

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

