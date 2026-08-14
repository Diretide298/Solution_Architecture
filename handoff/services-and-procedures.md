# Services and stored procedures

**Where each operation gets its data, what service owns it, and the ten places a stored
procedure earns its keep.**

Companion to the **Data lineage** sheet in `TICVAI_Schema_Reference.xlsx`, which lists every
operation against the tables it reads and writes.

---

## The position on stored procedures, stated before the catalogue

You asked for tentative stored procedures. Here is the honest recommendation before the list,
because the list is short on purpose.

**Services for all 654 operations. Stored procedures for ten.**

A stored procedure per operation would be a second codebase in a second language with its own
deployment, its own review path and no type checking against the contracts. It also breaks two
things this platform has already committed to:

**Row-level security.** Every scoped read resolves through `platform.in_scope(scope_path)`
against a session variable the application sets. A procedure running as a definer role bypasses
that, and RLS with `FORCE` exists precisely so nothing bypasses it. A procedure would have to
run as invoker and set the session variable itself — at which point it is doing the
application's job in a worse place to test it.

**Forward-only migrations.** A procedure is schema. Changing one is a migration, and a hot-fix
to business logic then requires the same ceremony as adding a column.

**Where a procedure does earn its place** is a narrow, identifiable set: a multi-table write
that must be one transaction and is on a hot path, or a set-based operation where the round
trips cost more than the logic.

---

## Services — one per contract

Twenty-two services, mirroring the contract boundaries. **The contract is already the service
boundary**; inventing a different one would create two maps of the same territory.

### Spine

| Service | Operations | Owns |
|---|---|---|
| `TenancyService` | 18 | Scope tree, venues, workstations, devices, outlets |
| `IdentityService` | 38 | Principals, roles, grants, SSO, MFA, sessions |
| `CatalogueService` | 45 | Products, variants, envelopes, leases, entitlement templates |
| `OrderService` | 51 | Orders, lines, payments, refunds, holds, tips |
| `AccessService` | 19 | Validation, scans, access points, admission profiles |
| `LedgerService` | 46 | Journals, periods, FX, settlement, inter-entity |
| `ShiftService` | 13 | Open, suspend, close, variance, no-sale |
| `CrossCellService` | 16 | Redemption rights, guest links, wallet allocation |

### Satellite

`FnbService` 41 · `RetailService` 26 · `InventoryService` 39 · `SeatingService` 29 ·
`PromotionsService` 31 · `MarketingService` 49 · `MaintenanceService` 29 · `QueueService` 21 ·
`WhiteLabelService` 41 · `SubscriptionService` 34 · `PlatformOpsService` 24 ·
`ReportingService` 23 · `AssetsService` 10 · `GamesService` 13

### The rules that make this a boundary rather than a namespace

**A service owns its tables and no others.** `OrderService` writes `orders.*`. It does not
write `catalogue.inventory_lease` — it asks `CatalogueService` for a lease. That is the
difference between a service boundary and a folder.

**Cross-service writes go through the outbox.** `order.paid` is published; `CatalogueService`
consumes it and issues entitlements. `OrderService` never writes an entitlement itself, because
a service that writes another's tables is a distributed monolith with extra steps.

**Satellite services may call spine services. A satellite never calls another satellite.** The
same rule the contracts already follow, enforced at the service layer so it cannot quietly rot.

**Every service takes the scope from the request, never from a parameter.** The session variable
that drives RLS is set once per request, and a service that accepts a `venueId` it does not
verify is a service that can be asked for someone else's data.

---

## The ten stored procedures

Each is here for a stated reason, and each would be reviewed out if the reason stopped holding.

### 1. `orders.sp_capture_payment`

Writes `orders.payment`, `ledger.journal_entry` and `ledger.entry` in one transaction. Three
tables, two schemas, and a partial write leaves money captured with nothing posted.

**Why not a service transaction:** it can be, and on most paths it should. The procedure exists
because this runs at every till at closing time on a busy Saturday and the round trips are
measurable.

**Argument against:** the FX lookup and the tax calculation are business rules that will change,
and business rules in SQL age badly. **A defensible alternative is a service transaction with
the three inserts and no logic in the database at all** — this is the one on the list I would
most readily give up.

