# WS86 — Game and Ride board 9

**10 screens · 6 operations · 4 schemas · 4 permissions**

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
  `DEVELOPER_ADMIN, DEVICE_CONFIGURE, DEVICE_VIEW, PRODUCT_CONFIGURE`. A control nobody can use must say so,
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
| `BO-474` | Reader Integration Command Center | B–D | 2 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-475` | Reader Manufacturer & Model Profile | B–D | 9 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-476` | Communication Protocol Configuration | B–D | 10 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-477` | Reader Command & Event Mapping | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-478` | Reader Configuration Deployment & Synchronization | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-479` | Game Trigger & I/O Control Mapping | B–D | 0 | 12 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-480` | Reader Screen, LED & Sound Output Mapping | B–D | 0 | 0 | 6 | 0 | 2 | 0 | — | notStarted (—) |
| `BO-481` | Edge Cache & Offline Rule Package | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-482` | Device Diagnostics & Integration Logs | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-483` | Integration Certification & Test Console | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-477, BO-478, BO-479, BO-480, BO-481, BO-482, BO-483 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-474` Reader Integration Command Center

**Provide the technical team with a centralized view of every reader integration deployed across TICVAI clients and venues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/reader-integration-command-center-bo-474` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search reader integration | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by client, venue, manufacturer, model, protocol, status and 1 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Unconfigured · Active · Offline · Maintenance · Disabled | `listReaders` ?status |

#### Outputs: what the screen shows and produces

**Shown**

**Total Integrated Readers** (metric tile)

**Online** (metric tile)

**Offline** (metric tile)

**Integration Errors** (metric tile)

**Pending Configuration Sync** (metric tile)

**Transactions Today** (metric tile)

**Average Response Time** (metric tile)

**Protocol Errors** (metric tile)

**Data it reads**: `listReaders` (onLoad, Integrations by reader)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-475` Reader Manufacturer & Model Profile: *Reader Manufacturer & Model Profile*
- → `BO-476` Communication Protocol Configuration: *Communication Protocol Configuration*
- → `BO-477` Reader Command & Event Mapping: *Reader Command & Event Mapping*
- → `BO-478` Reader Configuration Deployment & Synchronization: *Reader Configuration Deployment & Synchronization*
- → `BO-479` Game Trigger & I/O Control Mapping: *Game Trigger & I/O Control Mapping*
- → `BO-480` Reader Screen, LED & Sound Output Mapping: *Reader Screen, LED & Sound Output Mapping*
- → `BO-481` Edge Cache & Offline Rule Package: *Edge Cache & Offline Rule Package*
- → `BO-482` Device Diagnostics & Integration Logs: *Device Diagnostics & Integration Logs*
- → `BO-483` Integration Certification & Test Console: *Integration Certification & Test Console*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader integration list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader integration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listReaders` → `DEVICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reader integration board configures lighting/display behaviour and other device-level settings exposed via the vendor SDK. *(client request · MoM 11 Sep 2026, 4.14 Reader Integration Protocol Management · DI-884)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-474` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-474`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 1: Opens Reader Integration Command Center → Provide the technical team with a centralized view of every reader integration deployed across TICVAI clients and venues.
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F195 branch at step 1 (expected): when Nothing has been set up on Reader Integration Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F195 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-474?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-475`, `BO-476`, `BO-477`, `BO-478`, `BO-479`, `BO-480`, `BO-481`, `BO-482`, `BO-483`.
- [ ] Every gated control is gated: `DEVICE_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-475` Reader Manufacturer & Model Profile

