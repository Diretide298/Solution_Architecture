# WS55 — Rules  Workflow  Approval   Automation Engine board 1

**10 screens · 12 operations · 19 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_VIEW`. A control nobody can use must say so,
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
| `ADM-238` | Rules & Workflow Command Center | B–D | 0 | 22 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-239` | Visual Business Rule Builder | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-240` | Conditions, Decision Logic & Decision Tables | B–D | 0 | 0 | 6 | 0 | 0 | 1 | — | notStarted (generated) |
| `ADM-241` | Visual Workflow Designer | B–D | 8 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-242` | Approval Matrix & Multi-Level Approval Configuration | B–D | 7 | 0 | 5 | 49 | 0 | 3 | — | notStarted (generated) |
| `ADM-243` | Roles, Authority, Delegation & Approval Limits | B–D | 14 | 0 | 5 | 51 | 0 | 6 | — | notStarted (generated) |
| `ADM-244` | SLA, Escalation, Reminder & Timeout Rules | B–D | 5 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-245` | Trigger, Action & Cross-Module Orchestration Configuration | B–D | 5 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-246` | Workflow Testing, Simulation & Impact Analysis | B–D | 0 | 16 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-247` | Versioning, Governance, Approval & Publication | B–D | 0 | 20 | 6 | 0 | 0 | 3 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-239, ADM-240 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-238` Rules & Workflow Command Center

**Provide administrators with a centralized portfolio of all business rules, workflows, approvals and automations configured across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each configuration should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/rules-workflow-command-center-adm-238` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Type | text field | — | — | `listRuleWorkflow` ?type |
| Status | text field | — | — | `listRuleWorkflow` ?status |
| Source module | text field | — | — | `listRuleWorkflow` ?sourceModule |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Active Rules** (metric tile)

**Active Workflows** (metric tile)

**Approval Workflows** (metric tile)

**Draft Configurations** (metric tile)

**Pending Approval** (metric tile)

**Scheduled Changes** (metric tile)

**Rules With Errors** (metric tile)

**Workflows With Warnings** (metric tile)

**Recently Modified** (metric tile)

**Modules Covered** (metric tile)

**Every rules workflow** (data table, from `listRuleWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Rule workflow | text | Rule/Workflow ID |
| Name | text | Name |
| Type | chip: Business rule, Approval workflow, Operational workflow, Decision rule, Validation … | Kind of configuration |
| Source module | text | Source Module |
| Business process | text | Business Process |
| Version | text | Version |
| Owner | text | Owner |
| Effective date | 1 Oct 2026, 14:30 | Effective Date |
| Status | chip: Draft, Testing, Review, Pending approval, Approved, Scheduled… | Lifecycle status |
| Last modified | 1 Oct 2026, 14:30 | Last Modified |
| Usage | text | Usage |

**The selected rules workflow** (detail panel): The pack groups this record's detail under its own headings: “Classify as”.

| Shows | Format | Notes |
|---|---|---|
| Rule workflow | text | Rule/Workflow ID |
| Name | text | Name |
| Type | chip: Business rule, Approval workflow, Operational workflow, Decision rule, Validation … | Kind of configuration |
| Source module | text | Source Module |
| Business process | text | Business Process |
| Version | text | Version |
| Owner | text | Owner |
| Effective date | 1 Oct 2026, 14:30 | Effective Date |
| Status | chip: Draft, Testing, Review, Pending approval, Approved, Scheduled… | Lifecycle status |
| Last modified | 1 Oct 2026, 14:30 | Last Modified |
| Usage | text | Usage |

**Data it reads**: `listRuleWorkflow` (onLoad, Rules & Workflow Command Center)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-239` Visual Business Rule Builder: *Works in Visual Business Rule Builder*; calls `listRuleWorkflow`
- → `ADM-240` Conditions, Decision Logic & Decision Tables: *Works in Conditions, Decision Logic & Decision Tables*; calls `listRuleWorkflow`
- → `ADM-241` Visual Workflow Designer: *Works in Visual Workflow Designer*; calls `listRuleWorkflow`
- → `ADM-242` Approval Matrix & Multi-Level Approval Configuration: *Works in Approval Matrix & Multi-Level Approval Configuration*; calls `listRuleWorkflow`
- → `ADM-243` Roles, Authority, Delegation & Approval Limits: *Works in Roles, Authority, Delegation & Approval Limits*; calls `listRuleWorkflow`
- → `ADM-244` SLA, Escalation, Reminder & Timeout Rules: *Works in SLA, Escalation, Reminder & Timeout Rules*; calls `listRuleWorkflow`
- → `ADM-245` Trigger, Action & Cross-Module Orchestration Configuration: *Works in Trigger, Action & Cross-Module Orchestration Configuration*; calls `listRuleWorkflow`
- → `ADM-246` Workflow Testing, Simulation & Impact Analysis: *Works in Workflow Testing, Simulation & Impact Analysis*; calls `listRuleWorkflow`
- → `ADM-247` Versioning, Governance, Approval & Publication: *Works in Versioning, Governance, Approval & Publication*; calls `listRuleWorkflow`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rules workflow list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rules workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rules workflow yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rules workflow are still there. The pack's own statuses are Suspended → Retired — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listRuleWorkflow` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-238` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-238`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 1: Opens Rules & Workflow Command Center → Provide administrators with a centralized portfolio of all business rules, workflows, approvals and automations configured across TICVAI.
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F164 branch at step 1 (expected): when Nothing has been set up on Rules & Workflow Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F164 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-238?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-239`, `ADM-240`, `ADM-241`, `ADM-242`, `ADM-243`, `ADM-244`, `ADM-245`, `ADM-246`, `ADM-247`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-239` Visual Business Rule Builder

