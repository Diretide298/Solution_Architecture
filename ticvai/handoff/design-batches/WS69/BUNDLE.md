# WS69 — Unified BI Reporting and AI Analytics Platform board 4

**10 screens · 11 operations · 16 schemas · 8 permissions**

Platform P16 Venue Analytics · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `APPROVAL_CONFIGURE, PERMISSION_VIEW, REPORT_EXPORT, REPORT_SCHEDULE, REPORT_VIEW_TENANT, REPORT_VIEW_VENUE, TENANT_CONFIGURE, TENANT_VIEW`. A control nobody can use must say so,
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
| `ANL-041` | Reporting Governance Command Center | B–D | 0 | 36 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-042` | Report Scheduler | B–D | 23 | 0 | 5 | 4 | 1 | 0 | — | notStarted (—) |
| `ANL-043` | Subscription Manager | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-044` | Distribution & Delivery Configuration | B–D | 14 | 0 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `ANL-045` | Export & Download Center | B–D | 0 | 22 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `ANL-046` | Report API & Data Delivery Manager | B–D | 10 | 0 | 5 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-047` | Report Access & Sharing Control | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-048` | Delivery Monitoring & Failure Management | B–D | 0 | 20 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-049` | Report Audit Trail & Compliance | B–D | 16 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-050` | Retention, Archive & Governance Policy | B–D | 14 | 0 | 5 | 2 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-041, ANL-043, ANL-045, ANL-047 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-041` Reporting Governance Command Center

**Provide administrators with a centralized overview of reporting operations, governance, distribution and compliance.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/reporting-governance-command-center-anl-041` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listReportDeliveries` ?from |
| Failed only | toggle | — | — | `listReportDeliveries` ?failedOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every reporting governance** (data table)

| Shows | Format | Notes |
|---|---|---|
| Active reports | text | not in the schema: `Active Reports` |
| Published dashboards | text | not in the schema: `Published Dashboards` |
| Active schedules | text | not in the schema: `Active Schedules` |
| Active subscriptions | text | not in the schema: `Active Subscriptions` |
| Reports generated today | text | not in the schema: `Reports Generated Today` |
| Successful deliveries | text | not in the schema: `Successful Deliveries` |
| Failed deliveries | text | not in the schema: `Failed Deliveries` |
| Pending approvals | text | not in the schema: `Pending Approvals` |
| Exports today | text | not in the schema: `Exports Today` |
| API report requests | text | not in the schema: `API Report Requests` |
| Shared reports | text | not in the schema: `Shared Reports` |
| Governance exceptions | text | not in the schema: `Governance Exceptions` |
| Recently generated reports | text | not in the schema: `Recently generated reports` |
| Failed reports | text | not in the schema: `Failed reports` |
| Recently shared reports | text | not in the schema: `Recently shared reports` |
| Large exports | text | not in the schema: `Large exports` |
| Permission changes | text | not in the schema: `Permission changes` |
| Scheduled report changes | text | not in the schema: `Scheduled-report changes` |

**The selected reporting governance** (detail panel): The pack groups this record's detail under its own headings: “Show health by”.

| Shows | Format | Notes |
|---|---|---|
| Active reports | text | not in the schema: `Active Reports` |
| Published dashboards | text | not in the schema: `Published Dashboards` |
| Active schedules | text | not in the schema: `Active Schedules` |
| Active subscriptions | text | not in the schema: `Active Subscriptions` |
| Reports generated today | text | not in the schema: `Reports Generated Today` |
| Successful deliveries | text | not in the schema: `Successful Deliveries` |
| Failed deliveries | text | not in the schema: `Failed Deliveries` |
| Pending approvals | text | not in the schema: `Pending Approvals` |
| Exports today | text | not in the schema: `Exports Today` |
| API report requests | text | not in the schema: `API Report Requests` |
| Shared reports | text | not in the schema: `Shared Reports` |
| Governance exceptions | text | not in the schema: `Governance Exceptions` |
| Recently generated reports | text | not in the schema: `Recently generated reports` |
| Failed reports | text | not in the schema: `Failed reports` |
| Recently shared reports | text | not in the schema: `Recently shared reports` |
| Large exports | text | not in the schema: `Large exports` |
| Permission changes | text | not in the schema: `Permission changes` |
| Scheduled report changes | text | not in the schema: `Scheduled-report changes` |

**Data it reads**: `listReportSchedules` (onLoad, What runs when); `listReportDeliveries` (onLoad, What arrived and what did not)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*; carries `reportId`
- → `ANL-050` Retention, Archive & Governance Policy: *Retention, Archive & Governance Policy*
- → `ANL-042` Report Scheduler: *Report Scheduler*
- → `ANL-043` Subscription Manager: *Subscription Manager*
- → `ANL-044` Distribution & Delivery Configuration: *Distribution & Delivery Configuration*
- → `ANL-045` Export & Download Center: *Export & Download Center*
- → `ANL-046` Report API & Data Delivery Manager: *Report API & Data Delivery Manager*
- → `ANL-047` Report Access & Sharing Control: *Report Access & Sharing Control*
- → `ANL-048` Delivery Monitoring & Failure Management: *Delivery Monitoring & Failure Management*
- → `ANL-049` Report Audit Trail & Compliance: *Report Audit Trail & Compliance*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The reporting governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the reporting governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No reporting governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the reporting governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listReportSchedules` → `REPORT_VIEW_VENUE` (operate) · staff
- `listReportDeliveries` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-041` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-041`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 1: Opens Reporting Governance Command Center → Provide administrators with a centralized overview of reporting operations, governance, distribution and compliance.
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F178 branch at step 1 (expected): when Nothing has been set up on Reporting Governance Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F178 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-041?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-050`, `ANL-042`, `ANL-043`, `ANL-044`, `ANL-045`, `ANL-046`, `ANL-047`, `ANL-048`, `ANL-049`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-042` Report Scheduler

