# WS84 — Game and Ride board 7

**10 screens · 6 operations · 6 schemas · 4 permissions**

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
  `ACCESS_VALIDATE, PRODUCT_CONFIGURE, PRODUCT_VIEW, WALLET_OPERATE`. A control nobody can use must say so,
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
| `BO-454` | Card Lifecycle Command Center | B–D | 2 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-455` | Card / Credential Profile | B–D | 0 | 18 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-456` | Card Expiry Rule Configuration | B–D | 4 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-457` | Last Recharge & Last Activity Tracking | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-458` | Expiry Monitoring & Upcoming Expiration | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-459` | Card Expiry Runtime Validation | B–D | 0 | 2 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-460` | Card Block, Suspend & Reactivation Control | B–D | 0 | 8 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-461` | Card Replacement & Wallet Relinking | B–D | 0 | 4 | 6 | 0 | 2 | 6 | — | notStarted (—) |
| `BO-462` | Customer Balance & Credential Status View | B–D | 0 | 6 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `BO-463` | Card Lifecycle Audit & History | B–D | 0 | 4 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-455, BO-457, BO-458, BO-459, BO-461, BO-462, BO-463 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-454` Card Lifecycle Command Center

**Give operations and management a central view of all active game cards / RFID credentials and their lifecycle status.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `cardCode` (navigation) |
| Route | `/games-rides/card-lifecycle-command-center-bo-454` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search card lifecycle | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by venue, status, expiry period, last activity, last recharge, customer/card — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Total Active Cards** (metric tile)

**Cards Used Today** (metric tile)

**Cards Recharged Today** (metric tile)

**Expiring in 30 Days** (metric tile)

**Expired Cards** (metric tile)

**Blocked Cards** (metric tile)

**Dormant Cards** (metric tile)

**Cards with Wallet Balance** (metric tile)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-455` Card / Credential Profile: *Card / Credential Profile*; carries `cardCode`
- → `BO-456` Card Expiry Rule Configuration: *Card Expiry Rule Configuration*
- → `BO-457` Last Recharge & Last Activity Tracking: *Last Recharge & Last Activity Tracking*; carries `cardCode`
- → `BO-458` Expiry Monitoring & Upcoming Expiration: *Expiry Monitoring & Upcoming Expiration*
- → `BO-459` Card Expiry Runtime Validation: *Card Expiry Runtime Validation*
- → `BO-460` Card Block, Suspend & Reactivation Control: *Card Block, Suspend & Reactivation Control*
- → `BO-461` Card Replacement & Wallet Relinking: *Card Replacement & Wallet Relinking*
- → `BO-462` Customer Balance & Credential Status View: *Customer Balance & Credential Status View*; carries `cardCode`
- → `BO-463` Card Lifecycle Audit & History: *Card Lifecycle Audit & History*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card lifecycle list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card lifecycle untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card lifecycle yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card lifecycle are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGameCard` → no permission · guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.3 | The system should provide the ability to view all the credits stored in a digital wallet at multiple kiosks; operator kiosks and self-service kiosks. | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.20 | Check balance - There should be a reader to check the balance for the customer | Games & F&B Integration | CONTRACTED | `getGameCard` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-454` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-454`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 1: Opens Card Lifecycle Command Center → Give operations and management a central view of all active game cards / RFID credentials and their lifecycle status.
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F193 branch at step 1 (expected): when Nothing has been set up on Card Lifecycle Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F193 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-454?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-455`, `BO-456`, `BO-457`, `BO-458`, `BO-459`, `BO-460`, `BO-461`, `BO-462`, `BO-463`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-455` Card / Credential Profile

**Provide the master backend profile for an individual physical or digital game credential.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card Information) and no metric row |
| Offline | online only |
| Opens with | `cardCode` (navigation) |
| Route | `/games-rides/card-credential-profile-bo-455` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every card credential profile** (data table)

| Shows | Format | Notes |
|---|---|---|
| Card ID | text | not in the schema: `Card ID` |
| RFID UID / credential ID | text | not in the schema: `RFID UID / Credential ID` |
| Card number | text | not in the schema: `Card Number` |
| Customer | text | not in the schema: `Customer` |
| Wallet ID | text | not in the schema: `Wallet ID` |
| Issue date | text | not in the schema: `Issue Date` |
| Issue location | text | not in the schema: `Issue Location` |
| Card type | text | not in the schema: `Card Type` |
| Status | text | not in the schema: `Status` |

**The selected card credential profile** (detail panel): The pack groups this record's detail under its own headings: “Linked Values”, “Page 65 of 105”.

