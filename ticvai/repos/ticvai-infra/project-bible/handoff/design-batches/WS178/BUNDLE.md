# WS178 — TICVAI Finance Backend Structure Reference v1.0 board 1

**1 screens · 6 operations · 17 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `LEDGER_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `BO-1081` | Finance Dashboard | C | 2 | 41 | 6 | 0 | 1 | 0 | — | notStarted (—) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-1081` Finance Dashboard

**Finance Dashboard**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 3 · needs the `core` module |
| Block | Block C · task VM-BO-1081 |
| Who uses it | venue staff holding `LEDGER_VIEW`, `REPORT_VIEW_VENUE` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/orders-money/finance-dashboard-bo-1081` |

**What the spec says about it.** **Measure names, not "Revenue"** (decided 2 October 2026, Chinmay; CHG-FIN-002; BOARDREQ MOM-2758..2761). Takings (money taken less money paid back, a cash-control figure), Gross sales (before discounts, excluding VAT), Net revenue (gross sales less discounts and refunds), Recognised revenue and Deferred revenue are different numbers and never share a label; a tile takes its label from the seeded KPI it is bound to (`ReportingSystemKpi`). The tiles bind the seeded finance KPIs (`grossSales`, `discounts`, `refunds`, `netRevenue`, `recognisedRevenue`, `deferredRevenue`, `taxCollected`; CHG-FIN-007) and never the `takings` KPI. **One reporting area, one set of numbers** (decided 2 October 2026, Chinmay; CHG-FIN-006; DI-721, DI-702). This screen is a scoped window onto the reporting area (Analytics, P16): it runs the same seeded report definitions and reads the same seeded KPIs, so its figures equal what Analytics shows for the same scope, period and as-of time. It computes no total of its own and shows the as-of time on every figure.

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The finance team's one-glance position for one legal entity and one period: Gross sales, Discounts, Refunds, Net revenue, Recognised revenue and Deferred revenue as six separate tiles, then where the money stands (POS, gateway, bank and wallet each against the ledger) and the health of tax documents. The one thing to get right: the six measures are different numbers with different sources and must never share a label or be stacked into one bar. Gross and net are operational sales facts; recognised and deferred are ledger facts that move on visit, redemption and expiry, not on sale.

**Known correction pending (do not draw the wrong version)**

- **Pattern fell back to listDetail, with a "Search finance" field and an empty state that "carries the create action".** Why: A dashboard has no population to search and nothing to create; the empty state should say no postings exist for the period yet. *(source: screens/P08-venue-back-office.yaml#BO-1081; Finance, Ledger & Tax · Reporting & Analytics)*

**Fixed on main** (the package already carries these; draw what it says): The screen carries only a filter bar: no tiles, no chart, no definitions. The client's tile set (gross, net, recognised, deferred, refunds) … (CHG-FIN-007); The seeded "takings" KPI (payments taken less refunds) must not be bound to the Gross sales or the Net revenue tile as a stop-gap. (CHG-FIN-007); A Finance Dashboard inside Orders & Money duplicates the consolidated reporting area. (CHG-SBO-023).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is Gross sales shown excluding VAT, and are service fees inside it or a separate line?** → Drawn default stands (answer: "Excluding VAT; fees on their own line with a footnote"): Draw excluding VAT, with fees as their own line under Gross sales and a footnote saying so. *(decided by Chinmay, 2026-10-02; DEC-217 / CHG-NOTE-003)*
- **What is the pack's "Attraction" filter in scope terms (a scope node below venue, or a product category)?** → Drawn default stands (answer: "Product category (venue + category filters)"): Leave it out; offer Venue plus Product category. *(decided by Chinmay, 2026-10-02; DEC-218 / CHG-NOTE-003)*
- **Does BO-1081 stay as its own P08 screen (DI-260) or become the Finance standard dashboard in P16 opened from Orders & Money (DI-721)?** → One P16 Finance dashboard; Orders & Money (P08) shows a link card to it. *(decided by Chinmay, 2026-10-02; DEC-219 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search finance | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by company: uae01, site: all sites, attraction: all, currency: aed, period: august 2026 — which are present is a decision the pack already made. | — |

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
| Module | select | — | Core · Ticketing · Access · Fnb · Retail · Inventory · Seating · Membership · Marketing · Resources · Queue · Transport … | `getKpiValues` ?module |
| From | date picker | — | — | `getUnifiedReconciliation` ?from |
| To | date picker | — | — | `getUnifiedReconciliation` ?to |
| Order | picker: choose an order | — | — | `listTaxInvoices` ?orderId |
| Legal entity | picker: choose a legal entity | — | — | `listTaxInvoices` ?legalEntityId |
| Invoice type | segmented control | — | Simplified · Full · Consolidated | `listTaxInvoices` ?invoiceType |
| Status | radio group | — | Issued · Partially credited · Fully credited · Superseded | `listTaxInvoices` ?status |
| Issued from | date picker | — | — | `listTaxInvoices` ?issuedFrom |
| Issued to | date picker | — | — | `listTaxInvoices` ?issuedTo |
| … 10 more | | | | `operations.json` |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **period**: Month is the default (the pack shows "August 2026"), with day, week, month, quarter, year and a custom range. "Year" means the legal entity's fiscal year, which varies by country (UAE January to December, India April to March). Charts re-draw for the chosen period without leaving the page. *(source: DI-260 / DI-263 / MoM 2026-08-12 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities / contracts/spine/finance.yaml#/components/schemas/LegalEntity)*
- **legal entity (the pack's "Company UAE01")**: Required, single choice, first in the filter bar. It fixes the base currency, so the pack's "Currency AED" is shown as read-only text next to it, not offered as a choice. Records are only ever in base currency; there is nothing to convert. *(source: DI-211 / DI-282 / contracts/spine/finance.yaml#/components/schemas/LegalEntity)*
- **venue (the pack's "Site All Sites")**: Lists only the venues the signed-in user may see; a venue manager arrives locked to their venue and the control is shown as text. Scope comes from the caller's permissions, not from what the filter sends. *(source: DI-061 / DI-248 / contracts/satellite/reporting.yaml#getKpiValues)*

#### Outputs: what the screen shows and produces

**Shown**

**Finance dashboard** (card list, from `listDashboards`): **The link card to ANL-072, the one P16 Finance dashboard (decided 2 October 2026 by Chinmay, DEC-219; CHG-CSA-022, CHG-SOT-008).** Orders & Money keeps no second copy of the figures.

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Module | chip: Core, Ticketing, Access, Fnb, Retail, Inventory… | Which module this dashboard belongs to, and therefore who may see it. Added 22 September for the command centre: one shell that shows each … |
| Description | text | — |
| Venue | the name it points at, never the id | Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. |
| Is shared | yes / no (icon or chip) | — |
| Tiles | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Title | text | — |
| Report | the name it points at, never the id | — |
| Visualisation | chip: Number, Line, Area, Bar, Stacked bar, Stacked bar100… | Extended 22 September from eight marks to twenty against `Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`, which names … |
| Parameters | grouped details | Open on purpose, and not yet specified. Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as … |
| Refresh seconds | 1,234 | Minimum thirty seconds. A tile refreshing every second is a load problem wearing a convenience costume. |
| Position | grouped details | — |
| Row | 1,234 | — |
| Column | 1,234 | — |
| Width | 1,234 | — |
| Height | 1,234 | — |
| ID | the name it points at, never the id | — |
| Owner principal | the name it points at, never the id | — |
| Aggregate cost | chip: Low, Medium, High | Combined refresh load of every tile. |

**Gross sales** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=grossSales`, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Discounts** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=discounts`, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Refunds** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=refunds`, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Net revenue** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=netRevenue`, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Recognised revenue** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=recognisedRevenue`, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Deferred revenue** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=deferredRevenue`, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**VAT collected** (metric tile, from `getKpiValues`): `getKpiValues?kpiCodes=taxCollected`, with its as-of time; formula in `ReportingSystemKpi` (D-185 default, client finance sign-off pending; CHG-FIN-007).

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **headline tiles**: Fixed order Gross sales, Discounts, Refunds, Net revenue, Recognised revenue, Deferred revenue (balance at period end). Each tile shows the base-currency value at the currency's scale (AED 2 decimals; BHD, KWD and OMR 3 decimals, third decimal never dropped), the comparison with the previous period, and a status colour only when a target exists (no target = no colour, not green). Discounts and Refunds are shown as positive amounts with a minus sign in the bridge, never as negative tiles. *(source: MoM 2026-08-12 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities / contracts/satellite/reporting.yaml#/components/schemas/KpiValue / DI-598)*
- **tile definitions (info popover on each tile)**: Gross sales = issued sales before discounts and refunds, with the footnote saying whether VAT and fees are included. Net revenue = Gross sales minus Discounts minus Refunds, adjusted for cancellations and voids per finance policy. Recognised revenue = posted to revenue accounts in the period: POS sales at sale, online tickets on visit or redemption, gift cards on redemption, annual passes straight-line or per visit, breakage on expiry. Deferred revenue = paid for and not yet earned at period end. *(source: MATRIX 5.12.6 / MoM 2026-08-12 8. Deferred Revenue and Ledger Flow)*
- **revenue chart**: One chart under the tiles, period-selectable: recognised and deferred by month as two series, and a Gross sales to Net revenue bridge (gross, minus discounts, minus refunds, equals net). The bridge uses the waterfall mark; never stack gross and net in one bar. *(source: DI-260 / MoM 2026-08-12 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*
- **where the money stands**: A strip of five sources (POS, Gateway, Bank, Wallet, Ledger), each with its total and transaction count, then the variances: each one names the two sources that disagree, the amount and the likely cause ("Gateway vs Ledger, short AED 500.00, likely a refund not yet settled"). No variance reads "Balanced". The variance is the answer; four balanced totals with no comparison is not a reconciliation. *(source: contracts/spine/finance.yaml#/components/schemas/UnifiedReconciliation / DI-268)*
- **tax documents**: Three small counts: Tax invoices issued, Credit memos (count and value), E-invoice transmissions failed. Failed is red above zero and links to the transmission log. Use "Credit memo", not "Tax credit note", until the label is decided. *(source: contracts/spine/finance.yaml#listTaxInvoices / contracts/spine/finance.yaml#listCreditMemos / contracts/spine/finance.yaml#listEInvoiceTransmissions)*
- **freshness**: "As of 09:40 · Updated 40 sec ago" under the title; a stale banner when any value comes back stale. Do not promise a refresh faster than 30 seconds per tile. *(source: MATRIX 8.7.22 / contracts/satellite/reporting.yaml#/components/schemas/DashboardTile)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **drill from a tile**: Net revenue opens year, month, day, channel, transaction list, then the order; Recognised revenue opens the revenue account's ledger entries (Admissions revenue is BO-1082). Drill only where a real hierarchy exists; a 10,000-row day pages and never freezes. *(source: DI-709 / DI-710)*
- **Export**: PDF or Excel of the view as filtered, with the filter values printed in the header. Needs the export permission. *(source: contracts/shared/permissions.yaml#/components/schemas/Permission / DI-019)*

**Data it reads**: `getKpiValues` (onLoad, Finance KPIs against target); `getUnifiedReconciliation` (onLoad, Where the money stands); `listTaxInvoices` (onLoad, List tax invoices); `listCreditMemos` (onLoad, List credit memos); `listEInvoiceTransmissions` (onLoad, E-invoicing transmission log and failures); `listDashboards` (onLoad, The P16 Finance standard dashboard the link card opens …)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ANL-072` Finance Dashboard: *Open the Finance dashboard*; carries `legalEntityId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The finance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the finance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No finance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the finance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **the recognition run for the period has not completed**: Recognised and Deferred tiles say "Recognition for September not yet run" instead of showing a low number. *(source: contracts/spine/finance.yaml#/components/schemas/PeriodCloseResult)*
- **the legal entity trades in two currencies**: One figure per currency on each tile, never a cross-currency sum. *(source: contracts/spine/finance.yaml#/components/schemas/Settlement / contracts/spine/finance.yaml#/components/schemas/DeferredRevenueReport)*
- **user can view reports but not the ledger**: The money-position strip shows "Not available with your access" in place of zeros; finance users see only finance; a role with Finance hidden never sees this page in navigation. *(source: DI-248 / DI-387 / contracts/spine/finance.yaml#getUnifiedReconciliation)*
- **the period was closed and later reopened**: A banner "Restated: September reopened on 6 Oct by Omar Haddad" because issued figures have changed. *(source: contracts/spine/finance.yaml#/components/schemas/FiscalPeriod / F13 step 6)*

#### Consistency with other screens

- Match `P16 ANL-013 Revenue Pulse, ANL-002 Sales Revenue & Channel, ANL-005 Cost Margin & Profitability`: Same KPI codes and the same labels for gross, net and refunds; DI-721 wants one consolidated reporting area, so this is the Finance standard dashboard of that area, reached from Orders & Money.
- Match `BO-076 Revenue Recognition`: The deferred balance must equal getDeferredRevenue for the same as-at date and venue.
- Match `BO-043 Daily Reconciliation`: Same variance sentence ("between Gateway and Ledger") and the same source names.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue: Aquaventure Waterpark, Dubai
legalEntity: UAE01 · Aquaventure Leisure LLC · TRN 100354829700003 · base currency AED
period: September 2026
tiles:
  grossSales: AED 4,812,450.00 (excl. VAT 5%)
  discounts: AED 312,600.00
  refunds: AED 96,240.00
  netRevenue: AED 4,403,610.00
  recognisedRevenue: AED 3,968,210.00
  deferredRevenue: AED 1,742,380.00 at 30 Sep (annual passes 1,104,500.00; dated tickets not yet visited 563,880.00;
    gift cards 74,000.00)
moneyPosition:
- POS AED 1,284,320.50 · 6,912 transactions
- Gateway (Network International) AED 3,119,289.50 · 18,406
- Ledger AED 4,403,610.00
- 'Variance: Gateway vs Ledger, short AED 500.00, likely a refund issued 30 Sep and settled 1 Oct'
taxDocuments: Tax invoices 25,318 · Credit memos 412 (AED 96,240.00) · E-invoice transmissions failed 3
bahrainVariant: 'Dilmun Waterpark, Bahrain: Net revenue BHD 182,406.125; Deferred BHD 41,230.750'
freshness: As of 09:40 · Updated 40 sec ago
```

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `getUnifiedReconciliation` → `LEDGER_VIEW` (read) · staff
- `listTaxInvoices` → `LEDGER_VIEW` (read) · staff, guest
- `listCreditMemos` → `LEDGER_VIEW` (read) · staff, guest
- `listEInvoiceTransmissions` → `LEDGER_VIEW` (read) · staff
- `listDashboards` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Finance dashboard: gross, net, recognised and deferred revenue and refunds, with charts selectable by period. Allam's screens are a base for TICVAI's design, not a template to copy. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-260)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-1081` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS163 TICVAI Finance Backend Structure Reference v1.0 Board 1.dc.html#bo-1081`
- Workshop pack: TICVAI Finance Backend Structure Reference v1.0.pdf board 1
- Flow F303 *TICVAI Finance Backend Structure Reference v1.0 board 1: Finance Dashboard*, step 1: Opens Finance Dashboard → Finance Dashboard
- Flow F303 branch at step 1 (expected): when Nothing has been set up on Finance Dashboard yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F303 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (41 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-1081?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ANL-072`.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 3 decision(s) taken on this screen are drawn as decided, not as the old default.
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

### In P08 · Orders & Money

- AI-assisted reporting for accountants/finance managers is phase two; phase-one finance screens do not include it. *(agreed · MoM 12 Aug 2026, 6. Finance & Ledger Architecture Overview · DI-278)*
- Financial reports generated automatically: P&L (revenue per category less cost of sales), balance sheet, trial balance and ledger view, cash flow, revenue and deferred-revenue analytics, site-wise revenue; plus daily/weekly/monthly finance summaries. *(agreed · MoM 12 Aug 2026, 21. Financial Reporting (P&L, Balance Sheet, Trial Balance) · DI-276)*
- Legal entities view lists all tenant sites with country, currency and active/inactive status. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-261)*
- Allam: Bulk QR option — for partners with no technical capability, the platform generates a bulk batch of tickets (e.g. 5,000) with a validity window, delivered as QR codes (e.g. CSV) for the partner to import and resell. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-135)*
- Full card numbers are never stored or shown; only a masked representation (e.g. last four digits) so the user can identify which card was used. *(agreed · MoM 31 Jul 2026, 10. Compliance & Data Protection · DI-069)*

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null},{"name":"module","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"getUnifiedReconciliation": {"method":"GET","path":"/reconciliation/unified","contract":"finance","summary":"Every money source against the ledger, in one view","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":true},{"name":"to","in":"query","required":true}],"requestBody":null,"responds":"UnifiedReconciliation"},
"listCreditMemos": {"method":"GET","path":"/credit-memos","contract":"finance","summary":"Credit memos issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"taxInvoiceId","in":"query","required":null},{"name":"refundId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDashboards": {"method":"GET","path":"/dashboards","contract":"reporting","summary":"List dashboards","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":false},{"name":"includeArchived","in":"query","required":false}],"requestBody":null,"responds":"Dashboard"},
"listEInvoiceTransmissions": {"method":"GET","path":"/e-invoicing/transmissions","contract":"finance","summary":"What was sent to the e-invoicing provider, and what came back","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"documentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxInvoices": {"method":"GET","path":"/tax-invoices","contract":"finance","summary":"Tax invoices issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"orderId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"invoiceType","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreateDashboardRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","module","tiles"],"properties":{"name":{"type":"string","maxLength":200},"module":{"$ref":"#/components/schemas/common::ModuleKey","description":"**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid","description":"Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"},"isShared":{"type":"boolean","default":false},"tiles":{"type":"array","minItems":1,"maxItems":24,"items":{"$ref":"#/components/schemas/DashboardTile"}}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"FinCreditMemo": {"x-ticvai-persistence":"ledger.credit_memo + ledger.credit_memo_line","type":"object","description":"5.7.94. **A tax credit note against one tax invoice**, with its own series. Never edited.","required":["id","creditMemoNumber","taxInvoiceId","kind","reason","legalEntityId","issuedAt","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"creditMemoNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's credit memo series, in sequence without gaps."},"taxInvoiceId":{"type":"string","format":"uuid"},"taxInvoiceNumber":{"type":"string","readOnly":true},"kind":{"type":"string","enum":["full","partial"]},"reason":{"type":"string","enum":["refund","cancellation","priceAdjustment","returnOfGoods","billingError","other"]},"refundId":{"type":"string","format":"uuid","nullable":true},"cancelledOrderId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid"},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"legalFxRate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"nullable":true,"readOnly":true,"description":"The invoice's own `legalFxRate`, never today's (CHG-FIN-011)."},"invoiceSupplyValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"**The value of the supply shown on the tax invoice** (Executive Regulation Art. 60(1)(e)), adjusted by any earlier credit note on the same invoice. With `correctedSupplyValue` and `netAmount` (the difference) and `taxAmountInLegalCurrency` (the tax on the difference in AED), the four figures the law requires (CHG-FIN-011)."},"correctedSupplyValue":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The correct value of the supply after this credit note (Art. 60(1)(e))."},"supplierName":{"type":"string","readOnly":true,"description":"Snapshot of the legal entity at issue, as on the invoice (Art. 60(1)(b))."},"supplierAddress":{"type":"string","nullable":true,"readOnly":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true,"readOnly":true},"buyerName":{"type":"string","nullable":true,"readOnly":true,"description":"The recipient as on the invoice; name, address and TRN where they are registered (Art. 60(1)(c))."},"buyerAddress":{"type":"string","nullable":true,"readOnly":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true,"description":"The brief explanation of why the credit note was issued, printed on it (Art. 60(1)(f)); the reason's own wording when no note is given (CHG-FIN-011)."},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinCreditMemoLine"}},"scopePath":{"type":"string","readOnly":true}}},
"FinCreditMemoLine": {"type":"object","required":["invoiceLineNumber","netAmount","taxAmount","grossAmount"],"properties":{"invoiceLineNumber":{"type":"integer","minimum":1},"description":{"type":"string","maxLength":500},"quantity":{"type":"number","nullable":true},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxRate":{"type":"number"},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FinEInvoiceTransmission": {"x-ticvai-persistence":"ledger.einvoice_transmission","type":"object","description":"6.1.1. One attempt to send one tax document to the provider, and its answer.","required":["id","documentKind","documentId","legalEntityId","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"documentKind":{"type":"string","enum":["taxInvoice","creditMemo"]},"documentId":{"type":"string","format":"uuid"},"documentNumber":{"type":"string"},"legalEntityId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid","nullable":true},"mode":{"type":"string","enum":["test","live"]},"status":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"payloadHash":{"type":"string","nullable":true,"description":"SHA-256 of the document as sent, so a resend can be shown to be the same document."},"providerMessageId":{"type":"string","nullable":true},"attempt":{"type":"integer","minimum":1},"errorCodes":{"type":"array","items":{"type":"string"}},"errorMessage":{"type":"string","nullable":true},"sentAt":{"type":"string","format":"date-time","nullable":true},"answeredAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true}}},
"FinEInvoiceTransmissionStatus": {"type":"string","description":"6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.","enum":["notRequired","queued","sent","accepted","rejected","failed"]},
"FinTaxCategory": {"type":"string","description":"How a line is treated for VAT. Taken from the tax code the line was posted with.","enum":["standardRated","zeroRated","exempt","outOfScope","reverseCharge"]},
"FinTaxInvoice": {"x-ticvai-persistence":"ledger.tax_invoice + ledger.tax_invoice_line","type":"object","description":"5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.","required":["id","invoiceNumber","invoiceType","status","legalEntityId","issuedAt","supplyDate","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"invoiceNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."},"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"status":{"$ref":"#/components/schemas/FinTaxInvoiceStatus"},"legalEntityId":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"orderIds":{"type":"array","items":{"type":"string","format":"uuid"}},"supplierName":{"type":"string"},"supplierAddress":{"type":"string","nullable":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest the orders belong to; the key a guest's own reads filter on."},"buyerName":{"type":"string","nullable":true},"buyerAddress":{"type":"string","nullable":true},"buyerCountryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true},"customerAccountId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"supplyDate":{"type":"string","format":"date","description":"The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs. **In the UAE the converted amounts use the UAE Central Bank rate at the date of supply** (Decree-Law Art. 69) and the rate is printed (`legalFxRate`, Executive Regulation Art. 59(1)(k)); CHG-FIN-011."},"legalCurrency":{"type":"string","pattern":"^[A-Z]{3}$","readOnly":true,"description":"The legal entity's currency (AED in the UAE), in which the law requires the tax and the gross amount (CHG-FIN-011)."},"grossAmountInLegalCurrency":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The gross amount payable in the legal currency (Executive Regulation Art. 59(1)(j); for a simplified invoice the total consideration, Art. 59(2)(e)). Equal to `grossAmount` when the invoice is in the legal currency (CHG-FIN-011)."},"legalFxRate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"nullable":true,"readOnly":true,"description":"Units of the legal currency per one unit of `currency`, printed with the tax where the invoice is not in the legal currency (Art. 59(1)(k)). Null when it is (CHG-FIN-011)."},"legalFxRateSource":{"allOf":[{"$ref":"#/components/schemas/FxRateSource"}],"nullable":true,"readOnly":true,"description":"`uaeCentralBank` for a UAE legal entity (Decree-Law Art. 69)."},"paidCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"Where the guest paid in a currency they selected (`orders.Order.chargeCurrency`, CHG-FIN-001), printed as payment information with `paidAmount` and the charge rate. The invoice itself is in the base currency, so the AED amounts the law requires are the invoice's own figures (CHG-FIN-011)."},"paidAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"What the guest paid in `paidCurrency` (`orders.Order.chargeTotal`)."},"reverseChargeStatement":{"type":"string","nullable":true,"readOnly":true,"description":"Where the recipient must account for the tax, the statement saying so and the Decree-Law provision (Art. 59(1)(l), Art. 48). Null otherwise (CHG-FIN-011)."},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"languages":{"type":"array","items":{"type":"string"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The PDF rendered at issue; read through getTaxDocumentRendition."},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null where the platform issued it."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinTaxInvoiceLine"}},"taxSummary":{"type":"array","x-ticvai-persisted":false,"description":"VAT per rate and category, summed from the lines for the response.","items":{"type":"object","properties":{"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxRate":{"type":"number"},"taxableAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."}}},
"FinTaxInvoiceLine": {"type":"object","description":"One line as it was sold and taxed. Amounts are in the invoice currency.","required":["lineNumber","description","quantity","netAmount","taxAmount","grossAmount","taxCategory"],"properties":{"lineNumber":{"type":"integer","minimum":1},"orderId":{"type":"string","format":"uuid"},"orderLineId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string","maxLength":500},"quantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true},"taxRate":{"type":"number","minimum":0,"maximum":100},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmountInLegalCurrency":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"description":"The amount payable for the line in the legal currency (AED), Executive Regulation Art. 59(1)(h); equal to `grossAmount` on an invoice in the legal currency (CHG-FIN-011)."}}},
"FinTaxInvoiceStatus": {"type":"string","description":"`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).","enum":["issued","partiallyCredited","fullyCredited","superseded"]},
"FinTaxInvoiceType": {"type":"string","description":"5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.\n**When a simplified tax invoice is allowed in the UAE** (research 2 October 2026, CHG-FIN-011; Executive Regulation, Cabinet Decision 52 of 2017 as amended, Art. 59(5)): the recipient is not VAT-registered, or is registered and the consideration does not exceed AED 10,000, and the reverse charge does not apply. Otherwise the invoice is `full`. Both kinds carry the title \"Tax Invoice\" (Art. 59(1)(a), 59(2)(a)); a simplified one is issued on the date of supply (Art. 59(13)(1)), a full one within 14 days (Decree-Law Art. 67(1)).","enum":["simplified","full","consolidated"]},
"FxRateSource": {"type":"string","description":"**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.","enum":["manual","uaeCentralBank","ecb","openExchangeRates","cardScheme","provider"]},
"FxRateValue": {"x-ticvai-persistence-column":"numeric(18,6)","type":"string","pattern":"^\\d+(\\.\\d{1,6})?$","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"UnifiedReconciliation": {"type":"object","description":"4.2.19. **Four sources and the variances between them.** A view showing each balanced against itself has not reconciled anything.\n","properties":{"from":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"to":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"sources":{"type":"array","items":{"type":"object","properties":{"source":{"type":"string","enum":["pos","gateway","bank","wallet","ledger"]},"providerName":{"type":"string","nullable":true},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"transactionCount":{"type":"integer"}}}},"variances":{"type":"array","description":"**Where two sources disagree, named.** A discrepancy is usually the gap between two of them rather than inside one, and *\"out by 240\"* without saying between what is not actionable.\n","items":{"type":"object","properties":{"between":{"type":"array","description":"The two sources that disagree, as named in `sources[].source`.","minItems":2,"maxItems":2,"items":{"type":"string","enum":["pos","gateway","bank","wallet","ledger"]}},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"likelyCause":{"type":"string","nullable":true}}}}}}
}
```
