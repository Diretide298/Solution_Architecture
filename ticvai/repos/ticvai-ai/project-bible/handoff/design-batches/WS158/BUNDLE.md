# WS158 — Resource Management Configuration board 4

**10 screens · 15 operations · 18 schemas · 5 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
true. **None of it is the subject.** The subject is the person in front of the screen and the one
thing they came to do.

## What to build

**A working surface, not a drawing of one.** Two references, both built from these same sources:

- `sources/designs/TICVAI_Mobile.dc.html` — 54 screens in one navigable file, 133 animations,
  a live seat map, a five-stage payment flow. **This is the bar for finish.**
- `sources/designs/TICVAI_POS_Terminal_client_approved.html` — the client-approved POS build. **This is the bar for operator density.**

`sources/designs/ticvai-motion-and-interaction.md` names every mechanism in them. Open them and
match their depth. Do not describe them, read them.

## The one rule that outranks the rest

**Nothing in this bundle may appear as text a user can read.** Not an operation id, not a schema
field name, not a permission key, not a screen id, not a file path, not a finding reference.

A homepage that prints `getTenantAppStatus → listProducts` under its header, or labels a column
`venueId · scopePath`, has published its own homework. It happened on `WEB-001`: four products on
sale and not a single price on the page, because the build rendered what `listProducts` returns
instead of what a guest wants — a photo, a name, a price, and a way to book.

**The test: would the person this screen is for understand every word on it?** If a line would
confuse them, it is spec leakage, not design. `bindsTo` tells you what data to invent
convincingly. It is never a caption.

## What is in this folder

| file | what it is |
|---|---|
| `BUNDLE.md` | **The one file to hand a design session.** This brief; then **Screen by screen**, a full specification of each screen (what the user enters and picks, what it shows and produces, every state, who may do what, the requirements it meets, what the client said about it in the meetings, the tracker items, what the tenant configures, the references and an acceptance checklist); then what applies to the whole batch; then the raw data. |
| `screens.json` | Every field of every screen in the batch, as the package holds it. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ATTENDANCE_RECORD, REPORT_MANAGE, REPORT_VIEW_VENUE, WORKFORCE_MANAGE, WORKFORCE_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.

## The processes these screens belong to

Written by the owner of each process (`handoff/design-notes/`). Read before any screen: it says how the process runs end to end and which words the screens must use.

### Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue)

