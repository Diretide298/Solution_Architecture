# WS34 — Pricing   Revenue Management board 1

**10 screens · 15 operations · 24 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-048` | Commercial Pricing Command Center | B–D | 2 | 26 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-049` | Price List Master Configuration | A | 21 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-050` | Price Category & Rate Type Library | A | 12 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-051` | Rate Structure Builder | A | 0 | 4 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-052` | Product & Service Price Assignment | B–D | 0 | 2 | 6 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-053` | Package, Bundle & Add-On Pricing | B–D | 21 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-054` | Market, Venue & Currency Pricing Structure | B–D | 23 | 0 | 5 | 0 | 1 | 4 | — | notStarted (generated) |
| `ADM-055` | Price Hierarchy & Inheritance Configuration | A | 10 | 0 | 5 | 0 | 2 | 0 | — | notStarted (generated) |
| `ADM-056` | Price List Templates, Clone & Reuse | B–D | 18 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-057` | Commercial Pricing Structure Validation | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-050, ADM-057 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-048` Commercial Pricing Command Center

**Provide the central administrative workspace for all commercial pricing structures across This is the first page a Revenue/Pricing Administrator sees when entering the module.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW`, `PRODUCT_VIEW` (2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each price list should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/commercial-pricing-command-center-adm-048` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 1 operation.** Unserved: Create Price List, Duplicate, Open, Compare, Validate, View Dependencies, Export, Archive. Each needs an …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search commercial pricing | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, brand, market, country, currency, product type and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Country | text field | — | — | `listCommercialPricing` ?country |
| Product type | text field | — | — | `listCommercialPricing` ?productType |
| Price list type | select | — | Standard retail · Venue · Attraction · Event · Membership · Group · Corporate · B2B · Reseller · Ota · Internal · Special market | `listCommercialPricing` ?priceListType |
| Venue | text field | — | — | `listCommercialPricing` ?venue |
| Brand | text field | — | — | `listCommercialPricing` ?brand |
| Market | text field | — | — | `listCommercialPricing` ?market |
| Currency | text field | — | pattern `^[A-Z]{3}$` | `listCommercialPricing` ?currency |
| Owner | text field | — | — | `listCommercialPricing` ?owner |
| Status | select | — | Draft · Configured · Validated · Active · Inactive · Expired · Archived | `listCommercialPricing` ?status |
| Search | text field | — | — | `listCommercialPricing` ?search |
| Severity | segmented control | — | Critical · Warning · Information | `listCommercialPricingStructure` ?severity |
| Category | select | — | Price list · Rate structure · Product mapping · Package · Market · Hierarchy | `listCommercialPricingStructure` ?category |
| Price list | text field | — | — | `listCommercialPricingStructure` ?priceListId |

#### Outputs: what the screen shows and produces

**Shown**

**Total Price Lists** (metric tile)

**Active Price Lists** (metric tile)

**Draft Price Lists** (metric tile)

**Price Categories** (metric tile)

**Configured Rates** (metric tile)

**Products with Pricing** (metric tile)

**Products Missing Pricing** (metric tile)

**Markets** (metric tile)

**Currencies** (metric tile)

**Pricing Validation Issues** (metric tile)

**Recently Modified Price Lists** (metric tile)

**Upcoming Price Structures** (metric tile)

**Every commercial pricing** (data table, from `listCommercialPricing`)

| Shows | Format | Notes |
|---|---|---|
| Price list | text | Price List ID |
| Name | text | Name |
| Code | text | Code |
| Type | chip: Standard retail, Venue, Attraction, Event, Membership, Group… | Price List Type (the pack's Price List Types, pp.6-7) |
| Currency | text | Currency: ISO 4217 code of the default currency |
| Market | text | Market |
| Venue | text | Venue |
| Brand | text | Brand |
| Product count | 1,234 | Product Count |
| Rate count | 1,234 | Rate Count |
| Version | text | Version |
| Status | text | Status: draft, configured, validated, active, inactive, expired or archived (p.7); approval and publication are Board 4's |
| Owner | text | Owner |

**The selected commercial pricing** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Price list | text | Price List ID |
| Name | text | Name |
| Code | text | Code |
| Type | chip: Standard retail, Venue, Attraction, Event, Membership, Group… | Price List Type (the pack's Price List Types, pp.6-7) |
| Currency | text | Currency: ISO 4217 code of the default currency |
| Market | text | Market |
| Venue | text | Venue |
| Brand | text | Brand |
| Product count | 1,234 | Product Count |
| Rate count | 1,234 | Rate Count |
| Version | text | Version |
| Status | text | Status: draft, configured, validated, active, inactive, expired or archived (p.7); approval and publication are Board 4's |
| Owner | text | Owner |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** View Pricing, Modify Pricing Structure. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create Price List (primary button) | navigation or local | — | — | — | — |
| Duplicate (secondary button) | navigation or local | — | — | — | — |
| Open (secondary button) | navigation or local | — | — | — | — |
| Compare (secondary button) | navigation or local | — | — | — | — |
| Validate (secondary button) | navigation or local | — | — | — | — |
| View Dependencies (secondary button) | navigation or local | — | — | — | — |
| Export (secondary button) | navigation or local | — | — | — | — |
| Archive (destructive button) | navigation or local | — | — | — | — |

**Data it reads**: `listCommercialPricing` (onLoad, Commercial Pricing Command Center); `listMembershipCommercialPricing` (onLoad, Membership Commercial, Pricing & Channel Association); `listCommercialPricingStructure` (onLoad, Commercial Pricing Structure Validation); `listBundlePricingCommercial` (onLoad, Bundle Pricing & Commercial Model)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-049` Price List Master Configuration: *Works in Price List Master Configuration*; calls `listCommercialPricing`
- → `ADM-050` Price Category & Rate Type Library: *Works in Price Category & Rate Type Library*; calls `listCommercialPricing`
- → `ADM-051` Rate Structure Builder: *Works in Rate Structure Builder*; calls `listCommercialPricing`
- → `ADM-052` Product & Service Price Assignment: *Works in Product & Service Price Assignment*; calls `listCommercialPricing`
- → `ADM-053` Package, Bundle & Add-On Pricing: *Works in Package, Bundle & Add-On Pricing*; calls `listCommercialPricing`
- → `ADM-054` Market, Venue & Currency Pricing Structure: *Works in Market, Venue & Currency Pricing Structure*; calls `listCommercialPricing`
- → `ADM-055` Price Hierarchy & Inheritance Configuration: *Works in Price Hierarchy & Inheritance Configuration*; calls `listCommercialPricing`
- → `ADM-056` Price List Templates, Clone & Reuse: *Works in Price List Templates, Clone & Reuse*; calls `listCommercialPricing`
- → `ADM-057` Commercial Pricing Structure Validation: *Works in Commercial Pricing Structure Validation*; calls `listCommercialPricing`

**What opens over it**

- confirmDialog *Archive*: **Archive on a commercial pricing is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial pricing list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial pricing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial pricing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCommercialPricing` → `PRODUCT_VIEW` (read) · staff
- `listCommercialPricingStructure` → `PRODUCT_VIEW` (read) · staff
- `listBundlePricingCommercial` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*
- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-048` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-048`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 1: Opens Commercial Pricing Command Center → Provide the central administrative workspace for all commercial pricing structures across This is the first page a Revenue/Pricing Administrator sees when entering the module.
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F143 branch at step 1 (expected): when Nothing has been set up on Commercial Pricing Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F143 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-048?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create Price List, Duplicate, Open, Compare, Validate, View Dependencies, Export, Archive.
- [ ] Every transition is wired: `ADM-002`, `ADM-049`, `ADM-050`, `ADM-051`, `ADM-052`, `ADM-053`, `ADM-054`, `ADM-055`, `ADM-056`, `ADM-057`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-049` Price List Master Configuration

**Create the master container that holds commercial rates. A Price List should be reusable across products and channels.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block A · ticket #20641 (APP-SETUP-ADM-049) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-list-master-configuration-adm-049` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Price List Name | select field | — | — | — | — | — | — |
| Price List Code | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Price List Type | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Business Unit | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Default Currency | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Tags | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Default Rate Category | select field | — | — | — | — | — | — |
| Default Rounding Profile | select field | — | — | — | — | — | — |
| Default Price Hierarchy | select field | — | — | — | — | — | — |
| Allow Overrides | select field | — | — | — | — | — | — |
| Allow Inheritance | select field | — | — | — | — | — | — |
| Allow Multiple Currencies | select field | — | — | — | — | — | — |
| Allow Product-Specific Rates | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `setPriceListMaster`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price list master configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price list master untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price list master configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPriceListMaster` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-049` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-049`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 2: Works in Price List Master Configuration → Create the master container that holds commercial rates. A Price List should be reusable across products and channels.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-049?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-050` Price Category & Rate Type Library

**Define standardized commercial rate categories used across TICVAI. This avoids different venues independently creating categories such as: “Adult,” “Adult Standard,” “Normal Adult,” and “Full Adult.”**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block A · ticket #20627 (APP-SETUP-ADM-050) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-category-rate-type-library-adm-050` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Entry kind | segmented control | — | Price category · Rate type | `listPriceCategoryRate` ?entryKind |
| Category family | text field | — | — | `listPriceCategoryRate` ?categoryFamily |
| Active | toggle | — | — | `listPriceCategoryRate` ?active |
| Search | text field | — | — | `listPriceCategoryRate` ?search |

**Form: Save price category rate type** (modal, opened by *Save price category rate type*; *Save price category rate type* calls `setPriceCategoryRateType`, *Cancel* sends nothing)

**Collects what `setPriceCategoryRateType` sends before it is called.** Required: `id`, `scopePath`, `entryKind`, `code`, `name`, `isActive`. Optional: `description`, `categoryFamily`, `displayName`, `localizedDisplayNames`, `iconLabel`, `parentId`, `isStandard`, `sortOrder`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Entry kind `entryKind` | segmented control | required | — | Price category · Rate type | — | — | `setPriceCategoryRateType` body |
| Code `code` | text field | required | — | max length 40 | — | Unique per `entryKind` within the tenant. | `setPriceCategoryRateType` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setPriceCategoryRateType` body |
| Description `description` | text area | optional | — | — | — | — | `setPriceCategoryRateType` body |
| Category family `categoryFamily` | text field | optional | — | max length 60 | — | — | `setPriceCategoryRateType` body |
| Display name `displayName` | text field | optional | — | max length 200 | — | — | `setPriceCategoryRateType` body |
| Localized display names `localizedDisplayNames` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `setPriceCategoryRateType` body |
| Icon label `iconLabel` | text field | optional | — | max length 40 | — | — | `setPriceCategoryRateType` body |
| Parent `parentId` | picker: choose a parent | optional | — | — | shows names, sends the id | A parent `catalogue.price_category` of the same `entryKind`. | `setPriceCategoryRateType` body |
| Is standard `isStandard` | toggle | optional | off | — | — | Shipped with the tenant; may be deactivated, not deleted. | `setPriceCategoryRateType` body |
| Sort order `sortOrder` | number field | optional | 100 | — | — | — | `setPriceCategoryRateType` body |
| Is active `isActive` | toggle | required | on | — | — | — | `setPriceCategoryRateType` body |

Errors to draw in the form: 409 `inUse`.; 422 `invalidParent`.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save price category rate type (primary button) | `setPriceCategoryRateType` PUT `/price-categories` | PriceCategory | PriceCategory | 409 `inUse`.; 422 `invalidParent`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listPriceCategoryRate` (onLoad, Price Category & Rate Type Library)

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `listPriceCategoryRate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price category rate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price category rate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price category rate yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the price category rate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `inUse`.; 422 `invalidParent`. |

#### Permissions

- `listPriceCategoryRate` → `PRODUCT_VIEW` (read) · staff
- `setPriceCategoryRateType` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-050` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-050`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 4: Works in Price Category & Rate Type Library → Define standardized commercial rate categories used across TICVAI. This avoids different venues independently creating categories such as: “Adult,” “Adult Standard,” “Normal Adult,” and “Full Adult.”

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-050?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save price category rate type.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-051` Rate Structure Builder

**Define the actual monetary rates contained within a price list. This is the core commercial configuration screen.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block A · ticket #20642 (APP-SETUP-ADM-051) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Detect) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/rate-structure-builder-adm-051` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 1 operation.** Unserved: Per Ticket, Per Resource, Per Package, Per Membership Period. Each needs an operation, or needs removing …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every rate structure** (data table, from `setRateStructure`)

| Shows | Format | Notes |
|---|---|---|
| Duplicate rates | text | not in the schema: `Duplicate Rates` |
| Validation issues | list or chips (count when long) | Validation (pp.12-13): problems found on this rate; read-only |

**The selected rate structure** (detail panel): The pack groups this record's detail under its own headings: “Adult”, “Child Reduced”, “Senior Reduced”, “Resident Reduced”, “Group Group”, “Each rate should contain”.

| Shows | Format | Notes |
|---|---|---|
| Duplicate rates | text | not in the schema: `Duplicate Rates` |
| Validation issues | list or chips (count when long) | Validation (pp.12-13): problems found on this rate; read-only |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Per Ticket (primary button) | navigation or local | — | — | — | — |
| Per Resource (secondary button) | navigation or local | — | — | — | — |
| Per Package (secondary button) | navigation or local | — | — | — | — |
| Per Membership Period (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `setRateStructure`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rate structure list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rate structure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rate structure yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rate structure are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRateStructure` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-051` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-051`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 6: Works in Rate Structure Builder → Define the actual monetary rates contained within a price list. This is the core commercial configuration screen.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Per Ticket, Per Resource, Per Package, Per Membership Period.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-052` Product & Service Price Assignment

**Connect commercial rates to the actual products and services being sold.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Product configuration should display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/product-service-price-assignment-adm-052` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Ticket Type, Event, Venue. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every product service price** (data table, from `setProductServicePrice`)

| Shows | Format | Notes |
|---|---|---|
| Pricing source: UAE standard admission 2027 | text | not in the schema: `Pricing Source: UAE Standard Admission 2027` |

**The selected product service price** (detail panel): The pack groups this record's detail under its own headings: “Pricing can be assigned to”, “Dependency View”.

| Shows | Format | Notes |
|---|---|---|
| Pricing source: UAE standard admission 2027 | text | not in the schema: `Pricing Source: UAE Standard Admission 2027` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Product Level (primary button) | navigation or local | — | — | — | — |
| Product Variant (secondary button) | navigation or local | — | — | — | — |
| Ticket Type (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `setProductServicePrice`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product service price list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product service price untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product service price yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product service price are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setProductServicePrice` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*
- UX reference: a competitor's pricing matrix that configures channel-and-variant pricing in one matrix view (e.g. adult/child x onsite/online/kiosk). Qossai: not to copy it, but match or improve on it. *(client request · MoM 31 Aug 2026, 4.11 Sales Channel, Pricing & Inventory Allocation · DI-582)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-052` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-052`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 8: Works in Product & Service Price Assignment → Connect commercial rates to the actual products and services being sold.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-052?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Product Level, Product Variant, Ticket Type, Event, Venue.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-053` Package, Bundle & Add-On Pricing

**Provide dedicated commercial structures for products containing multiple components. This is separate from the Product Relationship/Bundle module. Product Catalogue defines what the bundle contains. Pricing defines how that bundle is priced.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure pricing for; Configure whether the customer sees) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/package-bundle-add-on-pricing-adm-053` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Fast Track | select field | — | — | — | — | — | — |
| Parking | select field | — | — | — | — | — | — |
| Meal | select field | — | — | — | — | — | — |
| Photo | select field | — | — | — | — | — | — |
| Equipment | select field | — | — | — | — | — | — |
| Upgrade | select field | — | — | — | — | — | — |
| Additional Session | select field | — | — | — | — | — | — |
| Premium Access | select field | — | — | — | — | — | — |
| Package Total Only | select field | — | — | — | — | — | — |
| Individual Components | select field | — | — | — | — | — | — |
| Component + Package Saving | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Record kind | segmented control | — | Package · Bundle · Add on | `listPackageBundleAdd` ?recordKind |
| Pricing model | radio group | — | Fixed package price · Sum of components · Discounted component sum · Component override | `listPackageBundleAdd` ?pricingModel |
| Status | radio group | — | Draft · Active · Disabled · Expired | `listPackageBundleAdd` ?status |
| Search | text field | — | — | `listPackageBundleAdd` ?search |

**Form: Save package pricing definition** (modal, opened by *Save package pricing definition*; *Save package pricing definition* calls `setPackagePricingDefinition`, *Cancel* sends nothing)

**Collects what `setPackagePricingDefinition` sends before it is called.** Required: `id`, `scopePath`, `productId`, `recordKind`, `pricingModel`, `status`. Optional: `name`, `priceListId`, `addOnType`, `packagePrice`, `components`, `componentPriceVisibility`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Product `productId` | picker: choose a product | required | — | — | shows names, sends the id | — | `setPackagePricingDefinition` body |
| Record kind `recordKind` | segmented control | required | — | Package · Bundle · Add on | — | — | `setPackagePricingDefinition` body |
| Name `name` | text field | optional | — | max length 200 | — | — | `setPackagePricingDefinition` body |
| Price list `priceListId` | picker: choose a price list | optional | — | — | shows names, sends the id | — | `setPackagePricingDefinition` body |
| Pricing model `pricingModel` | radio group | required | — | Fixed package price · Sum of components · Discounted component sum · Component override | — | — | `setPackagePricingDefinition` body |
| Add on type `addOnType` | select | optional | — | Fast track · Parking · Meal · Photo · Equipment · Upgrade · Additional performance · Premium access · Other | — | — | `setPackagePricingDefinition` body |
| Package price `packagePrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setPackagePricingDefinition` body |
| Components `components` | key and value settings | optional | — | `[{productId, quantity, role, componentPrice}]`; `componentPrice` only for `componentOverride`. | — | `[{productId, quantity, role, componentPrice}]`; `componentPrice` only for `componentOverride`. | `setPackagePricingDefinition` body |
| Component price visibility `componentPriceVisibility` | segmented control | optional | Package total only | Package total only · Individual components · Component and saving | — | — | `setPackagePricingDefinition` body |
| Status `status` | radio group | required | Draft | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setPackagePricingDefinition` body |

Errors to draw in the form: 409 `changeRequestRequired`.; 422 `priceRequired` or `circularComponent`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fixed Package Price (primary button) | navigation or local | — | — | — | — |
| Component Override (secondary button) | navigation or local | — | — | — | — |
| Save package pricing definition (secondary button) | `setPackagePricingDefinition` PUT `/package-pricing` | PackagePricing | PackagePricing | 409 `changeRequestRequired`.; 422 `priceRequired` or `circularComponent`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listPackageBundleAdd` (onLoad, Package, Bundle & Add-On Pricing)

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `listPackageBundleAdd`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The package bundle add-on configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the package bundle add-on untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No package bundle add-on configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `changeRequestRequired`.; 422 `priceRequired` or `circularComponent`. |

#### Permissions

- `listPackageBundleAdd` → `PRODUCT_VIEW` (read) · staff
- `setPackagePricingDefinition` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-053` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-053`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 10: Works in Package, Bundle & Add-On Pricing → Provide dedicated commercial structures for products containing multiple components. This is separate from the Product Relationship/Bundle module. Product Catalogue defines what the bundle contains. …

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-053?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fixed Package Price, Component Override, Save package pricing definition.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-054` Market, Venue & Currency Pricing Structure

**Support TICVAI's multi-country, multi-market, multi-venue and multi-currency commercial model.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; FX-Assisted Setup) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/market-venue-currency-pricing-structure-adm-054` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Country | select field | — | — | — | — | — | — |
| Market | select field | — | — | — | — | — | — |
| Region | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Brand | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| AED 250 ≈ SAR 255 | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Hierarchy level | radio group | — | Global · Country · Region · Market · Venue | `listMarketVenueCurrency` ?hierarchyLevel |
| Country | text field | — | — | `listMarketVenueCurrency` ?country |
| Market | text field | — | — | `listMarketVenueCurrency` ?market |
| Venue | text field | — | — | `listMarketVenueCurrency` ?venue |
| Legal entity | text field | — | — | `listMarketVenueCurrency` ?legalEntity |
| Currency | text field | — | pattern `^[A-Z]{3}$` | `listMarketVenueCurrency` ?currency |

**Form: Save market pricing configuration** (modal, opened by *Save market pricing configuration*; *Save market pricing configuration* calls `setMarketPricingConfiguration`, *Cancel* sends nothing)

**Collects what `setMarketPricingConfiguration` sends before it is called.** Required: `id`, `scopePath`, `hierarchyLevel`. Optional: `parentId`, `countryCode`, `marketCode`, `region`, `venueId`, `brand`, `legalEntityId`, `baseCurrency`, `sellingCurrency`, `roundingProfileId`, `displayFormat`, `priceListId` and 2 more. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Hierarchy level `hierarchyLevel` | radio group | required | — | Global · Country · Region · Market · Venue | — | — | `setMarketPricingConfiguration` body |
| Parent `parentId` | picker: choose a parent | optional | — | — | shows names, sends the id | The parent `catalogue.pricing_market`. | `setMarketPricingConfiguration` body |
| Country code `countryCode` | text field | optional | — | max length 2; pattern `^[A-Z]{2}$` | — | — | `setMarketPricingConfiguration` body |
| Market code `marketCode` | text field | optional | — | max length 40 | — | — | `setMarketPricingConfiguration` body |
| Region `region` | text field | optional | — | max length 100 | — | — | `setMarketPricingConfiguration` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setMarketPricingConfiguration` body |
| Brand `brand` | text field | optional | — | max length 100 | — | — | `setMarketPricingConfiguration` body |
| Legal entity `legalEntityId` | picker: choose a legal entity | optional | — | — | shows names, sends the id | — | `setMarketPricingConfiguration` body |
| Base currency `baseCurrency` | text field | optional | — | max length 3; pattern `^[A-Z]{3}$` | — | — | `setMarketPricingConfiguration` body |
| Selling currency `sellingCurrency` | text field | optional | — | max length 3; pattern `^[A-Z]{3}$` | — | — | `setMarketPricingConfiguration` body |
| Rounding profile `roundingProfileId` | picker: choose a rounding profile | optional | — | — | shows names, sends the id | — | `setMarketPricingConfiguration` body |
| Display format `displayFormat` | text field | optional | — | max length 40 | — | — | `setMarketPricingConfiguration` body |
| Price list `priceListId` | picker: choose a price list | optional | — | — | shows names, sends the id | — | `setMarketPricingConfiguration` body |
| Inherits from parent `inheritsFromParent` | toggle | optional | on | — | — | — | `setMarketPricingConfiguration` body |
| FX reference rate `fxReferenceRate` | number field (%) | optional | — | — | — | Reference only; FX supplies inputs, it never decides a price. | `setMarketPricingConfiguration` body |

Errors to draw in the form: 422 `currencyNotVenueCurrency` or `invalidParent`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save market pricing configuration (primary button) | `setMarketPricingConfiguration` PUT `/pricing-markets` | PricingMarket | PricingMarket | 422 `currencyNotVenueCurrency` or `invalidParent`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listMarketVenueCurrency` (onLoad, Market, Venue & Currency Pricing Structure)

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `listMarketVenueCurrency`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The market venue currency configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the market venue currency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No market venue currency configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `currencyNotVenueCurrency` or `invalidParent`. |

#### Permissions

- `listMarketVenueCurrency` → `PRODUCT_VIEW` (read) · staff
- `setMarketPricingConfiguration` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Pricing module (~7 sub-screens): overview dashboard of all pricing setups and status; price lists per channel, segment or product category (several can coexist); price categories/rate types (adult, child, member); rate structure; product-rate association; bundle/add-on pricing; multi-market/currency pricing. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-591)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A43** Design multi-currency display to support both manual FX-rate entry (with configurable margin) and an optional real-time third-party FX-rate API; confirm which payment gateway(s) support Dynamic Currency Conversion (DCC) *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'multi-currency')*
- **A44** Add a foreign-currency collection report (transactions collected broken down by foreign currency) to the Finance reporting suite *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'foreign currency')*
- **C23** Confirm foreign-currency display approach (manual FX-rate entry with margin vs. live third-party FX-rate API) and confirm the payment gateway that will support Dynamic Currency Conversion *(Qossai / Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'fx-rate')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'multi-currency')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-054` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-054`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 12: Works in Market, Venue & Currency Pricing Structure → Support TICVAI's multi-country, multi-market, multi-venue and multi-currency commercial model.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-054?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save market pricing configuration.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-055` Price Hierarchy & Inheritance Configuration

