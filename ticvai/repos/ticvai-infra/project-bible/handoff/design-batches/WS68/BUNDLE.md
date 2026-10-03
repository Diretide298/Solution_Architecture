# WS68 — Unified BI Reporting and AI Analytics Platform board 3

**10 screens · 10 operations · 18 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `REPORT_MANAGE, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `ANL-031` | Report Catalogue & Library | D | 0 | 26 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-032` | Report Creation Wizard | D | 9 | 0 | 5 | 82 | 1 | 0 | — | notStarted (—) |
| `ANL-033` | Data Domain & Dataset Selector | D | 0 | 16 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-034` | Field & Column Selector | D | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `ANL-035` | Filter & Parameter Builder | D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-036` | Grouping, Aggregation & Calculation Builder | D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-037` | Cross-Domain Report Composer | D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-038` | Report Layout & Formatting Designer | D | 7 | 0 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-039` | Report Preview, Test & Validation | D | 0 | 16 | 6 | 5 | 0 | 0 | — | notStarted (—) |
| `ANL-040` | Save, Run & Report Results Viewer | D | 0 | 4 | 6 | 5 | 2 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-031, ANL-033, ANL-035, ANL-036, ANL-037, ANL-039 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-031` Report Catalogue & Library

**Provide a centralized repository containing all TICVAI standard, custom, scheduled and AI-generated reports.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-031 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each report shall display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/report-catalogue-library-anl-031` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The report library: the eight standard reports every venue starts with, plus the venue's own. It lists only reports the login may run; a report needing tenant-level access is absent for a venue user, not shown empty. The thing to get right: standard reports are copy-only (Make a copy, never Edit or Delete), and "scheduled" or "AI-generated" are properties of a report, not report types.

**Known correction pending (do not draw the wrong version)**

- **The gap says listReports returns no described schema** Why: It returns paged ReportDefinition (name, description, category, dataSource, version, isSystem, isRetired, lastRunAt, createdAt, requiredPermission); most columns can bind. *(source: contracts/satellite/reporting.yaml#listReports / screens/P16-venue-analytics.yaml#ANL-031; Finance, Ledger & Tax · Reporting & Analytics)*
- **Report Type values Standard, Custom, Scheduled, AI-generated** Why: Standard/Custom is isSystem; Scheduled is whether a schedule exists; AI-generated (saved from a natural-language answer) is not recorded on the definition. *(source: contracts/satellite/reporting.yaml#ReportDefinition / contracts/satellite/reporting.yaml#saveNaturalLanguageQuery; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | select | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | `listReports` ?category |
| Search | text field | — | — | `listReports` ?search |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **category (shown as "Category" chips)**: Sales, Admissions, Financial, Inventory, Guests, Operations, Marketing, Workforce, Compliance, Custom. *(source: contracts/satellite/reporting.yaml#ReportCategory / contracts/satellite/reporting.yaml#listReports)*
- **search**: Server-side search on the paged list; cursor paging, never page numbers. *(source: contracts/satellite/reporting.yaml#listReports)*

#### Outputs: what the screen shows and produces

**Shown**

**Every report catalogue** (data table)

| Shows | Format | Notes |
|---|---|---|
| Report name | text | not in the schema: `Report Name` |
| Report ID | text | not in the schema: `Report ID` |
| Description | text | not in the schema: `Description` |
| Category | text | not in the schema: `Category` |
| Business domain | text | not in the schema: `Business Domain` |
| Owner | text | not in the schema: `Owner` |
| Report type | text | not in the schema: `Report Type` |
| Site scope | text | not in the schema: `Site Scope` |
| Created date | text | not in the schema: `Created Date` |
| Last run | text | not in the schema: `Last Run` |
| Last modified | text | not in the schema: `Last Modified` |
| Status | text | not in the schema: `Status` |
| Usage count | text | not in the schema: `Usage Count` |

**The selected report catalogue** (detail panel): The pack groups this record's detail under its own headings: “Report Categories”, “Report Types”.

| Shows | Format | Notes |
|---|---|---|
| Report name | text | not in the schema: `Report Name` |
| Report ID | text | not in the schema: `Report ID` |
| Description | text | not in the schema: `Description` |
| Category | text | not in the schema: `Category` |
| Business domain | text | not in the schema: `Business Domain` |
| Owner | text | not in the schema: `Owner` |
| Report type | text | not in the schema: `Report Type` |
| Site scope | text | not in the schema: `Site Scope` |
| Created date | text | not in the schema: `Created Date` |
| Last run | text | not in the schema: `Last Run` |
| Last modified | text | not in the schema: `Last Modified` |
| Status | text | not in the schema: `Status` |
| Usage count | text | not in the schema: `Usage Count` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **row**: Name, category, data area, Standard or Custom badge, who can run it (in words: "Venue reports" / "Region reports" / "All venues"), last run, current version, Retired badge. Standard reports first, then custom by last run. Report ID is not shown. *(source: contracts/satellite/reporting.yaml#ReportDefinition / R096)*
- **standard reports**: The eight seeded reports with their one-line rationale: Terminal day view, Sales by channel, Attendance and footfall, Shift summary, Refunds, Voids and discounts, Stock valuation, F&B sales. A water park does not get a theatre's report: seeded reports apply to venue kinds. *(source: contracts/satellite/reporting.yaml#listSeededReports / contracts/satellite/reporting.yaml#SeededReport / R282)*
- **usage count**: From tenant-level usage; show to tenant-level users only. *(source: contracts/satellite/reporting.yaml#getAnalyticsUsage)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Run**: Opens ANL-040 for the report. *(source: contracts/satellite/reporting.yaml#runReport)*
- **Make a copy (standard reports)**: Creates a custom copy the venue can change; the standard report stays the shared reference. *(source: contracts/satellite/reporting.yaml#listSeededReports / R096)*
- **Retire**: Refused while an active schedule uses the report ("Pause or delete its 2 schedules first"). A report with past runs is retired, not removed, so its history still resolves; confirmation says which will happen. *(source: contracts/satellite/reporting.yaml#deleteReport)*

**Data it reads**: `listReports` (onLoad, The catalogue); `listSeededReports` (onLoad, What ships with the platform)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*
- → `ANL-040` Save, Run & Report Results Viewer: *Save, Run & Report Results Viewer*
- → `ANL-032` Report Creation Wizard: *Report Creation Wizard*
- → `ANL-033` Data Domain & Dataset Selector: *Data Domain & Dataset Selector*
- → `ANL-034` Field & Column Selector: *Field & Column Selector*
- → `ANL-035` Filter & Parameter Builder: *Filter & Parameter Builder*
- → `ANL-036` Grouping, Aggregation & Calculation Builder: *Grouping, Aggregation & Calculation Builder*
- → `ANL-037` Cross-Domain Report Composer: *Cross-Domain Report Composer*
- → `ANL-038` Report Layout & Formatting Designer: *Report Layout & Formatting Designer*
- → `ANL-039` Report Preview, Test & Validation: *Report Preview, Test & Validation*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report catalogue list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report catalogue untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report catalogue yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the report catalogue are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Venue user and a tenant-level report**: Absent from the list, not shown with a lock. *(source: contracts/satellite/reporting.yaml#listReports)*
- **Edit or Retire on a standard report**: Not offered; the server refuses both. *(source: contracts/satellite/reporting.yaml#updateReport / R096)*

#### Consistency with other screens

- Match `ANL-032`: New report starts the wizard; Make a copy opens the copy in the same builder steps.
- Match `ANL-021`: Same Standard/Custom badges and list layout as the dashboard library.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- name: Shift summary
  category: Financial
  area: Shifts
  type: Standard
  runBy: Venue reports
  lastRun: 01 Oct 2026 07:00
  version: '3'
- name: Sales by channel
  category: Sales
  area: Orders
  type: Standard
  runBy: Venue reports
  lastRun: 01 Oct 2026 08:15
- name: Foreign-currency collections by cashier
  category: Financial
  area: Payments
  type: Custom
  owner: Fatima Al Mansoori
  runBy: Venue reports
  lastRun: 30 Sep 2026 23:05
  version: '2'
- name: Locker rentals by hour (retired)
  category: Operations
  type: Custom
  status: Retired
```

