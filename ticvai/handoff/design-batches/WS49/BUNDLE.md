# WS49 — Promotions   Bundles Management board 5

**10 screens · 13 operations · 18 schemas · 4 permissions**

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
| `ADM-178` | Bundle & Combo Command Center | B–D | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-179` | Bundle Definition & Setup | A | 15 | 10 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-180` | Bundle Component Builder | A | 5 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-181` | Guest Choice & Build-Your-Own Bundle Designer | A | 3 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-182` | Bundle Pricing & Commercial Model | B–D | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-183` | Bundle Availability, Capacity & Validation | B–D | 0 | 4 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-184` | Bundle Validity, Scheduling & Redemption Rules | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-185` | Partner & External Product Bundle Manager | B–D | 13 | 14 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-186` | Revenue Allocation, Cost & Settlement Rules | B–D | 8 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-187` | Bundle Preview, Simulation & AI Recommendation | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-183, ADM-184 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-178` Bundle & Combo Command Center

**Provide centralized visibility and management of all bundles and combo products across**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bundle-combo-command-center-adm-178` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search bundle combo | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by ticket bundle, multi-attraction, multi-park, family package, ticket + f&b, ticket + retail and 7 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Ticket bundle | text field | — | — | `listBundleCombo` ?ticketBundle |
| Multi attraction | text field | — | — | `listBundleCombo` ?multiAttraction |
| Multi park | text field | — | — | `listBundleCombo` ?multiPark |
| Family package | text field | — | — | `listBundleCombo` ?familyPackage |
| Ticket FB | text field | — | — | `listBundleCombo` ?ticketFB |
| Ticket retail | text field | — | — | `listBundleCombo` ?ticketRetail |
| Ticket experience | text field | — | — | `listBundleCombo` ?ticketExperience |
| Ticket parking | text field | — | — | `listBundleCombo` ?ticketParking |
| Ticket fnb | text field | — | — | `listBundleCombo` ?ticketFnb |
| Membership package | text field | — | — | `listBundleCombo` ?membershipPackage |
| Partner bundle | text field | — | — | `listBundleCombo` ?partnerBundle |
| Hotel package | text field | — | — | `listBundleCombo` ?hotelPackage |
| Dynamic bundle | text field | — | — | `listBundleCombo` ?dynamicBundle |
| Build your own bundle | text field | — | — | `listBundleCombo` ?buildYourOwnBundle |

#### Outputs: what the screen shows and produces

**Shown**

**Active Bundles** (metric tile)

**Draft Bundles** (metric tile)

**Scheduled Bundles** (metric tile)

**Dynamic Bundles** (metric tile)

**Fixed Bundles** (metric tile)

**Guest-Choice Bundles** (metric tile)

**Partner Bundles** (metric tile)

**Bundle Sales** (metric tile)

**Bundle Revenue** (metric tile)

**Average Bundle Value** (metric tile)

**Bundle Conversion Rate** (metric tile)

**Redemption Rate** (metric tile)

**AOV Uplift** (metric tile)

**Bundle Margin** (metric tile)

**Data it reads**: `listBundleCombo` (onLoad, Bundle & Combo Command Center)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-179` Bundle Definition & Setup: *Works in Bundle Definition & Setup*; calls `listBundleCombo`
- → `ADM-180` Bundle Component Builder: *Works in Bundle Component Builder*; calls `listBundleCombo`
- → `ADM-181` Guest Choice & Build-Your-Own Bundle Designer: *Works in Guest Choice & Build-Your-Own Bundle Designer*; calls `listBundleCombo`
- → `ADM-182` Bundle Pricing & Commercial Model: *Works in Bundle Pricing & Commercial Model*; calls `listBundleCombo`
- → `ADM-183` Bundle Availability, Capacity & Validation: *Works in Bundle Availability, Capacity & Validation*; calls `listBundleCombo`
- → `ADM-184` Bundle Validity, Scheduling & Redemption Rules: *Works in Bundle Validity, Scheduling & Redemption Rules*; calls `listBundleCombo`
- → `ADM-185` Partner & External Product Bundle Manager: *Works in Partner & External Product Bundle Manager*; calls `listBundleCombo`
- → `ADM-186` Revenue Allocation, Cost & Settlement Rules: *Works in Revenue Allocation, Cost & Settlement Rules*; calls `listBundleCombo`
- → `ADM-187` Bundle Preview, Simulation & AI Recommendation: *Works in Bundle Preview, Simulation & AI Recommendation*; calls `listBundleCombo`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle combo list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle combo untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle combo yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bundle combo are still there. The pack's own statuses are Draft — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBundleCombo` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-178` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS110 Promotions   Bundles Management Board 5.dc.html#adm-178`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 5
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 1: Opens Bundle & Combo Command Center → Provide centralized visibility and management of all bundles and combo products across
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F158 branch at step 1 (expected): when Nothing has been set up on Bundle & Combo Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F158 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-178?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-179`, `ADM-180`, `ADM-181`, `ADM-182`, `ADM-183`, `ADM-184`, `ADM-185`, `ADM-186`, `ADM-187`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-179` Bundle Definition & Setup

