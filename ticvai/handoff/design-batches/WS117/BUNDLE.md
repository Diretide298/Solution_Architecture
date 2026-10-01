# WS117 — AI Configuration Assistant board 2

**10 screens · 6 operations · 9 schemas · 2 permissions**

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
  `AI_USE, PRODUCT_CONFIGURE`. A control nobody can use must say so,
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
| `ADM-479` | AI Configuration Build Command Center | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-480` | Venue & Organization Configuration | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-481` | Product Configuration Assistant | B–D | 0 | 0 | 6 | 0 | 2 | 3 | — | notStarted (—) |
| `ADM-482` | Schedule, Capacity & Availability Configuration | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-483` | Pricing & Commercial Configuration | B–D | 0 | 10 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-484` | Promotion, Bundle & Upsell Configuration | B–D | 0 | 0 | 6 | 0 | 0 | 2 | — | notStarted (—) |
| `ADM-485` | Seating, Access & Operational Configuration | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `ADM-486` | Channel, Media & Fulfillment Configuration | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-487` | Cross-Module Conflict & Dependency Validation | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-488` | Configuration Preview & Impact Analysis | B–D | 18 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-480, ADM-481, ADM-482, ADM-483, ADM-484, ADM-485, ADM-486 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-479` AI Configuration Build Command Center

**Provide a central workspace showing how the Board 1 blueprint is being converted into actual TICVAI configuration objects.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `planId` (navigation), `sessionId` (session) |
| Route | `/platform/ai-configuration-build-command-center-adm-479` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Configuration Areas** (metric tile)

**Objects Proposed** (metric tile)

**Ready** (metric tile)

**Warnings** (metric tile)

**Conflicts** (metric tile)

**Missing Configuration** (metric tile)

**AI Recommendations** (metric tile)

**Approval Required** (metric tile)

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-480` Venue & Organization Configuration: *Venue & Organization Configuration*; carries `decisionKey`, `planId`
- → `ADM-481` Product Configuration Assistant: *Product Configuration Assistant*; carries `decisionKey`, `planId`
- → `ADM-482` Schedule, Capacity & Availability Configuration: *Schedule, Capacity & Availability Configuration*; carries `decisionKey`, `planId`
- → `ADM-483` Pricing & Commercial Configuration: *Pricing & Commercial Configuration*; carries `decisionKey`, `planId`
- → `ADM-484` Promotion, Bundle & Upsell Configuration: *Promotion, Bundle & Upsell Configuration*; carries `decisionKey`, `planId`
- → `ADM-485` Seating, Access & Operational Configuration: *Seating, Access & Operational Configuration*; carries `decisionKey`, `planId`
- → `ADM-486` Channel, Media & Fulfillment Configuration: *Channel, Media & Fulfillment Configuration*; carries `decisionKey`, `planId`
- → `ADM-487` Cross-Module Conflict & Dependency Validation: *Cross-Module Conflict & Dependency Validation*; carries `planId`
- → `ADM-488` Configuration Preview & Impact Analysis: *Configuration Preview & Impact Analysis*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The build list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the build untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No build yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the build are still there. The pack's own statuses are Building Configuration — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The blueprint is not ready: a required decision is open or deferred (AIC-115). |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `buildConfigurationPlan` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-479` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-479`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 2
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 1: Opens AI Configuration Build Command Center → Provide a central workspace showing how the Board 1 blueprint is being converted into actual TICVAI configuration objects.
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F226 branch at step 1 (expected): when Nothing has been set up on AI Configuration Build Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F226 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-479?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-480`, `ADM-481`, `ADM-482`, `ADM-483`, `ADM-484`, `ADM-485`, `ADM-486`, `ADM-487`, `ADM-488`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-480` Venue & Organization Configuration

