# WS91 — Rental Management board 4

**10 screens · 11 operations · 14 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `PRICE_CONFIGURE, PRODUCT_VIEW, RENTAL_OVERRIDE, RENTAL_PRICE, RENTAL_VIEW`. A control nobody can use must say so,
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
| `BO-524` | Rental Pricing Command Center | B–D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-525` | Pricing Profile Builder | B–D | 8 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-526` | Duration & Tiered Pricing Configuration | B–D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-527` | Calendar, Peak & Seasonal Pricing | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-528` | Dynamic Pricing & AI Recommendation | B–D | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-529` | Deposit & Security Hold Policy | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-530` | Deposit Lifecycle & Settlement Rules | B–D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-531` | Late Fee, Grace Period & Extension Pricing | B–D | 7 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-532` | Commercial Exceptions, Waivers & Overrides | B–D | 0 | 0 | 6 | 0 | 1 | 4 | — | notStarted (—) |
| `BO-533` | Pricing Simulation, Validation & AI Commercial Intelligence | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-527, BO-528, BO-529, BO-532, BO-533 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-524` Rental Pricing Command Center

**Central management screen for all rental pricing and commercial policies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_PRICE`, `RENTAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-pricing-command-center-bo-524` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search rental pricing | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, location, product, category, pricing model, deposit type and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Product | picker: choose a product | — | — | `listRentalPricingProfiles` ?productId |
| Unpriced only | toggle | — | — | `listRentalPricingProfiles` ?unpricedOnly |

#### Outputs: what the screen shows and produces

**Shown**

**Active Pricing Profiles** (metric tile)

**Products Without Pricing** (metric tile)

**Deposit Policies** (metric tile)

**Dynamic Pricing Enabled** (metric tile)

**Upcoming Price Changes** (metric tile)

**Pricing Exceptions** (metric tile)

**Approval Pending** (metric tile)