**Create the commercial identity and high-level behavior of a bundle.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20654 (APP-SETUP-ADM-179) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE`, `PRICE_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Configure whether the bundle) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bundle-definition-setup-adm-179` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Bundle name | select field | — | — | — | — | — | — |
| Bundle ID | select field | — | — | — | — | — | — |
| Internal description | select field | — | — | — | — | — | — |
| Guest-facing description | select field | — | — | — | — | — | — |
| Business entity | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Bundle category | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Campaign | select field | — | — | — | — | — | — |
| Effective dates | select field | — | — | — | — | — | — |
| Sales status | select field | — | — | — | — | — | — |
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?venueId |
| Active at | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?activeAt=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?activeAt |
| Owner principal id | picker: choose an owner principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ownerPrincipalId=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?ownerPrincipalId |
| Q | text field | optional | — | max length 100 | — | Sends `?q=` to `listCommercialCampaigns`. | `listCommercialCampaigns` ?q |

#### Outputs: what the screen shows and produces

**Shown**

**Every commercial campaign** (data table, from `listCommercialCampaigns`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Owner principal | the name it points at, never the id | The campaign (and budget) owner. |
| Legal entity | the name it points at, never the id | The business entity that funds and books the campaign. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Budgets | list or chips (count when long) | The rows of `promotions.campaign_budget`, one per budget line. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCommercialCampaigns` (onLoad, List commercial campaigns)

**Where the user goes next**

- → `ADM-178` Bundle & Combo Command Center: *Returns to the board's landing screen*; calls `setBundleDefinition`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle definition configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle definition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle definition configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setBundleDefinition` → `PRICE_CONFIGURE` (configure) · staff
- `listCommercialCampaigns` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-179` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS110 Promotions   Bundles Management Board 5.dc.html#adm-179`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 5
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 2: Works in Bundle Definition & Setup → Create the commercial identity and high-level behavior of a bundle.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-179?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-178`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-180` Bundle Component Builder

**Define exactly what products and services make up the bundle.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20655 (APP-SETUP-ADM-180) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bundle-component-builder-adm-180` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Fixed quantity | select field | — | — | — | — | — | — |
| Minimum | select field | — | — | — | — | — | — |
| Maximum | select field | — | — | — | — | — | — |
| Quantity based on guest count | text field | — | — | — | — | — | — |
| Quantity based on ticket count | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-178` Bundle & Combo Command Center: *Returns to the board's landing screen*; calls `setBundleComponent`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle component configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle component untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle component configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setBundleComponent` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Multi-park / multi-attraction / multi-venue bundles are visually mapped, showing which venues, meal vouchers, VIP parking or upgrade options a bundle includes. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-469)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-180` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS110 Promotions   Bundles Management Board 5.dc.html#adm-180`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 5
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 4: Works in Bundle Component Builder → Define exactly what products and services make up the bundle.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-180?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-178`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-181` Guest Choice & Build-Your-Own Bundle Designer

**Configure bundles where the guest chooses products from predefined groups. The matrix specifically requires the guest to be able to choose attractions, experiences, F&B, retail products, or services from predefined categories while maintaining bundle pricing rules.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20656 (APP-SETUP-ADM-181) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Choose 1 F&B Option) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/guest-choice-build-your-own-bundle-designer-adm-181` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Meal A | select field | — | — | — | — | — | — |
| Meal B | select field | — | — | — | — | — | — |
| Meal C | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-178` Bundle & Combo Command Center: *Returns to the board's landing screen*; calls `setGuestChoiceBuild`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guest choice build-your-own configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guest choice build-your-own untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guest choice build-your-own configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGuestChoiceBuild` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-181` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS110 Promotions   Bundles Management Board 5.dc.html#adm-181`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 5
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 6: Works in Guest Choice & Build-Your-Own Bundle Designer → Configure bundles where the guest chooses products from predefined groups. The matrix specifically requires the guest to be able to choose attractions, experiences, F&B, retail products, or services …

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-181?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-178`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-182` Bundle Pricing & Commercial Model

**Determine how the bundle is commercially priced.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Pricing Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bundle-pricing-commercial-model-adm-182` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Base price | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Discount % | select field | — | — | — | — | — | — |
| Discount amount | select field | — | — | — | — | — | — |
| Minimum price | select field | — | — | — | — | — | — |
| Maximum price | select field | — | — | — | — | — | — |
| Price floor | select field | — | — | — | — | — | — |
| Margin floor | select field | — | — | — | — | — | — |
| Guest-specific price | select field | — | — | — | — | — | — |
| Channel-specific price | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listBundlePricingCommercial` (onLoad, Bundle Pricing & Commercial Model)

**Where the user goes next**

- → `ADM-178` Bundle & Combo Command Center: *Returns to the board's landing screen*; calls `listBundlePricingCommercial`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle pricing commercial configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle pricing commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle pricing commercial configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBundlePricingCommercial` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-182` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS110 Promotions   Bundles Management Board 5.dc.html#adm-182`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 5
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 8: Works in Bundle Pricing & Commercial Model → Determine how the bundle is commercially priced.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-182?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-178`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-183` Bundle Availability, Capacity & Validation