**Convert the discovered business structure into the actual organizational and venue configuration required by TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `planId` (navigation), `sessionId` (session) |
| Route | `/platform/venue-organization-configuration-adm-480` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-479` AI Configuration Build Command Center: *Back to AI Configuration Build Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue organization list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue organization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue organization yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue organization are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer open for decisions (`session-not-open`). |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-480` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-480`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 2
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 2: Works in Venue & Organization Configuration → Convert the discovered business structure into the actual organizational and venue configuration required by TICVAI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-480?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-479`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-481` Product Configuration Assistant

**Convert Board 1 product requirements into actual proposed TICVAI ticket products and associated product rules. This screen should connect directly to the existing Ticketing module architecture, not create a separate AI product model.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `planId` (navigation), `sessionId` (session) |
| Route | `/platform/product-configuration-assistant-adm-481` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-479` AI Configuration Build Command Center: *Back to AI Configuration Build Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product assistant list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product assistant untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product assistant yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product assistant are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer open for decisions (`session-not-open`). |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- The AI configuration assistant is conversational and iterative: on "I want to create a product" it asks follow-ups (ticket type, validity, date/time) and, if required information such as capacity is missing, asks for it rather than proceeding, before showing a configuration blueprint and dependency map. *(agreed · MoM 18 Sep 2026, 4.5 AI Configuration Assistant — Conversational Requirement Gathering · DI-937)*
- Phase-one AI priority is a conversational configuration assistant: the admin says e.g. "I want to configure a new product" and it asks the product type (admission, time slot, etc.) and walks through product/promotion setup. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-279)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A120** Build the product creation wizard with four paths (from scratch · save as reusable template · clone · file upload using a standard tenant data-collection template) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'product creation wizard')*
- **A135** Manage group, family and corporate/allocation ticket types inside the unified product screen rather than separate screens *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 25 Aug 2026 · workshop tracker · keyword 'ticket type')*
- **A229** Build turnstile and handheld scanner configuration (connection details, light and sound feedback by ticket type, custom welcome messaging and branding, compatibility testing and deployment) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S7 (HLD/LLD) · 2 Sep 2026 · workshop tracker · keyword 'ticket type')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-481` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-481`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 2
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 4: Works in Product Configuration Assistant → Convert Board 1 product requirements into actual proposed TICVAI ticket products and associated product rules. This screen should connect directly to the existing Ticketing module architecture, not …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-481?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-479`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-482` Schedule, Capacity & Availability Configuration

**Translate operating requirements into actual schedules, timeslots, reservation windows, and capacity structures.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `planId` (navigation), `sessionId` (session) |
| Route | `/platform/schedule-capacity-availability-configuration-adm-482` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-479` AI Configuration Build Command Center: *Back to AI Configuration Build Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The schedule capacity availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the schedule capacity availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No schedule capacity availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the schedule capacity availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer open for decisions (`session-not-open`). |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-482` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-482`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 2
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 6: Works in Schedule, Capacity & Availability Configuration → Translate operating requirements into actual schedules, timeslots, reservation windows, and capacity structures.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-482?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-479`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-483` Pricing & Commercial Configuration

**Convert commercial requirements into proposed pricing, tax, fee, and commercial rules using TICVAI's existing Pricing architecture.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `PRODUCT_CONFIGURE` (1 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `planId` (navigation), `sessionId` (session) |
| Route | `/platform/pricing-commercial-configuration-adm-483` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every pricing commercial** (data table)

| Shows | Format | Notes |
|---|---|---|
| Dynamic pricing configuration required → | text | not in the schema: `Dynamic Pricing Configuration Required →` |
| Price simulation | text | not in the schema: `Price Simulation` |
| Adult / saturday / B2 c | text | not in the schema: `Adult / Saturday / B2C` |
| AED 120 | text | not in the schema: `AED 120` |
| AED 20 | text | not in the schema: `AED 20` |

**The selected pricing commercial** (detail panel): The pack groups this record's detail under its own headings: “Child AED 80 AED 95”, “Customer Eligibility”, “Dynamic Pricing”.

| Shows | Format | Notes |
|---|---|---|
| Dynamic pricing configuration required → | text | not in the schema: `Dynamic Pricing Configuration Required →` |
| Price simulation | text | not in the schema: `Price Simulation` |
| Adult / saturday / B2 c | text | not in the schema: `Adult / Saturday / B2C` |
| AED 120 | text | not in the schema: `AED 120` |
| AED 20 | text | not in the schema: `AED 20` |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-479` AI Configuration Build Command Center: *Back to AI Configuration Build Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pricing commercial list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pricing commercial untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pricing commercial yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the pricing commercial are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer open for decisions (`session-not-open`). |

#### Permissions

- `setChannelPricingCommercial` → `PRODUCT_CONFIGURE` (configure) · staff
- `getActionPlan` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-483` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-483`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 2
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 8: Works in Pricing & Commercial Configuration → Convert commercial requirements into proposed pricing, tax, fee, and commercial rules using TICVAI's existing Pricing architecture.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (10 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-483?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-479`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-484` Promotion, Bundle & Upsell Configuration