#### Permissions

- `listReports` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listSeededReports` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Report builder provides a library of standard operations/finance reports exportable as PDF or Excel, plus custom reports built drag-and-drop (no SQL) by choosing which data-set fields appear as columns/rows. *(client request · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-708)*
- Report library filterable by site, operating area, sales channel, workstation or user; e.g. Sales Report (payment-method breakdown, totals, voids, deposits, itemised ticket sales) and Payment Summary (per-cashier breakdown). *(agreed · MoM 7 Aug 2026, 21. Dashboards & Reporting · DI-183)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-031` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-031`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 3
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 1: Opens Report Catalogue & Library → Provide a centralized repository containing all TICVAI standard, custom, scheduled and AI-generated reports.
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F177 branch at step 1 (expected): when Nothing has been set up on Report Catalogue & Library yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F177 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-031?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-040`, `ANL-032`, `ANL-033`, `ANL-034`, `ANL-035`, `ANL-036`, `ANL-037`, `ANL-038`, `ANL-039`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-032` Report Creation Wizard

**Guide users through creation of a new report without requiring technical knowledge. Step 1 — Report Information**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-032 |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Select one or multiple domains) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/report-creation-wizard-anl-032` |

**Known gaps.** **Report Creation Wizard declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Starts a report: Basics, Data area, Type, then the builder steps (fields, filters, grouping, layout, preview). A report can only be created once it has a data area, at least one column and the access level needed to run it, so the wizard keeps everything on the client until the first save. The thing to get right is the access level: an author can only give a report an access level they hold.

**Known correction pending (do not draw the wrong version)**

