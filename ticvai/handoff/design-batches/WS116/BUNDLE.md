# WS116 — AI Configuration Assistant board 1

**10 screens · 8 operations · 12 schemas · 1 permissions**

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

- **Every control that can be refused must be gated.** 1 permissions apply here:
  `AI_USE`. A control nobody can use must say so,
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
| `ADM-469` | AI Configuration Home & Start | B–D | 0 | 30 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `ADM-470` | Setup Type & Business Intent Discovery | B–D | 15 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-471` | Venue & Business Model Discovery | B–D | 30 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-472` | Guided Question & Answer Workspace | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-473` | Product & Admission Model Discovery | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-474` | Operational Requirement Discovery | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-475` | Commercial Requirement Discovery | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-476` | Required, Recommended & Optional Decisions | B–D | 4 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-477` | Missing Information & Clarification Center | B–D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |
| `ADM-478` | Configuration Blueprint & Dependency Map | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-472, ADM-473, ADM-474, ADM-475, ADM-478 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-469` AI Configuration Home & Start

**Provide one intelligent starting point for creating or modifying TICVAI configuration through AI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show intelligent cards such as; Show) and no metric row |
| Offline | online only |
| Opens with | `sessionId` (session) |
| Route | `/platform/ai-configuration-home-start-adm-469` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Create New Configuration, Modify Existing Configuration, Extend Existing Configuration, Clone & Adapt … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | select | — | Discovering · Blueprint ready · Planned · Executing · Completed · Abandoned | `listConfigurationSessions` ?status |
| Intent | radio group | — | Create · Modify · Extend · Clone | `listConfigurationSessions` ?intent |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every home start** (data table)

| Shows | Format | Notes |
|---|---|---|
| Museum | text | not in the schema: `Museum` |
| Theme park | text | not in the schema: `Theme Park` |
| Water park | text | not in the schema: `Water Park` |
| Zoo | text | not in the schema: `Zoo` |
| Aquarium | text | not in the schema: `Aquarium` |
| Theatre | text | not in the schema: `Theatre` |
| Stadium | text | not in the schema: `Stadium` |
| Indoor attraction | text | not in the schema: `Indoor Attraction` |
| Family entertainment center | text | not in the schema: `Family Entertainment Center` |
| Festival | text | not in the schema: `Festival` |
| Conference | text | not in the schema: `Conference` |
| Temporary event | text | not in the schema: `Temporary Event` |
| Start from scratch | text | not in the schema: `Start from Scratch` |
| Session type progress last activity status | text | not in the schema: `Session Type Progress Last Activity Status` |
| Summer festival event 100% yesterday blueprint ready | text | not in the schema: `Summer Festival Event 100% Yesterday Blueprint Ready` |

**The selected home start** (detail panel): The pack groups this record's detail under its own headings: “The screen should immediately answer”, “Subtitle”, “Large conversational input”.

