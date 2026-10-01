# WS115 — ACCREDITATION board 8

**10 screens · 10 operations · 11 schemas · 4 permissions**

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
  `ACCREDITATION_VIEW, DEVELOPER_MANAGE, DEVELOPER_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `BO-684` | Accreditation Executive Dashboard | B–D | 0 | 14 | 6 | 3 | 1 | 6 | — | notStarted (—) |
| `BO-685` | Accreditation Status & Portfolio Reporting | B–D | 0 | 0 | 6 | 3 | 1 | 6 | — | notStarted (—) |
| `BO-686` | Accreditation Utilization Analytics | B–D | 0 | 22 | 6 | 3 | 1 | 6 | — | notStarted (—) |
| `BO-687` | Accreditation Access Activity Reporting | B–D | 0 | 0 | 6 | 3 | 0 | 6 | — | notStarted (—) |
| `BO-688` | Accreditation Trend & Comparative Analysis | B–D | 4 | 19 | 6 | 0 | 1 | 6 | — | notStarted (—) |
| `BO-689` | Accreditation Audit Reporting | B–D | 0 | 0 | 6 | 2 | 0 | 6 | — | notStarted (—) |
| `BO-690` | Immutable Accreditation Audit Log | B–D | 14 | 0 | 6 | 2 | 0 | 6 | — | notStarted (—) |
| `BO-691` | Accreditation API Management | B–D | 0 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-692` | Accreditation Webhook Management | B–D | 8 | 0 | 6 | 0 | 0 | 6 | — | notStarted (—) |
| `BO-693` | Integration & Data Exchange Monitor | B–D | 0 | 0 | 6 | 2 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-684, BO-685, BO-686, BO-687, BO-689, BO-691, BO-693 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-684` Accreditation Executive Dashboard

**Provide management with a real-time overview of the complete accreditation operation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW`, `REPORT_VIEW_VENUE` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Dashboard filters shall include) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-executive-dashboard-bo-684` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationHolders` ?programmeId |
| Organisation | picker: choose an organisation | — | — | `listAccreditationHolders` ?organisationId |
| Status | text field | — | — | `listAccreditationHolders` ?status |
| Expiring within days | number field (days) | — | — | `listAccreditationHolders` ?expiringWithinDays |
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every accreditation executive** (data table)

| Shows | Format | Notes |
|---|---|---|
| Tenant | text | not in the schema: `Tenant` |
| Event | text | not in the schema: `Event` |
| Venue | text | not in the schema: `Venue` |
| Accreditation program | text | not in the schema: `Accreditation program` |
| Category | text | not in the schema: `Category` |
| Organization | text | not in the schema: `Organization` |
| Date range | text | not in the schema: `Date range` |

**The selected accreditation executive** (detail panel): The pack groups this record's detail under its own headings: “Scope of Work”, “Visualizations should include”, “Key requirements”.

| Shows | Format | Notes |
|---|---|---|
| Tenant | text | not in the schema: `Tenant` |
| Event | text | not in the schema: `Event` |
| Venue | text | not in the schema: `Venue` |
| Accreditation program | text | not in the schema: `Accreditation program` |
| Category | text | not in the schema: `Category` |
| Organization | text | not in the schema: `Organization` |
| Date range | text | not in the schema: `Date range` |