**Ensure that TICVAI does not sell a bundle unless all required components can actually be fulfilled. This is a direct requirement of the matrix: each bundle component maintains independent inventory, capacity, validity, redemption rules, and availability, and the system validates included products before confirming the sale.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§For each component display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bundle-availability-capacity-validation-adm-183` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every bundle availability capacity** (data table, from `listBundleAvailabilityCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Available | 1,234 | Quantity available |
| Component status | chip: Available, Low availability, Sold out, Suspended, Unpublished, Invalid date… | Availability of the component. |

**The selected bundle availability capacity** (detail panel): The pack groups this record's detail under its own headings: “Bundle selected”, “Check mandatory components”, “Check inventory”, “Check capacity”, “Check schedule/timeslot”, “Check validity”.

| Shows | Format | Notes |
|---|---|---|
| Available | 1,234 | Quantity available |
| Component status | chip: Available, Low availability, Sold out, Suspended, Unpublished, Invalid date… | Availability of the component. |

**Data it reads**: `listBundleAvailabilityCapacity` (onLoad, Bundle Availability, Capacity & Validation)

**Where the user goes next**

- → `ADM-178` Bundle & Combo Command Center: *Returns to the board's landing screen*; calls `listBundleAvailabilityCapacity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle availability capacity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle availability capacity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle availability capacity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bundle availability capacity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBundleAvailabilityCapacity` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-183` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS110 Promotions   Bundles Management Board 5.dc.html#adm-183`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 5
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 10: Works in Bundle Availability, Capacity & Validation → Ensure that TICVAI does not sell a bundle unless all required components can actually be fulfilled. This is a direct requirement of the matrix: each bundle component maintains independent inventory …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-183?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-178`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-184` Bundle Validity, Scheduling & Redemption Rules

**Control when bundle components may be consumed and whether they must be redeemed together or separately.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bundle-validity-scheduling-redemption-rules-adm-184` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listBundleValidityScheduling` (onLoad, Bundle Validity, Scheduling & Redemption Rules)

**Where the user goes next**

- → `ADM-178` Bundle & Combo Command Center: *Returns to the board's landing screen*; calls `listBundleValidityScheduling`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle validity scheduling list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle validity scheduling untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle validity scheduling yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bundle validity scheduling are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listBundleValidityScheduling` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-184` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS110 Promotions   Bundles Management Board 5.dc.html#adm-184`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 5
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 12: Works in Bundle Validity, Scheduling & Redemption Rules → Control when bundle components may be consumed and whether they must be redeemed together or separately.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-184?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-178`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-185` Partner & External Product Bundle Manager

**Allow TICVAI bundles to include products or services owned by external operators. The matrix requires combinations with external products/services and bundles across different destinations, including systems that may use different databases.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `bundleId` (navigation) |
| Route | `/commercial/partner-external-product-bundle-manager-adm-185` |

#### Inputs: what the user enters or picks

**Form: Save bundle partner product mappings** (modal, opened by *Save bundle partner product mappings*; *Save bundle partner product mappings* calls `setBundlePartnerProductMappings`, *Cancel* sends nothing)

