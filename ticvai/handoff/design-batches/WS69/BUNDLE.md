# WS69 — Unified BI Reporting and AI Analytics Platform board 4

**10 screens · 13 operations · 15 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `PERMISSION_MANAGE, PERMISSION_VIEW, REPORT_EXPORT, REPORT_SCHEDULE, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
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

### Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management)

Platform Foundation is everything the apps stand on. Five apps each have one door: the guest app and website (WEB-016, GST-042: a six-digit code to email or mobile, a password, Apple or Google, UAE Pass; never enterprise SSO), the till (POS-000: employee number and PIN, recent operators as tiles; the kitchen display is the same app), the staff handheld and scanner (EMP-001, SCN-001), Venue Management (SUP-001, the single door for the back office P08, the CMS P13, analytics P16 and the support desk P12) and TICVAI Control (ADM-001 for TICVAI's own platform operators, PTR-001 for partner users; the developer portal P14 and the sign-up P17 belong to this app too). A second factor is required by permission, not by role or device: ROLE_MANAGE, LEDGER_APPROVE and every PLATFORM_* permission, plus any the tenant adds; so a cashier never sees it and a platform operator always does. The factor is an authenticator app with an emailed code as fallback; five wrong codes lock step-up for the lockout minutes, never permanently. Guests get two-step verification only at a venue that switched it on. One person holds one session per workstation: a second sign-in is refused and only a supervisor ends the other session. Several roles mean a role prompt; one role goes straight in. The workstation decides the Sale Board, hardware and till identity, never what a person may do. Sensitive actions (refund approval, journal approval, credential reset, partner credit, commission rules, opening a platform-staff grant and 17 more) demand a fresh step-up on the operation itself, asked in place in the action's confirmation; the tenant may raise the strength, never remove it. Permission outcomes are three, never one word: self-authorised (proceeds, audited), escalated (a supervisor PIN in place), refused (the denied state, naming the permission); a missing permission is never an empty table, and a record outside the person's venues is "not found", indistinguishable from absent. The hierarchy is binding (tenant, brand, region, venue, department, sub-department, workstation; outlet beside department for F&B and retail); region owns currency, decimals, time zone, date format and fiscal year; configuration resolves nearest-ancestor across tenant, region and venue (outlet for F&B and retail), venue is the floor and a workstation is assigned a profile, never configured; every configuration screen says which level it writes and what it inherits. Venue Management is one tenant-level surface filtering across the venues in the session's scope. TICVAI's Console runs outside every cell: a platform operator picks a tenant and opens a time-boxed, audited platform-staff grant (with step-up) before any tenant action, and the tenant sees every action in its audit log (ADM-412 is the reference implementation). Approval workflows record authorisations and never perform the action; the requester cannot approve their own request; a venue may tighten and never loosen a rule from above; in-flight …
*(source: screens/P12-support-agent-console.yaml#SUP-001; R135; R126; R167; DI-1072; ADR-0002; ADR-0003; ADR-0004; R184; contracts/spine/identity.yaml#createMfaChallenge; contracts/spine/approvals.yaml#setStepUpPolicy; ADR-0011; ADR-0018; ADR-0029; R098; contracts/spine/approvals.yaml#decideApprovalRequest …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sign in / Sign out | Entering and leaving any app, staff or guest. | Login, Log in, Logon, Logout | screens/P04-point-of-sale.yaml#POS-000 … |
| Authentication code | The staff second factor from the authenticator app (or the emailed fallback). | OTP, 2FA code, token | screens/P09-platform-admin-console.yaml#ADM-001 |
| One-time code | The six-digit code a guest receives to sign in or prove a contact. | OTP, PIN, password | DI-1034; R167 |
| Two-step verification | The guest's optional second factor, asked only at venues that switched it on. | MFA, 2FA | DI-1072 |
| Tenant / Brand / Region / Venue / Department / Outlet | The binding hierarchy levels; region owns currency and dates; outlet is F&B or retail inside a venue. | Client, Customer, Org (for tenant), Site, Park, Property (for venue), Area, Territory (for region) | ADR-0011; ADR-0018 |
| Workstation (back office) / till (operator copy) | A configured device; decides Sale Board, hardware and till identity, never authorisation. | Terminal, Station, POS (for the device), till (for the Deposit Box) | ADR-0002; R156 |
| Sale Board | The configured front end a workstation loads (ticketing, F&B or retail). | Screen, Layout, Menu | ADR-0003 |
| Role | A named, fully configurable grouping of permissions; the seeded five are editable starting points. | Group, Profile | R229 |
| Staff member / Partner user / Platform operator | A tenant's staff principal; a partner's user; a TICVAI employee in the Console. | User (alone), Account, Agent (for venue staff) | F104 step 1; F104 step 4; F104 step 5 |
| Platform-staff grant | The time-boxed, audited access a platform operator opens into one tenant before acting in it. | Impersonation, Support login | R098 |
| Escalate / Refused | Escalate is supervisor approval captured in place; Refused is the denied state that names the permission. | Denied (for an action that can be escalated) | R197 |
| Approve / Reject / Return / Request information | The four decisions on an approval request; Withdraw is the requester's own act and never a rejection. | Accept, Decline, Cancel (for withdraw) | contracts/spine/approvals.yaml#decideApprovalRequest … |
| Subscription / Plan / Module / Licence | TICVAI's commercial relationship with a tenant, its plan, the modules it licenses and the limits. | Membership (that is the guest's pass) | R214 |
| Membership / Annual pass | A guest's pass product and its holder (BO-284 to BO-303). | Subscription (that is the tenant's TICVAI plan) | screens/P08-venue-back-office.yaml#BO-284 |
| Sandbox client / Production client | A developer's own test credential; a TICVAI-issued live credential after certification. | Test key, Live key, API key (without environment) | DI-927 |
| Asset (DAM) / Media (ticket) | A digital file in the library; ticket media is a wristband or card carrying entitlements. Never mix them. | Media (for a library asset) | contracts/satellite/assets.yaml#searchMedia … |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `ANL-041` | Reporting Governance Command Center | B–D | 0 | 36 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-042` | Report Scheduler | B–D | 23 | 0 | 5 | 4 | 1 | 0 | — | notStarted (—) |
| `ANL-043` | Subscription Manager | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-044` | Distribution & Delivery Configuration | B–D | 14 | 0 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-045` | Export & Download Center | B–D | 0 | 22 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `ANL-046` | Report API & Data Delivery Manager | B–D | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-047` | Report Access & Sharing Control | B–D | 39 | 24 | 6 | 7 | 0 | 0 | — | notStarted (—) |
| `ANL-048` | Delivery Monitoring & Failure Management | B–D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-049` | Report Audit Trail & Compliance | B–D | 16 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-050` | Retention, Archive & Governance Policy | B–D | 14 | 0 | 5 | 1 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-041, ANL-043, ANL-045 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-041` Reporting Governance Command Center

**Provide administrators with a centralized overview of reporting operations, governance, distribution and compliance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/reporting-governance-command-center-anl-041` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The reporting administrator's overview: what runs, what was delivered, what failed, what left the platform with personal data in it. The thing to get right: lead with failures and personal-data deliveries, because a report that silently stopped arriving is worse than one that never existed; and several pack counters have no source yet, so draw them as pending rather than as zeros.

**Known correction pending (do not draw the wrong version)**

- **Exports Today, Large Exports, Pending Approvals and API Report Requests have no source** Why: There is no operation listing exports, no approval for reports or dashboards, and no record of API report calls. *(source: contracts/satellite/reporting.yaml#getReportExport / contracts/spine/approvals.yaml#ApprovalKind / screens/P16-venue-analytics.yaml#ANL-041; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listReportDeliveries` ?from |
| Failed only | toggle | — | — | `listReportDeliveries` ?failedOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every reporting governance** (data table)

| Shows | Format | Notes |
|---|---|---|
| Active reports | text | not in the schema: `Active Reports` |
| Published dashboards | text | not in the schema: `Published Dashboards` |
| Active schedules | text | not in the schema: `Active Schedules` |
| Active subscriptions | text | not in the schema: `Active Subscriptions` |
| Reports generated today | text | not in the schema: `Reports Generated Today` |
| Successful deliveries | text | not in the schema: `Successful Deliveries` |
| Failed deliveries | text | not in the schema: `Failed Deliveries` |
| Pending approvals | text | not in the schema: `Pending Approvals` |
| Exports today | text | not in the schema: `Exports Today` |
| API report requests | text | not in the schema: `API Report Requests` |
| Shared reports | text | not in the schema: `Shared Reports` |
| Governance exceptions | text | not in the schema: `Governance Exceptions` |
| Recently generated reports | text | not in the schema: `Recently generated reports` |
| Failed reports | text | not in the schema: `Failed reports` |
| Recently shared reports | text | not in the schema: `Recently shared reports` |
| Large exports | text | not in the schema: `Large exports` |
| Permission changes | text | not in the schema: `Permission changes` |
| Scheduled report changes | text | not in the schema: `Scheduled-report changes` |

**The selected reporting governance** (detail panel): The pack groups this record's detail under its own headings: “Show health by”.

