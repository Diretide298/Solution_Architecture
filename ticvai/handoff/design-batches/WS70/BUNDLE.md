# WS70 — Unified BI Reporting and AI Analytics Platform board 9

**10 screens · 23 operations · 45 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `AI_APPROVE, AI_CONFIGURE, AI_USE, REPORT_MANAGE, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `ANL-051` | AI Analytics Command Center | B–D | 0 | 40 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ANL-052` | Ask TICVAI — Natural Language Analytics | B–D | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `ANL-053` | AI-Generated Dashboard Studio | B–D | 0 | 0 | 6 | 18 | 1 | 0 | — | notStarted (—) |
| `ANL-054` | AI Report Generator | B–D | 0 | 14 | 6 | 82 | 1 | 0 | — | notStarted (—) |
| `ANL-055` | Anomaly Detection Center | B–D | 0 | 20 | 6 | 4 | 0 | 0 | — | notStarted (—) |
| `ANL-056` | Root-Cause Analysis Explorer | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `ANL-057` | Forecasting & Predictive Analytics Studio | B–D | 7 | 0 | 5 | 39 | 1 | 0 | — | notStarted (—) |
| `ANL-058` | AI Recommendation & Next-Best-Action Center | B–D | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `ANL-059` | AI Insight History, Evidence & Explainability | B–D | 5 | 0 | 5 | 1 | 0 | 0 | — | notStarted (—) |
| `ANL-060` | AI Analytics Governance & Model Control | B–D | 0 | 26 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ANL-051, ANL-052, ANL-053, ANL-054, ANL-055, ANL-056, ANL-058 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ANL-051` AI Analytics Command Center

**Provide a centralized landing page for all AI-generated analytical intelligence across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/ai-analytics-command-center-anl-051` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAnalyticsAnomalies` ?from |
| Severity | segmented control | — | Low · Medium · High | `listAnalyticsAnomalies` ?severity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every analytics** (data table)

| Shows | Format | Notes |
|---|---|---|
| Executive insights | text | not in the schema: `Executive Insights` |
| Revenue insights | text | not in the schema: `Revenue Insights` |
| Operations insights | text | not in the schema: `Operations Insights` |
| Customer insights | text | not in the schema: `Customer Insights` |
| Finance insights | text | not in the schema: `Finance Insights` |
| Marketing insights | text | not in the schema: `Marketing Insights` |
| Access insights | text | not in the schema: `Access Insights` |
| Membership/loyalty insights | text | not in the schema: `Membership/Loyalty Insights` |
| Forecasts | text | not in the schema: `Forecasts` |
| Anomalies | text | not in the schema: `Anomalies` |
| Opportunities | text | not in the schema: `Opportunities` |
| Risks | text | not in the schema: `Risks` |
| New AI insights | text | not in the schema: `New AI Insights` |
| Critical insights | text | not in the schema: `Critical Insights` |
| Opportunities detected | text | not in the schema: `Opportunities Detected` |
| Risks detected | text | not in the schema: `Risks Detected` |
| Active anomalies | text | not in the schema: `Active Anomalies` |
| Forecast alerts | text | not in the schema: `Forecast Alerts` |
| Recommendations pending review | text | not in the schema: `Recommendations Pending Review` |
| AI queries today | text | not in the schema: `AI Queries Today` |

**The selected analytics** (detail panel): The pack groups this record's detail under its own headings: “Revenue Opportunity”.

| Shows | Format | Notes |
|---|---|---|
| Executive insights | text | not in the schema: `Executive Insights` |
| Revenue insights | text | not in the schema: `Revenue Insights` |
| Operations insights | text | not in the schema: `Operations Insights` |
| Customer insights | text | not in the schema: `Customer Insights` |
| Finance insights | text | not in the schema: `Finance Insights` |
| Marketing insights | text | not in the schema: `Marketing Insights` |
| Access insights | text | not in the schema: `Access Insights` |
| Membership/loyalty insights | text | not in the schema: `Membership/Loyalty Insights` |
| Forecasts | text | not in the schema: `Forecasts` |
| Anomalies | text | not in the schema: `Anomalies` |
| Opportunities | text | not in the schema: `Opportunities` |
| Risks | text | not in the schema: `Risks` |
| New AI insights | text | not in the schema: `New AI Insights` |
| Critical insights | text | not in the schema: `Critical Insights` |
| Opportunities detected | text | not in the schema: `Opportunities Detected` |
| Risks detected | text | not in the schema: `Risks Detected` |
| Active anomalies | text | not in the schema: `Active Anomalies` |
| Forecast alerts | text | not in the schema: `Forecast Alerts` |
| Recommendations pending review | text | not in the schema: `Recommendations Pending Review` |
| AI queries today | text | not in the schema: `AI Queries Today` |

**Data it reads**: `listAnalyticsAnomalies` (onLoad, What the models noticed)

**Where the user goes next**

- → `ANL-001` Executive Command Center: *Back to Executive Command Center*
- → `ANL-060` AI Analytics Governance & Model Control: *AI Analytics Governance & Model Control*
- → `ANL-052` Ask TICVAI — Natural Language Analytics: *Ask TICVAI — Natural Language Analytics*
- → `ANL-053` AI-Generated Dashboard Studio: *AI-Generated Dashboard Studio*
- → `ANL-054` AI Report Generator: *AI Report Generator*
- → `ANL-055` Anomaly Detection Center: *Anomaly Detection Center*
- → `ANL-056` Root-Cause Analysis Explorer: *Root-Cause Analysis Explorer*
- → `ANL-057` Forecasting & Predictive Analytics Studio: *Forecasting & Predictive Analytics Studio*
- → `ANL-058` AI Recommendation & Next-Best-Action Center: *AI Recommendation & Next-Best-Action Center*
- → `ANL-059` AI Insight History, Evidence & Explainability: *AI Insight History, Evidence & Explainability*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The analytics list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No analytics yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the analytics are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAnalyticsAnomalies` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-051` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-051`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 1: Opens AI Analytics Command Center → Provide a centralized landing page for all AI-generated analytical intelligence across TICVAI.
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F179 branch at step 1 (expected): when Nothing has been set up on AI Analytics Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F179 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-051?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-001`, `ANL-060`, `ANL-052`, `ANL-053`, `ANL-054`, `ANL-055`, `ANL-056`, `ANL-057`, `ANL-058`, `ANL-059`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-052` Ask TICVAI — Natural Language Analytics

**Allow users to query TICVAI business information using normal language instead of manually building reports.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE`, `REPORT_VIEW_VENUE` (1 configure, 1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `conversationId` (navigation) |
| Route | `/analytics/ask-ticvai-natural-language-analytics-anl-052` |

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

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ask ticvai natural list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ask ticvai natural untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ask ticvai natural yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ask ticvai natural are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem) |

#### Permissions

- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `saveNaturalLanguageQuery` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Conversational report building (Qossai): user asks e.g. "show me the top 10 products sold last week"; the AI asks clarifying questions when timeframe, venue or metric are missing instead of guessing or regenerating. *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-712)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-052` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-052`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 2: Works in Ask TICVAI — Natural Language Analytics → Allow users to query TICVAI business information using normal language instead of manually building reports.
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-052?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `REPORT_MANAGE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-053` AI-Generated Dashboard Studio

**Allow users to generate dashboards from natural-language requests.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/ai-generated-dashboard-studio-anl-053` |

