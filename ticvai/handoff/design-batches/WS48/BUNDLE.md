# WS48 — Promotions   Bundles Management board 4

**10 screens · 10 operations · 14 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PRICE_CONFIGURE, PRICE_VIEW`. A control nobody can use must say so,
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
| `ADM-168` | Advanced Offer Command Center | B–D | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-169` | Buy X Get Y / BOGO Rule Builder | A | 15 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-170` | Multi-Buy & Quantity Offer Configurator | B–D | 3 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-171` | Cheapest / Lowest-Value Item Promotion | B–D | 7 | 0 | 5 | 0 | 1 | 2 | — | notStarted (generated) |
| `ADM-172` | Fixed-Price & “N for X” Offer Builder | A | 8 | 0 | 5 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-173` | Gift, Free Product & Added-Value Offer Builder | A | 5 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-174` | Cross-Category Promotion Builder | A | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (generated) |
| `ADM-175` | Reward Selection, Substitution & Customer Choice | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-176` | Advanced Offer Guardrails & Conflict Controls | B–D | 6 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-177` | Offer Simulation, Basket Trace & AI Optimization | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-170, ADM-174, ADM-175 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-168` Advanced Offer Command Center

**Provide the centralized management workspace for all advanced promotional mechanics.**

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
| Route | `/commercial/advanced-offer-command-center-adm-168` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search advanced offer | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by buy x get x, buy x get y, buy n get x, buy n get multiple, cheapest item free, percentage off another product and 6 more — which are present is a decision the pack … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Buy x get x | text field | — | — | `listAdvancedOffer` ?buyXGetX |
| Buy x get y | text field | — | — | `listAdvancedOffer` ?buyXGetY |
| Buy n get x | text field | — | — | `listAdvancedOffer` ?buyNGetX |
| Buy n get multiple | text field | — | — | `listAdvancedOffer` ?buyNGetMultiple |
| Cheapest item free | text field | — | — | `listAdvancedOffer` ?cheapestItemFree |
| Percentage off another product | number field (%) | — | — | `listAdvancedOffer` ?percentageOffAnotherProduct |
| Amount off another product | text field | — | — | `listAdvancedOffer` ?amountOffAnotherProduct |
| Fixed bundle price | text field | — | — | `listAdvancedOffer` ?fixedBundlePrice |
| Gift with purchase | text field | — | — | `listAdvancedOffer` ?giftWithPurchase |
| Added value | text field | — | — | `listAdvancedOffer` ?addedValue |
| Cross category reward | text field | — | — | `listAdvancedOffer` ?crossCategoryReward |
| Upgrade offer | text field | — | — | `listAdvancedOffer` ?upgradeOffer |

#### Outputs: what the screen shows and produces

**Shown**

**Active Advanced Offers** (metric tile)

**Scheduled Offers** (metric tile)

**BOGO Campaigns** (metric tile)

**Gift-with-Purchase Offers** (metric tile)

**Fixed-Price Offers** (metric tile)

**Cross-Category Offers** (metric tile)

**Total Redemptions** (metric tile)

**Free Items Issued** (metric tile)

**Discount Granted** (metric tile)

**Revenue Generated** (metric tile)

**AOV Uplift** (metric tile)

**Margin Impact** (metric tile)

**Data it reads**: `listAdvancedOffer` (onLoad, Advanced Offer Command Center); `listAdvancedOfferGuardrail` (onLoad, Advanced Offer Guardrails & Conflict Controls)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-169` Buy X Get Y / BOGO Rule Builder: *Works in Buy X Get Y / BOGO Rule Builder*; calls `listAdvancedOffer`
- → `ADM-170` Multi-Buy & Quantity Offer Configurator: *Works in Multi-Buy & Quantity Offer Configurator*; calls `listAdvancedOffer`
- → `ADM-171` Cheapest / Lowest-Value Item Promotion: *Works in Cheapest / Lowest-Value Item Promotion*; calls `listAdvancedOffer`
- → `ADM-172` Fixed-Price & “N for X” Offer Builder: *Works in Fixed-Price & “N for X” Offer Builder*; calls `listAdvancedOffer`
- → `ADM-173` Gift, Free Product & Added-Value Offer Builder: *Works in Gift, Free Product & Added-Value Offer Builder*; calls `listAdvancedOffer`
- → `ADM-174` Cross-Category Promotion Builder: *Works in Cross-Category Promotion Builder*; calls `listAdvancedOffer`
- → `ADM-175` Reward Selection, Substitution & Customer Choice: *Works in Reward Selection, Substitution & Customer Choice*; calls `listAdvancedOffer`
- → `ADM-176` Advanced Offer Guardrails & Conflict Controls: *Works in Advanced Offer Guardrails & Conflict Controls*; calls `listAdvancedOffer`
- → `ADM-177` Offer Simulation, Basket Trace & AI Optimization: *Works in Offer Simulation, Basket Trace & AI Optimization*; calls `listAdvancedOffer`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The advanced offer list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the advanced offer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No advanced offer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the advanced offer are still there. The pack's own statuses are Draft — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAdvancedOffer` → `PRICE_VIEW` (read) · staff
- `listAdvancedOfferGuardrail` → `PRICE_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-168` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-168`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 1: Opens Advanced Offer Command Center → Provide the centralized management workspace for all advanced promotional mechanics.
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F157 branch at step 1 (expected): when Nothing has been set up on Advanced Offer Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F157 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-168?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-169`, `ADM-170`, `ADM-171`, `ADM-172`, `ADM-173`, `ADM-174`, `ADM-175`, `ADM-176`, `ADM-177`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-169` Buy X Get Y / BOGO Rule Builder

**Configure the fundamental qualifier → reward relationship.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20650 (APP-SETUP-ADM-169) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/buy-x-get-y-bogo-rule-builder-adm-169` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Product | select field | — | — | — | — | — | — |
| Product category | select field | — | — | — | — | — | — |
| Ticket type | select field | — | — | — | — | — | — |
| Quantity | select field | — | — | — | — | — | — |
| Minimum spend | select field | — | — | — | — | — | — |
| Customer segment | select field | — | — | — | — | — | — |
| Channel | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |
| Same product | select field | — | — | — | — | — | — |
| Different product | select field | — | — | — | — | — | — |
| Free | select field | — | — | — | — | — | — |
| Percentage discount | select field | — | — | — | — | — | — |
| Fixed discount | select field | — | — | — | — | — | — |
| Fixed reward price | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `setBuyGetBogo`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The buy get bogo configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the buy get bogo untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No buy get bogo configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setBuyGetBogo` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-169` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-169`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 2: Works in Buy X Get Y / BOGO Rule Builder → Configure the fundamental qualifier → reward relationship.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-169?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-170` Multi-Buy & Quantity Offer Configurator

