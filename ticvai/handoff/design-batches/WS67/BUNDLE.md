# WS67 — Unified BI Reporting and AI Analytics Platform board 2

**10 screens · 13 operations · 15 schemas · 3 permissions**

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
| `ANL-021` | Dashboard Library | D | 0 | 62 | 6 | 18 | 2 | 0 | — | notStarted (—) |
| `ANL-022` | Dashboard Creation Wizard | D | 18 | 0 | 5 | 18 | 1 | 0 | — | notStarted (—) |
| `ANL-023` | Drag-and-Drop Dashboard Canvas | A | 37 | 33 | 6 | 18 | 3 | 0 | — | notStarted (—) |
| `ANL-024` | Widget & Visualization Library | D | 0 | 12 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-025` | KPI Builder | A | 22 | 7 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-026` | Targets, Thresholds & KPI Status Rules | D | 0 | 16 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-027` | Data & Filter Configuration | D | 18 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ANL-028` | Drill-Down & Interaction Designer | D | 9 | 0 | 5 | 0 | 3 | 0 | — | notStarted (—) |
| `ANL-029` | Dashboard Access, Publishing & Versioning | D | 0 | 12 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `ANL-030` | Dashboard Preview, Validation & Health | D | 0 | 18 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-021, ANL-024, ANL-029, ANL-030 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-021` Dashboard Library

**Provide a centralized catalogue for all standard, custom, AI-generated and embedded TICVAI dashboards.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-021 |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display dashboard cards/table containing; Dashboard Categories; Dashboard Types) and no metric row |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/dashboard-library-anl-021` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The one catalogue of dashboards, inside the single permission-based reporting area (no copies of it inside each module). A login sees only the dashboards of modules it is entitled to, narrowed to its own scope; a module the tenant has not licensed never appears, not even as an empty filter. The thing to get right: the pack's Status, Version, Last Published and AI-generated columns have no source yet, so the library must not invent them; draw what exists (shared or private, archived, area, owner, refresh load) and show lifecycle as pending until ANL-029 has a contract.

**Known correction pending (do not draw the wrong version)**

