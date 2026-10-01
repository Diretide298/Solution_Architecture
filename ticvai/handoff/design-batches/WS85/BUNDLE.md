# WS85 — Game and Ride board 8

**9 screens · 7 operations · 10 schemas · 4 permissions**

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
  `DEVICE_VIEW, PRODUCT_CONFIGURE, PRODUCT_VIEW, WALLET_VIEW`. A control nobody can use must say so,
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
| `BO-464` | Game & Ride Operations Control Center | B–D | 2 | 0 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-465` | Live Gameplay Transaction Monitor | B–D | 0 | 24 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-466` | Reader & Device Health Monitor | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-467` | Tap Validation & Decision Trace | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-468` | Rejected Transaction & Reason Analysis | B–D | 0 | 14 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-469` | Wallet & Deduction Transaction Monitor | B–D | 0 | 0 | 6 | 3 | 0 | 6 | — | notStarted (—) |
| `BO-470` | Entitlement & Free-Play Consumption Monitor | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-471` | Offline, Synchronization & Recovery Monitor | B–D | 1 | 24 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-473` | Operational Analytics & Reconciliation Dashboard | B–D | 0 | 20 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-464, BO-465, BO-466, BO-467, BO-469 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-464` Game & Ride Operations Control Center

**Provide the main real-time operational dashboard for the entire game/ride ecosystem.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/game-ride-operations-control-center-bo-464` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search game ride operations | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by client, venue, zone, attraction type, attraction, reader and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listGameplayTransactions` ?from |
| Reader | picker: choose a reader | — | — | `listGameplayTransactions` ?readerId |
| Outcome | segmented control | — | Allowed · Refused · Reversed | `listGameplayTransactions` ?outcome |

#### Outputs: what the screen shows and produces

**Data it reads**: `listGameplayTransactions` (onLoad, Live operations)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-465` Live Gameplay Transaction Monitor: *Live Gameplay Transaction Monitor*
- → `BO-466` Reader & Device Health Monitor: *Reader & Device Health Monitor*
- → `BO-467` Tap Validation & Decision Trace: *Tap Validation & Decision Trace*
- → `BO-468` Rejected Transaction & Reason Analysis: *Rejected Transaction & Reason Analysis*
- → `BO-469` Wallet & Deduction Transaction Monitor: *Wallet & Deduction Transaction Monitor*
- → `BO-470` Entitlement & Free-Play Consumption Monitor: *Entitlement & Free-Play Consumption Monitor*
- → `BO-471` Offline, Synchronization & Recovery Monitor: *Offline, Synchronization & Recovery Monitor*
- → `BO-141` Operational Alerts, AI Replenishment & Action Center: *Operational Alerts & Exception Center (BO-141, absorbed BO-472, audit R276)*
- → `BO-473` Operational Analytics & Reconciliation Dashboard: *Operational Analytics & Reconciliation Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game ride operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game ride operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game ride operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game ride operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-464` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-464`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 1: Opens Game & Ride Operations Control Center → Provide the main real-time operational dashboard for the entire game/ride ecosystem.
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F194 branch at step 1 (expected): when Nothing has been set up on Game & Ride Operations Control Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F194 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-464?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-465`, `BO-466`, `BO-467`, `BO-468`, `BO-469`, `BO-470`, `BO-471`, `BO-141`, `BO-473`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-465` Live Gameplay Transaction Monitor

**Display gameplay transactions as they occur across all connected readers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Selecting a transaction should show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/live-gameplay-transaction-monitor-bo-465` |

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

**Every live gameplay transaction** (data table)

| Shows | Format | Notes |
|---|---|---|
| Transaction ID | text | not in the schema: `Transaction ID` |
| Card/credential | text | not in the schema: `Card/credential` |
| Wallet | text | not in the schema: `Wallet` |
| Reader | text | not in the schema: `Reader` |
| Attraction | text | not in the schema: `Attraction` |
| Price rule | text | not in the schema: `Price rule` |
| Funding source | text | not in the schema: `Funding source` |
| Before balance | text | not in the schema: `Before balance` |
| Deduction | text | not in the schema: `Deduction` |
| After balance | text | not in the schema: `After balance` |
| Authorization result | text | not in the schema: `Authorization result` |
| Response time | text | not in the schema: `Response time` |