**AI Recommendations** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| + Create Pricing Profile (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRentalPricingProfiles` (onLoad, Profiles, and products without one)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-525` Pricing Profile Builder: *Pricing Profile Builder*
- → `BO-526` Duration & Tiered Pricing Configuration: *Duration & Tiered Pricing Configuration*
- → `BO-527` Calendar, Peak & Seasonal Pricing: *Calendar, Peak & Seasonal Pricing*
- → `BO-528` Dynamic Pricing & AI Recommendation: *Dynamic Pricing & AI Recommendation*
- → `BO-529` Deposit & Security Hold Policy: *Deposit & Security Hold Policy*
- → `BO-530` Deposit Lifecycle & Settlement Rules: *Deposit Lifecycle & Settlement Rules*
- → `BO-531` Late Fee, Grace Period & Extension Pricing: *Late Fee, Grace Period & Extension Pricing*
- → `BO-532` Commercial Exceptions, Waivers & Overrides: *Commercial Exceptions, Waivers & Overrides*
- → `BO-533` Pricing Simulation, Validation & AI Commercial Intelligence: *Pricing Simulation, Validation & AI Commercial Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental pricing list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental pricing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental pricing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRentalPricingProfiles` → `RENTAL_VIEW` (read) · staff
- `createRentalPricingProfile` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-524` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-524`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 1: Opens Rental Pricing Command Center → Central management screen for all rental pricing and commercial policies.
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F200 branch at step 1 (expected): when Nothing has been set up on Rental Pricing Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F200 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-524?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: + Create Pricing Profile.
- [ ] Every transition is wired: `BO-100`, `BO-525`, `BO-526`, `BO-527`, `BO-528`, `BO-529`, `BO-530`, `BO-531`, `BO-532`, `BO-533`.
- [ ] Every gated control is gated: `RENTAL_PRICE`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-525` Pricing Profile Builder

**Create the master commercial pricing profile associated with a rental product.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/rentals/pricing-profile-builder-bo-525` |

**Known gaps.** **Pricing Profile Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Flat Rate | select field | — | — | — | — | — | — |
| Duration Based | select field | — | — | — | — | — | — |
| Tiered | select field | — | — | — | — | — | — |
| Peak / Off-Peak | select field | — | — | — | — | — | — |
| Weekend | select field | — | — | — | — | — | — |
| Seasonal | select field | — | — | — | — | — | — |
| Dynamic / AI-Assisted | select field | — | — | — | — | — | — |
| Hybrid | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createRentalPricingProfile` → `RENTAL_PRICE` (operate) · staff
- `updateRentalPricingProfile` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-525` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-525`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 2: Works in Pricing Profile Builder → Create the master commercial pricing profile associated with a rental product.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-525?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-526` Duration & Tiered Pricing Configuration

**Configure pricing according to rental duration. This directly implements the fixed and dynamic-duration requirements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§For customer-defined durations; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/rentals/duration-tiered-pricing-configuration-bo-526` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Minimum Charge: AED 40 | text field | — | — | — | — | — | — |
| Billing Increment: 15 minutes | text field | — | — | — | — | — | — |
| Additional Increment: AED 10 | text field | — | — | — | — | — | — |
| Exact usage | select field | — | — | — | — | — | — |
| Round up to 15 minutes | text field | — | — | — | — | — | — |
| Round up to 30 minutes | text field | — | — | — | — | — | — |
| Full next hour | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The duration tiered pricing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the duration tiered pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No duration tiered pricing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updateRentalPricingProfile` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-526` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-526`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 4: Works in Duration & Tiered Pricing Configuration → Configure pricing according to rental duration. This directly implements the fixed and dynamic-duration requirements.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-526?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-527` Calendar, Peak & Seasonal Pricing

**Allow price differentiation according to date and time.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `profileId` (navigation) |
| Route | `/rentals/calendar-peak-seasonal-pricing-bo-527` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The calendar peak seasonal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the calendar peak seasonal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No calendar peak seasonal yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the calendar peak seasonal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `updateRentalPricingProfile` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-527` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-527`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 6: Works in Calendar, Peak & Seasonal Pricing → Allow price differentiation according to date and time.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-527?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-528` Dynamic Pricing & AI Recommendation

**Connect Rental Management to TICVAI's broader Dynamic Pricing capability without duplicating the core Dynamic Pricing module. The original rental requirements explicitly support dynamic pricing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `strategyId` (navigation) |
| Route | `/rentals/dynamic-pricing-ai-recommendation-bo-528` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Strategy type | select | — | Demand based · Occupancy based · Availability based · Inventory based · Booking velocity · Time to event · Seasonal · Day of week · Timeslot · Channel · Segment · Location … | `listDynamicPricingStrategy` ?strategyType |
| Status | select | — | Draft · Testing · Ready · Scheduled · Active · Paused · Frozen · Expired · Retired | `listDynamicPricingStrategy` ?status |
| Automation mode | radio group | — | Monitor · Recommend · Prepare change · Auto execute within guardrails | `listDynamicPricingStrategy` ?automationMode |
| Venue | text field | — | — | `listDynamicPricingStrategy` ?venue |
| Search | text field | — | — | `listDynamicPricingStrategy` ?search |

**Form: Transition dynamic pricing strategy** (modal, opened by *Transition dynamic pricing strategy*; *Transition dynamic pricing strategy* calls `transitionDynamicPricingStrategy`, *Cancel* sends nothing)

**Collects what `transitionDynamicPricingStrategy` sends before it is called.** Required: `action`. Optional: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | radio group | required | — | Activate · Pause · Resume · Retire | — | — | `transitionDynamicPricingStrategy` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `transitionDynamicPricingStrategy` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `illegalTransition`.; 422 `strategyIncomplete`.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Accept / Modify / Reject / Schedule (primary button) | navigation or local | — | — | — | — |
| Transition dynamic pricing strategy (secondary button) | `transitionDynamicPricingStrategy` POST `/dynamic-pricing-strategies/{strategyId}/lifecycle` | inline | DynamicPricingStrategy | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `illegalTransition`.; 422 `strategyIncomplete`. | gated `PRICE_CONFIGURE`; opens modal first |

**Data it reads**: `listDynamicPricingStrategy` (onLoad, Dynamic pricing)

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic pricing recommendation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic pricing recommendation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic pricing recommendation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dynamic pricing recommendation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `illegalTransition`.; 422 `strategyIncomplete`. |

#### Permissions

- `listDynamicPricingStrategy` → `PRODUCT_VIEW` (read) · staff
- `transitionDynamicPricingStrategy` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental pricing: fixed and dynamic models; top-products-by-revenue view; pricing profile valid across a date range, optionally restricted to channels; tiered duration pricing (30/60/90 min at falling per-minute rates); weekday/weekend and peak pricing; demand-based pricing within min/max bounds. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-751)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-528` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-528`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 8: Works in Dynamic Pricing & AI Recommendation → Connect Rental Management to TICVAI's broader Dynamic Pricing capability without duplicating the core Dynamic Pricing module. The original rental requirements explicitly support dynamic pricing.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-528?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Accept / Modify / Reject / Schedule, Transition dynamic pricing strategy.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-529` Deposit & Security Hold Policy

**Configure financial security required before equipment is released. The original scope supports fixed and percentage deposits and multiple deposit methods.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/deposit-security-hold-policy-bo-529` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Credit Card Pre-Authorization (primary button) | navigation or local | — | — | — | — |
| Card Charge (secondary button) | navigation or local | — | — | — | — |
| Wallet (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deposit security hold list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deposit security hold untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deposit security hold yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the deposit security hold are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalDepositPolicy` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Refundable deposit (fixed amount or %), payable by cash or card per business policy; auto-release on return; partial capture (deduct damage charge, refund remainder). *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-752)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-529` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-529`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 10: Works in Deposit & Security Hold Policy → Configure financial security required before equipment is released. The original scope supports fixed and percentage deposits and multiple deposit methods.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-529?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Credit Card Pre-Authorization, Card Charge, Wallet.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-530` Deposit Lifecycle & Settlement Rules

**Control what happens to the deposit throughout the rental lifecycle.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/deposit-lifecycle-settlement-rules-bo-530` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Automatic release | select field | — | — | — | — | — | — |
| Manual inspection required | select field | — | — | — | — | — | — |
| Supervisor approval threshold | select field | — | — | — | — | — | — |
| Partial capture permitted | select field | — | — | — | — | — | — |
| Full capture permitted | select field | — | — | — | — | — | — |
| Auto-release delay | select field | — | — | — | — | — | — |
| Refund method | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The deposit lifecycle settlement configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the deposit lifecycle settlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No deposit lifecycle settlement configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalDepositPolicy` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Refundable deposit (fixed amount or %), payable by cash or card per business policy; auto-release on return; partial capture (deduct damage charge, refund remainder). *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-752)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-530` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-530`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 12: Works in Deposit Lifecycle & Settlement Rules → Control what happens to the deposit throughout the rental lifecycle.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-530?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-531` Late Fee, Grace Period & Extension Pricing