**Define where TICVAI should obtain a price when multiple commercial pricing layers exist. This is essential to prevent conflicting prices.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | Block A · ticket #20643 (APP-SETUP-ADM-055) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators configure; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-hierarchy-inheritance-configuration-adm-055` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Hierarchy Level | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Inheritance | select field | — | — | — | — | — | — |
| Override Permission | select field | — | — | — | — | — | — |
| Fallback Behavior | select field | — | — | — | — | — | — |
| Override Allowed | select field | — | — | — | — | — | — |
| Override Requires Reason | select field | — | — | — | — | — | — |
| Maximum Override Range | select field | — | — | — | — | — | — |
| Override Expiry | select field | — | — | — | — | — | — |
| Return to Parent Price | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `setPriceHierarchyInheritance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price hierarchy inheritance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price hierarchy inheritance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price hierarchy inheritance configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setPriceHierarchyInheritance` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- When several rules apply to one sale (e.g. summer rate plus school-group discount) the configurable pricing hierarchy decides; there is no automatic lowest-price-wins default. *(agreed · MoM 1 Sep 2026, 4.4 Seasonal & Date-Based Pricing; Rule Priority · DI-595)*
- Price hierarchy screen sets which level (category, item, segment) takes precedence; price lists can be cloned (e.g. B2C copied and discounted for B2B); a final validation screen confirms setup is complete. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-592)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-055` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-055`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 14: Works in Price Hierarchy & Inheritance Configuration → Define where TICVAI should obtain a price when multiple commercial pricing layers exist. This is essential to prevent conflicting prices.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-055?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-056` Price List Templates, Clone & Reuse

**Accelerate commercial setup across new venues, events, seasons and markets.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/price-list-templates-clone-reuse-adm-056` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Complete Price List, Rate Structure Only, Selected Categories, Product Assignments, Market Structure. Each …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ☑ Copy categories | select field | — | — | — | — | — | — |
| ☑ Copy rate structure | text field | — | — | — | — | — | — |
| ☑ Copy product mapping | text field | — | — | — | — | — | — |
| ☐ Copy monetary values | text field | — | — | — | — | — | — |
| ☑ Increase values by 5% | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Template type | text field | — | — | `listPriceListTemplate` ?templateType |
| Status | segmented control | — | Draft · Active · Archived | `listPriceListTemplate` ?status |
| Search | text field | — | — | `listPriceListTemplate` ?search |