**The selected live gameplay transaction** (detail panel): The pack groups this record's detail under its own headings: “Live Transaction Feed”, “Transaction Sources”, “Live Status”.

| Shows | Format | Notes |
|---|---|---|
| Transaction ID | text | not in the schema: `Transaction ID` |
| Card/credential | text | not in the schema: `Card/credential` |
| Wallet | text | not in the schema: `Wallet` |
| Reader | text | not in the schema: `Reader` |
| Attraction | text | not in the schema: `Attraction` |
| Price rule | text | not in the schema: `Price rule` |
| Funding source | text | not in the schema: `Funding source` |
| Before balance | text | not in the schema: `Before balance` |
| Deduction | text | not in the schema: `Deduction` |
| After balance | text | not in the schema: `After balance` |
| Authorization result | text | not in the schema: `Authorization result` |
| Response time | text | not in the schema: `Response time` |

**Data it reads**: `listGameplayTransactions` (onLoad, Every tap)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live gameplay transaction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live gameplay transaction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live gameplay transaction yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live gameplay transaction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-465` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-465`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 2: Works in Live Gameplay Transaction Monitor → Display gameplay transactions as they occur across all connected readers.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-465?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-466` Reader & Device Health Monitor

**Monitor communication and operational status of the physical Chinese readers and other connected devices.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `deviceId` (session) |
| Route | `/games-rides/reader-device-health-monitor-bo-466` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |
| From | date and time picker | — | — | `getDeviceTelemetry` ?from |
| To | date and time picker | — | — | `getDeviceTelemetry` ?to |
| Metric | text field | — | — | `getDeviceTelemetry` ?metric |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `listReaders` (onLoad, Reader and device health); `getDeviceTelemetry` (onLoad, Telemetry behind it)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader device health list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader device health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader device health yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader device health are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listReaders` → `DEVICE_VIEW` (read) · staff
- `getDeviceTelemetry` → `DEVICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.4.21 | Battery Monitoring - System shall monitor battery levels where applicable. | Device Management | CONTRACTED | `getDeviceTelemetry` |
| 16.4.22 | Device Performance Monitoring - System shall monitor device performance. | Device Management | CONTRACTED | `getDeviceTelemetry` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-466` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-466`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 4: Works in Reader & Device Health Monitor → Monitor communication and operational status of the physical Chinese readers and other connected devices.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-466?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `DEVICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-467` Tap Validation & Decision Trace

**Allow operations to understand exactly how TICVAI reached an approval or rejection decision for an individual customer tap. This relates directly to the requirement that balance, bonus and entitlements be validated in real time before gameplay.**

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
| Route | `/games-rides/tap-validation-decision-trace-bo-467` |

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

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tap validation decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tap validation decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tap validation decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the tap validation decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulateGameplayAuthorisation` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live operations view: taps, rejected plays, wallet value consumed, per-game play counts, reader status and tap-validation logs (which card on which reader, when). *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-881)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-467` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-467`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 6: Works in Tap Validation & Decision Trace → Allow operations to understand exactly how TICVAI reached an approval or rejection decision for an individual customer tap. This relates directly to the requirement that balance, bonus and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-467?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-468` Rejected Transaction & Reason Analysis

**Centralize all rejected gameplay transactions and identify why customers are being denied.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Rejection KPIs) and a per-row directory (§Time Attraction Card Reason Reader; Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/rejected-transaction-reason-analysis-bo-468` |

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

**Rejections Today** (metric tile)

**Rejection Rate** (metric tile)

**Insufficient Balance** (metric tile)

**Invalid/Expired Card** (metric tile)

**Entitlement Failure** (metric tile)

**Retap Protection** (metric tile)

**Reader/Technical Failure** (metric tile)

**Every rejected transaction reason** (data table)

