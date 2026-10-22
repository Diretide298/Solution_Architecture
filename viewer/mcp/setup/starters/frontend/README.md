# TICVAI frontend

Nx workspace: the package's 13 apps and four shared packages.

This is ADAM's old frontend starter, made only with setup's `-UseStarter`. The TICVAI frontend is
one repository per app now (the GitLab group `ticvai-frontend`): a developer runs setup, which
makes a frontend workspace with ADAM's files, and clones their app's repository inside it.

## Run it

Requires Node 22 and pnpm 9 or newer.

```
pnpm install
pnpm lint          # nx run-many -t lint
pnpm typecheck
pnpm test          # vitest per project
pnpm nx graph
```

## Layout

Nx 20, pnpm, TypeScript (strict). Import a package as `@ticvai/<name>` (see `tsconfig.base.json`).

| Path | What it is |
|---|---|
| `packages/api-client` | the typed client for the API contracts: the transport now, the generated operations from SETUP-CLIENTS |
| `packages/design-tokens` | the shared colours, type, spacing, density, from the package's `screens/_design-tokens.yaml` - depends on nothing. Not a guest app's theme: that is its own tokens file (`handoff/design-tokens/guest-web.yaml`, `guest-app.yaml`), applied by its SETUP-SHELL-<APP> ticket's shell |
| `packages/ui` | shared components; for now their props and the token-to-style mapping (`buttonStyle`, `badgeStyle`) |
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

## Rules of this workspace

- Apps depend only on packages (`.eslintrc.cjs` enforces it). A package never imports an app.
- **No app talks to SQLite or does its own sync.** Everything offline goes through `@ticvai/offline-core`.
- Ids created on a device come from `newId()` in `@ticvai/offline-core`.
- `packages/api-client` is filled from the contracts by the `SETUP-CLIENTS` ticket. What is there
  already is the transport the generated operations call: `createApiClient` sends the
  `Idempotency-Key` (a UUIDv7) on every write, returns the `X-Consistency-Token`, and throws a
  problem+json response as `ApiError` - switch on its `slug`, never on the status or the text.

## Working with Claude Code

`CLAUDE.md` tells Claude how to work a ticket through ADAM. The team's coding standards are in
`project-bible/setup/`.