**Configure the commercial treatment of rentals that extend beyond the original return time. The source explicitly requires automatic late-fee calculation and grace-period configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_PRICE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/late-fee-grace-period-extension-pricing-bo-531` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Fixed Fee | select field | — | — | — | — | — | — |
| Per Minute | select field | — | — | — | — | — | — |
| Per 15 Minutes | select field | — | — | — | — | — | — |
| Per 30 Minutes | select field | — | — | — | — | — | — |
| Per Hour | select field | — | — | — | — | — | — |
| Tiered | select field | — | — | — | — | — | — |
| Maximum Daily Charge | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The late fee grace configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the late fee grace untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No late fee grace configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalFeePolicy` → `RENTAL_PRICE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Late fee, grace period and extension pricing; fee waiver full or partial (amount or %), e.g. when equipment malfunctioned through no fault of the customer; a simulation tests pricing/deposit rules before publishing. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-753)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-531` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-531`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 14: Works in Late Fee, Grace Period & Extension Pricing → Configure the commercial treatment of rentals that extend beyond the original return time. The source explicitly requires automatic late-fee calculation and grace-period configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-531?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_PRICE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-532` Commercial Exceptions, Waivers & Overrides

**Control authorized deviations from normal commercial policies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_OVERRIDE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/commercial-exceptions-waivers-overrides-bo-532` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial exceptions waivers list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial exceptions waivers untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial exceptions waivers yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial exceptions waivers are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `requestRentalCommercialOverride` → `RENTAL_OVERRIDE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Late fee, grace period and extension pricing; fee waiver full or partial (amount or %), e.g. when equipment malfunctioned through no fault of the customer; a simulation tests pricing/deposit rules before publishing. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-753)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-532` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-532`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 16: Works in Commercial Exceptions, Waivers & Overrides → Control authorized deviations from normal commercial policies.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-532?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `RENTAL_OVERRIDE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-533` Pricing Simulation, Validation & AI Commercial Intelligence