**Collects what `setBundlePartnerProductMappings` sends before it is called.** Required: `mappings`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Mappings `mappings` | repeatable rows | required | — | at most 200 | — | — | `setBundlePartnerProductMappings` body |
| Bundle component `mappings[].bundleComponentId` | picker: choose a bundle component | required | — | — | shows names, sends the id | — | `setBundlePartnerProductMappings` body |
| Partner `mappings[].partnerId` | picker: choose a partner | required | — | — | shows names, sends the id | — | `setBundlePartnerProductMappings` body |
| External product `mappings[].externalProductId` | text field | required | — | max length 128 | — | — | `setBundlePartnerProductMappings` body |
| Product name `mappings[].productName` | text field | optional | — | max length 200 | — | — | `setBundlePartnerProductMappings` body |
| API source `mappings[].apiSource` | text field | optional | — | max length 100 | — | The partner integration the product comes through. | `setBundlePartnerProductMappings` body |
| Availability source `mappings[].availabilitySource` | segmented control | optional | Partner API | Partner API · Allocation · On request | — | Where availability is checked. | `setBundlePartnerProductMappings` body |
| External price `mappings[].externalPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setBundlePartnerProductMappings` body |
| Selling price `mappings[].sellingPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setBundlePartnerProductMappings` body |
| Commission `mappings[].commission` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setBundlePartnerProductMappings` body |
| Settlement rule `mappings[].settlementRule` | text area | optional | — | max length 500 | — | — | `setBundlePartnerProductMappings` body |
| Cancellation rule `mappings[].cancellationRule` | text area | optional | — | max length 500 | — | — | `setBundlePartnerProductMappings` body |
| Redemption method `mappings[].redemptionMethod` | text field | optional | — | max length 100 | — | — | `setBundlePartnerProductMappings` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A `bundleComponentId` is not a component of this bundle, two rows map the same component, or an `id` names a mapping of another bundle.

#### Outputs: what the screen shows and produces

**Shown**

**Every partner external product** (data table, from `listPartnerExternalProduct`)

| Shows | Format | Notes |
|---|---|---|
| Connection status | chip: Connected, Available, Degraded, API error, Product unavailable, Mapping error | Partner connection status. |

**Every partner bundle product** (data table, from `listBundlePartnerProductMappings`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Bundle component | the name it points at, never the id | — |
| Partner | the name it points at, never the id | — |
| External product | text | — |
| Product name | text | — |
| API source | text | The partner integration the product comes through. |
| Availability source | chip: Partner API, Allocation, On request | Where availability is checked. |
| External price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Selling price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Commission | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Settlement rule | text | — |
| Cancellation rule | text | — |

**The selected partner external product** (detail panel): The pack groups this record's detail under its own headings: “Dubai Weekend Package”.

| Shows | Format | Notes |
|---|---|---|
| Connection status | chip: Connected, Available, Degraded, API error, Product unavailable, Mapping error | Partner connection status. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save bundle partner product mappings (primary button) | `setBundlePartnerProductMappings` PUT `/bundles/{bundleId}/partner-products` | inline | inline | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 422 A `bundleComponentId` is not a component of this bundle, two rows map the same component, or an `id` names a … | gated `PRODUCT_CONFIGURE`; opens modal first |

**Data it reads**: `listPartnerExternalProduct` (onLoad, Partner & External Product Bundle Manager); `listBundlePartnerProductMappings` (onLoad, List a bundle's partner product mappings)

**Where the user goes next**

- → `ADM-178` Bundle & Combo Command Center: *Returns to the board's landing screen*; calls `listPartnerExternalProduct`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The partner external product list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the partner external product untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No partner external product yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the partner external product are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 A `bundleComponentId` is not a component of this bundle, two rows map the same component, or an `id` names a mapping of another bundle. |

#### Permissions

- `listPartnerExternalProduct` → `PRICE_VIEW` (read) · staff
- `listBundlePartnerProductMappings` → `PRODUCT_VIEW` (read) · staff
- `setBundlePartnerProductMappings` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-185` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS110 Promotions   Bundles Management Board 5.dc.html#adm-185`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 5
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 14: Works in Partner & External Product Bundle Manager → Allow TICVAI bundles to include products or services owned by external operators. The matrix requires combinations with external products/services and bundles across different destinations, including …

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-185?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save bundle partner product mappings.
- [ ] Every transition is wired: `ADM-178`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-186` Revenue Allocation, Cost & Settlement Rules

**Determine how bundle revenue is allocated across its components. This is explicitly required by the matrix for allocation across products, attractions, departments, partners, operators, and accounting entities.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Financial Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/revenue-allocation-cost-settlement-rules-adm-186` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Revenue account | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Cost center | select field | — | — | — | — | — | — |
| Legal entity | select field | — | — | — | — | — | — |
| Tax treatment | select field | — | — | — | — | — | — |
| Partner payable | select field | — | — | — | — | — | — |
| Commission | select field | — | — | — | — | — | — |
| Settlement cycle | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listRevenueAllocationCost` (onLoad, Revenue Allocation, Cost & Settlement Rules)

**Where the user goes next**

- → `ADM-178` Bundle & Combo Command Center: *Returns to the board's landing screen*; calls `listRevenueAllocationCost`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue allocation cost configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue allocation cost untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue allocation cost configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRevenueAllocationCost` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-186` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS110 Promotions   Bundles Management Board 5.dc.html#adm-186`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 5
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 16: Works in Revenue Allocation, Cost & Settlement Rules → Determine how bundle revenue is allocated across its components. This is explicitly required by the matrix for allocation across products, attractions, departments, partners, operators, and …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-186?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-178`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-187` Bundle Preview, Simulation & AI Recommendation