- **The gap says the screen's operations return no schema with described properties** Why: listDashboards returns Dashboard (name, module, description, venueId, isShared, ownerPrincipalId, aggregateCost, archivedAt, createdAt); Name, Owner, Sites/Venues and Category can bind today. *(source: contracts/satellite/reporting.yaml#Dashboard / screens/P16-venue-analytics.yaml#ANL-021; Finance, Ledger & Tax · Reporting & Analytics)*
- **18 of the 31 "columns" are category and type values (Executive ... Custom; System, Custom and AI-Generated Dashboard)** Why: They are filter values of one Area dimension and one origin dimension, not columns; drawn as columns the table is 31 wide and mostly empty. *(source: screens/P16-venue-analytics.yaml#ANL-021; Finance, Ledger & Tax · Reporting & Analytics)*
- **Status, Version, Last Modified, Last Published and origin (system, custom, AI-generated) have no field on Dashboard** Why: ReportDefinition has isSystem and versions; Dashboard has neither, so the library cannot tell a seeded dashboard from a custom one or show a published version. *(source: contracts/satellite/reporting.yaml#Dashboard / contracts/satellite/reporting.yaml#ReportDefinition / MATRIX 7.1.46; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does Dashboard gain an origin flag (standard, custom, AI-generated) and a lifecycle status with a version, as ReportDefinition has?** → Drawn default accepted: Draw Shared/Private and Archived, which exist; draw the Status and Version columns in a visibly pending style tied to ANL-029. *(decided by Chinmay, 2026-10-02; DEC-326 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | select | — | Core · Ticketing · Access · Fnb · Retail · Inventory · Seating · Membership · Marketing · Resources · Queue · Transport … | `listDashboards` ?module |
| Include archived | toggle | off | — | `listDashboards` ?includeArchived |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **module (shown as the "Area" filter chips)**: One chip per module the login is entitled to (Finance, Sales, Operations, F&B, Retail ...). Asking for a module the caller cannot see returns an empty list, so never render a chip for an unentitled module; a hidden module disappears from navigation rather than showing greyed. *(source: contracts/satellite/reporting.yaml#listDashboards / DI-721 / DI-387)*
- **includeArchived (shown as "Show archived")**: Off by default. Archived rows carry "Archived 12 Sep 2026" and are read-only; there is no restore operation, so draw no Restore button. *(source: contracts/satellite/reporting.yaml#Dashboard)*
- **search**: listDashboards has no search parameter and is not paged; search filters the returned list on the client by name and description. *(source: contracts/satellite/reporting.yaml#listDashboards)*

#### Outputs: what the screen shows and produces

**Shown**

**Every record** (data table)

| Shows | Format | Notes |
|---|---|---|
| Dashboard name | text | not in the schema: `Dashboard Name` |
| Dashboard ID | text | not in the schema: `Dashboard ID` |
| Category | text | not in the schema: `Category` |
| Business domain | text | not in the schema: `Business Domain` |
| Owner | text | not in the schema: `Owner` |
| Sites/venues | text | not in the schema: `Sites/Venues` |
| Audience/role | text | not in the schema: `Audience/Role` |
| Status | text | not in the schema: `Status` |
| Version | text | not in the schema: `Version` |
| Last modified | text | not in the schema: `Last Modified` |
| Last published | text | not in the schema: `Last Published` |
| Usage count | text | not in the schema: `Usage Count` |
| Data refresh status | text | not in the schema: `Data Refresh Status` |
| Executive | text | not in the schema: `Executive` |
| Operations | text | not in the schema: `Operations` |
| Finance | text | not in the schema: `Finance` |
| Sales | text | not in the schema: `Sales` |
| Ticketing | text | not in the schema: `Ticketing` |
| Access control | text | not in the schema: `Access Control` |
| CRM | text | not in the schema: `CRM` |
| Marketing | text | not in the schema: `Marketing` |
| Membership | text | not in the schema: `Membership` |
| Loyalty | text | not in the schema: `Loyalty` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Inventory | text | not in the schema: `Inventory` |
| Resources | text | not in the schema: `Resources` |
| Custom | text | not in the schema: `Custom` |
| System dashboard — TICVAI standard dashboard | text | not in the schema: `System Dashboard — TICVAI standard dashboard` |
| Custom dashboard — customer created | text | not in the schema: `Custom Dashboard — customer-created` |
| … 1 more | | `schemas.json` |

**The selected record** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Dashboard name | text | not in the schema: `Dashboard Name` |
| Dashboard ID | text | not in the schema: `Dashboard ID` |
| Category | text | not in the schema: `Category` |
| Business domain | text | not in the schema: `Business Domain` |
| Owner | text | not in the schema: `Owner` |
| Sites/venues | text | not in the schema: `Sites/Venues` |
| Audience/role | text | not in the schema: `Audience/Role` |
| Status | text | not in the schema: `Status` |
| Version | text | not in the schema: `Version` |
| Last modified | text | not in the schema: `Last Modified` |
| Last published | text | not in the schema: `Last Published` |
| Usage count | text | not in the schema: `Usage Count` |
| Data refresh status | text | not in the schema: `Data Refresh Status` |
| Executive | text | not in the schema: `Executive` |
| Operations | text | not in the schema: `Operations` |
| Finance | text | not in the schema: `Finance` |
| Sales | text | not in the schema: `Sales` |
| Ticketing | text | not in the schema: `Ticketing` |
| Access control | text | not in the schema: `Access Control` |
| CRM | text | not in the schema: `CRM` |
| Marketing | text | not in the schema: `Marketing` |
| Membership | text | not in the schema: `Membership` |
| Loyalty | text | not in the schema: `Loyalty` |
| F&B | text | not in the schema: `F&B` |
| Retail | text | not in the schema: `Retail` |
| Inventory | text | not in the schema: `Inventory` |
| Resources | text | not in the schema: `Resources` |
| Custom | text | not in the schema: `Custom` |
| System dashboard — TICVAI standard dashboard | text | not in the schema: `System Dashboard — TICVAI standard dashboard` |
| Custom dashboard — customer created | text | not in the schema: `Custom Dashboard — customer-created` |
| … 1 more | | `schemas.json` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **list row**: Name, area, owner, venue ("All my venues" when no venue is set), Shared or Private badge, created date. Shared dashboards first within an area, then alphabetical. Usage count and data freshness come from tenant-level reads, so show those two columns only to tenant-level users; never a column of blanks. *(source: contracts/satellite/reporting.yaml#Dashboard / contracts/satellite/reporting.yaml#getAnalyticsUsage / contracts/satellite/reporting.yaml#listAnalyticsPipelines)*
- **refresh load badge (authors only)**: aggregateCost low / medium / high, worded "Refresh load - High"; it is the summed refresh of every tile, a hint that the dashboard is near the per-venue refresh budget. *(source: contracts/satellite/reporting.yaml#createDashboard / R094)*
- **standard versus custom**: Seeded command-centre dashboards are rows like any other (a command centre is a saved dashboard). Mark them "Standard"; a venue copies and changes the copy. *(source: ADR-0041 / DI-697)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Open**: Reads the dashboard with tile data, then records one view in the background; a failed view record never blocks rendering. *(source: contracts/satellite/reporting.yaml#recordDashboardView)*
- **Duplicate**: No clone operation exists. The client reads the dashboard and creates a new one named "Copy of ..." with new tile ids, Private, owned by the caller. A tile id that belongs to another dashboard is refused. *(source: contracts/satellite/reporting.yaml#updateDashboard / MATRIX 7.1.46)*
- **Archive**: Archives, never deletes. Refused while the dashboard is shared, because it is on other people's screens: disable the action on a shared row with the reason "Stop sharing it first". *(source: contracts/satellite/reporting.yaml#deleteDashboard)*

**Data it reads**: `listDashboards` (onLoad, The library); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*; carries `dashboardId`, `reportId`
- → `ANL-030` Dashboard Preview, Validation & Health: *Dashboard Preview, Validation & Health*; carries `dashboardId`
- → `ANL-022` Dashboard Creation Wizard: *Dashboard Creation Wizard*
- → `ANL-023` Drag-and-Drop Dashboard Canvas: *Drag-and-Drop Dashboard Canvas*; carries `dashboardId`
- → `ANL-024` Widget & Visualization Library: *Widget & Visualization Library*
- → `ANL-025` KPI Builder: *KPI Builder*
- → `ANL-026` Targets, Thresholds & KPI Status Rules: *Targets, Thresholds & KPI Status Rules*
- → `ANL-027` Data & Filter Configuration: *Data & Filter Configuration*; carries `dashboardId`
- → `ANL-028` Drill-Down & Interaction Designer: *Drill-Down & Interaction Designer*; carries `dashboardId`
- → `ANL-029` Dashboard Access, Publishing & Versioning: *Dashboard Access, Publishing & Versioning*; carries `dashboardId`
- → `ANL-072` Finance Dashboard: *Finance Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The record list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the record untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No record yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the record are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094); 409 The caller is not entitled to the dashboard's module — the tenant has not licensed it, or the principal holds no permission in it.; 422 A tile's report lacks the column encodings its visualisation needs (problem type `tile-encoding-missing`, CHG-FIN-007; the … |

#### Edge cases to draw

- **A tenant-wide shared dashboard opened by a venue manager**: Every tile shows only that manager's venue; the header says "Showing Aquaventure Waterpark only". The scope comes from permissions, not from a filter the viewer could widen. *(source: DI-061 / contracts/satellite/reporting.yaml#CreateDashboardRequest)*
- **Login entitled to no analytics module**: The no-access state names the missing permission in words ("You need access to venue reports"); never an empty table. *(source: DI-387 / contracts/satellite/reporting.yaml#listDashboards)*

#### Consistency with other screens

- Match `ANL-023`: Open and New lead to the lead's canvas; the same Shared/Private and Standard badges appear in its header.
- Match `ANL-029`: Status and version shown here must be the lifecycle ANL-029 defines once it has a contract.
- Match `ANL-053`: AI-generated dashboards are created through the same create operation; nothing on the record says so (see corrections).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rows:
- name: Daily Sales & Channel
  area: Sales
  owner: Rahul Menon
  venue: Aquaventure Waterpark
  sharing: Shared
  created: 14 Sep 2026
  load: Medium
- name: Finance & Reconciliation
  area: Finance
  owner: Fatima Al Mansoori
  venue: All my venues
  sharing: Shared
  created: 02 Sep 2026
  load: Low
- name: Operations Control Room
  area: Operations
  owner: Standard
  venue: All my venues
  sharing: Shared
  created: 08 Sep 2026
  load: High
- name: Motiongate peak hours (draft)
  area: Operations
  owner: Omar Haddad
  venue: Dubai Parks - Motiongate
  sharing: Private
  created: 29 Sep 2026
  load: Low
```

#### Permissions

- `listDashboards` → `REPORT_VIEW_VENUE` (operate) · staff
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `createDashboard` → `REPORT_MANAGE` (configure) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.79 | System shall monitor operational service levels. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 1.3.27 | System shall provide real-time dashboards showing attendance, check-ins, occupancy, sales, capacity utilization and operational KPIs. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 1.3.28 | System shall provide event performance analytics including attendance, revenue, conversion rates, capacity utilization and customer engagement. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 8.7.1 | System shall provide executive dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.2 | System shall provide operational dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.3 | System shall provide financial dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.4 | System shall provide sales dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.5 | System shall provide marketing dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.6 | System shall provide ticketing dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.7 | System shall provide access control dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.8 | System shall provide membership dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.9 | System shall provide loyalty dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Business can build additional dashboards (e.g. separate finance, sales, operations dashboards) with role-based access so only the relevant team can view a given dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-702)*
- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-021` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-021`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 1: Opens Dashboard Library → Provide a centralized catalogue for all standard, custom, AI-generated and embedded TICVAI dashboards.
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F176 branch at step 1 (expected): when Nothing has been set up on Dashboard Library yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F176 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (62 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-030`, `ANL-022`, `ANL-023`, `ANL-024`, `ANL-025`, `ANL-026`, `ANL-027`, `ANL-028`, `ANL-029`, `ANL-072`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-022` Dashboard Creation Wizard

**Guide users through creation of a new dashboard.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-022 |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Select; Select one or multiple domains) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/dashboard-creation-wizard-anl-022` |

**Known gaps.** **Dashboard Creation Wizard declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** A short wizard (Basics, Scope, Data areas, Starting point) that ends in the canvas. Nothing is saved until Finish, because a dashboard cannot be created without at least one tile: the Starting point step supplies the first tiles (a standard template, or "Blank - one KPI card"). The thing to get right is what the wizard must not ask: the tenant, a default currency and an owner are not choices.

**Known correction pending (do not draw the wrong version)**

- **The gap says the wizard declares no write operation** Why: It declares createDashboard. The gap text is stale. *(source: screens/P16-venue-analytics.yaml#ANL-022 / contracts/satellite/reporting.yaml#createDashboard; Finance, Ledger & Tax · Reporting & Analytics)*
- **Tenant, Organization and Default Currency fields** Why: The tenant is never user-selectable; records and display are in the venue's base currency, so a dashboard-level default currency implies a conversion the platform does not do. *(source: DI-211; Finance, Ledger & Tax · Reporting & Analytics)*
- **The label "Queue - Accreditation" is a fragment of the pack's domain list collapsed into one select, and step titles are drawn as text fields** Why: Step 3 is a multi-select of data areas; step titles are headings, not inputs. *(source: screens/P16-venue-analytics.yaml#ANL-022; Finance, Ledger & Tax · Reporting & Analytics)*
- **Category, Tags and Language have no field on the dashboard** Why: Only name, module, description, venueId and isShared are stored; these three cannot be saved. *(source: contracts/satellite/reporting.yaml#CreateDashboardRequest; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Does a dashboard carry an Arabic name and description, or one name shown in both languages?** → Drawn default accepted: One name field; flag the Arabic layout of the wizard RTL but do not draw a second name field. *(decided by Chinmay, 2026-10-02; DEC-327 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Dashboard Name | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Category | select field | — | — | — | — | — | — |
| Business Domain | select field | — | — | — | — | — | — |
| Dashboard Owner | select field | — | — | — | — | — | — |
| Tags | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Default Currency | select field | — | — | — | — | — | — |
| Step 2 — Scope | text field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Organization | select field | — | — | — | — | — | — |
| Site(s) | select field | — | — | — | — | — | — |
| Venue(s) | select field | — | — | — | — | — | — |
| Attraction(s) | select field | — | — | — | — | — | — |
| Business Unit(s) | select field | — | — | — | — | — | — |
| Step 3 — Data Domains | text field | — | — | — | — | — | — |
| Queue • Accreditation | select field | — | — | — | — | — | — |
| Step 4 — Template | text field | — | — | — | — | — | — |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **module (shown as "Business area")**: Required. Only modules the tenant licenses and the login holds a permission in; "General" for a dashboard that belongs to no optional module. A module outside entitlement is refused by the server, so do not list it. *(source: contracts/satellite/reporting.yaml#CreateDashboardRequest)*
- **name, description**: Name required, up to 200 characters; description up to 1,000. Name must be unique in the caller's library for usability (not enforced by the contract; warn, do not block). *(source: contracts/satellite/reporting.yaml#CreateDashboardRequest)*
- **venueId (shown as "Venue")**: Optional, one venue. Default "All venues I am allowed to see": each viewer then sees their own scope and never beyond it. The pack's multi-select Site(s), Attraction(s) and Business Unit(s) have no field; draw one venue picker. *(source: contracts/satellite/reporting.yaml#CreateDashboardRequest / DI-061)*
- **Tenant (pack field)**: Remove. The tenant is applied at the security level and is never a user-editable choice; the platform never trusts a client-supplied tenant. *(source: MATRIX 6.1.78)*
- **Owner (pack field)**: Not a choice. The creator is the owner; show "Owner - you" read-only. *(source: contracts/satellite/reporting.yaml#Dashboard)*
- **isShared (shown as "Share with my team")**: Off by default; a private dashboard is visible to its owner only. *(source: contracts/satellite/reporting.yaml#CreateDashboardRequest)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Starting point step**: Offer the client's standard boards as templates: Executive Performance, Sales & Channel, Admissions & Capacity, Product & Pricing, Customer & Membership, Finance & Reconciliation, Operations Control Room, B2B / OTA Partner, F&B / Retail. Each card states its tile count and how many of its tiles use a mark that cannot bind data yet (combo, waterfall, matrix, funnel, scatter ...), so the user is not surprised in the canvas. *(source: MATRIX 8.7.1 / MATRIX 8.7.34 / MATRIX 6.1.41 / MATRIX 8.7.21 / contracts/satellite/reporting.yaml#DashboardTile)*
- **Refresh load summary on the last step**: Show "Refreshes per minute - 18 of 24 allowed" computed as the sum over tiles of 60 / refresh seconds; tiles refresh no faster than every 30 seconds. *(source: contracts/satellite/reporting.yaml#createDashboard / contracts/satellite/reporting.yaml#DashboardTile / R094)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Finish**: Creates the dashboard and opens it in the canvas. Over the refresh budget is refused with the budget named; a module outside entitlement is refused; both keep the wizard filled in. *(source: contracts/satellite/reporting.yaml#createDashboard)*
- **Cancel**: Discards everything; nothing was saved. *(source: contracts/satellite/reporting.yaml#createDashboard)*

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The creation wizard configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the creation wizard untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No creation wizard configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094); 409 The caller is not entitled to the dashboard's module — the tenant has not licensed it, or the principal holds no permission in it.; 422 A tile's report lacks the column encodings its visualisation needs (problem type `tile-encoding-missing`, CHG-FIN-007; the … |

#### Edge cases to draw

- **A template with 13 tiles at 30-second refresh (26 per minute)**: Finish is refused with the venue budget (24 per minute proposed). Offer "Slow the live tiles to 60 seconds" rather than a bare error. *(source: R094 / contracts/satellite/reporting.yaml#createDashboard)*
- **A template with more than 24 tiles**: Not possible; a dashboard holds at most 24 tiles, so no template may exceed it. *(source: contracts/satellite/reporting.yaml#CreateDashboardRequest)*

#### Consistency with other screens

- Match `ANL-023`: Finish lands in the lead's canvas with the new dashboard id.
- Match `ANL-032`: Same step pattern and wording as the report wizard (Basics, Scope, Data, Starting point).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
basics:
  name: Waterpark daily pulse
  area: Operations
  description: Admissions, capacity and F&B by hour for the duty manager
  share: 'Off'
scope:
  venue: Aquaventure Waterpark
startingPoint:
  template: Admissions & Capacity
  tiles: 9
  notYetAvailable: 0
  refreshesPerMinute: 14 of 24
```

#### Permissions

- `createDashboard` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.79 | System shall monitor operational service levels. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 1.3.27 | System shall provide real-time dashboards showing attendance, check-ins, occupancy, sales, capacity utilization and operational KPIs. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 1.3.28 | System shall provide event performance analytics including attendance, revenue, conversion rates, capacity utilization and customer engagement. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 8.7.1 | System shall provide executive dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.2 | System shall provide operational dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.3 | System shall provide financial dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.4 | System shall provide sales dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.5 | System shall provide marketing dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.6 | System shall provide ticketing dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.7 | System shall provide access control dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.8 | System shall provide membership dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.9 | System shall provide loyalty dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-022` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-022`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 2: Works in Dashboard Creation Wizard → Guide users through creation of a new dashboard.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-022?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-023` Drag-and-Drop Dashboard Canvas

**Provide the main visual workspace for dashboard construction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 1 · needs the `analytics` module |
| Block | Block A · ticket #28744 (APP-SETUP-ANL-023) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): A canvas edited and saved as a whole (`updateDashboard` replaces the tiles), drawn 2 October 2026 from the client's dashboard specification (MATRIX 8.7.12: grid, gallery, data pane, field wells … |
| Offline | online only |
| Opens with | `dashboardId` (navigation), `reportId` (navigation) |
| Route | `/analytics/drag-and-drop-dashboard-canvas-anl-023` |

**What the spec says about it.** **The nine new marks bind** (decided 2 October 2026, Chinmay; CHG-FIN-007). The canvas offers all twenty marks of `DashboardTile.visualisation` and, for each, field wells filled from the report's columns (`ReportColumn.role`, `encoding`, `axis`, `seriesType`, `hierarchyLevel`, `unitLabel`): combo (x, bars and lines, primary and secondary axis with units), matrix (rows, columns, values, with drill levels), funnel (ordered stages, value), waterfall (ordered steps of a measure set, total last), treemap (nested categories, size, colour), scatter (x, y, label, size, colour), map (venue, zone or map point, value), ribbon (period, series, value) and decomposition tree (value, levels). A tile whose report lacks a required well cannot be saved (422 `tile-encoding-missing`). At most 24 tiles; every tile shows its as-of time and a stale warning past its refresh (BOARDREQ MOM-2713/2714).

**Known gaps.** **No draft, preview-publish or rollback for a dashboard** (design-notes correction ANL-023, MATRIX 7.1.46). Every save overwrites the live dashboard; the contract has no dashboard version or publish …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The canvas where a dashboard is laid out: tiles on a grid, each bound to a report and drawn as one visual. The one thing to get right: the canvas may only offer what can actually be drawn and bound, and saving replaces the whole dashboard, so the designer must see what will be removed.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- No undo or redo, and no draft or version of a dashboard. (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): The layout has only Save, Cancel and an unlabelled detail panel; the gaps say the pack gives nothing to draw. (CHG-SOT-010).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which visuals ship bindable in the first release?** → Build all chart types, including the nine complex ones. *(decided by Chinmay, 2026-10-02; DEC-080 / CHG-FIN-007 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Find a report | search field | — | — | — | — | Sends `?search=`; the data pane lists the reports a tile may bind, by category. | `listReports` |
| Tile title | text field | optional | — | — | — | — | `DashboardTile.title` |
| Refresh every (seconds) | number field (seconds) | optional | — | min 30 | — | Minimum 30. | `DashboardTile.refreshSeconds` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | select | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | `listReports` ?category |
| Search | text field | — | — | `listReports` ?search |

**Form: Save dashboard** (confirmDialog, opened by *Save dashboard*; *Save dashboard* calls `updateDashboard`, *Keep editing* sends nothing)

**Names what the save removes**, because the tiles are replaced as a whole ("Save and remove 2 tiles: Refunds by channel, Queue time"). Dismissing keeps editing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `updateDashboard` body |
| Module `module` | select | required | — | Core · Ticketing · Access · Fnb · Retail · Inventory · Seating · Membership · Marketing · Resources · Queue · Transport … | — | Which module this dashboard belongs to, and therefore who may see it. Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it … | `updateDashboard` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `updateDashboard` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. | `updateDashboard` body |
| Is shared `isShared` | toggle | optional | off | — | — | — | `updateDashboard` body |
| Tiles `tiles` | repeatable rows | required | — | at least 1; at most 24 | — | — | `updateDashboard` body |
| ID `tiles[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `updateDashboard` body |
| Title `tiles[].title` | text field | optional | — | — | — | — | `updateDashboard` body |
| Report `tiles[].reportId` | picker: choose a report | required | — | — | shows names, sends the id | — | `updateDashboard` body |
| Visualisation `tiles[].visualisation` | select | required | — | Number · Line · Area · Bar · Stacked bar · Stacked bar100 · Combo · Pie · Donut · Table · Matrix · Gauge … | — | Extended 22 September from eight marks to twenty against `Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`, which names eighteen components and marks every one … | `updateDashboard` body |
| Parameters `tiles[].parameters` | key and value settings | optional | — | — | — | Open on purpose, and not yet specified. Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as `RunReportRequest.parameters`) and its display settings — … | `updateDashboard` body |
| Refresh seconds `tiles[].refreshSeconds` | number field (seconds) | optional | — | min 30 | — | Minimum thirty seconds. A tile refreshing every second is a load problem wearing a convenience costume. | `updateDashboard` body |
| Position `tiles[].position` | group | required | — | — | — | — | `updateDashboard` body |
| Row `tiles[].position.row` | number field | required | — | — | — | — | `updateDashboard` body |
| Column `tiles[].position.column` | number field | required | — | — | — | — | `updateDashboard` body |
| Width `tiles[].position.width` | number field | required | — | — | — | — | `updateDashboard` body |
| Height `tiles[].position.height` | number field | required | — | — | — | — | `updateDashboard` body |

Errors to draw in the form: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094), as on `createDashboard` …; 409 Moving a dashboard to a module the caller is not entitled to. The same guard as `createDashboard` — without it, an update would be the way round the create …; 422 A tile's report lacks the column encodings its visualisation needs (problem type `tile-encoding-missing`, CHG-FIN-007), as `createDashboard`.

**Form: Archive dashboard** (confirmDialog, opened by *Archive dashboard*; *Archive dashboard* calls `deleteDashboard`, *Cancel* sends nothing)

Names the dashboard and its tile count; archived dashboards leave the library unless asked for. Dismissing sends nothing.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 409 The dashboard is shared. Un-share it first.

**Form: Save dashboard** (modal, opened by *Save dashboard*; *Create dashboard* calls `createDashboard`, *Keep editing* sends nothing)

**The first Save of a new dashboard** (decided by Chinmay, 3 October 2026 (CHG-SPF-011)): names it and creates it with `createDashboard`, tiles and all; every later Save goes straight to `updateDashboard`. The refresh budget is checked here too. Dismissing sends nothing; the canvas keeps its tiles.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createDashboard` body |
| Module `module` | select | required | — | Core · Ticketing · Access · Fnb · Retail · Inventory · Seating · Membership · Marketing · Resources · Queue · Transport … | — | Which module this dashboard belongs to, and therefore who may see it. Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it … | `createDashboard` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createDashboard` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. | `createDashboard` body |
| Is shared `isShared` | toggle | optional | off | — | — | — | `createDashboard` body |
| Tiles `tiles` | repeatable rows | required | — | at least 1; at most 24 | — | — | `createDashboard` body |
| ID `tiles[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createDashboard` body |
| Title `tiles[].title` | text field | optional | — | — | — | — | `createDashboard` body |
| Report `tiles[].reportId` | picker: choose a report | required | — | — | shows names, sends the id | — | `createDashboard` body |
| Visualisation `tiles[].visualisation` | select | required | — | Number · Line · Area · Bar · Stacked bar · Stacked bar100 · Combo · Pie · Donut · Table · Matrix · Gauge … | — | Extended 22 September from eight marks to twenty against `Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`, which names eighteen components and marks every one … | `createDashboard` body |
| Parameters `tiles[].parameters` | key and value settings | optional | — | — | — | Open on purpose, and not yet specified. Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as `RunReportRequest.parameters`) and its display settings — … | `createDashboard` body |
| Refresh seconds `tiles[].refreshSeconds` | number field (seconds) | optional | — | min 30 | — | Minimum thirty seconds. A tile refreshing every second is a load problem wearing a convenience costume. | `createDashboard` body |
| Position `tiles[].position` | group | required | — | — | — | — | `createDashboard` body |
| Row `tiles[].position.row` | number field | required | — | — | — | — | `createDashboard` body |
| Column `tiles[].position.column` | number field | required | — | — | — | — | `createDashboard` body |
| Width `tiles[].position.width` | number field | required | — | — | — | — | `createDashboard` body |
| Height `tiles[].position.height` | number field | required | — | — | — | — | `createDashboard` body |

Errors to draw in the form: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094); 409 The caller is not entitled to the dashboard's module — the tenant has not licensed it, or the principal holds no permission in it.; 422 A tile's report lacks the column encodings its visualisation needs (problem type `tile-encoding-missing`, CHG-FIN-007; the rule is on …

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Grid and tile position**: A 12-column grid (the client's spec; not yet fixed in the contract); tiles snap to whole columns and rows; position is row, column, width, height. At most 24 tiles per dashboard. *(source: MATRIX 8.7.12 / contracts/satellite/reporting.yaml#/components/schemas/CreateDashboardRequest)*
- **Visual per tile**: One of the contracted marks (number, line, area, bar, stacked bar, 100% stacked bar, combo, pie, donut, table, matrix, gauge, heatmap, funnel, waterfall, treemap, scatter, map, ribbon, decomposition tree). Slicers, narrative text and cohorts are not visuals. A gauge only where the KPI has a target or range. *(source: contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / MATRIX 8.7.21)*
- **Refresh**: Per tile, 30 seconds minimum; the dashboard shows its combined load (low, medium, high). *(source: contracts/satellite/reporting.yaml#/components/schemas/DashboardTile / contracts/satellite/reporting.yaml#/components/schemas/Dashboard)*
- **Module and audience**: The module the dashboard belongs to decides who may see it (required; "Core" when it belongs to none); shared or personal; optionally one venue. *(source: contracts/satellite/reporting.yaml#/components/schemas/CreateDashboardRequest / DI-702)*

#### Outputs: what the screen shows and produces

**Shown**

**Visuals** (card list): **All twenty marks of `DashboardTile.visualisation`, the nine complex ones included** (decided 2 October 2026, Chinmay: "Build all chart types, including the nine complex ones"; DEC-080, CHG-FIN-007): number, line, area, bar, stackedBar, stackedBar100, combo, pie, donut, table, matrix, gauge, heatmap, funnel, waterfall, treemap, scatter, map, ribbon and decompositionTree. Each card names the …

**Reports and their columns** (tree nav, from `getReport`): Each report opens to its columns with `role`, `encoding`, `axis`, `seriesType`, `hierarchyLevel` and `unitLabel` (CHG-FIN-007); a column is dragged into a well.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Data source | chip: Orders, Order lines, Payments, Refunds, Shifts, Scan events… | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over … |
| Columns | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Field | text | — |
| Label | text | — |
| Aggregation | chip: None, Count, Count distinct, Sum, Average, Min… | — |
| Sort order | 1,234 | — |
| Sort direction | chip: Asc, Desc | — |
| Format | text | — |
| Role | chip: Dimension, Measure | What the column is to a chart (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a … |
| Encoding | chip: Category, X, Y, Series, Value, Size… | Which field well the column fills (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. |
| Axis | chip: Primary, Secondary | For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007). |
| Series type | chip: Bar, Line, Area | For a measure on a `combo`, how that series is drawn (CHG-FIN-007). |
| Hierarchy level | 1,234 | For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. |
| Unit label | text | The unit an axis states, for example "AED" or "Admissions". Required on a secondary axis (CHG-FIN-007). |
| Filters | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |

**Canvas** (detail panel, from `getDashboard`): A grid; each tile sits at `position` (row, column, width, height). **At most 24 tiles.** Every tile renders its mark with live data, shows its as-of time and a stale warning past its refresh (BOARDREQ MOM-2713/2714).

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Module | chip: Core, Ticketing, Access, Fnb, Retail, Inventory… | Which module this dashboard belongs to, and therefore who may see it. Added 22 September for the command centre: one shell that shows each … |
| Venue | the name it points at, never the id | Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. |
| Is shared | yes / no (icon or chip) | — |
| Tiles | list or chips (count when long) | — |

**Field wells** (detail panel, from `getReport`): The wells of the selected tile's mark, filled from its report's columns. A required well left empty is named in red, and Save is refused for it rather than drawing an empty chart.

| Shows | Format | Notes |
|---|---|---|
| Label | text | — |
| Role | chip: Dimension, Measure | What the column is to a chart (decided 2 October 2026, Chinmay; CHG-FIN-007). A `dimension` groups (date, venue, channel, product); a … |
| Encoding | chip: Category, X, Y, Series, Value, Size… | Which field well the column fills (CHG-FIN-007), the binding the twenty marks of `DashboardTile.visualisation` need. |
| Axis | chip: Primary, Secondary | For a measure on a `combo`, the axis it is drawn against. A secondary axis needs its own `unitLabel` (CHG-FIN-007). |
| Series type | chip: Bar, Line, Area | For a measure on a `combo`, how that series is drawn (CHG-FIN-007). |
| Hierarchy level | 1,234 | For `matrix` rows and columns, `treemap` nesting and `decompositionTree` levels, the depth of this dimension, 1 outermost. |
| Unit label | text | The unit an axis states, for example "AED" or "Admissions". Required on a secondary axis (CHG-FIN-007). |

**Formatting** (detail panel, from `updateDashboard`): The tile's run parameters and display settings (for `number`: comparison, variance, sparkline and status icon).

| Shows | Format | Notes |
|---|---|---|
| Parameters | grouped details | Open on purpose, and not yet specified. Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save dashboard (primary button) | `updateDashboard` PUT `/dashboards/{dashboardId}` | CreateDashboardRequest | Dashboard | 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094), as on `createDashboard` …; 409 Moving a dashboard to a module the caller is not … | opens confirmDialog first |
| Undo (icon button) | navigation or local | — | — | — | — |
| Redo (icon button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Archive dashboard (destructive button) | `deleteDashboard` DELETE `/dashboards/{dashboardId}` | — | — | 409 The dashboard is shared. Un-share it first. | opens confirmDialog first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Tile preview**: Live data in edit mode with loading, empty, error and stale states per tile; one failing tile never blanks the canvas. *(source: MATRIX 6.1.78)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save**: Replaces the dashboard with what is on the canvas; tiles removed since opening are listed in the confirmation ("3 tiles will be removed"). *(source: contracts/satellite/reporting.yaml#updateDashboard)*
- **Archive**: Hides it from the library; configuration is kept and can be restored by an administrator. *(source: contracts/satellite/reporting.yaml#/components/schemas/Dashboard)*

**Data it reads**: `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …); `listReports` (onLoad, The reports a tile may bind, for the data pane)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dashboard and its tiles. |
| Error (`?state=error`) | Could not load. Names which read failed (the dashboard or a report) and leaves the canvas as it was. |
| Empty, first run (`?state=emptyFirstRun`) | A new dashboard with no tiles yet. The gallery is open and says "Drag a visual onto the grid"; nothing is created until Save dashboard. |
| Empty, no results (`?state=emptyNoResults`) | The report search matched nothing. Names the search and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listReports` requires to show this screen, and names that permission. A caller without `REPORT_MANAGE` sees the dashboard read-only: Save (`createDashboard`, `updateDashboard`) and Archive (`deleteDashboard`) are disabled and name that permission (decided by Chinmay, 3 October 2026 (CHG-SPF-011)). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094); 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094), as on `createDashboard` …; 409 Moving a dashboard to a module the caller is not entitled to. The same guard as … |

#### Edge cases to draw

- **The chosen visual needs more than one dimension and one measure (combo, scatter, map, matrix…)**: Not bindable yet: report columns carry no axis, series, size or colour role. Show these visuals in the gallery as unavailable with that reason until the field-well model exists. *(source: contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*
- **Mobile layout**: Tiles stack in reading order at narrow widths; a CEO opening it on a phone sees the KPIs first. *(source: DI-696)*

#### Consistency with other screens

- Match `ANL-024`: The visual gallery and its availability come from the widget library.
- Match `ANL-029`: Publishing and approval happen there, not on the canvas.
- Match `ANL-025`: KPI tiles reference a library KPI; the formula is never edited on a tile.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
dashboard: Finance – Daily close · module Finance · shared · Aquaventure Waterpark
tiles:
- Takings today (number) · row 1, col 1, 3×2 · refresh 60 s
- Takings by hour (bar) · row 1, col 4, 6×4
- Tender mix (donut) · row 1, col 10, 3×4
- Unresolved settlement exceptions (table) · row 5, col 1, 12×4
```

#### Permissions

- `updateDashboard` → `REPORT_MANAGE` (configure) · staff
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `deleteDashboard` → `REPORT_MANAGE` (configure) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff
- `listReports` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `getReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `createDashboard` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listReports` requires to show this screen, and names that permission. A caller without `REPORT_MANAGE` sees the dashboard read-only: Save (`createDashboard`, `updateDashboard`) and Archive (`deleteDashboard`) are disabled and name that permission (decided by Chinmay, 3 October 2026 (CHG-SPF-011)).

Screen guard: `REPORT_MANAGE`

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.79 | System shall monitor operational service levels. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 1.3.27 | System shall provide real-time dashboards showing attendance, check-ins, occupancy, sales, capacity utilization and operational KPIs. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 1.3.28 | System shall provide event performance analytics including attendance, revenue, conversion rates, capacity utilization and customer engagement. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 8.7.1 | System shall provide executive dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.2 | System shall provide operational dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.3 | System shall provide financial dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.4 | System shall provide sales dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.5 | System shall provide marketing dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.6 | System shall provide ticketing dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.7 | System shall provide access control dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.8 | System shall provide membership dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.9 | System shall provide loyalty dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam shared the itemised dashboard-component document (chart types, drill-down tool, heat map, etc.) with a suggested reference architecture - explicitly a suggestion Softlabs may adopt, adapt or replace. *(agreed · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-750)*
- Dashboard creation is drag-and-drop against predefined data sets (revenue, sales quantity, sales channel, department, etc.); the user picks a visual format (bar chart, pie chart, etc.) without writing queries. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-703)*
- The platform ships a standard set of default dashboards out of the box, plus the ability for the business to design additional custom dashboards without SQL or programming knowledge. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-697)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-023` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-023`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 4: Works in Drag-and-Drop Dashboard Canvas → Provide the main visual workspace for dashboard construction.

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-023?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save dashboard, Undo, Redo, Cancel, Archive dashboard.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-024` Widget & Visualization Library

**Provide reusable visual components for dashboard construction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-024 |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§KPI Components) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/widget-visualization-library-anl-024` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The bounded catalogue of visuals the canvas drags from, as the client asked: an itemised list, like a bounded Power BI or Zoho canvas. Its contents are the contract's twenty marks, not a server collection. The thing to get right: nine of the twenty cannot bind data yet (no encoding role on report columns), and three things the client listed (slicer, narrative, cohort) are deliberately not marks.

**Known correction pending (do not draw the wrong version)**

- **The empty state "carries the create action"** Why: Nobody creates visual types; the list is the contract's fixed set. An empty library is impossible; drop the create action. *(source: screens/P16-venue-analytics.yaml#ANL-024 / contracts/satellite/reporting.yaml#DashboardTile; Finance, Ledger & Tax · Reporting & Analytics)*
- **The six "columns" (KPI Card ... Progress Indicator) are not marks and none is a column** Why: They are presets of number and gauge; the twenty marks are the catalogue. *(source: contracts/satellite/reporting.yaml#DashboardTile; Finance, Ledger & Tax · Reporting & Analytics)*
- **handoff/board-dashboard-requirements.md still says eight marks** Why: The enum went from eight to twenty on 22 September; a designer reading that summary would draw too few. *(source: contracts/satellite/reporting.yaml#DashboardTile; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which wells (Axis, Legend, Values, Small multiples, Tooltips, Filters) does each mark accept, so the nine unavailable marks can bind?** → Drawn default accepted: Show them as "Not yet available"; do not draw well layouts for them. *(decided by Chinmay, 2026-10-02; DEC-328 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Default category limit for pie and donut, and is the remainder grouped as Other?** → Drawn default accepted: Six slices plus Other. *(decided by Chinmay, 2026-10-02; DEC-329 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every widget visualization** (data table)

| Shows | Format | Notes |
|---|---|---|
| KPI card | text | not in the schema: `KPI Card` |
| Target card | text | not in the schema: `Target Card` |
| Variance card | text | not in the schema: `Variance Card` |
| Scorecard | text | not in the schema: `Scorecard` |
| Gauge | text | not in the schema: `Gauge` |
| Progress indicator | text | not in the schema: `Progress Indicator` |

**The selected widget visualization** (detail panel): The pack groups this record's detail under its own headings: “Chart Components”, “Operational Components”.

| Shows | Format | Notes |
|---|---|---|
| KPI card | text | not in the schema: `KPI Card` |
| Target card | text | not in the schema: `Target Card` |
| Variance card | text | not in the schema: `Variance Card` |
| Scorecard | text | not in the schema: `Scorecard` |
| Gauge | text | not in the schema: `Gauge` |
| Progress indicator | text | not in the schema: `Progress Indicator` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **gallery groups**: Cards and status (KPI card, gauge); Compare (bar, stacked bar, 100% stacked bar); Trend (line, area, combo); Part of whole (pie, donut, treemap, waterfall); Detail (table, matrix); Flow and spread (funnel, heatmap, scatter, map, ribbon, decomposition tree). Searchable, with a preview per card. *(source: contracts/satellite/reporting.yaml#DashboardTile / DI-707)*
- **pack card names (KPI Card, Target Card, Variance Card, Scorecard, Progress Indicator)**: These are presets of the KPI card (comparison, variance, sparkline and status icon are its settings) and of the gauge; show them as variants inside the KPI card and gauge, not as six marks. *(source: contracts/satellite/reporting.yaml#DashboardTile / MATRIX 8.7.21 / MATRIX 8.7.25)*
- **per-card guidance**: "Best for" and "Needs" lines from the client's selection guide, e.g. Line - change over time; needs a date or category axis and at least one number. Gauge - only when the KPI has a target or range; otherwise the KPI card is the default. Pie - few categories; prefer bar for many. *(source: MATRIX 8.7.21)*
- **availability state**: Combo, matrix, funnel, waterfall, treemap, scatter, map, ribbon and decomposition tree show a "Not yet available" ribbon and cannot be dragged, with the reason in a tooltip ("This visual needs axis and series roles the data model does not have yet"). Area, donut and 100% stacked bar bind as their parent marks and are available. *(source: contracts/satellite/reporting.yaml#DashboardTile / MATRIX 8.7.12)*
- **refused components**: No slicer card: a filter on the canvas is a report parameter, offered from the filter pane. No narrative card: written insights come from the AI insight panel. No cohort card: use matrix or heatmap over a cohort dimension. Searching "slicer" or "cohort" shows that pointer instead of no results. *(source: contracts/satellite/reporting.yaml#DashboardTile)*

**Data it reads**: `getSemanticModel` (onLoad, What a widget can be bound to)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The widget visualization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the widget visualization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No widget visualization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the widget visualization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **User looks for a way to add a custom visual**: None exists; custom visuals (sandboxed, signed, allow-listed) are not in scope, so draw no import button. *(source: MATRIX 6.1.78)*
- **User drags a pie onto a field with 14 categories**: The pie renders the largest categories and groups the rest as "Other" (limit to be decided), with a hint suggesting a bar chart. *(source: MATRIX 8.7.1)*

#### Consistency with other screens

- Match `ANL-023`: The canvas's visual gallery is this list, same groups, same availability states and same names.
- Match `ANL-028`: Visuals that support drill (bar, line, matrix, treemap, decomposition tree) say so on their card.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
cards:
- name: KPI card
  group: Cards and status
  bestFor: Current value with change
  example: Net revenue AED 412,860.50, up 6.2% vs last Tuesday
  state: Available
- name: Gauge
  group: Cards and status
  bestFor: Value against a target or band
  example: Capacity 86% - Warning
  state: Available
- name: Waterfall
  group: Part of whole
  bestFor: Gross sales to net revenue bridge
  state: Not yet available
```

#### Permissions

- `getSemanticModel` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam shared the itemised dashboard-component document (chart types, drill-down tool, heat map, etc.) with a suggested reference architecture - explicitly a suggestion Softlabs may adopt, adapt or replace. *(agreed · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-750)*
- Dashboard creation is drag-and-drop against predefined data sets (revenue, sales quantity, sales channel, department, etc.); the user picks a visual format (bar chart, pie chart, etc.) without writing queries. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-703)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-024` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-024`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 6: Works in Widget & Visualization Library → Provide reusable visual components for dashboard construction.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-024?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-025` KPI Builder

**Allow authorized business users to create standardized enterprise KPIs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 1 · needs the `analytics` module |
| Block | Block A · ticket #28745 (APP-SETUP-ANL-025) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Define whether) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/kpi-builder-anl-025` |

**Known gaps.** **No update or retire operation for a KPI** (design-notes correction ANL-025). `createKpi` writes one; nothing corrects or retires it, so a mistake cannot be put right. Logged as a contract gap 2 …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Where an authorised business user defines a company-wide KPI once, so "revenue" means the same on every dashboard. The one thing to get right: the formula is written against the business catalogue, not tables, and the direction (higher or lower is better) is a single choice that decides every status colour.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The gap says the screen declares no write operation. (CHG-SOT-016)

**Fixed on main** (the package already carries these; draw what it says): "Higher = Better" and "Lower = Better" are two fields, and "Revenue ↑", "Conversion ↑", "Refund Rate ↓", "Gate Rejection Rate ↓", "Queue … (CHG-SOT-012); Currency, decimal precision, measure, aggregation, data source, effective date and status are drawn as KPI fields. (CHG-SOT-012); The catalogue has no finance measures (gross sales, net revenue, refunds, tax). (CHG-FIN-007).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| KPI name | text field | optional | — | — | — | — | `KpiDefinition.name` |
| KPI code | text field | optional | — | — | — | Unique in the tenant; the seeded codes (`takings`, `admissions`, the finance measures) are taken. | `KpiDefinition.code` |
| Description | text area | optional | — | — | — | — | `KpiDefinition.description` |
| Business domain | text field | optional | — | — | — | The semantic model's domains. | `KpiDefinition.domain` |
| Owner | picker: choose an owner (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `KpiDefinition.owner` |
| Formula | text field | optional | — | — | — | **Against the semantic model, not tables.** The measure, the aggregation and the data source are all in the formula; there are no separate fields for them. | `KpiDefinition.formula` |
| Unit | select | optional | — | Currency · Count · Percentage · Duration · Ratio · Score | — | Currency, count, percentage, duration, ratio or score. Currency and decimal places follow the region (AED 2, BHD/KWD/OMR 3), not the KPI. | `KpiDefinition.unit` |
| Higher is better | toggle | optional | on | — | — | One yes/no. Examples, not fields: revenue and conversion up is better; refund rate, gate rejection rate and queue time down is better. | `KpiDefinition.higherIsBetter` |
| Default period | text field | optional | — | — | — | — | `KpiDefinition.defaultPeriod` |
| Active | toggle | optional | on | — | — | The KPI's status: inactive KPIs are kept and not offered on dashboards. | `KpiDefinition.isActive` |

**Sent by *Create KPI*** (`createKpi`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createKpi` body |
| Code `code` | text field | required | — | — | — | `takings` and `admissions` are seeded for every tenant as system KPIs (decided 28 September, audit R283), and the five accreditation KPIs for every tenant with the accreditation … | `createKpi` body |
| Name `name` | text field | required | — | — | — | — | `createKpi` body |
| Description `description` | text area | optional | — | — | — | — | `createKpi` body |
| Domain `domain` | text field | optional | — | — | — | — | `createKpi` body |
| Formula `formula` | text field | optional | — | — | — | Expressed against the semantic model, not against tables. A KPI written in SQL is a KPI that breaks when the warehouse is reshaped. | `createKpi` body |
| Unit `unit` | select | optional | — | Currency · Count · Percentage · Duration · Ratio · Score | — | — | `createKpi` body |
| Higher is better `higherIsBetter` | toggle | optional | on | — | — | Refund rate and revenue both go up. Without this the status colour is a coin toss. | `createKpi` body |
| Default period `defaultPeriod` | text field | optional | — | — | — | — | `createKpi` body |
| Owner `owner` | picker: choose an owner | optional | — | — | shows names, sends the id | — | `createKpi` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `createKpi` body |
| Is active `isActive` | toggle | optional | on | — | — | — | `createKpi` body |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Code and name**: Code unique in the company; the seeded system KPIs (takings, admissions and the accreditation ones) are shown read-only. *(source: contracts/satellite/reporting.yaml#/components/schemas/KpiDefinition / contracts/satellite/reporting.yaml#/components/schemas/ReportingSystemKpi)*
- **Formula**: Built from catalogue measures and fields with a formula editor that validates as you type; no SQL. *(source: contracts/satellite/reporting.yaml#/components/schemas/KpiDefinition / MATRIX 8.7.11 / MATRIX 6.1.78)*
- **Unit**: Currency, Count, Percentage, Duration, Ratio, Score. Currency takes the region's currency and decimals; it is not chosen here. *(source: contracts/satellite/reporting.yaml#/components/schemas/KpiDefinition / ADR-0018)*
- **Direction**: One toggle "Higher is better" (on by default). Refund rate, queue time and gate rejection rate set it off. *(source: contracts/satellite/reporting.yaml#/components/schemas/KpiDefinition)*
- **Domain, default period, owner, active**: Domain from the catalogue's domains; default period (today, week, month); owner is a person. *(source: contracts/satellite/reporting.yaml#/components/schemas/KpiDefinition)*

#### Outputs: what the screen shows and produces

**Shown**

**KPIs already defined** (data table, from `listKpis`): The seeded KPIs first (takings, admissions and the finance measures, CHG-FIN-007), then the tenant's own.

| Shows | Format | Notes |
|---|---|---|
| Code | text | `takings` and `admissions` are seeded for every tenant as system KPIs (decided 28 September, audit R283), and the five accreditation KPIs … |
| Name | text | — |
| Domain | text | — |
| Unit | chip: Currency, Count, Percentage, Duration, Ratio, Score | — |
| Higher is better | yes / no (icon or chip) | Refund rate and revenue both go up. Without this the status colour is a coin toss. |
| Owner | the name it points at, never the id | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create KPI (primary button) | `createKpi` POST `/kpis` | KpiDefinition | KpiDefinition | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Definition card**: Business definition in words beside the formula ("Net revenue = Gross sales − Discounts − Refunds"), its unit, direction and owner; this is what a dashboard tooltip shows. *(source: MATRIX 8.7.21)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Create KPI**: Adds it to the library; targets and bands are set on the targets screen. *(source: contracts/satellite/reporting.yaml#createKpi)*

**Data it reads**: `listKpis` (onLoad, KPIs already defined)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The KPIs already defined. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the form untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Only the seeded KPIs exist (takings, admissions and the finance measures). Offers Create KPI (`createKpi`) for the tenant's first own KPI. |
| Permission denied (`?state=emptyNoAccess`) | Without `REPORT_VIEW_TENANT`, which `listKpis` requires, the screen does not load and this state names that permission. Shown when the caller lacks `REPORT_MANAGE`, which `createKpi` requires; the KPI list stays readable and the form names that permission. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Someone defines "Revenue" without saying gross or net, or with or without tax**: The form requires the definition text to say whether tax and fees are included. *(source: MATRIX 5.12.6)*

#### Consistency with other screens

- Match `ANL-062`: The enterprise KPI library lists what is created here.
- Match `ANL-026`: Targets and warning/critical bands are set there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kpis:
- NET_REVENUE · Net revenue · currency · higher is better · Gross sales − Discounts − Refunds, excluding VAT · owner
  Layla Haddad, Finance
- 'REFUND_RATE · Refund rate · percentage · higher is better: off · Refunds ÷ Gross sales'
- ATV · Average ticket value · currency · Ticket revenue ÷ paid tickets (complimentary excluded)
```

#### Permissions

- `listKpis` → `REPORT_VIEW_TENANT` (operate) · staff
- `createKpi` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Without `REPORT_VIEW_TENANT`, which `listKpis` requires, the screen does not load and this state names that permission. Shown when the caller lacks `REPORT_MANAGE`, which `createKpi` requires; the KPI list stays readable and the form names that permission.

Screen guard: `REPORT_VIEW_TENANT`

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI threshold configuration defines normal/warning/critical bands per metric (e.g. capacity below 80% normal, 80-90% warning, above 95% critical), shown as status on the dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-704)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-025` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-025`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 8: Works in KPI Builder → Allow authorized business users to create standardized enterprise KPIs.

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state.
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-025?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create KPI.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-026` Targets, Thresholds & KPI Status Rules

**Configure how TICVAI determines whether KPI performance is healthy, warning or critical.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-026 |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§For each KPI) and no metric row |
| Offline | online only |
| Opens with | `kpiId` (navigation) |
| Route | `/analytics/targets-thresholds-kpi-status-rules-anl-026` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: If Critical → Generate Alert, Notify responsible user, Create operational task, Trigger AI analysis. Each … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Where a KPI's target and its Warning and Critical bands are set, so every dashboard shows the same status for the same number. A target is per scope (tenant, region, venue) and per period. The thing to get right is direction: a band means "below" for revenue and "above" for refund rate or capacity, taken from the KPI's higher-is-better flag, and the bands must not leave a gap.

**Known correction pending (do not draw the wrong version)**

- **Four Critical actions (generate alert, notify, create task, trigger AI) with no operation** Why: KpiTarget has no action; AlertRule watches a MetricSource value, not a KPI code, so "if Critical then alert" cannot be configured from a KPI. *(source: screens/P16-venue-analytics.yaml#ANL-026 / contracts/satellite/reporting.yaml#AlertRule; Finance, Ledger & Tax · Reporting & Analytics)*
- **KpiTarget.period is an untyped string** Why: Month, quarter and fiscal year (which varies by country) cannot be validated or picked consistently. *(source: contracts/satellite/reporting.yaml#KpiTarget / DI-263; Finance, Ledger & Tax · Reporting & Analytics)*
- **Finance KPIs to target do not exist yet** Why: The metric list has no gross sales, net revenue, refunds, refund rate or average ticket value, and the only seeded money KPI is Takings (payments less refunds). The Net revenue and Refund rate rows in the sample data are tenant-defined KPIs that need a governed formula first. *(source: contracts/satellite/reporting.yaml#MetricSource / contracts/satellite/reporting.yaml#ReportingSystemKpi / MoM 2026-08-12 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What is the period format, and does a fiscal-year target follow the tenant's fiscal calendar?** → Drawn default accepted: Month, quarter and calendar year pickers. *(decided by Chinmay, 2026-10-02; DEC-330 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **target, amberAt, redAt, stretch (shown as Target, Warning at, Critical at, Stretch)**: For a higher-is-better KPI, Critical < Warning < Target <= Stretch; for a lower-is-better KPI the order reverses. Validate the order before saving and say which value is out of place. Bands are contiguous by construction (Warning applies from its value to Critical), which avoids the client example's undefined 90-95% capacity gap. Money targets in the venue's base currency at its scale (AED 2 decimals, BHD 3); percentages to one decimal. *(source: contracts/satellite/reporting.yaml#KpiTarget / contracts/satellite/reporting.yaml#KpiDefinition / DI-704 / MATRIX 8.2.36 / MATRIX 1.1.40 / DI-306)*
- **scopePath (shown as "Applies to")**: A picker of the caller's own scope (organisation, region, venue), never typed. A scope outside the caller's is refused. *(source: contracts/satellite/reporting.yaml#setKpiTargets)*
- **period**: A period picker (month, quarter, year) defaulting to the KPI's default period; January and July differ, so targets are per period. *(source: contracts/satellite/reporting.yaml#setKpiTargets)*

#### Outputs: what the screen shows and produces

**Shown**

**Every targets thresholds kpi** (data table)

| Shows | Format | Notes |
|---|---|---|
| Target | text | not in the schema: `Target` |
| Minimum | text | not in the schema: `Minimum` |
| Maximum | text | not in the schema: `Maximum` |
| Warning threshold | text | not in the schema: `Warning Threshold` |
| Critical threshold | text | not in the schema: `Critical Threshold` |
| Benchmark | text | not in the schema: `Benchmark` |
| Tolerance | text | not in the schema: `Tolerance` |
| Evaluation frequency | text | not in the schema: `Evaluation Frequency` |

**The selected targets thresholds kpi** (detail panel): The pack groups this record's detail under its own headings: “Capacity Utilization”.

| Shows | Format | Notes |
|---|---|---|
| Target | text | not in the schema: `Target` |
| Minimum | text | not in the schema: `Minimum` |
| Maximum | text | not in the schema: `Maximum` |
| Warning threshold | text | not in the schema: `Warning Threshold` |
| Critical threshold | text | not in the schema: `Critical Threshold` |
| Benchmark | text | not in the schema: `Benchmark` |
| Tolerance | text | not in the schema: `Tolerance` |
| Evaluation frequency | text | not in the schema: `Evaluation Frequency` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| If Critical → Generate Alert (primary button) | navigation or local | — | — | — | — |
| Notify responsible user (secondary button) | navigation or local | — | — | — | — |
| Create operational task (secondary button) | navigation or local | — | — | — | — |
| Trigger AI analysis (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **status preview**: Beside the bands, a live strip showing the current value and the status it would get: On track, Warning, Critical, or No target. Status always carries a word and an icon, never colour alone. *(source: contracts/satellite/reporting.yaml#KpiValue)*
- **pack columns Minimum, Maximum, Benchmark, Tolerance, Evaluation frequency**: Not stored; do not draw them as editable. Benchmark comparison lives on ANL-064. *(source: contracts/satellite/reporting.yaml#KpiTarget)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save targets**: Replaces this KPI's whole target set inside the caller's scope: a row the editor leaves out is deleted. The editor therefore always sends every row it shows, and removing a row asks "Remove the October target for Aquaventure Waterpark?". Rows outside the caller's scope are never touched. *(source: contracts/satellite/reporting.yaml#setKpiTargets)*
- **If Critical - alert, notify, create task, ask AI (pack buttons)**: No operation ties a KPI status to an alert. Alerts are separate rules on a closed list of metrics. Draw a link "Set up an alert for this metric" that opens the alert-rule screen when the KPI's metric is on that list, and nothing for task creation. *(source: contracts/satellite/reporting.yaml#AlertRule / contracts/satellite/reporting.yaml#MetricSource)*

**Data it reads**: `listKpis` (onLoad, The KPI being targeted)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The targets thresholds kpi list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the targets thresholds kpi untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No targets thresholds kpi yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the targets thresholds kpi are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **The pipeline behind the KPI has not refreshed**: The preview shows the status with a "Data delayed" marker and its as-of time; a stale number is never shown as plainly On track. *(source: contracts/satellite/reporting.yaml#KpiValue / MATRIX 8.7.22)*
- **A venue manager edits a tenant-level KPI**: They see and edit only their venue's targets; tenant rows are shown read-only for context. *(source: contracts/satellite/reporting.yaml#setKpiTargets)*

#### Consistency with other screens

- Match `ANL-063`: Same band editor and same status words; ANL-063 is the admin grid across scopes and periods, this is one KPI.
- Match `ANL-025`: The higher-is-better flag set in the KPI builder decides the band direction here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- kpi: Capacity utilisation
  direction: lower is better
  scope: Aquaventure Waterpark
  period: Oct 2026
  target: 75%
  warningAt: 80%
  criticalAt: 95%
  now: 86% - Warning
- kpi: Net revenue
  direction: higher is better
  scope: Aquaventure Waterpark
  period: Oct 2026
  target: AED 4,200,000.00
  warningAt: AED 3,780,000.00
  criticalAt: AED 3,360,000.00
  now: AED 3,912,440.75 - Warning
- kpi: Net revenue
  scope: Lost Paradise of Dilmun, Bahrain
  period: Oct 2026
  target: BHD 185,500.000
  warningAt: BHD 166,950.000
  criticalAt: BHD 148,400.000
- kpi: Refund rate
  direction: lower is better
  scope: All venues
  period: Q4 2026
  target: 1.5%
  warningAt: 2.0%
  criticalAt: 3.0%
```

#### Permissions

- `setKpiTargets` → `REPORT_MANAGE` (configure) · staff
- `listKpis` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- KPI threshold configuration defines normal/warning/critical bands per metric (e.g. capacity below 80% normal, 80-90% warning, above 95% critical), shown as status on the dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-704)*
- Retail intelligence shows sales and outlet performance, top-performing stores, demand forecasting (from retail sales history and online ticket booking trends) and target-vs-actual per outlet (e.g. monthly target vs. achieved, with variance). *(client request · MoM 19 Aug 2026, 4.9 Retail Intelligence & Reporting · DI-368)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-026` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-026`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 10: Works in Targets, Thresholds & KPI Status Rules → Configure how TICVAI determines whether KPI performance is healthy, warning or critical.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-026?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: If Critical → Generate Alert, Notify responsible user, Create operational task, Trigger AI analysis.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-027` Data & Filter Configuration

**Control what data a dashboard/widget uses and how users can filter it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-027 |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_TENANT` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/data-filter-configuration-anl-027` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Sets what data a dashboard's tiles read and which filters a viewer gets. In the contract a tile reads a report definition, so dataset, measure and aggregation belong to that report; this screen sets the dashboard-wide venue, each tile's run values, and which report parameters appear as viewer filters. The thing to get right is filter scope: every filter says where it applies (this visual, this dashboard, the report itself), and the tenant is never a filter.

**Known correction pending (do not draw the wrong version)**

- **Relationship and Currency selectors** Why: The semantic model deliberately hides joins from authors; currency is the venue's base currency with no conversion. *(source: contracts/satellite/reporting.yaml#SemanticModel / DI-211; Finance, Ledger & Tax · Reporting & Analytics)*
- **Data Domain, Dataset, Measure, Dimension, Aggregation and Calculation drawn as dashboard fields** Why: A tile references a report definition; these are that report's columns and grouping, saved by the report operations, not by updateDashboard. *(source: contracts/satellite/reporting.yaml#DashboardTile / contracts/satellite/reporting.yaml#CreateReportRequest; Finance, Ledger & Tax · Reporting & Analytics)*
- **getSemanticModel requires tenant-level reporting permission** Why: A venue-level author (REPORT_MANAGE at venue) cannot read the catalogue this screen loads. *(source: contracts/satellite/reporting.yaml#getSemanticModel / contracts/satellite/reporting.yaml#createReport; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where do page scope, locked filters and hidden filters live, given dashboards have no pages and tiles have untyped parameters?** → Drawn default accepted: Two scopes (visual, dashboard) plus report; no lock or hide toggles. *(decided by Chinmay, 2026-10-02; DEC-331 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Does dragging a dataset field onto the canvas create a hidden report definition per tile?** → Drawn default accepted: Yes, as the lead decides for ANL-023; this screen then shows that report's parameters. *(decided by Chinmay, 2026-10-02; DEC-332 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search data filter | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by global, widget-level, mandatory, optional, hidden, defaulted — which are present is a decision the pack already made. | — |
| Data Domain | select field | — | — | — | — | — | — |
| Dataset | select field | — | — | — | — | — | — |
| Measure | select field | — | — | — | — | — | — |
| Dimension | select field | — | — | — | — | — | — |
| Aggregation | select field | — | — | — | — | — | — |
| Date Field | select field | — | — | — | — | — | — |
| Relationship | select field | — | — | — | — | — | — |
| Calculation | select field | — | — | — | — | — | — |
| Date Range | select field | — | — | — | — | — | — |
| Site | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Customer Segment | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **filter scope**: Three scopes, each labelled on the chip. "This visual" - the tile's own run values. "Whole dashboard" - the dashboard venue plus a shared parameter applied to every tile that has it. "Report" - a fixed filter in the report definition, edited only in the report builder because changing it publishes a new report version for every dashboard that uses it. *(source: contracts/satellite/reporting.yaml#DashboardTile / contracts/satellite/reporting.yaml#ReportFilter)*
- **Mandatory, Optional, Defaulted (pack filter kinds)**: Mandatory = the parameter is required; Defaulted = it has a default value; both come from the report's parameter definition. Hidden has no field (see decisions). *(source: contracts/satellite/reporting.yaml#ReportParameter)*
- **Date range**: When no dates are given a run covers today in the venue's time zone; a range longer than the report's limit (366 days unless set) is refused, so the picker caps it. *(source: contracts/satellite/reporting.yaml#RunReportRequest / R158)*
- **Site, Venue, Attraction, Channel, Product, Customer segment**: Offered only where the tile's report has that field as a filterable parameter. Values narrow the viewer's scope, never widen it. *(source: contracts/satellite/reporting.yaml#ReportFilter / DI-705)*
- **Relationship (pack field)**: Remove. Joins are not shown to authors; the semantic model owns relationships. *(source: contracts/satellite/reporting.yaml#SemanticModel / contracts/satellite/reporting.yaml#getSemanticModel)*
- **Currency (pack field)**: Remove as a choice. Figures are in each venue's base currency; there is no conversion to choose. *(source: DI-211)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **active-filter breadcrumb**: The viewer always sees which filters are applied, with Clear and Reset to the designed default. *(source: MATRIX 6.1.78)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save**: Saves the whole dashboard (full replace of the dashboard and its tiles). Concurrent edits are last-write-wins, so show "Saved 10:42 by you". *(source: contracts/satellite/reporting.yaml#updateDashboard)*

**Data it reads**: `getSemanticModel` (onLoad, Datasets and fields to filter on)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data filter configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data filter untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data filter configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data filter are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094), as on `createDashboard` …; 409 Moving a dashboard to a module the caller is not entitled to. The same guard as `createDashboard` — without it, an update would be the way round the create …; 422 A tile's report lacks the column encodings its visualisation needs … |

#### Edge cases to draw

- **A whole-dashboard filter (Channel) where some tiles' reports have no channel parameter**: Those tiles show "Not filtered by channel" on their header instead of silently ignoring it. *(source: MATRIX 6.1.78)*
- **Relative dates (last 7 days, month to date) and Top N**: Not expressible as filter operators; draw relative-date presets that resolve to from/to dates at run time, and no Top N. *(source: contracts/satellite/reporting.yaml#ReportFilter)*

#### Consistency with other screens

- Match `ANL-035`: Report-scope filters are authored there; this screen links to it rather than duplicating the editor.
- Match `ANL-023`: The canvas's filter pane uses the same scope chips and wording.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
filters:
- label: Visit date
  scope: Whole dashboard
  value: Today
  mandatory: true
- label: Channel
  scope: Whole dashboard
  values:
  - POS
  - Web
  - App
  mandatory: false
- label: Venue
  scope: Whole dashboard
  value: Aquaventure Waterpark
- label: Outlet
  scope: This visual
  tile: F&B sales by hour
  value: Poolside Grill
```

#### Permissions

- `getSemanticModel` → `REPORT_VIEW_TENANT` (operate) · staff
- `updateDashboard` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Date/filter configuration lets a dashboard be filtered by sales channel, department or period. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-705)*
- Dashboard creation is drag-and-drop against predefined data sets (revenue, sales quantity, sales channel, department, etc.); the user picks a visual format (bar chart, pie chart, etc.) without writing queries. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-703)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-027` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-027`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 12: Works in Data & Filter Configuration → Control what data a dashboard/widget uses and how users can filter it.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-027?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_TENANT`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-028` Drill-Down & Interaction Designer

**Configure how users move from high-level KPIs into deeper analytics.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-028 |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/drill-down-interaction-designer-anl-028` |

**Known gaps.** **Drill-Down & Interaction Designer declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Configures how a viewer moves from a headline number to the transactions behind it: drill down and up a real hierarchy, drill through to a detail page that keeps the filters and has a visible Back, and how a click on one visual filters or highlights the others. The thing to get right: drill only where the data has a genuine hierarchy, and a drill that lands on 10,000 transactions must page, not freeze.

**Known correction pending (do not draw the wrong version)**

- **The gap says the screen declares no write operation** Why: It declares updateDashboard; the gap text is stale. *(source: screens/P16-venue-analytics.yaml#ANL-028; Finance, Ledger & Tax · Reporting & Analytics)*
- **Drill paths, interactions, drill-through targets and tooltips have no field** Why: DashboardTile has only an untyped parameters object; the interaction framework is meant to be central, not per chart, and the semantic model declares no hierarchies. *(source: contracts/satellite/reporting.yaml#DashboardTile / contracts/satellite/reporting.yaml#SemanticModel; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Where are hierarchies declared (semantic model) and where is a tile's interaction setting stored?** → Drawn default accepted: Draw the editor; mark it pending the interaction-framework decision. *(decided by Chinmay, 2026-10-02; DEC-333 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Click behavior | select field | — | — | — | — | — | — |
| Cross-filtering | select field | — | — | — | — | — | — |
| Drill-down | select field | — | — | — | — | — | — |
| Drill-up | select field | — | — | — | — | — | — |
| Drill-through | select field | — | — | — | — | — | — |
| Tooltip | select field | — | — | — | — | — | — |
| Detail page | select field | — | — | — | — | — | — |
| Related dashboard | select field | — | — | — | — | — | — |
| Underlying report | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Drill-down path**: Chosen from declared hierarchies only, e.g. Year > Month > Day > Channel > Transaction > Detail, or Region > Venue > Product > Performance. A level the data does not support is not offered. *(source: DI-709 / MATRIX 8.7.28 / TRACKER Actions row 256)*
- **Interaction per pair of visuals (pack "Cross-filtering", "Click behavior")**: A small matrix, source visual by target visual, each cell Filter, Highlight or None. Highlight keeps the target's totals and emphasises the selected part. *(source: MATRIX 6.1.78)*
- **Drill-through target (pack "Detail page", "Related dashboard", "Underlying report")**: A dashboard or report the viewer could open anyway; the target receives the clicked values as filters and shows a Back control naming where it came from. *(source: MATRIX 8.7.28 / MATRIX 2.12.13)*
- **Tooltip**: Default tooltip shows the value and its comparison; rich tooltip adds fields (sales, tickets, average ticket value, variance for a hovered date). *(source: MATRIX 6.1.78 / MATRIX 8.7.28 / MATRIX 6.1.66)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **path preview**: A breadcrumb preview of the path with sample values ("2026 > October > 01 Oct > Web > Order 2026-104311") so the designer sees each step. *(source: DI-709)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save**: Saves the dashboard as a whole; see corrections for where these settings have to live. *(source: contracts/satellite/reporting.yaml#updateDashboard)*

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The drill-down interaction designer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the drill-down interaction designer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No drill-down interaction designer configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094), as on `createDashboard` …; 409 Moving a dashboard to a module the caller is not entitled to. The same guard as `createDashboard` — without it, an update would be the way round the create …; 422 A tile's report lacks the column encodings its visualisation needs … |

#### Edge cases to draw

- **Drill to transaction level returns 10,000 rows for one day**: The detail opens as a paged result (cursor pages, virtualised table); above the inline row limit (5,000 proposed) it runs in the background with progress and a Cancel. *(source: DI-710 / contracts/satellite/reporting.yaml#runReport / contracts/satellite/reporting.yaml#ReportResult / R094)*
- **Drill-through target the viewer cannot open (a module they are not entitled to)**: The drill-through option is not rendered for that viewer, not shown as an error after the click. *(source: DI-387 / MATRIX 8.9.10)*
- **Hierarchy level with an unknown member (sales with no channel)**: Shown as "Unknown" at that level, with its total, never dropped. *(source: MATRIX 8.7.28 / MATRIX 7.1.31)*

#### Consistency with other screens

- Match `ANL-040`: Drill to transactions ends in the same results viewer, paging and totals.
- Match `ANL-024`: Only marks that support drill show drill options.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
drillPath:
- Region
- Venue
- Product
- Performance
exampleTrail: UAE > Aquaventure Waterpark > Day pass - Adult > 01 Oct 2026 10:00
interactions:
- from: Sales by channel (bar)
  to: Orders (table)
  behaviour: Filter
- from: Sales by channel (bar)
  to: Monthly sales (line)
  behaviour: Highlight
drillThrough:
  from: Refund rate KPI
  to: Refund transactions report
  carries:
  - Venue
  - Visit date
```

#### Permissions

- `updateDashboard` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam shared the itemised dashboard-component document (chart types, drill-down tool, heat map, etc.) with a suggested reference architecture - explicitly a suggestion Softlabs may adopt, adapt or replace. *(agreed · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-750)*
- Very large drill-down result sets (e.g. 10,000 transactions in a single day) must be handled without the interface crashing or becoming unresponsive. *(agreed · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-710)*
- Drill-down from a high-level figure to transaction detail - yearly sales -> monthly -> daily -> sales channel -> individual transaction -> transaction detail (which customer, which ticket) - only where the data has a genuine hierarchy. *(agreed · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-709)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-028` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-028`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 14: Works in Drill-Down & Interaction Designer → Configure how users move from high-level KPIs into deeper analytics.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-028?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-029` Dashboard Access, Publishing & Versioning

**Govern who can access dashboards and how dashboard changes reach production.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-029 |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/dashboard-access-publishing-versioning-anl-029` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Governs who sees a dashboard and how a change reaches production: draft, preview and validate, approval, publish, with versions and rollback. The client asked for an approval step before publishing. The thing to get right: none of this lifecycle exists in the contract today (a dashboard is saved live by a full replace), so the design is the specification and must be flagged as such; access today is area (module) entitlement plus Shared or Private.

**Known correction pending (do not draw the wrong version)**

- **No draft, version, approval, publish or rollback exists for dashboards** Why: Dashboard has no status or version and updateDashboard replaces the live dashboard; DI-706 and the builder spec cannot be met. The workbook marks MOM-1480 and MOM-2741 Covered, which the contract does not support. *(source: contracts/satellite/reporting.yaml#Dashboard / contracts/satellite/reporting.yaml#updateDashboard / MoM 2026-09-08 4.3 Dashboard Designer (Board 2) / MATRIX 7.4.45 / MATRIX 11.1.2 / DI-706; Finance, Ledger & Tax · Reporting & Analytics)*
- **Approval has no kind for publishing a dashboard** Why: The approval kinds cover refunds, price, configuration and more, but not a dashboard or report publish. *(source: contracts/spine/approvals.yaml#ApprovalKind; Finance, Ledger & Tax · Reporting & Analytics)*
- **The gap says no schema with described properties** Why: Dashboard is described; the missing part is a version history schema, which is the real gap. *(source: screens/P16-venue-analytics.yaml#ANL-029; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is dashboard publishing a configurationChange approval or its own approval kind, and who may approve?** → Drawn default accepted: Draw an approver picker limited to people who can manage reports, excluding the author. *(decided by Chinmay, 2026-10-02; DEC-334 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Is promotion between environments (staging to production) in scope?** → Drawn default accepted: Not drawn. *(decided by Chinmay, 2026-10-02; DEC-335 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Access (pack "Assign dashboards to")**: What exists: the dashboard's area decides which logins can see it, and Shared/Private decides whether anyone but the owner can. Each viewer then sees only their own scope. Draw assignment to roles or users as pending. *(source: contracts/satellite/reporting.yaml#CreateDashboardRequest / DI-702 / DI-721)*
- **Change description**: Required when submitting for approval, so the version list explains itself. *(source: MATRIX 7.4.45 / MATRIX 11.1.2 / MATRIX 7.1.46)*

#### Outputs: what the screen shows and produces

**Shown**

**Every access publishing versioning** (data table)

| Shows | Format | Notes |
|---|---|---|
| Version number | text | not in the schema: `Version Number` |
| Changed by | text | not in the schema: `Changed By` |
| Date/time | text | not in the schema: `Date/Time` |
| Change description | text | not in the schema: `Change Description` |
| Approval status | text | not in the schema: `Approval Status` |
| Published version | text | not in the schema: `Published Version` |

**The selected access publishing versioning** (detail panel): The pack groups this record's detail under its own headings: “Assign dashboards to”, “Administer”, “Rollback”.

| Shows | Format | Notes |
|---|---|---|
| Version number | text | not in the schema: `Version Number` |
| Changed by | text | not in the schema: `Changed By` |
| Date/time | text | not in the schema: `Date/Time` |
| Change description | text | not in the schema: `Change Description` |
| Approval status | text | not in the schema: `Approval Status` |
| Published version | text | not in the schema: `Published Version` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **version list**: Version, changed by, date and time, change description, approval status (Draft, In review, Approved, Published, Rejected), and which version is live. Newest first; the live version pinned on top. *(source: screens/P16-venue-analytics.yaml#ANL-029 / MATRIX 7.1.46)*
- **compare**: A side-by-side of two versions listing tiles added, removed and changed, so a reviewer approves a difference, not a whole dashboard. *(source: MATRIX 7.1.46)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Submit for approval**: Moves the draft to In review; the author cannot approve their own change. *(source: DI-706 / DI-732)*
- **Approve and publish / Reject**: Human decision only; AI may show analytics about approvals but never recommends approve or reject. *(source: DI-735 / TRACKER Actions row 261)*
- **Roll back**: Republishes an earlier version as a new version (history is never rewritten); confirmation names the version and its date. *(source: MATRIX 7.1.46 / contracts/satellite/reporting.yaml#ReportDefinitionVersion)*
- **Stop sharing**: Makes the dashboard private; required before it can be archived, because it is on other people's screens. *(source: contracts/satellite/reporting.yaml#deleteDashboard)*

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access publishing versioning list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access publishing versioning untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access publishing versioning yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the access publishing versioning are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094), as on `createDashboard` …; 409 Moving a dashboard to a module the caller is not entitled to. The same guard as `createDashboard` — without it, an update would be the way round the create …; 422 A tile's report lacks the column encodings its visualisation needs … |

#### Edge cases to draw

- **A published dashboard whose tile report was retired**: The tile shows "This report was retired" and the version cannot be re-published until the tile is replaced. *(source: contracts/satellite/reporting.yaml#deleteReport)*
- **Viewers' permissions change after publishing**: Tiles the viewer may no longer read render the no-permission state; the dashboard never shows them stale data. *(source: MATRIX 7.1.50 / MATRIX 7.1.51)*

#### Consistency with other screens

- Match `ANL-039`: Reports already keep every published version; dashboard versions should read the same (version label, published by, published at).
- Match `ANL-030`: Submit for approval is offered only when validation on ANL-030 has no blocking issue.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
versions:
- version: v4 (draft)
  changedBy: Omar Haddad
  at: 01 Oct 2026 09:12
  change: Added F&B sales by hour heatmap
  status: Draft
- version: v3
  changedBy: Rahul Menon
  at: 22 Sep 2026 16:40
  change: Capacity gauge now uses venue target
  status: Published
  live: true
- version: v2
  changedBy: Rahul Menon
  at: 15 Sep 2026 11:05
  change: Removed duplicate revenue tile
  status: Superseded
approver: Fatima Al Mansoori
```

#### Permissions

- `updateDashboard` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dashboards go through an approval step before publishing. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-706)*
- Business can build additional dashboards (e.g. separate finance, sales, operations dashboards) with role-based access so only the relevant team can view a given dashboard. *(client request · MoM 8 Sep 2026, 4.3 Dashboard Designer (Board 2) · DI-702)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-029` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-029`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 16: Works in Dashboard Access, Publishing & Versioning → Govern who can access dashboards and how dashboard changes reach production.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409, 422).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-029?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-030` Dashboard Preview, Validation & Health

**Validate dashboards before publication and monitor their technical/analytical health afterward.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | Block D · task APP-ANALYTICS-ANL-030 |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `dashboardId` (navigation) |
| Route | `/analytics/dashboard-preview-validation-health-anl-030` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Two jobs: validate a dashboard before it is published, and show its health after. Validation stops a dashboard with a blocking problem from being submitted; health tells the owner whether viewers are seeing fresh, fast, complete data. The thing to get right: preview runs with the designer's own access, so it must say that viewers with less access will see less, and a preview must not count as a view.

**Known correction pending (do not draw the wrong version)**

- **Background "record a view" on this screen** Why: Designer previews would count as viewer opens and inflate the usage figures used to prune dashboards; preview must not record a view. *(source: contracts/satellite/reporting.yaml#recordDashboardView / contracts/satellite/reporting.yaml#getAnalyticsUsage; Finance, Ledger & Tax · Reporting & Analytics)*
- **Widget load time and API status columns** Why: No operation measures client render time per tile or an API status for a dashboard. *(source: contracts/satellite/reporting.yaml#AnalyticsUsageRow / MATRIX 8.7.32; Finance, Ledger & Tax · Reporting & Analytics)*
- **Validate-then-publish has nothing to gate** Why: There is no validate, submit, approve or publish operation for a dashboard; the only write is a full replace of the live dashboard, so "prevents dashboards with critical errors from being published" cannot be enforced. *(source: contracts/satellite/reporting.yaml#updateDashboard / DI-706 / MATRIX 7.4.45 / MATRIX 11.1.2 / screens/P16-venue-analytics.yaml#ANL-030; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is "preview as a role" (see what a venue manager would see) in scope?** → Drawn default accepted: Not drawn; preview is with the designer's access and says so. *(decided by Chinmay, 2026-10-02; DEC-336 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every preview validation health** (data table)

| Shows | Format | Notes |
|---|---|---|
| Data last refreshed | text | not in the schema: `Data Last Refreshed` |
| Refresh frequency | text | not in the schema: `Refresh Frequency` |
| Dataset status | text | not in the schema: `Dataset Status` |
| Query performance | text | not in the schema: `Query Performance` |
| Widget load time | text | not in the schema: `Widget Load Time` |
| Failed widgets | text | not in the schema: `Failed Widgets` |
| API status | text | not in the schema: `API Status` |
| User count | text | not in the schema: `User Count` |
| Usage frequency | text | not in the schema: `Usage Frequency` |

**The selected preview validation health** (detail panel): The pack groups this record's detail under its own headings: “Preview Modes”, “Ready to Publish”, “Issues Detected”, “The end user should experience”.

| Shows | Format | Notes |
|---|---|---|
| Data last refreshed | text | not in the schema: `Data Last Refreshed` |
| Refresh frequency | text | not in the schema: `Refresh Frequency` |
| Dataset status | text | not in the schema: `Dataset Status` |
| Query performance | text | not in the schema: `Query Performance` |
| Widget load time | text | not in the schema: `Widget Load Time` |
| Failed widgets | text | not in the schema: `Failed Widgets` |
| API status | text | not in the schema: `API Status` |
| User count | text | not in the schema: `User Count` |
| Usage frequency | text | not in the schema: `Usage Frequency` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **validation checklist**: Blocking: more than 24 tiles; a tile refreshing faster than every 30 seconds; refresh load over the venue budget; a tile whose report is retired or missing; a mark that cannot bind its data. Warning: a tile whose report needs higher access than some viewers of a shared dashboard have (they will see a no-permission tile); personal-data fields on a shared dashboard; a dataset whose pipeline is stale. Each issue names the tile and offers "Go to tile". *(source: contracts/satellite/reporting.yaml#CreateDashboardRequest / contracts/satellite/reporting.yaml#DashboardTile / contracts/satellite/reporting.yaml#createDashboard / …)*
- **health panel**: Data last refreshed (per pipeline behind the tiles, worded "Updated 4 min ago"), dataset status (Healthy, Degraded, Stale, Failed, Paused), failed tiles from the last load, average query time, viewers and opens. Thresholds from the client's targets - shell 2 s, cached visual 2 s, uncached query 5 s at p95 - colour the timings. *(source: contracts/satellite/reporting.yaml#AnalyticsPipeline / contracts/satellite/reporting.yaml#DashboardData / contracts/satellite/reporting.yaml#AnalyticsUsageRow)*
- **preview modes**: Desktop, tablet, phone (a CEO on a phone) and full-screen presentation; one tile failing never blanks the page. *(source: DI-696)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Preview**: Reads the dashboard with tile data under the designer's own access; banner "Previewing with your access". *(source: contracts/satellite/reporting.yaml#getDashboard)*
- **Submit for approval**: Enabled only with no blocking issues; leads to ANL-029. *(source: MATRIX 7.4.45 / MATRIX 11.1.2)*

**Data it reads**: `listAnalyticsPipelines` (onLoad, Whether its data is fresh); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ANL-021` Dashboard Library: *Back to Dashboard Library*; carries `dashboardId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The preview validation health list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the preview validation health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No preview validation health yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the preview validation health are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **One tile errors in preview**: That tile shows its error and a Retry; the others render; validation lists it. *(source: contracts/satellite/reporting.yaml#DashboardData)*
- **Tiles served from cache**: Show "Cached - as of 10:41" on the tile so a designer does not mistake cache for live. *(source: contracts/satellite/reporting.yaml#DashboardData)*

#### Consistency with other screens

- Match `ANL-067`: Pipeline status words and freshness wording are the same.
- Match `ANL-029`: Validation result gates submit.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
validation:
- severity: Blocking
  tile: Margin bridge
  issue: Waterfall cannot bind its data yet
- severity: Warning
  tile: Guest list
  issue: Contains personal data on a shared dashboard
- severity: Warning
  tile: Admissions by hour
  issue: Ticketing dataset delayed - last refreshed 38 min ago (expected 15)
health:
  lastRefreshed: Updated 4 min ago
  datasets: 5 healthy, 1 stale
  failedTiles: 0
  avgQuery: 1.8 s
  viewers30d: 42
  opens30d: 611
```

#### Permissions

- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAnalyticsPipelines` → `REPORT_VIEW_TENANT` (operate) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-030` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS173 Unified BI Reporting and AI Analytics Platform Board 2.dc.html#anl-030`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 2
- Flow F176 *Unified BI Reporting and AI Analytics Platform board 2: Dashboard Library*, step 18: Works in Dashboard Preview, Validation & Health → Validate dashboards before publication and monitor their technical/analytical health afterward.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-030?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-021`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
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

**18 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createDashboard": {"method":"POST","path":"/dashboards","contract":"reporting","summary":"Create a dashboard","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateDashboardRequest","responds":"Dashboard"},
"createKpi": {"method":"POST","path":"/kpis","contract":"reporting","summary":"Define a KPI once, for everywhere","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"KpiDefinition","responds":"KpiDefinition"},
"deleteDashboard": {"method":"DELETE","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Archive a dashboard","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"getReport": {"method":"GET","path":"/reports/{reportId}","contract":"reporting","summary":"Read a report definition","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportDefinition"},
"getSemanticModel": {"method":"GET","path":"/semantic-model","contract":"reporting","summary":"The business data catalogue reports are built from","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SemanticModel"},
"listAnalyticsPipelines": {"method":"GET","path":"/analytics-pipelines","contract":"reporting","summary":"Data sources, refresh state and freshness","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AnalyticsPipeline"},
"listDashboards": {"method":"GET","path":"/dashboards","contract":"reporting","summary":"List dashboards","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":false},{"name":"includeArchived","in":"query","required":false}],"requestBody":null,"responds":"Dashboard"},
"listKpis": {"method":"GET","path":"/kpis","contract":"reporting","summary":"The enterprise KPI library","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"KpiDefinition"},
"listReports": {"method":"GET","path":"/reports","contract":"reporting","summary":"List available report definitions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordDashboardView": {"method":"POST","path":"/dashboards/{dashboardId}/views","contract":"reporting","summary":"Record that a dashboard was opened","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setKpiTargets": {"method":"PUT","path":"/kpis/{kpiId}/targets","contract":"reporting","summary":"Targets, thresholds and what red means","permission":"REPORT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"KpiTarget"},
"updateDashboard": {"method":"PUT","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Update a dashboard","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateDashboardRequest","responds":"Dashboard"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Aggregation": {"type":"string","enum":["none","count","countDistinct","sum","average","min","max"]},
"AnalyticsPipeline": {"type":"object","x-ticvai-persistence":"reporting.pipeline","description":"BI board 10.7. **Freshness decides whether a dashboard can be trusted.**","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"sourceKind":{"type":"string"},"datasets":{"type":"array","items":{"type":"string"}},"schedule":{"type":"string","nullable":true},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastSuccessAt":{"type":"string","format":"date-time","nullable":true},"freshnessMinutes":{"type":"integer","nullable":true},"expectedFreshnessMinutes":{"type":"integer","nullable":true},"status":{"type":"string","enum":["healthy","degraded","stale","failed","paused"]},"lastError":{"type":"string","nullable":true},"rowsLastRun":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"CreateDashboardRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","module","tiles"],"properties":{"name":{"type":"string","maxLength":200},"module":{"$ref":"#/components/schemas/common::ModuleKey","description":"**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid","description":"Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"},"isShared":{"type":"boolean","default":false},"tiles":{"type":"array","minItems":1,"maxItems":24,"items":{"$ref":"#/components/schemas/DashboardTile"}}}},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"DashboardTile": {"x-ticvai-persistence":"reporting.dashboard_tile","type":"object","required":["id","reportId","visualisation","position"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string"},"reportId":{"type":"string","format":"uuid"},"visualisation":{"type":"string","description":"**Extended 22 September from eight marks to twenty** against `Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`, which names eighteen components and marks every one MVP. Nine were genuinely missing — `combo`, `matrix`, `funnel`, `waterfall`, `treemap`, `scatter`, `map`, `ribbon`, `decompositionTree` — and three are layout variants of marks already here: `area` beside `line`, `donut` beside `pie`, `stackedBar100` beside `stackedBar`.\n**`number` is the source's KPI / card.** Its comparison, variance, trend sparkline and status icon are tile parameters rather than separate marks.\n**Two of the eighteen are deliberately not here** — see `x-ticvai-refuses`. The source lists them as components; the platform already models each of them elsewhere, and a second model of either is the drift this enum exists to prevent.\n","enum":["number","line","area","bar","stackedBar","stackedBar100","combo","pie","donut","table","matrix","gauge","heatmap","funnel","waterfall","treemap","scatter","map","ribbon","decompositionTree"],"x-ticvai-refuses":{"slicer":"**A control, not a mark.** The source's slicer / filter is already `ReportFilter.isParameter` plus `ReportParameter` — a run-time prompt bound to the report. A slicer on the canvas places that parameter; it does not render a result, so it is not a visualisation and a second filter model beside `ReportFilter` would be one somebody keeps in step by hand.","narrative":"**Generated prose belongs with `ai.Suggestion`.** The source's narrative / insight text (*\"Admissions are 12% above last Tuesday\"*) is model output with traceability requirements, not a way of drawing a query result.","cohort":"**Not one of the eighteen.** It appears once in the source as a *usage* — *\"the Customer & Membership dashboard shall use cards, cohort and trend charts\"* — never as a specified component. A cohort view is a `matrix` or `heatmap` over a cohort dimension."},"x-ticvai-note":"**The marks bind through the report's column encodings** (decided 2 October 2026, Chinmay; CHG-FIN-007: build the nine). Superseding the note of 22 September, which left `ReportColumn.role` undecided. Each column of the tile's report carries `role` and `encoding` (and `axis`, `seriesType`, `hierarchyLevel`, `unitLabel` where the mark needs them), and `createDashboard` / `updateDashboard` refuse 422 `tile-encoding-missing` a tile whose report lacks what its mark requires:\n\n| Mark | Requires | |---|---| | `combo` | one `x` dimension; two or more measures, each with `axis` and `seriesType`; `unitLabel` on a secondary axis | | `matrix` | `row` dimensions (with `hierarchyLevel`), optional `column` dimensions, one or more `value` measures | | `funnel` | one `stage` dimension in order (`sortOrder`), one `value` measure | | `waterfall` | one `category` dimension of ordered steps, one `value` measure; the steps are a named measure set (for example Gross sales, Discounts, Refunds, Net revenue) and the last is the total | | `treemap` | one or more `category` dimensions with `hierarchyLevel`, one `size` measure, optional `colour` measure | | `scatter` | an `x` and a `y` measure, a `label` dimension, optional `size` and `colour` | | `map` | one `location` dimension (venue, zone or venue-map point), one `value` measure | | `ribbon` | an `x` dimension (period), a `series` dimension, one `value` measure (rank flow) | | `decompositionTree` | one `value` measure and two or more dimensions with `hierarchyLevel` |\n\nThe other eleven marks bind as before (`number` one measure; `line`, `area`, `bar` and the stacked bars an `x` dimension, optional `series`, one or more `y` measures; `pie`, `donut`, `gauge`, `heatmap`, `table` as their names). **Unchanged**: at most 24 tiles a dashboard, and every tile shows its as-of time and goes stale past its refresh (`KpiValue.asOf`, `stale`; BOARDREQ MOM-2713/2714).\n"},"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose, and not yet specified.** Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as `RunReportRequest.parameters`) and its display settings — for `number`, the comparison, variance, sparkline and status icon. The per-visualisation display shape waits on the field-wells decision in `visualisation`'s `x-ticvai-note`.\n"},"refreshSeconds":{"type":"integer","minimum":30,"description":"Minimum thirty seconds. A tile refreshing every second is a load problem wearing a convenience costume.\n"},"position":{"type":"object","required":["row","column","width","height"],"properties":{"row":{"type":"integer"},"column":{"type":"integer"},"width":{"type":"integer"},"height":{"type":"integer"}}}}},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"KpiDefinition": {"type":"object","x-ticvai-persistence":"reporting.kpi_definition","description":"BI boards 2.5 and 10.2. **One definition, referenced everywhere** — otherwise *revenue* means two things in the same meeting.\n","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","description":"`takings` and `admissions` are seeded for every tenant as system KPIs (decided 28 September, audit R283), and the five accreditation KPIs for every tenant with the accreditation module (29 September, build pass). The seeded codes are `ReportingSystemKpi`.\n"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"domain":{"type":"string","nullable":true},"formula":{"type":"string","description":"**Expressed against the semantic model, not against tables.** A KPI written in SQL is a KPI that breaks when the warehouse is reshaped.\n"},"unit":{"type":"string","enum":["currency","count","percentage","duration","ratio","score"]},"higherIsBetter":{"type":"boolean","default":true,"description":"**Refund rate and revenue both go up.** Without this the status colour is a coin toss.\n"},"defaultPeriod":{"type":"string","nullable":true},"owner":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"KpiTarget": {"type":"object","x-ticvai-persistence":"reporting.kpi_target","description":"BI board 2.6. **The threshold is what turns a number into a status.**","required":["scopePath","period","target"],"properties":{"kpiId":{"type":"string","format":"uuid"},"scopePath":{"type":"string","description":"The scope this target applies to. With `period`, the key `setKpiTargets` matches on."},"period":{"type":"string"},"target":{"$ref":"#/components/schemas/MetricValue"},"amberAt":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"redAt":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"stretch":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"SemanticModel": {"type":"object","x-ticvai-persistence":"reporting.semantic_model","description":"BI boards 3.3 and 10.6. **A vocabulary, not a schema.** Exposing joins to report authors produces reports that are wrong invisibly.\n","properties":{"version":{"type":"integer","readOnly":true,"description":"Assigned by the server on each publish."},"domains":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"datasets":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"name":{"type":"string"},"grain":{"type":"string","description":"**What one row means.** The single most common cause of a wrong report is a join that silently multiplied the grain.\n"},"fields":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"dataType":{"$ref":"#/components/schemas/FieldType"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"nullable":true,"description":"The default aggregation for the field, where it has one."},"sensitive":{"type":"boolean","default":false},"description":{"type":"string","nullable":true}}}}}}}}}},"relationships":{"type":"array","items":{"type":"object","properties":{"fromDataset":{"type":"string"},"toDataset":{"type":"string"},"cardinality":{"type":"string","enum":["oneToOne","oneToMany","manyToOne","manyToMany"]}}}},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string"}}}
}
```