**Configure advanced quantity relationships that go beyond simple BOGO.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrator shall configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/multi-buy-quantity-offer-configurator-adm-170` |

**Known gaps.** **Multi-Buy & Quantity Offer Configurator declares no operation that writes anything** — its only declared call is `listMultiBuyQuantity`, a read. The name promises authoring and the contract offers …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Apply once | select field | — | — | — | — | — | — |
| Repeat automatically | select field | — | — | — | — | — | — |
| Maximum repetitions | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listMultiBuyQuantity` (onLoad, Multi-Buy & Quantity Offer Configurator)

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `listMultiBuyQuantity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The multi-buy quantity offer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the multi-buy quantity offer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No multi-buy quantity offer configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listMultiBuyQuantity` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-170` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-170`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 4: Works in Multi-Buy & Quantity Offer Configurator → Configure advanced quantity relationships that go beyond simple BOGO.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-170?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-171` Cheapest / Lowest-Value Item Promotion

**Configure offers where TICVAI dynamically identifies the lowest-priced qualifying item. The matrix explicitly requires “buy multiple products and get cheapest item free” and adding cheaper qualifying items within the same transaction.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/cheapest-lowest-value-item-promotion-adm-171` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Eligible products | select field | — | — | — | — | — | — |
| Eligible categories | select field | — | — | — | — | — | — |
| Minimum quantity | select field | — | — | — | — | — | — |
| Number of free items | text field | — | — | — | — | — | — |
| Cheapest/lowest-priced selection | select field | — | — | — | — | — | — |
| Maximum free-item value | select field | — | — | — | — | — | — |
| Maximum repetitions | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Cheapest item free (primary button) | navigation or local | — | — | — | — |
| Cheapest item 50% off (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCheapestLowestValue` (onLoad, Cheapest / Lowest-Value Item Promotion)

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `listCheapestLowestValue`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cheapest lowest-value item configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cheapest lowest-value item untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cheapest lowest-value item configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCheapestLowestValue` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Price Book supports date-based pricing (regular this month, promotional next month). Promotion Builder supports rules such as "buy X get Y", "buy 2 get 1 free" and "buy 3, lowest-priced item discounted" (fully or partially). *(client request · MoM 19 Aug 2026, 4.2 Product Catalog; 4.3 Pricing, Bundles & Promotions · DI-357)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-171` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-171`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 6: Works in Cheapest / Lowest-Value Item Promotion → Configure offers where TICVAI dynamically identifies the lowest-priced qualifying item. The matrix explicitly requires “buy multiple products and get cheapest item free” and adding cheaper qualifying …

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-171?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Cheapest item free, Cheapest item 50% off.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-172` Fixed-Price & “N for X” Offer Builder

**Configure promotions where a qualifying collection of products is sold for a fixed promotional total.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20651 (APP-SETUP-ADM-172) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/fixed-price-n-for-x-offer-builder-adm-172` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Required quantity | select field | — | — | — | — | — | — |
| Required products | select field | — | — | — | — | — | — |
| Product category | select field | — | — | — | — | — | — |
| Mix-and-match allowed | select field | — | — | — | — | — | — |
| Fixed promotional price | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Maximum repetitions | select field | — | — | — | — | — | — |
| Minimum/maximum product values | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `setFixedPriceOffer`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The fixed-price for offer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the fixed-price for offer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No fixed-price for offer configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setFixedPriceOffer` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic strategies: buy 2 get the 3rd free / BOGO, sibling tiers (first child full price, later children reduced), early-bird phases (e.g. 20% off a AED 200 base for the first 200 of 500, then 10% for the next 100, then full; discount and quota per phase), and price steps as capacity sells (e.g. at 50%). *(client request · MoM 1 Sep 2026, 4.7 Dynamic Pricing Strategies · DI-600)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-172` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-172`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 8: Works in Fixed-Price & “N for X” Offer Builder → Configure promotions where a qualifying collection of products is sold for a fixed promotional total.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-172?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-173` Gift, Free Product & Added-Value Offer Builder

**Configure promotions where a purchase generates an additional entitlement rather than simply reducing price. The matrix explicitly provides the example: “Buy for more than 200 AED and get a free pencil.”**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20652 (APP-SETUP-ADM-173) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/gift-free-product-added-value-offer-builder-adm-173` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Do not offer promotion | text field | — | — | — | — | — | — |
| Provide alternative reward | select field | — | — | — | — | — | — |
| Issue voucher | select field | — | — | — | — | — | — |
| Allow later fulfillment | select field | — | — | — | — | — | — |
| Escalate to operator | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `setGiftFreeProduct`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The gift free product configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the gift free product untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No gift free product configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGiftFreeProduct` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-173` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-173`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 10: Works in Gift, Free Product & Added-Value Offer Builder → Configure promotions where a purchase generates an additional entitlement rather than simply reducing price. The matrix explicitly provides the example: “Buy for more than 200 AED and get a free …

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-173?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-174` Cross-Category Promotion Builder

**Create promotions spanning different TICVAI commercial domains.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20653 (APP-SETUP-ADM-174) |
| Who uses it | ticvai staff holding `PRICE_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/cross-category-promotion-builder-adm-174` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `setCrossCategoryPromotion`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-category promotion list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-category promotion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-category promotion yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-category promotion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setCrossCategoryPromotion` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-174` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-174`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 12: Works in Cross-Category Promotion Builder → Create promotions spanning different TICVAI commercial domains.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-174?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-175` Reward Selection, Substitution & Customer Choice

**Control situations where the customer can choose between multiple promotional rewards.**

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
| Route | `/commercial/reward-selection-substitution-customer-choice-adm-175` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listRewardSelectionSubstitution` (onLoad, Reward Selection, Substitution & Customer Choice)

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `listRewardSelectionSubstitution`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reward selection substitution list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reward selection substitution untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reward selection substitution yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reward selection substitution are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRewardSelectionSubstitution` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-175` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-175`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 14: Works in Reward Selection, Substitution & Customer Choice → Control situations where the customer can choose between multiple promotional rewards.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-175?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-176` Advanced Offer Guardrails & Conflict Controls

**Prevent advanced offers from generating unintended financial or operational outcomes. This screen handles offer-specific safeguards; the complete cross-promotion stacking hierarchy remains in Board 8.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Commercial · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Define preliminary behavior; Prevent configurations such as) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/commercial/advanced-offer-guardrails-conflict-controls-adm-176` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Can combine | select field | — | — | — | — | — | — |
| Cannot combine | select field | — | — | — | — | — | — |
| Exclusive | select field | — | — | — | — | — | — |
| Defer to central stacking engine | text field | — | — | — | — | — | — |
| Product A gives Product B free | text field | — | — | — | — | — | — |
| Product B gives Product A free | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listAdvancedOfferGuardrail` (onLoad, Advanced Offer Guardrails & Conflict Controls)