### 2. `orders.sp_post_refund`

Same shape in reverse, plus the reversal entry. A refund that posts to the ledger and not to
the entitlement leaves a guest holding a valid ticket for something they were paid back for.

### 3. `access.sp_validate_and_record`

The hot path. Reads `entitlement_template`, `admission_profile`, `blacklist` and
`access_point`, decides, and writes `scan_event` — with the entry count decremented under the
same lock that read it.

**This one earns it clearly.** Tens of thousands per day, and the read-decide-write must be
atomic or two gates admit the same single-entry ticket in the same second. Doing it in four
round trips from the application is both slower and racier.

### 4. `catalogue.sp_acquire_lease`

Allocates capacity to a terminal. Contended by definition — every POS asks for the same
envelope. A `SELECT … FOR UPDATE`, a check and an insert, and the whole point is that nothing
else runs between them.

### 5. `seating.sp_hold_seats`

Holds a set of seats or none. Partial seat holds are the worst outcome: a guest gets four of
six and neither the platform nor the guest knows what to do next. Set-based, atomic, and
returns which seats failed.

### 6. `orders.sp_close_shift`

Reads every payment, cash movement and no-sale for the shift, computes the expected figure,
compares against the blind count, and writes the shift and its journal. **Read-heavy and
set-based** — this is what SQL is for, and doing it in application code means pulling a shift's
worth of transactions across the wire to add them up.

### 7. `access.sp_sync_scan_batch`

Ingests an offline journal. Accepts what it can, rejects what it cannot, writes both, and
returns the split. Set-based over a batch, with per-row outcomes — a loop of single inserts
from the application would take minutes on a device that has been offline all day.

### 8. `inventory.sp_post_movement`

Stock movement plus its ledger consequence. Cost of sales, waste write-off and transfer all
post differently and all must be atomic with the movement.

### 9. `platform.sp_cascade_scope_path`

Already exists as a function. When a venue moves region, every denormalised `scope_path`
beneath it updates in the same transaction. **The riskiest thing in the schema** — if it is
wrong, RLS silently starts answering the wrong question — and recursive, which is exactly the
shape application code handles badly.

### 10. `pii.sp_erase_subject`

Already exists as a function. Erasure in one transaction across four tables. Written in the
database rather than the application because **a partial erasure reports success while leaving
an email address behind**, and nobody checks again.

---

## What is deliberately not a stored procedure

**Pricing and promotion evaluation.** The rules change monthly, they need testing against
fixtures, and they benefit from a type system. `evaluatePromotions` stays in the service layer
however tempting the join looks.

**Anything returning a projection to a screen.** `listOrders`, `getGuestProfile`,
`getSeatAvailability` — parameterised queries in the repository, cached where the routing says
replica.

**Reporting.** Report definitions are user-authored and run against the analytical replica.
Compiling them into procedures would mean a migration every time a manager saves a report.

---

## Data lineage — what the sheet shows

`TICVAI_Schema_Reference.xlsx`, sheet **Data lineage**: every operation, the tables it reads,
the tables it writes, its read routing, its scope level and whether it works offline.

| | |
|---|---|
| Operations with a resolved table | **336 of 654 (51%)** |
| Derived from persistence markers | 299 |
| Hand-mapped | 37 |
| Unresolved | 318 |

**The 318 are not a defect list.** Most return a projection — `OrderSummary`, `TicketStatus`,
`MediaEntitlements` — computed across tables rather than persisted, and a projection has no
marker because there is nothing to mark. Others are commands with no response body, health
checks, and the sync endpoints.

**What the resolved half is for:** before changing a table, the sheet says which operations
break. Before building an operation, it says which tables it needs and therefore which service
owns it. `orders.sales_order` is read by 23 operations across four services, and that number is
the argument for the outbox rather than direct writes.

**Where it is weakest:** an operation that reads a table only to check a permission or resolve
a scope does not show it. The lineage is what an operation *is about*, not every row it
touches, and RLS means every scoped read also touches `scope_node`.
