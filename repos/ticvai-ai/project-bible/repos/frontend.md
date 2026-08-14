# Frontend Runtime

Nx monorepo. Six apps, four shared packages.

## Enforced boundaries

`@nx/enforce-module-boundaries` blocks:

| Blocked | Why |
|---|---|
| Apps importing a SQLite driver directly | Everything goes through `offline-core`. Six sync engines is six divergent bug surfaces |
| Packages importing apps | Dependencies point one way |
| **Local permission computation** | Clients consume `effectivePermissions`. Client-side authz is both a security hole and a divergence source |
| `localStorage` / `sessionStorage` | Unsupported in the target runtime |

## Compiler

`strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`,
`verbatimModuleSyntax`. **`any` is prohibited** — use `unknown` and narrow.

## Offline

- **Every mutating call goes through the `offline-core` outbox.** No direct fetch on a write path
- Conflict policy declared **per entity at the call site**. No global default
- The offline indicator reflects real transport state, never an optimistic guess
- Errors surface to the user. A swallowed sync failure behind "all synced" is worse than an error

| Policy | Applies to | Behaviour |
|---|---|---|
| `append` | Sales, scans | Never conflict; server appends |
| `serverWins` | Configuration | Local change discarded |
| `manual` | Rare | Surfaced in UI, never resolved silently |

## Apps and their offline profile

| App | Offline | Note |
|---|---|---|
| pos | Full | Installable thick client |
| scanner | **Full, mandatory** | Native. Explicitly not web |
| employee | Partial | Validity lookup, not full scanning |
| guest | Partial | White-label per tenant, built per tenant |
| backoffice | None | Config-heavy, desktop |
| web-b2c | None | Tenant-themed |

## Style

Function components and hooks only · props typed with an interface, never inline · no
`React.FC` · discriminated unions over optional-field soup · no business logic in
components — hooks and packages · named exports.