**Where the user goes next**

- → `ADM-168` Advanced Offer Command Center: *Returns to the board's landing screen*; calls `listAdvancedOfferGuardrail`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The advanced offer guardrails configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the advanced offer guardrails untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No advanced offer guardrails configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAdvancedOfferGuardrail` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-176` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-176`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 16: Works in Advanced Offer Guardrails & Conflict Controls → Prevent advanced offers from generating unintended financial or operational outcomes. This screen handles offer-specific safeguards; the complete cross-promotion stacking hierarchy remains in Board 8.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-176?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-168`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-177` Offer Simulation, Basket Trace & AI Optimization

**Test complex promotion mechanics before publication.**

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
| Route | `/commercial/offer-simulation-basket-trace-ai-optimization-adm-177` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Single transaction, Historical transaction replay, Sample customer segment, Forecast simulation, Bulk … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Mode | radio group | — | Single transaction · Historical transaction replay · Sample customer segment · Forecast simulation · Bulk scenario testing | `listOfferBasketTrace` ?mode |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Single transaction (primary button) | navigation or local | — | — | — | — |
| Historical transaction replay (secondary button) | navigation or local | — | — | — | — |
| Sample customer segment (secondary button) | navigation or local | — | — | — | — |
| Forecast simulation (secondary button) | navigation or local | — | — | — | — |
| Bulk scenario testing (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listOfferBasketTrace` (onLoad, Offer Simulation, Basket Trace & AI Optimization)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offer simulation basket list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offer simulation basket untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offer simulation basket yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offer simulation basket are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listOfferBasketTrace` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-177` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS109 Promotions   Bundles Management Board 4.dc.html#adm-177`
- Workshop pack: Promotions___Bundles_Management_Reference.pdf board 4
- Flow F157 *Promotions Bundles Management board 4: Advanced Offer Command Center*, step 18: Works in Offer Simulation, Basket Trace & AI Optimization → Test complex promotion mechanics before publication.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-177?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Single transaction, Historical transaction replay, Sample customer segment, Forecast simulation, Bulk scenario testing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `PRICE_VIEW`.
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
"listAdvancedOffer": {"method":"GET","path":"/advanced-offer","contract":"promotions","summary":"Advanced Offer Command Center","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"buyXGetX","in":"query","required":false},{"name":"buyXGetY","in":"query","required":false},{"name":"buyNGetX","in":"query","required":false},{"name":"buyNGetMultiple","in":"query","required":false},{"name":"cheapestItemFree","in":"query","required":false},{"name":"percentageOffAnotherProduct","in":"query","required":false},{"name":"amountOffAnotherProduct","in":"query","required":false},{"name":"fixedBundlePrice","in":"query","required":false},{"name":"giftWithPurchase","in":"query","required":false},{"name":"addedValue","in":"query","required":false},{"name":"crossCategoryReward","in":"query","required":false},{"name":"upgradeOffer","in":"query","required":false}],"requestBody":null,"responds":"AdvancedOfferCommandCenterView"},
"listAdvancedOfferGuardrail": {"method":"GET","path":"/advanced-offer-guardrail","contract":"promotions","summary":"Advanced Offer Guardrails & Conflict Controls","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AdvancedOfferGuardrailsConflictControlsView"},
"listCheapestLowestValue": {"method":"GET","path":"/cheapest-lowest-value","contract":"promotions","summary":"Cheapest / Lowest-Value Item Promotion","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CheapestLowestValueItemPromotionView"},
"listMultiBuyQuantity": {"method":"GET","path":"/multi-buy-quantity","contract":"promotions","summary":"Multi-Buy & Quantity Offer Configurator","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MultiBuyQuantityOfferConfiguratorView"},
"listOfferBasketTrace": {"method":"GET","path":"/offer-basket-trace","contract":"promotions","summary":"Offer Simulation, Basket Trace & AI Optimization","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mode","in":"query","required":false}],"requestBody":null,"responds":"OfferSimulationBasketTraceAiOptimizationView"},
"listRewardSelectionSubstitution": {"method":"GET","path":"/reward-selection-substitution","contract":"promotions","summary":"Reward Selection, Substitution & Customer Choice","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"RewardSelectionSubstitutionCustomerChoiceView"},
"setBuyGetBogo": {"method":"PUT","path":"/buy-get-bogo","contract":"promotions","summary":"Buy X Get Y / BOGO Rule Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BuyXGetYBogoRuleBuilderInput","responds":"BuyXGetYBogoRuleBuilderView"},
"setCrossCategoryPromotion": {"method":"PUT","path":"/cross-category-promotion","contract":"promotions","summary":"Cross-Category Promotion Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CrossCategoryPromotionBuilderInput","responds":"CrossCategoryPromotionBuilderView"},
"setFixedPriceOffer": {"method":"PUT","path":"/fixed-price-offer","contract":"promotions","summary":"Fixed-Price & “N for X” Offer Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FixedPriceNForXOfferBuilderInput","responds":"FixedPriceNForXOfferBuilderView"},
"setGiftFreeProduct": {"method":"PUT","path":"/gift-free-product","contract":"promotions","summary":"Gift, Free Product & Added-Value Offer Builder","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GiftFreeProductAddedValueOfferBuilderInput","responds":"GiftFreeProductAddedValueOfferBuilderView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AdvancedOfferCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Advanced Offer Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"activeAdvancedOffers":{"type":"integer","description":"Active Advanced Offers"},"scheduledOffers":{"type":"integer","description":"Scheduled Offers"},"bogoCampaigns":{"type":"integer","description":"BOGO Campaigns"},"giftWithPurchaseOffers":{"type":"integer","description":"Gift-with-Purchase Offers"},"fixedPriceOffers":{"type":"integer","description":"Fixed-Price Offers"},"crossCategoryOffers":{"type":"integer","description":"Cross-Category Offers"},"totalRedemptions":{"type":"integer","description":"Total Redemptions"},"freeItemsIssued":{"type":"string","description":"Free Items Issued"},"discountGranted":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Discount Granted"},"revenueGenerated":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Generated"},"aovUplift":{"type":"number","description":"AOV Uplift"},"marginImpact":{"type":"number","description":"Margin Impact"},"draft":{"type":"string","description":"Draft"},"pendingValidation":{"type":"integer","description":"Pending Validation"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"scheduled":{"type":"string","format":"date-time","description":"Scheduled"},"active":{"type":"integer","description":"Active"},"paused":{"type":"string","description":"Paused"},"suspended":{"type":"string","description":"Suspended"},"expired":{"type":"integer","description":"Expired"},"archived":{"type":"string","description":"Archived"}}},
"AdvancedOfferGuardrailsConflictControlsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Advanced Offer Guardrails & Conflict Controls displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"maximumFreeItems":{"type":"string","description":"Maximum free items"},"maximumRewardValue":{"type":"string","description":"Maximum reward value"},"maximumDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Maximum discount"},"maximumApplicationsPerBasket":{"type":"string","description":"Maximum applications per basket"},"maximumApplicationsPerCustomer":{"type":"string","description":"Maximum applications per customer"},"maximumDailyRedemptions":{"type":"string","description":"Maximum daily redemptions"},"maximumCampaignRedemptions":{"type":"string","description":"Maximum campaign redemptions"},"minimumTransactionValue":{"type":"string","description":"Minimum transaction value"},"minimumMargin":{"type":"number","description":"Minimum margin"},"inventoryRequirement":{"type":"string","description":"Inventory requirement"},"combinationBehavior":{"type":"string","enum":["canCombine","cannotCombine","exclusive","deferToCentralStackingEngine"],"description":"Preliminary combination behaviour; the central stacking engine has the final say."}}},
"BuyXGetYBogoRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is promotions.bundle_component at 7%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Buy X Get Y / BOGO Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"product":{"type":"string","description":"Product"},"productCategory":{"type":"string","description":"Product category"},"ticketType":{"type":"string","description":"Ticket type"},"quantity":{"type":"integer","description":"Quantity"},"minimumSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum spend"},"customerSegment":{"type":"string","description":"Customer segment"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"sameProduct":{"type":"string","description":"Same product"},"differentProduct":{"type":"string","description":"Different product"},"free":{"type":"string","description":"Free"},"percentageDiscount":{"type":"number","description":"Percentage discount"},"fixedDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed discount"},"fixedRewardPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed reward price"}}},
"BuyXGetYBogoRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Buy X Get Y / BOGO Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Product"},"productCategory":{"type":"string","description":"Product category"},"ticketType":{"type":"string","description":"Ticket type"},"quantity":{"type":"integer","description":"Quantity"},"minimumSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Minimum spend"},"customerSegment":{"type":"string","description":"Customer segment"},"channel":{"type":"string","description":"Channel"},"venue":{"type":"string","description":"Venue"},"dateTime":{"type":"string","format":"date-time","description":"Date/time"},"sameProduct":{"type":"string","description":"Same product"},"differentProduct":{"type":"string","description":"Different product"},"free":{"type":"string","description":"Free"},"percentageDiscount":{"type":"number","description":"Percentage discount"},"fixedDiscount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed discount"},"fixedRewardPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed reward price"}}},
"CheapestLowestValueItemPromotionView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Cheapest / Lowest-Value Item Promotion displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"eligibleProducts":{"type":"string","description":"Eligible products"},"eligibleCategories":{"type":"string","description":"Eligible categories"},"minimumQuantity":{"type":"integer","description":"Minimum quantity"},"numberOfFreeItems":{"type":"integer","description":"Number of free items"},"cheapestLowestPricedSelection":{"type":"string","description":"Cheapest/lowest-priced selection"},"maximumFreeItemValue":{"type":"string","description":"Maximum free-item value"},"maximumRepetitions":{"type":"string","description":"Maximum repetitions"},"cheapestItemFree":{"type":"string","description":"Cheapest item free"},"nCheapestItemsFree":{"type":"string","description":"N cheapest items free"}}},
"CrossCategoryPromotionBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Cross-Category Promotion Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"ticketing":{"type":"string","description":"Ticketing"},"attractions":{"type":"string","description":"Attractions"},"events":{"type":"string","description":"Events"},"fB":{"type":"string","description":"F&B"},"retail":{"type":"string","description":"Retail"},"membership":{"type":"string","description":"Membership"},"experiences":{"type":"string","description":"Experiences"},"addOns":{"type":"string","description":"Add-ons"},"parking":{"type":"string","description":"Parking"},"services":{"type":"string","description":"Services"}}},
"CrossCategoryPromotionBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Cross-Category Promotion Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ticketing":{"type":"string","description":"Ticketing"},"attractions":{"type":"string","description":"Attractions"},"events":{"type":"string","description":"Events"},"fB":{"type":"string","description":"F&B"},"retail":{"type":"string","description":"Retail"},"membership":{"type":"string","description":"Membership"},"experiences":{"type":"string","description":"Experiences"},"addOns":{"type":"string","description":"Add-ons"},"parking":{"type":"string","description":"Parking"},"services":{"type":"string","description":"Services"}}},
"FixedPriceNForXOfferBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Fixed-Price & “N for X” Offer Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"requiredQuantity":{"type":"integer","description":"Required quantity"},"requiredProducts":{"type":"string","description":"Required products"},"productCategory":{"type":"string","description":"Product category"},"mixAndMatchAllowed":{"type":"boolean","description":"Mix-and-match allowed"},"fixedPromotionalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed promotional price"},"currency":{"type":"string","description":"Currency"},"maximumRepetitions":{"type":"string","description":"Maximum repetitions"},"minimumMaximumProductValues":{"type":"string","description":"Minimum/maximum product values"}}},
"FixedPriceNForXOfferBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Fixed-Price & “N for X” Offer Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"requiredQuantity":{"type":"integer","description":"Required quantity"},"requiredProducts":{"type":"string","description":"Required products"},"productCategory":{"type":"string","description":"Product category"},"mixAndMatchAllowed":{"type":"boolean","description":"Mix-and-match allowed"},"fixedPromotionalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed promotional price"},"currency":{"type":"string","description":"Currency"},"maximumRepetitions":{"type":"string","description":"Maximum repetitions"},"minimumMaximumProductValues":{"type":"string","description":"Minimum/maximum product values"}}},
"GiftFreeProductAddedValueOfferBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is promotions.bundle_component at 7%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Gift, Free Product & Added-Value Offer Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"basketValue":{"type":"string","description":"Basket value"},"product":{"type":"string","description":"Product"},"quantity":{"type":"integer","description":"Quantity"},"productCategory":{"type":"string","description":"Product category"},"ticket":{"type":"string","description":"Ticket"},"membership":{"type":"string","description":"Membership"},"customerSegment":{"type":"string","description":"Customer segment"},"typesType":{"type":"string","enum":["freeRetailProduct","freeFBProduct","freeTicket","freeAddOn","freeExperience","voucher","upgrade","service","additionalEntitlement"],"description":"Vocabulary listed under Reward Types."},"inventoryAvailability":{"type":"string","description":"Inventory availability"},"locationInventory":{"type":"string","description":"Location inventory"},"eligibleFulfillmentPoint":{"type":"string","description":"Eligible fulfillment point"},"substitutionRules":{"type":"string","description":"Substitution rules"},"doNotOfferPromotion":{"type":"string","description":"Do not offer promotion"},"provideAlternativeReward":{"type":"string","description":"Provide alternative reward"},"allowLaterFulfillment":{"type":"boolean","description":"Allow later fulfillment"}}},
"GiftFreeProductAddedValueOfferBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Gift, Free Product & Added-Value Offer Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"basketValue":{"type":"string","description":"Basket value"},"product":{"type":"string","description":"Product"},"quantity":{"type":"integer","description":"Quantity"},"productCategory":{"type":"string","description":"Product category"},"ticket":{"type":"string","description":"Ticket"},"membership":{"type":"string","description":"Membership"},"customerSegment":{"type":"string","description":"Customer segment"},"typesType":{"type":"string","enum":["freeRetailProduct","freeFBProduct","freeTicket","freeAddOn","freeExperience","voucher","upgrade","service","additionalEntitlement"],"description":"Vocabulary listed under Reward Types."},"inventoryAvailability":{"type":"string","description":"Inventory availability"},"locationInventory":{"type":"string","description":"Location inventory"},"eligibleFulfillmentPoint":{"type":"string","description":"Eligible fulfillment point"},"substitutionRules":{"type":"string","description":"Substitution rules"},"doNotOfferPromotion":{"type":"string","description":"Do not offer promotion"},"provideAlternativeReward":{"type":"string","description":"Provide alternative reward"},"allowLaterFulfillment":{"type":"boolean","description":"Allow later fulfillment"}}},
"MultiBuyQuantityOfferConfiguratorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Multi-Buy & Quantity Offer Configurator displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"minimumQuantity":{"type":"integer","description":"Minimum quantity"},"exactQuantity":{"type":"integer","description":"Exact quantity"},"quantityRange":{"type":"integer","description":"Quantity range"},"multiplesOfX":{"type":"string","description":"Multiples of X"},"oneFree":{"type":"string","description":"One free"},"multipleFree":{"type":"string","description":"Multiple free"},"percentageOff":{"type":"number","description":"Percentage off"},"amountOff":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Amount off"},"fixedTotalPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Fixed total price"},"repeatAutomatically":{"type":"string","description":"Repeat automatically"},"maximumRepetitions":{"type":"string","description":"Maximum repetitions"}}},
"OfferSimulationBasketTraceAiOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Offer Simulation, Basket Trace & AI Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"basketLines":{"type":"array","items":{"type":"string"},"description":"Basket lines evaluated"},"qualifiers":{"type":"array","items":{"type":"string"},"description":"Qualifier conditions met"},"rewards":{"type":"array","items":{"type":"string"},"description":"Rewards granted"},"guardrailsPassed":{"type":"array","items":{"type":"string"},"description":"Guardrails checked and passed"},"originalTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Original total"},"promotionAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Promotion amount"},"finalTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Final total"}}},
"RewardSelectionSubstitutionCustomerChoiceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Reward Selection, Substitution & Customer Choice displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"offerId":{"type":"string","description":"Offer ID"},"rewardOptions":{"type":"array","items":{"type":"string"},"description":"Rewards the guest may choose ONE of"},"selectionModel":{"type":"string","enum":["automatic","customerChoice","operatorChoice","aiRecommended"],"description":"Who picks the reward: the system, the guest from configured options, the POS or call-centre operator, or an AI recommendation"},"substitutes":{"type":"array","items":{"type":"string"},"description":"Ordered substitutes when a reward is unavailable"},"maximumSubstituteValue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Value protection: the most a substitute may be worth"}}}
}
```
