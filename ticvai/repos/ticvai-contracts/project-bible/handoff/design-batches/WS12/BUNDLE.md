# WS12 — Access Control board 12

**10 screens · 16 operations · 23 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `REPORT_SCHEDULE, REPORT_VIEW_VENUE, SCOPE_VIEW`. A control nobody can use must say so,
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
| `BO-254` | Access Monitoring & Analytics Command Center | B–D | 0 | 300 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `BO-255` | Live Venue Occupancy & People Counting | B–D | 0 | 0 | 6 | 0 | 4 | 0 | — | notStarted (generated) |
| `BO-256` | Graphical Access Map & Live Gate Performance | B–D | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-257` | Attendance & Admission Analytics | B–D | 2 | 18 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-258` | Entry, Exit, Re-entry & Crossover Analytics | B–D | 0 | 12 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `BO-259` | Throughput, Queue & Validation Performance Analytics | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (generated) |
| `BO-260` | Validation Outcome & Rejection Analytics | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-261` | Guest Dwell Time, Length of Stay & Attraction Flow | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `BO-262` | Access Reports, Scheduled Reporting & Data Export | B–D | 2 | 0 | 6 | 9 | 0 | 0 | — | notStarted (generated) |
| `BO-263` | AI Access Intelligence, Forecasting & Executive Insights | B–D | 0 | 16 | 6 | 1 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**BO-255, BO-256, BO-258, BO-260, BO-262, BO-263 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-254` Access Monitoring & Analytics Command Center

**Provide a single executive and operational overview of access performance across all TICVAI-controlled venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/access-monitoring-analytics-command-center-bo-254` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Board 12 hub, the management view of access across every venue the user can see: fourteen global KPI tiles (admissions, entries, exits, currently in venue, re-entries, crossovers, group admissions, Fast Pass uses, valid and rejected scans, intervention rate, average validation time, active gates, offline devices), a venue comparison and an AI operations summary, with tiles into BO-255 to BO-263. The one thing to get right: this is where management watches and analyses; live operational action stays on board 9 (BO-224), so the hub has no operational buttons.

**Known correction pending (do not draw the wrong version)**

- **The tile "Seconds" and the venue table "Every access monitoring analytics" with no columns** Why: The tile is Average validation time (seconds is its unit); the table is Venue comparison with five columns (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-254 / contracts/spine/access.yaml#/components/schemas/AccessMonitoringAnalyticsCommandCenterViewSummary; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Validation success is returned (validationSuccessRate) but not drawn** Why: It is one of the pack's four headline figures. *(source: screens/P08-venue-back-office.yaml#BO-254 / contracts/spine/access.yaml#listAccessMonitoring; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The AI operations summary has no field** Why: The pack shows it on the hub; the read returns no sentence. *(source: screens/P08-venue-back-office.yaml#BO-254; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **The pack says "across all TICVAI-controlled venues" but the read is venue-scoped; is this hub tenant-wide?** → Drawn default accepted: Tenant-wide when the switcher is on All venues, rows per venue; one venue selected shows its parks. *(decided by Chinmay, 2026-10-02; DEC-262 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period and venue filter**: Today by default (live), with Yesterday, Last 7 days and a date range; venues limited to the user's scope. *(source: DI-061 / designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Total Admissions Today** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Entries** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Exits** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Currently In Venue** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Re-entries** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Crossovers** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Group Admissions** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Fast Pass Uses** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Valid Scans** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Rejected Scans** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Intervention Rate** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Seconds** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Active Gates** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Offline Devices** (metric tile, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**Every access monitoring analytics** (data table, from `listAccessMonitoring`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Venue | text | — |
| Venue name | text | — |
| Venue entries | 1,234 | — |
| Venue in venue | 1,234 | — |
| Venue rejected rate | 12.5% | Percent |
| Venue throughput per minute | 1,234.5 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Total admissions today | 1,234 | Total Admissions Today |
| Entries | 1,234 | Entries |
| Exits | 1,234 | Exits |
| Currently in venue | 1,234 | Currently In Venue |
| Re entries | 1,234 | Re-entries |
| Crossovers | 1,234 | Crossovers |
| Group admissions | 1,234 | Group Admissions |
| Fast pass uses | 1,234 | Fast Pass Uses |
| Valid scans | 1,234 | Valid Scans |
| Rejected scans | 1,234 | Rejected Scans |

**The selected access monitoring analytics** (detail panel): The pack groups this record's detail under its own headings: “TOTAL ADMISSIONS”, “CURRENTLY IN VENUE”, “Venue Comparison”.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **KPI tiles**: Fourteen metric tiles with deltas against the same day last week (VO-R02); the hero row repeats the pack's four headline figures large - TOTAL ADMISSIONS 42,684, CURRENTLY IN VENUE 18,427, VALIDATION SUCCESS 97.8%, AVG. VALIDATION 0.42 sec. Offline devices red when above zero and opens BO-204. *(source: screens/P08-venue-back-office.yaml#BO-254 / contracts/spine/access.yaml#listAccessMonitoring)*
- **Venue comparison**: Table Venue, Entries, In venue, Rejected %, Throughput (per minute), one row per venue; sorted by entries. *(source: screens/P08-venue-back-office.yaml#BO-254 / contracts/spine/access.yaml#/components/schemas/AccessMonitoringAnalyticsCommandCenterView)*
- **AI operations summary**: Sentence with figures and a time window, e.g. "Adventure Park attendance is tracking 11% above forecast. Main Entrance is projected to exceed the configured queue target between 11:15 and 11:45", linking to BO-263 and BO-259; advisory only (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-254)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open a board 12 screen**: Tiles open BO-255 to BO-263 and return here (VO-R13). *(source: DI-653 / F122 step 1)*

**Data it reads**: `listAccessMonitoring` (onLoad, Access Monitoring & Analytics Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Venue Home*
- → `BO-255` Live Venue Occupancy & People Counting: *Works in Live Venue Occupancy & People Counting*; calls `listAccessMonitoring`
- → `BO-256` Graphical Access Map & Live Gate Performance: *Works in Graphical Access Map & Live Gate Performance*; calls `listAccessMonitoring`
- → `BO-257` Attendance & Admission Analytics: *Works in Attendance & Admission Analytics*; calls `listAccessMonitoring`
- → `BO-258` Entry, Exit, Re-entry & Crossover Analytics: *Works in Entry, Exit, Re-entry & Crossover Analytics*; calls `listAccessMonitoring`
- → `BO-259` Throughput, Queue & Validation Performance Analytics: *Works in Throughput, Queue & Validation Performance Analytics*; calls `listAccessMonitoring`
- → `BO-260` Validation Outcome & Rejection Analytics: *Works in Validation Outcome & Rejection Analytics*; calls `listAccessMonitoring`
- → `BO-261` Guest Dwell Time, Length of Stay & Attraction Flow: *Works in Guest Dwell Time, Length of Stay & Attraction Flow*; calls `listAccessMonitoring`
- → `BO-262` Access Reports, Scheduled Reporting & Data Export: *Works in Access Reports, Scheduled Reporting & Data Export*; calls `listAccessMonitoring`
- → `BO-263` AI Access Intelligence, Forecasting & Executive Insights: *Works in AI Access Intelligence, Forecasting & Executive Insights*; calls `listAccessMonitoring`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access monitoring analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access monitoring analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access monitoring analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access monitoring analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Offline scans not yet synced**: A note under the tiles "18 offline transactions not yet included" so the figures are not read as final. *(source: F06 step 6 / DI-065)*
- **Venue manager with one venue**: Venue comparison shows that venue's parks instead of other venues. *(source: DI-061)*

#### Consistency with other screens

- Match `BO-224`: Board 9 shows the same live counts for action; the numbers must agree for the same moment.
- Match `BO-255`: Currently in venue equals the occupancy screen's venue total.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tiles:
  totalAdmissionsToday: 42684
  entries: 44102
  exits: 25675
  currentlyInVenue: 18427
  reEntries: 3842
  crossovers: 1104
  groupAdmissions: 2216
  fastPassUses: 5130
  validationSuccess: 97.8%
  rejectedScans: 962
  interventionRate: 1.4%
  averageValidation: 0.42 sec
  activeGates: 64 / 70
  offlineDevices: 3
venues:
- venue: Summit Peaks
  entries: 18421
  inVenue: 8214
  rejected: 1.8%
  throughput: 32/min
- venue: Aqua Park
  entries: 12840
  inVenue: 6321
  rejected: 2.1%
  throughput: 27/min
```

#### Permissions