**Allow authorized users to automatically generate reports according to defined schedules.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure; Frequency Options) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/report-scheduler-anl-042` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Schedule Name | select field | — | — | — | — | — | — |
| Report | select field | — | — | — | — | — | — |
| Report Version | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Start Date | select field | — | — | — | — | — | — |
| End Date | select field | — | — | — | — | — | — |
| Time | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| Frequency | select field | — | — | — | — | — | — |
| Run immediately | select field | — | — | — | — | — | — |
| Retry on failure | select field | — | — | — | — | — | — |
| Maximum retries | select field | — | — | — | — | — | — |
| Timeout | select field | — | — | — | — | — | — |
| Skip if source data is stale | text field | — | — | — | — | — | — |
| Wait for source refresh | text field | — | — | — | — | — | — |
| Once | select field | — | — | — | — | — | — |
| Hourly | select field | — | — | — | — | — | — |
| Daily | select field | — | — | — | — | — | — |
| Weekly | select field | — | — | — | — | — | — |
| Monthly | select field | — | — | — | — | — | — |
| Quarterly | select field | — | — | — | — | — | — |
| Yearly | select field | — | — | — | — | — | — |
| Custom | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listReportSchedules` (onLoad, Schedules)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report scheduler configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report scheduler untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report scheduler configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Invalid cadence (a field its frequency needs is missing, or one it does not take is sent, audit R158), or no recipients |

#### Permissions

- `listReportSchedules` → `REPORT_VIEW_VENUE` (operate) · staff
- `createReportSchedule` → `REPORT_SCHEDULE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.14 | The system should have scheduling of report generation and delivery to web address location or list of email addresses. | Retail POS | CONTRACTED | `createReportSchedule` |
| 8.7.15 | System shall support report scheduling. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 8.7.16 | System shall support report subscriptions. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |
| 8.7.17 | System shall support report sharing. | Unified Operations Dashboard | CONTRACTED | `createReportSchedule` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reports can be scheduled to defined recipient groups - e.g. a daily closing/summary sales report or shift-closing report emailed each morning to operations, finance or sales - using configurable email templates with the report attached. *(client request · MoM 8 Sep 2026, 4.8 Report Distribution & Scheduling · DI-714)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-042` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-042`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 2: Works in Report Scheduler → Allow authorized users to automatically generate reports according to defined schedules.

#### Acceptance for the design

- [ ] Every input above is drawn (23), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-042?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-043` Subscription Manager