| Shows | Format | Notes |
|---|---|---|
| 10:42 VR racing ****3321 insufficient balance r 014 | text | not in the schema: `10:42 VR Racing ****3321 Insufficient Balance R-014` |
| 10:40 bumper cars ****2178 card expired r 007 | text | not in the schema: `10:40 Bumper Cars ****2178 Card Expired R-007` |
| 10:38 basketball ****6621 retap too soon r 023 | text | not in the schema: `10:38 Basketball ****6621 Retap Too Soon R-023` |
| Rejections by attraction | text | not in the schema: `Rejections by attraction` |
| Rejections by reader | text | not in the schema: `Rejections by reader` |
| Rejections by reason | text | not in the schema: `Rejections by reason` |
| Rejection trend | text | not in the schema: `Rejection trend` |

**The selected rejected transaction reason** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| 10:42 VR racing ****3321 insufficient balance r 014 | text | not in the schema: `10:42 VR Racing ****3321 Insufficient Balance R-014` |
| 10:40 bumper cars ****2178 card expired r 007 | text | not in the schema: `10:40 Bumper Cars ****2178 Card Expired R-007` |
| 10:38 basketball ****6621 retap too soon r 023 | text | not in the schema: `10:38 Basketball ****6621 Retap Too Soon R-023` |
| Rejections by attraction | text | not in the schema: `Rejections by attraction` |
| Rejections by reader | text | not in the schema: `Rejections by reader` |
| Rejections by reason | text | not in the schema: `Rejections by reason` |
| Rejection trend | text | not in the schema: `Rejection trend` |

**Data it reads**: `listGameplayTransactions` (onLoad, Refusals, by reason)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rejected transaction reason list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rejected transaction reason untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rejected transaction reason yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rejected transaction reason are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGameplayTransactions` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-468` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-468`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 8: Works in Rejected Transaction & Reason Analysis → Centralize all rejected gameplay transactions and identify why customers are being denied.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-468?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-469` Wallet & Deduction Transaction Monitor

**Monitor the financial/value movement generated by game and ride activity. The source requires the customer's amount to be deducted after the card tap based on available balance and the remaining balance to be updated.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WALLET_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `subjectId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that … |
| Route | `/games-rides/wallet-deduction-transaction-monitor-bo-469` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The wallet deduction transaction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the wallet deduction transaction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No wallet deduction transaction yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the wallet deduction transaction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listWalletTransactions` → `WALLET_VIEW` (read) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.112 | Transaction history | Ticketing Catalogue | CONTRACTED | `listWalletTransactions` |
| 5.3.17 | Maintain guest wallet balances, top-ups, spending history, refunds, transfers, expirations, and transaction history. | F&B & Guest Management | CONTRACTED | `listWalletTransactions` |
| 22.2.14 | Wallet History | Marketing & CRM | CONTRACTED | `listWalletTransactions` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A88** Design the CRM profile & field architecture (user-defined fields, per-field unique/required flags, either-email-or-mobile rule, group profiles, family/guardian linking with shared wallet) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 20 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A132** Build the entitlement engine (entry counts, time-bound product windows from first scan, combo redemption by QR at each counter, stored-value credit, referral-to-wallet option) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A137** Configure product-level stored value (minimum value, maximum balance, balance expiry, refund destination) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'stored value')*
- **A159** Build the wallet foundation & dashboard (wallet type library by category, provisioning triggers, gift-card-style vs. add-money patterns, live balance/spend/recharge totals) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*
- **A160** Record wallet balances against the chart of accounts (load booked as customer liability, recognised to product revenue on consumption, every wallet transaction mapped to a GL entry) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'wallet')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-469` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-469`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 10: Works in Wallet & Deduction Transaction Monitor → Monitor the financial/value movement generated by game and ride activity. The source requires the customer's amount to be deducted after the card tap based on available balance and the remaining …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-469?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `WALLET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-470` Entitlement & Free-Play Consumption Monitor

**Monitor consumption of packages, passes, limited plays, unlimited entitlements and free-game credits.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/entitlement-free-play-consumption-monitor-bo-470` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Entitlement Plays Today** (metric tile)

**Free Plays** (metric tile)

**Package Plays** (metric tile)

**Unlimited Pass Uses** (metric tile)

**Limited Plays Remaining** (metric tile)

