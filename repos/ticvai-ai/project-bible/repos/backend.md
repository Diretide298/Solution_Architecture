# Backend Runtime

.NET 8. One deployment of this repo serves **one tenant in one jurisdiction**.

## Enforced at compile time

`Directory.Build.props` sets `TreatWarningsAsErrors`, `Nullable=enable`, and wires
`BannedApiAnalyzers`.

| Banned | Use instead | Why |
|---|---|---|
| `System.DateTime` | `DateTimeOffset` | Venues span time zones within one tenant |
| `DateTime.Now` / `.Today` | `DateTimeOffset.UtcNow` | Server-local time is meaningless |
| `decimal` for money | `Money` | Raw decimal loses per-region currency scale |
| `Guid.NewGuid()` for entity IDs | `UlidGenerator.NewUlid()` | Offline generation; index locality |

## Module boundaries are a build gate

`Ticvai.ArchitectureTests` fails the build if a module references another module's
internals. Cross-module communication is via `Shared.Kernel.Abstractions` or the event bus.

`Shared.Kernel` holds **primitives only** — tenant context, money, IDs, result types. Domain
logic there means the boundaries are gone.

Domain layer is persistence-ignorant: no EF, Npgsql, Redis or ASP.NET references.
API layer returns contract DTOs, never domain entities.

## Data access

- Every query runs with `ticvai.scope_paths` set. RLS is defence in depth, not the only line
- Every tenant-scoped table: `ENABLE` **and** `FORCE ROW LEVEL SECURITY`
- Parameterised always. String-concatenated SQL is a blocking review finding
- **Order + payment + entitlement + ledger is one transaction**
- Partition key must be in the primary key on partitioned tables
- No lazy loading

## Style

`sealed` by default · `readonly record struct` for value objects · `Result<T>` for expected
failures, exceptions for the unexpected · `CancellationToken` on every async method ·
`.ConfigureAwait(false)` in library code · constructor injection only · one public type per file.

## Migrations

Forward-only, numbered, checksummed, per-cell version register. **Test rollback before
merge.** `CREATE INDEX CONCURRENTLY` where available — a lock on `sales_order` during
trading is an outage across every venue in the cell.
