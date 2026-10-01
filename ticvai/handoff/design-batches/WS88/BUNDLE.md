# WS88 — Rental Management board 1

**10 screens · 15 operations · 12 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AUDIT_VIEW, RENTAL_APPROVE, RENTAL_CONFIGURE, RENTAL_VIEW`. A control nobody can use must say so,
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
| `BO-494` | Rental Product Command Center | B–D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-495` | Create Rental Product Wizard | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-496` | Rental Product Profile | B–D | 0 | 28 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-497` | Rental Category & Classification Setup | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-498` | Inventory Tracking Model | B–D | 8 | 0 | 6 | 0 | 1 | 4 | — | notStarted (—) |
| `BO-499` | Rental Location Assignment | B–D | 0 | 0 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-500` | Rental Duration & Turnaround Configuration | B–D | 10 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-501` | Rental Rules & Operational Policy | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-502` | Customer Requirements, Agreement & Waiver | B–D | 16 | 0 | 6 | 0 | 1 | 4 | — | notStarted (—) |
| `BO-503` | Product Validation, Approval & Publication | B–D | 11 | 0 | 6 | 0 | 1 | 3 | — | notStarted (—) |

## Thin screens in this batch

**BO-495, BO-496, BO-497, BO-499, BO-501 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-494` Rental Product Command Center

**Central management screen for all rental products across tenants, venues and rental locations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_APPROVE`, `RENTAL_CONFIGURE`, `RENTAL_VIEW` (1 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Display configurable KPI cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/rental-product-command-center-bo-494` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search rental product | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, rental location, category, product status, tracking model and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Location | picker: choose a location | — | — | `listRentalProducts` ?locationId |
| Category | picker: choose a category | — | — | `listRentalProducts` ?categoryId |
| Tracking model | segmented control | — | Pooled · Serialised · Hybrid | `listRentalProducts` ?trackingModel |
| Status | text field | — | — | `listRentalProducts` ?status |

#### Outputs: what the screen shows and produces

**Shown**

**Total Rental Products** (metric tile)

**Active Products** (metric tile)

**Inactive Products** (metric tile)

**Serialized Products** (metric tile)

**Pooled Products** (metric tile)

**Products Requiring Maintenance** (metric tile)

**Products With Configuration Issues** (metric tile)

**Products Awaiting Approval** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| + Create Rental Product (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRentalProducts` (onLoad, Products across venues)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-495` Create Rental Product Wizard: *Create Rental Product Wizard*; carries `productId`
- → `BO-496` Rental Product Profile: *Rental Product Profile*; carries `productId`
- → `BO-497` Rental Category & Classification Setup: *Rental Category & Classification Setup*
- → `BO-498` Inventory Tracking Model: *Inventory Tracking Model*; carries `productId`
- → `BO-499` Rental Location Assignment: *Rental Location Assignment*; carries `productId`
- → `BO-500` Rental Duration & Turnaround Configuration: *Rental Duration & Turnaround Configuration*; carries `productId`
- → `BO-501` Rental Rules & Operational Policy: *Rental Rules & Operational Policy*; carries `productId`
- → `BO-502` Customer Requirements, Agreement & Waiver: *Customer Requirements, Agreement & Waiver*; carries `productId`
- → `BO-503` Product Validation, Approval & Publication: *Product Validation, Approval & Publication*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental product list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental product untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental product yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental product are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Blocking findings remain; they are listed |

#### Permissions

- `listRentalProducts` → `RENTAL_VIEW` (read) · staff
- `publishRentalProduct` → `RENTAL_APPROVE` (operate) · staff
- `importRentalCatalogue` → `RENTAL_CONFIGURE` (configure) · staff
- `createRentalProduct` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental product list shows active/inactive products and distinguishes serialized items (individually tracked, e.g. numbered bicycle) from pooled inventory (quantity only, e.g. life jackets); categories show how many product variants sit under each. *(client request · MoM 9 Sep 2026, 4.1 Rental Product Configuration & Categories · DI-739)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-494` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS116 Rental Management Board 1.dc.html#bo-494`
- Workshop pack: Rental_Management.pdf board 1
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 1: Opens Rental Product Command Center → Central management screen for all rental products across tenants, venues and rental locations.
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F197 branch at step 1 (expected): when Nothing has been set up on Rental Product Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F197 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-494?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes, + Create Rental Product.
- [ ] Every transition is wired: `BO-100`, `BO-495`, `BO-496`, `BO-497`, `BO-498`, `BO-499`, `BO-500`, `BO-501`, `BO-502`, `BO-503`.
- [ ] Every gated control is gated: `RENTAL_APPROVE`, `RENTAL_CONFIGURE`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-495` Create Rental Product Wizard

**Guided workflow for creating a new rental product.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/create-rental-product-wizard-bo-495` |

**Known gaps.** **Create Rental Product Wizard declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create rental product (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-494` Rental Product Command Center: *Back to Rental Product Command Center*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The create rental product list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the create rental product untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No create rental product yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the create rental product are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createRentalProduct` → `RENTAL_CONFIGURE` (configure) · staff
- `validateRentalProduct` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per product, tracking model is serialized, pooled or combined; plus whether the item must be scanned or simply picked, and whether substitution with another item is allowed if the requested one is unavailable. *(agreed · MoM 9 Sep 2026, 4.1 Rental Product Configuration & Categories · DI-740)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A120** Build the product creation wizard with four paths (from scratch · save as reusable template · clone · file upload using a standard tenant data-collection template) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'product creation wizard')*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker · keyword 'ticket type')*
- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A229** Build turnstile and handheld scanner configuration (connection details, light and sound feedback by ticket type, custom welcome messaging and branding, compatibility testing and deployment) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S7 (HLD/LLD) · 2 Sep 2026 · workshop tracker · keyword 'ticket type')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-495` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS116 Rental Management Board 1.dc.html#bo-495`
- Workshop pack: Rental_Management.pdf board 1
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 2: Works in Create Rental Product Wizard → Guided workflow for creating a new rental product.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-495?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create rental product, Cancel.
- [ ] Every transition is wired: `BO-494`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-496` Rental Product Profile

**Provide the complete master configuration of a rental product.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE`, `RENTAL_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/rental-product-profile-bo-496` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every rental product profile** (data table)