**Form: Save configuration template** (modal, opened by *Save configuration template*; *Save configuration template* calls `setConfigurationTemplate`, *Cancel* sends nothing)

**Collects what `setConfigurationTemplate` sends before it is called.** Required: `id`, `scopePath`, `subject`, `name`, `status`. Optional: `description`, `templateKind`, `productKind`, `venueId`, `sourceProductId`, `sourcePriceListId`, `includedComponents`, `reviewFields`, `isAiDrafted`, `ownerPrincipalId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Subject `subject` | segmented control | required | — | Product · Price list | — | — | `setConfigurationTemplate` body |
| Name `name` | text field | required | — | max length 200 | — | — | `setConfigurationTemplate` body |
| Description `description` | text area | optional | — | — | — | — | `setConfigurationTemplate` body |
| Template kind `templateKind` | text field | optional | — | max length 60 | — | Product: `ProductDuplicationTemplateLibraryView.templateKind`; price list: its `templateType`. | `setConfigurationTemplate` body |
| Product kind `productKind` | select | optional | — | Admission · Timed admission · Dated admission · Open dated · Seated · Membership · Bundle · Fnb · Retail · Rental · Add on · Gift card | — | `openDated` added 24 August from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: valid on any date within an eligible … | `setConfigurationTemplate` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |
| Source product `sourceProductId` | picker: choose a source product | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |
| Source price list `sourcePriceListId` | picker: choose a source price list | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |
| Included components `includedComponents` | list of values (chips) | optional | — | — | — | Product or price-list component names, per `subject`. | `setConfigurationTemplate` body |
| Review fields `reviewFields` | multi-select chips | optional | — | Dates · Prices · Venue · Capacity · Event · Tax · Channels | — | — | `setConfigurationTemplate` body |
| Is AI drafted `isAiDrafted` | toggle | optional | off | — | — | — | `setConfigurationTemplate` body |
| Status `status` | radio group | required | Draft | Draft · Active · Inactive · Retired | — | The status of a catalogue configuration record (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles … | `setConfigurationTemplate` body |
| Owner principal `ownerPrincipalId` | picker: choose an owner principal | optional | — | — | shows names, sends the id | — | `setConfigurationTemplate` body |

Errors to draw in the form: 422 `sourceRequired`.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Complete Price List (primary button) | navigation or local | — | — | — | — |
| Rate Structure Only (secondary button) | navigation or local | — | — | — | — |
| Selected Categories (secondary button) | navigation or local | — | — | — | — |
| Product Assignments (secondary button) | navigation or local | — | — | — | — |
| Market Structure (secondary button) | navigation or local | — | — | — | — |
| Save configuration template (secondary button) | `setConfigurationTemplate` PUT `/configuration-templates` | ConfigurationTemplate | ConfigurationTemplate | 422 `sourceRequired`. | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listPriceListTemplate` (onLoad, Price List Templates, Clone & Reuse)

