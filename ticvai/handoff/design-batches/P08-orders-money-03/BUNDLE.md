# P08-orders-money-03 — P08 · Orders & Money (3 of 3)

**7 screens · 42 operations · 39 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `ACCOUNT_CONFIGURE, LEDGER_APPROVE, LEDGER_POST, LEDGER_VIEW, ORDER_VIEW, SETTLEMENT_VIEW, TAX_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
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
| `BO-074` | Chart of Accounts | A | 35 | 44 | 6 | 39 | 2 | 0 | — | notStarted (generated) |
| `BO-075` | Account Mapping | A | 31 | 43 | 6 | 16 | 2 | 0 | — | notStarted (generated) |
| `BO-076` | Revenue Recognition | B–D | 16 | 31 | 6 | 74 | 2 | 0 | — | notStarted (generated) |
| `BO-077` | FX Rates & Variances | A | 15 | 34 | 6 | 1 | 2 | 4 | — | notStarted (generated) |
| `BO-089` | Journal Entries | B–D | 19 | 28 | 6 | 22 | 1 | 0 | — | notStarted (generated) |
| `BO-090` | Period Close | B–D | 5 | 22 | 6 | 11 | 1 | 0 | — | notStarted (generated) |
| `BO-101` | Orders & Money | B–D | 7 | 38 | 6 | 22 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-074` Chart of Accounts

**Accounts, cost centres and legal entities.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block A · ticket #18126 (APP-SETUP-BO-074) |
| Who uses it | venue staff holding `ACCOUNT_CONFIGURE`, `LEDGER_VIEW` (1 configure, 1 read); in the flows as finance controller, platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listAccounts` reads the population and `getAccount` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `accountId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/finance/chart-of-accounts` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. Pulled to Wave 1 (CF-101). **F16 says it itself** — no chart of accounts blocks the first sale, so it cannot be Wave 2 while venue provisioning is Wave 1.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Legal entity id | picker: choose a legal entity (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?legalEntityId=` to `listAccounts`. | `listAccounts` ?legalEntityId |
| Type | radio group | optional | — | Asset · Liability · Equity · Revenue · Expense | — | Sends `?type=` to `listAccounts`. | `listAccounts` ?type |
| Is postable | toggle | optional | — | Parent accounts aggregate and cannot be posted to. | — | Sends `?isPostable=` to `listAccounts`. | `listAccounts` ?isPostable |

**Form: Create account** (modal, opened by *Create account*; *Create account* calls `createAccount`, *Cancel* sends nothing)

**Collects what `createAccount` sends before it is called.** Required: `code`, `name`, `type`, `legalEntityId`. Optional: `externalCode`, `parentId`, `isPostable`, `isSuspense`, `subType`, `tags`, `notes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[A-Za-z0-9._-]+$` | — | — | `createAccount` body |
| External code `externalCode` | text field | optional | — | max length 64 | — | — | `createAccount` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createAccount` body |
| Type `type` | radio group | required | — | Asset · Liability · Equity · Revenue · Expense | — | — | `createAccount` body |
| Parent `parentId` | picker: choose a parent | optional | — | — | shows names, sends the id | — | `createAccount` body |
| Legal entity `legalEntityId` | picker: choose a legal entity | required | — | — | shows names, sends the id | — | `createAccount` body |
| Is postable `isPostable` | toggle | optional | on | — | — | — | `createAccount` body |
| Is suspense `isSuspense` | toggle | optional | off | — | — | See `Account.isSuspense`. | `createAccount` body |
| Sub type `subType` | text field | optional | — | — | — | See `Account.subType`. | `createAccount` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | See `Account.tags`. | `createAccount` body |
| Notes `notes` | text area | optional | — | — | — | See `Account.notes`. | `createAccount` body |

Errors to draw in the form: 400 Validation failed; 409 Code already in use within this legal entity

**Form: Save account** (modal, opened by *Save account*; *Save account* calls `updateAccount`, *Cancel* sends nothing)

**Collects what `updateAccount` sends before it is called.** Nothing in the body is required. Optional: `code`, `name`, `externalCode`, `isActive`, `isSuspense`, `subType`, `tags`, `notes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | optional | — | max length 64; pattern `^[A-Za-z0-9._-]+$` | — | Accepted only while the account has no entries. | `updateAccount` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `updateAccount` body |
| External code `externalCode` | text field | optional | — | max length 64 | — | — | `updateAccount` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updateAccount` body |
| Is suspense `isSuspense` | toggle | optional | — | — | — | — | `updateAccount` body |
| Sub type `subType` | text field | optional | — | — | — | — | `updateAccount` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateAccount` body |
| Notes `notes` | text area | optional | — | — | — | — | `updateAccount` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `code` sent for an account that already has entries, or a new code already in use within the legal entity.

**Form: Create cost center** (modal, opened by *Create cost center*; *Create cost center* calls `createCostCenter`, *Cancel* sends nothing)

**Collects what `createCostCenter` sends before it is called.** Required: `code`, `name`. Optional: `parentId`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createCostCenter` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createCostCenter` body |
| Parent `parentId` | picker: choose a parent | optional | — | — | shows names, sends the id | — | `createCostCenter` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `createCostCenter` body |

**Form: Create legal entity** (modal, opened by *Create legal entity*; *Create legal entity* calls `createLegalEntity`, *Cancel* sends nothing)