**Allow users and administrators to subscribe recipients to dashboards, reports and KPI summaries.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/subscription-manager-anl-043` |

**Known gaps.** **Subscription Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create report subscription (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listReportSubscriptions` (onLoad, Who receives what)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The subscription list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the subscription untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No subscription yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the subscription are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listReportSubscriptions` → `REPORT_VIEW_VENUE` (operate) · staff
- `createReportSubscription` → `REPORT_SCHEDULE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reports can be scheduled to defined recipient groups - e.g. a daily closing/summary sales report or shift-closing report emailed each morning to operations, finance or sales - using configurable email templates with the report attached. *(client request · MoM 8 Sep 2026, 4.8 Report Distribution & Scheduling · DI-714)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-043` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-043`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 4: Works in Subscription Manager → Allow users and administrators to subscribe recipients to dashboards, reports and KPI summaries.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-043?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create report subscription, Cancel.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_SCHEDULE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-044` Distribution & Delivery Configuration

**Configure how generated reporting content reaches approved recipients or destinations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_SCHEDULE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Define; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/distribution-delivery-configuration-anl-044` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: TICVAI Notification Center, Secure Download, API, External approved destination. Each needs an operation …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Destination | select field | — | — | — | — | — | — |
| Recipient | select field | — | — | — | — | — | — |
| Format | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| File Naming | select field | — | — | — | — | — | — |
| Password/Security Policy | select field | — | — | — | — | — | — |
| Expiration | select field | — | — | — | — | — | — |
| Delivery Priority | select field | — | — | — | — | — | — |
| Email Subject | select field | — | — | — | — | — | — |
| Email Body Template | select field | — | — | — | — | — | — |
| Attachment | select field | — | — | — | — | — | — |
| Secure Link | select field | — | — | — | — | — | — |
| Branding | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| TICVAI Notification Center (primary button) | navigation or local | — | — | — | — |
| Secure Download (secondary button) | navigation or local | — | — | — | — |
| API (secondary button) | navigation or local | — | — | — | — |
| External approved destination (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The distribution delivery configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the distribution delivery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No distribution delivery configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createReportSubscription` → `REPORT_SCHEDULE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Reports can be scheduled to defined recipient groups - e.g. a daily closing/summary sales report or shift-closing report emailed each morning to operations, finance or sales - using configurable email templates with the report attached. *(client request · MoM 8 Sep 2026, 4.8 Report Distribution & Scheduling · DI-714)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-044` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-044`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 6: Works in Distribution & Delivery Configuration → Configure how generated reporting content reaches approved recipients or destinations.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-044?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: TICVAI Notification Center, Secure Download, API, External approved destination.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_SCHEDULE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-045` Export & Download Center

**Provide centralized management of report and dashboard exports. The source matrix requires reporting export to multiple formats, including PDF, Excel, delimited text and XML.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_EXPORT` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `executionId` (navigation), `exportId` (navigation) |
| Route | `/analytics/export-download-center-anl-045` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every export download** (data table)

| Shows | Format | Notes |
|---|---|---|
| Export ID | text | not in the schema: `Export ID` |
| Report | text | not in the schema: `Report` |
| Requested by | text | not in the schema: `Requested By` |
| Site | text | not in the schema: `Site` |
| Format | text | not in the schema: `Format` |
| Requested time | text | not in the schema: `Requested Time` |
| Completed time | text | not in the schema: `Completed Time` |
| File size | text | not in the schema: `File Size` |
| Record count | text | not in the schema: `Record Count` |
| Status | text | not in the schema: `Status` |
| Expiration | text | not in the schema: `Expiration` |

**The selected export download** (detail panel): The pack groups this record's detail under its own headings: “At minimum”, “Export Status”, “Large Exports”.

| Shows | Format | Notes |
|---|---|---|
| Export ID | text | not in the schema: `Export ID` |
| Report | text | not in the schema: `Report` |
| Requested by | text | not in the schema: `Requested By` |
| Site | text | not in the schema: `Site` |
| Format | text | not in the schema: `Format` |
| Requested time | text | not in the schema: `Requested Time` |
| Completed time | text | not in the schema: `Completed Time` |
| File size | text | not in the schema: `File Size` |
| Record count | text | not in the schema: `Record Count` |
| Status | text | not in the schema: `Status` |
| Expiration | text | not in the schema: `Expiration` |

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The export download list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the export download untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No export download yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the export download are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `exportReportResult` → `REPORT_EXPORT` (read) · staff
- `getReportExport` → `REPORT_EXPORT` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 6.1.20 | The system should be able to all reporting functions should have export option to multiple file formats; minimum of PDF, Excel, delimited text, and XML. | Retail POS | CONTRACTED | `exportReportResult` |
| 6.1.26 | The system should be able to view/export (as CSV) user data. | Retail POS | CONTRACTED | `exportReportResult` |
| 8.7.18 | System shall support report exports to Excel. | Unified Operations Dashboard | CONTRACTED | `exportReportResult` |
| 8.7.19 | System shall support report exports to PDF. | Unified Operations Dashboard | CONTRACTED | `exportReportResult` |
| 8.7.20 | System shall support report exports through APIs. | Unified Operations Dashboard | CONTRACTED | `exportReportResult` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Report builder provides a library of standard operations/finance reports exportable as PDF or Excel, plus custom reports built drag-and-drop (no SQL) by choosing which data-set fields appear as columns/rows. *(client request · MoM 8 Sep 2026, 4.5 Self-Service Report Builder & Drill-Down Reporting · DI-708)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-045` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-045`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 8: Works in Export & Download Center → Provide centralized management of report and dashboard exports. The source matrix requires reporting export to multiple formats, including PDF, Excel, delimited text and XML.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-045?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_EXPORT`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-046` Report API & Data Delivery Manager

**Allow approved systems to receive reporting information programmatically. This supports the requirement for report export/access through APIs.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/report-api-data-delivery-manager-anl-046` |

**Known gaps.** **Report API & Data Delivery Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| API Name | select field | — | — | — | — | — | — |
| Report/Dataset | select field | — | — | — | — | — | — |
| Consumer/Application | select field | — | — | — | — | — | — |
| Authentication | select field | — | — | — | — | — | — |
| Allowed Sites | select field | — | — | — | — | — | — |
| Allowed Fields | select field | — | — | — | — | — | — |
| Filters | select field | — | — | — | — | — | — |
| Rate Limit | select field | — | — | — | — | — | — |
| Data Format | select field | — | — | — | — | — | — |
| Status | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `listReportSubscriptions` (onLoad, API and SFTP delivery)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report api data configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report api data untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report api data configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listReportSubscriptions` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-046` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-046`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 10: Works in Report API & Data Delivery Manager → Allow approved systems to receive reporting information programmatically. This supports the requirement for report export/access through APIs.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-046?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-047` Report Access & Sharing Control

**Provide centralized security for reports, dashboards and analytical information. The matrix specifically requires reporting access based on group rights, operating-area rights and user access rights.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PERMISSION_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/report-access-sharing-control-anl-047` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Pending approval · Active · Suspended · Retired | `listAuthorisationPolicies` ?status |
| Scope path | text field | — | — | `listAuthorisationPolicies` ?scopePath |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listAuthorisationPolicies` (onLoad, Who may see which report)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report access sharing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report access sharing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report access sharing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the report access sharing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAuthorisationPolicies` → `PERMISSION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-047` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-047`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 12: Works in Report Access & Sharing Control → Provide centralized security for reports, dashboards and analytical information. The matrix specifically requires reporting access based on group rights, operating-area rights and user access rights.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-047?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `PERMISSION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-048` Delivery Monitoring & Failure Management

**Monitor scheduled report execution and distribution and provide operational management of failures.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/delivery-monitoring-failure-management-anl-048` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 0 operations.** Unserved: Retry, Cancel, View Error, Change Destination, Notify Owner, Escalate. Each needs an operation, or needs … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listReportDeliveries` ?from |
| Failed only | toggle | — | — | `listReportDeliveries` ?failedOnly |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every delivery monitoring failure** (data table)

| Shows | Format | Notes |
|---|---|---|
| Job ID | text | not in the schema: `Job ID` |
| Report | text | not in the schema: `Report` |
| Schedule | text | not in the schema: `Schedule` |
| Start time | text | not in the schema: `Start Time` |
| Completion time | text | not in the schema: `Completion Time` |
| Recipient count | text | not in the schema: `Recipient Count` |
| Delivery method | text | not in the schema: `Delivery Method` |
| Status | text | not in the schema: `Status` |
| Error | text | not in the schema: `Error` |
| Retry count | text | not in the schema: `Retry Count` |

**The selected delivery monitoring failure** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Job ID | text | not in the schema: `Job ID` |
| Report | text | not in the schema: `Report` |
| Schedule | text | not in the schema: `Schedule` |
| Start time | text | not in the schema: `Start Time` |
| Completion time | text | not in the schema: `Completion Time` |
| Recipient count | text | not in the schema: `Recipient Count` |
| Delivery method | text | not in the schema: `Delivery Method` |
| Status | text | not in the schema: `Status` |
| Error | text | not in the schema: `Error` |
| Retry count | text | not in the schema: `Retry Count` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Retry (primary button) | navigation or local | — | — | — | — |
| Cancel (destructive button) | navigation or local | — | — | — | — |
| View Error (secondary button) | navigation or local | — | — | — | — |
| Change Destination (secondary button) | navigation or local | — | — | — | — |
| Notify Owner (secondary button) | navigation or local | — | — | — | — |
| Escalate (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listReportDeliveries` (onLoad, Failures and retries)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

**What opens over it**

- confirmDialog *Cancel*: **Cancel on a delivery monitoring failure is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delivery monitoring failure list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delivery monitoring failure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No delivery monitoring failure yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the delivery monitoring failure are still there. The pack's own statuses are Running — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listReportDeliveries` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-048` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-048`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 14: Works in Delivery Monitoring & Failure Management → Monitor scheduled report execution and distribution and provide operational management of failures.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-048?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Retry, Cancel, View Error, Change Destination, Notify Owner, Escalate.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-049` Report Audit Trail & Compliance

**Maintain complete traceability of reporting activity. The source matrix requires report logs and audit reporting for sales history.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_TENANT` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/report-audit-trail-compliance-anl-049` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search report audit trail | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by user, report, action, date, site, business unit and 2 more — which are present is a decision the pack already made. | — |
| Report Created | select field | — | — | — | — | — | — |
| Report Modified | select field | — | — | — | — | — | — |
| Report Published | select field | — | — | — | — | — | — |
| Report Executed | select field | — | — | — | — | — | — |
| Report Viewed | select field | — | — | — | — | — | — |
| Report Exported | select field | — | — | — | — | — | — |
| Report Shared | select field | — | — | — | — | — | — |
| Schedule Created | select field | — | — | — | — | — | — |
| Schedule Modified | select field | — | — | — | — | — | — |
| Subscription Created | select field | — | — | — | — | — | — |
| Permission Changed | select field | — | — | — | — | — | — |
| API Access | select field | — | — | — | — | — | — |
| Report Archived | select field | — | — | — | — | — | — |
| Report Deleted | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listReportDeliveries` ?from |
| Failed only | toggle | — | — | `listReportDeliveries` ?failedOnly |

#### Outputs: what the screen shows and produces

**Data it reads**: `listReportDeliveries` (onLoad, What left, with what in it)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report audit trail configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report audit trail untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report audit trail configured yet. Carries the create action and says what the platform does in the meantime. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the report audit trail are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listReportDeliveries` → `REPORT_VIEW_TENANT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-049` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-049`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 16: Works in Report Audit Trail & Compliance → Maintain complete traceability of reporting activity. The source matrix requires report logs and audit reporting for sales history.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-049?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `REPORT_VIEW_TENANT`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-050` Retention, Archive & Governance Policy

**Control the lifecycle of reports, generated files and historical analytical data. The reporting-platform specification requires long-term reporting history together with archival and retrieval capability.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `TENANT_CONFIGURE`, `TENANT_VIEW` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure retention separately for; Define) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `dataClass` (navigation) |
| Route | `/analytics/retention-archive-governance-policy-anl-050` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Report Definitions | select field | — | — | — | — | — | — |
| Dashboard Versions | select field | — | — | — | — | — | — |
| Generated Reports | select field | — | — | — | — | — | — |
| Export Files | select field | — | — | — | — | — | — |
| Audit Logs | select field | — | — | — | — | — | — |
| Schedule History | select field | — | — | — | — | — | — |
| API Logs | select field | — | — | — | — | — | — |
| Historical Analytics | select field | — | — | — | — | — | — |
| Retention Period | select field | — | — | — | — | — | — |
| Archive After | select field | — | — | — | — | — | — |
| Delete After | select field | — | — | — | — | — | — |
| Legal/Compliance Hold | select field | — | — | — | — | — | — |
| Storage Location | select field | — | — | — | — | — | — |
| Retrieval Rules | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Data class | select | — | Guest profile · Payment record · Financial record · Audit record · Approval record · Compliance inspection · Face tag biometric · Face pass biometric · AI prompts · AI conversations · AI decision records · AI metadata index | `listDataRetentionSettings` ?dataClass |

