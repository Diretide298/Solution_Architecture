# Flow coverage — three passes, and what each one found

**24 August 2026.** 93 flows, 1,014 operations, **53% coverage — from 21% at the start of the day.**

---

## What the passes bought

| Pass | What | Flows | Coverage |
|---|---|---:|---|
| — | Before | 35 | 21% |
| **1** | Guest and staff journeys from the screens | +28 | **30%** |
| **2** | Chains from the client boards' own `GOES TO` edges | +20 | **46%** |
| **3** | Service-boundary and platform journeys | +12 | **53%** |

**The forecast was 39%, 46% and ~60%.** Two landed; the third fell short because the resource-CRUD
tail was not worth writing — see the ceiling below.

---

## The number is not the point, and here is the evidence

**Every pass found defects the contract audit had not.** A screen with too many operations
validates cleanly; only a journey notices.

**Pass 1 — 67 operations stripped across 19 screens.** A till could author the catalogue and cancel
a performance. A scanner could create access points and run a cash shift. A staff app could create
roles. `EMP-004`, `EMP-005` and `EMP-006` — list, detail and raise — carried **identical
nine-operation sets**, so a list screen could complete a task.

**Pass 1 also found two contract gaps.** **No case operation was guest-callable** — a guest could
raise nothing and read nothing — and `GST-034 Lost & Found` declared exactly one operation, which
was `getGuestOrderStatus`. **Order tracking on a lost-property screen.**

**Pass 2 found the module system working.** Five of 74 board chains collapse to one screen, and all
five are `BO-044`: the client drew nine F&B views and nine retail views of one outlet-configuration
surface. **That is the strongest evidence in the package that `requiresModule` is the right shape.**

**Pass 3 found the largest single defect of the three.** **121 operations stripped from the platform
console.** Eleven P09 screens carried the same nine subscription operations; nine carried the tenant
lifecycle. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants and
declared no quota operation at all** — the screen for the job could not do the job. `setApiQuota`
existed and nothing called it.

**And three older flows were depending on that defect**, which is the part worth sitting with: a
flow written against a bulk-attached screen validates, and it is wrong.

---

## Coverage per service

**This is the number to report, not the aggregate.** 53% across 1,014 operations says nothing;
the spread says where to look.

| Service | Operations | In a flow | Coverage |
|---|---:|---:|---|
| CrossCellService | 16 | 5 | 31% |
| ControlService | 102 | 40 | 39% |
| MarketingService | 96 | 39 | 41% |
| RetailService | 35 | 15 | 43% |
| CatalogueService | 132 | 57 | 43% |
| WhiteLabelService | 50 | 22 | 44% |
| OrderService | 77 | 35 | 45% |
| VenueOpsService | 102 | 48 | 47% |
| IdentityService | 44 | 21 | 48% |
| AccessService | 30 | 17 | 57% |
| AiService | 30 | 17 | 57% |
| LedgerService | 54 | 33 | 61% |
| ReportingService | 29 | 18 | 62% |
| TenancyService | 71 | 50 | 70% |
| FnbService | 96 | 70 | 73% |
| InventoryService | 50 | 48 | 96% |

**`InventoryService` at 96% and `CrossCellService` at 31%** — and the difference is not risk, it is
attention. Inventory was walked four times across three passes; cross-cell has one flow and it is
the only service that reaches another jurisdiction.

---

## Where the ceiling is, and why we stopped

**78 operations are alone on their path** — no second operation on the resource, nothing to walk to.
They will never be in a journey and that is correct.

**The theoretical ceiling is 92%. The practical one is lower.**

**49 of the 74 board chains were left unbuilt because they add 13 operations between them.** They
revisit screens already walked from another direction — 74 chains across 156 frames means most
frames appear in several, and once `BO-007` and `KIT-002` are walked a chain passing through them
again adds nothing.

**The resource-CRUD tail was not written.** 203 resources hold uncovered operations and the top 20
hold 194 of them — but a create-read-update-close walk over `/promotions` crosses nothing. **One
service, one screen, one state machine `check-states` already validates.** It would move the number
and find little.

**Build is 0%.** Sixty CRUD flows is roughly the effort of writing the DDL for 379 tables, and only
one of those two unblocks a build team.

---

## What to do with this

**Report coverage per service and put it beside the deploy order.** It is now a column in
`TICVAI_Services_and_Data_Segregation.xlsx`, banded — green above 60%, amber above 40%, red below.

**Treat a service under 40% as unwalked rather than under-documented.** `CrossCellService`,
`ControlService`, `MarketingService`, `RetailService` and `CatalogueService` are there, and
Catalogue is the largest service in the package.

**Write a flow when a boundary is crossed, not to move a percentage.**