| Shows | Format | Notes |
|---|---|---|
| Card ID | text | not in the schema: `Card ID` |
| RFID UID / credential ID | text | not in the schema: `RFID UID / Credential ID` |
| Card number | text | not in the schema: `Card Number` |
| Customer | text | not in the schema: `Customer` |
| Wallet ID | text | not in the schema: `Wallet ID` |
| Issue date | text | not in the schema: `Issue Date` |
| Issue location | text | not in the schema: `Issue Location` |
| Card type | text | not in the schema: `Card Type` |
| Status | text | not in the schema: `Status` |

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*; carries `cardCode`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card credential profile list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card credential profile untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card credential profile yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card credential profile are still there. The pack's own statuses are Last Recharge — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGameCard` → no permission · guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.3 | The system should provide the ability to view all the credits stored in a digital wallet at multiple kiosks; operator kiosks and self-service kiosks. | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.20 | Check balance - There should be a reader to check the balance for the customer | Games & F&B Integration | CONTRACTED | `getGameCard` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-455` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-455`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 2: Works in Card / Credential Profile → Provide the master backend profile for an individual physical or digital game credential.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-455?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-456` Card Expiry Rule Configuration

**Configure the backend rule that determines when a card expires.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Rule Configuration; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/card-expiry-rule-configuration-bo-456` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Rule Name: Standard Game Card Expiry | text field | — | — | — | — | — | — |
| Last Recharge Date | select field | — | — | — | — | — | — |
| Last Activity Date | select field | — | — | — | — | — | — |
| Latest of Last Recharge or Last Activity | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card expiry rule configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card expiry rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card expiry rule configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGameCardExpiryRules` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-456` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-456`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 4: Works in Card Expiry Rule Configuration → Configure the backend rule that determines when a card expires.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-456?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-457` Last Recharge & Last Activity Tracking

**Maintain the two dates required for lifecycle calculation and show which events update them.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `cardCode` (navigation) |
| Route | `/games-rides/last-recharge-last-activity-tracking-bo-457` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*; carries `cardCode`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The last recharge last list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the last recharge last untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No last recharge last yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the last recharge last are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGameCard` → no permission · guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.3 | The system should provide the ability to view all the credits stored in a digital wallet at multiple kiosks; operator kiosks and self-service kiosks. | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.20 | Check balance - There should be a reader to check the balance for the customer | Games & F&B Integration | CONTRACTED | `getGameCard` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-457` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-457`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 6: Works in Last Recharge & Last Activity Tracking → Maintain the two dates required for lifecycle calculation and show which events update them.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-457?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-458` Expiry Monitoring & Upcoming Expiration

**Identify cards approaching expiry so operators can monitor liability and customer impact.**

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
| Route | `/games-rides/expiry-monitoring-upcoming-expiration-bo-458` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search expiry monitoring upcoming | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by balance > 0, bonus > 0, redemption credits > 0, venue, card type, expiry window — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| View Card / View Wallet / Export (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The expiry monitoring upcoming list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the expiry monitoring upcoming untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No expiry monitoring upcoming yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the expiry monitoring upcoming are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setGameCardExpiryRules` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-458` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-458`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 8: Works in Expiry Monitoring & Upcoming Expiration → Identify cards approaching expiry so operators can monitor liability and customer impact.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-458?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: View Card / View Wallet / Export.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-459` Card Expiry Runtime Validation

**Show how TICVAI automatically handles a card tap when the credential is active or expired.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_VALIDATE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§CARD VALID; CARD EXPIRED) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/card-expiry-runtime-validation-bo-459` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every card expiry runtime** (data table)

| Shows | Format | Notes |
|---|---|---|
| Expires: 08 mar 2027 | text | not in the schema: `Expires: 08 Mar 2027` |

**The selected card expiry runtime** (detail panel): The pack groups this record's detail under its own headings: “Reader Tap”, “Reader sends Credential ID”, “Check Status”, “Check Calculated Expiry”, “Continue to”, “Reason Code”.

| Shows | Format | Notes |
|---|---|---|
| Expires: 08 mar 2027 | text | not in the schema: `Expires: 08 Mar 2027` |

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card expiry runtime list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card expiry runtime untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card expiry runtime yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card expiry runtime are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `authoriseGameplay` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-459` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-459`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 10: Works in Card Expiry Runtime Validation → Show how TICVAI automatically handles a card tap when the credential is active or expired.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (2 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-459?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `ACCESS_VALIDATE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-460` Card Block, Suspend & Reactivation Control

**Allow authorized operators to disable a lost, suspicious or invalid card without affecting the underlying wallet record.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Blocked Card Tap) and no metric row |
| Offline | online only |
| Opens with | `cardId` (navigation) |
| Route | `/games-rides/card-block-suspend-reactivation-control-bo-460` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every card block suspend** (data table)