Venue operations is everything that happens after a sale and inside the gates. A guest's ticket is one virtual ticket with interchangeable media (QR, dynamic QR, RFID wristband, NFC, Face Pass or Face Tag); at an access point a scanner (P07, or the scan function inside the Staff App P06) validates the media against the admission profile and the guest admission policy, offline if it must, and every deny carries a reason and a next action. The back office (Venue Management P08) configures that estate: the venue topology (venue, park, zone, attraction, access point, gate and lane, device placement), admission profiles and rules (entry, exit, re-entry, anti-passback, validity, crossover, companions), credential security (dynamic QR, device binding, beacons), biometrics, gate modes, and the live operations, fraud and monitoring views. Accreditation (P08 setup and review, P11 web portal for applicants, web first) takes an applicant from a configurable form through document checks, OCR, duplicate blocking and multi-level approval to a credential with zone rights. Resources and capacity manage bookable resources (rooms, vehicles, equipment, cabanas, instructors) that are booked as a consequence of selling a product, never sold directly. Workforce covers shift templates, rosters, attendance, swaps and breaks, mirrored on the Staff App. Maintenance and safety cover the asset register, preventive calendars, work orders with scored priority, inspections and incidents, with technicians working from the Staff App. Games and rides configure readers, credit types and consumption priority, play entitlements, game pricing, retry pricing, redemption and the card lifecycle. The virtual queue (Q1) gives a guest a live wait time and a return window for a ride; it is not the on-sale waiting room (Q2). Every calendar has day, week and month views. Configuration resolves tenant, region, venue (outlet only for F&B and retail), and a user's permissions, never the device, decide what they may do. The guest apps (P01, P02) show the guest's side of this: My Tickets, the scan code, Face Pass, wait times, the virtual queue, map booking of cabanas and the visit planner.
*(source: F06 step 1 / F112 step 1 / F111 step 1 / ADR-0002 / ADR-0012 / ADR-0018 / ADR-0041 / ADR-0066 / ADR-0067 / ADR-0068 / DI-652 / DI-627 / DI-640 / DI-654 / DI-666 / DI-482 / DI-483 / DI-907 / DI-919 / DI-923 / DI-865 / DI-678 / TRACKER Actions row 160 / MoM 2026-09-02 AccessControl / MoM 2026-09-07 …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Ticket | The one virtual record a guest owns (ticket number, product, validity, entries). Its number never changes, whatever media carries it or whoever it is transferred or resold to. | Pass (unless the product is a pass), Booking, Order line | DI-652 / DI-620 / contracts/spine/access.yaml#/components/schemas/TicketStatus |
| Media | What the ticket is presented by at a gate (QR code, dynamic QR, wristband/RFID card, NFC, Face Pass, Face Tag). One ticket can carry several media as fallbacks; a media code can also cover several tickets scanned as one group. Show one … | Credential (for guest media; keep Credential for accreditation badges and staff), Ticket code | DI-180 / DI-608 / DI-652 |
| Access point | A place where a scan is judged, with a fixed direction (entry, exit, re-entry, crossover). Hierarchy shown to users is Venue > Park > Zone > Attraction > Access point > Gate/lane > Device. | Scanner (that is the device), Door | screens/P08-venue-back-office.yaml#BO-144 / … |
| Admission profile | The named set of rules an access point enforces (opening window, entries, exit scan, re-entry, validity, crossover). Products point at a profile; tiers such as Bronze/Silver/Gold are profiles with gate allow and deny lists. | Admission rules (as a screen title), Access rule set | DI-185 / contracts/spine/access.yaml#/components/schemas/AdmissionRules |
| Admitted / Denied / Overridden | The three scan outcomes. A denial is always shown with its reason in plain words and a next action; an override is a supervisor admitting despite a denial, and is always attributed and reasoned. | Valid/Invalid, Success/Fail, Error | contracts/spine/access.yaml#/components/schemas/ScanOutcome / … |
| Used | A ticket entry is used the moment a scan succeeds, whether or not the guest physically passed. Mistakes are resolved from the scan history, not by un-scanning. | Redeemed (for admission), Checked in (that is group check-in, a different step) | DI-627 / TRACKER Actions row 221 / TRACKER Actions row 189 |
| Gate mode | What a lane is doing now, set live by the podium or supervisor - Normal, Free flow (counts, does not validate), Drop arm (everybody through, evacuation), Closed (nobody through), Podium (staff validating by eye), Maintenance. Direction is … | Turnstile mode (as a label for direction), Open/Locked | contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode / R221 |
| Offline package | What a scanner holds to validate with no network - entitlements, blacklist, admission profiles and the active guest admission policy version - with its age always visible. | Cache, Local DB | F06 step 3 / ADR-0068 |
| Sync and reconciliation | Sending the offline scan journal to the server, and the duty manager's review of scans the server rejected after the device had already admitted the guest. | Upload, Retry | F06 step 6 / DI-065 |
| Face Pass / Face Tag | Face Pass is the long-lived face credential for members and season-pass holders (renewable); Face Tag is short-lived, for one day or event. Retention is set per tier by the venue. | Face ID, Biometric login | DI-640 / ADR-0063 |
| Accreditation / Credential (accreditation) | Accreditation is the application and approval of a person (media, contractor, corporate, staff of a partner) for an event or season; the credential is what is issued after approval (photo badge, QR or RFID) with zone access rights. | Registration (for the whole process), Ticket | DI-654 / DI-662 |
| Resource | A bookable thing or person a product needs (room, vehicle, cabana, equipment set, instructor). Guests buy products; resources are assigned to the booking, pre-assigned or dynamically. | Asset (that is maintenance), Inventory (that is stock) | DI-475 / DI-482 / TRACKER Actions row 160 |
| Asset | A physical item maintained by the venue (ride, turnstile, printer, pump) with a register record, documents, warranty and maintenance history. | Resource, Device (unless it is an IT device in the device register) | DI-910 / ADR-0067 |
| Work order | A unit of maintenance work, lifecycle Created > Assigned > In progress > Review > Closed, with a resolution timer. | Ticket (reserved for guest tickets), Job card | DI-231 |
| Game / attraction (games module) | In the games and rides module an attraction is an individual game or ride (roller coaster, racing game, bumper cars), not a venue. | Venue, Park | DI-863 |
| Virtual queue / Return window | A guest's place in a ride's queue held without standing in line, with a return window (for example 4:50 to 5:00 PM) that recalculates live. Distinct from the walk-in line and the VIP/express lane, and from the on-sale waiting room. | Waiting room, Fast pass (that is the express product), Booking | DI-675 / DI-678 / DI-679 / ADR-0066 |
| Wait time source | Where a ride's wait time comes from - Sensor, Throughput, Manual, or Unavailable - always shown beside the number. | Live (when the source is manual) | contracts/satellite/queue.yaml#/components/schemas/WaitTimeSource / DI-315 |

### Finance, Ledger & Tax · Reporting & Analytics

Finance and insights run underneath every sale. A sale at a till (P04), kiosk, web storefront (P01) or guest app (P02) is priced and taxed per line at the moment of sale, recorded in the venue's base currency (AED in the UAE; 2 decimals, or 3 for BHD, KWD and OMR, never rounded away), and posted to an append-only dual ledger through account mappings per money event; anything unmapped lands in suspense. Tax follows the jurisdiction's tax profile: inclusive or exclusive, compound where a tax applies on another, zero-rated or exempt with verified evidence, and computed on the discounted price by default or on the price before discount where the region requires it (Egypt). A guest may select a currency the venue charges and pay in it: the rate is locked on the order, the payment partner is asked in that currency, the ledger keeps the base amount with the rate, and a refund goes back in the currency paid (decided 2 October 2026, Chinmay); a currency shown but not charged is an approximate price. Foreign cash at a till is recorded at its base equivalent and change is given in base currency. A paid order can carry a VAT receipt (simplified tax invoice), a full tax invoice with the buyer's TRN, or a consolidated invoice for a company, each numbered without gaps and never edited; corrections are credit memos. Revenue is recognised by rule: POS-style immediate, tickets on the visit, gift cards and wallet on use, annual passes straight-line or per visit, breakage on expiry; deferred revenue is a balance that ages. Each venue's day is reconciled (POS cash, gateways, bank, wallet against the ledger, provider files matched automatically, only genuine mismatches to a person); chargebacks are defended against the bank's deadline; month end runs seven close checks and goes to a finance approver. Nothing posted is deleted: a correction is a reversal, an approver is never the preparer, and ledger approval needs a second factor. Back-office finance lives in Venue Management (P08: chart of accounts, mapping, FX, journals, recognition, reconciliation, period close, chargebacks); tax profiles, calculation validation and platform reconciliation in the TICVAI Console (P09); partner settlement in P10. Reporting is one consolidated, permission-based area (Analytics, P16): seeded standard dashboards and reports plus no-code builders over a governed business catalogue; the P08 report screens, the POS terminal day view and the kitchen performance view are scoped windows onto the same definitions and must show the same numbers. Every figure is read from a lag-tolerant reporting copy and shows its "as of" time; scope comes from the person's rights, never from a filter; AI explains and recommends but never acts, answers only within the person's role, labels forecasts, and is phase two for finance ledgers.

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Base currency | The venue's region currency; the currency every record and ledger posting is in. A guest may pay in a currency they select (where the venue charges it); the books still hold the base amount and the rate. | Home currency, Local price, Default currency | DI-211 / DI-282 / contracts/spine/orders.yaml#/components/schemas/Order |
| Pay in USD (a currency the venue charges) | The guest's selected payment currency; the card is charged in it at the rate locked on the order, and refunds go back in it. | Converted price, Approx. (for a charged currency) | contracts/spine/orders.yaml#checkoutCart / … |
| ≈ (approx.) price in USD / SAR / … | A conversion of a base-currency price for a currency the venue shows but does not charge, always next to the base price. | Converted price, USD price | DI-211 / screens/P02-guest-mobile-app.yaml#GST-044 |
| Takings | Money received in the period less refunds (cash-basis); the seeded KPI on hubs. | Revenue, Sales, Income | contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi / R283 |
| Gross sales | Issued sales before discounts and refunds; whether tax is included must be stated on the tile. | Revenue, Turnover | MATRIX 6.1.78 |
| Net revenue | Gross sales less discounts less refunds, adjusted per finance policy. | Net sales, Revenue, Income | MATRIX 6.1.78 |
| Recognised revenue / Deferred revenue | Earned under the recognition rules / paid for but not yet earned. Kept distinct from sales. | Realised revenue, Unearned income, Wallet revenue | MATRIX 5.12.6 / DI-260 / contracts/spine/finance.yaml#getDeferredRevenue |
| VAT receipt | The simplified tax invoice issued on a paid order. | Receipt (when it is a tax document), Bill | contracts/spine/finance.yaml#issueTaxInvoice |
| Tax invoice / Combined tax invoice | A full invoice with the buyer's details / one invoice for several paid orders of one buyer. | Bill, Statement | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoiceType |
| Credit memo | The document that corrects an issued invoice after a refund; the invoice itself is never edited. | Credit note (until the client's tax adviser chooses "Tax credit note"), Edit invoice | contracts/spine/finance.yaml#/components/schemas/FinTaxInvoice |
| VAT (or the jurisdiction's tax name) | Use the tax profile's own name on every surface; "Tax" only where several kinds are summed. | GST in UAE, Service charge for a tax | contracts/spine/catalogue.yaml#setTaxProfileJurisdiction |
| Price before discount | The taxable base where the jurisdiction taxes the undiscounted price. | Gross price, List tax | DI-598 |
| Post / Reverse | A journal reaches the ledger when approved and posted; a correction is a reversal, never an edit or delete. | Edit entry, Delete entry, Undo | contracts/spine/finance.yaml#reverseJournalEntry |
| Period (Open / Closing / Closed) | A fiscal period's state; closing stops postings, closed locks them. | Month locked, Frozen | contracts/spine/finance.yaml#/components/schemas/PeriodStatus |
| Variance (Over / Short) | The difference between expected and counted or recorded, always saying between which two figures. | Discrepancy, Error, Loss | DI-275 / contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation |
| Settlement / Exception / Resolve | A provider's file for a day / a line that did not match / the recorded explanation. | Payout file, Error, Close | contracts/spine/finance.yaml#/components/schemas/SettlementException |
| Chargeback | A bank-initiated reversal with an evidence deadline; not a refund. | Dispute refund, Reversal | contracts/spine/orders.yaml#/components/schemas/Chargeback |
| Report / Dashboard / Tile / KPI | A runnable, exportable, schedulable definition / a page of tiles / one visual bound to a report / a company-wide measure defined once. | Widget (outside the builder's library), Board (for a user-facing dashboard) | contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / … |
| Warning / Critical | KPI status bands set by a target's amber and red thresholds; always words plus colour. | Amber, Red (alone), Bad | contracts/satellite/reporting.yaml#/components/schemas/KpiTarget |
| As of HH:MM / Updated N sec ago | The freshness of every figure read from the reporting copy; stale shows a warning. | Live (unless refreshed), Real-time | MATRIX 8.7.22 |
| Forecast | Any projected figure, with its range; never shown as a fact. | Expected, Will be | DI-973 |
| Outlet / Workstation (till) | A sales point / the device; staff copy may say "till" for the workstation. | Store, POS (in copy), Drawer (for the device) | R156 |
| Channel | POS, Web, App, Kiosk, B2B, OTA, from one closed list. | Source, Platform | MoM 2026-08-18 4.2 Recipes, Operating Hours & Service Channels / MATRIX 1.4.7 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-883` | Workforce Roster Command Center | D | 0 | 0 | 6 | 10 | 1 | 0 | — | notStarted (—) |
| `BO-884` | Attraction & Operational Staffing Roster | D | 0 | 77 | 6 | 11 | 1 | 0 | — | notStarted (—) |
| `BO-885` | Minimum Staffing & Coverage Rule Configuration | D | 5 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-886` | Staffing Gap & Coverage Control Center | D | 4 | 22 | 6 | 1 | 2 | 0 | — | notStarted (—) |
| `BO-887` | Shift Marketplace & Workforce Requests | B–D | 0 | 8 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-888` | Attendance & Live Workforce Command Center | D | 0 | 22 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-889` | Staff Check-In, Check-Out & Attendance Exceptions | D | 19 | 5 | 6 | 4 | 1 | 0 | — | notStarted (—) |
| `BO-890` | Workforce Compliance Validation Center | D | 0 | 12 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-891` | Labor Cost & Staffing Budget Control | D | 10 | 17 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-892` | AI Workforce Planner & Roster Optimization | D | 4 | 15 | 6 | 1 | 1 | 1 | — | notStarted (—) |

## Thin screens in this batch

**BO-883, BO-887, BO-888, BO-890 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-883` Workforce Roster Command Center

**Provide managers with the primary operational workspace for viewing and managing workforce deployment across venues, attractions, events, departments, and shifts.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-883 |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/workforce-roster-command-center-bo-883` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The workforce roster command centre: the manager's landing page for board 4 - who is scheduled, on shift, checked in, absent or late now, where operations are understaffed, overtime and compliance risk, and today's staffing cost - above the roster timeline, with tiles into the board's detail screens. The one thing to get right: KPIs are metric tiles (per VO-R02) and the roster below is the shared rota calendar (Day, Week, Month, pivotable by venue, attraction, event, department, employee, role), not a blank data table.

**Known correction pending (do not draw the wrong version)**

- **The screen is a single dataTable with no label and no columns** Why: A command centre is KPI tiles, alerts and board tiles (VO-R02), and the pack lists twelve KPIs and a roster timeline. *(source: screens/P08-venue-back-office.yaml#BO-883; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **No calendar; the pack asks for Day, Week and Month roster views** Why: Every roster is a calendar (VO-R01). *(source: screens/P08-venue-back-office.yaml#BO-883; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation lists BO-884 to BO-892 but only BO-884 to BO-888 have triggers** Why: BO-889 to BO-892 are reached from here too and need their tiles and triggers. *(source: screens/P08-venue-back-office.yaml#BO-883; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How is a roster published (no publish operation; status changes one assignment at a time through updateRotaAssignment)?** → Drawn default accepted: Draw "Publish roster" for the date range with the compliance gate; mark the bulk write as pending. *(decided by Chinmay, 2026-10-02; DEC-500 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `listRotaAssignments` ?from |
| To | date picker | — | — | `listRotaAssignments` ?to |
| Principal | picker: choose a principal | — | — | `listRotaAssignments` ?principalId |
| Department | picker: choose a department | — | — | `listRotaAssignments` ?departmentId |
| From | date picker | — | — | `getStaffingCoverage` ?from |
| To | date picker | — | — | `getStaffingCoverage` ?to |
| Basis | segmented control | Minimum | Minimum · Forecast requirement · Higher of both | `getStaffingCoverage` ?basis |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Date range and view**: Day (default today, hours from the venue day start), Week, Month; pivot chips Venue / Attraction / Event / Department / Employee / Role. *(source: screens/P08-venue-back-office.yaml#BO-883)*
- **Coverage basis**: "Measure against" Minimum / Forecast / Higher of both (default Minimum); each coverage figure says which it used. *(source: contracts/satellite/workforce.yaml#getStaffingCoverage)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Total scheduled, On shift now, Checked in, Absent / no-show, Late arrivals, On leave, Open shifts, Unfilled positions, Understaffed operations, Overtime risk (hours), Compliance warnings, Staffing cost today (AED, with overtime share), AI staffing recommendations (count). Each with a delta against the same day last week and a tap into its detail screen. *(source: screens/P08-venue-back-office.yaml#BO-883 / DI-488)*
- **Coverage overview**: Per operation (Aqua Park Zone A, Wave Rider, Main Plaza gates) a severity pill (Covered, Tight, Short, Blocking) with "2 short at 14:00". *(source: screens/P08-venue-back-office.yaml#BO-883 / contracts/satellite/workforce.yaml#getStaffingCoverage)*
- **Roster timeline**: Person rows with assignment and break blocks ("08:00-10:00 Group lesson", "10:00-10:30 Break") and the smart status per person: Scheduled, Checked in, Working, On break, Available, Late, Absent, No-show, Overtime, Checked out. *(source: screens/P08-venue-back-office.yaml#BO-883 / screens/P08-venue-back-office.yaml#BO-884)*
- **Board tiles**: Attraction roster (BO-884), Minimum staffing rules (BO-885), Staffing gaps (BO-886), Shift marketplace (BO-887), Live attendance (BO-888), Exceptions (BO-889), Compliance (BO-890), Labour cost (BO-891), AI planner (BO-892). *(source: screens/P08-venue-back-office.yaml#BO-883)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Quick actions on a roster block**: Assign employee, Move assignment, Replace employee, Open shift (release to the marketplace), Notify employee; each opens a sheet and refuses overlaps or missing roles with the reason. *(source: screens/P08-venue-back-office.yaml#BO-884 / contracts/satellite/workforce.yaml#createRotaAssignment / contracts/satellite/workforce.yaml#updateRotaAssignment)*
- **Publish roster**: Runs the pre-publish compliance check first; blocking findings stop publication unless an authorised override is recorded; confirm names how many people will be notified. *(source: screens/P08-venue-back-office.yaml#BO-890 / screens/P08-venue-back-office.yaml#BO-891)*
- **Run AI optimisation**: Opens BO-892 with the same date range. *(source: screens/P08-venue-back-office.yaml#BO-884)*

**Data it reads**: `listRotaAssignments` (onLoad, The roster); `getStaffingCoverage` (onLoad, Where it is short)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-884` Attraction & Operational Staffing Roster: *Attraction & Operational Staffing Roster*
- → `BO-885` Minimum Staffing & Coverage Rule Configuration: *Minimum Staffing & Coverage Rule Configuration*
- → `BO-886` Staffing Gap & Coverage Control Center: *Staffing Gap & Coverage Control Center*
- → `BO-887` Shift Marketplace & Workforce Requests: *Shift Marketplace & Workforce Requests*
- → `BO-888` Attendance & Live Workforce Command Center: *Attendance & Live Workforce Command Center*
- → `BO-889` Staff Check-In, Check-Out & Attendance Exceptions: *Staff Check-In, Check-Out & Attendance Exceptions*
- → `BO-890` Workforce Compliance Validation Center: *Workforce Compliance Validation Center*
- → `BO-891` Labor Cost & Staffing Budget Control: *Labor Cost & Staffing Budget Control*
- → `BO-892` AI Workforce Planner & Roster Optimization: *AI Workforce Planner & Roster Optimization*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workforce roster list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workforce roster untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workforce roster yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workforce roster are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Forecast basis chosen for a period with no forecast handed over**: Rows fall back to the minimum and say "No forecast for this period - measured against minimum". *(source: contracts/satellite/workforce.yaml#/components/schemas/StaffingCoverage)*
- **Manager scoped to some venues only**: Tiles count only permitted venues; the venue chip says "2 of 3 venues". *(source: screens/P08-venue-back-office.yaml#BO-884)*

#### Consistency with other screens

- Match `BO-055`: The roster timeline here is the BO-055 rota calendar (same component, statuses and flags); draw once (per VO-R14).
- Match `BO-888`: Checked in, late and absent counts are the same numbers as the live attendance centre.
- Match `EMP-021`: The supervisor's phone roster is the mobile view of this timeline.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  scheduled: 126 (+8.5%)
  checkedIn: '98'
  onShift: '82'
  absentNoShow: '12'
  late: '6'
  openShifts: '9'
  understaffed: 2 operations
  overtimeRisk: 22 h
  compliance: 7 warnings
  costToday: AED 38,450 (overtime AED 6,850)
  aiRecommendations: '4'
coverage:
- operation: Aqua Park - Zone A lifeguards
  status: Short
  detail: 1 short 15:00-18:00
- operation: Summit Peaks - Ski School
  status: Tight
  detail: 90% 10:00-14:00
- operation: Main Plaza gates
  status: Covered
  detail: 100%
```

#### Permissions

- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `getStaffingCoverage` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 8.2.49 | System shall generate staffing shortage alerts. | Unified Operations Dashboard | CONTRACTED | `getStaffingCoverage` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staffing dashboard shows checked-in, on-shift, on-leave, open-shift and closed-shift counts from check-in/out logs, plus staffing cost including overtime. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-488)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-883` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-883`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 1: Opens Workforce Roster Command Center → Provide managers with the primary operational workspace for viewing and managing workforce deployment across venues, attractions, events, departments, and shifts.
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F267 branch at step 1 (expected): when Nothing has been set up on Workforce Roster Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F267 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-883?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-884`, `BO-885`, `BO-886`, `BO-887`, `BO-888`, `BO-889`, `BO-890`, `BO-891`, `BO-892`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-884` Attraction & Operational Staffing Roster

**Create detailed staffing plans for individual attractions, experiences, venues, departments, and events.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-884 |
| Who uses it | venue staff holding `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each candidate shall show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/attraction-operational-staffing-roster-bo-884` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Contract gap recorded 2 October 2026 (CHG-WIR-004): No read returns candidates for a rota position (skill, availability, suitability).

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The staffing roster for one attraction, experience, event or department on one date and operating period: the required roles against who is scheduled and who has checked in, the gap per role, and candidate cards to fill it by hand, drag and drop or smart assign. The one thing to get right: the required / scheduled / checked-in / gap table per role is the screen; candidates are the side panel that fills the gaps, and demand (tickets sold for each session) is visible beside the requirement it drives.

**Known correction pending (do not draw the wrong version)**

- **The table "Every attraction operational staffing" has candidate-card columns (Name, Photograph, Skill level, AI suitability score)** Why: The main table is the role requirement table; candidate fields belong on the cards. *(source: screens/P08-venue-back-office.yaml#BO-884; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"AI suitability score" as a label** Why: Skill matching was agreed as attribute matching, not a model; show "Match" with its reasons. *(source: contracts/satellite/resources.yaml#suggestResources; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Only createRotaAssignment is bound; nothing reads the roster, the coverage or the candidates (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where does ticket demand per session come from (tickets sold to staff required)?** → Drawn default accepted: Show the demand line from the forecast requirement where present; otherwise "Demand not linked". *(decided by Chinmay, 2026-10-02; DEC-501 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `listRotaAssignments` ?from |
| To | date picker | — | — | `listRotaAssignments` ?to |
| Principal | picker: choose a principal | — | — | `listRotaAssignments` ?principalId |
| Department | picker: choose a department | — | — | `listRotaAssignments` ?departmentId |
| From | date picker | — | — | `getStaffingCoverage` ?from |
| To | date picker | — | — | `getStaffingCoverage` ?to |
| Basis | segmented control | Minimum | Minimum · Forecast requirement · Higher of both | `getStaffingCoverage` ?basis |
| Date | date picker | — | — | `listAttendance` ?date |
| Principal | picker: choose a principal | — | — | `listAttendance` ?principalId |
| Exceptions only | toggle | — | — | `listAttendance` ?exceptionsOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scope**: Date, venue, attraction or experience or event, department, operating period (e.g. 10:00-18:00); pickers, not ids. *(source: screens/P08-venue-back-office.yaml#BO-884)*
- **Assign**: Drag a candidate onto a role row or slot, or choose "Smart assign" for a ranked list; the assignment is a rota assignment (person, position code, start, end, break minutes). Position codes come from the minimum-staffing rules so coverage counts them. *(source: contracts/satellite/workforce.yaml#createRotaAssignment / contracts/satellite/workforce.yaml#/components/schemas/RotaAssignment)*

#### Outputs: what the screen shows and produces

**Shown**

**Every attraction operational staffing** (data table)

| Shows | Format | Notes |
|---|---|---|
| Name | text | not in the schema: `Name` |
| Photograph | text | not in the schema: `Photograph` |
| Role | text | not in the schema: `Role` |
| Skill level | text | not in the schema: `Skill level` |
| Certifications | text | not in the schema: `Certifications` |
| Availability | text | not in the schema: `Availability` |
| Current hours | text | not in the schema: `Current hours` |
| Venue | text | not in the schema: `Venue` |
| Overtime impact | text | not in the schema: `Overtime impact` |
| AI suitability score | text | not in the schema: `AI suitability score` |

**Roster** (data table, from `listRotaAssignments`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Overtime minutes | 1,234 | BL-044, 1.2.83. UAE labour law limits working hours and mandates rest periods, and nothing in the package counted either. |
| Rest period before | 1,234 | Minutes since the previous shift ended. The check that stops a closing shift followed by an opening one, which is legal in most places and … |
| Breaches working hour limit | yes / no (icon or chip) | Flagged at assignment, not discovered at payroll. A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a … |
| Labour cost | AED 1,234.50 | Cost at the point of scheduling. A manager building a rota without seeing its cost is a manager who finds out from finance. |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Display name | text | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Position | text | What they are rostered to do — gate steward, cashier, lifeguard, technician. Most positions never touch a till, which is why a rota … |
| Required role | the name it points at, never the id | Checked on assignment. A rota naming someone unqualified is a rota that gets overridden. |
| Workstation | the name it points at, never the id | Where the position needs a till. The link between a rota and a cash session, without merging the two. |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Planned, Published, Confirmed, Swap pending, Cancelled, Completed… | — |
| Break minutes | 1,234 | — |
| Note | text | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Coverage** (data table, from `getStaffingCoverage`)

| Shows | Format | Notes |
|---|---|---|
| Date | 1 Oct 2026 | — |
| Venue | the name it points at, never the id | — |
| Position code | text | — |
| Label | text | — |
| From | text | — |
| To | text | — |
| Required | 1,234 | — |
| Rostered | 1,234 | — |
| Qualified | 1,234 | A position filled by somebody not qualified for it is still a gap. |
| Gap | 1,234 | — |
| Severity | chip: Covered, Tight, Short, Blocking | — |
| Open shifts | list or chips (count when long) | — |
| Basis applied | chip: Minimum, Forecast requirement | Which figure `required` is for this row. With `higherOfBoth`, the larger; with `forecastRequirement` and no handed-over requirement for the … |
| Minimum required | 1,234 | The configured minimum for the position and window. |
| Forecast required | 1,234.5 | The forecast staff requirement (p50) for the position and window, from `workforce.forecast_requirement`. |
| Forecast required P90 | 1,234.5 | The busy-case requirement, for planning to the busy case. |
| Forecast version | the name it points at, never the id | The AI forecast version the requirement is bound to (AIP-067), so a manager can open the forecast behind it. |

**Checked in** (data table, from `listAttendance`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Assignment | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Kind | chip: Clock in, Clock out, Break start, Break end | — |
| Occurred at | 1 Oct 2026, 14:30 | Device time — when it happened. |
| Recorded at | 1 Oct 2026, 14:30 | When the server received it. Both are kept: a steward clocking in offline at a gate is not late because the sync was. |
| Access point | the name it points at, never the id | — |
| Latitude | 1,234.5 | — |
| Longitude | 1,234.5 | — |
| Is amended | yes / no (icon or chip) | — |
| Amended by principal | the name it points at, never the id | Who made the latest amendment. The full history is `amendments` (audit R129 (7)). |
| Amendment reason | text | The latest amendment's reason. The full history is `amendments` (audit R129 (7)). |
| Original occurred at | 1 Oct 2026, 14:30 | The original is never overwritten. Attendance feeds pay, and a record that can be quietly rewritten is not evidence. |
| Amendments | list or chips (count when long) | Every correction, oldest first, one row each (decided 28 September, audit R129 (7)). |
| ID | the name it points at, never the id | — |
| Attendance record | the name it points at, never the id | — |
| Amended by principal | the name it points at, never the id | — |
| Amended at | 1 Oct 2026, 14:30 | — |
| Occurred at before | 1 Oct 2026, 14:30 | The record's time before this correction. |

**The selected attraction operational staffing** (detail panel): The pack groups this record's detail under its own headings: “Managers shall select”, “Required”, “Scheduled”, “Managers may assign employees through”, “Ticket/Experience Visibility”.

| Shows | Format | Notes |
|---|---|---|
| Name | text | not in the schema: `Name` |
| Photograph | text | not in the schema: `Photograph` |
| Role | text | not in the schema: `Role` |
| Skill level | text | not in the schema: `Skill level` |
| Certifications | text | not in the schema: `Certifications` |
| Availability | text | not in the schema: `Availability` |
| Current hours | text | not in the schema: `Current hours` |
| Venue | text | not in the schema: `Venue` |
| Overtime impact | text | not in the schema: `Overtime impact` |
| AI suitability score | text | not in the schema: `AI suitability score` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Role requirement table**: Role / position, Required, Scheduled, Checked in, Gap, Coverage % and actions; gaps red with a count, surplus grey. Header tiles: Required 24, Scheduled 21, Checked in 17, Gap 3, Coverage 87%. *(source: screens/P08-venue-back-office.yaml#BO-884 / DI-489)*
- **Demand driver**: Per session the tickets sold and the staff that requires ("14:00 Group lesson - 18 tickets - needs 3 instructors - 2 assigned - gap 1"). *(source: screens/P08-venue-back-office.yaml#BO-884)*
- **Candidate cards**: Name, photo, role, skill level, certifications (valid / expiring), availability, hours this week, venue, overtime impact ("+2 h overtime"), and a match score with its reasons. Candidates who fail a mandatory requirement are not listed as available; a "Show ineligible" toggle lists them with why. *(source: screens/P08-venue-back-office.yaml#BO-884 / screens/P08-venue-back-office.yaml#BO-882)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Assign / Move / Replace**: Creates or changes the assignment; refusals name the clash ("Omar Haddad is on Falcon Coaster 10:00-14:00") or the missing role. Rest and hour breaches come back as flags on the new block. *(source: contracts/satellite/workforce.yaml#createRotaAssignment / contracts/satellite/workforce.yaml#updateRotaAssignment)*
- **Smart assign**: Proposes the top candidate per gap with reasons; nothing is assigned until the manager applies it. *(source: contracts/satellite/resources.yaml#suggestResources)*

**Data it reads**: `listRotaAssignments` (onLoad, Who is rostered on each position); `getStaffingCoverage` (onLoad, Where the roster is short); `listAttendance` (onLoad, Who has checked in)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction operational staffing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction operational staffing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction operational staffing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attraction operational staffing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Overlaps an existing assignment, or the person lacks the required role |

#### Edge cases to draw

- **Assigned person is not qualified for the position**: The slot still counts as a gap ("Rostered 2, qualified 1") and says why. *(source: contracts/satellite/workforce.yaml#/components/schemas/StaffingCoverage)*
- **Two managers assign the same person at once**: The second gets the overlap refusal and the candidate card refreshes to "Assigned". *(source: contracts/satellite/workforce.yaml#createRotaAssignment)*

#### Consistency with other screens

- Match `BO-885`: Required counts come from the rules there; same position names.
- Match `BO-714`: Event rosters use the same grid.
- Match `BO-917`: Event staff candidates use the same card.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
scope: Summit Peaks - Ski School - Sat 10 Oct 2026, 09:00-17:00
roles:
- role: Ski School Supervisor
  required: 1
  scheduled: 1
  checkedIn: 1
  gap: 0
- role: Ski Instructor - Level 3
  required: 12
  scheduled: 10
  checkedIn: 8
  gap: 2
- role: Ski Instructor - Level 2
  required: 6
  scheduled: 5
  checkedIn: 4
  gap: 1
- role: Customer Service Agent
  required: 2
  scheduled: 2
  checkedIn: 2
  gap: 0
candidate:
  name: Layla Al Suwaidi
  role: Ski Instructor - Level 3
  certs: PSIA Level 3 valid to Jan 2027
  hours: 32 of 48 h
  overtime: None
  match: 96% - available, level 3, same venue, no overtime
```

#### Permissions

- `createRotaAssignment` → `WORKFORCE_MANAGE` (configure) · staff
- `listRotaAssignments` → `WORKFORCE_VIEW` (read) · staff
- `getStaffingCoverage` → `WORKFORCE_VIEW` (read) · staff
- `listAttendance` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.11 | The system should be able to generate operational rosters for staff resources. The rosters should provide information on the staff resources associated with an attraction, their availability, booked … | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.32 | System shall support staff scheduling and assignment. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.33 | System shall manage employee shifts. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.60 | Employees shall receive assignments on mobile devices. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.61 | Employees shall check into assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.62 | Employees shall check out assigned resources. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 1.2.63 | Employees shall view schedules via mobile app. | Ticketing Catalogue | CONTRACTED | `listRotaAssignments` |
| 18.1.1 | iOS Mobile Application - System shall provide a native iOS application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 18.1.2 | Android Mobile Application - System shall provide a native Android application. | Employee Mobile App & AI Assistant | CONTRACTED | `listRotaAssignments` |
| 8.2.49 | System shall generate staffing shortage alerts. | Unified Operations Dashboard | CONTRACTED | `getStaffingCoverage` |
| 8.9.7 | System shall display staffing levels, shift attendance, assignments, absences, overtime, and workforce utilization. | Unified Operations Dashboard | CONTRACTED | `listAttendance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Roster view per resource shows required vs. scheduled vs. checked-in counts for the day, surfacing discrepancies (e.g. 10 ski trainers scheduled, only 8 checked in). Minimum staffing/coverage rules are set per venue and day (e.g. minimum instructors per level). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-489)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-884` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-884`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 2: Works in Attraction & Operational Staffing Roster → Create detailed staffing plans for individual attractions, experiences, venues, departments, and events.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (77 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-884?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-885` Minimum Staffing & Coverage Rule Configuration

**Define the minimum personnel required to operate safely and effectively.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-885 |
| Who uses it | venue staff holding `WORKFORCE_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/minimum-staffing-coverage-rule-configuration-bo-885` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Minimum staffing and coverage rules: how many of which role, with which qualifications, each operation needs to run safely - fixed (Waterpark Zone A needs 1 supervisor, 4 lifeguards, 1 first-aider) or driven by demand (1 instructor per 8 participants) - with thresholds and what happens when a roster falls short. The one thing to get right: a rule says in plain words what it requires and what it enforces ("Wave Rider cannot run with fewer than 2 operators - closes rather than runs short").

**Known correction pending (do not draw the wrong version)**

- **Write with no read (no getStaffingRules), shared with BO-881 on a whole-record PUT** Why: The editor cannot open pre-filled, and saving from either screen without the other's values erases them. *(source: contracts/satellite/workforce.yaml#setStaffingRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Demand-based ratios, Target / Recommended / Maximum thresholds, event, experience and department dimensions, language, and the four enforcement levels have no field** Why: minimumCover holds a fixed minimum headcount, qualifications and blocksOperation only. *(source: screens/P08-venue-back-office.yaml#BO-885 / screens/P08-venue-back-office.yaml#BO-886 / contracts/satellite/workforce.yaml#/components/schemas/StaffingRules; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **"Minimum", "Target", "Recommended", "Maximum", "Enforcement" drawn as select fields with nothing around them** Why: They are numbers and one choice inside a rule; without the rule builder they mean nothing. *(source: screens/P08-venue-back-office.yaml#BO-886; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where does the list of position codes come from (RotaAssignment.position is tenant-defined text)?** → Drawn default accepted: A position picker seeded from job titles; mark the list source as pending. *(decided by Chinmay, 2026-10-02; DEC-502 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Minimum | select field | — | — | — | — | — | — |
| Target | select field | — | — | — | — | — | — |
| Recommended | select field | — | — | — | — | — | — |
| Maximum | select field | — | — | — | — | — | — |
| Enforcement | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Applies to**: Venue, attraction or experience, event, department, resource type; days of week (chips, empty = every open day); time window (from-to, empty = opening to closing). *(source: screens/P08-venue-back-office.yaml#BO-885 / contracts/satellite/workforce.yaml#/components/schemas/StaffingRules)*
- **Requirement**: Rows of position (picker of position codes) with minimum headcount and required qualifications (certification, skill level, language); "Fixed" or "Per demand" - per demand reads "1 per [8] participants" with a worked preview ("40 booked = 5 instructors"). *(source: screens/P08-venue-back-office.yaml#BO-885)*
- **Thresholds**: Minimum, Target, Recommended, Maximum as numbers on one line; minimum is the one coverage measures. *(source: screens/P08-venue-back-office.yaml#BO-886)*
- **Enforcement**: One choice: Warn / Require approval / Prevent roster publication / Trigger escalation, plus "Close the operation rather than run short" for safety-critical positions. *(source: screens/P08-venue-back-office.yaml#BO-886 / contracts/satellite/workforce.yaml#/components/schemas/StaffingRules)*
- **Rule id**: Never an input (per VO-R03), even though each minimumCover row requires an id. *(source: contracts/satellite/workforce.yaml#/components/schemas/StaffingRules)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Rules library**: List of rules by operation with status (Active) and a one-line summary; the selected rule's requirement logic as a table, as in the client render. *(source: screens/P08-venue-back-office.yaml#BO-885)*
- **Effect preview**: Against next week's roster - "Zone A would be short on 3 days" - before Save. *(source: contracts/satellite/workforce.yaml#getStaffingCoverage)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save rules**: Sends the whole staffing-rules record: every minimum-cover row for the venue plus the working-hour and overtime values from BO-881 (per VO-R04); confirm says "A position left out no longer has a minimum" if rows were removed. *(source: contracts/satellite/workforce.yaml#setStaffingRules)*

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The minimum staffing coverage configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the minimum staffing coverage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No minimum staffing coverage configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Position code typed differently from the rota's positions**: Not possible - positions are picked from one list; otherwise coverage would count against nothing. *(source: contracts/satellite/workforce.yaml#/components/schemas/RotaAssignment)*
- **Rule removed while the operation is open today**: Confirm names it ("Wave Rider will have no minimum from now"). *(source: contracts/satellite/workforce.yaml#setStaffingRules)*

#### Consistency with other screens

- Match `BO-881`: Same record; one editor with two sections, or both screens load and send the whole record.
- Match `BO-884`: Required counts shown there come from these rules.
- Match `BO-890`: "Below minimum cover" findings refer to these rules by name.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rules:
- operation: Aqua Park - Zone A
  fixed: 1 Supervisor, 4 Lifeguards, 1 First-aid qualified
  days: Every open day
  window: 10:00-19:00
  enforcement: Prevent roster publication
- operation: Summit Peaks - Ski School
  perDemand: 1 Instructor (Level 2+) per 8 participants
  preview: 40 booked = 5 instructors
  enforcement: Warn
- operation: Falcon Coaster
  fixed: 2 Ride operators
  enforcement: Close rather than run short
```

#### Permissions

- `setStaffingRules` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Roster view per resource shows required vs. scheduled vs. checked-in counts for the day, surfacing discrepancies (e.g. 10 ski trainers scheduled, only 8 checked in). Minimum staffing/coverage rules are set per venue and day (e.g. minimum instructors per level). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-489)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-885` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-885`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 4: Works in Minimum Staffing & Coverage Rule Configuration → Define the minimum personnel required to operate safely and effectively.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-885?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-886` Staffing Gap & Coverage Control Center

**Identify workforce shortages before they create operational problems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-886 |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE`, `WORKFORCE_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/staffing-gap-coverage-control-center-bo-886` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Staffing gaps before and during the day: required, scheduled and checked-in per role and slot, the gap each leaves and how severe it is, with a shortage alert. An operational control screen with actions, not a dashboard.

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How does the pack's four-level severity map onto covered, tight, short, blocking?** → Drawn default accepted: Informational = tight, Warning = short, High and Critical = blocking. *(decided by Chinmay, 2026-10-02; DEC-360 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |
| Venue | select field | — | — | — | — | Sends `?venueId=`. | — |
| Severity | select field | — | — | — | — | Client-side on `severity` (covered, tight, short, blocking); the pack's Informational / Warning / High / Critical scale does not map one to one. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getStaffingCoverage` ?from |
| To | date picker | — | — | `getStaffingCoverage` ?to |
| Basis | segmented control | Minimum | Minimum · Forecast requirement · Higher of both | `getStaffingCoverage` ?basis |
| Status | radio group | — | Raised · Acknowledged · Resolved · Expired | `listAlerts` ?status |
| Severity | segmented control | — | Info · Warning · Critical | `listAlerts` ?severity |
| Workstation | picker: choose a workstation | — | — | `listAlerts` ?workstationId |
| Shift | picker: choose a shift | — | — | `listAlerts` ?shiftId |
| Item | picker: choose an item | — | — | `listAlerts` ?itemId |

#### Outputs: what the screen shows and produces

**Shown**

**Planned gap** (metric tile, from `getStaffingCoverage`): Summed across positions.

| Shows | Format | Notes |
|---|---|---|
| Gap | 1,234 | — |

**Blocking gaps** (metric tile, from `getStaffingCoverage`): Count where `severity` is blocking.

| Shows | Format | Notes |
|---|---|---|
| Severity | chip: Covered, Tight, Short, Blocking | — |

**Live operational gap** (metric tile): Required against checked-in staff (the pack's 12 required / 9 checked in = 3); no attendance field is returned.

| Shows | Format | Notes |
|---|---|---|
| Live operational gap | text | not in the schema: `Live operational gap` |

**Coverage by position** (data table, from `getStaffingCoverage`)

| Shows | Format | Notes |
|---|---|---|
| Date | 1 Oct 2026 | — |
| Label | text | — |
| Position code | text | — |
| From | text | — |
| To | text | — |
| Severity | chip: Covered, Tight, Short, Blocking | — |

**The selected gap** (detail panel, from `getStaffingCoverage`): Gap type (missing staff / role / skill / certification, absence- or demand-created) and the AI recommendation are pack labels.

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | — |
| Label | text | — |
| From | text | — |
| To | text | — |
| Required | 1,234 | — |
| Rostered | 1,234 | — |
| Qualified | 1,234 | A position filled by somebody not qualified for it is still a gap. |
| Gap | 1,234 | — |
| Severity | chip: Covered, Tight, Short, Blocking | — |
| Open shifts | list or chips (count when long) | — |
| Gap type | text | not in the schema: `Gap type` |
| Recommended employee | text | not in the schema: `Recommended employee` |
| Match score | text | not in the schema: `Match score` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **gap row**: Role, slot, required, scheduled, checked in, planned gap (required minus scheduled), live gap (required minus checked in), severity. *(source: DI-489 / DI-490)*

**Data it reads**: `getStaffingCoverage` (onLoad, Gaps, by severity); `listAlerts` (onLoad, Staffing shortage alerts (metric staffingShortfall))

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staffing gap coverage list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staffing gap coverage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staffing gap coverage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the staffing gap coverage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 An `outsideRange` rule without both `threshold` and `thresholdUpper`, or with the upper not above the lower (audit R158) |

#### Consistency with other screens

- Match `P16 ANL-003 Operational Performance`: The staffing tile there links here; not a duplicate because this screen acts.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Ski instructors Level 2 · Sat 3 Oct 09:00–12:00 · required 12 · scheduled 10 · checked in 9 · planned gap 2 ·
  live gap 3 · Short
```

#### Permissions

- `getStaffingCoverage` → `WORKFORCE_VIEW` (read) · staff
- `listAlerts` → `REPORT_VIEW_VENUE` (operate) · staff
- `setAlertRule` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.49 | System shall generate staffing shortage alerts. | Unified Operations Dashboard | CONTRACTED | `getStaffingCoverage` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- If a scheduled resource fails to check in, the shortfall is flagged for operations and AI can recommend reassigning that resource's bookings. A compliance/validation centre flags events where required staffing is not met, with labour cost tracked. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-490)*
- Roster view per resource shows required vs. scheduled vs. checked-in counts for the day, surfacing discrepancies (e.g. 10 ski trainers scheduled, only 8 checked in). Minimum staffing/coverage rules are set per venue and day (e.g. minimum instructors per level). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-489)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-886` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-886`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 6: Works in Staffing Gap & Coverage Control Center → Identify workforce shortages before they create operational problems.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-886?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`, `WORKFORCE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-887` Shift Marketplace & Workforce Requests

**Allow employees and managers to manage shift changes through controlled workflows rather than informal manual communication.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/shift-marketplace-workforce-requests-bo-887` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-001): Claiming an open shift is an employee act on the Staff App; the manager publishes and approves here. The manager's queue needs the swap requests (design-notes …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The shift marketplace and workforce request queue for managers: swap, transfer, pickup and release requests with their validation, and the open shifts published for eligible staff to claim, all approved through the same approval path. The one thing to get right: each request shows the validation result before the manager decides (role, skills, certification, availability, hours, rest, overtime, minimum staffing, venue permission), and open shifts are only ever offered to people who meet the rules.

**Fixed on main** (the package already carries these; draw what it says): "Claim open shift" is a primary button on the back-office screen (CHG-WIR-001); No operation publishes, releases or withdraws an open shift, and transfer has none at all (CHG-WIR-001); Swap requests (listShiftSwapRequests) and approvals are not bound, though the client render's first tab is Swap Requests with approve and … (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which approvals does each request type need (employee acceptance, supervisor, department, workforce manager)?** → Drawn default accepted: Swap - colleague then supervisor; pickup - supervisor; release - supervisor; shown as a step tracker per row. *(decided by Chinmay, 2026-10-02; DEC-503 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Request tabs**: Swap requests / Pickup requests / Release requests / Open shifts, each with a count; status filter Pending, Approved, Rejected. *(source: screens/P08-venue-back-office.yaml#BO-887)*
- **Publish open shift**: From an unfilled assignment or a template: position, from-to, required qualifications, reason, and an incentive multiplier defaulted from the venue rule and capped at its maximum (above the approval threshold the release needs a second person). *(source: contracts/satellite/workforce.yaml#/components/schemas/OpenShift / contracts/satellite/workforce.yaml#/components/schemas/StaffingRules)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Swap requests** (data table, from `listShiftSwapRequests`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Assignment | the name it points at, never the id | — |
| From principal | the name it points at, never the id | — |
| To principal | the name it points at, never the id | — |
| Status | chip: Awaiting peer, Awaiting approval, Approved, Rejected, Withdrawn | Both parties before the supervisor. A swap approved against someone who never agreed is a gap in the rota nobody notices until the shift … |
| Approval request | text | Routed through `approvals` rather than a second mechanism here. |
| Reason | text | — |
| Requested at | 1 Oct 2026, 14:30 | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Request row**: Type pill (Swap, Pickup, Release, Transfer), from and to people with photos, shift date and time, status (Awaiting employee, Awaiting supervisor, Auto-match recommended, Approved), and Approve / Reject. *(source: screens/P08-venue-back-office.yaml#BO-887 / contracts/satellite/workforce.yaml#/components/schemas/ShiftSwap)*
- **Validation panel**: Checklist with ticks and crosses: role, skills, certification, availability, working-hour limits, rest, overtime ("David: +2 overtime hours"), minimum staffing maintained, venue permission; and the recommendation in one sentence ("All mandatory rules pass; creates 2 overtime hours"). *(source: screens/P08-venue-back-office.yaml#BO-888 / screens/P08-venue-back-office.yaml#BO-941)*
- **Open shift row**: Position, time, venue, required qualifications, eligible people ("6 eligible"), incentive ("x1.5"), status (Open, Claimed, Pending approval, Filled, Expired, Withdrawn). *(source: contracts/satellite/workforce.yaml#listOpenShifts)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Approve / Reject / Request changes**: Decides the approval request behind the swap or claim; a requester can never approve their own; reject needs a reason, which reaches the requester. *(source: contracts/spine/approvals.yaml#decideApprovalRequest / contracts/satellite/workforce.yaml#requestShiftSwap / DI-235)*
- **Publish open shift**: Confirm names who will see it ("Offered to 6 eligible lifeguards at Aqua Park"). *(source: contracts/satellite/workforce.yaml#/components/schemas/OpenShift)*

**Data it reads**: `listOpenShifts` (onLoad, The shift marketplace); `listShiftSwapRequests` (onLoad, Swap requests waiting on the manager)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift marketplace workforce list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift marketplace workforce untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shift marketplace workforce yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the shift marketplace workforce are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A claim would breach a working-hour rule**: Refused at claim ("would exceed 60 h this week"); shown on the row as Rejected by rule, not by a person. *(source: contracts/satellite/workforce.yaml#claimOpenShift)*
- **Swap not accepted by the colleague before the shift**: Expires; the original assignment stands and the row says so. *(source: F68 step 3)*

#### Consistency with other screens

- Match `EMP-023`: Staff create swaps there; the status words are identical.
- Match `BO-939`: The employee-side marketplace (open shifts, request shift) is the mobile half of this screen.
- Match `BO-883`: The Open shifts tile counts open rows here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
requests:
- type: Swap
  from: Maria Santos
  to: Omar Haddad
  shift: Tue 13 Oct 08:00-16:00
  status: Awaiting supervisor
  validation: All pass; Omar +2 h overtime
- type: Pickup
  from: Open shift
  to: Rahul Menon
  shift: Sat 17 Oct 14:00-22:00
  status: Auto-match recommended
- type: Release
  from: Fatima Al Hashimi
  shift: Fri 16 Oct 14:00-23:00
  status: Approved
openShift:
  position: Lifeguard
  time: Sat 17 Oct 15:00-18:00
  venue: Aqua Park - Zone B
  eligible: 6
  incentive: x1.5
  status: Open
```

#### Permissions

- `listOpenShifts` → `WORKFORCE_VIEW` (read) · staff
- `listShiftSwapRequests` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-887` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-887`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 8: Works in Shift Marketplace & Workforce Requests → Allow employees and managers to manage shift changes through controlled workflows rather than informal manual communication.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-887?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-888` Attendance & Live Workforce Command Center

**Provide real-time visibility into whether scheduled employees actually reported and are available for operation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-888 |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/attendance-live-workforce-command-center-bo-888` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The live attendance command centre: in real time, whether the people scheduled today actually reported - checked in, not yet arrived, late, absent, on break, checked out, in overtime - and the operational impact ("Ski School staffing has fallen below minimum coverage"). The one thing to get right: counts are KPI tiles and the per-person planned-versus-actual list includes the people with no clock-in, which is the list a duty manager needs.

**Known correction pending (do not draw the wrong version)**

- **The pack's KPIs (Scheduled today, Checked in, Not yet arrived...) are drawn as columns of a data table** Why: KPIs are metric tiles (VO-R02). *(source: screens/P08-venue-back-office.yaml#BO-888; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **listAttendance returns attendance records only; a scheduled person with no clock-in has no record** Why: "Not yet arrived" and "No-show" need the rota joined in; the description says "against the rota" but the response cannot list people who never clocked. *(source: contracts/satellite/workforce.yaml#listAttendance; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The gap says the operation returns no schema, though AttendanceRecord is fully described** Why: Bind the per-person list to it. *(source: contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is this screen live-updating (push) or refreshed on an interval?** → Drawn default accepted: Auto-refresh every 30 seconds with "Updated 14:31" and a manual refresh, as the client render's footer implies. *(decided by Chinmay, 2026-10-02; DEC-504 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Date | date picker | — | — | `listAttendance` ?date |
| Principal | picker: choose a principal | — | — | `listAttendance` ?principalId |
| Exceptions only | toggle | — | — | `listAttendance` ?exceptionsOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Date and filters**: Today by default; venue, department and position chips; "Exceptions only" toggle. *(source: contracts/satellite/workforce.yaml#listAttendance)*

#### Outputs: what the screen shows and produces

**Shown**

**Every attendance live workforce** (data table)

| Shows | Format | Notes |
|---|---|---|
| Scheduled today | text | not in the schema: `Scheduled today` |
| Checked in | text | not in the schema: `Checked in` |
| Not yet arrived | text | not in the schema: `Not yet arrived` |
| Late | text | not in the schema: `Late` |
| Absent | text | not in the schema: `Absent` |
| No show | text | not in the schema: `No-show` |
| On break | text | not in the schema: `On break` |
| Checked out | text | not in the schema: `Checked out` |
| Overtime | text | not in the schema: `Overtime` |
| Attendance exceptions | text | not in the schema: `Attendance exceptions` |
| Planned vs actual | text | not in the schema: `Planned vs Actual` |

**The selected attendance live workforce** (detail panel): The pack groups this record's detail under its own headings: “For each employee”.

| Shows | Format | Notes |
|---|---|---|
| Scheduled today | text | not in the schema: `Scheduled today` |
| Checked in | text | not in the schema: `Checked in` |
| Not yet arrived | text | not in the schema: `Not yet arrived` |
| Late | text | not in the schema: `Late` |
| Absent | text | not in the schema: `Absent` |
| No show | text | not in the schema: `No-show` |
| On break | text | not in the schema: `On break` |
| Checked out | text | not in the schema: `Checked out` |
| Overtime | text | not in the schema: `Overtime` |
| Attendance exceptions | text | not in the schema: `Attendance exceptions` |
| Planned vs actual | text | not in the schema: `Planned vs Actual` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Scheduled today, Checked in, Not yet arrived, Late, Absent, No-show, On break, Checked out, Overtime, Attendance exceptions - with percentage of scheduled and change against yesterday. *(source: screens/P08-venue-back-office.yaml#BO-888 / screens/P08-venue-back-office.yaml#BO-889)*
- **Planned versus actual**: Per person: name, role, planned start, actual in, actual out, status (Working, Late 14 min, No-show, On break, Checked out), location as a place name, and a Message action. Sorted with exceptions first. *(source: screens/P08-venue-back-office.yaml#BO-889 / screens/P08-venue-back-office.yaml#BO-888)*
- **Live alerts**: "Omar Haddad arrived 14 minutes late", "Maria Santos has not checked in", "Ski School staffing has fallen below minimum coverage", newest first, each linking to the person or the gap. *(source: screens/P08-venue-back-office.yaml#BO-889 / DI-490)*
- **Attendance trend**: Checked-in percentage by day for the week as a small line chart. *(source: screens/P08-venue-back-office.yaml#BO-888)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Find replacement**: From a no-show row, opens the gap with ranked replacements (applied by a person). *(source: DI-490)*
- **Message**: Direct message to the person. *(source: contracts/satellite/workforce.yaml#sendStaffMessage)*

**Data it reads**: `listAttendance` (onLoad, Live attendance)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attendance live workforce list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attendance live workforce untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attendance live workforce yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attendance live workforce are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Clock-in made offline and not yet synced**: The person may show "Not yet arrived" until sync; when the record arrives it shows device time, so they are not marked late retroactively. *(source: contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord)*
- **Missing clock-out at end of day**: Flagged "No clock-out", never filled in. *(source: contracts/satellite/workforce.yaml#recordAttendance)*

#### Consistency with other screens

- Match `BO-056`: The per-person list is BO-056's day view (same columns and status words); draw once (per VO-R14).
- Match `BO-883`: Same counts as the roster command centre tiles.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  scheduled: 126
  checkedIn: 98 (77.8%)
  notYetArrived: 12
  late: 6
  absent: 10
  onBreak: 9
  overtime: 4 people
rows:
- person: Rahul Menon
  role: Gate steward
  planned: 07:00
  in: 06:52
  out: '-'
  status: Working
  at: Staff Entrance North
- person: Maria Santos
  role: Cashier
  planned: 09:00
  in: 09:18
  out: '-'
  status: Late 18 min
- person: Omar Haddad
  role: Gate steward
  planned: 07:00
  in: '-'
  out: '-'
  status: No-show
```

#### Permissions

- `listAttendance` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.9.7 | System shall display staffing levels, shift attendance, assignments, absences, overtime, and workforce utilization. | Unified Operations Dashboard | CONTRACTED | `listAttendance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staffing dashboard shows checked-in, on-shift, on-leave, open-shift and closed-shift counts from check-in/out logs, plus staffing cost including overtime. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-488)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-888` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-888`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 10: Works in Attendance & Live Workforce Command Center → Provide real-time visibility into whether scheduled employees actually reported and are available for operation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-888?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-889` Staff Check-In, Check-Out & Attendance Exceptions

**Record actual employee working activity and manage exceptions to scheduled attendance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-889 |
| Who uses it | venue staff holding `ATTENDANCE_RECORD`, `WORKFORCE_MANAGE` (1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§The system shall capture; Every correction shall capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `recordId` (navigation) |
| Route | `/rentals/staff-check-in-check-out-attendance-exceptions-bo-889` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** One person's attendance record for a shift and its exceptions: planned against actual check-in and check-out, lateness, early departure, overtime, no-show, the source of each clock, and every correction with the original kept. A supervisor marks exceptions and corrects times here. The one thing to get right: the original value is never overwritten - each correction appends a row with who, when, before, after and why.

**Known correction pending (do not draw the wrong version)**

- **recordAttendance has no person field, so a manager cannot check someone in on their behalf** Why: The pack lists manager check-in and the client render has "Mark as Present"; the operation records the caller's own attendance only. (BO-056's "Record attendance (on behalf)" has the same gap.) *(source: screens/P08-venue-back-office.yaml#BO-889 / contracts/satellite/workforce.yaml#recordAttendance; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **amendAttendance corrects a time only; exceptions cannot be marked and the exception enum lacks sick, approved absence, emergency and system error** Why: DI-491 asks for manually marked exceptions (active, not active, absent, other). *(source: DI-491 / contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Planned check-in, actual check-in, lateness and the history columns (Original value, New value, User, Timestamp, Reason) are drawn as select fields** Why: They are read values and table columns, not inputs. *(source: screens/P08-venue-back-office.yaml#BO-889; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **AttendanceRecord has no source or device field** Why: The pack's "Source/device" cannot be shown beyond the access point. *(source: screens/P08-venue-back-office.yaml#BO-889 / contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which corrections need approval ("Approval where required"), and by whom?** → Drawn default accepted: None by default; a greyed "Requires approval above 60 min" setting. *(decided by Chinmay, 2026-10-02; DEC-505 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Planned check-in | select field | — | — | — | — | — | — |
| Actual check-in | select field | — | — | — | — | — | — |
| Planned check-out | select field | — | — | — | — | — | — |
| Actual check-out | select field | — | — | — | — | — | — |
| Attendance status | select field | — | — | — | — | — | — |
| Lateness | select field | — | — | — | — | — | — |
| Early departure | select field | — | — | — | — | — | — |
| Overtime | select field | — | — | — | — | — | — |
| No-show | select field | — | — | — | — | — | — |
| Exception | select field | — | — | — | — | — | — |
| Source/device | select field | — | — | — | — | — | — |
| Exception Types | select field | — | — | — | — | — | — |
| Original value | select field | — | — | — | — | — | — |
| New value | select field | — | — | — | — | — | — |
| User | select field | — | — | — | — | — | — |
| Timestamp | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |
| Approval where required | select field | — | — | — | — | — | — |
| Mobile Assignment Check-In | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Correct time**: New time (date-time in venue time) and a required reason (max 300, chips "Phone died", "Forgot to clock out", "System error"). *(source: contracts/satellite/workforce.yaml#amendAttendance)*
- **Mark exception**: One choice: Late arrival, Early departure, Missed check-in, Missed check-out, Approved absence, Sick, Emergency, System error, Manager adjustment; with a note. *(source: screens/P08-venue-back-office.yaml#BO-889 / DI-491)*

#### Outputs: what the screen shows and produces

**Shown**

**Amendment history** (data table, from `amendAttendance`): **Every correction, not only the last** (decided 28 September, audit R129 (7)) — read from `AttendanceRecord.amendments`: who, when, before, after and why.

| Shows | Format | Notes |
|---|---|---|
| Amended at | 1 Oct 2026, 14:30 | — |
| Amended by principal | the name it points at, never the id | — |
| Occurred at before | 1 Oct 2026, 14:30 | The record's time before this correction. |
| Occurred at after | 1 Oct 2026, 14:30 | The time this correction set (`correctedAt` on the request). |
| Reason | text | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Record header**: Person, role, shift (planned in-out), actual in-out, attendance status, and computed lateness, early departure and overtime in minutes. Read-only values, not select fields. *(source: screens/P08-venue-back-office.yaml#BO-889 / contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord)*
- **Source of each clock**: Employee App, Manager, Staff terminal, QR, NFC, Integrated system - with the place name and "Outside the venue area" where flagged. *(source: screens/P08-venue-back-office.yaml#BO-889 / contracts/satellite/workforce.yaml#/components/schemas/AttendanceRecord)*
- **Correction history**: Every amendment, oldest first - original value, new value, user, timestamp, reason, approval where required. *(source: screens/P08-venue-back-office.yaml#BO-889 / contracts/satellite/workforce.yaml#/components/schemas/AttendanceAmendment)*
- **Assignment check-ins**: Where configured, check-ins to specific activities ("Checked in - Private ski lesson - Ski School Zone A - 13:57"). *(source: screens/P08-venue-back-office.yaml#BO-889)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save adjustment**: Appends the correction; the header shows "Amended" with the original time struck through beside the new one. *(source: contracts/satellite/workforce.yaml#amendAttendance)*
- **Mark as present (no-show)**: Records the person's attendance with the supervisor named as source and a reason; needs a confirm. *(source: screens/P08-venue-back-office.yaml#BO-889)*

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The staff check-in check-out configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the staff check-in check-out untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No staff check-in check-out configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Out of sequence — a clock-out with no clock-in, or a second clock-in. Reported rather than silently corrected. |

#### Edge cases to draw

- **Second correction to the same record**: Both corrections are listed; the first is not replaced. *(source: contracts/satellite/workforce.yaml#amendAttendance)*
- **Supervisor corrects their own record**: Refused or routed to another supervisor, with the reason. *(source: designer default)*

#### Consistency with other screens

- Match `BO-056`: The same amendment form and history; draw once and open it from both.
- Match `EMP-024`: The person's phone shows "Corrected by" with the original kept.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
record:
  person: Maria Santos
  role: Cashier
  planned: 09:00-17:00
  actualIn: 09:18 (original) / 09:02 (amended)
  actualOut: '17:00'
  status: Amended
  source: Employee App - Staff Entrance North
amendments:
- when: 10 Oct 2026 09:40
  by: Fatima Al Hashimi
  before: Clock in 09:18
  after: Clock in 09:02
  reason: Phone died at the staff entrance; seen on post at 09:02
```

#### Permissions

- `recordAttendance` → `ATTENDANCE_RECORD` (operate) · staff
- `amendAttendance` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.81 | System shall record planned shifts, actual check-in times, actual check-out times, attendance status, lateness, early departures, no-shows, overtime hours, attendance exceptions, and workforce … | Ticketing Catalogue | CONTRACTED | `recordAttendance` |
| 18.9.1 | Attendance Management - Users shall clock in and clock out. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 18.9.2 | Shift Management - Users shall view assigned shifts. | Employee Mobile App & AI Assistant | CONTRACTED | `recordAttendance` |
| 1.2.75 | System shall maintain complete audit logs. | Ticketing Catalogue | CONTRACTED | `amendAttendance` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staff can request a swap (e.g. break coverage) from another resource; attendance exceptions are marked manually (active, not active, absent, other). *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering; 4.9 AI Optimization, Mobile App & Analytics · DI-491)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-889` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-889`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 12: Works in Staff Check-In, Check-Out & Attendance Exceptions → Record actual employee working activity and manage exceptions to scheduled attendance.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (5 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-889?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `ATTENDANCE_RECORD`, `WORKFORCE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-890` Workforce Compliance Validation Center

**Validate planned workforce schedules against legal, safety, certification, and organizational rules before roster publication or assignment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-890 |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each issue shall display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/workforce-compliance-validation-center-bo-890` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The workforce compliance validation centre: every place the planned rota breaks a legal, safety, certification or organisational rule, before it is published - expired qualifications, exceeded hours, insufficient rest, missed breaks, consecutive days, under-age night shifts, below minimum cover. The one thing to get right: each finding names the person, the rule, the affected shift, the operational impact and the action to fix it, and critical findings stop publication unless an authorised override is recorded.

**Known correction pending (do not draw the wrong version)**

- **The table is drawn with the pack's labels as unbound text and the gap says no schema exists** Why: validateWorkforceCompliance returns WorkforceComplianceFinding; bind code, severity, principalName, date, detail, rotaAssignmentIds. *(source: contracts/satellite/workforce.yaml#validateWorkforceCompliance; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Findings have no operational impact or recommended action, severity is breach or warning only, and there is no override operation or non-overridable setting** Why: The pack requires each issue to show impact and action, three severities in the client render, and authorised overrides. *(source: screens/P08-venue-back-office.yaml#BO-890 / screens/P08-venue-back-office.yaml#BO-891 / contracts/satellite/workforce.yaml#/components/schemas/WorkforceComplianceFinding; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Who may override a compliance finding, and is the override routed through approvals?** → Drawn default accepted: Override with reason by a workforce manager, logged; greyed for rules marked non-overridable. *(decided by Chinmay, 2026-10-02; DEC-506 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `validateWorkforceCompliance` ?from |
| To | date picker | — | — | `validateWorkforceCompliance` ?to |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period**: From-to dates (default the next 7 days); severity tabs All / Critical / Warning / Info with counts. *(source: screens/P08-venue-back-office.yaml#BO-890 / contracts/satellite/workforce.yaml#validateWorkforceCompliance)*
- **Override**: Where policy permits, a reason (required) and approver; rules configured as non-overridable show no override. *(source: screens/P08-venue-back-office.yaml#BO-891)*

#### Outputs: what the screen shows and produces

**Shown**

**Every workforce compliance validation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Employee | text | not in the schema: `Employee` |
| Rule violated | text | not in the schema: `Rule violated` |
| Severity | text | not in the schema: `Severity` |
| Affected shift | text | not in the schema: `Affected shift` |
| Operational impact | text | not in the schema: `Operational impact` |
| Recommended action | text | not in the schema: `Recommended action` |

**The selected workforce compliance validation** (detail panel): The pack groups this record's detail under its own headings: “The engine shall support”.

| Shows | Format | Notes |
|---|---|---|
| Employee | text | not in the schema: `Employee` |
| Rule violated | text | not in the schema: `Rule violated` |
| Severity | text | not in the schema: `Severity` |
| Affected shift | text | not in the schema: `Affected shift` |
| Operational impact | text | not in the schema: `Operational impact` |
| Recommended action | text | not in the schema: `Recommended action` |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Findings table**: Issue in words (Rest period violation, Weekly hours exceeded, Certification expired, Missing skill level, Consecutive days exceeded, Break not scheduled, Under-age night shift, Below minimum cover), Employee, Rule ("Min 11 h rest required"), Severity (Breach shown as Critical, Warning), Affected shift, Operational impact, Recommended action. *(source: screens/P08-venue-back-office.yaml#BO-890 / contracts/satellite/workforce.yaml#/components/schemas/WorkforceComplianceFinding)*
- **Pre-publish checklist**: Availability, Qualification, Certification, Coverage, Working-hour, Rest, Overtime and Conflict checks, each Pass or count of findings. *(source: screens/P08-venue-back-office.yaml#BO-890 / screens/P08-venue-back-office.yaml#BO-891)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Validate roster**: Runs the check for the period and refreshes the table with "Checked 14:20". *(source: contracts/satellite/workforce.yaml#validateWorkforceCompliance)*
- **Open shift**: Opens the affected assignment on the roster to move, replace or shorten it. *(source: contracts/satellite/workforce.yaml#/components/schemas/WorkforceComplianceFinding)*

**Data it reads**: `validateWorkforceCompliance` (onLoad, Where the rota breaks a rule)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workforce compliance validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workforce compliance validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workforce compliance validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workforce compliance validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Employee with no date of birth on a night shift**: A Warning "Age not on file", not assumed to be of age. *(source: contracts/satellite/workforce.yaml#/components/schemas/WorkforceEmployee)*
- **No findings**: "No issues for 10-16 Oct. Roster can be published." with the checklist all passed. *(source: designer default)*

#### Consistency with other screens

- Match `BO-881`: Rule names and limits are the ones configured there.
- Match `BO-885`: Below-minimum findings name the rule from there.
- Match `BO-883`: Compliance warnings tile counts these findings.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
findings:
- issue: Rest period violation
  employee: Fatima Al Hashimi
  rule: Min 11 h rest required, scheduled 9 h
  severity: Critical
  shift: Sat 10 Oct 14:00-23:00
  impact: Shift cannot be confirmed
  action: Move start to 16:00 or replace
- issue: Certification expiring
  employee: Rahul Menon
  rule: First aid expires in 5 days
  severity: Warning
  shift: Thu 15 Oct 07:00-15:00
  action: Book renewal
- issue: Below minimum cover
  employee: '-'
  rule: Aqua Park Zone A - 4 lifeguards
  severity: Critical
  shift: Sat 17 Oct 15:00-18:00
  action: Publish open shift
```

#### Permissions

- `validateWorkforceCompliance` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- If a scheduled resource fails to check in, the shortfall is flagged for operations and AI can recommend reassigning that resource's bookings. A compliance/validation centre flags events where required staffing is not met, with labour cost tracked. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-490)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-890` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-890`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 14: Works in Workforce Compliance Validation Center → Validate planned workforce schedules against legal, safety, certification, and organizational rules before roster publication or assignment.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-890?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-891` Labor Cost & Staffing Budget Control

**Give managers visibility into the financial impact of staffing decisions before and after roster publication.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-891 |
| Who uses it | venue staff holding `WORKFORCE_MANAGE`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/labor-cost-staffing-budget-control-bo-891` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Labour cost and staffing budget control: scheduled, forecast and actual labour cost against the budget a manager is held to, per venue, department and period, with the cost drivers (base, overtime, premium, temporary, cross-venue) and AI suggestions to reduce cost without breaking a rule. The one thing to get right: the budget comparison is four figures and a variance stated in words ("AED 600 favourable"), and the budget itself is edited per venue, department and period without overlaps.

**Known correction pending (do not draw the wrong version)**

- **"Venue id" and "Department id" text filters; the budget table shows id, venueId, departmentId and scopePath** Why: Pickers and names (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-891; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **getLabourCost has no forecast figure, no cost-driver breakdown, and cannot group by event or attraction** Why: The pack's comparison is Budget, Scheduled, Forecast, Actual, Variance and its cost kinds include event and attraction staffing cost. *(source: screens/P08-venue-back-office.yaml#BO-891 / contracts/satellite/workforce.yaml#getLabourCost; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **LabourBudget.id is a required request field** Why: Server-assigned (VO-R03); the PUT is keyed by venue, department and period start. *(source: contracts/satellite/workforce.yaml#/components/schemas/LabourBudget; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What is "Forecast" cost - rostered plus expected overtime, or the cost of the forecast staff requirement?** → Drawn default accepted: Draw the tile with "Forecast not available yet" until defined. *(decided by Chinmay, 2026-10-02; DEC-507 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listLabourBudgets`. | `listLabourBudgets` ?venueId |
| Department id | picker: choose a department (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?departmentId=` to `listLabourBudgets`. | `listLabourBudgets` ?departmentId |
| From | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?from=` to `listLabourBudgets`. | `listLabourBudgets` ?from |
| To | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?to=` to `listLabourBudgets`. | `listLabourBudgets` ?to |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getLabourCost` ?from |
| To | date picker | — | — | `getLabourCost` ?to |
| Group by | radio group | — | Venue · Department · Role · Day · Person | `getLabourCost` ?groupBy |

**Form: Save labour budget** (modal, opened by *Save labour budget*; *Save labour budget* calls `setLabourBudget`, *Cancel* sends nothing)

**Collects what `setLabourBudget` sends before it is called.** Required: `venueId`, `periodStart`, `periodEnd`, `budgetAmount`. Optional: `departmentId`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `id` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `setLabourBudget` body |
| Department `departmentId` | picker: choose a department | optional | — | — | shows names, sends the id | — | `setLabourBudget` body |
| Period start `periodStart` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | First day of the period, in the Region's time zone | `setLabourBudget` body |
| Period end `periodEnd` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | Last day of the period, in the Region's time zone | `setLabourBudget` body |
| Budget amount `budgetAmount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setLabourBudget` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setLabourBudget` body |

Errors to draw in the form: 409 The period overlaps another budget for the same venue and department; 422 periodEnd is before periodStart

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period and grouping**: From-to (required), group by Venue / Department / Role / Day / Person; venue and department pickers, no id fields. *(source: contracts/satellite/workforce.yaml#getLabourCost / contracts/satellite/workforce.yaml#listLabourBudgets)*
- **Set budget**: Venue (top bar), department (empty = whole venue), period start and end (dates in the region's time zone), amount in AED. No id field. Periods for one venue and department may not overlap. *(source: contracts/satellite/workforce.yaml#setLabourBudget)*

#### Outputs: what the screen shows and produces

**Shown**

**Every labor cost staffing** (data table)

| Shows | Format | Notes |
|---|---|---|
| Budget | text | not in the schema: `Budget` |
| Scheduled | text | not in the schema: `Scheduled` |
| Forecast | text | not in the schema: `Forecast` |
| Actual | text | not in the schema: `Actual` |
| Variance | text | not in the schema: `Variance` |

**Every labour budget** (data table, from `listLabourBudgets`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Department | the name it points at, never the id | — |
| Period start | 1 Oct 2026 | First day of the period, in the Region's time zone |
| Period end | 1 Oct 2026 | Last day of the period, in the Region's time zone |
| Budget amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Scope path | text | — |

**The selected labor cost staffing** (detail panel): The pack groups this record's detail under its own headings: “Cost Calculation”, “Managers shall understand”.

| Shows | Format | Notes |
|---|---|---|
| Budget | text | not in the schema: `Budget` |
| Scheduled | text | not in the schema: `Scheduled` |
| Forecast | text | not in the schema: `Forecast` |
| Actual | text | not in the schema: `Actual` |
| Variance | text | not in the schema: `Variance` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save labour budget (primary button) | `setLabourBudget` PUT `/labour-budgets` | LabourBudget | LabourBudget | 409 The period overlaps another budget for the same venue and department; 422 periodEnd is before periodStart | gated `WORKFORCE_MANAGE`; opens modal first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Budget tiles**: Budget, Scheduled cost, Forecast cost, Actual cost, Variance (amount and %, "favourable" or "over" in words and colour). *(source: screens/P08-venue-back-office.yaml#BO-891)*
- **Cost table**: Per group - rostered hours, actual hours, overtime hours, rostered cost, actual cost, budget, variance, headcount; money as "AED 16,750.00". *(source: contracts/satellite/workforce.yaml#/components/schemas/LabourCostRow)*
- **Cost drivers**: Breakdown of regular pay, overtime, premium shifts, allowances and other as a donut with amounts and shares. *(source: screens/P08-venue-back-office.yaml#BO-892 / screens/P08-venue-back-office.yaml#BO-891)*
- **AI cost suggestion**: "Replace Maria Santos (AED 480 incl. overtime) with Omar Haddad (AED 320) - saving AED 160 - equally qualified." with Apply; never offered when a mandatory rule would break. *(source: screens/P08-venue-back-office.yaml#BO-892)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save budget**: Creates or replaces the budget for that venue, department and period start; 409 "Overlaps the October budget for Guest Services" and 422 end before start shown against the fields. Past cost is not rewritten. *(source: contracts/satellite/workforce.yaml#setLabourBudget)*
- **Optimise with AI**: Opens BO-892 focused on cost. *(source: screens/P08-venue-back-office.yaml#BO-891)*

**Data it reads**: `getLabourCost` (onLoad, Cost against budget); `listLabourBudgets` (onLoad, Labour budgets, per venue, department and period)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The labor cost staffing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the labor cost staffing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No labor cost staffing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the labor cost staffing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The period overlaps another budget for the same venue and department; 422 periodEnd is before periodStart |

#### Edge cases to draw

- **No budget for the period**: Budget and variance show "No budget set" with Set budget; costs still shown. *(source: contracts/satellite/workforce.yaml#getLabourCost)*
- **Viewer without pay visibility**: Costs hidden with "Needs labour cost rights"; hours remain. *(source: screens/P08-venue-back-office.yaml#BO-882)*

#### Consistency with other screens

- Match `BO-883`: Staffing cost today tile is this screen's actual cost for today.
- Match `BO-892`: Projected cost and saving there use the same figures.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
week:
  budget: AED 120,000.00
  scheduled: AED 112,450.00
  forecast: AED 115,200.00
  actual: AED 74,310.00 (to Thu)
  variance: AED 4,800.00 favourable
event:
  name: Winter Lights Festival
  budget: AED 18,000.00
  scheduled: AED 16,750.00
  forecast: AED 17,400.00
  variance: AED 600.00 favourable
```

#### Permissions

- `getLabourCost` → `WORKFORCE_VIEW` (read) · staff
- `listLabourBudgets` → `WORKFORCE_VIEW` (read) · staff
- `setLabourBudget` → `WORKFORCE_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Staffing dashboard shows checked-in, on-shift, on-leave, open-shift and closed-shift counts from check-in/out logs, plus staffing cost including overtime. *(client request · MoM 26 Aug 2026, 4.6 Workforce Rostering, Attendance & Staffing Control · DI-488)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-891` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-891`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 16: Works in Labor Cost & Staffing Budget Control → Give managers visibility into the financial impact of staffing decisions before and after roster publication.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (17 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-891?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save labour budget.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_MANAGE`, `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-892` AI Workforce Planner & Roster Optimization

**Generate or optimise operational rosters against configured priorities, with safety, compliance and mandatory qualifications kept as hard constraints.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | Block D · task VM-BO-892 |
| Who uses it | venue staff holding `WORKFORCE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/ai-workforce-planner-roster-optimization-bo-892` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Contract gap recorded 2 October 2026 (CHG-WIR-004): No roster generation or optimisation operation.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The AI workforce planner: generate or optimise a roster for a period from demand, required roles, minimum staffing, skills, certifications, availability, leave, shift patterns and working-hour rules, against chosen objectives, and compare it with the current roster before a manager accepts any of it. The one thing to get right: AI prepares a proposal a person applies (L2 Prepare); safety, compliance and mandatory qualifications are hard constraints, every assignment explains itself, and nothing publishes automatically.

**Known correction pending (do not draw the wrong version)**

- **"Generate roster with AI" and the Coverage, Overtime hours, Projected labour cost and Projected saving tiles are bound to nothing** Why: No roster-generation or optimisation operation exists; only the current coverage can be read. *(source: screens/P08-venue-back-office.yaml#BO-892 / contracts/satellite/workforce.yaml#getStaffingCoverage; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which operation generates the plan, and at what autonomy level (L2 Prepare is assumed)?** → Drawn default accepted: Draw the full flow with Generate and the comparison greyed "Planner not connected yet", current coverage live. *(decided by Chinmay, 2026-10-02; DEC-508 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| From | date picker | — | — | — | — | Sends `?from=` (required). | — |
| To | date picker | — | — | — | — | Sends `?to=` (required). | — |
| Venue | select field | — | — | — | — | Sends `?venueId=`. | — |
| Optimization objective | select field | — | — | — | — | Best coverage, minimise overtime, minimise labour cost, balance hours, minimise cross-venue movement, maximise skill match, continuity. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getStaffingCoverage` ?from |
| To | date picker | — | — | `getStaffingCoverage` ?to |
| Basis | segmented control | Minimum | Minimum · Forecast requirement · Higher of both | `getStaffingCoverage` ?basis |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period and venue**: From-to (required) and venue; the period defaults to next week. *(source: contracts/satellite/workforce.yaml#getStaffingCoverage)*
- **Objectives**: Ranked chips: Best coverage, Minimise overtime, Minimise labour cost, Balance employee hours, Minimise cross-venue movement, Maximise skill match, Prioritise continuity. A locked list beneath: "Always enforced - safety, compliance, mandatory qualifications". *(source: screens/P08-venue-back-office.yaml#BO-892)*
- **Demand basis**: Minimum / Forecast / Higher of both, with the forecast version named ("Forecast v12, 28 Sep"). *(source: contracts/satellite/workforce.yaml#getStaffingCoverage / DI-501)*

#### Outputs: what the screen shows and produces

**Shown**

**Staffing gaps (current roster)** (metric tile, from `getStaffingCoverage`): Summed; the AI-optimised side of the comparison has no read.

| Shows | Format | Notes |
|---|---|---|
| Gap | 1,234 | — |

**Coverage** (metric tile): The pack asks for coverage; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Coverage | text | not in the schema: `Coverage` |

**Overtime hours** (metric tile): The pack asks for overtime hours; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Overtime hours | text | not in the schema: `Overtime hours` |

**Projected labour cost** (metric tile): The pack asks for projected labour cost; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Projected labour cost | text | not in the schema: `Projected labour cost` |

**Projected saving** (metric tile): The pack asks for projected saving; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Projected saving | text | not in the schema: `Projected saving` |

**Current roster coverage** (data table, from `getStaffingCoverage`)

| Shows | Format | Notes |
|---|---|---|
| Date | 1 Oct 2026 | — |
| Label | text | — |
| From | text | — |
| To | text | — |
| Required | 1,234 | — |
| Severity | chip: Covered, Tight, Short, Blocking | — |

**Why this assignment** (detail panel): The pack's explanation ("Available, Level 3 Instructor, certification valid, language match, already at venue, no overtime").

| Shows | Format | Notes |
|---|---|---|
| Employee | text | not in the schema: `Employee` |
| Assignment | text | not in the schema: `Assignment` |
| Reasons | text | not in the schema: `Reasons` |
| Hard constraints satisfied | text | not in the schema: `Hard constraints satisfied` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Generate roster with AI (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Scenario comparison**: Current roster against AI optimised, as paired tiles: Coverage 94% to 100%, Overtime 22 h to 8 h, Staffing gaps 4 to 0, Cross-venue transfers 7 to 3, Projected labour cost AED 48,200 to AED 45,900, Projected saving AED 2,300. *(source: screens/P08-venue-back-office.yaml#BO-892)*
- **Recommended assignments**: Each proposed assignment with person, shift, match and a "Why" line ("Available, Level 3 instructor, certification valid, language match, already at venue, no overtime"). *(source: screens/P08-venue-back-office.yaml#BO-892)*
- **Current coverage**: Table of date, position, from-to, required, rostered, qualified, gap, severity - the gaps the plan is solving. *(source: contracts/satellite/workforce.yaml#/components/schemas/StaffingCoverage)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Generate roster with AI**: Produces a draft plan; nothing changes on the rota. *(source: screens/P08-venue-back-office.yaml#BO-892 / ADR-0050)*
- **Accept all / Accept selected / Modify / Reject / Regenerate with different priorities**: Accepted rows become Planned assignments (not published); the confirm counts them; publication stays a separate, approved step. *(source: screens/P08-venue-back-office.yaml#BO-892 / ADR-0050)*

**Data it reads**: `getStaffingCoverage` (onLoad, What the planner is optimising)

**Where the user goes next**

- → `BO-883` Workforce Roster Command Center: *Back to Workforce Roster Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workforce planner roster list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workforce planner roster untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workforce planner roster yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workforce planner roster are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **No feasible plan meets all hard constraints**: "Cannot cover Zone B 15:00-18:00 without breaking a rule - 1 lifeguard short." The gap stays; no rule-breaking suggestion is offered. *(source: screens/P08-venue-back-office.yaml#BO-892)*
- **Rota changed after the plan was generated**: Banner "The roster changed at 14:05; regenerate before accepting". *(source: designer default)*

#### Consistency with other screens

- Match `BO-883`: Opened from Run AI optimisation; returns there.
- Match `BO-891`: Cost and saving figures use the same basis.
- Match `BO-890`: An accepted plan must pass the same compliance check before publication.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
comparison:
  coverage: 94% to 100%
  overtime: 22 h to 8 h
  gaps: 4 to 0
  transfers: 7 to 3
  cost: AED 48,200 to AED 45,900
  saving: AED 2,300
recommendations:
- person: Layla Al Suwaidi
  assignment: Ski Instructor L3, Sat 10 Oct 14:00-16:00
  why: Available, Level 3, certification valid, English and Hindi, already at Summit Peaks, no overtime
- person: Hessa Al Marzooqi
  assignment: Lifeguard, Aqua Park Zone B, Sat 17 Oct 15:00-18:00
  why: Available, lifeguard certificate valid to Mar 2027, no overtime
```

#### Permissions

- `getStaffingCoverage` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.49 | System shall generate staffing shortage alerts. | Unified Operations Dashboard | CONTRACTED | `getStaffingCoverage` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI forecasting from historical bookings recommends staffing levels for upcoming periods (e.g. "you will need this many resources over the next week") so leave and availability can be planned. Analytics show total cost and revenue by resource and by event. *(client request · MoM 26 Aug 2026, 4.9 AI Optimization, Mobile App & Analytics · DI-501)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A45** Design the "Plan Your Adventure" itinerary-planner feature for the guest app, including group-sharing / invite-to-itinerary functionality *(Softlabs Design Team · High · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'plan your adventure')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-892` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS129 Resource Management Configuration Board 4.dc.html#bo-892`
- Workshop pack: Resource_Management_Configuration_Reference.pdf board 4
- Flow F267 *Resource Management Configuration board 4: Workforce Roster Command Center*, step 18: Works in AI Workforce Planner & Roster Optimization → Provide TICVAI's intelligent workforce-planning experience by automatically generating or optimizing operational rosters.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-892?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Generate roster with AI.
- [ ] Every transition is wired: `BO-883`.
- [ ] Every gated control is gated: `WORKFORCE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P08 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-030, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051, DI-052 (each is in the design inputs below).

**Workshop tracker rows about P08 as a whole** (1: 1 open, 0 closed). Open first; a closed row says where it went on 30 September.

- **S8** Venue Management back-end configuration wireframes *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*

## Design inputs from the client meetings

**What the client asked for in the meetings and design reviews, for these screens.** Apply every item. They are the client's own requirements and they are later than the reference files: where a reference design or a screen's fields disagree with an item here, the item wins. Newest first; where two items disagree, the newer one wins (anything a later meeting replaced is already left out). An **Open question** is not settled: build the default it states and keep it easy to change. The text in brackets is for traceability and, like everything else in this bundle, never appears on a screen.

### Everywhere, on every app

- Allam (platform-wide requirement): every calendar throughout the platform, not just maintenance, must support day, week and month views, with the day view further broken down by hour from a defined start hour through the day. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-907)*
- Minimise the number of separate screens an end user navigates: consolidate related information wherever it can reasonably be shown together, rather than mirroring every workshop board as its own screen. *(agreed · MoM 7 Sep 2026, 4.10 Screen consolidation / 5. Key Decisions · DI-671)*
- Region-configurable tax on pre-discount price (e.g. Egypt: AED 100 ticket with 20% off is paid at AED 80 but taxed on AED 100). Rounding must support up to three decimal places without dropping the third decimal where the currency requires it. *(agreed · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-598)*
- "Powered by TICVAI" is shown consistently across staff and guest-facing surfaces. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-297)*
- Full multi-language support (Arabic and others such as Chinese) consistent with the agreed i18n/RTL architecture. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-210)*
- The reference system is a functional reference only: its dated UI/UX is not to be replicated; TICVAI delivers equivalent depth with a modern, AI-friendly, easy-to-configure experience. *(agreed · MoM 7 Aug 2026, 23. Reference System Access & Documentation · DI-186)*
- Direction: modern, minimalistic, spacious, cross-device designs that still convey a sense of place (venue or park); Softlabs proposes two to three enhanced visual concepts for TICVAI to steer. *(agreed · MoM 3 Aug 2026, 11. Design Alignment & Team Input · DI-126)*
- Languages: English and Arabic at minimum, with Russian, Spanish and Mandarin. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-080)*
- Clarity first; reduce cognitive load (simple layouts, familiar patterns); consistency ("Use the system. Do not recreate."); accessibility; hierarchy (guide attention with contrast, spacing and visual weight); feedback (every action has a clear response). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Design Principles in Action · DI-051)*
- Standard components: search bar with Cmd+K; tabs (Overview, Events, Sales, Reports); pagination; badges (New, Pending, Sold Out, Completed); toggle (Off/On); dropdown; removable chip ("VIP x"). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Example UI Components · DI-050)*
- Spacing on an 8px base grid: 4, 8, 12, 16, 24, 32, 40, 48, 64, 80. Border radius scale 4, 8, 12, 16, 24px, consistent across the platform. Soft shadows: sm 0 1px 2px rgba(0,0,0,.05); md 0 4px 6px rgba(0,0,0,.08); lg 0 10px 15px rgba(0,0,0,.10); xl 0 20px 40px rgba(0,0,0,.14). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 6. Spacing / 7. Border Radius / 8. Shadows · DI-049)*
- Icons: line style, outline, 2px stroke, round corners, clean and consistent. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 5. Icons · DI-048)*
- Component principles: clarity first; consistent spacing on an 8px grid; meaningful colour (colours communicate status and guide the user); accessible by design; mobile ready (components adapt across all screen sizes). Components are consistent, flexible, accessible and composable. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Component principles · DI-045)*
- Empty states have a title, one explanatory line and one action: "No events yet / Create your first event to get started / Create Event"; "No data available / We couldn't find anything to show here / Refresh". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Empty States · DI-044)*
- Notification list: status icon, title, one-line detail and relative time (e.g. "Payment received ... 2m ago", "High demand detected ... 10m ago"), with "View all notifications". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Notifications · DI-042)*
- Forms: label above field; text input, select ("Choose an option"), date picker, toggle, checkbox. Input states: Default, Focused, Filled, Disabled and Error with inline message (e.g. "This field is required"). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Forms; 08 Design System (p8) - 4. Inputs · DI-040)*
- Card types: event card (title, date and time, venue, "From 120.00 AED"); KPI card (label, value, delta, "vs last 7 days"); onboarding checklist card ("3 of 6 completed": Create Event, Add Staff, Configure Seating, Connect Payment). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Cards · DI-038)*
- Button hierarchy Primary, Secondary, Tertiary (text) and Icon buttons, each with Default, Hover, Pressed and Disabled states. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Buttons; 08 Design System (p8) - 3. Buttons · DI-036)*
- Regardless of the module a user is working in, the experience should feel like one product, not a collection of separate applications. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) · DI-034)*
- DO: focus on clarity and hierarchy, use clear simple interactive elements, give relevant information at a glance (card example: "Annual Membership / All Venues / 4.4 (388) / BESTSELLER"). DON'T: clutter and overload (e.g. "-10% NEW PROMO AED 450.00 !!! BOOK NOW!!!"), complex forms and flows, hard-to-read data visualisations. *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - DO / DON'T · DI-033)*
- Eight principles on every screen: User-Centric, AI-First, Simple & Clear (clean layouts, clear hierarchy, minimal noise), Fast & Efficient (optimised for quick actions), Reliable & Secure (permissions, data protection), Data-Driven (data visual, actionable, easy to understand), Scalable, Consistent (same patterns, components and interactions across the ecosystem). *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - Our Design Principles · DI-032)*
- Accessibility: high contrast, readable text, keyboard navigation and inclusive components throughout; WCAG AA standards minimum ("Design for everyone"). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Better Accessibility; 06 Component principles (p6); 08 Design principles in action (p8) · DI-029)*
- AI everywhere: AI insights, recommendations and smart assistance are embedded across the platform, not hidden. AI is not an add-on: it assists, predicts, recommends and automates. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - How TICVAI improves this concept; 05 Design Principles (p5) - 2. AI-First · DI-027)*
- Global Search: prominent, AI-powered search that finds anything, in the top bar with a Cmd+K shortcut (placeholder e.g. "Search events, customers, orders, venues or ask AI..."). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, item 1; 08 Design System (p8) - Search Bar · DI-025)*
- Visual direction: Purposeful (every element has a clear purpose), Consistent (one visual system across all modules and devices), Clear (easy to scan, understand and act on), Modern. Key takeaway: clean, modern, product-first layout with clear hierarchy and minimal visual noise; deep, modern, trustworthy; built for enterprise scale. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) · DI-024)*
- The brand is presented consistently across Web Platform, Mobile App and Admin Portal (and print). Ticvai identity, colours and typography are applied consistently across all screens and devices. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand in action; 03 Visual Direction (p3) - Consistent Branding · DI-023)*
- Copy is Professional, Friendly, Clear, Confident, Concise and Helpful. Avoid jargon, overly technical language, clutter, outdated language and complexity. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand voice · DI-022)*
- Brand personality: Modern, AI-First, Enterprise, Premium, Reliable, Minimal, Scalable, Human-Centred. Visual essence: intelligent and forward-thinking, clean and minimal, trustworthy and secure, modern and timeless, scalable and flexible. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand personality / Visual essence · DI-021)*
- Arabic is a core requirement, not later localisation: full Arabic RTL across web, mobile, POS, reports, emails, WhatsApp, SMS, notifications, tickets and receipts, and administrative interfaces. *(agreed · MoM 28 Jul 2026, 27. Internationalisation and Arabic Support · DI-019)*

### Across P08 Venue Management

- Qossai: configuration screens should consolidate related functionality, potentially merging 3-4 previously separate screens into one, rather than the repetitive one-screen-per-concept pattern of the AI-built reference system. *(agreed · MoM 24 Sep 2026, 4.5 Screen Consolidation Philosophy · DI-987)*
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- Custom data-capture fields ("data mask") at account, event, extended-ticket and product level: field types text, dropdown, radio, true/false; multi-language labels; validation (min/max length, required/optional); reusable value lists (e.g. country list). Standard fields come out of the box. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-155)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Allam: queue management is built into the system (not third-party) so traffic entering the site can be throttled from the back office itself. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-060)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Documentation deliverable includes user guides and help content; the preview shows a TICVAI Help Center with categories (Getting Started, Events, Tickets, Orders, Payments, Memberships, Access Control, Reports, Integrations), a "Welcome to TICVAI" getting-started article and Quick Links (Create an Event, Set Pricing, Manage Access, View Reports). *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - What We Deliver / Key Deliverables Preview · DI-052)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Back-office shell: collapsible left sidebar with Overview, Events, Tickets, Orders, Customers, Memberships, Access Control, POS, Reports, Analytics, AI Assistant, Settings, and the signed-in user (name, role) at the bottom; top bar with global search (Cmd+K), current time and date, Notifications with unread dot, and user menu. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - navigation shell · DI-030)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*
- Back-office controls for the waiting room: configurable maximum active users and admission intervals, set per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-017)*

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"amendAttendance": {"method":"POST","path":"/attendance/{recordId}/amend","contract":"workforce","summary":"A supervisor corrects a record","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"createRotaAssignment": {"method":"POST","path":"/rota-assignments","contract":"workforce","summary":"Put someone on the rota","permission":"WORKFORCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RotaAssignment","responds":"RotaAssignment"},
"getLabourCost": {"method":"GET","path":"/labour-cost","contract":"workforce","summary":"Rostered and actual labour cost against budget","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"LabourCostRow"},
"getStaffingCoverage": {"method":"GET","path":"/staffing-coverage","contract":"workforce","summary":"Where the rota is short, and by how much","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true},{"name":"venueId","in":"query","required":null},{"name":"basis","in":"query","required":null}],"requestBody":null,"responds":"StaffingCoverage"},
"listAlerts": {"method":"GET","path":"/alerts","contract":"reporting","summary":"What is currently wrong","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"itemId","in":"query","required":null}],"requestBody":null,"responds":"Alert"},
"listAttendance": {"method":"GET","path":"/attendance","contract":"workforce","summary":"Who was here","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"date","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"exceptionsOnly","in":"query","required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"listLabourBudgets": {"method":"GET","path":"/labour-budgets","contract":"workforce","summary":"Labour budgets, per venue, department and period","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOpenShifts": {"method":"GET","path":"/shift-marketplace","contract":"workforce","summary":"Shifts offered back, and who may take them","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"OpenShift"},
"listRotaAssignments": {"method":"GET","path":"/rota-assignments","contract":"workforce","summary":"The rota","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"departmentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShiftSwapRequests": {"method":"GET","path":"/shift-swaps","contract":"workforce","summary":"Swap requests and their state","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ShiftSwap"},
"recordAttendance": {"method":"POST","path":"/attendance/clock","contract":"workforce","summary":"Clock in, clock out, or take a break","permission":"ATTENDANCE_RECORD","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AttendanceRecord"},
"setAlertRule": {"method":"PUT","path":"/alert-rules","contract":"reporting","summary":"Watch a metric and tell somebody","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AlertRule","responds":"AlertRule"},
"setLabourBudget": {"method":"PUT","path":"/labour-budgets","contract":"workforce","summary":"Set the labour budget for a venue, department and period","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LabourBudget","responds":"LabourBudget"},
"setStaffingRules": {"method":"PUT","path":"/staffing-rules","contract":"workforce","summary":"Minimum cover, working-hour limits and overtime","permission":"WORKFORCE_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StaffingRules","responds":"StaffingRules"},
"validateWorkforceCompliance": {"method":"GET","path":"/workforce-compliance","contract":"workforce","summary":"Where the rota breaks a rule","permission":"WORKFORCE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"WorkforceComplianceFinding"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Alert": {"type":"object","x-ticvai-persistence":"reporting.alert","description":"A raised alert. **Acknowledged rather than dismissed** — CF-134 asked for it markable, and the difference is that an acknowledgement records who saw it.\n","required":["id","ruleId","raisedAt","severity","status"],"properties":{"id":{"type":"string","format":"uuid"},"ruleId":{"type":"string","format":"uuid"},"ruleName":{"type":"string","description":"`AlertRule.name` as it stood when the alert was raised. **The line a person reads** — a list of rule ids is not an alert panel, and a screen should not need `listAlertRules` to label one.\n"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"The rule's metric, carried so the alert says what went out of range."},"raisedAt":{"type":"string","format":"date-time"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"status":{"$ref":"#/components/schemas/AlertStatus"},"observedValue":{"$ref":"#/components/schemas/MetricValue"},"threshold":{"$ref":"#/components/schemas/MetricValue"},"scopePath":{"type":"string"},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation the reading was taken for, where the metric is measured per workstation (`salesByWorkstation`). Null otherwise. `listAlerts` filters on it."},"shiftId":{"type":"string","format":"uuid","nullable":true,"description":"The till shift (`orders.pos_shift`) the reading belongs to, where it was taken for a workstation with a shift open. Null otherwise. `listAlerts` filters on it."},"itemId":{"type":"string","format":"uuid","nullable":true,"description":"The inventory item the reading is about, where the metric is measured per item (`stockAgeing`, `stockTurnover`, `wastageRate`, `inventoryValuation`). Null otherwise. **What a replenishment screen prefills a requisition from.**\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true},"acknowledgementNote":{"type":"string","maxLength":300,"nullable":true,"description":"The `note` given to `acknowledgeAlert`. Kept, because an acknowledgement that says what is being done about it is the one escalation can skip."},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"description":"**Set when the metric returns to range, automatically.** An alert that only a person can close is an alert list that only grows.\n"},"escalatedAt":{"type":"string","format":"date-time","nullable":true,"description":"Where `VenueSettings.alerting.escalateAfterMinutes` passed with no acknowledgement. **A critical alert nobody acknowledged is the case escalation exists for.**\n"}}},
"AlertRule": {"type":"object","x-ticvai-persistence":"reporting.alert_rule","description":"BL-152, CF-134. **Six contracts detect their own trouble and none told a person.**\nFive sections ask for this and it is the same gap as `MessageTrigger`, seen from the operational side — **that one tells a guest something happened; this one tells an operator something is wrong.**\n**A threshold that nobody is watching is a threshold nobody set.** 6.1.57 wants an exception when a KPI leaves range, and an exception that arrives in a nightly report is an exception nobody acted on.\n","required":["id","name","metric","comparator","threshold","severity","isActive","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"metric":{"allOf":[{"$ref":"#/components/schemas/MetricSource"}],"description":"**From the closed set**, so a rule cannot watch something nothing produces — the same discipline `MetricSource` exists for.\n"},"comparator":{"type":"string","enum":["above","below","outsideRange","changesBy","equals"]},"threshold":{"$ref":"#/components/schemas/MetricValue"},"thresholdUpper":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true,"description":"**Required when `comparator` is `outsideRange`** (decided 28 September, audit R158): the range is `threshold` to `thresholdUpper`, and a rule missing either, or with the upper not above the lower, is refused by `setAlertRule` with 400. Ignored for every other comparator.\n"},"windowMinutes":{"type":"integer","default":15,"description":"**The window is what stops an alert firing on noise.** A queue that spikes for ninety seconds is not a queue that needs a manager, and a rule with no window is a rule somebody mutes within a week.\n"},"severity":{"$ref":"#/components/schemas/AlertSeverity"},"deliverTo":{"type":"array","description":"CF-134. **The dashboard panel is the default and the only one that always applies.** Email or WhatsApp where the matrix names them — an operational alert arriving by email is an alert nobody sees in time.\n","items":{"type":"string","enum":["dashboardPanel","email","whatsapp","sms","push"]},"x-ticvai-push-note":"**`push` added 29 September** (6.1.56, 18.1.5, build pass): delivered to every staff-app handset registered for a recipient (tenancy `RegisteredDevice`, kind `mobileHandset`, with a push token). It is how a daily revenue alert reaches a manager's phone, which a panel on a web dashboard does not.\n"},"recipientRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"cooldownMinutes":{"type":"integer","default":30,"description":"**How long before the same rule may fire again.** Without it, a metric hovering on a threshold produces forty alerts an hour and the panel becomes something people close.\n"},"isActive":{"type":"boolean"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**\n\n**Required, and it is the write target.** `setAlertRule` has no id in its path and a caller may hold several venues, so the rule names the venue it watches here — inside the caller's scope, or the write is refused."}}},
"AlertSeverity": {"type":"string","description":"How urgent an alert rule's breach is. Shared by `AlertRule`, `Alert` and the `listAlerts` filter.","enum":["info","warning","critical"]},
"AlertStatus": {"type":"string","description":"Where a raised alert is. Shared by `Alert` and the `listAlerts` filter.","enum":["raised","acknowledged","resolved","expired"]},
"AttendanceAmendment": {"type":"object","x-ticvai-persistence":"workforce.attendance_amendment","description":"One correction to an attendance record, appended by `amendAttendance` and never updated (decided 28 September, audit R129 (7)).\n","required":["id","attendanceRecordId","amendedByPrincipalId","amendedAt","occurredAtBefore","occurredAtAfter","reason"],"properties":{"id":{"type":"string","format":"uuid"},"attendanceRecordId":{"type":"string","format":"uuid"},"amendedByPrincipalId":{"type":"string","format":"uuid"},"amendedAt":{"type":"string","format":"date-time"},"occurredAtBefore":{"type":"string","format":"date-time","description":"The record's time before this correction."},"occurredAtAfter":{"type":"string","format":"date-time","description":"The time this correction set (`correctedAt` on the request)."},"reason":{"type":"string","maxLength":300}}},
"AttendanceRecord": {"type":"object","x-ticvai-persistence":"workforce.attendance","required":["id","principalId","kind","occurredAt"],"properties":{"id":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["clockIn","clockOut","breakStart","breakEnd"]},"occurredAt":{"type":"string","format":"date-time","description":"Device time — when it happened."},"recordedAt":{"type":"string","format":"date-time","description":"When the server received it. **Both are kept**: a steward clocking in offline at a gate is not late because the sync was.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true},"latitude":{"type":"number","nullable":true},"longitude":{"type":"number","nullable":true},"isAmended":{"type":"boolean","readOnly":true},"amendedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who made the latest amendment. The full history is `amendments` (audit R129 (7))."},"amendmentReason":{"type":"string","nullable":true,"readOnly":true,"description":"The latest amendment's reason. The full history is `amendments` (audit R129 (7))."},"originalOccurredAt":{"type":"string","format":"date-time","nullable":true,"description":"**The original is never overwritten.** Attendance feeds pay, and a record that can be quietly rewritten is not evidence.\n"},"amendments":{"type":"array","readOnly":true,"description":"**Every correction, oldest first, one row each** (decided 28 September, audit R129 (7)). A single set of amendment columns holds only the last one, and the second correction to a record would erase the evidence of the first.\n","items":{"$ref":"#/components/schemas/AttendanceAmendment"}},"exception":{"type":"string","nullable":true,"enum":["late","earlyLeave","missingClockOut","noShow","outOfGeofence","unscheduled"],"description":"Computed against the rota. Null where the record matches what was expected."}}},
"LabourBudget": {"type":"object","x-ticvai-persistence":"workforce.labour_budget","description":"**The labour budget a general manager is held to, per venue, department and period** (resource board 4.9; data model for the agreed operations, 29 September). `getLabourCost` compares rostered and actual cost against it (`LabourCostRow.budget`). A null `departmentId` is the whole venue's budget. Periods for one venue and department do not overlap. Written by `setLabourBudget`, listed by `listLabourBudgets` (decided 29 September, writers pass).","required":["id","venueId","periodStart","periodEnd","budgetAmount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"periodStart":{"type":"string","format":"date","description":"First day of the period, in the Region's time zone"},"periodEnd":{"type":"string","format":"date","description":"Last day of the period, in the Region's time zone"},"budgetAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scopePath":{"type":"string"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"LabourCostRow": {"type":"object","description":"Resource board 4.9. **Rostered and actual diverge every day.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"rosteredHours":{"type":"number"},"actualHours":{"type":"number"},"overtimeHours":{"type":"number"},"rosteredCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actualCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"budget":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variancePercent":{"type":"number"},"headcount":{"type":"integer"}}},
"MetricSource": {"type":"string","description":"**A named metric with a verified source.** BL-053, 75 requirement rows.\n`reporting` is a generic builder, and **a generic builder makes every reporting requirement look covered** — it will happily assemble a report over data nobody produces. That is the shape to watch across the whole walk, and this enum is the answer to it: each value below was checked against the schema before being named.\n| Metric | Source | |---|---| | `occupancy` | `catalogue.channel_capacity.sold` and `leased` against `capacity` | | `capacityUtilisation` | `catalogue.channel_capacity.remaining` over the same window | | `admissionRate` | `access.scan_event.outcome`, in-direction | | `noShowRate` | Entitlements issued against scans that never arrived | | `conversion` | `orders.cart` against `orders.sales_order` | | `salesByOperator` | `orders.sales_order.principal_id` | | `salesByWorkstation` | The workstation on the shift that took it | | `waitTime` | `queue.waiting_guest.estimated_call_at` against `called_at` | | `throughput` | `queue.waiting_guest` completions per hour | | `abandonmentRate` | Queue entries that left before being called |\n**`salesByInstructor` was deliberately absent from the first cut** because it needed the staff-assignment link CL-01 covers. It was added on 18 August once `resources.Resource` produced it — see `x-ticvai-extension-note` below. Naming a metric with no source is still the defect this enum exists to prevent.\n**Money-valued metrics are listed in `x-ticvai-money-valued`.** A reading or threshold on one of them is a `Money`, never a float (`MetricValue`).\n","enum":["occupancy","capacityUtilisation","admissionRate","noShowRate","conversion","salesByOperator","salesByWorkstation","waitTime","throughput","abandonmentRate","inventoryValuation","stockTurnover","stockAgeing","wastageRate","resaleVolume","resaleCommission","salesByInstructor","resourceUtilisation","allocationUtilisation","channelAllocationBurn","membershipChurn","membershipRenewalRate","supplierDeliveryPerformance","revenuePerEntitlement","revenuePerVisitor","assetDowntime","meanTimeToRepair","challengeCompletionRate","attributedRevenue","loyaltyActiveMembers","loyaltyTierDistribution","loyaltyPointsLiability","loyaltyBreakageRate","loyaltyMemberRetention","challengeParticipationRate","gamificationLoyaltyImpact","gamificationMembershipImpact","gamificationRetention","accreditationApplications","accreditationTimeToDecision","accreditationCredentialsIssued","accreditationActiveHolders","accreditationRenewalsDue","staffingShortfall","grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings"],"x-ticvai-money-valued":["grossSales","discounts","refunds","netRevenue","recognisedRevenue","deferredRevenue","taxCollected","takings","inventoryValuation","resaleCommission","revenuePerEntitlement","revenuePerVisitor","attributedRevenue","loyaltyPointsLiability"],"x-ticvai-extended-29-september":"**Fourteen metrics added 29 September (build pass)**, each checked against the schema of the contract that produces it.\n\n| Metric | Source | Requirement | |---|---|---| | `loyaltyActiveMembers` | `marketing.loyalty_position` members with a `marketing.loyalty_points` movement in the period | 5.4.27 | | `loyaltyTierDistribution` | `marketing.loyalty_position.tier_id` against `marketing.programme_tier`, members per tier | 5.4.27 | | `loyaltyPointsLiability` | the balance of `ledger.journal_line` on each programme's `pointsLiabilityAccountId`, where points post on accrual and release on redemption or expiry | 5.4.27 | | `loyaltyBreakageRate` | `marketing.loyalty_points` expiry movements over points earned, in the period | 5.4.27 | | `loyaltyMemberRetention` | members with a movement in the previous period who also have one in this period | 5.4.27 | | `challengeParticipationRate` | distinct `marketing.challenge_progress.subject_id` over active loyalty members | 22.6.20 | | `gamificationLoyaltyImpact` | points earned per member, challenge participants against non-participants (`marketing.loyalty_points` split by `marketing.challenge_progress`) | 22.6.20 | | `gamificationMembershipImpact` | joins and renewals in `identity.customer_membership`, participants against non-participants | 22.6.20 | | `gamificationRetention` | return visits (`access.scan_event`, in-direction) of participants against non-participants | 22.6.20 | | `accreditationApplications` | `accreditation.application` by `status` | 12.1.50 | | `accreditationTimeToDecision` | `accreditation.application.decided_at` minus `submitted_at` | 12.1.50 | | `accreditationCredentialsIssued` | `accreditation.credential.issued_at` | 12.1.50 | | `accreditationActiveHolders` | `accreditation.holder` `active`, by `category_code` | 12.1.50 | | `accreditationRenewalsDue` | `accreditation.holder.valid_to` inside `accreditation.validity.renewal_window_days` | 12.1.50 |\n\n**`staffingShortfall` added the same evening (build pass, group G2; 8.2.49)**: the largest gap in the window between the staff rostered and the staff the forecast requires, per venue and position, from `workforce.forecast_requirement` (the handed-over AI staff requirement) against `workforce.rota_assignment` and `workforce.open_shift`, computed as `workforce.getStaffingCoverage` with `basis` `forecastRequirement`. An `AlertRule` on it with `comparator` `above` and `threshold` 0 is the staffing shortage alert; `windowMinutes` looks ahead rather than back for this metric (the rota for the coming window), and `cooldownMinutes` stops one short shift alerting every quarter hour.\n\n**Points issued, points redeemed, campaign performance and reward redemption were already served** by the `loyalty` and `campaigns` sources, and challenge completion and revenue attribution by `challengeCompletionRate` and `attributedRevenue`.\n","x-ticvai-extended-2-october":"**Eight finance measures added 2 October 2026** (Chinmay; CHG-FIN-007, CHG-FIN-010), each with the source and formula of the seeded KPI of the same code in `ReportingSystemKpi`: `grossSales`, `discounts`, `refunds`, `netRevenue`, `recognisedRevenue`, `deferredRevenue`, `taxCollected` and `takings`, so an alert rule can watch them (a refund spike, takings below a target). Formulas are the D-185 default; client finance sign-off is pending.","x-ticvai-money-valued-note":"**`salesByOperator`, `salesByWorkstation` and `resaleVolume` are not listed because the package does not say whether they count sales or sum their value.** Until that is decided, a rule on them carries a plain number.\n","x-ticvai-extended":"18 August 2026","x-ticvai-extension-note":"**Nineteen metrics added when their upstream models landed**, which is how BL-053 was always going to close — not by changing `reporting` but by building the things it wanted to report on.\n`inventoryValuation`, `stockTurnover`, `stockAgeing` and `wastageRate` came from `inventory.StockBatch`; `resaleVolume` and `resaleCommission` from `orders.ResaleListing`; **`salesByInstructor` from `resources.Resource`, which was the one metric this enum deliberately refused to name in the morning** because nothing produced it. `allocationUtilisation` from `PartnerUser` and `ChannelListing`, `membershipChurn` from `Journey`, `supplierDeliveryPerformance` from `ProductionRun`, `assetDowntime` and `meanTimeToRepair` from `WorkOrder.downtimeMinutes`, `challengeCompletionRate` from `ChallengeProgress`, `attributedRevenue` from `AttributionTouch`.\n**Each was checked against the schema before being named.** That rule has not changed — naming a metric with no source is the defect this enum exists to prevent.\n"},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"OpenShift": {"type":"object","x-ticvai-persistence":"workforce.open_shift","description":"Resource board 4.6. **How a gap gets filled at nine on a Friday without a manager ringing round.**\n","properties":{"id":{"type":"string","format":"uuid"},"rotaAssignmentId":{"type":"string","format":"uuid","nullable":true},"shiftTemplateId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"releasedBy":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"requiredQualifications":{"type":"array","items":{"type":"string"}},"eligiblePrincipalCount":{"type":"integer","readOnly":true},"incentiveRateMultiplier":{"type":"number","nullable":true},"status":{"type":"string","enum":["open","claimed","pendingApproval","filled","expired","withdrawn"]},"claimedBy":{"type":"string","format":"uuid","nullable":true},"claimedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RotaAssignment": {"type":"object","x-ticvai-persistence":"workforce.rota_assignment","required":["principalId","venueId","startsAt","endsAt","position"],"properties":{"overtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"description":"BL-044, 1.2.83. **UAE labour law limits working hours and mandates rest periods**, and nothing in the package counted either. Derived from attendance against the shift.\n"},"restPeriodBefore":{"type":"integer","nullable":true,"description":"Minutes since the previous shift ended. **The check that stops a closing shift followed by an opening one**, which is legal in most places and unsafe in all of them.\n"},"breachesWorkingHourLimit":{"type":"boolean","default":false,"readOnly":true,"description":"**Flagged at assignment, not discovered at payroll.** A rota that breaches a statutory limit is a rota somebody has to redo, and finding out a month later means it was worked.\n"},"labourCost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**Cost at the point of scheduling.** A manager building a rota without seeing its cost is a manager who finds out from finance.\n"},"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string","readOnly":true},"venueId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"position":{"type":"string","description":"What they are rostered to do — gate steward, cashier, lifeguard, technician. **Most positions never touch a till**, which is why a rota assignment is not a shift.\n**A position code, not a label.** It is the same value as `StaffingRules.minimumCover[].positionCode`, `OpenShift.positionCode` and `StaffingCoverage.positionCode`: coverage counts rostered people per position, so an assignment spelled differently from the rule it fills is counted against nothing and the gap stays open. Tenant-defined, which is why it is not an enum here.\n"},"requiredRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Checked on assignment. A rota naming someone unqualified is a rota that gets overridden."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"Where the position needs a till. **The link between a rota and a cash session**, without merging the two.\n"},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time"},"status":{"$ref":"#/components/schemas/RotaStatus"},"breakMinutes":{"type":"integer","nullable":true},"note":{"type":"string","nullable":true}}},
"RotaStatus": {"type":"string","enum":["planned","published","confirmed","swapPending","cancelled","completed","noShow"]},
"ShiftSwap": {"type":"object","x-ticvai-persistence":"workforce.shift_swap","required":["id","assignmentId","fromPrincipalId","toPrincipalId","status"],"properties":{"id":{"type":"string","format":"uuid"},"assignmentId":{"type":"string","format":"uuid"},"fromPrincipalId":{"type":"string","format":"uuid"},"toPrincipalId":{"type":"string","format":"uuid"},"status":{"type":"string","enum":["awaitingPeer","awaitingApproval","approved","rejected","withdrawn"],"description":"**Both parties before the supervisor.** A swap approved against someone who never agreed is a gap in the rota nobody notices until the shift starts.\n"},"approvalRequestId":{"type":"string","nullable":true,"description":"Routed through `approvals` rather than a second mechanism here."},"reason":{"type":"string","nullable":true},"requestedAt":{"type":"string","format":"date-time"}}},
"StaffingCoverage": {"type":"object","description":"Resource board 4.4. **The gap is the product.**","properties":{"date":{"type":"string","format":"date"},"venueId":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"label":{"type":"string"},"from":{"type":"string"},"to":{"type":"string"},"required":{"type":"integer"},"rostered":{"type":"integer"},"qualified":{"type":"integer","description":"**A position filled by somebody not qualified for it is still a gap.**"},"gap":{"type":"integer"},"severity":{"type":"string","enum":["covered","tight","short","blocking"]},"openShiftIds":{"type":"array","items":{"type":"string","format":"uuid"}},"basisApplied":{"type":"string","enum":["minimum","forecastRequirement"],"description":"Which figure `required` is for this row. With `higherOfBoth`, the larger; with `forecastRequirement` and no handed-over requirement for the period, `minimum`."},"minimumRequired":{"type":"integer","nullable":true,"description":"The configured minimum for the position and window."},"forecastRequired":{"type":"number","nullable":true,"description":"The forecast staff requirement (p50) for the position and window, from `workforce.forecast_requirement`. Null where none was handed over."},"forecastRequiredP90":{"type":"number","nullable":true,"description":"The busy-case requirement, for planning to the busy case."},"forecastVersionId":{"type":"string","format":"uuid","nullable":true,"description":"The AI forecast version the requirement is bound to (AIP-067), so a manager can open the forecast behind it."}}},
"StaffingRules": {"type":"object","x-ticvai-persistence":"workforce.staffing_rules + workforce.position_requirement","description":"Resource board 4.3. **A safety rule before it is a cost rule.**","properties":{"minimumCover":{"type":"array","description":"**Minimum staffing per position, venue and time window, with the qualifications it requires**: the rows of `workforce.position_requirement` (data model for the agreed operations, 29 September). `getStaffingCoverage` measures the rota against them; before this they were an array with no table, so no minimum was stored.","items":{"type":"object","required":["id","positionCode","minimumHeadcount"],"properties":{"id":{"type":"string","format":"uuid"},"positionCode":{"type":"string"},"label":{"type":"string"},"venueId":{"type":"string","format":"uuid","nullable":true},"attractionId":{"type":"string","format":"uuid","nullable":true},"minimumHeadcount":{"type":"integer","minimum":0},"daysOfWeek":{"type":"array","nullable":true,"description":"Days the minimum applies; absent means every day the venue is open","items":{"type":"string","enum":["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]}},"startsAt":{"type":"string","nullable":true,"description":"Start of the time window, local time (HH:MM) as `ShiftTemplate.startsAt`; absent means opening"},"endsAt":{"type":"string","nullable":true,"description":"End of the time window, local time (HH:MM); absent means closing"},"requiredQualifications":{"type":"array","items":{"type":"string"}},"appliesWhenOpen":{"type":"boolean","default":true},"blocksOperation":{"type":"boolean","default":true,"description":"**A ride requiring two operators cannot run with one.** Where this is true the attraction closes rather than running short.\n"}}}},"maximumHoursPerDay":{"type":"integer","nullable":true},"maximumHoursPerWeek":{"type":"integer","nullable":true},"minimumRestHours":{"type":"integer","nullable":true},"maximumConsecutiveDays":{"type":"integer","nullable":true},"overtime":{"type":"object","properties":{"allowed":{"type":"boolean","default":true},"afterHoursPerWeek":{"type":"integer","nullable":true},"rateMultiplier":{"type":"number","nullable":true},"requiresApproval":{"type":"boolean","default":true}}},"minimumAgeForNightShift":{"type":"integer","nullable":true},"defaultIncentiveRateMultiplier":{"type":"number","nullable":true,"minimum":1,"description":"**What an open shift pays above base when it is released.** Added 22 September: `workforce.open_shift.incentive_rate_multiplier` was set per shift with nothing behind it, so two identical shifts could price differently and record no reason. The shift still carries its own value — **as the snapshot**, the rule-and-record split `payments.fee_rule` and `orders.order_fee` use — and this is where it comes from.\n**Top-level rather than beside `overtime`** so the value is its own column. Nested in an object it would be a key inside a JSON blob, which nothing can index, constrain or pair to the shift that uses it.\n"},"maximumIncentiveRateMultiplier":{"type":"number","nullable":true,"minimum":1,"description":"**The ceiling on an incentive.** A shift nobody claims is the moment somebody raises the multiplier in a hurry — the same reason `maximumDailyCharge` bounds a late fee."},"incentiveApprovalAbove":{"type":"number","nullable":true,"minimum":1,"description":"**Above this multiplier a second person approves the release.** Routed as an approval, not a boolean — `overtime.requiresApproval` beside it is one of 26 approval flags across the contracts that no approval kind, matrix row or SLA reaches."},"scopePath":{"type":"string"}}},
"WorkforceComplianceFinding": {"type":"object","description":"Resource board 4.8. **Checked before the rota is published, not in an inspection.**","properties":{"code":{"type":"string","enum":["expiredQualification","missingQualification","exceededDailyHours","exceededWeeklyHours","insufficientRest","missedBreak","consecutiveDaysExceeded","underAgeNightShift","belowMinimumCover"]},"severity":{"type":"string","enum":["breach","warning"]},"principalId":{"type":"string","format":"uuid","nullable":true},"principalName":{"type":"string","nullable":true},"date":{"type":"string","format":"date","nullable":true},"detail":{"type":"string"},"rotaAssignmentIds":{"type":"array","items":{"type":"string","format":"uuid"}}}}
}
```
