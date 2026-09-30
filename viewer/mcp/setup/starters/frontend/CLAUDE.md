# TICVAI frontend

Nx 20 workspace, pnpm, TypeScript (strict). 13 apps (React Native and React web) share four packages.

| Path | What it is |
|---|---|
| `packages/api-client` | the typed client for the API contracts |
| `packages/design-tokens` | colours, type, spacing - depends on nothing |
| `packages/ui` | shared components |
| `packages/offline-core` | the one offline store: SQLite adapter, outbox, sync, ids (UUIDv7) |

<!-- apps:begin (sync-frontend-apps.py) -->
The apps are the package's own (`ticvai/frontend/*.yaml`), named by who operates them. A screen's
`implementation.app` is the folder it goes in; its platform code (P01...) maps to an app here.

| App | Runtime | Offline | Serves | Screens |
|---|---|---|---|---|
| `apps/accreditation-web` | React web (web) | no | P11 | 8 |
| `apps/developer-portal-web` | React web (web) | no | P14 |  |
| `apps/guest-app` | React Native (mobileApp) | **yes** | P02, P05 | 80 |
| `apps/guest-web` | React web (web) | no | P01 | 35 |
| `apps/kitchen-display` | React web (kiosk) | **yes** | P15 |  |
| `apps/partner-web` | React web (web) | no | P10 | 21 |
| `apps/signup-web` | React web (web) | no | P17 |  |
| `apps/ticvai-web` | React web (web) | no | P09 | 37 |
| `apps/venue-management-web` | React web (web) | no | P08, P13, P16 | 111 |
| `apps/venue-pos` | React Native (posTerminal) | **yes** | P04 | 10 |
| `apps/venue-scanner` | React Native (handheld) | **yes** | P07 | 16 |
| `apps/venue-staff-app` | React Native (mobileApp) | **yes** | P06 | 50 |
| `apps/venue-support-web` | React web (web) | no | P12 | 8 |

**Adding an app:** the package adds its manifest first; then `python viewer/mcp/setup/starters/sync-frontend-apps.py`
in the ADAM repo scaffolds it here. Do not create an app folder by hand - it would not match the screens.
<!-- apps:end -->

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
- Ids created on a device are UUIDv7 from `newId()`, the format the server mints; human codes
  people read or type (order numbers, ticket codes) are separate fields.
- Function components with hooks, named exports, no `any`.
- The screen and its API calls come from ADAM: build what the screen and contract say.

## Working a ticket (ADAM)

ADAM is connected for this folder. It holds the screens, journeys and contracts; OpenProject holds the tickets.

1. `adam_pull` the ticket with `dir` set to this folder. Read `.adam/work/<ticket>/README.md`,
   then only the linked files it lists. Ask ADAM (`adam_screen`, `adam_journey`, `adam_contract`)
   rather than guessing a name or a shape.
   **Read its Comments section too**, the newest last: a clarification or QA's reason for sending
   it back overrides the description where they differ - say so when it does.
2. Build exactly what the ticket and its linked artefacts describe, in the app it names.
3. Add tests next to the code (`*.test.ts[x]`). `pnpm lint`, `pnpm typecheck` and `pnpm test` must pass.
4. `adam_propose` the ticket: **Ready for QA**, 100% (see the statuses below; never Closed), and a 2-4 line comment on what was built and
   that the checks pass. Show the proposal and **wait for a yes** before `adam_apply`.

## Ticket kinds

| Ticket | Built means | Tested means |
|---|---|---|
| **[FE]** (`APP-*`) | the screen in the app its `implementation.app` names, with every state the screen lists | component tests per state; `pnpm lint`, `pnpm typecheck`, `pnpm test` pass |
| **[DevOps]** / **[Onboarding]** | see the description; nothing is linked, and that is normal | as the description says |

**The API client is generated, not written.** `packages/api-client` is filled from the contracts by
the `SETUP-CLIENTS` ticket. Until it lands, a screen ticket builds against the client's generated
types as the contract names them and stubs the calls; do not hand-write a client.

**Wireframes.** Build from a screen's wireframe only when its record says it is client-verified.
Otherwise build the logic (calls, state, offline) with a placeholder layout, and never from a
wireframe that did not come through ADAM.

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
