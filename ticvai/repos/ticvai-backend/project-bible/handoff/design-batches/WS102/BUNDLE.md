# WS102 — Subscription Licensing AI Self Service board 5

**10 screens · 15 operations · 24 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `ACCOUNT_CONFIGURE, ORDER_VIEW, PLATFORM_BILLING_MANAGE, PLATFORM_BILLING_VIEW, PLATFORM_CELL_MANAGE, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_VIEW, SCOPE_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
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
| `ADM-409` | Purchase / Trial Journey Selection | B | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `ADM-410` | Contract & Billing Cycle Selection | B | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-411` | Billing & Legal Entity Information | B | 17 | 19 | 7 | 9 | 0 | 0 | — | notStarted (—) |
| `ADM-412` | Payment Method & Settlement Setup | A | 48 | 16 | 7 | 24 | 0 | 0 | — | notStarted (—) |
| `ADM-413` | Trial Configuration & Conversion Rules | B | 16 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `ADM-414` | Order & Commercial Pricing Review | B | 0 | 10 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-415` | Commercial Agreement, Billable Definition & Customer Acceptance | B | 0 | 16 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-416` | Payment, Contract & Commercial Validation | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-417` | Subscription Confirmation & Commercial Activation | B | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-418` | Subscription Lifecycle & Trial-to-Paid Handoff | B | 0 | 28 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-409, ADM-410, ADM-414, ADM-415, ADM-416, ADM-417, ADM-418 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-409` Purchase / Trial Journey Selection

**Determine how the customer enters the commercial activation journey.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29201 (APP-CONSOLE-ADM-409) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/purchase-trial-journey-selection-adm-409` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-021): setTrialConfiguration sets TICVAI's trial rules (PLATFORM_PLAN_MANAGE); the prospect chooses, TICVAI configures trials on ADM-413 (design-notes correction …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** How a customer enters activation: trial or purchase; also where TICVAI's trial terms are set.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setTrialConfiguration: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/subscription.yaml#setTrialConfiguration)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-410` Contract & Billing Cycle Selection: *Contract & Billing Cycle Selection*
- → `ADM-411` Billing & Legal Entity Information: *Billing & Legal Entity Information*
- → `ADM-412` Payment Method & Settlement Setup: *Payment Method & Settlement Setup*
- → `ADM-413` Trial Configuration & Conversion Rules: *Trial Configuration & Conversion Rules*
- → `ADM-414` Order & Commercial Pricing Review: *Order & Commercial Pricing Review*
- → `ADM-415` Commercial Agreement, Billable Definition & Customer Acceptance: *Commercial Agreement, Billable Definition & Customer Acceptance*
- → `ADM-416` Payment, Contract & Commercial Validation: *Payment, Contract & Commercial Validation*
- → `ADM-417` Subscription Confirmation & Commercial Activation: *Subscription Confirmation & Commercial Activation*
- → `ADM-418` Subscription Lifecycle & Trial-to-Paid Handoff: *Subscription Lifecycle & Trial-to-Paid Handoff*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The purchase trial journey list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the purchase trial journey untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No purchase trial journey yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the purchase trial journey are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
journey: 30-day trial
convertsTo: Growth plan
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- "Try it" is a single shared, pre-configured demo (sample products, working POS/admin sales flow, reporting) entered with shared credentials - evaluation only, cannot sell real tickets; not a per-prospect trial tenant. *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-831)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-409` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-409`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 5
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 1: Opens Purchase / Trial Journey Selection → Determine how the customer enters the commercial activation journey.
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F211 branch at step 1 (expected): when Nothing has been set up on Purchase / Trial Journey Selection yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F211 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-409?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-410`, `ADM-411`, `ADM-412`, `ADM-413`, `ADM-414`, `ADM-415`, `ADM-416`, `ADM-417`, `ADM-418`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-410` Contract & Billing Cycle Selection

**Define the contractual duration and billing/reconciliation cycle.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29324 (APP-CONSOLE-ADM-410) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/contract-billing-cycle-selection-adm-410` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Custom Term. Each needs an operation, or needs removing from the screen; this is the Phase 3 reconciliation … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Contract duration and billing cycle for a customer.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Custom Term (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-409` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The contract billing cycle list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the contract billing cycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No contract billing cycle yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the contract billing cycle are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Downgrade conflicts with current usage. The response names every module and limit that would be violated. (DowngradeConflictProblem); 422 `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed` … |

#### Edge cases to draw