- **The gap says the wizard declares no write operation** Why: It declares createReport; the gap text is stale. *(source: screens/P16-venue-analytics.yaml#ANL-032; Finance, Ledger & Tax · Reporting & Analytics)*
- **Labels "Inventory - Resources - Marketing" and "Step 2 - Business Domain" drawn as text fields** Why: A fragment of the pack's domain list and a step heading; the step is one data-area choice. *(source: screens/P16-venue-analytics.yaml#ANL-032; Finance, Ledger & Tax · Reporting & Analytics)*
- **No draft state for a report** Why: A definition exists only once it has columns, and every later save publishes a version, so the builder's "save draft" has nowhere to go. *(source: contracts/satellite/reporting.yaml#CreateReportRequest / contracts/satellite/reporting.yaml#updateReport / MATRIX 7.4.45 / MATRIX 11.1.2; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Report Name | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Tags | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Step 2 — Business Domain | text field | — | — | — | — | — | — |
| Inventory • Resources • Marketing | text field | — | — | — | — | — | — |
| Step 3 — Report Type | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **name, description**: Name required, up to 200 characters; description up to 1,000. *(source: contracts/satellite/reporting.yaml#CreateReportRequest)*
- **category (shown as "Type")**: One of the ten categories. The pack's step 3 "Report type" is this field. *(source: contracts/satellite/reporting.yaml#ReportCategory)*
- **dataSource (shown as "Data area")**: One area per report (Orders, Order lines, Payments, Refunds, Shifts, Admissions scans ...). Areas that name a person (guests, staff, loyalty, reviews, accreditation) carry a "Personal data" badge. *(source: contracts/satellite/reporting.yaml#DataSource)*
- **requiredPermission (shown as "Who can run it")**: Choices in words, only those the author holds - "Anyone with venue reports", "Region reports", "All venues". Choosing a level not held is refused. *(source: contracts/satellite/reporting.yaml#CreateReportRequest / contracts/satellite/reporting.yaml#createReport)*
- **maxDateRangeDays (shown as "Longest date range")**: Default 366 days; guards against a query over years of scan events. *(source: contracts/satellite/reporting.yaml#CreateReportRequest / R158)*
- **Owner, Tags, Language (pack fields)**: The creator is recorded automatically; tags and language have no field. Show owner read-only, omit the other two. *(source: contracts/satellite/reporting.yaml#ReportDefinition)*

#### Outputs: what the screen shows and produces

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save**: Creates version 1 and returns to the builder; an unknown field or an estimated cost beyond the limit is refused with the field named. *(source: contracts/satellite/reporting.yaml#createReport)*

**Where the user goes next**

- → `ANL-031` Report Catalogue & Library: *Back to Report Catalogue & Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report creation wizard configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report creation wizard untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report creation wizard configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown field, invalid filter, or estimated cost beyond the limit |

#### Edge cases to draw

- **User leaves the wizard before choosing a column**: Nothing can be saved (a report needs at least one column); warn "Your report has not been saved yet". *(source: contracts/satellite/reporting.yaml#CreateReportRequest)*

#### Consistency with other screens

- Match `ANL-022`: Same step pattern and wording.
- Match `ANL-054`: The AI report generator creates through the same operation; its draft lands in these steps for review.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
basics:
  name: Daily closing - Aquaventure
  type: Financial
  dataArea: Payments
  whoCanRun: Anyone with venue reports
  longestRange: 31 days
```

#### Permissions

- `createReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

82 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.40 | System shall provide analytics and dashboards covering ticket sales, attendance, utilization, conversion rates, capacity utilization and revenue performance. | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.104 | Membership analytics | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.135 | Required Reports Operational Reports Donations by Campaign. Donations by Site. Donations by Product. Donations by Sales Channel. Donations by Date. Donations by User/Cashier. Donations by Payment … | Ticketing Catalogue | CONTRACTED | `createReport` |
| 3.2.65 | An Entry or Exit report is expected presenting the readings per outcome (ok/ko), per time and per access point. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.66 | The in park report showing the difference between the Entries and the Exits. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.68 | The length of stay report shall present the difference between the time in scan and the time out scan. | Admission and Access | CONTRACTED | `createReport` |
| 3.5.12 | System shall provide analytics showing bundle sales volume, revenue contribution, conversion rate, redemption rate, average order value impact, profitability, and performance by channel. | Admission and Access | CONTRACTED | `createReport` |
| 3.7.11 | System shall provide reporting on upsell impressions, conversion rates, revenue generated, average order value uplift, and campaign effectiveness across channels. | Admission and Access | CONTRACTED | `createReport` |
| 5.6.28 | Provide reporting on wait times, abandonment rates, no-shows, throughput, utilization, and satisfaction. | F&B & Guest Management | CONTRACTED | `createReport` |
| 6.1.5 | The system should be able to Generate reports with admission types/information. | Retail POS | CONTRACTED | `createReport` |
| 6.1.8 | The system should have the ability to retrieve information "on the fly" for items, (e.g., keyword, item #, description, category etc.) in user-friendly format such as pull-down menus and/or auto fill … | Retail POS | CONTRACTED | `createReport` |
| 6.1.9 | The system should be able to report historical sales look up by item, ticket number etc.. | Retail POS | CONTRACTED | `createReport` |
| … 70 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Report builder provides a library of standard operations/finance reports exportable as PDF or Excel, plus custom reports built drag-and-drop (no SQL) by choosing which data-set fields appear as columns/rows. *(client request · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-708)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-032` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-032`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 3
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 2: Works in Report Creation Wizard → Guide users through creation of a new report without requiring technical knowledge. Step 1 — Report Information

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-032?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-031`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-033` Data Domain & Dataset Selector

**Allow users to select approved TICVAI data sources for reporting.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-033 |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/data-domain-dataset-selector-anl-033` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Picks the governed data a report is built from, in business words, with no database access. The catalogue shows each dataset's meaning, its grain (what one row is) and whether it holds personal data. The thing to get right: show grain prominently, because a report over the wrong grain is wrong in ways nobody can see; and only certified, published datasets are offered.

**Known correction pending (do not draw the wrong version)**

- **Two vocabularies for "what a report reads"** Why: The catalogue lists semantic-model datasets (codes), but a report stores one value of the DataSource list and fields are fetched per DataSource; nothing maps one to the other, so a dataset picked here cannot be saved on the report. *(source: contracts/satellite/reporting.yaml#SemanticModel / contracts/satellite/reporting.yaml#DataSource / contracts/satellite/reporting.yaml#listReportFields; Finance, Ledger & Tax · Reporting & Analytics)*
- **getSemanticModel requires tenant-level access while report authoring is venue-level** Why: A venue report author cannot load this screen. *(source: contracts/satellite/reporting.yaml#getSemanticModel / contracts/satellite/reporting.yaml#createReport; Finance, Ledger & Tax · Reporting & Analytics)*
- **Data Owner, Security Classification and certification are not in the model** Why: The client wants certified badges with owner and lineage; the model has a sensitive flag per field only. *(source: contracts/satellite/reporting.yaml#SemanticModel / MATRIX 8.7.11 / MATRIX 6.1.78; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the report's data area the semantic-model dataset or the DataSource list, and who maps them?** → Drawn default accepted: Draw datasets from the catalogue; show the data area name on the report. *(decided by Chinmay, 2026-10-02; DEC-337 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every data domain dataset** (data table)

| Shows | Format | Notes |
|---|---|---|
| Dataset name | text | not in the schema: `Dataset Name` |
| Description | text | not in the schema: `Description` |
| Domain | text | not in the schema: `Domain` |
| Available date range | text | not in the schema: `Available Date Range` |
| Refresh frequency | text | not in the schema: `Refresh Frequency` |
| Last refresh | text | not in the schema: `Last Refresh` |
| Data owner | text | not in the schema: `Data Owner` |
| Security classification | text | not in the schema: `Security Classification` |

**The selected data domain dataset** (detail panel): The pack groups this record's detail under its own headings: “Ticketing”, “Sales”, “Finance”, “Payments”, “Access”, “Customer”.

| Shows | Format | Notes |
|---|---|---|
| Dataset name | text | not in the schema: `Dataset Name` |
| Description | text | not in the schema: `Description` |
| Domain | text | not in the schema: `Domain` |
| Available date range | text | not in the schema: `Available Date Range` |
| Refresh frequency | text | not in the schema: `Refresh Frequency` |
| Last refresh | text | not in the schema: `Last Refresh` |
| Data owner | text | not in the schema: `Data Owner` |
| Security classification | text | not in the schema: `Security Classification` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **domain groups**: Ticketing, Sales, Finance, Payments, Access, Customer and the other domains of the published model; each with its datasets. *(source: contracts/satellite/reporting.yaml#SemanticModel / screens/P16-venue-analytics.yaml#ANL-033)*
- **dataset card**: Name, description, "One row = one order line" (grain), field count, "Contains personal data" when any field is sensitive, last refreshed and expected freshness from the pipeline that feeds it ("Updated 6 min ago - expected every 15 min"). *(source: contracts/satellite/reporting.yaml#SemanticModel / contracts/satellite/reporting.yaml#AnalyticsPipeline)*
- **available history**: State the history in words ("From 1 Jan 2024"); financial records are kept at least 7 years, and archived periods are still reachable by reports. *(source: ADR-0047 / DI-018 / MATRIX 6.1.43)*

**Data it reads**: `getSemanticModel` (onLoad, Domains and datasets)

**Where the user goes next**

- → `ANL-031` Report Catalogue & Library: *Back to Report Catalogue & Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data domain dataset list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data domain dataset untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data domain dataset yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data domain dataset are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Dataset whose pipeline is stale or failed**: Still selectable, with a "Data delayed" warning; never hidden. *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline)*
- **Forecast points**: Only published forecast versions are reachable; the card says "Published forecasts only". *(source: contracts/satellite/reporting.yaml#DataSource)*

#### Consistency with other screens

- Match `ANL-066`: Dataset names, descriptions and grain are the lead's catalogue, word for word.
- Match `ANL-024`: The canvas data pane lists the same datasets.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
datasets:
- domain: Sales
  name: Order lines
  grain: One row = one line on an order
  personalData: false
  refreshed: Updated 3 min ago
  history: From 1 Jan 2024
- domain: Access
  name: Admission scans
  grain: One row = one scan at a gate
  personalData: false
  refreshed: Updated 40 sec ago
- domain: Customer
  name: Guests
  grain: One row = one guest profile
  personalData: true
  refreshed: Updated 12 min ago
```

#### Permissions

- `getSemanticModel` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-033` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-033`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 3
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 4: Works in Data Domain & Dataset Selector → Allow users to select approved TICVAI data sources for reporting.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-033?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-031`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-034` Field & Column Selector

**Allow users to visually select which information appears in the report.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-034 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/field-column-selector-anl-034` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Reorder columns, Rename display labels, Set width, Configure formatting. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Chooses the report's columns from the data area's fields, in business names, and sets each column's label, order, sort and format. The thing to get right: what a field allows (group by, total, filter) decides what the user can do with it, and personal-data fields are marked because exporting them needs separate permission.

**Known correction pending (do not draw the wrong version)**

- **Four pack actions drawn as buttons with no operation (reorder, rename, set width, configure formatting)** Why: Reorder, rename and format are edits to the report columns saved with the report; they are not separate operations. Column width has no field. *(source: screens/P16-venue-analytics.yaml#ANL-034 / contracts/satellite/reporting.yaml#ReportColumn; Finance, Ledger & Tax · Reporting & Analytics)*
- **The screen has no content region** Why: listReportFields gives a full field list to draw (type, groupable, aggregatable, filterable, personal data, required permission). *(source: contracts/satellite/reporting.yaml#listReportFields; Finance, Ledger & Tax · Reporting & Analytics)*
- **ReportColumn.format is an unspecified string** Why: The format grammar (percent, decimals, date pattern) is not defined, so the builder cannot offer valid choices. *(source: contracts/satellite/reporting.yaml#ReportColumn; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Data source | select | — | Orders · Order lines · Payments · Refunds · Shifts · Scan events · Entitlements · Products · Inventory · Stock movements · Stock counts · Waste … | `listReportFields` ?dataSource |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **column list**: At least one column. Order on screen is the report's column order (drag to reorder). *(source: contracts/satellite/reporting.yaml#CreateReportRequest)*
- **label (shown as "Column heading")**: Defaults to the field's business name; rename freely. *(source: contracts/satellite/reporting.yaml#ReportColumn)*
- **aggregation**: Offered only for aggregatable fields - Count, Distinct count, Sum, Average, Min, Max; Sum and Average only for numbers and money. *(source: contracts/satellite/reporting.yaml#ReportField / contracts/satellite/reporting.yaml#Aggregation)*
- **sortOrder, sortDirection (shown as "Sort 1, 2, 3" with ascending/descending)**: Sort priority, not position. Default newest first for date-time columns. *(source: contracts/satellite/reporting.yaml#ReportColumn)*
- **format**: Money columns are not given a decimal choice; they follow the venue currency (AED 2, BHD 3). Dates follow the reader's locale and the venue time zone. *(source: contracts/satellite/reporting.yaml#ReportColumn / DI-306 / MATRIX 6.1.78)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Reorder columns (primary button) | navigation or local | — | — | — | — |
| Rename display labels (secondary button) | navigation or local | — | — | — | — |
| Set width (secondary button) | navigation or local | — | — | — | — |
| Configure formatting (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **field list**: Grouped by type with icons (text, number, money, date, yes/no, list); badges "Personal data" and "Restricted" (needs a permission the user lacks - shown locked with the permission named in words). *(source: contracts/satellite/reporting.yaml#ReportField / contracts/satellite/reporting.yaml#listReportFields)*

**Data it reads**: `listReportFields` (onLoad, Fields available here)

**Where the user goes next**

- → `ANL-031` Report Catalogue & Library: *Back to Report Catalogue & Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The field column selector list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the field column selector untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No field column selector yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the field column selector are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **User adds a personal-data field (guest email)**: Allowed in the report for people who may see it; a note says exports including it need personal-data export permission and are recorded. *(source: contracts/satellite/reporting.yaml#ReportField / contracts/satellite/reporting.yaml#exportReportResult)*

#### Consistency with other screens

- Match `ANL-036`: Aggregation chosen here is the same control as on the grouping step.
- Match `ANL-038`: Labels set here are the headings ANL-038 formats.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
columns:
- field: Business date
  heading: Date
  sort: 1 descending
- field: Workstation
  heading: Till
- field: Payment method
  heading: Tender
- field: Amount
  heading: Amount (AED)
  aggregation: Sum
- field: Order count
  heading: Orders
  aggregation: Count
```

#### Permissions

- `listReportFields` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.6 | The system should be able to use and allow standardized reporting structure/software . | Retail POS | CONTRACTED | `listReportFields` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Report builder provides a library of standard operations/finance reports exportable as PDF or Excel, plus custom reports built drag-and-drop (no SQL) by choosing which data-set fields appear as columns/rows. *(client request · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-708)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-034` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-034`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 3
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 6: Works in Field & Column Selector → Allow users to visually select which information appears in the report.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-034?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Reorder columns, Rename display labels, Set width, Configure formatting.
- [ ] Every transition is wired: `ANL-031`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-035` Filter & Parameter Builder

**Allow report creators to define which records are included.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-035 |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `reportId` (navigation) |
| Route | `/analytics/filter-parameter-builder-anl-035` |

**Known gaps.** **Filter & Parameter Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Defines which records the report includes, without SQL: fixed filters, and parameters the person running it is asked for. The thing to get right: parameters narrow, they never widen; a venue manager cannot widen a filter to another venue because the filter is not what constrains them.

**Known correction pending (do not draw the wrong version)**

- **Each builder step (filters, grouping, cross-domain, layout) saves with updateReport** Why: Every update publishes a new version (full replace); four steps saved separately produce four published versions of a half-built report. The builder must save the whole definition once. *(source: contracts/satellite/reporting.yaml#updateReport / screens/P16-venue-analytics.yaml#ANL-035; Finance, Ledger & Tax · Reporting & Analytics)*
- **The gap says no write operation** Why: updateReport is declared; the gap text is stale. *(source: screens/P16-venue-analytics.yaml#ANL-035; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search filter parameter | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by date range, site, venue, attraction, business unit, product and 8 more — which are present is a decision the pack already made. | — |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **filter rows**: Field, operator, value. Operators by field type - text: is, is not, contains, is one of, is not one of, is empty, is not empty; number, money, date: is, greater than, less than, between. Between takes exactly two values (from, to); "is one of" takes a list; "is empty" takes none. Only filterable fields are offered. All rows apply together (and). *(source: contracts/satellite/reporting.yaml#ReportFilter)*
- **isParameter (shown as "Ask when running")**: Turns a filter into a prompt. Each prompt has a label, a type, required or optional, and a default; a required prompt with no default blocks the run. *(source: contracts/satellite/reporting.yaml#ReportFilter / contracts/satellite/reporting.yaml#ReportParameter / contracts/satellite/reporting.yaml#runReport)*
- **date range**: Every run has a date range; when none is given it is today in the venue's time zone, capped at the report's longest range. *(source: contracts/satellite/reporting.yaml#RunReportRequest / R158)*
- **Site, Venue, Cashier, POS, Payment method, Transaction status ... (pack chips)**: Present only where the data area has the field. Site and venue values list only places inside the author's scope. *(source: contracts/satellite/reporting.yaml#listReportFields / DI-183 / DI-151)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **plain-language summary**: Under the rows, the filter read back as a sentence ("Payments at Aquaventure Waterpark, tender is Cash or Card, on the date you choose"). *(source: DI-708)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save**: Publishes a new version of the whole definition; see correction on saving per step. *(source: contracts/satellite/reporting.yaml#updateReport)*

**Where the user goes next**

- → `ANL-031` Report Catalogue & Library: *Back to Report Catalogue & Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The filter parameter list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the filter parameter untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No filter parameter yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the filter parameter are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The report is a system report, which is clone-only (audit R096). |

#### Edge cases to draw

- **An OR condition (Cash or Card) across two fields**: Only "is one of" on a single field is expressible; across fields it is not. Draw no OR builder. *(source: contracts/satellite/reporting.yaml#ReportFilter)*
- **Relative dates (last 7 days)**: Offered as presets on the run-time date prompt, not as stored filter operators. *(source: contracts/satellite/reporting.yaml#ReportFilter)*

#### Consistency with other screens

- Match `ANL-027`: Parameters defined here are what a dashboard offers as viewer filters.
- Match `ANL-040`: The run screen's prompts are these parameters, same labels.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
filters:
- field: Payment method
  operator: is one of
  values:
  - Cash
  - Card
  - Foreign cash
- field: Workstation
  operator: is
  askWhenRunning: true
  label: Till
  required: false
- field: Business date
  operator: between
  askWhenRunning: true
  required: true
  default: Today
```

#### Permissions

- `updateReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-035` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-035`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 3
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 8: Works in Filter & Parameter Builder → Allow report creators to define which records are included.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-035?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-031`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-036` Grouping, Aggregation & Calculation Builder

**Turn detailed transactional data into meaningful management reporting.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-036 |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `reportId` (navigation) |
| Route | `/analytics/grouping-aggregation-calculation-builder-anl-036` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Period-over-Period Change. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **Grouping, Aggregation & Calculation Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Turns detail into management summaries: group by fields, choose totals, and (where it exists) derived measures. The thing to get right is what the contract can express today: grouping by fields and seven aggregations with server totals. Ratios, percent of total, running totals, ranking and period-over-period are not expressible in a report yet, so draw them as pending, not as working controls.

**Known correction pending (do not draw the wrong version)**

- **Calculation builder and the Period-over-Period Change button** Why: ReportColumn holds field, label, aggregation and format only; ratios, percent of total, running totals, moving averages, rank and period comparison have no field. *(source: contracts/satellite/reporting.yaml#ReportColumn / MATRIX 6.1.78; Finance, Ledger & Tax · Reporting & Analytics)*
- **The gap says no write operation** Why: updateReport is declared; the gap text is stale. *(source: screens/P16-venue-analytics.yaml#ANL-036; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do reports get calculated columns and period comparison, or do those stay KPI-only?** → Drawn default accepted: Show them disabled with "Available for KPIs". *(decided by Chinmay, 2026-10-02; DEC-338 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search grouping aggregation calculation | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by site, attraction, product, ticket type, channel, customer segment and 5 more — which are present is a decision the pack already made. | — |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **groupBy**: Ordered list of groupable fields; the order is the subtotal hierarchy (Venue, then Channel). *(source: contracts/satellite/reporting.yaml#CreateReportRequest / contracts/satellite/reporting.yaml#ReportField)*
- **aggregation per measure**: Count, Distinct count, Sum, Average, Min, Max. Average of money is rounded to the currency's scale. *(source: contracts/satellite/reporting.yaml#Aggregation / DI-306)*
- **time grain (pack Date, Week, Month, Year)**: Only where the data area offers a week or month field; there is no bucketing option on the report. *(source: contracts/satellite/reporting.yaml#CreateReportRequest)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Period-over-Period Change (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **totals**: Server-computed totals for aggregated columns only; a grand total row at the bottom, bold. *(source: contracts/satellite/reporting.yaml#ReportResult)*
- **grain warning**: Averaging an already averaged measure, or summing across a grain the data area does not have, shows a warning naming the grain. *(source: contracts/satellite/reporting.yaml#SemanticModel)*

**Where the user goes next**

- → `ANL-031` Report Catalogue & Library: *Back to Report Catalogue & Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The grouping aggregation calculation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the grouping aggregation calculation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No grouping aggregation calculation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the grouping aggregation calculation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The report is a system report, which is clone-only (audit R096). |

#### Edge cases to draw

- **Tenant-wide sum of money across an AED venue and a BHD venue**: Never one total; group by venue (or currency) and show a total per currency. *(source: DI-211)*
- **Net revenue built by hand from gross minus discounts**: Use the governed KPI instead; a report must not create a second definition of Net revenue. *(source: MATRIX 8.7.21)*

#### Consistency with other screens

- Match `ANL-025`: Derived business measures belong in the KPI builder, not in a report.
- Match `ANL-063`: Period-over-period comparison exists for KPIs (previous period, same period last year), not for reports.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
groupBy:
- Venue
- Sales channel
measures:
- field: Net amount
  aggregation: Sum
  heading: Net revenue (AED)
- field: Order id
  aggregation: Distinct count
  heading: Orders
result:
- venue: Aquaventure Waterpark
  channel: POS
  net: AED 182,440.25
  orders: 3112
- venue: Aquaventure Waterpark
  channel: Web
  net: AED 241,090.00
  orders: 2874
```

#### Permissions

- `updateReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-036` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-036`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 3
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 10: Works in Grouping, Aggregation & Calculation Builder → Turn detailed transactional data into meaningful management reporting.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-036?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Period-over-Period Change.
- [ ] Every transition is wired: `ANL-031`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-037` Cross-Domain Report Composer

**Allow authorized users to combine information across multiple TICVAI modules. This is one of the most important capabilities of Board 3.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-037 |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `reportId` (navigation) |
| Route | `/analytics/cross-domain-report-composer-anl-037` |

**Known gaps.** **Cross-Domain Report Composer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The client calls cross-domain reporting one of the most important capabilities of the report builder: ticket sales with F&B spend per visitor, admissions with membership, and so on. The thing to get right: today a report reads exactly one data area, so nothing on this screen can be saved; the design is the specification, and it must keep relationships governed (declared joins only) and grain visible.

**Known correction pending (do not draw the wrong version)**

- **A report has exactly one data area** Why: CreateReportRequest.dataSource is a single value and listReportFields is per data area, so a cross-domain report cannot be defined; relationships in the semantic model are never used by a report. *(source: contracts/satellite/reporting.yaml#CreateReportRequest / MATRIX 8.7.11; Finance, Ledger & Tax · Reporting & Analytics)*
- **The gap says no write operation, and the screen has no content region** Why: updateReport is declared; the content (primary dataset, related datasets, cardinality) is drawable from the semantic model. *(source: screens/P16-venue-analytics.yaml#ANL-037; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **How does a definition name more than one dataset - a list of sources with declared joins, or a cross-domain dataset published in the semantic model?** → Drawn default accepted: Draw primary plus related datasets; mark Save as pending. *(decided by Chinmay, 2026-10-02; DEC-339 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **primary dataset**: The dataset whose grain the report keeps; every other dataset joins to it. *(source: contracts/satellite/reporting.yaml#SemanticModel)*
- **related datasets**: Only datasets with a declared relationship to the primary one. Many-to-one joins are safe; one-to-many shows "This repeats each order once per line - totals may multiply"; many-to-many is not offered. *(source: contracts/satellite/reporting.yaml#SemanticModel / contracts/satellite/reporting.yaml#getSemanticModel)*
- **access per domain**: The author must hold the access of every domain combined; a domain they cannot read is not offered. *(source: contracts/satellite/reporting.yaml#createReport)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save report (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getSemanticModel` (onLoad, How domains relate)

**Where the user goes next**

- → `ANL-031` Report Catalogue & Library: *Back to Report Catalogue & Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-domain report composer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-domain report composer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-domain report composer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-domain report composer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The report is a system report, which is clone-only (audit R096). |

#### Edge cases to draw

- **Two domains refreshed at different times**: Each joined dataset shows its own "as of" time on the result. *(source: contracts/satellite/reporting.yaml#ReportResult / contracts/satellite/reporting.yaml#AnalyticsPipeline)*

#### Consistency with other screens

- Match `ANL-066`: Relationships shown are the catalogue's, with the same cardinality wording.
- Match `ANL-033`: The primary dataset is chosen with the same cards.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
primary: Admission scans
related:
- dataset: Order lines
  via: Visit
  cardinality: one visit to many lines
  note: per-visit totals
- dataset: Memberships
  via: Guest
  cardinality: many scans to one membership
example: 'Spend per guest by visit day - Aquaventure Waterpark, September 2026: AED 96.40 average'
```

#### Permissions

- `getSemanticModel` → `REPORT_VIEW_TENANT` (operate) · staff
- `updateReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-037` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-037`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 3
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 12: Works in Cross-Domain Report Composer → Allow authorized users to combine information across multiple TICVAI modules. This is one of the most important capabilities of Board 3.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-037?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save report, Cancel.
- [ ] Every transition is wired: `ANL-031`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-038` Report Layout & Formatting Designer

**Control how the final report is displayed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-038 |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `reportId` (navigation) |
| Route | `/analytics/report-layout-formatting-designer-anl-038` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: TICVAI branding, Report logo. Each needs an operation, or needs removing from the screen; this is the Phase … **Report Layout & Formatting Designer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** How the finished report looks on screen, in Excel and in PDF, in English and in Arabic. The thing to get right is money and language: money keeps the currency's decimals (AED 2, BHD/KWD/OMR 3, never rounded away), exports carry numbers as numbers, and an Arabic PDF is laid out right to left.

**Known correction pending (do not draw the wrong version)**

- **Only a column label and a free-text format exist** Why: Page layout, orientation, header, footer, logo, language and conditional formatting have no field on the report; the pack's branding and logo buttons have nothing to save to. *(source: contracts/satellite/reporting.yaml#ReportColumn / screens/P16-venue-analytics.yaml#ANL-038; Finance, Ledger & Tax · Reporting & Analytics)*
- **A column has one label string** Why: Arabic reports are a core requirement; one label cannot carry an English and an Arabic heading. *(source: contracts/satellite/reporting.yaml#ReportColumn / DI-019; Finance, Ledger & Tax · Reporting & Analytics)*
- **Decimal precision and Currency drawn as free selects** Why: Money precision follows the currency (3 decimals for BHD/KWD/OMR) and records are in base currency; letting a user pick 2 decimals for BHD drops the third. *(source: DI-306 / DI-211; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is the report language chosen per run, per schedule, or by the reader's profile?** → Drawn default accepted: By the reader's language; the schedule's recipients get the owner's choice. *(decided by Chinmay, 2026-10-02; DEC-340 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Western or Arabic-Indic digits in Arabic PDFs?** → Drawn default accepted: Western digits. *(decided by Chinmay, 2026-10-02; DEC-341 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Column labels | select field | — | — | — | — | — | — |
| Number format | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Percentage | select field | — | — | — | — | — | — |
| Date format | select field | — | — | — | — | — | — |
| Decimal precision | select field | — | — | — | — | — | — |
| Conditional formatting | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Column labels**: From the field step; one heading per column (see correction on Arabic headings). *(source: contracts/satellite/reporting.yaml#ReportColumn)*
- **Number, Percentage, Decimal precision**: Percent to one decimal by default; counts with no decimals; money precision is not a user choice. *(source: DI-306)*
- **Currency**: Not a choice. Each venue's base currency; a multi-venue report shows the currency per row. *(source: DI-211)*
- **Date format**: Locale-aware, in the venue's time zone; the PDF header states the zone ("Times in Gulf Standard Time"). *(source: MATRIX 6.1.78)*
- **Conditional formatting**: Rule plus icon or text, never colour alone (e.g. variance below zero shows a down arrow and the word Short). *(source: MATRIX 8.7.1)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| TICVAI branding (primary button) | navigation or local | — | — | — | — |
| Report logo (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **PDF**: Header with tenant logo and report name, venue, period, parameters used, "Data as of 07:00" and version; footer with page x of y and generated-by. Arabic: mirrored layout, Arabic headings, right-aligned text, numbers left-to-right inside cells. *(source: DI-019 / contracts/satellite/reporting.yaml#ReportResult / contracts/satellite/reporting.yaml#ReportExecution)*
- **Excel**: Money as numeric cells with the currency format and its decimals (BHD 0.000); totals as values computed by the server, not spreadsheet formulas; frozen header row. *(source: contracts/satellite/reporting.yaml#ReportResult / DI-306)*

**Where the user goes next**

- → `ANL-031` Report Catalogue & Library: *Back to Report Catalogue & Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report layout formatting configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report layout formatting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report layout formatting configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The report is a system report, which is clone-only (audit R096). |

#### Consistency with other screens

- Match `ANL-044`: The logo and branding used here are the tenant's white-label assets, the same as on emails.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
header:
  report: Daily closing - Aquaventure Waterpark
  period: 30 Sep 2026
  asOf: 01 Oct 2026 07:00
  version: '4'
  zone: Gulf Standard Time
rows:
- till: POS-03 Main Gate
  tender: Cash
  amount: AED 8,460.00
  variance: AED -20.00 Short
- till: POS-07 Wave Bar
  tender: Card
  amount: AED 12,915.50
bahrainRow:
  venue: Lost Paradise of Dilmun
  amount: BHD 2,013.125
arabicHeading: تقرير الإغلاق اليومي
```

#### Permissions

- `updateReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Custom report templates (advanced users, SQL/scripting) exported as PDF or Excel; ticket and receipt layouts built in a drag-and-drop template builder placing dynamic variables (guest name, ticket number, QR) on a background image. *(agreed · MoM 7 Aug 2026, 22. Report & Document Template Design · DI-184)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-038` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-038`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 3
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 14: Works in Report Layout & Formatting Designer → Control how the final report is displayed.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-038?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: TICVAI branding, Report logo.
- [ ] Every transition is wired: `ANL-031`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-039` Report Preview, Test & Validation

**Allow users to verify report accuracy before saving or publishing it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-039 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `executionId` (navigation), `reportId` (navigation) |
| Route | `/analytics/report-preview-test-validation-anl-039` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Checks a report before it is saved or shared: run it, see what came back, how long it took, what constrained it, and whether totals look right. The thing to get right: there is no sample mode - a test run is a real run under the author's own access - so a large range may run in the background and must be cancellable.

**Known correction pending (do not draw the wrong version)**

- **"Run it against a sample"** Why: A run has no row limit or sample option; it is a full run under the author's access. Design a capped date range, not a sample. *(source: contracts/satellite/reporting.yaml#RunReportRequest / screens/P16-venue-analytics.yaml#ANL-039; Finance, Ledger & Tax · Reporting & Analytics)*
- **Testing a change means publishing it first** Why: runReport runs a saved definition and every save publishes a version, so an unsaved change cannot be tested. *(source: contracts/satellite/reporting.yaml#runReport / contracts/satellite/reporting.yaml#updateReport; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Can a draft definition be test-run before it is published?** → Drawn default accepted: Draw "Test run" on the draft; mark it pending. *(decided by Chinmay, 2026-10-02; DEC-342 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every report preview test** (data table)

| Shows | Format | Notes |
|---|---|---|
| Sample results | text | not in the schema: `Sample Results` |
| Total records | text | not in the schema: `Total Records` |
| Applied filters | text | not in the schema: `Applied Filters` |
| Calculated fields | text | not in the schema: `Calculated Fields` |
| Grouping | text | not in the schema: `Grouping` |
| Totals | text | not in the schema: `Totals` |
| Execution time | text | not in the schema: `Execution Time` |
| Data refresh time | text | not in the schema: `Data Refresh Time` |

**The selected report preview test** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Sample results | text | not in the schema: `Sample Results` |
| Total records | text | not in the schema: `Total Records` |
| Applied filters | text | not in the schema: `Applied Filters` |
| Calculated fields | text | not in the schema: `Calculated Fields` |
| Grouping | text | not in the schema: `Grouping` |
| Totals | text | not in the schema: `Totals` |
| Execution time | text | not in the schema: `Execution Time` |
| Data refresh time | text | not in the schema: `Data Refresh Time` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **run summary**: Rows returned, time taken, version tested, data as of, the parameters used (defaults filled in), and "What limited this result" in words ("Your access: Aquaventure Waterpark"). *(source: contracts/satellite/reporting.yaml#ReportExecution / contracts/satellite/reporting.yaml#ReportResult)*
- **checks**: Blocking: a required prompt with no value or default; a date range over the longest allowed. Warning: estimated cost High (will always run in the background); personal-data columns present; totals that do not match the standard report for the same period (e.g. Sales by channel). *(source: contracts/satellite/reporting.yaml#runReport / contracts/satellite/reporting.yaml#ReportDefinition)*
- **sample rows**: The first page of the result (cursor-paged), with totals. *(source: contracts/satellite/reporting.yaml#getReportResult)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Test run**: Up to the inline limit (5,000 rows proposed) results return at once; beyond it, or for a High-cost report, it queues and shows Queued, Running with a Cancel. *(source: contracts/satellite/reporting.yaml#runReport / R094)*
- **Cancel run**: Stops a running test; status Cancelled. *(source: contracts/satellite/reporting.yaml#cancelReportExecution)*

**Where the user goes next**

- → `ANL-031` Report Catalogue & Library: *Back to Report Catalogue & Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report preview test list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report preview test untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report preview test yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the report preview test are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 409 Already completed |

#### Edge cases to draw

- **Run fails**: Shows the error in words and keeps the definition unchanged. *(source: contracts/satellite/reporting.yaml#ReportExecution)*
- **Results expired**: The result is kept for a limited time; an old test shows "Results expired - run again". *(source: contracts/satellite/reporting.yaml#ReportExecution / contracts/satellite/reporting.yaml#ExecutionStatus)*

#### Consistency with other screens

- Match `ANL-040`: Same result table and header as the run screen.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
summary:
  rows: 1284
  took: 2.4 s
  version: draft of v5
  asOf: 01 Oct 2026 10:41
  limitedTo: Aquaventure Waterpark
  parameters: Business date 30 Sep 2026; Till - all
checks:
- severity: Warning
  text: Includes guest email - exports need personal-data permission
- severity: Pass
  text: Total AED 412,860.50 matches Sales by channel for 30 Sep 2026
```

#### Permissions

- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `getReportExecution` → `REPORT_VIEW_VENUE` (operate) · staff
- `cancelReportExecution` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-039` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-039`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 3
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 16: Works in Report Preview, Test & Validation → Allow users to verify report accuracy before saving or publishing it.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-039?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-031`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-040` Save, Run & Report Results Viewer

**Provide the final operational interface for executing and consuming reports.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-040 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display; Dashboard Designer Report Builder) and a per-row directory (§KPI cards/charts Rows, columns, matrices) — counts over a population, then … |
| Offline | online only |
| Opens with | `executionId` (navigation), `reportId` (navigation) |
| Route | `/analytics/save-run-report-results-viewer-anl-040` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Runs a report and shows the result: prompts, the table with totals, and exports. The header states exactly what was run, so a figure can be reproduced months later. The thing to get right: large results run in the background and page, never freeze; exports are permission-gated and personal data needs a separate permission and a stated purpose.

**Known correction pending (do not draw the wrong version)**

- **XML export** Why: The client's export list includes XML, but the export formats are CSV, Excel, PDF and JSON. *(source: contracts/satellite/reporting.yaml#ExportFormat / MATRIX 6.1.20 / screens/P16-venue-analytics.yaml#ANL-045; Finance, Ledger & Tax · Reporting & Analytics)*
- **Export permissions are listed as an unclaimed banner** Why: The export controls are the ones that claim them; draw them on the export menu (export, then personal-data export), not as a banner. *(source: screens/P16-venue-analytics.yaml#ANL-040 / contracts/satellite/reporting.yaml#exportReportResult; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **prompts**: The report's parameters with their labels and defaults; required ones marked; date range defaults to today in the venue's time zone. *(source: contracts/satellite/reporting.yaml#RunReportRequest / contracts/satellite/reporting.yaml#ReportParameter / R158)*
- **venueId (shown as "Venue")**: Narrows to one venue; it cannot reach beyond the user's access. *(source: contracts/satellite/reporting.yaml#RunReportRequest)*

#### Outputs: what the screen shows and produces

**Shown**

**Report Name** (metric tile)

**Description** (metric tile)

**Owner** (metric tile)

**Last Run** (metric tile)

**Data Refresh** (metric tile)

**Applied Parameters** (metric tile)

**Reporting Period** (metric tile)

**Visual management dashboards Detailed reporting** (metric tile)

**Every save run report** (data table)

| Shows | Format | Notes |
|---|---|---|
| Executive/operational monitoring analysis/reconciliation/detail | text | not in the schema: `Executive/operational monitoring Analysis/reconciliation/detail` |
| Persistent dashboard layout parameter driven report execution | text | not in the schema: `Persistent dashboard layout Parameter-driven report execution` |

**The selected save run report** (detail panel): The pack groups this record's detail under its own headings: “Further Actions”, “A user could type”, “Visualization focused Data/report focused”.

| Shows | Format | Notes |
|---|---|---|
| Executive/operational monitoring analysis/reconciliation/detail | text | not in the schema: `Executive/operational monitoring Analysis/reconciliation/detail` |
| Persistent dashboard layout parameter driven report execution | text | not in the schema: `Persistent dashboard layout Parameter-driven report execution` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Excel, PDF, CSV, XML. Each needs attaching to the control it gates, or the screen needs the control.

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **result header**: Report name and version, period, parameters used, "What limited this result" in words, "Data as of 10:41" (the replica position), run by and when, and "Results kept until 08 Oct 2026". *(source: contracts/satellite/reporting.yaml#ReportExecution / contracts/satellite/reporting.yaml#ReportResult)*
- **table**: Virtualised, cursor-paged; server totals pinned at the bottom; money in the venue currency at its scale; labels Gross sales, Discounts, Refunds, Net revenue never shortened to "Revenue". *(source: contracts/satellite/reporting.yaml#ReportResult / DI-710)*
- **export menu**: Excel, PDF, CSV (and JSON for systems). Shown only with export permission. "Include personal data" appears only with personal-data export permission and then requires a purpose; the dialog says the export is recorded. *(source: contracts/satellite/reporting.yaml#exportReportResult / contracts/satellite/reporting.yaml#ExportFormat)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Run**: Small results show at once; large ones queue with Queued and Running states and a Cancel; when complete the table loads. *(source: contracts/satellite/reporting.yaml#runReport / contracts/satellite/reporting.yaml#getReportExecution)*
- **Export**: Always in the background; a progress chip then a Download link that expires. *(source: contracts/satellite/reporting.yaml#exportReportResult / contracts/satellite/reporting.yaml#getReportExport)*
- **Schedule**: Opens ANL-042 with this report and the current prompt values. *(source: contracts/satellite/reporting.yaml#CreateReportScheduleRequest)*

**Where the user goes next**

- → `ANL-031` Report Catalogue & Library: *Back to Report Catalogue & Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The save run report list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the save run report untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No save run report yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the save run report are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 409 Execution has not completed |

#### Edge cases to draw

- **Date range longer than the report allows**: Refused before running, naming the limit ("This report covers at most 31 days"). *(source: contracts/satellite/reporting.yaml#runReport)*
- **AI-assisted building on a finance report**: Finance AI reporting is phase two; do not draw the AI prompt on financial reports in phase one. *(source: DI-278)*

#### Consistency with other screens

- Match `ANL-045`: Exports started here appear in the export centre with the same statuses.
- Match `ANL-052`: The "Ask TICVAI to build my report" entry hands off to the natural-language screen; its saved answer becomes a report run here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
header:
  report: Shift summary
  version: '3'
  period: 30 Sep 2026
  limitedTo: Aquaventure Waterpark
  asOf: 01 Oct 2026 07:00
  runBy: Fatima Al Mansoori
  keptUntil: 08 Oct 2026
rows:
- till: POS-03 Main Gate
  cashier: Rahul Menon
  expected: AED 8,480.00
  counted: AED 8,460.00
  variance: AED -20.00 Short
- till: POS-05 Kids Zone
  cashier: Omar Haddad
  expected: AED 3,215.50
  counted: AED 3,215.50
  variance: AED 0.00
totals:
  expected: AED 11,695.50
  counted: AED 11,675.50
  variance: AED -20.00
```

#### Permissions

- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `getReportResult` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Very large drill-down result sets (e.g. 10,000 transactions in a single day) must be handled without the interface crashing or becoming unresponsive. *(agreed · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-710)*
- Drill-down from a high-level figure to transaction detail - yearly sales -> monthly -> daily -> sales channel -> individual transaction -> transaction detail (which customer, which ticket) - only where the data has a genuine hierarchy. *(agreed · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-709)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-040` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS174 Unified BI Reporting and AI Analytics Platform Board 3.dc.html#anl-040`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 3
- Flow F177 *Unified BI Reporting and AI Analytics Platform board 3: Report Catalogue & …*, step 18: Works in Save, Run & Report Results Viewer → Provide the final operational interface for executing and consuming reports.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-040?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-031`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cancelReportExecution": {"method":"DELETE","path":"/report-executions/{executionId}","contract":"reporting","summary":"Cancel a running execution","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createReport": {"method":"POST","path":"/reports","contract":"reporting","summary":"Create a custom report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"getReportExecution": {"method":"GET","path":"/report-executions/{executionId}","contract":"reporting","summary":"Execution status, and where its result is","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportExecution"},
"getReportResult": {"method":"GET","path":"/report-executions/{executionId}/result","contract":"reporting","summary":"Paged result rows","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportResult"},
"getSemanticModel": {"method":"GET","path":"/semantic-model","contract":"reporting","summary":"The business data catalogue reports are built from","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SemanticModel"},
"listReportFields": {"method":"GET","path":"/report-fields","contract":"reporting","summary":"Fields available for a data source","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"dataSource","in":"query","required":true}],"requestBody":null,"responds":"ReportField"},
"listReports": {"method":"GET","path":"/reports","contract":"reporting","summary":"List available report definitions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSeededReports": {"method":"GET","path":"/reports/seeded","contract":"reporting","summary":"The reports every venue starts with","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SeededReport"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"updateReport": {"method":"PUT","path":"/reports/{reportId}","contract":"reporting","summary":"Publish a new version of a definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Aggregation": {"type":"string","enum":["none","count","countDistinct","sum","average","min","max"]},
"Cadence": {"x-ticvai-persistence":"none — embedded in schedule","type":"object","description":"**What each frequency needs (decided 28 September, audit R158).** `daily`: `timeOfDay`. `weekly`: `dayOfWeek` and `timeOfDay`. `monthly`: `dayOfMonth` and `timeOfDay`, a day past the month's end running on its last day. `quarterly`: `dayOfMonth` and `timeOfDay`, in the first month of each quarter. `onShiftClose` and `onPeriodClose`: nothing else, they run on the event. A field a frequency needs and does not have, or one it does not take, is the 400 on `createReportSchedule`. **Times are in the venue's time zone.**\n","required":["frequency"],"properties":{"frequency":{"type":"string","enum":["daily","weekly","monthly","quarterly","onShiftClose","onPeriodClose"]},"dayOfWeek":{"type":"integer","minimum":0,"maximum":6},"dayOfMonth":{"type":"integer","minimum":1,"maximum":31},"timeOfDay":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"timeZone":{"type":"string","readOnly":true,"description":"Always the venue's time zone (decided 28 September, audit R158), returned so a reader knows which. Not taken on a write."}}},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"DataSource": {"type":"string","description":"What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n","enum":["orders","orderLines","payments","refunds","shifts","scanEvents","entitlements","products","inventory","stockMovements","stockCounts","waste","workstations","devices","principals","loyalty","reviews","queueEntries","guests","campaigns","cases","ledgerEntries","workOrders","approvals","purchaseOrders","receipts","requisitions","stockBatches","resourceBookings","delegations","forms","challenges","wallets","resaleListings","accreditationApplications","accreditationHolders","accreditationCredentials","forecastPoints"],"x-ticvai-forecast-points":"**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"},
"ExecutionStatus": {"type":"string","enum":["queued","running","completed","failed","cancelled","expired"]},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReportCategory": {"type":"string","enum":["sales","admission","financial","inventory","guest","operations","marketing","workforce","compliance","custom"]},
"ReportColumn": {"x-ticvai-persistence":"reporting.report_column","type":"object","required":["field"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"label":{"type":"string"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"default":"none"},"sortOrder":{"type":"integer"},"sortDirection":{"type":"string","enum":["asc","desc"]},"format":{"type":"string","nullable":true},"role":{"type":"string","nullable":true,"enum":["dimension","measure"],"description":"**What the column is to a chart** (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a `measure` is aggregated (sum of net revenue, count of admissions). Null on a column only a table shows."},"encoding":{"type":"string","nullable":true,"enum":["category","x","y","series","value","size","colour","location","stage","source","target","row","column","hierarchyLevel","label","tooltip"],"description":"**Which field well the column fills** (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. The per-mark rule is on that field."},"axis":{"type":"string","nullable":true,"enum":["primary","secondary"],"description":"For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007)."},"seriesType":{"type":"string","nullable":true,"enum":["bar","line","area"],"description":"For a measure on a `combo`, how that series is drawn (CHG-FIN-007)."},"hierarchyLevel":{"type":"integer","nullable":true,"minimum":1,"description":"For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. Levels must follow a real hierarchy (DI-709), for example year, month, day, or region, venue, outlet (CHG-FIN-007)."},"unitLabel":{"type":"string","nullable":true,"maxLength":40,"description":"The unit an axis states, for example \"AED\" or \"Admissions\". Required on a secondary axis (CHG-FIN-007)."}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportExecution": {"x-ticvai-persistence":"reporting.execution","type":"object","required":["id","reportId","definitionVersion","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"reportId":{"type":"string","format":"uuid"},"reportName":{"type":"string"},"definitionVersion":{"type":"string","description":"The version this ran against. With the parameters and scope below, it is everything needed to reproduce the result.\n"},"status":{"$ref":"#/components/schemas/ExecutionStatus"},"parameters":{"type":"object","additionalProperties":true,"description":"The parameters it ran with, keyed by `ReportParameter.key` of `definitionVersion` — defaults filled in, so the record is complete."},"scopeApplied":{"type":"array","description":"Scope paths the caller held. What constrained the result.","items":{"type":"string"}},"rowCount":{"type":"integer","nullable":true},"durationMs":{"type":"integer","nullable":true},"error":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"scheduleId":{"type":"string","format":"uuid","nullable":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true,"description":"Results are retained for a limited period, then discarded."}}},
"ReportField": {"x-ticvai-persistence":"none — metadata catalogue, generated","type":"object","required":["key","label","type","isGroupable","isAggregatable","isFilterable"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"},"isGroupable":{"type":"boolean"},"isAggregatable":{"type":"boolean"},"isFilterable":{"type":"boolean"},"isPersonalData":{"type":"boolean","description":"Requires REPORT_EXPORT_PII to include in an export."},"requiredPermission":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}],"nullable":true,"description":"The permission a principal needs to see this field. Null where the report's own permission is enough."},"enumValues":{"type":"array","items":{"type":"string"}}}},
"ReportFilter": {"x-ticvai-persistence":"reporting.report_filter","type":"object","required":["field","operator"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","contains","isNull","isNotNull"]},"value":{"description":"**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"},"values":{"type":"array","description":"The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.","items":{}},"isParameter":{"type":"boolean","default":false,"description":"Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"}}},
"ReportParameter": {"x-ticvai-persistence":"reporting.report_parameter","type":"object","required":["key","label","type","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"},"isRequired":{"type":"boolean"},"defaultValue":{"description":"Open on purpose. A value of this parameter's `type`, used when a run supplies none."}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"SeededReport": {"type":"object","description":"BL-053. **`ReportDefinition.isSystem` existed and nothing populated it.** Twenty-eight requirements asked for dashboards and analyses over data that was already there, and the answer to every one of them was *\"the builder can do that\"* — which is true and is not a deliverable.\n**A venue opening on Monday does not want a report builder. It wants the eight reports every venue runs**, and the ability to change them.\nSeeded at provisioning, `isSystem` true, and **clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse a system report with 409, and a venue that wants one different clones it with `createReport`. The eight codes are listed on `listSeededReports` (proposed, audit R282).\n","required":["code","name","category","dataSource"],"properties":{"code":{"type":"string"},"name":{"type":"string"},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"appliesToVenueKinds":{"type":"array","description":"**A water park does not need a theatre's seat-utilisation report.** Empty means every venue kind.\n","items":{"type":"string"}},"defaultSchedule":{"$ref":"#/components/schemas/Cadence"},"rationale":{"type":"string","description":"**Why this report ships, in words a venue manager reads.** A seeded report with no rationale is one somebody deletes as clutter in the first week.\n"}}},
"SemanticModel": {"type":"object","x-ticvai-persistence":"reporting.semantic_model","description":"BI boards 3.3 and 10.6. **A vocabulary, not a schema.** Exposing joins to report authors produces reports that are wrong invisibly.\n","properties":{"version":{"type":"integer","readOnly":true,"description":"Assigned by the server on each publish."},"domains":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"datasets":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"grain":{"type":"string","description":"**What one row means.** The single most common cause of a wrong report is a join that silently multiplied the grain.\n"},"fields":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"dataType":{"$ref":"#/components/schemas/FieldType"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"nullable":true,"description":"The default aggregation for the field, where it has one."},"sensitive":{"type":"boolean","default":false},"description":{"type":"string","nullable":true}}}}}}}}}},"relationships":{"type":"array","items":{"type":"object","properties":{"fromDataset":{"type":"string"},"toDataset":{"type":"string"},"cardinality":{"type":"string","enum":["oneToOne","oneToMany","manyToOne","manyToMany"]}}}},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}}
}
```