| Shows | Format | Notes |
|---|---|---|
| → reader sends credential | text | not in the schema: `→ Reader sends credential` |
| → TICVAI recognizes blocked status | text | not in the schema: `→ TICVAI recognizes blocked status` |
| → transaction rejected | text | not in the schema: `→ Transaction rejected` |
| → wallet remains protected | text | not in the schema: `→ Wallet remains protected` |

**The selected card block suspend** (detail panel): The pack groups this record's detail under its own headings: “Block Form”, “Require”.

| Shows | Format | Notes |
|---|---|---|
| → reader sends credential | text | not in the schema: `→ Reader sends credential` |
| → TICVAI recognizes blocked status | text | not in the schema: `→ TICVAI recognizes blocked status` |
| → transaction rejected | text | not in the schema: `→ Transaction rejected` |
| → wallet remains protected | text | not in the schema: `→ Wallet remains protected` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Block (primary button) | navigation or local | — | — | — | — |
| Suspend (destructive button) | navigation or local | — | — | — | — |
| Reactivate (secondary button) | navigation or local | — | — | — | — |
| Replace Card (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*; carries `cardCode`

**What opens over it**

- confirmDialog *Suspend*: **Suspend on a card block suspend is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card block suspend list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card block suspend untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card block suspend yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card block suspend are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is not a legal move from the card's current status. `expired` and `transferred` are terminal (states/game-card.yaml), so nothing reactivates, blocks … |

#### Permissions

- `setGameCardLifecycle` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-460` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-460`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 12: Works in Card Block, Suspend & Reactivation Control → Allow authorized operators to disable a lost, suspicious or invalid card without affecting the underlying wallet record.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-460?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Block, Suspend, Reactivate, Replace Card.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-461` Card Replacement & Wallet Relinking

**Allow a damaged, lost or replaced physical card to be substituted while retaining the customer's wallet and entitlements.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE`, `WALLET_OPERATE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Old Card) and no metric row |
| Offline | online only |
| Opens with | `cardId` (navigation) |
| Route | `/games-rides/card-replacement-wallet-relinking-bo-461` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every card replacement wallet** (data table)

| Shows | Format | Notes |
|---|---|---|
| 4321 | text | not in the schema: `4321` |
| ↓ | text | not in the schema: `↓` |

**The selected card replacement wallet** (detail panel): The pack groups this record's detail under its own headings: “Block Old Credential”, “Issue / Scan New Credential”, “Link Existing Wallet”, “Preserve”, “Page 70 of 105”.

| Shows | Format | Notes |
|---|---|---|
| 4321 | text | not in the schema: `4321` |
| ↓ | text | not in the schema: `↓` |

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*; carries `cardCode`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card replacement wallet list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card replacement wallet untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card replacement wallet yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card replacement wallet are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already bound to another wallet; 409 The action is not a legal move from the card's current status. `expired` and `transferred` are terminal (states/game-card.yaml), so nothing reactivates, blocks … |

#### Permissions

- `setGameCardLifecycle` → `PRODUCT_CONFIGURE` (configure) · staff
- `linkWalletCredential` → `WALLET_OPERATE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Card lifecycle shows each card's balance, validity and expiry rule (fixed date or rolling from last top-up/activity) and last activity, with replace, block and suspend actions. *(client request · MoM 11 Sep 2026, 4.12 Redemption, Ticket-Based Rewards & Card Lifecycle · DI-880)*
- Lost wristband/card: operations identify the guest (phone number or ID), locate the original transaction and transfer the balance to a replacement wristband/card. *(client request · MoM 27 Aug 2026, 4.10 Lost-media recovery · DI-538)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-461` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-461`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 14: Works in Card Replacement & Wallet Relinking → Allow a damaged, lost or replaced physical card to be substituted while retaining the customer's wallet and entitlements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-461?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`, `WALLET_OPERATE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-462` Customer Balance & Credential Status View

**Provide the backend configuration/view that supports balance-check readers, operator kiosks and self-service kiosks. The source requires a dedicated reader for checking customer balance and also requires wallet credits to be viewable at operator and self-service kiosks.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card Information) and no metric row |
| Offline | online only |
| Opens with | `cardCode` (navigation) |
| Route | `/games-rides/customer-balance-credential-status-view-bo-462` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every customer balance credential** (data table)

