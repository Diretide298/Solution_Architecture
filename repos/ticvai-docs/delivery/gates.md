# Gates

> **Purpose:** What each gate checks and who signs  
> **Owner:** Chinmay  
> **Status:** Settled


## Gate 0 — Boundary sign-off

**Signs:** Dinesh

- Context boundary defined; entities owned vs referenced explicit
- Glossary terms for this context agreed
- Boundaries align with service boundaries in the HLD/LLD

## Gate 1 — Contract review

**Signs:** Chinmay, with backend, frontend and AI represented

Three questions only:

1. Can the frontend build **every page** in this context against it?
2. Can the backend implement it **without needing a field that isn't there**?
3. Does every operation declare `x-ticvai-permission`, `x-ticvai-scope-level`, `x-ticvai-offline-capable` and `x-ticvai-conflict-policy`?

Plus: Money uses the `Money` type · errors are RFC 9457 with enumerated types · pagination is cursor-based · mutations carry `Idempotency-Key`.

## Gate 2 — Mock-proven

**Signs:** Frontend lead

**One end-to-end flow runs against the Prism mock with zero backend code.**

If it cannot, the contract is wrong — and finding out now costs a day instead of a sprint.

**After Gate 2 the contract is frozen.** Changes need a version bump and review.

## Gate 3 — Migration safe

**Signs:** Dinesh

- Runs forward on a canary cell
- **Rollback tested**, not assumed
- Per-cell schema version register updated
- No long-held lock on a hot table during trading hours

## Gate 4 — Slice proven

**Signs:** All leads

- End-to-end path completes against the **reference fixture** — two brands, three regions, two currencies
- For contexts with offline surfaces: completes with the network **severed mid-transaction** and reconciles on reconnect
- Permission matrix asserted: every permission × every scope level
- Architecture tests, contract tests, integration tests green

## Gate 5 — Context closed

**Signs:** Chinmay

- Contract promoted to v1.0
- Deviations recorded in [registers/deviations](../registers/deviations.md)
- Domain page written in [product/modules](../product/modules/README.md)
- New decisions captured as [ADRs](../adr/README.md)
- Load tested at tenant aggregate with correlated peaks