**Collects what `createLegalEntity` sends before it is called.** Required: `id`, `code`, `name`, `countryCode`, `currency`, `currencyScale`, `fiscalYearStartMonth`. Optional: `taxRegistrationNumber`, `regionIds`, `isActive`, `scopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `createLegalEntity` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createLegalEntity` body |
| Country code `countryCode` | text field | required | — | pattern `^[A-Z]{2}$` | — | — | `createLegalEntity` body |
| Currency `currency` | text field | required | — | pattern `^[A-Z]{3}$` | — | — | `createLegalEntity` body |
| Currency scale `currencyScale` | stepper or slider | required | — | min 0; max 4 | — | — | `createLegalEntity` body |
| Tax registration number `taxRegistrationNumber` | text field | optional | — | — | — | — | `createLegalEntity` body |
| Fiscal year start month `fiscalYearStartMonth` | stepper or slider | required | — | min 1; max 12 | — | — | `createLegalEntity` body |
| Regions `regionIds` | multi-picker: choose regions | optional | — | — | — | — | `createLegalEntity` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `createLegalEntity` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every account** (data table, from `listAccounts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| External code | text | Code in the client's own chart. Used on export so their team sees their codes. |
| Is suspense | yes / no (icon or chip) | 5.7.x. Where a posting with no account mapping goes. |
| Sub type | text | 5.7.27. `AccountType` stays a closed enum of asset, liability, equity, revenue and expense because that is correct accounting, and a venue … |
| Tags | list or chips (count when long) | How a venue groups accounts for its own reporting. Free-form, and outside the type. |
| Notes | text | 5.7.27. Annotations on the account, which an auditor reads before the balance. |
| Name | text | — |
| Type | chip: Asset, Liability, Equity, Revenue, Expense | — |
| Parent | the name it points at, never the id | — |
| Legal entity | the name it points at, never the id | — |
| Currency | text | — |

**Every cost center** (data table, from `listCostCenters`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Parent | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Is active | yes / no (icon or chip) | — |

**Every legal entity** (data table, from `listLegalEntities`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Country code | text | — |
| Currency | text | — |
| Currency scale | 1,234 | — |
| Tax registration number | text | — |
| Fiscal year start month | 1,234 | — |
| Regions | list or chips (count when long) | — |
| Is active | yes / no (icon or chip) | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected account** (detail panel, from `getAccount`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| External code | text | Code in the client's own chart. Used on export so their team sees their codes. |
| Is suspense | yes / no (icon or chip) | 5.7.x. Where a posting with no account mapping goes. |
| Sub type | text | 5.7.27. `AccountType` stays a closed enum of asset, liability, equity, revenue and expense because that is correct accounting, and a venue … |
| Tags | list or chips (count when long) | How a venue groups accounts for its own reporting. Free-form, and outside the type. |
| Notes | text | 5.7.27. Annotations on the account, which an auditor reads before the balance. |
| Name | text | — |
| Type | chip: Asset, Liability, Equity, Revenue, Expense | — |
| Parent | the name it points at, never the id | — |
| Legal entity | the name it points at, never the id | — |
| Currency | text | — |
| Is postable | yes / no (icon or chip) | False for parent accounts, which aggregate only. |
| Is active | yes / no (icon or chip) | — |
| Balance | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create account (primary button) | `createAccount` POST `/accounts` | CreateAccountRequest | Account | 400 Validation failed; 409 Code already in use within this legal entity | opens modal first |
| Save account (secondary button) | `updateAccount` PATCH `/accounts/{accountId}` | inline | Account | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `code` sent for an account that already has entries, or a new code already in use within the legal entity. | opens modal first |
| Create cost center (secondary button) | `createCostCenter` POST `/cost-centers` | inline | CostCenter | — | opens modal first |
| Create legal entity (secondary button) | `createLegalEntity` POST `/legal-entities` | LegalEntity | LegalEntity | — | opens modal first |

**Data it reads**: `listAccounts` (onLoad, List the chart of accounts); `listCostCenters` (onLoad, List cost centres); `listLegalEntities` (onLoad, List legal entities)

**Where the user goes next**

- → `BO-075` Account Mapping: *Maps products to accounts*
- → `BO-077` FX Rates & Variances: *FX Rates & Variances*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The chart accounts list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the chart accounts untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No chart accounts yet. Offers Create account (`createAccount`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on legalEntityId, type, isPostable and the chart accounts are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listAccounts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Code already in use within this legal entity; 409 `code` sent for an account that already has entries, or a new code already in use within the legal entity. |

#### Permissions

- `listAccounts` → `LEDGER_VIEW` (read) · staff
- `getAccount` → `LEDGER_VIEW` (read) · staff
- `createAccount` → `ACCOUNT_CONFIGURE` (configure) · staff
- `updateAccount` → `ACCOUNT_CONFIGURE` (configure) · staff
- `listCostCenters` → `LEDGER_VIEW` (read) · staff
- `createCostCenter` → `ACCOUNT_CONFIGURE` (configure) · staff
- `listLegalEntities` → `LEDGER_VIEW` (read) · staff
- `createLegalEntity` → `ACCOUNT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listAccounts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

39 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.12.97 | System shall support account type filtering during journal entry creation. | F&B & Guest Management | CONTRACTED | `listAccounts` |
| 5.12.102 | System shall support account lookup and search capabilities. | F&B & Guest Management | CONTRACTED | `listAccounts` |
| 5.7.1 | The system should support entry and maintenance of data in accounts related information tables. The primary usage of this data will be to derive accounts for billing records and interface with the … | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.25 | System shall provide a configurable Chart of Accounts structure. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.26 | System shall support Asset, Liability, Equity, Revenue, and Expense account types. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.28 | System shall support account codes, names, and descriptions. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.32 | System shall provide account search and filtering capabilities. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.33 | Create and manage General Ledger accounts. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.34 | Support configurable account numbering structures. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.36 | Allow account classification by account type. | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.37 | Support account status management (active/inactive). | F&B & Guest Management | CONTRACTED | `createAccount` |
| 5.7.39 | Support account-level descriptions and metadata. | F&B & Guest Management | CONTRACTED | `createAccount` |
| … 27 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Chart of accounts screen: external-system codes for ERP mapping, classification (asset, liability, income, expense), parent-account hierarchy and edit view with financial dimensions (profit centre, cost centres); plus transaction-to-account and payment/offset account mapping. *(client request · MoM 12 Aug 2026, 14. Finance Module Walkthrough — Dashboards, Chart of Accounts & Entities · DI-262)*
- Chart of accounts can be created natively in TICVAI or mapped to a client's external/ERP chart of accounts. *(agreed · MoM 12 Aug 2026, 13. Chart of Accounts and Account Mapping · DI-259)*

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-074` · status **notStarted** · provenance generated
- Flow F16 *A venue opens for the first time*, step 5: Finance sets the chart of accounts → **Before the first sale.** Every sale posts somewhere
- Flow F98 *A day is reconciled from takings to the ledger*, step 2: Chart of Accounts. → 6 operations, 6 of them previously unwalked.
- Flow F16 branch at step 5 (abandonsFlow): when No chart of accounts, **Blocks the first sale**, and it is the failure a venue discovers on opening morning rather than in setup.

#### Acceptance for the design

- [ ] Every input above is drawn (35), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-074?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create account, Save account, Create cost center, Create legal entity.
- [ ] Every transition is wired: `BO-075`, `BO-077`.
- [ ] Every gated control is gated: `ACCOUNT_CONFIGURE`, `LEDGER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-075` Account Mapping

**Which product or movement posts to which account.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | Block A · ticket #20666 (APP-SETUP-BO-075) |
| Who uses it | venue staff holding `ACCOUNT_CONFIGURE`, `LEDGER_VIEW`, `TAX_CONFIGURE` (2 configure, 1 read); in the flows as finance controller, platform admin |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): 3 independent reads and no read of one record — the screen watches a population rather than working one |
| Offline | online only |
| Opens with | `taxCodeId` (deepLink), `exemptionId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/finance/account-mapping` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing. Pulled to Wave 1 (CF-101). Without a mapping every sale posts to suspense. **Cross-platform navigation removed 24 August**: ADM-020. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Country code | text field | — | pattern `^[A-Z]{2}$` | `listTaxCodes` ?countryCode |

**Form: Save account mappings** (modal, opened by *Save account mappings*; *Save account mappings* calls `setAccountMappings`, *Cancel* sends nothing)

**Collects what `setAccountMappings` sends before it is called.** Required: `mappings`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Mappings `mappings` | repeatable rows | required | — | — | — | — | `setAccountMappings` body |
| Event type `mappings[].eventType` | select | required | — | Ticket revenue · Fnb revenue · Retail revenue · Rental revenue · Tax payable · Cash received · Card received · Wallet received · Refund issued · Void reversal · Deferred revenue · Recognised revenue … | — | Every event that generates a ledger posting. How each money event posts (decided 28 September, audit R191). | `setAccountMappings` body |
| Debit account `mappings[].debitAccountId` | picker: choose a debit account | required | — | — | shows names, sends the id | — | `setAccountMappings` body |
| Credit account `mappings[].creditAccountId` | picker: choose a credit account | required | — | — | shows names, sends the id | — | `setAccountMappings` body |
| Venue `mappings[].venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | Null applies the mapping to every venue in the region. | `setAccountMappings` body |

Errors to draw in the form: 400 A required event type (`cardReceived`, `cashReceived`, `refundIssued`, `priceVariance`; audit R127 (1)) has no mapping, or maps to a non-postable account

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

**Form: Create tax exemption** (modal, opened by *Create tax exemption*; *Create tax exemption* calls `createTaxExemption`, *Cancel* sends nothing)

**Collects what `createTaxExemption` sends before it is called.** Required: `id`, `scope`, `taxCodeId`, `reason`. Optional: `scopeRef`, `certificateReference`, `validFrom`, `validTo`. Dismissing sends nothing; the screen behind is unchanged.

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

**Every account mapping** (data table, from `listAccountMappings`)

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listAccountMappings` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A required event type (`cardReceived`, `cashReceived`, `refundIssued`, `priceVariance`; audit R127 (1)) has no mapping, or maps to a non-postable account; 400 Compound reference is circular or crosses countries; 400 `rate` without `effectiveFrom`, or `effectiveFrom` without `rate`. `errors[]` names the field.; 409 A rate change whose `effectiveFrom` is today or earlier, which would reprice … |

#### Permissions

- `listAccountMappings` → `LEDGER_VIEW` (read) · staff
- `setAccountMappings` → `ACCOUNT_CONFIGURE` (configure) · staff
- `listTaxCodes` → `LEDGER_VIEW` (read) · staff
- `createTaxCode` → `TAX_CONFIGURE` (configure) · staff
- `updateTaxCode` → `TAX_CONFIGURE` (configure) · staff
- `listTaxExemptions` → `LEDGER_VIEW` (read) · staff
- `createTaxExemption` → `TAX_CONFIGURE` (configure) · staff
- `verifyTaxExemption` → `TAX_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listAccountMappings` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-076` Revenue Recognition

**Deferred revenue, its ageing, and the schedules that release it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCOUNT_CONFIGURE`, `LEDGER_POST`, `LEDGER_VIEW` (1 configure, 1 operate, 1 read); in the flows as finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRecognitionSchedules` reads the population and `getDeferredRevenue` reads one of them — list, select, act |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/finance/revenue-recognition` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.

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

**Collects what `createRecognitionSchedule` sends before it is called.** Required: `id`, `name`, `method`, `productKinds`. Optional: `priority`, `recognitionSite`, `frequency`, `revalidateOnValidityChange`, `deferredAccountId`, `recognisedAccountId`, `breakageAccountId`, `noShowTrigger`, `noShowAccountId`, `breakageAfterDays`, `isActive`. Dismissing sends nothing; the screen behind is unchanged.

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

#### Outputs: what the screen shows and produces

**Shown**

**Every recognition schedule** (data table, from `listRecognitionSchedules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Method | chip: Immediate, On redemption, Straight line, Per visit, On expiry | — |
| Priority | 1,234 | Two schedules may both claim a product kind and nothing resolved which wins — a silent double-recognition, which is the worst kind of … |
| Recognition site | chip: Sale, Admission, Consumption | Where revenue is earned, which is not always where it was sold. A ticket sold at one venue and admitted at another earns at the gate, and … |
| Frequency | chip: Daily, Weekly, Monthly, On event, On period close | Driven by the schedule rather than by whoever runs the job. Recognition that happens when somebody remembers is recognition with no cut-off. |
| Revalidate on validity change | yes / no (icon or chip) | Changing an entitlement's validity did not re-time its deferred balance. A pass extended by three months has three more months of deferral … |
| Product kinds | list or chips (count when long) | The product kinds this schedule claims, from the catalogue's `ProductKind`. |
| Deferred account | the name it points at, never the id | — |
| Recognised account | the name it points at, never the id | — |
| Breakage account | the name it points at, never the id | — |
| No show trigger | chip: Performance end, Validity end, None | 8.1.1. A no-show is breakage with a known moment, and the mechanism already existed — `breakageAfterDays` moves deferred revenue to earned … |

**The selected recognition schedule** (detail panel, from `listRecognitionSchedules`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Method | chip: Immediate, On redemption, Straight line, Per visit, On expiry | — |
| Priority | 1,234 | Two schedules may both claim a product kind and nothing resolved which wins — a silent double-recognition, which is the worst kind of … |
| Recognition site | chip: Sale, Admission, Consumption | Where revenue is earned, which is not always where it was sold. A ticket sold at one venue and admitted at another earns at the gate, and … |
| Frequency | chip: Daily, Weekly, Monthly, On event, On period close | Driven by the schedule rather than by whoever runs the job. Recognition that happens when somebody remembers is recognition with no cut-off. |
| Revalidate on validity change | yes / no (icon or chip) | Changing an entitlement's validity did not re-time its deferred balance. A pass extended by three months has three more months of deferral … |
| Product kinds | list or chips (count when long) | The product kinds this schedule claims, from the catalogue's `ProductKind`. |
| Deferred account | the name it points at, never the id | — |
| Recognised account | the name it points at, never the id | — |
| Breakage account | the name it points at, never the id | — |
| No show trigger | chip: Performance end, Validity end, None | 8.1.1. A no-show is breakage with a known moment, and the mechanism already existed — `breakageAfterDays` moves deferred revenue to earned … |
| No show account | the name it points at, never the id | Where no-show revenue lands. Separate from `recognisedAccountId` by default, because revenue from a guest who came and revenue from one who … |
| Breakage after days | 1,234 | Days after expiry at which unredeemed value becomes breakage. |
| Is active | yes / no (icon or chip) | — |

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `getDeferredRevenue` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An active schedule at the same `priority` already claims one of these product kinds.; 409 Period already closed, or a run is in progress |

#### Permissions

- `getDeferredRevenue` → `LEDGER_VIEW` (read) · staff
- `runRecognition` → `LEDGER_POST` (operate) · staff
- `listRecognitionSchedules` → `LEDGER_VIEW` (read) · staff
- `createRecognitionSchedule` → `ACCOUNT_CONFIGURE` (configure) · staff
- `validateRecognitionSchedules` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `getDeferredRevenue` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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
- [ ] Every output is drawn (31 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-076?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run recognition, Create recognition schedule, Validate recognition schedules.
- [ ] Every transition is wired: `BO-074`, `BO-075`, `BO-077`.
- [ ] Every gated control is gated: `ACCOUNT_CONFIGURE`, `LEDGER_POST`, `LEDGER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-077` FX Rates & Variances

**Rates, and the price variances waiting for review.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 2 · needs the `core` module |
| Block | Block A · ticket #17838 (APP-SETUP-BO-077) |
| Who uses it | venue staff holding `LEDGER_APPROVE`, `LEDGER_VIEW` (1 operate, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `reviewPriceVariance` decides items that `listFxRates` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `varianceId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/finance/fx-rates-variances` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| As at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?asAt=` to `listFxRates`. | `listFxRates` ?asAt |
| Purpose | radio group | optional | — | Tender · Inter entity · Reporting · Revaluation | — | Sends `?purpose=` to `listFxRates`. | `listFxRates` ?purpose |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
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

**Form: Save FX rate** (modal, opened by *Save FX rate*; *Save FX rate* calls `setFxRate`, *Cancel* sends nothing)

**Collects what `setFxRate` sends before it is called.** Required: `fromCurrency`, `toCurrency`, `rate`, `purpose`, `effectiveFrom`. Optional: `id`, `source`, `effectiveTo`, `setByPrincipalId`, `providerReference`, `fetchedAt`. Dismissing sends nothing; the screen behind is unchanged.

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

**Form: Review price variance** (modal, opened by *Review price variance*; *Review price variance* calls `reviewPriceVariance`, *Cancel* sends nothing)

**Collects what `reviewPriceVariance` sends before it is called.** Required: `outcome`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | segmented control | required | — | Accepted · Investigated · Catalogue corrected | — | — | `reviewPriceVariance` body |
| Note `note` | text area | required | — | min length 3; max length 1000 | — | — | `reviewPriceVariance` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The variance is not awaiting review: its `reviewStatus` is `notRequired` (below the venue's threshold) or already `reviewed`.

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listFxRates`)

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

**Every price variance** (data table, from `listPriceVariances`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Order | the name it points at, never the id | — |
| Order line | text | — |
| Venue | the name it points at, never the id | — |
| Variant | the name it points at, never the id | — |
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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listFxRates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 No `note` was given. A manual rate says where the figure came from (audit R127 (4)).; 409 Effective window overlaps an existing bounded rate for the same pair and purpose, or does not start after the rate in force; 409 No provider is assigned to this purpose in this region (`setFxProvider`).; 409 The variance is not awaiting review: its `reviewStatus` is `notRequired` (below the venue's … |

#### Permissions

- `listFxRates` → `LEDGER_VIEW` (read) · staff, guest
- `setFxRate` → `LEDGER_APPROVE` (operate) · staff
- `listPriceVariances` → `LEDGER_VIEW` (read) · staff
- `reviewPriceVariance` → `LEDGER_APPROVE` (operate) · staff
- `ingestFxRates` → `LEDGER_APPROVE` (operate) · staff, service

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listFxRates` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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
- ADR-0031 *Contention is leased, not locked — and where a lock is unavoidable it is named* (`docs/adr/0031-contention-and-locking.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-077?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save FX rate, Review price variance, Ingest FX rates.
- [ ] Every transition is wired: `BO-074`, `BO-075`.
- [ ] Every gated control is gated: `LEDGER_APPROVE`, `LEDGER_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-089` Journal Entries

**Every posting, and the ones waiting for approval.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_APPROVE`, `LEDGER_POST`, `LEDGER_VIEW` (2 operate, 1 read); in the flows as finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | approvalInbox (compact density): `approveJournalEntry` decides items that `listJournalEntries` queues — every row is waiting for a person, so the empty state is success |
| Offline | online only |
| Opens with | `entryId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/finance/journal-entries` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.

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

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listJournalEntries`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Entry number | text | Server-assigned, in sequence per legal entity per fiscal year (decided 28 September, audit R191), for example `JE-2026-000123`. |
| Fiscal period | the name it points at, never the id | — |
| Status | chip: Draft, Pending approval, Posted, Reversed | — |
| Source | chip: Manual, Order, Refund, Void, Shift, Recognition… | — |
| Source | text | The order, refund or run that generated this entry. |
| Description | text | — |
| Reference | text | — |
| Lines | list or chips (count when long) | — |
| Total debit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total credit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Posted by principal | the name it points at, never the id | — |

**The selected journal entry** (detail panel, from `getJournalEntry`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Entry number | text | Server-assigned, in sequence per legal entity per fiscal year (decided 28 September, audit R191), for example `JE-2026-000123`. |
| Fiscal period | the name it points at, never the id | — |
| Status | chip: Draft, Pending approval, Posted, Reversed | — |
| Source | chip: Manual, Order, Refund, Void, Shift, Recognition… | — |
| Source | text | The order, refund or run that generated this entry. |
| Description | text | — |
| Reference | text | — |
| Lines | list or chips (count when long) | — |
| Total debit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Total credit | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Posted by principal | the name it points at, never the id | — |
| Approved by principal | the name it points at, never the id | — |
| Reversal of entry | the name it points at, never the id | — |
| Reversed by entry | the name it points at, never the id | — |
| Posted at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create journal entry (primary button) | `createJournalEntry` POST `/journal-entries` | CreateJournalEntryRequest | JournalEntry | 400 Lines do not balance, or an account is not postable; 409 The fiscal period is not `open`. Postings stop once a close begins, so a `closing` period refuses them as a `closed` one does. | opens modal first |
| Approve journal entry (secondary button) | `approveJournalEntry` POST `/journal-entries/{entryId}/approve` | inline | JournalEntry | 403 Approver is the poster, or lacks LEDGER_APPROVE; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The entry is not awaiting approval (it is `posted` or … | step-up: mfa (Posts to the ledger. The entry is the record; there is no undo that is not another entry.); opens modal first |
| Reject journal (destructive button) | `rejectJournal` POST `/journal-entries/{entryId}/reject` | inline | JournalEntry | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The entry is not `pendingApproval`. | — |
| Reverse journal entry (destructive button) | `reverseJournalEntry` POST `/journal-entries/{entryId}/reverse` | inline | JournalEntry | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already reversed, not yet posted, or the target period is not `open`. Three causes, three types. | — |

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listJournalEntries` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Lines do not balance, or an account is not postable; 409 Already reversed, not yet posted, or the target period is not `open`. Three causes, three types.; 409 The entry is not `pendingApproval`.; 409 The entry is not awaiting approval (it is `posted` or `reversed` already; only a `draft` or `pendingApproval` entry is approved), or its fiscal period has … |

#### Permissions

- `listJournalEntries` → `LEDGER_VIEW` (read) · staff
- `getJournalEntry` → `LEDGER_VIEW` (read) · staff
- `createJournalEntry` → `LEDGER_POST` (operate) · staff
- `approveJournalEntry` → `LEDGER_APPROVE` (operate) · staff · step-up mfa
- `rejectJournal` → `LEDGER_APPROVE` (operate) · staff
- `reverseJournalEntry` → `LEDGER_APPROVE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listJournalEntries` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-089?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create journal entry, Approve journal entry, Reject journal, Reverse journal entry.
- [ ] Every transition is wired: `BO-090`, `BO-074`, `BO-075`.
- [ ] Every gated control is gated: `LEDGER_APPROVE`, `LEDGER_POST`, `LEDGER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-090` Period Close

**Close a fiscal period, and see what is stopping it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `LEDGER_APPROVE`, `LEDGER_VIEW` (1 operate, 1 read); in the flows as finance controller |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listFiscalPeriods` reads the population and `getTrialBalance` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `periodId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/finance/period-close` |

**What the spec says about it.** Added 17 August because the contract had operations no screen declared. **Not on the wireframe board** — needs drawing.

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
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `LEDGER_VIEW`, which `listFiscalPeriods` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The period is already `closed`, or one or more of the close checks failed. The checks are exactly the values of `PeriodCloseResult.checks[].check` … (PeriodCloseProblem); 409 The period is not `closed`.; 409 The period is not `closing`.; 409 The period is not `open`. |

#### Permissions

- `listFiscalPeriods` → `LEDGER_VIEW` (read) · staff
- `beginPeriodClose` → `LEDGER_APPROVE` (operate) · staff
- `closeFiscalPeriod` → `LEDGER_APPROVE` (operate) · staff
- `abandonPeriodClose` → `LEDGER_APPROVE` (operate) · staff
- `reopenPeriod` → `LEDGER_APPROVE` (operate) · staff
- `getTrialBalance` → `LEDGER_VIEW` (read) · staff
- `getVatReturn` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `LEDGER_VIEW`, which `listFiscalPeriods` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

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
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-101` Orders & Money

**Everything in orders & money, and what in it needs attention.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Orders & Money · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ORDER_VIEW`, `SETTLEMENT_VIEW`, `TENANT_VIEW` (3 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listOrders` reads the population and `getVenueSettings` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session) · cold entry: **Resolves from the session, so a cold arrival is the ordinary case** — a manager bookmarks the back office and opens it every morning. A principal with more … |
| Route | `/orders-money` |

**What the spec says about it.** Section landing. **28 screens reach the entry point through here** — before 20 August they reached it through nothing. **Given its section's own operations on 4 September.** It sat on `getVenueSettings` alone, which made it identical to every other section landing page — a hub that shows nothing of its section is a menu item, not a screen.

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
| ID | the name it points at, never the id | — |
| Order number | text | — |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | The same vocabulary as `Order.channel`, which this projects. |
| Line count | 1,234 | — |

**Every settlement** (data table, from `listSettlements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Currency code | text | A settlement has no account, so nothing else denominates it. A posting takes its currency from `ledger.account.currency` and a payment from … |
| Provider name | text | — |
| Period start | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| Period end | 1 Oct 2026 | A day in the region's time zone, local midnight to local midnight. |
| File reference | the name it points at, never the id | The `MediaAsset` holding the provider file, as given to `ingestSettlementFile`. Kept on the row because parsing is asynchronous: the job … |
| Format | chip: Csv, Fixed width, Xml, Json | The file format given at ingest. Null when none was given. |
| Status | chip: Ingesting, Parsing, Matching, Matched, Has exceptions, Resolved… | — |
| Line count | 1,234 | — |
| Matched count | 1,234 | — |
| Exception count | 1,234 | — |
| Provider gross | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

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

**The venue settings** (detail panel, from `getVenueSettings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Segregated access | grouped details | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a … |
| Alerting | grouped details | CF-134. On-platform notification, marked as read. |

**Data it reads**: `getVenueSettings` (onLoad, What is enabled here); `listOrders` (onLoad, Orders taken in this venue); `listSettlements` (onLoad, Money settled and what is outstanding)

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

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The list, with counts. |
| Error (`?state=error`) | Could not load. Venue Home is still reachable. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing configured in orders & money yet.** The action is the first thing to set up, not a blank list. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter. |
| Permission denied (`?state=emptyNoAccess`) | You do not have permission for orders & money. **Said plainly** — an empty section reads as broken. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getVenueSettings` → `TENANT_VIEW` (read) · staff
- `listOrders` → `ORDER_VIEW` (read) · staff, guest, partner
- `listSettlements` → `SETTLEMENT_VIEW` (read) · staff, partner

**A refused user sees:** You do not have permission for orders & money. **Said plainly** — an empty section reads as broken.

#### Requirements it meets

22 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.3.7 | The system should allow access to their purchase history and ongoing orders and preferences. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 5.9.4 | The system should be able to provide a detailed log of transactions for each till. Detailed log of transaction should be always accessible, searchable and printable at back office. | F&B & Guest Management | CONTRACTED | `listOrders` |
| 22.2.11 | Ticketing History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.12 | Membership History | Marketing & CRM | CONTRACTED | `listOrders` |
| 22.2.15 | Reservation History | Marketing & CRM | CONTRACTED | `listOrders` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.17 | Approval Notifications - System shall notify approvers when new approval requests are assigned. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.18 | Approval Reminder Notifications - System shall send reminder notifications for pending approvals. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.19 | Approval Outcome Notifications - System shall notify requestors when approvals are approved, rejected or escalated. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| … 10 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 5 for P08 · Orders & Money, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-101` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (38 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-101?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-008`, `BO-022`, `BO-023`, `BO-024`, `BO-025`, `BO-026`, `BO-027`, `BO-029`, `BO-039`, `BO-040`, `BO-041`, `BO-042`, `BO-043`, `BO-047`, `BO-048`, `BO-059`, `BO-061`, `BO-062`, `BO-065`, `BO-074`, `BO-075`, `BO-077`, `BO-089`, `BO-090`.
- [ ] Every gated control is gated: `ORDER_VIEW`, `SETTLEMENT_VIEW`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
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

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

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
"createAccount": {"method":"POST","path":"/accounts","contract":"finance","summary":"Create an account","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateAccountRequest","responds":"Account"},
"createCostCenter": {"method":"POST","path":"/cost-centers","contract":"finance","summary":"Create a cost centre","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CostCenter"},
"createJournalEntry": {"method":"POST","path":"/journal-entries","contract":"finance","summary":"Post a manual journal voucher","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateJournalEntryRequest","responds":"JournalEntry"},
"createLegalEntity": {"method":"POST","path":"/legal-entities","contract":"finance","summary":"Create a legal entity","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LegalEntity","responds":"LegalEntity"},
"createRecognitionSchedule": {"method":"POST","path":"/recognition-schedules","contract":"finance","summary":"Define how a product class recognises revenue","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecognitionSchedule","responds":"RecognitionSchedule"},
"createTaxCode": {"method":"POST","path":"/tax-codes","contract":"finance","summary":"Create a tax code","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateTaxCodeRequest","responds":"TaxCode"},
"createTaxExemption": {"method":"POST","path":"/tax-exemptions","contract":"finance","summary":"Grant a tax exemption","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TaxExemption","responds":"TaxExemption"},
"getAccount": {"method":"GET","path":"/accounts/{accountId}","contract":"finance","summary":"Read an account","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"Account"},
"getDeferredRevenue": {"method":"GET","path":"/deferred-revenue","contract":"finance","summary":"Deferred revenue balance and ageing","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"asAt","in":"query","required":null},{"name":"venueId","in":"query","required":null}],"requestBody":null,"responds":"DeferredRevenueReport"},
"getJournalEntry": {"method":"GET","path":"/journal-entries/{entryId}","contract":"finance","summary":"Read a journal entry","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"JournalEntry"},
"getTrialBalance": {"method":"GET","path":"/ledger/trial-balance","contract":"finance","summary":"Trial balance for a period","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"fiscalPeriodId","in":"query","required":true},{"name":"legalEntityId","in":"query","required":null}],"requestBody":null,"responds":"TrialBalance"},
"getVatReturn": {"method":"GET","path":"/tax/vat-returns","contract":"finance","summary":"A legal entity's VAT return for a tax period, in the FTA's boxes","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":true},{"name":"periodFrom","in":"query","required":true},{"name":"periodTo","in":"query","required":true},{"name":"format","in":"query","required":null}],"requestBody":null,"responds":"FinVatReturn"},
"getVenueSettings": {"method":"GET","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Operational settings for this venue","permission":"TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"ingestFxRates": {"method":"POST","path":"/fx-rates/ingest","contract":"finance","summary":"Pull rates from the configured provider","permission":"LEDGER_APPROVE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listAccountMappings": {"method":"GET","path":"/account-mappings","contract":"finance","summary":"Which account each transaction type posts to","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAccounts": {"method":"GET","path":"/accounts","contract":"finance","summary":"List the chart of accounts","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":"type","in":"query","required":null},{"name":"isPostable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCostCenters": {"method":"GET","path":"/cost-centers","contract":"finance","summary":"List cost centres","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFiscalPeriods": {"method":"GET","path":"/fiscal-periods","contract":"finance","summary":"List fiscal periods","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFxRates": {"method":"GET","path":"/fx-rates","contract":"finance","summary":"The rates in force","permission":"LEDGER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"asAt","in":"query","required":null},{"name":"purpose","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listJournalEntries": {"method":"GET","path":"/journal-entries","contract":"finance","summary":"List journal entries","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"fiscalPeriodId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"source","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listLegalEntities": {"method":"GET","path":"/legal-entities","contract":"finance","summary":"List legal entities","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
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
"updateAccount": {"method":"PATCH","path":"/accounts/{accountId}","contract":"finance","summary":"Rename, remap or deactivate an account","permission":"ACCOUNT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Account"},
"updateTaxCode": {"method":"PATCH","path":"/tax-codes/{taxCodeId}","contract":"finance","summary":"Amend a tax code","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TaxCode"},
"validateRecognitionSchedules": {"method":"POST","path":"/recognition-schedules/validate","contract":"finance","summary":"Find product kinds claimed by more than one schedule","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"verifyTaxExemption": {"method":"POST","path":"/tax-exemptions/{exemptionId}/verify","contract":"finance","summary":"Record that a tax exemption's evidence was checked","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TaxExemption"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Account": {"x-ticvai-persistence":"ledger.account","type":"object","required":["id","code","name","type","legalEntityId","isPostable","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"externalCode":{"type":"string","nullable":true,"description":"Code in the client's own chart. Used on export so their team sees their codes."},"isSuspense":{"type":"boolean","default":false,"description":"5.7.x. **Where a posting with no account mapping goes.** Today it has no destination, and a posting event that cannot be booked is a posting event that is silently dropped.\n**A suspense balance is a work queue, not a resting place.** It should trend to zero, and a balance that grows is the signal that a mapping is missing — which is the whole reason for having one rather than refusing the posting.\n"},"subType":{"type":"string","nullable":true,"description":"5.7.27. **`AccountType` stays a closed enum of asset, liability, equity, revenue and expense because that is correct accounting**, and a venue wanting *Deferred Revenue — Annual Pass* is asking for a sub-type rather than a sixth type.\n"},"tags":{"type":"array","items":{"type":"string"},"description":"How a venue groups accounts for its own reporting. Free-form, and outside the type."},"notes":{"type":"string","nullable":true,"description":"5.7.27. Annotations on the account, which an auditor reads before the balance."},"name":{"type":"string","maxLength":200},"type":{"$ref":"#/components/schemas/AccountType"},"parentId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"isPostable":{"type":"boolean","description":"False for parent accounts, which aggregate only."},"isActive":{"type":"boolean"},"balance":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"AccountMapping": {"x-ticvai-persistence":"ledger.account_mapping","type":"object","required":["eventType","debitAccountId","creditAccountId"],"properties":{"eventType":{"$ref":"#/components/schemas/PostingEventType"},"debitAccountId":{"type":"string","format":"uuid"},"creditAccountId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Null applies the mapping to every venue in the region."}}},
"AccountType": {"type":"string","enum":["asset","liability","equity","revenue","expense"]},
"CostCenter": {"x-ticvai-persistence":"ledger.cost_center","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"parentId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean"}}},
"CreateAccountRequest": {"type":"object","required":["code","name","type","legalEntityId"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9._-]+$"},"externalCode":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"type":{"$ref":"#/components/schemas/AccountType"},"parentId":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid"},"isPostable":{"type":"boolean","default":true},"isSuspense":{"type":"boolean","default":false,"description":"See `Account.isSuspense`."},"subType":{"type":"string","nullable":true,"description":"See `Account.subType`."},"tags":{"type":"array","items":{"type":"string"},"description":"See `Account.tags`."},"notes":{"type":"string","nullable":true,"description":"See `Account.notes`."}}},
"CreateJournalEntryRequest": {"type":"object","required":["id","fiscalPeriodId","description","lines"],"properties":{"id":{"type":"string","format":"uuid"},"fiscalPeriodId":{"type":"string","format":"uuid"},"postingDate":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"description":{"type":"string","minLength":3,"maxLength":500},"reference":{"type":"string","maxLength":128},"lines":{"type":"array","minItems":2,"items":{"$ref":"#/components/schemas/JournalLine"}}}},
"CreateTaxCodeRequest": {"type":"object","required":["code","name","countryCode","rate","effectiveFrom","accountId"],"properties":{"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$"},"rate":{"type":"number","minimum":0,"maximum":100},"compoundOnTaxCodeId":{"type":"string","format":"uuid"},"isInclusive":{"type":"boolean","default":false},"accountId":{"type":"string","format":"uuid"},"effectiveFrom":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."}}},
"DeferredRevenueReport": {"x-ticvai-persistence":"none — computed","type":"object","required":["asAt","totals","buckets"],"properties":{"asAt":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"totals":{"type":"array","description":"**One `Money` per currency in scope**, never a sum across currencies. One entry when every venue in scope trades in the same currency.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/Money"}},"total":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"The single total when everything in scope is in one currency; null otherwise. Read `totals`."},"buckets":{"type":"array","description":"One ageing band in one currency per entry. A band spanning two currencies is two entries.","items":{"type":"object","required":["label","amount","itemCount"],"properties":{"label":{"type":"string","description":"Ageing band by expected recognition date."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"itemCount":{"type":"integer"},"method":{"$ref":"#/components/schemas/RecognitionMethod"}}}}}},
"FinVatReturn": {"x-ticvai-persistence":"none — computed from ledger postings on the reporting replica","type":"object","description":"6.1.23. The FTA VAT 201 boxes for one legal entity and tax period.","required":["legalEntityId","periodFrom","periodTo","boxes","netTaxPayable"],"properties":{"legalEntityId":{"type":"string","format":"uuid"},"taxRegistrationNumber":{"type":"string"},"periodFrom":{"type":"string","format":"date"},"periodTo":{"type":"string","format":"date"},"boxes":{"type":"array","items":{"type":"object","required":["box","amount","taxAmount"],"properties":{"box":{"type":"string","description":"The form's box, e.g. `1a` (standard-rated supplies, Abu Dhabi) ... `1g`, `2` (tourist refunds), `3` (reverse charge), `4` (zero-rated), `5` (exempt), `6` and `7` (imports), `9` (standard-rated expenses), `10` (reverse charge inputs)."},"label":{"type":"string"},"emirate":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"adjustmentAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"postingCount":{"type":"integer"}}}},"totalOutputTax":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRecoverableTax":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netTaxPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fileUrl":{"type":"string","format":"uri","nullable":true,"description":"Set for `format` `csv` or `xlsx`; a short-lived link."},"generatedAt":{"type":"string","format":"date-time"}}},
"FiscalPeriod": {"x-ticvai-persistence":"ledger.fiscal_period + ledger.fiscal_period_event","type":"object","description":"`startDate` and `endDate` are days in the region's time zone: a posting belongs to the period when its `postedAt`, in that zone, falls on or between them.\n","required":["id","legalEntityId","name","startDate","endDate","status"],"properties":{"id":{"type":"string","format":"uuid"},"legalEntityId":{"type":"string","format":"uuid"},"name":{"type":"string"},"startDate":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"endDate":{"type":"string","format":"date","description":"A day in the region's time zone, local midnight to local midnight."},"status":{"$ref":"#/components/schemas/PeriodStatus"},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"closedAt":{"type":"string","format":"date-time","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The approval request a close or reopen is waiting on (`approvals`), routed to a finance approver (decided 28 September, audit R144). Null when nothing is waiting."},"events":{"type":"array","description":"**Every step of the period's close, oldest first**: begin, abandon, close and reopen, each with who, when and (for abandon and reopen) why. A reopened period restates figures somebody has already reported, so the reason is kept, not just the latest status.\n","items":{"$ref":"#/components/schemas/FiscalPeriodEvent"}}}},
"FiscalPeriodEvent": {"type":"object","description":"One step in a fiscal period's close. Written by the operation that took the step; never edited.","required":["action","principalId","occurredAt"],"properties":{"action":{"type":"string","enum":["beginClose","abandonClose","close","reopen"]},"reason":{"type":"string","nullable":true,"description":"Required by `abandonPeriodClose` and `reopenPeriod`; null for the other steps."},"principalId":{"type":"string","format":"uuid","description":"Who took the step."},"approverPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The approver of a `reopen`. Null for the other steps."},"occurredAt":{"type":"string","format":"date-time"}}},
"FxRate": {"type":"object","x-ticvai-persistence":"ledger.fx_rate","description":"Also the `setFxRate` body. **Server-owned fields are `readOnly`** and ignored if sent: `id`, `setByPrincipalId`, and the provenance `ingestFxRates` writes (`source`, `providerReference`, `fetchedAt`). A rate set through `setFxRate` has `source` `manual`.\n","required":["fromCurrency","toCurrency","rate","purpose","effectiveFrom"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"fromCurrency":{"type":"string","pattern":"^[A-Z]{3}$"},"toCurrency":{"type":"string","pattern":"^[A-Z]{3}$"},"rate":{"allOf":[{"$ref":"#/components/schemas/FxRateValue"}],"description":"Units of `toCurrency` per one `fromCurrency`. Six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly.\n"},"purpose":{"$ref":"#/components/schemas/FxRatePurpose"},"source":{"allOf":[{"$ref":"#/components/schemas/FxRateSource"}],"readOnly":true},"effectiveFrom":{"type":"string","format":"date-time"},"effectiveTo":{"type":"string","format":"date-time","nullable":true,"description":"A rate change is a new row. The old one is never edited — a transaction posted last Tuesday must still reconcile at last Tuesday's rate.\n"},"setByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"note":{"type":"string","maxLength":500,"nullable":true,"description":"Why this rate, and from where. **Required when `source` is `manual`** (decided 28 September, audit R127 (4)); null on a rate `ingestFxRates` fetched."},"providerReference":{"type":"string","nullable":true,"readOnly":true,"description":"The provider's own identifier for this quote. **What makes a rate reproducible** — an auditor asking why a payment converted at 3.6725 gets an answer that is checkable against the source rather than a number somebody typed."},"fetchedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the rate was pulled. **Distinct from `effectiveFrom`**, which is when it applies — a rate fetched at 06:00 for a business day starting at 00:00 has two different times and conflating them makes a late feed look like a backdated rate."}}},
"FxRatePurpose": {"type":"string","description":"A venue does not accept dollars at the rate it books an intercompany balance at. Separating them is what stops a spread on the counter appearing as a loss in the accounts.\n","enum":["tender","interEntity","reporting","revaluation"]},
"FxRateSource": {"type":"string","description":"**Where the rate came from, and which provider specifically.** `source: provider` said a feed set it and not which one — two tenants on different feeds were indistinguishable in the ledger, and a rate cannot be defended in an audit without naming its origin.\n\n**`uaeCentralBank` is the default for AED pairs.** The UAE Central Bank publishes an official daily rate and it is what a UAE auditor expects to see — a commercial feed is defensible for tender and awkward for statutory reporting.\n\n**`openExchangeRates` and `ecb` are the commercial and reference options.** ECB publishes daily reference rates free and is the usual fallback for non-AED pairs; Open Exchange Rates is the common commercial feed with intraday granularity. **The choice is per purpose, not per platform** — a tender rate wants intraday, a reporting rate wants the official daily close.","enum":["manual","uaeCentralBank","ecb","openExchangeRates","cardScheme","provider"]},
"FxRateValue": {"x-ticvai-persistence-column":"numeric(18,6)","type":"string","pattern":"^\\d+(\\.\\d{1,6})?$","description":"**An exchange rate: a decimal string, never a float**, for the reason `Money.amount` is one (naming-and-style 5.1). Up to six decimal places — a two-place rate on a three-place currency loses money on every transaction, quietly — and stored as `numeric(18,6)` so the six places the wire carries survive the database.\n"},
"JournalEntry": {"x-ticvai-persistence":"ledger.journal_entry + ledger.journal_line","type":"object","required":["id","entryNumber","fiscalPeriodId","status","source","description","lines","totalDebit","totalCredit","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"entryNumber":{"type":"string","readOnly":true,"description":"Server-assigned, **in sequence per legal entity per fiscal year** (decided 28 September, audit R191), for example `JE-2026-000123`. Gapless within the legal entity and year: a number is taken when the entry reaches the ledger, not when a draft is saved.\n"},"fiscalPeriodId":{"type":"string","format":"uuid"},"status":{"$ref":"#/components/schemas/JournalStatus"},"source":{"$ref":"#/components/schemas/JournalSource"},"sourceId":{"type":"string","nullable":true,"description":"The order, refund or run that generated this entry."},"description":{"type":"string"},"reference":{"type":"string","nullable":true},"lines":{"type":"array","items":{"$ref":"#/components/schemas/JournalLine"}},"totalDebit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCredit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"postedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"reversalOfEntryId":{"type":"string","format":"uuid","nullable":true},"reversedByEntryId":{"type":"string","format":"uuid","nullable":true},"reversalReason":{"type":"string","nullable":true,"description":"On a reversal, the `reason` given to `reverseJournalEntry`. Null on every other entry."},"rejectionReason":{"type":"string","nullable":true,"description":"The comment from the latest `rejectJournal`, which the preparer reads before resubmitting. Null until an entry is rejected.\n"},"rejectedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"rejectedAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"postedAt":{"type":"string","format":"date-time","nullable":true}}},
"JournalLine": {"x-ticvai-append-only":"postedAt","type":"object","required":["accountId","debit","credit"],"properties":{"accountId":{"type":"string","format":"uuid"},"debit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"credit":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"venueId":{"type":"string","format":"uuid","nullable":true},"costCenterId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string","maxLength":500},"postedAt":{"type":"string","format":"date-time","readOnly":true,"description":"**Copied from the journal entry when it posts** (ADR-0056), so the line table can be partitioned by month on its own column. Never differs from its entry's."}}},
"JournalSource": {"type":"string","enum":["manual","order","refund","void","shift","recognition","settlement","variance","reversal","writeOff","chargeback"]},
"JournalStatus": {"type":"string","enum":["draft","pendingApproval","posted","reversed"]},
"LegalEntity": {"x-ticvai-persistence":"ledger.legal_entity","type":"object","description":"Also the `createLegalEntity` body. **`id` and `scopePath` are server-owned** (`readOnly`) and ignored if sent.\n","required":["id","code","name","countryCode","currency","currencyScale","fiscalYearStartMonth"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"taxRegistrationNumber":{"type":"string","nullable":true},"fiscalYearStartMonth":{"type":"integer","minimum":1,"maximum":12},"regionIds":{"type":"array","items":{"type":"string","format":"uuid"}},"isActive":{"type":"boolean"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"OrderSummary": {"x-ticvai-persistence":"none — projection","type":"object","required":["id","orderNumber","status","grossAmount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderNumber":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"The same vocabulary as `Order.channel`, which this projects."},"lineCount":{"type":"integer"},"principalId":{"type":"string","format":"uuid","description":"The cashier who raised it — what the held-orders list shows."},"holdLabel":{"type":"string","nullable":true,"description":"As `Order.holdLabel`."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"description":"As `Order.heldUntil`, so a held-orders list can warn about the ones about to lapse."},"createdAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PeriodCloseResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["fiscalPeriodId","dryRun","passed","checks"],"properties":{"fiscalPeriodId":{"type":"string","format":"uuid"},"dryRun":{"type":"boolean"},"passed":{"type":"boolean"},"checks":{"type":"array","items":{"type":"object","required":["check","passed"],"properties":{"check":{"type":"string","enum":["trialBalanceBalances","noUnapprovedJournals","noOpenShifts","settlementsReconciled","recognitionRunComplete","priorPeriodClosed","varianceExceptionsReviewed"]},"passed":{"type":"boolean"},"detail":{"type":"string"},"blockingCount":{"type":"integer"}}}}}},
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
"VarianceReviewStatus": {"type":"string","enum":["notRequired","pendingReview","reviewed"]},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}}
}
```