| Shows | Format | Notes |
|---|---|---|
| Status: active | text | not in the schema: `Status: Active` |
| Card expiry: 08 mar 2027 | text | not in the schema: `Card Expiry: 08 Mar 2027` |
| Bonus expiry: 30 sep 2026 | text | not in the schema: `Bonus Expiry: 30 Sep 2026` |

**The selected customer balance credential** (detail panel): The pack groups this record's detail under its own headings: “Customer View”, “Redemption Credits”, “Free Games”, “Entitlements”.

| Shows | Format | Notes |
|---|---|---|
| Status: active | text | not in the schema: `Status: Active` |
| Card expiry: 08 mar 2027 | text | not in the schema: `Card Expiry: 08 Mar 2027` |
| Bonus expiry: 30 sep 2026 | text | not in the schema: `Bonus Expiry: 30 Sep 2026` |

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*; carries `cardCode`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The customer balance credential list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the customer balance credential untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No customer balance credential yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the customer balance credential are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGameCard` → no permission · guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 10.2.3 | The system should provide the ability to view all the credits stored in a digital wallet at multiple kiosks; operator kiosks and self-service kiosks. | Games & F&B Integration | CONTRACTED | `getGameCard` |
| 10.2.20 | Check balance - There should be a reader to check the balance for the customer | Games & F&B Integration | CONTRACTED | `getGameCard` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-462` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-462`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 16: Works in Customer Balance & Credential Status View → Provide the backend configuration/view that supports balance-check readers, operator kiosks and self-service kiosks. The source requires a dedicated reader for checking customer balance and also …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-462?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-463` Card Lifecycle Audit & History

