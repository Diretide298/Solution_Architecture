# ADR-0055: A modular monolith, deployed as five units

**Status:** Accepted · 30 September 2026 · Chinmay Parab
**Date:** 2026-09-30 · **Deciders:** Chinmay Parab
**Finding:** SD-001 (high), with SD-002 and SD-006
**Amends:** ADR-0028 (service decomposition, amended by this ADR) — the module map stays; the deployment shape and the ownership rule change
**Related:** ADR-0020 (AI boundary) · ADR-0013 (local-first POS) · ADR-0038, amended by ADR-0040 (database per tenant) · ADR-0007 (repositories)

---

## Context

**The package describes 17 services. They all use one database per tenant.** ADR-0038 (amended by ADR-0040
on instance count) puts every schema of a tenant in one database. So every service talks to the same
database. A network boundary between them buys no data isolation.

**The ownership rule is not true today.**

- ADR-0028 line 50: *"no schema is written by two services"*.
- `docs/architecture/data-model.md:19`: *"Each service connects with a role granted access only to its own schema — enforced by Postgres grants"*.
- `handoff/api-data-lineage.json`: **35 tables are written by more than one service**, and there are **894 cross-schema reads in 493 of 2,608 operations**.
- The sale path writes across services (SD-002): `addCartLine` writes `catalogue.inventory_hold`; nine operations write `access.entitlement`; `createPayment` writes `ledger.journal_entry`.

Per-service grants would break 493 operations on day one. Without them, the boundary is convention only.

**The cost of 17 deployables is real and paid from sprint 1.**

- `handoff/sizing.json`, small cell: **34 replicas at the floor** (17 services × 2) for a mean of 64.8 rps and a peak of 382 rps.
- Four deploy configs (`deploy/a-…` to `d-…yml`) and CI must build, version and roll out 17 units.
- The team is 14 people (`docs/active/six-month-plan-29-september.md`). Block A is 35 working days.

**The code is already shaped as a modular monolith.** The starter repository
(`repos/ticvai-backend`) has one host, `Ticvai.Api`, six `Ticvai.Modules.*` projects, and
`tests/Ticvai.ArchitectureTests/ModuleBoundaryTests.cs`, which fails the build if one module
references another. The package (deploy configs, sizing, diagrams) is shaped as 17 services. The two disagree.

**ADR-0028 rejected a modular monolith for two reasons** (line 149 onwards): Access must run at the edge
with a sub-300 ms local decision, and AI must be isolated (ADR-0020). Both reasons are real. The
decision below keeps both as separate deployables.

---

## Decision

**One .NET solution with 17 modules. ADR-0028's module map is unchanged. It is deployed as five units.**

| Deployable | Modules | Share of normal traffic (`sizing.json` mix) | Why it is its own unit |
|---|---|---:|---|
| `commerce` | Identity (with PII), Tenancy (with Workforce, Approvals, Shift), Catalogue, Order (with Payments), Ledger, Wallet | 49.2% | The sale path. Order, payment and ledger can commit in one transaction. Autoscales on RPS |
| `access` | Access | 15.3% | Gate hot path, flat high rate, offline package. The same module code builds the venue edge node |
| `operations` | F&B, Retail, Inventory, VenueOps, Marketing, WhiteLabel, Reporting, Platform (subscription, platform-ops, public-api), CrossRegion | 34.6% | Back office and engagement. Nothing that takes money waits on it |
| `ticvai-ai` | AI (Python) | 1.1% | ADR-0020. Unchanged, three process groups |
| `workers` | Outbox relay (ADR-0058, amended 1 October), event consumers for every module, scheduled jobs | — | Background work scales on queue depth, not on requests |

**The ownership rule is rewritten so that it is true and testable.**

1. A module owns its schemas. Only the owner migrates them.
2. Another module **reads** them only through views the owner publishes, or through the owner's in-process query interface. Not raw tables.
3. Another module **writes** them only by calling the owner's in-process API, inside the caller's transaction. Never with its own SQL.
4. Across deployables, modules talk by event (ADR-0057) or by the published contract over HTTP. Never by shared SQL.

**Enforcement is by three checks, not by grants per module.**

- Architecture tests: extend `ModuleBoundaryTests` from 6 to 17 modules.
- A lineage check in `check-package`: a module's operations touch only their own schemas and published views.
- Postgres roles **per deployable**. The AI role stays read-only on transactional schemas (ADR-0020). That grant is real because AI is its own deployable.

**Split rule.** A module moves to its own deployable when its load profile or release cadence
diverges from its host. Marketing is the first candidate, as ADR-0028 already says.

