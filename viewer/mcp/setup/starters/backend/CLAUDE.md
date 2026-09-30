# TICVAI backend

.NET 10, ASP.NET Core, EF Core on PostgreSQL. Clean architecture:

| Project | Holds | May reference |
|---|---|---|
| `src/TICVAI.Domain` | entities, value objects, domain exceptions | nothing |
| `src/TICVAI.Contracts` | request, response and event types | nothing |
| `src/TICVAI.Application` | features (use cases), `Result`/`Error`, abstractions | Domain, Contracts |
| `src/TICVAI.Infrastructure` | EF Core `DbContext`, repositories, external services | Application |
| `src/TICVAI.Api` | controllers, middleware, `Program.cs` | Application, Contracts, Infrastructure |
| `tests/TICVAI.UnitTests` | Domain and Application tests (xUnit) | |
| `tests/TICVAI.IntegrationTests` | tests through the API | |
| `tests/TICVAI.ArchitectureTests` | the reference rules above | |

```
dotnet build TICVAI-Backend.slnx
dotnet test TICVAI-Backend.slnx
dotnet run --project src/TICVAI.Api        # needs Database:ConnectionString
```

## Coding standards

Loaded into every session, so every ticket is built to them:

@project-bible/setup/naming-and-style.md
@project-bible/setup/backend-patterns.md
@project-bible/setup/quality-gates.md

Read these when the work calls for them, not before:

| Read | When |
|---|---|
| `project-bible/setup/api-conventions.md` | adding or changing an endpoint, an error or paging |
| `project-bible/setup/git-and-mrs.md` | before a commit or a merge request |
| `project-bible/setup/llm-conventions.md` | before a commit: what AI-written code must carry |
| `project-bible/setup/data-and-storage.md` | touching tables, migrations or local storage |
| `project-bible/setup/config-and-secrets.md` | adding a setting, a connection string or a secret |
| `project-bible/setup/dependencies.md` | adding a package |
| `project-bible/setup/adding-things.md` | adding a module, a permission or an integration |

In one session, a document already read does not need reading again.

The kernel those documents name is here: `Money` and `Id` (Domain), `ITenantContext`,
`ICurrentPrincipal` and `IIdempotencyStore` (Application), `SqlMigrationRunner` (Infrastructure).
`Directory.Build.props` treats warnings as errors and bans server-local time and `Guid.NewGuid()`.

## Hard rules

- A failed operation returns `Result.Failure(new Error(code, message))`; exceptions are for the unexpected.
  Errors leave the API as `application/problem+json` (see `ExceptionHandlingMiddleware`).
- Timestamps are UTC `DateTimeOffset`. Never `DateTime.Now`.
- Every id is a `uuid` (`Guid`). A new one is a UUIDv7 from `Id.New()`; an id a device sent keeps its value.
  Human codes people read or type (order numbers, ticket codes) are separate columns, not ids.
- No secrets or connection strings in source. `appsettings.json` keeps them empty.
- Every data path is scoped by `ITenantContext`.
- A contract comes first: build what the ADAM contract says - status codes, error codes, field names.

## Working a ticket (ADAM)

ADAM is connected for this folder. It holds the contracts, tables and screens; OpenProject holds the tickets.

1. `adam_pull` the ticket with `dir` set to this folder. Read `.adam/work/<ticket>/README.md`,
   then only the linked files it lists. Ask ADAM (`adam_contract`, `adam_table`, `adam_search`)
   rather than guessing a name or a shape.
   **Read its Comments section too**, the newest last: a clarification or QA's reason for sending
   it back overrides the description where they differ - say so when it does.
2. Build exactly what the ticket and its linked artefacts describe. Nothing outside the ticket.
3. Add tests for the success case and each error the contract lists. `dotnet test` must pass.
4. `adam_propose` the ticket: **Ready for QA**, 100% (see the statuses below; never Closed), and a 2-4 line comment on what was built and
   that the tests pass. Show the proposal and **wait for a yes** before `adam_apply`.

## Ticket kinds

"Working a ticket" above is the [BE] path: a contract-backed operation. The other kinds differ in
what "built" and "tested" mean:

| Ticket | Built means | Tested means | Propose |
|---|---|---|---|
| **[BE]** (`SVC-*`) | the operations the ticket names, as the contract says | a test for the success case and each listed error; `dotnet test` passes | Ready for QA |
| **[DB]** (`MIG-*`) | the ticket's numbered SQL file(s) in `db/<database>/`, from the package's `backend/` DDL | `SqlMigrationRunner` applies the folder to an empty PostgreSQL, and a second run applies nothing | Ready for QA |
| **[DevOps]** (`SETUP-*`) | the pipeline, environment or seed the description names, in the repository it names | it runs once end to end; say in the comment what QA can re-run | Ready for QA |
| **[Onboarding]** | nothing to build: the step is done when the connector answers in this folder | `adam_board` returns your board | Ready for QA with that as evidence |

A setup ticket links no contract or screen; that is normal, not a gap.

## Searching pulled files

`.adam/` is git-ignored, so **Grep skips it unless told not to**: search pulled files with
`--no-ignore` (or read them directly). Read works as usual.

## When the package is wrong

If the contract, table, screen or journey you are building from contradicts itself, is wrong, or
lacks something the ticket needs, **do not settle it in code** - not even with a sensible guess.

1. `adam_changes` for the artefact: somebody may have raised it already. If so, name that CR.
2. Otherwise `adam_draft_change`: quote the conflicting passages in `evidence`, list the `options`,
   say which you would pick in `recommendation`, set `blocking` and the `ticket`.
3. Show the draft and **wait for a yes** before `adam_raise_change`.
4. If it blocks the ticket, offer to propose the ticket **On hold** with "Blocked by CR-<n>".
   Build whatever the question does not touch.

Before building against an artefact, check `adam_changes` for an accepted request on it: the
package may be about to change.

## Ticket statuses (OpenProject)

| Status | Use it when |
|---|---|
| **New** | Not started. Never set it yourself. |
| **In progress** | Work has started but is not finished - a build that stopped part-way, or tests still failing. |
| **Ready for QA** | Done on your side: built as the ticket and its contract describe, and the tests pass. **This is where finished work goes.** Say in the comment what QA should check. |
| **Closed** | Set by QA after testing. **Never propose it yourself**, even when everything passes: the person who built it is not the person who says it works. |
| **On hold** | Blocked on something outside this repository - a missing contract, an unanswered question, an open change request. Say what in the comment. |
| **Rejected** | Only when the person says the ticket will not be done. Never on your own. |

Pair the status with % done: In progress 10-90, Ready for QA 100, On hold unchanged.
If the live statuses have no QA status, stop and ask rather than choosing Closed.
These are the statuses on pms.softlabsgroup.in. `adam_propose` with only a ticket number lists
the live ones; if they differ from this table, use those.

`.adam/` is a local copy and is git-ignored. Never commit it.