**Maintain full traceability of card lifecycle changes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card Issued; Card Blocked) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/card-lifecycle-audit-history-bo-463` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every card lifecycle audit** (data table)

| Shows | Format | Notes |
|---|---|---|
| 05 mar 2026 | text | not in the schema: `05 Mar 2026` |
| 18 apr 2026 | text | not in the schema: `18 Apr 2026` |

**The selected card lifecycle audit** (detail panel): The pack groups this record's detail under its own headings: “AED 100 Recharge”, “Game Played”, “Expiry Recalculated”, “Events”, “Page 72 of 105”, “Important architecture for the design”.

| Shows | Format | Notes |
|---|---|---|
| 05 mar 2026 | text | not in the schema: `05 Mar 2026` |
| 18 apr 2026 | text | not in the schema: `18 Apr 2026` |

**Data it reads**: `listGameplayTransactions` (onLoad, Card lifecycle history)

**Where the user goes next**

- → `BO-454` Card Lifecycle Command Center: *Back to Card Lifecycle Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The card lifecycle audit list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the card lifecycle audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No card lifecycle audit yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the card lifecycle audit are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-463` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS64 Game and Ride Board 7.dc.html#bo-463`
- Workshop pack: Game_and_Ride_Module.pdf board 7
- Flow F193 *Game and Ride board 7: Card Lifecycle Command Center*, step 18: Works in Card Lifecycle Audit & History → Maintain full traceability of card lifecycle changes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (4 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-463?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-454`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
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
"authoriseGameplay": {"method":"POST","path":"/gameplay-authorisations","contract":"games","summary":"Decide a tap, now","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameplayAuthorisationRequest","responds":"GameplayAuthorisation"},
"getGameCard": {"method":"GET","path":"/game-cards/{cardCode}","contract":"games","summary":"Read a card's balances","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameCard"},
"linkWalletCredential": {"method":"POST","path":"/wallet-credentials","contract":"wallet","summary":"Bind a wristband, card or device to a wallet","permission":"WALLET_OPERATE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WalletCredential","responds":"WalletCredential"},
"listGameplayTransactions": {"method":"GET","path":"/gameplay-transactions","contract":"games","summary":"Taps, decisions and what they cost","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"readerId","in":"query","required":null},{"name":"outcome","in":"query","required":null}],"requestBody":null,"responds":"GameplayTransaction"},
"setGameCardExpiryRules": {"method":"PUT","path":"/game-card-expiry-rules","contract":"games","summary":"When a card lapses, and what warns the guest first","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameCardExpiryRules","responds":"GameCardExpiryRules"},
"setGameCardLifecycle": {"method":"POST","path":"/game-cards/{cardId}/lifecycle","contract":"games","summary":"Block, suspend, reactivate, replace or expire a card","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GameCard"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"GameCard": {"x-ticvai-persistence":"games.card","type":"object","required":["cardCode","venueId","credits","bonusCredits","points","status","issuedAt"],"properties":{"cardCode":{"type":"string","description":"**A pre-printed card keeps the code printed on it. A generated code** (a digital card, or a card issued with no printed code) **is the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Each till holds a reserved range of that sequence, so a card issued offline takes its code at once. Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"credits":{"type":"integer","description":"Bought with money. Buys plays."},"bonusCredits":{"type":"integer","description":"From a promotion. Typically non-refundable and spent before paid credits.\n"},"points":{"type":"integer","description":"Won by playing. Buys prizes. **Not interchangeable with credits** — a guest who wins should not simply be able to play more.\n"},"status":{"type":"string","enum":["active","blocked","expired","transferred"]},"blockedReason":{"type":"string","nullable":true},"transferredToCardCode":{"type":"string","nullable":true},"lastPlayedAt":{"type":"string","format":"date-time","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},
"GameCardExpiryRules": {"type":"object","x-ticvai-persistence":"games.card_expiry_rules","description":"Boards 7.3 to 7.6. **Measured from last activity, and the warning is part of the rule.**\n","properties":{"basis":{"type":"string","enum":["fromIssue","fromLastActivity","fromLastRecharge"],"default":"fromLastActivity"},"validityMonths":{"type":"integer"},"warnBeforeDays":{"type":"array","items":{"type":"integer"},"description":"**Expiring a balance with no notice is what ends up on social media.**"},"warningChannels":{"type":"array","items":{"type":"string"}},"extendOnRecharge":{"type":"boolean","default":true},"onExpiry":{"type":"string","enum":["forfeit","holdForClaim","transferToBreakage"],"default":"holdForClaim"},"holdForClaimDays":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"GameplayAuthorisation": {"type":"object","x-ticvai-persistence":"games.authorisation","description":"Board 4.9. **The refusal reason is the product.**","properties":{"id":{"type":"string","format":"uuid"},"decision":{"type":"string","enum":["allow","refuse"]},"reason":{"type":"string","nullable":true,"enum":["ok","cardNotFound","cardExpired","cardBlocked","retapTooSoon","heightRestriction","ageRestriction","insufficientFunds","entitlementExhausted","entitlementNotValidHere","cooldownActive","dailyCapReached","readerNotConfigured","gameUnavailable"]},"guestMessage":{"type":"string","nullable":true,"description":"***\"No plays left on your pass\"* rather than *\"Declined\"*.** One is a guest who understands; the other is a member of staff walking over.\n"},"chargedFrom":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementId":{"type":"string","format":"uuid","nullable":true},"remainingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"remainingPlays":{"type":"integer","nullable":true},"trace":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string"},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"decidedOffline":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"GameplayAuthorisationRequest": {"type":"object","required":["readerId"],"properties":{"readerId":{"type":"string","format":"uuid"},"cardId":{"type":"string","format":"uuid","nullable":true},"credentialIdentifier":{"type":"string","nullable":true},"gameId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time","nullable":true},"guestHeightCm":{"type":"integer","nullable":true},"offline":{"type":"boolean","default":false}}},
"GameplayTransaction": {"type":"object","x-ticvai-persistence":"games.gameplay_transaction","description":"Boards 8.2 and 8.5. **The refused ones are the valuable half.**","properties":{"id":{"type":"string","format":"uuid"},"readerId":{"type":"string","format":"uuid"},"gameId":{"type":"string","format":"uuid","nullable":true},"cardId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["allowed","refused","reversed"]},"reason":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargedFrom":{"type":"string","nullable":true},"entitlementId":{"type":"string","format":"uuid","nullable":true},"ticketsEarned":{"type":"integer","nullable":true},"decidedOffline":{"type":"boolean","default":false},"syncedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"WalletCredential": {"type":"object","x-ticvai-persistence":"wallet.credential","description":"Boards 6.4 and 6.5. **A credential is not the wallet** — a lost wristband is relinked, not refunded.\n","required":["walletId","kind","identifier"],"properties":{"id":{"type":"string","format":"uuid"},"walletId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["card","wristband","nfc","rfid","qr","mobileApp","digitalKey"]},"identifier":{"type":"string"},"linkedAt":{"type":"string","format":"date-time"},"unlinkedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","lost","replaced","blocked","expired"]},"replacedByCredentialId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}}
}
```
