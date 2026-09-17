# TICVAI frontend

Nx 20 workspace, pnpm, TypeScript (strict). React Native apps and a React web app share four packages.

| Path | What it is |
|---|---|
| `apps/backoffice`, `apps/employee`, `apps/guest`, `apps/pos`, `apps/scanner` | React Native apps (`platform:react-native`) |
| `apps/web-b2c` | the public web app |
| `packages/api-client` | the typed client for the API contracts |
| `packages/design-tokens` | colours, type, spacing - depends on nothing |
| `packages/ui` | shared components |
| `packages/offline-core` | the one offline store: SQLite adapter, outbox, sync, ULIDs |

Import a package as `@ticvai/<name>` (see `tsconfig.base.json`).

```
pnpm install
pnpm lint          # nx run-many -t lint
pnpm typecheck
pnpm test          # vitest per project
pnpm nx graph
```

## Coding standards

Loaded into every session, so every ticket is built to them:

@project-bible/setup/naming-and-style.md
@project-bible/setup/frontend-patterns.md
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

## Hard rules

- Apps depend only on packages (`.eslintrc.cjs` enforces it). A package never imports an app.
- **No app talks to SQLite or does its own sync.** Everything offline goes through `@ticvai/offline-core`.
- Clients never compute permissions; they read `effectivePermissions` from the session.
- Ids created on a device are ULIDs from `newUlid()`.
- Function components with hooks, named exports, no `any`.
- The screen and its API calls come from ADAM: build what the screen and contract say.

## Working a ticket (ADAM)

ADAM is connected for this folder. It holds the screens, journeys and contracts; OpenProject holds the tickets.

1. `adam_pull` the ticket with `dir` set to this folder. Read `.adam/work/<ticket>/README.md`,
   then only the linked files it lists. Ask ADAM (`adam_screen`, `adam_journey`, `adam_contract`)
   rather than guessing a name or a shape.
2. Build exactly what the ticket and its linked artefacts describe, in the app it names.
3. Add tests next to the code (`*.test.ts[x]`). `pnpm lint`, `pnpm typecheck` and `pnpm test` must pass.
4. `adam_propose` the ticket: **Closed**, 100% (see the statuses below), and a 2-4 line comment on what was built and
   that the checks pass. Show the proposal and **wait for a yes** before `adam_apply`.

## Ticket statuses (OpenProject)

| Status | Use it when |
|---|---|
| **New** | Not started. Never set it yourself. |
| **In progress** | Work has started but is not finished - a build that stopped part-way, or tests still failing. |
| **Closed** | Done: built as the ticket and its contract describe, and the tests pass. |
| **On hold** | Blocked on something outside this repository - a missing contract, an unanswered question. Say what in the comment. |
| **Rejected** | Only when the person says the ticket will not be done. Never on your own. |

Pair the status with % done: In progress 10-90, Closed 100, On hold unchanged.
These are the statuses on pms.softlabsgroup.in. `adam_propose` with only a ticket number lists
the live ones; if they differ from this table, use those.

`.adam/` is a local copy and is git-ignored. Never commit it.