**Failed Entitlement Attempts** (metric tile)

**Data it reads**: `listGameEntitlements` (onLoad, Entitlement consumption)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The entitlement free-play consumption list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the entitlement free-play consumption untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No entitlement free-play consumption yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the entitlement free-play consumption are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGameEntitlements` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-470` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-470`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 12: Works in Entitlement & Free-Play Consumption Monitor → Monitor consumption of packages, passes, limited plays, unlimited entitlements and free-game credits.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-470?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-471` Offline, Synchronization & Recovery Monitor

**Monitor readers or edge components that temporarily lose connectivity with TICVAI and manage recovery/synchronization. This is a TICVAI Recommended Enhancement, based on the architecture we agreed for physical readers.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/offline-synchronization-recovery-monitor-bo-471` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Status | select field | — | — | — | — | Filters the returned readers client-side by `status` (online, offline, degraded, unreachable). The pack's statuses Synchronizing, Synchronized, Conflict and Failed Sync have no value in the enum. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Readers offline** (metric tile, from `getGameplaySyncStatus`): Count of readers whose `status` is offline or unreachable.

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Online, Offline, Degraded, Unreachable | — |

**Pending offline transactions** (metric tile, from `getGameplaySyncStatus`): Summed across readers.

| Shows | Format | Notes |
|---|---|---|
| Pending transactions | 1,234 | — |

**Pending offline value** (metric tile, from `getGameplaySyncStatus`): Summed across readers.

| Shows | Format | Notes |
|---|---|---|
| Pending value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Stale edge packages** (metric tile, from `getGameplaySyncStatus`): Count where `edgePackageStale` is true.

| Shows | Format | Notes |
|---|---|---|
| Edge package stale | yes / no (icon or chip) | — |

**Readers and their sync state** (data table, from `getGameplaySyncStatus`): The pack's device table: Offline Since is `oldestPendingAt`, Config Version is `edgePackageVersion`.

| Shows | Format | Notes |
|---|---|---|
| Reader | the name it points at, never the id | — |
| Reader name | text | — |
| Oldest pending at | 1 Oct 2026, 14:30 | — |
| Pending transactions | 1,234 | — |
| Pending value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Edge package version | 1,234 | — |
| Last sync at | 1 Oct 2026, 14:30 | — |
| Status | chip: Online, Offline, Degraded, Unreachable | — |

**The selected reader** (detail panel, from `getGameplaySyncStatus`): The three offline controls are the pack's; no field or operation carries them.

| Shows | Format | Notes |
|---|---|---|
| Reader | the name it points at, never the id | — |
| Reader name | text | — |
| Status | chip: Online, Offline, Degraded, Unreachable | — |
| Last sync at | 1 Oct 2026, 14:30 | — |
| Oldest pending at | 1 Oct 2026, 14:30 | — |
| Pending transactions | 1,234 | — |
| Pending value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Edge package version | 1,234 | — |
| Edge package stale | yes / no (icon or chip) | — |
| Offline operation allowed | text | not in the schema: `Offline operation allowed` |
| Maximum offline duration | text | not in the schema: `Maximum offline duration` |
| Maximum offline transaction value | text | not in the schema: `Maximum offline transaction value` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Force synchronization (secondary button) | navigation or local | — | — | — | — |
| Block offline operation (destructive button) | navigation or local | — | — | — | — |

**Data it reads**: `getGameplaySyncStatus` (onLoad, What is held offline)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline synchronization recovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline synchronization recovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline synchronization recovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the offline synchronization recovery are still there. The pack's own statuses are Online — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGameplaySyncStatus` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-471` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-471`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 14: Works in Offline, Synchronization & Recovery Monitor → Monitor readers or edge components that temporarily lose connectivity with TICVAI and manage recovery/synchronization. This is a TICVAI Recommended Enhancement, based on the architecture we agreed …

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (24 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-471?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Force synchronization, Block offline operation.
- [ ] Every transition is wired: `BO-464`.
- [ ] Every gated control is gated: `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-473` Operational Analytics & Reconciliation Dashboard

**Provide management and operations with consolidated performance analytics across gameplay, readers, wallets and redemption.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/operational-analytics-reconciliation-dashboard-bo-473` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Total plays** (metric tile): The pack asks for total plays; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Total plays | text | not in the schema: `Total plays` |

**Authorization rate** (metric tile): The pack asks for authorization rate; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Authorization rate | text | not in the schema: `Authorization rate` |

**Rejection rate** (metric tile): The pack asks for rejection rate; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Rejection rate | text | not in the schema: `Rejection rate` |

**Reader uptime** (metric tile): The pack asks for reader uptime; the contract has no field for it.

| Shows | Format | Notes |
|---|---|---|
| Reader uptime | text | not in the schema: `Reader uptime` |

**Offline readers** (metric tile, from `getGameplaySyncStatus`): The one device KPI the bound read supports: count of readers offline or unreachable.

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Online, Offline, Degraded, Unreachable | — |

**Pending offline transactions** (metric tile, from `getGameplaySyncStatus`): Summed across readers; feeds the reconciliation variance.

| Shows | Format | Notes |
|---|---|---|
| Pending transactions | 1,234 | — |

**Plays by attraction and rejection trend** (chart): The pack's analytics set (plays by attraction, revenue by game/ride, peak usage times, rejection trend). No operation returns gameplay aggregates.

| Shows | Format | Notes |
|---|---|---|
| Attraction | text | not in the schema: `Attraction` |
| Plays | text | not in the schema: `Plays` |
| Revenue | text | not in the schema: `Revenue` |
| Rejection rate | text | not in the schema: `Rejection rate` |
| Hour of day | text | not in the schema: `Hour of day` |

**Reconciliation summary** (data table): Clicking the variance drills to missing deduction, missing game-start confirmation, duplicate event or reader communication issue. No operation reconciles these three counts.

| Shows | Format | Notes |
|---|---|---|
| Authorized plays | text | not in the schema: `Authorized plays` |
| Wallet / entitlement transactions | text | not in the schema: `Wallet / entitlement transactions` |
| Confirmed game starts | text | not in the schema: `Confirmed game starts` |
| Variance | text | not in the schema: `Variance` |

**Reader performance** (data table, from `getGameplaySyncStatus`)

| Shows | Format | Notes |
|---|---|---|
| Reader name | text | — |
| Status | chip: Online, Offline, Degraded, Unreachable | — |
| Last sync at | 1 Oct 2026, 14:30 | — |
| Pending transactions | 1,234 | — |
| Edge package version | 1,234 | — |

**Data it reads**: `getGameplaySyncStatus` (onLoad, Reconciliation)

**Where the user goes next**

- → `BO-464` Game & Ride Operations Control Center: *Back to Game & Ride Operations Control Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational analytics reconciliation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational analytics reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational analytics reconciliation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operational analytics reconciliation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getGameplaySyncStatus` → `PRODUCT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Rejected taps logged with reason (no entitlement, insufficient balance, etc.); entitlement-consumption monitor, offline sync/queue monitor, operational alerts; analytics for total games played, unique players, paid vs value-credit usage. *(client request · MoM 11 Sep 2026, 4.13 Live Gameplay Operations Monitoring & Self-Service Kiosk · DI-882)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-473` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS65 Game and Ride Board 8.dc.html#bo-473`
- Workshop pack: Game_and_Ride_Module.pdf board 8
- Flow F194 *Game and Ride board 8: Game & Ride Operations Control Center*, step 18: Works in Operational Analytics & Reconciliation Dashboard → Provide management and operations with consolidated performance analytics across gameplay, readers, wallets and redemption.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-473?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-464`.
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

**8 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getDeviceTelemetry": {"method":"GET","path":"/devices/{deviceId}/telemetry","contract":"tenancy","summary":"Battery, performance and consumables over time","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"metric","in":"query","required":null}],"requestBody":null,"responds":"DeviceTelemetryPoint"},
"getGameplaySyncStatus": {"method":"GET","path":"/gameplay-sync-status","contract":"games","summary":"What readers took offline and have not sent","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReaderSyncStatus"},
"listGameEntitlements": {"method":"GET","path":"/game-entitlements","contract":"games","summary":"Passes, packages and per-game entitlements","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GameEntitlement"},
"listGameplayTransactions": {"method":"GET","path":"/gameplay-transactions","contract":"games","summary":"Taps, decisions and what they cost","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"readerId","in":"query","required":null},{"name":"outcome","in":"query","required":null}],"requestBody":null,"responds":"GameplayTransaction"},
"listReaders": {"method":"GET","path":"/readers","contract":"games","summary":"Readers, their attractions and their health","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Reader"},
"listWalletTransactions": {"method":"GET","path":"/wallets/{subjectId}/transactions","contract":"wallet","summary":"Wallet transaction history","permission":"WALLET_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"simulateGameplayAuthorisation": {"method":"POST","path":"/gameplay-authorisations/simulate","contract":"games","summary":"What would happen if this card tapped this reader","permission":"PRODUCT_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GameplayAuthorisationRequest","responds":"GameplayAuthorisation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"DeviceTelemetryPoint": {"type":"object","x-ticvai-persistence":"tenancy.device_telemetry","description":"16.4.21 and 16.4.22. **A series, because degradation is not visible in a point-in-time reading.**\n","properties":{"deviceId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"batteryPercent":{"type":"integer","nullable":true},"batteryHealthPercent":{"type":"integer","nullable":true},"charging":{"type":"boolean","nullable":true},"signalStrength":{"type":"integer","nullable":true},"cpuPercent":{"type":"number","nullable":true},"memoryPercent":{"type":"number","nullable":true},"storageFreeMb":{"type":"integer","nullable":true},"consumables":{"type":"object","additionalProperties":true,"description":"Paper, ribbon, wristband stock — whatever the device kind reports."},"uptimeSeconds":{"type":"integer","nullable":true},"scopePath":{"type":"string"}}},
"GameEntitlement": {"type":"object","x-ticvai-persistence":"games.entitlement","description":"Board 4. **A right to play, not money** — consumed before money is.","required":["code","kind"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"kind":{"type":"string","enum":["allGamesPass","unlimitedSingleGame","limitedSingleGame","package","freePlay"]},"gameIds":{"type":"array","items":{"type":"string","format":"uuid"}},"attractionTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"playCount":{"type":"integer","nullable":true,"description":"For `limitedSingleGame` and `package`. Null means unlimited."},"validityKind":{"type":"string","enum":["sameDay","days","untilDate","untilUsed"]},"validityDays":{"type":"integer","nullable":true},"activationKind":{"type":"string","enum":["onPurchase","onFirstUse","onDate"],"default":"onFirstUse","description":"**On first use is what a guest expects from a day pass bought the night before.** On purchase is what a venue defaults to by accident, and it costs them a day.\n"},"dailyPlayCap":{"type":"integer","nullable":true},"cooldownMinutes":{"type":"integer","nullable":true,"description":"**Unlimited does not mean continuous.** A cooldown is how one child does not hold a popular ride all afternoon.\n"},"linkedProductId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"isActive":{"type":"boolean","default":true}}},
"GameplayAuthorisation": {"type":"object","x-ticvai-persistence":"games.authorisation","description":"Board 4.9. **The refusal reason is the product.**","properties":{"id":{"type":"string","format":"uuid"},"decision":{"type":"string","enum":["allow","refuse"]},"reason":{"type":"string","nullable":true,"enum":["ok","cardNotFound","cardExpired","cardBlocked","retapTooSoon","heightRestriction","ageRestriction","insufficientFunds","entitlementExhausted","entitlementNotValidHere","cooldownActive","dailyCapReached","readerNotConfigured","gameUnavailable"]},"guestMessage":{"type":"string","nullable":true,"description":"***\"No plays left on your pass\"* rather than *\"Declined\"*.** One is a guest who understands; the other is a member of staff walking over.\n"},"chargedFrom":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementId":{"type":"string","format":"uuid","nullable":true},"remainingBalance":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"remainingPlays":{"type":"integer","nullable":true},"trace":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string"},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"decidedOffline":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"GameplayAuthorisationRequest": {"type":"object","required":["readerId"],"properties":{"readerId":{"type":"string","format":"uuid"},"cardId":{"type":"string","format":"uuid","nullable":true},"credentialIdentifier":{"type":"string","nullable":true},"gameId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time","nullable":true},"guestHeightCm":{"type":"integer","nullable":true},"offline":{"type":"boolean","default":false}}},
"GameplayTransaction": {"type":"object","x-ticvai-persistence":"games.gameplay_transaction","description":"Boards 8.2 and 8.5. **The refused ones are the valuable half.**","properties":{"id":{"type":"string","format":"uuid"},"readerId":{"type":"string","format":"uuid"},"gameId":{"type":"string","format":"uuid","nullable":true},"cardId":{"type":"string","format":"uuid","nullable":true},"at":{"type":"string","format":"date-time"},"outcome":{"type":"string","enum":["allowed","refused","reversed"]},"reason":{"type":"string","nullable":true},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"chargedFrom":{"type":"string","nullable":true},"entitlementId":{"type":"string","format":"uuid","nullable":true},"ticketsEarned":{"type":"integer","nullable":true},"decidedOffline":{"type":"boolean","default":false},"syncedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Reader": {"type":"object","x-ticvai-persistence":"games.reader","description":"Board 2. **A `tenancy` device with a game configuration on it.**","required":["deviceId"],"properties":{"deviceId":{"type":"string","format":"uuid","description":"`tenancy.RegisteredDevice`. **Enrolment, firmware and tamper state live there.**\n"},"gameId":{"type":"string","format":"uuid","nullable":true},"readerProfileId":{"type":"string","format":"uuid","nullable":true},"acceptedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"acceptsDirectPay":{"type":"boolean","default":false},"retapDelaySeconds":{"type":"integer","default":3,"description":"**The setting that stops a guest paying twice for one go.** A wristband held against a reader for a second and a half is two taps to the hardware and one intention to the guest.\n"},"displayRules":{"type":"object","properties":{"freeGameGlow":{"type":"boolean","default":true,"description":"**What tells a guest their entitlement was used rather than their money.** Without it the complaint arrives at the desk.\n"},"showBalance":{"type":"boolean","default":true},"showPrice":{"type":"boolean","default":true},"themeCode":{"type":"string","nullable":true},"languages":{"type":"array","items":{"type":"string"}}}},"ioMapping":{"type":"object","additionalProperties":true,"description":"Board 9.6. Which output starts the game, which input reports it finished. **Deliberately open.** The keys are the reader model's own I/O lines, so the shape belongs to the vendor adaptor for that model (game readers are a driver, not a build — ADR-0012, ADR-0015), not to this contract.\n"},"status":{"type":"string","enum":["unconfigured","active","offline","maintenance","disabled"]},"scopePath":{"type":"string"}}},
"ReaderSyncStatus": {"type":"object","description":"Board 8.8. **Revenue the platform has not seen.**","properties":{"readerId":{"type":"string","format":"uuid"},"readerName":{"type":"string"},"pendingTransactions":{"type":"integer"},"pendingValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"oldestPendingAt":{"type":"string","format":"date-time","nullable":true},"lastSyncAt":{"type":"string","format":"date-time","nullable":true},"edgePackageVersion":{"type":"integer","nullable":true},"edgePackageStale":{"type":"boolean"},"status":{"type":"string","enum":["online","offline","degraded","unreachable"]}}},
"WalletTransaction": {"x-ticvai-persistence":"wallet.wallet_transaction","type":"object","required":["id","kind","amount","balanceAfter","recordedAt"],"properties":{"id":{"type":"string"},"walletId":{"type":"string","format":"uuid","x-ticvai-references":"wallet.wallet","description":"The wallet this movement is on (SD-027, 29 September). A shared wallet has many subjects, so the subject alone cannot say which balance moved."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"wallet.hold","description":"The hold a spend settled, where it came through `holdWalletFunds`."},"kind":{"$ref":"#/components/schemas/WalletTransactionKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"balanceAfter":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"orderId":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"WalletTransactionKind": {"type":"string","enum":["topUp","spend","refund","adjustment","bonus","expiry","transfer"]}
}
```
