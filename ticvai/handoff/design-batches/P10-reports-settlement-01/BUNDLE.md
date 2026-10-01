# P10-reports-settlement-01 — P10 · Reports & Settlement

**3 screens · 14 operations · 22 schemas · 4 permissions**

Platform P10 Partner Web · ships as **ticvai-control** ·
partner audience · web ·
online only

## Who this is for

**partner on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `REPORT_MANAGE, REPORT_VIEW_VENUE, SETTLEMENT_RECONCILE, SETTLEMENT_VIEW`. A control nobody can use must say so,
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

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `PTR-014` | Settlement & Payment History | B–D | 12 | 39 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `PTR-017` | Commission Statement | B–D | 2 | 39 | 6 | 17 | 0 | 0 | — | notStarted (generated) |
| `PTR-018` | Reports & Sales Performance | B–D | 64 | 35 | 6 | 93 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `PTR-014` Settlement & Payment History

**Take the money, and be unambiguous about whether it worked.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Reports & Settlement · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `SETTLEMENT_RECONCILE`, `SETTLEMENT_VIEW` (1 operate, 1 read); in the flows as finance controller |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listSettlements` reads the population and `getSettlement` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `settlementId` (deepLink) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/general/settlement-and-payment-history` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Provider name | text field | optional | — | — | — | Sends `?providerName=` to `listSettlements`. | `listSettlements` ?providerName |
| Status | select | optional | — | Ingesting · Parsing · Matching · Matched · Has exceptions · Resolved · Failed | — | Sends `?status=` to `listSettlements`. | `listSettlements` ?status |

**Form: Ingest settlement file** (modal, opened by *Ingest settlement file*; *Ingest settlement file* calls `ingestSettlementFile`, *Cancel* sends nothing)

**Collects what `ingestSettlementFile` sends before it is called.** Required: `providerName`, `periodStart`, `periodEnd`, `fileReference`. Optional: `format`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Provider name `providerName` | text field | required | — | — | — | — | `ingestSettlementFile` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | The venue this day of settlement is for (audit R110 (b)). | `ingestSettlementFile` body |
| Period start `periodStart` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | A day in the region's time zone, local midnight to local midnight. | `ingestSettlementFile` body |
| Period end `periodEnd` | date picker | required | — | — | 1 Oct 2026 (dd MMM yyyy) | A day in the region's time zone, local midnight to local midnight. | `ingestSettlementFile` body |
| File reference `fileReference` | picker: choose a file reference | required | — | That upload route is staff-only and needs `ASSET_LIBRARY_MANAGE`; a partner caller has no upload route yet. | shows names, sends the id | The `id` of the `MediaAsset` holding the file, uploaded first through `assets.createUpload` then `assets.completeUpload` (direct to object storage through a signed URL). | `ingestSettlementFile` body |
| Format `format` | radio group | optional | — | Csv · Fixed width · Xml · Json | — | — | `ingestSettlementFile` body |

Errors to draw in the form: 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)).

**Form: Resolve settlement exception** (modal, opened by *Resolve settlement exception*; *Resolve settlement exception* calls `resolveSettlementException`, *Cancel* sends nothing)

**Collects what `resolveSettlementException` sends before it is called.** Required: `exceptionId`, `resolution`, `note`. Optional: `matchedPaymentId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Exception `exceptionId` | picker: choose an exception | required | — | — | shows names, sends the id | — | `resolveSettlementException` body |
| Resolution `resolution` | radio group | required | — | Matched manually · Write off · Dispute raised · Provider error · Timing difference | — | How a settlement exception was explained. One vocabulary for the request and the stored exception. | `resolveSettlementException` body |
| Matched payment `matchedPaymentId` | picker: choose a matched payment | optional | — | — | shows names, sends the id | — | `resolveSettlementException` body |
| Note `note` | text area | required | — | min length 3; max length 1000 | — | — | `resolveSettlementException` body |

Errors to draw in the form: 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 404 The settlement, or an exception with this `exceptionId` under it, does not exist or is outside the caller's scope.; 409 The exception is already resolved.

#### Outputs: what the screen shows and produces

**Shown**

**Every settlement** (data table, from `listSettlements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Provider name | text | — |
| Period start | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Period end | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Status | chip: Ingesting, Parsing, Matching, Matched, Has exceptions, Resolved… | — |
| Line count | 1,234 | — |
| Matched count | 1,234 | — |
| Exception count | 1,234 | — |
| Provider gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Provider fees | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Provider net | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Ledger gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Every settlement exception** (data table, from `listSettlementExceptions`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Server-created when parsing finds the exception, so a UUID (naming-and-style 4). |
| Settlement | the name it points at, never the id | — |
| Kind | chip: Unmatched in provider, Unmatched in ledger, Amount mismatch, Duplicate in provider … | — |
| Provider reference | text | — |
| Payment | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Expected amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Resolution | chip: Matched manually, Write off, Dispute raised, Provider error, Timing difference | Null while the exception is open. |
| Note | text | The `note` given to `resolveSettlementException`, stored with the resolution. |
| Resolved by principal | the name it points at, never the id | — |
| Resolved at | 1 Oct 2026, 14:30 | — |

**The selected settlement** (detail panel, from `getSettlement`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Provider name | text | — |
| Period start | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Period end | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Status | chip: Ingesting, Parsing, Matching, Matched, Has exceptions, Resolved… | — |
| Line count | 1,234 | — |
| Matched count | 1,234 | — |
| Exception count | 1,234 | — |
| Provider gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Provider fees | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Provider net | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Ledger gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Difference | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Ingested at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Ingest settlement file (primary button) | `ingestSettlementFile` POST `/settlements` | inline | Settlement | 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)). | opens modal first |
| Resolve settlement exception (secondary button) | `resolveSettlementException` POST `/settlements/{settlementId}/exceptions` | inline | SettlementException | 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 404 The settlement, or an exception with this `exceptionId` under it, does not exist or is outside the … | opens modal first |

