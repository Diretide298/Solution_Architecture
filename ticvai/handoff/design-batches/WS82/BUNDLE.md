# WS82 — Game and Ride board 5

**10 screens · 8 operations · 16 schemas · 4 permissions**

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
| `BO-434` | Game & Ride Pricing Command Center | B–D | 2 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-435` | Standard Game & Ride Price Configuration | B–D | 11 | 0 | 6 | 1 | 1 | 6 | — | notStarted (—) |
| `BO-436` | Group Pricing Configuration | B–D | 12 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-437` | Peak / Non-Peak Dynamic Pricing | B–D | 10 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-438` | Pricing Calendar & Exception Dates | B–D | 8 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-439` | Normal & VIP Pricing Configuration | B–D | 1 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-440` | Retry Price Configuration | B–D | 0 | 2 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `BO-441` | Price Priority & Conflict Rules | A | 20 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-442` | Effective Pricing & Reader Price Preview | B–D | 6 | 10 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-443` | Pricing Audit, Approval & Publication | B–D | 16 | 0 | 6 | 11 | 0 | 3 | — | notStarted (—) |

## Thin screens in this batch

**BO-439, BO-440, BO-441 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-434` Game & Ride Pricing Command Center

**Provide a central view of all game and ride pricing configurations, active pricing rules, upcoming changes, and pricing issues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/game-ride-pricing-command-center-bo-434` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search game ride pricing | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, zone, attraction, attraction type, pricing type, vip enabled and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Game | picker: choose a game | — | — | `getGamePricing` ?gameId |
| Reader | picker: choose a reader | — | — | `getGamePricing` ?readerId |
| At | date and time picker | — | — | `getGamePricing` ?at |
| Guest tier | text field | — | — | `getGamePricing` ?guestTier |

#### Outputs: what the screen shows and produces

**Shown**

**Total Priced Attractions** (metric tile)

**Active Price Rules** (metric tile)

**Peak Pricing Active** (metric tile)

**VIP Pricing Enabled** (metric tile)

**Retry Pricing Enabled** (metric tile)

**Data it reads**: `getGamePricing` (onLoad, Effective prices)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-435` Standard Game & Ride Price Configuration: *Standard Game & Ride Price Configuration*
- → `BO-436` Group Pricing Configuration: *Group Pricing Configuration*
- → `BO-437` Peak / Non-Peak Dynamic Pricing: *Peak / Non-Peak Dynamic Pricing*
- → `BO-438` Pricing Calendar & Exception Dates: *Pricing Calendar & Exception Dates*
- → `BO-439` Normal & VIP Pricing Configuration: *Normal & VIP Pricing Configuration*
- → `BO-440` Retry Price Configuration: *Retry Price Configuration*
- → `BO-441` Price Priority & Conflict Rules: *Price Priority & Conflict Rules*
- → `BO-442` Effective Pricing & Reader Price Preview: *Effective Pricing & Reader Price Preview*
- → `BO-443` Pricing Audit, Approval & Publication: *Pricing Audit, Approval & Publication*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride pricing list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride pricing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride pricing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGamePricing` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-434` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-434`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 1: Opens Game & Ride Pricing Command Center → Provide a central view of all game and ride pricing configurations, active pricing rules, upcoming changes, and pricing issues.
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F191 branch at step 1 (expected): when Nothing has been set up on Game & Ride Pricing Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F191 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-434?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-435`, `BO-436`, `BO-437`, `BO-438`, `BO-439`, `BO-440`, `BO-441`, `BO-442`, `BO-443`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-435` Standard Game & Ride Price Configuration

**Define the normal base price charged to play a specific game or ride. The source requires that prices be defined for each game.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/standard-game-ride-price-configuration-bo-435` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Price Rule Name | select field | — | — | — | — | — | — |
| Attraction | select field | — | — | — | — | — | — |
| Attraction Type | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Zone | select field | — | — | — | — | — | — |
| Standard Price | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Wallet/Credit Equivalent | select field | — | — | — | — | — | — |
| Effective From | select field | — | — | — | — | — | — |
| Effective To | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The standard game ride configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the standard game ride untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No standard game ride configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-435` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-435`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 2: Works in Standard Game & Ride Price Configuration → Define the normal base price charged to play a specific game or ride. The source requires that prices be defined for each game.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-435?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-436` Group Pricing Configuration

**Allow multiple games or rides to share a common pricing rule instead of configuring each attraction individually.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Group Setup; Configuration Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/group-pricing-configuration-bo-436` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Pricing Group Name | select field | — | — | — | — | — | — |
| Group Code | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Attraction Type | select field | — | — | — | — | — | — |
| Price | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Effective Period | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |
| Add Attraction | select field | — | — | — | — | — | — |
| Remove Attraction | select field | — | — | — | — | — | — |
| Apply price to all | text field | — | — | — | — | — | — |
| Individual override allowed: Yes/No | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group pricing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group pricing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-436` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-436`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 4: Works in Group Pricing Configuration → Allow multiple games or rides to share a common pricing rule instead of configuring each attraction individually.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-436?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-437` Peak / Non-Peak Dynamic Pricing

**Configure different game/ride prices based on date and time. The source explicitly requires peak/non-peak pricing for games/rides based on specific date/time.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Rule Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/peak-non-peak-dynamic-pricing-bo-437` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Rule Name | select field | — | — | — | — | — | — |
| Attraction / Group | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Days of Week | select field | — | — | — | — | — | — |
| Specific Date | select field | — | — | — | — | — | — |
| Start Time | select field | — | — | — | — | — | — |
| End Time | select field | — | — | — | — | — | — |
| Peak Price | select field | — | — | — | — | — | — |
| Non-Peak Price | select field | — | — | — | — | — | — |
| Effective From / To | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The peak non-peak dynamic configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the peak non-peak dynamic untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No peak non-peak dynamic configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-437` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-437`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 6: Works in Peak / Non-Peak Dynamic Pricing → Configure different game/ride prices based on date and time. The source explicitly requires peak/non-peak pricing for games/rides based on specific date/time.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-437?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-438` Pricing Calendar & Exception Dates

**Provide a visual calendar for understanding and overriding time-based pricing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Exception Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/pricing-calendar-exception-dates-bo-438` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Date | select field | — | — | — | — | — | — |
| Attraction / Group | select field | — | — | — | — | — | — |
| Pricing Type | select field | — | — | — | — | — | — |
| Price | select field | — | — | — | — | — | — |
| Start Time | select field | — | — | — | — | — | — |
| End Time | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing calendar exception configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing calendar exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing calendar exception configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-438` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-438`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 8: Works in Pricing Calendar & Exception Dates → Provide a visual calendar for understanding and overriding time-based pricing.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-438?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-439` Normal & VIP Pricing Configuration

**Configure different prices for Normal and VIP guests for the same game/ride and reader. The source explicitly requires one reader to show both Normal Price and VIP Price for a specific game, with VIP eligibility obtained through purchase of a VIP product.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/normal-vip-pricing-configuration-bo-439` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Attraction: VR Racing | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save game pricing (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The normal vip pricing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the normal vip pricing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No normal vip pricing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game pricing by customer profile (regular vs VIP), date range and peak/off-peak (weekday/weekend, time-of-day), with exception dates excluding certain pricing (e.g. New Year's Eve). *(client request · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-876)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-439` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-439`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 10: Works in Normal & VIP Pricing Configuration → Configure different prices for Normal and VIP guests for the same game/ride and reader. The source explicitly requires one reader to show both Normal Price and VIP Price for a specific game, with VIP …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-439?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save game pricing, Cancel.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-440` Retry Price Configuration

**Configure a discounted repeat-play price for applicable skill games. Requirement 10.2.16 describes a skill game where, before the game ends, the guest is offered: “Do you want to continue?” A subsequent RFID tap should deduct a lower amount than the original price.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Guest taps card) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/retry-price-configuration-bo-440` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every retry price** (data table)

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**The selected retry price** (detail panel): The pack groups this record's detail under its own headings: “Basketball Challenge”, “Runtime Flow”, “Game approaching completion”, “Reader displays”, “RETRY AED 10”, “AED 10 deducted”.

| Shows | Format | Notes |
|---|---|---|
| ↓ | text | not in the schema: `↓` |

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The retry price list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the retry price untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No retry price yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the retry price are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGamePricing` → `PRICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.15 | Dynamic pricing for games - System should provide an ability to set up peak / nonpeak pricing for all the games / rides based on specific date / time | Games & F&B Integration | CONTRACTED | `setGamePricing` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retry pricing: after a game the reader prompts a time-limited discounted price to replay immediately (e.g. a game normally 25 offered at a reduced rate), within a configurable window. *(agreed · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-877)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-440` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-440`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 12: Works in Retry Price Configuration → Configure a discounted repeat-play price for applicable skill games. Requirement 10.2.16 describes a skill game where, before the game ends, the guest is offered: “Do you want to continue?” A …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-440?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-441` Price Priority & Conflict Rules

**Define which pricing rule wins when several valid prices apply simultaneously. This is required to make the source pricing models operational because Standard, Group, Peak, VIP and Retry prices can overlap.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | Block A · ticket #20659 (APP-SETUP-BO-441) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/price-priority-conflict-rules-bo-441` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Case type | select | — | Low demand · High demand · Near sell out · Early bird · Last minute · Weekend peak · Member purchase · B2B contract · Custom | `listRulePriorityConflict` ?caseType |
| Conflict code | select | — | Contradictory rules · Same priority · Impossible condition · Overlapping strategy · Circular dependency · Missing fallback · Guardrail conflict | `listRulePriorityConflict` ?conflictCode |
| Strategy | text field | — | — | `listRulePriorityConflict` ?strategyId |

**Sent by *Reorder / Validate / Test / Save*** (`setRulePriorityConflict`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Ordered rules `orderedRuleIds` | list of values (chips) | optional | — | — | — | The rules in priority order, highest first. Reorder is this list. | `setRulePriorityConflict` body |
| Resolution method `resolutionMethod` | select | optional | Highest priority wins | Highest priority wins · Most specific rule wins · Cumulative adjustment · Maximum adjustment wins · Minimum adjustment wins · Weighted combination · Stop processing · Custom governed resolution | — | How two applicable rules are resolved; the same vocabulary as `RulePriorityConflictResolutionDynamicPricingTestConsSummary.resolutionMethod`. | `setRulePriorityConflict` body |
| Priority hierarchy `priorityHierarchy` | multi-select chips | optional | — | Commercial protection · Contract member protection · Event specific strategy · Inventory occupancy · Booking velocity · Time to event · Season day timeslot · Base price | — | The priority matrix, highest first; defaults to the pack's order. | `setRulePriorityConflict` body |
| Mode `mode` | segmented control | required | — | Save · Validate · Test | — | `validate` checks the order and returns conflicts without saving; `test` runs `testScenario` against the order and saves it as a test case; `save` stores the order and method … | `setRulePriorityConflict` body |
| Test scenario `testScenario` | group | optional | — | — | — | A sample booking for the conflict test console (pack p.90), the same inputs as a saved test case. | `setRulePriorityConflict` body |
| Case name `testScenario.caseName` | text field | optional | — | max length 120 | — | — | `setRulePriorityConflict` body |
| Case type `testScenario.caseType` | select | optional | — | Low demand · High demand · Near sell out · Early bird · Last minute · Weekend peak · Member purchase · B2B contract · Custom | — | — | `setRulePriorityConflict` body |
| Product `testScenario.productId` | picker: choose a product | optional | — | — | shows names, sends the id | — | `setRulePriorityConflict` body |
| Event `testScenario.eventId` | picker: choose an event | optional | — | — | shows names, sends the id | — | `setRulePriorityConflict` body |
| Performance `testScenario.performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `setRulePriorityConflict` body |
| Date `testScenario.date` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setRulePriorityConflict` body |
| Timeslot `testScenario.timeslot` | text field | optional | — | — | — | — | `setRulePriorityConflict` body |
| Channel `testScenario.channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Where a sale came from. Restored 24 August — this was lost in the `Money` rewrite and nine references across four contracts were pointing at nothing. | `setRulePriorityConflict` body |
| Customer segment `testScenario.customerSegment` | text field | optional | — | — | — | — | `setRulePriorityConflict` body |
| Base price `testScenario.basePrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setRulePriorityConflict` body |
| Occupancy `testScenario.occupancy` | stepper or slider | optional | — | min 0; max 100 | — | — | `setRulePriorityConflict` body |
| Inventory `testScenario.inventory` | number field | optional | — | min 0 | — | — | `setRulePriorityConflict` body |
| Booking velocity `testScenario.bookingVelocity` | number field | optional | — | — | — | — | `setRulePriorityConflict` body |
| Time to event `testScenario.timeToEvent` | number field | optional | — | min 0 | — | — | `setRulePriorityConflict` body |
| Expected price `testScenario.expectedPrice` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setRulePriorityConflict` body |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Reorder / Validate / Test / Save (primary button) | `setRulePriorityConflict` PUT `/rule-priority-conflict` | RulePriorityConflictInput | RulePriorityConflictView | 409 `save` while a critical conflict is open (`criticalConflictOpen`); the conflicts are named in the problem.; 422 `test` without a `testScenario` (`testScenarioRequired`), or `orderedRuleIds` naming a rule that does … | — |

**Data it reads**: `listRulePriorityConflict` (onLoad, Rule Priority, Conflict Resolution & Dynamic Pricing Test …)

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The price priority conflict list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the price priority conflict untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No price priority conflict yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the price priority conflict are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 `save` while a critical conflict is open (`criticalConflictOpen`); the conflicts are named in the problem.; 422 `test` without a `testScenario` (`testScenarioRequired`), or `orderedRuleIds` naming a rule that does not exist or is archived (`unknownRule`). |

#### Permissions

- `listRulePriorityConflict` → `PRODUCT_VIEW` (read) · staff
- `setRulePriorityConflict` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-441` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-441`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 14: Works in Price Priority & Conflict Rules → Define which pricing rule wins when several valid prices apply simultaneously. This is required to make the source pricing models operational because Standard, Group, Peak, VIP and Retry prices can …

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-441?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Reorder / Validate / Test / Save.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-442` Effective Pricing & Reader Price Preview

**Allow an administrator to preview what price will actually be presented/applied for a selected game before publishing configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/effective-pricing-reader-price-preview-bo-442` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Game or attraction | select field | — | — | — | — | Sends `?gameId=` (required). | — |
| Reader | select field | — | — | — | — | Sends `?readerId=`; the preview shows what this reader will display. | — |
| Date and time | date picker | — | — | — | — | Sends `?at=`; covers the pack's Date and Time inputs. | — |
| Customer type / VIP status | select field | — | — | — | — | Sends `?guestTier=`. | — |
| Retry status | select field | — | — | — | — | A pack simulation input with no query parameter. | — |
| Package / entitlement | select field | — | — | — | — | A pack simulation input with no query parameter. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Game | picker: choose a game | — | — | `getGamePricing` ?gameId |
| Reader | picker: choose a reader | — | — | `getGamePricing` ?readerId |
| At | date and time picker | — | — | `getGamePricing` ?at |
| Guest tier | text field | — | — | `getGamePricing` ?guestTier |

#### Outputs: what the screen shows and produces

**Shown**

**Final price** (metric tile, from `getGamePricing`)

| Shows | Format | Notes |
|---|---|---|
| Effective price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Applied rule** (metric tile, from `getGamePricing`)

| Shows | Format | Notes |
|---|---|---|
| Applied rule | text | — |

**Rule evaluation** (data table, from `getGamePricing`): Every candidate rule in evaluation order, the winner marked; matches the pack's Standard / Peak / VIP walk-through.

| Shows | Format | Notes |
|---|---|---|
| Rule | text | — |
| Applied | yes / no (icon or chip) | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Skipped because | text | — |

**Reader preview** (detail panel, from `getGamePricing`): The pack's reader mockup ("SKY COASTER / Normal AED 45 / VIP AED 30 / TAP TO PLAY"). The normal price can be read from the trace's untiered rule, but no field names it.

| Shows | Format | Notes |
|---|---|---|
| Game | the name it points at, never the id | — |
| Effective price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Normal price on reader | text | not in the schema: `Normal price on reader` |
| Reader display text | text | not in the schema: `Reader display text` |

**Data it reads**: `getGamePricing` (onLoad, What the reader will charge)

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The effective pricing reader list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the effective pricing reader untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No effective pricing reader yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the effective pricing reader are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGamePricing` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Retry pricing: after a game the reader prompts a time-limited discounted price to replay immediately (e.g. a game normally 25 offered at a reduced rate), within a configurable window. *(agreed · MoM 11 Sep 2026, 4.11 Game Pricing Management & Retry Pricing · DI-877)*
- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-442` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-442`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 16: Works in Effective Pricing & Reader Price Preview → Allow an administrator to preview what price will actually be presented/applied for a selected game before publishing configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state.
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-442?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-443` Pricing Audit, Approval & Publication

**Govern pricing changes and maintain a full historical record.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (2 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `ruleId` (navigation) |
| Route | `/games-rides/pricing-audit-approval-publication-bo-443` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Venue | text field | — | — | `listPricing` ?venue |
| Urgency | radio group | — | Low · Medium · High · Critical | `listPricing` ?urgency |
| Risk | segmented control | — | Low · Medium · High | `listPricing` ?risk |
| Min confidence | number field | — | — | `listPricing` ?minConfidence |

**Sent by *What publishing changes*** (`publishPricingEffectiveDate`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Version `version` | text field | optional | — | — | — | Approved pricing version to publish | `publishPricingEffectiveDate` body |
| Publication date `publicationDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Publish configuration at (empty for immediate) | `publishPricingEffectiveDate` body |
| Effective date `effectiveDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sales effective from; must not be in the past (never retroactive) | `publishPricingEffectiveDate` body |
| Expiry date `expiryDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Expiry; empty for open-ended | `publishPricingEffectiveDate` body |
| Venue `venue` | text field | optional | — | — | — | Scope: venue; empty for all venues in the version | `publishPricingEffectiveDate` body |
| Market `market` | text field | optional | — | — | — | Scope: market; empty for all | `publishPricingEffectiveDate` body |
| Channel `channel` | select | optional | — | POS · Kiosk · Guest app · Guest web · Call centre · Partner · API · Back office · B2B · Ota | — | Scope: channel; empty for all | `publishPricingEffectiveDate` body |
| Change request `changeRequestId` | text field | optional | — | — | — | Change request being published | `publishPricingEffectiveDate` body |
| Publication mode `publicationMode` | radio group | optional | — | Immediate · Scheduled · Future effective date · Staged | — | Publication Mode (pack p.66) | `publishPricingEffectiveDate` body |
| Visit effective from `visitEffectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Visit dates from which the new prices apply, when different from the sales effective date | `publishPricingEffectiveDate` body |
| Stages `stages` | repeatable rows | optional | — | — | — | Stages for staged publication (market-by-market, venue-by-venue, channel-by-channel) | `publishPricingEffectiveDate` body |
| Dimension `stages[].dimension` | segmented control | optional | — | Market · Venue · Channel | — | Staged by | `publishPricingEffectiveDate` body |
| Target `stages[].target` | text field | optional | — | — | — | Market, venue or channel ID | `publishPricingEffectiveDate` body |
| Publication date `stages[].publicationDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Publish at | `publishPricingEffectiveDate` body |
| Effective date `stages[].effectiveDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Effective from | `publishPricingEffectiveDate` body |
| Cancel `cancel` | toggle | optional | — | — | — | True cancels this scheduled publication; allowed only before activation | `publishPricingEffectiveDate` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish Now (primary button) | navigation or local | — | — | — | — |
| Schedule Publication (secondary button) | navigation or local | — | — | — | — |
| Deactivate Rule (destructive button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | `publishPricingEffectiveDate` PUT `/pricing-effective-date` | PricingPublicationEffectiveDateSchedulerInput | PricingPublicationEffectiveDateSchedulerView | — | — |

**Data it reads**: `listPricing` (onLoad, AI Pricing Intelligence Command Center); `listDynamicPriceRules` (onLoad, The dynamic price rules reviewed and published here)

**Where the user goes next**

- → `BO-434` Game & Ride Pricing Command Center: *Back to Game & Ride Pricing Command Center*

**What opens over it**

- confirmDialog *Deactivate Rule*: **Deactivate Rule on a pricing audit approval is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing audit approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing audit approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing audit approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing audit approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPricing` → `PRODUCT_VIEW` (read) · staff
- `publishPricingEffectiveDate` → `PRODUCT_CONFIGURE` (configure) · staff
- `setDynamicPriceRule` → `PRICE_CONFIGURE` (configure) · staff
- `listDynamicPriceRules` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.17 | - Dynamic Pricing | Ticketing Sales | CONTRACTED | `setDynamicPriceRule` |
| 2.9.10 | The system should have the ability to setup dynamic pricing rules of onsite and digital tickets based on seasonality, day of the week, guest type, time of day, capacity and group size. | Ticketing Sales | CONTRACTED | `setDynamicPriceRule` |
| 2.13.39 | Dynamic Pricing Support | Ticketing Sales | CONTRACTED | `setDynamicPriceRule` |
| 8.5.5 | System shall support seasonal pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.6 | System shall support event-based pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.7 | System shall support day-of-week pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.8 | System shall support time-slot pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.9 | System shall support customer-segment pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.10 | System shall support channel-based pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 8.5.11 | System shall support location-based pricing. | Unified Operations Dashboard | CONTRACTED | `setDynamicPriceRule` |
| 2.1.23 | POS shall retrieve real-time prices from the Dynamic Pricing Engine based on date, timeslot, demand, capacity, promotions, customer segment, and channel. | Ticketing Sales | CONTRACTED | `listDynamicPriceRules` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-443` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS62 Game and Ride Board 5.dc.html#bo-443`
- Workshop pack: Game_and_Ride_Module.pdf board 5
- Flow F191 *Game and Ride board 5: Game & Ride Pricing Command Center*, step 18: Works in Pricing Audit, Approval & Publication → Govern pricing changes and maintain a full historical record.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-443?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish Now, Schedule Publication, Deactivate Rule, What publishing changes.
- [ ] Every transition is wired: `BO-434`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
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

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getGamePricing": {"method":"GET","path":"/game-pricing","contract":"games","summary":"The effective price at a reader, and why","permission":"PRICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"gameId","in":"query","required":true},{"name":"readerId","in":"query","required":null},{"name":"at","in":"query","required":null},{"name":"guestTier","in":"query","required":null}],"requestBody":null,"responds":"GamePriceResolution"},
"listDynamicPriceRules": {"method":"GET","path":"/pricing/dynamic-rules","contract":"catalogue","summary":"Dynamic pricing rules","permission":"PRICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"PricingDynamicPriceRule"},
"listPricing": {"method":"GET","path":"/pricing","contract":"catalogue","summary":"AI Pricing Intelligence Command Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venue","in":"query","required":false},{"name":"urgency","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"minConfidence","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRulePriorityConflict": {"method":"GET","path":"/rule-priority-conflict","contract":"catalogue","summary":"Rule Priority, Conflict Resolution & Dynamic Pricing Test Console","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"caseType","in":"query","required":false},{"name":"conflictCode","in":"query","required":false},{"name":"strategyId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishPricingEffectiveDate": {"method":"PUT","path":"/pricing-effective-date","contract":"catalogue","summary":"Pricing Publication & Effective-Date Scheduler","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PricingPublicationEffectiveDateSchedulerInput","responds":"PricingPublicationEffectiveDateSchedulerView"},
"setDynamicPriceRule": {"method":"PUT","path":"/pricing/dynamic-rules/{ruleId}","contract":"catalogue","summary":"Replace a rule, its conditions and its actions","permission":"PRICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"ruleId","in":"path","required":true},{"name":null,"in":null,"required":null}],"requestBody":"DynamicPriceRuleDetail","responds":"DynamicPriceRuleDetail"},
"setGamePricing": {"method":"PUT","path":"/game-pricing","contract":"games","summary":"Standard, group, peak, VIP, retry and calendar prices","permission":"PRICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GamePricing","responds":"GamePricing"},
"setRulePriorityConflict": {"method":"PUT","path":"/rule-priority-conflict","contract":"catalogue","summary":"Reorder, validate, test or save the pricing rule priority","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RulePriorityConflictInput","responds":"RulePriorityConflictView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiPricingIntelligenceCommandCenterSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on AI Pricing Intelligence Command Center.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"activeAiRecommendations":{"type":"integer","description":"Active AI Recommendations"},"highPriorityOpportunities":{"type":"integer","description":"High-Priority Opportunities"},"estimatedRevenueOpportunity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated Revenue Opportunity"},"demandSurgesDetected":{"type":"integer","description":"Demand Surges Detected: granules forecast materially above baseline"},"demandRisksDetected":{"type":"integer","description":"Demand Risks Detected: granules forecast materially below baseline"},"externalSignalsActive":{"type":"integer","description":"External Signals Active"},"nearbyEventsDetected":{"type":"integer","description":"Nearby Events Detected within the configured monitoring radius"},"weatherImpacts":{"type":"integer","description":"Weather Impacts"},"competitorMovements":{"type":"integer","description":"Competitor Movements"},"forecastAccuracy":{"type":"number","description":"Forecast Accuracy (100 - MAPE over the last 30 days (decided 29 September, readiness close-out)), percent"},"averageAiConfidence":{"type":"number","description":"Average AI Confidence across active recommendations, percent"},"dataQualityIssues":{"type":"integer","description":"Data Quality Issues"},"aiSummary":{"type":"array","items":{"type":"string"},"description":"AI Summary (pack p.95), e.g. demand forecast 19% above baseline and its drivers. Advisory only: generated narrative never changes a price (decided 29 September, readiness close-out)"}}},
"AiPricingIntelligenceCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What AI Pricing Intelligence Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"productEvent":{"type":"string","description":"Product/Event name the opportunity applies to"},"venue":{"type":"string","description":"Venue name"},"currentPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Current Price"},"recommendedPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Recommended Price"},"adjustment":{"type":"number","description":"Adjustment % from current to recommended price, percent"},"demandForecast":{"type":"integer","description":"Demand Forecast: forecast demand (admissions) for the period"},"revenueOpportunity":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Revenue Opportunity"},"confidence":{"type":"number","description":"AI confidence in the recommendation, 0-100, percent"},"risk":{"type":"string","description":"Risk of acting on the recommendation","enum":["low","medium","high"]},"urgency":{"type":"string","description":"Urgency (time to event and velocity)","enum":["low","medium","high","critical"]},"recommendationId":{"type":"string","description":"Recommendation id; drill-down key into listPricingRecommendationExplainability"},"drivers":{"type":"array","items":{"type":"object","properties":{"signal":{"type":"string","enum":["internalSales","bookingVelocity","occupancy","historicalEvents","nearbyEvent","weather","marketTourism","competitor","priceElasticity","other"],"description":"Signal category behind the driver"},"direction":{"type":"string","enum":["up","down"],"description":"Whether the driver pushes the price up or down"},"explanation":{"type":"string","description":"Business-language evidence, e.g. booking velocity 31% above forecast"}}},"description":"Primary drivers of the recommendation (pack's up/down driver list); explanatory, not literal model weights"}}},
"DynamicPriceRuleDetail": {"type":"object","x-ticvai-persistence":"none — composed from a rule, its conditions and its actions","description":"**A rule is unreadable without both halves.** The conditions say when it fires, the actions say what it does to the price, and `minPrice`/`maxPrice` on the action are the guard rails a reviewer looks for first.\n","required":["rule"],"properties":{"rule":{"$ref":"#/components/schemas/PricingDynamicPriceRule"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/PricingDynamicPriceCondition"}},"actions":{"type":"array","items":{"$ref":"#/components/schemas/PricingDynamicPriceAction"}}}},
"GamePriceResolution": {"type":"object","description":"Board 5.9. **What will this actually charge.**","properties":{"gameId":{"type":"string","format":"uuid"},"effectivePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedRule":{"type":"string"},"trace":{"type":"array","items":{"type":"object","properties":{"rule":{"type":"string"},"applied":{"type":"boolean"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"skippedBecause":{"type":"string","nullable":true}}}}}},
"GamePricing": {"type":"object","x-ticvai-persistence":"games.pricing","description":"Board 5. **Priority is explicit**, because evaluation order is not a decision anybody made.\n`groupPricing`, `peakPricing` and `calendarExceptions` are stored one row per entry in `games.pricing_exception` (`GamePricingException`); the rest of this shape is `games.pricing`.\n","properties":{"gameId":{"type":"string","format":"uuid"},"standardPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"vipPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"groupPricing":{"type":"array","items":{"type":"object","properties":{"minimumPlayers":{"type":"integer"},"pricePerPlayer":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"peakPricing":{"type":"array","items":{"type":"object","properties":{"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string"},"to":{"type":"string"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"calendarExceptions":{"type":"array","items":{"type":"object","properties":{"date":{"type":"string","format":"date"},"price":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"closed":{"type":"boolean","default":false}}}},"retryPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"retryWindowSeconds":{"type":"integer","nullable":true},"priority":{"type":"array","items":{"type":"string","enum":["calendarException","peak","group","vip","retry","standard"]}},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PricingDynamicPriceAction": {"type":"object","x-ticvai-persistence":"pricing.dynamic_price_action","description":"**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price action.","required":["dynamicPriceRuleId","type","value"],"properties":{"id":{"type":"string","format":"uuid"},"dynamicPriceRuleId":{"type":"string","format":"uuid"},"type":{"type":"string","maxLength":30},"value":{"type":"number"},"minPrice":{"type":"number","nullable":true},"maxPrice":{"type":"number","nullable":true}}},
"PricingDynamicPriceCondition": {"type":"object","x-ticvai-persistence":"pricing.dynamic_price_condition","description":"**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price rule condition.","required":["actionId","dynamicPriceRuleId","type","ruleOperator","valueJson","sequenceNo"],"properties":{"actionId":{"type":"string","format":"uuid"},"dynamicPriceRuleId":{"type":"string","format":"uuid"},"type":{"type":"string","maxLength":50},"ruleOperator":{"type":"string","maxLength":20},"valueJson":{"type":"string"},"sequenceNo":{"type":"integer"}}},
"PricingDynamicPriceRule": {"type":"object","x-ticvai-persistence":"pricing.dynamic_price_rule","description":"**Taken from the backend workbook, 20 September.** Configurable dynamic pricing component for dynamic price rule.","required":["pricingRuleCode","name","priority","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"pricingRuleCode":{"type":"string","maxLength":100},"name":{"type":"string","maxLength":200},"productId":{"type":"string","format":"uuid","nullable":true},"priceListId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","nullable":true},"channelId":{"type":"string","format":"uuid","nullable":true},"priority":{"type":"integer"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"dynamicPricingStrategyId":{"type":"string","format":"uuid","nullable":true,"description":"The `catalogue.dynamic_pricing_strategy` a dynamic rule belongs to (29 September, data model DM3). Null for a static pricing rule."},"ruleType":{"type":"string","maxLength":40,"nullable":true,"description":"Static rules: `PricingRuleCommandCenterView.ruleType`; dynamic rules: the builder's `ruleKind`."},"inputMetric":{"type":"string","maxLength":40,"nullable":true},"conditionLogic":{"type":"string","enum":["all","any"],"default":"all"},"cooldownMinutes":{"type":"integer","nullable":true,"minimum":0},"minimumDurationMinutes":{"type":"integer","nullable":true,"minimum":0},"exitThresholdOffset":{"type":"number","nullable":true},"rangeMinPercent":{"type":"number","nullable":true},"rangeMaxPercent":{"type":"number","nullable":true},"isProtected":{"type":"boolean","default":false,"description":"A protected segment or channel: dynamic adjustments never apply."}}},
"PricingPublicationEffectiveDateSchedulerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Pricing Publication & Effective-Date Scheduler submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"version":{"type":"string","description":"Approved pricing version to publish"},"publicationDate":{"type":"string","format":"date-time","description":"Publish configuration at (empty for immediate)","nullable":true},"effectiveDate":{"type":"string","format":"date-time","description":"Sales effective from; must not be in the past (never retroactive)"},"expiryDate":{"type":"string","format":"date-time","description":"Expiry; empty for open-ended","nullable":true},"venue":{"type":"string","description":"Scope: venue; empty for all venues in the version","nullable":true},"market":{"type":"string","description":"Scope: market; empty for all","nullable":true},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"nullable":true,"description":"Scope: channel; empty for all"},"changeRequestId":{"type":"string","description":"Change request being published"},"publicationMode":{"type":"string","enum":["immediate","scheduled","futureEffectiveDate","staged"],"description":"Publication Mode (pack p.66)"},"visitEffectiveFrom":{"type":"string","format":"date","description":"Visit dates from which the new prices apply, when different from the sales effective date","nullable":true},"stages":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["market","venue","channel"],"description":"Staged by"},"target":{"type":"string","description":"Market, venue or channel ID"},"publicationDate":{"type":"string","format":"date-time","description":"Publish at"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective from"}},"description":"One stage"},"description":"Stages for staged publication (market-by-market, venue-by-venue, channel-by-channel)"},"cancel":{"type":"boolean","description":"True cancels this scheduled publication; allowed only before activation"}}},
"PricingPublicationEffectiveDateSchedulerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Pricing Publication & Effective-Date Scheduler displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"publicationDate":{"type":"string","format":"date-time","description":"Publish configuration at (empty for immediate)","nullable":true},"effectiveDate":{"type":"string","format":"date-time","description":"Sales effective from; must not be in the past (never retroactive)"},"expiryDate":{"type":"string","format":"date-time","description":"Expiry; empty for open-ended","nullable":true},"venue":{"type":"string","description":"Scope: venue; empty for all venues in the version","nullable":true},"market":{"type":"string","description":"Scope: market; empty for all","nullable":true},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"nullable":true,"description":"Scope: channel; empty for all"},"version":{"type":"string","description":"Approved pricing version to publish"},"changeRequestId":{"type":"string","description":"Change request being published"},"publicationMode":{"type":"string","enum":["immediate","scheduled","futureEffectiveDate","staged"],"description":"Publication Mode (pack p.66)"},"visitEffectiveFrom":{"type":"string","format":"date","description":"Visit dates from which the new prices apply, when different from the sales effective date","nullable":true},"stages":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string","enum":["market","venue","channel"],"description":"Staged by"},"target":{"type":"string","description":"Market, venue or channel ID"},"publicationDate":{"type":"string","format":"date-time","description":"Publish at"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective from"}},"description":"One stage"},"description":"Stages for staged publication (market-by-market, venue-by-venue, channel-by-channel)"},"cancel":{"type":"boolean","description":"True cancels this scheduled publication; allowed only before activation"},"prePublicationChecks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["approvalComplete","validationPassed","noCriticalConflicts","dependenciesAvailable","channelsReady","effectiveDatesValid"],"description":"Pre-Publication Check (pack p.67)"},"passed":{"type":"boolean","description":"Passed"},"message":{"type":"string","description":"Detail, e.g. the colliding version","nullable":true}},"description":"One check"},"description":"Pre-publication check results"},"collisions":{"type":"array","items":{"type":"string"},"description":"Other versions scheduled to become effective for the same object and date"},"status":{"type":"string","description":"Status: scheduled, blocked, published, cancelled or failed"}}},
"RulePriorityConflictInput": {"type":"object","x-ticvai-persistence":"none — request only; the saved hierarchy and test cases are the rows listRulePriorityConflict reads","description":"What `setRulePriorityConflict` takes (decided 29 September, readiness close-out; VM close-out for BO-441 Reorder, Validate, Test, Save).","required":["mode"],"properties":{"orderedRuleIds":{"type":"array","description":"The rules in priority order, highest first. Reorder is this list.","items":{"type":"string"}},"resolutionMethod":{"type":"string","enum":["highestPriorityWins","mostSpecificRuleWins","cumulativeAdjustment","maximumAdjustmentWins","minimumAdjustmentWins","weightedCombination","stopProcessing","customGovernedResolution"],"default":"highestPriorityWins","description":"How two applicable rules are resolved; the same vocabulary as `RulePriorityConflictResolutionDynamicPricingTestConsSummary.resolutionMethod`. Never lowest-price-wins by default (decided 29 September, readiness close-out)."},"priorityHierarchy":{"type":"array","description":"The priority matrix, highest first; defaults to the pack's order.","items":{"type":"string","enum":["commercialProtection","contractMemberProtection","eventSpecificStrategy","inventoryOccupancy","bookingVelocity","timeToEvent","seasonDayTimeslot","basePrice"]}},"mode":{"type":"string","enum":["save","validate","test"],"description":"`validate` checks the order and returns conflicts without saving; `test` runs `testScenario` against the order and saves it as a test case; `save` stores the order and method, refused with `409` while a critical conflict is open."},"testScenario":{"$ref":"#/components/schemas/RulePriorityTestScenario"}}},
"RulePriorityConflictResolutionDynamicPricingTestConsSummary": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection; the headline tiles over the list, computed at read time for the filters in force","description":"**The headline figures on Rule Priority, Conflict Resolution & Dynamic Pricing Test Console.** The pack's KPI cards, split out of the row (decided 29 September, readiness close-out): a count describes the list, not each item in it.","properties":{"contradictoryRules":{"type":"integer","description":"Open contradictoryRules conflicts detected across active and draft rules"},"samePriority":{"type":"integer","description":"Open samePriority conflicts detected across active and draft rules"},"impossibleCondition":{"type":"integer","description":"Open impossibleCondition conflicts detected across active and draft rules"},"overlappingStrategy":{"type":"integer","description":"Open overlappingStrategy conflicts detected across active and draft rules"},"circularDependency":{"type":"integer","description":"Open circularDependency conflicts detected across active and draft rules"},"missingFallback":{"type":"integer","description":"Open missingFallback conflicts detected across active and draft rules"},"guardrailConflict":{"type":"integer","description":"Open guardrailConflict conflicts detected across active and draft rules"},"resolutionMethod":{"type":"string","enum":["highestPriorityWins","mostSpecificRuleWins","cumulativeAdjustment","maximumAdjustmentWins","minimumAdjustmentWins","weightedCombination","stopProcessing","customGovernedResolution"],"description":"Resolution Method in force (pack p.89); defaults to highestPriorityWins (decided 29 September, readiness close-out)"},"priorityHierarchy":{"type":"array","items":{"type":"string","enum":["commercialProtection","contractMemberProtection","eventSpecificStrategy","inventoryOccupancy","bookingVelocity","timeToEvent","seasonDayTimeslot","basePrice"]},"description":"Priority Matrix, highest first; defaults to the pack's order (decided 29 September, readiness close-out)"}}},
"RulePriorityConflictResolutionDynamicPricingTestConsView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Rule Priority, Conflict Resolution & Dynamic Pricing Test Console displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"product":{"type":"string","description":"Test input: product"},"event":{"type":"string","description":"Test input: event","nullable":true},"performance":{"type":"string","description":"Test input: performance","nullable":true},"date":{"type":"string","format":"date","description":"Test input: visit/event date"},"timeslot":{"type":"string","description":"Test input: timeslot","nullable":true},"channel":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"}],"description":"Test input: channel"},"customerSegment":{"type":"string","description":"Test input: customer segment"},"basePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Test input: base price"},"occupancy":{"type":"number","description":"Test input: occupancy percent"},"inventory":{"type":"integer","description":"Test input: remaining inventory"},"bookingVelocity":{"type":"number","description":"Test input: booking velocity, percent against expected pace"},"timeToEvent":{"type":"integer","description":"Test input: days to event (0 = same day)"},"calculationPath":{"type":"array","items":{"type":"string"},"description":"Explainability: the complete calculation path, one step per line"},"testCaseId":{"type":"string","description":"Test case ID"},"caseName":{"type":"string","description":"Test case name"},"caseType":{"type":"string","enum":["lowDemand","highDemand","nearSellOut","earlyBird","lastMinute","weekendPeak","memberPurchase","b2bContract","custom"],"description":"Test case type (pack p.91)"},"rulesMatched":{"type":"array","items":{"type":"object","properties":{"ruleId":{"type":"string","description":"Rule"},"ruleName":{"type":"string","description":"Rule name"},"priorityLevel":{"type":"string","enum":["commercialProtection","contractMemberProtection","eventSpecificStrategy","inventoryOccupancy","bookingVelocity","timeToEvent","seasonDayTimeslot","basePrice"],"description":"Hierarchy level"},"adjustmentPercent":{"type":"number","description":"Adjustment in percent","nullable":true},"applied":{"type":"boolean","description":"Applied after resolution"}},"description":"One matched rule"},"description":"Rules matched"},"rawCalculatedPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Raw calculated price"},"ladderPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Nearest allowed band"},"guardrailOutcome":{"type":"string","enum":["passed","cappedAtMaximum","raisedToMinimum","protectedRateApplied"],"description":"Guardrail result"},"finalPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Final dynamic price"},"conflicts":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["contradictoryRules","samePriority","impossibleCondition","overlappingStrategy","circularDependency","missingFallback","guardrailConflict"],"description":"Conflict type (pack p.90)"},"message":{"type":"string","description":"Message"},"ruleIds":{"type":"array","items":{"type":"string"},"description":"Rules involved"}},"description":"One conflict"},"description":"Conflicts met while resolving this case"},"lastRunAt":{"type":"string","format":"date-time","description":"Last run"},"passed":{"type":"boolean","description":"Final price matched the expected price saved with the case","nullable":true},"expectedPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Expected final price for regression","nullable":true}}},
"RulePriorityConflictView": {"type":"object","x-ticvai-persistence":"none — projection over the saved priority order and test cases","description":"What `setRulePriorityConflict` returns: the order in force, the conflicts it has and, in `test` mode, the result.","properties":{"mode":{"type":"string","enum":["save","validate","test"]},"saved":{"type":"boolean"},"orderedRuleIds":{"type":"array","items":{"type":"string"}},"resolutionMethod":{"type":"string"},"priorityHierarchy":{"type":"array","items":{"type":"string"}},"conflicts":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["contradictoryRules","samePriority","impossibleCondition","overlappingStrategy","circularDependency","missingFallback","guardrailConflict"]},"severity":{"type":"string","enum":["critical","warning"]},"ruleIds":{"type":"array","items":{"type":"string"}},"message":{"type":"string"}}}},"testResult":{"nullable":true,"allOf":[{"$ref":"#/components/schemas/RulePriorityConflictResolutionDynamicPricingTestConsView"}],"description":"The saved test case with its deterministic result, in `test` mode."},"savedAt":{"type":"string","format":"date-time","nullable":true}}},
"RulePriorityTestScenario": {"type":"object","description":"A sample booking for the conflict test console (pack p.90), the same inputs as a saved test case.","properties":{"caseName":{"type":"string","maxLength":120},"caseType":{"type":"string","enum":["lowDemand","highDemand","nearSellOut","earlyBird","lastMinute","weekendPeak","memberPurchase","b2bContract","custom"]},"productId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"date":{"type":"string","format":"date"},"timeslot":{"type":"string","nullable":true},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"customerSegment":{"type":"string","nullable":true},"basePrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"occupancy":{"type":"number","minimum":0,"maximum":100},"inventory":{"type":"integer","minimum":0},"bookingVelocity":{"type":"number"},"timeToEvent":{"type":"integer","minimum":0},"expectedPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true}}}
}
```