| Shows | Format | Notes |
|---|---|---|
| Product name | text | not in the schema: `Product name` |
| Code | text | not in the schema: `Code` |
| Category | text | not in the schema: `Category` |
| Description | text | not in the schema: `Description` |
| Images | text | not in the schema: `Images` |
| Tracking model | text | not in the schema: `Tracking model` |
| Inventory quantity | text | not in the schema: `Inventory quantity` |
| Rental locations | text | not in the schema: `Rental locations` |
| Minimum duration | text | not in the schema: `Minimum duration` |
| Maximum duration | text | not in the schema: `Maximum duration` |
| Default turnaround time | text | not in the schema: `Default turnaround time` |
| Rental agreement requirement | text | not in the schema: `Rental agreement requirement` |
| Deposit requirement | text | not in the schema: `Deposit requirement` |
| Current status | text | not in the schema: `Current status` |

**The selected rental product profile** (detail panel): The pack groups this record's detail under its own headings: “Product Header”, “Display tabs”, “Missing”.

| Shows | Format | Notes |
|---|---|---|
| Product name | text | not in the schema: `Product name` |
| Code | text | not in the schema: `Code` |
| Category | text | not in the schema: `Category` |
| Description | text | not in the schema: `Description` |
| Images | text | not in the schema: `Images` |
| Tracking model | text | not in the schema: `Tracking model` |
| Inventory quantity | text | not in the schema: `Inventory quantity` |
| Rental locations | text | not in the schema: `Rental locations` |
| Minimum duration | text | not in the schema: `Minimum duration` |
| Maximum duration | text | not in the schema: `Maximum duration` |
| Default turnaround time | text | not in the schema: `Default turnaround time` |
| Rental agreement requirement | text | not in the schema: `Rental agreement requirement` |
| Deposit requirement | text | not in the schema: `Deposit requirement` |
| Current status | text | not in the schema: `Current status` |

**Where the user goes next**