**F&B prices stay out of `commerce` (2 October 2026).** F&B owns its own catalogue table, so an F&B sale in
`operations` reads no row of the central catalogue in `commerce`, and the ticketing sale path scales on
ticket traffic alone (Chinmay, DEC-034; recorded in ADR-0028's amendment of 2 October; CHG-DOC-009).

---

## Options Considered

### Option A: 17 services (ADR-0028 as written)

| Dimension | Assessment |
|---|---|
| Complexity | High. 17 pipelines, 17 rollouts, distributed transactions on the sale path |
| Cost | 34 replicas at the floor in the smallest cell |
| Scalability | Per-service scaling. But every service shares the tenant database, which is the real limit |
| Team familiarity | Low for 17-service operations with a team of 14 |
| Time to Block A | Slow. Needs the saga for every cross-service write before checkout works |

**Pros:** Independent deploys per service. Matches today's diagrams and sizing.
**Cons:** Boundary is fiction at the data layer. 493 operations cross it. Highest running cost.

### Option B: Modular monolith, five deployables (recommended)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. One solution, five hosts, boundaries kept by tests |
| Cost | About 12 replicas at the floor instead of 34 (ADR-0061, accepted 1 October) |
| Scalability | Per deployable. Access and AI still scale apart. A module can be split out later |
| Team familiarity | High. It is what the starter repository already is |
| Time to Block A | Fastest. Order, payment and ledger in one transaction. Five rollouts |

**Pros:** Keeps both boundaries ADR-0028 needs (edge Access, isolated AI). One transaction on the sale path.
**Cons:** A bad release of `commerce` affects six modules at once. Needs discipline on module boundaries.

### Option C: One deployable for everything except AI

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Cost | Lowest |
| Scalability | Poor. Gate traffic and back-office reports share one process |
| Team familiarity | High |
| Time to Block A | Fast |

**Pros:** Simplest to run.
**Cons:** Loses the Access edge boundary ADR-0028 rightly insists on. A report can slow a gate.

---

## Trade-off Analysis

The real choice is between A and B. A pays for network boundaries that the data layer does not
respect. B accepts a shared deployment for modules that already share a database, and keeps the two
boundaries that matter: the gate at the edge and AI isolated.

B loses independent deploys per module. With one database per tenant and expand-contract
migrations, that independence was limited anyway. A schema change in `catalogue` already breaks
Order, because Order reads it by SQL.

C goes one step too far. Access has a different operational posture (offline, sub-300 ms, flat
load). It should not share a process with Marketing sends.

---

## Consequences

**Easier**

- Checkout commits order, payment and ledger in one transaction (SD-026 becomes smaller).
- Five rollouts per sprint, not 17. One CI pipeline, five images.
- The floor drops from 34 replicas to about 12 (ADR-0061, accepted 1 October, sets the exact floors).
- The shared kernel (tenant resolution, scope, idempotency, outbox) is built once.

**Harder**

- Boundaries depend on tests. A skipped architecture test is a boundary lost.
- A crash in one `commerce` module takes the other five down with it. Bulkheads per dependency (ADR-0032, pooling amended by ADR-0038) matter more.

**Revisit**

- When a module's load or release cadence diverges. Marketing first.
- If a tenant wants a module on dedicated hardware.

---

## Action Items

**Before Monday 5 October 2026**

1. [x] Chinmay's yes on the five-unit shape (30 September 2026).
2. [ ] Package: amend ADR-0028's status line and rule text; fix `data-model.md:19`; fix "Sixteen services" (SD-006). (1 pt)
3. [ ] Package: add a `deployable` field to `handoff/service-decomposition.json`. Keep the 17 services as modules. Re-derive diagrams, `sizing.json`, the four `deploy/*.yml`, then mirrors, then `check-package`. (2 pts)
4. [ ] Tickets: `SVC-*` tickets stay keyed per module; no ticket rewrite. Add **SETUP-HOSTS**: three .NET hosts (`commerce`, `access`, `operations`) and a `workers` host, each composing its modules. (3 pts)
5. [x] Fix the stale line in `repos/ticvai-backend/AGENTS.md` (and the same line in its `CLAUDE.md`): *"One deployment serves one tenant in one jurisdiction"* is no longer true after ADR-0038.

**Sprint 1 (5–23 October)**

6. [ ] **ARCH-TESTS**: extend `ModuleBoundaryTests` to 17 modules; add a test that no module's SQL names another module's schema. (3 pts)
7. [ ] **DB-READ-VIEWS**: generate published read views for the 894 cross-schema reads from lineage (a deriver), applied in the migrations. (5 pts)
8. [ ] **DB-ROLES**: one Postgres role per deployable in MIG-BASELINE; AI read-only. (2 pts)
9. [x] The runtime: the starter targeted .NET 8 (`global.json`, `Directory.Build.props`), and Microsoft's support for .NET 8 ends on 10 November 2026, inside Block A. **Decided 30 September: .NET 10 LTS from day one.** The starter now targets `net10.0` with SDK 10.0.100 (`rollForward: latestFeature`); SETUP-HOSTS builds the hosts on it.