**Data it reads**: `listSettlements` (onLoad, from page inventory)

**Where the user goes next**

- → `PTR-003` Profile & Company Details: *Profile & Company Details*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The settlement payment history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the settlement payment history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No settlement payment history yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on providerName, status and the settlement payment history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SETTLEMENT_VIEW`, which `listSettlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 `fileReference` names no completed upload in the caller's scope, or the period is not a single day (`settlement-period-not-a-day`, audit R110 (b)).; 400 `matchedManually` without a `matchedPaymentId`, or one that names no payment. `errors[]` names the field.; 409 The exception is already resolved. |

#### Permissions

- `listSettlements` → `SETTLEMENT_VIEW` (read) · staff, partner
- `getSettlement` → `SETTLEMENT_VIEW` (read) · staff, partner
- `ingestSettlementFile` → `SETTLEMENT_RECONCILE` (operate) · staff, partner
- `listSettlementExceptions` → `SETTLEMENT_VIEW` (read) · staff, partner
- `resolveSettlementException` → `SETTLEMENT_RECONCILE` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `SETTLEMENT_VIEW`, which `listSettlements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-014` · status **notStarted** · provenance generated
- Flow F99 *A chargeback arrives and is defended*, step 3: Settlement & Payment History. → 5 operations, 5 of them previously unwalked.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (39 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Ingest settlement file, Resolve settlement exception.
- [ ] Every transition is wired: `PTR-003`.
- [ ] Every gated control is gated: `SETTLEMENT_RECONCILE`, `SETTLEMENT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-017` Commission Statement

**Answer a question about commission with numbers someone can check.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Reports & Settlement · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listPartnerAgreements` reads the population and `getCommissionStatement` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `agreementId` (deepLink) · cold entry: **A partner link resolves within that partner's own scope and refuses outside it.** A forwarded link between partners must not open another partner's record. … |
| Route | `/general/commission-statement` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.**  Open: No contract — commission not modelled

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Expiring within days | number field | — | — | — | — | Sends `?expiringWithinDays=` to `listPartnerAgreements`. | `listPartnerAgreements` ?expiringWithinDays |
| Status | text field | — | — | — | — | Sends `?status=` to `listPartnerAgreements`. | `listPartnerAgreements` ?status |

#### Outputs: what the screen shows and produces

**Shown**

**Every partner agreement** (data table, from `listPartnerAgreements`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `PartnerAgreement.id` |
| Partner ID | text | not in the schema: `PartnerAgreement.partnerId` |
| Partner name | text | not in the schema: `PartnerAgreement.partnerName` |
| Status | text | not in the schema: `PartnerAgreement.status` |
| Rate mode | text | not in the schema: `PartnerAgreement.rateMode` |
| Commission percent | text | not in the schema: `PartnerAgreement.commissionPercent` |
| Volume tiers | text | not in the schema: `PartnerAgreement.volumeTiers` |
| Volume window | text | not in the schema: `PartnerAgreement.volumeWindow` |
| Seasonal rates | text | not in the schema: `PartnerAgreement.seasonalRates` |
| Segment tier | text | not in the schema: `PartnerAgreement.segmentTier` |
| Branding asset ID | text | not in the schema: `PartnerAgreement.brandingAssetId` |
| Storefront subdomain | text | not in the schema: `PartnerAgreement.storefrontSubdomain` |

**The selected partner agreement** (detail panel, from `listPartnerAgreements`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | not in the schema: `PartnerAgreement.id` |
| Partner ID | text | not in the schema: `PartnerAgreement.partnerId` |
| Partner name | text | not in the schema: `PartnerAgreement.partnerName` |
| Status | text | not in the schema: `PartnerAgreement.status` |
| Rate mode | text | not in the schema: `PartnerAgreement.rateMode` |
| Commission percent | text | not in the schema: `PartnerAgreement.commissionPercent` |
| Volume tiers | text | not in the schema: `PartnerAgreement.volumeTiers` |
| Volume window | text | not in the schema: `PartnerAgreement.volumeWindow` |
| Seasonal rates | text | not in the schema: `PartnerAgreement.seasonalRates` |
| Segment tier | text | not in the schema: `PartnerAgreement.segmentTier` |
| Branding asset ID | text | not in the schema: `PartnerAgreement.brandingAssetId` |
| Storefront subdomain | text | not in the schema: `PartnerAgreement.storefrontSubdomain` |
| Sponsorship | text | not in the schema: `PartnerAgreement.sponsorship` |
| Net rates | text | not in the schema: `PartnerAgreement.netRates` |
| Credit term days | text | not in the schema: `PartnerAgreement.creditTermDays` |
| Accepted by principal ID | text | not in the schema: `PartnerAgreement.acceptedByPrincipalId` |

**The commission statement** (detail panel, from `getCommissionStatement`)

| Shows | Format | Notes |
|---|---|---|
| Agreement ID | text | not in the schema: `CommissionStatement.agreementId` |
| Partner name | text | not in the schema: `CommissionStatement.partnerName` |
| From | text | not in the schema: `CommissionStatement.from` |
| To | text | not in the schema: `CommissionStatement.to` |
| Currency | text | not in the schema: `CommissionStatement.currency` |
| Gross sales | text | not in the schema: `CommissionStatement.grossSales` |
| Refunds | text | not in the schema: `CommissionStatement.refunds` |
| Net sales | text | not in the schema: `CommissionStatement.netSales` |
| Commission earned | text | not in the schema: `CommissionStatement.commissionEarned` |
| Amount due | text | not in the schema: `CommissionStatement.amountDue` |
| Lines | text | not in the schema: `CommissionStatement.lines` |

**Data it reads**: `listPartnerAgreements` (onLoad, Commercial agreements with B2B partners)

**Where the user goes next**

- → `PTR-003` Profile & Company Details: *Profile & Company Details*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commission statement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commission statement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commission statement yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on expiringWithinDays, status and the commission statement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PARTNER_VIEW`, which `getCommissionStatement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

**A refused user sees:** Shown when the caller lacks `PARTNER_VIEW`, which `getCommissionStatement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

17 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.7.56 | System shall automatically calculate commissions, incentives, bonuses, overrides, deductions, refunds, and settlement amounts based on partner agreements and sales performance. | Ticketing Sales | CONTRACTED | `getCommissionStatement` |
| 2.7.12 | - Discounts | Ticketing Sales | CONTRACTED | `listPartnerAgreements` |
| 2.7.13 | - Commissions | Ticketing Sales | CONTRACTED | `listPartnerAgreements` |
| 1.1.30 | System shall support corporate ticket allocations, corporate pricing, quotas, approval workflows and corporate account management. | Ticketing Catalogue | CONTRACTED | data `PartnerAgreement` |
| 1.1.102 | Corporate memberships | Ticketing Catalogue | CONTRACTED | data `PartnerAgreement` |
| 1.3.24 | System shall support sponsor packages, sponsor entitlements, sponsorship inventory and sponsor reporting. | Ticketing Catalogue | CONTRACTED | data `PartnerAgreement` |
| 2.7.44 | The system should have the ability to adapt branding and logos on emails and tickets according to B2B client (e.g. co-branded Partner logos to be used on sales through their channels). | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| 2.7.48 | The system should offer white label e-commerce engine for B2B sales (internal CMS). The interface of e-commerce engine should have configurable theming: - Color scheme can be updated - Background … | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| 2.7.50 | System shall support electronic approval and digital signature workflows for B2B agreements, including approval routing, partner acceptance, version history, timestamping, and document storage. | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| 2.7.57 | System shall support partner-specific pricing based on contract terms, tiers, volume thresholds, seasonality, event type, customer segment, product category, negotiated rates, and promotional rules. | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| 2.9.15 | System shall support dedicated pricing structures for memberships, annual passes, member-exclusive products, and member-only promotions. | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| 2.9.16 | System shall support pricing variations and exclusive pricing benefits based on loyalty tier, status level, and guest segmentation. | Ticketing Sales | CONTRACTED | data `PartnerAgreement` |
| … 5 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-017` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (39 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `PTR-003`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `PTR-018` Reports & Sales Performance

**Answer a question about reports with numbers someone can check.**

| | |
|---|---|
| App · platform | TICVAI Control · P10 Partner Web (web) |
| Module | Reports & Settlement · wave 3 · needs the `partner` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | partner staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate) |
| Device and orientation | web · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listReports` reads the population and `getFinancialReport` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `conversationId` (deepLink), `reportId` (deepLink) · cold entry: A conversation link an agent opens from a notification. Resolves, or says it was closed and by whom. |
| Route | `/general/reports-and-sales-performance` |

**What the spec says about it.** States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Category | select | optional | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | Sends `?category=` to `listReports`. | `listReports` ?category |
| Search | text field | optional | — | — | — | Sends `?search=` to `listReports`. | `listReports` ?search |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Report | select | — | Profit and loss · Balance sheet · Cash flow · Revenue by venue · Revenue by product · Tax summary | `getFinancialReport` ?report |
| Fiscal period | picker: choose a fiscal period | — | — | `getFinancialReport` ?fiscalPeriodId |
| Legal entity | picker: choose a legal entity | — | — | `getFinancialReport` ?legalEntityId |
| Cost center | picker: choose a cost center | — | — | `getFinancialReport` ?costCenterId |

**Form: Run report** (modal, opened by *Run report*; *Run report* calls `runReport`, *Cancel* sends nothing)

**Collects what `runReport` sends before it is called.** Nothing in the body is required. Optional: `parameters`, `venueId`, `dateFrom`, `dateTo`, `forceAsync`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Parameters `parameters` | key and value settings | optional | — | — | — | Open on purpose; its shape is the report's. Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. | `runReport` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that. | `runReport` body |
| Date from `dateFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158). | `runReport` body |
| Date to `dateTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Defaults to today in the venue's time zone when not sent (audit R158). | `runReport` body |
| Force async `forceAsync` | toggle | optional | off | — | — | Queue regardless of size, for a result to be collected later. | `runReport` body |

Errors to draw in the form: 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope

**Form: Ask reporting question** (modal, opened by *Ask reporting question*; *Ask reporting question* calls `askReportingQuestion`, *Cancel* sends nothing)

**Collects what `askReportingQuestion` sends before it is called.** Required: `question`. Optional: `conversationId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Question `question` | text area | required | — | min length 3; max length 1000 | — | — | `askReportingQuestion` body |
| Conversation `conversationId` | text field | optional | — | — | — | Continue a prior exchange for follow-up questions. | `askReportingQuestion` body |
| Venue `venueId` | picker: choose a venue | optional | — | Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | shows names, sends the id | Narrows the answer to one venue. Omitting it answers over everything the caller's scope permits — it cannot be used to reach beyond that. | `askReportingQuestion` body |

Errors to draw in the form: 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope

**Form: Create report** (modal, opened by *Create report*; *Create report* calls `createReport`, *Cancel* sends nothing)

**Collects what `createReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `createReport` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `createReport` body |
| Category `category` | select | required | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `createReport` body |
| Data source `dataSource` | select | required | — | Orders · Order lines · Payments · Refunds · Shifts · Scan events · Entitlements · Products · Inventory · Stock movements · Stock counts · Waste … | — | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over data nobody maintains. | `createReport` body |
| Columns `columns` | repeatable rows | required | — | at least 1 | — | — | `createReport` body |
| Field `columns[].field` | text field | required | — | — | — | — | `createReport` body |
| Label `columns[].label` | text field | optional | — | — | — | — | `createReport` body |
| Aggregation `columns[].aggregation` | select | optional | None | None · Count · Count distinct · Sum · Average · Min · Max | — | — | `createReport` body |
| Sort order `columns[].sortOrder` | number field | optional | — | — | — | — | `createReport` body |
| Sort direction `columns[].sortDirection` | segmented control | optional | — | Asc · Desc | — | — | `createReport` body |
| Format `columns[].format` | text field | optional | — | — | — | — | `createReport` body |
| Filters `filters` | repeatable rows | optional | — | — | — | — | `createReport` body |
| Field `filters[].field` | text field | required | — | — | — | — | `createReport` body |
| Operator `filters[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Contains · Is null · Is not null | — | — | `createReport` body |
| Value `filters[].value` | field | optional | — | — | — | Open on purpose; its type is the field's. One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a … | `createReport` body |
| Values `filters[].values` | list of values (chips) | optional | — | — | — | The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`. | `createReport` body |
| Is parameter `filters[].isParameter` | toggle | optional | off | — | — | Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope. | `createReport` body |
| Group by `groupBy` | list of values (chips) | optional | — | — | — | — | `createReport` body |
| Parameters `parameters` | repeatable rows | optional | — | — | — | — | `createReport` body |
| Key `parameters[].key` | text field | required | — | — | — | — | `createReport` body |
| Label `parameters[].label` | text field | required | — | — | — | — | `createReport` body |
| Type `parameters[].type` | select | required | — | String · Integer · Decimal · Money · Boolean · Date · Date time · Uuid · Enum | — | — | `createReport` body |
| Is required `parameters[].isRequired` | toggle | required | — | — | — | — | `createReport` body |
| Default value `parameters[].defaultValue` | field | optional | — | — | — | Open on purpose. A value of this parameter's `type`, used when a run supplies none. | `createReport` body |
| Required permission `requiredPermission` | select | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a venue user could build themselves a … | `createReport` body |
| Max date range days `maxDateRangeDays` | number field (days) | optional | 366 | min 1 | — | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so `runReport`'s date-range 400 always has a … | `createReport` body |

Errors to draw in the form: 400 Unknown field, invalid filter, or estimated cost beyond the limit; 403 Author does not hold the permission they assigned to the report

**Form: Save natural language query** (modal, opened by *Save natural language query*; *Save natural language query* calls `saveNaturalLanguageQuery`, *Cancel* sends nothing)

**Collects what `saveNaturalLanguageQuery` sends before it is called.** Required: `name`. Optional: `category`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `saveNaturalLanguageQuery` body |
| Category `category` | select | optional | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `saveNaturalLanguageQuery` body |

**Form: Save report** (modal, opened by *Save report*; *Save report* calls `updateReport`, *Cancel* sends nothing)

**Collects what `updateReport` sends before it is called.** Required: `name`, `category`, `dataSource`, `columns`, `requiredPermission`. Optional: `description`, `filters`, `groupBy`, `parameters`, `maxDateRangeDays`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 200 | — | — | `updateReport` body |
| Description `description` | text area | optional | — | max length 1000 | — | — | `updateReport` body |
| Category `category` | select | required | — | Sales · Admission · Financial · Inventory · Guest · Operations · Marketing · Workforce · Compliance · Custom | — | — | `updateReport` body |
| Data source `dataSource` | select | required | — | Orders · Order lines · Payments · Refunds · Shifts · Scan events · Entitlements · Products · Inventory · Stock movements · Stock counts · Waste … | — | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over data nobody maintains. | `updateReport` body |
| Columns `columns` | repeatable rows | required | — | at least 1 | — | — | `updateReport` body |
| Field `columns[].field` | text field | required | — | — | — | — | `updateReport` body |
| Label `columns[].label` | text field | optional | — | — | — | — | `updateReport` body |
| Aggregation `columns[].aggregation` | select | optional | None | None · Count · Count distinct · Sum · Average · Min · Max | — | — | `updateReport` body |
| Sort order `columns[].sortOrder` | number field | optional | — | — | — | — | `updateReport` body |
| Sort direction `columns[].sortDirection` | segmented control | optional | — | Asc · Desc | — | — | `updateReport` body |
| Format `columns[].format` | text field | optional | — | — | — | — | `updateReport` body |
| Filters `filters` | repeatable rows | optional | — | — | — | — | `updateReport` body |
| Field `filters[].field` | text field | required | — | — | — | — | `updateReport` body |
| Operator `filters[].operator` | select | required | — | Equals · Not equals · Greater than · Less than · Between · In · Not in · Contains · Is null · Is not null | — | — | `updateReport` body |
| Value `filters[].value` | field | optional | — | — | — | Open on purpose; its type is the field's. One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a … | `updateReport` body |
| Values `filters[].values` | list of values (chips) | optional | — | — | — | The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`. | `updateReport` body |
| Is parameter `filters[].isParameter` | toggle | optional | off | — | — | Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope. | `updateReport` body |
| Group by `groupBy` | list of values (chips) | optional | — | — | — | — | `updateReport` body |
| Parameters `parameters` | repeatable rows | optional | — | — | — | — | `updateReport` body |
| Key `parameters[].key` | text field | required | — | — | — | — | `updateReport` body |
| Label `parameters[].label` | text field | required | — | — | — | — | `updateReport` body |
| Type `parameters[].type` | select | required | — | String · Integer · Decimal · Money · Boolean · Date · Date time · Uuid · Enum | — | — | `updateReport` body |
| Is required `parameters[].isRequired` | toggle | required | — | — | — | — | `updateReport` body |
| Default value `parameters[].defaultValue` | field | optional | — | — | — | Open on purpose. A value of this parameter's `type`, used when a run supplies none. | `updateReport` body |
| Required permission `requiredPermission` | select | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a venue user could build themselves a … | `updateReport` body |
| Max date range days `maxDateRangeDays` | number field (days) | optional | 366 | min 1 | — | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so `runReport`'s date-range 400 always has a … | `updateReport` body |

Errors to draw in the form: 409 The report is a system report, which is clone-only (audit R096).

#### Outputs: what the screen shows and produces

**Shown**

**Every report definition** (data table, from `listReports`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Data source | chip: Orders, Order lines, Payments, Refunds, Shifts, Scan events… | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over … |
| Columns | list or chips (count when long) | — |
| Filters | list or chips (count when long) | — |
| Group by | list or chips (count when long) | — |
| Parameters | list or chips (count when long) | — |
| Required permission | chip: SESSION FORCE LOGOUT, USER MANAGE, ROLE MANAGE, PERMISSION GRANT, PERMISSION VIEW … | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a … |
| Max date range days | 1,234 | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so … |
| ID | the name it points at, never the id | — |
| Is system | yes / no (icon or chip) | Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). Clone-only (decided 28 September, audit R096): `updateReport` … |

**The selected report definition** (detail panel, from `getReport`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Description | text | — |
| Category | chip: Sales, Admission, Financial, Inventory, Guest, Operations… | — |
| Data source | chip: Orders, Order lines, Payments, Refunds, Shifts, Scan events… | What a report may be built over. A closed set, and that is the point — a builder that accepts any table will happily produce a report over … |
| Columns | list or chips (count when long) | — |
| Filters | list or chips (count when long) | — |
| Group by | list or chips (count when long) | — |
| Parameters | list or chips (count when long) | — |
| Required permission | chip: SESSION FORCE LOGOUT, USER MANAGE, ROLE MANAGE, PERMISSION GRANT, PERMISSION VIEW … | Permission needed to run this report, from the shared `Permission` vocabulary. The author cannot assign one they do not hold — otherwise a … |
| Max date range days | 1,234 | Guards against a query spanning years of scan events. When a report sets none, 366 days applies (decided 28 September, audit R158), so … |
| ID | the name it points at, never the id | — |
| Is system | yes / no (icon or chip) | Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). Clone-only (decided 28 September, audit R096): `updateReport` … |
| Is retired | yes / no (icon or chip) | — |
| Estimated cost | chip: Low, Medium, High | Informs whether it may run inline or must be queued. |
| Created by principal | the name it points at, never the id | — |
| Last run at | 1 Oct 2026, 14:30 | — |

**The financial report** (detail panel, from `getFinancialReport`)

| Shows | Format | Notes |
|---|---|---|
| Report | chip: Profit and loss, Balance sheet, Cash flow, Revenue by venue, Revenue by product … | The report `getFinancialReport` returns. One vocabulary for the query and the response. |
| Fiscal period | the name it points at, never the id | — |
| Legal entity | the name it points at, never the id | — |
| Currency | text | — |
| Currency scale | 1,234 | — |
| Generated at | 1 Oct 2026, 14:30 | — |
| Sections | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run report (primary button) | `runReport` POST `/reports/{reportId}/run` | RunReportRequest | ReportResult | 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Ask reporting question (secondary button) | `askReportingQuestion` POST `/reports/ask` | inline | NaturalLanguageAnswer | 400 Question could not be interpreted. (ReportQuestionProblem); 403 Authenticated but not permitted at the requested scope | opens modal first |
| Create report (secondary button) | `createReport` POST `/reports` | CreateReportRequest | ReportDefinition | 400 Unknown field, invalid filter, or estimated cost beyond the limit; 403 Author does not hold the permission they assigned to the report | opens modal first |
| Delete report (destructive button) | `deleteReport` DELETE `/reports/{reportId}` | — | — | 409 Active schedules reference this report (`report-scheduled`), or it is a system report, which is clone-only (`system-report`, audit R096) | — |
| Save natural language query (secondary button) | `saveNaturalLanguageQuery` POST `/reports/ask/{conversationId}/save` | inline | ReportDefinition | — | opens modal first |
| Save report (secondary button) | `updateReport` PUT `/reports/{reportId}` | CreateReportRequest | ReportDefinition | 409 The report is a system report, which is clone-only (audit R096). | opens modal first |

**Data it reads**: `getFinancialReport` (onLoad, P&L, balance sheet or cash flow); `listReports` (onLoad, List available report definitions)

**Where the user goes next**

- → `PTR-003` Profile & Company Details: *Profile & Company Details*

**What opens over it**

- confirmDialog *Delete report*: **Names what `deleteReport` changes and what it leaves alone**, in the consequence rather than the verb. A reports sales performance this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reports sales performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reports sales performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reports sales performance yet. Offers Create report (`createReport`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on category, search and the reports sales performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getFinancialReport` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem); 400 Required parameter missing, or the date range exceeds `maxDateRangeDays` (366 days when the definition sets none, audit R158); 400 Unknown field, invalid filter, or estimated cost beyond the limit; 409 Active schedules reference this report (`report-scheduled`), or it is a system report, which is clone-only (`system-report` … |

#### Permissions

- `runReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `createReport` → `REPORT_MANAGE` (configure) · staff, partner
- `deleteReport` → `REPORT_MANAGE` (configure) · staff, partner
- `getFinancialReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `getReport` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `listReports` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `saveNaturalLanguageQuery` → `REPORT_MANAGE` (configure) · staff, partner
- `updateReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `getFinancialReport` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

93 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.19 | The system should have ability for reporting ranges which allow for specific beginning/end points; e.g., date-to-date as well as month, or guest name list | Retail POS | CONTRACTED | `runReport` |
| 6.1.43 | The system should be able to report on Historical records up to 5 years for internal reporting requirements or as required by finance operation team for Audit purpose. | Retail POS | CONTRACTED | `runReport` |
| 8.7.24 | System shall support historical analytics. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 8.7.25 | System shall support trend analysis. | Unified Operations Dashboard | CONTRACTED | `runReport` |
| 13.3.14 | APIs shall expose operational, financial, attendance, membership and sales reporting data. | Developer & API Management | CONTRACTED | `runReport` |
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |
| 1.1.40 | System shall provide analytics and dashboards covering ticket sales, attendance, utilization, conversion rates, capacity utilization and revenue performance. | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.104 | Membership analytics | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.135 | Required Reports Operational Reports Donations by Campaign. Donations by Site. Donations by Product. Donations by Sales Channel. Donations by Date. Donations by User/Cashier. Donations by Payment … | Ticketing Catalogue | CONTRACTED | `createReport` |
| 3.2.65 | An Entry or Exit report is expected presenting the readings per outcome (ok/ko), per time and per access point. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.66 | The in park report showing the difference between the Entries and the Exits. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.68 | The length of stay report shall present the difference between the time in scan and the time out scan. | Admission and Access | CONTRACTED | `createReport` |
| … 81 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 12 for all of P10, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P10 Partner Web.dc.html#ptr-018` · status **notStarted** · provenance generated
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (64), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#PTR-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run report, Ask reporting question, Create report, Delete report, Save natural language query, Save report.
- [ ] Every transition is wired: `PTR-003`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P10 as a whole** (12: 0 open, 12 closed). Open first; a closed row says where it went on 30 September.

- **A89** Build corporate/B2B self-service onboarding (trade licence & VAT upload → approve/reject → rate setup → credential issuance) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker)*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker)*
- **A170** Build family and corporate wallets (parent-funded child wristbands, per-member allowances, parent-only top-up, guest self-service family setup, department-segregated corporate funds, bidirectional transfer as a venue … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker)*
- **A178** Build B2B partner management (configurable profiles, onboarding workflow, sub-agents, territory and distribution rights, venue association with per-venue pricing, document compliance repository, action permissions … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A179** Support all three B2B/OTA routes (direct portal · bidirectional API with external OTAs · bulk pre-generated QR CSV for non-integrating partners), with an existing OTA integration reusable by configuration *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A180** Build B2B agreements & payment models (tiered volume discounts, commission rates, credit limit vs. prepaid wallet vs. card, partner-reserved inventory, booking limits) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A181** Build B2B settlement & reconciliation (per-partner operations dashboard, statements of account, exception management for unsettled transfers, dispute handling, AI partner performance view) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A184** Build group, school and corporate sales (inquiry dashboard, configurable customer categories, package builder against live inventory and resources, versioned quotations with discount approval, conversion to confirmed … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker)*
- **A208** Check amendments and cancellations against policy before allowing refund, cancellation or reschedule, track booking financial status, and support deposits for school and corporate bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 1 Sep 2026 · workshop tracker)*
- **A231** Build the live operations dashboard and group/B2B admission profile (real-time attendance by venue and gate, gate status, turnstile mode reconfigurable through the day, entry stats by category) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker)*
- **C35** Share the wallet-configuration reference documentation (foundation, funding, stored value, family/corporate, gift cards, payments, fraud/risk, API) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 27 Aug 2026 · workshop tracker)*
- **C44** Confirm how B2B/reseller-issued tickets are handled under a fully-dynamic-QR event policy *(Qossai · Pending → 30 Sep: Closed, Moved to T10 · 2 Sep 2026 · workshop tracker)*

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

