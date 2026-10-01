# WS20 — Approval Workflows and Governance board 8

**10 screens · 6 operations · 10 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `APPROVAL_CONFIGURE, APPROVAL_VIEW, PRICE_VIEW, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-359` | Approval Executive KPI Dashboard | B–D | 2 | 0 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `ADM-360` | Approval Volume & Outcome Analytics | B–D | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |
| `ADM-361` | Approval Processing Time Analytics | B–D | 0 | 0 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `ADM-362` | Bottleneck Analysis & Heatmap | B–D | 0 | 12 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-363` | Approval Trend & Comparative Analytics | B–D | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |
| `ADM-364` | Approver & Team Performance Analytics | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-365` | Risk & Governance Analytics | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-366` | AI Approval Intelligence Center | B–D | 0 | 0 | 6 | 0 | 1 | 3 | — | notStarted (—) |
| `ADM-367` | AI Optimization & What-If Simulator | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-368` | AI Governance Executive Advisor | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-359, ADM-360, ADM-361, ADM-362, ADM-363, ADM-365, ADM-366, ADM-367, ADM-368 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-359` Approval Executive KPI Dashboard

**Provide executives and senior management with a high-level view of approval performance across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-executive-kpi-dashboard-adm-359` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search approval executive kpi | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, department, module, workflow, request type and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

#### Outputs: what the screen shows and produces

**Data it reads**: `getApprovalAnalytics` (onLoad, The executive view)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-368` AI Governance Executive Advisor: *AI Governance Executive Advisor*
- → `ADM-360` Approval Volume & Outcome Analytics: *Approval Volume & Outcome Analytics*
- → `ADM-361` Approval Processing Time Analytics: *Approval Processing Time Analytics*
- → `ADM-362` Bottleneck Analysis & Heatmap: *Bottleneck Analysis & Heatmap*
- → `ADM-363` Approval Trend & Comparative Analytics: *Approval Trend & Comparative Analytics*
- → `ADM-364` Approver & Team Performance Analytics: *Approver & Team Performance Analytics*
- → `ADM-365` Risk & Governance Analytics: *Risk & Governance Analytics*
- → `ADM-366` AI Approval Intelligence Center: *AI Approval Intelligence Center*
- → `ADM-367` AI Optimization & What-If Simulator: *AI Optimization & What-If Simulator*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval executive kpi list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval executive kpi untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval executive kpi yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval executive kpi are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval analytics shows how long each request took and overall turnaround across all logged requests. *(client request · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-734)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-359` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-359`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 8
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 1: Opens Approval Executive KPI Dashboard → Provide executives and senior management with a high-level view of approval performance across TICVAI.
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F130 branch at step 1 (expected): when Nothing has been set up on Approval Executive KPI Dashboard yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F130 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-359?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-368`, `ADM-360`, `ADM-361`, `ADM-362`, `ADM-363`, `ADM-364`, `ADM-365`, `ADM-366`, `ADM-367`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-360` Approval Volume & Outcome Analytics

**Analyze how many approval requests are being generated and what happens to them.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-volume-outcome-analytics-adm-360` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Data it reads**: `getApprovalAnalytics` (onLoad, Volume and outcome)

**Where the user goes next**

- → `ADM-359` Approval Executive KPI Dashboard: *Back to Approval Executive KPI Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval volume outcome list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval volume outcome untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval volume outcome yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval volume outcome are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-360` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-360`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 8
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 2: Works in Approval Volume & Outcome Analytics → Analyze how many approval requests are being generated and what happens to them.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-360?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-359`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-361` Approval Processing Time Analytics

**Measure exactly how long approval processes and individual stages take. The matrix explicitly requires processing-time analytics.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-processing-time-analytics-adm-361` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Data it reads**: `getApprovalAnalytics` (onLoad, Processing time)

**Where the user goes next**

- → `ADM-359` Approval Executive KPI Dashboard: *Back to Approval Executive KPI Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval processing time list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval processing time untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval processing time yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval processing time are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval analytics shows how long each request took and overall turnaround across all logged requests. *(client request · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-734)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-361` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-361`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 8
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 4: Works in Approval Processing Time Analytics → Measure exactly how long approval processes and individual stages take. The matrix explicitly requires processing-time analytics.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-361?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-359`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-362` Bottleneck Analysis & Heatmap

**Automatically identify where approval processes are becoming slow or congested. The source explicitly requires approval bottleneck analysis.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Columns) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/bottleneck-analysis-heatmap-adm-362` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workflow | text field | — | — | `listSlaEscalationBottleneck` ?workflow |
| Risk | text field | — | — | `listSlaEscalationBottleneck` ?risk |
| Escalation level | text field | — | — | `listSlaEscalationBottleneck` ?escalationLevel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every bottleneck analysis heatmap** (data table)

