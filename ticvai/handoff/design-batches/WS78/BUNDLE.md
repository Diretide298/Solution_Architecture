# WS78 — Game and Ride board 1

**10 screens · 17 operations · 13 schemas · 5 permissions**

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
  `DEVICE_CONFIGURE, DEVICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, WALLET_CONFIGURE`. A control nobody can use must say so,
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
| `BO-394` | Game & Ride Operations Dashboard | B–D | 0 | 0 | 6 | 1 | 1 | 6 | — | notStarted (—) |
| `BO-395` | Game & Ride Directory | B–D | 7 | 0 | 6 | 1 | 2 | 6 | — | notStarted (—) |
| `BO-396` | Attraction Profile | B–D | 1 | 0 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `BO-397` | Attraction Type Configuration | B–D | 5 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-398` | Game & Ride Operational Configuration | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-399` | Wallet & Credit Acceptance Mapping | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-400` | Attraction / Reader Mapping | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-401` | Game Package & Entitlement Association | B–D | 0 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-402` | Configuration Health & Validation | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-403` | Attraction Audit, Dependencies & Governed Actions | B–D | 11 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-398, BO-399, BO-401 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-394` Game & Ride Operations Dashboard

**Provide management with one central view of the operational and configuration status of all games, rides, skill games, video games and redemption games.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `gameId` (navigation) |
| Route | `/games-rides/game-ride-operations-dashboard-bo-394` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | In service · Out of service · Maintenance · Retired | `listGames` ?status |
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total Attractions** (metric tile)

**Active Attractions** (metric tile)

**Offline / Unavailable** (metric tile)

**Active Readers** (metric tile)

**Reader Faults** (metric tile)

**Transactions Today** (metric tile)

**Wallet Credits Consumed** (metric tile)

**Redemption Credits Earned** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add Attraction (primary button) | navigation or local | — | — | — | — |
| Open Attraction (secondary button) | navigation or local | — | — | — | — |
| Disable Attraction (destructive button) | navigation or local | — | — | — | — |
| View Configuration (secondary button) | navigation or local | — | — | — | — |
| View Reader (secondary button) | navigation or local | — | — | — | — |
| View Transactions (secondary button) | navigation or local | — | — | — | — |
| Filter by venue/zone/type/status (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listGames` (onLoad, Games and rides today); `listGameplayTransactions` (onLoad, Live taps)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-395` Game & Ride Directory: *Game & Ride Directory*; carries `gameId`
- → `BO-396` Attraction Profile: *Attraction Profile*; carries `gameId`
- → `BO-397` Attraction Type Configuration: *Attraction Type Configuration*
- → `BO-398` Game & Ride Operational Configuration: *Game & Ride Operational Configuration*; carries `gameId`
- → `BO-399` Wallet & Credit Acceptance Mapping: *Wallet & Credit Acceptance Mapping*
- → `BO-400` Attraction / Reader Mapping: *Attraction / Reader Mapping*; carries `readerId`
- → `BO-401` Game Package & Entitlement Association: *Game Package & Entitlement Association*
- → `BO-402` Configuration Health & Validation: *Configuration Health & Validation*
- → `BO-403` Attraction Audit, Dependencies & Governed Actions: *Attraction Audit, Dependencies & Governed Actions*

**What opens over it**

- confirmDialog *Disable Attraction*: **Disable Attraction on a game ride operations is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride operations list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride operations are still there. The pack's own statuses are Active — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move … |

#### Permissions

- `listGames` → `PRODUCT_VIEW` (read) · staff
- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff
- `createGame` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateGame` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.7 | Gameplay validation Prices to be defined for each game Assign prices for the Group. Game Reader - Access to the particular game - Bonus deduction should be done first Package - To create a package … | Games & F&B Integration | CONTRACTED | `createGame` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Command centre lists all games/rides with active/offline status. In the reference docs "attractions" means individual games (roller coaster, racing game, bumper cars), not venues. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-863)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-394` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-394`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 1: Opens Game & Ride Operations Dashboard → Provide management with one central view of the operational and configuration status of all games, rides, skill games, video games and redemption games.
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F187 branch at step 1 (expected): when Nothing has been set up on Game & Ride Operations Dashboard yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F187 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-394?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add Attraction, Open Attraction, Disable Attraction, View Configuration, View Reader, View Transactions, Filter by venue/zone/type/status.
- [ ] Every transition is wired: `BO-100`, `BO-395`, `BO-396`, `BO-397`, `BO-398`, `BO-399`, `BO-400`, `BO-401`, `BO-402`, `BO-403`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-395` Game & Ride Directory

**Maintain the master catalogue of all attractions participating in the payment/redemption ecosystem.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Field Description) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `gameId` (navigation) |
| Route | `/games-rides/game-ride-directory-bo-395` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search game ride | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, zone, attraction type, reader type, wallet enabled, redemption enabled and 1 more — which are present is a decision the pack already made. | — |
| Redemption Earn / Spend / N/A | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | In service · Out of service · Maintenance · Retired | `listGames` ?status |

**Sent by *Clone*** (`cloneGame`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64 | — | — | `cloneGame` body |
| Name `name` | text field | required | — | max length 200 | — | — | `cloneGame` body |
| Include readers `includeReaders` | toggle | optional | off | — | — | — | `cloneGame` body |
| Include pricing `includePricing` | toggle | optional | on | — | — | — | `cloneGame` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | navigation or local | — | — | — | — |
| Edit (secondary button) | navigation or local | — | — | — | — |
| Clone (secondary button) | `cloneGame` POST `/games/{gameId}/clone` | inline | Game | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `code` already used by another game in the venue. | — |
| View (secondary button) | navigation or local | — | — | — | — |
| Export (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listGames` (onLoad, The directory)

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move …; 409 `code` already used by another game in the venue. |

