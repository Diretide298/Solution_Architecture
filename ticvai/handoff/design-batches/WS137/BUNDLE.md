# WS137 — Marketing CRM Configuration Reference v1.0 board 3

**10 screens · 11 operations · 13 schemas · 4 permissions**

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
  `AI_USE, MARKETING_MANAGE, MARKETING_VIEW, PRICE_VIEW`. A control nobody can use must say so,
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
| `BO-754` | Audience Intelligence | B–D | 0 | 0 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `BO-755` | Dynamic Segment Builder | A | 0 | 0 | 6 | 12 | 1 | 6 | — | notStarted (—) |
| `BO-756` | Static Lists & Imports | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-757` | Behavioral Segmentation | B–D | 0 | 0 | 6 | 9 | 1 | 6 | — | notStarted (—) |
| `BO-758` | Membership & Loyalty Segments | B–D | 0 | 0 | 6 | 9 | 1 | 6 | — | notStarted (—) |
| `BO-759` | Demographic & Geographic | B–D | 0 | 0 | 6 | 9 | 0 | 0 | — | notStarted (—) |
| `BO-760` | Revenue & Engagement Segments | B–D | 0 | 0 | 6 | 9 | 0 | 6 | — | notStarted (—) |
| `BO-761` | AI Audience Discovery | B–D | 0 | 0 | 6 | 3 | 0 | 0 | — | notStarted (—) |
| `BO-762` | Predictive Audiences | B–D | 0 | 0 | 6 | 14 | 0 | 0 | — | notStarted (—) |
| `BO-763` | Activation & Governance | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-754, BO-755, BO-756, BO-757, BO-758, BO-759, BO-760, BO-761, BO-762 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-754` Audience Intelligence

**Give marketers and CRM teams an overview of addressable audience health. Show total guests, reachable guests, active segments, consent-eligible audience, high-value and churn-risk populations. Visualize growth, overlap, duplication, suppression and reachability by channel, brand, venue and region. Identify stale, shrinking, high-performing or conflicting audiences and link to the responsible definitions. Provide explainable AI observations without modifying or activating segments automatically. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/audience-intelligence-bo-754` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Segments | text field | — | — | `getAudienceOverlap` ?segmentIds |
| Channel | text field | — | — | `getAudienceOverlap` ?channel |
| Search | text field | — | max length 200 | `listSegments` ?search |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `getAudienceOverlap` (onLoad, Reachability and overlap); `listSegments` (onLoad, Active segments)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-755` Dynamic Segment Builder: *Dynamic Segment Builder*; carries `segmentId`
- → `BO-756` Static Lists & Imports: *Static Lists & Imports*
- → `BO-757` Behavioral Segmentation: *Behavioral Segmentation*
- → `BO-758` Membership & Loyalty Segments: *Membership & Loyalty Segments*
- → `BO-759` Demographic & Geographic: *Demographic & Geographic*
- → `BO-760` Revenue & Engagement Segments: *Revenue & Engagement Segments*
- → `BO-761` AI Audience Discovery: *AI Audience Discovery*
- → `BO-762` Predictive Audiences: *Predictive Audiences*; carries `segmentId`
- → `BO-763` Activation & Governance: *Activation & Governance*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audience intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audience intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audience intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audience intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getAudienceOverlap` → `MARKETING_VIEW` (read) · staff
- `listSegments` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.14.25 | Segmentation & Attribution Audit Trail | Marketing & CRM | CONTRACTED | `listSegments` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-754` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-754`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 1: Opens Audience Intelligence → Give marketers and CRM teams an overview of addressable audience health. Show total guests, reachable guests, active segments, consent-eligible audience, high-value and churn-risk populations. …
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F246 branch at step 1 (expected): when Nothing has been set up on Audience Intelligence yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F246 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-754?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-755`, `BO-756`, `BO-757`, `BO-758`, `BO-759`, `BO-760`, `BO-761`, `BO-762`, `BO-763`.
- [ ] Every gated control is gated: `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-755` Dynamic Segment Builder

