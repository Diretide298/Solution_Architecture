# Sprint 1

> **Purpose:** Weeks 1–2. Foundations. Nothing waits on anyone  
> **Owner:** Chinmay  
> **Status:** **In progress**

**8 people, 21 tasks, zero external dependencies.** Every task below can start today.

## Exit criteria — Gate 0

- [ ] Migration applies **and rolls back** on a canary cell
- [ ] A query without `ticvai.scope_paths` set returns **zero rows**, not everything
- [ ] All permission vectors pass in CI
- [ ] Second login rejected; supervisor force-logout works
- [ ] Reference fixture seeds 3 regions = **3 cells**, 2 currencies
- [ ] A clean clone builds and architecture tests pass

---

## Backend

| # | Task | Owner | Est. | Depends | Status |
|---|---|---|---|---|---|
| B1 | Tenant resolution + RLS with **FORCE** + policy template | BE1 | 5d | — | |
| B2 | Session registry — Redis, single-session, force-logout | BE1 | 4d | — | |
| **B3** | **Permission resolver — R9/R10 closed, vectors in CI** | BE2 | 5d | — | **✅ done** |
| B4 | `ltree` scope tree + grant table + deny-overrides-allow | BE2 | 5d | B3 | |
| **B5** | **Migration orchestrator** — fan-out, version register, resumable, canary gate | BE3 | 10d | — | **critical path** |
| B6 | Outbox + domain event bus | BE3 | 4d | — | |
| B7 | Catalogue bundle — sign, version, delta | BE4 | 8d | — | |
| B8 | Lease manager — grant, renew, expire, sub-lease, force-release | BE4 | 6d | — | |

## Frontend

| # | Task | Owner | Est. | Depends | Status |
|---|---|---|---|---|---|
| F1 | `offline-core` — conflict handlers, connectivity, complete orchestrator | FE1 | 6d | — | |
| F2 | `offline-core` — bundle apply, signature verify, atomic rollback | FE1 | 5d | F1 | |
| F3 | `offline-core` — lease hold, countdown, exhaustion, staleness bound | FE2 | 6d | F1 | |
| F4 | `offline-core` — local order journal, commit-before-acknowledge | FE2 | 5d | F1 | |
| F5 | `design-tokens` + touch-target baseline + **RTL + dark theme** | FE3 | **6d** | — | **scope +2d (CF-42)** |
| F6 | `ui` primitives on tokens, **RTL-aware** | FE3 | **8d** | F5 | **scope +2d (CF-42)** |
| F7 | `api-client` generation + Prism mock in CI | FE4 | 4d | — | |
| F8 | POS shell + nav from `effectivePermissions` | FE4 | 6d | F7 | |

## Infrastructure & architecture

| # | Task | Owner | Est. | Status |
|---|---|---|---|---|
| I1 | Six repos, private registries, CI pipelines | Dinesh | 3d | |
| I2 | Reference fixture — 3 cells, 2 currencies | BE1 | 3d | |
| I3 | OpenTelemetry — tenant, region, venue, cell on every span | BE3 | 3d | |
| C1 | **Audit existing 20% against ADR-0002** | Chinmay | 1d | |
| C2 | Glossary sign-off with Allam | Chinmay | 1d | |

---

## Scope change — 13 August

The client UI/UX boards were read after this sprint was drafted. **The page inventory went
from 99 to 364 screens.** Two Sprint 1 effects:

- **F5 and F6 gain RTL and dark theme.** A full Arabic mirror is not a translation layer,
  and the venue-staff-app app is dark by default. +4 days across the two.
- **White Label Builder is a new Wave 1 context** — 20 screens, C105 and C106. Not in this
  sprint, but it enters the contract queue ahead of some satellites.

## Watch items

**B5 is the critical path and was unowned for two weeks.** Under cell-per-region it fans out
per region, not per tenant. Nothing downstream ships without it.

**C1 is the task most likely to be skipped.** CF-03 was ambiguous for the entire period the
first 20% was built, so whether that code assumed user-driven or device-driven access is
currently unknown. One day now; a sprint at integration.

**F1 blocks F2, F3 and F4.** Three of four frontend tasks queue behind one. Consider pairing
FE1 and FE2 on F1 for the first three days.

## Awaiting client — does not block this sprint

CF-37 FX policy · pilot venue · payment sandbox credentials · hardware models.
