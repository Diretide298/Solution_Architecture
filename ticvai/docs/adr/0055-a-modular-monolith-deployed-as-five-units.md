# ADR-0055: A modular monolith, deployed as five units

**Status:** Accepted · 30 September 2026 · Chinmay Parab
**Date:** 2026-09-30 · **Deciders:** Chinmay Parab
**Finding:** SD-001 (high), with SD-002 and SD-006
**Amends:** ADR-0028 (service decomposition, amended by this ADR) — the module map stays; the deployment shape and the ownership rule change
**Related:** ADR-0020 (AI boundary) · ADR-0013 (local-first POS) · ADR-0038, amended by ADR-0040 (database per tenant) · ADR-0007 (repositories)

---

## Amended 25 October 2026: which hosts compose which modules' in-process queries

**Decided by Chinmay** (ADAM CR-167, option A, accepted 18 October 2026; CR-234 and CR-240, option A, settled 25
October 2026; change entries CHG-R10ORD-010, CHG-R10ORD-008 and CHG-R10ORD-009). The 21 October amendment below allows
a granted read across deployables in process. Three hosts now compose another module's query interfaces (the read
side only, `IModuleQueries`), each read in the caller's transaction under the caller's own connection, so row-level
security still scopes every row:

1. **`workers` composes every module's query interfaces.** It runs every module's event consumers (the table above)
   and DB-ROLES gives its role the schemas they touch, so a consumer's reads are in process wherever the owner sits:
   `access.issueOrderEntitlements`, the `order.paid` consumer, reads Orders and Catalogue in process, as
   `finance.postOrderRevenue` already did (CR-167). `tools/check-cross-module-reads.py` treats an operation with
   `x-ticvai-consumes` as running in workers (XR-ROUTE).
2. **`operations` composes Tenancy's venue and region settings queries** (`tenancy#venueSettingsRecords`,
   `tenancy#regionSettingsRecords`), as the workers host does: every F&B operation that answers Money reads the
   venue's frozen trading currency and its scale this way (naming-and-style 5.1, ADR-0018), mergeTableVisits first
   (CR-234). Granted read XDR-004 in `docs/active/cross-deployable-writes.yaml`.
3. **`access` composes Tenancy's workstation query and Catalogue's entitlement template query**
   (`tenancy#workstationRecords`, `catalogue#entitlementTemplateRecords`): getOfflinePackage reads the session's
   access point and each entitlement's re-entry and admission rules this way, and so does every Access operation
   that reads the template (CR-240). Granted read XDR-003. Pinning the template values onto `access.entitlement` at
   issue (CR-240 option C) is a later change.

Writes are unchanged: rule 3 and the cross-deployable write routes stand. A call into another host's write is still
an event (Queue's Fast Pass redemption writes `queueEntry.redeemed`, which Access consumes; CR-238) or the owner's
published operation.

---

## Amended 21 October 2026: a granted read across deployables is asked in process

**Decided by Chinmay, 21 October 2026** (ADAM CR-196, option B, as recommended; change entry CHG-R9CR-005). Orders'
`getMediaEntitlements` runs in `commerce` and answers from Access's `access.entitlement` and `access.scan_event`, which
`access` owns. Rule 4 sent that read over Access's service route, and serviceAuth between deployables inside a cell is
not built and has no ticket (CR-174); a call on it would also run at the tenant root (IDENTITY-C48), so a venue cashier
would see every venue's entitlements. The lead had already chosen in-process reads for the same kind of read in CR-167
(the `workers` host).

**Rule 4 gains one exception, by name.** Where the lead grants it, a deployable's role may SELECT a table another
deployable owns, and asks the owner's declared query **in process**: the owner serves the query `in-process` as well
as `service`, the asking host composes the owner's query interface (the read side only), and the read runs in the
asker's transaction under the caller's own connection, so the table's row-level security still scopes every row. It
is a read, never a write (rule 3 and the cross-deployable write routes stand). Each grant is an entry under `reads` in
`docs/active/cross-deployable-writes.yaml` (the first: XDR-001, `commerce` reads `access.entitlement` and
`access.scan_event` through `access#entitlementRecords` and `access#scanEventRecords`, for `getMediaEntitlements`);
`tools/derive-ddl.py` writes the guarded `GRANT SELECT` into the next forward migration, and
`tools/check-cross-module-reads.py` allows an in-process route across deployables only for a query so granted
(XR-ROUTE). The exception is removed when the service route is built, if the lead wants the deployables kept apart
(CR-196 option A).

---

## Amended 14 October 2026: a rule question is asked of the owner by a declared query

**Decided by Chinmay, 14 October 2026** (the settlement of ADAM CR-081, CR-083 and CR-084; change entry
CHG-GEN-009). Three refusals the developers raised that day were the same question: an operation must refuse when
another module's data says so (a board tile names a variant Catalogue does not sell; a workstation has a shift open in
Orders; a guest still holds a live entitlement in Access or an open order in Orders), and the only way the package
gave to know was to read the owner's tables raw, some across deployables, some not in the lineage at all. On 14
October the lineage held 941 cross-module table reads in 517 of 2,796 operations, and nothing checked rule 2 or rule 4
(the lineage check promised under "Enforcement" did not exist). **One pattern now answers every such question.**