**Known gaps.** **AI-Generated Dashboard Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create dashboard (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ai-generated list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ai-generated untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ai-generated yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the ai-generated are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The tiles' refreshes per minute exceed `VenueSettings.reporting.dashboardRefreshBudgetPerMinute` (proposed default 24, audit R094); 409 The caller is not entitled to the dashboard's module — the tenant has not licensed it, or the principal holds no permission in it. |

#### Permissions

- `createDashboard` → `REPORT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.79 | System shall monitor operational service levels. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 1.3.27 | System shall provide real-time dashboards showing attendance, check-ins, occupancy, sales, capacity utilization and operational KPIs. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 1.3.28 | System shall provide event performance analytics including attendance, revenue, conversion rates, capacity utilization and customer engagement. | Ticketing Catalogue | CONTRACTED | `createDashboard` |
| 8.7.1 | System shall provide executive dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.2 | System shall provide operational dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.3 | System shall provide financial dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.4 | System shall provide sales dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.5 | System shall provide marketing dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.6 | System shall provide ticketing dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.7 | System shall provide access control dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.8 | System shall provide membership dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| 8.7.9 | System shall provide loyalty dashboards. | Unified Operations Dashboard | CONTRACTED | `createDashboard` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Conversational report building (Qossai): user asks e.g. "show me the top 10 products sold last week"; the AI asks clarifying questions when timeframe, venue or metric are missing instead of guessing or regenerating. *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-712)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-053` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-053`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 4: Works in AI-Generated Dashboard Studio → Allow users to generate dashboards from natural-language requests.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-053?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create dashboard, Cancel.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-054` AI Report Generator

**Generate detailed reports from natural-language instructions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/ai-report-generator-anl-054` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every report generator** (data table)

| Shows | Format | Notes |
|---|---|---|
| Selected dataset | text | not in the schema: `Selected Dataset` |
| Fields | text | not in the schema: `Fields` |
| Filters | text | not in the schema: `Filters` |
| Grouping | text | not in the schema: `Grouping` |
| Calculations | text | not in the schema: `Calculations` |
| Sort | text | not in the schema: `Sort` |
| Output | text | not in the schema: `Output` |

**The selected report generator** (detail panel): The pack groups this record's detail under its own headings: “User asks”, “Dimensions”, “Measures”, “Relationship to Board 3”.

| Shows | Format | Notes |
|---|---|---|
| Selected dataset | text | not in the schema: `Selected Dataset` |
| Fields | text | not in the schema: `Fields` |
| Filters | text | not in the schema: `Filters` |
| Grouping | text | not in the schema: `Grouping` |
| Calculations | text | not in the schema: `Calculations` |
| Sort | text | not in the schema: `Sort` |
| Output | text | not in the schema: `Output` |

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The report generator list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the report generator untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No report generator yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the report generator are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Unknown field, invalid filter, or estimated cost beyond the limit |

#### Permissions

- `createReport` → `REPORT_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

82 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.40 | System shall provide analytics and dashboards covering ticket sales, attendance, utilization, conversion rates, capacity utilization and revenue performance. | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.104 | Membership analytics | Ticketing Catalogue | CONTRACTED | `createReport` |
| 1.1.135 | Required Reports Operational Reports Donations by Campaign. Donations by Site. Donations by Product. Donations by Sales Channel. Donations by Date. Donations by User/Cashier. Donations by Payment … | Ticketing Catalogue | CONTRACTED | `createReport` |
| 3.2.65 | An Entry or Exit report is expected presenting the readings per outcome (ok/ko), per time and per access point. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.66 | The in park report showing the difference between the Entries and the Exits. | Admission and Access | CONTRACTED | `createReport` |
| 3.2.68 | The length of stay report shall present the difference between the time in scan and the time out scan. | Admission and Access | CONTRACTED | `createReport` |
| 3.5.12 | System shall provide analytics showing bundle sales volume, revenue contribution, conversion rate, redemption rate, average order value impact, profitability, and performance by channel. | Admission and Access | CONTRACTED | `createReport` |
| 3.7.11 | System shall provide reporting on upsell impressions, conversion rates, revenue generated, average order value uplift, and campaign effectiveness across channels. | Admission and Access | CONTRACTED | `createReport` |
| 5.6.28 | Provide reporting on wait times, abandonment rates, no-shows, throughput, utilization, and satisfaction. | F&B & Guest Management | CONTRACTED | `createReport` |
| 6.1.5 | The system should be able to Generate reports with admission types/information. | Retail POS | CONTRACTED | `createReport` |
| 6.1.8 | The system should have the ability to retrieve information "on the fly" for items, (e.g., keyword, item #, description, category etc.) in user-friendly format such as pull-down menus and/or auto fill … | Retail POS | CONTRACTED | `createReport` |
| 6.1.9 | The system should be able to report historical sales look up by item, ticket number etc.. | Retail POS | CONTRACTED | `createReport` |
| … 70 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Conversational report building (Qossai): user asks e.g. "show me the top 10 products sold last week"; the AI asks clarifying questions when timeframe, venue or metric are missing instead of guessing or regenerating. *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-712)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-054` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-054`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 6: Works in AI Report Generator → Generate detailed reports from natural-language instructions.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-054?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `REPORT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-055` Anomaly Detection Center

**Automatically identify unusual behavior across TICVAI data without requiring users to manually monitor every KPI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_CONFIGURE`, `AI_USE`, `REPORT_VIEW_VENUE` (1 configure, 2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each Anomaly Displays) and no metric row |
| Offline | online only |
| Opens with | `detectorKey` (navigation) |
| Route | `/analytics/anomaly-detection-center-anl-055` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAnalyticsAnomalies` ?from |
| Severity | segmented control | — | Low · Medium · High | `listAnalyticsAnomalies` ?severity |
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listAiInsights` ?status |
| Kind | select | — | Anomaly · Forecast deviation · Trend · Opportunity · Executive summary · Root cause · Forecast threshold · Marketing recommendation | `listAiInsights` ?kind |
| Priority | radio group | — | Low · Medium · High · Critical | `listAiInsights` ?priority |
| From | date and time picker | — | — | `listAiInsights` ?from |
| Metric key | text field | — | — | `listAnomalyDetectors` ?metricKey |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every anomaly detection** (data table)

| Shows | Format | Notes |
|---|---|---|
| KPI | text | not in the schema: `KPI` |
| Expected range | text | not in the schema: `Expected Range` |
| Actual value | text | not in the schema: `Actual Value` |
| Variance | text | not in the schema: `Variance` |
| Severity | text | not in the schema: `Severity` |
| Start time | text | not in the schema: `Start Time` |
| Duration | text | not in the schema: `Duration` |
| Affected site | text | not in the schema: `Affected Site` |
| Affected domain | text | not in the schema: `Affected Domain` |
| Confidence | text | not in the schema: `Confidence` |

**The selected anomaly detection** (detail panel): The pack groups this record's detail under its own headings: “Detect abnormal patterns involving”, “High Refund Anomaly”, “Detection Methods”.

| Shows | Format | Notes |
|---|---|---|
| KPI | text | not in the schema: `KPI` |
| Expected range | text | not in the schema: `Expected Range` |
| Actual value | text | not in the schema: `Actual Value` |
| Variance | text | not in the schema: `Variance` |
| Severity | text | not in the schema: `Severity` |
| Start time | text | not in the schema: `Start Time` |
| Duration | text | not in the schema: `Duration` |
| Affected site | text | not in the schema: `Affected Site` |
| Affected domain | text | not in the schema: `Affected Domain` |
| Confidence | text | not in the schema: `Confidence` |

**Data it reads**: `listAnalyticsAnomalies` (onLoad, Anomalies, with severity); `listAiInsights` (onLoad, Insights and anomalies); `listAnomalyDetectors` (onLoad, Anomaly detectors)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The anomaly detection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the anomaly detection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No anomaly detection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the anomaly detection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAnalyticsAnomalies` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAiInsights` → `AI_USE` (operate) · staff
- `configureAnomalyDetector` → `AI_CONFIGURE` (configure) · staff
- `listAnomalyDetectors` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.17 | System shall support AI-powered anomaly explanations. | Unified Operations Dashboard | CONTRACTED | `listAiInsights` |
| 8.2.20 | System shall generate attendance forecast alerts when predefined thresholds are exceeded. | Unified Operations Dashboard | CONTRACTED | `configureAnomalyDetector` |
| 8.2.41 | System shall generate capacity alerts. | Unified Operations Dashboard | CONTRACTED | `configureAnomalyDetector` |
| 8.3.16 | System shall detect abnormal refund volumes. | Unified Operations Dashboard | CONTRACTED | `configureAnomalyDetector` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-055` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-055`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 8: Works in Anomaly Detection Center → Automatically identify unusual behavior across TICVAI data without requiring users to manually monitor every KPI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-055?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-056` Root-Cause Analysis Explorer

**Help users understand why a KPI changed. This is one of the most important AI capabilities in the entire platform.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/root-cause-analysis-explorer-anl-056` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAnalyticsAnomalies` ?from |
| Severity | segmented control | — | Low · Medium · High | `listAnalyticsAnomalies` ?severity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAnalyticsAnomalies` (onLoad, Candidate causes)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The root-cause analysis list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the root-cause analysis untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No root-cause analysis yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the root-cause analysis are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Question could not be interpreted. (ReportQuestionProblem) |

#### Permissions

- `listAnalyticsAnomalies` → `REPORT_VIEW_VENUE` (operate) · staff
- `askReportingQuestion` → `REPORT_VIEW_VENUE` (operate) · staff, partner
- `explainMetricChange` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.7.30 | System shall support natural language reporting. | Unified Operations Dashboard | CONTRACTED | `askReportingQuestion` |
| 8.4.18 | System shall support AI-powered root cause analysis. | Unified Operations Dashboard | CONTRACTED | `explainMetricChange` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- An AI layer across all dashboards explains why a metric changed (e.g. why revenue dropped on a given day) and recommends management actions from sales, revenue and attendance trends. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-719)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-056` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-056`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 10: Works in Root-Cause Analysis Explorer → Help users understand why a KPI changed. This is one of the most important AI capabilities in the entire platform.
- ADR-0054 *Natural-language analytics goes through the semantic layer* (`docs/adr/0054-natural-language-analytics-goes-through-the-semantic-layer.md`)
- ADR-0059 *AI phasing against the six-month plan* (`docs/adr/0059-ai-phasing-against-the-six-month-plan.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-056?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-057` Forecasting & Predictive Analytics Studio

**Provide configurable forward-looking analytics across business domains.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `versionId` (navigation) |
| Route | `/analytics/forecasting-predictive-analytics-studio-anl-057` |

**Known gaps.** **The pack names 11 actions on this screen and the screen declares 0 operations.** Unserved: Revenue, Ticket Sales, Attendance, Capacity, Queue Demand, Cash Collection, Membership Renewals, Customer … **Forecasting & Predictive Analytics Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Next Hour | select field | — | — | — | — | — | — |
| Today | select field | — | — | — | — | — | — |
| Tomorrow | select field | — | — | — | — | — | — |
| Next 7 Days | select field | — | — | — | — | — | — |
| Month End | select field | — | — | — | — | — | — |
| Quarter | select field | — | — | — | — | — | — |
| Custom | select field | — | — | — | — | — | — |

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
| Subject | select | — | Attendance · Arrival pattern · Product demand · Timeslot demand · Channel pace · Revenue · Occupancy · Attraction utilisation · Queue · Entry flow · Staffing · POS demand … | `listForecastDefinitions` ?subject |
| Definition key | text field | — | — | `getForecast` ?definitionKey |
| Version | picker: choose a version | — | — | `getForecast` ?versionId |
| From | date and time picker | — | — | `getForecast` ?from |
| To | date and time picker | — | — | `getForecast` ?to |
| Dimension key | text field | — | — | `getForecast` ?dimensionKey |
| Scenario | picker: choose a scenario | — | — | `getForecast` ?scenarioId |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Revenue (primary button) | navigation or local | — | — | — | — |
| Ticket Sales (secondary button) | navigation or local | — | — | — | — |
| Attendance (secondary button) | navigation or local | — | — | — | — |
| Capacity (secondary button) | navigation or local | — | — | — | — |
| Queue Demand (secondary button) | navigation or local | — | — | — | — |
| Cash Collection (secondary button) | navigation or local | — | — | — | — |
| Membership Renewals (secondary button) | navigation or local | — | — | — | — |
| Customer Churn (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getKpiValues` (onLoad, The series being forecast); `listForecastDefinitions` (onLoad, What is forecast); `getForecast` (onLoad, Forecast values)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The forecasting predictive analytics configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the forecasting predictive analytics untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No forecasting predictive analytics configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Permissions

- `getKpiValues` → `REPORT_VIEW_VENUE` (operate) · staff
- `listForecastDefinitions` → `AI_USE` (operate) · staff
- `getForecast` → `AI_USE` (operate) · staff
- `createForecastScenario` → `AI_USE` (operate) · staff
- `exportForecastVersion` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

39 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.55 | AI shall forecast future resource demand. | Ticketing Catalogue | CONTRACTED | `getForecast` |
| 4.1.17 | Forecast demand based on historical and operational data. | Bundles and Promotions | CONTRACTED | `getForecast` |
| 5.6.26 | Predict queue lengths, wait times, peak demand, and capacity shortages. | F&B & Guest Management | CONTRACTED | `getForecast` |
| 8.2.1 | System shall forecast attendance based on historical attendance patterns. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.2 | System shall forecast attendance by venue. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.3 | System shall forecast attendance by attraction. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.4 | System shall forecast attendance by event. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.5 | System shall forecast attendance by session. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.6 | System shall forecast attendance by date range. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.7 | System shall forecast attendance by day of week. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.8 | System shall forecast attendance by month. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| 8.2.9 | System shall forecast attendance by season. | Unified Operations Dashboard | CONTRACTED | `getForecast` |
| … 27 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Data-dependent forecasting (demand/revenue) cannot be delivered in phase one for lack of history, though its front end, back end and data components can be built. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-280)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-057` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-057`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 12: Works in Forecasting & Predictive Analytics Studio → Provide configurable forward-looking analytics across business domains.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-057?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Revenue, Ticket Sales, Attendance, Capacity, Queue Demand, Cash Collection, Membership Renewals, Customer Churn.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-058` AI Recommendation & Next-Best-Action Center

**Convert analytical insights into prioritized business recommendations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/analytics/ai-recommendation-next-best-action-center-anl-058` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAnalyticsAnomalies` ?from |
| Severity | segmented control | — | Low · Medium · High | `listAnalyticsAnomalies` ?severity |
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listAiInsights` ?status |
| Kind | select | — | Anomaly · Forecast deviation · Trend · Opportunity · Executive summary · Root cause · Forecast threshold · Marketing recommendation | `listAiInsights` ?kind |
| Priority | radio group | — | Low · Medium · High · Critical | `listAiInsights` ?priority |
| From | date and time picker | — | — | `listAiInsights` ?from |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listAnalyticsAnomalies` (onLoad, What to act on); `listAiInsights` (onLoad, Insights and anomalies)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The recommendation next-best-action list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the recommendation next-best-action untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No recommendation next-best-action yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the recommendation next-best-action are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAnalyticsAnomalies` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAiInsights` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.17 | System shall support AI-powered anomaly explanations. | Unified Operations Dashboard | CONTRACTED | `listAiInsights` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- An AI layer across all dashboards explains why a metric changed (e.g. why revenue dropped on a given day) and recommends management actions from sales, revenue and attendance trends. *(client request · MoM 8 Sep 2026, 4.10 AI Intelligence Layer & KPI/Benchmarking Administration · DI-719)*

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-058` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-058`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 14: Works in AI Recommendation & Next-Best-Action Center → Convert analytical insights into prioritized business recommendations.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-058?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-059` AI Insight History, Evidence & Explainability

