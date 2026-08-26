# F&B hi-fi board pack — audit against the package

**Received 20 August from Claude Design.** Six boards, 63 frames, 60 of 63 drawn. Installed to
`wireframes/`, alongside `POS Frontline Board 2` and the index.

Every frame carries four traceability lines — `OPERATIONS`, `STATES`, `ARRIVES WITH`, `GOES TO` —
which makes this the first board pack that can be checked rather than looked at. **That is what
this audit does.**

---

## The headline

**The boards declare 205 distinct operations across 63 F&B screens. The `fnb` contract has 50.**

31 of the 205 exist. **174 do not.**

That is not 174 defects. **It is a statement that the client's designers specified an API roughly
four times finer than the contracts**, and the honest response is to decide which grain is right
rather than to build 174 operations or dismiss them.

**Split by what the gap actually is:**

| | | |
|---|---:|---|
| **Capabilities** | **90** | Something the platform cannot do |
| **Reads** | **84** | A finer cut of data the platform already holds |

---

## The 84 reads are mostly a contract question, not a gap

`getKitchenLoad`, `getKitchenSla` and `listKitchenExceptions` are three reads a board draws as three
panels. **One `listKitchenTickets` with a filter and an aggregate serves all three**, and a contract
with an operation per panel is a contract that changes every time a panel moves.

**The same pattern runs through Board 6 entirely:** `getMarginBridge`, `getFoodCostBridge`,
`getCategoryMargin`, `getChannelContribution`, `getDaypartRevenue`, `getRevpash` — **twenty-plus
analytics reads that are one reporting operation with a dimension.** `runReport` and `getDashboard`
already exist and already take a definition.

**Recommendation: do not build these as operations.** Map each board panel to an existing read plus
its parameters, and record the mapping. **A board panel is not an endpoint.**

---

## The 90 capabilities are the real finding, and six clusters carry them

**Course firing — 6 of 6 missing.** `fireCourse`, `holdCourse`, `setCourseRules`, `refireItem`,
`recallKitchenTicket`, `chaseStation`. `KitchenTicket.coursing` carries the *policy*
(`holdAndFire`, `phased`, `timed`) and **nothing fires a held course.** Starters before mains is
the entire job of a kitchen pass.

**Table service — 10 of 10 missing.** `seatParty`, `mergeTables`, `moveTable`, `reassignTable`,
`reassignServer`, `splitCheck`, `printBill`, `compItem`, `voidOrderItem`, `transferOrderItems`.
The package has `openTableVisit`, `mergeTableVisits` and `transferTableVisit` — **a visit is not a
table.** Moving a party to a different table and merging two visits into one bill are different
acts, and the board draws both.

**Waitlist — 5 of 5 missing.** `joinRestaurantWaitlist` exists and **nothing quotes a wait,
notifies a party or calls them.** A waitlist a guest joins and never hears from is a queue with no
service.

**🔴 Food safety — 4 of 4 missing.** `logTemperature`, `logColdChain`, `getHaccpStatus`,
`signCorrectiveAction`. **This one is not a convenience.** HACCP records are a regulatory
obligation in the UAE, they are inspected, and **a venue that cannot produce a temperature log has
a compliance failure rather than a missing screen.** Nothing anywhere in 947 operations touches it.

**Stock counting — 5 of 5 missing.** `startStockCount` and `postStockCount` exist; **entering a
count line does not.** The count can be opened and posted and nothing records what was counted.

**Menu publishing — 5 of 5 missing.** `publishMenu`, `scheduleMenuPublish`, `rollbackMenu`.
`updateMenu` exists and **a menu edited is a menu live** — no draft, no schedule, no rollback. A
venue changing prices for next Monday has to do it on Monday.

---

## What I would do, in the order asked

**1 — ADRs and contracts.** Nothing in the boards contradicts an ADR. `fnb` is a satellite reading
down into the spine and every capability above lives inside that boundary. **No ADR needs
changing; ADR-0013 local-first covers the kitchen, and CF-115's three data classes cover the
counting.**

**2 — API.** Build the six capability clusters — roughly 35 operations, not 90, because the
clusters overlap and several boards name the same act twice. **Food safety first**: it is the only
one where the absence is a regulatory exposure rather than a feature gap.

**3 — Pages and tables.** `fnb.temperature_log`, `fnb.cold_chain_event`, `fnb.corrective_action`
are new. Table service needs `fnb.table` as a first-class row — the package models a *visit* and
infers the table. Counting needs `inventory.count_line`.

**4 — Workflows and journeys.** Three flows the boards make obvious and the package does not have:
**a course is fired and a table is served**, **a temperature excursion is caught and signed off**,
and **a count is entered, varied and posted.** Each crosses three or more screens and every flow
written so far has found a defect.

---

## Two things about the pack itself

**Three Board 2 frames are undrawn** — Substitution/Allergen/Nutrition, Production Planning,
Central Kitchen. The README says so, and they are the three where the client's own specification
was thinnest.

**The index links ten boards and seven are here.** Inventory Board 1, Retail Board 1 and TICVAI
Boards v2 are referenced and not present — **the index will 404 on three tiles** until they arrive.