**Convert identified commercial opportunities into proposed promotion, package, bundle, upsell, and cross- sell configuration. This screen should only become prominent when relevant.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `planId` (navigation), `sessionId` (session) |
| Route | `/platform/promotion-bundle-upsell-configuration-adm-484` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-479` AI Configuration Build Command Center: *Back to AI Configuration Build Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The promotion bundle upsell list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the promotion bundle upsell untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No promotion bundle upsell yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the promotion bundle upsell are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer open for decisions (`session-not-open`). |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A66** Design a promotions engine: single/shared promo codes, bulk-generated unique single-use codes, and rule-based dynamic offers (e.g., buy-2-get-1-free) applied automatically without code entry *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Aug 2026 · workshop tracker · keyword 'promo code')*
- **A171** Build gift cards and vouchers in two variants (monetary vs. product-specific entitlement) with redemption channel rules, wallet-to-media linking and spend reporting by department and channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 27 Aug 2026 · workshop tracker · keyword 'voucher')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-484` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-484`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 2
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 10: Works in Promotion, Bundle & Upsell Configuration → Convert identified commercial opportunities into proposed promotion, package, bundle, upsell, and cross- sell configuration. This screen should only become prominent when relevant.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-484?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-479`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-485` Seating, Access & Operational Configuration

**Configure the operational rules required to fulfill and validate the products. The screen should adapt depending on venue type. For the museum example, seating is irrelevant and should not consume UI attention.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `planId` (navigation), `sessionId` (session) |
| Route | `/platform/seating-access-operational-configuration-adm-485` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-479` AI Configuration Build Command Center: *Back to AI Configuration Build Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The seating access operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the seating access operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No seating access operational yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the seating access operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer open for decisions (`session-not-open`). |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **C18** Locate and share the AutoCAD/PDF seating drawing from the Bahrain project (also to be shared with 3D vendor "3DDV") *(Allam · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'seating')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'seat-map')*
- **A102** Build a single unified seat map builder screen (section type as a section-level attribute — seated / zone / standing / suite — mixed types in one map, suites sold bulk or by seat) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker · keyword 'seat map')*
- **A104** Make best-seat ranking configurable per map/event and implement section-wise holds rather than freeform polygon selection *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'best-seat')*
- **A105** Make seating rules configurable per venue/event (consecutive-seat enforcement, social-distancing buffer, seat-kill, company/held-seat) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'seating')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-485` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-485`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 2
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 12: Works in Seating, Access & Operational Configuration → Configure the operational rules required to fulfill and validate the products. The screen should adapt depending on venue type. For the museum example, seating is irrelevant and should not consume UI …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-485?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-479`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-486` Channel, Media & Fulfillment Configuration

**Determine how the proposed products are sold, delivered, and fulfilled across TICVAI channels.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `planId` (navigation), `sessionId` (session) |
| Route | `/platform/channel-media-fulfillment-configuration-adm-486` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-479` AI Configuration Build Command Center: *Back to AI Configuration Build Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The channel media fulfillment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the channel media fulfillment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No channel media fulfillment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the channel media fulfillment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer open for decisions (`session-not-open`). |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-486` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-486`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 2
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 14: Works in Channel, Media & Fulfillment Configuration → Determine how the proposed products are sold, delivered, and fulfilled across TICVAI channels.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-486?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-479`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-487` Cross-Module Conflict & Dependency Validation

**Perform a comprehensive validation of the proposed configuration across all TICVAI modules before it is presented for approval. This should be one of the most important screens in Board 2.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/platform/cross-module-conflict-dependency-validation-adm-487` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Link Existing, Configure Later, Ask AI. Each needs an operation, or needs removing from the screen; this is …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Configuration Objects** (metric tile)

**Passed** (metric tile)

**Warnings** (metric tile)

**Conflicts** (metric tile)

**Missing Dependencies** (metric tile)

**Approval Requirements** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Link Existing (primary button) | navigation or local | — | — | — | — |
| Configure Later (secondary button) | navigation or local | — | — | — | — |
| Ask AI (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps)

**Where the user goes next**

