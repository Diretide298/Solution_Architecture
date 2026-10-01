# WS124 — AI Governance board 4

**10 screens · 20 operations · 17 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `AI_APPROVE, AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, PRODUCT_VIEW`. A control nobody can use must say so,
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
| `ADM-549` | AI Governance Monitoring Command Center | B–D | 2 | 25 | 6 | 3 | 1 | 0 | — | notStarted (—) |
| `ADM-550` | AI Risk Register & Risk Exposure Management | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-551` | AI Governance Control Library & Control Effectiveness | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-552` | AI Policy Compliance & Violation Monitoring | B–D | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-553` | AI Data, Privacy & Usage Compliance Monitoring | B–D | 0 | 34 | 6 | 0 | 0 | 4 | — | notStarted (—) |
| `ADM-554` | AI Quality, Behavior & Governance Drift Monitoring | A | 0 | 7 | 6 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-555` | AI Governance Alert & Detection Center | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-556` | AI Incident & Remediation Management | A | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-557` | AI Compliance, Assurance & Governance Reporting | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-558` | AI Governance Review, Action Plan & Continuous Improvement | B–D | 1 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-551, ADM-555, ADM-558 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-549` AI Governance Monitoring Command Center

**Provide executives, governance teams and authorized administrators with one centralized real-time view of AI governance health across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `AI_USE`, `PRODUCT_VIEW` (2 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-governance-monitoring-command-center-adm-549` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search governance monitoring | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, capability, module, environment, risk and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Severity | radio group | — | Critical · High · Medium · Low | `listGovernanceRiskMonitoring` ?severity |
| Risk | select | — | Product without owner · Missing approval · Outdated pricing · Conflicting validity · Missing channel configuration · Orphaned dependency · Unused product · Duplicate product · Unusual configuration change · High override level · Scheduled publication conflict … | `listGovernanceRiskMonitoring` ?risk |
| Owner | text field | — | — | `listGovernanceRiskMonitoring` ?owner |
| Status | text field | — | — | `listGovernanceRiskMonitoring` ?status |
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |
| Status | radio group | — | Open · Contained · Investigating · Remediating · Closed | `listAiIncidents` ?status |
| Severity | radio group | — | Low · Medium · High · Critical | `listAiIncidents` ?severity |
| Breaker state | segmented control | — | Closed · Half open · Open | `listAiCapabilityHealth` ?breakerState |
| From | date picker | — | — | `getAiUsage` ?from |
| Group by | select | — | Tenant · Venue · Principal · Provider · Capability · Day · Agent · Model · Task | `getAiUsage` ?groupBy |

#### Outputs: what the screen shows and produces

**Shown**

**Capability health** (data table, from `listAiCapabilityHealth`): **Overall AI health in production** (21 September minutes, M21-13).

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | — |
| Availability | 1,234.5 | — |
| P95 latency ms | 1,234 | — |
| Error rate | 12.5% | — |
| Breaker state | chip: Closed, Half open, Open | — |
| Degraded | yes / no (icon or chip) | Answering from its degradation mode (rules only, search only, a person). |
| Data freshness | text | e.g. index lag, the last forecast published. |

**Spend by agent** (chart, from `getAiUsage`): `getAiUsage` grouped by `agent`, with the month-end projection labelled a forecast: which agents consume the most, and for what (M21-13).

| Shows | Format | Notes |
|---|---|---|
| From | 1 Oct 2026 | — |
| To | 1 Oct 2026 | — |
| Group by | text | — |
| Rows | list or chips (count when long) | — |
| Key | text | — |
| Interactions | 1,234 | — |
| Prompt tokens | 1,234 | — |
| Completion tokens | 1,234 | — |
| Cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| P95 latency ms | 1,234 | — |
| Refusal rate | 12.5% | — |
| Rejection rate | 12.5% | Proposals a person refused. The number that says whether the assistant is worth having, and the one nobody thinks to measure. |
| Forecast | grouped details | A month-end projection, labelled a forecast (AI design 2.3, 4.5). Present where `to` is inside the current month. |
| Label | chip: Forecast | — |
| Period end | 1 Oct 2026 | — |
| Projected tokens | 1,234 | — |
| Projected cost | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Basis | text | How it was projected, e.g. the run rate of the last 7 days. |

**Active AI Capabilities** (metric tile)

**AI Decisions Today** (metric tile)

**Governance Compliance Rate** (metric tile)

**Policy Violations** (metric tile)

**High-Risk Events** (metric tile)

**Critical AI Events** (metric tile)

**Open AI Incidents** (metric tile)

**Active Exceptions** (metric tile)

**Controls Passing** (metric tile)

**Controls Failing** (metric tile)

**AI Capabilities Under Review** (metric tile)

**Governance Health Score** (metric tile)

**Data it reads**: `listGovernanceRiskMonitoring` (onLoad, Governance Risk, AI Monitoring & Control Center); `listAiGovernanceAlerts` (onLoad, Governance alerts); `listAiIncidents` (onLoad, AI incidents); `listAiCapabilityHealth` (onLoad, Health per capability); `getAiUsage` (onLoad, Consumption by agent)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-550` AI Risk Register & Risk Exposure Management: *AI Risk Register & Risk Exposure Management*
- → `ADM-551` AI Governance Control Library & Control Effectiveness: *AI Governance Control Library & Control Effectiveness*
- → `ADM-552` AI Policy Compliance & Violation Monitoring: *AI Policy Compliance & Violation Monitoring*
- → `ADM-553` AI Data, Privacy & Usage Compliance Monitoring: *AI Data, Privacy & Usage Compliance Monitoring*
- → `ADM-554` AI Quality, Behavior & Governance Drift Monitoring: *AI Quality, Behavior & Governance Drift Monitoring*; carries `releaseId`
- → `ADM-555` AI Governance Alert & Detection Center: *AI Governance Alert & Detection Center*
- → `ADM-556` AI Incident & Remediation Management: *AI Incident & Remediation Management*; carries `capabilityKey`, `incidentId`, `releaseId`
- → `ADM-557` AI Compliance, Assurance & Governance Reporting: *AI Compliance, Assurance & Governance Reporting*
- → `ADM-558` AI Governance Review, Action Plan & Continuous Improvement: *AI Governance Review, Action Plan & Continuous Improvement*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance monitoring list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance monitoring untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance monitoring yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance monitoring are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listGovernanceRiskMonitoring` → `PRODUCT_VIEW` (read) · staff
- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `listAiIncidents` → `AI_USE` (operate) · staff
- `listAiCapabilityHealth` → `AI_USE` (operate) · staff
- `getAiUsage` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.7 | AI Usage Analytics System shall provide reporting on AI usage and outcomes. | Unified Operations Dashboard | CONTRACTED | `getAiUsage` |
| 8.4.27 | System shall support AI usage monitoring. | Unified Operations Dashboard | CONTRACTED | `getAiUsage` |
| 8.7.10 | System shall provide AI analytics dashboards. | Unified Operations Dashboard | CONTRACTED | `getAiUsage` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI governance shows overall AI health in production and spend by agent, with the month-end projection labelled a forecast. *(agreed · MoM 21 Sep 2026, M21-13 · DI-973)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-549` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-549`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 1: Opens AI Governance Monitoring Command Center → Provide executives, governance teams and authorized administrators with one centralized real-time view of AI governance health across TICVAI.
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F233 branch at step 1 (expected): when Nothing has been set up on AI Governance Monitoring Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F233 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (25 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-549?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-550`, `ADM-551`, `ADM-552`, `ADM-553`, `ADM-554`, `ADM-555`, `ADM-556`, `ADM-557`, `ADM-558`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_USE`, `PRODUCT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-550` AI Risk Register & Risk Exposure Management

**Maintain the enterprise risk register specifically for TICVAI AI capabilities. Board 1 classifies individual capabilities/actions. Board 4 manages the ongoing risk exposure after those capabilities are operational.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `entryId` (navigation) |
| Route | `/platform/ai-risk-register-risk-exposure-management-adm-550` |

**Known gaps.** **The pack names 21 actions on this screen and the screen declares 0 operations.** Unserved: Customer, Commercial, Financial, Operational, Security, Model / AI Quality, Risk Matrix, Critical …. Each … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | select | — | Customer · Commercial · Financial · Operational · Security · Model quality · Privacy · Compliance | `listAiRiskRegister` ?category |
| Status | radio group | — | Open · Mitigating · Accepted · Closed | `listAiRiskRegister` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Customer (primary button) | navigation or local | — | — | — | — |
| Commercial (secondary button) | navigation or local | — | — | — | — |
| Financial (secondary button) | navigation or local | — | — | — | — |
| Operational (secondary button) | navigation or local | — | — | — | — |
| Security (secondary button) | navigation or local | — | — | — | — |
| Model / AI Quality (secondary button) | navigation or local | — | — | — | — |
| Risk Matrix (secondary button) | navigation or local | — | — | — | — |
| Critical (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAiRiskRegister` (onLoad, The AI risk register)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The risk register risk list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the risk register risk untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No risk register risk yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the risk register risk are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAiRiskRegister` → `AI_USE` (operate) · staff
- `setAiRiskRegisterEntry` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-550` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-550`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 2: Works in AI Risk Register & Risk Exposure Management → Maintain the enterprise risk register specifically for TICVAI AI capabilities. Board 1 classifies individual capabilities/actions. Board 4 manages the ongoing risk exposure after those capabilities …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-550?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Customer, Commercial, Financial, Operational, Security, Model / AI Quality, Risk Matrix, Critical.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-551` AI Governance Control Library & Control Effectiveness

**Define and continuously test whether the controls designed to govern AI are actually working. A policy existing on paper does not mean the control is effective.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `AI_USE` (1 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `controlKey` (navigation) |
| Route | `/platform/ai-governance-control-library-control-effectiveness-adm-551` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Effectiveness | radio group | — | Effective · Partially effective · Ineffective · Untested | `listAiControls` ?effectiveness |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAiControls` (onLoad, Governance controls)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance effectiveness list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance effectiveness untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance effectiveness yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance effectiveness are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAiControls` → `AI_USE` (operate) · staff
- `runAiControlTest` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-551` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-551`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 4: Works in AI Governance Control Library & Control Effectiveness → Define and continuously test whether the controls designed to govern AI are actually working. A policy existing on paper does not mean the control is effective.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-551?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-552` AI Policy Compliance & Violation Monitoring

**Continuously detect AI activity that violates or attempts to violate Board 1 governance policies.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Compliance KPIs) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `alertId` (navigation) |
| Route | `/platform/ai-policy-compliance-violation-monitoring-adm-552` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Evaluated Actions** (metric tile)

**Compliant** (metric tile)

**Blocked by Policy** (metric tile)

**Policy Violations** (metric tile)

**Attempted Violations** (metric tile)

**Exception-Based Actions** (metric tile)

**Unknown / Unclassified Actions** (metric tile)

**Every policy compliance violation** (data table)

| Shows | Format | Notes |
|---|---|---|
| Request | text | not in the schema: `Request` |
| → governance evaluation | text | not in the schema: `→ Governance Evaluation` |
| → violation detected | text | not in the schema: `→ Violation Detected` |
| → execution blocked | text | not in the schema: `→ Execution Blocked` |
| → alert created | text | not in the schema: `→ Alert Created` |
| Repeated violation detection | text | not in the schema: `Repeated Violation Detection` |
| 14 times in 24 hours | text | not in the schema: `14 times in 24 hours` |

**The selected policy compliance violation** (detail panel): The pack groups this record's detail under its own headings: “Actor”.

| Shows | Format | Notes |
|---|---|---|
| Request | text | not in the schema: `Request` |
| → governance evaluation | text | not in the schema: `→ Governance Evaluation` |
| → violation detected | text | not in the schema: `→ Violation Detected` |
| → execution blocked | text | not in the schema: `→ Execution Blocked` |
| → alert created | text | not in the schema: `→ Alert Created` |
| Repeated violation detection | text | not in the schema: `Repeated Violation Detection` |
| 14 times in 24 hours | text | not in the schema: `14 times in 24 hours` |

**Data it reads**: `listAiGovernanceAlerts` (onLoad, Governance alerts)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The policy compliance violation list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the policy compliance violation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No policy compliance violation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the policy compliance violation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The alert is already closed (`alert-not-open`). |

#### Permissions

- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `decideAiGovernanceAlert` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-552` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-552`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 6: Works in AI Policy Compliance & Violation Monitoring → Continuously detect AI activity that violates or attempts to violate Board 1 governance policies.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-552?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-553` AI Data, Privacy & Usage Compliance Monitoring

**Monitor whether AI capabilities are actually using data according to the policies configured in Board 1. This screen is monitoring—not the configuration of the data policies themselves.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Data Usage KPIs) and a per-row directory (§Show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `alertId` (navigation) |
| Route | `/platform/ai-data-privacy-usage-compliance-monitoring-adm-553` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**AI Data Requests** (metric tile)

**Allowed** (metric tile)

**Conditionally Allowed** (metric tile)

**Blocked** (metric tile)

**External Transfers** (metric tile)

**Masked / Redacted** (metric tile)

**Data Policy Violations** (metric tile)

**Unknown Data Categories** (metric tile)

**Every data privacy usage** (data table)

| Shows | Format | Notes |
|---|---|---|
| Provider | text | not in the schema: `Provider` |
| Approved provider a | text | not in the schema: `Approved Provider A` |
| Data categories sent | text | not in the schema: `Data Categories Sent` |
| Product | text | not in the schema: `Product` |
| Basket context | text | not in the schema: `Basket Context` |
| Venue | text | not in the schema: `Venue` |
| Prohibited data | text | not in the schema: `Prohibited Data` |
| Full payment details | text | not in the schema: `Full Payment Details` |
| Restricted PII | text | not in the schema: `Restricted PII` |
| Data minimization monitoring | text | not in the schema: `Data Minimization Monitoring` |
| Requested data | text | not in the schema: `Requested Data` |
| Actually sent | text | not in the schema: `Actually Sent` |
| 24 available fields | text | not in the schema: `24 available fields` |
| ↓ | text | not in the schema: `↓` |
| 8 required fields | text | not in the schema: `8 required fields` |
| 6 sent after masking | text | not in the schema: `6 sent after masking` |
| Sensitive data alert | text | not in the schema: `Sensitive Data Alert` |

**The selected data privacy usage** (detail panel): The pack groups this record's detail under its own headings: “Data Usage Matrix”, “HIGH”, “Response”.

| Shows | Format | Notes |
|---|---|---|
| Provider | text | not in the schema: `Provider` |
| Approved provider a | text | not in the schema: `Approved Provider A` |
| Data categories sent | text | not in the schema: `Data Categories Sent` |
| Product | text | not in the schema: `Product` |
| Basket context | text | not in the schema: `Basket Context` |
| Venue | text | not in the schema: `Venue` |
| Prohibited data | text | not in the schema: `Prohibited Data` |
| Full payment details | text | not in the schema: `Full Payment Details` |
| Restricted PII | text | not in the schema: `Restricted PII` |
| Data minimization monitoring | text | not in the schema: `Data Minimization Monitoring` |
| Requested data | text | not in the schema: `Requested Data` |
| Actually sent | text | not in the schema: `Actually Sent` |
| 24 available fields | text | not in the schema: `24 available fields` |
| ↓ | text | not in the schema: `↓` |
| 8 required fields | text | not in the schema: `8 required fields` |
| 6 sent after masking | text | not in the schema: `6 sent after masking` |
| Sensitive data alert | text | not in the schema: `Sensitive Data Alert` |

**Data it reads**: `listAiGovernanceAlerts` (onLoad, Governance alerts)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data privacy usage list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data privacy usage untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data privacy usage yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data privacy usage are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The alert is already closed (`alert-not-open`). |

#### Permissions

- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `decideAiGovernanceAlert` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-553` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-553`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 8: Works in AI Data, Privacy & Usage Compliance Monitoring → Monitor whether AI capabilities are actually using data according to the policies configured in Board 1. This screen is monitoring—not the configuration of the data policies themselves.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-553?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-554` AI Quality, Behavior & Governance Drift Monitoring

**Detect meaningful changes in AI behavior that may increase governance risk. This is not the full model monitoring platform. Board 4 focuses specifically on governance-relevant behavioral changes.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | Block A · ticket #20755 (APP-SETUP-ADM-554) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE` (2 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `releaseId` (navigation) |
| Route | `/platform/ai-quality-behavior-governance-drift-monitoring-adm-554` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Release | picker: choose a release | — | — | `listAiEvaluations` ?releaseId |
| Capability key | text field | — | — | `listAiEvaluations` ?capabilityKey |
| Status | radio group | — | Queued · Running · Passed · Failed · Error | `listAiEvaluations` ?status |
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |
| Capability key | text field | — | — | `listAiTrainingRuns` ?capabilityKey |
| Status | select | — | Queued · Training · Backtesting · Shadow · Gate passed · Gate failed · Failed | `listAiTrainingRuns` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Training and backtest runs** (data table, from `listAiTrainingRuns`): **Per tenant, own data only** (AIP-149). A run that passes its shadow gate raises `promotionReady`; the admin promotes it here with `promoteAiRelease`. Nothing switches by itself (AI-D16).

| Shows | Format | Notes |
|---|---|---|
| Capability key | text | — |
| Training window from | 1 Oct 2026 | — |
| Training window to | 1 Oct 2026 | — |
| Includes imported history | yes / no (icon or chip) | — |
| Status | chip: Queued, Training, Backtesting, Shadow, Gate passed, Gate failed… | — |
| Metrics | grouped details | — |
| Release | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAiEvaluations` (onLoad, Evaluation runs); `listAiGovernanceAlerts` (onLoad, Governance alerts); `listAiTrainingRuns` (onLoad, The per-tenant training and backtest runs)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The quality behavior governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the quality behavior governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No quality behavior governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the quality behavior governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not promotable: the gate has not passed (`gate-not-passed`), an isolation case failed (`isolation-cases-failed`), or the stage cannot follow the current one …; 409 Nothing to roll back to (`no-previous-release`). |

#### Permissions

- `runAiEvaluation` → `AI_CONFIGURE` (configure) · staff
- `listAiEvaluations` → `AI_USE` (operate) · staff
- `promoteAiRelease` → `AI_APPROVE` (operate) · staff
- `rollbackAiRelease` → `AI_APPROVE` (operate) · staff
- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `listAiTrainingRuns` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.2.52 | System shall continuously retrain forecasting models. | Unified Operations Dashboard | CONTRACTED | `promoteAiRelease` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-554` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-554`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 10: Works in AI Quality, Behavior & Governance Drift Monitoring → Detect meaningful changes in AI behavior that may increase governance risk. This is not the full model monitoring platform. Board 4 focuses specifically on governance-relevant behavioral changes.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-554?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , , Cancel.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-555` AI Governance Alert & Detection Center

**Centralize governance-related alerts generated from policy, control, data, behavior and operational monitoring.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `alertId` (navigation) |
| Route | `/platform/ai-governance-alert-detection-center-adm-555` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAiGovernanceAlerts` (onLoad, Governance alerts)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance alert detection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance alert detection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance alert detection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the governance alert detection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The alert is already closed (`alert-not-open`). |

#### Permissions

- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `decideAiGovernanceAlert` → `AI_CONFIGURE` (configure) · staff
- `openAiIncident` → `AI_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-555` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-555`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 12: Works in AI Governance Alert & Detection Center → Centralize governance-related alerts generated from policy, control, data, behavior and operational monitoring.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-555?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-556` AI Incident & Remediation Management

**Manage significant AI governance failures from detection through containment, investigation, remediation and closure.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | Block A · ticket #20756 (APP-SETUP-ADM-556) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE` (2 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `capabilityKey` (navigation), `incidentId` (navigation), `releaseId` (navigation) |
| Route | `/platform/ai-incident-remediation-management-adm-556` |

**Known gaps.** **The pack names 2 actions on this screen and the screen declares 0 operations.** Unserved: Revalidate thresholds Fraud Team 15 Sep Pending, Run control test Governance 15 Sep Pending. Each needs an …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Root Cause | select field | — | — | — | — | — | — |
| Impact | select field | — | — | — | — | — | — |
| Customers / Transactions Affected | text field | — | — | — | — | — | — |
| Control Failure | select field | — | — | — | — | — | — |
| Corrective Actions | select field | — | — | — | — | — | — |
| Preventive Actions | select field | — | — | — | — | — | — |
| Lessons Learned | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Open · Contained · Investigating · Remediating · Closed | `listAiIncidents` ?status |
| Severity | radio group | — | Low · Medium · High · Critical | `listAiIncidents` ?severity |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Revalidate thresholds Fraud Team 15 Sep Pending (primary button) | navigation or local | — | — | — | — |
| Run control test Governance 15 Sep Pending (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAiIncidents` (onLoad, AI incidents)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The incident remediation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the incident remediation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No incident remediation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already closed (`incident-closed`), or never contained (`incident-not-contained`).; 409 Already paused.; 409 Nothing to roll back to (`no-previous-release`).; 409 The incident is closed (`incident-closed`). |

#### Permissions

- `pauseAiCapability` → `AI_CONFIGURE` (configure) · staff
- `rollbackAiRelease` → `AI_APPROVE` (operate) · staff
- `listAiIncidents` → `AI_USE` (operate) · staff
- `openAiIncident` → `AI_CONFIGURE` (configure) · staff
- `containAiIncident` → `AI_APPROVE` (operate) · staff
- `closeAiIncident` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-556` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-556`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 14: Works in AI Incident & Remediation Management → Manage significant AI governance failures from detection through containment, investigation, remediation and closure.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-556?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Revalidate thresholds Fraud Team 15 Sep …, Run control test Governance 15 Sep ….
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_CONFIGURE`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-557` AI Compliance, Assurance & Governance Reporting

**Provide structured governance evidence and management reporting without duplicating TICVAI's generic BI platform.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW`, `AI_USE` (1 read, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-compliance-assurance-governance-reporting-adm-557` |

**Known gaps.** **The pack names 9 actions on this screen and the screen declares 0 operations.** Unserved: AI Capability Inventory, AI Risk Register, AI Policy Compliance, AI Approval Compliance, AI Data Usage, AI … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | select | — | Customer · Commercial · Financial · Operational · Security · Model quality · Privacy · Compliance | `listAiRiskRegister` ?category |
| Status | radio group | — | Open · Mitigating · Accepted · Closed | `listAiRiskRegister` ?status |
| Effectiveness | radio group | — | Effective · Partially effective · Ineffective · Untested | `listAiControls` ?effectiveness |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| AI Capability Inventory (primary button) | navigation or local | — | — | — | — |
| AI Risk Register (secondary button) | navigation or local | — | — | — | — |
| AI Policy Compliance (secondary button) | navigation or local | — | — | — | — |
| AI Approval Compliance (secondary button) | navigation or local | — | — | — | — |
| AI Data Usage (secondary button) | navigation or local | — | — | — | — |
| AI Exceptions (secondary button) | navigation or local | — | — | — | — |
| Control Effectiveness (secondary button) | navigation or local | — | — | — | — |
| Model / Provider Governance (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAiRiskRegister` (onLoad, The AI risk register); `listAiControls` (onLoad, Governance controls)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The compliance assurance governance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the compliance assurance governance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No compliance assurance governance yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the compliance assurance governance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `exportAiEvidencePackage` → `AI_AUDIT_VIEW` (read) · staff
- `listAiRiskRegister` → `AI_USE` (operate) · staff
- `listAiControls` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-557` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-557`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 16: Works in AI Compliance, Assurance & Governance Reporting → Provide structured governance evidence and management reporting without duplicating TICVAI's generic BI platform.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-557?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: AI Capability Inventory, AI Risk Register, AI Policy Compliance, AI Approval Compliance, AI Data Usage, AI Exceptions, Control Effectiveness, Model / Provider Governance.
- [ ] Every transition is wired: `ADM-549`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`, `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-558` AI Governance Review, Action Plan & Continuous Improvement

**Bring all governance monitoring together into a structured periodic review and improvement cycle. This is the final screen of the entire AI Governance module.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Another option) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-governance-review-action-plan-continuous-improvement-adm-558` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: Critical Continuous Monitoring Architecture. Each needs an operation, or needs removing from the screen …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Pause Specific Model | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Policy violation · Cross scope attempt · Masking defect · Data usage · Behaviour drift · Input drift · Bias · Override rate shift · Control failed · Spend · Provider breaker · Evaluation regression … | `listAiGovernanceAlerts` ?kind |
| Status | radio group | — | Open · Acknowledged · Dismissed · Resolved · Incident opened | `listAiGovernanceAlerts` ?status |
| Severity | radio group | — | Info · Low · Medium · High · Critical | `listAiGovernanceAlerts` ?severity |
| Category | select | — | Customer · Commercial · Financial · Operational · Security · Model quality · Privacy · Compliance | `listAiRiskRegister` ?category |
| Status | radio group | — | Open · Mitigating · Accepted · Closed | `listAiRiskRegister` ?status |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Critical Continuous Monitoring Architecture (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAiGovernanceAlerts` (onLoad, Governance alerts); `listAiRiskRegister` (onLoad, The AI risk register)

**Where the user goes next**

- → `ADM-549` AI Governance Monitoring Command Center: *Back to AI Governance Monitoring Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The governance review action configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the governance review action untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No governance review action configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAiGovernanceAlerts` → `AI_USE` (operate) · staff
- `listAiRiskRegister` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-558` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS17 AI Governance Board 4.dc.html#adm-558`
- Workshop pack: AI_Governance_Reference.pdf board 4
- Flow F233 *AI Governance board 4: AI Governance Monitoring Command Center*, step 18: Works in AI Governance Review, Action Plan & Continuous Improvement → Bring all governance monitoring together into a structured periodic review and improvement cycle. This is the final screen of the entire AI Governance module.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-558?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: Critical Continuous Monitoring ….
- [ ] Every transition is wired: `ADM-549`.
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
"closeAiIncident": {"method":"POST","path":"/incidents/{incidentId}/close","contract":"ai","summary":"Close an incident","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiIncident"},
"containAiIncident": {"method":"POST","path":"/incidents/{incidentId}/contain","contract":"ai","summary":"Contain an incident","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiIncident"},
"decideAiGovernanceAlert": {"method":"POST","path":"/governance-alerts/{alertId}/decide","contract":"ai","summary":"Acknowledge, dismiss, resolve, or open an incident","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiGovernanceAlert"},
"exportAiEvidencePackage": {"method":"POST","path":"/evidence-packages","contract":"ai","summary":"Export an evidence package","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getAiUsage": {"method":"GET","path":"/usage","contract":"ai","summary":"Usage, cost and performance","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"AiUsageReport"},
"listAiCapabilityHealth": {"method":"GET","path":"/governance/capability-health","contract":"ai","summary":"How each AI capability is running now","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"breakerState","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiControls": {"method":"GET","path":"/controls","contract":"ai","summary":"Governance controls","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"effectiveness","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiEvaluations": {"method":"GET","path":"/evaluations","contract":"ai","summary":"Evaluation runs","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"releaseId","in":"query","required":null},{"name":"capabilityKey","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiGovernanceAlerts": {"method":"GET","path":"/governance-alerts","contract":"ai","summary":"Governance alerts","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiIncidents": {"method":"GET","path":"/incidents","contract":"ai","summary":"AI incidents","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"severity","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiRiskRegister": {"method":"GET","path":"/risk-register","contract":"ai","summary":"The AI risk register","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"category","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiTrainingRuns": {"method":"GET","path":"/training-runs","contract":"ai","summary":"The per-tenant training and backtest runs","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"capabilityKey","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGovernanceRiskMonitoring": {"method":"GET","path":"/governance-risk-monitoring","contract":"catalogue","summary":"Governance Risk, AI Monitoring & Control Center","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"venueId","in":"query","required":false},{"name":"owner","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"openAiIncident": {"method":"POST","path":"/incidents","contract":"ai","summary":"Open an AI incident","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiIncident"},
"pauseAiCapability": {"method":"POST","path":"/governance/capabilities/{capabilityKey}/pause","contract":"ai","summary":"Stop a capability now","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiCapabilityRegistration"},
"promoteAiRelease": {"method":"POST","path":"/releases/{releaseId}/promote","contract":"ai","summary":"Promote a release to its next stage (a person)","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRelease"},
"rollbackAiRelease": {"method":"POST","path":"/releases/{releaseId}/rollback","contract":"ai","summary":"Roll a release back","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiRelease"},
"runAiControlTest": {"method":"POST","path":"/controls/{controlKey}/tests","contract":"ai","summary":"Test a control now","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiControlTest"},
"runAiEvaluation": {"method":"POST","path":"/evaluations","contract":"ai","summary":"Evaluate a candidate","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setAiRiskRegisterEntry": {"method":"PUT","path":"/risk-register/{entryId}","contract":"ai","summary":"Record or update a risk register entry","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AiRiskRegisterEntry","responds":"AiRiskRegisterEntry"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiCapabilityFamily": {"type":"string","enum":["gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"],"description":"The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."},
"AiCapabilityHealth": {"type":"object","x-ticvai-persistence":"none — computed from gateway telemetry, ai.activity and the breaker state in cache","description":"How one capability is running over the last hour (21 September minutes, M21-13).","required":["capabilityKey"],"properties":{"capabilityKey":{"type":"string"},"availability":{"type":"number","minimum":0,"maximum":1},"p95LatencyMs":{"type":"integer"},"latencyBudgetMs":{"type":"integer","nullable":true},"errorRate":{"type":"number","minimum":0,"maximum":1},"breakerState":{"type":"string","enum":["closed","halfOpen","open"]},"degraded":{"type":"boolean","description":"Answering from its degradation mode (rules only, search only, a person)."},"dataFreshness":{"type":"string","nullable":true,"description":"e.g. index lag, the last forecast published."},"requests":{"type":"integer"},"measuredAt":{"type":"string","format":"date-time"}}},
"AiCapabilityRegistration": {"type":"object","x-ticvai-persistence":"ai.capability","description":"**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).","required":["capabilityKey","family","riskClass","autonomyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string","description":"Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."},"family":{"$ref":"#/components/schemas/AiCapabilityFamily"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"The accountable business owner (AIC-144)."},"businessFunction":{"type":"string","nullable":true},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"autonomyCeiling":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"readOnly":true,"description":"The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."},"autonomyLevel":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"description":"The level in force at this scope. At most `autonomyCeiling`."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories the capability reads (ADM-524)."},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"degradationMode":{"type":"string","enum":["rulesOnly","searchOnly","humanHandoff","hidden","failOpen","lastPublished"],"description":"What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."},"status":{"type":"string","enum":["active","paused"],"readOnly":true,"description":"Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."},"pausedReason":{"type":"string","nullable":true,"readOnly":true},"pausedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiControl": {"type":"object","x-ticvai-persistence":"ai.control","description":"**A governance control** (AIC-219, ADM-551). Deterministic controls run nightly as SQL over system records (design 4.4): every applied tier-2 action has an approver other than the requester; no L3+ action executed without approval; no card field in any prompt.","required":["controlKey","name","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"controlKey":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"kind":{"type":"string","enum":["deterministic","manual"]},"checkRef":{"type":"string","nullable":true,"description":"The registered check a deterministic control runs. Not free SQL from a request."},"frequency":{"type":"string","enum":["nightly","weekly","monthly","onDemand"]},"capabilityKeys":{"type":"array","items":{"type":"string"}},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"effectiveness":{"type":"string","enum":["effective","partiallyEffective","ineffective","untested"],"readOnly":true},"lastTestedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiControlTest": {"type":"object","x-ticvai-persistence":"ai.control_test","description":"One run of a control and what it found. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["controlId","result"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"controlId":{"type":"string","format":"uuid","x-ticvai-references":"ai.control"},"result":{"type":"string","enum":["pass","fail","error"]},"exceptionsFound":{"type":"integer","minimum":0},"evidence":{"type":"object","additionalProperties":true,"nullable":true},"runByPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"Null where the nightly job ran it."},"runAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiEvaluationRun": {"type":"object","x-ticvai-persistence":"ai.eval_run","description":"One evaluation of a candidate against its baseline: offline golden set, backtest or shadow comparison. **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["suiteId","kind","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"suiteId":{"type":"string","format":"uuid","x-ticvai-references":"ai.eval_suite"},"releaseId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.release"},"kind":{"type":"string","enum":["offline","backtest","shadow"]},"candidateRef":{"type":"string"},"baselineRef":{"type":"string","nullable":true},"status":{"type":"string","enum":["queued","running","passed","failed","error"],"readOnly":true},"metrics":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true},"gate":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"The promotion gate thresholds (design 3.5 table) and whether each passed."},"isolationCasesPassed":{"type":"boolean","readOnly":true,"description":"False blocks release, whatever the other metrics say."},"requestedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"startedAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiGovernanceAlert": {"type":"object","x-ticvai-persistence":"ai.governance_alert","description":"**A governance alert** (design 4.4, AIC-210..223; ADM-549..555). Kept separate from operational incidents and linked where both apply (AIC-250). **`promotionReady`** (design 3.12, decided 29 September): a shadow model passed its promotion gate; the alert names the release and waits for a person to call `promoteAiRelease`. Monitoring never switches a model (AIC-252).","required":["kind","severity","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["policyViolation","crossScopeAttempt","maskingDefect","dataUsage","behaviourDrift","inputDrift","bias","overrideRateShift","controlFailed","spend","providerBreaker","evaluationRegression","forecastNotPublished","indexLag","promotionReady"]},"severity":{"type":"string","enum":["info","low","medium","high","critical"]},"capabilityKey":{"type":"string","nullable":true},"releaseId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.release","description":"For `promotionReady` and `evaluationRegression`: the release concerned."},"subjectRef":{"type":"string","nullable":true},"evidence":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["open","acknowledged","dismissed","resolved","incidentOpened"],"readOnly":true},"incidentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.incident"},"raisedAt":{"type":"string","format":"date-time","readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"note":{"type":"string","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiIncident": {"type":"object","x-ticvai-persistence":"ai.incident","description":"**An AI governance incident** (ADM-556): detection, containment, investigation, remediation and closure.","required":["reference","title","severity","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"reference":{"type":"string","readOnly":true},"title":{"type":"string"},"kind":{"type":"string","enum":["governance","operational","both"]},"severity":{"type":"string","enum":["low","medium","high","critical"]},"status":{"type":"string","enum":["open","contained","investigating","remediating","closed"],"readOnly":true},"capabilityKeys":{"type":"array","items":{"type":"string"}},"alertIds":{"type":"array","items":{"type":"string","format":"uuid"}},"operationalIncidentRef":{"type":"string","nullable":true,"description":"The linked operational incident, where both apply (AIC-250)."},"containment":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"targetRef":{"type":"string"},"at":{"type":"string","format":"date-time"},"byPrincipalId":{"type":"string","format":"uuid"}}},"readOnly":true},"rootCause":{"type":"string","nullable":true},"remediation":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"openedAt":{"type":"string","format":"date-time","readOnly":true},"containedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"closedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRelease": {"type":"object","x-ticvai-persistence":"ai.release","description":"**The release pointer per capability and tenant** (design 3.5): draft, offline evaluation, shadow, canary, production, monitored. Rollback is a pointer switch. **A model goes live only when a person promotes it** (design 3.12, decided 29 September).","required":["capabilityKey","artefactKind","candidateRef","layer","stage"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string"},"artefactKind":{"type":"string","enum":["model","prompt","routing","embedding","retrieval","rule"]},"candidateRef":{"type":"string"},"currentRef":{"type":"string","nullable":true,"description":"What production runs now: the rule, or the previously promoted artefact."},"previousRef":{"type":"string","nullable":true,"readOnly":true},"layer":{"type":"string","enum":["platform","tenant"]},"suggestionKind":{"allOf":[{"$ref":"#/components/schemas/SuggestionKind"}],"nullable":true,"description":"Where the capability answers a `requestSuggestion` kind: promotion rewrites that kind's assignment in `AiPolicy.suggestionProviders`."},"stage":{"type":"string","enum":["draft","offlineEval","shadow","canary","production","monitored","rolledBack","rejected"],"readOnly":true},"shadowStartedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"gatePassedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the shadow run passed its gate and `promotionReady` was raised."},"canaryScope":{"type":"object","additionalProperties":true,"nullable":true,"description":"Venues or share of traffic in canary."},"promotedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"promotedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"rolledBackByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"rolledBackAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiRiskClass": {"type":"string","enum":["low","medium","high","critical"],"description":"Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."},
"AiRiskRegisterEntry": {"type":"object","x-ticvai-persistence":"ai.risk_register","description":"**The AI risk register** (ADM-550): ongoing risks of AI capabilities with likelihood, impact, controls and residual rating. Board 1 classifies capabilities; this manages the risks over time.","required":["title","category","likelihood","impact"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"type":"string"},"category":{"type":"string","enum":["customer","commercial","financial","operational","security","modelQuality","privacy","compliance"]},"capabilityKeys":{"type":"array","items":{"type":"string"}},"likelihood":{"type":"integer","minimum":1,"maximum":5},"impact":{"type":"integer","minimum":1,"maximum":5},"inherentRating":{"type":"string","enum":["low","medium","high","critical"],"readOnly":true},"controlKeys":{"type":"array","items":{"type":"string"}},"residualRating":{"type":"string","enum":["low","medium","high","critical"]},"treatment":{"type":"string","enum":["accept","mitigate","transfer","avoid"]},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal"},"status":{"type":"string","enum":["open","mitigating","accepted","closed"]},"reviewDueAt":{"type":"string","format":"date-time","nullable":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiTrainingRun": {"type":"object","x-ticvai-persistence":"ai.training_run","description":"**One per-tenant training run** (29 September, AI functions review; design 3.5): trained on the tenant's own data only, backtested, then run in shadow. When its shadow period passes the gate, the release moves to `gatePassedAt` and a `promotionReady` alert goes to the admin (AI-D16).","required":["capabilityKey","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string"},"suggestionKind":{"allOf":[{"$ref":"#/components/schemas/SuggestionKind"}],"nullable":true},"forecastDefinitionKey":{"type":"string","nullable":true},"trainingWindowFrom":{"type":"string","format":"date"},"trainingWindowTo":{"type":"string","format":"date"},"dataCutoffAt":{"type":"string","format":"date-time"},"includesImportedHistory":{"type":"boolean","default":false},"featureSetVersion":{"type":"string"},"artefactRef":{"type":"string","nullable":true,"description":"The model file in the tenant's Blob container."},"backtestRunId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.eval_run"},"releaseId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.release"},"status":{"type":"string","enum":["queued","training","backtesting","shadow","gatePassed","gateFailed","failed"]},"metrics":{"type":"object","additionalProperties":true,"nullable":true},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiUsageReport": {"type":"object","x-ticvai-persistence":"none — aggregated from ai.activity","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"groupBy":{"type":"string"},"rows":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"interactions":{"type":"integer"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"p95LatencyMs":{"type":"integer"},"refusalRate":{"type":"number"},"rejectionRate":{"type":"number","description":"Proposals a person refused. **The number that says whether the assistant is worth having**, and the one nobody thinks to measure.\n"}}}},"forecast":{"type":"object","nullable":true,"description":"**A month-end projection, labelled a forecast** (AI design 2.3, 4.5). Present where `to` is inside the current month. Never added into `rows`.\n","properties":{"label":{"type":"string","enum":["forecast"]},"periodEnd":{"type":"string","format":"date"},"projectedTokens":{"type":"integer"},"projectedCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"basis":{"type":"string","description":"How it was projected, e.g. the run rate of the last 7 days."}}}}},
"GovernanceRiskAiMonitoringControlCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Governance Risk, AI Monitoring & Control Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"risk":{"type":"string","enum":["productWithoutOwner","missingApproval","outdatedPricing","conflictingValidity","missingChannelConfiguration","orphanedDependency","unusedProduct","duplicateProduct","unusualConfigurationChange","highOverrideLevel","scheduledPublicationConflict","expiredCommercialConfiguration","activeAfterEventEnd","brokenDependency"],"description":"Risk detected (AI Monitoring, pack p.26)"},"product":{"type":"string","description":"Product name"},"venue":{"type":"string","description":"Venue name"},"businessImpact":{"type":"string","description":"Business impact, in plain language"},"recommendedAction":{"type":"string","description":"Recommended action; advisory"},"owner":{"type":"string","description":"Owner (display name)","nullable":true},"dueDate":{"type":"string","description":"Due date","format":"date","nullable":true},"status":{"type":"string","description":"Status: open, acknowledged, inRemediation, resolved or dismissed (decided 29 September, readiness close-out)"},"riskId":{"type":"string","description":"Risk id","format":"uuid"},"productId":{"type":"string","description":"Product id","format":"uuid","nullable":true},"severity":{"type":"string","enum":["critical","high","medium","low"],"description":"Severity (Risk Dashboard)"},"explanation":{"type":"string","description":"AI explanation, e.g. the two products share 96% of their configuration; advisory"},"detectedAt":{"type":"string","description":"Detected","format":"date-time"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SuggestionKind": {"type":"string","description":"What is being suggested. **A closed set, and the reason it is closed is the swap.** Every entry here is a question a venue asks that a model could answer better than a rule — and each one starts as a heuristic and becomes a model when there is data.\n**Six of these were drawn as their own endpoints on the client F&B boards** — `suggestPrice`, `simulateScenario`, `simulateSlaPolicy`, `suggestRequisition`, `suggestReplenishment`, `publishDemandPlan`. **Building six endpoints means six places to change when a model changes**, and the model will change more often than the venue's question does.\n**What each kind is based on, and when the venue's own data takes over. Proposed, client to correct (decided 28 September, audit R213; re-read 29 September, AI functions review).** The figure after each rule is **the point where own data takes over from the baseline, not a refusal**: below it the kind answers from the baseline (venue AI settings, the starting pattern for the venue type, the UAE calendar, the weather) with `maturity.stage` `starting`, and between it and about three months it blends the two (`learning`). The day-one baseline per kind: `replenishment`, `requisition`, `prepPlan`, `staffing`, `demandForecast` and `scenario` from the baseline forecast (typical attendance from the venue AI settings x the venue-type month curve x the calendar x weather, bookings on hand as a floor); `menuEngineering` ranked by margin with popularity marked learning; `slaTarget` a standard default; `waitTime` people ahead / configured capacity; `upsell` the relationship map and business priority; `segmentation` known guest attributes; `anomaly` the venue's configured thresholds and actual against the forecast's low end; `sendTime` the channel's typical hour; `wasteRisk` shelf life and par against the forecast; `queueBalancing` configured capacity per queue. Only a missing setting refuses (422 `AiMissingSettingProblem`).\n- `price`: unit cost plus the category's target margin, held inside the price band. Minimum: a current cost, no history.\n- `replenishment`: par level minus on-hand plus expected use over the supplier lead time. Minimum: 14 days of stock movements.\n- `requisition`: the next service's prep-plan ingredient needs minus kitchen stock. Minimum: 14 days of sales.\n- `demandForecast`: the average of the same weekday over the last 8 weeks, adjusted by admissions already booked. Minimum: 8 weeks of sales.\n- `prepPlan`: forecast covers for the service times each item's share of the last 4 same weekdays. Minimum: 4 weeks of sales.\n- `menuEngineering`: each item placed by popularity against margin, over 90 days. Minimum: 90 days of sales.\n- `staffing`: forecast demand divided by the role's standard covers per staff hour. Minimum: 8 weeks of sales (the forecast it rests on).\n- `slaTarget`: the 80th percentile of actual times over the last 30 days. Minimum: 30 days of timed events.\n- `waitTime`: people ahead divided by the throughput of the last 30 minutes. Minimum: 30 minutes of throughput today.\n- `upsell`: the item most often bought with the basket's items over 90 days. Minimum: 90 days of orders.\n- `segmentation`: recency, frequency and spend scores over 12 months. Minimum: 90 days of orders.\n- `anomaly`: a value outside three standard deviations of the same weekday over 8 weeks. Minimum: 8 weeks of the measure.\n- `scenario`: the demand forecast re-run with the stated changes. Minimum: as `demandForecast`.\n- `sendTime` (added 29 September): per recipient, the hour inside `context.sendWindow` in which they have most often opened or clicked over the last 90 days (marketing-crm attribution touches), and where `context.channel` is `best`, the consented channel with the highest engagement. A recipient with fewer than three touches gets their segment's modal hour, and one with none the window's start. Asked with `subjectRef` a segment id or `context.subjectIds` (at most 10,000). `value` is `{recommendations: [{subjectId, sendAt, channel, basisTouches}]}`. Minimum: 90 days of message touches at the scope.\n- `wasteRisk` (added 29 September): per item at an outlet or store location, planned production and stock on hand minus forecast demand over the item's shelf life, plus batches expiring inside the horizon (`inventory.listExpiringBatches`). `value` is `{items: [{itemRef, quantityAtRisk, valueAtCost, expiresAt, recommendedAction (reducePrep, promote, transfer, useInRecipe), transferTo}]}`. Minimum: 14 days of recorded waste and of sales.\n- `queueBalancing` (added 29 September): per queue or attraction at `subjectRef` (a venue) over `horizon`, the forecast wait (the `queue` forecast definition) against throughput capacity, a recommended virtual-queue return-slot allocation by queue type, and guest redirection from over-used to under-used attractions. `value` is `{queues: [{queueId, forecastWaitMinutes, capacityPerHour, returnSlotsPerInterval, redirectTo}]}`. Minimum: 14 days of queue readings.\n- `itinerary` (added 29 September, MOB-6, guest-allowed): refines a `venue-map` visit plan the guest owns. `subjectRef` is the plan id; `value` is `{planId, baseVersion, changes, rationale}`, applied with `updateVisitPlan` as the guest. Minimum: none; the rules plan is the baseline. Every change names a point or performance of that day's venue only, rides, dining and retail alike (30 September client meeting, MoM 4.7).\n","enum":["price","replenishment","requisition","demandForecast","prepPlan","menuEngineering","staffing","slaTarget","waitTime","upsell","segmentation","anomaly","scenario","sendTime","wasteRisk","queueBalancing","itinerary"]}
}
```