### Across P10 Partner Web

- **Open question.** Qossai proposes a POS-style interface for high-volume resellers (hotels, travel agents) instead of a B2C-style site with login: assigned tickets and partner prices after login, optional cash drawer, sent-ticket history and resend, balance view. Chinmay wireframes both options; decide after review. *(open · MoM 29 Sep 2026, 3. B2B / reseller portal · DI-1023)*
- Qossai: partners may use the TICVAI B2B portal directly with a white-label-style B2B credential (similar to B2C), or integrate via API (preferred for OTAs such as Ticketmaster, Platinum List, BookMyShow). *(agreed · MoM 31 Aug 2026, 4.3 Clarified (integration models) · DI-552)*
- Partner access controls define which actions a partner may perform (e.g. refund, reschedule); the partner portal should only offer the actions granted. *(client request · MoM 31 Aug 2026, 4.3 B2B Reseller & OTA Partner Management · DI-551)*
- Allam: B2B Portal option — partners without their own platform use a TICVAI B2B portal structured like the B2C store but behind login credentials, showing pre-configured partner pricing and products, with commission tracked the same way. *(client request · MoM 5 Aug 2026, 2. B2B Ticket Distribution Models · DI-134)*
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)*
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)*
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
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"createReport": {"method":"POST","path":"/reports","contract":"reporting","summary":"Create a custom report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"deleteReport": {"method":"DELETE","path":"/reports/{reportId}","contract":"reporting","summary":"Retire a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getFinancialReport": {"method":"GET","path":"/reports/financial","contract":"finance","summary":"Financial statements, revenue and tax summaries","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"report","in":"query","required":true},{"name":"fiscalPeriodId","in":"query","required":true},{"name":"legalEntityId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"costCenterId","in":"query","required":null}],"requestBody":null,"responds":"FinancialReport"},
"getReport": {"method":"GET","path":"/reports/{reportId}","contract":"reporting","summary":"Read a report definition","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportDefinition"},
"getSettlement": {"method":"GET","path":"/settlements/{settlementId}","contract":"finance","summary":"Settlement detail with match results","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"Settlement"},
"ingestSettlementFile": {"method":"POST","path":"/settlements","contract":"finance","summary":"Ingest a provider settlement file","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listReports": {"method":"GET","path":"/reports","contract":"reporting","summary":"List available report definitions","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"category","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSettlementExceptions": {"method":"GET","path":"/settlements/{settlementId}/exceptions","contract":"finance","summary":"Unmatched or mismatched settlement lines","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSettlements": {"method":"GET","path":"/settlements","contract":"finance","summary":"List settlement batches","permission":"SETTLEMENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"providerName","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"resolveSettlementException": {"method":"POST","path":"/settlements/{settlementId}/exceptions","contract":"finance","summary":"Resolve a settlement exception","permission":"SETTLEMENT_RECONCILE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SettlementException"},
"runReport": {"method":"POST","path":"/reports/{reportId}/run","contract":"reporting","summary":"Run a report","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RunReportRequest","responds":"ReportResult"},
"saveNaturalLanguageQuery": {"method":"POST","path":"/reports/ask/{conversationId}/save","contract":"reporting","summary":"Save a natural-language answer as a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportDefinition"},
"updateReport": {"method":"PUT","path":"/reports/{reportId}","contract":"reporting","summary":"Publish a new version of a definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"DataSource": {"type":"string","description":"What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n","enum":["orders","orderLines","payments","refunds","shifts","scanEvents","entitlements","products","inventory","stockMovements","stockCounts","waste","workstations","devices","principals","loyalty","reviews","queueEntries","guests","campaigns","cases","ledgerEntries","workOrders","approvals","purchaseOrders","receipts","requisitions","stockBatches","resourceBookings","delegations","forms","challenges","wallets","resaleListings","accreditationApplications","accreditationHolders","accreditationCredentials","forecastPoints"],"x-ticvai-forecast-points":"**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"},
"FieldType": {"type":"string","enum":["string","integer","decimal","money","boolean","date","dateTime","uuid","enum"]},
"FinancialReport": {"x-ticvai-persistence":"none — computed from replica","type":"object","required":["report","fiscalPeriodId","currency","generatedAt","sections"],"properties":{"report":{"$ref":"#/components/schemas/FinancialReportKind"},"fiscalPeriodId":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer"},"generatedAt":{"type":"string","format":"date-time"},"sections":{"type":"array","items":{"type":"object","required":["name","lines","total"],"properties":{"name":{"type":"string"},"lines":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"accountCode":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"priorPeriodAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The same line for **the same period last year** (decided 28 September, audit R127 (3)). Absent where that period did not exist."}}}},"total":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"FinancialReportKind": {"type":"string","description":"The report `getFinancialReport` returns. One vocabulary for the query and the response.","enum":["profitAndLoss","balanceSheet","cashFlow","revenueByVenue","revenueByProduct","taxSummary"]},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReportCategory": {"type":"string","enum":["sales","admission","financial","inventory","guest","operations","marketing","workforce","compliance","custom"]},
"ReportColumn": {"x-ticvai-persistence":"reporting.report_column","type":"object","required":["field"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"label":{"type":"string"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"default":"none"},"sortOrder":{"type":"integer"},"sortDirection":{"type":"string","enum":["asc","desc"]},"format":{"type":"string","nullable":true}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportFilter": {"x-ticvai-persistence":"reporting.report_filter","type":"object","required":["field","operator"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","contains","isNull","isNotNull"]},"value":{"description":"**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"},"values":{"type":"array","description":"The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.","items":{}},"isParameter":{"type":"boolean","default":false,"description":"Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"}}},
"ReportParameter": {"x-ticvai-persistence":"reporting.report_parameter","type":"object","required":["key","label","type","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"},"isRequired":{"type":"boolean"},"defaultValue":{"description":"Open on purpose. A value of this parameter's `type`, used when a run supplies none."}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"RunReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","properties":{"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose; its shape is the report's.** Keyed by `ReportParameter.key` of the definition being run, each value of that parameter's `type`. An `isRequired` parameter with no value here and no `defaultValue` is the `400` `runReport` lists.\n"},"venueId":{"type":"string","format":"uuid","description":"Narrows to one venue. Omitting it returns everything the caller's scope permits — it cannot be used to reach beyond that.\n"},"dateFrom":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (decided 28 September, audit R158)."},"dateTo":{"type":"string","format":"date","description":"Defaults to today in the venue's time zone when not sent (audit R158)."},"forceAsync":{"type":"boolean","default":false,"description":"Queue regardless of size, for a result to be collected later."}}},
"Settlement": {"x-ticvai-persistence":"ledger.settlement","type":"object","required":["id","providerName","periodStart","periodEnd","status","ingestedAt"],"properties":{"id":{"type":"string","format":"uuid"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","description":"**A settlement has no account, so nothing else denominates it.** A posting takes its currency from `ledger.account.currency` and a payment from `tenderCurrency`, but a settlement is a provider file for a period: `providerGross`, `ledgerGross` and `difference` are bare amounts, and a provider file in one currency against a ledger in another computes a difference that means nothing. Added 20 September, when a venue became able to trade outside its region's currency.\n"},"providerName":{"type":"string"},"venueId":{"type":"string","format":"uuid","description":"The venue this settlement is for. **Reconciled daily per venue** (decided 28 September, audit R110 (b)), so `periodStart` and `periodEnd` are the same day."},"periodStart":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"periodEnd":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"fileReference":{"type":"string","format":"uuid","description":"The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. **Kept on the row because parsing is asynchronous**: the job that parses the file reads it from here.\n"},"format":{"type":"string","nullable":true,"enum":["csv","fixedWidth","xml","json"],"description":"The file format given at ingest. Null when none was given."},"status":{"$ref":"#/components/schemas/SettlementStatus"},"lineCount":{"type":"integer"},"matchedCount":{"type":"integer"},"exceptionCount":{"type":"integer"},"providerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerFees":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"providerNet":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ledgerGross":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ingestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `region` scope.**"}}},
"SettlementException": {"x-ticvai-persistence":"ledger.settlement_exception","type":"object","required":["id","settlementId","kind","providerReference","amount"],"properties":{"id":{"type":"string","format":"uuid","description":"Server-created when parsing finds the exception, so a UUID (naming-and-style 4)."},"settlementId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["unmatchedInProvider","unmatchedInLedger","amountMismatch","duplicateInProvider","feeUnexplained"]},"providerReference":{"type":"string","nullable":true},"paymentId":{"type":"string","format":"uuid","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"expectedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"resolution":{"allOf":[{"$ref":"#/components/schemas/SettlementResolution"}],"nullable":true,"description":"Null while the exception is open."},"note":{"type":"string","nullable":true,"description":"The `note` given to `resolveSettlementException`, stored with the resolution."},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"resolvedAt":{"type":"string","format":"date-time","nullable":true}}},
"SettlementResolution": {"type":"string","description":"How a settlement exception was explained. One vocabulary for the request and the stored exception.","enum":["matchedManually","writeOff","disputeRaised","providerError","timingDifference"]},
"SettlementStatus": {"type":"string","enum":["ingesting","parsing","matching","matched","hasExceptions","resolved","failed"]}
}
```