| Shows | Format | Notes |
|---|---|---|
| Museum | text | not in the schema: `Museum` |
| Theme park | text | not in the schema: `Theme Park` |
| Water park | text | not in the schema: `Water Park` |
| Zoo | text | not in the schema: `Zoo` |
| Aquarium | text | not in the schema: `Aquarium` |
| Theatre | text | not in the schema: `Theatre` |
| Stadium | text | not in the schema: `Stadium` |
| Indoor attraction | text | not in the schema: `Indoor Attraction` |
| Family entertainment center | text | not in the schema: `Family Entertainment Center` |
| Festival | text | not in the schema: `Festival` |
| Conference | text | not in the schema: `Conference` |
| Temporary event | text | not in the schema: `Temporary Event` |
| Start from scratch | text | not in the schema: `Start from Scratch` |
| Session type progress last activity status | text | not in the schema: `Session Type Progress Last Activity Status` |
| Summer festival event 100% yesterday blueprint ready | text | not in the schema: `Summer Festival Event 100% Yesterday Blueprint Ready` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create New Configuration (primary button) | navigation or local | — | — | — | — |
| Modify Existing Configuration (secondary button) | navigation or local | — | — | — | — |
| Extend Existing Configuration (secondary button) | navigation or local | — | — | — | — |
| Clone & Adapt Existing Setup (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listConfigurationSessions` (onLoad, Configuration-assistant sessions)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-470` Setup Type & Business Intent Discovery: *Setup Type & Business Intent Discovery*
- → `ADM-471` Venue & Business Model Discovery: *Venue & Business Model Discovery*
- → `ADM-472` Guided Question & Answer Workspace: *Guided Question & Answer Workspace*
- → `ADM-473` Product & Admission Model Discovery: *Product & Admission Model Discovery*
- → `ADM-474` Operational Requirement Discovery: *Operational Requirement Discovery*
- → `ADM-475` Commercial Requirement Discovery: *Commercial Requirement Discovery*
- → `ADM-476` Required, Recommended & Optional Decisions: *Required, Recommended & Optional Decisions*
- → `ADM-477` Missing Information & Clarification Center: *Missing Information & Clarification Center*
- → `ADM-478` Configuration Blueprint & Dependency Map: *Configuration Blueprint & Dependency Map*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The home start list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the home start untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No home start yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the home start are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer discovering (`session-not-open`), or the governance data policy refuses the document (`governance-blocked`).; 422 The asset is not a readable document or image (`unreadable-source`), for example a scan with no text layer the extractor could read. |

#### Permissions

- `startConfigurationSession` → `AI_USE` (operate) · staff
- `listConfigurationSessions` → `AI_USE` (operate) · staff
- `attachConfigurationSource` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.31 | System shall allow administrators to upload event briefs, brochures, schedules, PDFs or spreadsheets and use AI to automatically generate event configurations, sessions, ticket types, capacities … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |
| 1.4.21 | System shall allow administrators to upload spreadsheets, brochures, PDFs or existing catalogues and automatically generate products, pricing structures, rules, entitlements and configurations using … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Phase-one AI priority is a conversational configuration assistant: the admin says e.g. "I want to configure a new product" and it asks the product type (admission, time slot, etc.) and walks through product/promotion setup. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-279)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-469` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-469`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 1: Opens AI Configuration Home & Start → Provide one intelligent starting point for creating or modifying TICVAI configuration through AI.
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F225 branch at step 1 (expected): when Nothing has been set up on AI Configuration Home & Start yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F225 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (30 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-469?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create New Configuration, Modify Existing Configuration, Extend Existing Configuration, Clone & Adapt Existing Setup.
- [ ] Every transition is wired: `ADM-002`, `ADM-470`, `ADM-471`, `ADM-472`, `ADM-473`, `ADM-474`, `ADM-475`, `ADM-476`, `ADM-477`, `ADM-478`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-470` Setup Type & Business Intent Discovery

**Understand what the administrator is actually trying to accomplish before asking detailed configuration questions. This is the first AI interview screen.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Detected Setup; Likely Configuration Areas) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `sessionId` (session) |
| Route | `/platform/setup-type-business-intent-discovery-adm-470` |

**Known gaps.** **Setup Type & Business Intent Discovery declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Action: Create | select field | — | — | — | — | — | — |
| Object: Venue | select field | — | — | — | — | — | — |
| Venue Type: Museum | select field | — | — | — | — | — | — |
| Organization: Existing | select field | — | — | — | — | — | — |
| Location: Dubai | select field | — | — | — | — | — | — |
| Operation Type: Permanent | select field | — | — | — | — | — | — |
| Confidence: 96% | select field | — | — | — | — | — | — |
| ✓ Venue | select field | — | — | — | — | — | — |
| ✓ Products | select field | — | — | — | — | — | — |
| ✓ Schedule | select field | — | — | — | — | — | — |
| ✓ Capacity | select field | — | — | — | — | — | — |
| ✓ Pricing | select field | — | — | — | — | — | — |
| ✓ Sales Channels | select field | — | — | — | — | — | — |
| ✓ Ticket Media | select field | — | — | — | — | — | — |
| ✓ Access | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listConfigurationSources` (onLoad, Attached documents with extraction status and what they …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The type business intent configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the type business intent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No type business intent configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer discovering (`session-not-open`), or the governance data policy refuses the document (`governance-blocked`).; 409 The session is no longer discovering (`session-not-open`).; 422 The asset is not a readable document or image (`unreadable-source`), for example a scan with no text layer the extractor could read. |

#### Permissions

- `startConfigurationSession` → `AI_USE` (operate) · staff
- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `attachConfigurationSource` → `AI_USE` (operate) · staff
- `listConfigurationSources` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.31 | System shall allow administrators to upload event briefs, brochures, schedules, PDFs or spreadsheets and use AI to automatically generate event configurations, sessions, ticket types, capacities … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |
| 1.4.21 | System shall allow administrators to upload spreadsheets, brochures, PDFs or existing catalogues and automatically generate products, pricing structures, rules, entitlements and configurations using … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-470` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-470`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 2: Works in Setup Type & Business Intent Discovery → Understand what the administrator is actually trying to accomplish before asking detailed configuration questions. This is the first AI interview screen.

#### Acceptance for the design

- [ ] Every input above is drawn (15), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-470?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-471` Venue & Business Model Discovery

**Understand how the business operates so TICVAI can determine which configuration branches are relevant.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture as relevant) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `sessionId` (session) |
| Route | `/platform/venue-business-model-discovery-adm-471` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Confirm / Edit Understanding / Continue. Each needs an operation, or needs removing from the screen; this …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue Name | select field | — | — | — | — | — | — |
| Venue Type | select field | — | — | — | — | — | — |
| Country | select field | — | — | — | — | — | — |
| City | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Operating Model | select field | — | — | — | — | — | — |
| Permanent / Seasonal / Temporary | text field | — | — | — | — | — | — |
| Indoor / Outdoor / Mixed | text field | — | — | — | — | — | — |
| Number of Locations | select field | — | — | — | — | — | — |
| Number of Attractions / Experiences | text field | — | — | — | — | — | — |
| Business Model Discovery | select field | — | — | — | — | — | — |
| General Admission | select field | — | — | — | — | — | — |
| Dated Admission | select field | — | — | — | — | — | — |
| Open-Dated Admission | select field | — | — | — | — | — | — |
| Timeslot Admission | select field | — | — | — | — | — | — |
| Assigned Seating | select field | — | — | — | — | — | — |
| Multi-Day Admission | select field | — | — | — | — | — | — |
| Membership | select field | — | — | — | — | — | — |
| Subscription | select field | — | — | — | — | — | — |
| Pass | select field | — | — | — | — | — | — |
| Attraction / Ride-Based | select field | — | — | — | — | — | — |
| Mixed Model | select field | — | — | — | — | — | — |
| Conditional Logic | select field | — | — | — | — | — | — |
| Venue = Theatre | select field | — | — | — | — | — | — |
| Performances | select field | — | — | — | — | — | — |
| Seat Map | select field | — | — | — | — | — | — |
| Sections | select field | — | — | — | — | — | — |
| Price Categories | select field | — | — | — | — | — | — |
| Show Schedule | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm / Edit Understanding / Continue (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue business model configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue business model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue business model configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer discovering (`session-not-open`). |

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-471` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-471`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 4: Works in Venue & Business Model Discovery → Understand how the business operates so TICVAI can determine which configuration branches are relevant.

#### Acceptance for the design

- [ ] Every input above is drawn (30), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-471?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Confirm / Edit Understanding / Continue.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-472` Guided Question & Answer Workspace

**Provide the main adaptive AI interview workspace. This is the core screen of Board 1. It should feel conversational but remain structured and controlled.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session) |
| Route | `/platform/guided-question-answer-workspace-adm-472` |

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

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guided question answer list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guided question answer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guided question answer yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guided question answer are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer discovering (`session-not-open`). |

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-472` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-472`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 6: Works in Guided Question & Answer Workspace → Provide the main adaptive AI interview workspace. This is the core screen of Board 1. It should feel conversational but remain structured and controlled.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-472?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-473` Product & Admission Model Discovery

**Determine what the venue sells and how each product provides admission or entitlement.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session) |
| Route | `/platform/product-admission-model-discovery-adm-473` |

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

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product admission model list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product admission model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product admission model yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the product admission model are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer discovering (`session-not-open`). |

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-473` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-473`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 8: Works in Product & Admission Model Discovery → Determine what the venue sells and how each product provides admission or entitlement.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-473?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-474` Operational Requirement Discovery

**Understand the operational rules needed to deliver the configured products.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session) |
| Route | `/platform/operational-requirement-discovery-adm-474` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Confirm Operations / Add Requirement / Continue. Each needs an operation, or needs removing from the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

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
| Confirm Operations / Add Requirement / Continue (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The operational requirement discovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the operational requirement discovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No operational requirement discovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the operational requirement discovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer discovering (`session-not-open`). |

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-474` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-474`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 10: Works in Operational Requirement Discovery → Understand the operational rules needed to deliver the configured products.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-474?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm Operations / Add Requirement / …, Cancel.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-475` Commercial Requirement Discovery

**Understand how the venue intends to sell and commercially manage its products without actually configuring pricing yet.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session) |
| Route | `/platform/commercial-requirement-discovery-adm-475` |

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

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The commercial requirement discovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the commercial requirement discovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No commercial requirement discovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the commercial requirement discovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer discovering (`session-not-open`). |

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-475` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-475`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 12: Works in Commercial Requirement Discovery → Understand how the venue intends to sell and commercially manage its products without actually configuring pricing yet.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-475?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-476` Required, Recommended & Optional Decisions

**Prevent the administrator from forgetting important configuration while also preventing unnecessary questions from blocking setup. This screen is fundamental to making the AI genuinely useful.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `sessionId` (session) |
| Route | `/platform/required-recommended-optional-decisions-adm-476` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Configure Now | select field | — | — | — | — | — | — |
| Use Recommended Policy | select field | — | — | — | — | — | — |
| Decide Later | select field | — | — | — | — | — | — |
| Required Rule | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

#### Outputs: what the screen shows and produces

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The required recommended optional configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the required recommended optional untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No required recommended optional configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer open for decisions (`session-not-open`). |

#### Permissions

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-476` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-476`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 14: Works in Required, Recommended & Optional Decisions → Prevent the administrator from forgetting important configuration while also preventing unnecessary questions from blocking setup. This screen is fundamental to making the AI genuinely useful.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-476?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-477` Missing Information & Clarification Center

**Allow AI to identify incomplete, contradictory, ambiguous, or logically inconsistent requirements before producing the final blueprint.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `decisionKey` (navigation), `sessionId` (session) |
| Route | `/platform/missing-information-clarification-center-adm-477` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `getConfigurationBlueprint` ?module |
| Decision class | segmented control | — | Required · Recommended · Optional | `getConfigurationBlueprint` ?decisionClass |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Required Missing** (metric tile)

**Clarifications Needed** (metric tile)

**Conflicts** (metric tile)

**Warnings** (metric tile)

**Recommendations** (metric tile)

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far); `listConfigurationSources` (onLoad, Attached documents with extraction status and what they …)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The missing information clarification list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the missing information clarification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No missing information clarification yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the missing information clarification are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The session is no longer discovering (`session-not-open`), or the governance data policy refuses the document (`governance-blocked`).; 409 The session is no longer discovering (`session-not-open`).; 409 The session is no longer open for decisions (`session-not-open`).; 422 The asset is not a readable document or image (`unreadable-source`), for example a scan with no text layer the extractor … |

#### Permissions

- `answerConfigurationQuestion` → `AI_USE` (operate) · staff
- `getConfigurationBlueprint` → `AI_USE` (operate) · staff
- `decideBlueprintRecommendation` → `AI_USE` (operate) · staff
- `attachConfigurationSource` → `AI_USE` (operate) · staff
- `listConfigurationSources` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.3.31 | System shall allow administrators to upload event briefs, brochures, schedules, PDFs or spreadsheets and use AI to automatically generate event configurations, sessions, ticket types, capacities … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |
| 1.4.21 | System shall allow administrators to upload spreadsheets, brochures, PDFs or existing catalogues and automatically generate products, pricing structures, rules, entitlements and configurations using … | Ticketing Catalogue | CONTRACTED | `attachConfigurationSource` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-477` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-477`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 16: Works in Missing Information & Clarification Center → Allow AI to identify incomplete, contradictory, ambiguous, or logically inconsistent requirements before producing the final blueprint.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-477?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-469`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-478` Configuration Blueprint & Dependency Map

**Convert the entire AI conversation into a structured configuration blueprint that can be reviewed before moving to Board 2. This is the final output of Board 1. Nothing should yet be created in production.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `sessionId` (session) |
| Route | `/platform/configuration-blueprint-dependency-map-adm-478` |

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

**Data it reads**: `getConfigurationBlueprint` (onLoad, The blueprint so far)

**Where the user goes next**

- → `ADM-469` AI Configuration Home & Start: *Back to AI Configuration Home & Start*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The blueprint dependency map list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the blueprint dependency map untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No blueprint dependency map yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the blueprint dependency map are still there. The pack's own statuses are Blueprint Ready — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The blueprint is not ready: a required decision is open or deferred (AIC-115). |

#### Permissions

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-478` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS09 AI Configuration Assistant Board 1.dc.html#adm-478`
- Workshop pack: AI_Configuration_Assistant_Reference.pdf board 1
- Flow F225 *AI Configuration Assistant board 1: AI Configuration Home & Start*, step 18: Works in Configuration Blueprint & Dependency Map → Convert the entire AI conversation into a structured configuration blueprint that can be reviewed before moving to Board 2. This is the final output of Board 1. Nothing should yet be created in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-478?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-469`.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"answerConfigurationQuestion": {"method":"POST","path":"/configuration-sessions/{sessionId}/answers","contract":"ai","summary":"Answer the current question","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConfigurationTurn"},
"attachConfigurationSource": {"method":"POST","path":"/configuration-sessions/{sessionId}/sources","contract":"ai","summary":"Seed a configuration session from an uploaded document","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"buildConfigurationPlan": {"method":"POST","path":"/configuration-sessions/{sessionId}/plan","contract":"ai","summary":"Compile the blueprint into a plan","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlanDetail"},
"decideBlueprintRecommendation": {"method":"POST","path":"/configuration-sessions/{sessionId}/decisions/{decisionKey}","contract":"ai","summary":"Accept, modify, reject or defer a blueprint decision","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiBlueprintDecision"},
"getConfigurationBlueprint": {"method":"GET","path":"/configuration-sessions/{sessionId}/blueprint","contract":"ai","summary":"The blueprint so far","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":null},{"name":"decisionClass","in":"query","required":null}],"requestBody":null,"responds":"AiBlueprintView"},
"listConfigurationSessions": {"method":"GET","path":"/configuration-sessions","contract":"ai","summary":"Configuration-assistant sessions","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"intent","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConfigurationSources": {"method":"GET","path":"/configuration-sessions/{sessionId}/sources","contract":"ai","summary":"Documents attached to a configuration session","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"startConfigurationSession": {"method":"POST","path":"/configuration-sessions","contract":"ai","summary":"Start the configuration assistant","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiConfigurationSession"}
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
"AiConfigurationQuestion": {"type":"object","x-ticvai-persistence":"none — chosen per turn from the configuration knowledge model","description":"**The next question, chosen by the configuration knowledge model, not by the language model** (design 2.2 D, AIC-111). The model only extracts a structured answer against `answerSchema`.","required":["questionKey","text","decisionClass"],"properties":{"questionKey":{"type":"string"},"text":{"type":"string"},"module":{"type":"string","nullable":true},"decisionClass":{"type":"string","enum":["required","recommended","optional"]},"answerType":{"type":"string","enum":["freeText","singleChoice","multiChoice","number","date","confirm"]},"options":{"type":"array","items":{"type":"string"}},"why":{"type":"string","nullable":true,"description":"Why it is asked: which configuration branch it opens or closes."},"answerSchema":{"type":"object","additionalProperties":true,"nullable":true,"description":"JSON Schema the extracted answer must satisfy."}}},
"AiConfigurationSession": {"type":"object","x-ticvai-persistence":"ai.config_session","description":"**A configuration-assistant session** (design 2.2 D steps 1-2, C7; ADM-469..478). Discovery runs from the configuration knowledge model; every value carries provenance.","required":["intent","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"intent":{"type":"string","enum":["create","modify","extend","clone"]},"venueType":{"type":"string","nullable":true,"description":"Museum, theme park, water park, zoo, aquarium, theatre, stadium, festival, conference..."},"sourceScopePath":{"type":"string","nullable":true,"description":"The setup being cloned or extended."},"status":{"type":"string","enum":["discovering","blueprintReady","planned","executing","completed","abandoned"],"readOnly":true},"progressPercent":{"type":"integer","minimum":0,"maximum":100,"readOnly":true},"nextQuestion":{"allOf":[{"$ref":"#/components/schemas/AiConfigurationQuestion"}],"nullable":true,"readOnly":true},"conversationId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.conversation"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan"},"locale":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"lastActivityAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiConfigurationSource": {"type":"object","x-ticvai-persistence":"ai.config_source","description":"**A document attached to a configuration session** (1.3.31, 1.4.21, 2.6.50): the uploaded asset, what kind of source it is, and how its extraction went. The values it yields are blueprint decisions with provenance `inferred` and a citation back here. **Scoped through its session** (`platform.apply_parent_rls`).","required":["sessionId","assetId","sourceKind","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"sessionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.config_session"},"assetId":{"type":"string","format":"uuid","x-ticvai-references":"assets.MediaAsset"},"sourceKind":{"type":"string","enum":["brief","brochure","catalogue","priceList","spreadsheet","brandAsset"]},"note":{"type":"string","nullable":true},"status":{"type":"string","enum":["extracting","extracted","partial","failed"],"readOnly":true},"pageCount":{"type":"integer","nullable":true,"readOnly":true},"valuesExtracted":{"type":"integer","readOnly":true,"description":"Questions it pre-answered."},"unreadRegions":{"type":"array","items":{"type":"string"},"readOnly":true,"description":"Pages or regions it could not read, named so a person can answer by hand."},"attachedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"attachedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"AiConfigurationTurn": {"type":"object","x-ticvai-persistence":"none — the answer is written to ai.blueprint_decision and the session","description":"The result of one answer: what was extracted with its provenance, the next question and progress.","required":["session"],"properties":{"session":{"$ref":"#/components/schemas/AiConfigurationSession"},"extracted":{"type":"array","items":{"type":"object","properties":{"decisionKey":{"type":"string"},"value":{"type":"object","additionalProperties":true,"nullable":true},"provenance":{"$ref":"#/components/schemas/AiProvenance"}}}},"nextQuestion":{"allOf":[{"$ref":"#/components/schemas/AiConfigurationQuestion"}],"nullable":true},"clarificationsNeeded":{"type":"array","items":{"type":"string"}}}},
"AiProvenance": {"type":"string","enum":["confirmed","aiRecommended","inferred","unknown"],"description":"**Where a configuration value came from** (design 2.2 D, AIC-111): said by the administrator, recommended by the assistant, inferred from other answers, or not known yet. Shown beside every value; no confidence number is shown for configuration (design 5.6)."},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