| Shows | Format | Notes |
|---|---|---|
| Refund | text | not in the schema: `Refund` |
| Discount | text | not in the schema: `Discount` |
| Price override | text | not in the schema: `Price Override` |
| Complimentary | text | not in the schema: `Complimentary` |
| Access change | text | not in the schema: `Access Change` |
| Configuration | text | not in the schema: `Configuration` |

**The selected bottleneck analysis heatmap** (detail panel): The pack groups this record's detail under its own headings: “Rows”, “Cells”, “Commercial”, “Director”.

| Shows | Format | Notes |
|---|---|---|
| Refund | text | not in the schema: `Refund` |
| Discount | text | not in the schema: `Discount` |
| Price override | text | not in the schema: `Price Override` |
| Complimentary | text | not in the schema: `Complimentary` |
| Access change | text | not in the schema: `Access Change` |
| Configuration | text | not in the schema: `Configuration` |

**Data it reads**: `listSlaEscalationBottleneck` (onLoad, Where it backs up)

**Where the user goes next**

- → `ADM-359` Approval Executive KPI Dashboard: *Back to Approval Executive KPI Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bottleneck analysis heatmap list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bottleneck analysis heatmap untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bottleneck analysis heatmap yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bottleneck analysis heatmap are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listSlaEscalationBottleneck` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval is human-governed (Qossai): AI is limited to analytics (turnaround, bottlenecks, individual approver performance) and must not recommend or influence whether a request is approved or rejected. *(agreed · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-735)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-362` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-362`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 8
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 6: Works in Bottleneck Analysis & Heatmap → Automatically identify where approval processes are becoming slow or congested. The source explicitly requires approval bottleneck analysis.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-362?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-359`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-363` Approval Trend & Comparative Analytics

**Identify whether approval performance is improving or deteriorating over time. The matrix specifically requires approval trend reporting.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-trend-comparative-analytics-adm-363` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Data it reads**: `getApprovalAnalytics` (onLoad, Trend and comparison)

**Where the user goes next**

- → `ADM-359` Approval Executive KPI Dashboard: *Back to Approval Executive KPI Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval trend comparative list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval trend comparative untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval trend comparative yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval trend comparative are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-363` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-363`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 8
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 8: Works in Approval Trend & Comparative Analytics → Identify whether approval performance is improving or deteriorating over time. The matrix specifically requires approval trend reporting.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-363?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-359`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-364` Approver & Team Performance Analytics

**Understand workload and operational performance at approver and team level without reducing governance to a simplistic employee ranking.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Metrics) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approver-team-performance-analytics-adm-364` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Assigned requests** (metric tile)

**Completed approvals** (metric tile)

**Average response time** (metric tile)

**SLA compliance** (metric tile)

**escalation rate** (metric tile)

**workload** (metric tile)

**pending queue** (metric tile)

**delegation frequency** (metric tile)

**approval/rejection ratio** (metric tile)

**Data it reads**: `getApprovalAnalytics` (onLoad, By approver and team)

**Where the user goes next**

- → `ADM-359` Approval Executive KPI Dashboard: *Back to Approval Executive KPI Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approver team performance list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approver team performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approver team performance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approver team performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval is human-governed (Qossai): AI is limited to analytics (turnaround, bottlenecks, individual approver performance) and must not recommend or influence whether a request is approved or rejected. *(agreed · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-735)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-364` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-364`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 8
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 10: Works in Approver & Team Performance Analytics → Understand workload and operational performance at approver and team level without reducing governance to a simplistic employee ranking.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-364?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-359`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-365` Risk & Governance Analytics

**Provide management with consolidated visibility of approval risk.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PRICE_VIEW`, `PRODUCT_VIEW` (2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/risk-governance-analytics-adm-365` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search risk governance analytics | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by workflow, venue, department, requester, approver, transaction type and 2 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Severity | radio group | — | Critical · High · Medium · Low | `listGovernanceRiskMonitoring` ?severity |
| Risk | select | — | Product without owner · Missing approval · Outdated pricing · Conflicting validity · Missing channel configuration · Orphaned dependency · Unused product · Duplicate product · Unusual configuration change · High override level · Scheduled publication conflict … | `listGovernanceRiskMonitoring` ?risk |
| Owner | text field | — | — | `listGovernanceRiskMonitoring` ?owner |
| Status | text field | — | — | `listGovernanceRiskMonitoring` ?status |

#### Outputs: what the screen shows and produces

**Data it reads**: `listGovernanceRiskMonitoring` (onLoad, Governance Risk, AI Monitoring & Control Center); `listGovernanceRiskLaunch` (onLoad, Governance Audit, AI Risk & Launch Readiness)

**Where the user goes next**

- → `ADM-359` Approval Executive KPI Dashboard: *Back to Approval Executive KPI Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The risk governance analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the risk governance analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No risk governance analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the risk governance analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGovernanceRiskMonitoring` → `PRODUCT_VIEW` (read) · staff
- `listGovernanceRiskLaunch` → `PRICE_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-365` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-365`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 8
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 12: Works in Risk & Governance Analytics → Provide management with consolidated visibility of approval risk.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-365?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-359`.
- [ ] Every gated control is gated: `PRICE_VIEW`, `PRODUCT_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-366` AI Approval Intelligence Center

**Provide one centralized location for AI-generated approval intelligence. This should be one of the strongest screens in the entire module.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `approvalRequestId` (navigation) |
| Route | `/platform/ai-approval-intelligence-center-adm-366` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel): One record, read-only.