**Allow administrators to test promotional rules before activating them. This is critical because the matrix requires simulation of redemption, discount exposure, revenue impact, margin impact and financial performance before activation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/bundle-preview-simulation-ai-recommendation-adm-187` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Campaign Manager, Commercial Manager, Revenue Manager, Finance, B2B Manager, Venue Manager. Each needs an … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Create rules, Edit rules, Change discount, Change thresholds, Change segments, Change dates, Override limits, Run simulation, Submit, Approve, Activate. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Campaign Manager (primary button) | navigation or local | — | — | — | — |
| Commercial Manager (secondary button) | navigation or local | — | — | — | — |
| Revenue Manager (secondary button) | navigation or local | — | — | — | — |
| Finance (secondary button) | navigation or local | — | — | — | — |
| B2B Manager (secondary button) | navigation or local | — | — | — | — |
| Venue Manager (secondary button) | navigation or local | — | — | — | — |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bundle preview simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bundle preview simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bundle preview simulation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bundle preview simulation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulateBundlePreviewRecommendation` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-187` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS110 Promotions   Bundles Management Board 5.dc.html#adm-187`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 5
- Flow F158 *Promotions Bundles Management board 5: Bundle & Combo Command Center*, step 18: Works in Bundle Preview, Simulation & AI Recommendation → Allow administrators to test promotional rules before activating them. This is critical because the matrix requires simulation of redemption, discount exposure, revenue impact, margin impact and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-187?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Campaign Manager, Commercial Manager, Revenue Manager, Finance, B2B Manager, Venue Manager.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
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

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"listBundleAvailabilityCapacity": {"method":"GET","path":"/bundle-availability-capacity","contract":"promotions","summary":"Bundle Availability, Capacity & Validation","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleAvailabilityCapacityValidationView"},
"listBundleCombo": {"method":"GET","path":"/bundle-combo","contract":"promotions","summary":"Bundle & Combo Command Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"ticketBundle","in":"query","required":false},{"name":"multiAttraction","in":"query","required":false},{"name":"multiPark","in":"query","required":false},{"name":"familyPackage","in":"query","required":false},{"name":"ticketFB","in":"query","required":false},{"name":"ticketRetail","in":"query","required":false},{"name":"ticketExperience","in":"query","required":false},{"name":"ticketParking","in":"query","required":false},{"name":"ticketFnb","in":"query","required":false},{"name":"membershipPackage","in":"query","required":false},{"name":"partnerBundle","in":"query","required":false},{"name":"hotelPackage","in":"query","required":false},{"name":"dynamicBundle","in":"query","required":false},{"name":"buildYourOwnBundle","in":"query","required":false}],"requestBody":null,"responds":"BundleComboCommandCenterView"},
"listBundlePartnerProductMappings": {"method":"GET","path":"/bundles/{bundleId}/partner-products","contract":"promotions","summary":"List a bundle's partner product mappings","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBundlePricingCommercial": {"method":"GET","path":"/bundle-pricing-commercial","contract":"promotions","summary":"Bundle Pricing & Commercial Model","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundlePricingCommercialModelView"},
"listBundleValidityScheduling": {"method":"GET","path":"/bundle-validity-scheduling","contract":"promotions","summary":"Bundle Validity, Scheduling & Redemption Rules","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"BundleValiditySchedulingRedemptionRulesView"},
"listCommercialCampaigns": {"method":"GET","path":"/commercial-campaigns","contract":"promotions","summary":"List commercial campaigns","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"activeAt","in":"query","required":null},{"name":"ownerPrincipalId","in":"query","required":null},{"name":"q","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPartnerExternalProduct": {"method":"GET","path":"/partner-external-product","contract":"promotions","summary":"Partner & External Product Bundle Manager","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PartnerExternalProductBundleManagerView"},
"listRevenueAllocationCost": {"method":"GET","path":"/revenue-allocation-cost","contract":"promotions","summary":"Revenue Allocation, Cost & Settlement Rules","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RevenueAllocationCostSettlementRulesView"},
"setBundleComponent": {"method":"PUT","path":"/bundle-component","contract":"promotions","summary":"Bundle Component Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BundleComponentBuilderInput","responds":"BundleComponentBuilderView"},
"setBundleDefinition": {"method":"PUT","path":"/bundle-definition","contract":"promotions","summary":"Bundle Definition & Setup","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BundleDefinitionSetupInput","responds":"BundleDefinitionSetupView"},
"setBundlePartnerProductMappings": {"method":"PUT","path":"/bundles/{bundleId}/partner-products","contract":"promotions","summary":"Set a bundle's partner product mappings","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setGuestChoiceBuild": {"method":"PUT","path":"/guest-choice-build","contract":"promotions","summary":"Guest Choice & Build-Your-Own Bundle Designer","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestChoiceBuildYourOwnBundleDesignerInput","responds":"GuestChoiceBuildYourOwnBundleDesignerView"},
"simulateBundlePreviewRecommendation": {"method":"PUT","path":"/bundle-preview-recommendation","contract":"promotions","summary":"Bundle Preview, Simulation & AI Recommendation","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BundlePreviewSimulationAiRecommendationInput","responds":"BundlePreviewSimulationAiRecommendationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"BundleAvailabilityCapacityValidationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Availability, Capacity & Validation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"componentStatus":{"type":"string","enum":["available","lowAvailability","soldOut","suspended","unpublished","invalidDate","capacityUnavailable"],"description":"Availability of the component."},"bundleId":{"type":"string","description":"Bundle ID"},"componentId":{"type":"string","description":"Component ID"},"componentName":{"type":"string","description":"Component"},"available":{"type":"integer","description":"Quantity available"},"failureBehavior":{"type":"string","enum":["preventSale","hideBundle","offerSubstitute","allowAlternateDate","allowAlternateTimeslot","removeOptionalComponent","recommendAnotherBundle"],"description":"Configured behaviour when a component is unavailable"}}},
"BundleComboCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle & Combo Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activeBundles":{"type":"integer","description":"Active Bundles"},"draftBundles":{"type":"integer","description":"Draft Bundles"},"scheduledBundles":{"type":"integer","description":"Scheduled Bundles"},"dynamicBundles":{"type":"integer","description":"Dynamic Bundles"},"fixedBundles":{"type":"integer","description":"Fixed Bundles"},"guestChoiceBundles":{"type":"integer","description":"Guest-Choice Bundles"},"partnerBundles":{"type":"integer","description":"Partner Bundles"},"bundleSales":{"type":"integer","description":"Bundle Sales"},"bundleRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Bundle Revenue"},"averageBundleValue":{"type":"number","description":"Average Bundle Value"},"bundleConversionRate":{"type":"number","description":"Bundle Conversion Rate"},"redemptionRate":{"type":"number","description":"Redemption Rate"},"aovUplift":{"type":"number","description":"AOV Uplift"},"bundleMargin":{"type":"number","description":"Bundle Margin"},"draft":{"type":"string","description":"Draft"},"incomplete":{"type":"string","description":"Incomplete"},"pendingValidation":{"type":"integer","description":"Pending Validation"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"scheduled":{"type":"string","format":"date-time","description":"Scheduled"},"active":{"type":"integer","description":"Active"},"paused":{"type":"string","description":"Paused"},"suspended":{"type":"string","description":"Suspended"},"expired":{"type":"integer","description":"Expired"},"archived":{"type":"string","description":"Archived"}}},
"BundleComponentBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Bundle Component Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"typesType":{"type":"string","enum":["mandatory","optional","choice","conditional","recommended"],"description":"Vocabulary listed under Component Types."},"fixedQuantity":{"type":"integer","description":"Fixed quantity"},"minimum":{"type":"string","description":"Minimum"},"maximum":{"type":"string","description":"Maximum"},"quantityBasedOnGuestCount":{"type":"integer","description":"Quantity based on guest count"},"quantityBasedOnTicketCount":{"type":"integer","description":"Quantity based on ticket count"},"componentType":{"type":"string","enum":["admissionTicket","attraction","event","timeslot","experience","membership","annualPass","fBProduct","fBMealPackage","retailProduct","parking","locker","photo","rental","voucher","giftCard","service","externalProduct"],"description":"What the component is."}}},
"BundleComponentBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Component Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"typesType":{"type":"string","enum":["mandatory","optional","choice","conditional","recommended"],"description":"Vocabulary listed under Component Types."},"fixedQuantity":{"type":"integer","description":"Fixed quantity"},"minimum":{"type":"string","description":"Minimum"},"maximum":{"type":"string","description":"Maximum"},"quantityBasedOnGuestCount":{"type":"integer","description":"Quantity based on guest count"},"quantityBasedOnTicketCount":{"type":"integer","description":"Quantity based on ticket count"},"componentType":{"type":"string","enum":["admissionTicket","attraction","event","timeslot","experience","membership","annualPass","fBProduct","fBMealPackage","retailProduct","parking","locker","photo","rental","voucher","giftCard","service","externalProduct"],"description":"What the component is."}}},
"BundleDefinitionSetupInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is promotions.allocation_split at 5%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Bundle Definition & Setup submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"bundleName":{"type":"string","description":"Bundle name"},"bundleId":{"type":"string","description":"Bundle ID"},"internalDescription":{"type":"string","description":"Internal description"},"guestFacingDescription":{"type":"string","description":"Guest-facing description"},"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"bundleCategory":{"type":"string","description":"Bundle category"},"owner":{"type":"string","description":"Owner"},"campaign":{"type":"string","description":"Campaign"},"effectiveDates":{"type":"string","description":"Effective dates"},"salesStatus":{"type":"string","description":"Sales status"},"appearsAsStandaloneProduct":{"type":"string","description":"Appears as standalone product"},"isRecommendedDuringCheckout":{"type":"boolean","description":"Is recommended during checkout"},"requiresAnotherProduct":{"type":"string","description":"Requires another product"},"bundleType":{"type":"string","enum":["fixed","configurable","buildYourOwn","dynamic","partner"],"description":"Bundle type"}}},
"BundleDefinitionSetupView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Definition & Setup displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"bundleName":{"type":"string","description":"Bundle name"},"bundleId":{"type":"string","description":"Bundle ID"},"internalDescription":{"type":"string","description":"Internal description"},"guestFacingDescription":{"type":"string","description":"Guest-facing description"},"businessEntity":{"type":"string","description":"Business entity"},"venue":{"type":"string","description":"Venue"},"bundleCategory":{"type":"string","description":"Bundle category"},"owner":{"type":"string","description":"Owner"},"campaign":{"type":"string","description":"Campaign"},"effectiveDates":{"type":"string","description":"Effective dates"},"salesStatus":{"type":"string","description":"Sales status"},"appearsAsStandaloneProduct":{"type":"string","description":"Appears as standalone product"},"isRecommendedDuringCheckout":{"type":"boolean","description":"Is recommended during checkout"},"requiresAnotherProduct":{"type":"string","description":"Requires another product"},"bundleType":{"type":"string","enum":["fixed","configurable","buildYourOwn","dynamic","partner"],"description":"Bundle type: all components predefined; required plus optional choices; guest selects from permitted categories; changes with availability or rules; contains internal and external products"}}},
"BundlePreviewSimulationAiRecommendationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is promotions.bundle_component at 3%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Bundle Preview, Simulation & AI Recommendation submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"bundleId":{"type":"string","description":"Bundle ID"},"previewChannel":{"type":"string","enum":["b2c","mobileApp","pos","kiosk","b2b","partnerChannel"],"description":"Channel whose guest journey is previewed"},"components":{"type":"array","items":{"type":"string"},"description":"Components to simulate"}}},
"BundlePreviewSimulationAiRecommendationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Preview, Simulation & AI Recommendation displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"bundleId":{"type":"string","description":"Bundle ID"},"previewChannel":{"type":"string","enum":["b2c","mobileApp","pos","kiosk","b2b","partnerChannel"],"description":"Channel whose guest journey is previewed"},"components":{"type":"array","items":{"type":"string"},"description":"Components in the simulated bundle"},"individualValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Individual value of the components"},"bundlePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Bundle price"},"guestSaving":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Guest saving"},"guestSavingPercent":{"type":"number","description":"Guest saving, percent"},"estimatedMargin":{"type":"number","description":"Estimated margin, percent"},"failedValidations":{"type":"array","items":{"type":"string","enum":["componentAvailability","capacity","pricing","validity","revenueAllocation","channelAssignment","tax","partnerConnection","marginFloor"]},"description":"Validations that block publication; empty means READY TO PUBLISH"},"readyToPublish":{"type":"boolean","description":"Ready to publish"},"aiRecommendation":{"type":"string","description":"AI bundle recommendation (a draft; never published without configured approval)"}}},
"BundlePricingCommercialModelView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Pricing & Commercial Model displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Base price"},"currency":{"type":"string","description":"Currency"},"discount":{"type":"number","description":"Discount %"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount amount"},"minimumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum price"},"maximumPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum price"},"priceFloor":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Price floor"},"marginFloor":{"type":"number","description":"Margin floor"},"guestSpecificPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Guest-specific price"},"channelSpecificPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Channel-specific price"},"pricingModel":{"type":"string","enum":["fixedBundlePrice","sumMinusDiscount","componentPricing","startingFrom","tieredBundlePrice","dynamicBundlePrice"],"description":"How the bundle is priced; a dynamic bundle price is calculated by the pricing engine"},"upgradeCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Surcharge when the guest picks a premium option"}}},
"BundleValiditySchedulingRedemptionRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Bundle Validity, Scheduling & Redemption Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ownValidity":{"type":"string","description":"Own validity"},"ownCapacity":{"type":"integer","description":"Own capacity"},"ownTimeslot":{"type":"string","description":"Own timeslot"},"ownRedemptionCount":{"type":"integer","description":"Own redemption count"},"ownEntitlement":{"type":"string","description":"Own entitlement"},"ownAccessRule":{"type":"string","description":"Own access rule"},"redemptionModel":{"type":"string","enum":["allComponentsTogether","independentRedemption","sequentialRedemption","firstUseActivation","scheduledRedemption","timeslotReservationRequired"],"description":"How the bundle's components are redeemed."}}},
"CampaignBudget": {"x-ticvai-persistence":"promotions.campaign_budget","type":"object","description":"One budget line of a commercial campaign (setCampaignBudgetFinancial): what kind of spend it caps, who funds it, what it covers, and what happens as it is consumed. **Consumed, committed and reserved are not stored**: consumed is the discount given on orders (`orders.discount`, `promotions.promotion.discount_given`), committed and reserved are priced carts not yet paid, all worked out on read so they cannot drift from the orders they summarise. (DM5, 29 September: data model for the agreed operations)","required":["budgetType","amount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"budgetType":{"type":"string","enum":["total","discount","reward","freeProduct"],"description":"The spend this line caps (total campaign, discount, reward or free-product budget)."},"fundingSource":{"type":"string","nullable":true,"enum":["venue","department","marketing","partner"],"description":"Who pays for it; `partner` is a co-funded (e.g. bank or partner-funded) line."},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"scope":{"type":"string","enum":["entireCampaign","promotion","product","channel","partner","customerSegment"],"default":"entireCampaign","description":"What the line covers."},"scopeRef":{"type":"string","nullable":true,"description":"The promotion, product, partner or segment id, or the SalesChannel value, that `scope` names. Null for `entireCampaign`."},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The budget owner."},"costCentre":{"type":"string","maxLength":64,"nullable":true},"department":{"type":"string","maxLength":100,"nullable":true},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"thresholdPolicy":{"$ref":"#/components/schemas/BudgetThresholdPolicy"}}},
"CommercialCampaign": {"x-ticvai-persistence":"promotions.campaign + promotions.campaign_budget","type":"object","description":"A commercial campaign: the grouping of promotions, coupon campaigns and bundles that share an owner, a business entity, dates and a budget. **Not `marketing.campaign`**, which is the CRM send campaign in another service. The header is saved with its budget lines by setCampaignBudgetFinancial (the budget screen is where the pack captures campaign, owner, business entity and effective dates), and on its own by createCommercialCampaign and updateCommercialCampaign; listCommercialCampaigns lists it (decided 29 September, writers pass); promotions, coupon campaigns and bundles point at it by `campaignId`. No status of its own: a campaign is live while its promotions are, and a threshold action that stops it pauses them. (DM5, 29 September: data model for the agreed operations)","required":["id","venueId","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64,"nullable":true},"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000,"nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The campaign (and budget) owner."},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"The business entity that funds and books the campaign."},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"budgets":{"type":"array","description":"The rows of `promotions.campaign_budget`, one per budget line.","items":{"$ref":"#/components/schemas/CampaignBudget"}}}},
"GuestChoiceBuildYourOwnBundleDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Guest Choice & Build-Your-Own Bundle Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each group* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"groupName":{"type":"string","description":"Group name"},"category":{"type":"string","description":"Category"},"minimumSelections":{"type":"string","description":"Minimum selections"},"maximumSelections":{"type":"string","description":"Maximum selections"},"requiredOptional":{"type":"string","description":"Required/optional"},"eligibleProducts":{"type":"string","description":"Eligible products"},"additionalCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Additional charge"},"selectionOrder":{"type":"string","description":"Selection order"}},"x-ticvai-record-definition":"For each group"},
"GuestChoiceBuildYourOwnBundleDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Guest Choice & Build-Your-Own Bundle Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"groupName":{"type":"string","description":"Group name"},"category":{"type":"string","description":"Category"},"minimumSelections":{"type":"string","description":"Minimum selections"},"maximumSelections":{"type":"string","description":"Maximum selections"},"requiredOptional":{"type":"string","description":"Required/optional"},"eligibleProducts":{"type":"string","description":"Eligible products"},"additionalCharge":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Additional charge"},"selectionOrder":{"type":"string","description":"Selection order"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PartnerBundleProduct": {"x-ticvai-persistence":"promotions.partner_bundle_product","type":"object","description":"A partner's or external product sold as a bundle component: the partner's product id and source, its price to us and ours to the guest, the commission, and the settlement, cancellation and redemption terms (Partner & External Product Bundle Manager). Tied to the `promotions.bundle_component` that stands for it. `connectionStatus` is the last health reading of the partner integration, written by the sync job. (DM5, 29 September: data model for the agreed operations)\n**Written by setBundlePartnerProductMappings; read by listBundlePartnerProductMappings and listPartnerExternalProduct** (decided 29 September, writers pass). `connectionStatus` and `lastCheckedAt` are the partner sync job's alone: it polls each mapped partner product and writes them, and no operation takes them from a request.","required":["id","bundleComponentId","partnerId","externalProductId"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"bundleComponentId":{"type":"string","format":"uuid"},"partnerId":{"type":"string","format":"uuid"},"externalProductId":{"type":"string","maxLength":128},"productName":{"type":"string","maxLength":200},"apiSource":{"type":"string","maxLength":100,"nullable":true,"description":"The partner integration the product comes through."},"availabilitySource":{"type":"string","enum":["partnerApi","allocation","onRequest"],"default":"partnerApi","description":"Where availability is checked."},"externalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"sellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"settlementRule":{"type":"string","maxLength":500,"nullable":true},"cancellationRule":{"type":"string","maxLength":500,"nullable":true},"redemptionMethod":{"type":"string","maxLength":100,"nullable":true},"connectionStatus":{"type":"string","readOnly":true,"description":"Written by the partner sync job only; `available` until its first reading.","enum":["connected","available","degraded","apiError","productUnavailable","mappingError"]},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the partner sync job last read the partner."}}},
"PartnerExternalProductBundleManagerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Partner & External Product Bundle Manager displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"partner":{"type":"string","description":"Partner"},"externalProductId":{"type":"string","description":"External product ID"},"productName":{"type":"string","description":"Product name"},"apiSource":{"type":"string","description":"API source"},"availabilitySource":{"type":"string","description":"Availability source"},"externalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"External price"},"ticvaiSellingPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"TICVAI selling price"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission"},"settlementRule":{"type":"string","description":"Settlement rule"},"cancellationRule":{"type":"string","description":"Cancellation rule"},"redemptionMethod":{"type":"string","description":"Redemption method"},"connectionStatus":{"type":"string","enum":["connected","available","degraded","apiError","productUnavailable","mappingError"],"description":"Partner connection status."}}},
"RevenueAllocationCostSettlementRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Revenue Allocation, Cost & Settlement Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"revenueAccount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue account"},"department":{"type":"string","description":"Department"},"costCenter":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost center"},"legalEntity":{"type":"string","description":"Legal entity"},"taxTreatment":{"type":"string","description":"Tax treatment"},"partnerPayable":{"type":"string","description":"Partner payable"},"commission":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Commission"},"settlementCycle":{"type":"string","description":"Settlement cycle"},"allocationMethod":{"type":"string","enum":["fixedAmount","percentage","proportionalListPrice","weightedAllocation","costPlus","contractualPartnerAllocation","redemptionBasedAllocation"],"description":"How bundle revenue is allocated to components."}}}
}
```