#### Permissions

- `listGames` → `PRODUCT_VIEW` (read) · staff
- `createGame` → `PRODUCT_CONFIGURE` (configure) · staff
- `updateGame` → `PRODUCT_CONFIGURE` (configure) · staff
- `cloneGame` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.7 | Gameplay validation Prices to be defined for each game Assign prices for the Group. Game Reader - Access to the particular game - Bonus deduction should be done first Package - To create a package … | Games & F&B Integration | CONTRACTED | `createGame` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*
- Command centre lists all games/rides with active/offline status. In the reference docs "attractions" means individual games (roller coaster, racing game, bumper cars), not venues. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-863)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-395` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-395`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 2: Works in Game & Ride Directory → Maintain the master catalogue of all attractions participating in the payment/redemption ecosystem.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-395?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create, Edit, Clone, View, Export.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-396` Attraction Profile

**Create or maintain the master record for an individual game or ride.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Transaction Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `cardCode` (navigation), `gameId` (navigation) |
| Route | `/games-rides/attraction-profile-bo-396` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Wallet Payment Enabled | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save game (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction profile configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction profile configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Refused. Either `creditCost`, `minPointsAwarded` or `maxPointsAwarded` changed while plays on this game are in flight, or `status` asks for a move … |

#### Permissions

- `getGameCard` → no permission · guest
- `updateGame` → `PRODUCT_CONFIGURE` (configure) · staff
- `createGame` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.3 | The system should provide the ability to view all the credits stored in a digital wallet at multiple kiosks; operator kiosks and self-service kiosks. | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.20 | Check balance - There should be a reader to check the balance for the customer | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.7 | Gameplay validation Prices to be defined for each game Assign prices for the Group. Game Reader - Access to the particular game - Bonus deduction should be done first Package - To create a package … | Games & F&B Integration | CONTRACTED | `createGame` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-396` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-396`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 4: Works in Attraction Profile → Create or maintain the master record for an individual game or ride.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-396?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Save game, Cancel.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-397` Attraction Type Configuration

**Configure reusable categories for games and rides so common rules do not have to be configured separately for every attraction.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration Fields) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/attraction-type-configuration-bo-397` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Type Name | select field | — | — | — | — | — | — |
| Type Code | select field | — | — | — | — | — | — |
| Description | select field | — | — | — | — | — | — |
| Default Reader Type | select field | — | — | — | — | — | — |
| Wallet Allowed | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listAttractionTypes` (onLoad, Types defined)

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction type configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction type untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction type configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAttractionTypes` → `PRODUCT_VIEW` (read) · staff
- `setAttractionType` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-397` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-397`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 6: Works in Attraction Type Configuration → Configure reusable categories for games and rides so common rules do not have to be configured separately for every attraction.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-397?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-398` Game & Ride Operational Configuration

