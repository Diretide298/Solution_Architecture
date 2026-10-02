# WS71 — Unified BI Reporting and AI Analytics Platform board 10

**10 screens · 17 operations · 21 schemas · 6 permissions**

Platform P16 Venue Analytics · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `AI_AUDIT_VIEW, AUDIT_VIEW, REPORT_GOVERNANCE_MANAGE, REPORT_MANAGE, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `ANL-061` | BI & Analytics Administration Command Center | B–D | 0 | 2 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-062` | Enterprise KPI Library | B–D | 0 | 28 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-063` | KPI Targets, Thresholds & Scorecards | B–D | 8 | 0 | 5 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-064` | Benchmark & Comparative Analytics Configuration | B–D | 12 | 8 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-065` | Data Source & Integration Registry | B–D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-066` | Semantic Model & Business Data Catalogue | A | 14 | 19 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-067` | Data Refresh, Pipeline & Data Health Monitor | B–D | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-068` | Embedded BI, Workspace & Tenant Administration | B–D | 7 | 0 | 5 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-069` | Analytics Performance, Usage & Cost Monitor | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-070` | Analytics Governance, Security & Audit Center | B–D | 20 | 91 | 6 | 6 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-062, ANL-065 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-061` BI & Analytics Administration Command Center

**Provide administrators with one consolidated view of the health and governance of the TICVAI analytics platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each component shall show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/bi-analytics-administration-command-center-anl-061` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The analytics administrator's one view of platform health: data freshness, failed refreshes, usage, KPIs in force, open alerts. The thing to get right: freshness first, because a revenue figure that stopped updating at nine this morning looks exactly like a low number; and counters with no source (data quality score, BI service health, AI analytics health) are drawn as pending, not invented.

**Known correction pending (do not draw the wrong version)**

