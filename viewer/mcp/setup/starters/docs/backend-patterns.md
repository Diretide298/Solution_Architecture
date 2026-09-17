# Backend Patterns — C# / .NET 8

Shared rules: [quality-gates](quality-gates.md). Naming: [naming-and-style](naming-and-style.md).

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