- `listAccessMonitoring` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Fraud assessment view flags suspicious usage patterns or threats; live monitoring shows current attendance, in-park counts and entry/exit/crossover activity per venue in real time. *(client request · MoM 2 Sep 2026, 4.16 Fraud Detection & Live Monitoring · DI-651)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-254` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-254`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 1: Opens Access Monitoring & Analytics Command Center → Provide a single executive and operational overview of access performance across all TICVAI-controlled venues.
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F122 branch at step 1 (expected): when Nothing has been set up on Access Monitoring & Analytics Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F122 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (300 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-254?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-255`, `BO-256`, `BO-257`, `BO-258`, `BO-259`, `BO-260`, `BO-261`, `BO-262`, `BO-263`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-255` Live Venue Occupancy & People Counting

**Provide real-time people counting and occupancy using entry and exit events.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/live-venue-occupancy-people-counting-bo-255` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Live people count: opening occupancy plus entries minus exits plus operational adjustments gives current occupancy, by venue, park, zone, attraction and controlled area, each against its capacity and coloured by thresholds (Normal 0-79%, Warning 80-89%, High 90-94%, Critical 95% and above). The one thing to get right: this is admission capacity (people inside now), shown apart from sales capacity, and when the venue reaches its maximum the scanners deny "Venue full" until guests exit.

**Known correction pending (do not draw the wrong version)**

- **The content is an empty unbound table** Why: Bind listLiveVenueOccupancy and draw the hierarchy with bars. *(source: contracts/spine/access.yaml#listLiveVenueOccupancy; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Thresholds and operational adjustments have no write; the read has no opening occupancy** Why: The pack has administrators configure thresholds and the equation needs opening occupancy and adjustments. *(source: screens/P08-venue-back-office.yaml#BO-255 / screens/P08-venue-back-office.yaml#BO-256; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation has no trigger back to BO-254** Why: Board screens return to their hub (VO-R13). *(source: DI-653; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where is a venue's maximum live occupancy (the Venue full limit) set?** → Drawn default accepted: Show capacity read-only here with a link to the capacity configuration; do not edit it on this screen. *(decided by Chinmay, 2026-10-02; DEC-263 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Thresholds**: Four bands with editable lower bounds (80, 90, 95) per area level; bands cannot overlap. *(source: screens/P08-venue-back-office.yaml#BO-256)*
- **Operational adjustment**: A supervisor enters "+/- N" with a reason (e.g. counter fault at Gate 4, staff group not scanned); the reason is mandatory and the adjustment is audited. *(source: screens/P08-venue-back-office.yaml#BO-255)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Occupancy equation**: A strip "Opening occupancy + Entries - Exits +/- Adjustments = CURRENT OCCUPANCY" with today's numbers. *(source: screens/P08-venue-back-office.yaml#BO-255)*
- **Hierarchy**: Expandable tree Venue > Park > Zone > Attraction > Controlled area; each row "8,214 / 12,000 - 68.5%" with a bar in its threshold colour; zones sorted by occupancy descending. *(source: screens/P08-venue-back-office.yaml#BO-255 / contracts/spine/access.yaml#listLiveVenueOccupancy)*
- **Alerts**: "Adventure Zone has exceeded its 90% operational threshold" with time and Open on the map (BO-256). *(source: screens/P08-venue-back-office.yaml#BO-256)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Save thresholds**: Applies to alerts from now; logged (VO-R05). *(source: screens/P08-venue-back-office.yaml#BO-256)*
- **Record adjustment**: Changes current occupancy immediately and appears in the equation as Adjustments with who and why. *(source: screens/P08-venue-back-office.yaml#BO-255)*

**Data it reads**: `listLiveVenueOccupancy` (onLoad, Live Venue Occupancy & People Counting)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listLiveVenueOccupancy`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live venue occupancy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live venue occupancy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live venue occupancy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live venue occupancy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Exit scan is optional (free rotation exits)**: Occupancy is labelled "estimated" because exits are inferred, not scanned. *(source: contracts/spine/access.yaml#updateAdmissionRules)*
- **Venue reaches its maximum live occupancy**: Status Critical and a banner "Gates are denying Venue full"; scans resume admitting as guests exit. *(source: DI-650)*
- **Gates offline and journalling**: Area shows "Includes estimates - 2 gates not synced" until sync. *(source: F06 step 6)*

#### Consistency with other screens

- Match `BO-254`: Venue total equals Currently in venue there.
- Match `BO-237`: Occupancy policies (Peak capacity control) read this same figure.
- Match `BO-064`: Sales capacity screens show the other capacity type; label both distinctly (Admission capacity vs Sales capacity).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
equation: 0 opening + 15,920 entries - 7,706 exits + 0 adjustments = 8,214
areas:
- area: Summit Peaks
  current: 8214
  capacity: 12000
  occupancy: 68.5%
  status: Normal
- area: Kids Zone
  current: 1842
  capacity: 2500
  occupancy: 74%
  status: Normal
- area: Adventure Zone
  current: 3107
  capacity: 3500
  occupancy: 89%
  status: Warning
- area: VIP Zone
  current: 421
  capacity: 600
  occupancy: 70%
  status: Normal
```

#### Permissions

- `listLiveVenueOccupancy` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Fraud assessment view flags suspicious usage patterns or threats; live monitoring shows current attendance, in-park counts and entry/exit/crossover activity per venue in real time. *(client request · MoM 2 Sep 2026, 4.16 Fraud Detection & Live Monitoring · DI-651)*
- Access decisions consider who, ticket type, where, when and context; e.g. an otherwise valid unused ticket is denied once the venue's maximum live occupancy is reached, until guests exit. Scanners need a venue-full denial state. *(agreed · MoM 2 Sep 2026, 4.16 Attribute-Based Access Control · DI-650)*
- Two capacity types shown distinctly: sales capacity (tickets sellable per performance) and admission capacity (a real-time, scan-based count of guests inside via entry/exit turnstiles), capping on-site attendance independent of tickets sold. *(client request · MoM 25 Aug 2026, 4.6 Performances & Capacity Management · DI-455)*
- Admission Summary dashboard: real-time headcount of guests inside the venue from ticket scans. *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-182)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-255` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-255`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 2: Works in Live Venue Occupancy & People Counting → Provide real-time people counting and occupancy using entry and exit events.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-255?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-256` Graphical Access Map & Live Gate Performance

**Turn the graphical access topology created in Board 1 into a live operational analytics map.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/graphical-access-map-live-gate-performance-bo-256` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The board 1 topology turned into a live map: every gate, turnstile, entry and exit point, re-entry, group and VIP gate, attraction access and crossover point placed on the venue plan with a status colour, and a gate overlay with guests, throughput, success, reject and yellow rates and average validation. Heatmap layers (guest flow, queue pressure, rejection rate, device health, occupancy) and drill-down from venue to device. The one thing to get right: it is a map, not a table, and a bottleneck is visible at a glance.

**Known correction pending (do not draw the wrong version)**

- **The screen is a data table "Every graphical access map" with one column (pointType)** Why: The pack asks for a venue digital twin with heatmap layers; draw the map component with the overlay, and use the table only as an accessible alternative (VO-R12). *(source: screens/P08-venue-back-office.yaml#BO-256; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The read returns no map coordinates and no heatmap values (queue pressure, device health, occupancy)** Why: Positions live with setAccessGraphicalMap; the layers need per-point values. *(source: contracts/spine/access.yaml#listGraphicalAccessMap / contracts/spine/access.yaml#setAccessGraphicalMap; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listGraphicalAccessMap` ?venue |
| Park | text field | — | — | `listGraphicalAccessMap` ?park |
| Zone | text field | — | — | `listGraphicalAccessMap` ?zone |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Layer**: One heatmap layer at a time from the pack's five; default Guest flow. *(source: screens/P08-venue-back-office.yaml#BO-257)*
- **Drill-down**: Breadcrumb Venue > Park > Zone > Access point > Gate > Device; the map zooms to the level chosen. *(source: screens/P08-venue-back-office.yaml#BO-257 / contracts/spine/access.yaml#listGraphicalAccessMap)*

#### Outputs: what the screen shows and produces

**Shown**

**Every graphical access map** (data table, from `listGraphicalAccessMap`)

| Shows | Format | Notes |
|---|---|---|
| Point type | chip: Gate, Turnstile, Entry point, Exit point, Re entry gate, Group gate… | — |

**The selected graphical access map** (detail panel): The pack groups this record's detail under its own headings: “Guests”, “Throughput”, “Success”, “Reject”, “Yellow”.

| Shows | Format | Notes |
|---|---|---|
| Point type | chip: Gate, Turnstile, Entry point, Exit point, Re entry gate, Group gate… | — |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Venue digital twin**: Point icons by type (nine types) on the venue plan from BO-15x topology, coloured Healthy green, Warning amber, Critical red, Offline grey with a crossed icon; RTL mirrors the legend, not the map. *(source: screens/P08-venue-back-office.yaml#BO-256 / contracts/spine/access.yaml#listGraphicalAccessMap)*
- **Gate overlay**: "MAIN GATE 03 - Guests 4,821 - Throughput 31/min - Success 96.4% - Reject 2.1% - Yellow 1.5% - Average validation 0.38 sec" on hover or tap. *(source: screens/P08-venue-back-office.yaml#BO-256 / screens/P08-venue-back-office.yaml#BO-257)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open gate**: Opens BO-259 on that gate for performance, or BO-230 for lane control when the user has live operation rights. *(source: designer default)*

**Data it reads**: `listGraphicalAccessMap` (onLoad, Graphical Access Map & Live Gate Performance)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listGraphicalAccessMap`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The graphical access map list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the graphical access map untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No graphical access map yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the graphical access map are still there. The pack's own statuses are 🟢 Healthy — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Venue has no plan image or point positions**: Fall back to a schematic list grouped by zone with the same colours, and say "No map positions configured". *(source: contracts/spine/access.yaml#setAccessGraphicalMap)*
- **Gate offline**: Grey with the time last seen; rates show "No data since 10:42", not zero. *(source: DI-071 / DI-072)*

#### Consistency with other screens

- Match `BO-150`: Point positions and types come from the board 1 graphical map; same icons.
- Match `BO-224`: Same status colours as live operations.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
gate:
  name: Main Plaza Gate 3
  guests: 4821
  throughput: 31/min
  success: 96.4%
  reject: 2.1%
  yellow: 1.5%
  averageValidation: 0.38 sec
  status: Healthy
critical: North Entry turnstile 2 - Critical - reject 9.8%
```

#### Permissions

- `listGraphicalAccessMap` → `SCOPE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Venue-wide attendance overview (open/closed gates, offline/maintenance status, graphed) and a visual map of all access-control locations across venues/tenants, including entry and exit turnstile layouts that vary by venue. *(client request · MoM 2 Sep 2026, 4.1 Access Control Overview & Gate/Device Visualization · DI-623)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-256` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-256`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 4: Works in Graphical Access Map & Live Gate Performance → Turn the graphical access topology created in Board 1 into a live operational analytics map.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-256?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `SCOPE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-257` Attendance & Admission Analytics

**Provide detailed reporting of who actually attended compared with tickets sold/reserved. This is particularly important because group admission may differ from purchased quantity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/attendance-admission-analytics-bo-257` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Who actually came compared with what was sold: tickets sold, eligible today, scanned, unique guests, no-shows, group and membership attendance, repeat entry and attendance rate (21,384 attended of 23,842 eligible = 89.7%), broken down by ticket type, product, event, timeslot, membership, channel, B2B partner, reseller, customer segment, guest category and venue; group analytics (school group 112 of 120 = 93.3%); no-show analysis; AI insight. The one thing to get right: attendance is people admitted, including group waves, never the purchased quantity.

**Known correction pending (do not draw the wrong version)**

- **The nine KPIs drawn as columns of a data table; attendance rate missing** Why: KPIs are tiles (VO-R02); attendanceRate is in the read. *(source: contracts/spine/access.yaml#listAttendanceAdmission; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The read returns one set of totals - no breakdown rows, no group list, no no-show analysis** Why: The pack's breakdown, group analytics and no-show analysis need rows per dimension value. *(source: screens/P08-venue-back-office.yaml#BO-257 / contracts/spine/access.yaml#listAttendanceAdmission; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Filter drawn with six of the twelve dimensions the read accepts** Why: Ticket type, event, channel, customer segment, venue and date are missing. *(source: screens/P08-venue-back-office.yaml#BO-257 / contracts/spine/access.yaml#listAttendanceAdmission; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search attendance admission analytics | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by ticket type, product, event, timeslot, membership, channel and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | text field | — | — | `listAttendanceAdmission` ?product |
| Timeslot | text field | — | — | `listAttendanceAdmission` ?timeslot |
| Membership | text field | — | — | `listAttendanceAdmission` ?membership |
| B2B partner | text field | — | — | `listAttendanceAdmission` ?b2bPartner |
| Reseller | text field | — | — | `listAttendanceAdmission` ?reseller |
| Guest category | text field | — | — | `listAttendanceAdmission` ?guestCategory |
| Venue | text field | — | — | `listAttendanceAdmission` ?venue |
| Ticket type | text field | — | — | `listAttendanceAdmission` ?ticketType |
| Event | text field | — | — | `listAttendanceAdmission` ?event |
| Channel | text field | — | — | `listAttendanceAdmission` ?channel |
| Customer segment | text field | — | — | `listAttendanceAdmission` ?customerSegment |
| Date | text field | — | — | `listAttendanceAdmission` ?date |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Date / breakdown**: Date (default today) or range; "Break down by" one of eleven dimensions, plus filters. *(source: screens/P08-venue-back-office.yaml#BO-257 / contracts/spine/access.yaml#listAttendanceAdmission)*

#### Outputs: what the screen shows and produces

**Shown**

**Every attendance admission analytics** (data table, from `listAttendanceAdmission`)

| Shows | Format | Notes |
|---|---|---|
| Tickets sold | 1,234 | Tickets Sold |
| Tickets eligible today | 1,234 | Tickets Eligible Today |
| Tickets scanned | 1,234 | Tickets Scanned |
| Unique guests | 1,234 | Unique Guests |
| No shows | 1,234 | No-Shows |
| Group attendance | 1,234 | Group Attendance |
| Membership attendance | 1,234 | Membership Attendance |
| Repeat entry | 1,234 | Repeat Entry |
| No show rate | 12.5% | no-show rate |

**The selected attendance admission analytics** (detail panel): The pack groups this record's detail under its own headings: “Sold”, “Eligible”, “Attended”, “ATTENDANCE RATE”, “Purchased”, “Actual Attendance”.

| Shows | Format | Notes |
|---|---|---|
| Tickets sold | 1,234 | Tickets Sold |
| Tickets eligible today | 1,234 | Tickets Eligible Today |
| Tickets scanned | 1,234 | Tickets Scanned |
| Unique guests | 1,234 | Unique Guests |
| No shows | 1,234 | No-Shows |
| Group attendance | 1,234 | Group Attendance |
| Membership attendance | 1,234 | Membership Attendance |
| Repeat entry | 1,234 | Repeat Entry |
| No show rate | 12.5% | no-show rate |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Attendance KPIs**: Tiles (VO-R02) - Sold, Eligible, Attended, Attendance rate defined as attended / eligible, Unique guests, No-shows, Group, Membership, Repeat entry. *(source: screens/P08-venue-back-office.yaml#BO-257 / contracts/spine/access.yaml#listAttendanceAdmission)*
- **Breakdown table**: One row per value of the chosen dimension with sold, eligible, attended, rate, no-show rate. *(source: screens/P08-venue-back-office.yaml#BO-257)*
- **Group analytics**: Groups with purchased vs actual and rate (from the waves of BO-217); morning vs afternoon comparison. *(source: screens/P08-venue-back-office.yaml#BO-257 / screens/P08-venue-back-office.yaml#BO-258)*
- **AI insight**: "Morning school groups average 94% attendance, afternoon 81%; consider adjusting capacity assumptions for afternoon group products" - advisory. *(source: screens/P08-venue-back-office.yaml#BO-258)*

**Data it reads**: `listAttendanceAdmission` (onLoad, Attendance & Admission Analytics)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listAttendanceAdmission`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attendance admission analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attendance admission analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attendance admission analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attendance admission analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-217`: Group attendance is the waves admitted there.
- Match `BO-060`: Attendance & Footfall reporting uses the same definitions (cross-process).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  sold: 25000
  eligible: 23842
  attended: 21384
  rate: 89.7%
  uniqueGuests: 20917
  noShows: 2458
  group: 2911
  membership: 3120
  repeatEntry: 467
groups:
- group: Abu Dhabi International School
  purchased: 120
  attended: 112
  rate: 93.3%
```

#### Permissions

- `listAttendanceAdmission` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-257` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-257`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 6: Works in Attendance & Admission Analytics → Provide detailed reporting of who actually attended compared with tickets sold/reserved. This is particularly important because group admission may differ from purchased quantity.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-257?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-258` Entry, Exit, Re-entry & Crossover Analytics

**Analyze complete guest movement across the access journey.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Measure) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/entry-exit-re-entry-crossover-analytics-bo-258` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Guest movement analysed as a journey: first entries, temporary exits, re-entries, crossovers and final exits as a funnel, re-entry analytics (rate, average time outside, most-used re-entry gates, rejected re-entry, by product) and crossover analytics (Park A to Park B and back, crossover time, product, utilisation). The one thing to get right: re-entries and crossovers are counted apart from first entries, so movement is understood rather than only totals.

**Known correction pending (do not draw the wrong version)**

- **The read's single object is drawn as a six-column data table "Every entry exit re-entry"** Why: These are metrics and a funnel, not rows; draw tiles, funnel and flow (VO-R02, VO-R12). *(source: contracts/spine/access.yaml#listEntryExitCrossover; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **crossoverFlows, mostUsedReEntryGates and reEntryByProduct are arrays of strings** Why: Directional flows and ranked gates need counts; strings cannot be drawn as a flow or ranking. *(source: contracts/spine/access.yaml#/components/schemas/EntryExitReEntryCrossoverAnalyticsView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Date range and venue**: Default today; park filter for multi-park venues. *(source: designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Every entry exit re-entry** (data table, from `listEntryExitCrossover`)

| Shows | Format | Notes |
|---|---|---|
| Re entry rate | 12.5% | Re-entry rate |
| Average time outside | 1,234 | Minutes |
| Most used re entry gates | list or chips (count when long) | most-used re-entry gates |
| Rejected re entry | 1,234 | rejected re-entry |
| Crossover time | 1,234 | Average minutes between leaving one park and entering the next |
| Crossover product | list or chips (count when long) | Products used for crossover, with counts |

**The selected entry exit re-entry** (detail panel): The pack groups this record's detail under its own headings: “Adventure Park”, “Water Park”.

| Shows | Format | Notes |
|---|---|---|
| Re entry rate | 12.5% | Re-entry rate |
| Average time outside | 1,234 | Minutes |
| Most used re entry gates | list or chips (count when long) | most-used re-entry gates |
| Rejected re entry | 1,234 | rejected re-entry |
| Crossover time | 1,234 | Average minutes between leaving one park and entering the next |
| Crossover product | list or chips (count when long) | Products used for crossover, with counts |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Journey funnel**: Five stages with counts (18,421 first entries, 5,284 temporary exits, 3,842 re-entries, 1,104 crossovers, 17,921 final exits) as a funnel or stepped bars, not a table. *(source: screens/P08-venue-back-office.yaml#BO-258 / contracts/spine/access.yaml#listEntryExitCrossover)*
- **Re-entry analytics**: Re-entry rate %, average time outside (h m), most-used re-entry gates ranked, rejected re-entries with top reason, re-entry by product. *(source: screens/P08-venue-back-office.yaml#BO-258 / contracts/spine/access.yaml#listEntryExitCrossover)*
- **Crossover flow**: A two-way flow between parks with counts each way (Adventure Park 2,184, Water Park 1,327), average crossover time and utilisation of crossover entitlements. *(source: screens/P08-venue-back-office.yaml#BO-259 / contracts/spine/access.yaml#listEntryExitCrossover)*

**Data it reads**: `listEntryExitCrossover` (onLoad, Entry, Exit, Re-entry & Crossover Analytics)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listEntryExitCrossover`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entry exit re-entry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entry exit re-entry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entry exit re-entry yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entry exit re-entry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Exits not scanned (free rotation exits)**: Temporary exits and final exits are shown as "not measured" for those gates rather than zero. *(source: contracts/spine/access.yaml#updateAdmissionRules)*

#### Consistency with other screens

- Match `BO-219`: Re-entry rules configured there explain the re-entry figures here.
- Match `BO-220`: Same crossover event definitions.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
funnel: 18,421 first entries / 5,284 temporary exits / 3,842 re-entries / 1,104 crossovers / 17,921 final exits
reEntry:
  rate: 20.9%
  averageTimeOutside: 1h 12m
  topGate: Re-entry Gate 03
  rejected: 61
crossover:
  summitToAqua: 2184
  aquaToSummit: 1327
  averageTime: 3h 40m
```

#### Permissions

- `listEntryExitCrossover` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group/B2B admission profile view shows entry statistics by category (general admission, group, re-entry, crossover) and attendance breakdowns for schools and other groups from scanned tickets. *(client request · MoM 2 Sep 2026, 4.15 Guest Journey, Group/B2B Profiles & Live Operations Dashboard · DI-647)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-258` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-258`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 8: Works in Entry, Exit, Re-entry & Crossover Analytics → Analyze complete guest movement across the access journey.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-258?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-259` Throughput, Queue & Validation Performance Analytics

**Measure the operational efficiency of gates and validation devices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/throughput-queue-validation-performance-analytics-bo-259` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Gate efficiency: guests per minute and hour, average scan time and gate cycle, success, yellow, reject and manual intervention rates and downtime, per gate side by side, with bottleneck detection naming the likely reason (QR read failures, excessive manual verification, hardware latency, policy complexity, wrong guest routing) and queue analytics current, historical and forecast. The one thing to get right: an underperforming gate is flagged with its cause, not just a low number.

**Known correction pending (do not draw the wrong version)**

- **The eight metric tiles are bound to no operation and there is no gate comparison table** Why: The read returns per-gate rows; tiles summarise the selection and the comparison is the pack's main table. *(source: screens/P08-venue-back-office.yaml#BO-259 / contracts/spine/access.yaml#listThroughputQueueValidation; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Queue analytics (current, historical, forecast) has no field** Why: The read is per gate with no time series. *(source: screens/P08-venue-back-office.yaml#BO-260; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Period and gate group**: Today by default; compare gates within a gate group so like is compared with like. *(source: screens/P08-venue-back-office.yaml#BO-259 / designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Guests per Minute** (metric tile)

**Guests per Hour** (metric tile)

**Average Scan Time** (metric tile)

**Average Gate Cycle** (metric tile)

**Success Rate** (metric tile)

**Yellow Rate** (metric tile)

**Reject Rate** (metric tile)

**Manual Intervention Rate** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Gate KPIs**: Nine metric tiles for the selection (the screen is missing Downtime). *(source: screens/P08-venue-back-office.yaml#BO-259 / contracts/spine/access.yaml#listThroughputQueueValidation)*
- **Gate comparison**: Table Gate, Guests/hr, Validation (s), Reject %, Intervention %, Downtime, with the underperforming gate highlighted and labelled "GATE 03 - UNDERPERFORMING" and its bottleneck reason in words. *(source: screens/P08-venue-back-office.yaml#BO-259 / contracts/spine/access.yaml#listThroughputQueueValidation)*
- **Queue analytics**: Current, Historical and Forecast as three tabs on one chart of queue length by time. *(source: screens/P08-venue-back-office.yaml#BO-260)*
- **AI recommendation**: "Gate 03 processes 39% fewer guests per minute than comparable gates. RFID read retries are the primary contributor", advisory (VO-R11). *(source: screens/P08-venue-back-office.yaml#BO-260)*

**Data it reads**: `listThroughputQueueValidation` (onLoad, Throughput, Queue & Validation Performance Analytics)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listThroughputQueueValidation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The throughput queue validation list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the throughput queue validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No throughput queue validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the throughput queue validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Gate in Free flow or Drop arm for part of the period**: Validation figures exclude those minutes and the row notes "Free flow 10:00-10:40". *(source: contracts/spine/access.yaml#/components/schemas/AccessPointOperatingMode)*

#### Consistency with other screens

- Match `BO-231`: Board 9 queue and lane optimisation acts on the same throughput figures live.
- Match `BO-203`: The 0.9-second validation target used by the hardware advisor is the same target.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
gates:
- gate: Main Plaza Gate 1
  guestsPerHour: 1482
  validation: 0.39 s
  reject: 1.2%
  intervention: 0.8%
- gate: Main Plaza Gate 2
  guestsPerHour: 1391
  validation: 0.42 s
  reject: 1.4%
  intervention: 1.1%
- gate: Main Plaza Gate 3
  guestsPerHour: 821
  validation: 0.81 s
  reject: 8.2%
  intervention: 6.4%
  flag: UNDERPERFORMING - QR read failures
```

#### Permissions

- `listThroughputQueueValidation` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'wait-time')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A244** Build virtual queue with 3 guest tiers (walk-in, VQ, VIP); keep VQ separate from VIP lane *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A245** Recalculate virtual queue return times live, not fixed at booking *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A246** Support virtual queue via app (theme parks) and kiosk/wristband scan (water parks) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*
- **A247** Build virtual queue ops dashboard, AI guest-flow tips and fast-lane upsell on long waits *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'virtual queue')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-259` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-259`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 10: Works in Throughput, Queue & Validation Performance Analytics → Measure the operational efficiency of gates and validation devices.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-259?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-260` Validation Outcome & Rejection Analytics

**Analyze why guests are denied or require manual intervention.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/validation-outcome-rejection-analytics-bo-260` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Why guests are denied or need intervention: the outcome split (Allowed, Operator review, Denied), the rejection reasons ranked with count and share, analysis by ten dimensions, and override correlation (482 Wrong visit date rejections, 281 overrides, 58.3%), with an AI root cause. The one thing to get right: a reason with a high override rate is shown as a likely configuration or business-process problem, not fraud.

**Known correction pending (do not draw the wrong version)**

- **The screen has only a search and a filter; nothing draws the read** Why: Bind listValidationOutcomeRejection to the outcome bar and reasons table. *(source: contracts/spine/access.yaml#listValidationOutcomeRejection; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **rejectionReasons is an array of strings with no count, share or overrides per reason** Why: The ranked table and the override correlation need them per reason. *(source: screens/P08-venue-back-office.yaml#BO-261 / contracts/spine/access.yaml#/components/schemas/ValidationOutcomeRejectionAnalyticsView; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search validation outcome rejection | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, gate, product, ticket type, channel, reseller and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listValidationOutcomeRejection` ?venue |
| Gate | text field | — | — | `listValidationOutcomeRejection` ?gate |
| Product | text field | — | — | `listValidationOutcomeRejection` ?product |
| Ticket type | text field | — | — | `listValidationOutcomeRejection` ?ticketType |
| Channel | text field | — | — | `listValidationOutcomeRejection` ?channel |
| Reseller | text field | — | — | `listValidationOutcomeRejection` ?reseller |
| Operator | text field | — | — | `listValidationOutcomeRejection` ?operator |
| Device | text field | — | — | `listValidationOutcomeRejection` ?device |
| Credential type | text field | — | — | `listValidationOutcomeRejection` ?credentialType |
| Time | text field | — | — | `listValidationOutcomeRejection` ?time |

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Analyse by and filters**: Venue, Gate, Product, Ticket type, Channel, Reseller, Operator, Device, Credential type, Time; date range default today. *(source: screens/P08-venue-back-office.yaml#BO-261 / contracts/spine/access.yaml#listValidationOutcomeRejection)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Outcome distribution**: A single stacked bar Allowed 96.8% green, Operator review 2.1% amber, Denied 1.1% red, with counts on hover. *(source: screens/P08-venue-back-office.yaml#BO-260)*
- **Rejection reasons**: Ranked table Reason, Count, %, Overrides, Override rate, using the deny reason labels of VO-R06 (Wrong visit date, Already used, Wrong park, Anti-passback, Expired, Credential revoked, Other); a row with override rate above 50% carries "Likely configuration issue". *(source: screens/P08-venue-back-office.yaml#BO-260 / screens/P08-venue-back-office.yaml#BO-261)*
- **AI root cause**: "72% of Wrong Visit Date overrides originate from tickets sold through Reseller X. Review the reseller's date-mapping configuration", advisory. *(source: screens/P08-venue-back-office.yaml#BO-261)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open scans for a reason**: Opens the scan activity filtered to that reason and period. *(source: screens/P08-venue-back-office.yaml#BO-034)*

**Data it reads**: `listValidationOutcomeRejection` (onLoad, Validation Outcome & Rejection Analytics)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listValidationOutcomeRejection`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The validation outcome rejection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the validation outcome rejection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No validation outcome rejection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the validation outcome rejection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `BO-227`: Reason labels come from the reason code manager; same words.
- Match `BO-228`: Override counts equal the override audit for the period.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
distribution:
  allowed: 96.8%
  operatorReview: 2.1%
  denied: 1.1%
reasons:
- reason: Wrong visit date
  count: 482
  share: 31%
  overrides: 281
  overrideRate: 58.3%
- reason: Already used
  count: 318
  share: 20%
- reason: Wrong park
  count: 201
  share: 13%
- reason: Anti-passback
  count: 184
  share: 12%
- reason: Expired
  count: 129
  share: 8%
- reason: Credential revoked
  count: 82
  share: 5%
```

#### Permissions

- `listValidationOutcomeRejection` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-260` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-260`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 12: Works in Validation Outcome & Rejection Analytics → Analyze why guests are denied or require manual intervention.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-260?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-261` Guest Dwell Time, Length of Stay & Attraction Flow

**Use access events to understand how guests move through and use the venue.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Show) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/guest-dwell-time-length-of-stay-attraction-flow-bo-261` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** How guests use the venue, from access events: length of stay where entry and final exit exist (09:12 to 16:42 = 7h 30m), average and median stay, peak arrival and departure, zone dwell time, attraction visits, Fast Pass use and re-entry behaviour; a guest flow (main entrance > adventure zone > coaster > F&B > water zone > exit); per-attraction figures (Falcon Coaster - 5,842 unique guests, 6,211 validations, 1,827 Fast Pass, 369 repeat visits, peak 14:00-15:00). The one thing to get right: pseudonymised, aggregated figures with their coverage stated, never individual guest tracking on this screen.

**Known correction pending (do not draw the wrong version)**

- **Seven tiles drawn with no operation bound** Why: Bind listGuestDwellTime. *(source: screens/P08-venue-back-office.yaml#BO-261 / contracts/spine/access.yaml#listGuestDwellTime; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The read returns one set of totals - no per-attraction rows, no flow between areas, no coverage figure** Why: The pack's attraction analytics and guest flow cannot be drawn; coverage is needed to read stay figures honestly. *(source: screens/P08-venue-back-office.yaml#BO-261 / contracts/spine/access.yaml#listGuestDwellTime; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **The pack's flow includes F&B, which is not an access event** Why: An F&B step needs POS events (cross-process); without them the flow shows access points only. *(source: screens/P08-venue-back-office.yaml#BO-261; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the guest flow use F&B and retail transactions as flow steps?** → Drawn default accepted: Access points only; F&B shown greyed "Needs POS data". *(decided by Chinmay, 2026-10-02; DEC-264 / CHG-NOTE-008)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Date range / venue / zone**: Default yesterday (a complete day); filters by park and zone. *(source: designer default)*

#### Outputs: what the screen shows and produces

**Shown**

**Average Length of Stay** (metric tile)

**Median Stay** (metric tile)

**Peak Arrival** (metric tile)

**Peak Departure** (metric tile)

**Zone Dwell Time** (metric tile)

**Attraction Visits** (metric tile)

**Fast Pass Usage** (metric tile)

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Stay KPIs**: Average and median length of stay (h:mm), peak arrival and departure (hour bands), zone dwell time; each with "based on 62% of guests with a final exit scan". *(source: screens/P08-venue-back-office.yaml#BO-261 / contracts/spine/access.yaml#listGuestDwellTime)*
- **Guest flow**: A flow (Sankey) between areas in visit order, widths by guest count. *(source: screens/P08-venue-back-office.yaml#BO-261)*
- **Attraction analytics**: Per attraction - unique guests, total validations, Fast Pass, repeat visits, peak hour; sortable. *(source: screens/P08-venue-back-office.yaml#BO-261)*

**Data it reads**: `listGuestDwellTime` (onLoad, Guest Dwell Time, Length of Stay & Attraction Flow)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listGuestDwellTime`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest dwell time list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest dwell time untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest dwell time yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guest dwell time are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Exits not scanned (free rotation) or guests leaving through an unscanned exit**: Length of stay is computed only for guests with a final exit; the coverage is always shown. *(source: screens/P08-venue-back-office.yaml#BO-261 / contracts/spine/access.yaml#/components/schemas/AdmissionRules)*
- **Request for one named guest's movements**: Not on this screen; individual history is in the ticket investigation console (BO-226) for permitted roles. *(source: screens/P08-venue-back-office.yaml#BO-262)*

#### Consistency with other screens

- Match `BO-258`: Re-entry behaviour uses the same re-entry counts.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
  averageStay: 6h 10m
  medianStay: 5h 45m
  peakArrival: 09:30-10:30
  peakDeparture: 16:30-17:30
  coverage: 62% of guests
attraction:
  name: Falcon Coaster
  uniqueGuests: 5842
  validations: 6211
  fastPass: 1827
  repeatVisits: 369
  peak: 14:00-15:00
```

#### Permissions

- `listGuestDwellTime` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-261` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-261`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 14: Works in Guest Dwell Time, Length of Stay & Attraction Flow → Use access events to understand how guests move through and use the venue.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-261?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-262` Access Reports, Scheduled Reporting & Data Export

**Provide configurable operational and management reports.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `reportId` (navigation), `scheduleId` (navigation) |
| Route | `/access-venue/access-reports-scheduled-reporting-data-export-bo-262` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Access-control reports (entries, exits, denials, in-park count, length of stay by gate and time) run now, scheduled, or exported. In-park is entries minus exits; length of stay is the time between a guest's scans.

**Known correction pending (do not draw the wrong version)**

- **Two sources of access schedules: the access contract's own "scheduled reporting" list and the reporting schedules.** Why: A schedule created in one will not show in the other. *(source: contracts/spine/access.yaml#listAccessReportScheduled / contracts/satellite/reporting.yaml#listReportSchedules; Finance, Ledger & Tax · Reporting & Analytics)*
- **BO-262 duplicates the reporting area's scheduler and export centre.** Why: DI-721. *(source: DI-721 / screens/P16-venue-analytics.yaml#ANL-045; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search access reports scheduled | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, park, zone, event, date and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listAccessReportScheduled` ?venue |
| Park | text field | — | — | `listAccessReportScheduled` ?park |
| Zone | text field | — | — | `listAccessReportScheduled` ?zone |
| Event | text field | — | — | `listAccessReportScheduled` ?event |
| Date | text field | — | — | `listAccessReportScheduled` ?date |
| Ticket type | text field | — | — | `listAccessReportScheduled` ?ticketType |
| Product | text field | — | — | `listAccessReportScheduled` ?product |
| Gate | text field | — | — | `listAccessReportScheduled` ?gate |
| Device | text field | — | — | `listAccessReportScheduled` ?device |
| Channel | text field | — | — | `listAccessReportScheduled` ?channel |
| Partner | text field | — | — | `listAccessReportScheduled` ?partner |
| Category | select | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | `listReports` ?category |
| Search | text field | — | — | `listReports` ?search |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **filters**: Venue, zone, gate or access point, event, date range (bounded by the report's maximum range), outcome. *(source: MATRIX 3.2.65 / MATRIX 6.1.19)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **report list**: Access reports only (category access); each with Run now, Schedule, Export. *(source: contracts/satellite/reporting.yaml#listReports)*

**Data it reads**: `listAccessReportScheduled` (onLoad, Access Reports, Scheduled Reporting & Data Export); `listReportSchedules` (onLoad, The scheduled access reports); `listReports` (onLoad, The access reports to run or schedule)

**Where the user goes next**

- → `BO-254` Access Monitoring & Analytics Command Center: *Returns to the board's landing screen*; calls `listAccessReportScheduled`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access reports scheduled list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access reports scheduled untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access reports scheduled yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access reports scheduled are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Invalid cadence (a field its frequency needs is missing, or one it does not take is sent, audit R158), or no recipients; 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158) |

#### Edge cases to draw

- **a range longer than the report allows**: The date picker stops at the limit and says so. *(source: MATRIX 6.1.19)*
- **guest-level rows (names, photos)**: Hidden unless the user may export personal data; the export is audited. *(source: contracts/shared/permissions.yaml#/components/schemas/Permission)*

#### Consistency with other screens

- Match `P16 ANL-031 Report Catalogue, ANL-042 Report Scheduler, ANL-045 Export & Download Center`: Access reports are definitions in the one catalogue; this screen is the same list filtered to access.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- Entries by gate, hourly · Aquaventure · Gate 2 · 30 Sep 10:00–11:00 · 1,284 entries, 41 denied (expired 22, wrong
  date 19)
- In-park now · 6,912 (entries 9,140 − exits 2,228)
```

#### Permissions

- `listAccessReportScheduled` → `REPORT_VIEW_VENUE` (operate) · staff
- `listReportSchedules` → `REPORT_VIEW_VENUE` (operate) · staff
- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `createReportSchedule` → `REPORT_SCHEDULE` (operate) · staff
- `updateReportSchedule` → `REPORT_SCHEDULE` (operate) · staff
- `deleteReportSchedule` → `REPORT_SCHEDULE` (operate) · staff
- `listReports` → `REPORT_VIEW_VENUE` (operate) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 6.1.14 | The system should have scheduling of report generation and delivery to web address location or list of email addresses. | Retail POS | CONTRACTED | `createReportSchedule` |
| 8.7.15 | System shall support report scheduling. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 8.7.16 | System shall support report subscriptions. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 8.7.17 | System shall support report sharing. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-262` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-262`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 16: Works in Access Reports, Scheduled Reporting & Data Export → Provide configurable operational and management reports.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-262?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-254`.
- [ ] Every gated control is gated: `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-263` AI Access Intelligence, Forecasting & Executive Insights

**Turn access-control data into proactive operational intelligence. This should be the final intelligence screen of the entire Access Control module.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Forecast) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/ai-access-intelligence-forecasting-executive-insights-bo-263` |

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** The intelligence screen of the access module: Ask TICVAI in plain language ("Why was Main Entrance slow yesterday 10-11?" - throughput down 22%, Gate 04 offline 18 minutes, QR retries at Gate 07, two school groups of 286 within 12 minutes); forecasts for tomorrow (attendance 28,400, peak arrival 09:40-10:30, recommended entry lanes 14 vs 10 planned); a recommendation; what-if scenarios (attendance 35,000); and executive insights. AI analyses, explains, forecasts and recommends; people act through the normal permissions. The one thing to get right: every forecast and recommendation shows its basis and is accepted or rejected by a person.

**Known correction pending (do not draw the wrong version)**

- **The eight forecast metrics drawn as data table columns; field name "tomorrowSAttendance"** Why: They are tiles of one forecast (VO-R02); the label is "Tomorrow's attendance". *(source: screens/P08-venue-back-office.yaml#BO-263 / contracts/spine/access.yaml#listAccessExecutiveInsight; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Ask TICVAI, scenario planning and recommendation decisions are not bound; aiRecommendation is one string without its basis** Why: The platform already offers askReportingQuestion, createForecastScenario and decideAiInsight; a recommendation must carry its reasons (VO-R11). *(source: contracts/satellite/reporting.yaml#askReportingQuestion / contracts/satellite/ai.yaml#createForecastScenario / contracts/satellite/ai.yaml#decideAiInsight; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Navigation has no return edge to BO-254** Why: Board screens return to their command centre (VO-R13). *(source: screens/P08-venue-back-office.yaml#BO-263; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Ask TICVAI**: A question box with suggested questions; answers cite the figures and time ranges they used. *(source: screens/P08-venue-back-office.yaml#BO-263 / contracts/satellite/reporting.yaml#askReportingQuestion)*
- **Scenario**: "What if attendance reaches [35,000]" (and date); returns gate requirements, throughput, occupancy risk, queue duration, device utilisation. *(source: screens/P08-venue-back-office.yaml#BO-263 / contracts/satellite/ai.yaml#createForecastScenario)*

#### Outputs: what the screen shows and produces

**Shown**

**Every access intelligence forecasting** (data table, from `listAccessExecutiveInsight`)

| Shows | Format | Notes |
|---|---|---|
| Tomorrow s attendance | 1,234 | Tomorrow's Attendance |
| Peak arrival time | text | Forecast time window, e.g. |
| Peak exit time | text | Forecast time window |
| Venue occupancy | 1,234 | Venue Occupancy |
| Zone occupancy | 1,234 | Zone Occupancy |
| Gate demand | 1,234 | Forecast guests per hour at peak across gates |
| Group arrival pressure | text | Group Arrival Pressure |
| Re entry demand | text | Re-entry Demand |

**The selected access intelligence forecasting** (detail panel): The pack groups this record's detail under its own headings: “Expected Attendance”, “Peak Arrival”, “Current Planned”, “Board 12 Key Workflow”, “Final Access Control Architecture”, “Board Area”.

| Shows | Format | Notes |
|---|---|---|
| Tomorrow s attendance | 1,234 | Tomorrow's Attendance |
| Peak arrival time | text | Forecast time window, e.g. |
| Peak exit time | text | Forecast time window |
| Venue occupancy | 1,234 | Venue Occupancy |
| Zone occupancy | 1,234 | Zone Occupancy |
| Gate demand | 1,234 | Forecast guests per hour at peak across gates |
| Group arrival pressure | text | Group Arrival Pressure |
| Re entry demand | text | Re-entry Demand |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Tomorrow forecast**: Tiles for expected attendance, peak arrival and exit times, venue and zone occupancy, gate demand, group arrival pressure, re-entry demand, device capacity; "Recommended entry lanes 14 - currently planned 10" as a gap. *(source: screens/P08-venue-back-office.yaml#BO-263 / contracts/spine/access.yaml#listAccessExecutiveInsight)*
- **Recommendation**: "Open four more standard lanes 09:30-10:45 and give Group Gate 02 to B2B arrivals 10:00-10:30" with its reasons, Accept / Reject; accepting opens BO-230 prefilled, nothing changes by itself. *(source: screens/P08-venue-back-office.yaml#BO-263)*
- **Executive insights**: Attendance vs forecast, guest flow efficiency, gate efficiency, access failure rate, security impact, venue utilisation, operational recommendations - tiles with trend. *(source: screens/P08-venue-back-office.yaml#BO-263)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Accept / Reject recommendation**: Records the decision (a rejection with a reason is the false-alarm signal); accepted actions go through the normal screens and permissions. *(source: contracts/satellite/ai.yaml#decideAiInsight)*

**Data it reads**: `listAccessExecutiveInsight` (onLoad, AI Access Intelligence, Forecasting & Executive Insights)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access intelligence forecasting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access intelligence forecasting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access intelligence forecasting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access intelligence forecasting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `ANL-052`: Ask TICVAI in analytics (cross-process) is the same natural-language capability; board 12 must not become a second BI module.
- Match `BO-253`: Security impact figures come from security analytics.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
forecast:
  date: Sat 3 Oct 2026
  attendance: 28400
  peakArrival: 09:40-10:30
  peakExit: 17:00-18:00
  recommendedLanes: 14
  planned: 10
answer: 'Throughput fell 22%: Main Plaza Gate 4 offline 18 min, elevated QR retries at Gate 7, and two school groups
  (286 guests) arrived within 12 minutes.'
```

#### Permissions

- `listAccessExecutiveInsight` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.46 | AI Policy Recommendations - System shall provide AI-assisted policy recommendations. | Admission and Access | CONTRACTED_PARTIAL | `listAccessExecutiveInsight` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-263` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS29 Access Control Board 12.dc.html#bo-263`
- Workshop pack: Access Control Module_Reference.pdf board 12
- Flow F122 *Access Control board 12: Access Monitoring & Analytics Command Center*, step 18: Works in AI Access Intelligence, Forecasting & Executive Insights → Turn access-control data into proactive operational intelligence. This should be the final intelligence screen of the entire Access Control module.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-263?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createReportSchedule": {"method":"POST","path":"/report-schedules","contract":"reporting","summary":"Schedule a report","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportScheduleRequest","responds":"ReportSchedule"},
"deleteReportSchedule": {"method":"DELETE","path":"/report-schedules/{scheduleId}","contract":"reporting","summary":"Delete a schedule","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listAccessExecutiveInsight": {"method":"GET","path":"/access-executive-insight","contract":"access","summary":"AI Access Intelligence, Forecasting & Executive Insights","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAccessIntelligenceForecastingExecutiveInsightsView"},
"listAccessMonitoring": {"method":"GET","path":"/access-monitoring","contract":"access","summary":"Access Monitoring & Analytics Command Center","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccessReportScheduled": {"method":"GET","path":"/access-report-scheduled","contract":"access","summary":"Access Reports, Scheduled Reporting & Data Export","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"park","in":"query","required":false},{"name":"zone","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"date","in":"query","required":false},{"name":"ticketType","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"gate","in":"query","required":false},{"name":"device","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"partner","in":"query","required":false}],"requestBody":null,"responds":"AccessReportsScheduledReportingDataExportView"},
"listAttendanceAdmission": {"method":"GET","path":"/attendance-admission","contract":"access","summary":"Attendance & Admission Analytics","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"product","in":"query","required":false},{"name":"timeslot","in":"query","required":false},{"name":"membership","in":"query","required":false},{"name":"b2bPartner","in":"query","required":false},{"name":"reseller","in":"query","required":false},{"name":"guestCategory","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"ticketType","in":"query","required":false},{"name":"event","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"customerSegment","in":"query","required":false},{"name":"date","in":"query","required":false}],"requestBody":null,"responds":"AttendanceAdmissionAnalyticsView"},
"listEntryExitCrossover": {"method":"GET","path":"/entry-exit-crossover","contract":"access","summary":"Entry, Exit, Re-entry & Crossover Analytics","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EntryExitReEntryCrossoverAnalyticsView"},
"listGraphicalAccessMap": {"method":"GET","path":"/graphical-access-map","contract":"access","summary":"Graphical Access Map & Live Gate Performance","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"park","in":"query","required":false},{"name":"zone","in":"query","required":false}],"requestBody":null,"responds":"GraphicalAccessMapLiveGatePerformanceView"},
"listGuestDwellTime": {"method":"GET","path":"/guest-dwell-time","contract":"access","summary":"Guest Dwell Time, Length of Stay & Attraction Flow","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestDwellTimeLengthOfStayAttractionFlowView"},
"listLiveVenueOccupancy": {"method":"GET","path":"/live-venue-occupancy","contract":"access","summary":"Live Venue Occupancy & People Counting","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LiveVenueOccupancyPeopleCountingView"},
"listReportSchedules": {"method":"GET","path":"/report-schedules","contract":"reporting","summary":"List scheduled reports","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReports": {"method":"GET","path":"/reports","contract":"reporting","summary":"List available report definitions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listThroughputQueueValidation": {"method":"GET","path":"/throughput-queue-validation","contract":"access","summary":"Throughput, Queue & Validation Performance Analytics","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ThroughputQueueValidationPerformanceAnalyticsView"},
"listValidationOutcomeRejection": {"method":"GET","path":"/validation-outcome-rejection","contract":"access","summary":"Validation Outcome & Rejection Analytics","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"venue","in":"query","required":false},{"name":"gate","in":"query","required":false},{"name":"product","in":"query","required":false},{"name":"ticketType","in":"query","required":false},{"name":"channel","in":"query","required":false},{"name":"reseller","in":"query","required":false},{"name":"operator","in":"query","required":false},{"name":"device","in":"query","required":false},{"name":"credentialType","in":"query","required":false},{"name":"time","in":"query","required":false}],"requestBody":null,"responds":"ValidationOutcomeRejectionAnalyticsView"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"updateReportSchedule": {"method":"PATCH","path":"/report-schedules/{scheduleId}","contract":"reporting","summary":"Amend, pause or resume a schedule","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportSchedule"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessMonitoringAnalyticsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Monitoring & Analytics Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"venueId":{"type":"string"},"venueName":{"type":"string"},"venueEntries":{"type":"integer"},"venueInVenue":{"type":"integer"},"venueRejectedRate":{"type":"number","description":"Percent"},"venueThroughputPerMinute":{"type":"number"}},"required":["venueId"]},
"AccessMonitoringAnalyticsCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"totalAdmissionsToday":{"type":"integer","description":"Total Admissions Today"},"entries":{"type":"integer","description":"Entries"},"exits":{"type":"integer","description":"Exits"},"currentlyInVenue":{"type":"integer","description":"Currently In Venue"},"reEntries":{"type":"integer","description":"Re-entries"},"crossovers":{"type":"integer","description":"Crossovers"},"groupAdmissions":{"type":"integer","description":"Group Admissions"},"fastPassUses":{"type":"integer","description":"Fast Pass Uses"},"validScans":{"type":"integer","description":"Valid Scans"},"rejectedScans":{"type":"integer","description":"Rejected Scans"},"interventionRate":{"type":"number","description":"Intervention Rate"},"averageValidationTime":{"type":"number","description":"Seconds"},"activeGates":{"type":"integer","description":"Active Gates"},"offlineDevices":{"type":"integer","description":"Offline Devices"},"validationSuccessRate":{"type":"number","description":"Percent"}}},
"AccessReportsScheduledReportingDataExportView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Access Reports, Scheduled Reporting & Data Export displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string"},"reportId":{"type":"string"},"formats":{"type":"array","items":{"type":"string","enum":["dashboard","csv","xlsx","pdf","apiDataFeed","biIntegration"]}},"filterCriteria":{"type":"array","items":{"type":"string"},"description":"Saved filters, e.g. venue=..., gate=..."},"scheduleTime":{"type":"string","description":"Local time of day, e.g. 07:00"},"recipients":{"type":"array","items":{"type":"string"},"description":"Authorized recipients or reporting destinations"}},"required":["reportId","name"]},
"AiAccessIntelligenceForecastingExecutiveInsightsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What AI Access Intelligence, Forecasting & Executive Insights displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"tomorrowSAttendance":{"type":"integer","description":"Tomorrow's Attendance"},"peakArrivalTime":{"type":"string","description":"Forecast time window, e.g. 09:40-10:30"},"peakExitTime":{"type":"string","description":"Forecast time window"},"venueOccupancy":{"type":"integer","description":"Venue Occupancy"},"zoneOccupancy":{"type":"integer","description":"Zone Occupancy"},"gateDemand":{"type":"integer","description":"Forecast guests per hour at peak across gates"},"groupArrivalPressure":{"type":"string","description":"Group Arrival Pressure"},"reEntryDemand":{"type":"string","description":"Re-entry Demand"},"deviceCapacity":{"type":"integer","description":"Device Capacity"},"currentPlanned":{"type":"integer","description":"Entry lanes currently planned"},"recommendedEntryLanes":{"type":"integer"},"aiRecommendation":{"type":"string","description":"Advisory text only; any operational change goes through the normal permission and approval controls"}}},
"AttendanceAdmissionAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Attendance & Admission Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ticketsSold":{"type":"integer","description":"Tickets Sold"},"ticketsEligibleToday":{"type":"integer","description":"Tickets Eligible Today"},"ticketsScanned":{"type":"integer","description":"Tickets Scanned"},"uniqueGuests":{"type":"integer","description":"Unique Guests"},"noShows":{"type":"integer","description":"No-Shows"},"groupAttendance":{"type":"integer","description":"Group Attendance"},"membershipAttendance":{"type":"integer","description":"Membership Attendance"},"repeatEntry":{"type":"integer","description":"Repeat Entry"},"attendanceRate":{"type":"number","description":"Percent"},"noShowRate":{"type":"number","description":"no-show rate"}}},
"Cadence": {"x-ticvai-persistence":"none — embedded in schedule","type":"object","description":"**What each frequency needs (decided 28 September, audit R158).** `daily`: `timeOfDay`. `weekly`: `dayOfWeek` and `timeOfDay`. `monthly`: `dayOfMonth` and `timeOfDay`, a day past the month's end running on its last day. `quarterly`: `dayOfMonth` and `timeOfDay`, in the first month of each quarter. `onShiftClose` and `onPeriodClose`: nothing else, they run on the event. A field a frequency needs and does not have, or one it does not take, is the 400 on `createReportSchedule`. **Times are in the venue's time zone.**\n","required":["frequency"],"properties":{"frequency":{"type":"string","enum":["daily","weekly","monthly","quarterly","onShiftClose","onPeriodClose"]},"dayOfWeek":{"type":"integer","minimum":0,"maximum":6},"dayOfMonth":{"type":"integer","minimum":1,"maximum":31},"timeOfDay":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"timeZone":{"type":"string","readOnly":true,"description":"Always the venue's time zone (decided 28 September, audit R158), returned so a reader knows which. Not taken on a write."}}},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"CreateReportScheduleRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["reportId","cadence","recipients","format"],"properties":{"reportId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"cadence":{"$ref":"#/components/schemas/Cadence"},"parameters":{"type":"object","additionalProperties":true,"description":"As `RunReportRequest.parameters` — keyed by the report's `ReportParameter.key`, applied to every run."},"recipients":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/Recipient"}},"format":{"$ref":"#/components/schemas/ExportFormat"},"includePersonalData":{"type":"boolean","default":false},"skipIfEmpty":{"type":"boolean","default":true,"description":"An empty report every morning trains people to ignore the report."}}},
"EntryExitReEntryCrossoverAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Entry, Exit, Re-entry & Crossover Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"reEntryRate":{"type":"number","description":"Re-entry rate"},"averageTimeOutside":{"type":"integer","description":"Minutes"},"mostUsedReEntryGates":{"type":"array","items":{"type":"string"},"description":"most-used re-entry gates"},"rejectedReEntry":{"type":"integer","description":"rejected re-entry"},"reEntryByProduct":{"type":"array","items":{"type":"string"},"description":"Product and re-entry count pairs"},"crossoverTime":{"type":"integer","description":"Average minutes between leaving one park and entering the next"},"crossoverProduct":{"type":"array","items":{"type":"string"},"description":"Products used for crossover, with counts"},"crossoverUtilization":{"type":"number","description":"crossover utilization"},"firstEntries":{"type":"integer"},"temporaryExits":{"type":"integer"},"reEntries":{"type":"integer"},"crossovers":{"type":"integer"},"finalExits":{"type":"integer"},"crossoverFlows":{"type":"array","items":{"type":"string"},"description":"From park, to park and count, e.g. Park A to Park B"}}},
"ExecutionStatus": {"type":"string","enum":["queued","running","completed","failed","cancelled","expired"]},
"ExportFormat": {"type":"string","enum":["csv","xlsx","pdf","json"]},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"GraphicalAccessMapLiveGatePerformanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Graphical Access Map & Live Gate Performance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"accessPointId":{"type":"string"},"pointType":{"type":"string","enum":["gate","turnstile","entryPoint","exitPoint","reEntryGate","groupGate","vipGate","attractionAccess","crossoverPoint"]},"status":{"type":"string","enum":["healthy","warning","critical","offline"]},"guests":{"type":"integer","description":"Guests (the pack shows 4,821)"},"success":{"type":"number","description":"Success rate, percent"},"reject":{"type":"number","description":"Reject rate, percent"},"yellow":{"type":"number","description":"Operator-review rate, percent"},"name":{"type":"string"},"parentId":{"type":"string","description":"Zone or park the point sits in"},"throughputPerMinute":{"type":"number"},"averageValidationSeconds":{"type":"number"}},"required":["accessPointId","pointType","status"]},
"GuestDwellTimeLengthOfStayAttractionFlowView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Guest Dwell Time, Length of Stay & Attraction Flow displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"averageLengthOfStay":{"type":"integer","description":"Minutes, where entry and exit data exist"},"medianStay":{"type":"integer","description":"Minutes"},"peakArrival":{"type":"string","description":"Time window, e.g. 09:40-10:30"},"peakDeparture":{"type":"string","description":"Time window"},"zoneDwellTime":{"type":"integer","description":"Average minutes in the selected zone"},"attractionVisits":{"type":"integer","description":"Attraction Visits"},"fastPassUsage":{"type":"integer","description":"Fast Pass Usage"},"reEntryBehavior":{"type":"string","description":"Re-entry behavior"},"uniqueGuests":{"type":"integer","description":"Unique Guests (the pack shows 5,842)"},"totalValidations":{"type":"integer","description":"Total Validations (the pack shows 6,211)"},"repeatVisits":{"type":"integer","description":"Repeat Visits (the pack shows 369)"}}},
"LiveVenueOccupancyPeopleCountingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Live Venue Occupancy & People Counting displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"areaLevel":{"type":"string","enum":["venue","park","zone","attraction","controlledArea"]},"areaId":{"type":"string"},"exits":{"type":"integer","description":"Exits (the pack shows ±)"},"operationalAdjustments":{"type":"integer","description":"Operational Adjustments (the pack shows =)"},"current":{"type":"integer","description":"Current (the pack shows 8,214)"},"capacity":{"type":"integer","description":"Capacity (the pack shows 12,000)"},"occupancy":{"type":"number","description":"Percent of capacity"},"areaName":{"type":"string"},"parentAreaId":{"type":"string"},"entries":{"type":"integer"},"status":{"type":"string","enum":["normal","warning","high","critical"],"description":"Band from the configured occupancy thresholds"}},"required":["areaId","areaLevel"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Recipient": {"x-ticvai-persistence":"reporting.schedule_recipient","type":"object","description":"One recipient of a schedule. **A row of `reporting.schedule_recipient`, a child of `reporting.schedule`** — `ReportSchedule` declares the pair, which is what gives the table its `schedule_id`. Pull audit 26 September: declared on its own, the table had no column tying a recipient to its schedule.\n","required":["kind","address"],"properties":{"kind":{"type":"string","enum":["principal","email","sftp","webhook"]},"address":{"type":"string"},"principalId":{"type":"string","format":"uuid"}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportSchedule": {"x-ticvai-persistence":"reporting.schedule + reporting.schedule_recipient","allOf":[{"$ref":"#/components/schemas/CreateReportScheduleRequest"},{"type":"object","required":["id","ownerPrincipalId","isPaused","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid","description":"The schedule runs under this principal's permissions, not the recipients'. A standing grant of whatever the owner can see.\n"},"isPaused":{"type":"boolean"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastRunStatus":{"$ref":"#/components/schemas/ExecutionStatus"},"nextRunAt":{"type":"string","format":"date-time","nullable":true},"consecutiveFailures":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}}]},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"ThroughputQueueValidationPerformanceAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Throughput, Queue & Validation Performance Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"gateId":{"type":"string"},"guestsPerMinute":{"type":"number","description":"Guests per Minute"},"guestsPerHour":{"type":"integer","description":"Guests per Hour"},"averageScanTime":{"type":"number","description":"Seconds"},"averageGateCycle":{"type":"number","description":"Seconds"},"successRate":{"type":"number","description":"Success Rate"},"yellowRate":{"type":"number","description":"Yellow Rate"},"manualInterventionRate":{"type":"number","description":"Manual Intervention Rate"},"downtime":{"type":"integer","description":"Minutes"},"bottleneckReason":{"type":"string","enum":["qrReadFailures","excessiveManualVerification","hardwareLatency","policyComplexity","wrongGuestRouting"],"description":"Vocabulary listed under Potential reasons."},"gateName":{"type":"string"},"rejectRate":{"type":"number","description":"Percent"},"underperforming":{"type":"boolean"}},"required":["gateId"]},
"ValidationOutcomeRejectionAnalyticsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over access state, assembled at read time from tables that already exist","description":"**What Validation Outcome & Rejection Analytics displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"rejected":{"type":"integer","description":"Rejected (the pack shows 482)"},"overrides":{"type":"integer","description":"Overrides (the pack shows 281)"},"allowedRate":{"type":"number","description":"Percent"},"operatorReviewRate":{"type":"number","description":"Percent"},"deniedRate":{"type":"number","description":"Percent"},"overrideRate":{"type":"number","description":"Overrides as a percent of rejections"},"rejectionReasons":{"type":"array","items":{"type":"string"},"description":"Reason, count and share, e.g. Wrong Visit Date"}}}
}
```