**Data it reads**: `getApprovalAnalytics` (onLoad, What the models see); `getApprovalRequestScore` (onLoad, Risk band, priority and suggested escalation for the …)

**Where the user goes next**

- → `ADM-359` Approval Executive KPI Dashboard: *Back to Approval Executive KPI Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff
- `getApprovalRequestScore` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval is human-governed (Qossai): AI is limited to analytics (turnaround, bottlenecks, individual approver performance) and must not recommend or influence whether a request is approved or rejected. *(agreed · MoM 8 Sep 2026, 4.19 Approval Analytics & the Role of AI · DI-735)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-366` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-366`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 8
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 14: Works in AI Approval Intelligence Center → Provide one centralized location for AI-generated approval intelligence. This should be one of the strongest screens in the entire module.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-366?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-359`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-367` AI Optimization & What-If Simulator

**Allow management to evaluate proposed governance changes before implementing them.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-optimization-what-if-simulator-adm-367` |

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

- → `ADM-359` Approval Executive KPI Dashboard: *Back to Approval Executive KPI Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The optimization what-if simulator list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the optimization what-if simulator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No optimization what-if simulator yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the optimization what-if simulator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `simulateWorkflowTestingImpact` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-367` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-367`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 8
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 16: Works in AI Optimization & What-If Simulator → Allow management to evaluate proposed governance changes before implementing them.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-367?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-359`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-368` AI Governance Executive Advisor

**Turn all approval analytics into prioritized management recommendations. Instead of management examining dozens of dashboards, TICVAI AI should answer: “What requires my attention?”**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-governance-executive-advisor-adm-368` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Data it reads**: `getApprovalAnalytics` (onLoad, Governance for the executive)

**Where the user goes next**