- → `ADM-479` AI Configuration Build Command Center: *Back to AI Configuration Build Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-module conflict dependency list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-module conflict dependency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-module conflict dependency yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-module conflict dependency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The plan is executing or finished; simulate a rollback plan instead. |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `simulateActionPlan` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-487` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-487`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 2
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 16: Works in Cross-Module Conflict & Dependency Validation → Perform a comprehensive validation of the proposed configuration across all TICVAI modules before it is presented for approval. This should be one of the most important screens in Board 2.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-487?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Link Existing, Configure Later, Ask AI.
- [ ] Every transition is wired: `ADM-479`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-488` Configuration Preview & Impact Analysis

**Present the complete proposed configuration in business and technical terms before moving to approval and execution in Board 3. This is the final output of Board 2.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Critical AI Configuration Object Model; Three Sources of Configuration; AI Configuration Builder & Validation) and no display directory — it is … |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/platform/configuration-preview-impact-analysis-adm-488` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 👤 User Provided | select field | — | — | — | — | — | — |
| 1. AI Configuration Build Command Center | text field | — | — | — | — | — | — |
| 2. Venue & Organization Configuration | text field | — | — | — | — | — | — |
| 3. Product Configuration Assistant | text field | — | — | — | — | — | — |
| 4. Schedule, Capacity & Availability Configuration | text field | — | — | — | — | — | — |
| 5. Pricing & Commercial Configuration | text field | — | — | — | — | — | — |
| 6. Promotion, Bundle & Upsell Configuration | text field | — | — | — | — | — | — |
| 7. Seating, Access & Operational Configuration | text field | — | — | — | — | — | — |
| 8. Channel, Media & Fulfillment Configuration | text field | — | — | — | — | — | — |
| 9. Cross-Module Conflict & Dependency Validation | text field | — | — | — | — | — | — |
| 10. Configuration Preview & Impact Analysis | text field | — | — | — | — | — | — |
| “Tell TICVAI what your business needs.” | text field | — | — | — | — | — | — |
| ↓ | select field | — | — | — | — | — | — |
| “Govern, approve, and safely execute those changes.” | text field | — | — | — | — | — | — |
| & Continuous Configuration | select field | — | — | — | — | — | — |
| Module: AI Configuration Assistant | text field | — | — | — | — | — | — |
| Board: 3 of 3 | text field | — | — | — | — | — | — |
| Screens: 10 | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps)

**Where the user goes next**