**Where the user goes next**

- → `ADM-048` Commercial Pricing Command Center: *Returns to the board's landing screen*; calls `listPriceListTemplate`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price list templates configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price list templates untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price list templates configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 `sourceRequired`. |

#### Permissions

- `listPriceListTemplate` → `PRODUCT_VIEW` (read) · staff
- `setConfigurationTemplate` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price hierarchy screen sets which level (category, item, segment) takes precedence; price lists can be cloned (e.g. B2C copied and discounted for B2B); a final validation screen confirms setup is complete. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-592)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-056` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-056`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 16: Works in Price List Templates, Clone & Reuse → Accelerate commercial setup across new venues, events, seasons and markets.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-056?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Complete Price List, Rate Structure Only, Selected Categories, Product Assignments, Market Structure, Save configuration template.
- [ ] Every transition is wired: `ADM-048`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-057` Commercial Pricing Structure Validation

**Validate that the commercial pricing foundation is structurally complete before it proceeds to rule configuration, governance, or publication. This is not the final publication screen. Board 4 owns approval and publication. Board 1 defined what the commercial prices are and how they are structured.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `ticketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRODUCT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/commercial-pricing-structure-validation-adm-057` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Severity | segmented control | — | Critical · Warning · Information | `listCommercialPricingStructure` ?severity |
| Category | select | — | Price list · Rate structure · Product mapping · Package · Market · Hierarchy | `listCommercialPricingStructure` ?category |
| Price list | text field | — | — | `listCommercialPricingStructure` ?priceListId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCommercialPricingStructure` (onLoad, Commercial Pricing Structure Validation)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial pricing structure list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial pricing structure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial pricing structure yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial pricing structure are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCommercialPricingStructure` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price hierarchy screen sets which level (category, item, segment) takes precedence; price lists can be cloned (e.g. B2C copied and discounted for B2B); a final validation screen confirms setup is complete. *(client request · MoM 1 Sep 2026, 4.1 Pricing Foundation & Structure · DI-592)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-057` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS95 Pricing   Revenue Management Board 1.dc.html#adm-057`
- Workshop pack: Pricing___Revenue_Management_Reference.pdf board 1
- Flow F143 *Pricing Revenue Management board 1: Commercial Pricing Command Center*, step 18: Works in Commercial Pricing Structure Validation → Validate that the commercial pricing foundation is structurally complete before it proceeds to rule configuration, governance, or publication. This is not the final publication screen. Board 4 owns …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-057?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**12 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listBundlePricingCommercial": {"method":"GET","path":"/bundle-pricing-commercial","contract":"promotions","summary":"Bundle Pricing & Commercial Model","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundlePricingCommercialModelView"},
"listCommercialPricing": {"method":"GET","path":"/commercial-pricing","contract":"catalogue","summary":"Commercial Pricing Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"country","in":"query","required":false},{"name":"productType","in":"query","required":false},{"name":"priceListType","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"brand","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"currency","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCommercialPricingStructure": {"method":"GET","path":"/commercial-pricing-structure","contract":"catalogue","summary":"Commercial Pricing Structure Validation","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":false},{"name":"category","in":"query","required":false},{"name":"priceListId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMarketVenueCurrency": {"method":"GET","path":"/market-venue-currency","contract":"catalogue","summary":"Market, Venue & Currency Pricing Structure","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"hierarchyLevel","in":"query","required":false},{"name":"country","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"legalEntity","in":"query","required":false},{"name":"currency","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPackageBundleAdd": {"method":"GET","path":"/package-bundle-add","contract":"catalogue","summary":"Package, Bundle & Add-On Pricing","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"recordKind","in":"query","required":false},{"name":"pricingModel","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceCategoryRate": {"method":"GET","path":"/price-category-rate","contract":"catalogue","summary":"Price Category & Rate Type Library","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"entryKind","in":"query","required":false},{"name":"categoryFamily","in":"query","required":false},{"name":"active","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPriceListTemplate": {"method":"GET","path":"/price-list-template","contract":"catalogue","summary":"Price List Templates, Clone & Reuse","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"templateType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setConfigurationTemplate": {"method":"PUT","path":"/configuration-templates","contract":"catalogue","summary":"Create or update a product or price-list template","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConfigurationTemplate","responds":"ConfigurationTemplate"},
"setMarketPricingConfiguration": {"method":"PUT","path":"/pricing-markets","contract":"catalogue","summary":"Create or update a node of the market pricing structure","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingMarket","responds":"PricingMarket"},
"setPackagePricingDefinition": {"method":"PUT","path":"/package-pricing","contract":"catalogue","summary":"Set how a package, bundle or add-on is priced","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PackagePricing","responds":"PackagePricing"},
"setPriceCategoryRateType": {"method":"PUT","path":"/price-categories","contract":"catalogue","summary":"Create or update a price category or rate type","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PriceCategory","responds":"PriceCategory"},
"setPriceHierarchyInheritance": {"method":"PUT","path":"/price-hierarchy-inheritance","contract":"catalogue","summary":"Price Hierarchy & Inheritance Configuration","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PriceHierarchyInheritanceConfigurationInput","responds":"PriceHierarchyInheritanceConfigurationView"},
"setPriceListMaster": {"method":"PUT","path":"/price-list-master","contract":"catalogue","summary":"Price List Master Configuration","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PriceListMasterConfigurationInput","responds":"PriceListMasterConfigurationView"},
"setProductServicePrice": {"method":"PUT","path":"/product-service-price","contract":"catalogue","summary":"Product & Service Price Assignment","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ProductServicePriceAssignmentInput","responds":"ProductServicePriceAssignmentView"},
"setRateStructure": {"method":"PUT","path":"/rate-structure","contract":"catalogue","summary":"Rate Structure Builder","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RateStructureBuilderInput","responds":"RateStructureBuilderView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BundlePricingCommercialModelView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Pricing & Commercial Model displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Base price"},"currency":{"type":"string","description":"Currency"},"discount":{"type":"number","description":"Discount %"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount amount"},"minimumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum price"},"maximumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum price"},"priceFloor":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price floor"},"marginFloor":{"type":"number","description":"Margin floor"},"guestSpecificPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Guest-specific price"},"channelSpecificPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Channel-specific price"},"pricingModel":{"type":"string","enum":["fixedBundlePrice","sumMinusDiscount","componentPricing","startingFrom","tieredBundlePrice","dynamicBundlePrice"],"description":"How the bundle is priced; a dynamic bundle price is calculated by the pricing engine"},"upgradeCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Surcharge when the guest picks a premium option"}}},
"CatalogueConfigStatus": {"type":"string","enum":["draft","active","inactive","retired"],"description":"**The status of a catalogue configuration record** (29 September, data model DM3): price lists, rates, fees and fee rules, tax profiles and rules, calculation and rounding profiles, package pricing and templates. `draft` is being prepared and is never used by a calculation; `active` is in use from its effective date; `inactive` is switched off and may be switched back; `retired` is kept for history only. A record already used by a live price becomes `active` through a published change request, not by an edit."},
"CommercialPricingCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Commercial Pricing Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"totalPriceLists":{"type":"integer","description":"Total Price Lists"},"activePriceLists":{"type":"integer","description":"Active Price Lists"},"draftPriceLists":{"type":"integer","description":"Draft Price Lists"},"priceCategories":{"type":"integer","description":"Price Categories"},"configuredRates":{"type":"integer","description":"Configured Rates"},"productsWithPricing":{"type":"integer","description":"Products with Pricing: sellable products that reference at least one active price list rate"},"productsMissingPricing":{"type":"integer","description":"Products Missing Pricing: active sellable products with no price list rate"},"markets":{"type":"integer","description":"Markets"},"currencies":{"type":"integer","description":"Currencies"},"pricingValidationIssues":{"type":"integer","description":"Pricing Validation Issues"},"recentlyModifiedPriceLists":{"type":"integer","description":"Recently Modified Price Lists: price lists changed in the last 7 days (decided 29 September, readiness close-out)"},"upcomingPriceStructures":{"type":"integer","description":"Upcoming Price Structures: price lists whose effective-from date is in the future"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI observations for this screen; advisory only, never applied automatically"}}},
"CommercialPricingCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Commercial Pricing Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"priceListId":{"type":"string","description":"Price List ID"},"name":{"type":"string","description":"Name"},"code":{"type":"string","description":"Code"},"type":{"type":"string","enum":["standardRetail","venue","attraction","event","membership","group","corporate","b2b","reseller","ota","internal","specialMarket"],"description":"Price List Type (the pack's Price List Types, pp.6-7)"},"currency":{"type":"string","description":"Currency: ISO 4217 code of the default currency","pattern":"^[A-Z]{3}$"},"market":{"type":"string","description":"Market"},"venue":{"type":"string","description":"Venue"},"brand":{"type":"string","description":"Brand"},"productCount":{"type":"integer","description":"Product Count"},"rateCount":{"type":"integer","description":"Rate Count"},"version":{"type":"string","description":"Version"},"status":{"type":"string","description":"Status: draft, configured, validated, active, inactive, expired or archived (p.7); approval and publication are Board 4's"},"owner":{"type":"string","description":"Owner"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From (the first half of the pack's Effective Period)"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"CommercialPricingStructureValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Commercial Pricing Structure Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"findingId":{"type":"string","description":"Finding ID"},"category":{"type":"string","enum":["priceList","rateStructure","productMapping","package","market","hierarchy"],"description":"Validation Category (pp.19-20)"},"check":{"type":"string","enum":["requiredFieldsComplete","currencyDefined","ownershipAssigned","categoriesConfigured","monetaryValuesValid","derivedRelationshipsValid","requiredProductsPriced","noOrphanAssignments","componentPricingValid","currencyAndVenueConfigurationValid","noConflictingSourcePriority","fallbackConfigured"],"description":"The check that failed"},"severity":{"type":"string","enum":["critical","warning","information"],"description":"Validation Results: critical (sale cannot proceed), warning (review), information (optimization suggestion)"},"message":{"type":"string","description":"What was found, e.g. \"7 active ticket products have no Adult rate\""},"subjectType":{"type":"string","enum":["priceList","rate","priceCategory","product","package","venue","market","hierarchy"],"description":"What the finding is about"},"subjectId":{"type":"string","description":"ID of that record"},"aiGenerated":{"type":"boolean","description":"Raised by AI QA rather than a rule; advisory"}}},
"ConfigurationTemplate": {"type":"object","x-ticvai-persistence":"catalogue.configuration_template","description":"**A reusable starting point for a product or a price list** (29 September, data model DM3). Merges the product duplication and template library (ADM-126) and price list templates (ADM-063). `subject` says which; a template copies the listed components and marks `reviewFields` for the operator to confirm.","required":["id","scopePath","subject","name","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"subject":{"type":"string","enum":["product","priceList"]},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"templateKind":{"type":"string","maxLength":60,"nullable":true,"description":"Product: `ProductDuplicationTemplateLibraryView.templateKind`; price list: its `templateType`."},"productKind":{"allOf":[{"$ref":"#/components/schemas/ProductKind"}],"nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"sourceProductId":{"type":"string","format":"uuid","nullable":true},"sourcePriceListId":{"type":"string","format":"uuid","nullable":true},"includedComponents":{"type":"array","items":{"type":"string"},"description":"Product or price-list component names, per `subject`."},"reviewFields":{"type":"array","items":{"type":"string","enum":["dates","prices","venue","capacity","event","tax","channels"]}},"isAiDrafted":{"type":"boolean","default":false},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"draft"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MarketVenueCurrencyPricingStructureView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Market, Venue & Currency Pricing Structure displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"country":{"type":"string","description":"Country"},"market":{"type":"string","description":"Market"},"region":{"type":"string","description":"Region"},"venue":{"type":"string","description":"Venue"},"brand":{"type":"string","description":"Brand"},"legalEntity":{"type":"string","description":"Legal Entity"},"baseCurrency":{"type":"string","description":"Base Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"sellingCurrency":{"type":"string","description":"Selling Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"currencyPrecision":{"type":"integer","description":"Currency Precision: decimal places, 0 to 3","minimum":0,"maximum":3},"rounding":{"type":"string","description":"Rounding: code of the currency rounding rule (ADM-075)"},"displayFormat":{"type":"string","description":"Display Format: e.g. \"AED 1,250.00\" or \"1.250,00 EUR\""},"structureId":{"type":"string","description":"Pricing structure node ID"},"hierarchyLevel":{"type":"string","enum":["global","country","region","market","venue"],"description":"Level of this node in the Market Hierarchy (p.15)"},"parentStructureId":{"type":"string","nullable":true,"description":"Parent node; empty for Global"},"priceListId":{"type":"string","nullable":true,"description":"Price list governing this node; empty when it inherits"},"inheritsFromParent":{"type":"boolean","description":"Venue Overrides (p.16): true when the node uses its parent's prices (Abu Dhabi Venue -> inherit AED 250)"},"fxReferenceRate":{"type":"number","nullable":true,"description":"FX-Assisted Setup: reference rate base -> selling currency shown during setup; advisory"}}},
"PackageBundleAddOnPricingView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Package, Bundle & Add-On Pricing displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"packagePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Package Price: the fixed or derived price charged for the package (AED 850 in the example)"},"pricingId":{"type":"string","description":"Package / add-on pricing ID"},"recordKind":{"type":"string","enum":["package","bundle","addOn"],"description":"What is priced"},"productId":{"type":"string","description":"The catalogue package, bundle or add-on product"},"name":{"type":"string","description":"Name"},"priceListId":{"type":"string","description":"Price list the pricing belongs to"},"pricingModel":{"type":"string","enum":["fixedPackagePrice","sumOfComponents","discountedComponentSum","componentOverride"],"description":"Package Pricing Model (p.14)","nullable":true},"addOnType":{"type":"string","enum":["fastTrack","parking","meal","photo","equipment","upgrade","additionalPerformance","premiumAccess","other"],"description":"Add-On Pricing kind (p.15); additionalPerformance is the design's \"additional session\"; empty for a package","nullable":true},"components":{"type":"array","items":{"type":"object","properties":{"productId":{"type":"string"},"quantity":{"type":"integer"},"role":{"type":"string","enum":["included","requiredPaid","optionalPaid"]},"componentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"description":"Components with their role (Required vs Optional, p.15) and the price each contributes"},"normalTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Normal Total: sum of the components at their own rates; read-only"},"packageSaving":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commercial package saving: normal total less package price; read-only"},"componentPriceVisibility":{"type":"string","enum":["packageTotalOnly","individualComponents","componentAndSaving"],"description":"Component Price Visibility (p.15): what the customer sees"},"status":{"type":"string","description":"Status: draft, active, disabled or expired"},"validationIssues":{"type":"array","description":"Bundle Price Integrity (p.15)","items":{"type":"object","properties":{"code":{"type":"string","enum":["componentPriceChanged","missingComponentRate","packageAboveNormalTotal"]},"message":{"type":"string"}}}}}},
"PackagePricing": {"type":"object","x-ticvai-persistence":"catalogue.package_pricing","description":"**How a package, bundle or add-on is priced from its components** (29 September, data model DM3). ADM-062. The bundle's composition for sale stays `catalogue.published_bundle`; this row is its pricing model. `normalTotal` and `packageSaving` are computed on read from the component rates.","required":["id","scopePath","productId","recordKind","pricingModel","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"productId":{"type":"string","format":"uuid"},"recordKind":{"type":"string","enum":["package","bundle","addOn"]},"name":{"type":"string","maxLength":200,"nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"pricingModel":{"type":"string","enum":["fixedPackagePrice","sumOfComponents","discountedComponentSum","componentOverride"]},"addOnType":{"type":"string","enum":["fastTrack","parking","meal","photo","equipment","upgrade","additionalPerformance","premiumAccess","other",null],"nullable":true},"packagePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"components":{"type":"object","additionalProperties":true,"description":"`[{productId, quantity, role, componentPrice}]`; `componentPrice` only for `componentOverride`."},"componentPriceVisibility":{"type":"string","enum":["packageTotalOnly","individualComponents","componentAndSaving"],"default":"packageTotalOnly"},"status":{"allOf":[{"$ref":"#/components/schemas/CatalogueConfigStatus"}],"default":"draft"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PriceCategory": {"type":"object","x-ticvai-persistence":"catalogue.price_category","description":"**The library of price categories and rate types** (29 September, data model DM3). ADM-059. A price category is who or what is priced (Adult, Child, Resident ...); a rate type is how (Standard, Peak, Member ...). Both are rows here, `entryKind` says which. Distinct from `catalogue.product_category`, which groups merchandise.","required":["id","scopePath","entryKind","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."},"entryKind":{"type":"string","enum":["priceCategory","rateType"]},"code":{"type":"string","maxLength":40,"description":"Unique per `entryKind` within the tenant."},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"categoryFamily":{"type":"string","maxLength":60,"nullable":true},"displayName":{"type":"string","maxLength":200,"nullable":true},"localizedDisplayNames":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"iconLabel":{"type":"string","maxLength":40,"nullable":true},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"A parent `catalogue.price_category` of the same `entryKind`."},"isStandard":{"type":"boolean","default":false,"description":"Shipped with the tenant; may be deactivated, not deleted."},"sortOrder":{"type":"integer","default":100},"isActive":{"type":"boolean","default":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"PriceCategoryRateTypeLibraryView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price Category & Rate Type Library displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"categoryId":{"type":"string","description":"Category ID"},"name":{"type":"string","description":"Name"},"code":{"type":"string","description":"Code"},"description":{"type":"string","description":"Description"},"categoryFamily":{"type":"string","description":"Category Family: e.g. Visitor or Member (Parent/Child Structure, p.10)"},"displayName":{"type":"string","description":"Display Name"},"iconLabel":{"type":"string","description":"Icon/Label"},"active":{"type":"boolean","description":"Active/Inactive: true when the category can be used on new rates"},"entryKind":{"type":"string","enum":["priceCategory","rateType"],"description":"Whether the row is a price category (who the price represents) or a rate type (how the rate behaves: standard, reduced, contract, negotiated, complimentary, fixed, derived, package, add-on), p.10"},"standard":{"type":"boolean","description":"A TICVAI standard category (Adult, Child, Junior, Senior, Student, Resident, Non-Resident, Member, VIP, Group, Corporate, B2B, Complimentary, Staff, Promotional) rather than a custom one"},"sortOrder":{"type":"integer","description":"Sort Order"},"parentCategoryId":{"type":"string","nullable":true,"description":"Parent category (Parent/Child Structure: Visitor -> Adult, Member -> Gold); empty for a top-level category"},"localizedDisplayNames":{"type":"object","additionalProperties":{"type":"string"},"description":"Display name per language code, at least en and ar (Localization, p.11)"},"possibleDuplicateOf":{"type":"array","items":{"type":"string"},"description":"AI Standardization: ids of categories that appear to mean the same thing (Kids / Child / Children Rate); advisory"}}},
"PriceHierarchyInheritanceConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.price_list at 17%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Price Hierarchy & Inheritance Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"hierarchyId":{"type":"string","description":"Price hierarchy ID; empty on create"},"name":{"type":"string","description":"Hierarchy name"},"levels":{"type":"array","items":{"type":"object","properties":{"hierarchyLevel":{"type":"string","enum":["globalMaster","country","market","venue","product","approvedOverride"],"description":"Hierarchy Level (Example Hierarchy, p.17)"},"priority":{"type":"integer","description":"Priority; the lower number is the more general level, the most specific existing price wins"},"inheritance":{"type":"boolean","description":"Inheritance: the level takes its parent's price when it has none of its own"},"overrideAllowed":{"type":"boolean","description":"Override Permission / Override Allowed"},"overrideRequiresReason":{"type":"boolean","description":"Override Requires Reason"},"maximumOverrideRangePercent":{"type":"number","nullable":true,"description":"Maximum Override Range: largest allowed deviation from the parent price, in percent; empty for no limit"},"overrideExpiryDays":{"type":"integer","nullable":true,"description":"Override Expiry: days an override stays in force; empty for no expiry (decided 29 September, readiness close-out)"},"returnToParentPrice":{"type":"boolean","description":"Return to Parent Price when an override expires"},"fallbackBehavior":{"type":"string","enum":["useParent","useDefault","blockSale"],"description":"Fallback (p.18): what happens when a child rate does not exist"}}},"description":"Hierarchy Builder (p.17): the ordered levels; saved as a whole so two sources can never be left at equal priority"}}},
"PriceHierarchyInheritanceConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price Hierarchy & Inheritance Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"hierarchyId":{"type":"string","description":"Price hierarchy ID; empty on create"},"name":{"type":"string","description":"Hierarchy name"},"levels":{"type":"array","items":{"type":"object","properties":{"hierarchyLevel":{"type":"string","enum":["globalMaster","country","market","venue","product","approvedOverride"],"description":"Hierarchy Level (Example Hierarchy, p.17)"},"priority":{"type":"integer","description":"Priority; the lower number is the more general level, the most specific existing price wins"},"inheritance":{"type":"boolean","description":"Inheritance: the level takes its parent's price when it has none of its own"},"overrideAllowed":{"type":"boolean","description":"Override Permission / Override Allowed"},"overrideRequiresReason":{"type":"boolean","description":"Override Requires Reason"},"maximumOverrideRangePercent":{"type":"number","nullable":true,"description":"Maximum Override Range: largest allowed deviation from the parent price, in percent; empty for no limit"},"overrideExpiryDays":{"type":"integer","nullable":true,"description":"Override Expiry: days an override stays in force; empty for no expiry (decided 29 September, readiness close-out)"},"returnToParentPrice":{"type":"boolean","description":"Return to Parent Price when an override expires"},"fallbackBehavior":{"type":"string","enum":["useParent","useDefault","blockSale"],"description":"Fallback (p.18): what happens when a child rate does not exist"}}},"description":"Hierarchy Builder (p.17): the ordered levels; saved as a whole so two sources can never be left at equal priority"},"validationIssues":{"type":"array","description":"Conflict Detection (p.18); read-only","items":{"type":"object","properties":{"code":{"type":"string","enum":["equalPriority","missingFallback","circularInheritance"]},"message":{"type":"string"}}}}}},
"PriceListMasterConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Price List Master Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"priceListName":{"type":"string","description":"Price List Name"},"priceListCode":{"type":"string","description":"Price List Code; unique within the tenant"},"description":{"type":"string","description":"Description"},"priceListType":{"type":"string","enum":["standardRetail","venue","attraction","event","membership","group","corporate","b2b","reseller","ota","internal","specialMarket"],"description":"Price List Type (Commercial Types, pp.8-9, and the directory's Price List Types)"},"legalEntity":{"type":"string","description":"Legal Entity"},"brand":{"type":"string","description":"Brand"},"businessUnit":{"type":"string","description":"Business Unit"},"country":{"type":"string","description":"Country"},"market":{"type":"string","description":"Market"},"venue":{"type":"string","description":"Venue"},"defaultCurrency":{"type":"string","description":"Default Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"owner":{"type":"string","description":"Owner"},"tags":{"type":"array","items":{"type":"string"},"description":"Tags"},"status":{"type":"string","description":"Status: draft, configured, inactive or archived are set here; validated is set by structure validation (ADM-057) and active / expired by Board 4 publication"},"defaultRateCategory":{"type":"string","description":"Default Rate Category: code of a price category from the library (ADM-050)"},"defaultRoundingProfile":{"type":"string","description":"Default Rounding Profile: code of a currency rounding rule (ADM-075)"},"defaultPriceHierarchy":{"type":"string","description":"Default Price Hierarchy: id of the price hierarchy (ADM-055) this list resolves against"},"allowOverrides":{"type":"boolean","description":"Allow Overrides"},"allowInheritance":{"type":"boolean","description":"Allow Inheritance"},"allowMultipleCurrencies":{"type":"boolean","description":"Allow Multiple Currencies"},"allowProductSpecificRates":{"type":"boolean","description":"Allow Product-Specific Rates"},"priceListId":{"type":"string","description":"Price List ID; empty on create, the list to update otherwise"},"scope":{"type":"string","enum":["global","country","market","brand","venue","event","businessUnit"],"description":"Scope: where the price list can apply (p.8)"},"clonedFromPriceListId":{"type":"string","nullable":true,"description":"The price list this one was duplicated from (Duplicate, p.9: UAE Standard 2026 into UAE Standard 2027); empty when built from scratch"}}},
"PriceListMasterConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price List Master Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"priceListName":{"type":"string","description":"Price List Name"},"priceListCode":{"type":"string","description":"Price List Code; unique within the tenant"},"description":{"type":"string","description":"Description"},"priceListType":{"type":"string","enum":["standardRetail","venue","attraction","event","membership","group","corporate","b2b","reseller","ota","internal","specialMarket"],"description":"Price List Type (Commercial Types, pp.8-9, and the directory's Price List Types)"},"legalEntity":{"type":"string","description":"Legal Entity"},"brand":{"type":"string","description":"Brand"},"businessUnit":{"type":"string","description":"Business Unit"},"country":{"type":"string","description":"Country"},"market":{"type":"string","description":"Market"},"venue":{"type":"string","description":"Venue"},"defaultCurrency":{"type":"string","description":"Default Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"owner":{"type":"string","description":"Owner"},"tags":{"type":"array","items":{"type":"string"},"description":"Tags"},"status":{"type":"string","description":"Status: draft, configured, inactive or archived are set here; validated is set by structure validation (ADM-057) and active / expired by Board 4 publication"},"defaultRateCategory":{"type":"string","description":"Default Rate Category: code of a price category from the library (ADM-050)"},"defaultRoundingProfile":{"type":"string","description":"Default Rounding Profile: code of a currency rounding rule (ADM-075)"},"defaultPriceHierarchy":{"type":"string","description":"Default Price Hierarchy: id of the price hierarchy (ADM-055) this list resolves against"},"allowOverrides":{"type":"boolean","description":"Allow Overrides"},"allowInheritance":{"type":"boolean","description":"Allow Inheritance"},"allowMultipleCurrencies":{"type":"boolean","description":"Allow Multiple Currencies"},"allowProductSpecificRates":{"type":"boolean","description":"Allow Product-Specific Rates"},"priceListId":{"type":"string","description":"Price List ID; empty on create, the list to update otherwise"},"scope":{"type":"string","enum":["global","country","market","brand","venue","event","businessUnit"],"description":"Scope: where the price list can apply (p.8)"},"clonedFromPriceListId":{"type":"string","nullable":true,"description":"The price list this one was duplicated from (Duplicate, p.9: UAE Standard 2026 into UAE Standard 2027); empty when built from scratch"},"consumingModules":{"type":"array","items":{"type":"string","enum":["ticketing","b2c","pos","kiosk","b2b","groupSales","membership","fnb","retail","rental"]},"description":"Dependencies: the modules that consume this list (p.9); read-only"}}},
"PriceListTemplatesCloneReuseView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Price List Templates, Clone & Reuse displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"templateId":{"type":"string","description":"Template ID"},"name":{"type":"string","description":"Template name, e.g. Theme Park Pricing"},"templateType":{"type":"string","description":"Template Library type: standardAttraction, themePark, museum, concert, sports, membership, group, corporate, b2b, rental or custom (p.18)"},"description":{"type":"string","description":"Description"},"components":{"type":"array","items":{"type":"string","enum":["priceCategories","rateTypes","rateMatrixStructure","currencyStructure","hierarchy","productMappingPattern","packagePricingPattern"]},"description":"Template Components the template carries (p.18)"},"sourcePriceListId":{"type":"string","nullable":true,"description":"Price list the template was taken from; empty when built directly"},"aiDrafted":{"type":"boolean","description":"Drafted by AI-assisted template generation and awaiting administrator review"},"status":{"type":"string","description":"Status: draft, active or archived"},"owner":{"type":"string","description":"Owner"}}},
"PricingMarket": {"type":"object","x-ticvai-persistence":"catalogue.pricing_market","description":"**A node of the market pricing structure: global, country, region, market or venue** (29 September, data model DM3). ADM-064. Says which price list and rounding a market uses and whether it inherits from its parent. **At venue level the selling currency is the venue's trading currency** and cannot differ from it (ADR-0018, frozen once the venue has traded); above venue level the currencies are reporting and base currencies.","required":["id","scopePath","hierarchyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `tenant` scope."},"hierarchyLevel":{"type":"string","enum":["global","country","region","market","venue"]},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"The parent `catalogue.pricing_market`."},"countryCode":{"type":"string","maxLength":2,"nullable":true,"pattern":"^[A-Z]{2}$"},"marketCode":{"type":"string","maxLength":40,"nullable":true},"region":{"type":"string","maxLength":100,"nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"brand":{"type":"string","maxLength":100,"nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true},"baseCurrency":{"type":"string","maxLength":3,"nullable":true,"pattern":"^[A-Z]{3}$"},"sellingCurrency":{"type":"string","maxLength":3,"nullable":true,"pattern":"^[A-Z]{3}$"},"roundingProfileId":{"type":"string","format":"uuid","nullable":true},"displayFormat":{"type":"string","maxLength":40,"nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"inheritsFromParent":{"type":"boolean","default":true},"fxReferenceRate":{"type":"number","nullable":true,"description":"Reference only; FX supplies inputs, it never decides a price."},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductServicePriceAssignmentInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Product & Service Price Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"assignmentId":{"type":"string","description":"Assignment ID; empty on create"},"objectType":{"type":"string","enum":["ticketProduct","ticketType","admission","event","performance","membership","annualPass","addOn","fnbItem","retailProduct","rentalItem","resource","reservationService","experience","otherSellableService"],"description":"Supported Commercial Objects (p.13): the kind of sellable object being priced"},"objectIds":{"type":"array","items":{"type":"string"},"description":"The objects assigned; more than one is a Bulk Assignment (25 attraction products -> one price list)"},"assignmentScope":{"type":"string","enum":["productLevel","productVariant","ticketType","event","performance","venue"],"description":"Assignment Scope (p.14): the level at which the assignment holds"},"scopeRefId":{"type":"string","nullable":true,"description":"The variant, ticket type, event, performance or venue the assignment is limited to; empty at product level"},"priceListId":{"type":"string","description":"The price list assigned"},"categoryRates":{"type":"array","items":{"type":"object","properties":{"priceCategory":{"type":"string"},"rateId":{"type":"string"}}},"description":"Product -> Price List -> Category -> Rate (Assignment Workspace, p.13): which rate of the list serves each category; empty uses every active rate of the list"}}},
"ProductServicePriceAssignmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Product & Service Price Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"assignmentId":{"type":"string","description":"Assignment ID; empty on create"},"objectType":{"type":"string","enum":["ticketProduct","ticketType","admission","event","performance","membership","annualPass","addOn","fnbItem","retailProduct","rentalItem","resource","reservationService","experience","otherSellableService"],"description":"Supported Commercial Objects (p.13): the kind of sellable object being priced"},"objectIds":{"type":"array","items":{"type":"string"},"description":"The objects assigned; more than one is a Bulk Assignment (25 attraction products -> one price list)"},"assignmentScope":{"type":"string","enum":["productLevel","productVariant","ticketType","event","performance","venue"],"description":"Assignment Scope (p.14): the level at which the assignment holds"},"scopeRefId":{"type":"string","nullable":true,"description":"The variant, ticket type, event, performance or venue the assignment is limited to; empty at product level"},"priceListId":{"type":"string","description":"The price list assigned"},"categoryRates":{"type":"array","items":{"type":"object","properties":{"priceCategory":{"type":"string"},"rateId":{"type":"string"}}},"description":"Product -> Price List -> Category -> Rate (Assignment Workspace, p.13): which rate of the list serves each category; empty uses every active rate of the list"},"pricingSource":{"type":"string","description":"Price Source Visibility (p.14): the name shown on the product, e.g. UAE Standard Admission 2027; read-only"}}},
"RateStructureBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.price at 4%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Rate Structure Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *Each rate should contain* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"rateId":{"type":"string","description":"Rate ID"},"rateName":{"type":"string","description":"Rate Name"},"rateCode":{"type":"string","description":"Rate Code"},"priceCategory":{"type":"string","description":"Price Category: code of a category from the library (ADM-050)"},"rateType":{"type":"string","description":"Rate Type: code of a rate type from the library (ADM-050), e.g. standard, reduced, derived"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount; ignored when derivedFrom is set"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"unitBasis":{"type":"string","enum":["perTicket","perPerson","perUnit","perHour","perDay","perPerformance","perResource","perPackage","perMembershipPeriod"],"description":"Unit Basis (p.12); perPerformance is the pack's \"Per Session\" (a session is a Performance)"},"precision":{"type":"integer","description":"Precision: decimal places, 0 to 3 (MoM 1 Sep §4.5 requires up to three)","minimum":0,"maximum":3},"roundingProfile":{"type":"string","description":"Rounding Profile: code of a currency rounding rule (ADM-075)"},"status":{"type":"string","description":"Status: draft, active or disabled"},"priceListId":{"type":"string","description":"The price list the rate belongs to"},"derivedFrom":{"type":"object","nullable":true,"description":"Derived Rates (p.12): this rate is another rate adjusted (Child = Adult - 25%, VIP = Standard + AED 200); a commercial relationship, not dynamic pricing. Empty for an entered amount","properties":{"baseRateId":{"type":"string"},"adjustmentType":{"type":"string","enum":["percentage","fixedAmount"]},"adjustmentValue":{"type":"number","description":"Percent or amount in the rate currency; negative reduces"}}}},"x-ticvai-record-definition":"Each rate should contain"},
"RateStructureBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Rate Structure Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"rateId":{"type":"string","description":"Rate ID"},"rateName":{"type":"string","description":"Rate Name"},"rateCode":{"type":"string","description":"Rate Code"},"priceCategory":{"type":"string","description":"Price Category: code of a category from the library (ADM-050)"},"rateType":{"type":"string","description":"Rate Type: code of a rate type from the library (ADM-050), e.g. standard, reduced, derived"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount; for a derived rate this is the computed value, read-only"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"unitBasis":{"type":"string","enum":["perTicket","perPerson","perUnit","perHour","perDay","perPerformance","perResource","perPackage","perMembershipPeriod"],"description":"Unit Basis (p.12); perPerformance is the pack's \"Per Session\" (a session is a Performance)"},"precision":{"type":"integer","description":"Precision: decimal places, 0 to 3 (MoM 1 Sep §4.5 requires up to three)","minimum":0,"maximum":3},"roundingProfile":{"type":"string","description":"Rounding Profile: code of a currency rounding rule (ADM-075)"},"status":{"type":"string","description":"Status: draft, active or disabled"},"priceListId":{"type":"string","description":"The price list the rate belongs to"},"derivedFrom":{"type":"object","nullable":true,"description":"Derived Rates (p.12): this rate is another rate adjusted (Child = Adult - 25%, VIP = Standard + AED 200); a commercial relationship, not dynamic pricing. Empty for an entered amount","properties":{"baseRateId":{"type":"string"},"adjustmentType":{"type":"string","enum":["percentage","fixedAmount"]},"adjustmentValue":{"type":"number","description":"Percent or amount in the rate currency; negative reduces"}}},"validationIssues":{"type":"array","description":"Validation (pp.12-13): problems found on this rate; read-only","items":{"type":"object","properties":{"code":{"type":"string","enum":["duplicateRate","missingAmount","unsupportedCurrency","invalidDerivedRate","circularRateRelationship"]},"message":{"type":"string"}}}}}}
}
```
