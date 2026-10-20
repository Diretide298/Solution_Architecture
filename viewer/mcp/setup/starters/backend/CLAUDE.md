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
`ICurrentPrincipal`, `IIdempotencyStore`, `IIntegrationEvent`, `IOutbox` and `IBrokerPublisher`
(Application), `SqlMigrationRunner` and `RelayOptions` (Infrastructure).
`Directory.Build.props` treats warnings as errors and bans server-local time and `Guid.NewGuid()`.

## Hard rules

- A failed operation returns `Result.Failure(new Error(code, message))`; exceptions are for the unexpected.
  Errors leave the API as `application/problem+json` (see `ExceptionHandlingMiddleware`).
- Timestamps are UTC `DateTimeOffset`. Never `DateTime.Now`.
- Every id is a `uuid` (`Guid`). A new one is a UUIDv7 from `Id.New()`; an id a device sent keeps its value.
  Human codes people read or type (order numbers, ticket codes) are separate columns, not ids.
- No secrets or connection strings in source. `appsettings.json` keeps them empty.
- Every data path is scoped by `ITenantContext`.
- A module publishes an event with `IOutbox.EnqueueAsync`, in the transaction of the change it reports.
  `IBrokerPublisher` is the relay's; no module calls it or a broker client (backend-patterns 3.5).
- A contract comes first: build what the ADAM contract says - status codes, error codes, field names.

<!-- ADAM:start working-a-ticket -->
## Working a ticket (ADAM)

ADAM is connected for this folder. It holds the contracts, tables and screens; OpenProject holds the tickets.

No ticket named? Do not ask for a number: `adam_board` with `only: "workable"` gives `startHere`, the first ticket
you can finish or its first open sub-task of yours. Start that one.

1. `adam_pull` the ticket with `dir` set to this folder. Read `.adam/work/<ticket>/README.md`,
   then only the linked files it lists. Ask ADAM (`adam_contract`, `adam_table`, `adam_search`)
   rather than guessing a name or a shape.
   **Read its Comments section too**, the newest last: a clarification or QA's reason for sending
   it back overrides the description where they differ - say so when it does.
   **Sub-tasks** in README.md are the work under the ticket, in order: pull the first open one of yours and work
   that, one at a time; work the ticket itself only when none of its open sub-tasks is yours. **Part of** names
   the ticket it belongs to.
   **You are always on the latest release.** ADAM serves the package at its latest release tag
   (r1, r2, …) and every pull is at it; there is no release to choose and nothing to re-pin. If
   README.md says **What changed since your previous pull (rA -> rB)**, tell the person in one line
   (`spec-diff.md` has the diffs) and build against the files as they are now.
   **Read "Change requests on this ticket" too**, near the top of README.md: follow a settled
   decision where it differs from the description, and wait on the part an open non-blocking request
   covers; a blocking one is "When the package is wrong", step 4.
2. Build exactly what the ticket and its linked artefacts describe. Nothing outside the ticket.
3. Add tests for the success case and each error the contract lists. `dotnet test` must pass.
   A [DB] ticket is checked another way: see "A [DB] ticket" below.
4. `adam_propose` the ticket: **Ready for QA**, 100% (see the statuses below; never Closed), and a 2-4 line comment on what was built and
   that the tests pass. Show the proposal and **wait for a yes** before `adam_apply`.

To see a teammate's work, ask ("what is Hrushikant working on?", "what's everyone doing?"):
`adam_team` answers, read-only, with their open and in-progress tickets and what they finished lately.

<!-- ADAM:end working-a-ticket -->

## Ticket kinds

"Working a ticket" above is the [BE] path: a contract-backed operation. The other kinds differ in
what "built" and "tested" mean:

| Ticket | Built means | Tested means | Propose |
|---|---|---|---|
| **[BE]** (`SVC-*`) | the operations the ticket names, as the contract says | a test for the success case and each listed error; `dotnet test` passes | Ready for QA |
| **[DB]** (`MIG-*`) | the ticket's numbered SQL file in `db/<database>/`, from the package's `backend/` DDL | `node .claude/scripts/db-ticket.mjs <ticket>` says MATCH (see "A [DB] ticket") | Ready for QA |
| **[DevOps]** (`SETUP-*`) | the pipeline, environment or seed the description names, in the repository it names | it runs once end to end; say in the comment what QA can re-run | Ready for QA |
| **[Onboarding]** | nothing to build: the step is done when the connector answers in this folder | `adam_board` returns your board | Ready for QA with that as evidence |

A setup ticket links no contract or screen; that is normal, not a gap.

## A [DB] ticket