**Allow administrators to create business rules without software development.**

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
| Route | `/platform/visual-business-rule-builder-adm-239` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*; calls `setVisualBusinessRule`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visual business rule list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visual business rule untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visual business rule yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visual business rule are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setVisualBusinessRule` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-239` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-239`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 2: Works in Visual Business Rule Builder → Allow administrators to create business rules without software development.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-239?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes, Cancel.
- [ ] Every transition is wired: `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-240` Conditions, Decision Logic & Decision Tables

**Configure advanced decision logic where simple IF/THEN rules are insufficient.**

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
| Route | `/platform/conditions-decision-logic-decision-tables-adm-240` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listConditionDecisionLogic` (onLoad, Conditions, Decision Logic & Decision Tables)

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*; calls `listConditionDecisionLogic`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The conditions decision logic list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the conditions decision logic untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No conditions decision logic yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the conditions decision logic are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listConditionDecisionLogic` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-240` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-240`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 4: Works in Conditions, Decision Logic & Decision Tables → Configure advanced decision logic where simple IF/THEN rules are insufficient.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-240?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-241` Visual Workflow Designer

**Allow administrators to visually design complete business processes.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/visual-workflow-designer-adm-241` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workflow Name | select field | — | — | — | — | — | — |
| Module | select field | — | — | — | — | — | — |
| Business Process | select field | — | — | — | — | — | — |
| Owner | select field | — | — | — | — | — | — |
| Trigger | select field | — | — | — | — | — | — |
| Version | select field | — | — | — | — | — | — |
| Priority | select field | — | — | — | — | — | — |
| Effective Dates | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*; calls `setVisualWorkflow`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visual workflow designer configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visual workflow designer untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visual workflow designer configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setVisualWorkflow` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-241` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-241`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 6: Works in Visual Workflow Designer → Allow administrators to visually design complete business processes.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-241?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-242` Approval Matrix & Multi-Level Approval Configuration

**Configure when approvals are required and who must approve.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-matrix-multi-level-approval-configuration-adm-242` |

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Single Approval, Sequential Approval, Parallel Approval, Any-One Approval, Conditional Approval, Multi-Level …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Sequential/Parallel | select field | — | — | — | — | — | — |
| Minimum Approvals | select field | — | — | — | — | — | — |
| Rejection Behavior | select field | — | — | — | — | — | — |
| Request Changes | select field | — | — | — | — | — | — |
| Delegate | select field | — | — | — | — | — | — |
| Reassign | select field | — | — | — | — | — | — |
| Skip Conditions | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Single Approval (primary button) | navigation or local | — | — | — | — |
| Sequential Approval (secondary button) | navigation or local | — | — | — | — |
| Parallel Approval (secondary button) | navigation or local | — | — | — | — |
| Any-One Approval (secondary button) | navigation or local | — | — | — | — |
| Conditional Approval (secondary button) | navigation or local | — | — | — | — |
| Multi-Level Approval (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listApprovalMatrices` (onLoad, The approval matrices in force)

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval multi-level approval configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval multi-level approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval multi-level approval configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem) |

#### Permissions

- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff
- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

49 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.51 | System shall support reservation approvals. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 1.2.76 | System shall support configurable approval workflows. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 2.12.4 | The system should support configuration of required access level to allow refund, exchange and/or void actions. At minimum, the system should provide: - Ability to enable/disable supervisor access … | Ticketing Sales | CONTRACTED | `setApprovalMatrix` |
| 3.3.31 | Segregation of Duties - System shall enforce segregation of duties in access policies. | Admission and Access | CONTRACTED | `setApprovalMatrix` |
| 7.1.22 | The system shall support approval workflows for user creation, role assignment, permission changes, privileged access requests, and user deactivation. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.1.24 | The system shall support configurable approval requirements for refunds, ticket cancellations, price changes, promotion changes, membership changes, wallet adjustments, and manual overrides. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.5.10 | Support multi-level approval processes for complimentary tickets, VIP invitations and sponsor allocations with full audit history. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 11.1.1 | Provides configurable workflows requiring one or more approvals before sensitive actions can be executed. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.2 | Approval Workflow Configuration System shall allow administrators to configure approval workflows for different business processes. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.3 | Multi-Level Approval System shall support single-level and multi-level approval chains. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.4 | Role-Based Approval Routing System shall automatically route approval requests based on organizational hierarchy and user roles. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.5 | Escalation Rules System shall automatically escalate pending approvals after configurable time thresholds. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| … 37 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-242` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-242`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 8: Works in Approval Matrix & Multi-Level Approval Configuration → Configure when approvals are required and who must approve.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-242?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Single Approval, Sequential Approval, Parallel Approval, Any-One Approval, Conditional Approval, Multi-Level Approval.
- [ ] Every transition is wired: `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-243` Roles, Authority, Delegation & Approval Limits

**Define who has authority to perform or approve specific actions. This should work with TICVAI RBAC/PBAC rather than replace it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_VIEW` (1 configure, 1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Define by; Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/roles-authority-delegation-approval-limits-adm-243` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Event operations. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| User | select field | — | — | — | — | — | — |
| Role | select field | — | — | — | — | — | — |
| Position | select field | — | — | — | — | — | — |
| Department | select field | — | — | — | — | — | — |
| Venue | select field | — | — | — | — | — | — |
| Business Unit | select field | — | — | — | — | — | — |
| Legal Entity | select field | — | — | — | — | — | — |
| Region | select field | — | — | — | — | — | — |
| Delegator | select field | — | — | — | — | — | — |
| Delegate | select field | — | — | — | — | — | — |
| Scope | select field | — | — | — | — | — | — |
| Start | select field | — | — | — | — | — | — |
| End | select field | — | — | — | — | — | — |
| Reason | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Event operations (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listApprovalDelegations` (onLoad, Delegations in force)

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The roles authority delegation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the roles authority delegation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No roles authority delegation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem); 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says … |

#### Permissions

- `listApprovalDelegations` → `APPROVAL_VIEW` (read) · staff
- `createApprovalDelegation` → `APPROVAL_DECIDE` (operate) · staff
- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

51 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.8 | Approval Delegation - System shall allow approvers to delegate approval authority to designated users. | Approval Workflows & Governance | CONTRACTED | `createApprovalDelegation` |
| 11.1.9 | Temporary Delegation - System shall support delegation periods with automatic expiration. | Approval Workflows & Governance | CONTRACTED | `createApprovalDelegation` |
| 1.2.51 | System shall support reservation approvals. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 1.2.76 | System shall support configurable approval workflows. | Ticketing Catalogue | CONTRACTED | `setApprovalMatrix` |
| 2.12.4 | The system should support configuration of required access level to allow refund, exchange and/or void actions. At minimum, the system should provide: - Ability to enable/disable supervisor access … | Ticketing Sales | CONTRACTED | `setApprovalMatrix` |
| 3.3.31 | Segregation of Duties - System shall enforce segregation of duties in access policies. | Admission and Access | CONTRACTED | `setApprovalMatrix` |
| 7.1.22 | The system shall support approval workflows for user creation, role assignment, permission changes, privileged access requests, and user deactivation. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.1.24 | The system shall support configurable approval requirements for refunds, ticket cancellations, price changes, promotion changes, membership changes, wallet adjustments, and manual overrides. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 7.5.10 | Support multi-level approval processes for complimentary tickets, VIP invitations and sponsor allocations with full audit history. | F&B POS | CONTRACTED | `setApprovalMatrix` |
| 11.1.1 | Provides configurable workflows requiring one or more approvals before sensitive actions can be executed. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.2 | Approval Workflow Configuration System shall allow administrators to configure approval workflows for different business processes. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| 11.1.3 | Multi-Level Approval System shall support single-level and multi-level approval chains. | Approval Workflows & Governance | CONTRACTED | `setApprovalMatrix` |
| … 39 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-243` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-243`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 10: Works in Roles, Authority, Delegation & Approval Limits → Define who has authority to perform or approve specific actions. This should work with TICVAI RBAC/PBAC rather than replace it.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-243?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Event operations.
- [ ] Every transition is wired: `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-244` SLA, Escalation, Reminder & Timeout Rules

**Define how workflows behave when people or systems do not act within the expected time.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/sla-escalation-reminder-timeout-rules-adm-244` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Venue Calendar. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Response SLA | select field | — | — | — | — | — | — |
| Approval SLA | select field | — | — | — | — | — | — |
| Task SLA | select field | — | — | — | — | — | — |
| Resolution SLA | select field | — | — | — | — | — | — |
| System Action Timeout | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Venue Calendar (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listSlaEscalationReminder` (onLoad, SLA, Escalation, Reminder & Timeout Rules)

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*; calls `listSlaEscalationReminder`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sla escalation reminder configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sla escalation reminder untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sla escalation reminder configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listSlaEscalationReminder` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-244` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-244`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 12: Works in SLA, Escalation, Reminder & Timeout Rules → Define how workflows behave when people or systems do not act within the expected time.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-244?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Venue Calendar.
- [ ] Every transition is wired: `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-245` Trigger, Action & Cross-Module Orchestration Configuration

**Define what starts a workflow and what TICVAI services may be called during execution.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/trigger-action-cross-module-orchestration-configuration-adm-245` |

**Known gaps.** **The pack names 13 actions on this screen and the screen declares 1 operation.** Unserved: Create Approval, Create Task, Update Status, Apply Hold, Release Hold, Create Notification, Generate …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Retry | select field | — | — | — | — | — | — |
| Rollback where supported | select field | — | — | — | — | — | — |
| Compensation Action | select field | — | — | — | — | — | — |
| Exception Queue | select field | — | — | — | — | — | — |
| Human Intervention | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create Approval (primary button) | navigation or local | — | — | — | — |
| Create Task (secondary button) | navigation or local | — | — | — | — |
| Update Status (secondary button) | navigation or local | — | — | — | — |
| Apply Hold (secondary button) | navigation or local | — | — | — | — |
| Release Hold (secondary button) | navigation or local | — | — | — | — |
| Create Notification (secondary button) | navigation or local | — | — | — | — |
| Generate Document (secondary button) | navigation or local | — | — | — | — |
| Execute Refund (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*; calls `setTriggerActionCross`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The trigger action cross-module configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the trigger action cross-module untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No trigger action cross-module configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setTriggerActionCross` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-245` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-245`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 14: Works in Trigger, Action & Cross-Module Orchestration Configuration → Define what starts a workflow and what TICVAI services may be called during execution.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-245?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create Approval, Create Task, Update Status, Apply Hold, Release Hold, Create Notification, Generate Document, Execute Refund.
- [ ] Every transition is wired: `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-246` Workflow Testing, Simulation & Impact Analysis

**Allow administrators to test rules and workflows before they affect live operations. This is a critical screen.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-testing-simulation-impact-analysis-adm-246` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Manual Test Case, Sample Transaction, Historical Replay, Scenario Simulation, Batch Test. Each needs an …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every workflow testing simulation** (data table, from `simulateWorkflowTestingImpact`)

| Shows | Format | Notes |
|---|---|---|
| Rules evaluated | 1,234 | Rules Evaluated |
| Conditions matched | 1,234 | Conditions Matched |
| Decisions | 1,234 | Decisions |
| Approval path | text | Approval Path |
| Actions | 1,234 | Actions |
| Notifications | 1,234 | Notifications |
| Sla | text | SLA |
| Expected outcome | text | Expected Outcome |

**The selected workflow testing simulation** (detail panel): The pack groups this record's detail under its own headings: “Input”, “Historical Replay”, “Result”, “This workflow is used by”, “Regression Testing”.

| Shows | Format | Notes |
|---|---|---|
| Rules evaluated | 1,234 | Rules Evaluated |
| Conditions matched | 1,234 | Conditions Matched |
| Decisions | 1,234 | Decisions |
| Approval path | text | Approval Path |
| Actions | 1,234 | Actions |
| Notifications | 1,234 | Notifications |
| Sla | text | SLA |
| Expected outcome | text | Expected Outcome |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Manual Test Case (primary button) | navigation or local | — | — | — | — |
| Sample Transaction (secondary button) | navigation or local | — | — | — | — |
| Historical Replay (secondary button) | navigation or local | — | — | — | — |
| Scenario Simulation (secondary button) | navigation or local | — | — | — | — |
| Batch Test (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*; calls `simulateWorkflowTestingImpact`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow testing simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow testing simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow testing simulation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow testing simulation are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-246` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-246`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 16: Works in Workflow Testing, Simulation & Impact Analysis → Allow administrators to test rules and workflows before they affect live operations. This is a critical screen.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-246?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Manual Test Case, Sample Transaction, Historical Replay, Scenario Simulation, Batch Test.
- [ ] Every transition is wired: `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-247` Versioning, Governance, Approval & Publication

**Control how rules and workflows move safely from configuration into production. Board 1 configured the rules and workflows. Board 2 is the live operational layer where TICVAI executes, monitors, manages, troubleshoots, analyzes, and optimizes those workflows across the entire platform.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/versioning-governance-approval-publication-adm-247` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Publish Now, Schedule, Selected Tenant, Selected Venue, Selected Brand. Each needs an operation, or needs …

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every versioning governance approval** (data table, from `approveVersioningGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Workflow | text | Rule or workflow the version belongs to |
| Changed by | text | Changed By |
| Change date | 1 Oct 2026, 14:30 | Change Date |
| Change reason | text | Change Reason |
| Business owner | text | Business Owner |
| Technical owner | text | Technical Owner |
| Risk classification | text | Risk Classification |
| Test results | text | Test Results |
| Approval | text | Approval request id for this version |
| Changed areas | list or chips (count when long) | Areas that differ from the compared version (read-only) |
| Rollout scope | chip: All scopes, Selected tenant, Selected venue, Selected brand, Controlled rollout | Where the version is published |
| Who created | text | User who created the version |
| Who changed | text | Who changed |
| Who tested | text | Who tested |
| Who approved | text | Who approved |
| Who published | text | Who published |
| What changed | text | What changed |
| Lifecycle status | chip: Draft, Tested, Business review, Technical validation, Approval, Scheduled… | Version lifecycle status |
| Scopes | list or chips (count when long) | Tenant, venue or brand ids for a selected rollout |
| Effective from | 1 Oct 2026, 14:30 | Scheduled activation; absent means publish now |

**The selected versioning governance approval** (detail panel): The pack groups this record's detail under its own headings: “Refund Approval”, “Highlight changes to”, “Draft”, “Rollback”, “Kill Switch”, “Record”.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Publish Now (primary button) | navigation or local | — | — | — | — |
| Schedule (secondary button) | navigation or local | — | — | — | — |
| Selected Tenant (secondary button) | navigation or local | — | — | — | — |
| Selected Venue (secondary button) | navigation or local | — | — | — | — |
| Selected Brand (secondary button) | navigation or local | — | — | — | — |

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The versioning governance approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the versioning governance approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No versioning governance approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the versioning governance approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `approveVersioningGovernance` → `APPROVAL_CONFIGURE` (configure) · staff · step-up mfa

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-247` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-247`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 18: Works in Versioning, Governance, Approval & Publication → Control how rules and workflows move safely from configuration into production. Board 1 configured the rules and workflows. Board 2 is the live operational layer where TICVAI executes, monitors …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-247?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish Now, Schedule, Selected Tenant, Selected Venue, Selected Brand.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
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
"approveVersioningGovernance": {"method":"PUT","path":"/versioning-governance","contract":"approvals","summary":"Versioning, Governance, Approval & Publication","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VersioningGovernanceApprovalPublicationInput","responds":"VersioningGovernanceApprovalPublicationView"},
"createApprovalDelegation": {"method":"POST","path":"/delegations","contract":"approvals","summary":"Delegate approval authority","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalDelegation","responds":"ApprovalDelegation"},
"listApprovalDelegations": {"method":"GET","path":"/delegations","contract":"approvals","summary":"Who is standing in for whom","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ApprovalDelegation"},
"listApprovalMatrices": {"method":"GET","path":"/approval-matrices","contract":"approvals","summary":"What requires approval here","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"effective","in":"query","required":null}],"requestBody":null,"responds":"ApprovalMatrix"},
"listConditionDecisionLogic": {"method":"GET","path":"/condition-decision-logic","contract":"approvals","summary":"Conditions, Decision Logic & Decision Tables","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ConditionsDecisionLogicDecisionTablesView"},
"listRuleWorkflow": {"method":"GET","path":"/rule-workflow","contract":"approvals","summary":"Rules & Workflow Command Center","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"type","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"sourceModule","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSlaEscalationReminder": {"method":"GET","path":"/sla-escalation-reminder","contract":"approvals","summary":"SLA, Escalation, Reminder & Timeout Rules","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SlaEscalationReminderTimeoutRulesView"},
"setApprovalMatrix": {"method":"PUT","path":"/approval-matrices","contract":"approvals","summary":"Configure what requires approval","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalMatrix","responds":"ApprovalMatrix"},
"setTriggerActionCross": {"method":"PUT","path":"/trigger-action-cross","contract":"approvals","summary":"Trigger, Action & Cross-Module Orchestration Configuration","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TriggerActionCrossModuleOrchestrationConfigurationInput","responds":"TriggerActionCrossModuleOrchestrationConfigurationView"},
"setVisualBusinessRule": {"method":"PUT","path":"/visual-business-rule","contract":"approvals","summary":"Visual Business Rule Builder","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualBusinessRuleBuilderInput","responds":"VisualBusinessRuleBuilderView"},
"setVisualWorkflow": {"method":"PUT","path":"/visual-workflow","contract":"approvals","summary":"Visual Workflow Designer","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualWorkflowDesignerInput","responds":"VisualWorkflowDesignerView"},
"simulateWorkflowTestingImpact": {"method":"PUT","path":"/workflow-testing-impact","contract":"approvals","summary":"Workflow Testing, Simulation & Impact Analysis","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkflowTestingSimulationImpactAnalysisInput","responds":"WorkflowTestingSimulationImpactAnalysisView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalDelegation": {"type":"object","x-ticvai-persistence":"approvals.delegation","required":["delegatorPrincipalId","delegatePrincipalId","from","to"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"delegatorPrincipalId":{"type":"string","format":"uuid","description":"A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and `identity.getPrincipal`.\n"},"delegatePrincipalId":{"type":"string","format":"uuid","description":"A principal id, resolved to a name the same way as `delegatorPrincipalId`."},"kinds":{"type":"array","description":"Absent means everything the delegator may approve.","items":{"$ref":"#/components/schemas/ApprovalKind"}},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"A delegate may be given less authority than the delegator, never more."},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time","description":"**Required.** An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it.\n"},"reason":{"type":"string"},"isActive":{"type":"boolean","readOnly":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"}}},
"ConditionsDecisionLogicDecisionTablesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.decision_table and decision_table_row (schema DecisionTable) (data model for the agreed operations, 29 September)","description":"**What Conditions, Decision Logic & Decision Tables displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Name"},"decisionTableId":{"type":"string","description":"Decision table or condition set identifier"},"resolutionStrategy":{"type":"string","enum":["priority","sequence","specificity"],"description":"How to choose when multiple rules apply"},"onMatch":{"type":"string","enum":["stopProcessing","continueEvaluation"],"description":"Whether evaluation stops at the first match"},"conflicts":{"type":"array","items":{"type":"string","enum":["contradictoryRules","overlappingConditions","unreachableOutcomes","circularLogic","missingOutcomes"]},"description":"Conflicts detected in this decision logic (read-only)"}},"required":["decisionTableId","name"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RulesWorkflowCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_definition, workflow_version, business_rule, decision_table, automation, matrix and rule; one row per configuration (data model for the agreed operations, 29 September)","description":"**What Rules & Workflow Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleWorkflowId":{"type":"string","description":"Rule/Workflow ID"},"name":{"type":"string","description":"Name"},"type":{"type":"string","enum":["businessRule","approvalWorkflow","operationalWorkflow","decisionRule","validationRule","escalationRule","automation","crossModuleWorkflow"],"description":"Kind of configuration"},"sourceModule":{"type":"string","description":"Source Module"},"businessProcess":{"type":"string","description":"Business Process"},"version":{"type":"string","description":"Version"},"owner":{"type":"string","description":"Owner"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective Date"},"status":{"type":"string","enum":["draft","testing","review","pendingApproval","approved","scheduled","active","suspended","retired"],"description":"Lifecycle status"},"lastModified":{"type":"string","format":"date-time","description":"Last Modified"},"usage":{"type":"string","description":"Usage"}},"required":["ruleWorkflowId"]},
"RulesWorkflowCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeRules":{"type":"integer","description":"Active Rules"},"activeWorkflows":{"type":"integer","description":"Active Workflows"},"approvalWorkflows":{"type":"integer","description":"Approval Workflows"},"draftConfigurations":{"type":"integer","description":"Draft Configurations"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"scheduledChanges":{"type":"integer","description":"Scheduled Changes"},"rulesWithErrors":{"type":"integer","description":"Rules With Errors"},"workflowsWithWarnings":{"type":"integer","description":"Workflows With Warnings"},"recentlyModified":{"type":"integer","description":"Configurations modified in the recent period"},"modulesCovered":{"type":"integer","description":"Number of modules using configured rules and workflows"}}},
"SlaEscalationReminderTimeoutRulesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.sla_policy (schema ApprovalSlaPolicy), including its reminder-percentage columns (data model for the agreed operations, 29 September)","description":"**What SLA, Escalation, Reminder & Timeout Rules displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"code":{"type":"string","description":"Policy code, the same key setApprovalSlaPolicy upserts by"},"slaType":{"type":"string","enum":["responseSla","approvalSla","taskSla","resolutionSla","systemActionTimeout"],"description":"Which clock this policy governs"},"calendarBasis":{"type":"string","enum":["calendarHours","businessHours","workingDays","venueCalendar","holidayCalendar"],"description":"How elapsed time is counted"},"escalationActions":{"type":"array","items":{"type":"string","enum":["notify","reassign","escalate","addApprover","createTask","raisePriority","triggerBackupWorkflow"]},"description":"What happens on escalation"},"channelsType":{"type":"string","enum":["email","push","inApp","smsWhereAppropriate"],"description":"Vocabulary listed under Reminder Channels."},"targetMinutes":{"type":"integer","description":"SLA target in minutes"},"onBreach":{"type":"string","enum":["notifyOnly","escalate","autoApprove","autoReject"],"description":"Outcome at breach; auto outcomes only where explicitly permitted"},"autoActionAllowed":{"type":"boolean","description":"Auto-approve or auto-reject on breach is explicitly permitted; default false"},"firstReminderAtPercent":{"type":"integer","description":"Percent of target at which the first reminder goes"},"secondReminderAtPercent":{"type":"integer","description":"Percent of target at which the second reminder goes"},"escalateAtPercent":{"type":"integer","description":"Percent of target at which the request escalates"}},"required":["code"]},
"TriggerActionCrossModuleOrchestrationConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.workflow_trigger (schema WorkflowTrigger) (data model for the agreed operations, 29 September)","description":"**What Trigger, Action & Cross-Module Orchestration Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"triggerType":{"type":"string","enum":["event","dataCondition","schedule","manual"],"description":"What starts the workflow"},"workflowId":{"type":"string","description":"Workflow this trigger and action set belongs to"},"allowedActions":{"type":"array","items":{"type":"string","enum":["createApproval","createTask","updateStatus","applyHold","releaseHold","createNotification","generateDocument","executeRefund","updateAllocation","activateMembership","suspendPartner","callApprovedApi","callApprovedService","startSubWorkflow"]},"description":"Actions this workflow may call"},"onFailure":{"type":"string","enum":["retry","rollback","compensate","exceptionQueue","humanIntervention"],"description":"What happens when an action fails"},"triggerDefinition":{"type":"string","description":"Event name, data condition (e.g. Balance > Limit) or schedule"},"maxRetries":{"type":"integer","description":"Retries before the failure handling applies"}},"required":["workflowId","triggerType"]},
"TriggerActionCrossModuleOrchestrationConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_trigger (schema WorkflowTrigger) (data model for the agreed operations, 29 September)","description":"**What Trigger, Action & Cross-Module Orchestration Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"triggerType":{"type":"string","enum":["event","dataCondition","schedule","manual"],"description":"What starts the workflow"},"workflowId":{"type":"string","description":"Workflow this trigger and action set belongs to"},"allowedActions":{"type":"array","items":{"type":"string","enum":["createApproval","createTask","updateStatus","applyHold","releaseHold","createNotification","generateDocument","executeRefund","updateAllocation","activateMembership","suspendPartner","callApprovedApi","callApprovedService","startSubWorkflow"]},"description":"Actions this workflow may call"},"onFailure":{"type":"string","enum":["retry","rollback","compensate","exceptionQueue","humanIntervention"],"description":"What happens when an action fails"},"triggerDefinition":{"type":"string","description":"Event name, data condition (e.g. Balance > Limit) or schedule"},"maxRetries":{"type":"integer","description":"Retries before the failure handling applies"}},"required":["workflowId","triggerType"]},
"VersioningGovernanceApprovalPublicationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.workflow_version and raises an approvals.request for publication (data model for the agreed operations, 29 September)","description":"**What Versioning, Governance, Approval & Publication submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"workflowId":{"type":"string","description":"Rule or workflow the version belongs to"},"version":{"type":"string","description":"Version"},"changedBy":{"type":"string","description":"Changed By"},"changeDate":{"type":"string","format":"date-time","description":"Change Date"},"changeReason":{"type":"string","description":"Change Reason"},"businessOwner":{"type":"string","description":"Business Owner"},"technicalOwner":{"type":"string","description":"Technical Owner"},"riskClassification":{"type":"string","description":"Risk Classification"},"testResults":{"type":"string","description":"Test Results"},"approval":{"type":"string","description":"Approval request id for this version"},"changedAreas":{"type":"array","items":{"type":"string","enum":["conditions","thresholds","approvers","actions","sla","escalation","integrations"]},"description":"Areas that differ from the compared version (read-only)"},"rolloutScope":{"type":"string","enum":["allScopes","selectedTenant","selectedVenue","selectedBrand","controlledRollout"],"description":"Where the version is published"},"whoCreated":{"type":"string","description":"User who created the version"},"whoChanged":{"type":"string","description":"Who changed"},"whoTested":{"type":"string","description":"Who tested"},"whoApproved":{"type":"string","description":"Who approved"},"whoPublished":{"type":"string","description":"Who published"},"whatChanged":{"type":"string","description":"What changed"},"lifecycleStatus":{"type":"string","enum":["draft","tested","businessReview","technicalValidation","approval","scheduled","active","suspended","retired"],"description":"Version lifecycle status"},"scopeIds":{"type":"array","items":{"type":"string"},"description":"Tenant, venue or brand ids for a selected rollout"},"effectiveFrom":{"type":"string","format":"date-time","description":"Scheduled activation; absent means publish now"}},"required":["workflowId","version"]},
"VersioningGovernanceApprovalPublicationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_version (schema WorkflowVersion) (data model for the agreed operations, 29 September)","description":"**What Versioning, Governance, Approval & Publication displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowId":{"type":"string","description":"Rule or workflow the version belongs to"},"version":{"type":"string","description":"Version"},"changedBy":{"type":"string","description":"Changed By"},"changeDate":{"type":"string","format":"date-time","description":"Change Date"},"changeReason":{"type":"string","description":"Change Reason"},"businessOwner":{"type":"string","description":"Business Owner"},"technicalOwner":{"type":"string","description":"Technical Owner"},"riskClassification":{"type":"string","description":"Risk Classification"},"testResults":{"type":"string","description":"Test Results"},"approval":{"type":"string","description":"Approval request id for this version"},"changedAreas":{"type":"array","items":{"type":"string","enum":["conditions","thresholds","approvers","actions","sla","escalation","integrations"]},"description":"Areas that differ from the compared version (read-only)"},"rolloutScope":{"type":"string","enum":["allScopes","selectedTenant","selectedVenue","selectedBrand","controlledRollout"],"description":"Where the version is published"},"whoCreated":{"type":"string","description":"User who created the version"},"whoChanged":{"type":"string","description":"Who changed"},"whoTested":{"type":"string","description":"Who tested"},"whoApproved":{"type":"string","description":"Who approved"},"whoPublished":{"type":"string","description":"Who published"},"whatChanged":{"type":"string","description":"What changed"},"lifecycleStatus":{"type":"string","enum":["draft","tested","businessReview","technicalValidation","approval","scheduled","active","suspended","retired"],"description":"Version lifecycle status"},"scopeIds":{"type":"array","items":{"type":"string"},"description":"Tenant, venue or brand ids for a selected rollout"},"effectiveFrom":{"type":"string","format":"date-time","description":"Scheduled activation; absent means publish now"}},"required":["workflowId","version"]},
"VisualBusinessRuleBuilderInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.business_rule (schema BusinessRule) (data model for the agreed operations, 29 September)","description":"**What Visual Business Rule Builder submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"outcome":{"type":"string","enum":["allow","reject","requireApproval","requireAdditionalInformation","applyHold","createTask","generateAlert","startWorkflow","executeApprovedAction"],"description":"THEN outcome when the conditions match"},"businessObjectField":{"type":"string","description":"Governed field from a registered module, e.g. Refund.Amount"},"name":{"type":"string","description":"Rule name"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","contains","inList","exists","doesNotExist","beforeAfter","percentageThreshold","boolean"],"description":"Comparison operator of the condition"},"ruleId":{"type":"string","description":"Rule identifier; absent on input to create a new rule"},"value":{"type":"string","description":"Comparison value"},"explanation":{"type":"string","description":"Plain-language rule explanation"}},"required":["name","businessObjectField","operator","outcome"]},
"VisualBusinessRuleBuilderView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.business_rule, the row setVisualBusinessRule writes (data model for the agreed operations, 29 September)","description":"**What Visual Business Rule Builder displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"outcome":{"type":"string","enum":["allow","reject","requireApproval","requireAdditionalInformation","applyHold","createTask","generateAlert","startWorkflow","executeApprovedAction"],"description":"THEN outcome when the conditions match"},"businessObjectField":{"type":"string","description":"Governed field from a registered module, e.g. Refund.Amount"},"name":{"type":"string","description":"Rule name"},"operator":{"type":"string","enum":["equals","notEquals","greaterThan","lessThan","between","contains","inList","exists","doesNotExist","beforeAfter","percentageThreshold","boolean"],"description":"Comparison operator of the condition"},"ruleId":{"type":"string","description":"Rule identifier; absent on input to create a new rule"},"value":{"type":"string","description":"Comparison value"},"explanation":{"type":"string","description":"Plain-language rule explanation"}},"required":["name","businessObjectField","operator","outcome"]},
"VisualWorkflowDesignerInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.workflow_definition and a draft approvals.workflow_version (data model for the agreed operations, 29 September)","description":"**What Visual Workflow Designer submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"definition":{"type":"string","description":"The workflow graph (nodes and connections) as a JSON document"},"nodeTypes":{"type":"array","items":{"type":"string","enum":["start","trigger","task","decision","approval","systemAction","notification","wait","timer","parallelBranch","merge","escalation","subWorkflow","end"]},"description":"Node kinds used in this workflow"},"workflowName":{"type":"string","description":"Workflow Name"},"module":{"type":"string","description":"Module"},"businessProcess":{"type":"string","description":"Business Process"},"owner":{"type":"string","description":"Owner"},"version":{"type":"string","description":"Version"},"priority":{"type":"string","description":"Priority"},"effectiveFrom":{"type":"string","description":"Effective Dates"},"validationIssues":{"type":"array","items":{"type":"string","enum":["deadEnds","missingOutcomes","circularLoops","missingAssignee","invalidActions"]},"description":"Design problems the designer found (read-only)"},"workflowId":{"type":"string","description":"Workflow identifier; absent on input to create a new workflow"},"trigger":{"type":"string","description":"What starts the workflow"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"}},"required":["workflowName","module","definition"]},
"VisualWorkflowDesignerView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_definition and its draft approvals.workflow_version (data model for the agreed operations, 29 September)","description":"**What Visual Workflow Designer displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"definition":{"type":"string","description":"The workflow graph (nodes and connections) as a JSON document"},"nodeTypes":{"type":"array","items":{"type":"string","enum":["start","trigger","task","decision","approval","systemAction","notification","wait","timer","parallelBranch","merge","escalation","subWorkflow","end"]},"description":"Node kinds used in this workflow"},"workflowName":{"type":"string","description":"Workflow Name"},"module":{"type":"string","description":"Module"},"businessProcess":{"type":"string","description":"Business Process"},"owner":{"type":"string","description":"Owner"},"version":{"type":"string","description":"Version"},"priority":{"type":"string","description":"Priority"},"effectiveFrom":{"type":"string","description":"Effective Dates"},"validationIssues":{"type":"array","items":{"type":"string","enum":["deadEnds","missingOutcomes","circularLoops","missingAssignee","invalidActions"]},"description":"Design problems the designer found (read-only)"},"workflowId":{"type":"string","description":"Workflow identifier; absent on input to create a new workflow"},"trigger":{"type":"string","description":"What starts the workflow"},"effectiveTo":{"type":"string","format":"date-time","description":"Effective to"}},"required":["workflowName","module","definition"]},
"WorkflowTestingSimulationImpactAnalysisInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; the outcome is recorded as approvals.workflow_version test results (data model for the agreed operations, 29 September)","description":"**What Workflow Testing, Simulation & Impact Analysis submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"workflowId":{"type":"string","description":"Workflow under test"},"testMode":{"type":"string","enum":["manualTestCase","sampleTransaction","historicalReplay","scenarioSimulation","batchTest"],"description":"How the workflow is tested"},"version":{"type":"string","description":"Version under test"},"compareWithVersion":{"type":"string","description":"Existing version to compare against for regression"},"inputPayload":{"type":"string","description":"Sample transaction as a JSON document, for manual and sample tests"},"replayFrom":{"type":"string","format":"date","description":"Historical replay start"},"replayTo":{"type":"string","format":"date","description":"Historical replay end"}},"required":["workflowId","testMode"]},
"WorkflowTestingSimulationImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — computed by simulation over approvals.workflow_version and the rules it calls; never executes actions (data model for the agreed operations, 29 September)","description":"**What Workflow Testing, Simulation & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowId":{"type":"string","description":"Workflow under test"},"testMode":{"type":"string","enum":["manualTestCase","sampleTransaction","historicalReplay","scenarioSimulation","batchTest"],"description":"How the workflow is tested"},"rulesEvaluated":{"type":"integer","description":"Rules Evaluated"},"conditionsMatched":{"type":"integer","description":"Conditions Matched"},"decisions":{"type":"integer","description":"Decisions"},"approvalPath":{"type":"string","description":"Approval Path"},"actions":{"type":"integer","description":"Actions"},"notifications":{"type":"integer","description":"Notifications"},"sla":{"type":"string","description":"SLA"},"expectedOutcome":{"type":"string","description":"Expected Outcome"},"version":{"type":"string","description":"Version under test"},"compareWithVersion":{"type":"string","description":"Existing version to compare against for regression"},"inputPayload":{"type":"string","description":"Sample transaction as a JSON document, for manual and sample tests"},"replayFrom":{"type":"string","format":"date","description":"Historical replay start"},"replayTo":{"type":"string","format":"date","description":"Historical replay end"}},"required":["workflowId","testMode"]}
}
```