**Rule 2 is refined, not reversed.**

1. **A rule question goes through a declared query.** The owner declares it in its contract, in a top-level
   `x-ticvai-queries:` map: `<queryName>: {module, inputs, returns, rule, served}`, where `rule` states the rule in
   words (what "sellable", "open" or "live" means), and `served` lists the routes it answers on. The asking operation
   names it: `x-ticvai-read-via: [{query: <contract>#<queryName>, route, for}]`, `for` saying which check or field it
   feeds. `tools/derive-lineage.py` copies it into the lineage as `readVia`, as `x-ticvai-write-via` became `writeVia`
   (CHG-R6-020).
2. **The route follows the deployables.** `in-process`: within one deployable, a C# interface in the application
   abstractions, implemented by the owner module and called in the caller's transaction (rule 2). `service`: across
   deployables, the owner's published serviceAuth operation (rule 4). `projection`: the asker keeps a local copy fed by
   the owner's events (ADR-0057), the only way Identity learns about a module above it (ADR-0028 tiers).
3. **Generated views are for bulk data reads within one deployable, never for rule questions.** DB-READ-VIEWS keeps
   its shape, `<table>_for_<reader module>` in the owner's schema, for reads of data an operation shows or exports.
   **Across deployables there is no view**: a view granted to another deployable's role is shared SQL, which rule 4
   forbids, so a reader in another deployable asks the owner's service or keeps a projection. Within a deployable all
   modules share one role (DB-ROLES), so the view is a boundary the architecture tests keep, not a grant.
4. **Identity reads nothing above it but a projection.** Tenancy shares the foundation tier but runs in `commerce`
   with Orders and Catalogue, and asks them in-process (CR-083: `configureWorkstation` asks Orders whether a shift is
   open, after locking the workstation row).

**Enforcement.** `tools/check-cross-module-reads.py` (in `run-checks.py`): every cross-module lineage read is the
module's own schema, a view named for the reader inside its deployable, or covered by a `readVia` to a query of the
owning module; every `readVia` names a declared query whose module owns its contract; `in-process` only within one
deployable; Identity reads above it only through a projection. The 941 reads already in the lineage are baselined and
leave the baseline as each is routed; the reads the r6 fixes route (sale-board tiles, workstation shifts, the guest
account deletion and export, the PIN step-ups) cannot be baselined. **ARCH-TESTS** (action item 6) allows a module's SQL
to name exactly one kind of object in another module's schema: a view named `<table>_for_<its own module>`.

**Shift is Orders'.** The deployable table below said "Tenancy (with Workforce, Approvals, Shift)". `shift` moved to
OrderService on 24 August (`handoff/service-decomposition.json`), and the lineage agrees: its rows are
`orders.pos_shift`, `orders.cash_movement`, `orders.deposit_box`. The table is corrected; ADR-0028 is corrected the
same day.

---

## Context