#### Outputs: what the screen shows and produces

**Data it reads**: `listDataRetentionSettings` (onLoad, Retention period per data class)

**Where the user goes next**

- → `ANL-041` Reporting Governance Command Center: *Back to Reporting Governance Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The retention archive governance configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the retention archive governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No retention archive governance configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A period below the class's legal minimum or above its legal maximum, a period sent for `aiMetadataIndex`, or a `followsDataClass` chain that loops |

#### Permissions

- `setApprovalRetentionPolicy` → `APPROVAL_CONFIGURE` (configure) · staff
- `listDataRetentionSettings` → `TENANT_VIEW` (read) · staff
- `setDataRetentionSetting` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.58 | Approval Record Retention - System shall support configurable approval record retention policies. | Approval Workflows & Governance | CONTRACTED | `setApprovalRetentionPolicy` |
| 4.3.4 | The system should support payment servers that provide the following functions: - Record transactions below the authorization threshold - Procure authorizations over the automatic authorization … | Bundles and Promotions | CONTRACTED | `setDataRetentionSetting` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-050` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS175 Unified BI Reporting and AI Analytics Platform Board 4.dc.html#anl-050`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 4
- Flow F178 *Unified BI Reporting and AI Analytics Platform board 4: Reporting Governance …*, step 18: Works in Retention, Archive & Governance Policy → Control the lifecycle of reports, generated files and historical analytical data. The reporting-platform specification requires long-term reporting history together with archival and retrieval …
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-050?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-041`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P16 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: for density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

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

### Across P16 Venue Analytics

- One consolidated, permission-based reporting/dashboard area: a user opens "dashboards" once and sees all dashboards their access allows (finance sees finance; a CEO sees sales, admissions, access control), with dashboard settings there too - not duplicated dashboard screens inside each functional module. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-721)*
- Dashboards should refresh near-real-time (seconds) so management can monitor sales continuously rather than wait for periodic or end-of-day refreshes. *(agreed · MoM 8 Sep 2026, 4.6 Real-Time Reporting Architecture · DI-711)*
- Dashboards must be mobile-responsive so management (e.g. a CEO outside the venue) can log in from a smartphone via a URL rather than needing a laptop. *(agreed · MoM 8 Sep 2026, 4.1 Rationale for a Native BI/Reporting Platform · DI-696)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*

### In P16 · Analytics

- Finance board: revenue by department and cost centre, shift-closing details, and payment gateway reconciliation, shown as bar and pie charts. *(client request · MoM 8 Sep 2026, 4.9 Sales, Finance, Operations & CRM Boards · DI-716)*

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createReportSchedule": {"method":"POST","path":"/report-schedules","contract":"reporting","summary":"Schedule a report","permission":"REPORT_SCHEDULE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportScheduleRequest","responds":"ReportSchedule"},
"createReportSubscription": {"method":"POST","path":"/report-subscriptions","contract":"reporting","summary":"Send a report to somebody, on terms","permission":"REPORT_SCHEDULE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReportSubscription","responds":"ReportSubscription"},
"exportReportResult": {"method":"POST","path":"/report-executions/{executionId}/export","contract":"reporting","summary":"Export a completed result","permission":"REPORT_EXPORT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getReportExport": {"method":"GET","path":"/report-exports/{exportId}","contract":"reporting","summary":"Export status and download link","permission":"REPORT_EXPORT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportExport"},
"listAuthorisationPolicies": {"method":"GET","path":"/authorisation-policies","contract":"identity","summary":"Attribute-based authorisation policies","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"scopePath","in":"query","required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"listDataRetentionSettings": {"method":"GET","path":"/data-retention-settings","contract":"tenancy","summary":"How long the tenant keeps each class of data","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"dataClass","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReportDeliveries": {"method":"GET","path":"/report-deliveries","contract":"reporting","summary":"What was sent, to whom, and what failed","permission":"REPORT_VIEW_TENANT","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"failedOnly","in":"query","required":null}],"requestBody":null,"responds":"ReportDelivery"},
"listReportSchedules": {"method":"GET","path":"/report-schedules","contract":"reporting","summary":"List scheduled reports","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listReportSubscriptions": {"method":"GET","path":"/report-subscriptions","contract":"reporting","summary":"Who receives what, and by which route","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ReportSubscription"},
"setApprovalRetentionPolicy": {"method":"PUT","path":"/approval-retention","contract":"approvals","summary":"How long decision records are kept, and what survives","permission":"APPROVAL_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalRetentionPolicy","responds":"ApprovalRetentionPolicy"},
"setDataRetentionSetting": {"method":"PUT","path":"/data-retention-settings/{dataClass}","contract":"tenancy","summary":"Set how long the tenant keeps one class of data","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TenantDataRetentionSetting","responds":"TenantDataRetentionSetting"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCondition": {"type":"object","description":"**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n","required":["attribute","operator"],"properties":{"attribute":{"type":"string","enum":["user.attribute","employee.attribute","employee.onShift","membership.tier","membership.status","accreditation.type","accreditation.status","customer.segment","resource.classification","venue.attribute","venue.id","attraction.attribute","device.kind","device.id","device.trusted","time.ofDay","time.dayOfWeek","time.season","time.withinOperatingHours","event.id","event.status","capacity.utilisationPercent","occupancy.level","risk.score","ticket.status","location.scopePath"]},"key":{"type":"string","nullable":true,"description":"For the `*.attribute` forms — which attribute, by code."},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","greaterThan","lessThan","between","contains","startsWith","exists"]},"value":{"nullable":true,"description":"The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"},"values":{"type":"array","items":{"type":"string"}}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalRetentionPolicy": {"type":"object","x-ticvai-persistence":"approvals.retention_policy","description":"Approvals board 6.7. **Approval records outlive what they approved.**","properties":{"id":{"type":"string","format":"uuid"},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"retainYears":{"type":"integer","nullable":true,"description":"**Null takes the tenant's `approvalRecord` retention setting** (tenancy `setDataRetentionSetting`; decided 29 September, all data retention is tenant configuration). A value here applies to the request kinds this policy names and may only lengthen what the tenant setting keeps.\n"},"retainSignatures":{"type":"boolean","default":true},"retainAttachments":{"type":"boolean","default":false},"onExpiry":{"type":"string","enum":["delete","anonymise","archive"],"default":"archive"},"overridesPrivacyDeletion":{"type":"boolean","default":true,"description":"**Can extend, never shorten, what privacy retention would delete.** The interaction is decided once here instead of argued per data-subject request.\n"},"legalBasis":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"AuthorisationPolicy": {"type":"object","x-ticvai-persistence":"identity.authorisation_policy","description":"3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here).\n**Settled by ADR-0068 (accepted 1 October): guest admission lives in Access only.** This engine keeps staff authorisation and was renamed to say so: `identity.access_policy` became `identity.authorisation_policy`, its versions `identity.authorisation_policy_version`, and its operations `*AuthorisationPolicy*`. \"Access policy\" now means `AccessDynamicPolicy` and nothing else.\n","required":["code","name","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on `createAuthorisationPolicy`; the path names the policy on update."},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"isTemplate":{"type":"boolean","default":false},"permissions":{"type":"array","items":{"type":"string"},"description":"**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/AccessCondition"}},"combining":{"type":"string","enum":["allMustMatch","anyMayMatch"],"default":"allMustMatch"},"effect":{"type":"string","enum":["permit","deny"],"description":"**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"},"priority":{"type":"integer","default":0},"scopePath":{"type":"string","description":"3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"},"appliesToRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"status":{"type":"string","readOnly":true,"description":"**Moved only by `setAuthorisationPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n","enum":["draft","pendingApproval","active","suspended","retired"]},"version":{"type":"integer","default":1,"readOnly":true,"description":"Set by the server; every `updateAuthorisationPolicy` writes a new version."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"delegatedAdminRoleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"}}},
"Cadence": {"x-ticvai-persistence":"none — embedded in schedule","type":"object","description":"**What each frequency needs (decided 28 September, audit R158).** `daily`: `timeOfDay`. `weekly`: `dayOfWeek` and `timeOfDay`. `monthly`: `dayOfMonth` and `timeOfDay`, a day past the month's end running on its last day. `quarterly`: `dayOfMonth` and `timeOfDay`, in the first month of each quarter. `onShiftClose` and `onPeriodClose`: nothing else, they run on the event. A field a frequency needs and does not have, or one it does not take, is the 400 on `createReportSchedule`. **Times are in the venue's time zone.**\n","required":["frequency"],"properties":{"frequency":{"type":"string","enum":["daily","weekly","monthly","quarterly","onShiftClose","onPeriodClose"]},"dayOfWeek":{"type":"integer","minimum":0,"maximum":6},"dayOfMonth":{"type":"integer","minimum":1,"maximum":31},"timeOfDay":{"type":"string","pattern":"^([01]\\d|2[0-3]):[0-5]\\d$"},"timeZone":{"type":"string","readOnly":true,"description":"Always the venue's time zone (decided 28 September, audit R158), returned so a reader knows which. Not taken on a write."}}},
"CreateReportScheduleRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["reportId","cadence","recipients","format"],"properties":{"reportId":{"type":"string","format":"uuid"},"name":{"type":"string","maxLength":200},"cadence":{"$ref":"#/components/schemas/Cadence"},"parameters":{"type":"object","additionalProperties":true,"description":"As `RunReportRequest.parameters` — keyed by the report's `ReportParameter.key`, applied to every run."},"recipients":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/Recipient"}},"format":{"$ref":"#/components/schemas/ExportFormat"},"includePersonalData":{"type":"boolean","default":false},"skipIfEmpty":{"type":"boolean","default":true,"description":"An empty report every morning trains people to ignore the report."}}},
"ExecutionStatus": {"type":"string","enum":["queued","running","completed","failed","cancelled","expired"]},
"ExportFormat": {"type":"string","enum":["csv","xlsx","pdf","json"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Recipient": {"x-ticvai-persistence":"reporting.schedule_recipient","type":"object","description":"One recipient of a schedule. **A row of `reporting.schedule_recipient`, a child of `reporting.schedule`** — `ReportSchedule` declares the pair, which is what gives the table its `schedule_id`. Pull audit 26 September: declared on its own, the table had no column tying a recipient to its schedule.\n","required":["kind","address"],"properties":{"kind":{"type":"string","enum":["principal","email","sftp","webhook"]},"address":{"type":"string"},"principalId":{"type":"string","format":"uuid"}}},
"ReportDelivery": {"type":"object","x-ticvai-persistence":"reporting.delivery","description":"BI boards 4.8 and 4.9. **A report that silently stopped arriving is worse than one that never existed.**\n","properties":{"id":{"type":"string","format":"uuid"},"subscriptionId":{"type":"string","format":"uuid"},"reportId":{"type":"string","format":"uuid"},"attemptedAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["delivered","failed","retrying","suppressed"]},"recipientCount":{"type":"integer"},"failureReason":{"type":"string","nullable":true},"retryCount":{"type":"integer","default":0},"containedPersonalData":{"type":"boolean","default":false},"scopePath":{"type":"string"}}},
"ReportExport": {"x-ticvai-persistence":"reporting.export","type":"object","required":["id","executionId","format","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"executionId":{"type":"string"},"format":{"$ref":"#/components/schemas/ExportFormat"},"status":{"type":"string","enum":["queued","generating","ready","failed","expired"]},"includesPersonalData":{"type":"boolean"},"purpose":{"type":"string","nullable":true},"downloadUrl":{"type":"string","nullable":true,"description":"Signed and expiring. Present only while status is `ready`."},"sizeBytes":{"type":"integer","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"requestedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},
"ReportSchedule": {"x-ticvai-persistence":"reporting.schedule + reporting.schedule_recipient","allOf":[{"$ref":"#/components/schemas/CreateReportScheduleRequest"},{"type":"object","required":["id","ownerPrincipalId","isPaused","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid","description":"The schedule runs under this principal's permissions, not the recipients'. A standing grant of whatever the owner can see.\n"},"isPaused":{"type":"boolean"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"lastRunStatus":{"$ref":"#/components/schemas/ExecutionStatus"},"nextRunAt":{"type":"string","format":"date-time","nullable":true},"consecutiveFailures":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}}]},
"ReportSubscription": {"type":"object","x-ticvai-persistence":"reporting.subscription","description":"BI boards 4.3 and 4.4. **Not a schedule** — one schedule serves several of these.","required":["reportId"],"properties":{"id":{"type":"string","format":"uuid"},"reportId":{"type":"string","format":"uuid"},"scheduleId":{"type":"string","format":"uuid","nullable":true},"recipients":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid","nullable":true},"email":{"type":"string","nullable":true},"external":{"type":"boolean","default":false}}}},"channel":{"type":"string","enum":["email","sftp","webhook","inPlatform"]},"format":{"type":"string","enum":["pdf","xlsx","csv","json"]},"includesPersonalData":{"type":"boolean","default":false,"description":"**Gates on `REPORT_EXPORT_PII` and is audited.** A report that leaves the tenant with personal data in it is a fact somebody will ask about.\n"},"runsAsPrincipalId":{"type":"string","format":"uuid","description":"**The report runs under the owner's permissions, not the recipient's.**"},"active":{"type":"boolean","default":true},"scopePath":{"type":"string"}}},
"TenantDataRetentionClass": {"type":"string","description":"**The data classes a tenant sets a retention period for** (decided 29 September, Chinmay: all data retention is tenant configuration, one setting per class). Defaults are ADR-0047's and the AI system design's (section 8, decision 5); a legal limit is the only thing the platform enforces.\n| Class | Default | Counted from | Legal limit (refused) | |---|---|---|---| | `guestProfile` | 5 years | last activity | none | | `paymentRecord` | 10 years | created | at least 10 years (4.3.4) | | `financialRecord` | 7 years | created | at least 7 years (6.1.78) | | `auditRecord` | 2 years (authorisation and device audit) | created | none | | `approvalRecord` | 7 years (approvals board 6.7) | decided | none | | `complianceInspection` | 7 years | created | none | | `faceTagBiometric` | 7 days | ticket expiry | make-or-break | | `facePassBiometric` | follows `guestProfile` | last activity | make-or-break | | `aiPrompts` | 90 days (prompts and responses) | created | none | | `aiConversations` | 90 days | last activity | none | | `aiDecisionRecords` | follows `auditRecord` (decision records and the approvals of AI actions) | decided | none | | `aiMetadataIndex` | always follows `aiDecisionRecords` (summaries, entities, embeddings) | created | none |\n**ADR-0047's floors and ceilings that are not law are defaults now, not refusals** (the audit floor of one year, the proposed seven-year guest-profile ceiling, the Face Tag thirty-day ceiling). Platform-owned copies — the burst environment copy, a decommissioned cell — are not tenant data classes and are not here.\n","enum":["guestProfile","paymentRecord","financialRecord","auditRecord","approvalRecord","complianceInspection","faceTagBiometric","facePassBiometric","aiPrompts","aiConversations","aiDecisionRecords","aiMetadataIndex"]},
"TenantDataRetentionSetting": {"type":"object","x-ticvai-persistence":"tenancy.data_retention_setting","description":"**One tenant's retention period for one data class** (decided 29 September, Chinmay). One row per tenant and class, written by `setDataRetentionSetting`; a class with no row takes the platform default. The limit and default fields are the platform's catalogue, computed for the response and not stored on the row.\n","required":["dataClass"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"dataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"x-ticvai-unique":"tenant","description":"One row per class per tenant. On a write it comes from the path; a body value is ignored."},"retainAmount":{"type":"integer","nullable":true,"minimum":0,"description":"The tenant's period. Null with no `followsDataClass` means the platform default applies. Zero means the data is not kept past the transaction that produced it.\n"},"retainUnit":{"type":"string","nullable":true,"enum":["days","months","years"],"description":"Required with `retainAmount`."},"followsDataClass":{"allOf":[{"$ref":"#/components/schemas/TenantDataRetentionClass"}],"nullable":true,"description":"Keep this class for as long as another class is kept. Set by default for `aiDecisionRecords` (follows `auditRecord`), `facePassBiometric` (follows `guestProfile`) and `aiMetadataIndex` (follows `aiDecisionRecords`, and cannot be changed).\n"},"onExpiry":{"type":"string","enum":["archive","anonymise","delete"],"default":"archive","description":"ADR-0047's stages. `archive` moves the data to the archive instance, from where it is erased on the class's own schedule; derived stores (the AI index, search) purge at archive, not later.\n"},"anchor":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["createdAt","lastActivity","decidedAt","ticketExpiry"],"description":"What the period is counted from. Fixed per class by the platform."},"effectiveAmount":{"type":"integer","readOnly":true,"x-ticvai-persisted":false,"description":"The period actually applied, after follows and defaults are resolved."},"effectiveUnit":{"type":"string","readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"isDefault":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"description":"True when the tenant has not set this class and the platform default applies."},"defaultAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false},"defaultUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalMinimumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A floor the law sets. A shorter period is refused (`422`)."},"legalMaximumAmount":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"A maximum the law sets. A longer period is refused (`422`). Null for every class until the biometric make-or-break is answered."},"legalLimitUnit":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"enum":["days","months","years"]},"legalBasis":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"description":"The law or requirement the limit comes from, e.g. `4.3.4`."},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"updatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The tenant. Retention is set at tenant scope only."}}}
}
```