- → `ADM-479` AI Configuration Build Command Center: *Back to AI Configuration Build Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The preview impact analysis configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the preview impact analysis untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No preview impact analysis configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The plan is executing or finished; simulate a rollback plan instead. |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `simulateActionPlan` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-488` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS10 AI Configuration Assistant Board 2.dc.html#adm-488`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 2
- Flow F226 *AI Configuration Assistant board 2: AI Configuration Build Command Center*, step 18: Works in Configuration Preview & Impact Analysis → Present the complete proposed configuration in business and technical terms before moving to approval and execution in Board 3. This is the final output of Board 2.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-488?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-479`.
- [ ] Every gated control is gated: `AI_USE`.
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

### In P09 · Platform

- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"buildConfigurationPlan": {"method":"POST","path":"/configuration-sessions/{sessionId}/plan","contract":"ai","summary":"Compile the blueprint into a plan","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlanDetail"},
"decideBlueprintRecommendation": {"method":"POST","path":"/configuration-sessions/{sessionId}/decisions/{decisionKey}","contract":"ai","summary":"Accept, modify, reject or defer a blueprint decision","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiBlueprintDecision"},
"getActionPlan": {"method":"GET","path":"/action-plans/{planId}","contract":"ai","summary":"A plan with its steps","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiActionPlanDetail"},
"getConfigurationBlueprint": {"method":"GET","path":"/configuration-sessions/{sessionId}/blueprint","contract":"ai","summary":"The blueprint so far","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":null},{"name":"decisionClass","in":"query","required":null}],"requestBody":null,"responds":"AiBlueprintView"},
"setChannelPricingCommercial": {"method":"PUT","path":"/channel-pricing-commercial","contract":"catalogue","summary":"Channel Pricing & Commercial Profile Assignment","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelPricingCommercialProfileAssignmentInput","responds":"ChannelPricingCommercialProfileAssignmentView"},
"simulateActionPlan": {"method":"POST","path":"/action-plans/{planId}/simulate","contract":"ai","summary":"Validate and simulate a plan without changing anything","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlanDetail"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiActionPlan": {"type":"object","x-ticvai-persistence":"ai.action_plan","description":"**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).","required":["origin","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"origin":{"type":"string","enum":["configurationSession","generateConfiguration","assistant","riskCase","operationalRequirement","rollback"]},"originRef":{"type":"string","nullable":true},"summary":{"type":"string"},"status":{"type":"string","enum":["draft","validated","simulated","awaitingApproval","approved","executing","paused","completed","partiallyCompleted","failed","compensated","cancelled","rolledBack"],"readOnly":true},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"approvalTier":{"type":"integer","minimum":1,"maximum":2,"description":"The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request, where tier 2 or the matrix caught the plan."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.proposed_action","description":"The `ai.proposed_action` the plan is presented as for a decision."},"changeSetHash":{"type":"string","readOnly":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"readOnly":true},"policyVersionRef":{"type":"string","readOnly":true,"description":"The governance policy version that decided it."},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."},"partialCompletionAllowed":{"type":"boolean","default":false,"description":"Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."},"rollbackOfPlanId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.action_plan"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiActionPlanDetail": {"type":"object","x-ticvai-persistence":"none — ai.action_plan with its ai.action_step rows","description":"A plan with its steps in DAG order.","required":["plan","steps"],"properties":{"plan":{"$ref":"#/components/schemas/AiActionPlan"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/AiActionStep"}}}},
"AiActionStep": {"type":"object","x-ticvai-persistence":"ai.action_step","description":"One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).","required":["planId","stepNumber","toolKey","targetContract","targetOperation","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","x-ticvai-references":"ai.action_plan"},"stepNumber":{"type":"integer","minimum":1},"dependsOn":{"type":"array","items":{"type":"integer","minimum":1},"description":"Step numbers that must succeed first. The plan is a DAG."},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body of `targetOperation`, validated against it before the plan is approved."},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"idempotencyKey":{"type":"string","readOnly":true},"targetObjectRef":{"type":"string","nullable":true},"targetObjectVersion":{"type":"string","nullable":true,"description":"The version the step was planned against. A different version at execution is drift."},"reversible":{"type":"boolean"},"compensation":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["pending","validated","running","succeeded","failed","compensated","skipped","paused"],"readOnly":true},"attempts":{"type":"integer","minimum":0,"maximum":3,"readOnly":true,"description":"Bounded at 3 (AIC-135)."},"lastError":{"type":"string","nullable":true,"readOnly":true},"resultRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning service's response: success is its answer, not a model's judgement (AIC-097)."},"startedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"AiBlueprintDecision": {"type":"object","x-ticvai-persistence":"ai.blueprint_decision","description":"One decision in a blueprint and what the administrator did with it. **Scoped through its blueprint** (`platform.apply_parent_rls`).","required":["blueprintId","decisionKey","decisionClass","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"blueprintId":{"type":"string","format":"uuid","x-ticvai-references":"ai.blueprint"},"decisionKey":{"type":"string"},"module":{"type":"string"},"decisionClass":{"type":"string","enum":["required","recommended","optional"]},"question":{"type":"string","nullable":true},"value":{"type":"object","additionalProperties":true,"nullable":true},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"sourceId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.config_source","description":"The attached document the value was extracted from (29 September, build; `attachConfigurationSource`)."},"sourceCitation":{"type":"string","nullable":true,"maxLength":200,"description":"Where in it, e.g. `page 4`, `sheet Prices!B7`, `logo region`."},"recommendation":{"type":"object","additionalProperties":true,"nullable":true,"description":"What the assistant recommends and why (ADM-491): mandatory configuration and best practice kept apart."},"status":{"type":"string","enum":["open","accepted","modified","rejected","deferred"]},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true}}},
"AiBlueprintView": {"type":"object","x-ticvai-persistence":"none — ai.blueprint with its ai.blueprint_decision rows","description":"A blueprint with its decisions.","required":["blueprint","decisions"],"properties":{"blueprint":{"$ref":"#/components/schemas/AiConfigurationBlueprint"},"decisions":{"type":"array","items":{"$ref":"#/components/schemas/AiBlueprintDecision"}}}},
"AiConfigurationBlueprint": {"type":"object","x-ticvai-persistence":"ai.blueprint","description":"**The blueprint** (design 2.2 D step 2, ADM-478): decisions, severity-graded issues and a dependency map. **Never `ready` while a required decision is deferred** (AIC-115).","required":["sessionId","version","readiness"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"sessionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.config_session"},"version":{"type":"integer","minimum":1},"readiness":{"type":"string","enum":["notReady","readyWithWarnings","ready"],"readOnly":true},"requiredOpen":{"type":"integer","minimum":0,"readOnly":true,"description":"Required decisions not yet accepted or modified."},"issues":{"$ref":"#/components/schemas/AiBlueprintIssueList"},"dependencyMap":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Configuration objects and the order they depend on each other, by module."},"summary":{"type":"string","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiProvenance": {"type":"string","enum":["confirmed","aiRecommended","inferred","unknown"],"description":"**Where a configuration value came from** (design 2.2 D, AIC-111): said by the administrator, recommended by the assistant, inferred from other answers, or not known yet. Shown beside every value; no confidence number is shown for configuration (design 5.6)."},
"ChannelPricingCommercialProfileAssignmentInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table covers these fields** — the closest is catalogue.price_list at 6%, so this is not an update to anything the package stores today and no new table has been decided","description":"**What Channel Pricing & Commercial Profile Assignment submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.\n\n**The pack defines this as a record**, under *For each assignment* - one of only 13 drafted writes that does. That is the client writing a row rather than a screen, and it is where the table conversation should start.","properties":{"priceProfile":{"type":"string","description":"Price Profile: the ID of the approved price list or profile consumed (the Pricing Engine calculates the price)"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"venue":{"type":"string","description":"Venue ID","nullable":true},"event":{"type":"string","description":"Event ID","nullable":true},"product":{"type":"string","description":"Product ID","nullable":true},"customerSegment":{"type":"string","description":"Customer Segment ID","nullable":true},"priority":{"type":"integer","description":"Priority: when several assignments match, the lower number wins","minimum":1},"channelId":{"type":"string","description":"Channel ID"},"pricingSource":{"type":"string","enum":["standardPriceList","channelPriceList","b2bRate","resellerRate","otaRate","posPrice","promotionalPriceProfile","dynamicPricingProfile"],"description":"Pricing Association (pack p.8): which kind of approved pricing this assignment consumes"},"overridePermission":{"type":"string","description":"Override Permission: the permission a user needs to override price on this channel","nullable":true},"fixedPriceOnly":{"type":"boolean","description":"Price Override Governance: use fixed price only"},"promotionAllowed":{"type":"boolean","description":"Price Override Governance: apply promotion"},"discountAllowed":{"type":"boolean","description":"Price Override Governance: apply discount"},"priceOverrideAllowed":{"type":"boolean","description":"Price Override Governance: override price"},"overrideRequiresApproval":{"type":"boolean","description":"Price Override Governance: require approval for override"},"dynamicPricingAllowed":{"type":"boolean","description":"Price Override Governance: use dynamic pricing"}},"x-ticvai-record-definition":"For each assignment"},
"ChannelPricingCommercialProfileAssignmentView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Pricing & Commercial Profile Assignment displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"priceProfile":{"type":"string","description":"Price Profile: the ID of the approved price list or profile consumed (the Pricing Engine calculates the price)"},"currency":{"type":"string","description":"Currency: ISO 4217 code","pattern":"^[A-Z]{3}$"},"effectiveFrom":{"type":"string","format":"date","description":"Effective From"},"effectiveTo":{"type":"string","format":"date","description":"Effective To; empty for open-ended","nullable":true},"venue":{"type":"string","description":"Venue ID","nullable":true},"event":{"type":"string","description":"Event ID","nullable":true},"product":{"type":"string","description":"Product ID","nullable":true},"customerSegment":{"type":"string","description":"Customer Segment ID","nullable":true},"priority":{"type":"integer","description":"Priority: when several assignments match, the lower number wins","minimum":1},"channelId":{"type":"string","description":"Channel ID"},"pricingSource":{"type":"string","enum":["standardPriceList","channelPriceList","b2bRate","resellerRate","otaRate","posPrice","promotionalPriceProfile","dynamicPricingProfile"],"description":"Pricing Association (pack p.8): which kind of approved pricing this assignment consumes"},"overridePermission":{"type":"string","description":"Override Permission: the permission a user needs to override price on this channel","nullable":true},"fixedPriceOnly":{"type":"boolean","description":"Price Override Governance: use fixed price only"},"promotionAllowed":{"type":"boolean","description":"Price Override Governance: apply promotion"},"discountAllowed":{"type":"boolean","description":"Price Override Governance: apply discount"},"priceOverrideAllowed":{"type":"boolean","description":"Price Override Governance: override price"},"overrideRequiresApproval":{"type":"boolean","description":"Price Override Governance: require approval for override"},"dynamicPricingAllowed":{"type":"boolean","description":"Price Override Governance: use dynamic pricing"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["missingPrice","expiredPrice","currencyMismatch","conflictingProfiles","invalidOverride"]},"message":{"type":"string"}}},"description":"Price Validation (pack p.9)"}}}
}
```