- → `BO-494` Rental Product Command Center: *Back to Rental Product Command Center*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental product profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental product profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental product profile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental product profile are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getRentalProduct` → `RENTAL_VIEW` (read) · staff
- `updateRentalProduct` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-496` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS116 Rental Management Board 1.dc.html#bo-496`
- Workshop pack: Rental_Management.pdf board 1
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 4: Works in Rental Product Profile → Provide the complete master configuration of a rental product.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (28 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-496?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-494`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`, `RENTAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-497` Rental Category & Classification Setup

**Configure reusable categories rather than hard-coding individual rental types.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE`, `RENTAL_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/rentals/rental-category-classification-setup-bo-497` |

**Known gaps.** **Rental Category & Classification Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create rental category (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listRentalCategories` (onLoad, Categories and their defaults)

**Where the user goes next**

- → `BO-494` Rental Product Command Center: *Back to Rental Product Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental category classification list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental category classification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental category classification yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental category classification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRentalCategories` → `RENTAL_VIEW` (read) · staff
- `createRentalCategory` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rental product list shows active/inactive products and distinguishes serialized items (individually tracked, e.g. numbered bicycle) from pooled inventory (quantity only, e.g. life jackets); categories show how many product variants sit under each. *(client request · MoM 9 Sep 2026, 4.1 Rental Product Configuration & Categories · DI-739)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-497` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS116 Rental Management Board 1.dc.html#bo-497`
- Workshop pack: Rental_Management.pdf board 1
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 6: Works in Rental Category & Classification Setup → Configure reusable categories rather than hard-coding individual rental types.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-497?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create rental category, Cancel.
- [ ] Every transition is wired: `BO-494`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`, `RENTAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-498` Inventory Tracking Model

**Determine how the product's physical inventory will be controlled.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/inventory-tracking-model-bo-498` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tracking Model | select field | — | — | — | — | — | — |
| Inventory Unit | select field | — | — | — | — | — | — |
| Quantity Control | select field | — | — | — | — | — | — |
| Assignment Required at Checkout | text field | — | — | — | — | — | — |
| Scan Required | select field | — | — | — | — | — | — |
| Allow Manual Assignment | select field | — | — | — | — | — | — |
| Allow Substitution | select field | — | — | — | — | — | — |
| Allow Equipment Swap | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-494` Rental Product Command Center: *Back to Rental Product Command Center*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The inventory tracking model configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the inventory tracking model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No inventory tracking model configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Bookings exist under the current model |

#### Permissions

- `setRentalInventoryModel` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per product, tracking model is serialized, pooled or combined; plus whether the item must be scanned or simply picked, and whether substitution with another item is allowed if the requested one is unavailable. *(agreed · MoM 9 Sep 2026, 4.1 Rental Product Configuration & Categories · DI-740)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A87** Design the Inventory & Procurement module: an Item Master with UOM/pack-size conversions supporting both Weighted-Average and FIFO costing, a customizable warehouse/location hierarchy with batch/date-level expiry … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A101** Schedule and hold the outstanding F&B, Retail, Procurement & Inventory workshop *(Chinmay Parab / Allam · High · Done → 30 Sep: Closed, Done (as recorded earlier) · 21 Aug 2026 · workshop tracker · keyword 'procurement')*
- **A301** Build maintenance vendor/procurement ops and analytics *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 17 Sep 2026 · workshop tracker · keyword 'procurement')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-498` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS116 Rental Management Board 1.dc.html#bo-498`
- Workshop pack: Rental_Management.pdf board 1
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 8: Works in Inventory Tracking Model → Determine how the product's physical inventory will be controlled.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-498?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-494`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-499` Rental Location Assignment

**Define where a product can physically be rented, collected and returned.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/rental-location-assignment-bo-499` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Different return locations (primary button) | navigation or local | — | — | — | — |
| Allow return to different location: YES/NO (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-494` Rental Product Command Center: *Back to Rental Product Command Center*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental location list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental location untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental location yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental location are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalProductLocations` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Physical rental booths/stations need to appear on the live venue map; open whether the map builder already covers booth/station configuration or a dedicated addition is needed (Chinmay to check). *(open · MoM 9 Sep 2026, 4.11 Follow-Ups from Prior Sessions · DI-773)*
- Location assignment defines pickup and return points, including cross-location return (pick up at A, return at B). Duration supports fixed blocks (e.g. 1-hour or 2-hour cycle rental) with min/max duration. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-741)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-499` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS116 Rental Management Board 1.dc.html#bo-499`
- Workshop pack: Rental_Management.pdf board 1
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 10: Works in Rental Location Assignment → Define where a product can physically be rented, collected and returned.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-499?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Different return locations, Allow return to different location ….
- [ ] Every transition is wired: `BO-494`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-500` Rental Duration & Turnaround Configuration

**Define how long the product can be rented. The source requires minimum and maximum rental durations and both fixed and customer-defined durations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/rental-duration-turnaround-configuration-bo-500` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Minimum Duration | select field | — | — | — | — | — | — |
| Maximum Duration | select field | — | — | — | — | — | — |
| Duration Increment | select field | — | — | — | — | — | — |
| Default Duration | select field | — | — | — | — | — | — |
| Allow Extension | select field | — | — | — | — | — | — |
| Maximum Extension | select field | — | — | — | — | — | — |
| Same-Day Return Required | select field | — | — | — | — | — | — |
| Overnight Rental Allowed | select field | — | — | — | — | — | — |
| Recommended Addition — Turnaround Time | text field | — | — | — | — | — | — |
| Preparation / Inspection / Cleaning Buffer | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-494` Rental Product Command Center: *Back to Rental Product Command Center*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental duration turnaround configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental duration turnaround untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental duration turnaround configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalDurationRules` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Location assignment defines pickup and return points, including cross-location return (pick up at A, return at B). Duration supports fixed blocks (e.g. 1-hour or 2-hour cycle rental) with min/max duration. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-741)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-500` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS116 Rental Management Board 1.dc.html#bo-500`
- Workshop pack: Rental_Management.pdf board 1
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 12: Works in Rental Duration & Turnaround Configuration → Define how long the product can be rented. The source requires minimum and maximum rental durations and both fixed and customer-defined durations.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-500?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-494`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-501` Rental Rules & Operational Policy

