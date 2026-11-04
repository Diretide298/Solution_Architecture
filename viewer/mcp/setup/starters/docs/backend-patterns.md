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
| `DateTime.Now` / `.Today` / `.UtcNow`, `DateTimeOffset.Now`, `TimeZoneInfo.Local` | `DateTimeOffset.UtcNow` or `TimeProvider`, and the venue's time zone | Venues span time zones within one tenant; server-local time is meaningless |
| `Guid.NewGuid()` | `TICVAI.Domain.Identity.Id.New()` | It mints UUID v4; every new id is UUIDv7 ([naming-and-style](naming-and-style.md) 4) |

| Rule (review) | Use | Why |
|---|---|---|
| No bare `decimal` for money | `TICVAI.Domain.ValueObjects.Money`: `{ amount, currency, scale }` (ADR-0008). The trading currency's scale comes from the venue's or region's settings; any other currency's from `CurrencyMinorUnits` (`Money.InMinorUnits`). On the wire `MoneyJsonConverter` writes the amount as a decimal string; `Allocate` splits an amount without losing a minor unit | A raw decimal loses the currency and its scale (AED 2, OMR 3); an amount with more places than its scale is refused |
| Every id is a `Guid`, stored as `uuid` | `TICVAI.Domain.Identity.Id.New()` (UUIDv7) for a row created on the server; the device's id, unchanged, for one created offline | One id type ([naming-and-style](naming-and-style.md) 4); time-ordered, so indexes stay compact; PostgreSQL 16 has no `uuidv7()`, so the application mints every id |
| Human codes people read or type (order numbers, ticket codes) | a separate column | A code is not the id; it can be reissued or reformatted without touching a key |

`BaseEntity<TId>` takes the id from its caller and never mints one, so a row loaded from the
database or created offline keeps the id it arrived with. Inside an entity its own `Id` property hides
the `Id` class: write `Identity.Id.New()` there.

### 3.2 Structure

| Project | Holds | May reference |
|---|---|---|
| `TICVAI.Domain` | entities, value objects (`Money`, `CurrencyMinorUnits`), `Id`, domain exceptions | nothing |
| `TICVAI.Contracts` | request, response and event types, named as the contract names them | nothing |
| `TICVAI.Application` | `Features/<Module>/` use cases, `Result`/`Error`, abstractions (`ITenantContext`, `ICurrentPrincipal`, `ResolvedAuthority`, `ISessionRegistry`, `ITenantDirectory`, `IIdempotencyStore`, `IdempotentExecution`, `ITransactionRunner`, `IOutbox`, `IBrokerPublisher`) | Domain, Contracts |
| `TICVAI.Infrastructure` | EF Core `DbContext` on the request's tenant database, `ScopeContextInterceptor`, `EfTransactionRunner`, `PostgresIdempotencyStore`, repositories, `SqlMigrationRunner`, external services | Application |
| `TICVAI.Api` | controllers, middleware, `Program.cs` | Application, Contracts, Infrastructure |

- **The reference rules are enforced by `TICVAI.ArchitectureTests`, not by convention.** A
  layer referencing one it may not fails the test run.
- A module is a folder `Features/<Module>/` (in Application, and in Infrastructure or Api where it has
  code there), named as ADR-0055's module map names it: the 16 in
  `tests/TICVAI.ArchitectureTests/modules.json` (`Order`, `Catalogue`, `FnB`, ...). Another module uses
  it only through its `Features/<Module>/Public/` types (its query and write API, ADR-0055 rules 2 and
  3); across deployables not even that, except where the reader's host composes the module's queries
  in process. `ModuleBoundaryTests` checks every module on the compiled IL, method bodies included.
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

        // Guard clauses first, happy path unindented. The permission is checked at the scope the
        // operation acts on (spec 7.2), never against the flat EffectivePermissions.
        if (!principal.Permits("ORDER_REFUND", request.VenueScopePath))
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
| `readonly record struct` for value objects | `Money` |
| `Result<T>` for expected failures | Exceptions for the genuinely unexpected |
| `CancellationToken` on every async method | Threaded through, never ignored |
| `.ConfigureAwait(false)` in library code | Not in the API layer |
| Constructor injection only | No service locator, no static access to DI |
| One public type per file | File named for the type |

### 3.4 Data access

- **The tenant is the request's host's** (ADR-0038: one process serves every tenant of the cell, a
  database each). `TenantResolutionMiddleware` resolves the host through `ITenantDirectory` before
  authentication; no tenant header or body field is read. A token whose `tenant` claim (`tid` for
  serviceAuth) is not that tenant, or whose `sid` names a session of another tenant, is `401`
  (`TenantBinding`, r13 review C-05). `TicvaiDbContext` connects to that tenant's database.
- **Every permission check is per scope**: `ICurrentPrincipal.Permits(permission, scopePath)` with the
  scope the operation acts on (the venue, the workstation, the tenant root for a tenant-level
  operation). It runs section 2 of the permission-resolution spec over the selected role's grants
  (`ResolvedAuthority`); `EffectivePermissions` is for coarse checks only and never decides an
  operation (spec 7.2, CR-189, CR-367). Every vector of `PermissionVectors.json` runs through it in
  `TICVAI.UnitTests`.