**Allow administrators to test commercial configuration before publishing it. This is particularly important because rental pricing can involve duration, calendar, location, deposit and dynamic pricing simultaneously.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW`, `RENTAL_PRICE`, `RENTAL_VIEW` (2 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/pricing-simulation-validation-ai-commercial-intelligence-bo-533` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCommercialPricing` (onLoad, Commercial Pricing Command Center)

**Where the user goes next**

- → `BO-524` Rental Pricing Command Center: *Back to Rental Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing simulation validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing simulation validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing simulation validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing simulation validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCommercialPricing` → `PRODUCT_VIEW` (read) · staff
- `simulateRentalPricing` → `RENTAL_PRICE` (operate) · staff
- `explainRentalPrice` → `RENTAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Late fee, grace period and extension pricing; fee waiver full or partial (amount or %), e.g. when equipment malfunctioned through no fault of the customer; a simulation tests pricing/deposit rules before publishing. *(client request · MoM 9 Sep 2026, 4.5 Rental Pricing, Deposits & Commercial Rules · DI-753)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-533` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS119 Rental Management Board 4.dc.html#bo-533`
- Workshop pack: Rental_Management.pdf board 4
- Flow F200 *Rental Management board 4: Rental Pricing Command Center*, step 18: Works in Pricing Simulation, Validation & AI Commercial Intelligence → Allow administrators to test commercial configuration before publishing it. This is particularly important because rental pricing can involve duration, calendar, location, deposit and dynamic pricing …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-533?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-524`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`, `RENTAL_PRICE`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**10 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createRentalPricingProfile": {"method":"POST","path":"/rental-pricing-profiles","contract":"rental","summary":"Define how a rental is priced","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalPricingProfile","responds":"RentalPricingProfile"},
"explainRentalPrice": {"method":"POST","path":"/rental-price/explain","contract":"rental","summary":"Why the price is what it is, rule by rule","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalQuoteRequest","responds":"RentalPriceExplanation"},
"listCommercialPricing": {"method":"GET","path":"/commercial-pricing","contract":"catalogue","summary":"Commercial Pricing Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"country","in":"query","required":false},{"name":"productType","in":"query","required":false},{"name":"priceListType","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"brand","in":"query","required":false},{"name":"market","in":"query","required":false},{"name":"currency","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listDynamicPricingStrategy": {"method":"GET","path":"/dynamic-pricing-strategy","contract":"catalogue","summary":"Dynamic Pricing Strategy Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"strategyType","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"automationMode","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"search","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRentalPricingProfiles": {"method":"GET","path":"/rental-pricing-profiles","contract":"rental","summary":"Pricing profiles, and the products with none","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"productId","in":"query","required":null},{"name":"unpricedOnly","in":"query","required":null}],"requestBody":null,"responds":"RentalPricingProfile"},
"requestRentalCommercialOverride": {"method":"POST","path":"/rental-overrides","contract":"rental","summary":"Deviate from policy, with a reason and an approver","permission":"RENTAL_OVERRIDE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalOverride","responds":"RentalOverride"},
"setRentalDepositPolicy": {"method":"PUT","path":"/rental-deposit-policies","contract":"rental","summary":"How much is held, how, and what happens to it","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalDepositPolicy","responds":"RentalDepositPolicy"},
"setRentalFeePolicy": {"method":"PUT","path":"/rental-fee-policies","contract":"rental","summary":"Grace period, late fees and extension pricing","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalFeePolicy","responds":"RentalFeePolicy"},
"simulateRentalPricing": {"method":"POST","path":"/rental-price/simulate","contract":"rental","summary":"Test a commercial configuration before publishing it","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalQuoteRequest","responds":null},
"transitionDynamicPricingStrategy": {"method":"POST","path":"/dynamic-pricing-strategies/{strategyId}/lifecycle","contract":"catalogue","summary":"Activate, pause, resume or retire a dynamic pricing strategy","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"DynamicPricingStrategy"},
"updateRentalPricingProfile": {"method":"PUT","path":"/rental-pricing-profiles/{profileId}","contract":"rental","summary":"Change a pricing profile","permission":"RENTAL_PRICE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalPricingProfile","responds":"RentalPricingProfile"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CommercialPricingCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Commercial Pricing Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"totalPriceLists":{"type":"integer","description":"Total Price Lists"},"activePriceLists":{"type":"integer","description":"Active Price Lists"},"draftPriceLists":{"type":"integer","description":"Draft Price Lists"},"priceCategories":{"type":"integer","description":"Price Categories"},"configuredRates":{"type":"integer","description":"Configured Rates"},"productsWithPricing":{"type":"integer","description":"Products with Pricing: sellable products that reference at least one active price list rate"},"productsMissingPricing":{"type":"integer","description":"Products Missing Pricing: active sellable products with no price list rate"},"markets":{"type":"integer","description":"Markets"},"currencies":{"type":"integer","description":"Currencies"},"pricingValidationIssues":{"type":"integer","description":"Pricing Validation Issues"},"recentlyModifiedPriceLists":{"type":"integer","description":"Recently Modified Price Lists: price lists changed in the last 7 days (decided 29 September, readiness close-out)"},"upcomingPriceStructures":{"type":"integer","description":"Upcoming Price Structures: price lists whose effective-from date is in the future"},"aiInsights":{"type":"array","items":{"type":"string"},"description":"AI observations for this screen; advisory only, never applied automatically"}}},
"CommercialPricingCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Commercial Pricing Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"priceListId":{"type":"string","description":"Price List ID"},"name":{"type":"string","description":"Name"},"code":{"type":"string","description":"Code"},"type":{"type":"string","enum":["standardRetail","venue","attraction","event","membership","group","corporate","b2b","reseller","ota","internal","specialMarket"],"description":"Price List Type (the pack's Price List Types, pp.6-7)"},"currency":{"type":"string","description":"Currency: ISO 4217 code of the default currency","pattern":"^[A-Z]{3}$"},"market":{"type":"string","description":"Market"},"venue":{"type":"string","description":"Venue"},"brand":{"type":"string","description":"Brand"},"productCount":{"type":"integer","description":"Product Count"},"rateCount":{"type":"integer","description":"Rate Count"},"version":{"type":"string","description":"Version"},"status":{"type":"string","description":"Status: draft, configured, validated, active, inactive, expired or archived (p.7); approval and publication are Board 4's"},"owner":{"type":"string","description":"Owner"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From (the first half of the pack's Effective Period)"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true}}},
"DynamicPricingStrategy": {"type":"object","x-ticvai-persistence":"catalogue.dynamic_pricing_strategy","description":"**A dynamic pricing strategy: what it prices, from which base and how often** (29 September, data model DM3). ADM-088 and ADM-089. Its rules are `pricing.dynamic_price_rule` rows naming it; its ladder `catalogue.price_ladder`; its limits and automation `catalogue.dynamic_pricing_control`. **Rules-based now; AI factors inform, never replace, the rules** (MoM 19 Aug 2026).","required":["id","scopePath","code","name","strategyType","scopeType","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"code":{"type":"string","maxLength":40},"name":{"type":"string","maxLength":200},"description":{"type":"string","nullable":true},"strategyType":{"type":"string","enum":["demandBased","occupancyBased","availabilityBased","inventoryBased","bookingVelocity","timeToEvent","seasonal","dayOfWeek","timeslot","channel","segment","location","hybrid"]},"scopeType":{"type":"string","enum":["singleProduct","productFamily","event","multiplePerformances","venue","selectedTimeslots","selectedPriceCategories"]},"venueId":{"type":"string","format":"uuid","nullable":true},"productId":{"type":"string","format":"uuid","nullable":true},"productFamily":{"type":"string","maxLength":100,"nullable":true},"eventId":{"type":"string","format":"uuid","nullable":true},"performanceIds":{"type":"array","items":{"type":"string","format":"uuid"}},"timeslotIds":{"type":"array","items":{"type":"string","format":"uuid"}},"priceCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"businessUnit":{"type":"string","maxLength":100,"nullable":true},"marketCode":{"type":"string","maxLength":40,"nullable":true},"basePriceSource":{"type":"string","maxLength":100,"description":"The price list or rate the adjustments start from."},"evaluationFrequency":{"type":"string","enum":["every15Minutes","every30Minutes","hourly","daily","onInventoryChange","onThresholdTrigger"],"default":"hourly"},"combinationMode":{"type":"string","enum":["independent","combinable","exclusive","fallback"],"default":"independent"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"clonedFromStrategyId":{"type":"string","format":"uuid","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["draft","active","paused","frozen","expired","retired"],"default":"draft"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"DynamicPricingStrategyCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Dynamic Pricing Strategy Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeStrategies":{"type":"integer","description":"Active Strategies"},"draftStrategies":{"type":"integer","description":"Draft Strategies"},"productsUnderDynamicPricing":{"type":"integer","description":"Products Under Dynamic Pricing"},"eventsUnderDynamicPricing":{"type":"integer","description":"Events Under Dynamic Pricing"},"performancesUnderDynamicPricing":{"type":"integer","description":"Performances Under Dynamic Pricing"},"rulesActive":{"type":"integer","description":"Rules Active"},"currentPriceAdjustments":{"type":"integer","description":"Current Price Adjustments"},"pricesAtMaximumGuardrail":{"type":"integer","description":"Prices at Maximum Guardrail"},"pricesAtMinimumGuardrail":{"type":"integer","description":"Prices at Minimum Guardrail"},"ruleConflicts":{"type":"integer","description":"Rule Conflicts"},"frozenStrategies":{"type":"integer","description":"Frozen Strategies"},"upcomingActivations":{"type":"integer","description":"Upcoming Activations: strategies scheduled to activate within 7 days (decided 29 September, readiness close-out)"},"operationalAlerts":{"type":"array","items":{"type":"string"},"description":"Operational Alerts (pack p.76), e.g. performances at their upper band, strategies with unresolved conflicts, strategies activating within 48 hours"}}},
"DynamicPricingStrategyCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Dynamic Pricing Strategy Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"strategyId":{"type":"string","description":"Strategy ID"},"strategyName":{"type":"string","description":"Strategy Name"},"strategyType":{"type":"string","enum":["demandBased","occupancyBased","availabilityBased","inventoryBased","bookingVelocity","timeToEvent","seasonal","dayOfWeek","timeslot","channel","segment","location","hybrid"],"description":"Strategy Type (pack pp.75-76)"},"productEvent":{"type":"string","description":"Product or event the strategy controls"},"venue":{"type":"string","description":"Venue"},"basePriceSource":{"type":"string","description":"Base price source: the Board 1 price list and rate the strategy moves from, e.g. UAE Standard Admission -> Adult"},"currentPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Current resolved dynamic price (for a single-price scope)","nullable":true},"adjustmentRange":{"type":"object","properties":{"minPercent":{"type":"number","description":"Lowest adjustment from base, percent"},"maxPercent":{"type":"number","description":"Highest adjustment from base, percent"}},"description":"Adjustment range allowed by the strategy"},"ruleCount":{"type":"integer","description":"Rule Count"},"effectivePeriod":{"type":"object","properties":{"from":{"type":"string","format":"date-time","description":"Effective from"},"to":{"type":"string","format":"date-time","description":"Effective to; empty for open-ended","nullable":true}},"description":"Effective period"},"automationMode":{"type":"string","enum":["monitor","recommend","prepareChange","autoExecuteWithinGuardrails"],"description":"Automation mode from the automation policy (listDynamicPricingAutomation); recommend by default"},"status":{"type":"string","description":"Status: draft, testing, ready, scheduled, active, paused, frozen, expired or retired"},"owner":{"type":"string","description":"Owner"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RentalConfigurationFinding": {"type":"object","description":"Boards 1.10 and 4.10. **Severity travels with the finding**, so the publish gate can distinguish a missing turnaround buffer from a missing price.\n","properties":{"code":{"type":"string"},"severity":{"type":"string","enum":["blocking","warning","advisory"]},"message":{"type":"string"},"field":{"type":"string","nullable":true},"source":{"type":"string","enum":["validation","ai"],"default":"validation","description":"**AI findings are advisory unless the client configures otherwise** (board 1.10), so the origin is on the record rather than assumed by the reader.\n"}}},
"RentalDepositPolicy": {"type":"object","x-ticvai-persistence":"rental.deposit_policy","description":"Boards 4.6 and 4.7. **Held, not taken**, and settled against an inspection.","properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"required":{"type":"boolean","default":true},"basis":{"type":"string","enum":["fixed","percentage","riskBased"]},"fixedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"percentage":{"type":"number","nullable":true},"minimumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"instruments":{"type":"array","items":{"type":"string","enum":["cardPreAuthorisation","cardCharge","cash","wallet"]}},"autoRelease":{"type":"boolean","default":true},"inspectionRequiredBeforeRelease":{"type":"boolean","default":false},"autoReleaseDelayHours":{"type":"integer","default":0},"partialCapturePermitted":{"type":"boolean","default":true},"supervisorApprovalThreshold":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"waiverEligible":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"RentalFeePolicy": {"type":"object","x-ticvai-persistence":"rental.fee_policy","description":"Board 4.8. **Extension is priced below late return on purpose** — *\"this encourages customers to extend properly rather than returning late.\"*\n","properties":{"id":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","nullable":true},"gracePeriodMinutes":{"type":"integer","default":0},"lateFeeBasis":{"type":"string","enum":["fixed","perMinute","per15Minutes","per30Minutes","perHour","tiered"]},"lateFeeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"lateFeeTiers":{"type":"array","items":{"type":"object","properties":{"afterMinutes":{"type":"integer"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"maximumDailyCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"extensionPricePerIncrement":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"extensionIncrementMinutes":{"type":"integer","default":30},"notReturnedAfterHours":{"type":"integer","nullable":true,"description":"**When a late rental becomes a lost one.** The deposit is captured in full and the asset retired; without a threshold the fee accrues forever and nobody decides.\n"},"damageFeeMaximum":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**A ceiling, not a rate.** Added 22 September: `rental.settlement.damage_fee` was stored with nothing bounding it. **A dent is assessed, not tabulated** — the amount is entered per incident against the actual damage, so the control is how high an operator may go, the same shape `maximumDailyCharge` already gives the late fee.\n"},"damageFeeApprovalAbove":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"**Above this, a second person signs it off.** A damage fee is the one charge on a settlement that a single operator decides alone, and the one a guest is most likely to dispute. The shape is `orders.RefundPolicy.requiresApprovalAbove`, applied to the other direction of money.\n"},"missingItemFeeBasis":{"type":"string","enum":["replacementCost","fixedAmount"],"description":"**What an unreturned item costs.** `replacementCost` reads the item's own replacement value, which is what the fee usually is; `fixedAmount` uses `missingItemFeeAmount`. Added 22 September — `rental.settlement.missing_item_fee` was stored with no source.\n"},"missingItemFeeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Used when `missingItemFeeBasis` is `fixedAmount`."},"scopePath":{"type":"string"}}},
"RentalOverride": {"type":"object","x-ticvai-persistence":"rental.override","description":"Board 4.9. **The original amount is recorded as well as the adjusted one.**","required":["kind","reason"],"properties":{"id":{"type":"string","format":"uuid"},"bookingId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","enum":["priceOverride","complimentary","depositWaiver","depositReduction","lateFeeWaiver","damageFeeWaiver","extensionFeeWaiver","manualRefund","goodwill"]},"originalAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"adjustedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"reason":{"type":"string"},"requestedBy":{"type":"string","format":"uuid"},"approvedBy":{"type":"string","format":"uuid","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"RentalPriceExplanation": {"type":"object","description":"Board 4.10 — *\"show why the price was calculated.\"* **The ordered trace, including the rules that did not apply**, because *\"why is it not the peak price\"* is asked as often as *\"why is it\"*.\n","properties":{"quote":{"$ref":"#/components/schemas/RentalQuote"},"steps":{"type":"array","items":{"type":"object","properties":{"order":{"type":"integer"},"stage":{"type":"string","enum":["basePrice","locationRule","calendarRule","dynamicPricing","channelEligibility","promotion","manualOverride","tax"]},"ruleId":{"type":"string","format":"uuid","nullable":true},"ruleName":{"type":"string","nullable":true},"applied":{"type":"boolean"},"skippedBecause":{"type":"string","nullable":true},"amountBefore":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"amountAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"RentalPricingProfile": {"type":"object","x-ticvai-persistence":"rental.pricing_profile","description":"Board 4.2. **Several will apply at once**, and the precedence is configurable and auditable (board 4.10).\n","required":["code","name","model"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"productId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true},"locationIds":{"type":"array","items":{"type":"string","format":"uuid"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018). Region-scoped and not overridable below it, so a row in a UAE region is AED and cannot be anything else. Kept on the wire, removed from the table.\n"},"salesChannel":{"type":"string","nullable":true},"customerSegmentId":{"type":"string","format":"uuid","nullable":true},"model":{"type":"string","enum":["flat","durationBased","tiered","peakOffPeak","weekend","seasonal","dynamic","hybrid"]},"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"durationTiers":{"type":"array","description":"Board 4.3. *30 min AED 40, 60 min AED 60, 90 min AED 80, 120 min AED 95.*","items":{"type":"object","properties":{"minutes":{"type":"integer"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"minimumCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"billingIncrementMinutes":{"type":"integer","nullable":true},"additionalIncrementPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"rounding":{"type":"string","enum":["exactUsage","roundUp15","roundUp30","roundUpHour"],"default":"exactUsage"},"calendarRules":{"type":"array","description":"Board 4.4. *Peak 16:00–20:00 AED 90/hr; off-peak 09:00–12:00 AED 50/hr; peak season 1 Nov – 31 Mar.*\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["peak","offPeak","weekend","seasonal","special"]},"from":{"type":"string","nullable":true},"to":{"type":"string","nullable":true},"dateFrom":{"type":"string","format":"date","nullable":true},"dateTo":{"type":"string","format":"date","nullable":true},"adjustmentPercent":{"type":"number","nullable":true},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"dynamicEnabled":{"type":"boolean","default":false},"dynamicMaxIncreasePercent":{"type":"number","default":25},"dynamicMaxDecreasePercent":{"type":"number","default":15},"priority":{"type":"integer","default":0},"effectiveFrom":{"type":"string","format":"date","nullable":true},"effectiveTo":{"type":"string","format":"date","nullable":true},"status":{"type":"string","enum":["draft","pendingApproval","active","scheduled","expired"]},"scopePath":{"type":"string"}}},
"RentalQuote": {"type":"object","x-ticvai-persistence":"rental.quote","description":"Board 4.10. **Rental amount and deposit are returned apart, because the deposit is not revenue.**\n**A quote `quoteRentalPrice` issues is stored until `expiresAt`**, with what was asked, so the figures it gave can be held to and checked later. `explainRentalPrice` and `simulateRentalPricing` return the same shape and store nothing (decided 29 September, data model DM4).\n**Consumed by `acceptedQuoteId`** on `createRentalBooking` and the extension. A quote is not deleted when it is used or expires: a nightly job removes quotes 30 days past `expiresAt` that no booking references, so a booking can always show the quote it was priced at (decided 29 September, writers pass; DM4).\n","required":["quoteId","productId","from","to","rentalAmount","depositAmount"],"properties":{"quoteId":{"type":"string","format":"uuid"},"productId":{"type":"string","format":"uuid","description":"The request's product; with `locationId`, `from`, `to` and `quantity`, what was quoted."},"locationId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer","default":1},"customerId":{"type":"string","format":"uuid","nullable":true},"rentalAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"addOnAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalPayable":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"depositInstrument":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `venue` scope."}}},
"RentalQuoteRequest": {"type":"object","required":["productId","from","to"],"properties":{"productId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid","nullable":true},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time"},"quantity":{"type":"integer","default":1},"salesChannel":{"type":"string","nullable":true},"customerId":{"type":"string","format":"uuid","nullable":true},"promotionCode":{"type":"string","nullable":true}}}
}
```
