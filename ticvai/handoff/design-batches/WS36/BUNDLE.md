# WS36 — Pricing   Revenue Management board 3

**10 screens · 21 operations · 31 schemas · 6 permissions**

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
  `LEDGER_POST, LEDGER_VIEW, PRICE_CONFIGURE, PRODUCT_CONFIGURE, PRODUCT_VIEW, TAX_CONFIGURE`. A control nobody can use must say so,
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
| `ADM-068` | Tax, Fee & Calculation Command Center | B–D | 2 | 258 | 6 | 1 | 1 | 0 | — | notStarted (generated) |
| `ADM-069` | Tax Profile & Jurisdiction Configuration | A | 12 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-070` | Tax Rule & Treatment Builder | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-071` | Fee & Surcharge Library | B–D | 30 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-072` | Fee Applicability & Charging Rule Builder | B–D | 5 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-073` | Fee Waiver, Tax Exemption & Exception Rules | B–D | 11 | 0 | 5 | 0 | 1 | 4 | — | notStarted (generated) |
| `ADM-074` | Price Calculation Sequence & Formula Engine | B–D | 25 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-075` | Currency Precision, Rounding & Monetary Rules | A | 11 | 2 | 6 | 0 | 0 | 4 | — | notStarted (generated) |
| `ADM-076` | Price Breakdown, Calculation Simulation & Explainability | B–D | 13 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-077` | Calculation Validation, Reconciliation & Service Interface | A | 0 | 0 | 6 | 1 | 0 | 6 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-077 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-068` Tax, Fee & Calculation Command Center

**Provide Finance, Commercial and Pricing administrators with one central view of TICVAI's price-calculation configuration.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `LEDGER_VIEW`, `PRODUCT_VIEW` (2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/tax-fee-calculation-command-center-adm-068` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Create Tax Profile, Create Fee, Create Calculation Profile, Run Simulation, Validate Configuration, View …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search tax fee calculation | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tax, fee, surcharge, waiver, exemption, calculation profile and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Type | select | — | Tax · Fee · Surcharge · Waiver · Exemption · Calculation profile · Rounding profile | `listTaxFeeCalculation` ?type |
| Country | text field | — | — | `listTaxFeeCalculation` ?country |
| Legal entity | text field | — | — | `listTaxFeeCalculation` ?legalEntity |
| Status | radio group | — | Draft · Active · Inactive · Expired | `listTaxFeeCalculation` ?status |
| Search | text field | — | — | `listTaxFeeCalculation` ?search |
| Order | picker: choose an order | — | — | `listTaxInvoices` ?orderId |
| Legal entity | picker: choose a legal entity | — | — | `listTaxInvoices` ?legalEntityId |
| Invoice type | segmented control | — | Simplified · Full · Consolidated | `listTaxInvoices` ?invoiceType |
| Status | radio group | — | Issued · Partially credited · Fully credited · Superseded | `listTaxInvoices` ?status |
| Issued from | date picker | — | — | `listTaxInvoices` ?issuedFrom |
| Issued to | date picker | — | — | `listTaxInvoices` ?issuedTo |
| Legal entity | picker: choose a legal entity | — | — | `getVatReturn` ?legalEntityId |
| Period from | date picker | — | — | `getVatReturn` ?periodFrom |
| Period to | date picker | — | — | `getVatReturn` ?periodTo |
| Format | segmented control | Json | Json · Csv · Xlsx | `getVatReturn` ?format |

#### Outputs: what the screen shows and produces

**Shown**