**Configure whether an attraction is currently available for customer transactions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `gameId` (navigation) |
| Route | `/games-rides/game-ride-operational-configuration-bo-398` |

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

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride operational yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGameOperationalConfiguration` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Game directory categorised by type (skill, arcade, etc.); game profile captures description, type and location; reusable attraction-type templates (rides, skill games, video games); a game can be placed in maintenance mode for a defined period. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-864)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-398` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-398`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 8: Works in Game & Ride Operational Configuration → Configure whether an attraction is currently available for customer transactions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-398?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-399` Wallet & Credit Acceptance Mapping

**Define at attraction level which payment/value mechanisms are accepted. The source specifically requires digital-wallet credits to support pay-as-you-go for redemption games, skill games, rides and video games.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `creditTypeId` (navigation) |
| Route | `/games-rides/wallet-credit-acceptance-mapping-bo-399` |

**What the spec says about it.** **Superseded by `BO-1106` Credit Usage & Eligibility Rules** from `Wallet_Configuration_Backend_Structure_v1.0.pdf`, 19 September 2026. This screen came from `Game_and_Ride_Module.pdf`, which describes the wallet incidentally; the wallet pack is the workshop dedicated to it and is backed by the 27 August MoM and matrix 4.3.28-4.3.35. It has zero components, so nothing rendered is lost. Not `source.sameAs` - that means twin, and these are not copies of each other.

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

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet credit acceptance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet credit acceptance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet credit acceptance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet credit acceptance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setCreditEligibilityRules` → `WALLET_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Per game: which credit types are accepted (cash/wallet, bonus, redemption) and a configurable consumption priority (bonus first, then prepaid/cash, then others). *(agreed · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-865)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-399` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-399`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 10: Works in Wallet & Credit Acceptance Mapping → Define at attraction level which payment/value mechanisms are accepted. The source specifically requires digital-wallet credits to support pay-as-you-go for redemption games, skill games, rides and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (412).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-399?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save, Cancel.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `WALLET_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-400` Attraction / Reader Mapping

**Provide a high-level association between games/rides and their reader configurations. Important: This screen only performs the mapping. Detailed reader properties belong to Board 2 – Game Reader & Device Configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE`, `DEVICE_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/attraction-reader-mapping-bo-400` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Video Game Reader (primary button) | navigation or local | — | — | — | — |
| Skill Game Reader (secondary button) | navigation or local | — | — | — | — |
| Ride Reader (secondary button) | navigation or local | — | — | — | — |
| Assign Reader (secondary button) | navigation or local | — | — | — | — |
| Replace Reader (secondary button) | navigation or local | — | — | — | — |
| Remove Assignment (destructive button) | navigation or local | — | — | — | — |
| View Reader Configuration (secondary button) | navigation or local | — | — | — | — |
| Test Mapping (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listReaders` (onLoad, Readers on this attraction)

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

**What opens over it**

- confirmDialog *Remove Assignment*: **Remove Assignment on a attraction reader mapping is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction reader mapping list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction reader mapping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction reader mapping yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the attraction reader mapping are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listReaders` → `DEVICE_VIEW` (read) · staff
- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff
- `testReader` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each game maps to its physical reader; package entitlement sets play-count limits and validity per game; a dependency log records related configuration changes. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-866)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-400` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-400`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 12: Works in Attraction / Reader Mapping → Provide a high-level association between games/rides and their reader configurations. Important: This screen only performs the mapping. Detailed reader properties belong to Board 2 – Game Reader & …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-400?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Video Game Reader, Skill Game Reader, Ride Reader, Assign Reader, Replace Reader, Remove Assignment, View Reader Configuration, Test Mapping.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`, `DEVICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-401` Game Package & Entitlement Association

