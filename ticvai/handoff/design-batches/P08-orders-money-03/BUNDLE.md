# P08-orders-money-03 — P08 · Orders & Money (3 of 3)

**6 screens · 33 operations · 34 schemas · 7 permissions**

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

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `ACCOUNT_CONFIGURE, LEDGER_APPROVE, LEDGER_POST, LEDGER_VIEW, ORDER_VIEW, SETTLEMENT_VIEW, TAX_CONFIGURE`. A control nobody can use must say so,
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
| `BO-075` | Account Mapping | A | 31 | 43 | 6 | 16 | 2 | 0 | — | notStarted (generated) |
| `BO-076` | Revenue Recognition | C | 16 | 18 | 6 | 74 | 2 | 0 | — | notStarted (generated) |
| `BO-077` | FX Rates & Variances | A | 15 | 24 | 6 | 1 | 2 | 4 | — | notStarted (generated) |
| `BO-089` | Journal Entries | C | 19 | 14 | 6 | 22 | 1 | 0 | — | notStarted (generated) |
| `BO-090` | Period Close | C | 5 | 22 | 6 | 11 | 1 | 0 | — | notStarted (generated) |
| `BO-101` | Orders & Money | A | 7 | 22 | 6 | 5 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-075` Account Mapping

**Which account each money event posts to, per venue, and the tax codes and exemptions that apply.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block A · ticket #28487 (APP-SETUP-BO-075) |
| Who uses it | venue staff holding `ACCOUNT_CONFIGURE`, `LEDGER_VIEW`, `TAX_CONFIGURE` (2 configure, 1 read); in the flows as finance controller, platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): 3 independent reads and no read of one record — the screen watches a population rather than working one |
| Offline | online only |
| Opens with | `taxCodeId` (deepLink), `exemptionId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/finance/account-mapping` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. Pulled to Wave 1 (CF-101). Without a mapping every sale posts to suspense. **Cross-platform navigation removed 24 August**: ADM-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **One switch, not two** (decided 2 October 2026, Chinmay; CHG-FIN-004). "Price includes tax" on a tax code (`isInclusive`) says whether the price already contains the tax. Whether tax is computed before or after a discount is not set here: it is the jurisdiction's taxable base on its tax profile (ADM-069, `TaxProfile.taxBase`), shown here read-only with the Egypt example. The calculation's own `discountsAreTaxInclusive` is deprecated and ignored. Mappings are per money event and venue (`AccountMapping.eventType`), not per product (design-note correction, 2 October 2026); a product-level GL code is not in the catalogue (DI-466 is answered by the event mapping).

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Which account each money event posts to, and the tax codes and exemptions those postings use. Without a mapping a sale posts to suspense. The one thing to get right: saving replaces the whole mapping set for the region, and four events must be mapped before any venue can trade, so the screen edits a complete set and shows what changes before saving.

**Fixed on main** (the package already carries these; draw what it says): The purpose says "which product or movement posts to which account". (CHG-SBO-012); The mapping set is drawn as tiles and a table with a single "Save" that takes only the mappings. (CHG-SBO-012); The create-exemption form asks for an id. (CHG-SBO-012); Two switches decide whether tax is computed before or after discount. (CHG-FIN-004).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Is a product-level GL code (DI-466) needed, or is event-type mapping enough?** → Drawn default accepted: Event-type mapping as contracted; draw no product account picker. *(decided by Chinmay, 2026-10-02; DEC-083 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Country code | text field | — | pattern `^[A-Z]{2}$` | `listTaxCodes` ?countryCode |

**Form: Create tax code** (modal, opened by *Create tax code*; *Create tax code* calls `createTaxCode`, *Cancel* sends nothing)

**Collects what `createTaxCode` sends before it is called.** Required: `code`, `name`, `countryCode`, `rate`, `accountId`, `effectiveFrom`. Optional: `compoundOnTaxCodeId`, `isInclusive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createTaxCode` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createTaxCode` body |
| Country code `countryCode` | text field | required | — | pattern `^[A-Z]{2}$` | — | — | `createTaxCode` body |
| Rate `rate` | stepper or slider | required | — | min 0; max 100 | — | — | `createTaxCode` body |
| Compound on tax code `compoundOnTaxCodeId` | picker: choose a compound on tax code | optional | — | — | shows names, sends the id | — | `createTaxCode` body |
| Is inclusive `isInclusive` | toggle | optional | off | — | — | — | `createTaxCode` body |
| Account `accountId` | picker: choose an account | required | — | — | shows names, sends the id | — | `createTaxCode` body |
| Effective from `effectiveFrom` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | A day in the region's time zone, local midnight to local midnight. | `createTaxCode` body |

Errors to draw in the form: 400 Compound reference is circular or crosses countries

**Form: Save tax code** (modal, opened by *Save tax code*; *Save tax code* calls `updateTaxCode`, *Cancel* sends nothing)

**Collects what `updateTaxCode` sends before it is called.** Nothing in the body is required. Optional: `name`, `rate`, `effectiveFrom`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 200 | — | — | `updateTaxCode` body |
| Rate `rate` | stepper or slider | optional | — | min 0; max 100 | — | — | `updateTaxCode` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Required with `rate`, and only meaningful with it. A day in the region's time zone, later than today. | `updateTaxCode` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateTaxCode` body |

Errors to draw in the form: 400 `rate` without `effectiveFrom`, or `effectiveFrom` without `rate`. `errors[]` names the field.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A rate change whose `effectiveFrom` is today or earlier, which would reprice postings already made; or a rate change addressed to a row that is no longer in …

**Form: Save account mappings** (modal, opened by *Save account mappings*; *Save account mappings* calls `setAccountMappings`, *Cancel* sends nothing)

**Collects what `setAccountMappings` sends before it is called.** Required: `mappings`. Sends the full set; the preview of the changes is shown in the dialog before it is sent. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Mappings `mappings` | repeatable rows | required | — | — | — | — | `setAccountMappings` body |
| Event type `mappings[].eventType` | select | required | — | Ticket revenue · Fnb revenue · Retail revenue · Rental revenue · Tax payable · Cash received · Card received · Wallet received · Refund issued · Void reversal · Deferred revenue · Recognised revenue … | — | Every event that generates a ledger posting. How each money event posts (decided 28 September, audit R191). | `setAccountMappings` body |
| Debit account `mappings[].debitAccountId` | picker: choose a debit account | required | — | — | shows names, sends the id | — | `setAccountMappings` body |
| Credit account `mappings[].creditAccountId` | picker: choose a credit account | required | — | — | shows names, sends the id | — | `setAccountMappings` body |
| Venue `mappings[].venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Null applies the mapping to every venue in the region. | `setAccountMappings` body |

Errors to draw in the form: 400 A required event type (`cardReceived`, `cashReceived`, `refundIssued`, `priceVariance`; audit R127 (1)) has no mapping, or maps to a non-postable account

**Form: Create tax exemption** (modal, opened by *Create tax exemption*; *Create tax exemption* calls `createTaxExemption`, *Cancel* sends nothing)

**Collects what `createTaxExemption` sends before it is called.** Required: `scope`, `taxCodeId`, `reason`. Optional: `scopeRef`, `exemptionType`, `certificateReference`, `evidenceDocumentId`, `verificationStatus`, `validFrom`, `validTo`. The exemption id is the server's. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Scope `scope` | radio group | required | — | Account · Product kind · Channel · Legal entity | — | — | `createTaxExemption` body |
| Scope ref `scopeRef` | text field | optional | — | — | — | Identifier of the exempt subject, matching `scope`. | `createTaxExemption` body |
| Tax code `taxCodeId` | picker: choose a tax code | required | — | — | shows names, sends the id | — | `createTaxExemption` body |
| Reason `reason` | text area | required | — | max length 500 | — | — | `createTaxExemption` body |
| Exemption type `exemptionType` | select | optional | — | Diplomatic · Export · Business to business · Charity · Government entity · Free zone · Zero rated · Other | — | Tax Exemption Evidence: exemption type (pack 'Pricing___Revenue_Management_Reference.pdf' p.47). | `createTaxExemption` body |
| Certificate reference `certificateReference` | text field | optional | — | max length 100 | — | Tax Exemption Evidence: reference, e.g. the exemption certificate, diplomatic card or export declaration number. | `createTaxExemption` body |
| Evidence document `evidenceDocumentId` | picker: choose an evidence document | optional | — | — | shows names, sends the id | Tax Exemption Evidence: the uploaded document (certificate scan, declaration). Kept for the retention period of the postings it exempted, not of the exemption. | `createTaxExemption` body |
| Verification status `verificationStatus` | radio group | optional | Pending | Not required · Pending · Verified · Rejected · Expired | — | Tax Exemption Evidence: verification status. Only `verified` and `notRequired` exempt a line; `calculateTax` treats `pending`, `rejected` and `expired` as no exemption and records … | `createTaxExemption` body |
| Valid from `validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Tax Exemption Evidence: validity, first day. A day in the region's time zone, local midnight to local midnight. | `createTaxExemption` body |
| Valid to `validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Tax Exemption Evidence: validity, last day. A day in the region's time zone, local midnight to local midnight. | `createTaxExemption` body |

**Sent by *Verify tax exemption*** (`verifyTaxExemption`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Verification status `verificationStatus` | segmented control | required | — | Verified · Rejected | — | — | `verifyTaxExemption` body |
| Evidence document `evidenceDocumentId` | picker: choose an evidence document | optional | — | — | shows names, sends the id | Replaces the evidence document on the record when given. | `verifyTaxExemption` body |
| Certificate reference `certificateReference` | text field | optional | — | max length 100 | — | — | `verifyTaxExemption` body |
| Note `note` | text area | optional | — | max length 500 | — | Required with `rejected`. | `verifyTaxExemption` body |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Mapping row (event → debit account, credit account, venue)**: One row per money event (card received, cash received, refund issued, price variance, ticket, food, retail and rental revenue, VAT payable, deferred, recognised and breakage revenue, cash over/short, settlement fees, chargebacks…). Venue empty means every venue in the region; a venue row overrides it. Card received, cash received, refund issued and price variance are required and marked so. *(source: contracts/spine/finance.yaml#/components/schemas/PostingEventType / contracts/spine/finance.yaml#/components/schemas/AccountMapping / R127)*
- **Tax code**: Code, name, country, rate 0–100 (0% is a valid rate, e.g. donations where untaxed), the account the tax posts to, effective from (future-dated: a rate change is a new row, history keeps the old rate), inclusive or exclusive, and optionally "applies on top of" another code for tax on tax. Show the application order explicitly. *(source: contracts/spine/finance.yaml#/components/schemas/TaxCode / DI-596 / DI-472)*
- **Tax exemption**: Scope (customer account, product kind, channel, legal entity), the tax code, reason, exemption type (diplomatic, export, business-to-business, charity, government, free zone, zero-rated, other), certificate reference, evidence document, validity. Only verified or not-required exemptions take effect; pending, rejected or expired ones do not. *(source: contracts/spine/finance.yaml#/components/schemas/TaxExemption)*

#### Outputs: what the screen shows and produces

**Shown**

**Account mappings** (metric tile, from `listAccountMappings`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Event type | chip: Ticket revenue, Fnb revenue, Retail revenue, Rental revenue, Tax payable, Cash … | Every event that generates a ledger posting. How each money event posts (decided 28 September, audit R191). |
| Debit account | the name it points at, never the id | — |
| Credit account | the name it points at, never the id | — |
| Venue | the name it points at, never the id | Null applies the mapping to every venue in the region. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Tax codes** (metric tile, from `listTaxCodes`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Country code | text | — |
| Applies to | list or chips (count when long) | What this code covers, and `donation` is why the field exists (CF-84). Donation tax treatment varies by jurisdiction — 0% is a valid rate … |
| Rate | 1,234.5 | — |
| Compound on tax code | the name it points at, never the id | When set, this tax applies to the base plus the referenced tax, not to the base alone. |
| Is inclusive | yes / no (icon or chip) | True when the displayed price already contains this tax. |
| Account | the name it points at, never the id | — |
| Effective from | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Effective to | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Is active | yes / no (icon or chip) | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Tax exemptions** (metric tile, from `listTaxExemptions`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Scope | chip: Account, Product kind, Channel, Legal entity | — |
| Scope ref | text | Identifier of the exempt subject, matching `scope`. |
| Tax code | the name it points at, never the id | — |
| Reason | text | — |
| Exemption type | chip: Diplomatic, Export, Business to business, Charity, Government entity, Free zone… | Tax Exemption Evidence: exemption type (pack 'Pricing___Revenue_Management_Reference.pdf' p.47). |
| Certificate reference | text | Tax Exemption Evidence: reference, e.g. the exemption certificate, diplomatic card or export declaration number. |
| Evidence document | the name it points at, never the id | Tax Exemption Evidence: the uploaded document (certificate scan, declaration). Kept for the retention period of the postings it exempted … |
| Verification status | chip: Not required, Pending, Verified, Rejected, Expired | Tax Exemption Evidence: verification status. Only `verified` and `notRequired` exempt a line; `calculateTax` treats `pending`, `rejected` … |
| Verified by | the name it points at, never the id | — |
| Verified at | 1 Oct 2026, 14:30 | — |
| Verification note | text | The `note` given to `verifyTaxExemption`; required when evidence was rejected. |
| Valid from | 1 Oct 2026 | Tax Exemption Evidence: validity, first day. A day in the region's time zone, local midnight to local midnight. |
| Valid to | 1 Oct 2026 | Tax Exemption Evidence: validity, last day. A day in the region's time zone, local midnight to local midnight. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Every account mapping** (data table, from `listAccountMappings`): The whole mapping set, editable in place: `setAccountMappings` replaces the region's whole set, so the screen shows every row and a change preview (rows added, changed, removed) before Save.

| Shows | Format | Notes |
|---|---|---|
| Event type | chip: Ticket revenue, Fnb revenue, Retail revenue, Rental revenue, Tax payable, Cash … | Every event that generates a ledger posting. How each money event posts (decided 28 September, audit R191). |
| Debit account | the name it points at, never the id | — |
| Credit account | the name it points at, never the id | — |
| Venue | the name it points at, never the id | Null applies the mapping to every venue in the region. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save account mappings (primary button) | `setAccountMappings` PUT `/account-mappings` | inline | AccountMapping[] | 400 A required event type (`cardReceived`, `cashReceived`, `refundIssued`, `priceVariance`; audit R127 (1)) has no mapping, or maps to a non-postable account | opens modal first |
| Create tax code (secondary button) | `createTaxCode` POST `/tax-codes` | CreateTaxCodeRequest | TaxCode | 400 Compound reference is circular or crosses countries | opens modal first |
| Save tax code (secondary button) | `updateTaxCode` PATCH `/tax-codes/{taxCodeId}` | inline | TaxCode | 400 `rate` without `effectiveFrom`, or `effectiveFrom` without `rate`. `errors[]` names the field.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 A rate … | opens modal first |
| Create tax exemption (secondary button) | `createTaxExemption` POST `/tax-exemptions` | TaxExemption | TaxExemption | — | opens modal first |
| Verify tax exemption (primary button) | `verifyTaxExemption` POST `/tax-exemptions/{exemptionId}/verify` | inline | TaxExemption | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The exemption is `expired`, or `notRequired`.; 422 `verified` with no evidence document on the record or in the … | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Mapping set**: Grouped: receipts, revenue, tax, deferral and recognition, variances, settlement, chargebacks. Unmapped events show "Posts to suspense" in amber; the four required ones in red until mapped. *(source: contracts/spine/finance.yaml#/components/schemas/PostingEventType)*
- **Tax codes**: Active codes with rate, inclusive or exclusive, compounding and effective dates; future rates listed under the current one. *(source: contracts/spine/finance.yaml#/components/schemas/TaxCode)*
- **Exemptions waiting for verification**: Pending evidence first, with its expiry; a verify action with a note (required when rejecting). *(source: contracts/spine/finance.yaml#/components/schemas/TaxExemption / contracts/spine/finance.yaml#verifyTaxExemption)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save mappings**: Shows the change list (added, changed, removed) and saves the full set; postings already made keep their accounts. Refused, with the missing event named, if a required event is unmapped. *(source: contracts/spine/finance.yaml#setAccountMappings)*
- **Verify exemption**: Records verified or rejected with who and when; a rejection needs a note. *(source: contracts/spine/finance.yaml#/components/schemas/TaxExemption)*

**Data it reads**: `listAccountMappings` (onLoad, Which account each transaction type posts to); `listTaxCodes` (onLoad, List tax codes); `listTaxExemptions` (onLoad, List tax exemptions)

**Where the user goes next**

- → `BO-076` Revenue Recognition: *Revenue Recognition*
- → `BO-074` Chart of Accounts: *Chart of Accounts*; carries `accountId`
- → `BO-077` FX Rates & Variances: *FX Rates & Variances*
- → `ADM-020` Platform User Directory: *Creates the first venue manager*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The account mapping figures; each tile loads on its own. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the account mapping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No account mapping yet. Offers Create tax code (`createTaxCode`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listAccountMappings` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listAccountMappings` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCOUNT_CONFIGURE` for `setAccountMappings`; `TAX_CONFIGURE` for `createTaxCode`, `updateTaxCode`, `createTaxExemption`, `verifyTaxExemption`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A required event type (`cardReceived`, `cashReceived`, `refundIssued`, `priceVariance`; audit R127 (1)) has no mapping, or maps to a non-postable account; 400 Compound reference is circular or crosses countries; 400 `rate` without `effectiveFrom`, or `effectiveFrom` without `rate`. `errors[]` names the field.; 409 A rate change whose `effectiveFrom` is today or earlier, which would reprice … |

