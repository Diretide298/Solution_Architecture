# P09-security-compliance-01 — P09 · Security & Compliance

**2 screens · 10 operations · 12 schemas · 6 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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
  `PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW, REPORT_MANAGE, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `ADM-031` | Security & Compliance Dashboard | D | 42 | 26 | 7 | 19 | 0 | 0 | — | notStarted (generated) |
| `ADM-032` | WAF & Security Policy View | B–D | 9 | 6 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-032 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-031` Security & Compliance Dashboard

**See a tenant's security and compliance position from the console: second-factor coverage, failed sign-ins, open grants and exports.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Security & Compliance · wave 1 · needs the `core` module |
| Block | Block D · task APP-CONSOLE-ADM-031 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (2 operate, 1 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listDashboards` reads the population and `getDashboard` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `dashboardId` (deepLink), `tenantId` (navigation) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/security-and-compliance-dashboard` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — not specified

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The platform's security and compliance picture: who holds sensitive rights without a second factor, open platform-staff access into tenants, unusual sign-in patterns and override rates, personal-data exports, and retention. It is where an investigation starts and hands over to the audit logs. The one thing to get right: a platform operator sees a tenant only after picking it and opening an audited, time-boxed grant, and the grant is always visible.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The operations are generic dashboard create/list/update, gated by a venue report permission, and none of the tiles has a metric source. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The purpose ("the screen this app sits on; everything else is entered from here") is the console home's purpose. (CHG-SBO-012).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which security measures does the platform compute, and from which logs?** → Drawn default accepted: Draw the tiles above as the intended set, marked "awaiting source". *(decided by Chinmay, 2026-10-02; DEC-077 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant … | `Tenant.id` |
| Module | select | optional | — | Core · Ticketing · Access · Fnb · Retail · Inventory · Seating · Membership · Marketing · Resources · Queue · Transport … | — | Sends `?module=` to `listDashboards`. | `listDashboards` ?module |
| Include archived | toggle | optional | off | — | — | Sends `?includeArchived=` to `listDashboards`. | `listDashboards` ?includeArchived |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client UUIDv7), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Create dashboard** (modal, opened by *Create dashboard*; *Create dashboard* calls `createDashboard`, *Cancel* sends nothing)

**Collects what `createDashboard` sends before it is called.** Required: `name`, `module`, `tiles`. Optional: `description`, `venueId`, `isShared`. Dismissing sends nothing; the screen behind is unchanged.

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

**Form: Save dashboard** (modal, opened by *Save dashboard*; *Save dashboard* calls `updateDashboard`, *Cancel* sends nothing)

**Collects what `updateDashboard` sends before it is called.** Required: `name`, `module`, `tiles`. Optional: `description`, `venueId`, `isShared`. Dismissing sends nothing; the screen behind is unchanged.

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

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Tenant**: Picked first; every figure below is for that tenant, and nothing tenant-specific shows until a grant is open. *(source: R098 / screens/P09-platform-admin-console.yaml#ADM-031)*
- **Open access grant**: Reason, permissions (preselected to what this screen reads), expiry; asks for the second factor first. *(source: R098 / R135)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (detail panel, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Every dashboard** (data table, from `listDashboards`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Venue | the name it points at, never the id | Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. |
| Is shared | yes / no (icon or chip) | — |
| Tiles | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Owner principal | the name it points at, never the id | — |
| Aggregate cost | chip: Low, Medium, High | Combined refresh load of every tile. |

**The selected dashboard** (detail panel, from `listDashboards`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Module | chip: Core, Ticketing, Access, Fnb, Retail, Inventory… | Which module this dashboard belongs to, and therefore who may see it. Added 22 September for the command centre: one shell that shows each … |
| Description | text | — |
| Venue | the name it points at, never the id | Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. |
| Is shared | yes / no (icon or chip) | — |
| Tiles | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Owner principal | the name it points at, never the id | — |
| Aggregate cost | chip: Low, Medium, High | Combined refresh load of every tile. |
| Archived at | 1 Oct 2026, 14:30 | Set by `deleteDashboard`, which archives rather than removes. A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` … |

**The dashboard data** (detail panel, from `getDashboard`)

| Shows | Format | Notes |
|---|---|---|
| Tile data | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Create dashboard (primary button) | `createDashboard` POST `/dashboards` | CreateDashboardRequest | Dashboard | 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094); 409 The caller is not entitled to the dashboard's module — the tenant has not … | opens modal first |
| Save dashboard (secondary button) | `updateDashboard` PUT `/dashboards/{dashboardId}` | CreateDashboardRequest | Dashboard | 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094), as on `createDashboard` …; 409 Moving a dashboard to a module the caller is not … | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Tiles**: Principals holding MFA-required rights without an active second factor (the floor is role management, ledger approval and every platform right); open platform-staff grants with time left; failed sign-ins and lockouts; personal-data exports in the period; override rate at gates and tills; segregation-of-duties conflicts. *(source: contracts/shared/permissions.yaml#/components/schemas/Permission / DI-732 / F106 step 1)*
- **Grant banner**: Tenant, permissions, reason, time left; at expiry every tenant action disables and the screen returns to "grant required". *(source: R098)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Investigate**: Opens the platform audit log (ADM-004) or the tenant audit log (BO-068) filtered to the figure clicked. *(source: F106 step 2 / F106 step 3)*

**Data it reads**: `listTenants` (onLoad, The tenant picker — the operator picks a tenant before …); `listDashboards` (onLoad, List dashboards); `recordDashboardView` (background, Record that a dashboard was opened — fired once when the …)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-004` Platform Audit Log: *Platform Audit Log*; carries `tenantId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The security compliance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the security compliance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No security compliance yet. Offers Create dashboard (`createDashboard`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on module, includeArchived and the security compliance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires to show this screen, and names that permission (the screen's other reads need `REPORT_VIEW_VENUE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for `openPlatformStaffGrant` … |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094); 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094), as on `createDashboard` …; 400 Validation failed; 409 Moving a dashboard to a module the caller is not entitled to. The same … |

#### Edge cases to draw

- **The grant expires during an investigation**: Figures stay visible as last loaded but labelled; actions disable; a new grant is a new reason. *(source: R098)*

#### Consistency with other screens

- Match `ANL-069`: Usage and cost of analytics is there; security events are here.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tenant: Dubai Parks & Resorts
grant: 'Read security dashboards · reason: quarterly access review · 1 h 42 min left'
tiles:
- 7 people with ledger approval have no second factor
- 2 open platform-staff grants
- Failed sign-ins 184 (last 24 h) · 3 accounts locked
- Personal-data exports 5 this month
- Gate overrides 0.8% of scans
```

#### Permissions

- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listDashboards` → `REPORT_VIEW_VENUE` (operate) · staff
- `getDashboard` → `REPORT_VIEW_VENUE` (operate) · staff
- `createDashboard` → `REPORT_MANAGE` (configure) · staff
- `updateDashboard` → `REPORT_MANAGE` (configure) · staff
- `recordDashboardView` → `REPORT_VIEW_VENUE` (operate) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires to show this screen, and names that permission (the screen's other reads need `REPORT_VIEW_VENUE` and say so in their own panels). **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_TENANT_ACCESS` for `openPlatformStaffGrant` …

#### Requirements it meets

19 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 7 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-031` · status **notStarted** · provenance generated
- Flow F106 *A security dashboard surfaces something and it is investigated*, step 1: Security & Compliance Dashboard. → 3 operations, 3 of them previously unwalked.
- Flow F106 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.

#### Acceptance for the design

- [ ] Every input above is drawn (42), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-031?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Create dashboard, Save dashboard.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-004`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-032` WAF & Security Policy View

**See the firewall rules in force and change the WAF policy.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Security & Compliance · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/waf-and-security-policy-view` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. An editor of the firewall policy (`setWafPolicy`) with the rules in force; the name says View and the screen edits (design-note correction).

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Copied cell actions (decommission, tier) on the WAF policy screen; decommission stays on ADM-003 only (design-notes corrections platform-foundation ADM-032 … Removed 2 October 2026 (CHG-WIR-021): Copied cell actions (decommission, tier) on the WAF policy screen; decommission stays on ADM-003 only (design-notes corrections platform-foundation ADM-032 … Removed 2 October 2026 (CHG-WIR-021): Copied cell actions (decommission, tier) on the WAF policy screen; decommission stays on ADM-003 only (design-notes corrections platform-foundation ADM-032 … Open: No contract — infrastructure

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** WAF rules and their hits per cell (read-only view).

**Fixed on main** (the package already carries these; draw what it says): "Save waf policy" on a screen named "View", plus copied cell actions. (CHG-SBO-015); formSetWafPolicy asks the person for id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every cell job' drop id; 'Every waf rule' drop id. (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**Form: Save waf policy** (modal, opened by *Save waf policy*; *Save waf policy* calls `setWafPolicy`, *Cancel* sends nothing)

**Collects what `setWafPolicy` sends before it is called.** Nothing in the body is required. Optional: `name`, `action`, `matchOn`, `pattern`, `enabled`, `hitCount24h`. **Not asked:** `id` is a client UUIDv7 generated silently (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setWafPolicy` body |
| Cell `cellId` | picker: choose a cell | optional | — | — | shows names, sends the id | — | `setWafPolicy` body |
| Name `name` | text field | optional | — | — | — | — | `setWafPolicy` body |
| Action `action` | radio group | optional | — | Allow · Block · Rate limit · Challenge | — | — | `setWafPolicy` body |
| Match on `matchOn` | text field | optional | — | — | — | What the rule inspects - a path, a header, a source range. | `setWafPolicy` body |
| Pattern `pattern` | text field | optional | — | — | — | — | `setWafPolicy` body |
| Enabled `enabled` | toggle | optional | — | — | — | — | `setWafPolicy` body |
| Hit count24h `hitCount24h` | number field | optional | — | — | — | A rule with no hits is either protecting nothing or blocking everything silently, and both want looking at. | `setWafPolicy` body |
| Updated at `updatedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setWafPolicy` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setWafPolicy: set per region (money, tax, ledger); venues inherit and cannot override. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/platform-ops.yaml#setWafPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Every waf rule** (data table, from `listWafRules`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Action | chip: Allow, Block, Rate limit, Challenge | — |
| Match on | text | What the rule inspects - a path, a header, a source range. |
| Pattern | text | — |
| Enabled | yes / no (icon or chip) | — |
| Hit count24h | 1,234 | A rule with no hits is either protecting nothing or blocking everything silently, and both want looking at. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save waf policy (secondary button) | `setWafPolicy` PUT `/waf-policies` | WafRule | WafRule | — | opens modal first |

**Data it reads**: `listWafRules` (onLoad, Firewall rules in force)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The waf security policy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the waf security policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No waf security policy yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listWafRules` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_CELL_MANAGE` for `setWafPolicy`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for Cancel decommission, Decommission cell, Save cell tier. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **cancelDecommission answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **decommissionCell answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#decommissionCell)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell job:
- kind: standard
  status: active
  progressPercent: 12.5
  scheduledFor: 31/12/2026 23:59
  completedAt: 01/10/2026 09:14
- kind: standard
  status: pending
  progressPercent: 8.0
  scheduledFor: 15/10/2026 00:00
  completedAt: 30/09/2026 18:02
- kind: override
  status: suspended
  progressPercent: 15.0
  scheduledFor: 01/11/2026 06:00
  completedAt: 28/09/2026 11:45
```

#### Permissions

- `listWafRules` → `PLATFORM_CELL_VIEW` (read) · staff
- `setWafPolicy` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listWafRules` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_CELL_MANAGE` for `setWafPolicy`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-032` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-032?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save waf policy.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P09 reference designs** (from `handoff/design-batches/apps/6-ticvai-controller/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P09 TICVAI Web

- Portal access exposes TICVAI pricing, so prospects submit contact details and a trade license as proof of a real venue, reviewed and approved by TICVAI before access is granted. *(agreed · MoM 10 Sep 2026, 4.8 Customer Portal Access, Authentication & Verification · DI-827)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createDashboard": {"method":"POST","path":"/dashboards","contract":"reporting","summary":"Create a dashboard","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateDashboardRequest","responds":"Dashboard"},
"getDashboard": {"method":"GET","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Read a dashboard with tile data","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"refresh","in":"query","required":null}],"requestBody":null,"responds":"DashboardData"},
"listDashboards": {"method":"GET","path":"/dashboards","contract":"reporting","summary":"List dashboards","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":false},{"name":"includeArchived","in":"query","required":false}],"requestBody":null,"responds":"Dashboard"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWafRules": {"method":"GET","path":"/waf-policies","contract":"platform-ops","summary":"Web application firewall rules in force","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"WafRule"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"recordDashboardView": {"method":"POST","path":"/dashboards/{dashboardId}/views","contract":"reporting","summary":"Record that a dashboard was opened","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setWafPolicy": {"method":"PUT","path":"/waf-policies","contract":"platform-ops","summary":"Change the firewall policy","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WafRule","responds":"WafRule"},
"updateDashboard": {"method":"PUT","path":"/dashboards/{dashboardId}","contract":"reporting","summary":"Update a dashboard","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateDashboardRequest","responds":"Dashboard"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreateDashboardRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","module","tiles"],"properties":{"name":{"type":"string","maxLength":200},"module":{"$ref":"#/components/schemas/common::ModuleKey","description":"**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid","description":"Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"},"isShared":{"type":"boolean","default":false},"tiles":{"type":"array","minItems":1,"maxItems":24,"items":{"$ref":"#/components/schemas/DashboardTile"}}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardData": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/Dashboard"},{"type":"object","properties":{"tileData":{"type":"array","items":{"type":"object","properties":{"tileId":{"type":"string","format":"uuid"},"result":{"$ref":"#/components/schemas/ReportResult"},"isCached":{"type":"boolean"},"error":{"type":"string","nullable":true}}}}}}]},
"DashboardTile": {"x-ticvai-persistence":"reporting.dashboard_tile","type":"object","required":["id","reportId","visualisation","position"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string"},"reportId":{"type":"string","format":"uuid"},"visualisation":{"type":"string","description":"**Extended 22 September from eight marks to twenty** against `Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`, which names eighteen components and marks every one MVP. Nine were genuinely missing — `combo`, `matrix`, `funnel`, `waterfall`, `treemap`, `scatter`, `map`, `ribbon`, `decompositionTree` — and three are layout variants of marks already here: `area` beside `line`, `donut` beside `pie`, `stackedBar100` beside `stackedBar`.\n**`number` is the source's KPI / card.** Its comparison, variance, trend sparkline and status icon are tile parameters rather than separate marks.\n**Two of the eighteen are deliberately not here** — see `x-ticvai-refuses`. The source lists them as components; the platform already models each of them elsewhere, and a second model of either is the drift this enum exists to prevent.\n","enum":["number","line","area","bar","stackedBar","stackedBar100","combo","pie","donut","table","matrix","gauge","heatmap","funnel","waterfall","treemap","scatter","map","ribbon","decompositionTree"],"x-ticvai-refuses":{"slicer":"**A control, not a mark.** The source's slicer / filter is already `ReportFilter.isParameter` plus `ReportParameter` — a run-time prompt bound to the report. A slicer on the canvas places that parameter; it does not render a result, so it is not a visualisation and a second filter model beside `ReportFilter` would be one somebody keeps in step by hand.","narrative":"**Generated prose belongs with `ai.Suggestion`.** The source's narrative / insight text (*\"Admissions are 12% above last Tuesday\"*) is model output with traceability requirements, not a way of drawing a query result.","cohort":"**Not one of the eighteen.** It appears once in the source as a *usage* — *\"the Customer & Membership dashboard shall use cards, cohort and trend charts\"* — never as a specified component. A cohort view is a `matrix` or `heatmap` over a cohort dimension."},"x-ticvai-note":"**The marks bind through the report's column encodings** (decided 2 October 2026, Chinmay; CHG-FIN-007: build the nine). Superseding the note of 22 September, which left `ReportColumn.role` undecided. Each column of the tile's report carries `role` and `encoding` (and `axis`, `seriesType`, `hierarchyLevel`, `unitLabel` where the mark needs them), and `createDashboard` / `updateDashboard` refuse 422 `tile-encoding-missing` a tile whose report lacks what its mark requires:\n\n| Mark | Requires | |---|---| | `combo` | one `x` dimension; two or more measures, each with `axis` and `seriesType`; `unitLabel` on a secondary axis | | `matrix` | `row` dimensions (with `hierarchyLevel`), optional `column` dimensions, one or more `value` measures | | `funnel` | one `stage` dimension in order (`sortOrder`), one `value` measure | | `waterfall` | one `category` dimension of ordered steps, one `value` measure; the steps are a named measure set (for example Gross sales, Discounts, Refunds, Net revenue) and the last is the total | | `treemap` | one or more `category` dimensions with `hierarchyLevel`, one `size` measure, optional `colour` measure | | `scatter` | an `x` and a `y` measure, a `label` dimension, optional `size` and `colour` | | `map` | one `location` dimension (venue, zone or venue-map point), one `value` measure | | `ribbon` | an `x` dimension (period), a `series` dimension, one `value` measure (rank flow) | | `decompositionTree` | one `value` measure and two or more dimensions with `hierarchyLevel` |\n\nThe other eleven marks bind as before (`number` one measure; `line`, `area`, `bar` and the stacked bars an `x` dimension, optional `series`, one or more `y` measures; `pie`, `donut`, `gauge`, `heatmap`, `table` as their names). **Unchanged**: at most 24 tiles a dashboard, and every tile shows its as-of time and goes stale past its refresh (`KpiValue.asOf`, `stale`; BOARDREQ MOM-2713/2714).\n"},"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose, and not yet specified.** Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as `RunReportRequest.parameters`) and its display settings — for `number`, the comparison, variance, sparkline and status icon. The per-visualisation display shape waits on the field-wells decision in `visualisation`'s `x-ticvai-note`.\n"},"refreshSeconds":{"type":"integer","minimum":30,"description":"Minimum thirty seconds. A tile refreshing every second is a load problem wearing a convenience costume.\n"},"position":{"type":"object","required":["row","column","width","height"],"properties":{"row":{"type":"integer"},"column":{"type":"integer"},"width":{"type":"integer"},"height":{"type":"integer"}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/subscription::LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]},
"WafRule": {"type":"object","x-ticvai-persistence":"control.waf_rule","description":"**Drafted 4 September.** One firewall rule, and the reason it is a row rather than a config file is that somebody has to be able to say who changed it and when.","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"name":{"type":"string"},"action":{"type":"string","enum":["allow","block","rateLimit","challenge"]},"matchOn":{"type":"string","description":"What the rule inspects - a path, a header, a source range."},"pattern":{"type":"string"},"enabled":{"type":"boolean"},"hitCount24h":{"type":"integer","description":"**A rule with no hits is either protecting nothing or blocking everything silently**, and both want looking at."},"updatedAt":{"type":"string","format":"date-time"}}}
}
```
