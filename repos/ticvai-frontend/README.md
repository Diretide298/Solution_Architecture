# ticvai-frontend

Nx monorepo. Six apps, four shared packages.

This is the one boundary in the platform where a monorepo earns its cost: the
apps share `offline-core`, which is the hardest code in the project. Six copies
of a sync engine is six divergent bug surfaces.

## Layout

    packages/api-client      generated from ticvai-contracts; auth + tenant interceptors
    packages/offline-core    SQLite, outbox, sync orchestrator, conflict policy
    packages/design-tokens   colour, type, spacing, touch-target minimums
    packages/ui              primitives built on tokens

    apps/pos                 RN thick client. Full offline
    apps/scanner             RN. Full offline, mandatory. Native, not web
    apps/employee            RN. Partial offline. Validity lookup, not full scanning
    apps/guest               RN. White-label per tenant, built per tenant
    apps/backoffice          React web. No offline
    apps/web-b2c             React web. No offline

## Rules enforced by lint, not convention

- Apps may not import a SQLite driver directly. Everything goes through `offline-core`.
- Apps never compute permissions. They consume `effectivePermissions` from the session.
- `design-tokens` and `api-client` are leaves.

## Order of work

Shared packages before apps. Building POS before `offline-core` means writing the
hard parts three more times. App teams start once packages are usable.