#### Edge cases to draw

- **A row is left out of the set when saving**: The change list shows it as removed ("Refunds will post to suspense") before confirming. *(source: contracts/spine/finance.yaml#setAccountMappings)*
- **Suspense balance is not zero**: A banner with the balance and the events that fed it, linking to the chart. *(source: contracts/spine/finance.yaml#/components/schemas/Account)*

#### Consistency with other screens

- Match `ADM-069`: The tax profile (type, jurisdiction, taxable base) lives on ADM-069 in the catalogue; the tax code (rate, account, compounding) lives here in finance. Use the same tax names on both.
- Match `BO-074`: Account pickers show the chart's codes and names.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
mappings:
- Card received · Dr 1120 Card clearing · Cr 1190 Sales control · all venues
- Ticket revenue · Dr 1190 Sales control · Cr 2300 Deferred revenue · all venues
- Cash over/short · Dr 6900 Cash over/short · Cr 1100 Cash on hand
- Price variance · not mapped (required)
taxCodes:
- VAT-AE-5 · UAE VAT standard · 5% · inclusive · posts to 2400 · from 1 Jan 2018
- VAT-AE-0 · Zero-rated export · 0%
- EG-VAT-14 · Egypt VAT · 14% · exclusive
exemption: Free zone · VAT-AE-5 · Dubai Silicon Oasis Authority · certificate DSOA-2026-1142 · pending · valid to
  31 Dec 2026
```

#### Permissions

- `listAccountMappings` → `LEDGER_VIEW` (read) · staff
- `setAccountMappings` → `ACCOUNT_CONFIGURE` (configure) · staff
- `listTaxCodes` → `LEDGER_VIEW` (read) · staff
- `createTaxCode` → `TAX_CONFIGURE` (configure) · staff
- `updateTaxCode` → `TAX_CONFIGURE` (configure) · staff
- `listTaxExemptions` → `LEDGER_VIEW` (read) · staff
- `createTaxExemption` → `TAX_CONFIGURE` (configure) · staff
- `verifyTaxExemption` → `TAX_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listAccountMappings` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCOUNT_CONFIGURE` for `setAccountMappings`; `TAX_CONFIGURE` for `createTaxCode`, `updateTaxCode`, `createTaxExemption`, `verifyTaxExemption`.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.2 | The system should be able to store account information for each Offset/Balancing Account by Payment Type (e.g. cash, bank card, tax, etc.). At minimum, the below fields should be included for … | F&B & Guest Management | CONTRACTED | `setAccountMappings` |
| 5.7.3 | The system should be able to store account information for each Revenue Account by Item or Item Type (Merchandise, etc.). At minimum, the below fields should be included for storage: - Company I … | F&B & Guest Management | CONTRACTED | `setAccountMappings` |
| 5.7.6 | The system allow general ledger revenue rules to be configured to trigger account allocation based on product sale and redemption events. Revenue allocation rules can be defined for all products and … | F&B & Guest Management | CONTRACTED | `setAccountMappings` |
| 5.7.87 | The system shall support configurable mapping between operational transactions and accounting accounts. Examples include Ticket Revenue to Revenue Account, Wallet Liability to Deferred Revenue, VAT … | F&B & Guest Management | CONTRACTED | `setAccountMappings` |
| 5.12.36 | Support site-level account mappings. | F&B & Guest Management | CONTRACTED | `setAccountMappings` |
| 5.12.37 | Support multi-site revenue reporting. | F&B & Guest Management | CONTRACTED | `setAccountMappings` |
| 5.12.38 | Support consolidated group reporting. | F&B & Guest Management | CONTRACTED | `setAccountMappings` |
| 5.12.67 | Site-level revenue reports. | F&B & Guest Management | CONTRACTED | `setAccountMappings` |
| 7.4.31 | For each PLU, it is possible to manage the company to which the ticket revenue shall be attached to. | F&B POS | CONTRACTED | `setAccountMappings` |
| 7.4.32 | Disbursement rules might be used to distribute the revenue either between parks or departments. | F&B POS | CONTRACTED | `setAccountMappings` |
| 7.4.50 | Support accounting rules where revenue can be recognized over time, by visit, by consumption or according to accounting standards such as IFRS. | F&B POS | CONTRACTED | `setAccountMappings` |
| 2.9.11 | The system should be able to support multiple tax rates (service charge, GST, VAT, etc.) and tax profiles for different products to conform to actual and future local regulatory requirements. There … | Ticketing Sales | CONTRACTED | `createTaxCode` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Chart of accounts screen: external-system codes for ERP mapping, classification (asset, liability, income, expense), parent-account hierarchy and edit view with financial dimensions (profit centre, cost centres); plus transaction-to-account and payment/offset account mapping. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-262)*
- Chart of accounts can be created natively in TICVAI or mapped to a client's external/ERP chart of accounts. *(agreed · MoM 12 Aug 2026, 13. Chart of Accounts and Account Mapping · DI-259)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-075` · status **notStarted** · provenance generated
- Flow F16 *A venue opens for the first time*, step 6: Maps products to accounts → Or everything lands in suspense
- Flow F98 *A day is reconciled from takings to the ledger*, step 3: Account Mapping. → 5 operations, 5 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (31), with its required mark, default, format and its error state (400, 404, 409, 422).
- [ ] Every output is drawn (43 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-075?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save account mappings, Create tax code, Save tax code, Create tax exemption, Verify tax exemption.
- [ ] Every transition is wired: `BO-076`, `BO-074`, `BO-077`, `ADM-020`.
- [ ] Every gated control is gated: `ACCOUNT_CONFIGURE`, `LEDGER_VIEW`, `TAX_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-076` Revenue Recognition

**Deferred revenue, its ageing, and the schedules that release it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `core` module |
| Block | Block C · task VM-BO-076 |
| Who uses it | venue staff holding `ACCOUNT_CONFIGURE`, `LEDGER_POST`, `LEDGER_VIEW` (1 configure, 1 operate, 1 read); in the flows as finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRecognitionSchedules` reads the population and `getDeferredRevenue` reads one of them — list, select, act |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/finance/revenue-recognition` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Deferred revenue (paid for, not yet earned), when it will unwind, and the rules that release it: ticket revenue on the visit, gift cards and wallet on use, annual passes straight-line or per visit, unredeemed value as breakage on expiry, no-shows when the performance ends. The one thing to get right: a product kind may be claimed by only one rule, because two rules claiming it recognise the same revenue twice and the numbers still look plausible.

**Known correction pending (do not draw the wrong version)**

- **Rules can be created and validated but not edited or deactivated.** Why: No update operation exists, although the rule carries an active flag. *(source: contracts/spine/finance.yaml#/components/schemas/RecognitionSchedule / screens/P08-venue-back-office.yaml#BO-076; Finance, Ledger & Tax · Reporting & Analytics)*
- **The create form lists the rule id as required.** Why: The id is server-owned. *(source: contracts/spine/finance.yaml#/components/schemas/RecognitionSchedule; Finance, Ledger & Tax · Reporting & Analytics)*
- **The revenue allocation split builder from 12 August is not on this screen or any contract.** Why: Splitting a combo or two-venue pass across products or legal entities was agreed; fixed against percentage is still open. *(source: DI-267 / MoM 2026-08-12 16. Revenue Recognition Rules and Allocation Splits; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **POS sales recognise immediately (12 August) but rules are per product kind, not per channel. How is a POS-sold dated ticket treated?** → Drawn default stands (answer: "By the product kind's rule (a dated ticket is recognised at admission)"): By its product kind's rule; recognised at admission the same day. *(decided by Chinmay, 2026-10-02; DEC-216 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| As at | date picker | — | — | `getDeferredRevenue` ?asAt |

**Form: Run recognition** (modal, opened by *Run recognition*; *Run recognition* calls `runRecognition`, *Cancel* sends nothing)

**Collects what `runRecognition` sends before it is called.** Required: `fiscalPeriodId`. Optional: `dryRun`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Fiscal period `fiscalPeriodId` | picker: choose a fiscal period | required | — | — | shows names, sends the id | — | `runRecognition` body |
| Dry run `dryRun` | toggle | optional | off | — | — | Compute and return without posting. | `runRecognition` body |

Errors to draw in the form: 409 Period already closed, or a run is in progress

**Form: Create recognition schedule** (modal, opened by *Create recognition schedule*; *Create recognition schedule* calls `createRecognitionSchedule`, *Cancel* sends nothing)

**Collects what `createRecognitionSchedule` sends before it is called.** Required: `name`, `method`, `productKinds`. Optional: `priority`, `recognitionSite`, `frequency`, `revalidateOnValidityChange`, `deferredAccountId`, `recognisedAccountId`, `breakageAccountId`, `noShowTrigger`, `noShowAccountId`, `breakageAfterDays`, `isActive`. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `id` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createRecognitionSchedule` body |
| Method `method` | radio group | required | — | Immediate · On redemption · Straight line · Per visit · On expiry | — | — | `createRecognitionSchedule` body |
| Priority `priority` | number field | optional | 100 | Lowest priority wins, and two schedules at the same priority claiming the same kind is refused at save rather than resolved at run time. | — | Two schedules may both claim a product kind and nothing resolved which wins — a silent double-recognition, which is the worst kind of accounting defect because the numbers look … | `createRecognitionSchedule` body |
| Recognition site `recognitionSite` | segmented control | optional | Sale | Sale · Admission · Consumption | — | Where revenue is earned, which is not always where it was sold. A ticket sold at one venue and admitted at another earns at the gate, and recognising at the sale site puts the … | `createRecognitionSchedule` body |
| Frequency `frequency` | radio group | optional | On period close | Daily · Weekly · Monthly · On event · On period close | — | Driven by the schedule rather than by whoever runs the job. Recognition that happens when somebody remembers is recognition with no cut-off. | `createRecognitionSchedule` body |
| Revalidate on validity change `revalidateOnValidityChange` | toggle | optional | on | — | — | Changing an entitlement's validity did not re-time its deferred balance. A pass extended by three months has three more months of deferral, and a schedule that ignores that … | `createRecognitionSchedule` body |
| Product kinds `productKinds` | multi-select chips | required | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card; at least 1 | — | The product kinds this schedule claims, from the catalogue's `ProductKind`. | `createRecognitionSchedule` body |
| Deferred account `deferredAccountId` | picker: choose a deferred account | optional | — | — | shows names, sends the id | — | `createRecognitionSchedule` body |
| Recognised account `recognisedAccountId` | picker: choose a recognised account | optional | — | — | shows names, sends the id | — | `createRecognitionSchedule` body |
| Breakage account `breakageAccountId` | picker: choose a breakage account | optional | — | — | shows names, sends the id | — | `createRecognitionSchedule` body |
| No show trigger `noShowTrigger` | segmented control | optional | — | Performance end · Validity end · None | — | 8.1.1. A no-show is breakage with a known moment, and the mechanism already existed — `breakageAfterDays` moves deferred revenue to earned after a period. | `createRecognitionSchedule` body |
| No show account `noShowAccountId` | picker: choose a no show account | optional | — | — | shows names, sends the id | Where no-show revenue lands. Separate from `recognisedAccountId` by default, because revenue from a guest who came and revenue from one who did not are different lines to whoever … | `createRecognitionSchedule` body |
| Breakage after days `breakageAfterDays` | number field (days) | optional | — | — | — | Days after expiry at which unredeemed value becomes breakage. | `createRecognitionSchedule` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createRecognitionSchedule` body |

Errors to draw in the form: 400 Validation failed; 409 An active schedule at the same `priority` already claims one of these product kinds.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Recognition rule**: Name, method (Immediately, On redemption, Straight line, Per visit, On expiry), product kinds claimed, priority (lower wins; equal priority on the same kind is refused), where revenue is earned (Sale, Admission, Consumption: a ticket sold at one venue and admitted at another earns at the gate; a wallet top-up earns when spent), how often it runs (default at period close), deferred, recognised, breakage and no-show accounts, breakage after N days, no-show trigger. *(source: contracts/spine/finance.yaml#/components/schemas/RecognitionSchedule / contracts/spine/finance.yaml#/components/schemas/RecognitionMethod)*
- **Run recognition**: A fiscal period and a dry run first; the dry run shows recognised and breakage totals by method before posting. *(source: contracts/spine/finance.yaml#runRecognition / contracts/spine/finance.yaml#/components/schemas/RecognitionRunResult)*

#### Outputs: what the screen shows and produces

**Shown**

**Every recognition schedule** (data table, from `listRecognitionSchedules`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Method | chip: Immediate, On redemption, Straight line, Per visit, On expiry | — |
| Priority | 1,234 | Two schedules may both claim a product kind and nothing resolved which wins — a silent double-recognition, which is the worst kind of … |
| Recognition site | chip: Sale, Admission, Consumption | Where revenue is earned, which is not always where it was sold. A ticket sold at one venue and admitted at another earns at the gate, and … |
| Frequency | chip: Daily, Weekly, Monthly, On event, On period close | Driven by the schedule rather than by whoever runs the job. Recognition that happens when somebody remembers is recognition with no cut-off. |
| Revalidate on validity change | yes / no (icon or chip) | Changing an entitlement's validity did not re-time its deferred balance. A pass extended by three months has three more months of deferral … |

**The selected recognition schedule** (detail panel, from `listRecognitionSchedules`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Method | chip: Immediate, On redemption, Straight line, Per visit, On expiry | — |
| Priority | 1,234 | Two schedules may both claim a product kind and nothing resolved which wins — a silent double-recognition, which is the worst kind of … |
| Recognition site | chip: Sale, Admission, Consumption | Where revenue is earned, which is not always where it was sold. A ticket sold at one venue and admitted at another earns at the gate, and … |
| Frequency | chip: Daily, Weekly, Monthly, On event, On period close | Driven by the schedule rather than by whoever runs the job. Recognition that happens when somebody remembers is recognition with no cut-off. |
| Revalidate on validity change | yes / no (icon or chip) | Changing an entitlement's validity did not re-time its deferred balance. A pass extended by three months has three more months of deferral … |
| Product kinds | list or chips (count when long) | The product kinds this schedule claims, from the catalogue's `ProductKind`. |
| No show trigger | chip: Performance end, Validity end, None | 8.1.1. A no-show is breakage with a known moment, and the mechanism already existed — `breakageAfterDays` moves deferred revenue to earned … |

**The deferred revenue report** (detail panel, from `getDeferredRevenue`)

| Shows | Format | Notes |
|---|---|---|
| As at | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Totals | list or chips (count when long) | One `Money` per currency in scope, never a sum across currencies. One entry when every venue in scope trades in the same currency. |
| Total | AED 1,234.50 | The single total when everything in scope is in one currency; null otherwise. Read `totals`. |
| Buckets | list or chips (count when long) | One ageing band in one currency per entry. A band spanning two currencies is two entries. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run recognition (primary button) | `runRecognition` POST `/recognition/run` | inline | RecognitionRunResult | 409 Period already closed, or a run is in progress | opens modal first |
| Create recognition schedule (secondary button) | `createRecognitionSchedule` POST `/recognition-schedules` | RecognitionSchedule | RecognitionSchedule | 400 Validation failed; 409 An active schedule at the same `priority` already claims one of these product kinds. | opens modal first |
| Validate recognition schedules (secondary button) | `validateRecognitionSchedules` POST `/recognition-schedules/validate` | — | inline | — | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Deferred balance**: One total per currency, never summed across currencies, then ageing bands by expected recognition date, each with items and method. A chart of recognised against still-deferred (wallet and passes) by month. *(source: contracts/spine/finance.yaml#getDeferredRevenue / DI-266)*
- **Rules list**: Method, kinds, priority, site, frequency, accounts; conflicts found by validation flagged in red. *(source: contracts/spine/finance.yaml#validateRecognitionSchedules)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Validate rules**: Lists product kinds claimed by more than one rule. *(source: contracts/spine/finance.yaml#validateRecognitionSchedules)*
- **Run recognition**: Posts the moves; running the same period again finds nothing left and says "Nothing to recognise", not an error. *(source: contracts/spine/finance.yaml#runRecognition)*

**Data it reads**: `getDeferredRevenue` (onLoad, Deferred revenue balance and ageing); `listRecognitionSchedules` (onLoad, List revenue recognition schedules)

**Where the user goes next**

- → `BO-074` Chart of Accounts: *Chart of Accounts*
- → `BO-075` Account Mapping: *Account Mapping*
- → `BO-077` FX Rates & Variances: *FX Rates & Variances*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue recognition list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue recognition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue recognition yet. Offers Create recognition schedule (`createRecognitionSchedule`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listRecognitionSchedules` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `getDeferredRevenue` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCOUNT_CONFIGURE` for `createRecognitionSchedule`; `LEDGER_POST` for `runRecognition`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An active schedule at the same `priority` already claims one of these product kinds.; 409 Period already closed, or a run is in progress |

#### Edge cases to draw

- **A pass's validity is extended by three months**: Its deferred balance re-times; the ageing moves out. *(source: contracts/spine/finance.yaml#/components/schemas/RecognitionSchedule)*
- **The period is closing**: Run is still allowed for the closing period until it is closed; the close check "Recognition run complete" turns green. *(source: contracts/spine/finance.yaml#/components/schemas/PeriodCloseResult)*

#### Consistency with other screens

- Match `BO-090`: Recognition run complete is a close check.
- Match `BO-1081`: Recognised and deferred figures must be the same numbers on the finance dashboard.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
deferred: AED 1,842,350.00 deferred · 0–30 days AED 612,400.00 (8,214 items, on redemption) · 31–90 AED 498,950.00
  · 91–365 AED 731,000.00 (annual passes, straight line)
rules:
- Admission tickets · On redemption · site Admission · priority 100
- Annual pass · Straight line · AED 1,800.00 → AED 150.00 a month · priority 50
- Gift cards and wallet · On redemption · site Consumption · breakage 365 days after expiry
```

#### Permissions

- `getDeferredRevenue` → `LEDGER_VIEW` (read) · staff
- `runRecognition` → `LEDGER_POST` (operate) · staff
- `listRecognitionSchedules` → `LEDGER_VIEW` (read) · staff
- `createRecognitionSchedule` → `ACCOUNT_CONFIGURE` (configure) · staff
- `validateRecognitionSchedules` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `getDeferredRevenue` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `ACCOUNT_CONFIGURE` for `createRecognitionSchedule`; `LEDGER_POST` for `runRecognition`.

#### Requirements it meets

74 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.12.117 | Deferred Revenue Management | F&B & Guest Management | CONTRACTED | `getDeferredRevenue` |
| 5.12.118 | Deferred Revenue Management | F&B & Guest Management | CONTRACTED | `getDeferredRevenue` |
| 5.12.119 | Deferred Revenue Management | F&B & Guest Management | CONTRACTED | `getDeferredRevenue` |
| 5.12.120 | Deferred Revenue Management | F&B & Guest Management | CONTRACTED | `getDeferredRevenue` |
| 5.12.121 | Deferred Revenue Management | F&B & Guest Management | CONTRACTED | `getDeferredRevenue` |
| 5.12.122 | Deferred Revenue Management | F&B & Guest Management | CONTRACTED | `getDeferredRevenue` |
| 5.12.123 | Deferred Revenue Management | F&B & Guest Management | CONTRACTED | `getDeferredRevenue` |
| 5.12.124 | Deferred Revenue Management | F&B & Guest Management | CONTRACTED | `getDeferredRevenue` |
| 5.12.125 | Deferred Revenue Management | F&B & Guest Management | CONTRACTED | `getDeferredRevenue` |
| 4.3.36 | Gift Card Liability Reporting | Bundles and Promotions | CONTRACTED | `runRecognition` |
| 4.3.37 | Gift Card Breakage & Revenue Recognition | Bundles and Promotions | CONTRACTED | `runRecognition` |
| 5.7.12 | The system should be able generate offsetting entries when an admission ticket expires (e.g., debit unearned revenue, credit revenue). If a ticket is not used, the system will need to get revenue … | F&B & Guest Management | CONTRACTED | `runRecognition` |
| … 62 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Revenue allocation split builder splits a combo/package price across products (tickets, F&B) or legal entities (e.g. a two-venue two-day pass), by fixed amount or percentage. *(agreed · MoM 12 Aug 2026, 16. Revenue Recognition Rules and Allocation Splits · DI-267)*
- Revenue allocation screen graphs recognised vs unrecognised (wallet) revenue and holds recognition rules, e.g. F&B on sale; annual membership straight-line monthly (1,500 AED → 150 AED/month, balance at expiry). *(client request · MoM 12 Aug 2026, 16. Revenue Recognition Rules and Allocation Splits · DI-266)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-076` · status **notStarted** · provenance generated
- Flow F98 *A day is reconciled from takings to the ledger*, step 4: Revenue Recognition. → 4 operations, 4 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-076?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run recognition, Create recognition schedule, Validate recognition schedules.
- [ ] Every transition is wired: `BO-074`, `BO-075`, `BO-077`.
- [ ] Every gated control is gated: `ACCOUNT_CONFIGURE`, `LEDGER_POST`, `LEDGER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-077` FX Rates & Variances

**Rates, and the price variances waiting for review.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block A · ticket #28485 (APP-SETUP-BO-077) |
| Who uses it | venue staff holding `LEDGER_APPROVE`, `LEDGER_VIEW` (1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `reviewPriceVariance` decides items that `listFxRates` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `varianceId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/finance/fx-rates-variances` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **The tender rate now charges guests** (decided 2 October 2026, Chinmay; CHG-FIN-001). A `tender` rate is what a guest who selects a currency is charged at (locked on the order at checkout) and refunded at; a rate change never moves an order already quoted. Per region, as before (audit R120 (a)); the venue chooses which currencies it shows and which it charges (`VenueSettings.displayCurrencies`, `chargeCurrencies`).

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Two finance queues in one place: the exchange rates in force for the region (set by hand with a margin, or pulled from a provider), and the price variances waiting for review, where a till priced a sale differently from the server. The one thing to get right: a rate change never edits a rate; it adds a new one from a date, so the screen shows rates as a timeline and every manual rate carries a reason.

**Fixed on main** (the package already carries these; draw what it says): The queue "Waiting for a decision" binds exchange rates. (CHG-SBO-012); The set-rate form offers server-owned fields (id, source, set-by, provider reference, fetched at) and omits the note. (CHG-SBO-012); The screen is wave 2 while it is in the Block A set-up tickets. (CHG-SBO-012).

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Should the margin over market be stored, or only the resulting rate?** → Drawn default accepted: Only the rate, with the margin stated in the note. *(decided by Chinmay, 2026-10-02; DEC-084 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| As at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?asAt=` to `listFxRates`. | `listFxRates` ?asAt |
| Purpose | radio group | optional | — | Tender · Inter entity · Reporting · Revaluation | — | Sends `?purpose=` to `listFxRates`. | `listFxRates` ?purpose |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Chargeable | toggle | — | — | `listFxRates` ?chargeable |
| Exceptions only | toggle | off | — | `listPriceVariances` ?exceptionsOnly |
| Review status | segmented control | — | Not required · Pending review · Reviewed | `listPriceVariances` ?reviewStatus |
| Occurred from | date picker | — | — | `listPriceVariances` ?occurredFrom |
| Occurred to | date picker | — | — | `listPriceVariances` ?occurredTo |

**Form: Ingest FX rates** (modal, opened by *Ingest FX rates*; *Ingest FX rates* calls `ingestFxRates`, *Cancel* sends nothing)

**Collects what `ingestFxRates` sends before it is called.** Required: `purpose`. Optional: `pairs`, `effectiveFrom`, `dryRun`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Purpose `purpose` | radio group | required | — | Tender · Inter entity · Reporting · Revaluation | — | A venue does not accept dollars at the rate it books an intercompany balance at. | `ingestFxRates` body |
| Pairs `pairs` | list of values (chips) | optional | — | — | — | `AED/USD` form. Omitted means every pair this region trades in. | `ingestFxRates` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to the next business day in the region timezone. A day in the region's time zone: the rates written take effect at local midnight at the start of it, stored as that … | `ingestFxRates` body |
| Dry run `dryRun` | toggle | optional | off | — | — | Fetch and report without writing. A rate that moved four percent overnight is worth a person seeing before it prices anything. | `ingestFxRates` body |

Errors to draw in the form: 409 No provider is assigned to this purpose in this region (`setFxProvider`).

**Form: Review price variance** (modal, opened by *Review price variance*; *Review price variance* calls `reviewPriceVariance`, *Cancel* sends nothing)

**Collects what `reviewPriceVariance` sends before it is called.** Required: `outcome`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | segmented control | required | — | Accepted · Investigated · Catalogue corrected | — | — | `reviewPriceVariance` body |
| Note `note` | text area | required | — | min length 3; max length 1000 | — | — | `reviewPriceVariance` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The variance is not awaiting review: its `reviewStatus` is `notRequired` (below the venue's threshold) or already `reviewed`.

**Form: Save FX rate** (modal, opened by *Save FX rate*; *Save FX rate* calls `setFxRate`, *Cancel* sends nothing)

**Collects what `setFxRate` sends before it is called.** Required: `fromCurrency`, `toCurrency`, `rate`, `purpose`, `effectiveFrom`. Optional: `effectiveTo`, `note`. **The note is required for a manual rate** and the call is refused without it (R127); set-by, provider reference and fetched-at are the server's. Dismissing sends nothing; the screen behind is unchanged. Not asked, because the server sets it (readOnly in the contract): `source` (3 October 2026, CHG-SPF-001).

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| From currency `fromCurrency` | text field | required | — | pattern `^[A-Z]{3}$` | — | — | `setFxRate` body |
| To currency `toCurrency` | text field | required | — | pattern `^[A-Z]{3}$` | — | — | `setFxRate` body |
| Rate `rate` | text field | required | — | pattern `^\d+(\.\d{1,6})?$` | — | Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly. | `setFxRate` body |
| Purpose `purpose` | radio group | required | — | Tender · Inter entity · Reporting · Revaluation | — | A venue does not accept dollars at the rate it books an intercompany balance at. | `setFxRate` body |
| Effective from `effectiveFrom` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setFxRate` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | A rate change is a new row. The old one is never edited — a transaction posted last Tuesday must still reconcile at last Tuesday's rate. | `setFxRate` body |
| Note `note` | text area | optional | — | max length 500; Required when `source` is `manual` (decided 28 September, audit R127 (4)); null on a rate `ingestFxRates` fetched. | — | Why this rate, and from where. Required when `source` is `manual` (decided 28 September, audit R127 (4)); null on a rate `ingestFxRates` fetched. | `setFxRate` body |

Errors to draw in the form: 400 No `note` was given. A manual rate says where the figure came from (audit R127 (4)).; 409 Effective window overlaps an existing bounded rate for the same pair and purpose, or does not start after the rate in force

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Set a rate**: From currency, to currency, rate (up to six decimals), purpose (Tender = what guests pay at, Reporting, Revaluation, Inter-entity), effective from, optional end, and a required note saying why and from where. The new rate closes the open-ended one in force at its start; a window that overlaps a bounded one is refused. *(source: contracts/spine/finance.yaml#setFxRate / contracts/spine/finance.yaml#/components/schemas/FxRate / R127)*
- **Margin helper**: Optional: show the latest provider rate as a reference beside the typed rate and the resulting spread ("market 3.68 · venue 3.80 · +3.3%"); the stored value is the rate itself. *(source: DI-212)*
- **Pull rates now**: Purpose (required), currency pairs (default all the region trades), effective date (default next business day), and a dry run option that shows the rates without saving. *(source: contracts/spine/finance.yaml#ingestFxRates)*
- **Variance review outcome**: Accepted, Investigated, or Catalogue corrected, with a required note. *(source: contracts/spine/finance.yaml#/components/schemas/PriceVariance / contracts/spine/finance.yaml#reviewPriceVariance)*

#### Outputs: what the screen shows and produces

**Shown**

**Rates in force** (data table, from `listFxRates`): Not a queue: rates wait for nobody.

| Shows | Format | Notes |
|---|---|---|
| From currency | text | — |
| To currency | text | — |
| Rate | text | Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every … |
| Effective from | 1 Oct 2026, 14:30 | — |
| Provider reference | text | The provider's own identifier for this quote. What makes a rate reproducible — an auditor asking why a payment converted at 3.6725 gets an … |
| Fetched at | 1 Oct 2026, 14:30 | When the rate was pulled. Distinct from `effectiveFrom`, which is when it applies — a rate fetched at 06:00 for a business day starting at … |

**Waiting for a decision** (data table, from `listPriceVariances`): The queue: price variances pending review.

| Shows | Format | Notes |
|---|---|---|
| Quoted price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Server price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Variance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Catalogue bundle version | text | The bundle the terminal priced from. Turns "the price was wrong" into "the terminal was two bundles behind", which is actionable. |
| Is exception | yes / no (icon or chip) | Above the venue's configured variance threshold. |
| Review status | chip: Not required, Pending review, Reviewed | — |
| Review outcome | chip: Accepted, Investigated, Catalogue corrected | The `outcome` given to `reviewPriceVariance`. Null until reviewed. |

**The selected FX rate** (detail panel, from `listFxRates`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| From currency | text | — |
| To currency | text | — |
| Rate | text | Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every … |
| Purpose | chip: Tender, Inter entity, Reporting, Revaluation | A venue does not accept dollars at the rate it books an intercompany balance at. |
| Source | chip: Manual, Uae central bank, Ecb, Open exchange rates, Card scheme, Provider | Where the rate came from, and which provider specifically. `source: provider` said a feed set it and not which one — two tenants on … |
| Effective from | 1 Oct 2026, 14:30 | — |
| Effective to | 1 Oct 2026, 14:30 | A rate change is a new row. The old one is never edited — a transaction posted last Tuesday must still reconcile at last Tuesday's rate. |
| Set by principal | the name it points at, never the id | — |
| Provider reference | text | The provider's own identifier for this quote. What makes a rate reproducible — an auditor asking why a payment converted at 3.6725 gets an … |
| Fetched at | 1 Oct 2026, 14:30 | When the rate was pulled. Distinct from `effectiveFrom`, which is when it applies — a rate fetched at 06:00 for a business day starting at … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save FX rate (primary button) | `setFxRate` PUT `/fx-rates` | FxRate | FxRate | 400 No `note` was given. A manual rate says where the figure came from (audit R127 (4)).; 409 Effective window overlaps an existing bounded rate for the same pair and purpose, or does not start after the rate in force | opens modal first |
| Review price variance (secondary button) | `reviewPriceVariance` POST `/price-variances/{varianceId}/review` | inline | PriceVariance | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The variance is not awaiting review: its `reviewStatus` is `notRequired` (below the venue's threshold) or … | opens modal first |
| Ingest FX rates (secondary button) | `ingestFxRates` POST `/fx-rates/ingest` | inline | inline | 409 No provider is assigned to this purpose in this region (`setFxProvider`). | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Rates**: Per pair and purpose: rate in force, source in words (Manual, UAE Central Bank, ECB, Open Exchange Rates, Card scheme), effective from, fetched at, who set it and the note. Earlier rates listed beneath, never edited. *(source: contracts/spine/finance.yaml#/components/schemas/FxRateSource / contracts/spine/finance.yaml#/components/schemas/FxRate)*
- **Variances waiting**: Only exceptions above the venue threshold that are pending review: order, quoted against server price, difference, and the catalogue bundle the till priced from ("till was two bundles behind"). Oldest first. *(source: contracts/spine/finance.yaml#/components/schemas/PriceVariance)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Save rate**: Adds the rate from its effective time; the timeline shows the previous one closed at that moment. *(source: contracts/spine/finance.yaml#setFxRate)*
- **Pull rates now**: Writes new rows; refused with "Provider unreachable, no rates changed" rather than reusing old ones. *(source: contracts/spine/finance.yaml#ingestFxRates)*
- **Review variance**: Records the outcome; the row leaves the queue. *(source: contracts/spine/finance.yaml#reviewPriceVariance)*

**Data it reads**: `listFxRates` (onLoad, The rates in force); `listPriceVariances` (onLoad, List price variances)

**Where the user goes next**

- → `BO-074` Chart of Accounts: *Chart of Accounts*
- → `BO-075` Account Mapping: *Account Mapping*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rates variances list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rates variances untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on asAt, purpose and the rates variances are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listFxRates` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_APPROVE` for `setFxRate`, `reviewPriceVariance`, `ingestFxRates`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 No `note` was given. A manual rate says where the figure came from (audit R127 (4)).; 409 Effective window overlaps an existing bounded rate for the same pair and purpose, or does not start after the rate in force; 409 No provider is assigned to this purpose in this region (`setFxProvider`).; 409 The variance is not awaiting review: its `reviewStatus` is `notRequired` (below the venue's … |

#### Edge cases to draw

- **The person holds the venue role but rates are set per region**: Rates are read-only for them, with "Rates are set for the region by finance". *(source: contracts/spine/finance.yaml#setFxRate / R120)*
- **A three-decimal currency pair**: Rates always show their six decimals; amounts use the currency's three. *(source: contracts/spine/finance.yaml#/components/schemas/FxRateValue)*

#### Consistency with other screens

- Match `WEB-035`: The tender rate set here is what guests see as the approximate conversion.
- Match `POS-008`: Foreign tender is converted at the tender rate in force at the time of sale.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rates:
- 'USD → AED · Tender · 3.800000 · Manual · from 1 Oct 2026 00:00 · note: market 3.68, counter spread per finance
  policy'
- USD → AED · Reporting · 3.672500 · UAE Central Bank · fetched 06:00
- SAR → AED · Tender · 0.979300 · Open Exchange Rates · fetched 06:00
variance: ORD-8K21P · Day Pass Adult · quoted AED 279.00 · server AED 299.00 · −AED 20.00 · bundle 2026.09.30-2
  (current .10.01-1)
```

#### Permissions

- `listFxRates` → `LEDGER_VIEW` (read) · staff, guest
- `setFxRate` → `LEDGER_APPROVE` (operate) · staff
- `listPriceVariances` → `LEDGER_VIEW` (read) · staff
- `reviewPriceVariance` → `LEDGER_APPROVE` (operate) · staff
- `ingestFxRates` → `LEDGER_APPROVE` (operate) · staff, service

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listFxRates` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_APPROVE` for `setFxRate`, `reviewPriceVariance`, `ingestFxRates`.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 4.2.8 | The system should allow creation and management of currency exchange rates. The exchange rates can be updated manually or automatically based on a configured frequency. | Bundles and Promotions | CONTRACTED | `setFxRate` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- POS applies the same foreign-currency display/charge logic, records in base currency, and has a report of total foreign-currency collections by currency. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-213)*
- Back office supports both a manually set rate with margin (Qossai: ~90% of regional clients, e.g. 3.80 when market is 3.68) and a live third-party FX-rate feed (e.g. XE). *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-212)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'multi-currency')*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'multi-currency')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-077` · status **notStarted** · provenance generated
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0031 *Contention is leased, not locked — and where a lock is unavoidable it is named* (`docs/adr/0031-contention-and-locking.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-077?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save FX rate, Review price variance, Ingest FX rates.
- [ ] Every transition is wired: `BO-074`, `BO-075`.
- [ ] Every gated control is gated: `LEDGER_APPROVE`, `LEDGER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 1 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-089` Journal Entries

**Every posting, and the ones waiting for approval.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block C · task VM-BO-089 |
| Who uses it | venue staff holding `LEDGER_APPROVE`, `LEDGER_POST`, `LEDGER_VIEW` (2 operate, 1 read); in the flows as finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `approveJournalEntry` decides items that `listJournalEntries` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `entryId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/finance/journal-entries` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. **Every manual journal needs approval** (decided 2 October 2026, Chinmay; CHG-FIN-008; DI-265): a finance user prepares it, a finance manager or director approves it, and only then does it reach the ledger. There is no threshold below which it posts itself (the state model's "above the venue threshold" is wrong). **Posted entries are never edited, only reversed** (CHG-FIN-005): a posted entry offers Reverse, never Edit or Delete; a reversal a person asks for waits for approval like any manual journal. **The approver is never the preparer**: Approve is hidden on an entry the viewer prepared and refused by the server (`approver-is-preparer`).

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The journal: every posting, and the manual entries waiting for a finance manager. A finance user prepares a voucher, a different person approves it, and only then it reaches the ledger. Nothing posted is ever edited or deleted: a correction is a reversal. The one thing to get right: the approver can never be the preparer, and the screen must make that visible before anyone tries.

**Known correction pending (do not draw the wrong version)**

- **There is no way to edit a draft or send a rejected draft back for approval.** Why: The journal state model moves draft to pending only when the entry is created; after a rejection the draft can only be approved directly or abandoned. *(source: contracts/spine/finance.yaml#/components/schemas/JournalStatus / contracts/spine/finance.yaml#rejectJournal; Finance, Ledger & Tax · Reporting & Analytics)*
- **The state model says approval is needed only "above the venue threshold".** Why: The 12 August minutes and the operation say every manual voucher is approved by a manager before it posts. *(source: contracts/spine/finance.yaml#/components/schemas/JournalStatus / DI-265 / contracts/spine/finance.yaml#createJournalEntry; Finance, Ledger & Tax · Reporting & Analytics)*
- **Period, status and source filters are free text.** Why: Pick lists of periods and the two closed enumerations. *(source: screens/P08-venue-back-office.yaml#BO-089; Finance, Ledger & Tax · Reporting & Analytics)*

**Fixed on main** (the package already carries these; draw what it says): The whole journal list is titled "Waiting for a decision" and the empty state says "nothing is waiting… offers no create action", yet the … (CHG-FIN-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Fiscal period id | picker: choose a fiscal period (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?fiscalPeriodId=` to `listJournalEntries`. | `listJournalEntries` ?fiscalPeriodId |
| Status | radio group | optional | — | Draft · Pending approval · Posted · Reversed | — | Sends `?status=` to `listJournalEntries`. | `listJournalEntries` ?status |
| Source | select | optional | — | Manual · Order · Refund · Void · Shift · Recognition · Settlement · Variance · Reversal · Write off · Chargeback | — | Sends `?source=` to `listJournalEntries`. | `listJournalEntries` ?source |

**Form: Create journal entry** (modal, opened by *Create journal entry*; *Create journal entry* calls `createJournalEntry`, *Cancel* sends nothing)

**Collects what `createJournalEntry` sends before it is called.** Required: `id`, `fiscalPeriodId`, `description`, `lines`. Optional: `postingDate`, `reference`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createJournalEntry` body |
| Fiscal period `fiscalPeriodId` | picker: choose a fiscal period | required | — | — | shows names, sends the id | — | `createJournalEntry` body |
| Posting date `postingDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | A day in the region's time zone, local midnight to local midnight. | `createJournalEntry` body |
| Description `description` | text area | required | — | min length 3; max length 500 | — | — | `createJournalEntry` body |
| Reference `reference` | text field | optional | — | max length 128 | — | — | `createJournalEntry` body |
| Lines `lines` | repeatable rows | required | — | at least 2 | — | — | `createJournalEntry` body |
| Account `lines[].accountId` | picker: choose an account | required | — | — | shows names, sends the id | — | `createJournalEntry` body |
| Debit `lines[].debit` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createJournalEntry` body |
| Credit `lines[].credit` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createJournalEntry` body |
| Venue `lines[].venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createJournalEntry` body |
| Cost center `lines[].costCenterId` | picker: choose a cost center | optional | — | — | shows names, sends the id | — | `createJournalEntry` body |
| Description `lines[].description` | text area | optional | — | max length 500 | — | — | `createJournalEntry` body |

Errors to draw in the form: 400 Lines do not balance, or an account is not postable; 409 The fiscal period is not `open`. Postings stop once a close begins, so a `closing` period refuses them as a `closed` one does.

**Form: Approve journal entry** (modal, opened by *Approve journal entry*; *Approve journal entry* calls `approveJournalEntry`, *Cancel* sends nothing)

**Collects what `approveJournalEntry` sends before it is called.** Nothing in the body is required. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | optional | — | max length 500 | — | — | `approveJournalEntry` body |

Errors to draw in the form: 403 Approver is the poster, or lacks LEDGER_APPROVE; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The entry is not awaiting approval (it is `posted` or `reversed` already; only a `draft` or `pendingApproval` entry is approved), or its fiscal period has …

**Sent by *Reject journal*** (`rejectJournal`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `rejectJournal` body |

**Sent by *Reverse journal entry*** (`reverseJournalEntry`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `reverseJournalEntry` body |
| Fiscal period `fiscalPeriodId` | picker: choose a fiscal period | optional | — | — | shows names, sends the id | Period to post the reversal into. Defaults to the current open period. | `reverseJournalEntry` body |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Journal entry**: Fiscal period (open periods only), posting date, description (3–500 characters), reference, and at least two lines, each with account (postable, active), debit or credit, venue, cost centre and line description. A running "Debits AED x · Credits AED y · Difference" bar; saving is refused while unbalanced. *(source: contracts/spine/finance.yaml#/components/schemas/CreateJournalEntryRequest / contracts/spine/finance.yaml#createJournalEntry)*
- **Reject**: A required comment the preparer will read; the entry returns to draft. *(source: contracts/spine/finance.yaml#rejectJournal)*
- **Reverse**: A required reason and the period to post the reversal into (default the current open period). *(source: contracts/spine/finance.yaml#reverseJournalEntry)*

#### Outputs: what the screen shows and produces

**Shown**

**Journal entries** (data table, from `listJournalEntries`): Opens on `pendingApproval`; drafts, posted and reversed entries are a filter away.

| Shows | Format | Notes |
|---|---|---|
| Entry number | text | Server-assigned, in sequence per legal entity per fiscal year (decided 28 September, audit R191), for example `JE-2026-000123`. |
| Status | chip: Draft, Pending approval, Posted, Reversed | — |
| Description | text | — |
| Reference | text | — |
| Total debit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total credit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**The selected journal entry** (detail panel, from `getJournalEntry`)

| Shows | Format | Notes |
|---|---|---|
| Entry number | text | Server-assigned, in sequence per legal entity per fiscal year (decided 28 September, audit R191), for example `JE-2026-000123`. |
| Status | chip: Draft, Pending approval, Posted, Reversed | — |
| Source | chip: Manual, Order, Refund, Void, Shift, Recognition… | — |
| Description | text | — |
| Reference | text | — |
| Total debit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total credit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Posted at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create journal entry (primary button) | `createJournalEntry` POST `/journal-entries` | CreateJournalEntryRequest | JournalEntry | 400 Lines do not balance, or an account is not postable; 409 The fiscal period is not `open`. Postings stop once a close begins, so a `closing` period refuses them as a `closed` one does. | opens modal first |
| Approve journal entry (secondary button) | `approveJournalEntry` POST `/journal-entries/{entryId}/approve` | inline | JournalEntry | 403 Approver is the poster, or lacks LEDGER_APPROVE; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The entry is not awaiting approval (it is `posted` or … | step-up: mfa (Posts to the ledger. The entry is the record; there is no undo that is not another entry.); opens modal first |
| Reject journal (destructive button) | `rejectJournal` POST `/journal-entries/{entryId}/reject` | inline | JournalEntry | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The entry is not `pendingApproval`. | — |
| Reverse journal entry (destructive button) | `reverseJournalEntry` POST `/journal-entries/{entryId}/reverse` | inline | JournalEntry | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already reversed, not yet posted, or the target period is not `open`. Three causes, three types. | — |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Two views**: "Waiting for approval" (pending entries, oldest first; empty means all done) and "All entries" (filter by period, status and source: manual, order, refund, void, shift, recognition, settlement, variance, reversal, write-off, chargeback). *(source: contracts/spine/finance.yaml#/components/schemas/JournalSource / contracts/spine/finance.yaml#/components/schemas/JournalStatus)*
- **Entry detail**: Number, status, source, preparer, approver, lines with account code and name, totals; for a reversal, a link to the original and back; a rejected draft shows the rejection comment. *(source: contracts/spine/finance.yaml#/components/schemas/JournalEntry / contracts/spine/finance.yaml#/components/schemas/JournalStatus)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Approve and post**: Posts to the ledger; needs the approver's second factor. *(source: contracts/spine/finance.yaml#approveJournalEntry / R135)*
- **Reject**: Back to draft with the comment. *(source: contracts/spine/finance.yaml#rejectJournal)*
- **Reverse**: Creates the mirror entry referencing the original; the original stays as posted and is marked Reversed. The confirmation states the accounts and amounts that will move. *(source: contracts/spine/finance.yaml#reverseJournalEntry)*

**Data it reads**: `listJournalEntries` (onLoad, List journal entries)

**Where the user goes next**

- → `BO-090` Period Close: *Begins the close*
- → `BO-074` Chart of Accounts: *Chart of Accounts*; carries `accountId`
- → `BO-075` Account Mapping: *Account Mapping*

**What opens over it**

- confirmDialog *Reject journal*: **Names what `rejectJournal` changes and what it leaves alone**, in the consequence rather than the verb. A journal entries this affects should be identified in the dialog, not just counted. **Collects what `rejectJournal` sends before it is called.** Required: `reason`.
- confirmDialog *Reverse journal entry*: **Names what `reverseJournalEntry` changes and what it leaves alone**, in the consequence rather than the verb. A journal entries this affects should be identified in the dialog, not just counted. **Collects what `reverseJournalEntry` sends before it is called.** Required: `reason`. Optional …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The journal entries list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the journal entries untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on fiscalPeriodId, status, source and the journal entries are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listJournalEntries` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_APPROVE` for `approveJournalEntry`, `rejectJournal`, `reverseJournalEntry`; `LEDGER_POST` for `createJournalEntry`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Lines do not balance, or an account is not postable; 409 Already reversed, not yet posted, or the target period is not `open`. Three causes, three types.; 409 The entry is not `pendingApproval`.; 409 The entry is not awaiting approval (it is `posted` or `reversed` already; only a `draft` or `pendingApproval` entry is approved), or its fiscal period has … |

#### Edge cases to draw

- **The preparer opens their own pending entry**: Approve is not offered; "Waiting for another approver" with the routing. *(source: contracts/spine/finance.yaml#approveJournalEntry)*
- **The period stopped taking postings after the entry was prepared**: Approve is refused with "Period is closing; choose an open period". *(source: contracts/spine/finance.yaml#approveJournalEntry)*
- **The approver is on leave at month end**: Delegation routes it to a delegate for a limited time. *(source: F13 step 3)*

#### Consistency with other screens

- Match `BO-090`: "No unapproved journals" is a close check linking here.
- Match `BO-074`: Account pickers show code, name and type.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
pending:
- 'JV-2026-000418 · Accrual: September cleaning contract · Dr 6200 Facilities AED 42,000.00 · Cr 2100 Accruals AED
  42,000.00 · prepared by Rahul Menon'
posted:
- 'JE-2026-091233 · Source: shift · Till 3 close · Dr 6900 Cash over/short AED 20.00 · Cr 1100 Cash on hand AED
  20.00'
```

#### Permissions

- `listJournalEntries` → `LEDGER_VIEW` (read) · staff
- `getJournalEntry` → `LEDGER_VIEW` (read) · staff
- `createJournalEntry` → `LEDGER_POST` (operate) · staff
- `approveJournalEntry` → `LEDGER_APPROVE` (operate) · staff · step-up mfa
- `rejectJournal` → `LEDGER_APPROVE` (operate) · staff
- `reverseJournalEntry` → `LEDGER_APPROVE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listJournalEntries` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_APPROVE` for `approveJournalEntry`, `rejectJournal`, `reverseJournalEntry`; `LEDGER_POST` for `createJournalEntry`.

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.12.77 | Complete audit trail of rule changes. | F&B & Guest Management | CONTRACTED | `listJournalEntries` |
| 5.12.78 | User activity logging. | F&B & Guest Management | CONTRACTED | `listJournalEntries` |
| 5.7.16 | The system should be able to validate that all transactions are balanced. Total debits must equal total credits per transaction. | F&B & Guest Management | CONTRACTED | `createJournalEntry` |
| 5.7.20 | The system should support real-time or near real-time processing of journal entries and revenue allocation as configured in the system. | F&B & Guest Management | CONTRACTED | `createJournalEntry` |
| 5.11.1 | Provides accounting-grade financial recording of all platform transactions. | F&B & Guest Management | CONTRACTED | `createJournalEntry` |
| 5.11.2 | Double Entry Accounting Each financial transaction shall create balanced debit and credit entries. | F&B & Guest Management | CONTRACTED | `createJournalEntry` |
| 5.11.4 | Journal Management System shall support accounting journals and transaction classifications. | F&B & Guest Management | CONTRACTED | `createJournalEntry` |
| 5.12.81 | General Ledger posting integration. | F&B & Guest Management | CONTRACTED | `createJournalEntry` |
| 5.12.82 | Real-time financial posting APIs. | F&B & Guest Management | CONTRACTED | `createJournalEntry` |
| 5.12.83 | Journal entry automation. | F&B & Guest Management | CONTRACTED | `createJournalEntry` |
| 5.12.87 | System shall support manual journal entry creation. | F&B & Guest Management | CONTRACTED | `createJournalEntry` |
| 5.12.91 | System shall allow users to specify transaction date during journal creation. | F&B & Guest Management | CONTRACTED | `createJournalEntry` |
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Journal entry list of posted debits/credits, with manual journal entry that needs approval: a finance user posts a voucher, a finance manager/director approves, only then it hits the ledger. *(client request · MoM 12 Aug 2026, 15. Financial Transactions Ledger and Journal Entries · DI-265)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-089` · status **notStarted** · provenance generated
- Flow F13 *Month end closes*, step 3: Posts the remaining journals → Accruals, adjustments, corrections
- Flow F13 branch at step 3 (recoverable): when A journal needs approval and the approver is away, `approvals` delegation. **This is why delegation is time-bounded** — a month end waiting on someone on leave is the case it exists for.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-089?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create journal entry, Approve journal entry, Reject journal, Reverse journal entry.
- [ ] Every transition is wired: `BO-090`, `BO-074`, `BO-075`.
- [ ] Every gated control is gated: `LEDGER_APPROVE`, `LEDGER_POST`, `LEDGER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 3 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-090` Period Close

**Close a fiscal period, and see what is stopping it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block C · task VM-BO-090 |
| Who uses it | venue staff holding `LEDGER_APPROVE`, `LEDGER_VIEW` (1 operate, 1 read); in the flows as finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listFiscalPeriods` reads the population and `getTrialBalance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `periodId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/finance/period-close` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** Close a fiscal period and see exactly what is stopping it. Beginning the close stops postings to the period (sales continue, posting to the next period); the close runs seven checks and, when they pass, goes to a finance approver; reopening is rare and approved. The one thing to get right: the checklist is the screen; every failing check names how many items block it and links to where they are fixed.

**Known correction pending (do not draw the wrong version)**

- **Legal entity and status filters are free text.** Why: An entity switcher and the three statuses. *(source: screens/P08-venue-back-office.yaml#BO-090; Finance, Ledger & Tax · Reporting & Analytics)*
- **The close checks are not drawn; the screen shows a period list and a trial balance.** Why: The close returns seven named checks with blocking counts; that checklist is what "see what is stopping it" means. *(source: contracts/spine/finance.yaml#/components/schemas/PeriodCloseResult / screens/P08-venue-back-office.yaml#BO-090; Finance, Ledger & Tax · Reporting & Analytics)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Legal entity id | picker: choose a legal entity (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?legalEntityId=` to `listFiscalPeriods`. | `listFiscalPeriods` ?legalEntityId |
| Status | segmented control | optional | — | Open · Closing · Closed | — | Sends `?status=` to `listFiscalPeriods`. | `listFiscalPeriods` ?status |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Fiscal period | picker: choose a fiscal period | — | — | `getTrialBalance` ?fiscalPeriodId |
| Legal entity | picker: choose a legal entity | — | — | `getTrialBalance` ?legalEntityId |
| Legal entity | picker: choose a legal entity | — | — | `getVatReturn` ?legalEntityId |
| Period from | date picker | — | — | `getVatReturn` ?periodFrom |
| Period to | date picker | — | — | `getVatReturn` ?periodTo |
| Format | segmented control | Json | Json · Csv · Xlsx | `getVatReturn` ?format |

**Form: Reopen period** (modal, opened by *Reopen period*; *Reopen period* calls `reopenPeriod`, *Cancel* sends nothing)

**Collects what `reopenPeriod` sends before it is called.** Required: `reason` only — the approver is not named here. **The request answers 202 with an `approvalRequestId`** and the period shows *reopen pending finance approval* until a finance approver acts (decided 28 September, audit R144). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `reopenPeriod` body |

Errors to draw in the form: 403 The caller lacks `LEDGER_APPROVE` there.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The period is not `closed`.

**Sent by *Close fiscal period*** (`closeFiscalPeriod`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Dry run `dryRun` | toggle | optional | off | — | — | Run the checks and report without locking. | `closeFiscalPeriod` body |

**Sent by *Abandon period close*** (`abandonPeriodClose`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | — | — | — | `abandonPeriodClose` body |

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Legal entity and period**: Entity switcher, then the periods by year with status Open, Closing, Closed. Periods follow the entity's fiscal year (January or April start). *(source: contracts/spine/finance.yaml#/components/schemas/FiscalPeriod / DI-263)*
- **Abandon or reopen reason**: Required text; kept in the period's history. *(source: contracts/spine/finance.yaml#/components/schemas/FiscalPeriodEvent)*
- **VAT return range**: Its own date range (the tax period), which need not be the fiscal period. *(source: contracts/spine/finance.yaml#getVatReturn)*

#### Outputs: what the screen shows and produces

**Shown**

**Every fiscal period** (data table, from `listFiscalPeriods`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Legal entity | the name it points at, never the id | — |
| Name | text | — |
| Start date | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| End date | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Status | chip: Open, Closing, Closed | — |
| Closed by principal | the name it points at, never the id | — |
| Closed at | 1 Oct 2026, 14:30 | — |

**The selected fiscal period** (detail panel, from `listFiscalPeriods`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Legal entity | the name it points at, never the id | — |
| Name | text | — |
| Start date | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| End date | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Status | chip: Open, Closing, Closed | — |
| Closed by principal | the name it points at, never the id | — |
| Closed at | 1 Oct 2026, 14:30 | — |
| Events | list or chips (count when long) | Every step of the period's close, oldest first: begin, abandon, close and reopen, each with who, when and (for abandon and reopen) why. |

**The trial balance** (detail panel, from `getTrialBalance`)

| Shows | Format | Notes |
|---|---|---|
| Fiscal period | the name it points at, never the id | — |
| Is balanced | yes / no (icon or chip) | False indicates a defect, not a business condition. Double-entry cannot be unbalanced by legitimate activity. |
| Total debit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total credit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Accounts | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Begin period close (primary button) | `beginPeriodClose` POST `/fiscal-periods/{periodId}/begin-close` | — | FiscalPeriod | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The period is not `open`. | — |
| Close fiscal period (destructive button) | `closeFiscalPeriod` POST `/fiscal-periods/{periodId}/close` | inline | PeriodCloseResult | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The period is already `closed`, or one or more of the close checks failed. The checks are exactly the values of … | — |
| Abandon period close (destructive button) | `abandonPeriodClose` POST `/fiscal-periods/{periodId}/abandon-close` | inline | FiscalPeriod | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The period is not `closing`. | — |
| Reopen period (secondary button) | `reopenPeriod` POST `/fiscal-periods/{periodId}/reopen` | inline | FiscalPeriod | 403 The caller lacks `LEDGER_APPROVE` there.; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The period is not `closed`. | opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Close checklist**: Trial balance balances; no unapproved journals; no open shifts; settlements reconciled; recognition run complete; prior period closed; variance exceptions reviewed. Each with pass or fail, the blocking count and a link (BO-089, shifts, BO-043, BO-076, BO-077). Run as a dry run any time. *(source: contracts/spine/finance.yaml#/components/schemas/PeriodCloseResult / F13 step 1)*
- **Trial balance**: Accounts with debit, credit and balance; total debits and credits; "Balanced" or "Not balanced: this is a defect" in words. *(source: contracts/spine/finance.yaml#/components/schemas/TrialBalance)*
- **VAT return**: The return boxes as filed (standard-rated supplies by emirate, zero-rated, exempt, reverse charge, imports, tourist refunds, recoverable input tax, net payable), each traceable to its tax codes and postings; download CSV or Excel for the adviser. *(source: contracts/spine/finance.yaml#getVatReturn)*
- **History**: Every begin, abandon, close and reopen with who, when, why and the approver. *(source: contracts/spine/finance.yaml#/components/schemas/FiscalPeriodEvent)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Begin close**: Status Closing; postings to the period stop; new sales post to the next period with a reference. *(source: contracts/spine/finance.yaml#beginPeriodClose / F13 step 4)*
- **Close**: Runs the checks; if they pass, raises an approval to another finance approver and shows "Close pending finance approval"; locks when approved. Failing checks are listed instead. *(source: contracts/spine/finance.yaml#closeFiscalPeriod / R144)*
- **Abandon close**: Back to Open with the reason. *(source: contracts/spine/finance.yaml#abandonPeriodClose)*
- **Request reopen**: "Reopen pending finance approval"; when approved the period goes back to Closing. *(source: contracts/spine/finance.yaml#reopenPeriod / R144)*

**Data it reads**: `listFiscalPeriods` (onLoad, List fiscal periods); `getTrialBalance` (onLoad, Trial balance for a period); `getVatReturn` (onLoad, VAT return (FTA boxes) for a period)

**Where the user goes next**

- → `BO-040` Variance Approval: *Clears outstanding shift variances*
- → `BO-074` Chart of Accounts: *Chart of Accounts*; carries `accountId`
- → `BO-075` Account Mapping: *Account Mapping*

**What opens over it**

- confirmDialog *Close fiscal period*: **Names what `closeFiscalPeriod` changes and what it leaves alone**, in the consequence rather than the verb. A period close this affects should be identified in the dialog, not just counted. **Collects what `closeFiscalPeriod` sends before it is called.** Nothing in the body is required. Optional …
- confirmDialog *Abandon period close*: **Names what `abandonPeriodClose` changes and what it leaves alone**, in the consequence rather than the verb. A period close this affects should be identified in the dialog, not just counted. **Collects what `abandonPeriodClose` sends before it is called.** Required: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The period close list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the period close untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No period close yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on legalEntityId, status and the period close are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listFiscalPeriods` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_APPROVE` for `beginPeriodClose`, `closeFiscalPeriod`, `abandonPeriodClose`, `reopenPeriod`. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The period is already `closed`, or one or more of the close checks failed. The checks are exactly the values of `PeriodCloseResult.checks[].check` … (PeriodCloseProblem); 409 The period is not `closed`.; 409 The period is not `closing`.; 409 The period is not `open`. |

#### Edge cases to draw

- **The trial balance does not balance**: The close stops; recommend abandoning and investigating rather than closing over it. *(source: F13 step 5)*
- **A correction is needed after closing**: Recommend a reversal in the current period; reopening invalidates reports already issued. *(source: F13 step 6)*
- **FX revaluation of cross-currency balances**: Not available yet; show it as a pending step, not a passed check. *(source: contracts/spine/finance.yaml#closeFiscalPeriod)*

#### Consistency with other screens

- Match `BO-089`: Same wording for unapproved journals.
- Match `BO-043`: Same settlement exception counts.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
period: September 2026 · Aquaventure Leisure LLC · Closing since 1 Oct 09:12 by Layla Haddad
checks:
- Trial balance balances · passed · Dr AED 18,442,910.25 = Cr AED 18,442,910.25
- No unapproved journals · failed · 2 waiting
- No open shifts · failed · Till 7 Surf Café
- Settlements reconciled · passed
- Recognition run complete · passed
vatReturn: Jul–Sep 2026 · Standard-rated supplies Dubai AED 9,812,400.00 · VAT AED 490,620.00 · net payable AED
  431,905.40
```

#### Permissions

- `listFiscalPeriods` → `LEDGER_VIEW` (read) · staff
- `beginPeriodClose` → `LEDGER_APPROVE` (operate) · staff
- `closeFiscalPeriod` → `LEDGER_APPROVE` (operate) · staff
- `abandonPeriodClose` → `LEDGER_APPROVE` (operate) · staff
- `reopenPeriod` → `LEDGER_APPROVE` (operate) · staff
- `getTrialBalance` → `LEDGER_VIEW` (read) · staff
- `getVatReturn` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listFiscalPeriods` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `LEDGER_APPROVE` for `beginPeriodClose`, `closeFiscalPeriod`, `abandonPeriodClose`, `reopenPeriod`.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.89 | The system shall support fiscal year management, fiscal periods, month-end and year-end closing. Authorized users shall be able to open, close, lock, unlock, and re-open accounting periods with … | F&B & Guest Management | CONTRACTED | `closeFiscalPeriod` |
| 5.7.63 | Revenue recognition audit reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.64 | Revenue recognition reconciliation reports. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.71 | General Ledger reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.72 | Trial Balance reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.75 | Revenue reporting by account. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.76 | Revenue reporting by site. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.77 | Deferred revenue reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.78 | Account activity reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 5.7.79 | Account balance reporting. | F&B & Guest Management | CONTRACTED | `getTrialBalance` |
| 6.1.23 | The system should be able to tax reports in approved government formats for submittal. | Retail POS | CONTRACTED | `getVatReturn` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Financial year/period setup varies by country (UAE Jan–Dec, India Apr–Mar); closing a period locks further postings. An ERP integration centre manages external connections. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-263)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-090` · status **notStarted** · provenance generated
- Flow F13 *Month end closes*, step 1: Opens the period and sees what is blocking → Unposted journals, open shifts, unreconciled settlements — each named
- Flow F13 *Month end closes*, step 4: Begins the close → The period stops accepting postings. **Sales continue** — the period is a ledger boundary, not a trading one
- Flow F13 *Month end closes*, step 5: Reviews the trial balance → It balances, or the close does not proceed
- Flow F13 *Month end closes*, step 6: Closes → Locked. Later corrections post to the next period with a reference
- Flow F13 branch at step 1 (requiresStaff): when An open shift in the period, **The close blocks.** A shift with an uncounted drawer is a cash figure nobody has confirmed, and closing over it books a number that will change.
- Flow F13 branch at step 1 (requiresStaff): when A settlement exception is unresolved, Blocks. The gateway says one figure and the ledger says another, and closing picks one arbitrarily.
- Flow F13 branch at step 4 (recoverable): when A sale arrives after the period began closing, Posts to the next period automatically with a reference to the date. **It is not rejected** — a guest buying a ticket does not care that finance is closing.
- Flow F13 branch at step 5 (abandonsFlow): when The trial balance does not balance, **Stops.** The close is abandoned, the period reopens for posting, and the difference is investigated. Closing an unbalanced period moves the problem rather than solving it.
- Flow F13 branch at step 6 (requiresStaff): when A correction is needed after closing, `reopenPeriod`, which requires approval and is recorded. **Or a reversal in the current period**, which is usually right — reopening a closed period invalidates every report already issued from it.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-090?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Begin period close, Close fiscal period, Abandon period close, Reopen period.
- [ ] Every transition is wired: `BO-040`, `BO-074`, `BO-075`.
- [ ] Every gated control is gated: `LEDGER_APPROVE`, `LEDGER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-101` Orders & Money

**Everything in orders & money, and what in it needs attention.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block A · ticket #28283 (VM-BO-101) |
| Who uses it | venue staff holding `ORDER_VIEW`, `SETTLEMENT_VIEW` (2 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOrders` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/orders-money` |

**What the spec says about it.** Section landing. **28 screens reach the entry point through here** — before 20 August they reached it through nothing. **Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.

**Known gaps.** Venue settings are not part of orders and money (design-note correction platform-foundation BO-101, CHG-SBO-015).

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A venue manager's overview of orders and settlements and what needs attention (refunds pending, unmatched settlement lines). It is a section hub, not an editor.

**Fixed on main** (the package already carries these; draw what it says): getVenueSettings is declared on an orders overview. (CHG-SBO-015); Tables show every schema field, plumbing included: 'Every order' drop id; 'Every settlement' drop id. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listOrders`. | `listOrders` ?venueId |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listOrders`. | `listOrders` ?principalId |
| Shift id | picker: choose a shift (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?shiftId=` to `listOrders`. | `listOrders` ?shiftId |
| Status | select | optional | — | Pending · Held · Paid · Partially paid · Completed · Voided · Refunded · Partially refunded · Failed; It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed. | — | Sends `?status=` to `listOrders`. | `listOrders` ?status |
| Created from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdFrom=` to `listOrders`. | `listOrders` ?createdFrom |
| Created to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?createdTo=` to `listOrders`. | `listOrders` ?createdTo |
| Search orders & money | search field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listOrders` ?workstationId |
| Subject | picker: choose a subject | — | — | `listOrders` ?subjectId |
| Tender | select | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | `listOrders` ?tender |
| Provider name | text field | — | — | `listSettlements` ?providerName |
| Status | select | — | Ingesting · Parsing · Matching · Matched · Has exceptions · Resolved · Failed | `listSettlements` ?status |

#### Outputs: what the screen shows and produces

**Shown**

**Every order** (data table, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Every settlement** (data table, from `listSettlements`)

| Shows | Format | Notes |
|---|---|---|
| Currency code | text | A settlement has no account, so nothing else denominates it. A posting takes its currency from `ledger.account.currency` and a payment from … |
| Provider name | text | — |
| File reference | the name it points at, never the id | The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. Kept on the row because parsing is asynchronous: the job … |
| Line count | 1,234 | — |
| Matched count | 1,234 | — |
| Exception count | 1,234 | — |

**Card list** (card list): 28 screens, each with what needs attention.

**The selected order** (detail panel, from `listOrders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |
| Principal | the name it points at, never the id | The cashier who raised it — what the held-orders list shows. |
| Hold label | text | As `Order.holdLabel`. |
| Held until | 1 Oct 2026, 14:30 | As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse. |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (grossAmount, refundedAmount)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listOrders` (onLoad, Orders taken in this venue); `listSettlements` (onLoad, Money settled and what is outstanding)

**Where the user goes next**

- → `BO-008` Product Detail & Variants: *Product Detail & Variants*
- → `BO-022` Order Detail: *Order Detail*
- → `BO-023` Refunds & Exchanges: *Refunds & Exchanges*
- → `BO-024` Payment Exceptions: *Payment Exceptions*
- → `BO-025` Chargebacks & Disputes: *Chargebacks & Disputes*; carries `settlementId`
- → `BO-026` Group Bookings: *Group Bookings*
- → `BO-027` Reissue & Media Replacement: *Reissue & Media Replacement*
- → `BO-029` Report Builder: *Report Builder*
- → `BO-039` Shift Directory: *Shift Directory*
- → `BO-040` Variance Approval: *Variance Approval*
- → `BO-041` Cash Movements: *Cash Movements*
- → `BO-042` Banking & Safe: *Banking & Safe*
- → `BO-043` Daily Reconciliation: *Daily Reconciliation*; carries `settlementId`
- → `BO-047` Order Corrections & Exceptions: *Order Corrections & Exceptions*
- → `BO-048` Retail Products: *Retail Products*
- → `BO-059` Sales Reports: *Sales Reports*
- → `BO-061` Scheduled Reports: *Scheduled Reports*
- → `BO-062` Venue Profile: *Venue Profile*
- → `BO-065` Venue Configuration: *Venue Configuration*
- → `BO-074` Chart of Accounts: *Chart of Accounts*
- → `BO-075` Account Mapping: *Account Mapping*
- → `BO-077` FX Rates & Variances: *FX Rates & Variances*
- → `BO-089` Journal Entries: *Journal Entries*
- → `BO-090` Period Close: *Period Close*
- → `BO-028` Refund Approval Queue: *Refund Approval Queue*
- → `BO-1094` Funding Method Configuration: *Opens Funding Method Configuration*
- → `BO-1111` Credit Expiry, Extension & Forfeiture Operations: *Opens Credit Expiry, Extension & Forfeiture Operations*
- → `BO-1146` Refund-to-Wallet Policy Configuration: *Opens Refund-to-Wallet Policy Configuration*; carries `venueId`
- → `BO-1162` Security Governance, Audit & Rule Publication: *Opens Security Governance, Audit & Rule Publication*
- → `BO-1179` Integration Monitoring & Exception Workbench: *Opens Integration Monitoring & Exception Workbench*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list, with counts. |
| Error (`?state=error`) | Could not load. Venue Home is still reachable. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing configured in orders & money yet.** The action is the first thing to set up, not a blank list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter. |
| Permission denied (`?state=emptyNoAccess`) | You do not have permission for orders & money. **Said plainly** — an empty section reads as broken. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every order:
- status: active
  grossAmount: AED 1,250.00
  refundedAmount: AED 1,250.00
  lineCount: 12
- status: pending
  grossAmount: AED 48,000.00
  refundedAmount: AED 48,000.00
  lineCount: 3
- status: suspended
  grossAmount: OMR 48.500
  refundedAmount: OMR 48.500
  lineCount: 0
```

#### Permissions

- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `listSettlements` → `SETTLEMENT_VIEW` (read) · staff, partner

**A refused user sees:** You do not have permission for orders & money. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-101` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-101?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-008`, `BO-022`, `BO-023`, `BO-024`, `BO-025`, `BO-026`, `BO-027`, `BO-029`, `BO-039`, `BO-040`, `BO-041`, `BO-042`, `BO-043`, `BO-047`, `BO-048`, `BO-059`, `BO-061`, `BO-062`, `BO-065`, `BO-074`, `BO-075`, `BO-077`, `BO-089`, `BO-090`, `BO-028`, `BO-1094`, `BO-1111`, `BO-1146`, `BO-1162`, `BO-1179`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `SETTLEMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"abandonPeriodClose": {"method":"POST","path":"/fiscal-periods/{periodId}/abandon-close","contract":"finance","summary":"Abandon a close in progress","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FiscalPeriod"},
"approveJournalEntry": {"method":"POST","path":"/journal-entries/{entryId}/approve","contract":"finance","summary":"Approve a journal entry and post it","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"JournalEntry"},
"beginPeriodClose": {"method":"POST","path":"/fiscal-periods/{periodId}/begin-close","contract":"finance","summary":"Begin closing a period","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"FiscalPeriod"},
"closeFiscalPeriod": {"method":"POST","path":"/fiscal-periods/{periodId}/close","contract":"finance","summary":"Close a period and lock postings","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PeriodCloseResult"},
"createJournalEntry": {"method":"POST","path":"/journal-entries","contract":"finance","summary":"Post a manual journal voucher","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateJournalEntryRequest","responds":"JournalEntry"},
"createRecognitionSchedule": {"method":"POST","path":"/recognition-schedules","contract":"finance","summary":"Define how a product class recognises revenue","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecognitionSchedule","responds":"RecognitionSchedule"},
"createTaxCode": {"method":"POST","path":"/tax-codes","contract":"finance","summary":"Create a tax code","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateTaxCodeRequest","responds":"TaxCode"},
"createTaxExemption": {"method":"POST","path":"/tax-exemptions","contract":"finance","summary":"Grant a tax exemption","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TaxExemption","responds":"TaxExemption"},
"getDeferredRevenue": {"method":"GET","path":"/deferred-revenue","contract":"finance","summary":"Deferred revenue balance and ageing","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"asAt","in":"query","required":null},{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"DeferredRevenueReport"},
"getJournalEntry": {"method":"GET","path":"/journal-entries/{entryId}","contract":"finance","summary":"Read a journal entry","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"JournalEntry"},
"getTrialBalance": {"method":"GET","path":"/ledger/trial-balance","contract":"finance","summary":"Trial balance for a period","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"fiscalPeriodId","in":"query","required":true},{"name":"legalEntityId","in":"query","required":null}],"requestBody":null,"responds":"TrialBalance"},
"getVatReturn": {"method":"GET","path":"/tax/vat-returns","contract":"finance","summary":"A legal entity's VAT return for a tax period, in the FTA's boxes","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":true},{"name":"periodFrom","in":"query","required":true},{"name":"periodTo","in":"query","required":true},{"name":"format","in":"query","required":null}],"requestBody":null,"responds":"FinVatReturn"},
"ingestFxRates": {"method":"POST","path":"/fx-rates/ingest","contract":"finance","summary":"Pull rates from the configured provider","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listAccountMappings": {"method":"GET","path":"/account-mappings","contract":"finance","summary":"Which account each transaction type posts to","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFiscalPeriods": {"method":"GET","path":"/fiscal-periods","contract":"finance","summary":"List fiscal periods","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFxRates": {"method":"GET","path":"/fx-rates","contract":"finance","summary":"The rates in force","permission":"LEDGER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"asAt","in":"query","required":null},{"name":"purpose","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"chargeable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listJournalEntries": {"method":"GET","path":"/journal-entries","contract":"finance","summary":"List journal entries","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"fiscalPeriodId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"source","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrders": {"method":"GET","path":"/orders","contract":"orders","summary":"List orders","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"shiftId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"createdFrom","in":"query","required":null},{"name":"createdTo","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"tender","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceVariances": {"method":"GET","path":"/price-variances","contract":"finance","summary":"List price variances","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"exceptionsOnly","in":"query","required":null},{"name":"reviewStatus","in":"query","required":null},{"name":"occurredFrom","in":"query","required":null},{"name":"occurredTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRecognitionSchedules": {"method":"GET","path":"/recognition-schedules","contract":"finance","summary":"List revenue recognition schedules","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSettlements": {"method":"GET","path":"/settlements","contract":"finance","summary":"List settlement batches","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"providerName","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxCodes": {"method":"GET","path":"/tax-codes","contract":"finance","summary":"List tax codes","permission":"LEDGER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"countryCode","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxExemptions": {"method":"GET","path":"/tax-exemptions","contract":"finance","summary":"List tax exemptions","permission":"LEDGER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"rejectJournal": {"method":"POST","path":"/journal-entries/{entryId}/reject","contract":"finance","summary":"Reject a journal awaiting approval","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"JournalEntry"},
"reopenPeriod": {"method":"POST","path":"/fiscal-periods/{periodId}/reopen","contract":"finance","summary":"Reopen a closed period","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"reverseJournalEntry": {"method":"POST","path":"/journal-entries/{entryId}/reverse","contract":"finance","summary":"Reverse a posted entry","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"JournalEntry"},
"reviewPriceVariance": {"method":"POST","path":"/price-variances/{varianceId}/review","contract":"finance","summary":"Record a review decision on an exception variance","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PriceVariance"},
"runRecognition": {"method":"POST","path":"/recognition/run","contract":"finance","summary":"Recognise earned revenue for a period","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RecognitionRunResult"},
"setAccountMappings": {"method":"PUT","path":"/account-mappings","contract":"finance","summary":"Set posting mappings","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccountMapping"},
"setFxRate": {"method":"PUT","path":"/fx-rates","contract":"finance","summary":"Set a rate","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FxRate","responds":"FxRate"},
"updateTaxCode": {"method":"PATCH","path":"/tax-codes/{taxCodeId}","contract":"finance","summary":"Amend a tax code","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TaxCode"},
"validateRecognitionSchedules": {"method":"POST","path":"/recognition-schedules/validate","contract":"finance","summary":"Find product kinds claimed by more than one schedule","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"verifyTaxExemption": {"method":"POST","path":"/tax-exemptions/{exemptionId}/verify","contract":"finance","summary":"Record that a tax exemption's evidence was checked","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TaxExemption"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccountMapping": {"x-ticvai-persistence":"ledger.account_mapping","type":"object","required":["eventType","debitAccountId","creditAccountId"],"properties":{"eventType":{"$ref":"#/components/schemas/PostingEventType"},"debitAccountId":{"type":"string","format":"uuid"},"creditAccountId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Null applies the mapping to every venue in the region."}}},
"AccountType": {"type":"string","enum":["asset","liability","equity","revenue","expense"]},
"CreateJournalEntryRequest": {"type":"object","required":["id","fiscalPeriodId","description","lines"],"properties":{"id":{"type":"string","format":"uuid"},"fiscalPeriodId":{"type":"string","format":"uuid"},"postingDate":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"description":{"type":"string","minLength":3,"maxLength":500},"reference":{"type":"string","maxLength":128},"lines":{"type":"array","minItems":2,"items":{"$ref":"#/components/schemas/JournalLine"}}}},
"CreateTaxCodeRequest": {"type":"object","required":["code","name","countryCode","rate","effectiveFrom","accountId"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$"},"rate":{"type":"number","minimum":0,"maximum":100},"compoundOnTaxCodeId":{"type":"string","format":"uuid"},"isInclusive":{"type":"boolean","default":false},"accountId":{"type":"string","format":"uuid"},"effectiveFrom":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."}}},
"DeferredRevenueReport": {"x-ticvai-persistence":"none — computed","type":"object","required":["asAt","totals","buckets"],"properties":{"asAt":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"totals":{"type":"array","description":"**One `Money` per currency in scope**, never a sum across currencies. One entry when every venue in scope trades in the same currency.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/Money"}},"total":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"The single total when everything in scope is in one currency; null otherwise. Read `totals`."},"buckets":{"type":"array","description":"One ageing band in one currency per entry. A band spanning two currencies is two entries.","items":{"type":"object","required":["label","amount","itemCount"],"properties":{"label":{"type":"string","description":"Ageing band by expected recognition date."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"itemCount":{"type":"integer"},"method":{"$ref":"#/components/schemas/RecognitionMethod"}}}}}},
"FinVatReturn": {"x-ticvai-persistence":"none — computed from ledger postings on the reporting replica","type":"object","description":"6.1.23. The FTA VAT 201 boxes for one legal entity and tax period.","required":["legalEntityId","periodFrom","periodTo","boxes","netTaxPayable"],"properties":{"legalEntityId":{"type":"string","format":"uuid"},"taxRegistrationNumber":{"type":"string"},"periodFrom":{"type":"string","format":"date"},"periodTo":{"type":"string","format":"date"},"boxes":{"type":"array","items":{"type":"object","required":["box","amount","taxAmount"],"properties":{"box":{"type":"string","description":"The form's box, e.g. `1a` (standard-rated supplies, Abu Dhabi) ... `1g`, `2` (tourist refunds), `3` (reverse charge), `4` (zero-rated), `5` (exempt), `6` and `7` (imports), `9` (standard-rated expenses), `10` (reverse charge inputs)."},"label":{"type":"string"},"emirate":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"adjustmentAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"postingCount":{"type":"integer"}}}},"totalOutputTax":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRecoverableTax":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netTaxPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fileUrl":{"type":"string","format":"uri","nullable":true,"description":"Set for `format` `csv` or `xlsx`; a short-lived link."},"generatedAt":{"type":"string","format":"date-time"}}},
"FiscalPeriod": {"x-ticvai-persistence":"ledger.fiscal_period + ledger.fiscal_period_event","type":"object","description":"`startDate` and `endDate` are days in the region's time zone: a posting belongs to the period when its `postedAt`, in that zone, falls on or between them.\n","required":["id","legalEntityId","name","startDate","endDate","status"],"properties":{"id":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid"},"name":{"type":"string"},"startDate":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"endDate":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"status":{"$ref":"#/components/schemas/PeriodStatus"},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"closedAt":{"type":"string","format":"date-time","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The approval request a close or reopen is waiting on (`approvals`), routed to a finance approver (decided 28 September, audit R144). Null when nothing is waiting."},"events":{"type":"array","description":"**Every step of the period's close, oldest first**: begin, abandon, close and reopen, each with who, when and (for abandon and reopen) why. A reopened period restates figures somebody has already reported, so the reason is kept, not just the latest status.\n","items":{"$ref":"#/components/schemas/FiscalPeriodEvent"}}}},
"FiscalPeriodEvent": {"type":"object","description":"One step in a fiscal period's close. Written by the operation that took the step; never edited.","required":["action","principalId","occurredAt"],"properties":{"action":{"type":"string","enum":["beginClose","abandonClose","close","reopen"]},"reason":{"type":"string","nullable":true,"description":"Required by `abandonPeriodClose` and `reopenPeriod`; null for the other steps."},"principalId":{"type":"string","format":"uuid","description":"Who took the step."},"approverPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The approver of a `reopen`. Null for the other steps."},"occurredAt":{"type":"string","format":"date-time"}}},
"FxRate": {"type":"object","x-ticvai-persistence":"ledger.fx_rate","description":"Also the `setFxRate` body. **Server-owned fields are `readOnly`** and ignored if sent: `id`, `setByPrincipalId`, and the provenance `ingestFxRates` writes (`source`, `providerReference`, `fetchedAt`). A rate set through `setFxRate` has `source` `manual`.\n","required":["fromCurrency","toCurrency","rate","purpose","effectiveFrom"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"fromCurrency":{"type":"string","pattern":"^[A-Z]{3}$"},"toCurrency":{"type":"string","pattern":"^[A-Z]{3}$"},"rate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"description":"Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly.\n"},"purpose":{"$ref":"#/components/schemas/FxRatePurpose"},"source":{"allOf":[{"$ref":"#/components/schemas/FxRateSource"}],"readOnly":true},"effectiveFrom":{"type":"string","format":"date-time"},"effectiveTo":{"type":"string","format":"date-time","nullable":true,"description":"A rate change is a new row. The old one is never edited — a transaction posted last Tuesday must still reconcile at last Tuesday's rate.\n"},"setByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"note":{"type":"string","maxLength":500,"nullable":true,"description":"Why this rate, and from where. **Required when `source` is `manual`** (decided 28 September, audit R127 (4)); null on a rate `ingestFxRates` fetched."},"providerReference":{"type":"string","nullable":true,"readOnly":true,"description":"The provider's own identifier for this quote. **What makes a rate reproducible** — an auditor asking why a payment converted at 3.6725 gets an answer that is checkable against the source rather than a number somebody typed."},"fetchedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the rate was pulled. **Distinct from `effectiveFrom`**, which is when it applies — a rate fetched at 06:00 for a business day starting at 00:00 has two different times and conflating them makes a late feed look like a backdated rate."},"chargeable":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"With `venueId`, true where a guest may select this currency and pay in it at that venue (`tenancy.VenueSettings.chargeCurrencies`), false where it is shown as an approximate price only (CHG-FIN-001)."}}},
"FxRatePurpose": {"type":"string","description":"A venue does not accept dollars at the rate it books an intercompany balance at. Separating them is what stops a spread on the counter appearing as a loss in the accounts.\n","enum":["tender","interEntity","reporting","revaluation"]},
"FxRateSource": {"type":"string","description":"**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.","enum":["manual","uaeCentralBank","ecb","openExchangeRates","cardScheme","provider"]},
"FxRateValue": {"x-ticvai-persistence-column":"numeric(18,6)","type":"string","pattern":"^\\d+(\\.\\d{1,6})?$","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"},
"JournalEntry": {"x-ticvai-persistence":"ledger.journal_entry + ledger.journal_line","type":"object","required":["id","entryNumber","fiscalPeriodId","status","source","description","lines","totalDebit","totalCredit","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"entryNumber":{"type":"string","readOnly":true,"description":"Server-assigned, **in sequence per legal entity per fiscal year** (decided 28 September, audit R191), for example `JE-2026-000123`. Gapless within the legal entity and year: a number is taken when the entry reaches the ledger, not when a draft is saved.\n"},"fiscalPeriodId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/JournalStatus"},"source":{"$ref":"#/components/schemas/JournalSource"},"sourceId":{"type":"string","nullable":true,"description":"The order, refund or run that generated this entry."},"description":{"type":"string"},"reference":{"type":"string","nullable":true},"lines":{"type":"array","items":{"$ref":"#/components/schemas/JournalLine"}},"totalDebit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"postedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"reversalOfEntryId":{"type":"string","format":"uuid","nullable":true},"reversedByEntryId":{"type":"string","format":"uuid","nullable":true},"reversalReason":{"type":"string","nullable":true,"description":"On a reversal, the `reason` given to `reverseJournalEntry`. Null on every other entry."},"rejectionReason":{"type":"string","nullable":true,"description":"The comment from the latest `rejectJournal`, which the preparer reads before resubmitting. Null until an entry is rejected.\n"},"rejectedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"rejectedAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"postedAt":{"type":"string","format":"date-time","nullable":true}}},
"JournalLine": {"x-ticvai-append-only":"postedAt","type":"object","required":["accountId","debit","credit"],"properties":{"accountId":{"type":"string","format":"uuid"},"debit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"venueId":{"type":"string","format":"uuid","nullable":true},"costCenterId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string","maxLength":500},"postedAt":{"type":"string","format":"date-time","readOnly":true,"description":"**Copied from the journal entry when it posts** (ADR-0056), so the line table can be partitioned by month on its own column. Never differs from its entry's."}}},
"JournalSource": {"type":"string","enum":["manual","order","refund","void","shift","recognition","settlement","variance","reversal","writeOff","chargeback"]},
"JournalStatus": {"type":"string","enum":["draft","pendingApproval","posted","reversed"]},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PeriodCloseResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["fiscalPeriodId","dryRun","passed","checks"],"properties":{"fiscalPeriodId":{"type":"string","format":"uuid"},"dryRun":{"type":"boolean"},"passed":{"type":"boolean"},"checks":{"type":"array","items":{"type":"object","required":["check","passed"],"properties":{"check":{"type":"string","description":"**What each check is, and what fails it** (4 October 2026, CHG-FXC-009; the Sprint 1-2 judging found the values and\nno definition). Each runs over the period's legal entity and dates; `blockingCount` is what fails it.\n- `trialBalanceBalances`: posted `ledger.journal_line` debits equal credits for the period, per currency. Blocking:\n  currencies out of balance.\n- `noUnapprovedJournals`: no `ledger.journal_entry` dated in the period is `draft` or awaiting approval. Blocking: those\n  entries.\n- `noOpenShifts`: no POS shift with a business date in the period is still open, suspended or awaiting close approval,\n  asked of `orders.listShifts`. Blocking: those shifts.\n- `settlementsReconciled`: every `ledger.settlement` in the period is reconciled and no `ledger.settlement_exception`\n  on it is open. Blocking: unreconciled settlements plus open exceptions.\n- `recognitionRunComplete`: no `ledger.recognition_schedule` line due on or before the period end is unrecognised.\n  Blocking: those lines.\n- `priorPeriodClosed`: the legal entity's previous `ledger.fiscal_period` is `closed`. Blocking: 1 or 0.\n- `varianceExceptionsReviewed`: no `ledger.price_variance` in the period is unreviewed. Blocking: those variances.\nThe close fails (409, `PeriodCloseProblem.failedChecks`) when any check or wallet check fails; a dry run reports the\nsame list and locks nothing. Each run, dry or not, appends one `ledger.fiscal_period_event` with the results.","enum":["trialBalanceBalances","noUnapprovedJournals","noOpenShifts","settlementsReconciled","recognitionRunComplete","priorPeriodClosed","varianceExceptionsReviewed"]},"passed":{"type":"boolean"},"detail":{"type":"string"},"blockingCount":{"type":"integer"}}}},"walletChecks":{"type":"array","description":"**The wallet pre-close checks** (decided 2 October 2026, Chinmay, batch 6 #220, BO-1170; DEC-220; CHG-CSP-040). Beside `checks`, whose values clients built at r1 already switch on, so no value is added there. `passed` is false while any of these fails. Empty where the tenant has no wallet module.","items":{"type":"object","required":["check","passed"],"properties":{"check":{"type":"string","enum":["walletRollForwardTies","walletLiabilityMatchesLedger","noPendingWalletAuthorisations","expiredBalancesReleased","walletDisputesReviewed"],"description":"`walletRollForwardTies`: opening liability plus top-ups, minus spend, refunds and expiry, equals closing liability. `walletLiabilityMatchesLedger`: that closing liability equals the wallet liability account. `noPendingWalletAuthorisations`: no authorisation is still held open in the period. `expiredBalancesReleased`: balances past expiry were released to breakage. `walletDisputesReviewed`: no wallet dispute raised in the period is unreviewed."},"passed":{"type":"boolean"},"detail":{"type":"string"},"blockingCount":{"type":"integer"}}}},"walletRollForward":{"type":"object","nullable":true,"description":"**The period's wallet movement summary, as the close checked it** (DEC-220; CHG-CSP-040): read from wallet `getWalletMovementSummary` so BO-1170 shows the roll-forward beside the ledger checks. Null where the tenant has no wallet module.","properties":{"openingLiability":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"toppedUp":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"spent":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refunded":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expired":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closingLiability":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ledgerLiability":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The wallet liability account's balance, to compare with `closingLiability`."}}}}},
"PeriodStatus": {"type":"string","enum":["open","closing","closed"]},
"PostingEventType": {"type":"string","description":"Every event that generates a ledger posting.\n**How each money event posts** (decided 28 September, audit R191). Card payment `cardReceived`, cash payment `cashReceived`, refund `refundIssued`, a POS offline sync the same events as the payments it replays, dated by when the till recorded them. **Two added on that date**: `gameCreditLoaded`, the liability `wallet.loadGameCredits` creates, and `pointsAccrued`, the liability for loyalty points earned. Every posting goes to the fiscal period open for the event date, through the mapping for its event type, or to suspense where none is mapped.\n**Required before a venue trades**: `cardReceived`, `cashReceived`, `refundIssued` and `priceVariance` (audit R127 (1)).\n","enum":["ticketRevenue","fnbRevenue","retailRevenue","rentalRevenue","taxPayable","cashReceived","cardReceived","walletReceived","refundIssued","voidReversal","deferredRevenue","recognisedRevenue","breakageRevenue","priceVariance","cashOverShort","settlementFee","settlementClearing","gameCreditLoaded","pointsAccrued","chargebackDebit","chargebackReversal","chargebackFee"]},
"PriceVariance": {"x-ticvai-persistence":"ledger.price_variance","type":"object","required":["id","orderId","orderLineId","venueId","quotedPrice","serverPrice","variance","isException","occurredAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"orderLineId":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"quotedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"serverPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"catalogueBundleVersion":{"type":"string","nullable":true,"description":"The bundle the terminal priced from. Turns \"the price was wrong\" into \"the terminal was two bundles behind\", which is actionable.\n"},"isException":{"type":"boolean","description":"Above the venue's configured variance threshold."},"reviewStatus":{"$ref":"#/components/schemas/VarianceReviewStatus"},"reviewOutcome":{"type":"string","nullable":true,"description":"The `outcome` given to `reviewPriceVariance`. Null until reviewed.","enum":["accepted","investigated","catalogueCorrected"]},"reviewedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"journalEntryId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"RecognitionMethod": {"type":"string","enum":["immediate","onRedemption","straightLine","perVisit","onExpiry"]},
"RecognitionRunResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["fiscalPeriodId","dryRun","recognisedTotal","breakageTotal","entryCount"],"properties":{"fiscalPeriodId":{"type":"string","format":"uuid"},"dryRun":{"type":"boolean"},"recognisedTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"breakageTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entryCount":{"type":"integer"},"byMethod":{"type":"array","items":{"type":"object","properties":{"method":{"$ref":"#/components/schemas/RecognitionMethod"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"itemCount":{"type":"integer"}}}},"journalEntryIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"RecognitionSchedule": {"x-ticvai-persistence":"ledger.recognition_schedule","type":"object","description":"Also the `createRecognitionSchedule` body. **`id` is server-owned** (`readOnly`): a client does not send it, and one sent is ignored.\n","required":["id","name","method","productKinds"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string","maxLength":200},"method":{"$ref":"#/components/schemas/RecognitionMethod"},"priority":{"type":"integer","default":100,"description":"**Two schedules may both claim a product kind and nothing resolved which wins** — a silent double-recognition, which is the worst kind of accounting defect because the numbers look plausible.\nLowest priority wins, and **two schedules at the same priority claiming the same kind is refused at save** rather than resolved at run time.\n"},"recognitionSite":{"type":"string","enum":["sale","admission","consumption"],"default":"sale","description":"**Where revenue is earned, which is not always where it was sold.** A ticket sold at one venue and admitted at another earns at the gate, and recognising at the sale site puts the revenue in the wrong entity's books.\n`consumption` is for stored value — a wallet top-up is not revenue until it is spent.\n"},"frequency":{"type":"string","enum":["daily","weekly","monthly","onEvent","onPeriodClose"],"default":"onPeriodClose","description":"**Driven by the schedule rather than by whoever runs the job.** Recognition that happens when somebody remembers is recognition with no cut-off.\n"},"revalidateOnValidityChange":{"type":"boolean","default":true,"description":"**Changing an entitlement's validity did not re-time its deferred balance.** A pass extended by three months has three more months of deferral, and a schedule that ignores that recognises revenue the venue has not yet earned.\n"},"productKinds":{"type":"array","minItems":1,"description":"The product kinds this schedule claims, from the catalogue's `ProductKind`.","items":{"type":"string","allOf":[{"$ref":"../spine/catalogue.yaml#/components/schemas/ProductKind"}]}},"deferredAccountId":{"type":"string","format":"uuid"},"recognisedAccountId":{"type":"string","format":"uuid"},"breakageAccountId":{"type":"string","format":"uuid","nullable":true},"noShowTrigger":{"type":"string","nullable":true,"enum":["performanceEnd","validityEnd","none"],"description":"8.1.1. **A no-show is breakage with a known moment**, and the mechanism already existed — `breakageAfterDays` moves deferred revenue to earned after a period. A ticket for a performance that has finished does not need a waiting period: **the guest cannot arrive any more.**\n`performanceEnd` recognises when the performance completes. `validityEnd` recognises when an open-dated entitlement lapses, which is where `breakageAfterDays` still applies.\n**`none` keeps the current behaviour** — recognise on the schedule and nothing else — so no existing schedule changes.\n"},"noShowAccountId":{"type":"string","format":"uuid","nullable":true,"description":"Where no-show revenue lands. **Separate from `recognisedAccountId` by default**, because revenue from a guest who came and revenue from one who did not are different lines to whoever reads the P&L — and 8.1.2 asks for a report on exactly that distinction.\n"},"breakageAfterDays":{"type":"integer","nullable":true,"description":"Days after expiry at which unredeemed value becomes breakage."},"isActive":{"type":"boolean"}}},
"Settlement": {"x-ticvai-persistence":"ledger.settlement","type":"object","required":["id","providerName","periodStart","periodEnd","status","ingestedAt"],"properties":{"id":{"type":"string","format":"uuid"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","description":"**A settlement has no account, so nothing else denominates it.** A posting takes its currency from `ledger.account.currency` and a payment from `tenderCurrency`, but a settlement is a provider file for a period: `providerGross`, `ledgerGross` and `difference` are bare amounts, and a provider file in one currency against a ledger in another computes a difference that means nothing. Added 20 September, when a venue became able to trade outside its region's currency.\n"},"providerName":{"type":"string"},"venueId":{"type":"string","format":"uuid","description":"The venue this settlement is for. **Reconciled daily per venue** (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are the same day."},"periodStart":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"periodEnd":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"fileReference":{"type":"string","format":"uuid","description":"The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. **Kept on the row because parsing is asynchronous**: the job that parses the file reads it from here.\n"},"format":{"type":"string","nullable":true,"enum":["csv","fixedWidth","xml","json"],"description":"The file format given at ingest. Null when none was given."},"status":{"$ref":"#/components/schemas/SettlementStatus"},"lineCount":{"type":"integer"},"matchedCount":{"type":"integer"},"exceptionCount":{"type":"integer"},"providerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerFees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerNet":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ledgerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ingestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region` scope.**"}}},
"SettlementStatus": {"type":"string","enum":["ingesting","parsing","matching","matched","hasExceptions","resolved","failed"]},
"TaxCode": {"x-ticvai-persistence":"ledger.tax_code","type":"object","required":["id","code","name","countryCode","rate","effectiveFrom","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$"},"appliesTo":{"type":"array","description":"**What this code covers, and `donation` is why the field exists** (CF-84). Donation tax treatment varies by jurisdiction — **0% is a valid rate, not an absence of one** — and it is set here rather than assumed in the posting.\nThe liability-account posting stays the default and is no longer the only option.\n","items":{"type":"string","enum":["goods","services","admission","food","accommodation","donation","gratuity","fee"]}},"rate":{"type":"number","minimum":0,"maximum":100},"compoundOnTaxCodeId":{"type":"string","format":"uuid","nullable":true,"description":"When set, this tax applies to the base **plus** the referenced tax, not to the base alone. Ordering is explicit rather than implied.\n"},"isInclusive":{"type":"boolean","description":"True when the displayed price already contains this tax."},"accountId":{"type":"string","format":"uuid"},"effectiveFrom":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"effectiveTo":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight.","nullable":true},"isActive":{"type":"boolean"}}},
"TaxExemption": {"x-ticvai-persistence":"ledger.tax_exemption","type":"object","description":"Also the `createTaxExemption` body. **`id` is server-owned** (`readOnly`): a client does not send it, and one sent is ignored. OpenAPI 3.1: a `readOnly` property in `required` is required in responses only.\n","required":["id","scope","taxCodeId","reason"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scope":{"type":"string","enum":["account","productKind","channel","legalEntity"]},"scopeRef":{"type":"string","description":"Identifier of the exempt subject, matching `scope`."},"taxCodeId":{"type":"string","format":"uuid"},"reason":{"type":"string","maxLength":500},"exemptionType":{"type":"string","enum":["diplomatic","export","businessToBusiness","charity","governmentEntity","freeZone","zeroRated","other"],"description":"Tax Exemption Evidence: exemption type (pack 'Pricing___Revenue_Management_Reference.pdf' p.47). Moved here from catalogue `listFeeWaiverTax`, whose rule now only says `evidenceRequired` (decided 29 September, readiness close-out). Which types a jurisdiction recognises is the client's tax configuration; the list names the kinds, it does not grant any. **Proposed values: tax configuration per jurisdiction, client to correct.**"},"certificateReference":{"type":"string","maxLength":100,"nullable":true,"description":"Tax Exemption Evidence: reference, e.g. the exemption certificate, diplomatic card or export declaration number."},"evidenceDocumentId":{"type":"string","format":"uuid","nullable":true,"description":"Tax Exemption Evidence: the uploaded document (certificate scan, declaration). Kept for the retention period of the postings it exempted, not of the exemption."},"verificationStatus":{"type":"string","enum":["notRequired","pending","verified","rejected","expired"],"default":"pending","description":"Tax Exemption Evidence: verification status. **Only `verified` and `notRequired` exempt a line**; `calculateTax` treats `pending`, `rejected` and `expired` as no exemption and records the exemption id on the line so the refusal is explainable. `expired` is set by the server once `validTo` has passed; evidence checked after the grant is recorded with `verifyTaxExemption`. The granter sends `verified` on `createTaxExemption` when the evidence was checked at the grant; `verifiedBy` and `verifiedAt` are then set from the caller."},"verifiedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"verificationNote":{"type":"string","maxLength":500,"nullable":true,"readOnly":true,"description":"The `note` given to `verifyTaxExemption`; required when evidence was rejected."},"validFrom":{"type":"string","format":"date","description":"Tax Exemption Evidence: validity, first day. A day in the region's time zone, local midnight to local midnight."},"validTo":{"type":"string","format":"date","description":"Tax Exemption Evidence: validity, last day. A day in the region's time zone, local midnight to local midnight.","nullable":true}}},
"TrialBalance": {"x-ticvai-persistence":"none — computed","type":"object","required":["fiscalPeriodId","isBalanced","totalDebit","totalCredit","accounts"],"properties":{"fiscalPeriodId":{"type":"string","format":"uuid"},"isBalanced":{"type":"boolean","description":"False indicates a defect, not a business condition. Double-entry cannot be unbalanced by legitimate activity.\n"},"totalDebit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accounts":{"type":"array","items":{"type":"object","required":["accountId","accountCode","accountName","debit","credit","balance"],"properties":{"accountId":{"type":"string","format":"uuid"},"accountCode":{"type":"string"},"accountName":{"type":"string"},"type":{"$ref":"#/components/schemas/AccountType"},"debit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"VarianceReviewStatus": {"type":"string","enum":["notRequired","pendingReview","reviewed"]}
}
```
