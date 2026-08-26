# Client design boards — audit of all eight documents

**Received 20 August.** Eight PDFs across four domains, together describing **156+ screens**. This
is the audit of every one against the package.

| Document | Pages | What it is | Screens |
|---|---:|---|---:|
| POS Frontline — Operations Professional | 45 | functional reference | **36** |
| POS Frontline — Dashboard Screens | 6 | rendered boards | 36 |
| F&B Backend Structure Module | 130 | functional reference | **60** |
| F&B Dashboard Screens | 6 | rendered boards | — |
| Retail Backend Structure Module | 202 | functional reference | **60** |
| Retail Dashboard Screens | 6 | rendered boards | — |
| Inventory & Procurement Dashboard | 7 | rendered boards | — |
| Inventory & Procurement Backend | — | **corrupt in the project copy** | — |

**Every domain follows the same shape: six boards, ten screens each, a command centre first and an
AI/analytics board last.** That is a deliberate architecture, not four documents that happen to
resemble each other.

---

## The finding, stated plainly

**The contracts already do this work. The screens do not.**

| Domain | Client screens | Package screens | Package operations |
|---|---:|---:|---:|
| POS & frontline | 36 | 10 | — |
| F&B | 60 | **0** | 50 |
| Retail | 60 | 3 | 35 |
| Inventory | ~10 | 2 | 44 |

**F&B is the sharpest case: 50 contracted operations and not one screen calls them.** `listMenus`,
`setRecipe`, `planProductionRun`, `setKitchenTicketStatus`, `openTableVisit`, `recordWaste`,
`joinRestaurantWaitlist` — all built, all reachable by no interface in this package.

**A sample of 15 F&B board screens against real operations: 11 fully backed, 2 partly, 2 not.** The
two misses were my probe using the wrong names — `updateKitchenTicket` is `setKitchenTicketStatus`,
`listTables` is `getTableMap`. **Course firing is the one genuine absence, and `KitchenTicket.coursing`
was added on 18 August precisely because starters before mains is the entire job of a kitchen pass.**

---

## What the boards give us that the matrix does not

**Structure.** The matrix is 3,184 requirement rows with no notion of what a person opens. The
boards are 24 boards of ten screens with a stated architecture: *Company → Venue → Department →
Workstation → Operator/Shift → Transaction → Exception → Reconciliation → Analytics.*

**That hierarchy is a design decision the matrix never made**, and it happens to match `scope_path`
— which is the thing 289 of 358 tables anchor on.

**Detail the matrix does not reach.** `1C Workstation Details` specifies six tabs, a health score, a
current-operator card with role and shift, an IP address, a configuration profile with version and
deployment date, and a today's-summary carrying transactions, refunds and cash collected. **The
matrix has requirements about workstation management. It does not say what a person looks at.**

**Answers to open conflicts.** `1D Hardware & Peripherals` names nine device kinds with status,
battery and last check. **CF-136 has been waiting on Dinesh for a device list since 12 August**, and
it arrived in a design document.

---

## Genuine functional gaps — six, not many

Everything else resolves. These do not:

**`5B` Offline policy configuration** and **`5D` Connectivity auto-switch.** ADR-0013 makes POS
local-first; nothing configures the policy or holds a threshold. **A device that flips offline on
one dropped packet and one that waits five minutes are different products.**

**Workstation health score.** `platform.device_heartbeat` exists and nothing computes a percentage.
**A number a manager can sort by is a different artefact from a timestamp.**

**Versioned configuration profiles with deployments.** `1F` shows 1,248 workstations across four
versions. We hold a version field and model no profile, no deployment.

**Peripheral battery and last-check.** Follows from CF-136 closing.

**Retail RFID and serialised stock.** Board 4 Page 9 — `Barcode, RFID, Serialized Stock &
Traceability`. `StockBatch` was added 18 August with lot numbers; **serialisation to the individual
item is a step beyond it**, and it is what a jewellery counter or a high-value electronics store
needs.

---

## What I would not do

**Adopt 156 screens.** The screens plan says design 40 across the whole estate — guest-facing, wave
1, or carrying money or a legal act. **156 in four domains is four times that budget on a fifth of
the platform.**

**Put Boards 1 and 6 in P04.** Workstation registry across 1,248 devices and enterprise analytics
are back-office. **A cashier does not open a fleet dashboard on a till.** They belong in P08, which
now has a home screen and eight sections to hang them from.

---

## The question that has to be asked first

**These documents contain functionality the matrix does not.** Before adopting them, Qossai has to
say **which document is the specification.**

If the boards win, **the matrix needs a revision rather than a reconciliation** — and the 3,184-row
traceability walk is measured against a document that is no longer the source.

If the matrix wins, **the boards are a design reference** and the extra functionality is out of
scope until it is added to the matrix.

**Either answer is workable. Not answering is the expensive option**, because every screen built
against the boards is a screen whose requirement cannot be cited at sign-off.

---

## Recommended order

**1 — Ask the scope question.** One line to Qossai. Everything below depends on it.

**2 — Close CF-136 with the peripheral list.** It is answered; it just has not been recorded.

**3 — Build the six functional gaps.** Small, and they are the only places the boards describe
something the platform cannot do.

**4 — Adopt the six-board structure for F&B, without building 60 screens.** F&B has 50 operations
and zero screens; the boards give a defensible shape for the ten or so that matter. **The command
centre and the KDS are the two a venue opens daily.**

**5 — Leave Retail and Inventory until F&B has proven the pattern.** Same architecture, same
approach, and doing them in parallel means making the same mistake three times.