- **Data Quality Score, BI Service Health and AI Analytics Health** Why: Nothing measures them; a pipeline carries freshness and last error only. *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline / screens/P16-venue-analytics.yaml#ANL-061; Finance, Ledger & Tax · Reporting & Analytics)*
- **Active Alerts tile with no alert read declared** Why: Alerts exist (list of current alerts) but the screen does not call it. *(source: contracts/satellite/reporting.yaml#listAlerts; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getAnalyticsUsage` ?from |
| Group by | radio group | — | Report · Dashboard · User · Venue | `getAnalyticsUsage` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Dashboards** (metric tile)

**Active Reports** (metric tile)

**Published KPIs** (metric tile)

**Connected Data Sources** (metric tile)

**Active Datasets** (metric tile)

**Data Refresh Success %** (metric tile)

**Data Quality Score** (metric tile)

**Failed Refreshes** (metric tile)

**BI Service Health** (metric tile)

**AI Analytics Health** (metric tile)

**Active Alerts** (metric tile)

**Analytics Users** (metric tile)

**Every analytics administration** (data table)

| Shows | Format | Notes |
|---|---|---|
| Healthy / warning / critical / offline | text | not in the schema: `Healthy / Warning / Critical / Offline` |

**The selected analytics administration** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Healthy / warning / critical / offline | text | not in the schema: `Healthy / Warning / Critical / Offline` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **headline counters (available)**: Pipelines by status (Healthy, Degraded, Stale, Failed, Paused), stale datasets, failed refreshes now, active dashboards, active KPIs, analytics users in the period (distinct users from usage). *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline / contracts/satellite/reporting.yaml#listDashboards / contracts/satellite/reporting.yaml#listKpis / …)*
- **headline counters (pending)**: Data refresh success % over a period (only each pipeline's latest state is known), data quality score, BI service health, AI analytics health; active reports (no count). Greyed, "Not yet available". *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline)*
- **component health list**: One row per pipeline and its datasets, worded with the pipeline statuses, worst first, each with "Updated 38 min ago - expected every 15 min". The pack's Healthy / Warning / Critical / Offline maps to Healthy / Degraded or Stale / Failed / Paused. *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline / screens/P16-venue-analytics.yaml#ANL-061)*
- **why a KPI is failing**: KPIs in Critical link to their explanation (AI explains why a metric moved and suggests actions); AI never decides approvals. *(source: DI-720 / DI-719 / DI-735)*

**Data it reads**: `getAnalyticsUsage` (onLoad, Estate at a glance); `listAnalyticsPipelines` (onLoad, Data health)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*
- → `ANL-070` Analytics Governance, Security & Audit Center: *Analytics Governance, Security & Audit Center*
- → `ANL-062` Enterprise KPI Library: *Enterprise KPI Library*
- → `ANL-063` KPI Targets, Thresholds & Scorecards: *KPI Targets, Thresholds & Scorecards*
- → `ANL-064` Benchmark & Comparative Analytics Configuration: *Benchmark & Comparative Analytics Configuration*
- → `ANL-065` Data Source & Integration Registry: *Data Source & Integration Registry*
- → `ANL-066` Semantic Model & Business Data Catalogue: *Semantic Model & Business Data Catalogue*
- → `ANL-067` Data Refresh, Pipeline & Data Health Monitor: *Data Refresh, Pipeline & Data Health Monitor*
- → `ANL-068` Embedded BI, Workspace & Tenant Administration: *Embedded BI, Workspace & Tenant Administration*
- → `ANL-069` Analytics Performance, Usage & Cost Monitor: *Analytics Performance, Usage & Cost Monitor*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The analytics administration list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the analytics administration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No analytics administration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the analytics administration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `ANL-067`: Same pipeline rows and status words.
- Match `ANL-041`: Same counter style as the reporting governance board.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
counters:
  pipelines: 11 healthy, 1 stale, 1 failed
  staleDatasets: 2
  activeDashboards: 46
  activeKpis: 28
  users30d: 134
worst:
- pipeline: Ticketing orders to replica
  status: Stale
  freshness: Updated 38 min ago - expected every 15 min
  datasets:
  - Orders
  - Order lines
- pipeline: Google Analytics sessions
  status: Failed
  lastError: Credential expired
  lastSuccess: 30 Sep 2026 22:00
```

#### Permissions

- `getAnalyticsUsage` → `REPORT_VIEW_TENANT` (operate) · staff
- `listAnalyticsPipelines` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-061` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-061`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 1: Opens BI & Analytics Administration Command Center → Provide administrators with one consolidated view of the health and governance of the TICVAI analytics platform.
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F180 branch at step 1 (expected): when Nothing has been set up on BI & Analytics Administration Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F180 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-061?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-070`, `ANL-062`, `ANL-063`, `ANL-064`, `ANL-065`, `ANL-066`, `ANL-067`, `ANL-068`, `ANL-069`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-062` Enterprise KPI Library

**Maintain the authoritative catalogue of approved TICVAI business KPIs. This is essential because every dashboard must use the same definition of a metric.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§KPI Categories; KPI Status) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/enterprise-kpi-library-anl-062` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The authoritative catalogue of KPIs: one definition, referenced everywhere, so "revenue" means the same thing on every dashboard. Each KPI has a business name, a formula written against the semantic model (never SQL), a unit, a direction, an owner and a default period. The thing to get right: finance labels - Gross sales, Net revenue, Recognised and Deferred revenue are different measures - and today the only seeded money KPI is Takings.

**Known correction pending (do not draw the wrong version)**

- **No finance measures exist to build finance KPIs from** Why: The closed metric list has no gross sales, net revenue, refunds, refund rate, tax or average ticket value; the only seeded money KPI is Takings. Finance tile formulas are an open decision. *(source: contracts/satellite/reporting.yaml#MetricSource / contracts/satellite/reporting.yaml#ReportingSystemKpi / MoM 2026-08-12 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities; Finance, Ledger & Tax · Reporting & Analytics)*
- **Takings is described both as "gross value of payments" and as "payments less refunds"** Why: Less refunds is not gross; a tile labelled from either description would mislead, and neither is Net revenue. *(source: contracts/satellite/reporting.yaml#getKpiValues / contracts/satellite/reporting.yaml#ReportingSystemKpi / R283; Finance, Ledger & Tax · Reporting & Analytics)*
- **No edit, deactivate or delete for a KPI, and no KPI status beyond active** Why: Only list and create exist; the pack's KPI Status (draft, certified, deprecated) and a deprecation workflow have no field or operation. *(source: contracts/satellite/reporting.yaml#listKpis / contracts/satellite/reporting.yaml#createKpi / MATRIX 13.1.32; Finance, Ledger & Tax · Reporting & Analytics)*
- **The 14 "columns" are domain values** Why: Executive ... Resources are values of the KPI's domain, a filter, not columns. *(source: screens/P16-venue-analytics.yaml#ANL-062; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which finance KPIs ship (gross sales, net revenue, recognised and deferred revenue, refunds) and with what formulas?** → Finance KPIs seeded with formulas. *(decided by Chinmay, 2026-10-02; DEC-351 / CHG-FIN-007 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **code, name, description, domain**: Code is system-facing and never shown; the name is the label every tile uses. Domain is the grouping (Executive, Sales, Finance, Operations, Access, Customer, Membership, Loyalty, Marketing, F&B, Retail, Inventory, Resources). *(source: contracts/satellite/reporting.yaml#KpiDefinition)*
- **formula**: Built from semantic-model measures with a formula editor that offers only catalogue names; no free SQL. *(source: contracts/satellite/reporting.yaml#KpiDefinition / MATRIX 8.7.11 / MATRIX 6.1.78)*
- **unit, higherIsBetter**: Currency, count, percentage, duration, ratio, score. Higher-is-better decides whether Warning means below or above target. *(source: contracts/satellite/reporting.yaml#KpiDefinition)*

#### Outputs: what the screen shows and produces

**Shown**

**Every enterprise kpi** (data table)

| Shows | Format | Notes |
|---|---|---|
| Executive | text | not in the schema: `Executive` |
| Sales | text | not in the schema: `Sales` |
| Revenue | text | not in the schema: `Revenue` |
| Finance | text | not in the schema: `Finance` |
| Operations | text | not in the schema: `Operations` |
| Access | text | not in the schema: `Access` |
| Customer | text | not in the schema: `Customer` |
| Membership | text | not in the schema: `Membership` |
| Loyalty | text | not in the schema: `Loyalty` |
| Marketing | text | not in the schema: `Marketing` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Inventory | text | not in the schema: `Inventory` |
| Resources | text | not in the schema: `Resources` |

**The selected enterprise kpi** (detail panel): The pack groups this record's detail under its own headings: “Formula”.

| Shows | Format | Notes |
|---|---|---|
| Executive | text | not in the schema: `Executive` |
| Sales | text | not in the schema: `Sales` |
| Revenue | text | not in the schema: `Revenue` |
| Finance | text | not in the schema: `Finance` |
| Operations | text | not in the schema: `Operations` |
| Access | text | not in the schema: `Access` |
| Customer | text | not in the schema: `Customer` |
| Membership | text | not in the schema: `Membership` |
| Loyalty | text | not in the schema: `Loyalty` |
| Marketing | text | not in the schema: `Marketing` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Inventory | text | not in the schema: `Inventory` |
| Resources | text | not in the schema: `Resources` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **KPI row**: Name, domain, unit, direction arrow, owner, default period, Active/Inactive, Standard badge for seeded KPIs, and a "Used on 7 dashboards" count where known. *(source: contracts/satellite/reporting.yaml#KpiDefinition / contracts/satellite/reporting.yaml#ReportingSystemKpi)*
- **definition panel**: Formula in words, source, owner and a worked example ("Net revenue = Gross sales - Discounts - Refunds, per finance policy"). *(source: MATRIX 8.7.21)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Add KPI**: Creates the definition tenant-wide. *(source: contracts/satellite/reporting.yaml#createKpi)*

**Data it reads**: `listKpis` (onLoad, The enterprise library)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The enterprise kpi list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the enterprise kpi untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No enterprise kpi yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the enterprise kpi are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Someone defines a second "Net revenue"**: Warn on duplicate names and point to the existing KPI; the model must hold one Net revenue across POS, B2C, B2B and OTA. *(source: MATRIX 8.7.21)*

#### Consistency with other screens

- Match `ANL-025`: The lead's KPI builder creates the same definition; this is the library view.
- Match `ANL-066`: Formulas name catalogue measures exactly as the catalogue spells them.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- name: Takings
  domain: Finance
  unit: Currency
  direction: up
  standard: true
  definition: Payments taken in the period less refunds
  example: AED 418,230.50 today
- name: Admissions
  domain: Access
  unit: Count
  direction: up
  standard: true
  example: 6,214 today
- name: Capacity utilisation
  domain: Operations
  unit: Percentage
  direction: down
  owner: Omar Haddad
- name: Net revenue (proposed)
  domain: Finance
  unit: Currency
  owner: Fatima Al Mansoori
  status: Awaiting formula
```

#### Permissions

- `listKpis` → `REPORT_VIEW_TENANT` (operate) · staff
- `createKpi` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-062` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-062`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 2: Works in Enterprise KPI Library → Maintain the authoritative catalogue of approved TICVAI business KPIs. This is essential because every dashboard must use the same definition of a metric.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-062?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-063` KPI Targets, Thresholds & Scorecards

**Centrally configure performance targets and thresholds used throughout TICVAI analytics.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Targets may be configured by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `kpiId` (navigation) |
| Route | `/analytics/kpi-targets-thresholds-scorecards-anl-063` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Central targets and scorecards: set targets per scope and period, and see every KPI against target with variance, direction and status. The thing to get right: targets exist for organisation, region and venue scopes and for a period - not per product or channel - and a stale value is marked as stale, never shown as a confident status.

**Known correction pending (do not draw the wrong version)**

- **Product, Channel, Attraction and Business Unit drawn as target dimensions** Why: A target is keyed on scope and period only. *(source: contracts/satellite/reporting.yaml#KpiTarget / screens/P16-venue-analytics.yaml#ANL-063; Finance, Ledger & Tax · Reporting & Analytics)*
- **Scorecards assume finance KPIs (net revenue, refund rate, average ticket value)** Why: None exists as a governed measure; only Takings and Admissions are seeded. *(source: contracts/satellite/reporting.yaml#MetricSource / contracts/satellite/reporting.yaml#ReportingSystemKpi; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Organization | select field | — | — | — | — | — | — |
| Site | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Business Unit | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Period | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |
| Module | field | — | — | `getKpiValues` ?module |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **scope (Organization, Site, Venue)**: A picker of the caller's own scope; a target outside it is refused. *(source: contracts/satellite/reporting.yaml#setKpiTargets)*
- **Attraction, Business Unit, Product, Channel (pack fields)**: Not target dimensions; draw them only as filters on the scorecard where the KPI can be broken down by them. *(source: contracts/satellite/reporting.yaml#KpiTarget / contracts/satellite/reporting.yaml#getKpiValues)*
- **compareTo (shown as "Compare with")**: Previous period, Same period last year, Target, Benchmark. *(source: contracts/satellite/reporting.yaml#getKpiValues)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **scorecard row**: KPI, actual, target, % of target with a progress bar, variance %, direction arrow, status word (On track, Warning, Critical, No target), as-of time; Critical first. Money in the venue currency at its scale. *(source: contracts/satellite/reporting.yaml#KpiValue / MATRIX 6.1.45 / MATRIX 6.1.78)*
- **stale value**: "Data delayed - as of 09:02" replaces the status colour; the value is still shown. *(source: contracts/satellite/reporting.yaml#KpiValue)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save targets**: Replaces the KPI's target set inside the caller's scope; rows left out are removed, so the grid always sends every row it shows and confirms removals. *(source: contracts/satellite/reporting.yaml#setKpiTargets)*

**Data it reads**: `getKpiValues` (onLoad, Where they stand)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The kpi targets thresholds configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the kpi targets thresholds untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No kpi targets thresholds configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Retail outlet monthly target**: Target versus achieved with variance per outlet per month is a target at the outlet's venue scope for that month. *(source: DI-368 / MoM 2026-08-19 4.9 Retail Intelligence & Reporting)*

#### Consistency with other screens

- Match `ANL-026`: Same band editor and status words.
- Match `ANL-064`: The "Compare with Benchmark" option uses the normalisation set there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- kpi: Takings
  scope: Aquaventure Waterpark
  period: Sep 2026
  actual: AED 11,842,300.25
  target: AED 12,500,000.00
  ofTarget: 94.7%
  variance: -5.3%
  status: Warning
- kpi: Admissions
  scope: Aquaventure Waterpark
  period: Sep 2026
  actual: 158,402
  target: 150,000
  ofTarget: 105.6%
  status: On track
- kpi: Takings
  scope: Lost Paradise of Dilmun
  period: Sep 2026
  actual: BHD 171,204.375
  target: BHD 185,500.000
  ofTarget: 92.3%
  status: Warning
```

#### Permissions

- `setKpiTargets` → `REPORT_MANAGE` (configure) · staff
- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*
- KPI threshold configuration defines normal/warning/critical bands per metric (e.g. capacity below 80% normal, 80-90% warning, above 95% critical), shown as status on the dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-704)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-063` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-063`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 4: Works in KPI Targets, Thresholds & Scorecards → Centrally configure performance targets and thresholds used throughout TICVAI analytics.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-063?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-064` Benchmark & Comparative Analytics Configuration

**Define how TICVAI compares performance between sites, periods and peer groups.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Support metrics such as) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/benchmark-comparative-analytics-configuration-anl-064` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Defines how sites are compared fairly: per visitor, per operating hour, per staffed position or per square metre, using denominators recorded per site and period. A water park and a museum differ on revenue per visitor for reasons that are not performance, so the basis always travels with the comparison. This is the one screen in the set with fully bound data.

**Known correction pending (do not draw the wrong version)**

- **Columns labelled with schema paths (SiteNormalisationBasis.id, .scopePath ...) and a free-text Scope path field** Why: Spec leak onto the screen; labels must be Site, From, To, Visitors, Operating hours, Staffed positions, Area, and the id is not shown. *(source: screens/P16-venue-analytics.yaml#ANL-064; Finance, Ledger & Tax · Reporting & Analytics)*
- **The pack's measures drawn as metric tiles (Revenue per Visitor, Entries per Gate per Hour, Incidents per 10,000 Visitors ...)** Why: They are comparison choices, not values; and gates and incidents are not normalisation bases, so two of the seven cannot be computed. Revenue per visitor needs a revenue KPI, which today is Takings only. *(source: contracts/satellite/reporting.yaml#BenchmarkNormalisation / contracts/satellite/reporting.yaml#ReportingSystemKpi; Finance, Ledger & Tax · Reporting & Analytics)*
- **The benchmark read is triggered on load with no KPI** Why: It requires a KPI id; the screen needs a KPI picker first. *(source: contracts/satellite/reporting.yaml#getAnalyticsBenchmark; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is saving bases a replace of the whole set or an upsert per site and period, and may periods overlap?** → Drawn default accepted: Upsert per site and period; overlapping periods refused. *(decided by Chinmay, 2026-10-02; DEC-352 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listSiteNormalisationBases`. | `listSiteNormalisationBases` ?scopePath |
| Period from | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?periodFrom=` to `listSiteNormalisationBases`. | `listSiteNormalisationBases` ?periodFrom |
| Period to | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?periodTo=` to `listSiteNormalisationBases`. | `listSiteNormalisationBases` ?periodTo |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpi | picker: choose a kpi | — | — | `getAnalyticsBenchmark` ?kpiId |
| Scope paths | text field | — | — | `getAnalyticsBenchmark` ?scopePaths |
| Normalise by | radio group | — | None · Per visitor · Per operating hour · Per staffed position · Per square metre | `getAnalyticsBenchmark` ?normaliseBy |

**Form: Save site normalisation basis** (modal, opened by *Save site normalisation basis*; *Save site normalisation basis* calls `setSiteNormalisationBasis`, *Cancel* sends nothing)

**Collects what `setSiteNormalisationBasis` sends before it is called.** Required: `bases`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Bases `bases` | repeatable rows | required | — | at least 1 | — | — | `setSiteNormalisationBasis` body |
| ID `bases[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `setSiteNormalisationBasis` body |
| Scope path `bases[].scopePath` | text field | required | — | — | — | The site (venue scope) the basis applies to. | `setSiteNormalisationBasis` body |
| Period start `bases[].periodStart` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setSiteNormalisationBasis` body |
| Period end `bases[].periodEnd` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setSiteNormalisationBasis` body |
| Visitors `bases[].visitors` | number field | optional | — | min 0 | — | `perVisitor`. | `setSiteNormalisationBasis` body |
| Operating hours `bases[].operatingHours` | number field (hours) | optional | — | min 0 | — | `perOperatingHour`. | `setSiteNormalisationBasis` body |
| Staffed positions `bases[].staffedPositions` | number field | optional | — | min 0 | — | `perStaffedPosition`. Average positions staffed over the period. | `setSiteNormalisationBasis` body |
| Area square metres `bases[].areaSquareMetres` | number field | optional | — | min 0 | — | `perSquareMetre`. Operated area. | `setSiteNormalisationBasis` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 422 A period ends before it starts, or overlaps another basis for the same site.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **site (pack "Scope path")**: A site picker; never a typed path. *(source: contracts/satellite/reporting.yaml#SiteNormalisationBasis)*
- **periodStart, periodEnd**: Required; one basis per site per period. Periods for one site should not overlap (see decisions). *(source: contracts/satellite/reporting.yaml#SiteNormalisationBasis)*
- **visitors, operatingHours, staffedPositions, areaSquareMetres**: Whole visitors; hours, positions (average staffed over the period) and area to one decimal; none negative; leave empty when not applicable (a ride-only site has no meaningful area). *(source: contracts/satellite/reporting.yaml#SiteNormalisationBasis)*
- **KPI to benchmark**: Required before any comparison loads; the benchmark read needs a KPI. *(source: contracts/satellite/reporting.yaml#getAnalyticsBenchmark)*

#### Outputs: what the screen shows and produces

**Shown**

**Revenue per Visitor** (metric tile)

**Transactions per 1,000 Visitors** (metric tile)

**Entries per Gate per Hour** (metric tile)

**Incidents per 10,000 Visitors** (metric tile)

**Revenue per m² where applicable** (metric tile)

**Revenue per Operating Hour** (metric tile)

**Utilization %** (metric tile)

**Every site normalisation basis** (data table, from `listSiteNormalisationBases`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Scope path | text | The site (venue scope) the basis applies to. |
| Period start | 1 Oct 2026 | — |
| Period end | 1 Oct 2026 | — |
| Visitors | 1,234 | `perVisitor`. |
| Operating hours | 1,234.5 | `perOperatingHour`. |
| Staffed positions | 1,234.5 | `perStaffedPosition`. Average positions staffed over the period. |
| Area square metres | 1,234.5 | `perSquareMetre`. Operated area. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save site normalisation basis (primary button) | `setSiteNormalisationBasis` PUT `/site-normalisation-bases` | inline | SiteNormalisationBasis[] | 403 Authenticated but not permitted at the requested scope; 422 A period ends before it starts, or overlaps another basis for the same site. | gated `REPORT_MANAGE`; opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **comparison**: Per site - value, normalised value with its basis in the label ("AED 96.40 per visitor"), rank and percentile. *(source: contracts/satellite/reporting.yaml#BenchmarkRow)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save basis**: Saves the denominators for the selected sites and periods. *(source: contracts/satellite/reporting.yaml#setSiteNormalisationBasis)*

**Data it reads**: `getAnalyticsBenchmark` (onLoad, Configure the comparison basis); `listSiteNormalisationBases` (onLoad, The denominators each site is benchmarked by)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The benchmark comparative analytics list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the benchmark comparative analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No benchmark comparative analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the benchmark comparative analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A period ends before it starts, or overlaps another basis for the same site. |

#### Edge cases to draw

- **A site with no basis for the period**: Its normalised value is empty with "No visitors recorded for Sep 2026 - add a basis"; it is not ranked. *(source: contracts/satellite/reporting.yaml#BenchmarkRow)*

#### Consistency with other screens

- Match `ANL-020`: The multi-site comparison screen reads these comparisons; same basis wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
bases:
- site: Aquaventure Waterpark
  period: Sep 2026
  visitors: 158402
  operatingHours: 300
  staffedPositions: 214.5
  area: 102,000 m²
- site: House of Wisdom, Sharjah
  period: Sep 2026
  visitors: 41250
  operatingHours: 330
  staffedPositions: 38.0
  area: 15,000 m²
comparison:
- site: Aquaventure Waterpark
  kpi: Takings
  value: AED 11,842,300.25
  perVisitor: AED 74.76
  rank: 1
- site: House of Wisdom, Sharjah
  kpi: Takings
  value: AED 1,212,950.00
  perVisitor: AED 29.40
  rank: 2
```

#### Permissions

- `getAnalyticsBenchmark` → `REPORT_VIEW_TENANT` (operate) · staff
- `listSiteNormalisationBases` → `REPORT_VIEW_TENANT` (operate) · staff
- `setSiteNormalisationBasis` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI/benchmarking admin board defines each KPI's target, data sources and rules, and shows why a KPI is failing and what actions could help meet it. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-720)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-064` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-064`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 6: Works in Benchmark & Comparative Analytics Configuration → Define how TICVAI compares performance between sites, periods and peer groups.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403, 422).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-064?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save site normalisation basis.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-065` Data Source & Integration Registry

**Maintain a centralized catalogue of data sources feeding the analytics platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/data-source-integration-registry-anl-065` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The register of every source feeding analytics, its refresh state and its health. Read-only: sources are connected by the platform, not added here. The thing to get right is the security principle the pack calls out: connection details and credentials are never displayed, only whether the connection works.

**Known correction pending (do not draw the wrong version)**

- **Empty first-run state "carries the create action"** Why: There is no operation to add or edit a source; the registry is read-only. *(source: contracts/satellite/reporting.yaml#listAnalyticsPipelines / screens/P16-venue-analytics.yaml#ANL-065; Finance, Ledger & Tax · Reporting & Analytics)*
- **One row per source assumed; the data is one row per pipeline** Why: A source with two pipelines shows twice; group rows by source name. *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every data source integration** (data table)

| Shows | Format | Notes |
|---|---|---|
| Source name | text | not in the schema: `Source Name` |
| Source type | text | not in the schema: `Source Type` |
| Owner | text | not in the schema: `Owner` |
| Connection | text | not in the schema: `Connection` |
| Authentication method | text | not in the schema: `Authentication Method` |
| Refresh type | text | not in the schema: `Refresh Type` |
| Last sync | text | not in the schema: `Last Sync` |
| Records processed | text | not in the schema: `Records Processed` |
| Status | text | not in the schema: `Status` |
| Data classification | text | not in the schema: `Data Classification` |

**The selected data source integration** (detail panel): The pack groups this record's detail under its own headings: “Important Security Principle”.

| Shows | Format | Notes |
|---|---|---|
| Source name | text | not in the schema: `Source Name` |
| Source type | text | not in the schema: `Source Type` |
| Owner | text | not in the schema: `Owner` |
| Connection | text | not in the schema: `Connection` |
| Authentication method | text | not in the schema: `Authentication Method` |
| Refresh type | text | not in the schema: `Refresh Type` |
| Last sync | text | not in the schema: `Last Sync` |
| Records processed | text | not in the schema: `Records Processed` |
| Status | text | not in the schema: `Status` |
| Data classification | text | not in the schema: `Data Classification` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **row**: Source name, kind (operational replica, Google Analytics, file import ...), refresh schedule in words, last successful sync, last attempt, rows in the last run, status, last error in words, the datasets it feeds. Failed and stale first. *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline / contracts/satellite/reporting.yaml#listAnalyticsPipelines)*
- **Owner, Connection, Authentication method, Data classification**: Not stored; Authentication is never shown beyond "Connected" or "Credential expired". *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline)*

**Data it reads**: `listAnalyticsPipelines` (onLoad, Sources and integrations)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data source integration list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data source integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data source integration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data source integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Google Analytics conversion source fails**: Conversion tiles show "Data delayed"; the row names the affected datasets. *(source: MoM 2026-09-08 4.2 Command Center Overview (Board 1) / contracts/satellite/reporting.yaml#AnalyticsPipeline)*

#### Consistency with other screens

- Match `ANL-067`: Same rows; ANL-067 adds the time view and quality checks.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- name: Ticketing and orders (replica)
  kind: Operational replica
  schedule: Continuous
  lastSuccess: Updated 40 sec ago
  rows: 18240
  status: Healthy
  feeds:
  - Orders
  - Order lines
  - Payments
- name: Google Analytics - web sessions
  kind: External
  schedule: Every hour
  lastSuccess: 30 Sep 2026 22:00
  status: Failed
  error: Credential expired
  feeds:
  - Web sessions
```

#### Permissions

- `listAnalyticsPipelines` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-065` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-065`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 8: Works in Data Source & Integration Registry → Maintain a centralized catalogue of data sources feeding the analytics platform.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-065?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-066` Semantic Model & Business Data Catalogue

**Create the governed business layer between raw data and dashboards/AI. This is one of the most important technical screens in Board 10.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block A · ticket #20784 (APP-SETUP-ANL-066) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `getSemanticModel` reads the model as a tree; the selection is a domain, dataset or field (CHG-SOT-012). |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/semantic-model-business-data-catalogue-anl-066` |

**Known gaps.** **No certification, owner, glossary or lineage on a dataset or field** (design-notes correction ANL-066). The client asks for certified badges with owner, glossary and lineage; the model holds none …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The governed business layer between raw data and dashboards, reports and AI: domains, datasets with their grain, fields with labels, types, default aggregation and a personal-data flag, and how datasets relate. The one thing to get right: publishing replaces the whole model, so anything left out disappears from every report that used it; the design must show what a publish removes.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- There is no certification, owner or lineage on a dataset or field. (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): The gap says the operations return no schema with described properties. (CHG-SOT-012).

#### Inputs: what the user enters or picks

**Form: Publish model** (confirmDialog, opened by *Publish model*; *Publish model* calls `setSemanticModel`, *Cancel* sends nothing)

**Names what changes for report authors** (fields added, removed or renamed, relationships changed) before the new version is published. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Domains `domains` | repeatable rows | optional | — | — | — | — | `setSemanticModel` body |
| Code `domains[].code` | text field | optional | — | — | — | — | `setSemanticModel` body |
| Name `domains[].name` | text field | optional | — | — | — | — | `setSemanticModel` body |
| Description `domains[].description` | text area | optional | — | — | — | — | `setSemanticModel` body |
| Datasets `domains[].datasets` | repeatable rows | optional | — | — | — | — | `setSemanticModel` body |
| Code `domains[].datasets[].code` | text field | optional | — | — | — | — | `setSemanticModel` body |
| Name `domains[].datasets[].name` | text field | optional | — | — | — | — | `setSemanticModel` body |
| Grain `domains[].datasets[].grain` | text field | optional | — | — | — | What one row means. The single most common cause of a wrong report is a join that silently multiplied the grain. | `setSemanticModel` body |
| Fields `domains[].datasets[].fields` | repeatable rows | optional | — | — | — | — | `setSemanticModel` body |
| Relationships `relationships` | repeatable rows | optional | — | — | — | — | `setSemanticModel` body |
| From dataset `relationships[].fromDataset` | text field | optional | — | — | — | — | `setSemanticModel` body |
| To dataset `relationships[].toDataset` | text field | optional | — | — | — | — | `setSemanticModel` body |
| Cardinality `relationships[].cardinality` | radio group | optional | — | One to one · One to many · Many to one · Many to many | — | — | `setSemanticModel` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setSemanticModel` body |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Dataset grain**: A required sentence "One row is one …" for each dataset; the most common cause of a wrong report is a silently multiplied grain. *(source: contracts/satellite/reporting.yaml#/components/schemas/SemanticModel)*
- **Field**: Code, business label, data type, default aggregation, description, and Personal data on or off. *(source: contracts/satellite/reporting.yaml#/components/schemas/SemanticModel)*
- **Relationship**: From dataset, to dataset, cardinality (one-to-one, one-to-many, many-to-one, many-to-many); many-to-many shown with a warning. *(source: contracts/satellite/reporting.yaml#/components/schemas/SemanticModel)*

#### Outputs: what the screen shows and produces

**Shown**

**Domains, datasets and fields** (tree nav, from `getSemanticModel`): Domain (code, name), then its datasets (name and **grain: what one row means**), then their fields (label, data type, default aggregation, sensitive).

| Shows | Format | Notes |
|---|---|---|
| Domains | list or chips (count when long) | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Datasets | list or chips (count when long) | — |
| Code | text | — |
| Name | text | — |
| Grain | text | What one row means. The single most common cause of a wrong report is a join that silently multiplied the grain. |
| Fields | list or chips (count when long) | — |
| Relationships | list or chips (count when long) | — |
| From dataset | text | — |
| To dataset | text | — |
| Cardinality | chip: One to one, One to many, Many to one, Many to many | — |
| Published at | 1 Oct 2026, 14:30 | — |

**Relationships** (data table, from `getSemanticModel`): From dataset, to dataset, cardinality. The pack's checks (missing, circular, duplicate aggregation risk, invalid cardinality, broken references) flag rows here before publish.

| Shows | Format | Notes |
|---|---|---|
| Relationships | list or chips (count when long) | — |

**The model** (detail panel, from `getSemanticModel`)

| Shows | Format | Notes |
|---|---|---|
| Version | 1,234 | Assigned by the server on each publish. |
| Published at | 1 Oct 2026, 14:30 | — |
| Domains | list or chips (count when long) | — |
| Relationships | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish model (primary button) | `setSemanticModel` PUT `/semantic-model` | SemanticModel | SemanticModel | — | opens confirmDialog first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Catalogue tree**: Domain → dataset → fields, with the published version number and date. *(source: contracts/satellite/reporting.yaml#getSemanticModel)*
- **Publish preview**: Added, changed and removed datasets and fields, and the reports and KPIs that use each removed one. *(source: contracts/satellite/reporting.yaml#setSemanticModel)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Publish**: Replaces the model and assigns the next version; reports resolve their fields against it. *(source: contracts/satellite/reporting.yaml#setSemanticModel)*

**Data it reads**: `getSemanticModel` (onLoad, The catalogue)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The semantic model. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No model published yet. Offers Publish model (`setSemanticModel`); until then reports read the seeded catalogue. |
| Empty, no results (`?state=emptyNoResults`) | Nothing in the model matches the search. Names it and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_TENANT`, which `getSemanticModel` requires, and names that permission. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A personal-data field is added to a dataset used by scheduled reports**: Warn that exports of it need the personal-data export permission and are audited. *(source: contracts/shared/permissions.yaml#/components/schemas/Permission / MATRIX 8.3.73)*

#### Consistency with other screens

- Match `ANL-033`: The dataset selector shows exactly this catalogue.
- Match `ANL-025`: KPI formulas reference these fields.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
domains:
- 'Sales · dataset Sales lines (one row is one order line) · fields: sale date, channel, product, gross amount,
  discount, VAT, net amount'
- 'Admissions · dataset Scans (one row is one admitted scan) · fields: scan time, gate, product, guest (personal
  data)'
- 'Finance · dataset Postings (one row is one journal line) · fields: posted at, account, cost centre, debit, credit'
```

#### Permissions

- `getSemanticModel` → `REPORT_VIEW_TENANT` (operate) · staff
- `setSemanticModel` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_TENANT`, which `getSemanticModel` requires, and names that permission.

Screen guard: `REPORT_VIEW_TENANT`

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-066` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-066`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 10: Works in Semantic Model & Business Data Catalogue → Create the governed business layer between raw data and dashboards/AI. This is one of the most important technical screens in Board 10.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-066?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish model.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-067` Data Refresh, Pipeline & Data Health Monitor

**Monitor movement of information from operational systems into the analytics platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§KPI Cards) and a per-row directory (§Monitor) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/data-refresh-pipeline-data-health-monitor-anl-067` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Watches data moving from operations into analytics so stale or failed data is caught before anyone decides on it. The thing to get right: name what is affected ("Ticketing dataset delayed - affects Revenue Pulse and 4 other dashboards") and how late it is against what was expected.

**Known correction pending (do not draw the wrong version)**

- **Pipelines Running and Average Refresh Duration** Why: Pipeline status has no running value and no duration is recorded. *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline; Finance, Ledger & Tax · Reporting & Analytics)*
- **Completeness, accuracy checks, duplicates, missing values, schema changes, reconciliation status** Why: None is measured; only timeliness exists. *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline / MATRIX 8.7.21; Finance, Ledger & Tax · Reporting & Analytics)*
- **Affected dashboards cannot be computed** Why: A pipeline lists dataset codes, a report reads a data area from a different list and a tile reads a report; nothing links a stale dataset to the dashboards that show it. *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline / contracts/satellite/reporting.yaml#DataSource / contracts/satellite/reporting.yaml#DashboardTile; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Pipelines Running** (metric tile)

**Successful Refreshes** (metric tile)

**Failed Refreshes** (metric tile)

**Average Refresh Duration** (metric tile)

**Data Latency** (metric tile)

**Stale Datasets** (metric tile)

**Records Processed** (metric tile)

**Every data refresh pipeline** (data table)

| Shows | Format | Notes |
|---|---|---|
| Completeness | text | not in the schema: `Completeness` |
| Timeliness | text | not in the schema: `Timeliness` |
| Accuracy checks | text | not in the schema: `Accuracy checks` |
| Duplicate records | text | not in the schema: `Duplicate records` |
| Missing values | text | not in the schema: `Missing values` |
| Schema changes | text | not in the schema: `Schema changes` |
| Reconciliation status | text | not in the schema: `Reconciliation status` |

**The selected data refresh pipeline** (detail panel): The pack groups this record's detail under its own headings: “Source”, “Ticketing Dataset Delayed”, “Affected”.

| Shows | Format | Notes |
|---|---|---|
| Completeness | text | not in the schema: `Completeness` |
| Timeliness | text | not in the schema: `Timeliness` |
| Accuracy checks | text | not in the schema: `Accuracy checks` |
| Duplicate records | text | not in the schema: `Duplicate records` |
| Missing values | text | not in the schema: `Missing values` |
| Schema changes | text | not in the schema: `Schema changes` |
| Reconciliation status | text | not in the schema: `Reconciliation status` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **headline counters**: Stale datasets (freshness beyond expected), failed pipelines, worst latency ("38 min late"), rows processed in last runs. "Pipelines running" and "average refresh duration" have no source (see corrections). *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline)*
- **pipeline row**: Status, freshness against expected, last success, last error, datasets; Stale when freshness exceeds expected. *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline)*
- **replica lag**: The reporting replica's lag is part of freshness; reports state the replica position they read. *(source: contracts/satellite/reporting.yaml#ReportResult / TRACKER Actions row 255)*

**Data it reads**: `listAnalyticsPipelines` (onLoad, Refresh and freshness)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data refresh pipeline list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data refresh pipeline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data refresh pipeline yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data refresh pipeline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A KPI over a stale pipeline**: The KPI shows "Data delayed" everywhere it appears. *(source: contracts/satellite/reporting.yaml#KpiValue)*

#### Consistency with other screens

- Match `ANL-030`: Same freshness wording on the dashboard health panel.
- Match `ANL-061`: Same status words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
alert: Ticketing dataset delayed - last refreshed 09:02, expected every 15 min (38 min late)
pipelines:
- name: Ticketing orders to replica
  status: Stale
  freshness: 38 min (expected 15)
  lastSuccess: 01 Oct 2026 09:02
  datasets:
  - Orders
  - Order lines
- name: Access scans
  status: Healthy
  freshness: 1 min (expected 5)
  rowsLastRun: 6214
```

#### Permissions

- `listAnalyticsPipelines` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-067` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-067`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 12: Works in Data Refresh, Pipeline & Data Health Monitor → Monitor movement of information from operational systems into the analytics platform.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-067?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-068` Embedded BI, Workspace & Tenant Administration

**Configure how BI technology is embedded inside TICVAI and separated across clients/tenants.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/embedded-bi-workspace-tenant-administration-anl-068` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Workspace settings for analytics inside the tenant: default dashboard per role, theme from the tenant's brand, language, mobile and full-screen behaviour. The thing to get right: TICVAI's BI is native, there is no third-party BI engine to embed, and a tenant never sees or chooses another tenant.

**Known correction pending (do not draw the wrong version)**

- **The screen's premise is embedding a BI technology** Why: The decision is a native BI platform with no Power BI or other engine; the screen is workspace settings. *(source: TRACKER Actions row 253 / MoM 2026-09-08 4.1 Rationale for a Native BI/Reporting Platform; Finance, Ledger & Tax · Reporting & Analytics)*
- **None of the seven settings has a field or operation** Why: The screen only lists dashboards; default dashboard, theme, language, mobile and full-screen settings cannot be saved. *(source: contracts/satellite/reporting.yaml#listDashboards / screens/P16-venue-analytics.yaml#ANL-068; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where is the default dashboard per role stored?** → Drawn default accepted: Draw the setting; mark pending. *(decided by Chinmay, 2026-10-02; DEC-353 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Navigation | select field | — | — | — | — | — | — |
| Theme | select field | — | — | — | — | — | — |
| Branding | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Default Dashboard | select field | — | — | — | — | — | — |
| Mobile behavior | select field | — | — | — | — | — | — |
| Full-screen mode | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | field | — | — | `listDashboards` ?module |
| Include archived | toggle | off | — | `listDashboards` ?includeArchived |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Default dashboard**: Chosen from shared dashboards of the tenant; shown first in the command centre for that role. *(source: contracts/satellite/reporting.yaml#listDashboards / ADR-0041)*
- **Theme, Branding**: From the tenant's white-label tokens (logo, colours, fonts, status colours); not edited here. *(source: MATRIX 6.1.78)*
- **Full-screen mode, Mobile behaviour**: Presentation mode (wall display, large type, auto-refresh) and phone layout for executives on the move. *(source: MATRIX 8.7.23 / DI-696)*
- **Language**: English and Arabic; Arabic is right to left throughout. *(source: DI-019)*

#### Outputs: what the screen shows and produces

**Data it reads**: `listDashboards` (onLoad, Workspaces and embedding)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The embedded tenant administration configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the embedded tenant administration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No embedded tenant administration configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `ANL-001`: The default dashboard is what the executive command centre opens.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
defaults:
- role: Executive
  dashboard: Executive Performance
- role: Operations manager
  dashboard: Operations Control Room
  presentation: Wall display, refresh every 60 s
language:
- English
- Arabic
```

#### Permissions

- `listDashboards` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-068` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-068`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 14: Works in Embedded BI, Workspace & Tenant Administration → Configure how BI technology is embedded inside TICVAI and separated across clients/tenants.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-068?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-069` Analytics Performance, Usage & Cost Monitor

**Monitor BI adoption, system performance, capacity consumption and analytical operating costs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Usage KPIs; Performance KPIs) and a per-row directory (§Identify) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/analytics-performance-usage-cost-monitor-anl-069` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Shows which dashboards and reports are actually used, by whom, and how heavy they are, so the estate can be pruned: four hundred reports of which thirty are opened is four hundred things to maintain. The thing to get right: "cost" is a load indicator (rows scanned, runtime, refresh load), not money.

**Known correction pending (do not draw the wrong version)**

- **The usage read promises "what they cost" and returns no cost** Why: Rows carry opens, users, runtime and rows scanned only. *(source: contracts/satellite/reporting.yaml#getAnalyticsUsage / contracts/satellite/reporting.yaml#AnalyticsUsageRow; Finance, Ledger & Tax · Reporting & Analytics)*
- **AI Queries, Exports, API Requests, Peak Concurrent Users, Dashboard Load Time, Failed Queries, Dataset Size, Refresh Duration, Embedded BI Availability** Why: No source records them; draw as pending. *(source: contracts/satellite/reporting.yaml#AnalyticsUsageRow / screens/P16-venue-analytics.yaml#ANL-069; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getAnalyticsUsage` ?from |
| Group by | radio group | — | Report · Dashboard · User · Venue | `getAnalyticsUsage` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **groupBy (shown as "By")**: Dashboard, Report, User, Venue. *(source: contracts/satellite/reporting.yaml#getAnalyticsUsage)*
- **from**: Default last 30 days. *(source: contracts/satellite/reporting.yaml#getAnalyticsUsage)*

#### Outputs: what the screen shows and produces

**Shown**

**Active Analytics Users** (metric tile)

**Dashboard Views** (metric tile)

**Report Runs** (metric tile)

**AI Queries** (metric tile)

**Exports** (metric tile)

**API Requests** (metric tile)

**Peak Concurrent Users** (metric tile)

**Average Dashboard Load Time** (metric tile)

**Query Duration** (metric tile)

**Slowest Reports** (metric tile)

**Failed Queries** (metric tile)

**Dataset Size** (metric tile)

**Refresh Duration** (metric tile)

**Embedded BI Availability** (metric tile)

**Every analytics performance usage** (data table)

| Shows | Format | Notes |
|---|---|---|
| Most used dashboards | text | not in the schema: `Most Used Dashboards` |
| Least used dashboards | text | not in the schema: `Least Used Dashboards` |
| Most used reports | text | not in the schema: `Most Used Reports` |
| Unused reports | text | not in the schema: `Unused Reports` |
| Most queried KP is | text | not in the schema: `Most Queried KPIs` |
| Most active users/roles | text | not in the schema: `Most Active Users/Roles` |

**The selected analytics performance usage** (detail panel): The pack groups this record's detail under its own headings: “Where supported, monitor”, “Tenant Usage”.

| Shows | Format | Notes |
|---|---|---|
| Most used dashboards | text | not in the schema: `Most Used Dashboards` |
| Least used dashboards | text | not in the schema: `Least Used Dashboards` |
| Most used reports | text | not in the schema: `Most Used Reports` |
| Unused reports | text | not in the schema: `Unused Reports` |
| Most queried KP is | text | not in the schema: `Most Queried KPIs` |
| Most active users/roles | text | not in the schema: `Most Active Users/Roles` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **usage table**: Name, opens or runs, distinct users, last opened, average runtime, rows scanned, "Never opened" badge. Sort by opens; a "Never opened" filter for pruning. *(source: contracts/satellite/reporting.yaml#AnalyticsUsageRow)*
- **load**: "Load" column - dashboard refresh load (Low, Medium, High) and report estimated cost - never a currency amount. *(source: contracts/satellite/reporting.yaml#Dashboard / contracts/satellite/reporting.yaml#ReportDefinition)*

**Data it reads**: `getAnalyticsUsage` (onLoad, Usage, runtime and cost)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The analytics performance usage list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the analytics performance usage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No analytics performance usage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the analytics performance usage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Usage by user**: Shows people by name to tenant-level administrators only. *(source: contracts/satellite/reporting.yaml#getAnalyticsUsage)*

#### Consistency with other screens

- Match `ANL-021`: Usage counts in the dashboard library are these numbers.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- name: Operations Control Room
  kind: Dashboard
  opens: 1840
  users: 22
  lastOpened: 01 Oct 2026 10:41
  avgRuntime: 1.2 s
  load: High
- name: Shift summary
  kind: Report
  runs: 612
  users: 31
  avgRuntime: 0.9 s
  rowsScanned: 2.1 M
- name: Locker rentals by hour
  kind: Report
  runs: 0
  neverOpened: true
```

#### Permissions

- `getAnalyticsUsage` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-069` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-069`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 16: Works in Analytics Performance, Usage & Cost Monitor → Monitor BI adoption, system performance, capacity consumption and analytical operating costs.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-069?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-070` Analytics Governance, Security & Audit Center

**Provide final governance over the entire BI and analytics environment.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_AUDIT_VIEW`, `AUDIT_VIEW`, `REPORT_GOVERNANCE_MANAGE`, `REPORT_VIEW_TENANT` (2 read, 1 ?, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Monitor; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/analytics-governance-security-audit-center-anl-070` |

**What the spec says about it.** **Governance policy bound 2 October 2026 (CHG-SOT-009).** Chinmay, workbook Q225: "Add a governance policy operation (masking, export, retention, sharing, AI/API access)" (DEC-225). This screen edits the one policy per tenant; ANL-047 shows its sharing and export parts beside report access.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … Removed 2 October 2026 (CHG-WIR-001): listSecurityDetectionGovernance is access fraud analytics (BO-253); this screen governs BI and analytics, whose data is the platform audit trail and AI usage and … Contract gap recorded 2 October 2026 (CHG-WIR-004): No analytics governance read (report and dataset access, sharing, sensitivity). **Closed 2 October 2026:** getAnalyticsGovernancePolicy and …

**From the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process.** Final governance over the BI and analytics estate (BI board 10.10): who may see which dashboards, reports and datasets, KPI changes, exports, API and AI access, sensitive-data use, configuration and administrative actions; field classification (Public, Internal, Confidential, PII, Financial sensitive, Restricted); governance policies (masking, export restrictions, retention, sharing, AI and API access, approvals); the audit trail (who did what, when, to which object, from where, result); governance exceptions; and AI governance monitoring. The one thing to get right: it governs analytics, not gate security - the exceptions list (unauthorised export, cross-tenant access attempt, unapproved KPI change) leads.

**Known correction pending (do not draw the wrong version)**

- **The 17 table columns are the pack's monitored areas and AI monitoring labels** Why: They are tiles and categories, not columns of one table. *(source: screens/P16-venue-analytics.yaml#ANL-070; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*
- **Placed in process-module Admission & Access Control, and the purpose note is the pack's architecture heading ("Critical Data Architecture for the Complete Module")** Why: It is a BI board 10 screen (Analytics); the note is pack text that follows the screen. *(source: screens/P16-venue-analytics.yaml#ANL-070; Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue))*

**Fixed on main** (the package already carries these; draw what it says): Bound to listSecurityDetectionGovernance (access fraud analytics, BO-253) (CHG-WIR-001); The audit trail and AI governance parts have existing operations; the rest has none (CHG-WIR-001).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which operation will hold analytics governance policies (masking, export restriction, retention, sharing, AI and API access)?** → Add an analytics governance policy operation (masking, export restriction, retention, sharing, AI/API access). *(decided by Chinmay, 2026-10-02; DEC-225 / CHG-NOTE-008)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Masked fields | group | optional | — | — | — | `masking.maskedFields` as `schema.table.column`, picked from the semantic model's sensitive fields; `masking.unmaskedForPermissions` names who may see them unmasked. Masked before a value leaves the … | `AnalyticsGovernancePolicy.masking` |
| Export formats allowed | group | optional | — | — | — | `export.allowedFormats`; `export.personalDataNeedsPermission` (default on: an export carrying personal data needs `REPORT_EXPORT_PII`) and `export.maxRows` beside it. | `AnalyticsGovernancePolicy.export` |
| Keep report results and exports for (days) | group | optional | — | — | — | `retention.resultDays`; empty keeps them until the data-retention settings remove them (ANL-050). | `AnalyticsGovernancePolicy.retention` |
| Allow external share links | group | optional | — | — | — | `sharing.externalLinks` (default off) and `sharing.allowedDomains`, the only domains a link may be sent to. | `AnalyticsGovernancePolicy.sharing` |
| AI assistant may answer analytics questions | group | optional | — | — | — | `aiAndApiAccess.aiAssistant` (default on, through the semantic layer only) and `aiAndApiAccess.publicApi` (default off). | `AnalyticsGovernancePolicy.aiAndApiAccess` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Org unit | picker: choose an org unit | — | — | `listAuditRecords` ?orgUnitId |
| Principal | picker: choose a principal | — | — | `listAuditRecords` ?principalId |
| Workstation | picker: choose a workstation | — | — | `listAuditRecords` ?workstationId |
| Action | text field | — | — | `listAuditRecords` ?action |
| Subject ref | text field | — | — | `listAuditRecords` ?subjectRef |
| Platform staff grant | picker: choose a platform staff grant | — | — | `listAuditRecords` ?platformStaffGrantId |
| From | date and time picker | — | — | `listAuditRecords` ?from |
| To | date and time picker | — | — | `listAuditRecords` ?to |
| From | date picker | — | — | `getAiUsage` ?from |
| Group by | select | — | Tenant · Venue · Principal · Provider · Capability · Day · Agent · Model · Task | `getAiUsage` ?groupBy |

**Form: Save governance policy** (confirmDialog, opened by *Save governance policy*; *Save governance policy* calls `setAnalyticsGovernancePolicy`, *Cancel* sends nothing)

**Names what changes before it is saved**, section by section ("Exports of personal data will need REPORT_EXPORT_PII; external share links switched off"). The whole policy is replaced; the semantic layer applies it to every report, dashboard, export and natural-language answer at once. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Masking `masking` | group | optional | — | — | — | Masked fields, as `schema.table.column`, and who may see them unmasked. | `setAnalyticsGovernancePolicy` body |
| Masked fields `masking.maskedFields` | list of values (chips) | optional | — | — | — | — | `setAnalyticsGovernancePolicy` body |
| Unmasked for permissions `masking.unmaskedForPermissions` | list of values (chips) | optional | — | — | — | — | `setAnalyticsGovernancePolicy` body |
| Export `export` | group | optional | — | — | — | — | `setAnalyticsGovernancePolicy` body |
| Allowed formats `export.allowedFormats` | list of values (chips) | optional | — | — | — | — | `setAnalyticsGovernancePolicy` body |
| Personal data needs permission `export.personalDataNeedsPermission` | toggle | optional | on | An export carrying personal data needs `REPORT_EXPORT_PII`. | — | An export carrying personal data needs `REPORT_EXPORT_PII`. | `setAnalyticsGovernancePolicy` body |
| Max rows `export.maxRows` | number field | optional | — | — | — | — | `setAnalyticsGovernancePolicy` body |
| Retention `retention` | group | optional | — | — | — | — | `setAnalyticsGovernancePolicy` body |
| Result days `retention.resultDays` | number field (days) | optional | — | min 1 | — | How long report results and exports are kept. | `setAnalyticsGovernancePolicy` body |
| Sharing `sharing` | group | optional | — | — | — | — | `setAnalyticsGovernancePolicy` body |
| External links `sharing.externalLinks` | toggle | optional | off | — | — | — | `setAnalyticsGovernancePolicy` body |
| Allowed domains `sharing.allowedDomains` | list of values (chips) | optional | — | — | — | — | `setAnalyticsGovernancePolicy` body |
| AI and API access `aiAndApiAccess` | group | optional | — | — | — | — | `setAnalyticsGovernancePolicy` body |
| AI assistant `aiAndApiAccess.aiAssistant` | toggle | optional | on | — | — | The AI assistant may answer analytics questions through the semantic layer (ADR-0054). | `setAnalyticsGovernancePolicy` body |
| Public API `aiAndApiAccess.publicApi` | toggle | optional | off | — | — | — | `setAnalyticsGovernancePolicy` body |

Errors to draw in the form: 400 Validation failed

**Rules for these inputs** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Audit filters**: Who (user or role), action, object (dashboard, report, dataset, KPI, export, AI query), date range, result (allowed / blocked). *(source: screens/P16-venue-analytics.yaml#ANL-070 / contracts/spine/tenancy.yaml#listAuditRecords)*
- **Field classification**: Per semantic-model field, one of Public / Internal / Confidential / PII / Financial sensitive / Restricted (chips, not text). *(source: screens/P16-venue-analytics.yaml#ANL-070 / contracts/satellite/reporting.yaml#setSemanticModel)*
- **Governance policies**: Data masking, Export restrictions, Retention, Sharing, AI access, API access, Approval requirements - each a policy card with its current setting. *(source: screens/P16-venue-analytics.yaml#ANL-070)*

#### Outputs: what the screen shows and produces

**Shown**

**Every analytics governance security** (data table)

| Shows | Format | Notes |
|---|---|---|
| Dashboard permissions | text | not in the schema: `Dashboard Permissions` |
| Report permissions | text | not in the schema: `Report Permissions` |
| Dataset permissions | text | not in the schema: `Dataset Permissions` |
| KPI changes | text | not in the schema: `KPI Changes` |
| Data exports | text | not in the schema: `Data Exports` |
| API access | text | not in the schema: `API Access` |
| AI access | text | not in the schema: `AI Access` |
| Sensitive data usage | text | not in the schema: `Sensitive Data Usage` |
| Configuration changes | text | not in the schema: `Configuration Changes` |
| Administrative actions | text | not in the schema: `Administrative Actions` |
| AI queries | text | not in the schema: `AI Queries` |
| Blocked queries | text | not in the schema: `Blocked Queries` |
| Sensitive data requests | text | not in the schema: `Sensitive-Data Requests` |
| AI cost | text | not in the schema: `AI Cost` |
| Model errors | text | not in the schema: `Model Errors` |
| Low confidence answers | text | not in the schema: `Low-Confidence Answers` |
| User feedback | text | not in the schema: `User Feedback` |

**Audit trail** (data table, from `listAuditRecords`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Principal | the name it points at, never the id | Who acted. |
| Org unit | the name it points at, never the id | The scope node the action happened in. |
| Workstation | the name it points at, never the id | The workstation it was done from, where there was one. |
| Action | text | What was done, as the writing operation names it. |
| Subject ref | text | The thing acted on — a profile, a shift, an order. The same value the `subjectRef` filter matches. |
| Occurred at | 1 Oct 2026, 14:30 | When. The list is ordered by this, most recent first. |
| Platform staff grant | the name it points at, never the id | Set when a TICVAI platform operator acted, naming the grant they acted under (`identity.openPlatformStaffGrant`; decided 28 September … |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**AI usage** (detail panel, from `getAiUsage`)

| Shows | Format | Notes |
|---|---|---|
| Currency | text | The tenant's selected currency, USD by default (Chinmay, 2 October, workbook Q8; CHG-CSA-004). |
| Ceiling | grouped details | The spend ceiling in force (`getAiSpendCeiling`), with the tokens it equals at the current blended rate and what is used so far … |
| Spend | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tokens | 1,234 | — |
| Used spend | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Used tokens | 1,234 | — |
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | text | — |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Interactions | 1,234 | — |
| Prompt tokens | 1,234 | — |
| Completion tokens | 1,234 | — |
| Cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| P95 latency ms | 1,234 | — |
| Refusal rate | 12.5% | — |
| Rejection rate | 12.5% | Proposals a person refused. The number that says whether the assistant is worth having, and the one nobody thinks to measure. |
| Forecast | grouped details | A month-end projection, labelled a forecast (AI design 2.3, 4.5). Present where `to` is inside the current month. |
| Label | chip: Forecast | — |

**AI interactions** (data table, from `listAiInteractions`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Conversation | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Audience | chip: Staff, Guest | Billing divides on this. Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop … |
| Subject | the name it points at, never the id | The guest, where the audience is `guest`. `principalId` is null in that case — a guest is not a principal, and attributing their tokens to … |
| Billable to tenant | the name it points at, never the id | Resolved from `scopePath` at write time, not derived later. Billing must not depend on walking a scope tree that has since been reorganised. |
| Capability | text | — |
| Prompt | text | — |
| Response | text | — |
| Sources | list or chips (count when long) | The sources an answer was grounded in, stored with the answer (8.3.70). One `jsonb` column on the row that carries it — … |
| Kind | chip: Document, Product, Entitlement, Report, Record | — |
| ID | text | — |
| Title | text | — |
| Collection | the name it points at, never the id | — |
| Excerpt | text | — |
| Relevance | 1,234.5 | — |
| Outcome | chip: Answered, Refused, Applied, Rejected, Failed | — |
| Refusal reason | text | — |
| Provider | chip: Openai, Gemini, Anthropic, Azure openai, Local llm, Openai compatible | `openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development … |

**The policy in force** (detail panel, from `getAnalyticsGovernancePolicy`): A tenant that never set one reads the defaults: personal fields masked, personal-data exports need `REPORT_EXPORT_PII`, no external sharing, AI and API access through the semantic layer only. Shown as "Defaults" until saved.

| Shows | Format | Notes |
|---|---|---|
| Masking | grouped details | Masked fields, as `schema.table.column`, and who may see them unmasked. |
| Export | grouped details | — |
| Retention | grouped details | — |
| Sharing | grouped details | — |
| AI and API access | grouped details | — |
| Updated at | 1 Oct 2026, 14:30 | — |

**The selected analytics governance security** (detail panel): The pack groups this record's detail under its own headings: “The desired structure is”, “Unified Data Integration Layer”, “Analytics Data Platform”, “Instead”, “Board 10 Benchmarking”.

| Shows | Format | Notes |
|---|---|---|
| Dashboard permissions | text | not in the schema: `Dashboard Permissions` |
| Report permissions | text | not in the schema: `Report Permissions` |
| Dataset permissions | text | not in the schema: `Dataset Permissions` |
| KPI changes | text | not in the schema: `KPI Changes` |
| Data exports | text | not in the schema: `Data Exports` |
| API access | text | not in the schema: `API Access` |
| AI access | text | not in the schema: `AI Access` |
| Sensitive data usage | text | not in the schema: `Sensitive Data Usage` |
| Configuration changes | text | not in the schema: `Configuration Changes` |
| Administrative actions | text | not in the schema: `Administrative Actions` |
| AI queries | text | not in the schema: `AI Queries` |
| Blocked queries | text | not in the schema: `Blocked Queries` |
| Sensitive data requests | text | not in the schema: `Sensitive-Data Requests` |
| AI cost | text | not in the schema: `AI Cost` |
| Model errors | text | not in the schema: `Model Errors` |
| Low confidence answers | text | not in the schema: `Low-Confidence Answers` |
| User feedback | text | not in the schema: `User Feedback` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save governance policy (primary button) | `setAnalyticsGovernancePolicy` PUT `/analytics-governance-policy` | AnalyticsGovernancePolicy | AnalyticsGovernancePolicy | 400 Validation failed | gated `REPORT_GOVERNANCE_MANAGE`; opens confirmDialog first |

**Rules for what is shown** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Governance exceptions**: Top list, newest first, severity coloured - Unauthorised export attempt, Excessive data extraction, Failed permission check, Sensitive data accessed, AI request blocked, Cross-tenant access attempt, Unapproved KPI modification - each with who, what, when, from where. *(source: screens/P16-venue-analytics.yaml#ANL-070)*
- **Monitored areas**: Ten tiles (dashboard, report and dataset permissions changed, KPI changes, data exports, API access, AI access, sensitive data usage, configuration changes, administrative actions) with counts for the period (VO-R02). *(source: screens/P16-venue-analytics.yaml#ANL-070)*
- **AI governance monitoring**: AI queries, blocked queries, sensitive-data requests, AI cost (AED), model errors, low-confidence answers, user feedback - as tiles with a trend. *(source: screens/P16-venue-analytics.yaml#ANL-070 / contracts/satellite/ai.yaml#getAiUsage / contracts/satellite/ai.yaml#listAiInteractions)*
- **Audit trail**: Who, did what, when, to which object or data, from where, result - cursor paging; reading the trail is itself audited. *(source: screens/P16-venue-analytics.yaml#ANL-070 / contracts/spine/tenancy.yaml#listAuditRecords)*

**What each action does** (from the Venue Operations (admission and access, accreditation, resources and capacity, workforce, maintenance and safety, games and rides, virtual queue) process; these refine the tables above and win where they differ)

- **Open exception**: Shows the audit records around it and links to the object (report, dashboard, export). *(source: contracts/spine/tenancy.yaml#listAuditRecords)*
- **Edit policy / classification**: Edits a policy card through an analytics governance policy operation (masking, export restriction, retention, sharing, AI and API access), to be added; classification stays part of the semantic model write. *(source: contracts/satellite/reporting.yaml#setSemanticModel / decided 2 October 2026 by Chinmay (CHG-NOTE-008))*

**Data it reads**: `listAuditRecords` (onLoad, Changes to analytics objects: who did what, and when); `getAiUsage` (onLoad, AI usage, cost and performance in analytics); `getAnalyticsGovernancePolicy` (onLoad, The tenant's analytics governance policy: masking, export …)

**Where the user goes next**

- → `ANL-061` BI & Analytics Administration Command Center: *Back to BI & Analytics Administration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The analytics governance security list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the analytics governance security untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No analytics governance security yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the analytics governance security are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission: reading the audit trail and the governance policy needs `REPORT_VIEW_TENANT`, and changing the policy needs `REPORT_GOVERNANCE_MANAGE` (CHG-FUP-007); without it the policy shows read-only and says who can change it. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **Cross-tenant access attempt**: Always Critical, never dismissible without a note; shows the tenant names. *(source: screens/P16-venue-analytics.yaml#ANL-070)*
- **Platform staff acted in the tenant**: Rows carry "TICVAI platform staff under grant G-..." so the tenant sees every platform action. *(source: contracts/spine/tenancy.yaml#listAuditRecords)*

#### Consistency with other screens

- Match `ANL-061`: Board 10 hub; this screen returns to it.
- Match `ANL-060`: AI Analytics Governance & Model Control owns AI policy; this screen monitors it.
- Match `BO-253`: Security Analytics, AI Detection & Governance (access fraud analytics) is what is currently bound here by mistake; keep the two separate.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exceptions:
- severity: High
  what: Unauthorised export attempt
  who: Rahul Menon (Analyst)
  object: Guest PII - Annual pass holders
  when: 1 Oct 2026 10:42
  from: Office network
  result: Blocked
- severity: Critical
  what: Cross-tenant access attempt
  who: api-client B2B-17
  object: Dataset Sales (other tenant)
  result: Blocked
- severity: Medium
  what: Unapproved KPI modification
  who: Fatima Al Hashimi
  object: KPI NET_REVENUE draft
  result: Held for approval
ai:
  queries: 1840
  blocked: 23
  sensitiveRequests: 11
  cost: AED 412.60
  lowConfidence: 37
```

#### Permissions

- `listAuditRecords` → `AUDIT_VIEW` (read) · staff
- `getAiUsage` → `AI_AUDIT_VIEW` (read) · staff
- `listAiInteractions` → `AI_AUDIT_VIEW` (read) · staff
- `getAnalyticsGovernancePolicy` → `REPORT_VIEW_TENANT` (operate) · staff
- `setAnalyticsGovernancePolicy` → `REPORT_GOVERNANCE_MANAGE` (tier not set) · staff

**A refused user sees:** Names the missing permission: reading the audit trail and the governance policy needs `REPORT_VIEW_TENANT`, and changing the policy needs `REPORT_GOVERNANCE_MANAGE` (CHG-FUP-007); without it the policy shows read-only and says who can change it. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.7 | AI Usage Analytics System shall provide reporting on AI usage and outcomes. | Unified Operations Dashboard | CONTRACTED | `getAiUsage` |
| 8.4.27 | System shall support AI usage monitoring. | Unified Operations Dashboard | CONTRACTED | `getAiUsage` |
| 8.7.10 | System shall provide AI analytics dashboards. | Unified Operations Dashboard | CONTRACTED | `getAiUsage` |
| 8.1.2 | Prompt Logging System shall store prompts submitted to AI services. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |
| 8.1.3 | Response Logging System shall store AI-generated responses. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |
| 8.1.6 | AI Audit Trail System shall maintain a history of AI-generated actions and user decisions. | Unified Operations Dashboard | CONTRACTED | `listAiInteractions` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-070` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS177 Unified BI Reporting and AI Analytics Platform Board 10.dc.html#anl-070`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 10
- Flow F180 *Unified BI Reporting and AI Analytics Platform board 10: BI & Analytics …*, step 18: Works in Analytics Governance, Security & Audit Center → Provide final governance over the entire BI and analytics environment.
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (91 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-070?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save governance policy.
- [ ] Every transition is wired: `ANL-061`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AUDIT_VIEW`, `REPORT_GOVERNANCE_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P16 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P16 Venue Analytics

- One consolidated, permission-based reporting/dashboard area: a user opens "dashboards" once and sees all dashboards their access allows (finance sees finance; a CEO sees sales, admissions, access control), with dashboard settings there too - not duplicated dashboard screens inside each functional module. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-721)*
- Dashboards should refresh near-real-time (seconds) so management can monitor sales continuously rather than wait for periodic or end-of-day refreshes. *(agreed · MoM 8 Sep 2026, 4.6 Real-Time Reporting Architecture · DI-711)*
- Dashboards must be mobile-responsive so management (e.g. a CEO outside the venue) can log in from a smartphone via a URL rather than needing a laptop. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-696)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*

### In P16 · Analytics

- Finance board: revenue by department and cost centre, shift-closing details, and payment gateway reconciliation, shown as bar and pie charts. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-716)*

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createKpi": {"method":"POST","path":"/kpis","contract":"reporting","summary":"Define a KPI once, for everywhere","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"KpiDefinition","responds":"KpiDefinition"},
"getAiUsage": {"method":"GET","path":"/usage","contract":"ai","summary":"Usage, cost and performance","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"AiUsageReport"},
"getAnalyticsBenchmark": {"method":"GET","path":"/analytics-benchmarks","contract":"reporting","summary":"One site against another, on a like-for-like basis","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"kpiId","in":"query","required":true},{"name":"scopePaths","in":"query","required":null},{"name":"normaliseBy","in":"query","required":null}],"requestBody":null,"responds":"BenchmarkRow"},
"getAnalyticsGovernancePolicy": {"method":"GET","path":"/analytics-governance-policy","contract":"reporting","summary":"The tenant's analytics governance policy","permission":"REPORT_VIEW_TENANT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AnalyticsGovernancePolicy"},
"getAnalyticsUsage": {"method":"GET","path":"/analytics-usage","contract":"reporting","summary":"Which dashboards and reports are actually used, and what they cost","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"AnalyticsUsageRow"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getSemanticModel": {"method":"GET","path":"/semantic-model","contract":"reporting","summary":"The business data catalogue reports are built from","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SemanticModel"},
"listAiInteractions": {"method":"GET","path":"/interactions","contract":"ai","summary":"Every prompt, response and action","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"principalId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAnalyticsPipelines": {"method":"GET","path":"/analytics-pipelines","contract":"reporting","summary":"Data sources, refresh state and freshness","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AnalyticsPipeline"},
"listAuditRecords": {"method":"GET","path":"/audit-records","contract":"tenancy","summary":"Who did what, where, and when","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orgUnitId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"action","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"platformStaffGrantId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDashboards": {"method":"GET","path":"/dashboards","contract":"reporting","summary":"List dashboards","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":false},{"name":"includeArchived","in":"query","required":false}],"requestBody":null,"responds":"Dashboard"},
"listKpis": {"method":"GET","path":"/kpis","contract":"reporting","summary":"The enterprise KPI library","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"KpiDefinition"},
"listSiteNormalisationBases": {"method":"GET","path":"/site-normalisation-bases","contract":"reporting","summary":"The denominators each site is benchmarked by","permission":"REPORT_VIEW_TENANT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"periodFrom","in":"query","required":null},{"name":"periodTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setAnalyticsGovernancePolicy": {"method":"PUT","path":"/analytics-governance-policy","contract":"reporting","summary":"Set the analytics governance policy","permission":"REPORT_GOVERNANCE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AnalyticsGovernancePolicy","responds":"AnalyticsGovernancePolicy"},
"setKpiTargets": {"method":"PUT","path":"/kpis/{kpiId}/targets","contract":"reporting","summary":"Targets, thresholds and what red means","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KpiTarget"},
"setSemanticModel": {"method":"PUT","path":"/semantic-model","contract":"reporting","summary":"Publish the catalogue","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SemanticModel","responds":"SemanticModel"},
"setSiteNormalisationBasis": {"method":"PUT","path":"/site-normalisation-bases","contract":"reporting","summary":"Set the denominators a site is benchmarked by","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SiteNormalisationBasis"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Aggregation": {"type":"string","enum":["none","count","countDistinct","sum","average","min","max"]},
"AiInteraction": {"type":"object","x-ticvai-persistence":"ai.activity","required":["id","principalId","capability","outcome","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid","nullable":true},"principalId":{"type":"string","format":"uuid"},"audience":{"type":"string","enum":["staff","guest"],"description":"**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"},"billableToTenantId":{"type":"string","format":"uuid","description":"Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"},"scopePath":{"type":"string"},"capability":{"type":"string"},"prompt":{"type":"string"},"response":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"outcome":{"type":"string","enum":["answered","refused","applied","rejected","failed"]},"refusalReason":{"type":"string","nullable":true},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"x-ticvai-column":"cost_amount","description":"What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"},"latencyMs":{"type":"integer"},"maskedFieldCount":{"type":"integer","description":"How many fields were redacted. Zero on a prompt touching guest data is a defect."},"traceId":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."},"cacheLayer":{"type":"string","nullable":true,"enum":["guardrail","semantic","exact","negative","analytics"],"description":"Which cache answered, where one did (AI design 3.6). Null for a model call."},"createdAt":{"type":"string","format":"date-time"}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n**Core42 Compass is reached through `openaiCompatible`** (Chinmay, 2 October: the AI residency decision, amending AI-D02; CHG-CSA-002). Compass is the provider of the `uaeOnly` residency class (common `AiResidencyClass`): Small tier Compass GPT-4.1 mini (or Seraj), Strong tier Compass GPT-5, with OpenAI UAE and then the in-cell open-weights model as the fallback chain. OpenAI UAE is `openai` with a UAE `endpoint`; the in-cell model is `localLlm`.\n**A kind is a protocol, not a vendor** (Chinmay, 2 October, contract follow-ups: BYOK accepts any provider; CHG-FUP-008). Any vendor is accepted, named in `AiProvider.vendor`: Mistral, Cohere or any other is reached through `openaiCompatible` where its API speaks it, which the compatibility test confirms before activation (`AiProviderCompatibility`). A new native adapter is a new value here, a breaking change for a client built earlier that goes out with an approval (`docs/active/breaking-changes.yaml`); until then a vendor without either protocol is refused `422 provider-protocol-unsupported`.\n"},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AiUsageReport": {"type":"object","x-ticvai-persistence":"none — aggregated from ai.activity","properties":{"currency":{"type":"string","minLength":3,"maxLength":3,"readOnly":true,"description":"**The tenant's selected currency, USD by default** (Chinmay, 2 October, workbook Q8; CHG-CSA-004). Every `cost` here is in it; token counts sit beside each cost."},"ceiling":{"type":"object","nullable":true,"readOnly":true,"description":"The spend ceiling in force (`getAiSpendCeiling`), with the tokens it equals at the current blended rate and what is used so far (CHG-CSA-004).","properties":{"spend":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tokens":{"type":"integer","nullable":true},"usedSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"usedTokens":{"type":"integer"}}},"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"groupBy":{"type":"string"},"rows":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"interactions":{"type":"integer"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"p95LatencyMs":{"type":"integer"},"refusalRate":{"type":"number"},"rejectionRate":{"type":"number","description":"Proposals a person refused. **The number that says whether the assistant is worth having**, and the one nobody thinks to measure.\n"}}}},"forecast":{"type":"object","nullable":true,"description":"**A month-end projection, labelled a forecast** (AI design 2.3, 4.5). Present where `to` is inside the current month. Never added into `rows`.\n","properties":{"label":{"type":"string","enum":["forecast"]},"periodEnd":{"type":"string","format":"date"},"projectedTokens":{"type":"integer"},"projectedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"basis":{"type":"string","description":"How it was projected, e.g. the run rate of the last 7 days."}}}}},
"AnalyticsGovernancePolicy": {"type":"object","x-ticvai-persistence":"reporting.analytics_governance_policy","description":"**What analytics may show and where it may go** (Chinmay, 2 October, workbook Q225; CHG-CSA-021). One row per tenant.","properties":{"masking":{"type":"object","description":"Masked fields, as `schema.table.column`, and who may see them unmasked.","properties":{"maskedFields":{"type":"array","items":{"type":"string"}},"unmaskedForPermissions":{"type":"array","items":{"type":"string"}}}},"export":{"type":"object","properties":{"allowedFormats":{"type":"array","items":{"type":"string"}},"personalDataNeedsPermission":{"type":"boolean","default":true,"description":"An export carrying personal data needs `REPORT_EXPORT_PII`."},"maxRows":{"type":"integer","nullable":true}}},"retention":{"type":"object","properties":{"resultDays":{"type":"integer","minimum":1,"nullable":true,"description":"How long report results and exports are kept."}}},"sharing":{"type":"object","properties":{"externalLinks":{"type":"boolean","default":false},"allowedDomains":{"type":"array","items":{"type":"string"}}}},"aiAndApiAccess":{"type":"object","properties":{"aiAssistant":{"type":"boolean","default":true,"description":"The AI assistant may answer analytics questions through the semantic layer (ADR-0054)."},"publicApi":{"type":"boolean","default":false}}},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `tenant` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AnalyticsPipeline": {"type":"object","x-ticvai-persistence":"reporting.pipeline","description":"BI board 10.7. **Freshness decides whether a dashboard can be trusted.**","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"sourceKind":{"type":"string"},"datasets":{"type":"array","items":{"type":"string"}},"schedule":{"type":"string","nullable":true},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastSuccessAt":{"type":"string","format":"date-time","nullable":true},"freshnessMinutes":{"type":"integer","nullable":true},"expectedFreshnessMinutes":{"type":"integer","nullable":true},"status":{"type":"string","enum":["healthy","degraded","stale","failed","paused"]},"lastError":{"type":"string","nullable":true},"rowsLastRun":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"AnalyticsUsageRow": {"type":"object","description":"BI board 10.9. **The number that lets a BI estate be pruned.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"opens":{"type":"integer"},"distinctUsers":{"type":"integer"},"lastOpenedAt":{"type":"string","format":"date-time","nullable":true},"averageRuntimeMs":{"type":"integer","nullable":true},"rowsScanned":{"type":"integer","nullable":true},"neverOpened":{"type":"boolean"}}},
"AuditRecord": {"x-ticvai-append-only":"occurredAt","type":"object","x-ticvai-persistence":"platform.audit_record","description":"26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n","required":["id","action","occurredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid","description":"Who acted."},"orgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The scope node the action happened in."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation it was done from, where there was one."},"action":{"type":"string","description":"What was done, as the writing operation names it."},"subjectRef":{"type":"string","nullable":true,"description":"**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"},"occurredAt":{"type":"string","format":"date-time","description":"When. The list is ordered by this, most recent first."},"platformStaffGrantId":{"type":"string","format":"uuid","nullable":true,"description":"**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"}}},
"BenchmarkNormalisation": {"type":"string","description":"The basis a benchmark is compared on. Shared by `getAnalyticsBenchmark` and `BenchmarkRow`.","enum":["none","perVisitor","perOperatingHour","perStaffedPosition","perSquareMetre"]},
"BenchmarkRow": {"type":"object","description":"BI board 10.4. **The normalisation travels with the comparison.**","properties":{"scopePath":{"type":"string"},"label":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"normalisedValue":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"normaliseBy":{"$ref":"#/components/schemas/BenchmarkNormalisation"},"rank":{"type":"integer"},"percentile":{"type":"number","nullable":true}}},
"CreateDashboardRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","module","tiles"],"properties":{"name":{"type":"string","maxLength":200},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey","description":"**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid","description":"Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"},"isShared":{"type":"boolean","default":false},"tiles":{"type":"array","minItems":1,"maxItems":24,"items":{"$ref":"#/components/schemas/DashboardTile"}}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"KpiDefinition": {"type":"object","x-ticvai-persistence":"reporting.kpi_definition","description":"BI boards 2.5 and 10.2. **One definition, referenced everywhere** — otherwise *revenue* means two things in the same meeting.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","description":"`takings` and `admissions` are seeded for every tenant as system KPIs (decided 28 September, audit R283), and the five accreditation KPIs for every tenant with the accreditation module (29 September, build pass). The seeded codes are `ReportingSystemKpi`.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"domain":{"type":"string","nullable":true},"formula":{"type":"string","description":"**Expressed against the semantic model, not against tables.** A KPI written in SQL is a KPI that breaks when the warehouse is reshaped.\n"},"unit":{"type":"string","enum":["currency","count","percentage","duration","ratio","score"]},"higherIsBetter":{"type":"boolean","default":true,"description":"**Refund rate and revenue both go up.** Without this the status colour is a coin toss.\n"},"defaultPeriod":{"type":"string","nullable":true},"owner":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"KpiTarget": {"type":"object","x-ticvai-persistence":"reporting.kpi_target","description":"BI board 2.6. **The threshold is what turns a number into a status.**","required":["scopePath","period","target"],"properties":{"kpiId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"The scope this target applies to. With `period`, the key `setKpiTargets` matches on."},"period":{"type":"string"},"target":{"$ref":"#/components/schemas/MetricValue"},"amberAt":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"redAt":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"stretch":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SemanticModel": {"type":"object","x-ticvai-persistence":"reporting.semantic_model","description":"BI boards 3.3 and 10.6. **A vocabulary, not a schema.** Exposing joins to report authors produces reports that are wrong invisibly.\n","properties":{"version":{"type":"integer","readOnly":true,"description":"Assigned by the server on each publish."},"domains":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"datasets":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"grain":{"type":"string","description":"**What one row means.** The single most common cause of a wrong report is a join that silently multiplied the grain.\n"},"fields":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"dataType":{"$ref":"#/components/schemas/FieldType"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"nullable":true,"description":"The default aggregation for the field, where it has one."},"sensitive":{"type":"boolean","default":false},"description":{"type":"string","nullable":true}}}}}}}}}},"relationships":{"type":"array","items":{"type":"object","properties":{"fromDataset":{"type":"string"},"toDataset":{"type":"string"},"cardinality":{"type":"string","enum":["oneToOne","oneToMany","manyToOne","manyToMany"]}}}},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}},
"SiteNormalisationBasis": {"type":"object","x-ticvai-persistence":"reporting.site_normalisation_basis","description":"BI boards 7.9 and 10.4. **The denominators a benchmark divides by**, per site and period: visitors, operating hours, staffed positions and area, one for each `BenchmarkNormalisation` other than `none`. Read by `getAnalyticsBenchmark` for the period that covers the benchmark (data model, 29 September).\n","required":["scopePath","periodStart","periodEnd"],"properties":{"id":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"The site (venue scope) the basis applies to."},"periodStart":{"type":"string","format":"date"},"periodEnd":{"type":"string","format":"date"},"visitors":{"type":"integer","nullable":true,"minimum":0,"description":"`perVisitor`."},"operatingHours":{"type":"number","nullable":true,"minimum":0,"description":"`perOperatingHour`."},"staffedPositions":{"type":"number","nullable":true,"minimum":0,"description":"`perStaffedPosition`. Average positions staffed over the period."},"areaSquareMetres":{"type":"number","nullable":true,"minimum":0,"description":"`perSquareMetre`. Operated area."}}}
}
```