**Show which packages, tickets and entitlements provide access to each game or ride. The source requires packages containing specific games with configurable entitlement validity, plus products that can allow all games/rides, specific games/rides unlimited times, or specific games/rides a limited number of times.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `PRODUCT_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/game-package-entitlement-association-bo-401` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| View Package (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listGameEntitlements` (onLoad, Packages and entitlements)

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game package entitlement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game package entitlement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game package entitlement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game package entitlement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGameEntitlements` → `PRODUCT_VIEW` (read) · staff
- `createGameEntitlement` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each game maps to its physical reader; package entitlement sets play-count limits and validity per game; a dependency log records related configuration changes. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-866)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-401` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-401`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 14: Works in Game Package & Entitlement Association → Show which packages, tickets and entitlements provide access to each game or ride. The source requires packages containing specific games with configurable entitlement validity, plus products that …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-401?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: View Package, Cancel.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-402` Configuration Health & Validation

**Prevent incomplete or conflicting game/ride configurations from becoming operational.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/configuration-health-validation-bo-402` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Validate Again*** (`validateGameConfiguration`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `validateGameConfiguration` body |
| Games `gameIds` | multi-picker: choose games | optional | — | at most 500 | — | Empty or absent means every game in the venue. | `validateGameConfiguration` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Fix Issue (primary button) | navigation or local | — | — | — | — |
| Open Configuration (secondary button) | navigation or local | — | — | — | — |
| Validate Again (secondary button) | `validateGameConfiguration` POST `/game-configuration-validations` | inline | GameConfigurationHealth | — | — |
| View Dependencies (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The health validation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the health validation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No health validation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the health validation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulateGameplayAuthorisation` → `PRODUCT_CONFIGURE` (configure) · staff
- `validateGameConfiguration` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-402` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-402`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 16: Works in Configuration Health & Validation → Prevent incomplete or conflicting game/ride configurations from becoming operational.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-402?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Fix Issue, Open Configuration, Validate Again, View Dependencies.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-403` Attraction Audit, Dependencies & Governed Actions

**Provide traceability and controlled management of attraction configuration changes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/attraction-audit-dependencies-governed-actions-bo-403` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Attraction created | select field | — | — | — | — | — | — |
| Type changed | select field | — | — | — | — | — | — |
| Reader assigned/replaced | select field | — | — | — | — | — | — |
| Wallet acceptance changed | select field | — | — | — | — | — | — |
| Package association changed | select field | — | — | — | — | — | — |
| Operational status changed | select field | — | — | — | — | — | — |
| Activation/deactivation | select field | — | — | — | — | — | — |
| User | select field | — | — | — | — | — | — |
| Date/time | select field | — | — | — | — | — | — |
| Previous value | select field | — | — | — | — | — | — |
| New value | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

#### Outputs: what the screen shows and produces

**Data it reads**: `listGameplayTransactions` (onLoad, Audit and governed actions)

**Where the user goes next**

- → `BO-394` Game & Ride Operations Dashboard: *Back to Game & Ride Operations Dashboard*; carries `gameId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The attraction audit dependencies configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the attraction audit dependencies untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No attraction audit dependencies configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each game maps to its physical reader; package entitlement sets play-count limits and validity per game; a dependency log records related configuration changes. *(client request · MoM 11 Sep 2026, 4.7 Game & Ride Command Center · DI-866)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-403` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS58 Game and Ride Board 1.dc.html#bo-403`
- Workshop pack: Game_and_Ride_Module.pdf board 1
- Flow F187 *Game and Ride board 1: Game & Ride Operations Dashboard*, step 18: Works in Attraction Audit, Dependencies & Governed Actions → Provide traceability and controlled management of attraction configuration changes.

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-403?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-394`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
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
"cloneGame": {"method":"POST","path":"/games/{gameId}/clone","contract":"games","summary":"Copy a game or ride as a new one","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Game"},
"createGame": {"method":"POST","path":"/games","contract":"games","summary":"Register a game","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Game","responds":"Game"},
"createGameEntitlement": {"method":"POST","path":"/game-entitlements","contract":"games","summary":"Define a pass, package or per-game entitlement","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameEntitlement","responds":"GameEntitlement"},
"getGameCard": {"method":"GET","path":"/game-cards/{cardCode}","contract":"games","summary":"Read a card's balances","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameCard"},
"listAttractionTypes": {"method":"GET","path":"/attraction-types","contract":"games","summary":"The classes of game and ride","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AttractionType"},
"listGameEntitlements": {"method":"GET","path":"/game-entitlements","contract":"games","summary":"Passes, packages and per-game entitlements","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameEntitlement"},
"listGameplayTransactions": {"method":"GET","path":"/gameplay-transactions","contract":"games","summary":"Taps, decisions and what they cost","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"readerId","in":"query","required":null},{"name":"outcome","in":"query","required":null}],"requestBody":null,"responds":"GameplayTransaction"},
"listGames": {"method":"GET","path":"/games","contract":"games","summary":"List games","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Game"},
"listReaders": {"method":"GET","path":"/readers","contract":"games","summary":"Readers, their attractions and their health","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Reader"},
"setAttractionType": {"method":"PUT","path":"/attraction-types","contract":"games","summary":"Define a class of attraction","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AttractionType","responds":"AttractionType"},
"setCreditEligibilityRules": {"method":"PUT","path":"/credit-types/{creditTypeId}/eligibility","contract":"wallet","summary":"Where this credit may be spent, and on what","permission":"WALLET_CONFIGURE","offlineCapable":null,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":"CreditEligibility","responds":"CreditEligibility"},
"setGameOperationalConfiguration": {"method":"PUT","path":"/games/{gameId}/operations","contract":"games","summary":"Capacity, cycle time, restrictions and staffing","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameOperationalConfig","responds":"GameOperationalConfig"},
"setReaderConfiguration": {"method":"PUT","path":"/readers/{readerId}","contract":"games","summary":"What this reader charges, opens, shows and refuses","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Reader","responds":"Reader"},
"simulateGameplayAuthorisation": {"method":"POST","path":"/gameplay-authorisations/simulate","contract":"games","summary":"What would happen if this card tapped this reader","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameplayAuthorisationRequest","responds":"GameplayAuthorisation"},
"testReader": {"method":"POST","path":"/readers/{readerId}/test","contract":"games","summary":"Prove a reader works before a guest finds out it does not","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReaderTestResult"},
"updateGame": {"method":"PATCH","path":"/games/{gameId}","contract":"games","summary":"Amend a game","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Game"},
"validateGameConfiguration": {"method":"POST","path":"/game-configuration-validations","contract":"games","summary":"Re-run the configuration health checks for some or all games","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GameConfigurationHealth"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AttractionType": {"type":"object","x-ticvai-persistence":"games.attraction_type","description":"Board 1.4. **The type decides which settings apply.**","required":["code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"family":{"type":"string","enum":["ride","arcadeGame","redemptionGame","crane","vrExperience","softPlay","attraction","show"]},"hasTicketPayout":{"type":"boolean","default":false},"hasDirectPay":{"type":"boolean","default":false},"hasCycleTime":{"type":"boolean","default":true},"hasHeightRestriction":{"type":"boolean","default":false},"supportsEntitlements":{"type":"boolean","default":true},"scopePath":{"type":"string"}}},
"CreditEligibility": {"type":"object","x-ticvai-persistence":"wallet.credit_eligibility","description":"Board 3.4. **Where credit may be spent** — acceptance, not funding.","properties":{"creditTypeId":{"type":"string","format":"uuid"},"allowedVenueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowedOutletKinds":{"type":"array","items":{"type":"string"}},"allowedProductCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"excludedProductIds":{"type":"array","items":{"type":"string","format":"uuid"}},"allowedChannels":{"type":"array","items":{"type":"string"}},"minimumSpend":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maximumPercentOfBasket":{"type":"number","nullable":true,"description":"**Caps how much of a purchase one credit type may cover.** A venue that lets promotional credit pay for everything has run a free day it did not intend.\n"},"validDaysOfWeek":{"type":"array","items":{"type":"string"}},"scopePath":{"type":"string"}}},
"Game": {"x-ticvai-persistence":"games.game","type":"object","required":["id","code","name","venueId","creditCost","status"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"zone":{"type":"string","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"The machine. Taken out of service by maintenance, the game stops accepting play rather than swallowing credits.\n"},"readerId":{"type":"string","format":"uuid","nullable":true},"creditCost":{"type":"integer","minimum":1},"minPointsAwarded":{"type":"integer"},"maxPointsAwarded":{"type":"integer"},"heightRequirementCm":{"type":"integer","nullable":true},"status":{"$ref":"#/components/schemas/GameStatus"},"playsToday":{"type":"integer"},"creditsTakenToday":{"type":"integer"},"pointsAwardedToday":{"type":"integer"}}},
"GameCard": {"x-ticvai-persistence":"games.card","type":"object","required":["cardCode","venueId","credits","bonusCredits","points","status","issuedAt"],"properties":{"cardCode":{"type":"string","description":"**A pre-printed card keeps the code printed on it. A generated code** (a digital card, or a card issued with no printed code) **is the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Each till holds a reserved range of that sequence, so a card issued offline takes its code at once. Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"credits":{"type":"integer","description":"Bought with money. Buys plays."},"bonusCredits":{"type":"integer","description":"From a promotion. Typically non-refundable and spent before paid credits.\n"},"points":{"type":"integer","description":"Won by playing. Buys prizes. **Not interchangeable with credits** — a guest who wins should not simply be able to play more.\n"},"status":{"type":"string","enum":["active","blocked","expired","transferred"]},"blockedReason":{"type":"string","nullable":true},"transferredToCardCode":{"type":"string","nullable":true},"lastPlayedAt":{"type":"string","format":"date-time","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},
"GameConfigurationHealth": {"x-ticvai-persistence":"none — computed","type":"object","description":"Board 1, p.10. The result of `validateGameConfiguration`; nothing is stored.","required":["venueId","checkedAt","games"],"properties":{"venueId":{"type":"string","format":"uuid"},"checkedAt":{"type":"string","format":"date-time"},"games":{"type":"array","items":{"type":"object","required":["gameId","health"],"properties":{"gameId":{"type":"string","format":"uuid"},"health":{"type":"string","enum":["healthy","warning","blocking"]},"findings":{"type":"array","items":{"type":"object","required":["check","severity"],"properties":{"check":{"type":"string","enum":["priceResolves","readerMapped","readerDeployed","edgePackageCurrent","entitlementCoverage","redemptionRule","assetInService"]},"severity":{"type":"string","enum":["warning","blocking"]},"message":{"type":"string"},"readerId":{"type":"string","format":"uuid","nullable":true},"fixOn":{"type":"string","nullable":true,"description":"The screen that fixes it, e.g. BO-407."}}}}}}}}},
"GameEntitlement": {"type":"object","x-ticvai-persistence":"games.entitlement","description":"Board 4. **A right to play, not money** — consumed before money is.","required":["code","kind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"type":"string","enum":["allGamesPass","unlimitedSingleGame","limitedSingleGame","package","freePlay"]},"gameIds":{"type":"array","items":{"type":"string","format":"uuid"}},"attractionTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"playCount":{"type":"integer","nullable":true,"description":"For `limitedSingleGame` and `package`. Null means unlimited."},"validityKind":{"type":"string","enum":["sameDay","days","untilDate","untilUsed"]},"validityDays":{"type":"integer","nullable":true},"activationKind":{"type":"string","enum":["onPurchase","onFirstUse","onDate"],"default":"onFirstUse","description":"**On first use is what a guest expects from a day pass bought the night before.** On purchase is what a venue defaults to by accident, and it costs them a day.\n"},"dailyPlayCap":{"type":"integer","nullable":true},"cooldownMinutes":{"type":"integer","nullable":true,"description":"**Unlimited does not mean continuous.** A cooldown is how one child does not hold a popular ride all afternoon.\n"},"linkedProductId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"GameOperationalConfig": {"type":"object","x-ticvai-persistence":"games.operational_config","description":"Board 1.5. **Cycle time is the number everything else derives from.**","properties":{"gameId":{"type":"string","format":"uuid"},"cycleSeconds":{"type":"integer","nullable":true},"riderCapacity":{"type":"integer","nullable":true},"throughputPerHour":{"type":"integer","readOnly":true},"minimumHeightCm":{"type":"integer","nullable":true},"maximumHeightCm":{"type":"integer","nullable":true},"minimumAge":{"type":"integer","nullable":true},"supervisionRequiredBelowAge":{"type":"integer","nullable":true},"healthRestrictions":{"type":"array","items":{"type":"string"}},"staffPositions":{"type":"integer","nullable":true},"operatingHours":{"type":"array","nullable":true,"description":"Weekly opening windows, in venue local time, in the same window shape as `GamePricing.peakPricing`. Null means the game follows the venue's hours.\n","items":{"type":"object","required":["daysOfWeek","from","to"],"properties":{"daysOfWeek":{"type":"array","items":{"type":"string"}},"from":{"type":"string","description":"Local time, HH:MM."},"to":{"type":"string","description":"Local time, HH:MM."}}}},"scopePath":{"type":"string"}}},
"GameStatus": {"type":"string","enum":["inService","outOfService","maintenance","retired"]},
"GameplayAuthorisation": {"type":"object","x-ticvai-persistence":"games.authorisation","description":"Board 4.9. **The refusal reason is the product.**","properties":{"id":{"type":"string","format":"uuid"},"decision":{"type":"string","enum":["allow","refuse"]},"reason":{"type":"string","nullable":true,"enum":["ok","cardNotFound","cardExpired","cardBlocked","retapTooSoon","heightRestriction","ageRestriction","insufficientFunds","entitlementExhausted","entitlementNotValidHere","cooldownActive","dailyCapReached","readerNotConfigured","gameUnavailable"]},"guestMessage":{"type":"string","nullable":true,"description":"***\"No plays left on your pass\"* rather than *\"Declined\"*.** One is a guest who understands; the other is a member of staff walking over.\n"},"chargedFrom":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementId":{"type":"string","format":"uuid","nullable":true},"remainingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"remainingPlays":{"type":"integer","nullable":true},"trace":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string"},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"decidedOffline":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"GameplayAuthorisationRequest": {"type":"object","required":["readerId"],"properties":{"readerId":{"type":"string","format":"uuid"},"cardId":{"type":"string","format":"uuid","nullable":true},"credentialIdentifier":{"type":"string","nullable":true},"gameId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time","nullable":true},"guestHeightCm":{"type":"integer","nullable":true},"offline":{"type":"boolean","default":false}}},
"GameplayTransaction": {"type":"object","x-ticvai-persistence":"games.gameplay_transaction","description":"Boards 8.2 and 8.5. **The refused ones are the valuable half.**","properties":{"id":{"type":"string","format":"uuid"},"readerId":{"type":"string","format":"uuid"},"gameId":{"type":"string","format":"uuid","nullable":true},"cardId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["allowed","refused","reversed"]},"reason":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargedFrom":{"type":"string","nullable":true},"entitlementId":{"type":"string","format":"uuid","nullable":true},"ticketsEarned":{"type":"integer","nullable":true},"decidedOffline":{"type":"boolean","default":false},"syncedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"Reader": {"type":"object","x-ticvai-persistence":"games.reader","description":"Board 2. **A `tenancy` device with a game configuration on it.**","required":["deviceId"],"properties":{"deviceId":{"type":"string","format":"uuid","description":"`tenancy.RegisteredDevice`. **Enrolment, firmware and tamper state live there.**\n"},"gameId":{"type":"string","format":"uuid","nullable":true},"readerProfileId":{"type":"string","format":"uuid","nullable":true},"acceptedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"acceptsDirectPay":{"type":"boolean","default":false},"retapDelaySeconds":{"type":"integer","default":3,"description":"**The setting that stops a guest paying twice for one go.** A wristband held against a reader for a second and a half is two taps to the hardware and one intention to the guest.\n"},"displayRules":{"type":"object","properties":{"freeGameGlow":{"type":"boolean","default":true,"description":"**What tells a guest their entitlement was used rather than their money.** Without it the complaint arrives at the desk.\n"},"showBalance":{"type":"boolean","default":true},"showPrice":{"type":"boolean","default":true},"themeCode":{"type":"string","nullable":true},"languages":{"type":"array","items":{"type":"string"}}}},"ioMapping":{"type":"object","additionalProperties":true,"description":"Board 9.6. Which output starts the game, which input reports it finished. **Deliberately open.** The keys are the reader model's own I/O lines, so the shape belongs to the vendor adaptor for that model (game readers are a driver, not a build — ADR-0012, ADR-0015), not to this contract.\n"},"status":{"type":"string","enum":["unconfigured","active","offline","maintenance","disabled"]},"scopePath":{"type":"string"}}},
"ReaderTestResult": {"type":"object","description":"Boards 2.10 and 9.9. **Each check separately**, because they send an engineer to different places.\n","properties":{"readerId":{"type":"string","format":"uuid"},"testedAt":{"type":"string","format":"date-time"},"checks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["connectivity","cardRead","balanceCheck","display","sound","gameTrigger","gameCompleteSignal"]},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"overall":{"type":"string","enum":["pass","partial","fail"]}}}
}
```