- **Data access runs in a transaction** (`ITransactionRunner`). Its start sets `ticvai.scope_paths`,
  `ticvai.subject_id` and `ticvai.principal_id` with `SET LOCAL` semantics (`ScopeContextInterceptor`:
  `set_config(..., true)`), so the context ends with the transaction and never reaches the next user
  of a pooled connection. Never `SET` them on the connection. A query outside a transaction sees no
  scoped rows. RLS is defence in depth, not the only line.
- **The schema is plain SQL migrations we write, not EF Core migrations.** Each [DB] ticket names
  its file (`V0001__baseline.sql`, `V0022__catalogue.sql`, ...); you write it in our `db/tenant`
  or `db/control` folder. The package's numbered files (`backend/tenant` and `backend/control`:
  000 schemas, 002 the migration register, 010 per module, 900 foreign keys, 910 indexes, 920
  row-level security, 930 partitioning, and the `V01nn__after_r1_*` files) are the **reference you
  copy from, never run as they are**. Copying functions or tables out of them, such as the
  helpers at the top of 920 and 930, is expected; their "Do not hand-edit" is about the package's
  own files. `SqlMigrationRunner` applies our files in order and records each with its checksum in
  `platform.schema_version`. A [DB] ticket is done when `node .claude/scripts/db-ticket.mjs <ticket>`
  says MATCH: its file, applied to a copy of the previous state and then applied again, leaves exactly
  what the package's statements leave and changes nothing else. Before the merge request,
  `--full <database>` applies every file once, in order, to an empty database. Never edit an
  applied file: add a new one.
- **Idempotency-Key** (`common.yaml` `IdempotencyKey`, SD-024, CR-182): run the change through
  `IdempotentExecution`. A replay with the same request gets the first answer and writes nothing; the
  same key with a different request is `409` `idempotency-conflict` and is never applied; two
  concurrent first requests apply once. The record is `platform.idempotency_record`, written by
  `PostgresIdempotencyStore` in the change's own transaction and unique on (operation, key). Redis may
  cache it; it is never the guarantee.
- Parameterised always. String-concatenated SQL is a build-blocking review finding.
- Explicit transaction boundaries. Order + payment + entitlement + ledger is **one**
  transaction.
- No lazy loading. Fetch what you need.

### 3.5 Events

An event is published in two steps, by two interfaces that must not be confused (ADR-0033, ADR-0058
as amended 1 October 2026):

| Interface | Who calls it | What it does |
|---|---|---|
| `IOutbox` (`Application/Abstractions/Messaging`) | a module, in a use case | `EnqueueAsync` writes the event to `platform.outbox` **in the transaction of the state change**. It never talks to the broker |
| `IBrokerPublisher` (same folder) | the outbox relay, and nothing else (ADR-0055 puts it in the workers deployable; this starter has no workers host yet) | `PublishBatchAsync` sends a batch of `EventEnvelope`s, keyed by aggregate id, and returns once the broker has confirmed all of them. One adapter per broker implements it |

- **A module never publishes to the broker.** A crash between commit and a direct publish loses the
  event; the outbox row commits with the change or not at all. Modules do not reference a broker
  client, and do not take `IBrokerPublisher`.
- **An event implements `IIntegrationEvent`**, which carries the ADR-0058 envelope: `EventId`
  (UUIDv7, the outbox row id and every consumer's inbox key), `EventName` and `EventVersion` as the
  catalogue (`events/*.yaml`) names them, `AggregateType`, `AggregateId` (the ordering key),
  `Sequence` (the aggregate's version after the change, assigned in the same transaction),
  `TenantId`, `ScopePath` and `OccurredAt`. The type's own properties are the payload.
- **The relay drains.** One loop per tenant database reads up to `Relay:BatchSize` unpublished rows
  (200; 1,000 in the flash-sale burst environment), publishes them, marks them published and commits.
  A full batch polls again at once; a partial one waits `Relay:BusyInterval` (100 ms); an empty one
  backs off to `Relay:IdleInterval` (2 s). `RelayOptions` and `RelayPacing` in
  `Infrastructure/Messaging` hold the rule.
- **Consumers de-duplicate in their inbox**, in the transaction of their effect, and check
  `Sequence` for gaps. Delivery is at least once on either broker.
- **Republishing is the relay's job too.** Recovering a lost broker re-reads outbox rows by tenant
  and time range and sends them through `IBrokerPublisher` again; the inboxes absorb the duplicates.

---

## 7. Terraform

| Rule | Detail |
|---|---|
| Provider: `azurerm`, Azure in a UAE region | Decided 28 September, audit R057. The region per cell is a tfvar |
| Modules parameterised, never copy-pasted per cell | One `cell` module, N tfvars |
| `prevent_destroy` on databases and key vaults | — |
| No inline secrets | Key vault references |
| Variables carry `description` and `validation` | Validation catches jurisdiction typos at plan time |
| `terraform fmt` and `validate` in CI | Blocking |
| State backed remotely, locked, per environment | `azurerm` backend (blob lease lock). Staging's state is a storage account in the Softlabs subscription, configured at `terraform init -backend-config=backend.hcl` (`environments/staging/backend.hcl.example`); production's is the client's, later (the lead, 20 October 2026, r8 causes FOUNDATION-AI-C23, C52) |
| Environments | dev on laptops (docker compose, no cell); one shared `staging` in the Softlabs subscription; `production` hosted by the client later. `environment` and `cell` name every resource; tenants are never module inputs (ADR-0039; FOUNDATION-AI-C55) |

---