**Create a full governance trail for AI-generated analytics and recommendations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `REPORT_VIEW_VENUE` (2 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `insightId` (navigation) |
| Route | `/analytics/ai-insight-history-evidence-explainability-anl-059` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Who asked | select field | — | — | — | — | — | — |
| What data was accessed | text field | — | — | — | — | — | — |
| What answer was generated | text field | — | — | — | — | — | — |
| Whether it was exported/shared | text field | — | — | — | — | — | — |
| Whether recommendation was accepted | text field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listAnalyticsAnomalies` ?from |
| Severity | segmented control | — | Low · Medium · High | `listAnalyticsAnomalies` ?severity |
| Status | select | — | New · Reviewed · Accepted · Rejected · Actioned · Measured | `listAiInsights` ?status |
| Kind | select | — | Anomaly · Forecast deviation · Trend · Opportunity · Executive summary · Root cause · Forecast threshold · Marketing recommendation | `listAiInsights` ?kind |
| Priority | radio group | — | Low · Medium · High · Critical | `listAiInsights` ?priority |
| From | date and time picker | — | — | `listAiInsights` ?from |

#### Outputs: what the screen shows and produces

**Data it reads**: `listAnalyticsAnomalies` (onLoad, Past insights and their evidence); `listAiInsights` (onLoad, Insights and anomalies)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The insight history evidence configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the insight history evidence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No insight history evidence configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The move is not allowed from the insight's state. |

#### Permissions

- `listAnalyticsAnomalies` → `REPORT_VIEW_VENUE` (operate) · staff
- `listAiInsights` → `AI_USE` (operate) · staff
- `decideAiInsight` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.4.17 | System shall support AI-powered anomaly explanations. | Unified Operations Dashboard | CONTRACTED | `listAiInsights` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-059` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-059`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 16: Works in AI Insight History, Evidence & Explainability → Create a full governance trail for AI-generated analytics and recommendations.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-059?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_USE`, `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ANL-060` AI Analytics Governance & Model Control

**Provide administrators with centralized control over how AI may access and use TICVAI analytics. This screen is critical because Board 9 should not give an LLM unrestricted access to the TICVAI database.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P16 Venue Analytics (web) |
| Module | Analytics · wave 3 · needs the `analytics` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE` (2 operate, 1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Track) and no metric row |
| Offline | online only |
| Opens with | `capabilityKey` (navigation), `templateKey` (navigation) |
| Route | `/analytics/ai-analytics-governance-model-control-anl-060` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Family | select | — | Gateway and models · Governance · Action pipeline · Knowledge retrieval · Assistants · Analytics insights · Configuration assistant · Forecasting · Anomaly detection · Risk intelligence · Recommendations · Decision records … | `listAiCapabilities` ?family |
| Status | segmented control | — | Active · Paused | `listAiCapabilities` ?status |
| Risk class | radio group | — | Low · Medium · High · Critical | `listAiCapabilities` ?riskClass |
| Capability key | text field | — | — | `getEffectiveAiPolicy` ?capabilityKey |
| Scope path | text field | — | — | `getEffectiveAiPolicy` ?scopePath |
| Environment | radio group | — | Development · Sandbox · Staging · Production | `getEffectiveAiPolicy` ?environment |
| Layer | segmented control | — | Platform · Tenant | `listAiModels` ?layer |
| Producer type | radio group | — | Llm · Embedding · Reranker · Classical · Rule | `listAiModels` ?producerType |
| Task | text field | — | — | `listPromptTemplates` ?task |
| Layer | segmented control | — | Platform · Tenant | `listPromptTemplates` ?layer |
| Status | segmented control | — | Draft · Published · Retired | `listPromptTemplates` ?status |
| Release | picker: choose a release | — | — | `listAiEvaluations` ?releaseId |
| Capability key | text field | — | — | `listAiEvaluations` ?capabilityKey |
| Status | radio group | — | Queued · Running · Passed · Failed · Error | `listAiEvaluations` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every analytics governance model** (data table)

| Shows | Format | Notes |
|---|---|---|
| AI service | text | not in the schema: `AI Service` |
| Model | text | not in the schema: `Model` |
| Use case | text | not in the schema: `Use Case` |
| Status | text | not in the schema: `Status` |
| Consumption | text | not in the schema: `Consumption` |
| Cost | text | not in the schema: `Cost` |
| Response time | text | not in the schema: `Response Time` |
| Error rate | text | not in the schema: `Error Rate` |
| Queries | text | not in the schema: `Queries` |
| Tokens/units | text | not in the schema: `Tokens/Units` |
| User | text | not in the schema: `User` |
| Tenant | text | not in the schema: `Tenant` |
| Module | text | not in the schema: `Module` |

**The selected analytics governance model** (detail panel): The pack groups this record's detail under its own headings: “Administrators can enable/disable”, “User”, “Ask TICVAI”, “Analytics / Data Platform”, “Authorized Result”.

| Shows | Format | Notes |
|---|---|---|
| AI service | text | not in the schema: `AI Service` |
| Model | text | not in the schema: `Model` |
| Use case | text | not in the schema: `Use Case` |
| Status | text | not in the schema: `Status` |
| Consumption | text | not in the schema: `Consumption` |
| Cost | text | not in the schema: `Cost` |
| Response time | text | not in the schema: `Response Time` |
| Error rate | text | not in the schema: `Error Rate` |
| Queries | text | not in the schema: `Queries` |
| Tokens/units | text | not in the schema: `Tokens/Units` |
| User | text | not in the schema: `User` |
| Tenant | text | not in the schema: `Tenant` |
| Module | text | not in the schema: `Module` |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** ↓. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listAiCapabilities` (onLoad, The capability registry); `getEffectiveAiPolicy` (onLoad, The policy in force for a capability at a scope); `listAiModels` (onLoad, The model catalogue); `listPromptTemplates` (onLoad, The prompt registry); `listAiEvaluations` (onLoad, Evaluation runs)

**Where the user goes next**

- → `ANL-051` AI Analytics Command Center: *Back to AI Analytics Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The analytics governance model list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the analytics governance model untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No analytics governance model yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the analytics governance model are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The requested `autonomyLevel` is above the capability's `autonomyCeiling` (AIC-151). |

#### Permissions

- `listAiCapabilities` → `AI_USE` (operate) · staff
- `configureAiCapability` → `AI_CONFIGURE` (configure) · staff
- `getEffectiveAiPolicy` → `AI_USE` (operate) · staff
- `listAiModels` → `AI_USE` (operate) · staff
- `listPromptTemplates` → `AI_USE` (operate) · staff
- `publishPromptTemplate` → `AI_APPROVE` (operate) · staff
- `runAiEvaluation` → `AI_CONFIGURE` (configure) · staff
- `listAiEvaluations` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P16 · Analytics, 14 for all of P16, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P16 Venue Analytics.dc.html#anl-060` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS176 Unified BI Reporting and AI Analytics Platform Board 9.dc.html#anl-060`
- Workshop pack: Unified_BI_Reporting_and_AI_Analytics_Platform_Reference.pdf board 9
- Flow F179 *Unified BI Reporting and AI Analytics Platform board 9: AI Analytics Command …*, step 18: Works in AI Analytics Governance & Model Control → Provide administrators with centralized control over how AI may access and use TICVAI analytics. This screen is critical because Board 9 should not give an LLM unrestricted access to the TICVAI …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ANL-060?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: .
- [ ] Every transition is wired: `ANL-051`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`.
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

**6 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"askReportingQuestion": {"method":"POST","path":"/reports/ask","contract":"reporting","summary":"Natural-language reporting query","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NaturalLanguageAnswer"},
"configureAiCapability": {"method":"PUT","path":"/governance/capabilities/{capabilityKey}","contract":"ai","summary":"Register a capability, or change its owner, risk class or autonomy","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiCapabilityRegistration","responds":"AiCapabilityRegistration"},
"configureAnomalyDetector": {"method":"PUT","path":"/anomaly-detectors/{detectorKey}","contract":"ai","summary":"Set up anomaly detection on a KPI","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiAnomalyDetector","responds":"AiAnomalyDetector"},
"createDashboard": {"method":"POST","path":"/dashboards","contract":"reporting","summary":"Create a dashboard","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateDashboardRequest","responds":"Dashboard"},
"createForecastScenario": {"method":"POST","path":"/forecast-scenarios","contract":"ai","summary":"Run a what-if","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiForecastScenario","responds":null},
"createReport": {"method":"POST","path":"/reports","contract":"reporting","summary":"Create a custom report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateReportRequest","responds":"ReportDefinition"},
"decideAiInsight": {"method":"POST","path":"/insights/{insightId}/decide","contract":"ai","summary":"Review, accept, reject or mark an insight actioned","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiInsight"},
"explainMetricChange": {"method":"POST","path":"/insights/explain-metric-change","contract":"ai","summary":"Why did this metric change","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMetricChangeExplanation"},
"exportForecastVersion": {"method":"POST","path":"/forecast-versions/{versionId}/exports","contract":"ai","summary":"Export a forecast version as a file","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getEffectiveAiPolicy": {"method":"GET","path":"/governance/effective-policy","contract":"ai","summary":"The policy in force for a capability at a scope","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":true},{"name":"scopePath","in":"query","required":null},{"name":"environment","in":"query","required":null}],"requestBody":null,"responds":"AiEffectivePolicy"},
"getForecast": {"method":"GET","path":"/forecasts","contract":"ai","summary":"Forecast values","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"definitionKey","in":"query","required":true},{"name":"versionId","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"dimensionKey","in":"query","required":null},{"name":"scenarioId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"getKpiValues": {"method":"GET","path":"/kpi-values","contract":"reporting","summary":"Current values, against target, with movement","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"kpiIds","in":"query","required":null},{"name":"kpiCodes","in":"query","required":null},{"name":"scopePath","in":"query","required":null},{"name":"period","in":"query","required":null},{"name":"compareTo","in":"query","required":null},{"name":"interval","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"KpiValue"},
"listAiCapabilities": {"method":"GET","path":"/governance/capabilities","contract":"ai","summary":"The capability registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"family","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"riskClass","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiEvaluations": {"method":"GET","path":"/evaluations","contract":"ai","summary":"Evaluation runs","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"releaseId","in":"query","required":null},{"name":"capabilityKey","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiInsights": {"method":"GET","path":"/insights","contract":"ai","summary":"Insights and anomalies","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiModels": {"method":"GET","path":"/models","contract":"ai","summary":"The model catalogue","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"layer","in":"query","required":null},{"name":"producerType","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAnalyticsAnomalies": {"method":"GET","path":"/analytics-anomalies","contract":"reporting","summary":"Numbers that moved more than they should have","permission":"REPORT_VIEW_VENUE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"severity","in":"query","required":null}],"requestBody":null,"responds":"AnalyticsAnomaly"},
"listAnomalyDetectors": {"method":"GET","path":"/anomaly-detectors","contract":"ai","summary":"Anomaly detectors","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"metricKey","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listForecastDefinitions": {"method":"GET","path":"/forecast-definitions","contract":"ai","summary":"What is forecast","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"subject","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPromptTemplates": {"method":"GET","path":"/prompt-templates","contract":"ai","summary":"The prompt registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"task","in":"query","required":null},{"name":"layer","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishPromptTemplate": {"method":"POST","path":"/prompt-templates/{templateKey}/versions","contract":"ai","summary":"Publish a prompt template version","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiPromptTemplate"},
"runAiEvaluation": {"method":"POST","path":"/evaluations","contract":"ai","summary":"Evaluate a candidate","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"saveNaturalLanguageQuery": {"method":"POST","path":"/reports/ask/{conversationId}/save","contract":"reporting","summary":"Save a natural-language answer as a report definition","permission":"REPORT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ReportDefinition"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAnomalyDetector": {"type":"object","x-ticvai-persistence":"ai.anomaly_detector","description":"**An anomaly detector on one KPI** (C9, AIP-080..095). Configured thresholds on day one; a seasonal robust baseline (median/MAD) and peer comparison across venues as history builds. Detects **aggregate** deviations; actor-level patterns belong to risk, and both share one correlation key (AIP-090).","required":["detectorKey","method"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"detectorKey":{"type":"string"},"source":{"type":"string","enum":["metric","forecast","deviceHealth"],"default":"metric","description":"What is watched (29 September, build): a semantic-layer KPI, a published forecast (8.2.20, 8.2.41), or device status events (8.9.9)."},"metricKey":{"type":"string","nullable":true,"description":"A metric of the semantic layer (Reporting KPI). Required where `source` is `metric`."},"forecastSource":{"type":"object","nullable":true,"description":"Required where `source` is `forecast`; `method` is then `threshold`.","required":["definitionKey","comparator","threshold"],"properties":{"definitionKey":{"type":"string"},"dimensionKey":{"type":"string","nullable":true},"percentile":{"type":"string","enum":["p10","p50","p90"],"default":"p50"},"comparator":{"type":"string","enum":["above","atOrAbove","below","atOrBelow"]},"threshold":{"type":"number"},"thresholdKind":{"type":"string","enum":["absolute","percentOfCapacity"],"default":"absolute","description":"`percentOfCapacity` compares with the period's capacity (occupancy, 8.2.41)."},"horizonDays":{"type":"integer","minimum":1,"maximum":365,"nullable":true,"description":"Only points this many days ahead are compared. Null means the whole horizon."}}},"deviceHealthSource":{"type":"object","nullable":true,"description":"Required where `source` is `deviceHealth`.","properties":{"deviceKinds":{"type":"array","items":{"type":"string"},"description":"DeviceKind values; empty means every kind."},"failureRatePercent":{"type":"number","minimum":0,"maximum":100},"windowMinutes":{"type":"integer","minimum":5,"maximum":1440,"default":60}}},"method":{"type":"string","enum":["threshold","seasonalRobustZ","peerComparison","model"]},"thresholds":{"type":"object","additionalProperties":true,"nullable":true},"sensitivity":{"type":"string","enum":["low","medium","high"],"default":"medium"},"dimensions":{"type":"array","items":{"type":"string"}},"cadence":{"type":"string","enum":["hourly","daily"]},"isActive":{"type":"boolean","default":true},"falseAlarmRate":{"type":"number","nullable":true,"readOnly":true,"description":"Share of its insights rejected over 90 days. The number that decides whether a model is worth it."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiCapability": {"type":"string","description":"What a capability needs, not which provider serves it. This indirection is what makes \"no provider SDK in capability code\" enforceable.\n**`speechToText` and `textToSpeech` added 18 August (BL-164)** — voice added rather than declined. **Speech is the capability where UAE residency is hardest to satisfy**: the major providers run it in fewer regions than text, and a guest speaking into a kiosk is producing personal data in the moment. `AiProvider.residency` already carries the constraint and **speech is the capability most likely to fail it**, which is why it is separate rather than folded into `chat`.\n","enum":["chat","embedding","vision","rerank","speechToText","textToSpeech"]},
"AiCapabilityFamily": {"type":"string","enum":["gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"],"description":"The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."},
"AiCapabilityRegistration": {"type":"object","x-ticvai-persistence":"ai.capability","description":"**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).","required":["capabilityKey","family","riskClass","autonomyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string","description":"Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."},"family":{"$ref":"#/components/schemas/AiCapabilityFamily"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"The accountable business owner (AIC-144)."},"businessFunction":{"type":"string","nullable":true},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"autonomyCeiling":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"readOnly":true,"description":"The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."},"autonomyLevel":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"description":"The level in force at this scope. At most `autonomyCeiling`."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories the capability reads (ADM-524)."},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"degradationMode":{"type":"string","enum":["rulesOnly","searchOnly","humanHandoff","hidden","failOpen","lastPublished"],"description":"What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."},"status":{"type":"string","enum":["active","paused"],"readOnly":true,"description":"Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."},"pausedReason":{"type":"string","nullable":true,"readOnly":true},"pausedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiEffectivePolicy": {"type":"object","x-ticvai-persistence":"none — resolved from published policy versions, exceptions and ai.policy","description":"**The policy in force for a capability at a scope** (AIC-153, AIC-165; ADM-525, ADM-528): the intersection of the capability, governance policy and the tenant or venue AI policy, with where each part came from.","required":["capabilityKey","autonomyLevel","rules"],"properties":{"capabilityKey":{"type":"string"},"scopePath":{"type":"string"},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"autonomyCeiling":{"$ref":"#/components/schemas/AiAutonomyLevel"},"rules":{"type":"array","items":{"type":"object","properties":{"rule":{"$ref":"#/components/schemas/AiGovernanceRule"},"policyKey":{"type":"string"},"version":{"type":"integer"},"scopePath":{"type":"string"}}}},"exceptions":{"type":"array","items":{"$ref":"#/components/schemas/AiPolicyException"}},"conflicts":{"type":"array","items":{"type":"object","properties":{"description":{"type":"string"},"resolvedTo":{"$ref":"#/components/schemas/AiGovernanceOutcome"}}},"description":"Conflicting rules and the more restrictive result they resolved to (AIC-161)."},"resolvedAt":{"type":"string","format":"date-time"}}},
"AiEvaluationRun": {"type":"object","x-ticvai-persistence":"ai.eval_run","description":"One evaluation of a candidate against its baseline: offline golden set, backtest or shadow comparison. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["suiteId","kind","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"suiteId":{"type":"string","format":"uuid","x-ticvai-references":"ai.eval_suite"},"releaseId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.release"},"kind":{"type":"string","enum":["offline","backtest","shadow"]},"candidateRef":{"type":"string"},"baselineRef":{"type":"string","nullable":true},"status":{"type":"string","enum":["queued","running","passed","failed","error"],"readOnly":true},"metrics":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"gate":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"The promotion gate thresholds (design 3.5 table) and whether each passed."},"isolationCasesPassed":{"type":"boolean","readOnly":true,"description":"False blocks release, whatever the other metrics say."},"requestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiEvidenceItem": {"type":"object","x-ticvai-persistence":"none — held in jsonb on ai.decision_record.evidence, through AiEvidenceItemList","description":"One piece of evidence behind a decision, **labelled by origin** (AIC-197): read from a source system, derived by a rule or feature, or inferred by a model. An explanation is built from these, never from a model's chain of thought (AIC-192).","required":["label","kind"],"properties":{"label":{"type":"string","enum":["source","derived","modelInferred"]},"kind":{"type":"string","description":"What it is: `feature`, `rule`, `document`, `metric`, `transaction`, `candidateSet`."},"ref":{"type":"string","nullable":true,"description":"Where it came from: a table and id, a document chunk, a metric key."},"name":{"type":"string"},"value":{"type":"object","additionalProperties":true,"nullable":true},"observedAt":{"type":"string","format":"date-time","nullable":true}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiForecastDefinition": {"type":"object","x-ticvai-persistence":"ai.forecast_definition","description":"**What is forecast, at what grain, for what horizon, how often and by which producer** (design 3.1 Forecast, 5.2; ADM-500). One forecasting service for the platform: BI's extra subjects are definitions here, not a second forecaster (AIP-036, AIP-037).","required":["definitionKey","subject","grain","horizonDays","producer"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionKey":{"type":"string"},"name":{"type":"string"},"subject":{"type":"string","enum":["attendance","arrivalPattern","productDemand","timeslotDemand","channelPace","revenue","occupancy","attractionUtilisation","queue","entryFlow","staffing","posDemand","fnbDemand","retailDemand","stockDemand","resourceDemand","refunds","cashCollection","membershipRenewals","churn"]},"grain":{"type":"string","enum":["hour","day","week","month"]},"dimensions":{"type":"array","items":{"type":"string"},"description":"Breakdowns forecast directly or reconciled to. **Documented keys (29 September, build; 8.2.12, 8.2.14, 8.2.27):** `product`, `channel`, `timeslot`, `gate`, `outlet`, `customerSegment` and `originCountry`. `customerSegment` is the marketing-crm segment (of those in `segmentIds`, else the membership tier) the guest belonged to on the day of the booking; `originCountry` is the guest profile's country, else the order's billing country, else the channel's market, recorded as `unknown` rather than guessed. **The nightly snapshot (design 2.2 C step 1) carries both for every booking and admission**, so a definition that names them is forecast and reconciled by them. Any other key is accepted and forecast only where the snapshot carries it."},"segmentIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"The marketing-crm segments `customerSegment` breaks down by, in priority order where a guest is in several. Empty means membership tiers."},"horizonDays":{"type":"integer","minimum":1,"maximum":730},"refreshCadence":{"type":"string","enum":["hourly","daily","weekly"]},"producer":{"type":"string","enum":["rule","statistical","model","ensemble"],"description":"Which producer is live (design 3.10). A model is promoted only through `promoteAiRelease`. **`ensemble`** (18 September minutes, M18-16): a weighted blend of the rule and statistical producers, and of a promoted model where one exists; the weights are recorded on each version. Setting `ensemble` never brings in an unpromoted model."},"historyWindowMonths":{"type":"integer","minimum":1,"maximum":60,"default":36,"description":"How much of the venue's own history the statistical producer reads (18 September minutes, M18-16: \"36 months of history\"). Imported history (`importVenueHistory`) counts. Less than the window is not an error: the cold-start setting fills the gap."},"coldStart":{"type":"object","description":"**What the forecast stands on before the venue has history** (29 September, AI functions review; forecasting book p.27 \"New Venue / New Product Problem\"). Day one is never empty: the prior is the venue AI settings (typical weekday and weekend attendance, capacity, opening hours) x the starting pattern for the venue type x the UAE calendar x weather, with bookings on hand as a floor. The statistical producer blends own data in as `(k x prior + n x own) / (k + n)`, with `k` = `priorWeightObservations`. The version's `maturity` says which stage it reached.","properties":{"strategy":{"type":"string","enum":["venueSettings","startingPattern","sisterVenue","categoryBaseline","importedHistory"],"default":"venueSettings","description":"`venueSettings` uses the onboarding figures with the venue-type pattern; `sisterVenue` a venue of the same tenant; `categoryBaseline` a product category's own history; `importedHistory` means an import covers the window and the prior only fills unseen holidays."},"sisterVenueId":{"type":"string","format":"uuid","nullable":true,"description":"For `sisterVenue`. Same tenant only (no data is pooled across tenants, AIP-149)."},"priorWeightObservations":{"type":"integer","minimum":1,"maximum":52,"default":4,"description":"`k`: how many own observations the prior is worth (4 same weekdays by default)."},"startingBandPercent":{"type":"integer","minimum":5,"maximum":80,"default":40,"description":"The width of the range while the prior carries most of the weight (about +/-40%)."}}},"producerRef":{"type":"string","readOnly":true},"shadowProducerRef":{"type":"string","nullable":true,"readOnly":true,"description":"Runs alongside and is recorded, never shown (design 3.5)."},"autoPublish":{"type":"boolean","default":false,"description":"Publish without approval when the quality gates pass (autonomy L4, design 3.8). Otherwise an `AI_APPROVE` holder publishes."},"qualityGates":{"type":"object","additionalProperties":true,"nullable":true,"description":"Completeness, blocking signals and accuracy-regression thresholds a version must pass to publish."},"signalKeys":{"type":"array","items":{"type":"string"},"description":"Signal sources this definition may use (ADM-501)."},"isActive":{"type":"boolean","default":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastPoint": {"type":"object","x-ticvai-persistence":"ai.forecast_point","description":"One forecast value with its interval: 10th, 50th and 90th percentile (design 5.6: a range, never a bare percentage). Partitioned by target month. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["versionId","targetStart","p50"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"versionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"scenarioId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.forecast_scenario","description":"Set where the point belongs to a what-if scenario rather than the version itself."},"targetStart":{"type":"string","format":"date-time"},"targetEnd":{"type":"string","format":"date-time"},"dimensionKey":{"type":"string","nullable":true,"description":"Canonical key of the breakdown, e.g. `product=…;channel=web`."},"p10":{"type":"number","nullable":true},"p50":{"type":"number"},"p90":{"type":"number","nullable":true},"unit":{"type":"string"},"drivers":{"type":"object","additionalProperties":true,"nullable":true,"description":"Component decomposition or SHAP contributions, largest first (ADM-506)."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastScenario": {"type":"object","x-ticvai-persistence":"ai.forecast_scenario","description":"**A what-if against a published version** (ADM-507, ADM-517, BO-931). Changes nothing in production; its points are written with `scenarioId`.","required":["baseVersionId","changes"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"name":{"type":"string"},"baseVersionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_version"},"changes":{"type":"array","items":{"type":"object","required":["lever"],"properties":{"lever":{"type":"string","enum":["price","capacity","openingHours","weather","event","marketing","staffing","closure"]},"target":{"type":"string","nullable":true},"value":{"type":"object","additionalProperties":true,"nullable":true}}},"minItems":1},"status":{"type":"string","enum":["computing","ready","failed"],"readOnly":true},"result":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Deltas against the base version by subject and period."},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiForecastVersion": {"type":"object","x-ticvai-persistence":"ai.forecast_version","description":"**An immutable forecast version** (AIP-032): producer, model version, data cut-off, horizon and status. Nothing is overwritten; yesterday's actuals are scored against every earlier version.","required":["definitionId","versionNumber","status","basis"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"definitionId":{"type":"string","format":"uuid","x-ticvai-references":"ai.forecast_definition"},"versionNumber":{"type":"integer","minimum":1},"status":{"type":"string","enum":["running","draft","awaitingApproval","published","superseded","rejected","failed"],"readOnly":true},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"maturity":{"$ref":"#/components/schemas/AiMaturity"},"producerRef":{"type":"string"},"modelVersion":{"type":"string","nullable":true},"dataCutoffAt":{"type":"string","format":"date-time","description":"The analytical replica watermark the snapshot was taken at."},"horizonStart":{"type":"string","format":"date-time"},"horizonEnd":{"type":"string","format":"date-time"},"qualityChecks":{"type":"object","additionalProperties":true,"readOnly":true,"description":"Each gate and whether it passed."},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal","description":"Null where the definition auto-published."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiGovernanceOutcome": {"type":"string","enum":["allow","allowWithConditions","prepareOnly","approvalRequired","escalate","block"],"description":"What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."},
"AiGovernanceRule": {"type":"object","x-ticvai-persistence":"none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList","description":"One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).","required":["effect"],"properties":{"effect":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKeys":{"type":"array","items":{"type":"string"},"description":"Registered capabilities it applies to. Empty means every capability the policy names."},"actions":{"type":"array","items":{"type":"string","enum":["read","analyze","recommend","generate","prepare","create","modify","publish","execute","delete"]},"description":"ADM-523: what AI may do, from reading to executing."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."},"purposes":{"type":"array","items":{"type":"string"},"description":"Permitted purposes for those categories (AIC-156, AIR-182)."},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Above this value the effect escalates one step (for example to `approvalRequired`)."},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Roles the rule applies to; empty means every role."},"environments":{"type":"array","items":{"type":"string","enum":["development","sandbox","staging","production"]},"description":"ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."},"conditions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."}}},
"AiInsight": {"type":"object","x-ticvai-persistence":"ai.insight","description":"**An insight with a lifecycle** (AIP-181): new, reviewed, accepted or rejected, actioned, measured. Anomalies, forecast deviations, trends and opportunities land here; the narrative binds numbers to results, so a figure can only come from a query (design 8, 5.10).","required":["kind","title","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["anomaly","forecastDeviation","trend","opportunity","executiveSummary","rootCause","forecastThreshold","marketingRecommendation"]},"detectorId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.anomaly_detector"},"metricKey":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true,"enum":["campaign","journey","forecastDefinition","venue"],"description":"What the insight is about where it is not a KPI (29 September, build): a marketing-crm campaign or journey for `marketingRecommendation`, a forecast definition for `forecastThreshold`."},"subjectRef":{"type":"string","nullable":true},"recommendedAction":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `marketingRecommendation`: `{recommendation, parameters}` as `AiMarketingRecommendation`. Applied by a person in the owning module, never here."},"expectedImpact":{"type":"object","additionalProperties":true,"nullable":true,"description":"A range on a named metric (`metric`, `low`, `high`), never a single number (design 5.6)."},"title":{"type":"string"},"narrative":{"type":"string","nullable":true},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"magnitude":{"type":"number","nullable":true},"priority":{"type":"string","enum":["low","medium","high","critical"]},"correlationKey":{"type":"string","nullable":true},"status":{"type":"string","enum":["new","reviewed","accepted","rejected","actioned","measured"],"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"actionRef":{"type":"string","nullable":true},"measuredImpact":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"detectedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMaturity": {"type":"object","x-ticvai-persistence":"none — embedded as jsonb on ai.suggestion and ai.forecast_version","description":"**Where an answer stands, on every answer** (29 September, AI functions review; baseline then learn). The customer sees a stage badge and a \"Based on\" chip, never a bare percentage (design 5.6), and \"Limited historical data\" while the starting pattern carries more than half the weight.","required":["stage","basedOn"],"properties":{"stage":{"type":"string","enum":["starting","learning","established","learned"],"description":"`starting`: the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, weather). `learning`: own data carries short-range patterns (about 4 weeks). `established`: own level and trend lead, the baseline fills gaps such as a holiday not yet seen (about 3 months, or at once with 12+ months imported). `learned`: a model trained on this tenant's data, promoted by an admin (AI-D16)."},"basedOn":{"type":"string","description":"The \"Based on\" line, in words, e.g. *Based on: your venue profile, UAE calendar, weather, 23 days of your sales*. Always present."},"sources":{"type":"array","items":{"type":"object","required":["source"],"properties":{"source":{"type":"string","enum":["venueSettings","startingPattern","calendar","weather","bookingsOnHand","ownHistory","importedHistory","configuration","trainedModel"]},"detail":{"type":"string","nullable":true,"description":"e.g. *23 days*, *water park pattern v3*, *Eid al-Adha 2027*."},"observations":{"type":"integer","nullable":true}}}},"ownDataShare":{"type":"number","minimum":0,"maximum":1,"description":"The weight own data carries, `n / (k + n)`. Below 0.5 the answer is marked \"Limited historical data\"."},"limitedHistory":{"type":"boolean"},"nextStage":{"type":"object","nullable":true,"description":"What the next stage needs, e.g. *8 more Saturdays of sales*, or *an admin promotion*.","properties":{"stage":{"type":"string","enum":["learning","established","learned"]},"needs":{"type":"string"},"expectedBy":{"type":"string","format":"date","nullable":true}}}}},
"AiMetricChangeExplanation": {"type":"object","x-ticvai-persistence":"none — computed; written as an ai.insight of kind rootCause when kept","description":"**Why a metric changed** (AIP-176..180, ANL-056): drivers with their contribution, computed from the semantic layer. The narrative binds every figure to a result placeholder (design 8, 5.10).","required":["metricKey","change","drivers"],"properties":{"metricKey":{"type":"string"},"period":{"type":"string"},"comparison":{"type":"string"},"change":{"type":"number"},"changePercent":{"type":"number","nullable":true},"drivers":{"type":"array","items":{"type":"object","properties":{"dimension":{"type":"string"},"member":{"type":"string"},"contribution":{"type":"number"},"evidence":{"$ref":"#/components/schemas/AiEvidenceItem"}}}},"narrative":{"type":"string","nullable":true},"reliability":{"type":"string","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},"dataAsOf":{"type":"string","format":"date-time"}}},
"AiModel": {"type":"object","x-ticvai-persistence":"ai.model","description":"**The model catalogue** (design 3.1 Registry, 3.3; AIC-013, AIC-026). One row per model a task can be routed to: large language models, embedding and reranking models, and classical models (LightGBM, statistical forecasters) registered the same way so lifecycle, release and audit are uniform. **Platform rows** are mastered in the control plane and replicated read-only into each tenant database with the tenant root as `scopePath`; a tenant row exists only where bring-your-own-key is enabled for the tenant.","required":["layer","modelName","producerType"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"layer":{"type":"string","enum":["platform","tenant"]},"providerKind":{"allOf":[{"$ref":"#/components/schemas/AiProviderKind"}],"nullable":true},"producerType":{"type":"string","enum":["llm","embedding","reranker","classical","rule"]},"modelName":{"type":"string","description":"The deployment or model name as the provider knows it, or the package and version for a classical model."},"capabilities":{"type":"array","items":{"$ref":"#/components/schemas/AiCapability"}},"contextTokens":{"type":"integer","nullable":true},"toolCalling":{"type":"boolean","default":false},"structuredOutput":{"type":"boolean","default":false},"languages":{"type":"array","items":{"type":"string"}},"residency":{"type":"string","nullable":true,"description":"Where inference happens. Checked against `tenancy.RegionSettings.allowedAiResidencies`."},"inputCostPerMillionTokens":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"outputCostPerMillionTokens":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"isDefaultForTasks":{"type":"array","items":{"type":"string"},"description":"Tasks this model is the default for (AIC-010), e.g. `assistant.guest.answer`, `config.extract`."},"taskFitness":{"type":"array","readOnly":true,"description":"**Evaluated fitness per task** (21 September minutes, M21-09, our proposal): a score from the task's golden set (`runAiEvaluation`) and the band the task needs. Below `floor` the model is underpowered for the task; far above `ceiling` it is overpowered (it costs more than the task needs). `setAiProvider` returns a warning (`AiProvider.fitnessWarnings`) when a choice falls outside the band, and ADM-037 shows the band beside `setAiModel`; neither refuses on it.","items":{"type":"object","required":["taskKey","score"],"properties":{"taskKey":{"type":"string"},"score":{"type":"number","minimum":0,"maximum":1},"floor":{"type":"number","minimum":0,"maximum":1},"ceiling":{"type":"number","minimum":0,"maximum":1,"nullable":true},"evaluationRunId":{"type":"string","format":"uuid","nullable":true},"evaluatedAt":{"type":"string","format":"date-time"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiPolicyException": {"type":"object","x-ticvai-persistence":"ai.policy_exception","description":"**A temporary, recorded exception to a governance policy** (AIC-162, ADM-526): an expiry, an approver and compensating controls. Governance is never bypassed silently.","required":["policyId","reason","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","x-ticvai-references":"ai.governance_policy"},"capabilityKey":{"type":"string","nullable":true},"reason":{"type":"string","maxLength":2000},"compensatingControls":{"type":"array","items":{"type":"string"}},"startsAt":{"type":"string","format":"date-time","nullable":true},"expiresAt":{"type":"string","format":"date-time","description":"Required. An exception with no end is a policy change, and goes through publication."},"status":{"type":"string","enum":["active","expired","revoked"],"readOnly":true},"approvedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"revokedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"revokedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"revokeReason":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiPromptTemplate": {"type":"object","x-ticvai-persistence":"ai.prompt_template","description":"**The prompt registry** (design 3.1 Registry, AIC-022). Versioned and **immutable once published**: a change is a new version, so every decision record can name the exact template it used. Platform templates are replicated read-only like platform models; a tenant may publish its own variant of a task's template.","required":["templateKey","version","layer","task","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"templateKey":{"type":"string"},"version":{"type":"integer","minimum":1},"layer":{"type":"string","enum":["platform","tenant"]},"task":{"type":"string","description":"The gateway task it serves (design 3.3), e.g. `assistant.guest.answer`, `case.summarise`, `guidedChoice.wording`."},"body":{"type":"string","description":"The template text. Stable content first, so the provider's prefix cache applies (ADR-0034)."},"variables":{"type":"array","items":{"type":"string"}},"outputSchema":{"type":"object","additionalProperties":true,"nullable":true,"description":"JSON Schema the structured output must satisfy, where the task has one."},"status":{"type":"string","enum":["draft","published","retired"]},"contentHash":{"type":"string","readOnly":true},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"},
"AiRiskClass": {"type":"string","enum":["low","medium","high","critical"],"description":"Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."},
"AnalyticsAnomaly": {"type":"object","x-ticvai-persistence":"reporting.anomaly","description":"BI boards 9.5 and 9.6. **A departure from the series' own behaviour**, which catches what no threshold was set for.\n","properties":{"id":{"type":"string","format":"uuid"},"kpiId":{"type":"string","format":"uuid","nullable":true},"metric":{"type":"string"},"scopePath":{"type":"string"},"detectedAt":{"type":"string","format":"date-time"},"observed":{"$ref":"#/components/schemas/MetricValue"},"expected":{"$ref":"#/components/schemas/MetricValue"},"deviationSigma":{"type":"number","nullable":true},"severity":{"$ref":"#/components/schemas/AnomalySeverity"},"candidateCauses":{"type":"array","description":"**The beginning of the question, not the end of it.**","items":{"type":"object","properties":{"dimension":{"type":"string"},"value":{"type":"string"},"contribution":{"type":"number"}}}},"acknowledgedBy":{"type":"string","format":"uuid","nullable":true},"acknowledgedAt":{"type":"string","format":"date-time","nullable":true}}},
"AnomalySeverity": {"type":"string","description":"Shared by `AnalyticsAnomaly` and the `listAnalyticsAnomalies` filter.","enum":["low","medium","high"]},
"CreateDashboardRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","module","tiles"],"properties":{"name":{"type":"string","maxLength":200},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey","description":"**Which module this dashboard belongs to, and therefore who may see it.** Added 22 September for the command centre: one shell that shows each login the dashboards of the modules it is entitled to. **A dashboard with no module could not be placed in that shell at all** — the field the whole design hangs on did not exist.\n**Required, and `core` is the answer for a dashboard that belongs to no optional module.** An empty field and *belongs everywhere* look identical, and only one of them is a decision — the rule `ModuleKey` already states for screens.\n**Creating one is gated twice**, by `REPORT_MANAGE` and by the module: a principal cannot build a dashboard for a module the tenant has not licensed or that the principal holds no permission in. The server refuses with `409`; a client that hides the option has not enforced anything.\n"},"description":{"type":"string","maxLength":1000},"venueId":{"type":"string","format":"uuid","description":"Narrows every tile to one venue. Omitting it shows each viewer everything their own scope permits — it can never show a viewer beyond that. The same rule as `RunReportRequest.venueId`.\n"},"isShared":{"type":"boolean","default":false},"tiles":{"type":"array","minItems":1,"maxItems":24,"items":{"$ref":"#/components/schemas/DashboardTile"}}}},
"CreateReportRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["name","category","dataSource","columns","requiredPermission"],"properties":{"name":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":1000},"category":{"$ref":"#/components/schemas/ReportCategory"},"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"parameters":{"type":"array","items":{"$ref":"#/components/schemas/ReportParameter"}},"requiredPermission":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission","description":"Permission needed to run this report, from the shared `Permission` vocabulary. **The author cannot assign one they do not hold** — otherwise a venue user could build themselves a tenant-wide view.\n"},"maxDateRangeDays":{"type":"integer","nullable":true,"minimum":1,"default":366,"description":"Guards against a query spanning years of scan events. **When a report sets none, 366 days applies (decided 28 September, audit R158)**, so `runReport`'s date-range 400 always has a limit."}}},
"Dashboard": {"x-ticvai-persistence":"reporting.dashboard + reporting.dashboard_tile","allOf":[{"$ref":"#/components/schemas/CreateDashboardRequest"},{"type":"object","required":["id","ownerPrincipalId","aggregateCost","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"ownerPrincipalId":{"type":"string","format":"uuid"},"aggregateCost":{"type":"string","enum":["low","medium","high"],"description":"Combined refresh load of every tile."},"archivedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"},"createdAt":{"type":"string","format":"date-time"}}}]},
"DashboardTile": {"x-ticvai-persistence":"reporting.dashboard_tile","type":"object","required":["id","reportId","visualisation","position"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string"},"reportId":{"type":"string","format":"uuid"},"visualisation":{"type":"string","description":"**Extended 22 September from eight marks to twenty** against `Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`, which names eighteen components and marks every one MVP. Nine were genuinely missing — `combo`, `matrix`, `funnel`, `waterfall`, `treemap`, `scatter`, `map`, `ribbon`, `decompositionTree` — and three are layout variants of marks already here: `area` beside `line`, `donut` beside `pie`, `stackedBar100` beside `stackedBar`.\n**`number` is the source's KPI / card.** Its comparison, variance, trend sparkline and status icon are tile parameters rather than separate marks.\n**Two of the eighteen are deliberately not here** — see `x-ticvai-refuses`. The source lists them as components; the platform already models each of them elsewhere, and a second model of either is the drift this enum exists to prevent.\n","enum":["number","line","area","bar","stackedBar","stackedBar100","combo","pie","donut","table","matrix","gauge","heatmap","funnel","waterfall","treemap","scatter","map","ribbon","decompositionTree"],"x-ticvai-refuses":{"slicer":"**A control, not a mark.** The source's slicer / filter is already `ReportFilter.isParameter` plus `ReportParameter` — a run-time prompt bound to the report. A slicer on the canvas places that parameter; it does not render a result, so it is not a visualisation and a second filter model beside `ReportFilter` would be one somebody keeps in step by hand.","narrative":"**Generated prose belongs with `ai.Suggestion`.** The source's narrative / insight text (*\"Admissions are 12% above last Tuesday\"*) is model output with traceability requirements, not a way of drawing a query result.","cohort":"**Not one of the eighteen.** It appears once in the source as a *usage* — *\"the Customer & Membership dashboard shall use cards, cohort and trend charts\"* — never as a specified component. A cohort view is a `matrix` or `heatmap` over a cohort dimension."},"x-ticvai-note":"**These marks cannot yet bind data.** `ReportColumn` carries `field`, `label`, `aggregation` and `format` and **no encoding role** — no axis, series, size or colour. A `number` needs none and an eight-mark enum survived without one; a `scatter` needs x, y, size and colour, and a `combo` needs a secondary axis with stated units. **Adding `ReportColumn.role` is the harder half of this decision and is deliberately not made here** — it is the field-wells model the source's builder specifies, and it belongs with the engine and semantic-layer split that needs an ADR first.\n"},"parameters":{"type":"object","additionalProperties":true,"description":"**Open on purpose, and not yet specified.** Holds the tile's run parameters (keyed by the report's `ReportParameter.key`, as `RunReportRequest.parameters`) and its display settings — for `number`, the comparison, variance, sparkline and status icon. The per-visualisation display shape waits on the field-wells decision in `visualisation`'s `x-ticvai-note`.\n"},"refreshSeconds":{"type":"integer","minimum":30,"description":"Minimum thirty seconds. A tile refreshing every second is a load problem wearing a convenience costume.\n"},"position":{"type":"object","required":["row","column","width","height"],"properties":{"row":{"type":"integer"},"column":{"type":"integer"},"width":{"type":"integer"},"height":{"type":"integer"}}}}},
"DataSource": {"type":"string","description":"What a report may be built over. **A closed set, and that is the point** — a builder that accepts any table will happily produce a report over data nobody maintains.\n**Eight sources added 18 August** (BL-143), each because the matrix asks for a report the builder could not source. `stockCounts` and `waste`: 6.1.21 wants count variance and `stockMovements` records the movement rather than **the count that found the discrepancy**. `workstations`, `devices` and `principals`: 6.1.28 — **who did what at which till** is the question an auditor asks first and it had no source. `loyalty`: 6.1.37, points earned, burned and expiring. `reviews`: 6.1.46. `queueEntries`: **wait times are already measured and nothing could report on them.**\n**Adding a source is a decision, not an omission.** `principals`, `guests`, `loyalty` and `reviews` all name a person, and `REPORT_EXPORT_PII` gates them.\n\n**`forecastPoints` added 29 September** (8.2.55, build pass, group G2): the points of published AI forecast versions; see `x-ticvai-forecast-points`.\n\n**Three accreditation sources added 29 September** (12.1.50, build pass): `accreditationApplications`, `accreditationHolders` and `accreditationCredentials`, over `accreditation.application`, `accreditation.holder` and `accreditation.credential`. They are what the accreditation KPIs and any accreditation report or export (`exportReportResult`, csv or xlsx) are built over. **All three name a person**, and `REPORT_EXPORT_PII` gates them as it gates `guests`.\n","enum":["orders","orderLines","payments","refunds","shifts","scanEvents","entitlements","products","inventory","stockMovements","stockCounts","waste","workstations","devices","principals","loyalty","reviews","queueEntries","guests","campaigns","cases","ledgerEntries","workOrders","approvals","purchaseOrders","receipts","requisitions","stockBatches","resourceBookings","delegations","forms","challenges","wallets","resaleListings","accreditationApplications","accreditationHolders","accreditationCredentials","forecastPoints"],"x-ticvai-forecast-points":"**`forecastPoints` added 29 September (build pass, group G2; 8.2.55)**: one row per forecast point (`ai.forecast_point`) of a **published** forecast version (`ai.forecast_version` status `published`), with the definition it belongs to (`ai.forecast_definition`: subject, grain, unit), the period, the dimension key and the p10, p50 and p90 values. Draft, awaiting-approval and superseded versions are not reachable, and scenario points (`scenarioId` set) only with the scenario named as a filter: **a forecast leaves the platform as the one somebody published**. It is how a forecast is exported (`runReport` then `exportReportResult`, csv or xlsx), scheduled or put on a dashboard. Names no person, so `REPORT_EXPORT` is enough. Read from the reporting replica of the AI log database (design 2.4), never from the model service.\n"},
"GeneratedQuery": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"The structured query a natural-language question produced — data source, columns, filters, grouping. Named on 26 September so the answer and the kept copy are one shape.\n","properties":{"dataSource":{"$ref":"#/components/schemas/DataSource"},"columns":{"type":"array","items":{"$ref":"#/components/schemas/ReportColumn"}},"filters":{"type":"array","items":{"$ref":"#/components/schemas/ReportFilter"}},"groupBy":{"type":"array","items":{"type":"string"}},"compiledSql":{"type":"string","nullable":true,"description":"The SQL the semantic spec compiled to, exactly as run on the analytical replica (29 September, design 5.7). The replica's row-level security applies beneath it, so it does not need to carry the caller's scope. Null on queries kept before the semantic compile.\n"}}},
"KpiValue": {"type":"object","description":"BI board 10.3. **Value, target, variance, direction and freshness in one read.**","properties":{"kpiId":{"type":"string","format":"uuid"},"code":{"type":"string"},"bucketStart":{"type":"string","format":"date-time","nullable":true,"description":"The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."},"groupKey":{"type":"string","nullable":true,"description":"The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."},"name":{"type":"string"},"scopePath":{"type":"string"},"period":{"type":"string"},"value":{"$ref":"#/components/schemas/MetricValue"},"target":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"comparison":{"allOf":[{"$ref":"#/components/schemas/MetricValue"}],"nullable":true},"variancePercent":{"type":"number","nullable":true},"direction":{"type":"string","enum":["up","down","flat"]},"status":{"type":"string","enum":["green","amber","red","noTarget"]},"asOf":{"type":"string","format":"date-time"},"stale":{"type":"boolean","description":"**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"}}},
"MetricValue": {"x-ticvai-persistence-column":"numeric(18,4)","description":"**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n","oneOf":[{"type":"number"},{"$ref":"../shared/common.yaml#/components/schemas/Money"}]},
"NaturalLanguageAnswer": {"x-ticvai-persistence":"none — computed","type":"object","required":["conversationId","question","interpretation","result","reliability"],"properties":{"conversationId":{"type":"string"},"question":{"type":"string"},"interpretation":{"type":"string","description":"What the question was understood to mean, in plain language. When the question is outside the semantic model, the \"not available yet\" sentence."},"semanticSpec":{"allOf":[{"$ref":"#/components/schemas/ReportingSemanticQuerySpec"}],"nullable":true,"description":"What the model returned instead of SQL (design 2.2 E, 5.7): metric, dimensions, filters, period, comparison, as validated against the semantic model. Null when the question is outside it. **Also kept**, on `NaturalLanguageQuery`, so a follow-up edits it.\n"},"generatedQuery":{"allOf":[{"$ref":"#/components/schemas/GeneratedQuery"}],"nullable":true,"description":"The query the spec compiled to: data source, columns, filters, grouping, and the compiled SQL in `compiledSql`. Returned so the answer can be checked. An answer nobody can verify is worse than no answer. **Also kept, as `NaturalLanguageQuery`**, for `saveNaturalLanguageQuery`. Null when the question is outside the semantic model.\n"},"result":{"allOf":[{"$ref":"#/components/schemas/ReportResult"}],"nullable":true,"description":"Null when the question is outside the semantic model."},"dataAsOf":{"type":"string","format":"date-time","nullable":true,"description":"Replica position the answer was read at, the result's `dataAsOf`, stated beside the answer so a figure that moved is not argued about. Null when nothing was run."},"reliability":{"$ref":"#/components/schemas/ReportingAnswerReliability"},"unavailableReason":{"allOf":[{"$ref":"#/components/schemas/ReportingUnavailableReason"}],"nullable":true,"description":"Set only when `reliability` is `insufficientEvidence` because the question is outside the semantic model (\"not available yet\"); names which part is not modelled."},"confidence":{"type":"number","minimum":0,"maximum":1,"deprecated":true,"description":"Superseded by `reliability` on 29 September (design 5.6, never a bare percentage for analytics). Returned for one release, then removed."},"suggestedFollowUps":{"type":"array","items":{"type":"string"}},"modelVersion":{"type":"string"},"tokensUsed":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReportCategory": {"type":"string","enum":["sales","admission","financial","inventory","guest","operations","marketing","workforce","compliance","custom"]},
"ReportColumn": {"x-ticvai-persistence":"reporting.report_column","type":"object","required":["field"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"label":{"type":"string"},"aggregation":{"allOf":[{"$ref":"#/components/schemas/Aggregation"}],"default":"none"},"sortOrder":{"type":"integer"},"sortDirection":{"type":"string","enum":["asc","desc"]},"format":{"type":"string","nullable":true}}},
"ReportDefinition": {"x-ticvai-persistence":"reporting.report_definition + reporting.report_column + reporting.report_filter","allOf":[{"$ref":"#/components/schemas/CreateReportRequest"},{"type":"object","required":["id","version","isSystem","isRetired","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The current version. Assigned by the server on each publish; earlier ones are kept as `ReportDefinitionVersion`."},"isSystem":{"type":"boolean","description":"Shipped with the platform — seeded at provisioning (BL-053, `SeededReport`). **Clone-only (decided 28 September, audit R096)**: `updateReport` and `deleteReport` refuse it with 409 `system-report`; a venue changes a copy made with `createReport`.\n"},"isRetired":{"type":"boolean"},"estimatedCost":{"type":"string","enum":["low","medium","high"],"description":"Informs whether it may run inline or must be queued."},"createdByPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"lastRunAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}}]},
"ReportFilter": {"x-ticvai-persistence":"reporting.report_filter","type":"object","required":["field","operator"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"field":{"type":"string"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","contains","isNull","isNotNull"]},"value":{"description":"**Open on purpose; its type is the field's.** One value, of the `FieldType` that `listReportFields` gives for `field` — a string, number, boolean, or a date, date-time or uuid as a string. Absent for `in`, `notIn`, `between`, `isNull` and `isNotNull`.\n"},"values":{"type":"array","description":"The values for `in` and `notIn`, or exactly two (from, to) for `between`. Each of the field's `FieldType`, as `value`.","items":{}},"isParameter":{"type":"boolean","default":false,"description":"Prompted at run time rather than fixed. Parameters narrow the result; they never widen scope.\n"}}},
"ReportParameter": {"x-ticvai-persistence":"reporting.report_parameter","type":"object","required":["key","label","type","isRequired"],"properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"},"isRequired":{"type":"boolean"},"defaultValue":{"description":"Open on purpose. A value of this parameter's `type`, used when a run supplies none."}}},
"ReportResult": {"x-ticvai-persistence":"none — result set, cached in object storage","type":"object","required":["executionId","columns","rows"],"properties":{"executionId":{"type":"string"},"columns":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"label":{"type":"string"},"type":{"$ref":"#/components/schemas/FieldType"}}}},"rows":{"type":"array","description":"**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n","items":{"type":"object","additionalProperties":true}},"totals":{"type":"object","additionalProperties":true,"description":"Aggregated columns only, keyed and typed as a row is."},"rowCount":{"type":"integer"},"nextCursor":{"type":"string","nullable":true},"generatedAt":{"type":"string","format":"date-time"},"dataAsOf":{"type":"string","format":"date-time","description":"Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"}}},
"ReportingAnswerReliability": {"type":"string","description":"**How far an analytics answer can be relied on** (decided 29 September, AI system design 5.6): a category, never a bare percentage. `grounded`: every figure comes from a result of the compiled spec. `partial`: part of the question was answered and the rest was not modelled. `conflictingSources`: the result and a cited source disagree. `insufficientEvidence`: the question could not be answered, including \"not available yet\" outside the semantic model. The same four values as `ai.yaml`'s assistant answers.\n","enum":["grounded","partial","conflictingSources","insufficientEvidence"]},
"ReportingSemanticQuerySpec": {"x-ticvai-persistence":"none — embedded; stored whole in `reporting.natural_language_query`","type":"object","description":"**A question in the semantic model's own vocabulary** (decided 29 September, AI system design 2.2 E and 5.7). What the model returns for a live-number question instead of SQL, and what `runSemanticQuery` takes. Every code is a `SemanticModel` field code or a KPI code; Reporting validates the spec against the published model and compiles it deterministically, so the same spec compiles to the same SQL for the same model version.\n","required":["metric","period"],"properties":{"metric":{"type":"string","description":"A measure field code in the `SemanticModel`, or a `KpiDefinition.code`. The governed definition the dashboards use, so the number matches them."},"dimensions":{"type":"array","maxItems":5,"description":"Field codes to group by. Each must be reachable from the metric's dataset through a relationship the semantic model declares.","items":{"type":"string"}},"filters":{"type":"array","items":{"type":"object","required":["field","operator"],"properties":{"field":{"type":"string","description":"A `SemanticModel` field code."},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","in","notIn","isNull","isNotNull"]},"values":{"type":"array","description":"**Open on purpose; typed by the field.** One value for the comparison operators, exactly two (from, to) for `between`, any number for `in` and `notIn`, none for `isNull` and `isNotNull`.\n","items":{}}}}},"period":{"type":"string","description":"ISO 8601 interval in the venue's time zone, e.g. `2026-09-21/2026-09-27`, the form `explainMetricChange` takes."},"comparison":{"type":"string","nullable":true,"description":"As `getKpiValues` `compareTo`. With one, each row carries the metric for the comparison beside the current value.","enum":["previousPeriod","samePeriodLastYear","target","benchmark"]},"semanticModelVersion":{"type":"integer","readOnly":true,"description":"The `SemanticModel.version` the spec was validated and compiled against. Set by Reporting."}}},
"ReportingUnavailableReason": {"type":"string","description":"Which part of a question is outside the semantic model, so the answer is \"not available yet\" (design 5.7). A metric or field the caller may not see is reported as not modelled, so the reason does not reveal that it exists.","enum":["metricNotModelled","dimensionNotModelled","filterNotModelled","comparisonNotAvailable","periodOutsideHistory"]},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]}
}
```