- → `ADM-359` Approval Executive KPI Dashboard: *Back to Approval Executive KPI Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance executive advisor list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance executive advisor untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance executive advisor yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance executive advisor are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-368` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS37 Approval Workflows and Governance Board 8.dc.html#adm-368`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 8
- Flow F130 *Approval Workflows and Governance board 8: Approval Executive KPI Dashboard*, step 18: Works in AI Governance Executive Advisor → Turn all approval analytics into prioritized management recommendations. Instead of management examining dozens of dashboards, TICVAI AI should answer: “What requires my attention?”

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-368?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-359`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getApprovalAnalytics": {"method":"GET","path":"/approval-analytics","contract":"approvals","summary":"Volumes, times, rejections and bottlenecks","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ApprovalAnalytics"},
"getApprovalRequestScore": {"method":"GET","path":"/approval-requests/{approvalRequestId}/score","contract":"ai","summary":"The latest context score of an approval request","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiApprovalRequestScore"},
"listGovernanceRiskLaunch": {"method":"GET","path":"/governance-risk-launch","contract":"promotions","summary":"Governance Audit, AI Risk & Launch Readiness","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GovernanceAuditAiRiskLaunchReadinessView"},
"listGovernanceRiskMonitoring": {"method":"GET","path":"/governance-risk-monitoring","contract":"catalogue","summary":"Governance Risk, AI Monitoring & Control Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSlaEscalationBottleneck": {"method":"GET","path":"/sla-escalation-bottleneck","contract":"approvals","summary":"SLA, Escalation & Bottleneck Monitor","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workflow","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"escalationLevel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"simulateWorkflowTestingImpact": {"method":"PUT","path":"/workflow-testing-impact","contract":"approvals","summary":"Workflow Testing, Simulation & Impact Analysis","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkflowTestingSimulationImpactAnalysisInput","responds":"WorkflowTestingSimulationImpactAnalysisView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiApprovalRequestScore": {"type":"object","x-ticvai-persistence":"ai.approval_request_score","description":"**Context for an approval reviewer** (11.1.73..75): risk, priority and a suggested escalation for one pending request, the latest per request. **There is no approve or reject field, by design** (minutes of 8 September: AI in approvals never recommends or influences approve or reject).","required":["approvalRequestId","riskScore","riskBand","priorityScore","escalationSuggestion"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"approvalRequestId":{"type":"string","format":"uuid","x-ticvai-references":"approvals.request"},"trigger":{"type":"string","enum":["submitted","resubmitted","slaTick","escalated"]},"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"],"description":"Design 5.6: a risk score and band, never a probability."},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"description":"For ordering work in an inbox; higher first."},"escalationSuggestion":{"type":"object","required":["action"],"properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}},"description":"A suggestion for an SLA problem, carried out if at all by a person or the tenant's SLA policy."},"signals":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","description":"e.g. `amountAboveRequesterNorm`, `requesterEntityRisk`, `outOfHours`, `irreversibleAction`, `slaDueSoon`, `stepBreachRate`, `approverUnavailable`."},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"scoredAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"ApprovalAnalytics": {"type":"object","x-ticvai-persistence":"none — aggregated from approvals.request","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"groupBy":{"type":"string","description":"The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it.","enum":["kind","approver","venue","day","week"]},"rows":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"raised":{"type":"integer"},"approved":{"type":"integer"},"rejected":{"type":"integer"},"withdrawn":{"type":"integer"},"expired":{"type":"integer","description":"**Requests nobody answered.** Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person.\n"},"escalated":{"type":"integer"},"slaBreached":{"type":"integer"},"medianMinutes":{"type":"number"},"p95Minutes":{"type":"number"}}}}}},
"GovernanceAuditAiRiskLaunchReadinessView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over promotions state, assembled at read time from tables that already exist","description":"**What Governance Audit, AI Risk & Launch Readiness displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"promotionConfiguration":{"type":"string","description":"Promotion Configuration ✓"},"eligibility":{"type":"string","description":"Eligibility ✓"},"stackingRules":{"type":"string","description":"Stacking Rules ✓"},"budget":{"type":"string","description":"Budget ✓"},"redemptionLimits":{"type":"string","description":"Redemption Limits ✓"},"marginGuardrail":{"type":"number","description":"Margin Guardrail ✓"},"simulationCompleted":{"type":"string","description":"Simulation Completed ✓"},"requiredApproval":{"type":"string","description":"Required Approval ✓"},"channelPublication":{"type":"string","description":"Channel Publication ✓"},"auditRequirements":{"type":"string","description":"Audit Requirements ✓"},"budgetCreation":{"type":"string","description":"Budget creation"},"budgetChange":{"type":"string","description":"Budget change"},"limitChanges":{"type":"integer","description":"Limit changes"},"approvalSubmissions":{"type":"string","description":"Approval submissions"},"approvalDecisions":{"type":"string","description":"Approval decisions"},"overrides":{"type":"string","description":"Overrides"},"automaticSuspension":{"type":"string","description":"Automatic suspension"},"reactivation":{"type":"string","description":"Reactivation"},"simulationResults":{"type":"string","description":"Simulation results"},"experimentChanges":{"type":"string","description":"Experiment changes"},"campaignLaunch":{"type":"string","description":"Campaign launch"}}},
"GovernanceRiskAiMonitoringControlCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Governance Risk, AI Monitoring & Control Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"risk":{"type":"string","enum":["productWithoutOwner","missingApproval","outdatedPricing","conflictingValidity","missingChannelConfiguration","orphanedDependency","unusedProduct","duplicateProduct","unusualConfigurationChange","highOverrideLevel","scheduledPublicationConflict","expiredCommercialConfiguration","activeAfterEventEnd","brokenDependency"],"description":"Risk detected (AI Monitoring, pack p.26)"},"product":{"type":"string","description":"Product name"},"venue":{"type":"string","description":"Venue name"},"businessImpact":{"type":"string","description":"Business impact, in plain language"},"recommendedAction":{"type":"string","description":"Recommended action; advisory"},"owner":{"type":"string","description":"Owner (display name)","nullable":true},"dueDate":{"type":"string","description":"Due date","format":"date","nullable":true},"status":{"type":"string","description":"Status: open, acknowledged, inRemediation, resolved or dismissed (decided 29 September, readiness close-out)"},"riskId":{"type":"string","description":"Risk id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid","nullable":true},"severity":{"type":"string","enum":["critical","high","medium","low"],"description":"Severity (Risk Dashboard)"},"explanation":{"type":"string","description":"AI explanation, e.g. the two products share 96% of their configuration; advisory"},"detectedAt":{"type":"string","description":"Detected","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SlaEscalationBottleneckMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_instance, whose SLA and reminder timestamps it lists (data model for the agreed operations, 29 September)","description":"**What SLA, Escalation & Bottleneck Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflow":{"type":"string","description":"Workflow"},"instance":{"type":"string","description":"Instance"},"currentStep":{"type":"string","description":"Current Step"},"owner":{"type":"string","description":"Owner"},"started":{"type":"string","format":"date-time","description":"Started"},"target":{"type":"string","format":"date-time","description":"SLA deadline"},"timeRemaining":{"type":"integer","description":"Minutes until breach; negative once breached"},"risk":{"type":"string","description":"Risk"},"escalationLevel":{"type":"string","description":"Escalation Level"},"firstReminder":{"type":"string","format":"date-time","description":"First Reminder"},"secondReminder":{"type":"string","format":"date-time","description":"Second Reminder"},"managerEscalation":{"type":"string","format":"date-time","description":"Manager Escalation"},"executiveEscalation":{"type":"string","format":"date-time","description":"Executive Escalation"},"finalOutcome":{"type":"string","description":"Final Outcome"}},"required":["instance"]},
"SlaEscalationBottleneckMonitorViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"withinSla":{"type":"integer","description":"Within SLA"},"atRisk":{"type":"integer","description":"At Risk"},"breached":{"type":"integer","description":"Breached"},"escalated":{"type":"integer","description":"Escalated"},"averageProcessingTime":{"type":"integer","description":"Minutes"},"averageApprovalTime":{"type":"integer","description":"Minutes"},"longestWaitingStep":{"type":"string","description":"Longest Waiting Step"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"WorkflowTestingSimulationImpactAnalysisInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; the outcome is recorded as approvals.workflow_version test results (data model for the agreed operations, 29 September)","description":"**What Workflow Testing, Simulation & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"workflowId":{"type":"string","description":"Workflow under test"},"testMode":{"type":"string","enum":["manualTestCase","sampleTransaction","historicalReplay","scenarioSimulation","batchTest"],"description":"How the workflow is tested"},"version":{"type":"string","description":"Version under test"},"compareWithVersion":{"type":"string","description":"Existing version to compare against for regression"},"inputPayload":{"type":"string","description":"Sample transaction as a JSON document, for manual and sample tests"},"replayFrom":{"type":"string","format":"date","description":"Historical replay start"},"replayTo":{"type":"string","format":"date","description":"Historical replay end"}},"required":["workflowId","testMode"]},
"WorkflowTestingSimulationImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — computed by simulation over approvals.workflow_version and the rules it calls; never executes actions (data model for the agreed operations, 29 September)","description":"**What Workflow Testing, Simulation & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowId":{"type":"string","description":"Workflow under test"},"testMode":{"type":"string","enum":["manualTestCase","sampleTransaction","historicalReplay","scenarioSimulation","batchTest"],"description":"How the workflow is tested"},"rulesEvaluated":{"type":"integer","description":"Rules Evaluated"},"conditionsMatched":{"type":"integer","description":"Conditions Matched"},"decisions":{"type":"integer","description":"Decisions"},"approvalPath":{"type":"string","description":"Approval Path"},"actions":{"type":"integer","description":"Actions"},"notifications":{"type":"integer","description":"Notifications"},"sla":{"type":"string","description":"SLA"},"expectedOutcome":{"type":"string","description":"Expected Outcome"},"version":{"type":"string","description":"Version under test"},"compareWithVersion":{"type":"string","description":"Existing version to compare against for regression"},"inputPayload":{"type":"string","description":"Sample transaction as a JSON document, for manual and sample tests"},"replayFrom":{"type":"string","format":"date","description":"Historical replay start"},"replayTo":{"type":"string","format":"date","description":"Historical replay end"}},"required":["workflowId","testMode"]}
}
```