**Data it reads**: `listAccreditationHolders` (onLoad, The executive view); `getKpiValues` (onLoad, Accreditation KPIs (kpiCodes=accreditation*))

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-685` Accreditation Status & Portfolio Reporting: *Accreditation Status & Portfolio Reporting*
- → `BO-686` Accreditation Utilization Analytics: *Accreditation Utilization Analytics*
- → `BO-687` Accreditation Access Activity Reporting: *Accreditation Access Activity Reporting*
- → `BO-688` Accreditation Trend & Comparative Analysis: *Accreditation Trend & Comparative Analysis*
- → `BO-689` Accreditation Audit Reporting: *Accreditation Audit Reporting*
- → `BO-690` Immutable Accreditation Audit Log: *Immutable Accreditation Audit Log*
- → `BO-691` Accreditation API Management: *Accreditation API Management*
- → `BO-692` Accreditation Webhook Management: *Accreditation Webhook Management*
- → `BO-693` Integration & Data Exchange Monitor: *Integration & Data Exchange Monitor*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation executive list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation executive untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation executive yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation executive are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff
- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Accreditation analytics: approvals, upcoming expiries, per-category detail, attended vs issued (e.g. 1,000 passes issued, 700 scanned), and year-over-year or venue-over-venue comparisons. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-665)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-684` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-684`
- Workshop pack: ACCREDITATION.pdf board 8
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 1: Opens Accreditation Executive Dashboard → Provide management with a real-time overview of the complete accreditation operation.
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F224 branch at step 1 (expected): when Nothing has been set up on Accreditation Executive Dashboard yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F224 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-684?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-685`, `BO-686`, `BO-687`, `BO-688`, `BO-689`, `BO-690`, `BO-691`, `BO-692`, `BO-693`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-685` Accreditation Status & Portfolio Reporting

**Report on active, expired, suspended and revoked accreditation records.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW`, `REPORT_VIEW_VENUE` (1 read, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-status-portfolio-reporting-bo-685` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Programme | picker: choose a programme | — | — | `listAccreditationHolders` ?programmeId |
| Organisation | picker: choose an organisation | — | — | `listAccreditationHolders` ?organisationId |
| Status | text field | — | — | `listAccreditationHolders` ?status |
| Expiring within days | number field (days) | — | — | `listAccreditationHolders` ?expiringWithinDays |
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listAccreditationHolders` (onLoad, Status and portfolio); `getKpiValues` (onLoad, Applications by status, active holders by category (groupBy))

**Where the user goes next**

- → `BO-684` Accreditation Executive Dashboard: *Back to Accreditation Executive Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation status portfolio list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation status portfolio untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation status portfolio yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation status portfolio are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `listAccreditationHolders` → `ACCREDITATION_VIEW` (read) · staff
- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.7 | Accreditation Reporting System shall provide reports on active, expired and revoked accreditations. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.47 | Accreditation Dashboard - System shall provide accreditation dashboards. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |
| 12.1.52 | Accreditation API - System shall expose accreditation functionality through APIs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationHolders` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Accreditation analytics: approvals, upcoming expiries, per-category detail, attended vs issued (e.g. 1,000 passes issued, 700 scanned), and year-over-year or venue-over-venue comparisons. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-665)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-685` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-685`
- Workshop pack: ACCREDITATION.pdf board 8
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 2: Works in Accreditation Status & Portfolio Reporting → Report on active, expired, suspended and revoked accreditation records.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-685?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-684`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-686` Accreditation Utilization Analytics

**Determine whether issued accreditations are actually being used.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Metrics shall include) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-utilization-analytics-bo-686` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAccreditationAccessActivity` ?from |
| Holder | picker: choose a holder | — | — | `listAccreditationAccessActivity` ?holderId |
| Zone | picker: choose a zone | — | — | `listAccreditationAccessActivity` ?zoneId |
| Denied only | toggle | — | — | `listAccreditationAccessActivity` ?deniedOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every accreditation utilization analytics** (data table)

| Shows | Format | Notes |
|---|---|---|
| Accreditations issued | text | not in the schema: `Accreditations issued` |
| Accreditations activated | text | not in the schema: `Accreditations activated` |
| Accreditations used | text | not in the schema: `Accreditations used` |
| Never used accreditations | text | not in the schema: `Never-used accreditations` |
| First use date/time | text | not in the schema: `First-use date/time` |
| Last use date/time | text | not in the schema: `Last-use date/time` |
| Number of access transactions | text | not in the schema: `Number of access transactions` |
| Utilization percentage | text | not in the schema: `Utilization percentage` |
| Utilization by category | text | not in the schema: `Utilization by category` |
| Utilization by venue | text | not in the schema: `Utilization by venue` |
| Utilization by event | text | not in the schema: `Utilization by event` |

**The selected accreditation utilization analytics** (detail panel): The pack groups this record's detail under its own headings: “Scope of Work”.

| Shows | Format | Notes |
|---|---|---|
| Accreditations issued | text | not in the schema: `Accreditations issued` |
| Accreditations activated | text | not in the schema: `Accreditations activated` |
| Accreditations used | text | not in the schema: `Accreditations used` |
| Never used accreditations | text | not in the schema: `Never-used accreditations` |
| First use date/time | text | not in the schema: `First-use date/time` |
| Last use date/time | text | not in the schema: `Last-use date/time` |
| Number of access transactions | text | not in the schema: `Number of access transactions` |
| Utilization percentage | text | not in the schema: `Utilization percentage` |
| Utilization by category | text | not in the schema: `Utilization by category` |
| Utilization by venue | text | not in the schema: `Utilization by venue` |
| Utilization by event | text | not in the schema: `Utilization by event` |

**Data it reads**: `listAccreditationAccessActivity` (onLoad, Utilisation)

**Where the user goes next**

- → `BO-684` Accreditation Executive Dashboard: *Back to Accreditation Executive Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation utilization analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation utilization analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation utilization analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation utilization analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAccreditationAccessActivity` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.31 | Access Audit Trail - System shall maintain audit logs of accreditation access activities. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAccessActivity` |
| 12.1.48 | Accreditation Utilization Reporting - System shall provide accreditation utilization reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAccessActivity` |
| 12.1.49 | Accreditation Access Reporting - System shall provide reports on accreditation access activity. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAccessActivity` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Accreditation analytics: approvals, upcoming expiries, per-category detail, attended vs issued (e.g. 1,000 passes issued, 700 scanned), and year-over-year or venue-over-venue comparisons. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-665)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-686` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-686`
- Workshop pack: ACCREDITATION.pdf board 8
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 4: Works in Accreditation Utilization Analytics → Determine whether issued accreditations are actually being used.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-686?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-684`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-687` Accreditation Access Activity Reporting

**Provide detailed reporting of accreditation access activity.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-access-activity-reporting-bo-687` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAccreditationAccessActivity` ?from |
| Holder | picker: choose a holder | — | — | `listAccreditationAccessActivity` ?holderId |
| Zone | picker: choose a zone | — | — | `listAccreditationAccessActivity` ?zoneId |
| Denied only | toggle | — | — | `listAccreditationAccessActivity` ?deniedOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listAccreditationAccessActivity` (onLoad, Access activity)

**Where the user goes next**

- → `BO-684` Accreditation Executive Dashboard: *Back to Accreditation Executive Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation access activity list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation access activity untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation access activity yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation access activity are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAccreditationAccessActivity` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.31 | Access Audit Trail - System shall maintain audit logs of accreditation access activities. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAccessActivity` |
| 12.1.48 | Accreditation Utilization Reporting - System shall provide accreditation utilization reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAccessActivity` |
| 12.1.49 | Accreditation Access Reporting - System shall provide reports on accreditation access activity. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAccessActivity` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-687` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-687`
- Workshop pack: ACCREDITATION.pdf board 8
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 6: Works in Accreditation Access Activity Reporting → Provide detailed reporting of accreditation access activity.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-687?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-684`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-688` Accreditation Trend & Comparative Analysis

**Analyze accreditation behavior over time.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-trend-comparative-analysis-bo-688` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Measures | multi select | — | — | — | — | Sends `?kpiCodes=`; each pack trend is a KPI code. | — |
| Compare | select field | — | — | — | — | Sends `?scopePath=`: event, venue, category or organisation. | — |
| Period | select field | — | — | — | — | Sends `?period=`: daily, weekly, monthly, seasonal or event-level. | — |
| Compare to | select field | — | — | — | — | Sends `?compareTo=` (previousPeriod, samePeriodLastYear, target, benchmark). | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kpis | text field | — | — | `getKpiValues` ?kpiIds |
| Kpi codes | text field | — | — | `getKpiValues` ?kpiCodes |
| Scope path | text field | — | — | `getKpiValues` ?scopePath |
| Period | text field | — | — | `getKpiValues` ?period |
| Compare to | radio group | — | Previous period · Same period last year · Target · Benchmark | `getKpiValues` ?compareTo |
| Interval | radio group | — | Hour · Day · Week · Month | `getKpiValues` ?interval |
| Group by | text field | — | — | `getKpiValues` ?groupBy |

#### Outputs: what the screen shows and produces

**Shown**

**Approval rate** (metric tile, from `getKpiValues`): `kpiCodes` must include an approval-rate code; only takings and admissions are seeded.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Average approval time** (metric tile, from `getKpiValues`): Needs an average-approval-time KPI code, which is not seeded.

| Shows | Format | Notes |
|---|---|---|
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Direction | chip: Up, Down, Flat | — |

**Accreditation trends** (chart, from `getKpiValues`): One point per period; a trend needs one read per period, because `getKpiValues` returns a single period.

| Shows | Format | Notes |
|---|---|---|
| Period | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |

**Comparative analysis** (data table, from `getKpiValues`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Scope path | text | — |
| Period | text | — |
| Value | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Comparison | 1,234.5 | A reading of a metric or KPI, or a threshold on one. A `Money` where the metric is money-valued — `MetricSource` lists those in … |
| Variance percent | 1,234.5 | — |
| Direction | chip: Up, Down, Flat | — |
| Status | chip: Green, Amber, Red, No target | — |
| As of | 1 Oct 2026, 14:30 | — |
| Stale | yes / no (icon or chip) | True when the pipeline behind it has not refreshed. A number nobody flagged as stale is a number somebody will act on. |

**Data it reads**: `getKpiValues` (onLoad, Trend and comparison)

**Where the user goes next**

- → `BO-684` Accreditation Executive Dashboard: *Back to Accreditation Executive Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation trend comparative list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation trend comparative untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation trend comparative yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation trend comparative are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Accreditation analytics: approvals, upcoming expiries, per-category detail, attended vs issued (e.g. 1,000 passes issued, 700 scanned), and year-over-year or venue-over-venue comparisons. *(client request · MoM 7 Sep 2026, 4.7 Notifications, Bulk Operations & Analytics · DI-665)*

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-688` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-688`
- Workshop pack: ACCREDITATION.pdf board 8
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 8: Works in Accreditation Trend & Comparative Analysis → Analyze accreditation behavior over time.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (19 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-688?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-684`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-689` Accreditation Audit Reporting

**Provide compliance and management reporting across accreditation actions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-audit-reporting-bo-689` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationAudit` ?holderId |
| From | date and time picker | — | — | `listAccreditationAudit` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listAccreditationAudit` (onLoad, Audit reporting)

**Where the user goes next**

- → `BO-684` Accreditation Executive Dashboard: *Back to Accreditation Executive Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation audit reporting list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation audit reporting untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation audit reporting yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation audit reporting are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAccreditationAudit` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.51 | Accreditation Audit Reporting - System shall provide accreditation audit reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.58 | Accreditation Audit Logs - System shall maintain immutable accreditation audit logs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-689` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-689`
- Workshop pack: ACCREDITATION.pdf board 8
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 10: Works in Accreditation Audit Reporting → Provide compliance and management reporting across accreditation actions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-689?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-684`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-690` Immutable Accreditation Audit Log

**Maintain the authoritative security record of all accreditation actions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Audit records shall capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/immutable-accreditation-audit-log-bo-690` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Audit ID | select field | — | — | — | — | — | — |
| Timestamp | select field | — | — | — | — | — | — |
| User/service identity | select field | — | — | — | — | — | — |
| Tenant | select field | — | — | — | — | — | — |
| Action | select field | — | — | — | — | — | — |
| Entity type | select field | — | — | — | — | — | — |
| Entity ID | select field | — | — | — | — | — | — |
| Previous value | select field | — | — | — | — | — | — |
| New value | select field | — | — | — | — | — | — |
| Source application/API | select field | — | — | — | — | — | — |
| Correlation/reference ID | select field | — | — | — | — | — | — |
| Result | select field | — | — | — | — | — | — |
| Reason where applicable | select field | — | — | — | — | — | — |
| Key requirement: 12.1.58 | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationAudit` ?holderId |
| From | date and time picker | — | — | `listAccreditationAudit` ?from |

#### Outputs: what the screen shows and produces

**Data it reads**: `listAccreditationAudit` (onLoad, The immutable log)

**Where the user goes next**

- → `BO-684` Accreditation Executive Dashboard: *Back to Accreditation Executive Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The immutable accreditation audit configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the immutable accreditation audit untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No immutable accreditation audit configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAccreditationAudit` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.51 | Accreditation Audit Reporting - System shall provide accreditation audit reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.58 | Accreditation Audit Logs - System shall maintain immutable accreditation audit logs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-690` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-690`
- Workshop pack: ACCREDITATION.pdf board 8
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 12: Works in Immutable Accreditation Audit Log → Maintain the authoritative security record of all accreditation actions.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-690?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-684`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-691` Accreditation API Management

**Expose accreditation functionality securely to approved external systems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVELOPER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/accreditation-api-management-bo-691` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listApiClients` (onLoad, API management)

**Where the user goes next**

- → `BO-684` Accreditation Executive Dashboard: *Back to Accreditation Executive Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation api list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation api untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation api yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the accreditation api are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listApiClients` → `DEVELOPER_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-691` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-691`
- Workshop pack: ACCREDITATION.pdf board 8
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 14: Works in Accreditation API Management → Expose accreditation functionality securely to approved external systems.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-691?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-684`.
- [ ] Every gated control is gated: `DEVELOPER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-692` Accreditation Webhook Management

**Notify external systems when accreditation events occur.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Webhook configuration shall include) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `subscriptionId` (navigation) |
| Route | `/access-venue/accreditation-webhook-management-bo-692` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Endpoint | select field | — | — | — | — | — | — |
| Event subscriptions | select field | — | — | — | — | — | — |
| Authentication/security | select field | — | — | — | — | — | — |
| Secret/signature | select field | — | — | — | — | — | — |
| Retry policy | select field | — | — | — | — | — | — |
| Active/inactive | select field | — | — | — | — | — | — |
| Delivery history | select field | — | — | — | — | — | — |
| Key requirement: 12.1.53 | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Client | picker: choose a client | — | — | `listWebhookSubscriptions` ?clientId |
| Publisher | text field | — | — | `listWebhookEventTypes` ?publisher |

#### Outputs: what the screen shows and produces

**Data it reads**: `listWebhookSubscriptions` (onLoad, Webhooks); `listWebhookEventTypes` (onLoad, Accreditation events (publisher=accreditation))

**Where the user goes next**

- → `BO-684` Accreditation Executive Dashboard: *Back to Accreditation Executive Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The accreditation webhook configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the accreditation webhook untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No accreditation webhook configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 An entry in `eventTypes` is not in the webhook event catalogue.; 422 `eventType` is not one this subscription takes. |

#### Permissions

- `listWebhookSubscriptions` → `DEVELOPER_VIEW` (read) · staff, partner
- `listWebhookEventTypes` → `DEVELOPER_VIEW` (read) · staff, partner
- `createWebhookSubscription` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `testWebhookSubscription` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `listWebhookDeliveries` → `DEVELOPER_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A235** Build accreditation setup: form builder, categories, programmes and document rules *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A236** Auto-fill accreditation forms from ID uploads (OCR), saved as fields to track expiry *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A237** Block duplicate accreditations by passport / Emirates ID *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A238** Build accreditation approvals: multi-level by category, SLA alerts, auto-escalation *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A240** Keep accreditation web-portal first, with mobile app as a secondary channel *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*
- **A243** Merge accreditation, entitlement and virtual queue boards into fewer screens *(Chinmay Parab / Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 7 Sep 2026 · workshop tracker · keyword 'accreditation')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-692` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-692`
- Workshop pack: ACCREDITATION.pdf board 8
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 16: Works in Accreditation Webhook Management → Notify external systems when accreditation events occur.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-692?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-684`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-693` Integration & Data Exchange Monitor

**Monitor accreditation APIs, webhooks and external-system synchronization.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Access & Venue · wave 3 · needs the `accreditation` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCREDITATION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/access-venue/integration-data-exchange-monitor-bo-693` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Holder | picker: choose a holder | — | — | `listAccreditationAudit` ?holderId |
| From | date and time picker | — | — | `listAccreditationAudit` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listAccreditationAudit` (onLoad, Integration audit)

**Where the user goes next**

- → `BO-684` Accreditation Executive Dashboard: *Back to Accreditation Executive Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration data exchange list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration data exchange untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration data exchange yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration data exchange are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAccreditationAudit` → `ACCREDITATION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 12.1.51 | Accreditation Audit Reporting - System shall provide accreditation audit reports. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |
| 12.1.58 | Accreditation Audit Logs - System shall maintain immutable accreditation audit logs. | Accreditation & Credential Management | CONTRACTED | `listAccreditationAudit` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Access & Venue, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-693` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS08 ACCREDITATION Board 8.dc.html#bo-693`
- Workshop pack: ACCREDITATION.pdf board 8
- Flow F224 *ACCREDITATION board 8: Accreditation Executive Dashboard*, step 18: Works in Integration & Data Exchange Monitor → Monitor accreditation APIs, webhooks and external-system synchronization.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-693?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-684`.
- [ ] Every gated control is gated: `ACCREDITATION_VIEW`.
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

### In P08 · Access & Venue

- Accreditation-holder monitoring is a filtered view inside general entitlement monitoring, not a separate system. *(agreed · MoM 7 Sep 2026, Accreditation (cited in P11 resolvedQuestions) · DI-694)*

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createWebhookSubscription": {"method":"POST","path":"/webhook-subscriptions","contract":"public-api","summary":"Subscribe to business events","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WebhookSubscription","responds":"WebhookSubscription"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"listAccreditationAccessActivity": {"method":"GET","path":"/accreditation-access-activity","contract":"accreditation","summary":"Where accredited people actually went","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"holderId","in":"query","required":null},{"name":"zoneId","in":"query","required":null},{"name":"deniedOnly","in":"query","required":null}],"requestBody":null,"responds":"AccreditationAccessEvent"},
"listAccreditationAudit": {"method":"GET","path":"/accreditation-audit","contract":"accreditation","summary":"The immutable record of who granted what to whom","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"holderId","in":"query","required":null},{"name":"from","in":"query","required":null}],"requestBody":null,"responds":"AccreditationAuditRecord"},
"listAccreditationHolders": {"method":"GET","path":"/accreditation-holders","contract":"accreditation","summary":"Everybody accredited, and what state they are in","permission":"ACCREDITATION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"programmeId","in":"query","required":null},{"name":"organisationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"expiringWithinDays","in":"query","required":null}],"requestBody":null,"responds":"AccreditationHolder"},
"listApiClients": {"method":"GET","path":"/api-clients","contract":"public-api","summary":"Registered clients for this developer","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApiClient"},
"listWebhookDeliveries": {"method":"GET","path":"/webhook-subscriptions/{subscriptionId}/deliveries","contract":"public-api","summary":"What was sent, what failed, and why","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"WebhookDelivery"},
"listWebhookEventTypes": {"method":"GET","path":"/webhook-event-types","contract":"public-api","summary":"The events a webhook may subscribe to","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"publisher","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWebhookSubscriptions": {"method":"GET","path":"/webhook-subscriptions","contract":"public-api","summary":"The tenant's webhook subscriptions, filterable by API client","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"clientId","in":"query","required":false}],"requestBody":null,"responds":"WebhookSubscription"},
"testWebhookSubscription": {"method":"POST","path":"/webhook-subscriptions/{subscriptionId}/test","contract":"public-api","summary":"Send a signed test event to the endpoint, now","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WebhookDelivery"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccreditationAccessEvent": {"type":"object","description":"Board 8.4. **Granted access against used access is the whole of the annual review.**\n","properties":{"at":{"type":"string","format":"date-time"},"holderId":{"type":"string","format":"uuid"},"holderName":{"type":"string"},"zoneId":{"type":"string","format":"uuid"},"zoneName":{"type":"string"},"credentialId":{"type":"string","format":"uuid","nullable":true},"outcome":{"type":"string","enum":["admitted","denied","escorted"]},"deniedReason":{"type":"string","nullable":true}}},
"AccreditationAuditRecord": {"type":"object","x-ticvai-persistence":"accreditation.audit","description":"Board 8.7. **Who gave this person access to that place, when, and on whose authority.**\n","properties":{"id":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"holderId":{"type":"string","format":"uuid","nullable":true},"action":{"type":"string"},"actorPrincipalId":{"type":"string","format":"uuid","nullable":true},"previousValue":{"nullable":true},"newValue":{"nullable":true},"reason":{"type":"string","nullable":true},"approvalRequestId":{"type":"string","format":"uuid","nullable":true},"previousRecordHash":{"type":"string","nullable":true},"recordHash":{"type":"string"},"integrity":{"type":"string","readOnly":true,"enum":["intact","broken","unverifiable"]},"scopePath":{"type":"string"}}},
"AccreditationHolder": {"type":"object","x-ticvai-persistence":"accreditation.holder","description":"**A subject who may never sign in to anything.** `identity` owns principals; this owns accredited people.\n","required":["id","fullName"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"dateOfBirth":{"type":"string","format":"date","nullable":true},"nationality":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true,"description":"12.1.16. The holder's own address — where a mobile credential and renewal notices go"},"phone":{"type":"string","nullable":true,"description":"12.1.16. E.164"},"identityDocumentVerified":{"type":"boolean","default":false},"organisationId":{"type":"string","format":"uuid","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","suspended","revoked","expired","archived"]},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"completenessPercent":{"type":"integer","readOnly":true},"scopePath":{"type":"string"}}},
"ApiClient": {"type":"object","x-ticvai-persistence":"control.api_client","description":"CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n","required":["id","developerId","name","environment","scopes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid"},"name":{"type":"string"},"clientId":{"type":"string","readOnly":true},"environment":{"type":"string","enum":["sandbox","production"],"description":"**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"},"scopes":{"type":"array","description":"**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n","items":{"type":"string","pattern":"^[a-zA-Z]+\\.(read|write)$"}},"issuedBy":{"type":"string","enum":["partner","ticvai"],"readOnly":true,"description":"Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"},"certificationListingId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.integration_listing","description":"For a production client, the certified integration it was issued against."},"credentialTtlDays":{"type":"integer","minimum":1,"maximum":730,"nullable":true,"description":"Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the key stops working unless rotated. No token is issued after it."},"allowedTenantIds":{"type":"array","description":"13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","description":"13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n","items":{"type":"string"}},"status":{"type":"string","enum":["active","suspended","revoked"],"readOnly":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A credential unused for a year is a credential nobody will notice being stolen.**\n"}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"WebhookDelivery": {"type":"object","x-ticvai-persistence":"control.webhook_delivery","description":"13.1.30. **The log a developer needs most**, and without it every question becomes a support ticket.\n","required":["id","subscriptionId","eventType","status"],"properties":{"id":{"type":"string","format":"uuid"},"subscriptionId":{"type":"string","format":"uuid"},"eventId":{"type":"string","format":"uuid"},"eventType":{"type":"string"},"status":{"type":"string","enum":["pending","delivered","failed","retrying","abandoned"]},"attemptCount":{"type":"integer"},"responseCode":{"type":"integer","nullable":true},"responseBodyExcerpt":{"type":"string","nullable":true,"description":"**Truncated, and it is what makes the log useful** — a 500 with the receiver's own error message in it answers the question without a conversation.\n"},"isReplay":{"type":"boolean","default":false},"isTest":{"type":"boolean","default":false,"description":"Sent by `testWebhookSubscription` (VM close-out, 29 September). Marked in the payload so a receiver never books it, and never counted towards `consecutiveFailures`.\n"},"deliveredAt":{"type":"string","format":"date-time","nullable":true}}},
"WebhookEventCatalogueEntry": {"type":"object","x-ticvai-persistence":"none — read from the event catalogue (events/*.yaml) shipped with the release","description":"One event a webhook may subscribe to, as the event catalogue declares it. What a receiver needs to write a handler: the name, the version in the payload, who publishes it, what it is about and when, and the payload fields.\n","required":["name","version","publisher"],"properties":{"name":{"$ref":"#/components/schemas/WebhookEventType"},"version":{"type":"integer","minimum":1},"publisher":{"type":"string","description":"The one context that publishes it."},"aggregate":{"type":"string","description":"What the event is about. Delivery is ordered within one instance of it."},"description":{"type":"string"},"emittedWhen":{"type":"string","nullable":true},"payload":{"type":"array","items":{"type":"object","required":["field","type"],"properties":{"field":{"type":"string"},"type":{"type":"string"},"required":{"type":"boolean","default":true},"notes":{"type":"string","nullable":true}}}}}},
"WebhookEventType": {"type":"string","description":"**The webhook event catalogue: every event a subscription may name** (29 September, build pass). Each value is the `name` of an event in `events/` — `aggregate.pastTenseFact`, published through `platform.outbox` by exactly one context. A name is added here in the same change that adds its event file, and never before.\n**Added 29 September**, each closing a requirement that had the webhook mechanism and nothing to subscribe to:\n| Events | Publisher | Requirement | |---|---|---| | `device.statusChanged`, `device.tamperDetected`, `device.enrolmentChanged`, `device.firmwareReleased`, `device.firmwareRolloutCompleted` | tenancy | 16.9.56 | | `accreditation.applicationDecided`, `accreditation.holderStatusChanged`, `accreditation.credentialIssued`, `accreditation.renewalDue` | accreditation | 12.1.53 | | `approval.requested`, `approval.escalated`, `approval.stepCompleted`, `approval.expired` | approvals | 11.1.64, 11.1.66 | | `seat.held`, `seat.released`, `seat.blocked`, `seatMap.published` | seating | 21.13.4 | | `consent.deviceConsentRecorded`, `consent.deviceConsentClaimed` | marketing | 2.6.65 | | `order.chargebackRecorded` | orders | 8.3.11 to 8.3.15 (a tenant's own finance or fraud tooling) | | `entitlement.expiringSoon` | access | 5.5.30 (a tenant's own CRM) | | `apiClient.anomalyDetected` | public-api | 17 September minutes M17-07 (added 30 September with its event file) |\n**Deprecated** (1 October, ADR-0067 amendment): `device.enrolmentChanged` is still offered but nothing inside the platform consumes it any more; it is removed at the next major version of this API. Subscribers are told in the release note.\n**Published and deliberately not offered** (29 September, build pass, group G2): `identity.credentialResetRequested` and `identity.loginRecorded` are security signals, and a stream of them to an outside receiver is a map of which accounts are under attack; `storefront.sessionEvent` is high-volume fraud telemetry, not a business fact a receiver acts on.\n","x-ticvai-deprecated-values":["device.enrolmentChanged"],"enum":["access.validated","accreditation.applicationDecided","accreditation.credentialIssued","accreditation.holderStatusChanged","accreditation.renewalDue","ai.ceilingApproaching","apiClient.anomalyDetected","approval.escalated","approval.expired","approval.granted","approval.rejected","approval.requested","approval.stepCompleted","assets.documentIndexed","cart.abandoned","catalogue.productPublished","consent.deviceConsentClaimed","consent.deviceConsentRecorded","conversation.handedOver","device.enrolmentChanged","device.firmwareReleased","device.firmwareRolloutCompleted","device.statusChanged","device.tamperDetected","entitlement.expiringSoon","entitlement.issued","entitlement.statusChanged","fnb.menuPublished","fnb.orderReady","inventory.purchaseOrderReceived","ledger.journalPosted","ledger.periodClosed","maintenance.assetReturnedToService","maintenance.templatePublished","maintenance.workOrderCompleted","marketing.caseClosed","order.chargebackRecorded","order.completed","order.paid","order.refunded","performance.cancelled","reporting.definitionPublished","retail.merchandisePublished","seat.blocked","seat.held","seat.released","seat.sold","seatMap.published","shift.closed","stock.depleted","tenant.suspended","whitelabel.contentPublished"]},
"WebhookSubscription": {"type":"object","x-ticvai-persistence":"control.webhook_subscription","description":"13.1.26, 13.3.18 and 13.3.22. **The 29 events already exist and nothing outside could receive one.**\n","required":["id","clientId","endpointUrl","eventTypes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"clientId":{"type":"string","format":"uuid"},"endpointUrl":{"type":"string"},"eventTypes":{"type":"array","description":"**Filtered at subscription, not at delivery.** A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. Each entry is a name from the webhook event catalogue (`WebhookEventType`).\n","items":{"$ref":"#/components/schemas/WebhookEventType"}},"filters":{"type":"object","nullable":true,"description":"13.3.22. Tenant, venue, or a business condition on the payload.","additionalProperties":true},"signingSecret":{"type":"string","format":"password","writeOnly":true,"description":"**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n**Write-only: accepted on create, never returned.** The same rule as `clientSecret` — a system that can show you a secret later is a system that hands it to whoever reads the subscription.\n"},"status":{"type":"string","enum":["pendingVerification","active","paused","failing","disabled"],"readOnly":true},"consecutiveFailures":{"type":"integer","readOnly":true},"disabledReason":{"type":"string","nullable":true,"readOnly":true,"description":"13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"}}}
}
```