**Allow authorized users to create automatically refreshed rule-based audiences. Provide nested AND/OR/NOT logic across profile, behavior, transaction, membership, loyalty, wallet and custom attributes. Show live audience count, reachable count, exclusions, consent impact and representative sample guests while rules are edited. Support effective dates, refresh frequency, ownership, tags, descriptions, approvals and reusable rule groups. Validate incompatible conditions, excessive complexity and restricted attributes before save or activation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | Block A · ticket #20765 (APP-SETUP-BO-755) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `segmentId` (navigation) |
| Route | `/engagement-support/dynamic-segment-builder-bo-755` |

**Known gaps.** **Dynamic Segment Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The dynamic segment list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the dynamic segment untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No dynamic segment yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the dynamic segment are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes |

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff
- `previewSegment` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.1.6 | Audience Selection | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.3 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.4 | Audience Targeting | Marketing & CRM | CONTRACTED | `previewSegment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic segment builder supports rule-based segments (purchase value bands, product-specific purchases, recency); static lists import from CSV/Excel for migration; behavioural segments (cart-abandon, app session, campaign-open, survey-completed) feed marketing automation. *(client request · MoM 20 Aug 2026, 4.4 Audience Segmentation, Behavioural Analytics & Data Migration · DI-381)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-755` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-755`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 2: Works in Dynamic Segment Builder → Allow authorized users to create automatically refreshed rule-based audiences. Provide nested AND/OR/NOT logic across profile, behavior, transaction, membership, loyalty, wallet and custom …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-755?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-756` Static Lists & Imports