The ticket is one numbered SQL file in `db/<database>/` (the baseline has one in each database). Its
folder holds `expected-schema.json`: the end state of its tables and the package statements that make it.
This replaces the older rule of applying every migration to an empty database for each ticket,
wherever you meet it (the ticket's Done when, `backend-patterns.md`, an older copy of these files).

1. Write the file the ticket names, from the package statements in `expected-schema.json`. Every
   statement in it must be safe to run twice: `IF NOT EXISTS`, `CREATE OR REPLACE`, and
   `DROP ... IF EXISTS` before an `ADD CONSTRAINT`. Do not `BEGIN` or `COMMIT`: the runner wraps each
   file in one transaction. No GRANT, OWNER, COMMENT or UNLOGGED the package does not have, and no
   rows written into tables that are not the ticket's. The check refuses these outright: `DISABLE` or
   `ENABLE REPLICA/ALWAYS TRIGGER`, `ALTER DEFAULT PRIVILEGES`, role membership (`GRANT <role> TO`,
   `REVOKE <role> FROM`), `GRANT`/`REVOKE` on a database, parameter, tablespace, language, foreign
   server or data wrapper, or large object, `CREATE RULE`, publications and subscriptions, event
   triggers, `CREATE/ALTER/DROP ROLE`, `USER` or `GROUP`, `ALTER SYSTEM`, and `SET ROLE`,
   `SET SESSION AUTHORIZATION` or `session_replication_role` (also through `set_config`). Files
   already applied stay as they are.
2. Run `node .claude/scripts/db-ticket.mjs <ticket>`. It applies only this file to a copy of the
   database at the previous state, applies it a second time (which must succeed and change nothing),
   applies the package statements to a second copy, and compares the two databases whole: the ticket's
   tables must be what the package makes, and nothing else may change, privileges, owners, the
   migration register and rows included. It needs Docker Desktop running; the first run starts its own
   PostgreSQL 16 container. **The first run for a folder can take several minutes** (it builds a
   template of the earlier files): give the command a 10-minute timeout (Bash `timeout: 600000`) or run
   it in the background. Later runs take seconds.
3. A difference names the object and what differs: fix the file and run it again. **MATCH is the evidence
   for done**: quote its result lines in the comment. PARTIAL is not. A foreign key "left for a later
   migration" is not a difference. Rows the file leaves in the ticket's own tables are listed: right
   only if the ticket asks for a backfill.
4. Do not rebuild the other migrations, do not work out the effect by hand, and do not run `dotnet build`
   or `dotnet test` unless the ticket changes C#.
5. Before opening the merge request, run `node .claude/scripts/db-ticket.mjs --full <database>` once
   (the same 10-minute timeout): every migration applied once, in order, to an empty database, as
   SqlMigrationRunner does. Say the result in the comment. No pipeline runs this yet.

If MATCH cannot be reached because the package itself is wrong (a type no file creates, a policy on a
table a later migration creates), the check says so; that is a change request, as in "When the package
is wrong". `node .claude/scripts/db-ticket.mjs --clean` drops this folder's check databases (template,
copies, the --full database) and its kept snapshots, and in its own container removes any role or role
membership a file made and resets role settings. Another folder's databases (template, half-built
template, --full) go by themselves after two weeks unused, or at once when none of them carries a
date of use (leftovers of an older version), but never while that folder is running.

## Searching pulled files

`.adam/` is git-ignored, so **Grep skips it unless told not to**: search pulled files with
`--no-ignore` (or read them directly). Read works as usual.

## When the package is wrong

If the contract, table, screen or journey you are building from contradicts itself, is wrong, or
lacks something the ticket needs, **do not settle it in code** - not even with a sensible guess.

1. `adam_changes` for the artefact: somebody may have raised it already. If so, name that CR.
2. Otherwise `adam_draft_change`: quote the conflicting passages in `evidence`, list the `options`,
   say which you would pick in `recommendation`, set `blocking` and the `ticket`. The intake goes
   with it: `source` is `developer` (the reference defaults to the ticket) unless the person says
   it came from minutes, a client answer, a design or an audit - then `sourceRef`, and for minutes
   `clientSignoff`; `triage` and `when` if known; other `artefacts` it touches; `contractImpact`
   (none, additive, breaking - breaking needs an `approver`); `effortPoints` if the estimate moves.
3. Show the draft and **wait for a yes** before `adam_raise_change`.
4. **A blocker is always a change request** (CHG-ADM-004): set `blocking: true`, and once it is filed,
   propose the ticket **On hold** with "Blocked by CR-<n>" (applied only after a yes). Never work around
   it and never build a guess. Then find the next ticket you can finish: `adam_board` with
   `only: "workable"` lists, in board order, the tickets no open blocking CR affects (a ticket's
   `blocked` column and the "Blocked by" section of its README.md name the CRs). Propose the first one,
   and say which CR holds back each ticket you skipped.

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