**Active Tax Profiles** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Tax Jurisdictions** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Active Fee Profiles** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Active Surcharges** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Exemption Rules** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Calculation Profiles** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Products missing tax** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Products Missing Calculation Profile** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Configuration Conflicts** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Upcoming Tax Changes** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Validation Issues** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Recently modified rules** (metric tile, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |
| Profile | text | ID of the tax profile, fee, rule or profile |
| Effective from | 1 Oct 2026 | Effective From |
| Effective to | 1 Oct 2026 | Effective To; empty for open-ended |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The headline figures on Tax, Fee & Calculation Command Center. The pack's KPI cards, split out of the row (decided 29 September, readiness … |
| Active tax profiles | 1,234 | Active Tax Profiles |
| Tax jurisdictions | 1,234 | Tax Jurisdictions |
| Active fee profiles | 1,234 | Active Fee Profiles |
| Active surcharges | 1,234 | Active Surcharges |

**Every tax fee calculation** (data table, from `listTaxFeeCalculation`)

| Shows | Format | Notes |
|---|---|---|
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |

**The selected tax fee calculation** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Profile name | text | Profile Name |
| Type | chip: Tax, Fee, Surcharge, Waiver, Exemption, Calculation profile… | Configuration Type (p.39) |
| Country | text | Country |
| Legal entity | text | Legal Entity |
| Market | text | Market |
| Currency | text | Currency: ISO 4217 code |
| Product scope | text | Product Scope |
| Status | text | Status: draft, active, inactive or expired |
| Owner | text | Owner |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create Tax Profile (primary button) | navigation or local | — | — | — | — |
| Create Fee (secondary button) | navigation or local | — | — | — | — |
| Create Calculation Profile (secondary button) | navigation or local | — | — | — | — |
| Run Simulation (secondary button) | navigation or local | — | — | — | — |
| Validate Configuration (secondary button) | navigation or local | — | — | — | — |
| View Dependencies (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listTaxFeeCalculation` (onLoad, Tax, Fee & Calculation Command Center); `listTaxInvoices` (onLoad, List tax invoices); `getVatReturn` (onLoad, VAT return (FTA boxes) for a period)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-069` Tax Profile & Jurisdiction Configuration: *Works in Tax Profile & Jurisdiction Configuration*; calls `listTaxFeeCalculation`
- → `ADM-070` Tax Rule & Treatment Builder: *Works in Tax Rule & Treatment Builder*; calls `listTaxFeeCalculation`
- → `ADM-071` Fee & Surcharge Library: *Works in Fee & Surcharge Library*; calls `listTaxFeeCalculation`
- → `ADM-072` Fee Applicability & Charging Rule Builder: *Works in Fee Applicability & Charging Rule Builder*; calls `listTaxFeeCalculation`
- → `ADM-073` Fee Waiver, Tax Exemption & Exception Rules: *Works in Fee Waiver, Tax Exemption & Exception Rules*; calls `listTaxFeeCalculation`
- → `ADM-074` Price Calculation Sequence & Formula Engine: *Works in Price Calculation Sequence & Formula Engine*; calls `listTaxFeeCalculation`
- → `ADM-075` Currency Precision, Rounding & Monetary Rules: *Works in Currency Precision, Rounding & Monetary Rules*; calls `listTaxFeeCalculation`
- → `ADM-076` Price Breakdown, Calculation Simulation & Explainability: *Works in Price Breakdown, Calculation Simulation & Explainability*; calls `listTaxFeeCalculation`
- → `ADM-077` Calculation Validation, Reconciliation & Service Interface: *Works in Calculation Validation, Reconciliation & Service Interface*; calls `listTaxFeeCalculation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tax fee calculation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tax fee calculation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tax fee calculation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the tax fee calculation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The period is not whole tax months, or the legal entity has no tax registration number. |

#### Permissions

- `listTaxFeeCalculation` → `PRODUCT_VIEW` (read) · staff
- `listTaxInvoices` → `LEDGER_VIEW` (read) · staff, guest
- `getVatReturn` → `LEDGER_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.23 | The system should be able to tax reports in approved government formats for submittal. | Retail POS | CONTRACTED | `getVatReturn` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-068` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-068`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 1: Opens Tax, Fee & Calculation Command Center → Provide Finance, Commercial and Pricing administrators with one central view of TICVAI's price-calculation configuration.
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F145 branch at step 1 (expected): when Nothing has been set up on Tax, Fee & Calculation Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F145 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (258 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-068?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create Tax Profile, Create Fee, Create Calculation Profile, Run Simulation, Validate Configuration, View Dependencies.
- [ ] Every transition is wired: `ADM-002`, `ADM-069`, `ADM-070`, `ADM-071`, `ADM-072`, `ADM-073`, `ADM-074`, `ADM-075`, `ADM-076`, `ADM-077`.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-069` Tax Profile & Jurisdiction Configuration

**Define reusable tax profiles according to legal entity, country, jurisdiction and commercial context.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block A · ticket #20665 (APP-SETUP-ADM-069) |
| Who uses it | ticvai staff holding `LEDGER_VIEW`, `PRODUCT_CONFIGURE`, `TAX_CONFIGURE` (1 read, 2 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/tax-profile-jurisdiction-configuration-adm-069` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Sales Tax, Entertainment Tax, Tourism Tax, Municipality Tax, Service Tax. Each needs an operation, or needs …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tax Profile Name | select field | — | — | — | — | — | — |
| Tax Profile Code | select field | — | — | — | — | — | — |
| Tax Type | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Region/Jurisdiction | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Tax Registration Number | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Effective From | select field | — | — | — | — | — | — |
| Effective To | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Legal entity | picker: choose a legal entity | — | — | `listTaxInvoiceTemplates` ?legalEntityId |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sales Tax (primary button) | navigation or local | — | — | — | — |
| Entertainment Tax (secondary button) | navigation or local | — | — | — | — |
| Tourism Tax (secondary button) | navigation or local | — | — | — | — |
| Municipality Tax (secondary button) | navigation or local | — | — | — | — |
| Service Tax (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listTaxInvoiceTemplates` (onLoad, Show invoice templates and number series); `listEInvoicingProviders` (onLoad, Show the e-invoicing provider connection)

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `setTaxProfileJurisdiction`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tax profile jurisdiction configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tax profile jurisdiction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tax profile jurisdiction configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `live` requested before any `test` transmission from this legal entity was accepted.; 422 `nextNumber` below the last number issued in the series, or a language the legal entity's region does not offer. |

#### Permissions

- `setTaxProfileJurisdiction` → `PRODUCT_CONFIGURE` (configure) · staff
- `listTaxInvoiceTemplates` → `LEDGER_VIEW` (read) · staff
- `setTaxInvoiceTemplate` → `TAX_CONFIGURE` (configure) · staff
- `listEInvoicingProviders` → `LEDGER_VIEW` (read) · staff
- `setEInvoicingProvider` → `TAX_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Taxes inclusive or exclusive at product or category level; tax profiles combine several taxes incl. tax-on-tax (e.g. Egypt); per-product/transaction tax exemption flag. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-596)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-069` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-069`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 2: Works in Tax Profile & Jurisdiction Configuration → Define reusable tax profiles according to legal entity, country, jurisdiction and commercial context.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-069?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sales Tax, Entertainment Tax, Tourism Tax, Municipality Tax, Service Tax.
- [ ] Every transition is wired: `ADM-068`.
- [ ] Every gated control is gated: `LEDGER_VIEW`, `PRODUCT_CONFIGURE`, `TAX_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-070` Tax Rule & Treatment Builder

**Define how taxes are applied to products and transactions.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/tax-rule-treatment-builder-adm-070` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Out of Scope, Fixed Tax. Each needs an operation, or needs removing from the screen; this is the Phase 3 … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Tax Inclusive (primary button) | navigation or local | — | — | — | — |
| Tax Exclusive (secondary button) | navigation or local | — | — | — | — |
| Tax Exempt (secondary button) | navigation or local | — | — | — | — |
| Out of Scope (secondary button) | navigation or local | — | — | — | — |
| Fixed Tax (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `setTaxRuleTreatment`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tax rule treatment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tax rule treatment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tax rule treatment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the tax rule treatment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setTaxRuleTreatment` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Taxes inclusive or exclusive at product or category level; tax profiles combine several taxes incl. tax-on-tax (e.g. Egypt); per-product/transaction tax exemption flag. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-596)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-070` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-070`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 4: Works in Tax Rule & Treatment Builder → Define how taxes are applied to products and transactions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-070?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Tax Inclusive, Tax Exclusive, Tax Exempt, Out of Scope, Fixed Tax.
- [ ] Every transition is wired: `ADM-068`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-071` Fee & Surcharge Library

**Create standardized reusable non-base-price charges.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture; Configure whether the fee is) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/fee-surcharge-library-adm-071` |

**Known gaps.** **The pack names 18 actions on this screen; 8 are served since the writers pass (29 September): Booking Fee, Transaction Fee, Service Fee, Convenience Fee, Delivery Fee, Handling Fee, Modification …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Fee Name | select field | — | — | — | — | — | — |
| Fee Code | select field | — | — | — | — | — | — |
| Fee Type | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Calculation Method | select field | — | — | — | — | — | — |
| Value | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Tax Treatment | select field | — | — | — | — | — | — |
| Refundability | select field | — | — | — | — | — | — |
| Effective Period | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Customer Visible | select field | — | — | — | — | — | — |
| Included in Display Price | text field | — | — | — | — | — | — |
| Shown Separately | select field | — | — | — | — | — | — |
| Internal Only | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Fee type | select | — | Booking fee · Transaction fee · Service fee · Convenience fee · Delivery fee · Handling fee · Modification fee · Rescheduling fee · Cancellation fee · Refund fee · Payment fee · Channel fee … | `listFeeSurcharge` ?feeType |
| Status | radio group | — | Draft · Active · Inactive · Expired | `listFeeSurcharge` ?status |
| Search | text field | — | — | `listFeeSurcharge` ?search |

**Form: Save fee definition** (modal, opened by *Save fee definition*; *Save fee definition* calls `setFeeDefinition`, *Cancel* sends nothing)

**Collects what `setFeeDefinition` sends before it is called.** Required: `id`, `scopePath`, `code`, `name`, `feeType`, `valueType`, `chargeBasis`, `status`. Optional: `description`, `amount`, `percentage`, `tiers`, `taxTreatment`, `refundability`, `visibility`, `effectiveFrom`, `effectiveTo`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 40 | — | — | `setFeeDefinition` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setFeeDefinition` body |
| Description `description` | text area | optional | — | — | — | — | `setFeeDefinition` body |
| Fee type `feeType` | select | required | — | Booking fee · Transaction fee · Service fee · Convenience fee · Delivery fee · Handling fee · Modification fee · Rescheduling fee · Cancellation fee · Refund fee · Payment fee · Channel fee … | — | — | `setFeeDefinition` body |
| Value type `valueType` | segmented control | required | — | Fixed amount · Percentage · Tiered | — | — | `setFeeDefinition` body |
| Charge basis `chargeBasis` | select | required | — | Per ticket · Per product · Per person · Per order · Per transaction · Per day | — | — | `setFeeDefinition` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setFeeDefinition` body |
| Percentage `percentage` | stepper or slider (%) | optional | — | min 0; max 100 | — | — | `setFeeDefinition` body |
| Tiers `tiers` | key and value settings | optional | — | — | — | `[{fromOrderValue, amount, percentage}]` for `valueType: tiered`. | `setFeeDefinition` body |
| Tax treatment `taxTreatment` | text field | optional | — | max length 60 | — | How the fee is taxed; a `catalogue.tax_rule` may refine it. | `setFeeDefinition` body |
| Refundability `refundability` | segmented control | optional | Non refundable | Refundable · Non refundable | — | — | `setFeeDefinition` body |
| Visibility `visibility` | radio group | optional | Shown separately | Customer visible · Included in display price · Shown separately · Internal only | — | — | `setFeeDefinition` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setFeeDefinition` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setFeeDefinition` body |
| Status `status` | radio group | required | Draft | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setFeeDefinition` body |

Errors to draw in the form: 409 `changeRequestRequired`.; 422 `valueRequired`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Booking Fee (primary button) | navigation or local | — | — | — | — |
| Transaction Fee (secondary button) | navigation or local | — | — | — | — |
| Service Fee (secondary button) | navigation or local | — | — | — | — |
| Convenience Fee (secondary button) | navigation or local | — | — | — | — |
| Delivery Fee (secondary button) | navigation or local | — | — | — | — |
| Handling Fee (secondary button) | navigation or local | — | — | — | — |
| Modification Fee (secondary button) | navigation or local | — | — | — | — |
| Rescheduling Fee (secondary button) | navigation or local | — | — | — | — |
| Save fee definition (secondary button) | `setFeeDefinition` PUT `/fees` | PricingFee | PricingFee | 409 `changeRequestRequired`.; 422 `valueRequired`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listFeeSurcharge` (onLoad, Fee & Surcharge Library)

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `listFeeSurcharge`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fee surcharge configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fee surcharge untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fee surcharge configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `changeRequestRequired`.; 422 `valueRequired`. |

#### Permissions

- `listFeeSurcharge` → `PRODUCT_VIEW` (read) · staff
- `setFeeDefinition` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Fees are separate from taxes: e.g. a call-center convenience fee, or a shipping fee varying by destination (Dubai, Abu Dhabi, Ras Al Khaimah, international) calculated from the checkout address; applied at transaction, item or ticket level. Checkout must show the fee once the address is entered. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-597)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-071` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-071`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 6: Works in Fee & Surcharge Library → Create standardized reusable non-base-price charges.

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-071?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Booking Fee, Transaction Fee, Service Fee, Convenience Fee, Delivery Fee, Handling Fee, Modification Fee, Rescheduling Fee, Save fee definition.
- [ ] Every transition is wired: `ADM-068`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-072` Fee Applicability & Charging Rule Builder

**Determine when a fee or surcharge should apply. Screen 10.3.4 defines the fee. Screen 10.3.5 defines the conditions that trigger it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure whether fees can) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/fee-applicability-charging-rule-builder-adm-072` |

**Known gaps.** **The pack names 16 actions on this screen and the screen declares 1 operation.** Unserved: Product, Product Category, Channel, Venue, Event, Customer Type, Membership, Transaction Type …. Each needs …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Stack | select field | — | — | — | — | — | — |
| Replace | select field | — | — | — | — | — | — |
| Exclude Another Fee | select field | — | — | — | — | — | — |
| Apply Once | select field | — | — | — | — | — | — |
| Apply Per Item | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Product (primary button) | navigation or local | — | — | — | — |
| Product Category (secondary button) | navigation or local | — | — | — | — |
| Channel (secondary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Customer Type (secondary button) | navigation or local | — | — | — | — |
| Membership (secondary button) | navigation or local | — | — | — | — |
| Transaction Type (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `setFeeApplicabilityCharging`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fee applicability charging configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fee applicability charging untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fee applicability charging configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setFeeApplicabilityCharging` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Fees are separate from taxes: e.g. a call-center convenience fee, or a shipping fee varying by destination (Dubai, Abu Dhabi, Ras Al Khaimah, international) calculated from the checkout address; applied at transaction, item or ticket level. Checkout must show the fee once the address is entered. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-597)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-072` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-072`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 8: Works in Fee Applicability & Charging Rule Builder → Determine when a fee or surcharge should apply. Screen 10.3.4 defines the fee. Screen 10.3.5 defines the conditions that trigger it.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-072?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Product, Product Category, Channel, Venue, Event, Customer Type, Membership, Transaction Type.
- [ ] Every transition is wired: `ADM-068`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-073` Fee Waiver, Tax Exemption & Exception Rules

**Govern circumstances under which a normally applicable tax or fee may be reduced, waived or exempted.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure by) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/fee-waiver-tax-exemption-exception-rules-adm-073` |

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 1 operation.** Unserved: Zero-Rated Tax, Complimentary Transaction, Operational Waiver, Contractual Waiver. Each needs an operation …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Membership Benefit | select field | — | — | — | — | — | — |
| Loyalty Tier | select field | — | — | — | — | — | — |
| Corporate Agreement | select field | — | — | — | — | — | — |
| B2B Contract | select field | — | — | — | — | — | — |
| Customer Segment | select field | — | — | — | — | — | — |
| Staff Role | select field | — | — | — | — | — | — |
| Promotion | select field | — | — | — | — | — | — |
| Service Recovery | select field | — | — | — | — | — | — |
| Operational Issue | select field | — | — | — | — | — | — |
| Legal Exemption | select field | — | — | — | — | — | — |
| Supervisor Override | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Exception type | select | — | Fee waiver · Fee reduction · Tax exemption · Zero rated tax · Complimentary transaction · Operational waiver · Contractual waiver | `listFeeWaiverTax` ?exceptionType |
| Eligibility basis | select | — | Membership benefit · Loyalty tier · Corporate agreement · B2B contract · Customer segment · Staff role · Promotion · Service recovery · Operational issue · Legal exemption · Supervisor override | `listFeeWaiverTax` ?eligibilityBasis |
| Status | radio group | — | Draft · Active · Inactive · Expired | `listFeeWaiverTax` ?status |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fee Waiver (primary button) | navigation or local | — | — | — | — |
| Fee Reduction (secondary button) | navigation or local | — | — | — | — |
| Tax Exemption (secondary button) | navigation or local | — | — | — | — |
| Zero-Rated Tax (secondary button) | navigation or local | — | — | — | — |
| Complimentary Transaction (secondary button) | navigation or local | — | — | — | — |
| Operational Waiver (secondary button) | navigation or local | — | — | — | — |
| Contractual Waiver (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listFeeWaiverTax` (onLoad, Fee Waiver, Tax Exemption & Exception Rules)

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `listFeeWaiverTax`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fee waiver tax configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fee waiver tax untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fee waiver tax configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listFeeWaiverTax` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Taxes inclusive or exclusive at product or category level; tax profiles combine several taxes incl. tax-on-tax (e.g. Egypt); per-product/transaction tax exemption flag. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-596)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-073` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-073`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 10: Works in Fee Waiver, Tax Exemption & Exception Rules → Govern circumstances under which a normally applicable tax or fee may be reduced, waived or exempted.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-073?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fee Waiver, Fee Reduction, Tax Exemption, Zero-Rated Tax, Complimentary Transaction, Operational Waiver, Contractual Waiver.
- [ ] Every transition is wired: `ADM-068`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-074` Price Calculation Sequence & Formula Engine

**Define the exact sequence TICVAI follows to calculate the final payable amount. This is the heart of Board 3.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Each step should define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-calculation-sequence-formula-engine-adm-074` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Input | select field | — | — | — | — | — | — |
| Formula | select field | — | — | — | — | — | — |
| Sequence | select field | — | — | — | — | — | — |
| Taxability | select field | — | — | — | — | — | — |
| Rounding | select field | — | — | — | — | — | — |
| Dependency | select field | — | — | — | — | — | — |
| Output | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Calculation profile | text field | — | — | `listPriceCalculationSequence` ?calculationProfileId |
| As of | date picker | — | — | `listPriceCalculationSequence` ?asOf |

**Form: Save price calculation policy** (modal, opened by *Save price calculation policy*; *Save price calculation policy* calls `setPriceCalculationPolicy`, *Cancel* sends nothing)

**Collects what `setPriceCalculationPolicy` sends before it is called.** Required: `id`, `scopePath`, `code`, `name`, `status`. Optional: `isDefault`, `effectiveFrom`, `effectiveTo`, `steps`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 40 | — | — | `setPriceCalculationPolicy` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setPriceCalculationPolicy` body |
| Version `version` | number field | required | — | min 1 | — | — | `setPriceCalculationPolicy` body |
| Is default `isDefault` | toggle | optional | off | — | — | — | `setPriceCalculationPolicy` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setPriceCalculationPolicy` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setPriceCalculationPolicy` body |
| Status `status` | radio group | required | Draft | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setPriceCalculationPolicy` body |
| Steps `steps` | repeatable rows | optional | — | — | — | — | `setPriceCalculationPolicy` body |
| Calculation profile `steps[].calculationProfileId` | picker: choose a calculation profile | required | — | — | shows names, sends the id | — | `setPriceCalculationPolicy` body |
| Sequence `steps[].sequence` | number field | required | — | min 1 | — | — | `setPriceCalculationPolicy` body |
| Step type `steps[].stepType` | select | required | — | Commercial base rate · Contextual rate selection · Dynamic pricing adjustment · Promotion discount · Package bundle adjustment · Fees surcharges · Tax calculation · Rounding · Final payable amount | — | — | `setPriceCalculationPolicy` body |
| Formula type `steps[].formulaType` | select | required | — | Fixed amount · Percentage · Percentage of base · Percentage of subtotal · Tiered · Conditional · Minimum · Maximum · Custom governed formula | — | — | `setPriceCalculationPolicy` body |
| Input `steps[].input` | text field | optional | — | max length 200 | — | — | `setPriceCalculationPolicy` body |
| Formula `steps[].formula` | text field | optional | — | — | — | — | `setPriceCalculationPolicy` body |
| Depends on `steps[].dependsOn` | list of values (chips) | optional | — | — | — | — | `setPriceCalculationPolicy` body |
| Output `steps[].output` | text field | optional | — | max length 200 | — | — | `setPriceCalculationPolicy` body |
| Taxability `steps[].taxability` | segmented control | optional | — | In tax base · Outside tax base | — | — | `setPriceCalculationPolicy` body |
| Rounding profile `steps[].roundingProfileId` | picker: choose a rounding profile | optional | — | — | shows names, sends the id | — | `setPriceCalculationPolicy` body |

Errors to draw in the form: 409 `versionInUse`.; 422 `invalidSequence` or `circularDependency`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save price calculation policy (primary button) | `setPriceCalculationPolicy` PUT `/calculation-profiles` | CalculationProfile | CalculationProfile | 409 `versionInUse`.; 422 `invalidSequence` or `circularDependency`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listPriceCalculationSequence` (onLoad, Price Calculation Sequence & Formula Engine)

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `listPriceCalculationSequence`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price calculation sequence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price calculation sequence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price calculation sequence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `versionInUse`.; 422 `invalidSequence` or `circularDependency`. |

#### Permissions

- `listPriceCalculationSequence` → `PRODUCT_VIEW` (read) · staff
- `setPriceCalculationPolicy` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-074` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-074`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 12: Works in Price Calculation Sequence & Formula Engine → Define the exact sequence TICVAI follows to calculate the final payable amount. This is the heart of Board 3.

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-074?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save price calculation policy.
- [ ] Every transition is wired: `ADM-068`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-075` Currency Precision, Rounding & Monetary Rules

**Ensure monetary calculations remain consistent across countries, currencies, channels and payment systems.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block A · ticket #20628 (APP-SETUP-ADM-075) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/currency-precision-rounding-monetary-rules-adm-075` |

#### Inputs: what the user enters or picks

**Form: Save currency rounding rule** (modal, opened by *Save currency rounding rule*; *Save currency rounding rule* calls `setCurrencyRoundingRule`, *Cancel* sends nothing)

**Collects what `setCurrencyRoundingRule` sends before it is called.** Required: `id`, `scopePath`, `currency`, `decimalPlaces`, `roundingMethod`, `roundingStage`, `status`. Optional: `code`, `name`, `minimumMonetaryUnit`, `displayPrecision`, `calculationPrecision`, `cashRoundingIncrement`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | optional | — | max length 40 | — | — | `setCurrencyRoundingRule` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setCurrencyRoundingRule` body |
| Currency `currency` | text field | required | — | max length 3; pattern `^[A-Z]{3}$` | — | — | `setCurrencyRoundingRule` body |
| Decimal places `decimalPlaces` | stepper or slider | required | — | min 0; max 3 | — | Up to three without rounding the third away (MoM 1 Sep 2026 §4.5). | `setCurrencyRoundingRule` body |
| Minimum monetary unit `minimumMonetaryUnit` | number field | optional | — | — | — | — | `setCurrencyRoundingRule` body |
| Display precision `displayPrecision` | stepper or slider | optional | — | min 0; max 4 | — | — | `setCurrencyRoundingRule` body |
| Calculation precision `calculationPrecision` | stepper or slider | optional | 4 | min 0; max 4 | — | — | `setCurrencyRoundingRule` body |
| Rounding method `roundingMethod` | select | required | — | Standard · Round up · Round down · Bankers · Nearest currency unit · Custom regulatory rule | — | — | `setCurrencyRoundingRule` body |
| Rounding stage `roundingStage` | radio group | required | — | Per item · Per tax · Per fee · Per line · At order total | — | — | `setCurrencyRoundingRule` body |
| Cash rounding increment `cashRoundingIncrement` | number field | optional | — | — | — | — | `setCurrencyRoundingRule` body |
| Status `status` | radio group | required | Active | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setCurrencyRoundingRule` body |

Errors to draw in the form: 422 `precisionBelowDecimals`.

#### Outputs: what the screen shows and produces

**Shown**

**Every currency precision rounding** (data table, from `listCurrencyPrecisionRounding`)

| Shows | Format | Notes |
|---|---|---|
| 50 | text | not in the schema: `AED 199.50` |

**The selected currency precision rounding** (detail panel): The pack groups this record's detail under its own headings: “Calculated”, “Calculated Total”, “Cash Payable”, “The engine should ensure”, “Currency Conversion”.

| Shows | Format | Notes |
|---|---|---|
| 50 | text | not in the schema: `AED 199.50` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Round Down (primary button) | navigation or local | — | — | — | — |
| Save currency rounding rule (secondary button) | `setCurrencyRoundingRule` PUT `/rounding-profiles` | RoundingProfile | RoundingProfile | 422 `precisionBelowDecimals`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listCurrencyPrecisionRounding` (onLoad, Currency Precision, Rounding & Monetary Rules)

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `listCurrencyPrecisionRounding`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The currency precision rounding list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the currency precision rounding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No currency precision rounding yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the currency precision rounding are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `precisionBelowDecimals`. |

#### Permissions

- `listCurrencyPrecisionRounding` → `PRODUCT_VIEW` (read) · staff
- `setCurrencyRoundingRule` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'multi-currency')*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'multi-currency')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-075` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-075`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 14: Works in Currency Precision, Rounding & Monetary Rules → Ensure monetary calculations remain consistent across countries, currencies, channels and payment systems.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-075?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Round Down, Save currency rounding rule.
- [ ] Every transition is wired: `ADM-068`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-076` Price Breakdown, Calculation Simulation & Explainability

**Allow administrators to test the complete calculation before releasing configuration into production.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-breakdown-calculation-simulation-explainability-adm-076` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Customer | select field | — | — | — | — | — | — |
| Product | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Event | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Date | select field | — | — | — | — | — | — |
| Timeslot | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Promotion | select field | — | — | — | — | — | — |
| Payment Method | select field | — | — | — | — | — | — |
| Delivery Method | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Run simulation (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-068` Tax, Fee & Calculation Command Center: *Returns to the board's landing screen*; calls `simulatePriceBreakdownCalculation`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price breakdown calculation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price breakdown calculation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price breakdown calculation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulatePriceBreakdownCalculation` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-076` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-076`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 16: Works in Price Breakdown, Calculation Simulation & Explainability → Allow administrators to test the complete calculation before releasing configuration into production.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-076?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Run simulation.
- [ ] Every transition is wired: `ADM-068`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-077` Calculation Validation, Reconciliation & Service Interface

**Provide final technical and commercial validation of the pricing calculation engine and define how other TICVAI modules consume it. Boards 1–3 established the commercial and calculation engines: Board 1: What prices exist? Board 2: Which price applies? Board 3: How is the final payable amount calculated?**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block A · ticket #20638 (APP-SETUP-ADM-077) |
| Who uses it | ticvai staff holding `LEDGER_POST`, `LEDGER_VIEW`, `PRODUCT_VIEW` (1 operate, 2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/calculation-validation-reconciliation-service-interface-adm-077` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Result kind | segmented control | — | Validation finding · Test scenario result | `listCalculationValidationReconciliation` ?resultKind |
| Area | select | — | Tax · Fees · Formula · Currency · Reconciliation · Test suite | `listCalculationValidationReconciliation` ?area |
| Severity | segmented control | — | Critical · Warning · Information | `listCalculationValidationReconciliation` ?severity |
| Passed | toggle | — | — | `listCalculationValidationReconciliation` ?passed |
| Legal entity | picker: choose a legal entity | — | — | `listEInvoiceTransmissions` ?legalEntityId |
| Status | select | — | Not required · Queued · Sent · Accepted · Rejected · Failed | `listEInvoiceTransmissions` ?status |
| Document | picker: choose a document | — | — | `listEInvoiceTransmissions` ?documentId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCalculationValidationReconciliation` (onLoad, Calculation Validation, Reconciliation & Service Interface); `listEInvoicingProviders` (onLoad, Show the e-invoicing provider connection); `listEInvoiceTransmissions` (onLoad, E-invoicing transmission log and failures)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The calculation validation reconciliation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the calculation validation reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No calculation validation reconciliation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the calculation validation reconciliation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The legal entity has no provider, or its provider is `disabled`. |

#### Permissions

- `listCalculationValidationReconciliation` → `PRODUCT_VIEW` (read) · staff
- `listEInvoicingProviders` → `LEDGER_VIEW` (read) · staff
- `listEInvoiceTransmissions` → `LEDGER_VIEW` (read) · staff
- `transmitEInvoices` → `LEDGER_POST` (operate) · staff, service

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.1 | The system should share all transactions and receipts generated in the system with the external e-invoicing solution. | Retail POS | CONTRACTED_PARTIAL | `transmitEInvoices` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S11** Email: invoicing and taxation questions; biometrics, including children (exclude, or guardian consent) *(Chinmay Parab · Open · due 30 Sep · 30 Sep 2026 · 30 Sep tracker · keyword 'biometric')*
- **A119** Share the selected access control / facial recognition vendor (HID vs. Suprema) so integration scope can be confirmed *(Qossai Alqawasmi · High · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 24 Aug 2026 · workshop tracker · keyword 'facial recognition')*
- **A224** Build the media types board and verification configuration (QR, RFID, NFC, biometric against one virtual ticket; issuance/encoding profiles; on-site media swap as a zero-value transaction; compatibility testing per gate) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **A226** Build facial recognition in two tiers (Face Pass for memberships, Face Tag for single visits) with enrolment via app, web, POS, kiosk or turnstile, plus re-enrolment and fallback media *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'biometric')*
- **C41** Confirm the access control / facial recognition vendor selection (HID vs. Suprema) and share the vendor details *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 2 Sep 2026 · workshop tracker · keyword 'facial recognition')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-077` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS97 Pricing   Revenue Management Board 3.dc.html#adm-077`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 3
- Flow F145 *Pricing Revenue Management board 3: Tax, Fee & Calculation Command Center*, step 18: Works in Calculation Validation, Reconciliation & Service Interface → Provide final technical and commercial validation of the pricing calculation engine and define how other TICVAI modules consume it. Boards 1–3 established the commercial and calculation engines …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-077?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `LEDGER_POST`, `LEDGER_VIEW`, `PRODUCT_VIEW`.
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

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getVatReturn": {"method":"GET","path":"/tax/vat-returns","contract":"finance","summary":"A legal entity's VAT return for a tax period, in the FTA's boxes","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":true},{"name":"periodFrom","in":"query","required":true},{"name":"periodTo","in":"query","required":true},{"name":"format","in":"query","required":null}],"requestBody":null,"responds":"FinVatReturn"},
"listCalculationValidationReconciliation": {"method":"GET","path":"/calculation-validation-reconciliation","contract":"catalogue","summary":"Calculation Validation, Reconciliation & Service Interface","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"resultKind","in":"query","required":false},{"name":"area","in":"query","required":false},{"name":"severity","in":"query","required":false},{"name":"passed","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCurrencyPrecisionRounding": {"method":"GET","path":"/currency-precision-rounding","contract":"catalogue","summary":"Currency Precision, Rounding & Monetary Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CurrencyPrecisionRoundingMonetaryRulesView"},
"listEInvoiceTransmissions": {"method":"GET","path":"/e-invoicing/transmissions","contract":"finance","summary":"What was sent to the e-invoicing provider, and what came back","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"documentId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEInvoicingProviders": {"method":"GET","path":"/e-invoicing/providers","contract":"finance","summary":"The e-invoicing service provider connection per legal entity","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFeeSurcharge": {"method":"GET","path":"/fee-surcharge","contract":"catalogue","summary":"Fee & Surcharge Library","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"feeType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listFeeWaiverTax": {"method":"GET","path":"/fee-waiver-tax","contract":"catalogue","summary":"Fee Waiver, Tax Exemption & Exception Rules","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"exceptionType","in":"query","required":false},{"name":"eligibilityBasis","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceCalculationSequence": {"method":"GET","path":"/price-calculation-sequence","contract":"catalogue","summary":"Price Calculation Sequence & Formula Engine","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"calculationProfileId","in":"query","required":false},{"name":"asOf","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxFeeCalculation": {"method":"GET","path":"/tax-fee-calculation","contract":"catalogue","summary":"Tax, Fee & Calculation Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"type","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"legalEntity","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxInvoiceTemplates": {"method":"GET","path":"/tax-invoice-templates","contract":"finance","summary":"Invoice and credit memo templates and number series, per legal entity","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"legalEntityId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxInvoices": {"method":"GET","path":"/tax-invoices","contract":"finance","summary":"Tax invoices issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"orderId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"invoiceType","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setCurrencyRoundingRule": {"method":"PUT","path":"/rounding-profiles","contract":"catalogue","summary":"Set precision and rounding for a currency","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RoundingProfile","responds":"RoundingProfile"},
"setEInvoicingProvider": {"method":"PUT","path":"/e-invoicing/providers","contract":"finance","summary":"Connect a legal entity to its accredited e-invoicing service provider","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FinEInvoicingProvider","responds":"FinEInvoicingProvider"},
"setFeeApplicabilityCharging": {"method":"PUT","path":"/fee-applicability-charging","contract":"catalogue","summary":"Fee Applicability & Charging Rule Builder","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FeeApplicabilityChargingRuleBuilderInput","responds":"FeeApplicabilityChargingRuleBuilderView"},
"setFeeDefinition": {"method":"PUT","path":"/fees","contract":"catalogue","summary":"Create or update a fee or surcharge","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingFee","responds":"PricingFee"},
"setPriceCalculationPolicy": {"method":"PUT","path":"/calculation-profiles","contract":"catalogue","summary":"Save a price calculation sequence, whole","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CalculationProfile","responds":"CalculationProfile"},
"setTaxInvoiceTemplate": {"method":"PUT","path":"/tax-invoice-templates","contract":"finance","summary":"Set a legal entity's template and number series for one document kind","permission":"TAX_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FinTaxInvoiceTemplate","responds":"FinTaxInvoiceTemplate"},
"setTaxProfileJurisdiction": {"method":"PUT","path":"/tax-profile-jurisdiction","contract":"catalogue","summary":"Tax Profile & Jurisdiction Configuration","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TaxProfileJurisdictionConfigurationInput","responds":"TaxProfileJurisdictionConfigurationView"},
"setTaxRuleTreatment": {"method":"PUT","path":"/tax-rule-treatment","contract":"catalogue","summary":"Tax Rule & Treatment Builder","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TaxRuleTreatmentBuilderInput","responds":"TaxRuleTreatmentBuilderView"},
"simulatePriceBreakdownCalculation": {"method":"PUT","path":"/price-breakdown-calculation","contract":"catalogue","summary":"Price Breakdown, Calculation Simulation & Explainability","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PriceBreakdownCalculationSimulationExplainabilityInput","responds":"PriceBreakdownCalculationSimulationExplainabilityView"},
"transmitEInvoices": {"method":"POST","path":"/e-invoicing/transmissions","contract":"finance","summary":"Send issued tax documents to the e-invoicing provider","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CalculationProfile": {"type":"object","x-ticvai-persistence":"catalogue.calculation_profile + catalogue.calculation_step","description":"**The ordered sequence that turns a rate into a payable amount** (29 September, data model DM3). ADM-074: base rate, contextual rate, dynamic adjustment, promotion, package adjustment, fees, tax, rounding, final amount. Versioned; a calculation records the version it used (`calculationVersion`), so history is reproducible.","required":["id","scopePath","code","name","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"code":{"type":"string","maxLength":40},"name":{"type":"string","maxLength":200},"version":{"type":"integer","minimum":1},"isDefault":{"type":"boolean","default":false},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"draft"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/CalculationStep"}},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"CalculationStep": {"type":"object","x-ticvai-persistence":"catalogue.calculation_step","description":"**One step of a calculation profile** (29 September, data model DM3). `dependsOn` names earlier steps; a cycle or a step depending on a later one is refused (`422 circularDependency` / `invalidSequence`).","required":["id","calculationProfileId","sequence","stepType","formulaType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"calculationProfileId":{"type":"string","format":"uuid"},"sequence":{"type":"integer","minimum":1},"stepType":{"type":"string","enum":["commercialBaseRate","contextualRateSelection","dynamicPricingAdjustment","promotionDiscount","packageBundleAdjustment","feesSurcharges","taxCalculation","rounding","finalPayableAmount"]},"formulaType":{"type":"string","enum":["fixedAmount","percentage","percentageOfBase","percentageOfSubtotal","tiered","conditional","minimum","maximum","customGovernedFormula"]},"input":{"type":"string","maxLength":200,"nullable":true},"formula":{"type":"string","nullable":true},"dependsOn":{"type":"array","items":{"type":"string"}},"output":{"type":"string","maxLength":200,"nullable":true},"taxability":{"type":"string","enum":["inTaxBase","outsideTaxBase",null],"nullable":true},"roundingProfileId":{"type":"string","format":"uuid","nullable":true}}},
"CalculationValidationReconciliationServiceInterfaceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Calculation Validation, Reconciliation & Service Interface displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"resultId":{"type":"string","description":"Result ID"},"resultKind":{"type":"string","enum":["validationFinding","testScenarioResult"],"description":"A configuration finding or a test-suite scenario result"},"area":{"type":"string","enum":["tax","fees","formula","currency","reconciliation","testSuite"],"description":"Validation Area (p.52)"},"code":{"type":"string","enum":["missingProfile","invalidRate","expiredRule","overlappingRule","duplicateFee","conflictingRule","missingTaxTreatment","circularDependency","invalidSequence","missingInput","invalidPrecision","unsupportedCurrency","roundingDifference","reconciliationMismatch","scenarioFailed"],"description":"What was checked"},"severity":{"type":"string","enum":["critical","warning","information"],"description":"Severity; critical blocks progress"},"message":{"type":"string","description":"What was found"},"subjectId":{"type":"string","nullable":true,"description":"The profile, rule, fee, formula or currency concerned"},"scenarioName":{"type":"string","nullable":true,"description":"Test scenario name"},"scenarioType":{"type":"string","enum":["standardB2cSale","posSale","memberSale","groupBooking","b2bSale","refund","reschedule","multiProductOrder","packageSale","multiCurrencySale"],"description":"Test Suite scenario type (pp.52-53)","nullable":true},"passed":{"type":"boolean","nullable":true,"description":"Scenario passed; empty for a finding"},"reconciliation":{"type":"object","nullable":true,"description":"Reconciliation (p.52): expected against actual totals for a scenario","properties":{"lineTotal":{"type":"object","properties":{"expected":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actual":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"taxTotal":{"type":"object","properties":{"expected":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actual":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"feeTotal":{"type":"object","properties":{"expected":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actual":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"discountTotal":{"type":"object","properties":{"expected":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actual":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"finalTotal":{"type":"object","properties":{"expected":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"actual":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}},"calculationVersion":{"type":"string","description":"Calculation version the result was produced with (Historical Reproducibility)"}}},
"CatalogueConfigStatus": {"type":"string","enum":["draft","active","inactive","retired"],"description":"**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."},
"CurrencyPrecisionRoundingMonetaryRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Currency Precision, Rounding & Monetary Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"decimalPlaces":{"type":"integer","description":"Decimal Places of the currency, 0 to 3 (MoM 1 Sep §4.5)","minimum":0,"maximum":3},"minimumMonetaryUnit":{"type":"number","description":"Minimum Monetary Unit, e.g. 0.01, 0.001, 0.05"},"displayPrecision":{"type":"integer","description":"Display Precision: decimals shown","minimum":0,"maximum":3},"calculationPrecision":{"type":"integer","description":"Calculation Precision: decimals carried while calculating; at most 4, the scale Money is stored at (decided 29 September, readiness close-out)","minimum":0,"maximum":4},"roundingMethod":{"type":"string","enum":["standard","roundUp","roundDown","bankers","nearestCurrencyUnit","customRegulatoryRule"],"description":"Rounding Method (p.49)"},"ruleId":{"type":"string","description":"Currency rule ID"},"roundingStage":{"type":"string","enum":["perItem","perTax","perFee","perLine","atOrderTotal"],"description":"Rounding Stage (p.50): where rounding happens"},"cashRoundingIncrement":{"type":"number","nullable":true,"description":"Cash Rounding: increment cash totals round to (CHF 19.98 -> 20.00 at 0.05) while electronic payment keeps the exact total; empty for none"},"status":{"type":"string","description":"Status: active or inactive"}}},
"FeeApplicabilityChargingRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.channel_allocation at 5%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Fee Applicability & Charging Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"product":{"type":"string","nullable":true,"description":"Condition: product; empty for any"},"productCategory":{"type":"string","nullable":true,"description":"Condition: product category"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Condition: channel (Call Center Fee IF Channel = Call Center); empty for any"},"venue":{"type":"string","nullable":true,"description":"Condition: venue"},"event":{"type":"string","nullable":true,"description":"Condition: event"},"customerType":{"type":"string","nullable":true,"description":"Condition: customer type"},"membership":{"type":"string","nullable":true,"description":"Condition: membership product or tier"},"transactionType":{"type":"string","nullable":true,"description":"Condition: transaction type"},"paymentMethod":{"type":"string","nullable":true,"description":"Condition: payment method"},"deliveryMethod":{"type":"string","nullable":true,"description":"Condition: delivery method"},"market":{"type":"string","nullable":true,"description":"Condition: market"},"country":{"type":"string","nullable":true,"pattern":"^[A-Z]{2}$","description":"Condition: country"},"serviceAction":{"type":"string","enum":["newSale","modification","reschedule","cancellation","refund","upgrade"],"description":"Condition: service action (Action = Reschedule); empty for any","nullable":true},"rulePriority":{"type":"integer","description":"Rule Priority: the lower number is evaluated first"},"ruleId":{"type":"string","description":"Charging rule ID; empty on create"},"ruleName":{"type":"string","description":"Rule name"},"feeId":{"type":"string","description":"The fee from the library (Screen 10.3.4, ADM-071) this rule charges"},"orderValueMin":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Threshold: order value at or above which the fee applies"},"orderValueMax":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Threshold: order value below which the fee applies (Order Value < AED 100 -> handling fee)"},"quantityMin":{"type":"integer","nullable":true,"description":"Condition: minimum quantity"},"quantityMax":{"type":"integer","nullable":true,"description":"Condition: maximum quantity"},"hoursBeforeEventMax":{"type":"integer","nullable":true,"description":"Condition: the event occurs within this many hours (reschedule within 48 hours)"},"deliveryDestinationZones":{"type":"array","items":{"type":"string"},"description":"Condition: delivery destination zones (Dubai, Abu Dhabi, Ras Al Khaimah, international), matched from the checkout address (MoM 1 Sep §4.5 shipping fee)"},"combination":{"type":"string","enum":["stack","replace","exclude"],"description":"Fee Combination (p.45): add to other fees, replace them, or exclude named fees"},"excludedFeeIds":{"type":"array","items":{"type":"string"},"description":"Fees excluded or replaced when combination is exclude or replace"},"application":{"type":"string","enum":["applyOnce","applyPerItem"],"description":"Apply Once per order or Apply Per Item"},"onMatch":{"type":"string","enum":["stopProcessing","continueProcessing"],"description":"Stop or Continue Processing after this rule applies"},"mutualExclusionGroup":{"type":"string","nullable":true,"description":"Mutual Exclusion: rules sharing a group never apply together; empty for none"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"}}},
"FeeApplicabilityChargingRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Fee Applicability & Charging Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","nullable":true,"description":"Condition: product; empty for any"},"productCategory":{"type":"string","nullable":true,"description":"Condition: product category"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Condition: channel (Call Center Fee IF Channel = Call Center); empty for any"},"venue":{"type":"string","nullable":true,"description":"Condition: venue"},"event":{"type":"string","nullable":true,"description":"Condition: event"},"customerType":{"type":"string","nullable":true,"description":"Condition: customer type"},"membership":{"type":"string","nullable":true,"description":"Condition: membership product or tier"},"transactionType":{"type":"string","nullable":true,"description":"Condition: transaction type"},"paymentMethod":{"type":"string","nullable":true,"description":"Condition: payment method"},"deliveryMethod":{"type":"string","nullable":true,"description":"Condition: delivery method"},"market":{"type":"string","nullable":true,"description":"Condition: market"},"country":{"type":"string","nullable":true,"pattern":"^[A-Z]{2}$","description":"Condition: country"},"serviceAction":{"type":"string","enum":["newSale","modification","reschedule","cancellation","refund","upgrade"],"description":"Condition: service action (Action = Reschedule); empty for any","nullable":true},"rulePriority":{"type":"integer","description":"Rule Priority: the lower number is evaluated first"},"ruleId":{"type":"string","description":"Charging rule ID; empty on create"},"ruleName":{"type":"string","description":"Rule name"},"feeId":{"type":"string","description":"The fee from the library (Screen 10.3.4, ADM-071) this rule charges"},"orderValueMin":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Threshold: order value at or above which the fee applies"},"orderValueMax":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Threshold: order value below which the fee applies (Order Value < AED 100 -> handling fee)"},"quantityMin":{"type":"integer","nullable":true,"description":"Condition: minimum quantity"},"quantityMax":{"type":"integer","nullable":true,"description":"Condition: maximum quantity"},"hoursBeforeEventMax":{"type":"integer","nullable":true,"description":"Condition: the event occurs within this many hours (reschedule within 48 hours)"},"deliveryDestinationZones":{"type":"array","items":{"type":"string"},"description":"Condition: delivery destination zones (Dubai, Abu Dhabi, Ras Al Khaimah, international), matched from the checkout address (MoM 1 Sep §4.5 shipping fee)"},"combination":{"type":"string","enum":["stack","replace","exclude"],"description":"Fee Combination (p.45): add to other fees, replace them, or exclude named fees"},"excludedFeeIds":{"type":"array","items":{"type":"string"},"description":"Fees excluded or replaced when combination is exclude or replace"},"application":{"type":"string","enum":["applyOnce","applyPerItem"],"description":"Apply Once per order or Apply Per Item"},"onMatch":{"type":"string","enum":["stopProcessing","continueProcessing"],"description":"Stop or Continue Processing after this rule applies"},"mutualExclusionGroup":{"type":"string","nullable":true,"description":"Mutual Exclusion: rules sharing a group never apply together; empty for none"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"}}},
"FeeSurchargeLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Fee & Surcharge Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"percentage":{"type":"number","nullable":true,"description":"Value in percent when the method is percentage (Online Service Fee 3%)"},"feeName":{"type":"string","description":"Fee Name"},"feeCode":{"type":"string","description":"Fee Code"},"feeType":{"type":"string","enum":["bookingFee","transactionFee","serviceFee","convenienceFee","deliveryFee","handlingFee","modificationFee","reschedulingFee","cancellationFee","refundFee","paymentFee","channelFee","facilityFee","surcharge","customFee"],"description":"Fee Type (p.43)"},"description":{"type":"string","description":"Description"},"valueType":{"type":"string","enum":["fixedAmount","percentage","tiered"],"description":"Calculation Method: how the value is expressed"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"taxTreatment":{"type":"string","nullable":true,"description":"Tax Treatment: the tax rule (ADM-070) applied to the fee; empty is flagged Missing Tax Treatment by validation"},"refundability":{"type":"string","enum":["refundable","nonRefundable"],"description":"Refundability when the order is refunded"},"status":{"type":"string","description":"Status: draft, active, inactive or expired"},"feeId":{"type":"string","description":"Fee ID"},"chargeBasis":{"type":"string","enum":["perTicket","perProduct","perPerson","perOrder","perTransaction","perDay"],"description":"What the value is charged per (Call Center Booking Fee AED 15 per order; Online Service Fee 3% per transaction)"},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Value when the method is fixedAmount"},"tiers":{"type":"array","items":{"type":"object","properties":{"fromOrderValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"percentage":{"type":"number","nullable":true}}},"description":"Tiers when the method is tiered"},"visibility":{"type":"string","enum":["customerVisible","includedInDisplayPrice","shownSeparately","internalOnly"],"description":"Fee Visibility (p.44)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"FeeWaiverTaxExemptionExceptionRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Fee Waiver, Tax Exemption & Exception Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"reasonRequired":{"type":"boolean","description":"Reason mandatory when the exception is applied"},"exemptionType":{"type":"string","nullable":true,"description":"Exemption Type for tax exemptions, e.g. diplomatic, charity (the client's list); empty for fee exceptions"},"ruleId":{"type":"string","description":"Exception rule ID"},"ruleName":{"type":"string","description":"Rule name"},"exceptionType":{"type":"string","enum":["feeWaiver","feeReduction","taxExemption","zeroRatedTax","complimentaryTransaction","operationalWaiver","contractualWaiver"],"description":"Exception Type (p.46)"},"targetFeeIds":{"type":"array","items":{"type":"string"},"description":"Fees waived or reduced; empty for a tax exception"},"targetTaxProfileIds":{"type":"array","items":{"type":"string"},"description":"Tax profiles exempted or zero-rated; empty for a fee exception"},"reductionPercent":{"type":"number","nullable":true,"description":"Fee Reduction in percent; empty for a full waiver"},"reductionAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Fee Reduction as an amount; empty for a full waiver"},"eligibilityBasis":{"type":"string","enum":["membershipBenefit","loyaltyTier","corporateAgreement","b2bContract","customerSegment","staffRole","promotion","serviceRecovery","operationalIssue","legalExemption","supervisorOverride"],"description":"Eligibility Condition (p.46)"},"eligibilityRefId":{"type":"string","nullable":true,"description":"The membership tier, agreement, contract, segment, role or promotion that qualifies (Gold Member -> Booking Fee waived)"},"approvalRequired":{"type":"boolean","description":"Approval required before the exception takes effect"},"evidenceRequired":{"type":"boolean","description":"Tax Exemption Evidence must be captured (p.47)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"}}},
"FinEInvoiceTransmission": {"x-ticvai-persistence":"ledger.einvoice_transmission","type":"object","description":"6.1.1. One attempt to send one tax document to the provider, and its answer.","required":["id","documentKind","documentId","legalEntityId","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"documentKind":{"type":"string","enum":["taxInvoice","creditMemo"]},"documentId":{"type":"string","format":"uuid"},"documentNumber":{"type":"string"},"legalEntityId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid","nullable":true},"mode":{"type":"string","enum":["test","live"]},"status":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"payloadHash":{"type":"string","nullable":true,"description":"SHA-256 of the document as sent, so a resend can be shown to be the same document."},"providerMessageId":{"type":"string","nullable":true},"attempt":{"type":"integer","minimum":1},"errorCodes":{"type":"array","items":{"type":"string"}},"errorMessage":{"type":"string","nullable":true},"sentAt":{"type":"string","format":"date-time","nullable":true},"answeredAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true}}},
"FinEInvoiceTransmissionStatus": {"type":"string","description":"6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.","enum":["notRequired","queued","sent","accepted","rejected","failed"]},
"FinEInvoicingProvider": {"x-ticvai-persistence":"ledger.einvoicing_provider","type":"object","description":"6.1.1. Also the `setEInvoicingProvider` body. One per legal entity.","required":["legalEntityId","providerName","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"legalEntityId":{"type":"string","format":"uuid"},"providerName":{"type":"string","maxLength":200,"description":"The accredited service provider the client appoints."},"endpointUrl":{"type":"string","format":"uri","nullable":true},"testEndpointUrl":{"type":"string","format":"uri","nullable":true},"credentialRef":{"type":"string","maxLength":300,"nullable":true,"description":"A reference to the secret in the vault; the secret is never stored here."},"participantId":{"type":"string","maxLength":100,"nullable":true,"description":"The legal entity's Peppol participant identifier."},"documentFormat":{"type":"string","enum":["pintAe"],"default":"pintAe"},"mode":{"type":"string","enum":["disabled","test","live"]},"transmitWithinHours":{"type":"integer","minimum":1,"nullable":true},"lastAcceptedTestAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."}}},
"FinTaxCategory": {"type":"string","description":"How a line is treated for VAT. Taken from the tax code the line was posted with.","enum":["standardRated","zeroRated","exempt","outOfScope","reverseCharge"]},
"FinTaxInvoice": {"x-ticvai-persistence":"ledger.tax_invoice + ledger.tax_invoice_line","type":"object","description":"5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.","required":["id","invoiceNumber","invoiceType","status","legalEntityId","issuedAt","supplyDate","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"invoiceNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."},"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"status":{"$ref":"#/components/schemas/FinTaxInvoiceStatus"},"legalEntityId":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"orderIds":{"type":"array","items":{"type":"string","format":"uuid"}},"supplierName":{"type":"string"},"supplierAddress":{"type":"string","nullable":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest the orders belong to; the key a guest's own reads filter on."},"buyerName":{"type":"string","nullable":true},"buyerAddress":{"type":"string","nullable":true},"buyerCountryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true},"customerAccountId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"supplyDate":{"type":"string","format":"date","description":"The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs, at the rate the orders were stored at."},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"languages":{"type":"array","items":{"type":"string"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The PDF rendered at issue; read through getTaxDocumentRendition."},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null where the platform issued it."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinTaxInvoiceLine"}},"taxSummary":{"type":"array","x-ticvai-persisted":false,"description":"VAT per rate and category, summed from the lines for the response.","items":{"type":"object","properties":{"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxRate":{"type":"number"},"taxableAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."}}},
"FinTaxInvoiceLine": {"type":"object","description":"One line as it was sold and taxed. Amounts are in the invoice currency.","required":["lineNumber","description","quantity","netAmount","taxAmount","grossAmount","taxCategory"],"properties":{"lineNumber":{"type":"integer","minimum":1},"orderId":{"type":"string","format":"uuid"},"orderLineId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string","maxLength":500},"quantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true},"taxRate":{"type":"number","minimum":0,"maximum":100},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FinTaxInvoiceStatus": {"type":"string","description":"`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).","enum":["issued","partiallyCredited","fullyCredited","superseded"]},
"FinTaxInvoiceTemplate": {"x-ticvai-persistence":"ledger.tax_invoice_template","type":"object","description":"5.7.93, 5.7.94. Also the `setTaxInvoiceTemplate` body. One per legal entity and document kind.","required":["legalEntityId","documentKind","numberPrefix","languages"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"legalEntityId":{"type":"string","format":"uuid"},"documentKind":{"type":"string","enum":["taxInvoice","simplifiedTaxInvoice","creditMemo"]},"numberPrefix":{"type":"string","maxLength":20,"description":"e.g. `INV-`, `SINV-`, `CN-`. The year is added by the series when `resetsYearly`."},"resetsYearly":{"type":"boolean","default":true,"description":"A new series per fiscal year of the legal entity."},"nextNumber":{"type":"integer","minimum":1,"description":"May be raised, never lowered below the last number issued."},"numberPadding":{"type":"integer","minimum":1,"maximum":12,"default":6},"languages":{"type":"array","minItems":1,"description":"Rendered on one page in this order, e.g. `en`, `ar`.","items":{"type":"string","pattern":"^[a-z]{2}(-[A-Z]{2})?$"}},"title":{"type":"object","description":"The document title per language, e.g. \"Tax Invoice\". Prescribed wording is law (CF-133).","additionalProperties":{"type":"string"}},"footerText":{"type":"object","additionalProperties":{"type":"string"}},"logoAssetId":{"type":"string","format":"uuid","nullable":true},"layoutKey":{"type":"string","maxLength":64,"nullable":true},"autoIssueOnPayment":{"type":"boolean","default":false,"description":"For `simplifiedTaxInvoice`, issue one on every paid order (the VAT receipt)."},"simplifiedAllowedUpTo":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"showLegalCurrencyTax":{"type":"boolean","default":true,"description":"Show the tax in the legal entity's currency when the invoice currency differs."},"effectiveFrom":{"type":"string","format":"date"},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."}}},
"FinTaxInvoiceType": {"type":"string","description":"5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.","enum":["simplified","full","consolidated"]},
"FinVatReturn": {"x-ticvai-persistence":"none — computed from ledger postings on the reporting replica","type":"object","description":"6.1.23. The FTA VAT 201 boxes for one legal entity and tax period.","required":["legalEntityId","periodFrom","periodTo","boxes","netTaxPayable"],"properties":{"legalEntityId":{"type":"string","format":"uuid"},"taxRegistrationNumber":{"type":"string"},"periodFrom":{"type":"string","format":"date"},"periodTo":{"type":"string","format":"date"},"boxes":{"type":"array","items":{"type":"object","required":["box","amount","taxAmount"],"properties":{"box":{"type":"string","description":"The form's box, e.g. `1a` (standard-rated supplies, Abu Dhabi) ... `1g`, `2` (tourist refunds), `3` (reverse charge), `4` (zero-rated), `5` (exempt), `6` and `7` (imports), `9` (standard-rated expenses), `10` (reverse charge inputs)."},"label":{"type":"string"},"emirate":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"adjustmentAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"postingCount":{"type":"integer"}}}},"totalOutputTax":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalRecoverableTax":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netTaxPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"fileUrl":{"type":"string","format":"uri","nullable":true,"description":"Set for `format` `csv` or `xlsx`; a short-lived link."},"generatedAt":{"type":"string","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PriceBreakdownCalculationSimulationExplainabilityInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Price Breakdown, Calculation Simulation & Explainability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"customerId":{"type":"string","nullable":true,"description":"Customer"},"productId":{"type":"string","description":"Product"},"quantity":{"type":"integer","description":"Quantity","minimum":1},"venueId":{"type":"string","nullable":true,"description":"Venue"},"eventId":{"type":"string","nullable":true,"description":"Event"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Channel"},"date":{"type":"string","format":"date","description":"Date of visit"},"timeslotId":{"type":"string","nullable":true,"description":"Timeslot"},"membershipId":{"type":"string","nullable":true,"description":"Membership"},"promotionCode":{"type":"string","nullable":true,"description":"Promotion"},"paymentMethod":{"type":"string","nullable":true,"description":"Payment Method"},"deliveryMethod":{"type":"string","nullable":true,"description":"Delivery Method"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"compareChannels":{"type":"array","items":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"description":"Channel Comparison (p.51): run the same transaction through these channels too; empty for none"}}},
"PriceBreakdownCalculationSimulationExplainabilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price Breakdown, Calculation Simulation & Explainability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"finalPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Final Payable"},"components":{"type":"array","items":{"type":"object","properties":{"sequence":{"type":"integer"},"componentType":{"type":"string","enum":["selectedRate","memberAdjustment","dynamicAdjustment","promotion","packageAdjustment","fee","surcharge","waiver","tax","rounding"]},"label":{"type":"string","description":"e.g. Booking Fee, VAT"},"source":{"type":"string","description":"Source: the price list, rule, fee or tax profile"},"rule":{"type":"string","description":"Rule: id of the rule applied, e.g. FE-021, TAX-UAE-01"},"formula":{"type":"string"},"input":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Input amount"},"output":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Output amount (negative for a reduction)"},"reason":{"type":"string"},"taxTreatment":{"type":"string","nullable":true}}},"description":"Explainability Panel and Rule Trace (p.51), in sequence"},"selectedRate":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Selected Rate x quantity"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discounts and adjustments total"},"feeTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fees total"},"subtotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Subtotal before tax"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Tax total"},"calculationVersion":{"type":"string","description":"Calculation version used"},"channelComparison":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"finalPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"difference":{"type":"string","description":"Why it differs, e.g. Call Center Booking Fee"}}},"description":"Channel Comparison results"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI observations for this screen; advisory only, never applied automatically"}}},
"PriceCalculationSequenceFormulaEngineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price Calculation Sequence & Formula Engine displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"input":{"type":"string","description":"Input: the named value the step reads, e.g. subtotal"},"formula":{"type":"string","description":"Formula expression, governed"},"sequence":{"type":"integer","description":"Sequence: position in the pipeline"},"taxability":{"type":"string","enum":["inTaxBase","outsideTaxBase"],"description":"Taxability: whether this step's amount is part of the tax base; a discount outsideTaxBase gives tax on the pre-discount price where the region requires it (MoM 1 Sep §4.5)"},"rounding":{"type":"string","nullable":true,"description":"Rounding rule applied after the step (ADM-075); empty for none"},"dependsOn":{"type":"array","items":{"type":"string"},"description":"Dependency: steps whose output this step needs"},"output":{"type":"string","description":"Output: the named value the step produces"},"stepId":{"type":"string","description":"Step ID"},"calculationProfileId":{"type":"string","description":"Calculation profile the step belongs to"},"stepType":{"type":"string","enum":["commercialBaseRate","contextualRateSelection","dynamicPricingAdjustment","promotionDiscount","packageBundleAdjustment","feesSurcharges","taxCalculation","rounding","finalPayableAmount"],"description":"Pipeline stage (Recommended Calculation Pipeline, pp.47-48)"},"formulaType":{"type":"string","enum":["fixedAmount","percentage","percentageOfBase","percentageOfSubtotal","tiered","conditional","minimum","maximum","customGovernedFormula"],"description":"Formula Builder kind (p.48)"},"version":{"type":"string","description":"Formula version"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"PricingFee": {"type":"object","x-ticvai-persistence":"catalogue.fee","description":"**The fee and surcharge library** (29 September, data model DM3). ADM-071. What a fee is and how it computes; when it applies is `catalogue.fee_rule`. Distinct from `payments.fee_rule` (a provider's processing cost) and `orders.order_fee` (a fee as charged on one order).","required":["id","scopePath","code","name","feeType","valueType","chargeBasis","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"code":{"type":"string","maxLength":40},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"feeType":{"type":"string","enum":["bookingFee","transactionFee","serviceFee","convenienceFee","deliveryFee","handlingFee","modificationFee","reschedulingFee","cancellationFee","refundFee","paymentFee","channelFee","facilityFee","surcharge","customFee"]},"valueType":{"type":"string","enum":["fixedAmount","percentage","tiered"]},"chargeBasis":{"type":"string","enum":["perTicket","perProduct","perPerson","perOrder","perTransaction","perDay"]},"amount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"percentage":{"type":"number","nullable":true,"minimum":0,"maximum":100},"tiers":{"type":"object","additionalProperties":true,"nullable":true,"description":"`[{fromOrderValue, amount, percentage}]` for `valueType: tiered`."},"taxTreatment":{"type":"string","maxLength":60,"nullable":true,"description":"How the fee is taxed; a `catalogue.tax_rule` may refine it."},"refundability":{"type":"string","enum":["refundable","nonRefundable"],"default":"nonRefundable"},"visibility":{"type":"string","enum":["customerVisible","includedInDisplayPrice","shownSeparately","internalOnly"],"default":"shownSeparately"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"draft"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"RoundingProfile": {"type":"object","x-ticvai-persistence":"catalogue.rounding_profile","description":"**Precision and rounding for one currency** (29 September, data model DM3). ADM-075. One per currency the tenant sells in; the engine keeps line totals + tax + fees equal to the transaction total. Distinct from `payments.currency_rule` (settlement currency and payment limits). The currency here is the subject of the rule, not the denomination of an amount.","required":["id","scopePath","currency","decimalPlaces","roundingMethod","roundingStage","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."},"code":{"type":"string","maxLength":40,"nullable":true},"name":{"type":"string","maxLength":200,"nullable":true},"currency":{"type":"string","maxLength":3,"pattern":"^[A-Z]{3}$"},"decimalPlaces":{"type":"integer","minimum":0,"maximum":3,"description":"Up to three without rounding the third away (MoM 1 Sep 2026 §4.5)."},"minimumMonetaryUnit":{"type":"number","nullable":true},"displayPrecision":{"type":"integer","nullable":true,"minimum":0,"maximum":4},"calculationPrecision":{"type":"integer","minimum":0,"maximum":4,"default":4},"roundingMethod":{"type":"string","enum":["standard","roundUp","roundDown","bankers","nearestCurrencyUnit","customRegulatoryRule"]},"roundingStage":{"type":"string","enum":["perItem","perTax","perFee","perLine","atOrderTotal"]},"cashRoundingIncrement":{"type":"number","nullable":true},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"active"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"TaxFeeCalculationCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Tax, Fee & Calculation Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeTaxProfiles":{"type":"integer","description":"Active Tax Profiles"},"taxJurisdictions":{"type":"integer","description":"Tax Jurisdictions"},"activeFeeProfiles":{"type":"integer","description":"Active Fee Profiles"},"activeSurcharges":{"type":"integer","description":"Active Surcharges"},"exemptionRules":{"type":"integer","description":"Exemption Rules"},"calculationProfiles":{"type":"integer","description":"Calculation Profiles"},"productsMissingTax":{"type":"integer","description":"Products Missing Tax: active products with no applicable tax profile"},"productsMissingCalculationProfile":{"type":"integer","description":"Products Missing Calculation Profile"},"configurationConflicts":{"type":"integer","description":"Configuration Conflicts"},"upcomingTaxChanges":{"type":"integer","description":"Upcoming Tax Changes"},"validationIssues":{"type":"integer","description":"Validation Issues"},"recentlyModifiedRules":{"type":"integer","description":"Recently Modified Rules: changed in the last 7 days (decided 29 September, readiness close-out)"},"alerts":{"type":"array","items":{"type":"string"},"description":"Alerts (pp.39-40), e.g. \"14 active products have no applicable VAT profile\""},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI observations for this screen; advisory only, never applied automatically"}}},
"TaxFeeCalculationCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Tax, Fee & Calculation Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"profileName":{"type":"string","description":"Profile Name"},"type":{"type":"string","enum":["tax","fee","surcharge","waiver","exemption","calculationProfile","roundingProfile"],"description":"Configuration Type (p.39)"},"country":{"type":"string","description":"Country"},"legalEntity":{"type":"string","description":"Legal Entity"},"market":{"type":"string","description":"Market"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"productScope":{"type":"string","description":"Product Scope"},"status":{"type":"string","description":"Status: draft, active, inactive or expired"},"owner":{"type":"string","description":"Owner"},"profileId":{"type":"string","description":"ID of the tax profile, fee, rule or profile"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"TaxProfileJurisdictionConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Tax Profile & Jurisdiction Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"taxProfileName":{"type":"string","description":"Tax Profile Name"},"taxProfileCode":{"type":"string","description":"Tax Profile Code"},"taxType":{"type":"string","enum":["vat","gst","salesTax","entertainmentTax","tourismTax","municipalityTax","serviceTax","customRegulatoryTax"],"description":"Tax Type (pp.40-41)"},"country":{"type":"string","description":"Country: ISO 3166-1 alpha-2 code","pattern":"^[A-Z]{2}$"},"jurisdiction":{"type":"string","description":"Region/Jurisdiction"},"legalEntity":{"type":"string","description":"Legal Entity"},"taxRegistrationNumber":{"type":"string","description":"Tax Registration Number"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From; new structures are future-dated and never change historical transactions"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"},"owner":{"type":"string","description":"Owner"},"ratePercent":{"type":"number","nullable":true,"description":"Rate in percent (UAE VAT 5); empty when the tax is a fixed amount set on the tax rule"},"taxProfileId":{"type":"string","description":"Tax profile ID; empty on create"},"jurisdictionLevel":{"type":"string","enum":["country","region","municipality"],"description":"Jurisdiction Hierarchy (p.41): the level this profile applies at"},"applicability":{"type":"array","items":{"type":"object","properties":{"level":{"type":"string","enum":["legalEntity","country","market","venue","productCategory","product","service","channel"]},"refId":{"type":"string"}}},"description":"Applicability (p.41): where the profile applies; a channel only where legally applicable"},"taxBase":{"type":"string","enum":["discountedPrice","preDiscountPrice"],"description":"Which price the tax is computed on; preDiscountPrice where the jurisdiction taxes the full price before discount (MoM 1 Sep §4.5, e.g. Egypt). The client sets it per jurisdiction; discountedPrice is the default (decided 29 September, readiness close-out)"}}},
"TaxProfileJurisdictionConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Tax Profile & Jurisdiction Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"taxProfileName":{"type":"string","description":"Tax Profile Name"},"taxProfileCode":{"type":"string","description":"Tax Profile Code"},"taxType":{"type":"string","enum":["vat","gst","salesTax","entertainmentTax","tourismTax","municipalityTax","serviceTax","customRegulatoryTax"],"description":"Tax Type (pp.40-41)"},"country":{"type":"string","description":"Country: ISO 3166-1 alpha-2 code","pattern":"^[A-Z]{2}$"},"jurisdiction":{"type":"string","description":"Region/Jurisdiction"},"legalEntity":{"type":"string","description":"Legal Entity"},"taxRegistrationNumber":{"type":"string","description":"Tax Registration Number"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From; new structures are future-dated and never change historical transactions"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"},"owner":{"type":"string","description":"Owner"},"ratePercent":{"type":"number","nullable":true,"description":"Rate in percent (UAE VAT 5); empty when the tax is a fixed amount set on the tax rule"},"taxProfileId":{"type":"string","description":"Tax profile ID; empty on create"},"jurisdictionLevel":{"type":"string","enum":["country","region","municipality"],"description":"Jurisdiction Hierarchy (p.41): the level this profile applies at"},"applicability":{"type":"array","items":{"type":"object","properties":{"level":{"type":"string","enum":["legalEntity","country","market","venue","productCategory","product","service","channel"]},"refId":{"type":"string"}}},"description":"Applicability (p.41): where the profile applies; a channel only where legally applicable"},"taxBase":{"type":"string","enum":["discountedPrice","preDiscountPrice"],"description":"Which price the tax is computed on; preDiscountPrice where the jurisdiction taxes the full price before discount (MoM 1 Sep §4.5, e.g. Egypt). The client sets it per jurisdiction; discountedPrice is the default (decided 29 September, readiness close-out)"},"consumingProductCount":{"type":"integer","description":"Dependencies: products using the profile; read-only"},"consumingVenueCount":{"type":"integer","description":"Dependencies: venues using the profile; read-only"}}},
"TaxRuleTreatmentBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Tax Rule & Treatment Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"product":{"type":"string","nullable":true,"description":"Condition: product; empty for any"},"productCategory":{"type":"string","nullable":true,"description":"Condition: product category; empty for any"},"venue":{"type":"string","nullable":true,"description":"Condition: venue; empty for any"},"country":{"type":"string","nullable":true,"pattern":"^[A-Z]{2}$","description":"Condition: country; empty for any"},"legalEntity":{"type":"string","nullable":true,"description":"Condition: legal entity; empty for any"},"transactionType":{"type":"string","nullable":true,"description":"Condition: transaction type (sale, refund, amendment, ...); empty for any"},"customerType":{"type":"string","nullable":true,"description":"Condition: customer type, only where legally relevant"},"salesChannel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Condition: sales channel, only where legally relevant; empty for any"},"taxRuleId":{"type":"string","description":"Tax rule ID; empty on create"},"ruleName":{"type":"string","description":"Rule name"},"treatment":{"type":"string","enum":["taxInclusive","taxExclusive","taxExempt","zeroRated","outOfScope"],"description":"Tax Treatment (pp.41-42): inclusive (displayed price contains the tax) or exclusive (tax added on top), exempt, zero rated or out of scope"},"calculationMethod":{"type":"string","enum":["percentage","fixedTax","tiered","compound","sequential","multipleConcurrent"],"description":"Calculation Method (p.42)"},"taxes":{"type":"array","items":{"type":"object","properties":{"taxProfileId":{"type":"string"},"sequence":{"type":"integer","description":"Order of application (Base -> Entertainment Tax -> Municipality Fee -> VAT)"},"onPreviousTaxes":{"type":"boolean","description":"Tax-on-tax: computed on the base plus the taxes before it (MoM 1 Sep §4.5)"},"fixedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Amount when the method is fixedTax"}}},"description":"The tax profiles applied, in configurable sequence (Multiple Taxes, pp.42-43)"},"tiers":{"type":"array","items":{"type":"object","properties":{"fromAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ratePercent":{"type":"number"}}},"description":"Tiers when the method is tiered; empty otherwise"},"exemptionRuleIds":{"type":"array","items":{"type":"string"},"description":"Approved exemption conditions this rule honours (Screen 10.3.6, ADM-073)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"}}},
"TaxRuleTreatmentBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Tax Rule & Treatment Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","nullable":true,"description":"Condition: product; empty for any"},"productCategory":{"type":"string","nullable":true,"description":"Condition: product category; empty for any"},"venue":{"type":"string","nullable":true,"description":"Condition: venue; empty for any"},"country":{"type":"string","nullable":true,"pattern":"^[A-Z]{2}$","description":"Condition: country; empty for any"},"legalEntity":{"type":"string","nullable":true,"description":"Condition: legal entity; empty for any"},"transactionType":{"type":"string","nullable":true,"description":"Condition: transaction type (sale, refund, amendment, ...); empty for any"},"customerType":{"type":"string","nullable":true,"description":"Condition: customer type, only where legally relevant"},"salesChannel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel","description":"Condition: sales channel, only where legally relevant; empty for any"},"taxRuleId":{"type":"string","description":"Tax rule ID; empty on create"},"ruleName":{"type":"string","description":"Rule name"},"treatment":{"type":"string","enum":["taxInclusive","taxExclusive","taxExempt","zeroRated","outOfScope"],"description":"Tax Treatment (pp.41-42): inclusive (displayed price contains the tax) or exclusive (tax added on top), exempt, zero rated or out of scope"},"calculationMethod":{"type":"string","enum":["percentage","fixedTax","tiered","compound","sequential","multipleConcurrent"],"description":"Calculation Method (p.42)"},"taxes":{"type":"array","items":{"type":"object","properties":{"taxProfileId":{"type":"string"},"sequence":{"type":"integer","description":"Order of application (Base -> Entertainment Tax -> Municipality Fee -> VAT)"},"onPreviousTaxes":{"type":"boolean","description":"Tax-on-tax: computed on the base plus the taxes before it (MoM 1 Sep §4.5)"},"fixedAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Amount when the method is fixedTax"}}},"description":"The tax profiles applied, in configurable sequence (Multiple Taxes, pp.42-43)"},"tiers":{"type":"array","items":{"type":"object","properties":{"fromAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"ratePercent":{"type":"number"}}},"description":"Tiers when the method is tiered; empty otherwise"},"exemptionRuleIds":{"type":"array","items":{"type":"string"},"description":"Approved exemption conditions this rule honours (Screen 10.3.6, ADM-073)"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"status":{"type":"string","description":"Status: draft, active, inactive or expired"}}}
}
```