**Allow TICVAI to support multiple reader manufacturers/models without building business rules specifically for one Chinese reader.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure supported capabilities) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/reader-manufacturer-model-profile-bo-475` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| ☑ RFID | select field | — | — | — | — | — | — |
| ☑ NFC | select field | — | — | — | — | — | — |
| ☑ Screen | select field | — | — | — | — | — | — |
| ☑ LED / RGB Lighting | text field | — | — | — | — | — | — |
| ☑ Sound | select field | — | — | — | — | — | — |
| ☑ Touch Screen | select field | — | — | — | — | — | — |
| ☑ Local Storage | select field | — | — | — | — | — | — |
| ☑ I/O Output | select field | — | — | — | — | — | — |
| ☑ Network Connectivity | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader manufacturer model configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader manufacturer model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader manufacturer model configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setReaderProfile` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-475` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-475`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 2: Works in Reader Manufacturer & Model Profile → Allow TICVAI to support multiple reader manufacturers/models without building business rules specifically for one Chinese reader.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-475?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-476` Communication Protocol Configuration

**Configure how TICVAI communicates with each reader/device family.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRODUCT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Connection Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/games-rides/communication-protocol-configuration-bo-476` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Protocol | select field | — | — | — | — | — | — |
| Host / IP | select field | — | — | — | — | — | — |
| Port | select field | — | — | — | — | — | — |
| Endpoint | select field | — | — | — | — | — | — |
| Authentication | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Retry Count | select field | — | — | — | — | — | — |
| Heartbeat Interval | select field | — | — | — | — | — | — |
| Encryption | select field | — | — | — | — | — | — |
| Connection Mode | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The communication protocol configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the communication protocol untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No communication protocol configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setReaderProfile` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reader integration board configures lighting/display behaviour and other device-level settings exposed via the vendor SDK. *(client request · MoM 11 Sep 2026, 4.14 Reader Integration Protocol Management · DI-884)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-476` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-476`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 4: Works in Communication Protocol Configuration → Configure how TICVAI communicates with each reader/device family.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-476?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `PRODUCT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-477` Reader Command & Event Mapping

**Translate TICVAI's standardized commands into the specific commands understood by each reader manufacturer. This is one of the most important architectural screens. DISPLAY_PRICE DISPLAY_MESSAGE LED_COLOR APPROVE_PLAY REJECT_PLAY TRIGGER_GAME SHOW_BALANCE SYNC_CONFIG**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/reader-command-event-mapping-bo-477` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save reader configuration (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader command event list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader command event untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader command event yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader command event are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-477` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-477`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 6: Works in Reader Command & Event Mapping → Translate TICVAI's standardized commands into the specific commands understood by each reader manufacturer. This is one of the most important architectural screens. DISPLAY_PRICE DISPLAY_MESSAGE …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-477?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save reader configuration, Cancel.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-478` Reader Configuration Deployment & Synchronization

**Push backend configuration from TICVAI to readers where local configuration is required.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/reader-configuration-deployment-synchronization-bo-478` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader deployment synchronization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader deployment synchronization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader deployment synchronization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader deployment synchronization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `deployReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-478` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-478`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 8: Works in Reader Configuration Deployment & Synchronization → Push backend configuration from TICVAI to readers where local configuration is required.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-478?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-479` Game Trigger & I/O Control Mapping

**Configure how an approved TICVAI transaction physically starts a game or ride.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card Tap) and no metric row |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/game-trigger-i-o-control-mapping-bo-479` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every game trigger mapping** (data table)

| Shows | Format | Notes |
|---|---|---|
| → TICVAI authorization | text | not in the schema: `→ TICVAI Authorization` |
| → APPROVED | text | not in the schema: `→ APPROVED` |
| → reader receives command | text | not in the schema: `→ Reader receives command` |
| → reader sends output | text | not in the schema: `→ Reader sends output` |
| → game controller | text | not in the schema: `→ Game Controller` |
| → GAME START | text | not in the schema: `→ GAME START` |

**The selected game trigger mapping** (detail panel): The pack groups this record's detail under its own headings: “Depending on hardware”, “Page 90 of 105”, “Basketball Pro”, “Potential inputs”.

| Shows | Format | Notes |
|---|---|---|
| → TICVAI authorization | text | not in the schema: `→ TICVAI Authorization` |
| → APPROVED | text | not in the schema: `→ APPROVED` |
| → reader receives command | text | not in the schema: `→ Reader receives command` |
| → reader sends output | text | not in the schema: `→ Reader sends output` |
| → game controller | text | not in the schema: `→ Game Controller` |
| → GAME START | text | not in the schema: `→ GAME START` |

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The game trigger mapping list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the game trigger mapping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No game trigger mapping yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the game trigger mapping are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A286** Integrate gaming readers directly via vendor SDK (no middleware) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A287** Build game & ride command centre and reader configuration *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A288** Gaming credit order (bonus first) with category limits on bonus credit *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **A289** Add retap protection and per-game retry pricing *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 11 Sep 2026 · workshop tracker · keyword 'game')*
- **A291** Find a gaming reader vendor with India support *(Chinmay Parab · Medium · Ongoing → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 11 Sep 2026 · workshop tracker · keyword 'gaming')*
- **C56** Share DAM and gaming/redemption documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 11 Sep 2026 · workshop tracker · keyword 'gaming')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-479` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-479`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 10: Works in Game Trigger & I/O Control Mapping → Configure how an approved TICVAI transaction physically starts a game or ride.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-479?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-480` Reader Screen, LED & Sound Output Mapping

**Map TICVAI transaction results to the physical reader's screen, lighting and sound capabilities. This supports the matrix requirement for free-game color indication and custom reader themes.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/reader-screen-led-sound-output-mapping-bo-480` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save reader configuration (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reader screen led list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reader screen led untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reader screen led yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reader screen led are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reader integration board configures lighting/display behaviour and other device-level settings exposed via the vendor SDK. *(client request · MoM 11 Sep 2026, 4.14 Reader Integration Protocol Management · DI-884)*
- Each game/ride has a TICVAI reader that displays pricing, branding and theme pushed from the TICVAI back end; a tap triggers a dry-contact-style start/stop signal (like a turnstile). *(agreed · MoM 11 Sep 2026, 4.6 Gaming - Reader Hardware Strategy & Vendor Sourcing · DI-862)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-480` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-480`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 12: Works in Reader Screen, LED & Sound Output Mapping → Map TICVAI transaction results to the physical reader's screen, lighting and sound capabilities. This supports the matrix requirement for free-game color indication and custom reader themes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-480?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save reader configuration, Cancel.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-481` Edge Cache & Offline Rule Package

**Configure what information can be securely distributed to the edge/reader or local gateway for temporary offline operation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/edge-cache-offline-rule-package-bo-481` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The edge cache offline list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the edge cache offline untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No edge cache offline yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the edge cache offline are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `deployReaderConfiguration` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-481` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-481`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 14: Works in Edge Cache & Offline Rule Package → Configure what information can be securely distributed to the edge/reader or local gateway for temporary offline operation.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-481?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-482` Device Diagnostics & Integration Logs

**Give development team / support teams detailed technical visibility when a reader or game is not operating correctly.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVICE_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `readerId` (navigation) |
| Route | `/games-rides/device-diagnostics-integration-logs-bo-482` |

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

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The device diagnostics integration list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the device diagnostics integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No device diagnostics integration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the device diagnostics integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `testReader` → `DEVICE_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-482` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-482`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 16: Works in Device Diagnostics & Integration Logs → Give development team / support teams detailed technical visibility when a reader or game is not operating correctly.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-482?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVICE_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-483` Integration Certification & Test Console

**Provide a controlled environment for testing and approving a new reader model before deployment. This is particularly important for your plan because you will purchase the hardware separately and TICVAI must verify that the reader supports everything required by the platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Games & Rides · wave 3 · needs the `games` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVELOPER_ADMIN` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Card; Display) and no metric row |
| Offline | online only |
| Opens with | `listingId` (navigation) |
| Route | `/games-rides/integration-certification-test-console-bo-483` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every integration certification test** (data table)

| Shows | Format | Notes |
|---|---|---|
| RFID tap | text | not in the schema: `RFID Tap` |
| NFC tap | text | not in the schema: `NFC Tap` |
| Credential reading | text | not in the schema: `Credential Reading` |
| Text | text | not in the schema: `Text` |
| Price | text | not in the schema: `Price` |
| Balance | text | not in the schema: `Balance` |

**The selected integration certification test** (detail panel): The pack groups this record's detail under its own headings: “Connectivity”, “LED”, “Gameplay”, “Transactions”, “Offline”, “GR-X20 Reader”.

| Shows | Format | Notes |
|---|---|---|
| RFID tap | text | not in the schema: `RFID Tap` |
| NFC tap | text | not in the schema: `NFC Tap` |
| Credential reading | text | not in the schema: `Credential Reading` |
| Text | text | not in the schema: `Text` |
| Price | text | not in the schema: `Price` |
| Balance | text | not in the schema: `Balance` |

**Where the user goes next**

- → `BO-474` Reader Integration Command Center: *Back to Reader Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration certification test list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration certification test untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration certification test yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration certification test are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `certifyIntegration` → `DEVELOPER_ADMIN` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-483` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS66 Game and Ride Board 9.dc.html#bo-483`
- Workshop pack: Game_and_Ride_Module.pdf board 9
- Flow F195 *Game and Ride board 9: Reader Integration Command Center*, step 18: Works in Integration Certification & Test Console → Provide a controlled environment for testing and approving a new reader model before deployment. This is particularly important for your plan because you will purchase the hardware separately and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-483?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-474`.
- [ ] Every gated control is gated: `DEVELOPER_ADMIN`.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"certifyIntegration": {"method":"POST","path":"/listings/{listingId}/certify","contract":"public-api","summary":"Approve, reject or revoke a certification","permission":"DEVELOPER_ADMIN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"IntegrationListing"},
"deployReaderConfiguration": {"method":"POST","path":"/readers/{readerId}/deploy","contract":"games","summary":"Push configuration and the offline rule package to a reader","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listReaders": {"method":"GET","path":"/readers","contract":"games","summary":"Readers, their attractions and their health","permission":"DEVICE_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"status","in":"query","required":null}],"requestBody":null,"responds":"Reader"},
"setReaderConfiguration": {"method":"PUT","path":"/readers/{readerId}","contract":"games","summary":"What this reader charges, opens, shows and refuses","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Reader","responds":"Reader"},
"setReaderProfile": {"method":"PUT","path":"/reader-profiles","contract":"games","summary":"How a reader behaves and what it shows","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReaderProfile","responds":"ReaderProfile"},
"testReader": {"method":"POST","path":"/readers/{readerId}/test","contract":"games","summary":"Prove a reader works before a guest finds out it does not","permission":"DEVICE_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReaderTestResult"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"IntegrationListing": {"type":"object","x-ticvai-persistence":"control.integration_listing","description":"13.1.50, decision D1. **A listing, not an installation.** The integration runs on the developer's own infrastructure.\n**Third-party code does not execute inside TICVAI** — stated rather than assumed, because that is a different product with a different threat model.\n","required":["id","developerId","name","category","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid"},"name":{"type":"string"},"category":{"type":"string","enum":["crm","marketing","accounting","hotel","transport","analytics","accessibility","other"]},"description":{"type":"string"},"integrationUrl":{"type":"string"},"requiredScopes":{"type":"array","items":{"type":"string"}},"status":{"type":"string","enum":["draft","submitted","inReview","certified","rejected","revoked","delisted"],"readOnly":true},"certifiedUntil":{"type":"string","format":"date","nullable":true,"readOnly":true,"description":"**Certification expires.** An integration certified against v1 and still listed after v3 is TICVAI vouching for something it has not looked at in two years.\n"},"certifiedAgainstVersion":{"type":"string","nullable":true,"readOnly":true},"listingFeeModel":{"type":"string","enum":["none","flat","revenueShare"],"nullable":true},"visibility":{"type":"string","enum":["public","private"],"default":"public","description":"`private`: certified for production access and never shown in the marketplace (17 September minutes, M17-06). `public`: also listed once certified.\n"}}},
"Reader": {"type":"object","x-ticvai-persistence":"games.reader","description":"Board 2. **A `tenancy` device with a game configuration on it.**","required":["deviceId"],"properties":{"deviceId":{"type":"string","format":"uuid","description":"`tenancy.RegisteredDevice`. **Enrolment, firmware and tamper state live there.**\n"},"gameId":{"type":"string","format":"uuid","nullable":true},"readerProfileId":{"type":"string","format":"uuid","nullable":true},"acceptedCreditTypeIds":{"type":"array","items":{"type":"string","format":"uuid"}},"acceptsDirectPay":{"type":"boolean","default":false},"retapDelaySeconds":{"type":"integer","default":3,"description":"**The setting that stops a guest paying twice for one go.** A wristband held against a reader for a second and a half is two taps to the hardware and one intention to the guest.\n"},"displayRules":{"type":"object","properties":{"freeGameGlow":{"type":"boolean","default":true,"description":"**What tells a guest their entitlement was used rather than their money.** Without it the complaint arrives at the desk.\n"},"showBalance":{"type":"boolean","default":true},"showPrice":{"type":"boolean","default":true},"themeCode":{"type":"string","nullable":true},"languages":{"type":"array","items":{"type":"string"}}}},"ioMapping":{"type":"object","additionalProperties":true,"description":"Board 9.6. Which output starts the game, which input reports it finished. **Deliberately open.** The keys are the reader model's own I/O lines, so the shape belongs to the vendor adaptor for that model (game readers are a driver, not a build — ADR-0012, ADR-0015), not to this contract.\n"},"status":{"type":"string","enum":["unconfigured","active","offline","maintenance","disabled"]},"scopePath":{"type":"string"}}},
"ReaderProfile": {"type":"object","x-ticvai-persistence":"games.reader_profile","description":"BL-153. **`games` is well built on the money and what is missing sits at the reader.**\n10.2.14 and 10.2.17 want a different colour for a free game and a different one for insufficient credit — **because a guest at an arcade machine cannot read a message, they can only see a light.** The whole interaction is a second long and happens across a noisy room.\n","required":["id","name"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"displayBehaviour":{"type":"object","description":"**What the reader shows, per outcome.** Colour and tone, because the guest is looking at a machine rather than a screen.\n","properties":{"accepted":{"type":"string"},"freeGame":{"type":"string"},"insufficientCredit":{"type":"string"},"cardBlocked":{"type":"string"},"readError":{"type":"string"}}},"retryPricing":{"type":"object","nullable":true,"description":"**A retry after a machine fault is not a second play.** Without this a guest whose game crashed pays twice, and the attendant refunds by hand — which is how an arcade loses money and goodwill at once.\n","properties":{"isFree":{"type":"boolean","default":true},"withinSeconds":{"type":"integer","default":60},"maxRetries":{"type":"integer","default":1}}},"rePlayWindowSeconds":{"type":"integer","nullable":true,"description":"**A second tap within this window is the same play, not a new one.** A guest tapping twice because nothing appeared to happen should not be charged twice.\n"},"entitlementProductIds":{"type":"array","description":"**Per-game entitlement.** A pass that includes ten specific rides needs the reader to know which, and a card that works everywhere is a different product.\n","items":{"type":"string","format":"uuid"}},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ReaderTestResult": {"type":"object","description":"Boards 2.10 and 9.9. **Each check separately**, because they send an engineer to different places.\n","properties":{"readerId":{"type":"string","format":"uuid"},"testedAt":{"type":"string","format":"date-time"},"checks":{"type":"array","items":{"type":"object","properties":{"check":{"type":"string","enum":["connectivity","cardRead","balanceCheck","display","sound","gameTrigger","gameCompleteSignal"]},"passed":{"type":"boolean"},"detail":{"type":"string","nullable":true}}}},"overall":{"type":"string","enum":["pass","partial","fail"]}}}
}
```