**Manage governed fixed audiences and externally supplied lists. Create lists manually or through secure file import with field mapping, validation, deduplication and error handling. Configuration Scope of Work / Version 1.0 16 Match imported members to the Customer Master and control whether unmatched records may create leads or remain quarantined. Record source, owner, purpose, consent basis, expiry, refresh history and file provenance. Support additions, removals, suppression and export under RBAC/PBAC and audit controls. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/static-lists-imports-bo-756` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Import audience list (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAudienceLists` (onLoad, Lists held)

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The static lists imports list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the static lists imports untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No static lists imports yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the static lists imports are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `importAudienceList` → `MARKETING_MANAGE` (configure) · staff
- `listAudienceLists` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic segment builder supports rule-based segments (purchase value bands, product-specific purchases, recency); static lists import from CSV/Excel for migration; behavioural segments (cart-abandon, app session, campaign-open, survey-completed) feed marketing automation. *(client request · MoM 20 Aug 2026, 4.4 Audience Segmentation, Behavioural Analytics & Data Migration · DI-381)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-756` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-756`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 4: Works in Static Lists & Imports → Manage governed fixed audiences and externally supplied lists. Create lists manually or through secure file import with field mapping, validation, deduplication and error handling. Configuration …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-756?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Import audience list, Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-757` Behavioral Segmentation

**Build audiences from observable guest activity. Use purchase, visit, ticket scan, reservation, cart, app, web, campaign, chatbot, survey and review events. Support recency, frequency, count, value, sequence, absence-of-event and time-window conditions. Preview top behaviors, sources and data freshness and exclude bot, employee, test or fraudulent activity. Refresh segments through event streams and expose rule/version provenance for each inclusion. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/behavioral-segmentation-bo-757` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The behavioral segmentation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the behavioral segmentation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No behavioral segmentation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the behavioral segmentation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes |

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Dynamic segment builder supports rule-based segments (purchase value bands, product-specific purchases, recency); static lists import from CSV/Excel for migration; behavioural segments (cart-abandon, app session, campaign-open, survey-completed) feed marketing automation. *(client request · MoM 20 Aug 2026, 4.4 Audience Segmentation, Behavioural Analytics & Data Migration · DI-381)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-757` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-757`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 6: Works in Behavioral Segmentation → Build audiences from observable guest activity. Use purchase, visit, ticket scan, reservation, cart, app, web, campaign, chatbot, survey and review events. Support recency, frequency, count, value …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-757?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-758` Membership & Loyalty Segments

**Create audiences using membership, loyalty and wallet state. Filter by membership type, status, start, expiry, renewal, freeze, benefit use and upgrade eligibility. Filter by loyalty tier, points, earn/redemption history, reward use, milestone and tier movement. Use wallet balance, top-up, spend, low-balance and dormancy conditions while protecting financial data. Combine these signals with profile and behavior rules and show reachable audience before activation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/membership-loyalty-segments-bo-758` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The membership loyalty segments list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the membership loyalty segments untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No membership loyalty segments yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the membership loyalty segments are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes |

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- **Open question.** Loyalty accrues points by product/spend tier (e.g. bronze/silver/gold thresholds) and unlocks tier benefits (e.g. platinum-tier discounts on F&B and ticketing). Full programme configuration (tiers, points, redemption, expiry) pending a dedicated session. *(open · MoM 20 Aug 2026, 4.5 Loyalty, Membership & Wallet · DI-382)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A94** Hold the loyalty workshop and define the full programme configuration (tiers, point accrual, redemption, expiry, benefit unlocks) *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'loyalty')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A134** Build the eligibility rules engine (residency/nationality with ID capture, minimum age by DOB, VIP-only profiles, loyalty-points thresholds, purchase limits per order/guest/category/channel) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 25 Aug 2026 · workshop tracker · keyword 'loyalty')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-758` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-758`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 8: Works in Membership & Loyalty Segments → Create audiences using membership, loyalty and wallet state. Filter by membership type, status, start, expiry, renewal, freeze, benefit use and upgrade eligibility. Filter by loyalty tier, points …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-758?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-759` Demographic & Geographic

**Configure demographic and location-based audiences responsibly. Use age band, household, language, country, city, postcode, visitor type, nationality where lawful and custom demographics. Support location radius, venue proximity, travel market, timezone and resident/tourist classification. Display consent, fairness, minimum-audience and restricted-attribute warnings before use. Allow jurisdiction-specific field availability and prevent prohibited sensitive targeting. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/demographic-geographic-bo-759` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The demographic geographic list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the demographic geographic untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No demographic geographic yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the demographic geographic are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes |

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-759` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-759`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 10: Works in Demographic & Geographic → Configure demographic and location-based audiences responsibly. Use age band, household, language, country, city, postcode, visitor type, nationality where lawful and custom demographics. Support …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-759?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-760` Revenue & Engagement Segments

**Create value- and engagement-based audiences. Configuration Scope of Work / Version 1.0 17 Use total revenue, LTV, average order value, purchase frequency, category spend, refund behavior and propensity. Use engagement score, campaign interaction, app activity, visit frequency, inactivity and product affinity. Define bands, percentiles, scoring periods and calculation sources and preview distribution before publishing. Protect against circular attribution and record the data snapshot and scoring version used. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/revenue-engagement-segments-bo-760` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The revenue engagement segments list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the revenue engagement segments untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No revenue engagement segments yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the revenue engagement segments are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes |

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A92** Build audience segmentation (rule-based dynamic segments, CSV/Excel list import, Google Analytics behavioural tracking into native reporting) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'segmentation')*
- **A93** Hold the data-migration workshop and define customer/segment import formats and validation rules *(Allam / Chinmay Parab · High · Not started → 30 Sep: Closed, Rolled into S14 (weekly tracker) · 20 Aug 2026 · workshop tracker · keyword 'segment')*
- **A95** Design marketing automation (campaign attribution with success criteria, Offers module, Visual Journey Builder referencing pre-configured offers only) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 20 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A139** Build donation campaigns (fixed or variable, per channel, per product or global, separate account code) and confirm VAT treatment *(Chinmay Parab · Medium · With client → 30 Sep: Closed, Moved to T2 (TICVAI to act) · 25 Aug 2026 · workshop tracker · keyword 'campaign')*
- **A195** Build the pricing foundation (price lists per channel/segment/category, price categories and rate types, rate structure, product association, bundle pricing, multi-market and multi-currency pricing, list cloning … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'segment')*
- **A196** Build the pricing rules layer (segment, membership, residency/market, channel, venue/event, tiered volume bands, time-slot pricing) with a conflict-surfacing overview *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 1 Sep 2026 · workshop tracker · keyword 'segment')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-760` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-760`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 12: Works in Revenue & Engagement Segments → Create value- and engagement-based audiences. Configuration Scope of Work / Version 1.0 17 Use total revenue, LTV, average order value, purchase frequency, category spend, refund behavior and …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-760?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-761` AI Audience Discovery

**Discover meaningful customer clusters using explainable AI. Present suggested clusters with dominant traits, size, reachability, value, engagement and observed opportunity. Show contributing variables, confidence, stability, bias/fairness checks and excluded sensitive attributes. Allow users to inspect sample profiles and convert a recommendation into an editable governed segment. Require human approval and retain feedback, model/version and final segment definition. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `PRICE_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/ai-audience-discovery-bo-761` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAudienceDiscoveryTargeting` (onLoad, AI Audience Discovery & Targeting Optimization)

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The audience discovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the audience discovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No audience discovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the audience discovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 Neither seed was sent (`seed-required`), or the seed has fewer than 50 consented guests (`seed-too-small`). |