**Define the fundamental operational restrictions for the product.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/rental-rules-operational-policy-bo-501` |

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

- → `BO-494` Rental Product Command Center: *Back to Rental Product Command Center*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rental rules operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rental rules operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rental rules operational yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rental rules operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalOperationalRules` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Eligibility rules: required documentation (e.g. Emirates ID collected and returned with the item), age restrictions, and which customer-profile fields must be captured at rental time. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-742)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A154** Build rental & equipment management (per-day inventory, check-out/in, refundable deposits, usage-based excess charging, available/rented/faulty states) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'rental')*
- **A260** Build rental product setup: categories, locations, durations and eligibility *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A261** Support serialised, pooled or combined rental inventory per product *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A262** Build rental availability, pricing, deposits and group bookings *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A263** Build rental checkout and swaps (quick swap restarts timer; late swap gets free extension) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker · keyword 'rental')*
- **A264** Build rental returns, damage checks, deposit settlement and maintenance reports *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 9 Sep 2026 · workshop tracker · keyword 'rental')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-501` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS116 Rental Management Board 1.dc.html#bo-501`
- Workshop pack: Rental_Management.pdf board 1
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 14: Works in Rental Rules & Operational Policy → Define the fundamental operational restrictions for the product.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-501?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-494`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-502` Customer Requirements, Agreement & Waiver