**The package describes 17 services. They all use one database per tenant.** ADR-0038 (amended by ADR-0040
on instance count) puts every schema of a tenant in one database. So every service talks to the same
database. A network boundary between them buys no data isolation.

**The ownership rule is not true today.**

- ADR-0028 line 50: *"no schema is written by two services"*.
- `docs/architecture/data-model.md:19`: *"Each service connects with a role granted access only to its own schema — enforced by Postgres grants"*.
- `handoff/api-data-lineage.json`: **35 tables are written by more than one service**, and there are **894 cross-schema reads in 493 of 2,608 operations**.
- The sale path writes across services (SD-002): `addCartLine` writes `catalogue.inventory_reservation`; nine operations write `access.entitlement`; `createPayment` writes `ledger.journal_entry`.

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
| `commerce` | Identity (with PII), Tenancy (with Workforce, Approvals), Catalogue, Order (with Payments and Shift; corrected 14 October 2026), Ledger, Wallet | 49.2% | The sale path. Order, payment and ledger can commit in one transaction. Autoscales on RPS |
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
   - **14 October 2026 (amendment above, CHG-GEN-009).** The test allows one kind of object in another module's
     schema: a view named `<table>_for_<this module>`. Anything else is a declared query through the owner's
     interface.
7. [ ] **DB-READ-VIEWS**: generate published read views for the 894 cross-schema reads from lineage (a deriver), applied in the migrations. (5 pts)
   - **14 October 2026 (amendment above, CHG-GEN-009; the grant question).** A view is generated only for a reader in
     the owner's deployable, for bulk data reads, never for a rule question (a lineage read covered by a `readVia` gets
     no view). **No view is granted to another deployable's role**: across deployables the reader asks the owner's
     service or keeps a projection (rule 4). The task text's "SELECT granted to the reader's deployable role" reads,
     after this, as the owner's own deployable role only. The ticket text is not rewritten (a started ticket is not,
     and the plan input waits for a plan change); the developer reads this line and
     `tools/check-cross-module-reads.py`, which reports a view read across deployables as XR-VIEW-ACROSS.
8. [ ] **DB-ROLES**: one Postgres role per deployable in MIG-BASELINE; AI read-only. (2 pts)
   - **12 October 2026 (ADAM CR-002, raised on DB-ROLES; Chinmay chose option A; CHG-R6-020).** The lineage still
     recorded writes into tables another deployable owns as the caller's own SQL, which these grants refuse. Rule 4
     now holds for every one: each names its route as `x-ticvai-write-via` on the operation (an event the owning
     module consumes, or the owner's published operation), copied into the lineage as `writeVia`. The kernel tables
     granted to every role directly are exactly `platform.outbox` INSERT, `platform.scope` SELECT,
     `platform.audit_record` INSERT and `platform.idempotency_record` SELECT/INSERT/UPDATE; a write that cannot
     route yet is a dated exception with a removal release. Both lists are `docs/active/cross-deployable-writes.yaml`;
     the readable table per write is `handoff/cross-deployable-writes.md`; `tools/check-cross-deployable-writes.py`
     fails on a write with neither.
   - **21 October 2026 (ADAM CR-196, option B; CHG-R9CR-005; the amendment at the top).** Beyond its own schemas and
     the kernel, a deployable's role is granted SELECT on a table another deployable owns only where the lead decided
     a read (`reads` in `docs/active/cross-deployable-writes.yaml`). The first is XDR-001: `commerce` SELECT on
     `access.entitlement` and `access.scan_event`, for Orders' `getMediaEntitlements`. A database already built gets
     the grant from the forward migration (guarded on the role and the table); the ticket text is not rewritten, and
     the developer reads this line.
9. [x] The runtime: the starter targeted .NET 8 (`global.json`, `Directory.Build.props`), and Microsoft's support for .NET 8 ends on 10 November 2026, inside Block A. **Decided 30 September: .NET 10 LTS from day one.** The starter now targets `net10.0` with SDK 10.0.100 (`rollForward: latestFeature`); SETUP-HOSTS builds the hosts on it.