- **setSubscription answers 409**: Show it as something the person can act on, not a failure: Downgrade conflicts with current usage. The response names every module and limit that would be violated. Or the subscription is `expired` and cannot be reactivated (`subscription-expired`, audit STATE-SUBSCRIPTION); start a new one. *(source: contracts/satellite/subscription.yaml#setSubscription)*
- **setSubscription answers 422**: Show it as something the person can act on, not a failure: `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed`, audit R214 (1)). Or the plan is a custom package private to another tenant (`plan-not-offered`, decided 29 September). *(source: contracts/satellite/subscription.yaml#setSubscription)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
term: 36 months
billingCycle: monthly
reconciliation: quarterly
```

#### Permissions

- `setSubscription` → `PLATFORM_TENANT_MANAGE` (configure) · staff, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.2 | Monthly Billing - System shall support monthly subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |
| 20.2.3 | Annual Billing - System shall support annual subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-410` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-410`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 5
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 2: Works in Contract & Billing Cycle Selection → Define the contractual duration and billing/reconciliation cycle.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-410?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Custom Term, Cancel.
- [ ] Every transition is wired: `ADM-409`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-411` Billing & Legal Entity Information

**Capture the legally correct customer and billing information.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29325 (APP-CONSOLE-ADM-411) |
| Who uses it | ticvai staff holding `ACCOUNT_CONFIGURE`, `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW` (2 configure, 2 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/tenants-licensing/billing-legal-entity-information-adm-411` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `createLegalEntity` (ACCOUNT_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it. **Billing entity (decided 2 October 2026 by Chinmay, DEC-209, DEC-210; CHG-CSA-030, CHG-CSP-008):** the invoiced company and its TRN certificate are a billing-entity record in the subscription contract (`getBillingEntity`, `setBillingEntity`); a trade licence is always required, a VAT certificate when a TRN is entered, configurable per country (`RegionSettings.requiredBillingDocuments`). This screen is the console copy of SGN-020: the bindings land through `tools/applied/apply-subscription-placement.py` once the P17 twin is updated (screens-other).

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Commercial Customer ≠ Operating Venue, Validate Entity / Save / Continue. Each needs an operation, or needs … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Finance, Ledger & Tax · Reporting & Analytics process.** The operator-led step where TICVAI staff capture who TICVAI invoices: the legal name, tax registration (TRN) and its certificate, billing address and contact, invoicing frequency and payment method. The company that pays may not be the company that operates the venue, and the invoice must carry the payer's legal details exactly.

**Known correction pending (do not draw the wrong version)**

- **The screen calls createLegalEntity, which creates the tenant's own ledger entity (chart of accounts, fiscal periods) and has no billing address, billing contact or TRN certificate.** Why: The customer TICVAI invoices is a commercial-account record on the subscription side, not a ledger entity in the tenant's cell; the onboarding application carries no TRN or billing address either. *(source: contracts/spine/finance.yaml#createLegalEntity / contracts/satellite/subscription.yaml#submitOnboardingApplication / DI-830; Finance, Ledger & Tax · Reporting & Analytics)*
- **"Commercial Customer ≠ Operating Venue" is drawn as the primary button.** Why: It is a rule about the data (payer may differ from operator), so it is a switch, not an action. *(source: screens/P09-platform-admin-console.yaml#ADM-411; Finance, Ledger & Tax · Reporting & Analytics)*

#### Decided on this screen

Answered questions: draw the decision, not the old default. Where a decision and the tables below differ, the decision wins.

- **Which record holds the invoiced company (billing entity) and its TRN certificate?** → A new billing-entity record (invoiced company and TRN certificate) in the subscription contract. *(decided by Chinmay, 2026-10-02; DEC-209 / CHG-NOTE-003)*
- **Which document types are mandatory per country (trade licence, VAT certificate)?** → Trade licence always; VAT certificate when a TRN is entered; configurable per country. *(decided by Chinmay, 2026-10-02; DEC-210 / CHG-NOTE-003)*

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `ACCOUNT_CONFIGURE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Save billing entity** (modal, opened by *Save billing entity*; *Save billing entity* calls `setBillingEntity`, *Cancel* sends nothing)

**Collects what `setBillingEntity` sends before it is called.** Nothing in the body is required. Optional: `legalName`, `tradeLicenceNumber`, `trn`, `countryCode`, `address`, `invoiceEmail`, `documents`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Legal name `legalName` | text area | optional | — | max length 300 | — | — | `setBillingEntity` body |
| Trade licence number `tradeLicenceNumber` | text field | optional | — | max length 100 | — | — | `setBillingEntity` body |
| Trn `trn` | text field | optional | — | max length 30 | — | The tax registration number; entering one makes the VAT certificate required. | `setBillingEntity` body |
| Country code `countryCode` | text field | optional | — | min length 2; max length 2 | — | — | `setBillingEntity` body |
| Address `address` | text area | optional | — | max length 1000 | — | — | `setBillingEntity` body |
| Invoice email `invoiceEmail` | email field | optional | — | — | name@example.ae | — | `setBillingEntity` body |
| Documents `documents` | repeatable rows | optional | — | — | — | The trade licence and, where a TRN is entered, the VAT certificate, each a stored file with its verification. | `setBillingEntity` body |
| Document type `documents[].documentType` | segmented control | optional | — | Trade licence · VAT certificate | — | — | `setBillingEntity` body |
| File ref `documents[].fileRef` | text field | optional | — | — | — | — | `setBillingEntity` body |
| Expiry date `documents[].expiryDate` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setBillingEntity` body |
| Verification status `documents[].verificationStatus` | radio group | optional | — | Missing · Uploaded · Verified · Rejected · Expired | — | — | `setBillingEntity` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Rules for these inputs** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **the company we invoice is different from the venue operator**: A switch, off by default. On reveals a second block for the operating company; the invoice goes to the billing company, the licence to the operator. *(source: screens/P09-platform-admin-console.yaml#ADM-411 / DI-830)*
- **legal name, trade licence number, TRN, TRN certificate**: Legal name exactly as on the trade licence. TRN shown for VAT-registered countries; the certificate is uploaded as a PDF or image and checked against the typed number. Not registered for VAT is an explicit choice, not a blank. Saved on a billing-entity record (the invoiced company and its TRN certificate) in the subscription contract. The required documents are configurable per country; the default is the trade licence always and the VAT certificate when a TRN is entered. *(source: DI-830 / contracts/satellite/subscription.yaml#/components/schemas/PartnerDocument / contracts/spine/finance.yaml#/components/schemas/LegalEntity / decided 2 October 2026 by Chinmay (CHG-NOTE-003))*
- **country, currency, fiscal year start**: Country first; currency and its decimals follow from it; fiscal year start defaults to January (UAE) and April for India. *(source: MATRIX 5.7.38 / DI-263)*
- **invoicing frequency and payment method**: Monthly or annual; bank transfer or card. Values come from the commercial model already accepted on the previous step. *(source: DI-830)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Billing entity** (detail panel, from `getBillingEntity`): **The invoiced company and its TRN certificate are a billing-entity record (decided 2 October 2026 by Chinmay, DEC-209; CHG-CSA-030):** a trade licence always, a VAT certificate when a TRN is entered, configurable per country (DEC-210; `RegionSettings.requiredBillingDocuments`).

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Legal name | text | — |
| Trade licence number | text | — |
| Trn | text | The tax registration number; entering one makes the VAT certificate required. |
| Country code | text | — |
| Address | text | — |
| Invoice email | email, tap to write | — |
| Documents | list or chips (count when long) | The trade licence and, where a TRN is entered, the VAT certificate, each a stored file with its verification. |
| Document type | chip: Trade licence, VAT certificate | — |
| File ref | text | — |
| Expiry date | 1 Oct 2026 | — |
| Verification status | chip: Missing, Uploaded, Verified, Rejected, Expired | — |
| Missing documents | list or chips (count when long) | The documents the country's rule requires that are not yet uploaded and verified. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Commercial Customer ≠ Operating Venue (primary button) | navigation or local | — | — | — | — |
| Validate Entity / Save / Continue (secondary button) | navigation or local | — | — | — | — |
| Save billing entity (primary button) | `setBillingEntity` PUT `/tenants/{tenantId}/billing-entity` | BillingEntity | BillingEntity | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **invoice preview**: A small preview of the invoice header as it will print (legal name, address, TRN), so a typo is caught before the first invoice. *(source: designer default)*

**What each action does** (from the Finance, Ledger & Tax · Reporting & Analytics process; these refine the tables above and win where they differ)

- **Validate and continue**: Checks required fields and the TRN format; saves; continues to payment method. Errors name the field. *(source: screens/P09-platform-admin-console.yaml#ADM-411)*

**Data it reads**: `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …); `getBillingEntity` (onLoad, The company TICVAI invoices and its documents (DEC-209))

**Where the user goes next**

- → `ADM-409` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The billing legal entity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the billing legal entity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No billing legal entity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the billing legal entity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `ACCOUNT_CONFIGURE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **the TRN on the certificate does not match the typed TRN**: Blocks continue with "The TRN on the certificate is different from the one entered." *(source: designer default)*
- **a group with several venues in two countries**: One billing entity per country, because each invoice carries one country's tax. *(source: MATRIX 5.7.38)*

#### Consistency with other screens

- Match `SGN-020`: Same fields, same order and same words; SGN-020 is the self-service twin and the two are kept in step.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
billingCompany: Sharjah Leisure Holding PJSC · TRN 100217384600003 · PO Box 26300, Sharjah · accounts@shleisure.ae
operator: Al Majaz Leisure Parks LLC · operates Al Majaz Waterfront Fun Zone
invoicing: Monthly · bank transfer · AED
```

#### Permissions

- `createLegalEntity` → `ACCOUNT_CONFIGURE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `getBillingEntity` → `PLATFORM_BILLING_VIEW` (read) · staff
- `setBillingEntity` → `PLATFORM_BILLING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.7.38 | Support account ownership by business unit/site. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.49 | Support multiple sites/business entities. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.50 | Assign accounts to specific sites. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.51 | Site-level account reporting. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.52 | Site-level balance reporting. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.54 | Site-level revenue tracking. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.56 | Site-level accounting permissions. | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 5.7.88 | The system shall support multiple legal entities, companies, business units, and attractions while maintaining separate accounting books, reporting structures, and financial controls. Shared products … | F&B & Guest Management | CONTRACTED | `createLegalEntity` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-411` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-411`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 5
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 4: Works in Billing & Legal Entity Information → Capture the legally correct customer and billing information.

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-411?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Commercial Customer ≠ Operating Venue, Validate Entity / Save / Continue, Save billing entity, Open access grant.
- [ ] Every transition is wired: `ADM-409`.
- [ ] Every gated control is gated: `ACCOUNT_CONFIGURE`, `PLATFORM_BILLING_MANAGE`, `PLATFORM_BILLING_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] The 2 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] The 2 decision(s) taken on this screen are drawn as decided, not as the old default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-412` Payment Method & Settlement Setup

**Set up a tenant's payment provider and settlement for a venue, from the console under an open grant.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `core` module |
| Block | Block A · ticket #27966 (APP-SETUP-ADM-412) |
| Who uses it | ticvai staff holding `ORDER_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE` (3 read, 1 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/tenants-licensing/payment-method-settlement-setup-adm-412` |

**What the spec says about it.** **Save form bound 4 October 2026 to SetPaymentProviderRequest: name, kind, methods, currencies, channels, credential reference, scope, active and routing (the methods multiSelect alone could not send a provider)** (CHG-FXS-002)

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Set up how a tenant's payment provider collects and settles: supported methods per the provider, settlement, under a platform-staff grant into the picked tenant. This screen is the reference implementation of how a platform operator acts inside a tenant: pick a tenant, open a time-boxed grant with a second factor, see the grant and its countdown while working.

**Fixed on main** (the package already carries these; draw what it says): Purpose is "Configure how TICVAI collects its fees", and the only write is the tenant's setPaymentProvider (venue scope). (CHG-SBO-011); The gaps entry says the screen declares no write. (CHG-SBO-011); setPaymentProvider is configured per venue, but the picker chooses only a tenant. (CHG-SBO-011).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant … | `Tenant.id` |
| Venue | picker: choose an id | optional | — | — | shows names, sends the id | After the tenant, the venue: `setPaymentProvider` is configured per venue (ADR-0018), so a venue is picked inside the open grant. | `OrgUnit.id` |
| Provider name | text field | optional | — | — | — | — | `SetPaymentProviderRequest.name` |
| Gateway | select | optional | — | Network international · Stripe · Adyen · Checkout · Cash · Wallet · Other | — | Network International and Stripe for Phase 1 (CF-131). | `SetPaymentProviderRequest.kind` |
| Payment methods | multi-select chips | optional | — | Card · Apple pay · Google pay · Samsung pay · Wallet · Bank transfer · Cash · Bnpl | — | — | `SetPaymentProviderRequest.supportedMethods` |
| Currencies | list of values (chips) | optional | — | — | — | — | `SetPaymentProviderRequest.supportedCurrencies` |
| Channels | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | BL-115. Which channels may use this provider. | `SetPaymentProviderRequest.acceptedOnChannels` |
| Credential reference | text field | optional | — | — | — | The vault reference the operator was given, never the key itself. | `SetPaymentProviderRequest.credentialRef` |
| Applies at | segmented control | optional | — | Tenant · Region · Venue | — | Venue by default: the venue picked above. | `SetPaymentProviderRequest.scopeLevel` |
| Active | toggle | optional | — | — | — | — | `SetPaymentProviderRequest.isActive` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |
| Under | text field | — | — | `listOrgUnits` ?under |
| Level | select | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet; Modelling a restaurant as a department would put it in the staffing tree, which is why the two cannot be collapsed (CF-138, ADR-0018). | `listOrgUnits` ?level |
| Include inactive | toggle | off | — | `listOrgUnits` ?includeInactive |

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

**Sent by *Save payment provider*** (`setPaymentProvider`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setPaymentProvider` body |
| Name `name` | text field | required | — | — | — | — | `setPaymentProvider` body |
| Kind `kind` | select | required | — | Network international · Stripe · Adyen · Checkout · Cash · Wallet · Other | — | — | `setPaymentProvider` body |
| Supported methods `supportedMethods` | multi-select chips | optional | — | Card · Apple pay · Google pay · Samsung pay · Wallet · Bank transfer · Cash · Bnpl | — | — | `setPaymentProvider` body |
| Supported currencies `supportedCurrencies` | list of values (chips) | optional | — | — | — | — | `setPaymentProvider` body |
| Supports tokenisation `supportsTokenisation` | toggle | optional | — | — | — | The keystone. Recurring billing, wallet auto-reload, one-click checkout and payment links all require a stored credential, and none of them can be designed until this is answered … | `setPaymentProvider` body |
| Supports partial capture `supportsPartialCapture` | toggle | optional | on | — | — | — | `setPaymentProvider` body |
| Accepted on channels `acceptedOnChannels` | multi-select chips | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | BL-115. Which channels may use this provider. | `setPaymentProvider` body |
| Presentment currencies `presentmentCurrencies` | list of values (chips) | optional | — | — | — | BL-070. What a storefront may quote in, distinct from what it settles in. | `setPaymentProvider` body |
| Supports3ds `supports3ds` | toggle | optional | on | — | — | — | `setPaymentProvider` body |
| Terminal `terminal` | group | optional | — | — | — | BL-119. Terminal behaviour, where this provider drives a physical device. | `setPaymentProvider` body |
| Emv certification ref `terminal.emvCertificationRef` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Offline floor limit `terminal.offlineFloorLimit` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What a terminal may approve with no connection. Above it the sale waits; below it the venue carries the risk knowingly — and a floor limit of zero means a till stops when the line … | `setPaymentProvider` body |
| Supports offline approval `terminal.supportsOfflineApproval` | toggle | optional | off | — | — | — | `setPaymentProvider` body |
| Receipt signature required `terminal.receiptSignatureRequired` | toggle | optional | off | — | — | — | `setPaymentProvider` body |
| Supports tip on terminal `terminal.supportsTipOnTerminal` | toggle | optional | off | — | — | — | `setPaymentProvider` body |
| Credential ref `credentialRef` | text field | optional | — | — | — | A vault reference. Never the credential, never returned, and rotated without a contract change. | `setPaymentProvider` body |
| Scope level `scopeLevel` | segmented control | optional | — | Tenant · Region · Venue | — | — | `setPaymentProvider` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Is active `isActive` | toggle | required | — | — | — | — | `setPaymentProvider` body |
| Routing `routing` | repeatable rows | optional | — | — | — | The ordered rules that send payments to this provider. `providerId` on each is this provider's `id`. | `setPaymentProvider` body |
| ID `routing[].id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setPaymentProvider` body |
| Priority `routing[].priority` | number field | required | — | — | — | — | `setPaymentProvider` body |
| Provider `routing[].providerId` | picker: choose a provider | required | — | — | shows names, sends the id | — | `setPaymentProvider` body |
| Conditions `routing[].conditions` | group | optional | — | — | — | Match on what is known before the charge — channel, currency, method, issuer country, amount band. | `setPaymentProvider` body |
| Channel `routing[].conditions.channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing. | `setPaymentProvider` body |
| Currency `routing[].conditions.currency` | text field | optional | — | Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. | — | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per … | `setPaymentProvider` body |
| Method `routing[].conditions.method` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Issuer country `routing[].conditions.issuerCountry` | text field | optional | — | — | — | — | `setPaymentProvider` body |
| Min amount `routing[].conditions.minAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPaymentProvider` body |
| Max amount `routing[].conditions.maxAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPaymentProvider` body |
| Fallback provider `routing[].fallbackProviderId` | picker: choose a fallback provider | optional | — | — | shows names, sends the id | Where this provider declines or is unreachable. A decline is not always a fallback case — an insufficient-funds decline should not be retried elsewhere, and a gateway timeout … | `setPaymentProvider` body |
| Scope path `routing[].scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `setPaymentProvider` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Payment methods**: The options are exactly the provider's supportedMethods enum (card, bankTransfer, ...), not the pack's labels. *(source: contracts/spine/orders.yaml#setPaymentProvider)*
- **Open access grant (permissions, reason, expiry)**: Permissions preselected to exactly what this screen's tenant calls need (TENANT_CONFIGURE), never PLATFORM_* (those ride on the platform token); reason required and shown to the tenant; expiry at most 8 hours ahead (proposed). The tenant must be picked first. *(source: R098; contracts/spine/identity.yaml#openPlatformStaffGrant)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setPaymentProvider: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/orders.yaml#setPaymentProvider)*

#### Outputs: what the screen shows and produces

**Shown**

**Show the payment providers as configured** (card list, from `listPaymentProviders`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Network international, Stripe, Adyen, Checkout, Cash, Wallet… | — |
| Supports tokenisation | yes / no (icon or chip) | The keystone. Recurring billing, wallet auto-reload, one-click checkout and payment links all require a stored credential, and none of them … |
| Supports partial capture | yes / no (icon or chip) | — |
| Supports3ds | yes / no (icon or chip) | — |
| Scope level | chip: Tenant, Region, Venue | — |

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

**Routing** (card list, from `setPaymentProvider`): Ordered rules, first match wins; a fallback provider is required.

| Shows | Format | Notes |
|---|---|---|
| Priority | 1,234 | — |
| Conditions | grouped details | Match on what is known before the charge — channel, currency, method, issuer country, amount band. |
| Fallback provider | the name it points at, never the id | Where this provider declines or is unreachable. A decline is not always a fallback case — an insufficient-funds decline should not be … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save payment provider (primary button) | `setPaymentProvider` PUT `/payment-providers` | SetPaymentProviderRequest | PaymentProvider | 412 The row changed since the `If-Match` version was read (SD-013). Re-read and retry. | — |
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Grant panel**: Which tenant, which permissions, why, ticket reference and time left to expiry; always visible while acting in the tenant. *(source: R098; contracts/spine/identity.yaml#openPlatformStaffGrant)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Open access grant**: Confirmation names the consequence first, then asks for the authentication code (authenticator app, or an emailed code as fallback); only a verified challenge sends openPlatformStaffGrant with its single-use stepUpToken. Wrong code: the action is not sent and nothing changes; five wrong codes lock step-up for the policy's lockout minutes and the screen says when it lifts. Why the control exists: Opens a platform operator's access into a tenant's data. *(source: contracts/spine/identity.yaml#openPlatformStaffGrant; R126; contracts/spine/identity.yaml#createMfaChallenge)*

**Data it reads**: `listTenants` (onLoad, The tenant picker — the operator picks a tenant before …); `listOrgUnits` (onLoad, The picked tenant's venues, to pick the venue the payment …); `listPaymentProviders` (onLoad, Show the payment providers as configured)

**Where the user goes next**

- → `ADM-409` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment method settlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment method settlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment method settlement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment method settlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **The platform-staff grant expires while the operator is mid-edit**: Every tenant action disables at once, the grantRequired state returns with Open access grant, and anything typed is kept so it can be sent after a new grant; the countdown in the grant panel warns before expiry. *(source: R098; screens/P09-platform-admin-console.yaml#ADM-412)*
- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_TENANT_ACCESS for Open access grant; TENANT_CONFIGURE for Save payment provider. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/identity.yaml#openPlatformStaffGrant)*

#### Consistency with other screens

- Match `ADM-409`: Entered from and returns to it.
- Match `BO-068`: The tenant sees every action taken under the grant in its audit log.
- Match `ADM-412`: Same tenant picker, grant panel and grantRequired state on every P09 screen that acts in a tenant (R098).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tenant: Marina Leisure Group
grant:
  permissions:
  - TENANT_CONFIGURE
  reason: Set up Network International for AquaCove Muscat
  ticketRef: SUP-8812
  expiresIn: 3 h 12 min
provider:
  name: Network International
  supportedMethods:
  - card
  - applePay
  - googlePay
```

#### Permissions

- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `setPaymentProvider` → `TENANT_CONFIGURE` (configure) · staff, prospect
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `listOrgUnits` → `SCOPE_VIEW` (read) · staff
- `listPaymentProviders` → `ORDER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.7.3 | Integrate with Stripe payment gateway and issue ticket and send confirmation email immediately after payment confirmation. | Ticketing Sales | CONTRACTED | `setPaymentProvider` |
| 4.2.9 | The system should be able to process payments by integrating with Stripe payment service provider. | Bundles and Promotions | CONTRACTED | `setPaymentProvider` |
| 3.3.41 | Venue-Specific Policies - System shall support venue-specific access policies. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 3.3.43 | Policy Inheritance - System shall support inheritance of policies across organizational structures. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 7.1.13 | The system shall support permission assignment at company, department, venue, park, attraction, facility, event, sales channel, POS terminal, and product levels. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.27 | The system shall support management of companies, business units, departments, parks, venues, attractions, facilities, cost centers, and reporting structures. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.37 | Allow administrators to restrict access by venue, park, facility, attraction, sales channel, POS terminal, country, region, IP address and network range. Policies should support allow/deny logic and … | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.52 | Support policies spanning multiple parks, venues, attractions, departments and business units while maintaining centralized governance. | F&B POS | CONTRACTED | `listOrgUnits` |
| 2.6.33 | Website should be able to display multi currency and users should be able to switch the prices to the selected foreign currency. All the ticket prices, currency symbol to be shown based on the … | Ticketing Sales | CONTRACTED | data `PaymentProvider` |
| 2.9.1 | The system should display prices in multiple currencies in the B2C portal for guests comparison although the sale will be finalized always in local currency. | Ticketing Sales | CONTRACTED | data `PaymentProvider` |
| 4.2.10 | The system should support multiple different payments. The final list of payment methods will be dependent on the capabilities of the payment service provider. System should allow the admin team to … | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| 4.2.12 | The system should support configuration of variable payment methods for different sales channels. Payment methods can be different from one sales channel to another. | Bundles and Promotions | CONTRACTED | data `PaymentProvider` |
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-412` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-412`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 5
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 6: Works in Payment Method & Settlement Setup → Configure how TICVAI collects its fees.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)
- ADR-0020 *— Where AI runs, and what it is isolated from* (`docs/adr/0020-ai-isolation-boundary.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (48), with its required mark, default, format and its error state (400, 403, 412).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-412?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Save payment provider, Open access grant.
- [ ] Every transition is wired: `ADM-409`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `SCOPE_VIEW`, `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-413` Trial Configuration & Conversion Rules

**Configure trial terms where the selected package is trial-eligible. Not every commercial model needs to support trials.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29326 (APP-CONSOLE-ADM-413) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Trial Configuration; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/trial-configuration-conversion-rules-adm-413` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Trial terms: dates, modules, limits (POS, access, users, tickets, API, storage), free or paid, conversion rules.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Trial Start | select field | — | — | — | — | — | — |
| Trial End | select field | — | — | — | — | — | — |
| Duration | select field | — | — | — | — | — | — |
| Modules Enabled | select field | — | — | — | — | — | — |
| POS Limit | select field | — | — | — | — | — | — |
| Access Limit | select field | — | — | — | — | — | — |
| User Limit | select field | — | — | — | — | — | — |
| Transaction Limit | select field | — | — | — | — | — | — |
| Ticket Limit | select field | — | — | — | — | — | — |
| API Limit | select field | — | — | — | — | — | — |
| Storage Limit | select field | — | — | — | — | — | — |
| Free Trial | select field | — | — | — | — | — | — |
| Paid Trial | select field | — | — | — | — | — | — |
| Trial Credit | select field | — | — | — | — | — | — |
| Limited Usage | select field | — | — | — | — | — | — |
| Full Package Trial | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setTrialConfiguration: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/subscription.yaml#setTrialConfiguration)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-409` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The trial conversion rules configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the trial conversion rules untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No trial conversion rules configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
trial:
  type: Free trial
  duration: 30 days
  modules:
  - ticketing
  - pos
  posLimit: 2
  ticketLimit: 5000
```

#### Permissions

- `setTrialConfiguration` → `PLATFORM_PLAN_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Back-end configuration access can optionally be added to the demo for qualified prospects at TICVAI's discretion; demo credentials can be scoped and time-limited (auto-expire after an evaluation period). *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-832)*
- "Try it" is a single shared, pre-configured demo (sample products, working POS/admin sales flow, reporting) entered with shared credentials - evaluation only, cannot sell real tickets; not a per-prospect trial tenant. *(agreed · MoM 10 Sep 2026, 4.11 Demo Environment Scope · DI-831)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-413` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-413`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 5
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 8: Works in Trial Configuration & Conversion Rules → Configure trial terms where the selected package is trial-eligible. Not every commercial model needs to support trials.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-413?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-409`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-414` Order & Commercial Pricing Review

**Show the complete financial arrangement before contractual acceptance. This screen must adapt dynamically to the commercial model. Example — Per Ticket + Minimum Guarantee**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29331 (APP-CONSOLE-ADM-414) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/order-commercial-pricing-review-adm-414` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The full financial arrangement before acceptance (twin of SGN-022).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 5 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every order commercial pricing** (data table)

| Shows | Format | Notes |
|---|---|---|
| Discount type | text | not in the schema: `Discount Type` |
| Value | text | not in the schema: `Value` |
| Period | text | not in the schema: `Period` |
| Approved by | text | not in the schema: `Approved By` |
| Expiry | text | not in the schema: `Expiry` |

**The selected order commercial pricing** (detail panel): The pack groups this record's detail under its own headings: “Rate”, “Expected Volume”, “Included Modules”, “Technical Capacity”, “Show where applicable”.

| Shows | Format | Notes |
|---|---|---|
| Discount type | text | not in the schema: `Discount Type` |
| Value | text | not in the schema: `Value` |
| Period | text | not in the schema: `Period` |
| Approved by | text | not in the schema: `Approved By` |
| Expiry | text | not in the schema: `Expiry` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (Value)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `previewSubscriptionChange` (onLoad, Order and pricing review)

**Where the user goes next**

- → `ADM-409` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order commercial pricing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order commercial pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order commercial pricing yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the order commercial pricing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-022`: Twin.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every order commercial pricing:
- Discount Type: 233
  Value: AED 12,400.00
  Period: 57
  Approved By: Rahul Menon
  Expiry: 57
- Discount Type: 57
  Value: AED 482,300.00
  Period: 11
  Approved By: Fatima Al Mansoori
  Expiry: 11
- Discount Type: 11
  Value: AED 96,750.00
  Period: 128
  Approved By: Omar Haddad
  Expiry: 128
```

#### Permissions

- `previewSubscriptionChange` → `PLATFORM_TENANT_VIEW` (read) · staff, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.5 | Subscription Upgrade - System shall support subscription upgrades. | Subscription & Licensing Management | CONTRACTED | `previewSubscriptionChange` |
| 20.2.6 | Subscription Downgrade - System shall support subscription downgrades. | Subscription & Licensing Management | CONTRACTED | `previewSubscriptionChange` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-414` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-414`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 5
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 10: Works in Order & Commercial Pricing Review → Show the complete financial arrangement before contractual acceptance. This screen must adapt dynamically to the commercial model. Example — Per Ticket + Minimum Guarantee

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-414?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-409`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-415` Commercial Agreement, Billable Definition & Customer Acceptance

**This becomes one of the most important revised screens. The customer must understand and formally accept what TICVAI considers billable.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29327 (APP-CONSOLE-ADM-415) |
| Who uses it | ticvai staff holding `PLATFORM_CELL_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/commercial-agreement-billable-definition-customer-accept-adm-415` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The agreement and billable definition the customer accepts (twin of SGN-023).

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 8 labels bound). (CHG-SBO-005)

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every commercial agreement billable** (data table)

| Shows | Format | Notes |
|---|---|---|
| Commercial model | text | not in the schema: `Commercial Model` |
| Contracted rate | text | not in the schema: `Contracted Rate` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Guarantee period | text | not in the schema: `Guarantee Period` |
| Billing cycle | text | not in the schema: `Billing Cycle` |
| Contract duration | text | not in the schema: `Contract Duration` |
| Renewal | text | not in the schema: `Renewal` |
| Payment terms | text | not in the schema: `Payment Terms` |

**The selected commercial agreement billable** (detail panel): The pack groups this record's detail under its own headings: “For a transaction contract”, “For a per-ticket contract”, “Customer confirms”.

| Shows | Format | Notes |
|---|---|---|
| Commercial model | text | not in the schema: `Commercial Model` |
| Contracted rate | text | not in the schema: `Contracted Rate` |
| Minimum guarantee | text | not in the schema: `Minimum Guarantee` |
| Guarantee period | text | not in the schema: `Guarantee Period` |
| Billing cycle | text | not in the schema: `Billing Cycle` |
| Contract duration | text | not in the schema: `Contract Duration` |
| Renewal | text | not in the schema: `Renewal` |
| Payment terms | text | not in the schema: `Payment Terms` |

**Where the user goes next**

- → `ADM-409` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial agreement billable list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial agreement billable untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial agreement billable yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial agreement billable are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `SGN-023`: Twin.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every commercial agreement billable:
- Commercial Model: 128
  Contracted Rate: 94%
  Minimum Guarantee: AED 12,400.00
  Guarantee Period: AED 96,750.00
  Billing Cycle: AED 96,750.00
  Contract Duration: 1.8 s
  Renewal: 11
  Payment Terms: 233
- Commercial Model: 46
  Contracted Rate: 87%
  Minimum Guarantee: AED 482,300.00
  Guarantee Period: AED 12,400.00
  Billing Cycle: AED 12,400.00
  Contract Duration: 3 h 20 min
  Renewal: 128
  Payment Terms: 57
- Commercial Model: 312
  Contracted Rate: 71%
  Minimum Guarantee: AED 96,750.00
  Guarantee Period: AED 482,300.00
  Billing Cycle: AED 482,300.00
  Contract Duration: 42 min
  Renewal: 46
  Payment Terms: 11
```

#### Permissions

- `setAgreementContractTerm` → `PLATFORM_CELL_MANAGE` (configure) · partner, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-415` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-415`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 5
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 12: Works in Commercial Agreement, Billable Definition & Customer Acceptance → This becomes one of the most important revised screens. The customer must understand and formally accept what TICVAI considers billable.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-415?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-409`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-416` Payment, Contract & Commercial Validation

**Perform final checks before creating the active subscription.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29328 (APP-CONSOLE-ADM-416) |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/payment-contract-commercial-validation-adm-416` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Final checks (payment method, contract, commercial validity) before the subscription is created.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-409` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The payment contract commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the payment contract commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No payment contract commercial yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the payment contract commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
checks:
  paymentMethod: verified
  contractSigned: true
  creditCheck: passed
```

#### Permissions

- `simulateCommercialPackage` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-416` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-416`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 5
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 14: Works in Payment, Contract & Commercial Validation → Perform final checks before creating the active subscription.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-416?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-409`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-417` Subscription Confirmation & Commercial Activation

**Create the formal active subscription/contract record after successful validation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29329 (APP-CONSOLE-ADM-417) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/subscription-confirmation-commercial-activation-adm-417` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Create the active subscription (twin of SGN-024).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save subscription (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-409` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscription confirmation commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscription confirmation commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscription confirmation commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the subscription confirmation commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Downgrade conflicts with current usage. The response names every module and limit that would be violated. (DowngradeConflictProblem); 422 `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed` … |

#### Edge cases to draw

- **setSubscription answers 409**: Show it as something the person can act on, not a failure: Downgrade conflicts with current usage. The response names every module and limit that would be violated. Or the subscription is `expired` and cannot be reactivated (`subscription-expired`, audit STATE-SUBSCRIPTION); start a new one. *(source: contracts/satellite/subscription.yaml#setSubscription)*
- **setSubscription answers 422**: Show it as something the person can act on, not a failure: `effectiveFrom` was sent and is not the date the change must take effect: today for an upgrade, the next renewal for a downgrade (`effective-date-not-allowed`, audit R214 (1)). Or the plan is a custom package private to another tenant (`plan-not-offered`, decided 29 September). *(source: contracts/satellite/subscription.yaml#setSubscription)*

#### Consistency with other screens

- Match `SGN-024`: Twin.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
subscription: Enterprise v1
starts: 01/11/2026
renews: 01/11/2027
firstInvoice: 01/12/2026
```

#### Permissions

- `setSubscription` → `PLATFORM_TENANT_MANAGE` (configure) · staff, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.2.2 | Monthly Billing - System shall support monthly subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |
| 20.2.3 | Annual Billing - System shall support annual subscriptions. | Subscription & Licensing Management | CONTRACTED | `setSubscription` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-417` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-417`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 5
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 16: Works in Subscription Confirmation & Commercial Activation → Create the formal active subscription/contract record after successful validation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-417?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save subscription, Cancel.
- [ ] Every transition is wired: `ADM-409`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-418` Subscription Lifecycle & Trial-to-Paid Handoff

**Manage the immediate commercial lifecycle after purchase or trial activation and ensure clean handoff to operational provisioning. Automatically provision the customer's TICVAI tenant, organization, venue structure, administrator, licensed modules, entitlements, quotas, security baseline and venue template after subscription/trial activation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · ticket #29332 (APP-CONSOLE-ADM-418) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show; Track) and no metric row |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/subscription-lifecycle-trial-to-paid-handoff-adm-418` |

**What the spec says about it.** Retry, investigate, assign and escalate are four row actions on a stuck conversion; they need an operation each (none exists yet).

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Retry / Investigate / Assign / Escalate, Revised Board 5 — Commercial Model Behavior. Each needs an … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The commercial lifecycle right after purchase or trial, and the handoff to provisioning; stuck handoffs retried or escalated.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 14 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): One button labelled "Retry / Investigate / Assign / Escalate" and one labelled "Revised Board 5 — Commercial Model Behavior". (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every subscription lifecycle trial-to-paid** (data table)

| Shows | Format | Notes |
|---|---|---|
| Trial usage | text | not in the schema: `Trial Usage` |
| Trial ticket volume | text | not in the schema: `Trial Ticket Volume` |
| Trial expiry | text | not in the schema: `Trial Expiry` |
| Conversion package | text | not in the schema: `Conversion Package` |
| Commercial model | text | not in the schema: `Commercial Model` |
| Paid start date | text | not in the schema: `Paid Start Date` |
| First billing date | text | not in the schema: `First Billing Date` |
| Package approval | text | not in the schema: `Package Approval` |
| Customer acceptance | text | not in the schema: `Customer Acceptance` |
| Payment | text | not in the schema: `Payment` |
| Subscription creation | text | not in the schema: `Subscription Creation` |
| Commercial activation | text | not in the schema: `Commercial Activation` |
| License request | text | not in the schema: `License Request` |
| Provisioning request | text | not in the schema: `Provisioning Request` |

**The selected subscription lifecycle trial-to-paid** (detail panel): The pack groups this record's detail under its own headings: “Draft”, “Tier-Based Fixed recurring subscription”, “Fixed Fixed contractual value”, “For example”, “The key principle is”, “Board Flow”.

| Shows | Format | Notes |
|---|---|---|
| Trial usage | text | not in the schema: `Trial Usage` |
| Trial ticket volume | text | not in the schema: `Trial Ticket Volume` |
| Trial expiry | text | not in the schema: `Trial Expiry` |
| Conversion package | text | not in the schema: `Conversion Package` |
| Commercial model | text | not in the schema: `Commercial Model` |
| Paid start date | text | not in the schema: `Paid Start Date` |
| First billing date | text | not in the schema: `First Billing Date` |
| Package approval | text | not in the schema: `Package Approval` |
| Customer acceptance | text | not in the schema: `Customer Acceptance` |
| Payment | text | not in the schema: `Payment` |
| Subscription creation | text | not in the schema: `Subscription Creation` |
| Commercial activation | text | not in the schema: `Commercial Activation` |
| License request | text | not in the schema: `License Request` |
| Provisioning request | text | not in the schema: `Provisioning Request` |

**Data it reads**: `getSubscription` (onLoad, Confirmation)

**Where the user goes next**

- → `ADM-409` Purchase / Trial Journey Selection: *Back to Purchase / Trial Journey Selection*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscription lifecycle trial-to-paid list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscription lifecycle trial-to-paid untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscription lifecycle trial-to-paid yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the subscription lifecycle trial-to-paid are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every subscription lifecycle trial-to-paid:
- Trial Usage: 1.8 s
  Trial Ticket Volume: 74
  Trial Expiry: 19
  Conversion Package: 3 h 20 min
  Commercial Model: 128
  Paid Start Date: 01/10/2026 09:14
  First Billing Date: 01/10/2026 09:14
  Package Approval: 42 min
- Trial Usage: 3 h 20 min
  Trial Ticket Volume: 19
  Trial Expiry: 233
  Conversion Package: 42 min
  Commercial Model: 46
  Paid Start Date: 30/09/2026 18:02
  First Billing Date: 30/09/2026 18:02
  Package Approval: 1.8 s
- Trial Usage: 42 min
  Trial Ticket Volume: 233
  Trial Expiry: 57
  Conversion Package: 1.8 s
  Commercial Model: 312
  Paid Start Date: 28/09/2026 11:45
  First Billing Date: 28/09/2026 11:45
  Package Approval: 3 h 20 min
```

#### Permissions

- `getSubscription` → `PLATFORM_TENANT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-418` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS157 Subscription Licensing AI Self Service Board 5.dc.html#adm-418`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 5
- Flow F211 *Subscription Licensing AI Self Service board 5: Purchase / Trial Journey …*, step 18: Works in Subscription Lifecycle & Trial-to-Paid Handoff → Manage the immediate commercial lifecycle after purchase or trial activation and ensure clean handoff to operational provisioning.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-418?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-409`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
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

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createLegalEntity": {"method":"POST","path":"/legal-entities","contract":"finance","summary":"Create a legal entity","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LegalEntity","responds":"LegalEntity"},
"getBillingEntity": {"method":"GET","path":"/tenants/{tenantId}/billing-entity","contract":"subscription","summary":"The company TICVAI invoices for a tenant","permission":"PLATFORM_BILLING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"BillingEntity"},
"getSubscription": {"method":"GET","path":"/tenants/{tenantId}/subscription","contract":"subscription","summary":"Read the current subscription","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"Subscription"},
"listOrgUnits": {"method":"GET","path":"/org-units","contract":"tenancy","summary":"List scope nodes visible to the session","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"under","in":"query","required":null},{"name":"level","in":"query","required":null},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPaymentProviders": {"method":"GET","path":"/payment-providers","contract":"orders","summary":"Gateways configured for this scope","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"previewSubscriptionChange": {"method":"POST","path":"/tenants/{tenantId}/subscription/preview","contract":"subscription","summary":"Preview the effect of a plan change","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetSubscriptionRequest","responds":"SubscriptionPreview"},
"setAgreementContractTerm": {"method":"PUT","path":"/agreement-contract-term","contract":"subscription","summary":"Agreement & Contract Terms Builder","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AgreementContractTermsBuilderInput","responds":"AgreementContractTermsBuilderView"},
"setBillingEntity": {"method":"PUT","path":"/tenants/{tenantId}/billing-entity","contract":"subscription","summary":"Set the company TICVAI invoices for a tenant","permission":"PLATFORM_BILLING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BillingEntity","responds":"BillingEntity"},
"setPaymentProvider": {"method":"PUT","path":"/payment-providers","contract":"orders","summary":"Configure a gateway and its routing","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"SetPaymentProviderRequest","responds":"PaymentProvider"},
"setSubscription": {"method":"PUT","path":"/tenants/{tenantId}/subscription","contract":"subscription","summary":"Assign or change a subscription","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SetSubscriptionRequest","responds":"Subscription"},
"setTrialConfiguration": {"method":"PUT","path":"/trial-configurations","contract":"subscription","summary":"What a trial includes, how long it lasts and how it converts","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TrialConfiguration","responds":"TrialConfiguration"},
"simulateCommercialPackage": {"method":"POST","path":"/package-simulations","contract":"subscription","summary":"What this package would cost, and what it would provision","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PackageSimulationRequest","responds":"PackageSimulation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AgreementContractTermsBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; stored as control.partner_agreement (PartnerAgreement), a new version per amendment; documents are control.partner_document rows with agreementId; legalEntity, commercialOwner and financeOwner land in legalEntityId, commercialOwnerPrincipalId and financeOwnerPrincipalId (data model DM4)","description":"**What Agreement & Contract Terms Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"agreementId":{"type":"string","format":"uuid","description":"Agreement ID; omit to create"},"agreementName":{"type":"string","description":"Agreement Name"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"agreementType":{"type":"string","description":"Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"},"contractReference":{"type":"string","description":"Contract Reference"},"legalEntity":{"type":"string","description":"Legal Entity"},"brandId":{"type":"string","description":"Brand id","nullable":true},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Venues the agreement covers"},"territory":{"type":"string","description":"Territory"},"settlementCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Settlement currency, ISO 4217"},"validFrom":{"type":"string","format":"date","description":"Effective From"},"validTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"renewalType":{"type":"string","enum":["manual","auto"],"description":"Renewal Type"},"commercialOwner":{"type":"string","description":"Commercial Owner: staff principal id"},"financeOwner":{"type":"string","description":"Finance Owner: staff principal id"},"creditTermDays":{"type":"integer","description":"Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)"},"commissionTerms":{"type":"string","description":"Commission Terms: summary or reference to the commission rules (listCommissionMarginIncentive)","nullable":true},"pricingBasis":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"description":"Pricing Basis (pack p.27 pricing models)"},"creditTerms":{"type":"string","description":"Credit Terms","nullable":true},"allocationTerms":{"type":"string","description":"Allocation Terms","nullable":true},"cancellationConditions":{"type":"string","description":"Cancellation Conditions","nullable":true},"bookingRestrictions":{"type":"string","description":"Booking Restrictions","nullable":true},"settlementTerms":{"type":"string","description":"Settlement Terms","nullable":true},"minimumCommitment":{"type":"integer","description":"Minimum Commitment: tickets over the agreement term","nullable":true},"salesTarget":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sales Target over the agreement term"},"renewalNoticeDays":{"type":"integer","description":"Renewal Notice Period in days","nullable":true},"renegotiationRequired":{"type":"boolean","description":"Renegotiation Required"},"renewalRequiresApproval":{"type":"boolean","description":"Renewal Approval: renewal needs approval"},"rateMode":{"$ref":"#/components/schemas/PartnerRateMode","description":"Net rate or commission, as on PartnerAgreement"},"paymentModel":{"type":"string","enum":["creditAccount","prepaid","payPerTransaction"],"description":"Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"},"refundConditions":{"type":"string","description":"Refund Conditions (pack p.26)","nullable":true},"agreementValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Agreement value (MoM 31 Aug 4.4: each agreement captures term/value)"},"documents":{"type":"array","description":"Document Association","items":{"type":"object","properties":{"documentType":{"type":"string","enum":["signedContract","addendum","rateSheet","sla","nda","commercialAnnex"]},"documentId":{"type":"string","format":"uuid"}}}}}},
"AgreementContractTermsBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over control.partner_agreement and control.partner_document and the existing subscription state, assembled at read time (data model DM4)","description":"**What Agreement & Contract Terms Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"agreementId":{"type":"string","format":"uuid","description":"Agreement ID; omit to create"},"agreementName":{"type":"string","description":"Agreement Name"},"partnerId":{"type":"string","format":"uuid","description":"Partner"},"agreementType":{"type":"string","description":"Agreement Type code, seeded with reseller, ota, travelTrade, corporate, wholesale, affiliate, distribution, apiCommercial (pack p.26)"},"contractReference":{"type":"string","description":"Contract Reference"},"legalEntity":{"type":"string","description":"Legal Entity"},"brandId":{"type":"string","description":"Brand id","nullable":true},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Venues the agreement covers"},"territory":{"type":"string","description":"Territory"},"settlementCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"Settlement currency, ISO 4217"},"validFrom":{"type":"string","format":"date","description":"Effective From"},"validTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"renewalType":{"type":"string","enum":["manual","auto"],"description":"Renewal Type"},"commercialOwner":{"type":"string","description":"Commercial Owner: staff principal id"},"financeOwner":{"type":"string","description":"Finance Owner: staff principal id"},"creditTermDays":{"type":"integer","description":"Payment Terms in days (0 = due immediately; Net 7/15/30/45 or custom)"},"commissionTerms":{"type":"string","description":"Commission Terms: summary or reference to the commission rules (listCommissionMarginIncentive)","nullable":true},"pricingBasis":{"type":"string","enum":["retailPrice","netRate","discountFromRetail","markup","derivedRate"],"description":"Pricing Basis (pack p.27 pricing models)"},"creditTerms":{"type":"string","description":"Credit Terms","nullable":true},"allocationTerms":{"type":"string","description":"Allocation Terms","nullable":true},"cancellationConditions":{"type":"string","description":"Cancellation Conditions","nullable":true},"bookingRestrictions":{"type":"string","description":"Booking Restrictions","nullable":true},"settlementTerms":{"type":"string","description":"Settlement Terms","nullable":true},"minimumCommitment":{"type":"integer","description":"Minimum Commitment: tickets over the agreement term","nullable":true},"salesTarget":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Sales Target over the agreement term"},"renewalNoticeDays":{"type":"integer","description":"Renewal Notice Period in days","nullable":true},"renegotiationRequired":{"type":"boolean","description":"Renegotiation Required"},"renewalRequiresApproval":{"type":"boolean","description":"Renewal Approval: renewal needs approval"},"rateMode":{"$ref":"#/components/schemas/PartnerRateMode","description":"Net rate or commission, as on PartnerAgreement"},"paymentModel":{"type":"string","enum":["creditAccount","prepaid","payPerTransaction"],"description":"Payment model, the three confirmed at MoM 5 Aug and MoM 31 Aug 4.4: creditAccount (sells to an approved credit ceiling, invoiced periodically), prepaid (pre-funded wallet drawn down per sale) or payPerTransaction (card at each sale)"},"refundConditions":{"type":"string","description":"Refund Conditions (pack p.26)","nullable":true},"agreementValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Agreement value (MoM 31 Aug 4.4: each agreement captures term/value)"},"documents":{"type":"array","description":"Document Association","items":{"type":"object","properties":{"documentType":{"type":"string","enum":["signedContract","addendum","rateSheet","sla","nda","commercialAnnex"]},"documentId":{"type":"string","format":"uuid"}}}},"version":{"type":"integer","description":"Agreement version; amendments create a new one"},"status":{"$ref":"#/components/schemas/PartnerAgreementStatus","description":"Agreement status"}}},
"BillingEntity": {"type":"object","x-ticvai-persistence":"control.billing_entity","description":"**The company TICVAI invoices for a tenant, with its trade licence and VAT certificate** (Chinmay, 2 October, workbook Q209: \"a new billing-entity record in the subscription contract\"; DI-830; CHG-CSA-030). One per tenant, mastered in the control plane. `legalName` and `countryCode` are required on save (400 otherwise); they are not marked required here so the record can ride, optional, on an onboarding application. **Documents** (workbook Q210, the default): a trade licence always; a VAT certificate when a `trn` is entered. Which documents a country requires is configurable per country (tenancy `RegionSettings`); the default is that rule.","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"tenantId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null while it rides on an onboarding application."},"legalName":{"type":"string","maxLength":300},"tradeLicenceNumber":{"type":"string","maxLength":100,"nullable":true},"trn":{"type":"string","maxLength":30,"nullable":true,"description":"The tax registration number; entering one makes the VAT certificate required."},"countryCode":{"type":"string","minLength":2,"maxLength":2},"address":{"type":"string","maxLength":1000,"nullable":true},"invoiceEmail":{"type":"string","format":"email","nullable":true},"documents":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"The trade licence and, where a TRN is entered, the VAT certificate, each a stored file with its verification.","items":{"type":"object","properties":{"documentType":{"type":"string","enum":["tradeLicence","vatCertificate"]},"fileRef":{"type":"string","nullable":true},"expiryDate":{"type":"string","format":"date","nullable":true},"verificationStatus":{"type":"string","enum":["missing","uploaded","verified","rejected","expired"]}}}},"missingDocuments":{"type":"array","readOnly":true,"description":"The documents the country's rule requires that are not yet uploaded and verified.","items":{"type":"string"}},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CellTier": {"type":"string","enum":["shared","dedicated","isolated","clientHosted"]},
"DowngradeConflictProblem": {"x-ticvai-persistence":"none — error shape","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Problem"},{"type":"object","properties":{"modulesInUse":{"type":"array","description":"Enabled by the tenant but not licensed by the target plan.","items":{"type":"object","properties":{"moduleKey":{"type":"string"},"displayName":{"type":"string"},"isEnabled":{"type":"boolean"}}}},"limitsExceeded":{"type":"array","items":{"type":"object","properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"currentUsage":{"type":"integer"},"targetLimit":{"type":"integer"}}}}}}]},
"LegalEntity": {"x-ticvai-persistence":"ledger.legal_entity","type":"object","description":"Also the `createLegalEntity` body. **`id` and `scopePath` are server-owned** (`readOnly`) and ignored if sent.\n","required":["id","code","name","countryCode","currency","currencyScale","fiscalYearStartMonth"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"taxRegistrationNumber":{"type":"string","nullable":true},"fiscalYearStartMonth":{"type":"integer","minimum":1,"maximum":12},"regionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/tenancy::ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"PackageSimulation": {"type":"object","description":"Boards 3.9 and 4.8. **Refused at quote time rather than at go-live.**","properties":{"lines":{"type":"array","items":{"type":"object","properties":{"kind":{"type":"string","enum":["baseTier","module","addOn","capacityPack","overage","professionalServices","discount"]},"label":{"type":"string"},"quantity":{"type":"number","nullable":true},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"recurringTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"oneOffTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"contractTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"minimumGuarantee":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"findings":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string","enum":["blocking","warning","advisory"]},"code":{"type":"string"},"message":{"type":"string"}}}},"provisionable":{"type":"boolean"}}},
"PackageSimulationRequest": {"type":"object","required":["tierCode"],"properties":{"tierCode":{"type":"string"},"licensingModelId":{"type":"string","format":"uuid","nullable":true},"moduleCodes":{"type":"array","items":{"type":"string"}},"venueCount":{"type":"integer","default":1},"projectedVolumes":{"type":"object","additionalProperties":{"type":"integer"}},"contractMonths":{"type":"integer","default":12},"billingCycle":{"type":"string","nullable":true},"currency":{"type":"string","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PartnerAgreementStatus": {"type":"string","enum":["pendingApproval","active","expiringSoon","expired","suspended","terminated"]},
"PartnerRateMode": {"type":"string","description":"**Alternatives, not both.** A partner buys at a net rate and keeps the margin, or sells at face value and is paid commission. Both is being paid twice for the same sale.\n","enum":["netRate","commission"]},
"PaymentProvider": {"type":"object","x-ticvai-persistence":"payments.provider","description":"BL-116, CF-131. **`Payment` carried `providerName` and `providerReference`, which records a provider and does not abstract one.**\nTwo gateways are confirmed for Phase 1 — **Network International and Stripe** — and that is exactly the number that forces this: **one gateway can be hard-coded and two cannot.**\nCredentials live in the vault and never here, following `ai.AiProvider` (ADR-0020's rule applied outside AI): **no surface ever holds a provider key.**\n","required":["id","name","kind","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["networkInternational","stripe","adyen","checkout","cash","wallet","other"]},"supportedMethods":{"type":"array","items":{"type":"string","enum":["card","applePay","googlePay","samsungPay","wallet","bankTransfer","cash","bnpl"]}},"supportedCurrencies":{"type":"array","items":{"type":"string"}},"supportsTokenisation":{"type":"boolean","description":"**The keystone.** Recurring billing, wallet auto-reload, one-click checkout and payment links all require a stored credential, and none of them can be designed until this is answered per provider.\n"},"supportsPartialCapture":{"type":"boolean","default":true},"acceptedOnChannels":{"type":"array","description":"BL-115. **Which channels may use this provider.** A kiosk taking cash and a website taking cards is not a policy either could infer, and a venue that accepts cash at a till and not online had no way to say so.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}},"presentmentCurrencies":{"type":"array","description":"BL-070. **What a storefront may quote in**, distinct from what it settles in. A guest sees GBP and the venue books AED — the display currency is the provider's capability and the settlement currency is the venue's (CF-114 on multi-currency).\n","items":{"type":"string"}},"supports3ds":{"type":"boolean","default":true},"terminal":{"type":"object","nullable":true,"description":"BL-119. **Terminal behaviour, where this provider drives a physical device.** Unstated until now, and every field here is one a certification body asks about.\n","properties":{"emvCertificationRef":{"type":"string","nullable":true},"offlineFloorLimit":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What a terminal may approve with no connection.** Above it the sale waits; below it the venue carries the risk knowingly — and a floor limit of zero means a till stops when the line does.\n"},"supportsOfflineApproval":{"type":"boolean","default":false},"receiptSignatureRequired":{"type":"boolean","default":false},"supportsTipOnTerminal":{"type":"boolean","default":false}}},"credentialRef":{"type":"string","writeOnly":true,"description":"A vault reference. **Never the credential**, never returned, and rotated without a contract change.\n"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string"},"isActive":{"type":"boolean"}}},
"PaymentRouting": {"type":"object","x-ticvai-persistence":"payments.routing_rule","description":"**Which provider takes a given payment, and why.** With two gateways the question is live from day one: a UAE card may cost less through one and an international card less through the other.\n**Ordered rules, first match wins, and a fallback that is not optional.** A gateway outage with no fallback is a venue that cannot sell.\n","required":["id","priority","providerId"],"properties":{"id":{"type":"string","format":"uuid"},"priority":{"type":"integer"},"providerId":{"type":"string","format":"uuid"},"conditions":{"type":"object","description":"**Match on what is known before the charge** — channel, currency, method, issuer country, amount band. Not on anything that requires asking the provider first.\n","properties":{"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"currency":{"type":"string","nullable":true,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"method":{"type":"string","nullable":true},"issuerCountry":{"type":"string","nullable":true},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"fallbackProviderId":{"type":"string","format":"uuid","nullable":true,"description":"**Where this provider declines or is unreachable.** A decline is not always a fallback case — an insufficient-funds decline should not be retried elsewhere, and a gateway timeout should.\n"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"SetPaymentProviderRequest": {"x-ticvai-persistence":"none — request only; the provider lands in payments.provider and its rules in payments.routing_rule","description":"Request only. **A provider and the rules that route to it**, because `setPaymentProvider` is *\"configure a gateway and its routing\"* and writes both tables — and the provider schema alone carried no routing field, so the routing half had nothing to arrive in.\n","allOf":[{"$ref":"#/components/schemas/PaymentProvider"},{"type":"object","properties":{"routing":{"type":"array","description":"The ordered rules that send payments to this provider. `providerId` on each is this provider's `id`.","items":{"$ref":"#/components/schemas/PaymentRouting"}}}}]},
"SetSubscriptionRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["planId"],"properties":{"planId":{"type":"string","format":"uuid"},"planVersion":{"type":"string","description":"Defaults to the current version."},"effectiveFrom":{"type":"string","format":"date","description":"Optional, and set by the server if omitted. Today for an upgrade, `renewsAt` for a downgrade; any other date is refused (audit R214 (1))."},"prorate":{"type":"boolean","default":true,"description":"An upgrade is always prorated and a downgrade, which starts at renewal, never is (audit R214 (1)). Kept so a preview can show the unprorated figure; `setSubscription` applies the rule whatever is sent."},"note":{"type":"string","maxLength":500}}},
"Subscription": {"x-ticvai-persistence":"subscription.contract","type":"object","required":["tenantId","planId","planVersion","status","startsAt"],"properties":{"tenantId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid"},"planName":{"type":"string"},"planVersion":{"type":"string"},"status":{"type":"string","enum":["trial","active","pastDue","cancelled","expired"]},"startsAt":{"type":"string","format":"date"},"renewsAt":{"type":"string","format":"date","nullable":true},"cancelledAt":{"type":"string","format":"date","nullable":true},"scheduledChange":{"type":"object","nullable":true,"readOnly":true,"description":"A downgrade waiting for the next renewal (decided 28 September, audit R214 (1)). Null when none is scheduled.","properties":{"planId":{"type":"string","format":"uuid"},"planVersion":{"type":"string"},"effectiveFrom":{"type":"string","format":"date","description":"Always the `renewsAt` it was scheduled against."}}},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"billingPeriod":{"type":"string"}}},
"SubscriptionPreview": {"x-ticvai-persistence":"none — computed","type":"object","required":["canApply","priceChange"],"properties":{"canApply":{"type":"boolean"},"priceChange":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"proratedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"modulesGained":{"type":"array","items":{"type":"string"}},"modulesLost":{"type":"array","items":{"type":"string"}},"conflicts":{"$ref":"#/components/schemas/DowngradeConflictProblem"},"cellTierChange":{"type":"object","nullable":true,"properties":{"from":{"$ref":"#/components/schemas/CellTier"},"to":{"$ref":"#/components/schemas/CellTier"},"requiresMigration":{"type":"boolean"}}}}},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/subscription::LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]},
"TrialConfiguration": {"type":"object","x-ticvai-persistence":"subscription.trial_config","description":"Board 5.5. **A trial that expires with no conversion path is a tenant full of real data nobody can bill.**\n","properties":{"id":{"type":"string","format":"uuid"},"tierCode":{"type":"string","nullable":true},"durationDays":{"type":"integer","default":30},"includedModules":{"type":"array","items":{"type":"string"}},"usageCaps":{"type":"object","additionalProperties":{"type":"integer"}},"paymentMethodRequiredUpFront":{"type":"boolean","default":false},"conversionOfferPercent":{"type":"number","nullable":true},"noticeDaysBeforeExpiry":{"type":"array","items":{"type":"integer"}},"onExpiry":{"type":"string","enum":["suspend","convert","decommission"],"default":"suspend","description":"**Suspension is the humane default.** Customers routinely let a trial lapse and come back a week later.\n"},"retainDataDays":{"type":"integer","default":90}}}
}
```