#### Permissions

- `listAudienceDiscoveryTargeting` → `PRICE_VIEW` (read) · staff
- `proposeLookalikeSegment` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.6.31 | System shall provide customer-segment-based discount recommendations. | Unified Operations Dashboard | CONTRACTED | `listAudienceDiscoveryTargeting` |
| 22.14.11 | AI Audience Discovery | Marketing & CRM | CONTRACTED | `listAudienceDiscoveryTargeting` |
| 22.14.12 | AI Lookalike Audiences | Marketing & CRM | CONTRACTED | `proposeLookalikeSegment` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-761` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-761`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 14: Works in AI Audience Discovery → Discover meaningful customer clusters using explainable AI. Present suggested clusters with dominant traits, size, reachability, value, engagement and observed opportunity. Show contributing …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-761?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `AI_USE`, `PRICE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-762` Predictive Audiences

**Create model-based audiences for future behavior and opportunity. Support lookalike, churn, reactivation, membership upgrade, next purchase and high-value propensity audiences. Display prediction window, threshold, audience size, confidence, lift and primary model factors. Allow threshold simulation and exclusions and monitor drift, performance and fairness after activation. Never use predictive status to override consent, eligibility, pricing, capacity or service policies. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `MARKETING_MANAGE`, `MARKETING_VIEW` (1 operate, 1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `segmentId` (navigation), `actionId` (navigation) |
| Route | `/engagement-support/predictive-audiences-bo-762` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create segment (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The predictive audiences list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the predictive audiences untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No predictive audiences yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the predictive audiences are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Criteria are contradictory or reference unknown attributes; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 422 Neither seed was sent (`seed-required`), or the seed has fewer than 50 consented guests (`seed-too-small`). |

#### Permissions

- `createSegment` → `MARKETING_MANAGE` (configure) · staff
- `previewSegment` → `MARKETING_VIEW` (read) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff
- `proposeLookalikeSegment` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

14 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.4.5 | The Customer categories or Segments can be described in segments with 3 possible levels such as BtoC / BtoB, Individual / Groups. | F&B POS | CONTRACTED | `createSegment` |
| 22.2.10 | Guest Segmentation Attributes | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.1 | Audience Segmentation Engine | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.2 | Dynamic Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.3 | Static Segments | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.4 | Behavioral Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.6 | Membership Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.7 | Loyalty Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.14.9 | Revenue-Based Segmentation | Marketing & CRM | CONTRACTED | `createSegment` |
| 22.1.6 | Audience Selection | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.3 | Dynamic Personalization | Marketing & CRM | CONTRACTED | `previewSegment` |
| 22.4.4 | Audience Targeting | Marketing & CRM | CONTRACTED | `previewSegment` |
| … 2 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-762` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-762`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 16: Works in Predictive Audiences → Create model-based audiences for future behavior and opportunity. Support lookalike, churn, reactivation, membership upgrade, next purchase and high-value propensity audiences. Display prediction …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-762?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create segment, Cancel.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `AI_USE`, `MARKETING_MANAGE`, `MARKETING_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-763` Activation & Governance

**Control where audiences are used and how they remain compliant. Activate to campaigns, journeys, website, mobile app and approved external platforms through secured connectors. Configure suppression, consent enforcement, frequency limits, destination mapping, refresh schedule and expiry. Require approval for sensitive, high-volume or external activation and provide a pre-flight impact summary. Configuration Scope of Work / Version 1.0 18 Track synchronization, failures, member counts, destination use, versions and the complete activation audit trail. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work / Version 1.0 19 Board 4 - Campaign Management & Attribution Figure 4. High-definition configuration board with all 10 screens. Configuration Scope of Work / Version 1.0 20**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Engagement & Support · wave 3 · needs the `marketing` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MARKETING_MANAGE`, `MARKETING_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/engagement-support/activation-governance-bo-763` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listAudienceActivations` (onLoad, Where audiences are in use)

**Where the user goes next**

- → `BO-754` Audience Intelligence: *Back to Audience Intelligence*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The activation governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the activation governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No activation governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the activation governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Blocked by consent, volume or approval |

#### Permissions

- `activateAudience` → `MARKETING_MANAGE` (configure) · staff
- `listAudienceActivations` → `MARKETING_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-763` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS72 Marketing CRM Configuration Reference v1.0 Board 3.dc.html#bo-763`
- Workshop pack: Marketing_CRM_Configuration_Reference v1.0.pdf board 3
- Flow F246 *Marketing CRM Configuration Reference v1.0 board 3: Audience Intelligence*, step 18: Works in Activation & Governance → Control where audiences are used and how they remain compliant. Activate to campaigns, journeys, website, mobile app and approved external platforms through secured connectors. Configure suppression …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-763?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, What publishing changes.
- [ ] Every transition is wired: `BO-754`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`, `MARKETING_VIEW`.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"activateAudience": {"method":"POST","path":"/audience-activations","contract":"marketing-crm","summary":"Push an audience to a campaign, journey or external platform","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AudienceActivation","responds":null},
"createSegment": {"method":"POST","path":"/segments","contract":"marketing-crm","summary":"Create a segment","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateSegmentRequest","responds":"Segment"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"getAudienceOverlap": {"method":"GET","path":"/audience-overlap","contract":"marketing-crm","summary":"How much audiences overlap, and how many are reachable","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"segmentIds","in":"query","required":true},{"name":"channel","in":"query","required":null}],"requestBody":null,"responds":"AudienceOverlap"},
"importAudienceList": {"method":"POST","path":"/audience-lists","contract":"marketing-crm","summary":"Load a supplied list, matched against the guest master","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AudienceList","responds":"AudienceList"},
"listAudienceActivations": {"method":"GET","path":"/audience-activations","contract":"marketing-crm","summary":"Where audiences are being used, and whether they are still in sync","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAudienceDiscoveryTargeting": {"method":"GET","path":"/audience-discovery-targeting","contract":"promotions","summary":"AI Audience Discovery & Targeting Optimization","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiAudienceDiscoveryTargetingOptimizationView"},
"listAudienceLists": {"method":"GET","path":"/audience-lists","contract":"marketing-crm","summary":"Static and imported audiences","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSegments": {"method":"GET","path":"/segments","contract":"marketing-crm","summary":"List segments","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"search","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"previewSegment": {"method":"POST","path":"/segments/{segmentId}/preview","contract":"marketing-crm","summary":"Estimate segment size and reachability","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SegmentPreview"},
"proposeLookalikeSegment": {"method":"POST","path":"/ai/segment-suggestions","contract":"ai","summary":"Propose a lookalike segment from a seed, for a person to save","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiLookalikeSegmentProposal"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAudienceDiscoveryTargetingOptimizationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What AI Audience Discovery & Targeting Optimization displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"narrowAudience":{"type":"string","description":"Narrow audience"},"expandAudience":{"type":"string","description":"Expand audience"},"excludeLowValueSegment":{"type":"string","description":"Exclude low-value segment"},"changeEligibility":{"type":"string","description":"Change eligibility"},"changeChannel":{"type":"string","description":"Change channel"},"changeTiming":{"type":"string","description":"Change timing"},"changePromotion":{"type":"string","description":"Change promotion"},"reduceFrequency":{"type":"string","description":"Reduce frequency"},"membershipTierEligibility":{"type":"string","description":"Membership/tier eligibility"},"membershipAndLoyaltyEligibility":{"type":"string","description":"Membership and loyalty eligibility"},"audienceName":{"type":"string","description":"Discovered audience"},"audienceSize":{"type":"integer","description":"Audience size"},"suggestedOffer":{"type":"string","description":"Suggested offer"},"predictedConversion":{"type":"number","description":"Predicted conversion, percent"},"estimatedIncrementalRevenue":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Estimated incremental revenue"},"rationale":{"type":"string","description":"Why this audience (explainable factors)"}}},
"AiLookalikeSegmentProposal": {"type":"object","x-ticvai-persistence":"none — the draft is an ai.proposed_action row (kind audience); the evidence is its decision record","description":"A lookalike segment as rules a person can read, edit and save (22.14.12). The criteria are shaped as `marketing-crm` `SegmentCriterion` (attribute, operator, value) and restated here because a satellite cannot reference another satellite.","required":["proposedActionId","criteria","estimatedReach"],"properties":{"proposedActionId":{"type":"string","format":"uuid","description":"The `ai.proposed_action` row whose payload is the `marketing-crm.createSegment` body."},"name":{"type":"string","nullable":true},"criteria":{"type":"array","items":{"type":"object","required":["attribute","operator"],"properties":{"attribute":{"type":"string"},"operator":{"type":"string"},"value":{"description":"As `SegmentCriterion.value` in marketing-crm (any type)."},"weight":{"type":"number","nullable":true,"description":"How much this attribute separated the seed from everyone else."}}}},"similarityBasis":{"type":"array","items":{"type":"object","properties":{"attribute":{"type":"string"},"seedShare":{"type":"number","description":"Share of the seed holding the value."},"populationShare":{"type":"number","description":"Share of the tenant's consented guests holding it."}}}},"estimatedReach":{"type":"integer","description":"Consented guests the criteria select, excluding the seed where `excludeSeed`."},"seedSize":{"type":"integer"},"overlapWithSeed":{"type":"number","minimum":0,"maximum":1,"description":"Share of the seed the criteria would also select; a check that the rules describe the seed."},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"decisionRecordId":{"type":"string","format":"uuid"}}},
"AudienceActivation": {"type":"object","x-ticvai-persistence":"marketing.audience_activation","description":"Board 3.10. **Consent is enforced at activation, not at definition.**","required":["segmentId","destination"],"properties":{"id":{"type":"string","format":"uuid"},"segmentId":{"type":"string","format":"uuid"},"destination":{"type":"string","enum":["campaign","journey","website","mobileApp","externalAdPlatform","partnerFeed"]},"destinationReference":{"type":"string","nullable":true},"external":{"type":"boolean","default":false},"suppressionListIds":{"type":"array","items":{"type":"string","format":"uuid"}},"enforceConsent":{"type":"boolean","default":true},"frequencyCapPerWeek":{"type":"integer","nullable":true},"refreshSchedule":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date","nullable":true},"preFlight":{"type":"object","readOnly":true,"properties":{"members":{"type":"integer"},"reachable":{"type":"integer"},"suppressed":{"type":"integer"},"consentBlocked":{"type":"integer"},"frequencyBlocked":{"type":"integer"}}},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"status":{"type":"string","enum":["draft","pendingApproval","active","failed","expired"]},"lastSyncedAt":{"type":"string","format":"date-time","nullable":true},"lastSyncErrors":{"type":"integer","default":0},"scopePath":{"type":"string"}}},
"AudienceList": {"type":"object","x-ticvai-persistence":"marketing.audience_list","description":"Board 3.3. **Consent basis is required on the import, not optional metadata.**","required":["name"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","enum":["manual","imported","suppression"]},"assetId":{"type":"string","format":"uuid","nullable":true},"fieldMapping":{"type":"object","additionalProperties":{"type":"string"}},"rowsRead":{"type":"integer","readOnly":true},"matched":{"type":"integer","readOnly":true},"unmatched":{"type":"integer","readOnly":true},"duplicatesRemoved":{"type":"integer","readOnly":true},"rejected":{"type":"integer","readOnly":true},"unmatchedHandling":{"type":"string","enum":["createLead","quarantine"],"default":"quarantine","description":"**The two honest answers.** Silently dropping them tells a marketer their list of ten thousand reached ten thousand.\n"},"source":{"type":"string"},"owner":{"type":"string","format":"uuid"},"purpose":{"type":"string"},"consentBasis":{"type":"string"},"expiresAt":{"type":"string","format":"date","nullable":true},"scopePath":{"type":"string"}}},
"AudienceOverlap": {"type":"object","description":"Board 3.1. **Reachable is always smaller, and it is the number that matters.**","properties":{"segments":{"type":"array","items":{"type":"object","properties":{"segmentId":{"type":"string","format":"uuid"},"name":{"type":"string"},"members":{"type":"integer"},"reachable":{"type":"integer"},"suppressed":{"type":"integer"},"consentBlocked":{"type":"integer"},"duplicates":{"type":"integer"}}}},"pairwiseOverlap":{"type":"array","items":{"type":"object","properties":{"segmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"shared":{"type":"integer"},"sharedPercent":{"type":"number"}}}},"totalUnique":{"type":"integer"},"totalReachable":{"type":"integer"}}},
"CreateSegmentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","criteria"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid"},"match":{"type":"string","enum":["all","any"],"default":"all"},"criteria":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/SegmentCriterion"}},"excludeSegmentIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"Segment": {"x-ticvai-persistence":"marketing.segment + marketing.segment_criterion","allOf":[{"$ref":"#/components/schemas/CreateSegmentRequest"},{"type":"object","required":["id","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"lastEvaluatedSize":{"type":"integer","nullable":true},"lastEvaluatedAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"}}}]},
"SegmentCriterion": {"x-ticvai-persistence":"marketing.segment_criterion","type":"object","required":["attribute","operator"],"properties":{"attribute":{"type":"string","description":"Behavioural or profile attribute — visit count, last visit, lifetime value, product purchased, membership tier, venue visited, language.\n**Free-form rather than an enum, which is why 22.14.8, 5.3.19 and 5.5.17b were readable as gaps and are not.** `walletBalance`, `engagementTier` and `portfolioScope` are expressible today; what was missing was anybody saying so.\n**Three that need saying, because the naive reading is wrong:**\n`walletBalance` should segment on **`cash` credit only**. A guest with 200 dirhams of promotional credit expiring Friday is a different campaign from one with 200 of their own money, and treating them alike sends a spend-it-now message to somebody who was given it.\n`walletBalance.expiringWithinDays` is the segment that earns the attribute — **credit about to expire unspent is a guest about to be disappointed and a venue about to book breakage**, and only one of those is worth a message.\n`portfolioScope` aggregates across a `DelegatedAccess` delegation (CF-132) and **must not message every member about a household total** — that is how a venue tells a teenager what their parent spends.\n`entitlementExpiringWithinDays` (29 September, build pass, group G2; 5.5.30): the guest holds a ticket or pass in `issued` or `partiallyConsumed` whose `validTo` is within that many days, kept current from `entitlement.expiringSoon` and the entitlement read model. **Unused passes about to lapse** are this attribute with `entitlementRemainingUses` greater than zero.\n"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","exists","notExists","withinDays"]},"value":{},"values":{"type":"array","items":{}}}},
"SegmentPreview": {"x-ticvai-persistence":"none — evaluated live","type":"object","required":["segmentId","matchingCount","reachable"],"properties":{"segmentId":{"type":"string","format":"uuid"},"matchingCount":{"type":"integer"},"reachable":{"type":"array","description":"Per channel, after consent and suppression. A segment of 50,000 with 3,000 email consents is a 3,000-person campaign.\n","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/MessageChannel"},"reachableCount":{"type":"integer"},"excludedNoConsent":{"type":"integer"},"excludedSuppressed":{"type":"integer"},"excludedNoAddress":{"type":"integer"}}}},"evaluatedAt":{"type":"string","format":"date-time"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]}
}
```