| Shows | Format | Notes |
|---|---|---|
| Active reports | text | not in the schema: `Active Reports` |
| Published dashboards | text | not in the schema: `Published Dashboards` |
| Active schedules | text | not in the schema: `Active Schedules` |
| Active subscriptions | text | not in the schema: `Active Subscriptions` |
| Reports generated today | text | not in the schema: `Reports Generated Today` |
| Successful deliveries | text | not in the schema: `Successful Deliveries` |
| Failed deliveries | text | not in the schema: `Failed Deliveries` |
| Pending approvals | text | not in the schema: `Pending Approvals` |
| Exports today | text | not in the schema: `Exports Today` |
| API report requests | text | not in the schema: `API Report Requests` |
| Shared reports | text | not in the schema: `Shared Reports` |
| Governance exceptions | text | not in the schema: `Governance Exceptions` |
| Recently generated reports | text | not in the schema: `Recently generated reports` |
| Failed reports | text | not in the schema: `Failed reports` |
| Recently shared reports | text | not in the schema: `Recently shared reports` |
| Large exports | text | not in the schema: `Large exports` |
| Permission changes | text | not in the schema: `Permission changes` |
| Scheduled report changes | text | not in the schema: `Scheduled-report changes` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **headline counters (available)**: Active schedules and paused schedules; schedules with consecutive failures; deliveries today, delivered and failed; deliveries that contained personal data; external recipients. Failed and personal-data counters first, linking to ANL-048 and ANL-049. *(source: contracts/satellite/reporting.yaml#ReportSchedule / contracts/satellite/reporting.yaml#ReportDelivery / contracts/satellite/reporting.yaml#listReportDeliveries)*
- **headline counters (pending)**: Active reports and published dashboards (no count operation; lists only), pending approvals (no report or dashboard approval), exports today and large exports (no export list), API report requests (no source), governance exceptions (undefined). Draw greyed with "Not yet available". *(source: contracts/satellite/reporting.yaml#listReports / contracts/satellite/reporting.yaml#getReportExport)*
- **recent lists**: Failed deliveries (newest first, with reason), recently changed schedules, permission changes from the platform audit trail. *(source: contracts/satellite/reporting.yaml#listReportDeliveries / contracts/spine/tenancy.yaml#listAuditRecords)*

**Data it reads**: `listReportSchedules` (onLoad, What runs when); `listReportDeliveries` (onLoad, What arrived and what did not)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*; carries `reportId`
- → `ANL-050` Retention, Archive & Governance Policy: *Retention, Archive & Governance Policy*
- → `ANL-042` Report Scheduler: *Report Scheduler*
- → `ANL-043` Subscription Manager: *Subscription Manager*
- → `ANL-044` Distribution & Delivery Configuration: *Distribution & Delivery Configuration*
- → `ANL-045` Export & Download Center: *Export & Download Center*
- → `ANL-046` Report API & Data Delivery Manager: *Report API & Data Delivery Manager*
- → `ANL-047` Report Access & Sharing Control: *Report Access & Sharing Control*
- → `ANL-048` Delivery Monitoring & Failure Management: *Delivery Monitoring & Failure Management*
- → `ANL-049` Report Audit Trail & Compliance: *Report Audit Trail & Compliance*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reporting governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reporting governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reporting governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reporting governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Venue-level user opens the board**: Delivery data needs tenant-level access; a venue user sees schedules only and a note naming the missing access. *(source: contracts/satellite/reporting.yaml#listReportDeliveries / contracts/satellite/reporting.yaml#listReportSchedules)*

#### Consistency with other screens

- Match `ANL-061`: Same health words and counters style as the BI administration command centre.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
counters:
  activeSchedules: 37
  paused: 4
  failingSchedules: 2
  deliveredToday: 112
  failedToday: 3
  withPersonalData: 6
  externalRecipients: 9
failed:
- report: Daily closing - Aquaventure
  route: Email
  at: 01 Oct 2026 07:00
  reason: Mailbox full - finance@aquaventure.ae
  retries: 2
- report: F&B sales by outlet
  route: SFTP
  at: 01 Oct 2026 06:30
  reason: SFTP login rejected
  retries: 3
```

#### Permissions

- `listReportSchedules` → `REPORT_VIEW_VENUE` (operate) · staff
- `listReportDeliveries` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-041` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-041`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 1: Opens Reporting Governance Command Center → Provide administrators with a centralized overview of reporting operations, governance, distribution and compliance.
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F178 branch at step 1 (expected): when Nothing has been set up on Reporting Governance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F178 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-041?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-050`, `ANL-042`, `ANL-043`, `ANL-044`, `ANL-045`, `ANL-046`, `ANL-047`, `ANL-048`, `ANL-049`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-042` Report Scheduler

**Allow authorized users to automatically generate reports according to defined schedules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Frequency Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/report-scheduler-anl-042` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Schedules a report to run and be sent, e.g. the client's "daily closing sales report emailed each morning to finance". A schedule runs under its owner's permissions, not the recipients', so it is a standing grant of whatever the owner can see; the screen must make that plain. The thing to get right: the frequencies the platform supports are not the pack's list.

**Known correction pending (do not draw the wrong version)**

- **Frequencies Once, Hourly, Yearly and Custom; fields Start Date, End Date, Time Zone, Run immediately, Retry on failure, Maximum retries, Timeout, Skip if stale, Wait for source refresh, Report Version** Why: Cadence supports daily, weekly, monthly, quarterly, shift close and period close only; the time zone is always the venue's and read-only; the other fields do not exist (a schedule runs the report's current version). *(source: contracts/satellite/reporting.yaml#Cadence / contracts/satellite/reporting.yaml#CreateReportScheduleRequest / screens/P16-venue-analytics.yaml#ANL-042; Finance, Ledger & Tax · Reporting & Analytics)*
- **The screen declares only list and create** Why: Pause, resume, amend and delete exist and the scheduler cannot work without them. *(source: contracts/satellite/reporting.yaml#updateReportSchedule / contracts/satellite/reporting.yaml#deleteReportSchedule; Finance, Ledger & Tax · Reporting & Analytics)*
- **Recipient groups and email templates** Why: The client wants schedules to defined recipient groups using configurable email templates; Recipient is one person or address and nothing holds a template. *(source: DI-714 / MoM 2026-09-08 4.8 Report Distribution & Scheduling / contracts/satellite/reporting.yaml#Recipient; Finance, Ledger & Tax · Reporting & Analytics)*
- **dayOfWeek 0 to 6 does not say which day is 0** Why: UAE weeks start on Monday; an off-by-one sends the weekly report on the wrong day. *(source: contracts/satellite/reporting.yaml#Cadence; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Do recipient groups (Finance team, Operations leads) and email templates join the schedule?** → Drawn default accepted: Pick people and addresses individually; show the default email text read-only. *(decided by Chinmay, 2026-10-02; DEC-343 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **How does a scheduled run express "the previous day" when parameters are fixed values?** → Drawn default accepted: Draw relative presets; flag pending. *(decided by Chinmay, 2026-10-02; DEC-344 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Schedule Name | select field | — | — | — | — | — | — |
| Report | select field | — | — | — | — | — | — |
| Report Version | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Start Date | select field | — | — | — | — | — | — |
| End Date | select field | — | — | — | — | — | — |
| Time | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| Frequency | select field | — | — | — | — | — | — |
| Run immediately | select field | — | — | — | — | — | — |
| Retry on failure | select field | — | — | — | — | — | — |
| Maximum retries | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Skip if source data is stale | text field | — | — | — | — | — | — |
| Wait for source refresh | text field | — | — | — | — | — | — |
| Once | select field | — | — | — | — | — | — |
| Hourly | select field | — | — | — | — | — | — |
| Daily | select field | — | — | — | — | — | — |
| Weekly | select field | — | — | — | — | — | — |
| Monthly | select field | — | — | — | — | — | — |
| Quarterly | select field | — | — | — | — | — | — |
| Yearly | select field | — | — | — | — | — | — |
| Custom | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **cadence.frequency**: Daily, Weekly, Monthly, Quarterly, At shift close, At period close. Daily needs a time; weekly a day and time; monthly a day of the month and time (31 runs on the month's last day); quarterly a day and time in the first month of each quarter; the two event cadences need nothing else. Once, Hourly, Yearly and Custom are not supported. *(source: contracts/satellite/reporting.yaml#Cadence / R158)*
- **timeOfDay, timeZone**: Time is entered in the venue's time zone; the zone is shown, not chosen ("07:00 Gulf Standard Time"). Heavy schedules are spread across the window, so say "around 07:00". *(source: contracts/satellite/reporting.yaml#Cadence / contracts/satellite/reporting.yaml#createReportSchedule)*
- **parameters**: The report's prompts, fixed for every run; date prompts offered as "the previous day", "the previous week" (see decisions). *(source: contracts/satellite/reporting.yaml#CreateReportScheduleRequest)*
- **recipients**: People in the tenant, email addresses, SFTP or webhook destinations; at least one. Recipients outside the tenant are flagged "External". *(source: contracts/satellite/reporting.yaml#Recipient)*
- **format**: PDF, Excel, CSV or JSON. *(source: contracts/satellite/reporting.yaml#ExportFormat)*
- **includePersonalData**: Off by default; offered only to an owner with personal-data export permission; turning it on shows "Recorded in the audit trail". *(source: contracts/satellite/reporting.yaml#CreateReportScheduleRequest / contracts/shared/permissions.yaml#/components/schemas/Permission)*
- **skipIfEmpty (shown as "Don't send an empty report")**: On by default; an empty report every morning trains people to ignore it. *(source: contracts/satellite/reporting.yaml#CreateReportScheduleRequest)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **owner banner**: "Runs with your access. Recipients receive everything you can see in this report." *(source: contracts/satellite/reporting.yaml#ReportSchedule)*
- **schedule list**: Name, report, cadence in words ("Every day around 07:00"), next run, last run and its status, consecutive failures, Paused badge. *(source: contracts/satellite/reporting.yaml#ReportSchedule)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Schedule**: Creates the schedule; a cadence missing a field it needs, or sending one it does not take, is refused with the field named; no recipients is refused. *(source: contracts/satellite/reporting.yaml#createReportSchedule)*
- **Pause, Resume, Edit, Delete**: Exist in the contract (cadence, recipients, format, pause); see correction - this screen does not declare them. *(source: contracts/satellite/reporting.yaml#updateReportSchedule / contracts/satellite/reporting.yaml#deleteReportSchedule)*

**Data it reads**: `listReportSchedules` (onLoad, Schedules)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report scheduler configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report scheduler untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report scheduler configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Invalid cadence (a field its frequency needs is missing, or one it does not take is sent, audit R158), or no recipients |

#### Edge cases to draw

- **The owner loses access or leaves**: The schedule keeps the owner's (now reduced) access; flag schedules whose owner is inactive for reassignment (see decisions). *(source: contracts/satellite/reporting.yaml#ReportSchedule)*
- **The report is retired**: A report with an active schedule cannot be retired; the schedule list shows which reports are pinned by schedules. *(source: contracts/satellite/reporting.yaml#deleteReport)*

#### Consistency with other screens

- Match `ANL-043`: A subscription can point at a schedule; one schedule can serve several subscriptions.
- Match `BO-061`: The venue back-office Scheduled Reports screen uses the same schedule operations and must use the same cadence words.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- name: Daily closing - finance
  report: Daily closing - Aquaventure
  cadence: Every day around 07:00 GST
  parameters: Business date - previous day
  recipients:
  - Fatima Al Mansoori
  - finance@aquaventure.ae
  format: PDF
  skipIfEmpty: true
  nextRun: 02 Oct 2026 07:00
- name: Shift close - cash variance
  report: Shift summary
  cadence: At shift close
  recipients:
  - Omar Haddad
  format: PDF
- name: Bahrain weekly sales
  report: Sales by channel
  cadence: Every Sunday around 08:00 AST
  recipients:
  - sales@dilmun.bh
  format: Excel
  note: BHD amounts keep 3 decimals
```

#### Permissions

- `listReportSchedules` → `REPORT_VIEW_VENUE` (operate) · staff
- `createReportSchedule` → `REPORT_SCHEDULE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.14 | The system should have scheduling of report generation and delivery to web address location or list of email addresses. | Retail POS | CONTRACTED | `createReportSchedule` |
| 8.7.15 | System shall support report scheduling. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 8.7.16 | System shall support report subscriptions. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 8.7.17 | System shall support report sharing. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reports can be scheduled to defined recipient groups - e.g. a daily closing/summary sales report or shift-closing report emailed each morning to operations, finance or sales - using configurable email templates with the report attached. *(client request · MoM 8 Sep 2026, 4.8 Report Distribution & Scheduling · DI-714)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-042` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-042`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 2: Works in Report Scheduler → Allow authorized users to automatically generate reports according to defined schedules.

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-042?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-043` Subscription Manager

**Allow users and administrators to subscribe recipients to dashboards, reports and KPI summaries.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/subscription-manager-anl-043` |

**Known gaps.** **Subscription Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Who receives which report, in what format, by which route, and under whose access. A subscription is not a schedule: the schedule says when, the subscription says who and how, and one schedule can feed several. The thing to get right: personal data going out, especially to external addresses, is visible on every row, because someone will ask about it later.

**Known correction pending (do not draw the wrong version)**

- **No way to edit, deactivate or remove a subscription** Why: Only list and create exist; a subscription cannot be stopped from the platform. *(source: contracts/satellite/reporting.yaml#listReportSubscriptions / contracts/satellite/reporting.yaml#createReportSubscription; Finance, Ledger & Tax · Reporting & Analytics)*
- **Subscriptions to dashboards and KPI summaries** Why: The screen's purpose names them; a subscription references a report only. *(source: screens/P16-venue-analytics.yaml#ANL-043 / contracts/satellite/reporting.yaml#ReportSubscription; Finance, Ledger & Tax · Reporting & Analytics)*
- **Two recipient models** Why: A schedule carries its own recipients, format and personal-data flag, and a subscription carries another set (and different route values) for the same thing. *(source: contracts/satellite/reporting.yaml#CreateReportScheduleRequest / contracts/satellite/reporting.yaml#ReportSubscription; Finance, Ledger & Tax · Reporting & Analytics)*
- **The gap says no write operation and nothing drawable** Why: createReportSubscription is declared and the subscription schema gives a full row. *(source: screens/P16-venue-analytics.yaml#ANL-043; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a subscription without a schedule allowed, and when does it send?** → Drawn default accepted: Require a schedule. *(decided by Chinmay, 2026-10-02; DEC-345 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.
- **Can a recipient unsubscribe themselves from an email link?** → Drawn default accepted: Not drawn. *(decided by Chinmay, 2026-10-02; DEC-346 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **report**: Required. Dashboards and KPI summaries cannot be subscribed to (see correction). *(source: contracts/satellite/reporting.yaml#ReportSubscription)*
- **schedule**: Optional link to an existing schedule; without one the subscription has no timing of its own (see decisions). *(source: contracts/satellite/reporting.yaml#ReportSubscription)*
- **recipients**: A person in the tenant or an email address; addresses outside the tenant are marked External. *(source: contracts/satellite/reporting.yaml#ReportSubscription)*
- **channel (shown as "Send by")**: Email, SFTP, Webhook, In TICVAI (notification centre). *(source: contracts/satellite/reporting.yaml#ReportSubscription)*
- **includesPersonalData**: Needs personal-data export permission; recorded. *(source: contracts/satellite/reporting.yaml#ReportSubscription)*

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create report subscription (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **list**: Report, recipients (count plus first two names), route, format, "Runs as Fatima Al Mansoori", Personal data and External badges, Active or Inactive. Cursor-paged. *(source: contracts/satellite/reporting.yaml#listReportSubscriptions / contracts/satellite/reporting.yaml#ReportSubscription)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Add subscription**: Creates it; the confirmation repeats "Recipients receive what Fatima Al Mansoori can see". *(source: contracts/satellite/reporting.yaml#createReportSubscription)*

**Data it reads**: `listReportSubscriptions` (onLoad, Who receives what)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscription list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscription untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscription yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the subscription are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Personal data to an external address**: Requires an explicit second confirmation naming the address; recorded. *(source: contracts/satellite/reporting.yaml#ReportSubscription)*

#### Consistency with other screens

- Match `ANL-042`: Schedule recipients and subscription recipients must not become two separate lists people maintain (see correction).
- Match `ANL-044`: The route and format chosen here are configured in detail on ANL-044.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- report: Daily closing - Aquaventure
  recipients:
  - Fatima Al Mansoori
  - cfo@aquaventure.ae
  route: Email
  format: PDF
  runsAs: Fatima Al Mansoori
  personalData: false
  active: true
- report: Guest arrivals - VIP
  recipients:
  - concierge@partnerhotel.ae (External)
  route: Email
  format: Excel
  runsAs: Omar Haddad
  personalData: true
  active: true
```

#### Permissions

- `listReportSubscriptions` → `REPORT_VIEW_VENUE` (operate) · staff
- `createReportSubscription` → `REPORT_SCHEDULE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reports can be scheduled to defined recipient groups - e.g. a daily closing/summary sales report or shift-closing report emailed each morning to operations, finance or sales - using configurable email templates with the report attached. *(client request · MoM 8 Sep 2026, 4.8 Report Distribution & Scheduling · DI-714)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-043` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-043`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 4: Works in Subscription Manager → Allow users and administrators to subscribe recipients to dashboards, reports and KPI summaries.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-043?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create report subscription, Cancel.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 4 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-044` Distribution & Delivery Configuration

**Configure how generated reporting content reaches approved recipients or destinations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_SCHEDULE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Define; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/distribution-delivery-configuration-anl-044` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: TICVAI Notification Center, Secure Download, API, External approved destination. Each needs an operation …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Configures how a generated report reaches people: route, format, file and message. The thing to get right: the pack's four "buttons" are delivery routes, not actions, and most of the pack's settings (subject, body template, naming, password, expiry, priority, language) have no field yet; draw what can be stored and keep the rest visibly pending.

**Known correction pending (do not draw the wrong version)**

- **Email subject, body template, file naming, password policy, expiration, delivery priority, language and recipient fields** Why: A subscription holds route, format, recipients and the personal-data flag only. *(source: contracts/satellite/reporting.yaml#ReportSubscription / screens/P16-venue-analytics.yaml#ANL-044; Finance, Ledger & Tax · Reporting & Analytics)*
- **The four channel buttons are drawn as actions with no operation** Why: They are values of the route; there is nothing to call. *(source: contracts/satellite/reporting.yaml#ReportSubscription; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Must reports with personal data go by secure link only, never as an attachment?** → Drawn default accepted: Link only for personal data; attachment allowed otherwise. *(decided by Chinmay, 2026-10-02; DEC-347 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Destination | select field | — | — | — | — | — | — |
| Recipient | select field | — | — | — | — | — | — |
| Format | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| File Naming | select field | — | — | — | — | — | — |
| Password/Security Policy | select field | — | — | — | — | — | — |
| Expiration | select field | — | — | — | — | — | — |
| Delivery Priority | select field | — | — | — | — | — | — |
| Email Subject | select field | — | — | — | — | — | — |
| Email Body Template | select field | — | — | — | — | — | — |
| Attachment | select field | — | — | — | — | — | — |
| Secure Link | select field | — | — | — | — | — | — |
| Branding | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **route (pack buttons Notification Center, Secure Download, API, External approved destination)**: In TICVAI, Email, Webhook, SFTP - a single choice, drawn as a segmented control. *(source: contracts/satellite/reporting.yaml#ReportSubscription)*
- **format**: PDF, Excel, CSV, JSON. *(source: contracts/satellite/reporting.yaml#ReportSubscription)*
- **attachment or secure link**: Exports are produced as signed, expiring download links; personal data should go by link only (see decisions). *(source: contracts/satellite/reporting.yaml#ReportExport)*
- **Time zone**: Not a choice; the venue's zone. *(source: contracts/satellite/reporting.yaml#Cadence)*
- **Branding**: The tenant's white-label logo and colours; "Powered by TICVAI" footer. *(source: MATRIX 6.1.78)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| TICVAI Notification Center (primary button) | navigation or local | — | — | — | — |
| Secure Download (secondary button) | navigation or local | — | — | — | — |
| API (secondary button) | navigation or local | — | — | — | — |
| External approved destination (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **email preview**: Subject and body as the recipient sees them, in English and Arabic (right to left), with the period and "Data as of" in the body. *(source: DI-714 / DI-019)*

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The distribution delivery configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the distribution delivery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No distribution delivery configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `ANL-043`: This is the detail view of a subscription's route and format.
- Match `ANL-038`: The attached PDF is the layout designed there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
route: Email
format: PDF
subject: Daily closing - Aquaventure Waterpark - 30 Sep 2026
body: 'Attached: daily closing for 30 Sep 2026. Data as of 01 Oct 2026 07:00 GST. Net revenue AED 412,860.50.'
subjectAr: الإغلاق اليومي - أكوافنتشر - 30 سبتمبر 2026
```

#### Permissions

- `createReportSubscription` → `REPORT_SCHEDULE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reports can be scheduled to defined recipient groups - e.g. a daily closing/summary sales report or shift-closing report emailed each morning to operations, finance or sales - using configurable email templates with the report attached. *(client request · MoM 8 Sep 2026, 4.8 Report Distribution & Scheduling · DI-714)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-044` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-044`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 6: Works in Distribution & Delivery Configuration → Configure how generated reporting content reaches approved recipients or destinations.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-044?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: TICVAI Notification Center, Secure Download, API, External approved destination.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_SCHEDULE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-045` Export & Download Center

**Provide centralized management of report and dashboard exports. The source matrix requires reporting export to multiple formats, including PDF, Excel, delimited text and XML.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_EXPORT` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `executionId` (navigation), `exportId` (navigation) |
| Route | `/analytics/export-download-center-anl-045` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Where people collect exports and administrators see what data left the platform. Exports are always asynchronous: requested, generating, ready (with a signed link that expires), failed or expired. The thing to get right: personal-data exports are visibly different (who, why, when) and the purpose given is shown; and there is no list of exports to draw from yet.

**Known correction pending (do not draw the wrong version)**

- **No operation lists exports** Why: Exports can be created and read by id only; the centre has no list to show, and the administrator view of what left the platform has no source. *(source: contracts/satellite/reporting.yaml#getReportExport / screens/P16-venue-analytics.yaml#ANL-045; Finance, Ledger & Tax · Reporting & Analytics)*
- **XML in the required formats** Why: Export formats are CSV, Excel, PDF and JSON; XML is missing. *(source: contracts/satellite/reporting.yaml#ExportFormat / MATRIX 6.1.20; Finance, Ledger & Tax · Reporting & Analytics)*
- **Site, Record Count and Completed Time are not on the export** Why: The export holds format, status, size, requester, requested and expiry times; rows come from the execution, venue from the run. *(source: contracts/satellite/reporting.yaml#ReportExport; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **format**: Excel, PDF, CSV, JSON. *(source: contracts/satellite/reporting.yaml#ExportFormat)*
- **includePersonalData, purpose**: Only with personal-data export permission; purpose required (up to 500 characters) when on. *(source: contracts/satellite/reporting.yaml#exportReportResult)*

#### Outputs: what the screen shows and produces

**Shown**

**Every export download** (data table)

| Shows | Format | Notes |
|---|---|---|
| Export ID | text | not in the schema: `Export ID` |
| Report | text | not in the schema: `Report` |
| Requested by | text | not in the schema: `Requested By` |
| Site | text | not in the schema: `Site` |
| Format | text | not in the schema: `Format` |
| Requested time | text | not in the schema: `Requested Time` |
| Completed time | text | not in the schema: `Completed Time` |
| File size | text | not in the schema: `File Size` |
| Record count | text | not in the schema: `Record Count` |
| Status | text | not in the schema: `Status` |
| Expiration | text | not in the schema: `Expiration` |

**The selected export download** (detail panel): The pack groups this record's detail under its own headings: “At minimum”, “Export Status”, “Large Exports”.

| Shows | Format | Notes |
|---|---|---|
| Export ID | text | not in the schema: `Export ID` |
| Report | text | not in the schema: `Report` |
| Requested by | text | not in the schema: `Requested By` |
| Site | text | not in the schema: `Site` |
| Format | text | not in the schema: `Format` |
| Requested time | text | not in the schema: `Requested Time` |
| Completed time | text | not in the schema: `Completed Time` |
| File size | text | not in the schema: `File Size` |
| Record count | text | not in the schema: `Record Count` |
| Status | text | not in the schema: `Status` |
| Expiration | text | not in the schema: `Expiration` |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **export row**: Report, requested by, venue, format, requested at, size, rows (from the run), status, link expiry ("Link expires in 23 h"), Personal data badge with purpose on hover. *(source: contracts/satellite/reporting.yaml#ReportExport / contracts/satellite/reporting.yaml#ReportExecution)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Download**: Shown only while Ready; after expiry, "Export again" re-runs the export of the same result if the result is still kept, otherwise asks to run the report again. *(source: contracts/satellite/reporting.yaml#ReportExport / contracts/satellite/reporting.yaml#ReportExecution)*

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The export download list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the export download untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No export download yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the export download are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Personal data requested without permission**: Refused; the toggle should not have been offered. *(source: contracts/satellite/reporting.yaml#exportReportResult)*
- **Seven years of financial history in one export**: A single run covers the report's longest range (366 days unless set); draw a year picker and say "Export one year at a time". *(source: ADR-0047 / contracts/satellite/reporting.yaml#CreateReportRequest)*

#### Consistency with other screens

- Match `ANL-040`: Same statuses and same export dialog.
- Match `ANL-049`: Personal-data exports appear in the audit trail.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- report: Guest arrivals - VIP
  requestedBy: Omar Haddad
  venue: Aquaventure Waterpark
  format: Excel
  requested: 01 Oct 2026 09:02
  size: 184 KB
  rows: 212
  status: Ready
  expires: in 23 h
  personalData: true
  purpose: Concierge welcome calls for 2 Oct arrivals
- report: Sales by channel
  requestedBy: Rahul Menon
  venue: All my venues
  format: PDF
  requested: 01 Oct 2026 08:40
  status: Generating
```

#### Permissions

- `exportReportResult` → `REPORT_EXPORT` (read) · staff
- `getReportExport` → `REPORT_EXPORT` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.20 | The system should be able to all reporting functions should have export option to multiple file formats; minimum of PDF, Excel, delimited text, and XML. | Retail POS | CONTRACTED | `exportReportResult` |
| 6.1.26 | The system should be able to view/export (as CSV) user data. | Retail POS | CONTRACTED | `exportReportResult` |
| 8.7.18 | System shall support report exports to Excel. | Unified Operations Dashboard | CONTRACTED | `exportReportResult` |
| 8.7.19 | System shall support report exports to PDF. | Unified Operations Dashboard | CONTRACTED | `exportReportResult` |
| 8.7.20 | System shall support report exports through APIs. | Unified Operations Dashboard | CONTRACTED | `exportReportResult` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Report builder provides a library of standard operations/finance reports exportable as PDF or Excel, plus custom reports built drag-and-drop (no SQL) by choosing which data-set fields appear as columns/rows. *(client request · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-708)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-045` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-045`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 8: Works in Export & Download Center → Provide centralized management of report and dashboard exports. The source matrix requires reporting export to multiple formats, including PDF, Excel, delimited text and XML.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-045?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_EXPORT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-046` Report API & Data Delivery Manager

**Allow approved systems to receive reporting information programmatically. This supports the requirement for report export/access through APIs.**

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
| Route | `/analytics/report-api-data-delivery-manager-anl-046` |

**Known gaps.** **Report API & Data Delivery Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Lets an approved external system read reporting data without database access. In the platform this is an API client with the analytics read scope calling the report run, result and export operations, plus webhook or SFTP subscriptions for pushed data. The thing to get right: credentials are managed where every other API client is, not on this screen.

**Known correction pending (do not draw the wrong version)**

- **The screen reads subscriptions but describes API client configuration (API name, consumer, authentication, allowed sites, allowed fields, rate limit, status)** Why: API clients are the public-API client model; allowed sites and fields per consumer have no field anywhere (scope comes from the credential's principal). *(source: contracts/satellite/public-api.yaml#ApiClient / screens/P16-venue-analytics.yaml#ANL-046; Finance, Ledger & Tax · Reporting & Analytics)*
- **The gap says no write operation** Why: True, and correct for this screen; writes belong to the API client screens. *(source: contracts/satellite/public-api.yaml#createApiClient; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| API Name | select field | — | — | — | — | — | — |
| Report/Dataset | select field | — | — | — | — | — | — |
| Consumer/Application | select field | — | — | — | — | — | — |
| Authentication | select field | — | — | — | — | — | — |
| Allowed Sites | select field | — | — | — | — | — | — |
| Allowed Fields | select field | — | — | — | — | — | — |
| Filters | select field | — | — | — | — | — | — |
| Rate Limit | select field | — | — | — | — | — | — |
| Data Format | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **consumers**: API clients that hold the analytics read scope - name, environment (sandbox or production), status, key expiry. *(source: contracts/satellite/public-api.yaml#ApiClient / contracts/satellite/reporting.yaml#listReports / MATRIX 13.3.14)*
- **pushed deliveries**: Subscriptions whose route is webhook or SFTP, with their report and format. *(source: contracts/satellite/reporting.yaml#listReportSubscriptions)*

**Data it reads**: `listReportSubscriptions` (onLoad, API and SFTP delivery)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report api data configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report api data untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report api data configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A consumer asks for another tenant's data**: Impossible by construction; the tenant comes from the credential, never from a parameter. *(source: MATRIX 6.1.78)*

#### Consistency with other screens

- Match `BO-1073`: API Access & OAuth owns client creation, scopes and key rotation; this screen links there.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
consumers:
- name: Aquaventure finance ERP
  environment: Production
  scope: Analytics read
  status: Active
  keyExpires: 14 Sep 2027
pushes:
- report: Daily closing - Aquaventure
  route: SFTP
  format: CSV
  destination: sftp.erp.aquaventure.ae
```

#### Permissions

- `listReportSubscriptions` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-046` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-046`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 10: Works in Report API & Data Delivery Manager → Allow approved systems to receive reporting information programmatically. This supports the requirement for report export/access through APIs.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-046?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-047` Report Access & Sharing Control

**Provide centralized security for reports, dashboards and analytical information. The matrix specifically requires reporting access based on group rights, operating-area rights and user access rights.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PERMISSION_MANAGE`, `PERMISSION_VIEW`, `REPORT_VIEW_TENANT` (1 configure, 1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAuthorisationPolicies` reads the population and the selected policy is edited in place — list, select, act. Chosen 2 October 2026 (CHG-SOT-013); the pack gave no directory. |
| Offline | online only |
| Opens with | `policyId` (navigation) |
| Route | `/analytics/report-access-sharing-control-anl-047` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Who may see which reports and dashboards, by group, operating area and user.

**Fixed on main** (the package already carries these; draw what it says): Only listAuthorisationPolicies with an empty table. (CHG-SOT-013); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SOT-013).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select field | — | — | — | — | Sends `?status=`: draft, pending approval, active, suspended or retired. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Pending approval · Active · Suspended · Retired | `listAuthorisationPolicies` ?status |
| Scope path | text field | — | — | `listAuthorisationPolicies` ?scopePath |

**Form: New access policy** (drawer, opened by *New access policy*; *Create access policy* calls `createAuthorisationPolicy`, *Cancel* sends nothing)

**Collects what `createAuthorisationPolicy` sends.** Required: `code`, `name`, `effect` (permit or deny; deny wins). Optional: `description`, `permissions` (the reporting permissions it speaks to), `conditions`, `combining`, `priority`, `scopePath` (the operating area), `appliesToRoleIds` (the groups), `effectiveFrom`, `effectiveTo`. Never `id`, `status` or `version`: the server sets them. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `createAuthorisationPolicy` body |
| Name `name` | text field | required | — | — | — | — | `createAuthorisationPolicy` body |
| Description `description` | text area | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Is template `isTemplate` | toggle | optional | off | — | — | — | `createAuthorisationPolicy` body |
| Permissions `permissions` | list of values (chips) | optional | — | — | — | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about. | `createAuthorisationPolicy` body |
| Conditions `conditions` | repeatable rows | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Attribute `conditions[].attribute` | select | required | — | User.attribute · Employee.attribute · Employee.on shift · Membership.tier · Membership.status · Accreditation.type · Accreditation.status · Customer.segment · Resource.classification · Venue.attribute · Venue.id · Attraction.attribute … | — | — | `createAuthorisationPolicy` body |
| Key `conditions[].key` | text field | optional | — | — | — | For the `*.attribute` forms — which attribute, by code. | `createAuthorisationPolicy` body |
| Operator `conditions[].operator` | select | required | — | Equals · Not equals · In · Not in · Greater than · Less than · Between · Contains · Starts with · Exists | — | — | `createAuthorisationPolicy` body |
| Value `conditions[].value` | field | optional | — | — | — | The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. | `createAuthorisationPolicy` body |
| Values `conditions[].values` | list of values (chips) | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Combining `combining` | segmented control | optional | All must match | All must match · Any may match | — | — | `createAuthorisationPolicy` body |
| Effect `effect` | segmented control | required | — | Permit · Deny | — | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of … | `createAuthorisationPolicy` body |
| Priority `priority` | number field | optional | 0 | — | — | — | `createAuthorisationPolicy` body |
| Scope path `scopePath` | text field | optional | — | — | — | 3.3.40 to 3.3.43. Tenant, venue and cross-venue policies are one mechanism, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance … | `createAuthorisationPolicy` body |
| Applies to roles `appliesToRoleIds` | multi-picker: choose applies to roles | optional | — | — | — | — | `createAuthorisationPolicy` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createAuthorisationPolicy` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createAuthorisationPolicy` body |
| Delegated admin roles `delegatedAdminRoleIds` | multi-picker: choose delegated admin roles | optional | — | — | — | 3.3.35. Who may edit this policy without being a platform administrator. | `createAuthorisationPolicy` body |

**Form: Save access policy** (drawer, opened by *Save access policy*; *Save access policy* calls `updateAuthorisationPolicy`, *Cancel* sends nothing)

**The selected policy, editable.** The same fields as creating one; saving writes a new version and the panel shows it. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `updateAuthorisationPolicy` body |
| Name `name` | text field | required | — | — | — | — | `updateAuthorisationPolicy` body |
| Description `description` | text area | optional | — | — | — | — | `updateAuthorisationPolicy` body |
| Is template `isTemplate` | toggle | optional | off | — | — | — | `updateAuthorisationPolicy` body |
| Permissions `permissions` | list of values (chips) | optional | — | — | — | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about. | `updateAuthorisationPolicy` body |
| Conditions `conditions` | repeatable rows | optional | — | — | — | — | `updateAuthorisationPolicy` body |
| Attribute `conditions[].attribute` | select | required | — | User.attribute · Employee.attribute · Employee.on shift · Membership.tier · Membership.status · Accreditation.type · Accreditation.status · Customer.segment · Resource.classification · Venue.attribute · Venue.id · Attraction.attribute … | — | — | `updateAuthorisationPolicy` body |
| Key `conditions[].key` | text field | optional | — | — | — | For the `*.attribute` forms — which attribute, by code. | `updateAuthorisationPolicy` body |
| Operator `conditions[].operator` | select | required | — | Equals · Not equals · In · Not in · Greater than · Less than · Between · Contains · Starts with · Exists | — | — | `updateAuthorisationPolicy` body |
| Value `conditions[].value` | field | optional | — | — | — | The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. | `updateAuthorisationPolicy` body |
| Values `conditions[].values` | list of values (chips) | optional | — | — | — | — | `updateAuthorisationPolicy` body |
| Combining `combining` | segmented control | optional | All must match | All must match · Any may match | — | — | `updateAuthorisationPolicy` body |
| Effect `effect` | segmented control | required | — | Permit · Deny | — | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of … | `updateAuthorisationPolicy` body |
| Priority `priority` | number field | optional | 0 | — | — | — | `updateAuthorisationPolicy` body |
| Scope path `scopePath` | text field | optional | — | — | — | 3.3.40 to 3.3.43. Tenant, venue and cross-venue policies are one mechanism, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance … | `updateAuthorisationPolicy` body |
| Applies to roles `appliesToRoleIds` | multi-picker: choose applies to roles | optional | — | — | — | — | `updateAuthorisationPolicy` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAuthorisationPolicy` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateAuthorisationPolicy` body |
| Delegated admin roles `delegatedAdminRoleIds` | multi-picker: choose delegated admin roles | optional | — | — | — | 3.3.35. Who may edit this policy without being a platform administrator. | `updateAuthorisationPolicy` body |

#### Outputs: what the screen shows and produces

**Shown**

**Who may see which reports** (data table, from `listAuthorisationPolicies`): The policies whose permissions include a reporting permission (`REPORT_*`). Roles and scopes are shown by name (group rights, operating-area rights, user rights), never as ids. **Cursor pagination, never offset.**

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Effect | chip: Permit, Deny | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not … |
| Permissions | list or chips (count when long) | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being … |
| Applies to roles | list or chips (count when long) | — |
| Scope path | text | 3.3.40 to 3.3.43. Tenant, venue and cross-venue policies are one mechanism, because `scope_path` is prefix-comparable — `uae.dubai` … |
| Status | chip: Draft, Pending approval, Active, Suspended, Retired | Moved only by `setAuthorisationPolicyState`. A policy is created as a `draft`, and a status sent in a create or update body is ignored — … |
| Effective from | 1 Oct 2026, 14:30 | — |

**The selected access policy** (detail panel, from `listAuthorisationPolicies`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Effect | chip: Permit, Deny | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not … |
| Permissions | list or chips (count when long) | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being … |
| Conditions | list or chips (count when long) | — |
| Combining | chip: All must match, Any may match | — |
| Priority | 1,234 | — |
| Applies to roles | list or chips (count when long) | — |
| Scope path | text | 3.3.40 to 3.3.43. Tenant, venue and cross-venue policies are one mechanism, because `scope_path` is prefix-comparable — `uae.dubai` … |
| Status | chip: Draft, Pending approval, Active, Suspended, Retired | Moved only by `setAuthorisationPolicyState`. A policy is created as a `draft`, and a status sent in a create or update body is ignored — … |
| Version | 1,234 | Set by the server; every `updateAuthorisationPolicy` writes a new version. |
| Effective from | 1 Oct 2026, 14:30 | — |
| Effective to | 1 Oct 2026, 14:30 | — |

**Sharing and export rules** (detail panel, from `getAnalyticsGovernancePolicy`): Read-only here; edited on ANL-070 by holders of `REPORT_GOVERNANCE_MANAGE` (DEC-225, CHG-FUP-007). **Sharing, export and subscription cannot bypass the permission model** (the pack's acceptance condition).

| Shows | Format | Notes |
|---|---|---|
| Sharing | grouped details | — |
| Export | grouped details | — |
| Masking | grouped details | Masked fields, as `schema.table.column`, and who may see them unmasked. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| New access policy (primary button) | `createAuthorisationPolicy` POST `/authorisation-policies` | AuthorisationPolicy | AuthorisationPolicy | — | opens drawer first |
| Save access policy (secondary button) | `updateAuthorisationPolicy` PUT `/authorisation-policies/{policyId}` | AuthorisationPolicy | AuthorisationPolicy | — | opens drawer first |

**Data it reads**: `listAuthorisationPolicies` (onLoad, Who may see which report: the policies that speak to …); `getAnalyticsGovernancePolicy` (onLoad, The sharing and export rules that apply to every report)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report access sharing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report access sharing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report access policy yet: reports follow the roles' own reporting permissions alone. Offers New access policy (`createAuthorisationPolicy`) to narrow or widen that by group, operating area or user; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the status filter, and the access policies are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PERMISSION_VIEW`, which `listAuthorisationPolicies` requires, and names that permission. **Never an empty table** — that reads as *there is no data*. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listAuthorisationPolicies (AuthorisationPolicy):
- code: AQC-AUH
  name: AquaCove Abu Dhabi
  description: Guest charged twice at Main Gate Till 3
  isTemplate: true
  combining: allMustMatch
  effect: permit
- code: AQC-DXB
  name: Main Gate Till 3
  description: Group of 40 from Desert Gate Tours
  isTemplate: false
  combining: anyMayMatch
  effect: deny
```

#### Permissions

- `listAuthorisationPolicies` → `PERMISSION_VIEW` (read) · staff
- `createAuthorisationPolicy` → `PERMISSION_MANAGE` (configure) · staff
- `updateAuthorisationPolicy` → `PERMISSION_MANAGE` (configure) · staff
- `getAnalyticsGovernancePolicy` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PERMISSION_VIEW`, which `listAuthorisationPolicies` requires, and names that permission. **Never an empty table** — that reads as *there is no data*.

Screen guard: `PERMISSION_VIEW`

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.3.1 | Allows permissions to be granted dynamically based on attributes and context rather than fixed roles only. | Admission and Access | CONTRACTED | `createAuthorisationPolicy` |
| 3.3.5 | Dynamic Rule Engine Administrators shall configure access policies without software development. | Admission and Access | CONTRACTED | `createAuthorisationPolicy` |
| 7.1.44 | Provide a no-code visual interface for building access policies using conditions, rules, logic operators, approval requirements and reusable components. | F&B POS | CONTRACTED | `createAuthorisationPolicy` |
| 3.3.24 | Policy Versioning - System shall maintain versions of access policies. | Admission and Access | CONTRACTED | `updateAuthorisationPolicy` |
| 3.3.35 | Delegated Access Management - System shall support delegated administration of access policies. | Admission and Access | CONTRACTED | data `AuthorisationPolicy` |
| 3.3.40 | Tenant-Specific Policies - System shall support tenant-specific access policies. | Admission and Access | CONTRACTED | data `AuthorisationPolicy` |
| 3.3.42 | Cross-Venue Access Policies - System shall support policies spanning multiple venues. | Admission and Access | CONTRACTED | data `AuthorisationPolicy` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-047` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-047`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 12: Works in Report Access & Sharing Control → Provide centralized security for reports, dashboards and analytical information. The matrix specifically requires reporting access based on group rights, operating-area rights and user access rights.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (39), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-047?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: New access policy, Save access policy.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `PERMISSION_MANAGE`, `PERMISSION_VIEW`, `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-048` Delivery Monitoring & Failure Management

**Monitor scheduled report execution and distribution and provide operational management of failures.**

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
| Route | `/analytics/delivery-monitoring-failure-management-anl-048` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Retry, Cancel, View Error, Change Destination, Notify Owner, Escalate. Each needs an operation, or needs … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Monitors scheduled runs and deliveries and helps an administrator act on failures without server logs. The thing to get right: failure reasons in plain words, retries visible, and personal-data deliveries flagged; the pack's six actions have no operation yet.

**Known correction pending (do not draw the wrong version)**

- **Retry, Cancel, View Error, Change Destination, Notify Owner and Escalate, and the Cancel confirmation overlay** Why: No delivery action exists; the only reads are the delivery list and the schedule list. *(source: screens/P16-venue-analytics.yaml#ANL-048 / contracts/satellite/reporting.yaml#listReportDeliveries; Finance, Ledger & Tax · Reporting & Analytics)*
- **Job ID, Schedule, Start and Completion columns** Why: A delivery carries its subscription, report, one attempted time and counts, not a job id, a schedule or start and end times. *(source: contracts/satellite/reporting.yaml#ReportDelivery; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **What does a suppressed delivery mean, and how many retries happen before Failed?** → Drawn default accepted: Suppressed = empty report skipped; three retries. *(decided by Chinmay, 2026-10-02; DEC-348 / CHG-NOTE-003)* **Reviewable:** a default the lead may still overrule before the block is tasked.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listReportDeliveries` ?from |
| Failed only | toggle | — | — | `listReportDeliveries` ?failedOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **failedOnly, from**: Defaults to failed in the last 24 hours. *(source: contracts/satellite/reporting.yaml#listReportDeliveries)*

#### Outputs: what the screen shows and produces

**Shown**

**Every delivery monitoring failure** (data table)

| Shows | Format | Notes |
|---|---|---|
| Job ID | text | not in the schema: `Job ID` |
| Report | text | not in the schema: `Report` |
| Schedule | text | not in the schema: `Schedule` |
| Start time | text | not in the schema: `Start Time` |
| Completion time | text | not in the schema: `Completion Time` |
| Recipient count | text | not in the schema: `Recipient Count` |
| Delivery method | text | not in the schema: `Delivery Method` |
| Status | text | not in the schema: `Status` |
| Error | text | not in the schema: `Error` |
| Retry count | text | not in the schema: `Retry Count` |

**The selected delivery monitoring failure** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Job ID | text | not in the schema: `Job ID` |
| Report | text | not in the schema: `Report` |
| Schedule | text | not in the schema: `Schedule` |
| Start time | text | not in the schema: `Start Time` |
| Completion time | text | not in the schema: `Completion Time` |
| Recipient count | text | not in the schema: `Recipient Count` |
| Delivery method | text | not in the schema: `Delivery Method` |
| Status | text | not in the schema: `Status` |
| Error | text | not in the schema: `Error` |
| Retry count | text | not in the schema: `Retry Count` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Retry (primary button) | navigation or local | — | — | — | — |
| Cancel (destructive button) | navigation or local | — | — | — | — |
| View Error (secondary button) | navigation or local | — | — | — | — |
| Change Destination (secondary button) | navigation or local | — | — | — | — |
| Notify Owner (secondary button) | navigation or local | — | — | — | — |
| Escalate (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **delivery row**: Report, route, attempted at, recipients count, status (Delivered, Failed, Retrying, Not sent), reason in words, retries so far, Personal data badge. Failed first, then Retrying. *(source: contracts/satellite/reporting.yaml#ReportDelivery)*
- **schedule health**: Schedules with consecutive failures, with the last run status and next run. *(source: contracts/satellite/reporting.yaml#ReportSchedule)*

**Data it reads**: `listReportDeliveries` (onLoad, Failures and retries)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

**What opens over it**

- confirmDialog *Cancel*: **Cancel on a delivery monitoring failure is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delivery monitoring failure list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delivery monitoring failure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No delivery monitoring failure yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the delivery monitoring failure are still there. The pack's own statuses are Running — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Status suppressed**: Shown as "Not sent - report was empty" when the schedule skips empty reports (see decisions). *(source: contracts/satellite/reporting.yaml#ReportDelivery / contracts/satellite/reporting.yaml#CreateReportScheduleRequest)*

#### Consistency with other screens

- Match `ANL-041`: Failure counters link here with the same filter.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- report: Daily closing - Aquaventure
  route: Email
  attempted: 01 Oct 2026 07:00
  recipients: 2
  status: Failed
  reason: Mailbox full - finance@aquaventure.ae
  retries: 2
  personalData: false
- report: Guest arrivals - VIP
  route: Email
  attempted: 01 Oct 2026 06:00
  recipients: 1
  status: Delivered
  personalData: true
- report: Weekly F&B sales
  route: SFTP
  attempted: 01 Oct 2026 06:30
  status: Retrying
  reason: SFTP login rejected
  retries: 1
```

#### Permissions

- `listReportDeliveries` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-048` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-048`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 14: Works in Delivery Monitoring & Failure Management → Monitor scheduled report execution and distribution and provide operational management of failures.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-048?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Retry, Cancel, View Error, Change Destination, Notify Owner, Escalate.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-049` Report Audit Trail & Compliance

**Maintain complete traceability of reporting activity. The source matrix requires report logs and audit reporting for sales history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/report-audit-trail-compliance-anl-049` |

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Reconstructs who did what with reports: created, changed, published, ran, viewed, exported, shared, scheduled, subscribed, changed permissions, archived. It is a read-only trail, newest first, that nobody can edit, and reading it is itself recorded. The thing to get right: it reads the platform audit trail, not the delivery list, and personal-data exports stand out.

**Known correction pending (do not draw the wrong version)**

- **The screen reads the delivery list** Why: The reporting audit trail is the platform audit read (who, where, action, subject, when), gated by audit permission; deliveries cover only what was sent. *(source: contracts/spine/tenancy.yaml#listAuditRecords / contracts/satellite/reporting.yaml#listReportDeliveries; Finance, Ledger & Tax · Reporting & Analytics)*
- **Pattern configEditor with 14 select fields (Report Created ... Report Deleted)** Why: These are event types to filter by in a read-only list, not settings. *(source: screens/P16-venue-analytics.yaml#ANL-049; Finance, Ledger & Tax · Reporting & Analytics)*
- **Action names are free strings "as the writing operation names it"** Why: Without a fixed list the human labels above cannot be mapped reliably. *(source: contracts/spine/tenancy.yaml#AuditRecord; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search report audit trail | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by user, report, action, date, site, business unit and 2 more — which are present is a decision the pack already made. | — |
| Report Created | select field | — | — | — | — | — | — |
| Report Modified | select field | — | — | — | — | — | — |
| Report Published | select field | — | — | — | — | — | — |
| Report Executed | select field | — | — | — | — | — | — |
| Report Viewed | select field | — | — | — | — | — | — |
| Report Exported | select field | — | — | — | — | — | — |
| Report Shared | select field | — | — | — | — | — | — |
| Schedule Created | select field | — | — | — | — | — | — |
| Schedule Modified | select field | — | — | — | — | — | — |
| Subscription Created | select field | — | — | — | — | — | — |
| Permission Changed | select field | — | — | — | — | — | — |
| API Access | select field | — | — | — | — | — | — |
| Report Archived | select field | — | — | — | — | — | — |
| Report Deleted | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listReportDeliveries` ?from |
| Failed only | toggle | — | — | `listReportDeliveries` ?failedOnly |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **filters**: Person, report (the thing acted on), action, date range, venue. Business unit, export type and status have no filter. *(source: contracts/spine/tenancy.yaml#listAuditRecords)*

#### Outputs: what the screen shows and produces

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **event row**: When (venue time), who, what in words ("Exported Guest arrivals - VIP to Excel, with personal data, purpose given"), on what, where (venue, workstation). Actions by TICVAI support staff carry a "TICVAI support" badge. *(source: contracts/spine/tenancy.yaml#AuditRecord / R098)*
- **personal-data events**: Exports and deliveries with personal data are highlighted and filterable on their own. *(source: contracts/satellite/reporting.yaml#exportReportResult / contracts/satellite/reporting.yaml#ReportDelivery)*

**Data it reads**: `listReportDeliveries` (onLoad, What left, with what in it)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report audit trail configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report audit trail untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report audit trail configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the report audit trail are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Auditor opens the trail**: Their reading is recorded too; say so in the header ("Your access to this trail is recorded"). *(source: contracts/spine/tenancy.yaml#listAuditRecords)*

#### Consistency with other screens

- Match `BO-068`: Same audit row layout as the back-office audit log.
- Match `ANL-045`: Same personal-data badge and purpose text.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
- when: 01 Oct 2026 09:02
  who: Omar Haddad
  action: Exported to Excel with personal data
  subject: Guest arrivals - VIP
  where: Aquaventure Waterpark
  purpose: Concierge welcome calls
- when: 30 Sep 2026 17:20
  who: Rahul Menon
  action: Published version 4
  subject: Sales by channel (copy)
- when: 30 Sep 2026 11:03
  who: Support - Sara K.
  action: Viewed schedule
  subject: Daily closing - Aquaventure
  badge: TICVAI support
```

#### Permissions

- `listReportDeliveries` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-049` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-049`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 16: Works in Report Audit Trail & Compliance → Maintain complete traceability of reporting activity. The source matrix requires report logs and audit reporting for sales history.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-049?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-050` Retention, Archive & Governance Policy

**Control the lifecycle of reports, generated files and historical analytical data. The reporting-platform specification requires long-term reporting history together with archival and retrieval capability.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `TENANT_CONFIGURE`, `TENANT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure retention separately for; Define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `dataClass` (navigation) |
| Route | `/analytics/retention-archive-governance-policy-anl-050` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): setApprovalRetentionPolicy on the analytics retention screen; approval decision records are not reports, and ADM-346 keeps the operation (design-notes correction …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How long reports, exports and analytics history are kept, archived and deleted, with legal hold.

**Fixed on main** (the package already carries these; draw what it says): setApprovalRetentionPolicy on an analytics retention screen. (CHG-WIR-021).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Report Definitions | select field | — | — | — | — | — | — |
| Dashboard Versions | select field | — | — | — | — | — | — |
| Generated Reports | select field | — | — | — | — | — | — |
| Export Files | select field | — | — | — | — | — | — |
| Audit Logs | select field | — | — | — | — | — | — |
| Schedule History | select field | — | — | — | — | — | — |
| API Logs | select field | — | — | — | — | — | — |
| Historical Analytics | select field | — | — | — | — | — | — |
| Retention Period | select field | — | — | — | — | — | — |
| Archive After | select field | — | — | — | — | — | — |
| Delete After | select field | — | — | — | — | — | — |
| Legal/Compliance Hold | select field | — | — | — | — | — | — |
| Storage Location | select field | — | — | — | — | — | — |
| Retrieval Rules | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Data class | select | — | Guest profile · Payment record · Financial record · Audit record · Approval record · Compliance inspection · Face tag biometric · Face pass biometric · AI prompts · AI conversations · AI decision records · AI metadata index | `listDataRetentionSettings` ?dataClass |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApprovalRetentionPolicy, setDataRetentionSetting: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setApprovalRetentionPolicy)*

#### Outputs: what the screen shows and produces

**Data it reads**: `listDataRetentionSettings` (onLoad, Retention period per data class)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The retention archive governance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the retention archive governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No retention archive governance configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A period below the class's legal minimum or above its legal maximum, a period sent for `aiMetadataIndex`, or a `followsDataClass` chain that loops |

#### Edge cases to draw

- **Can read but not change (holds TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_CONFIGURE for setApprovalRetentionPolicy; TENANT_CONFIGURE for setDataRetentionSetting. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#setApprovalRetentionPolicy)*
- **setDataRetentionSetting answers 422**: Show it as something the person can act on, not a failure: A period below the class's legal minimum or above its legal maximum, a period sent for `aiMetadataIndex`, or a `followsDataClass` chain that loops *(source: contracts/spine/tenancy.yaml#setDataRetentionSetting)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
policy:
  object: Generated reports
  retention: 24 months
  archiveAfter: 6 months
  legalHold: false
```

#### Permissions

- `listDataRetentionSettings` → `TENANT_VIEW` (read) · staff
- `setDataRetentionSetting` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.3.4 | The system should support payment servers that provide the following functions: - Record transactions below the authorization threshold - Procure authorizations over the automatic authorization … | Bundles and Promotions | CONTRACTED | `setDataRetentionSetting` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-050` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-050`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 18: Works in Retention, Archive & Governance Policy → Control the lifecycle of reports, generated files and historical analytical data. The reporting-platform specification requires long-term reporting history together with archival and retrieval …
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-050?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createAuthorisationPolicy": {"method":"POST","path":"/authorisation-policies","contract":"identity","summary":"Write a policy without writing code","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AuthorisationPolicy","responds":"AuthorisationPolicy"},
"createReportSchedule": {"method":"POST","path":"/report-schedules","contract":"reporting","summary":"Schedule a report","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportScheduleRequest","responds":"ReportSchedule"},
"createReportSubscription": {"method":"POST","path":"/report-subscriptions","contract":"reporting","summary":"Send a report to somebody, on terms","permission":"REPORT_SCHEDULE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReportSubscription","responds":"ReportSubscription"},
"exportReportResult": {"method":"POST","path":"/report-executions/{executionId}/export","contract":"reporting","summary":"Export a completed result","permission":"REPORT_EXPORT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getAnalyticsGovernancePolicy": {"method":"GET","path":"/analytics-governance-policy","contract":"reporting","summary":"The tenant's analytics governance policy","permission":"REPORT_VIEW_TENANT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"AnalyticsGovernancePolicy"},
"getReportExport": {"method":"GET","path":"/report-exports/{exportId}","contract":"reporting","summary":"Export status and download link","permission":"REPORT_EXPORT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportExport"},
"listAuthorisationPolicies": {"method":"GET","path":"/authorisation-policies","contract":"identity","summary":"Attribute-based authorisation policies","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"scopePath","in":"query","required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"listDataRetentionSettings": {"method":"GET","path":"/data-retention-settings","contract":"tenancy","summary":"How long the tenant keeps each class of data","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"dataClass","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReportDeliveries": {"method":"GET","path":"/report-deliveries","contract":"reporting","summary":"What was sent, to whom, and what failed","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"failedOnly","in":"query","required":null}],"requestBody":null,"responds":"ReportDelivery"},
"listReportSchedules": {"method":"GET","path":"/report-schedules","contract":"reporting","summary":"List scheduled reports","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReportSubscriptions": {"method":"GET","path":"/report-subscriptions","contract":"reporting","summary":"Who receives what, and by which route","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportSubscription"},
"setDataRetentionSetting": {"method":"PUT","path":"/data-retention-settings/{dataClass}","contract":"tenancy","summary":"Set how long the tenant keeps one class of data","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TenantDataRetentionSetting","responds":"TenantDataRetentionSetting"},
"updateAuthorisationPolicy": {"method":"PUT","path":"/authorisation-policies/{policyId}","contract":"identity","summary":"Change a policy, as a new version","permission":"PERMISSION_MANAGE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AuthorisationPolicy","responds":"AuthorisationPolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCondition": {"type":"object","description":"**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n","required":["attribute","operator"],"properties":{"attribute":{"type":"string","enum":["user.attribute","employee.attribute","employee.onShift","membership.tier","membership.status","accreditation.type","accreditation.status","customer.segment","resource.classification","venue.attribute","venue.id","attraction.attribute","device.kind","device.id","device.trusted","time.ofDay","time.dayOfWeek","time.season","time.withinOperatingHours","event.id","event.status","capacity.utilisationPercent","occupancy.level","risk.score","ticket.status","location.scopePath"]},"key":{"type":"string","nullable":true,"description":"For the `*.attribute` forms — which attribute, by code."},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","greaterThan","lessThan","between","contains","startsWith","exists"]},"value":{"nullable":true,"description":"The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"},"values":{"type":"array","items":{"type":"string"}}}},
"AnalyticsGovernancePolicy": {"type":"object","x-ticvai-persistence":"reporting.analytics_governance_policy","description":"**What analytics may show and where it may go** (Chinmay, 2 October, workbook Q225; CHG-CSA-021). One row per tenant.","properties":{"masking":{"type":"object","description":"Masked fields, as `schema.table.column`, and who may see them unmasked.","properties":{"maskedFields":{"type":"array","items":{"type":"string"}},"unmaskedForPermissions":{"type":"array","items":{"type":"string"}}}},"export":{"type":"object","properties":{"allowedFormats":{"type":"array","items":{"type":"string"}},"personalDataNeedsPermission":{"type":"boolean","default":true,"description":"An export carrying personal data needs `REPORT_EXPORT_PII`."},"maxRows":{"type":"integer","nullable":true}}},"retention":{"type":"object","properties":{"resultDays":{"type":"integer","minimum":1,"nullable":true,"description":"How long report results and exports are kept."}}},"sharing":{"type":"object","properties":{"externalLinks":{"type":"boolean","default":false},"allowedDomains":{"type":"array","items":{"type":"string"}}}},"aiAndApiAccess":{"type":"object","properties":{"aiAssistant":{"type":"boolean","default":true,"description":"The AI assistant may answer analytics questions through the semantic layer (ADR-0054)."},"publicApi":{"type":"boolean","default":false}}},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `tenant` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AuthorisationPolicy": {"type":"object","x-ticvai-persistence":"identity.authorisation_policy","description":"3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here).\n**Settled by ADR-0068 (accepted 1 October): guest admission lives in Access only.** This engine keeps staff authorisation and was renamed to say so: `identity.access_policy` became `identity.authorisation_policy`, its versions `identity.authorisation_policy_version`, and its operations `*AuthorisationPolicy*`. \"Access policy\" now means `AccessDynamicPolicy` and nothing else.\n","required":["code","name","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on `createAuthorisationPolicy`; the path names the policy on update."},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"isTemplate":{"type":"boolean","default":false},"permissions":{"type":"array","items":{"type":"string"},"description":"**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/AccessCondition"}},"combining":{"type":"string","enum":["allMustMatch","anyMayMatch"],"default":"allMustMatch"},"effect":{"type":"string","enum":["permit","deny"],"description":"**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"},"priority":{"type":"integer","default":0},"scopePath":{"type":"string","description":"3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"},"appliesToRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"status":{"type":"string","readOnly":true,"description":"**Moved only by `setAuthorisationPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n","enum":["draft","pendingApproval","active","suspended","retired"]},"version":{"type":"integer","default":1,"readOnly":true,"description":"Set by the server; every `updateAuthorisationPolicy` writes a new version."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"delegatedAdminRoleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"}}},
"Cadence": {"x-ticvai-persistence":"none — embedded in schedule","type":"object","description":"**What each frequency needs (decided 28 September, audit R158).** `daily`: `timeOfDay`. `weekly`: `dayOfWeek` and `timeOfDay`. `monthly`: `dayOfMonth` and `timeOfDay`, a day past the month's end running on its last day. `quarterly`: `dayOfMonth` and `timeOfDay`, in the first month of each quarter. `onShiftClose` and `onPeriodClose`: nothing else, they run on the event. A field a frequency needs and does not have, or one it does not take, is the 400 on `createReportSchedule`. **Times are in the venue's time zone.**\n","required":["frequency"],"properties":{"frequency":{"type":"string","enum":["daily","weekly","monthly","quarterly","onShiftClose","onPeriodClose"]},"dayOfWeek":{"type":"integer","minimum":0,"maximum":6},"dayOfMonth":{"type":"integer","minimum":1,"maximum":31},"timeOfDay":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"timeZone":{"type":"string","readOnly":true,"description":"Always the venue's time zone (decided 28 September, audit R158), returned so a reader knows which. Not taken on a write."}}},
"CreateReportScheduleRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["reportId","cadence","recipients","format"],"properties":{"reportId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"cadence":{"$ref":"#/components/schemas/Cadence"},"parameters":{"type":"object","additionalProperties":true,"description":"As `RunReportRequest.parameters` — keyed by the report's `ReportParameter.key`, applied to every run."},"recipients":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/Recipient"}},"format":{"$ref":"#/components/schemas/ExportFormat"},"includePersonalData":{"type":"boolean","default":false},"skipIfEmpty":{"type":"boolean","default":true,"description":"An empty report every morning trains people to ignore the report."}}},
"ExecutionStatus": {"type":"string","enum":["queued","running","completed","failed","cancelled","expired"]},
"ExportFormat": {"type":"string","enum":["csv","xlsx","pdf","json"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Recipient": {"x-ticvai-persistence":"reporting.schedule_recipient","type":"object","description":"One recipient of a schedule. **A row of `reporting.schedule_recipient`, a child of `reporting.schedule`** — `ReportSchedule` declares the pair, which is what gives the table its `schedule_id`. Pull audit 26 September: declared on its own, the table had no column tying a recipient to its schedule.\n","required":["kind","address"],"properties":{"kind":{"type":"string","enum":["principal","email","sftp","webhook"]},"address":{"type":"string"},"principalId":{"type":"string","format":"uuid"}}},
"ReportDelivery": {"type":"object","x-ticvai-persistence":"reporting.delivery","description":"BI boards 4.8 and 4.9. **A report that silently stopped arriving is worse than one that never existed.**\n","properties":{"id":{"type":"string","format":"uuid"},"subscriptionId":{"type":"string","format":"uuid"},"reportId":{"type":"string","format":"uuid"},"attemptedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["delivered","failed","retrying","suppressed"]},"recipientCount":{"type":"integer"},"failureReason":{"type":"string","nullable":true},"retryCount":{"type":"integer","default":0},"containedPersonalData":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"ReportExport": {"x-ticvai-persistence":"reporting.export","type":"object","required":["id","executionId","format","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"executionId":{"type":"string"},"format":{"$ref":"#/components/schemas/ExportFormat"},"status":{"type":"string","enum":["queued","generating","ready","failed","expired"]},"includesPersonalData":{"type":"boolean"},"purpose":{"type":"string","nullable":true},"downloadUrl":{"type":"string","nullable":true,"description":"Signed and expiring. Present only while status is `ready`."},"sizeBytes":{"type":"integer","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"requestedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},
"ReportSchedule": {"x-ticvai-persistence":"reporting.schedule + reporting.schedule_recipient","allOf":[{"$ref":"#/components/schemas/CreateReportScheduleRequest"},{"type":"object","required":["id","ownerPrincipalId","isPaused","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid","description":"The schedule runs under this principal's permissions, not the recipients'. A standing grant of whatever the owner can see.\n"},"isPaused":{"type":"boolean"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastRunStatus":{"$ref":"#/components/schemas/ExecutionStatus"},"nextRunAt":{"type":"string","format":"date-time","nullable":true},"consecutiveFailures":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}}]},
"ReportSubscription": {"type":"object","x-ticvai-persistence":"reporting.subscription","description":"BI boards 4.3 and 4.4. **Not a schedule** — one schedule serves several of these.","required":["reportId"],"properties":{"id":{"type":"string","format":"uuid"},"reportId":{"type":"string","format":"uuid"},"scheduleId":{"type":"string","format":"uuid","nullable":true},"recipients":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid","nullable":true},"email":{"type":"string","nullable":true},"external":{"type":"boolean","default":false}}}},"channel":{"type":"string","enum":["email","sftp","webhook","inPlatform"]},"format":{"type":"string","enum":["pdf","xlsx","csv","json"]},"includesPersonalData":{"type":"boolean","default":false,"description":"**Gates on `REPORT_EXPORT_PII` and is audited.** A report that leaves the tenant with personal data in it is a fact somebody will ask about.\n"},"runsAsPrincipalId":{"type":"string","format":"uuid","description":"**The report runs under the owner's permissions, not the recipient's.**"},"active":{"type":"boolean","default":true},"scopePath":{"type":"string"}}},
"TenantDataRetentionClass": {"type":"string","description":"**The data classes a tenant sets a retention period for** (decided 29 September, Chinmay: all data retention is tenant configuration, one setting per class). Defaults are ADR-0047's and the AI system design's (section 8, decision 5); a legal limit is the only thing the platform enforces.\n| Class | Default | Counted from | Legal limit (refused) | |---|---|---|---| | `guestProfile` | 5 years | last activity | none | | `paymentRecord` | 10 years | created | at least 10 years (4.3.4) | | `financialRecord` | 7 years | created | at least 7 years (6.1.78) | | `auditRecord` | 2 years (authorisation and device audit) | created | none | | `approvalRecord` | 7 years (approvals board 6.7) | decided | none | | `complianceInspection` | 7 years | created | none | | `faceTagBiometric` | 7 days | ticket expiry | make-or-break | | `facePassBiometric` | follows `guestProfile` | last activity | make-or-break | | `aiPrompts` | 90 days (prompts and responses) | created | none | | `aiConversations` | 90 days | last activity | none | | `aiDecisionRecords` | follows `auditRecord` (decision records and the approvals of AI actions) | decided | none | | `aiMetadataIndex` | always follows `aiDecisionRecords` (summaries, entities, embeddings) | created | none |\n**ADR-0047's floors and ceilings that are not law are defaults now, not refusals** (the audit floor of one year, the proposed seven-year guest-profile ceiling, the Face Tag thirty-day ceiling). Platform-owned copies — the burst environment copy, a decommissioned cell — are not tenant data classes and are not here.\n","enum":["guestProfile","paymentRecord","financialRecord","auditRecord","approvalRecord","complianceInspection","faceTagBiometric","facePassBiometric","aiPrompts","aiConversations","aiDecisionRecords","aiMetadataIndex"]},
"TenantDataRetentionSetting": {"type":"object","x-ticvai-persistence":"tenancy.data_retention_setting","description":"**One tenant's retention period for one data class** (decided 29 September, Chinmay). One row per tenant and class, written by `setDataRetentionSetting`; a class with no row takes the platform default. The limit and default fields are the platform's catalogue, computed for the response and not stored on the row.\n","required":["dataClass"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"dataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"x-ticvai-unique":"tenant","description":"One row per class per tenant. On a write it comes from the path; a body value is ignored."},"retainAmount":{"type":"integer","nullable":true,"minimum":0,"description":"The tenant's period. Null with no `followsDataClass` means the platform default applies. Zero means the data is not kept past the transaction that produced it.\n"},"retainUnit":{"type":"string","nullable":true,"enum":["days","months","years"],"description":"Required with `retainAmount`."},"followsDataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"nullable":true,"description":"Keep this class for as long as another class is kept. Set by default for `aiDecisionRecords` (follows `auditRecord`), `facePassBiometric` (follows `guestProfile`) and `aiMetadataIndex` (follows `aiDecisionRecords`, and cannot be changed).\n"},"onExpiry":{"type":"string","enum":["archive","anonymise","delete"],"default":"archive","description":"ADR-0047's stages. `archive` moves the data to the archive instance, from where it is erased on the class's own schedule; derived stores (the AI index, search) purge at archive, not later.\n"},"anchor":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["createdAt","lastActivity","decidedAt","ticketExpiry"],"description":"What the period is counted from. Fixed per class by the platform."},"effectiveAmount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"The period actually applied, after follows and defaults are resolved."},"effectiveUnit":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"isDefault":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"True when the tenant has not set this class and the platform default applies."},"defaultAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false},"defaultUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalMinimumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A floor the law sets. A shorter period is refused (`422`)."},"legalMaximumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A maximum the law sets. A longer period is refused (`422`). Null for every class until the biometric make-or-break is answered."},"legalLimitUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalBasis":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"The law or requirement the limit comes from, e.g. `4.3.4`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"updatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The tenant. Retention is set at tenant scope only."}}}
}
```