**Define information and agreements required before a customer can receive the rental.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `RENTAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configurable fields; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/customer-requirements-agreement-waiver-bo-502` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Name | select field | — | — | — | — | — | — |
| Mobile | select field | — | — | — | — | — | — |
| Email | select field | — | — | — | — | — | — |
| Nationality | select field | — | — | — | — | — | — |
| ID Number | select field | — | — | — | — | — | — |
| Date of Birth | select field | — | — | — | — | — | — |
| Emergency Contact | select field | — | — | — | — | — | — |
| Address | select field | — | — | — | — | — | — |
| Custom Fields | select field | — | — | — | — | — | — |
| Rental Agreement Required | select field | — | — | — | — | — | — |
| Liability Waiver Required | select field | — | — | — | — | — | — |
| Terms & Conditions | select field | — | — | — | — | — | — |
| Safety Declaration | select field | — | — | — | — | — | — |
| E-Signature Required | select field | — | — | — | — | — | — |
| Guardian Signature for Minor | text field | — | — | — | — | — | — |
| Agreement Version | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Participant details (primary button) | navigation or local | — | — | — | — |
| Individual waiver (secondary button) | navigation or local | — | — | — | — |
| Group waiver (secondary button) | navigation or local | — | — | — | — |
| Guardian consent (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-494` Rental Product Command Center: *Back to Rental Product Command Center*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer requirements agreement configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer requirements agreement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer requirements agreement configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setRentalAgreementRequirements` → `RENTAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Eligibility rules: required documentation (e.g. Emirates ID collected and returned with the item), age restrictions, and which customer-profile fields must be captured at rental time. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-742)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A187** Build the waiver module (drag-and-drop field builder, conditional logic, signatory rules, product association, configurable trigger timing, versioning, mobile view, QR access, completion tracking with a verification … *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A188** Enforce waiver completion at access control, blocking ticket download, activation, check-in or entry where incomplete *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 31 Aug 2026 · workshop tracker · keyword 'waiver')*
- **A266** Confirm signature-pad integration for group rental waivers *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T8 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'waiver')*
- **C51** Share signature-capture pad spec for group rental waivers *(Qossai · Pending → 30 Sep: Closed, Moved to T8 · 9 Sep 2026 · workshop tracker · keyword 'waiver')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-502` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS116 Rental Management Board 1.dc.html#bo-502`
- Workshop pack: Rental_Management.pdf board 1
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 16: Works in Customer Requirements, Agreement & Waiver → Define information and agreements required before a customer can receive the rental.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-502?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Participant details, Individual waiver, Group waiver, Guardian consent.
- [ ] Every transition is wired: `BO-494`.
- [ ] Every gated control is gated: `RENTAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-503` Product Validation, Approval & Publication

**Provide controlled governance before a rental product becomes sellable.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Rentals · wave 3 · needs the `resources` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AUDIT_VIEW`, `RENTAL_APPROVE`, `RENTAL_CONFIGURE` (1 read, 1 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Product Setup; Operational Setup; AI Configuration Review) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `productId` (navigation) |
| Route | `/rentals/product-validation-approval-publication-bo-503` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ✓ Basic information | select field | — | — | — | — | — | — |
| ✓ Category | select field | — | — | — | — | — | — |
| ✓ Rental location | select field | — | — | — | — | — | — |
| ✓ Inventory model | select field | — | — | — | — | — | — |
| ✓ Duration | select field | — | — | — | — | — | — |
| ✓ Rental rules | select field | — | — | — | — | — | — |
| ✓ Customer requirements | select field | — | — | — | — | — | — |
| ✓ Agreement | select field | — | — | — | — | — | — |
| ⚠ Inventory not yet assigned | text field | — | — | — | — | — | — |
| Product: Double Kayak | select field | — | — | — | — | — | — |
| Configuration Score: 87% | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| Maker/checker workflow (primary button) | navigation or local | — | — | — | — |
| Approval comments (secondary button) | navigation or local | — | — | — | — |
| Rejection reason (secondary button) | navigation or local | — | — | — | — |
| Version history (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-494` Rental Product Command Center: *Back to Rental Product Command Center*; carries `productId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product validation approval configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product validation approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product validation approval configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Blocking findings remain; they are listed |

#### Permissions

- `validateRentalProduct` → `RENTAL_CONFIGURE` (configure) · staff
- `publishRentalProduct` → `RENTAL_APPROVE` (operate) · staff
- `listAuditRecords` → `AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A final validation step checks pricing, duration and inventory configuration before a rental product can be published for sale on-site or online. *(client request · MoM 9 Sep 2026, 4.2 Rental Location, Duration & Eligibility Rules · DI-743)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-503` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS116 Rental Management Board 1.dc.html#bo-503`
- Workshop pack: Rental_Management.pdf board 1
- Flow F197 *Rental Management board 1: Rental Product Command Center*, step 18: Works in Product Validation, Approval & Publication → Provide controlled governance before a rental product becomes sellable.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-503?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes, Maker/checker workflow, Approval comments, Rejection reason, Version history.
- [ ] Every transition is wired: `BO-494`.
- [ ] Every gated control is gated: `AUDIT_VIEW`, `RENTAL_APPROVE`, `RENTAL_CONFIGURE`.
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
"createRentalCategory": {"method":"POST","path":"/rental-categories","contract":"rental","summary":"Define a category and its defaults","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalCategory","responds":"RentalCategory"},
"createRentalProduct": {"method":"POST","path":"/rental-products","contract":"rental","summary":"Define a rental product","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalProduct","responds":"RentalProduct"},
"getRentalProduct": {"method":"GET","path":"/rental-products/{productId}","contract":"rental","summary":"The master configuration of one rental product","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RentalProduct"},
"importRentalCatalogue": {"method":"POST","path":"/rental-products/import","contract":"rental","summary":"Load a client's rental items and inventory at onboarding","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RentalImportResult"},
"listAuditRecords": {"method":"GET","path":"/audit-records","contract":"tenancy","summary":"Who did what, where, and when","permission":"AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orgUnitId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":"action","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"platformStaffGrantId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRentalCategories": {"method":"GET","path":"/rental-categories","contract":"rental","summary":"Reusable categories, with the defaults products inherit","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RentalCategory"},
"listRentalProducts": {"method":"GET","path":"/rental-products","contract":"rental","summary":"Rental products across venues and locations","permission":"RENTAL_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"locationId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"trackingModel","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"RentalProduct"},
"publishRentalProduct": {"method":"POST","path":"/rental-products/{productId}/publish","contract":"rental","summary":"Move a product through draft, review, approval and activation","permission":"RENTAL_APPROVE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RentalProduct"},
"setRentalAgreementRequirements": {"method":"PUT","path":"/rental-products/{productId}/agreement","contract":"rental","summary":"The agreement, waiver and signature a rental needs","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalAgreementRules","responds":"RentalAgreementRules"},
"setRentalDurationRules": {"method":"PUT","path":"/rental-products/{productId}/duration","contract":"rental","summary":"Minimum, maximum, increment, extension and turnaround","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalDurationRules","responds":"RentalDurationRules"},
"setRentalInventoryModel": {"method":"PUT","path":"/rental-products/{productId}/inventory-model","contract":"rental","summary":"Pooled, serialised or hybrid","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalInventoryModel","responds":"RentalInventoryModel"},
"setRentalOperationalRules": {"method":"PUT","path":"/rental-products/{productId}/rules","contract":"rental","summary":"Who may rent it, how many, and what must happen at the counter","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalOperationalRules","responds":"RentalOperationalRules"},
"setRentalProductLocations": {"method":"PUT","path":"/rental-products/{productId}/locations","contract":"rental","summary":"Where it can be collected, and where it can be returned","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RentalLocationRule"},
"updateRentalProduct": {"method":"PUT","path":"/rental-products/{productId}","contract":"rental","summary":"Change a rental product","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RentalProduct","responds":"RentalProduct"},
"validateRentalProduct": {"method":"POST","path":"/rental-products/{productId}/validate","contract":"rental","summary":"What is still missing before this can be sold","permission":"RENTAL_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"RentalConfigurationFinding"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AuditRecord": {"x-ticvai-append-only":"occurredAt","type":"object","x-ticvai-persistence":"platform.audit_record","description":"26 September, pull audit R198. **One row of the platform audit trail, as `listAuditRecords` returns it.** It was a free-form object, so nothing said what an audit row carries. These are the fields the operation already filters on — who, where, on which workstation, what action, on what, and when — and nothing more. Written by the operations that audit themselves; never edited and never deleted.\n","required":["id","action","occurredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"principalId":{"type":"string","format":"uuid","description":"Who acted."},"orgUnitId":{"type":"string","format":"uuid","nullable":true,"description":"The scope node the action happened in."},"workstationId":{"type":"string","format":"uuid","nullable":true,"description":"The workstation it was done from, where there was one."},"action":{"type":"string","description":"What was done, as the writing operation names it."},"subjectRef":{"type":"string","nullable":true,"description":"**The thing acted on** — a profile, a shift, an order. The same value the `subjectRef` filter matches.\n"},"occurredAt":{"type":"string","format":"date-time","description":"When. The list is ordered by this, most recent first."},"platformStaffGrantId":{"type":"string","format":"uuid","nullable":true,"description":"**Set when a TICVAI platform operator acted, naming the grant they acted under** (`identity.openPlatformStaffGrant`; decided 28 September, audit R098). Null for the tenant's own staff. Every platform action in a tenant carries one, so the tenant can see all of them.\n"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RentalAgreementRules": {"type":"object","x-ticvai-persistence":"rental.agreement_rules","description":"Board 1.9. **The version is part of the rule**, because a signature against text nobody kept is not a defence.\n","properties":{"customerFields":{"type":"object","additionalProperties":{"$ref":"#/components/schemas/RuleRequirement"}},"agreementRequired":{"type":"boolean","default":false},"liabilityWaiverRequired":{"type":"boolean","default":false},"termsDocumentAssetId":{"type":"string","format":"uuid","nullable":true},"agreementVersion":{"type":"string","nullable":true},"eSignatureRequired":{"type":"boolean","default":false},"guardianSignatureForMinor":{"type":"boolean","default":true},"groupWaiverMode":{"type":"string","enum":["perParticipant","singleGroupWaiver"],"default":"perParticipant"},"scopePath":{"type":"string"}}},
"RentalCategory": {"type":"object","x-ticvai-persistence":"maintenance.asset_category","description":"Board 1.4. **Defaults cascade and products override within a permitted set.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"parentCategoryId":{"type":"string","format":"uuid","nullable":true},"iconAssetId":{"type":"string","format":"uuid","nullable":true},"defaultTrackingModel":{"type":"string","nullable":true},"defaultDurationMinutes":{"type":"integer","nullable":true},"defaultTurnaroundMinutes":{"type":"integer","nullable":true},"defaultWaiverRequired":{"type":"boolean","default":false},"defaultDepositPolicyId":{"type":"string","format":"uuid","nullable":true},"overridableFields":{"type":"array","items":{"type":"string"},"description":"**Which defaults a product may override.** An empty list means the category is binding, which is the whole point of a category for a venue that wants consistency.\n"},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"RentalConfigurationFinding": {"type":"object","description":"Boards 1.10 and 4.10. **Severity travels with the finding**, so the publish gate can distinguish a missing turnaround buffer from a missing price.\n","properties":{"code":{"type":"string"},"severity":{"type":"string","enum":["blocking","warning","advisory"]},"message":{"type":"string"},"field":{"type":"string","nullable":true},"source":{"type":"string","enum":["validation","ai"],"default":"validation","description":"**AI findings are advisory unless the client configures otherwise** (board 1.10), so the origin is on the record rather than assumed by the reader.\n"}}},
"RentalDurationRules": {"type":"object","x-ticvai-persistence":"rental.duration_rules","description":"Board 1.7. **Turnaround feeds availability automatically.** *10:00–11:00 rental, 11:00–11:15 turnaround, next available 11:15.*\n","properties":{"minimumMinutes":{"type":"integer"},"maximumMinutes":{"type":"integer"},"incrementMinutes":{"type":"integer","default":15},"defaultMinutes":{"type":"integer"},"turnaroundMinutes":{"type":"integer","default":0},"extensionAllowed":{"type":"boolean","default":true},"maximumExtensionMinutes":{"type":"integer","nullable":true},"sameDayReturnRequired":{"type":"boolean","default":false},"overnightAllowed":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"RentalImportResult": {"type":"object","description":"26 August onboarding load. **Validated whole, written whole.**","properties":{"rowsRead":{"type":"integer"},"productsCreated":{"type":"integer"},"assetsCreated":{"type":"integer"},"rowsRejected":{"type":"integer"},"findings":{"type":"array","items":{"$ref":"#/components/schemas/RentalConfigurationFinding"}},"committed":{"type":"boolean"}}},
"RentalInventoryModel": {"type":"object","x-ticvai-persistence":"rental.inventory_model","description":"Board 1.5. **Pooled, serialised or hybrid**, and the switches the counter obeys.","required":["trackingModel"],"properties":{"trackingModel":{"type":"string","enum":["pooled","serialised","hybrid"]},"inventoryUnit":{"type":"string","nullable":true},"totalQuantity":{"type":"integer","nullable":true,"description":"Pooled only. *150 lockers.*"},"components":{"type":"array","description":"**Hybrid only** — *one serialised kayak, two pooled paddles, two pooled life jackets.* One booking, two mechanisms.\n","items":{"type":"object","properties":{"resourceTypeId":{"type":"string","format":"uuid","nullable":true},"label":{"type":"string"},"quantity":{"type":"integer"},"serialised":{"type":"boolean"}}}},"assignmentRequiredAtCheckout":{"type":"boolean","default":false},"scanRequired":{"type":"boolean","default":false},"allowManualAssignment":{"type":"boolean","default":true},"allowSubstitution":{"type":"boolean","default":true},"allowEquipmentSwap":{"type":"boolean","default":true},"scopePath":{"type":"string"}}},
"RentalLocationRule": {"type":"object","x-ticvai-persistence":"rental.location_rule","description":"Board 1.6. **Pickup and return are separate flags**, because a station that hands out kayaks and cannot receive them is a real shape.\n","required":["locationId"],"properties":{"locationId":{"type":"string","format":"uuid"},"enabled":{"type":"boolean","default":true},"pickupAllowed":{"type":"boolean","default":true},"returnAllowed":{"type":"boolean","default":true},"crossLocationReturnAllowed":{"type":"boolean","default":false},"inventoryAllocation":{"type":"integer","nullable":true},"inventoryBuffer":{"type":"integer","default":0,"description":"**Held back from online sale**, so the counter always has something to give the guest standing in front of it.\n"},"operatingHours":{"type":"object","nullable":true,"additionalProperties":true},"scopePath":{"type":"string"}}},
"RentalOperationalRules": {"type":"object","x-ticvai-persistence":"rental.operational_rules","description":"Board 1.8. **Three states per rule — required, optional, not applicable.** *Optional* and *not applicable* look identical at the counter and are entirely different in an audit.\n","properties":{"minimumAge":{"type":"integer","nullable":true},"maximumAge":{"type":"integer","nullable":true},"minimumHeightCm":{"type":"integer","nullable":true},"maximumWeightKg":{"type":"integer","nullable":true},"idRequired":{"$ref":"#/components/schemas/RuleRequirement"},"guardianRequired":{"$ref":"#/components/schemas/RuleRequirement"},"membershipRequired":{"$ref":"#/components/schemas/RuleRequirement"},"drivingLicenceRequired":{"$ref":"#/components/schemas/RuleRequirement"},"safetyBriefingRequired":{"$ref":"#/components/schemas/RuleRequirement"},"checkoutScanRequired":{"$ref":"#/components/schemas/RuleRequirement"},"returnScanRequired":{"$ref":"#/components/schemas/RuleRequirement"},"conditionInspectionRequired":{"$ref":"#/components/schemas/RuleRequirement"},"photoAtCheckoutRequired":{"$ref":"#/components/schemas/RuleRequirement"},"photoAtReturnRequired":{"$ref":"#/components/schemas/RuleRequirement"},"maximumQuantityPerCustomer":{"type":"integer","nullable":true},"returnLocationRestricted":{"type":"boolean","default":false},"partialReturnAllowed":{"type":"boolean","default":true},"staffApprovalRequired":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"RentalProduct": {"type":"object","x-ticvai-persistence":"rental.product","description":"Board 1.3. **The master reference every later board resolves against.**","required":["code","name","venueId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"internalName":{"type":"string","nullable":true},"description":{"type":"string","nullable":true},"categoryId":{"type":"string","format":"uuid","nullable":true},"imageAssetId":{"type":"string","format":"uuid","nullable":true},"tags":{"type":"array","items":{"type":"string"}},"tenantId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"trackingModel":{"type":"string","enum":["pooled","serialised","hybrid"]},"catalogueProductId":{"type":"string","format":"uuid","nullable":true,"description":"**The thing the guest actually buys.** `catalogue` sells it and this configures how it behaves once sold; the link is here so a rental is never sold twice through two different product records.\n"},"resourceTypeId":{"type":"string","format":"uuid","nullable":true,"description":"**For serialised products, the `resources` type its assets belong to.** The individual bikes are resources and maintenance assets — this contract does not keep a third register of them.\n"},"status":{"type":"string","enum":["draft","configurationReview","approved","active","suspended","archived"]},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"version":{"type":"integer","default":1},"isActive":{"type":"boolean","default":true}}},
"RuleRequirement": {"type":"string","enum":["required","optional","notApplicable"],"default":"notApplicable"}
}
```
