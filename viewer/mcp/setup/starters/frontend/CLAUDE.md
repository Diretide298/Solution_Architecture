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

## Read before writing code

1. `project-bible/setup/naming-and-style.md` - naming, money, time, banned words
2. `project-bible/setup/frontend-patterns.md` - compiler flags, forbidden imports, components and hooks
3. `project-bible/setup/api-conventions.md` - how the API behaves: errors, paging, versioning
4. `project-bible/setup/quality-gates.md` - what CI enforces
5. `project-bible/setup/git-and-mrs.md` - commits and merge requests
6. `project-bible/setup/llm-conventions.md` - rules for AI-written code
7. As needed: `data-and-storage.md`, `config-and-secrets.md`, `dependencies.md`, `adding-things.md`

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
4. `adam_propose` the ticket: the done status, 100%, and a 2-4 line comment on what was built and
   that the checks pass. Show the proposal and **wait for a yes** before `adam_apply`.

`.adam/` is a local copy and is git-ignored. Never commit it.
