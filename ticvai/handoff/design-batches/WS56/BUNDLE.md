# WS56 — Rules  Workflow  Approval   Automation Engine board 2

**10 screens · 13 operations · 25 schemas · 5 permissions**

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
  `APPROVAL_ACT, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `ADM-248` | Workflow Operations Command Center | B–D | 0 | 262 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-249` | Unified Approval Inbox & Decision Workspace | B–D | 5 | 18 | 6 | 20 | 1 | 3 | — | notStarted (generated) |
| `ADM-250` | Workflow Instance Monitor & Process Timeline | B–D | 9 | 20 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-251` | Workflow Exception, Failure & Recovery Center | B–D | 9 | 22 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-252` | SLA, Escalation & Bottleneck Monitor | B–D | 9 | 168 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-253` | Automation Execution & Autonomous Action Monitor | B–D | 0 | 34 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-254` | Cross-Module Orchestration Monitor | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-255` | Workflow Analytics & Process Performance | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-256` | Process Optimization & Automation Opportunity Center | B–D | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-257` | AI Workflow Intelligence & Autonomous Governance Center | B–D | 0 | 13 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-249, ADM-253, ADM-254, ADM-256, ADM-257 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-248` Workflow Operations Command Center

**Provide administrators and operational managers with a real-time view of all workflow activity across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-operations-command-center-adm-248` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Module | text field | — | — | `listWorkflow` ?module |
| Status | text field | — | — | `listWorkflow` ?status |
| Priority | text field | — | — | `listWorkflow` ?priority |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Workflows Running** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Started Today** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Completed Today** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Pending Approvals** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Waiting Tasks** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**SLA At Risk** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**SLA Breached** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Failed Workflows** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Escalated** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Automated Executions** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Minutes** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Automation Success Rate** (metric tile, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Workflows running | 1,234 | Workflows Running |
| Started today | 1,234 | Started Today |
| Completed today | 1,234 | Completed Today |
| Pending approvals | 1,234 | Pending Approvals |
| Waiting tasks | 1,234 | Waiting Tasks |

**Every workflow operations** (data table, from `listWorkflow`)

| Shows | Format | Notes |
|---|---|---|
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |

**The selected workflow operations** (detail panel): The pack groups this record's detail under its own headings: “Show activity originating from”, “Use”, “Refund Approval Workflow”.

| Shows | Format | Notes |
|---|---|---|
| Workflow instance | text | Workflow Instance ID |
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Owner | text | Owner |
| Priority | text | Priority |
| Sla | text | SLA |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |

**Data it reads**: `listWorkflow` (onLoad, Workflow Operations Command Center)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-249` Unified Approval Inbox & Decision Workspace: *Works in Unified Approval Inbox & Decision Workspace*; calls `listWorkflow`
- → `ADM-250` Workflow Instance Monitor & Process Timeline: *Works in Workflow Instance Monitor & Process Timeline*; calls `listWorkflow`
- → `ADM-251` Workflow Exception, Failure & Recovery Center: *Works in Workflow Exception, Failure & Recovery Center*; calls `listWorkflow`
- → `ADM-252` SLA, Escalation & Bottleneck Monitor: *Works in SLA, Escalation & Bottleneck Monitor*; calls `listWorkflow`
- → `ADM-253` Automation Execution & Autonomous Action Monitor: *Works in Automation Execution & Autonomous Action Monitor*; calls `listWorkflow`
- → `ADM-254` Cross-Module Orchestration Monitor: *Works in Cross-Module Orchestration Monitor*; calls `listWorkflow`
- → `ADM-255` Workflow Analytics & Process Performance: *Works in Workflow Analytics & Process Performance*; calls `listWorkflow`
- → `ADM-256` Process Optimization & Automation Opportunity Center: *Works in Process Optimization & Automation Opportunity Center*; calls `listWorkflow`
- → `ADM-257` AI Workflow Intelligence & Autonomous Governance Center: *Works in AI Workflow Intelligence & Autonomous Governance Center*; calls `listWorkflow`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow operations yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listWorkflow` → `APPROVAL_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-248` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-248`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 1: Opens Workflow Operations Command Center → Provide administrators and operational managers with a real-time view of all workflow activity across TICVAI.
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F165 branch at step 1 (expected): when Nothing has been set up on Workflow Operations Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F165 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (262 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-248?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-249`, `ADM-250`, `ADM-251`, `ADM-252`, `ADM-253`, `ADM-254`, `ADM-255`, `ADM-256`, `ADM-257`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-249` Unified Approval Inbox & Decision Workspace

**Provide users with one approval inbox across all TICVAI modules. This is extremely important. A manager should not need to open Finance for one approval, Pricing for another, Procurement for another, and Customer Service for another.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_DECIDE`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `requestId` (navigation), `approvalRequestId` (navigation) |
| Route | `/platform/unified-approval-inbox-decision-workspace-adm-249` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

**Sent by *Approve*** (`decideApprovalRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | radio group | required | — | Approve · Reject · Return · Request information | — | — | `decideApprovalRequest` body |
| Comment `comment` | text area | optional | — | max length 1000 | — | — | `decideApprovalRequest` body |
| Reason `reason` | text area | optional | — | max length 500 | — | Required on rejection. | `decideApprovalRequest` body |
| Step up token `stepUpToken` | text field | optional | — | — | — | Where the rule demands MFA (11.1.60). | `decideApprovalRequest` body |
| Signature `signature` | text field | optional | — | — | — | 11.1.57. Where the rule demands a digital signature. | `decideApprovalRequest` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every unified approval decision** (data table, from `listApprovalRequests`)

| Shows | Format | Notes |
|---|---|---|
| ID | text | — |
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Subject contract | text | — |
| Requested by principal | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Requested at | 1 Oct 2026, 14:30 | — |
| Sla due at | 1 Oct 2026, 14:30 | — |
| Current level | 1,234 | — |
| Status | chip: Draft, Pending, Escalated, Returned, Information requested, Approved… | — |

**The selected unified approval decision** (detail panel): The pack groups this record's detail under its own headings: “Pricing”, “Customer Service”, “Procurement”, “Resource Management”, “Request”, “Context”.

| Shows | Format | Notes |
|---|---|---|
| ID | text | — |
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Subject contract | text | — |
| Requested by principal | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Requested at | 1 Oct 2026, 14:30 | — |
| Sla due at | 1 Oct 2026, 14:30 | — |
| Current level | 1,234 | — |
| Status | chip: Draft, Pending, Escalated, Returned, Information requested, Approved… | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Approve (primary button) | `decideApprovalRequest` POST `/approval-requests/{requestId}/decide` | inline | ApprovalRequest | 403 The approver may not decide this request. Always carries `refusedReason`, one value per cause — the approver is the requester (`approverIsRequester`), is not … (ApprovalRefusedProblem); 409 The request is no longer … | — |

**Data it reads**: `listApprovalRequests` (onLoad, The approval inbox); `getApprovalRequestScore` (onLoad, Risk band, priority and suggested escalation for the …)

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The unified approval decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the unified approval decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No unified approval decision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the unified approval decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and … (ApprovalStateProblem) |

#### Permissions

- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public
- `decideApprovalRequest` → `APPROVAL_DECIDE` (operate) · staff, public
- `getApprovalRequestScore` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

20 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 11.1.20 | Approval Comments - System shall allow approvers to add comments to approval decisions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.21 | Approval Rejection Reasons - System shall require rejection reasons when approvals are denied. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.57 | Digital Signature Support - System shall support digital signatures for sensitive approvals. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.59 | Approval Authentication - System shall require authentication before approval actions are executed. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| 11.1.60 | MFA-Protected Approvals - System shall support MFA requirements for sensitive approval actions. | Approval Workflows & Governance | CONTRACTED | `decideApprovalRequest` |
| … 8 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval command centre/inbox shows all pending, validated and renewal requests and lets requests be assigned or reassigned to the relevant department or person. Approvals apply to any request type (new product, price change, website change). *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-723)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-249` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-249`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 2: Works in Unified Approval Inbox & Decision Workspace → Provide users with one approval inbox across all TICVAI modules. This is extremely important. A manager should not need to open Finance for one approval, Pricing for another, Procurement for another …

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-249?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve.
- [ ] Every transition is wired: `ADM-248`.
- [ ] Every gated control is gated: `APPROVAL_DECIDE`, `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-250` Workflow Instance Monitor & Process Timeline

**Allow administrators to inspect exactly what is happening inside an individual running workflow.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_ACT`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§For each step show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `instanceId` (navigation) |
| Route | `/platform/workflow-instance-monitor-process-timeline-adm-250` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workflow instance | text field | — | — | `listWorkflowInstanceProcess` ?workflowInstance |
| Source module | text field | — | — | `listWorkflowInstanceProcess` ?sourceModule |
| Current status | text field | — | — | `listWorkflowInstanceProcess` ?currentStatus |

**Form: Act on workflow instance** (modal, opened by *Act on workflow instance*; *Act on workflow instance* calls `actOnWorkflowInstance`, *Cancel* sends nothing)

**Collects what `actOnWorkflowInstance` sends before it is called.** Required: `action`, `reason`. Optional: `workflowStepExecutionId`, `workflowExceptionId`, `assigneePrincipalId`, `alternativeNodeId`, `correctedInput`, `extendByMinutes`, `priority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Reassign · Retry step · Skip step · Resume · Cancel · Extend sla · Add backup approver · Change priority · Escalate exception | — | What an operator did to a running workflow instance (pack 13.2.3, 13.2.4 and 13.2.5; decided 29 September, writers pass). | `actOnWorkflowInstance` body |
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | Mandatory for every action (pack 13.2.5, "actions capture a mandatory reason") | `actOnWorkflowInstance` body |
| Workflow step execution `workflowStepExecutionId` | picker: choose a workflow step execution | optional | — | — | shows names, sends the id | The step acted on; for `retryStep` the step to retry from. | `actOnWorkflowInstance` body |
| Workflow exception `workflowExceptionId` | picker: choose a workflow exception | optional | — | — | shows names, sends the id | The exception the action is taken from; required for `escalateException` | `actOnWorkflowInstance` body |
| Assignee principal `assigneePrincipalId` | picker: choose an assignee principal | optional | — | — | shows names, sends the id | Required for `reassign`, `addBackupApprover` and `escalateException` | `actOnWorkflowInstance` body |
| Alternative node `alternativeNodeId` | text field | optional | — | — | — | For `skipStep`, the node to continue at instead of the next one (Use Approved Alternative) | `actOnWorkflowInstance` body |
| Corrected input `correctedInput` | key and value settings | optional | — | — | — | For `resume`, the corrected input of the failed step (Correct Data) | `actOnWorkflowInstance` body |
| Extend by minutes `extendByMinutes` | number field (minutes) | optional | — | min 1; max 43200 | — | Required for `extendSla` | `actOnWorkflowInstance` body |
| Priority `priority` | text field | optional | — | max length 30 | — | Required for `changePriority` | `actOnWorkflowInstance` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not …

#### Outputs: what the screen shows and produces

**Shown**

**Workflow Instance** (metric tile)

**Workflow Name** (metric tile)

**Version** (metric tile)

**Source Module** (metric tile)

**Business Object** (metric tile)

**Initiated By** (metric tile)

**Start Time** (metric tile)

**Current Status** (metric tile)

**Current Step** (metric tile)

**SLA** (metric tile)

**Every workflow instance process** (data table, from `listWorkflowInstanceProcess`)

| Shows | Format | Notes |
|---|---|---|
| Step | text | Step |
| Type | text | Type |
| Started | 1 Oct 2026, 14:30 | Started |
| Completed | 1 Oct 2026, 14:30 | Completed |
| Assigned to | text | Assigned To |
| Input | text | Input |
| Output | text | Output |
| Decision | text | Decision |
| Duration | 1,234 | Seconds |
| Status | text | Status |

**The selected workflow instance process** (detail panel): The pack groups this record's detail under its own headings: “Execute Refund”, “Notify Customer”, “Show all”.

| Shows | Format | Notes |
|---|---|---|
| Step | text | Step |
| Type | text | Type |
| Started | 1 Oct 2026, 14:30 | Started |
| Completed | 1 Oct 2026, 14:30 | Completed |
| Assigned to | text | Assigned To |
| Input | text | Input |
| Output | text | Output |
| Decision | text | Decision |
| Duration | 1,234 | Seconds |
| Status | text | Status |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Reassign, Retry Step, Skip Step where explicitly allowed, Cancel Workflow, Resume, Escalate, Open Source Record. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Act on workflow instance (primary button) | `actOnWorkflowInstance` POST `/workflow-instances/{instanceId}/actions` | WorkflowInstanceActionInput | WorkflowInstance | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` … | gated `APPROVAL_ACT`; opens modal first |

**Data it reads**: `listWorkflowInstanceProcess` (onLoad, Workflow Instance Monitor & Process Timeline)

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `listWorkflowInstanceProcess`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow instance process list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow instance process untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow instance process yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow instance process are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not … |

#### Permissions

- `listWorkflowInstanceProcess` → `APPROVAL_VIEW` (read) · staff
- `actOnWorkflowInstance` → `APPROVAL_ACT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-250` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-250`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 4: Works in Workflow Instance Monitor & Process Timeline → Allow administrators to inspect exactly what is happening inside an individual running workflow.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-250?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Act on workflow instance.
- [ ] Every transition is wired: `ADM-248`.
- [ ] Every gated control is gated: `APPROVAL_ACT`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-251` Workflow Exception, Failure & Recovery Center

**Provide one controlled workspace for failed workflow executions.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_ACT`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `instanceId` (navigation) |
| Route | `/platform/workflow-exception-failure-recovery-center-adm-251` |

**Known gaps.** **The pack names 15 actions on this screen and the screen declares 1 operation.** Unserved: Business Rule Failure, Missing Data, Permission Failure, Integration Failure, Action Failure, Duplicate …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Error type | text field | — | — | `listWorkflowExceptionFailure` ?errorType |
| Module | text field | — | — | `listWorkflowExceptionFailure` ?module |
| Priority | text field | — | — | `listWorkflowExceptionFailure` ?priority |

**Form: Act on workflow instance** (modal, opened by *Act on workflow instance*; *Act on workflow instance* calls `actOnWorkflowInstance`, *Cancel* sends nothing)

**Collects what `actOnWorkflowInstance` sends before it is called.** Required: `action`, `reason`. Optional: `workflowStepExecutionId`, `workflowExceptionId`, `assigneePrincipalId`, `alternativeNodeId`, `correctedInput`, `extendByMinutes`, `priority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Reassign · Retry step · Skip step · Resume · Cancel · Extend sla · Add backup approver · Change priority · Escalate exception | — | What an operator did to a running workflow instance (pack 13.2.3, 13.2.4 and 13.2.5; decided 29 September, writers pass). | `actOnWorkflowInstance` body |
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | Mandatory for every action (pack 13.2.5, "actions capture a mandatory reason") | `actOnWorkflowInstance` body |
| Workflow step execution `workflowStepExecutionId` | picker: choose a workflow step execution | optional | — | — | shows names, sends the id | The step acted on; for `retryStep` the step to retry from. | `actOnWorkflowInstance` body |
| Workflow exception `workflowExceptionId` | picker: choose a workflow exception | optional | — | — | shows names, sends the id | The exception the action is taken from; required for `escalateException` | `actOnWorkflowInstance` body |
| Assignee principal `assigneePrincipalId` | picker: choose an assignee principal | optional | — | — | shows names, sends the id | Required for `reassign`, `addBackupApprover` and `escalateException` | `actOnWorkflowInstance` body |
| Alternative node `alternativeNodeId` | text field | optional | — | — | — | For `skipStep`, the node to continue at instead of the next one (Use Approved Alternative) | `actOnWorkflowInstance` body |
| Corrected input `correctedInput` | key and value settings | optional | — | — | — | For `resume`, the corrected input of the failed step (Correct Data) | `actOnWorkflowInstance` body |
| Extend by minutes `extendByMinutes` | number field (minutes) | optional | — | min 1; max 43200 | — | Required for `extendSla` | `actOnWorkflowInstance` body |
| Priority `priority` | text field | optional | — | max length 30 | — | Required for `changePriority` | `actOnWorkflowInstance` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not …

#### Outputs: what the screen shows and produces

**Shown**

**Every workflow exception failure** (data table, from `listWorkflowExceptionFailure`)

| Shows | Format | Notes |
|---|---|---|
| Exception | text | Exception ID |
| Workflow | text | Workflow |
| Instance | text | Instance |
| Module | text | Module |
| Failed step | text | Step that failed |
| Error type | chip: Business rule failure, Missing data, Missing approver, Permission failure … | Kind of failure |
| Time | 1 Oct 2026, 14:30 | Time |
| Retry count | text | not in the schema: `Retry Count` |
| Business impact | text | Business Impact |
| Priority | text | Priority |
| Owner | text | Owner |

**The selected workflow exception failure** (detail panel): The pack groups this record's detail under its own headings: “Dead-Letter Handling”, “Compensation Actions”, “Possible compensation”.

| Shows | Format | Notes |
|---|---|---|
| Exception | text | Exception ID |
| Workflow | text | Workflow |
| Instance | text | Instance |
| Module | text | Module |
| Failed step | text | Step that failed |
| Error type | chip: Business rule failure, Missing data, Missing approver, Permission failure … | Kind of failure |
| Time | 1 Oct 2026, 14:30 | Time |
| Retry count | text | not in the schema: `Retry Count` |
| Business impact | text | Business Impact |
| Priority | text | Priority |
| Owner | text | Owner |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Business Rule Failure (primary button) | navigation or local | — | — | — | — |
| Missing Data (secondary button) | navigation or local | — | — | — | — |
| Permission Failure (secondary button) | navigation or local | — | — | — | — |
| Integration Failure (secondary button) | navigation or local | — | — | — | — |
| Action Failure (secondary button) | navigation or local | — | — | — | — |
| Duplicate Event (secondary button) | navigation or local | — | — | — | — |
| Service Unavailable (secondary button) | navigation or local | — | — | — | — |
| Configuration Error (secondary button) | navigation or local | — | — | — | — |
| Act on workflow instance (secondary button) | `actOnWorkflowInstance` POST `/workflow-instances/{instanceId}/actions` | WorkflowInstanceActionInput | WorkflowInstance | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` … | gated `APPROVAL_ACT`; opens modal first |

**Data it reads**: `listWorkflowExceptionFailure` (onLoad, Workflow Exception, Failure & Recovery Center)

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `listWorkflowExceptionFailure`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow exception failure list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow exception failure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow exception failure yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow exception failure are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not … |

#### Permissions

- `listWorkflowExceptionFailure` → `APPROVAL_VIEW` (read) · staff
- `actOnWorkflowInstance` → `APPROVAL_ACT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-251` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-251`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 6: Works in Workflow Exception, Failure & Recovery Center → Provide one controlled workspace for failed workflow executions.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-251?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Business Rule Failure, Missing Data, Permission Failure, Integration Failure, Action Failure, Duplicate Event, Service Unavailable, Configuration Error, Act on workflow instance.
- [ ] Every transition is wired: `ADM-248`.
- [ ] Every gated control is gated: `APPROVAL_ACT`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-252` SLA, Escalation & Bottleneck Monitor

**Monitor workflows approaching or exceeding configured time limits.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_ACT`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `instanceId` (navigation) |
| Route | `/platform/sla-escalation-bottleneck-monitor-adm-252` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workflow | text field | — | — | `listSlaEscalationBottleneck` ?workflow |
| Risk | text field | — | — | `listSlaEscalationBottleneck` ?risk |
| Escalation level | text field | — | — | `listSlaEscalationBottleneck` ?escalationLevel |

**Form: Act on workflow instance** (modal, opened by *Act on workflow instance*; *Act on workflow instance* calls `actOnWorkflowInstance`, *Cancel* sends nothing)

**Collects what `actOnWorkflowInstance` sends before it is called.** Required: `action`, `reason`. Optional: `workflowStepExecutionId`, `workflowExceptionId`, `assigneePrincipalId`, `alternativeNodeId`, `correctedInput`, `extendByMinutes`, `priority`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | select | required | — | Reassign · Retry step · Skip step · Resume · Cancel · Extend sla · Add backup approver · Change priority · Escalate exception | — | What an operator did to a running workflow instance (pack 13.2.3, 13.2.4 and 13.2.5; decided 29 September, writers pass). | `actOnWorkflowInstance` body |
| Reason `reason` | text area | required | — | min length 1; max length 500 | — | Mandatory for every action (pack 13.2.5, "actions capture a mandatory reason") | `actOnWorkflowInstance` body |
| Workflow step execution `workflowStepExecutionId` | picker: choose a workflow step execution | optional | — | — | shows names, sends the id | The step acted on; for `retryStep` the step to retry from. | `actOnWorkflowInstance` body |
| Workflow exception `workflowExceptionId` | picker: choose a workflow exception | optional | — | — | shows names, sends the id | The exception the action is taken from; required for `escalateException` | `actOnWorkflowInstance` body |
| Assignee principal `assigneePrincipalId` | picker: choose an assignee principal | optional | — | — | shows names, sends the id | Required for `reassign`, `addBackupApprover` and `escalateException` | `actOnWorkflowInstance` body |
| Alternative node `alternativeNodeId` | text field | optional | — | — | — | For `skipStep`, the node to continue at instead of the next one (Use Approved Alternative) | `actOnWorkflowInstance` body |
| Corrected input `correctedInput` | key and value settings | optional | — | — | — | For `resume`, the corrected input of the failed step (Correct Data) | `actOnWorkflowInstance` body |
| Extend by minutes `extendByMinutes` | number field (minutes) | optional | — | min 1; max 43200 | — | Required for `extendSla` | `actOnWorkflowInstance` body |
| Priority `priority` | text field | optional | — | max length 30 | — | Required for `changePriority` | `actOnWorkflowInstance` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not …

#### Outputs: what the screen shows and produces

**Shown**

**Within SLA** (metric tile, from `listSlaEscalationBottleneck`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Owner | text | Owner |
| Started | 1 Oct 2026, 14:30 | Started |
| Target | 1 Oct 2026, 14:30 | SLA deadline |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Risk | text | Risk |
| Escalation level | text | Escalation Level |
| First reminder | 1 Oct 2026, 14:30 | First Reminder |
| Second reminder | 1 Oct 2026, 14:30 | Second Reminder |
| Manager escalation | 1 Oct 2026, 14:30 | Manager Escalation |
| Executive escalation | 1 Oct 2026, 14:30 | Executive Escalation |
| Final outcome | text | Final Outcome |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Within sla | 1,234 | Within SLA |
| At risk | 1,234 | At Risk |

**At Risk** (metric tile, from `listSlaEscalationBottleneck`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Owner | text | Owner |
| Started | 1 Oct 2026, 14:30 | Started |
| Target | 1 Oct 2026, 14:30 | SLA deadline |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Risk | text | Risk |
| Escalation level | text | Escalation Level |
| First reminder | 1 Oct 2026, 14:30 | First Reminder |
| Second reminder | 1 Oct 2026, 14:30 | Second Reminder |
| Manager escalation | 1 Oct 2026, 14:30 | Manager Escalation |
| Executive escalation | 1 Oct 2026, 14:30 | Executive Escalation |
| Final outcome | text | Final Outcome |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Within sla | 1,234 | Within SLA |
| At risk | 1,234 | At Risk |

**Breached** (metric tile, from `listSlaEscalationBottleneck`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Owner | text | Owner |
| Started | 1 Oct 2026, 14:30 | Started |
| Target | 1 Oct 2026, 14:30 | SLA deadline |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Risk | text | Risk |
| Escalation level | text | Escalation Level |
| First reminder | 1 Oct 2026, 14:30 | First Reminder |
| Second reminder | 1 Oct 2026, 14:30 | Second Reminder |
| Manager escalation | 1 Oct 2026, 14:30 | Manager Escalation |
| Executive escalation | 1 Oct 2026, 14:30 | Executive Escalation |
| Final outcome | text | Final Outcome |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Within sla | 1,234 | Within SLA |
| At risk | 1,234 | At Risk |

**Escalated** (metric tile, from `listSlaEscalationBottleneck`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Owner | text | Owner |
| Started | 1 Oct 2026, 14:30 | Started |
| Target | 1 Oct 2026, 14:30 | SLA deadline |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Risk | text | Risk |
| Escalation level | text | Escalation Level |
| First reminder | 1 Oct 2026, 14:30 | First Reminder |
| Second reminder | 1 Oct 2026, 14:30 | Second Reminder |
| Manager escalation | 1 Oct 2026, 14:30 | Manager Escalation |
| Executive escalation | 1 Oct 2026, 14:30 | Executive Escalation |
| Final outcome | text | Final Outcome |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Within sla | 1,234 | Within SLA |
| At risk | 1,234 | At Risk |

**Minutes** (metric tile, from `listSlaEscalationBottleneck`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Owner | text | Owner |
| Started | 1 Oct 2026, 14:30 | Started |
| Target | 1 Oct 2026, 14:30 | SLA deadline |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Risk | text | Risk |
| Escalation level | text | Escalation Level |
| First reminder | 1 Oct 2026, 14:30 | First Reminder |
| Second reminder | 1 Oct 2026, 14:30 | Second Reminder |
| Manager escalation | 1 Oct 2026, 14:30 | Manager Escalation |
| Executive escalation | 1 Oct 2026, 14:30 | Executive Escalation |
| Final outcome | text | Final Outcome |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Within sla | 1,234 | Within SLA |
| At risk | 1,234 | At Risk |

**Minutes** (metric tile, from `listSlaEscalationBottleneck`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Owner | text | Owner |
| Started | 1 Oct 2026, 14:30 | Started |
| Target | 1 Oct 2026, 14:30 | SLA deadline |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Risk | text | Risk |
| Escalation level | text | Escalation Level |
| First reminder | 1 Oct 2026, 14:30 | First Reminder |
| Second reminder | 1 Oct 2026, 14:30 | Second Reminder |
| Manager escalation | 1 Oct 2026, 14:30 | Manager Escalation |
| Executive escalation | 1 Oct 2026, 14:30 | Executive Escalation |
| Final outcome | text | Final Outcome |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Within sla | 1,234 | Within SLA |
| At risk | 1,234 | At Risk |

**Longest Waiting Step** (metric tile, from `listSlaEscalationBottleneck`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Owner | text | Owner |
| Started | 1 Oct 2026, 14:30 | Started |
| Target | 1 Oct 2026, 14:30 | SLA deadline |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Risk | text | Risk |
| Escalation level | text | Escalation Level |
| First reminder | 1 Oct 2026, 14:30 | First Reminder |
| Second reminder | 1 Oct 2026, 14:30 | Second Reminder |
| Manager escalation | 1 Oct 2026, 14:30 | Manager Escalation |
| Executive escalation | 1 Oct 2026, 14:30 | Executive Escalation |
| Final outcome | text | Final Outcome |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |
| Summary | grouped details | The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September … |
| Within sla | 1,234 | Within SLA |
| At risk | 1,234 | At Risk |

**Every sla escalation bottleneck** (data table, from `listSlaEscalationBottleneck`)

| Shows | Format | Notes |
|---|---|---|
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Owner | text | Owner |
| Started | 1 Oct 2026, 14:30 | Started |
| Target | 1 Oct 2026, 14:30 | SLA deadline |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Risk | text | Risk |
| Escalation level | text | Escalation Level |
| First reminder | 1 Oct 2026, 14:30 | First Reminder |
| Second reminder | 1 Oct 2026, 14:30 | Second Reminder |
| Manager escalation | 1 Oct 2026, 14:30 | Manager Escalation |
| Executive escalation | 1 Oct 2026, 14:30 | Executive Escalation |
| Final outcome | text | Final Outcome |

**The selected sla escalation bottleneck** (detail panel): The pack groups this record's detail under its own headings: “Purchase Order Approval”, “Breakdown”.

| Shows | Format | Notes |
|---|---|---|
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Owner | text | Owner |
| Started | 1 Oct 2026, 14:30 | Started |
| Target | 1 Oct 2026, 14:30 | SLA deadline |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Risk | text | Risk |
| Escalation level | text | Escalation Level |
| First reminder | 1 Oct 2026, 14:30 | First Reminder |
| Second reminder | 1 Oct 2026, 14:30 | Second Reminder |
| Manager escalation | 1 Oct 2026, 14:30 | Manager Escalation |
| Executive escalation | 1 Oct 2026, 14:30 | Executive Escalation |
| Final outcome | text | Final Outcome |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Reassign, Escalate, Extend SLA, Add Backup Approver, Change Priority. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Act on workflow instance (primary button) | `actOnWorkflowInstance` POST `/workflow-instances/{instanceId}/actions` | WorkflowInstanceActionInput | WorkflowInstance | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` … | gated `APPROVAL_ACT`; opens modal first |

**Data it reads**: `listSlaEscalationBottleneck` (onLoad, SLA, Escalation & Bottleneck Monitor)

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `listSlaEscalationBottleneck`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sla escalation bottleneck list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sla escalation bottleneck untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sla escalation bottleneck yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sla escalation bottleneck are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not … |

#### Permissions

- `listSlaEscalationBottleneck` → `APPROVAL_VIEW` (read) · staff
- `actOnWorkflowInstance` → `APPROVAL_ACT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-252` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-252`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 8: Works in SLA, Escalation & Bottleneck Monitor → Monitor workflows approaching or exceeding configured time limits.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (168 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-252?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Act on workflow instance.
- [ ] Every transition is wired: `ADM-248`.
- [ ] Every gated control is gated: `APPROVAL_ACT`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-253` Automation Execution & Autonomous Action Monitor

**Provide visibility and governance over actions executed automatically by TICVAI. This becomes especially important as TICVAI becomes more AI-driven.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/automation-execution-autonomous-action-monitor-adm-253` |

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every automation execution autonomous** (data table, from `createAutomationAutonomouAction`)

| Shows | Format | Notes |
|---|---|---|
| Automated actions today | 1,234 | Automated Actions Today |
| Successful | 1,234 | Successful |
| Failed | 1,234 | Failed |
| Human confirmation required | 1,234 | Actions waiting for human confirmation |
| Reversed | 1,234 | Reversed |
| Suspended | 1,234 | Suspended |
| Estimated manual actions avoided | 1,234 | Estimated Manual Actions Avoided |
| Estimated time saved | 1,234 | Minutes |
| Automation | text | Automation |
| Trigger | text | not in the schema: `Trigger` |
| Business object | text | Business Object |
| Rule | text | Rule |
| Action | text | Action |
| Result | text | Result |
| Confidence where AI assisted | 1,234.5 | Confidence of an AI-assisted non-approval action; never set for approve or reject |
| Execution time | 1 Oct 2026, 14:30 | Execution Time |
| Status | chip: Active, Paused, Disabled, Kill switched | Status |

**The selected automation execution autonomous** (detail panel): The pack groups this record's detail under its own headings: “Waiver Reminder Automation”, “Authorized administrators can”.

| Shows | Format | Notes |
|---|---|---|
| Automated actions today | 1,234 | Automated Actions Today |
| Successful | 1,234 | Successful |
| Failed | 1,234 | Failed |
| Human confirmation required | 1,234 | Actions waiting for human confirmation |
| Reversed | 1,234 | Reversed |
| Suspended | 1,234 | Suspended |
| Estimated manual actions avoided | 1,234 | Estimated Manual Actions Avoided |
| Estimated time saved | 1,234 | Minutes |
| Automation | text | Automation |
| Trigger | text | not in the schema: `Trigger` |
| Business object | text | Business Object |
| Rule | text | Rule |
| Action | text | Action |
| Result | text | Result |
| Confidence where AI assisted | 1,234.5 | Confidence of an AI-assisted non-approval action; never set for approve or reject |
| Execution time | 1 Oct 2026, 14:30 | Execution Time |
| Status | chip: Active, Paused, Disabled, Kill switched | Status |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `createAutomationAutonomouAction`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The automation execution autonomous list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the automation execution autonomous untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No automation execution autonomous yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the automation execution autonomous are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `createAutomationAutonomouAction` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-253` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-253`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 10: Works in Automation Execution & Autonomous Action Monitor → Provide visibility and governance over actions executed automatically by TICVAI. This becomes especially important as TICVAI becomes more AI-driven.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-253?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create.
- [ ] Every transition is wired: `ADM-248`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-254` Cross-Module Orchestration Monitor

**Monitor complex workflows involving multiple TICVAI services. Example — Group Booking Confirmation**

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
| Route | `/platform/cross-module-orchestration-monitor-adm-254` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Correlation | text field | — | — | `listCrossModuleOrchestration` ?correlationId |
| Status | text field | — | — | `listCrossModuleOrchestration` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listCrossModuleOrchestration` (onLoad, Cross-Module Orchestration Monitor)

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `listCrossModuleOrchestration`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The cross-module orchestration list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the cross-module orchestration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No cross-module orchestration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-module orchestration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCrossModuleOrchestration` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-254` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-254`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 12: Works in Cross-Module Orchestration Monitor → Monitor complex workflows involving multiple TICVAI services. Example — Group Booking Confirmation

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-254?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-248`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-255` Workflow Analytics & Process Performance

**Measure how effectively TICVAI's business workflows are performing.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Analyze; Measure; Compare) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-analytics-process-performance-adm-255` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search workflow analytics process | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by workflow, module, venue, brand, business process, department and 4 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workflow | text field | — | — | `listWorkflowProcessPerformance` ?workflow |
| Module | text field | — | — | `listWorkflowProcessPerformance` ?module |
| Venue | text field | — | — | `listWorkflowProcessPerformance` ?venue |
| Brand | text field | — | — | `listWorkflowProcessPerformance` ?brand |
| Business process | text field | — | — | `listWorkflowProcessPerformance` ?businessProcess |
| Department | text field | — | — | `listWorkflowProcessPerformance` ?department |
| Approver | text field | — | — | `listWorkflowProcessPerformance` ?approver |
| User | text field | — | — | `listWorkflowProcessPerformance` ?user |
| From | text field | — | — | `listWorkflowProcessPerformance` ?from |
| To | text field | — | — | `listWorkflowProcessPerformance` ?to |
| Min transaction value | text field | — | — | `listWorkflowProcessPerformance` ?minTransactionValue |
| Max transaction value | text field | — | — | `listWorkflowProcessPerformance` ?maxTransactionValue |

#### Outputs: what the screen shows and produces

**Shown**

**Workflow Volume** (metric tile)

**Completion Rate** (metric tile)

**Failure Rate** (metric tile)

**Average Completion Time** (metric tile)

**Approval Time** (metric tile)

**Automation Rate** (metric tile)

**Escalation Rate** (metric tile)

**Rejection Rate** (metric tile)

**Rework Rate** (metric tile)

**SLA Compliance** (metric tile)

**Average Approval Time** (metric tile)

**Approval Rate** (metric tile)

**Request Changes Rate** (metric tile)

**Delegation Rate** (metric tile)

**Data it reads**: `listWorkflowProcessPerformance` (onLoad, Workflow Analytics & Process Performance)

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `listWorkflowProcessPerformance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow analytics process list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow analytics process untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow analytics process yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow analytics process are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listWorkflowProcessPerformance` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-255` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-255`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 14: Works in Workflow Analytics & Process Performance → Measure how effectively TICVAI's business workflows are performing.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-255?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-248`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-256` Process Optimization & Automation Opportunity Center

**Identify business processes that should be simplified, redesigned or automated. This is where TICVAI moves beyond simply running workflows.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Identify; Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/process-optimization-automation-opportunity-center-adm-256` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Opportunity type | text field | — | — | `listProcessAutomationOpportunity` ?opportunityType |
| Module | text field | — | — | `listProcessAutomationOpportunity` ?module |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every process optimization automation** (data table, from `listProcessAutomationOpportunity`)

| Shows | Format | Notes |
|---|---|---|
| Opportunity type | chip: Repetitive approval, Unnecessary approval, High manual work, Excessive rework, Long … | Kind of improvement opportunity |
| Duplicate steps | text | not in the schema: `Duplicate Steps` |
| Process | text | Process |
| Module | text | Module |
| Monthly volume | 1,234 | Monthly Volume |
| Current steps | 1,234 | Current Steps |
| Average duration | 1,234 | Minutes |
| Manual steps | 1,234 | Manual Steps |
| Approval rate | 12.5% | Approval Rate |
| Exception rate | 12.5% | Exception Rate |
| Estimated opportunity | text | Estimated Opportunity |

**The selected process optimization automation** (detail panel): The pack groups this record's detail under its own headings: “Low-Value Refund Approval”, “Before changing anything”, “Estimated result”.

| Shows | Format | Notes |
|---|---|---|
| Opportunity type | chip: Repetitive approval, Unnecessary approval, High manual work, Excessive rework, Long … | Kind of improvement opportunity |
| Duplicate steps | text | not in the schema: `Duplicate Steps` |
| Process | text | Process |
| Module | text | Module |
| Monthly volume | 1,234 | Monthly Volume |
| Current steps | 1,234 | Current Steps |
| Average duration | 1,234 | Minutes |
| Manual steps | 1,234 | Manual Steps |
| Approval rate | 12.5% | Approval Rate |
| Exception rate | 12.5% | Exception Rate |
| Estimated opportunity | text | Estimated Opportunity |

**Data it reads**: `listProcessAutomationOpportunity` (onLoad, Process Optimization & Automation Opportunity Center)

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `listProcessAutomationOpportunity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The process optimization automation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the process optimization automation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No process optimization automation yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the process optimization automation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listProcessAutomationOpportunity` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-256` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-256`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 16: Works in Process Optimization & Automation Opportunity Center → Identify business processes that should be simplified, redesigned or automated. This is where TICVAI moves beyond simply running workflows.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-256?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-248`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-257` AI Workflow Intelligence & Autonomous Governance Center

**Create the AI intelligence layer across TICVAI's entire rules, workflow and automation ecosystem. This is the management-level AI brain for Area 13.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-workflow-intelligence-autonomous-governance-center-adm-257` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Autonomy level | text field | — | — | `listWorkflowAutonomouGovernance` ?autonomyLevel |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every workflow intelligence autonomous** (data table, from `listWorkflowAutonomouGovernance`)

| Shows | Format | Notes |
|---|---|---|
| Use case | text | AI use case identifier |
| AI model | text | AI Model |
| AI service | text | AI Service |
| Use case | text | Use Case |
| Autonomy level | chip: Observe, Recommend, Prepare, Governed automation, Autonomous low risk | Level 0 to 4; approval decisions are held at observe |
| Decision scope | text | Decision Scope |
| Confidence threshold | 1,234.5 | Confidence Threshold |
| Human approval requirement | text | Human Approval Requirement |
| Execution volume | 1,234 | Execution Volume |
| Exception rate | 12.5% | Exception Rate |
| Last review | 1 Oct 2026, 14:30 | Last Review |
| Owner | text | Owner |
| Override rate | 12.5% | Override rate |

**The selected workflow intelligence autonomous** (detail panel): The pack groups this record's detail under its own headings: “Natural-Language Questions”, “Actual common process”, “Automation”, “Approval Simplification”, “SLA”, “Workflow Redesign”.

**Data it reads**: `listWorkflowAutonomouGovernance` (onLoad, AI Workflow Intelligence & Autonomous Governance Center)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow intelligence autonomous list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow intelligence autonomous untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow intelligence autonomous yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow intelligence autonomous are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listWorkflowAutonomouGovernance` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI actions in progress are shown step by step in an AI action command center; if a process only partly completes (e.g. missing information) it rolls back rather than leaving a product half-configured, and a full change history records everything AI modified. *(client request · MoM 21 Sep 2026, 4.9 Core AI Platform — AI Tools, Agents & Action Orchestration · DI-965)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-257` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-257`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 18: Works in AI Workflow Intelligence & Autonomous Governance Center → Create the AI intelligence layer across TICVAI's entire rules, workflow and automation ecosystem. This is the management-level AI brain for Area 13.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-257?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**3 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"actOnWorkflowInstance": {"method":"POST","path":"/workflow-instances/{instanceId}/actions","contract":"approvals","summary":"An operator's intervention in a running workflow","permission":"APPROVAL_ACT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkflowInstanceActionInput","responds":"WorkflowInstance"},
"createAutomationAutonomouAction": {"method":"POST","path":"/automation-autonomou-action","contract":"approvals","summary":"Automation Execution & Autonomous Action Monitor","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"AutomationExecutionAutonomousActionMonitorInput","responds":"AutomationExecutionAutonomousActionMonitorView"},
"decideApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/decide","contract":"approvals","summary":"Approve, reject, return or ask for information","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"getApprovalRequestScore": {"method":"GET","path":"/approval-requests/{approvalRequestId}/score","contract":"ai","summary":"The latest context score of an approval request","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiApprovalRequestScore"},
"listApprovalRequests": {"method":"GET","path":"/approval-requests","contract":"approvals","summary":"Requests awaiting a decision, or already decided","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToMe","in":"query","required":null},{"name":"raisedByMe","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"breachingWithinMinutes","in":"query","required":null},{"name":"sort","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCrossModuleOrchestration": {"method":"GET","path":"/cross-module-orchestration","contract":"approvals","summary":"Cross-Module Orchestration Monitor","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"correlationId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProcessAutomationOpportunity": {"method":"GET","path":"/process-automation-opportunity","contract":"approvals","summary":"Process Optimization & Automation Opportunity Center","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"opportunityType","in":"query","required":false},{"name":"module","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSlaEscalationBottleneck": {"method":"GET","path":"/sla-escalation-bottleneck","contract":"approvals","summary":"SLA, Escalation & Bottleneck Monitor","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workflow","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"escalationLevel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkflow": {"method":"GET","path":"/workflow","contract":"approvals","summary":"Workflow Operations Command Center","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"module","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkflowAutonomouGovernance": {"method":"GET","path":"/workflow-autonomou-governance","contract":"approvals","summary":"AI Workflow Intelligence & Autonomous Governance Center","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"autonomyLevel","in":"query","required":false}],"requestBody":null,"responds":"AiWorkflowIntelligenceAutonomousGovernanceCenterView"},
"listWorkflowExceptionFailure": {"method":"GET","path":"/workflow-exception-failure","contract":"approvals","summary":"Workflow Exception, Failure & Recovery Center","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"errorType","in":"query","required":false},{"name":"module","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkflowInstanceProcess": {"method":"GET","path":"/workflow-instance-process","contract":"approvals","summary":"Workflow Instance Monitor & Process Timeline","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workflowInstance","in":"query","required":false},{"name":"sourceModule","in":"query","required":false},{"name":"currentStatus","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkflowProcessPerformance": {"method":"GET","path":"/workflow-process-performance","contract":"approvals","summary":"Workflow Analytics & Process Performance","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workflow","in":"query","required":false},{"name":"module","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"brand","in":"query","required":false},{"name":"businessProcess","in":"query","required":false},{"name":"department","in":"query","required":false},{"name":"approver","in":"query","required":false},{"name":"user","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"minTransactionValue","in":"query","required":false},{"name":"maxTransactionValue","in":"query","required":false}],"requestBody":null,"responds":"WorkflowAnalyticsProcessPerformanceView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiApprovalRequestScore": {"type":"object","x-ticvai-persistence":"ai.approval_request_score","description":"**Context for an approval reviewer** (11.1.73..75): risk, priority and a suggested escalation for one pending request, the latest per request. **There is no approve or reject field, by design** (minutes of 8 September: AI in approvals never recommends or influences approve or reject).","required":["approvalRequestId","riskScore","riskBand","priorityScore","escalationSuggestion"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"approvalRequestId":{"type":"string","format":"uuid","x-ticvai-references":"approvals.request"},"trigger":{"type":"string","enum":["submitted","resubmitted","slaTick","escalated"]},"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"],"description":"Design 5.6: a risk score and band, never a probability."},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"description":"For ordering work in an inbox; higher first."},"escalationSuggestion":{"type":"object","required":["action"],"properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}},"description":"A suggestion for an SLA problem, carried out if at all by a person or the tenant's SLA policy."},"signals":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","description":"e.g. `amountAboveRequesterNorm`, `requesterEntityRisk`, `outOfHours`, `irreversibleAction`, `slaDueSoon`, `stepBreachRate`, `approverUnavailable`."},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"basis":{"$ref":"#/components/schemas/SuggestionBasis"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"scoredAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiWorkflowIntelligenceAutonomousGovernanceCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over the AI use-case register, which belongs to the AI service (the AI design is under review, 29 September); not an approvals table and not read directly from here","description":"**What AI Workflow Intelligence & Autonomous Governance Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"useCaseId":{"type":"string","description":"AI use case identifier"},"aiModel":{"type":"string","description":"AI Model"},"aiService":{"type":"string","description":"AI Service"},"useCase":{"type":"string","description":"Use Case"},"autonomyLevel":{"type":"string","enum":["observe","recommend","prepare","governedAutomation","autonomousLowRisk"],"description":"Level 0 to 4; approval decisions are held at observe"},"decisionScope":{"type":"string","description":"Decision Scope"},"confidenceThreshold":{"type":"number","description":"Confidence Threshold"},"humanApprovalRequirement":{"type":"string","description":"Human Approval Requirement"},"executionVolume":{"type":"integer","description":"Execution Volume"},"exceptionRate":{"type":"number","description":"Exception Rate"},"lastReview":{"type":"string","format":"date-time","description":"Last Review"},"owner":{"type":"string","description":"Owner"},"overrideRate":{"type":"number","description":"Override rate"}},"required":["useCaseId"]},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"AutomationExecutionAutonomousActionMonitorInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; updates approvals.automation status (schema Automation) (data model for the agreed operations, 29 September)","description":"**What Automation Execution & Autonomous Action Monitor submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"command":{"type":"string","enum":["pause","resume","disable","killSwitch"],"description":"Control command"},"automationId":{"type":"string","description":"Automation to control"},"reason":{"type":"string","description":"Why the automation is being controlled"}},"required":["automationId","command"]},
"AutomationExecutionAutonomousActionMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.automation and approvals.automation_execution (data model for the agreed operations, 29 September)","description":"**What Automation Execution & Autonomous Action Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"command":{"type":"string","enum":["pause","resume","disable","killSwitch"],"description":"Control command"},"automationId":{"type":"string","description":"Automation to control"},"automatedActionsToday":{"type":"integer","description":"Automated Actions Today"},"successful":{"type":"integer","description":"Successful"},"failed":{"type":"integer","description":"Failed"},"humanConfirmationRequired":{"type":"integer","description":"Actions waiting for human confirmation"},"reversed":{"type":"integer","description":"Reversed"},"suspended":{"type":"integer","description":"Suspended"},"estimatedManualActionsAvoided":{"type":"integer","description":"Estimated Manual Actions Avoided"},"estimatedTimeSaved":{"type":"integer","description":"Minutes"},"automation":{"type":"string","description":"Automation"},"businessObject":{"type":"string","description":"Business Object"},"rule":{"type":"string","description":"Rule"},"action":{"type":"string","description":"Action"},"result":{"type":"string","description":"Result"},"confidenceWhereAiAssisted":{"type":"number","description":"Confidence of an AI-assisted non-approval action; never set for approve or reject"},"executionTime":{"type":"string","format":"date-time","description":"Execution Time"},"status":{"type":"string","enum":["active","paused","disabled","killSwitched"],"description":"Status"},"reason":{"type":"string","description":"Why the automation is being controlled"}},"required":["automationId","command"]},
"CrossModuleOrchestrationMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_step_execution joined to approvals.workflow_instance by correlation id (data model for the agreed operations, 29 September)","description":"**What Cross-Module Orchestration Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"service":{"type":"string","description":"Service"},"action":{"type":"string","description":"Action"},"status":{"type":"string","enum":["notStarted","running","waiting","successful","failed","compensated"],"description":"Status"},"started":{"type":"string","format":"date-time","description":"Started"},"completed":{"type":"string","format":"date-time","description":"Completed"},"duration":{"type":"integer","description":"Seconds"},"inputOutput":{"type":"string","description":"Input/Output"},"failureHandling":{"type":"string","enum":["waits","retries","rollsBack","continuesPartially","requiresHumanIntervention"],"description":"What the workflow does after this node fails"},"retries":{"type":"integer","description":"Retries"},"correlationId":{"type":"string","description":"a common correlation/workflow ID"}},"required":["correlationId","service"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProcessOptimizationAutomationOpportunityCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — aggregated from approvals.workflow_instance and workflow_step_execution per process (data model for the agreed operations, 29 September)","description":"**What Process Optimization & Automation Opportunity Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"opportunityType":{"type":"string","enum":["repetitiveApproval","unnecessaryApproval","highManualWork","excessiveRework","longWaitingTime","duplicateSteps","highFailureRate","lowRiskManualAction","processBottleneck"],"description":"Kind of improvement opportunity"},"process":{"type":"string","description":"Process"},"module":{"type":"string","description":"Module"},"monthlyVolume":{"type":"integer","description":"Monthly Volume"},"currentSteps":{"type":"integer","description":"Current Steps"},"averageDuration":{"type":"integer","description":"Minutes"},"manualSteps":{"type":"integer","description":"Manual Steps"},"approvalRate":{"type":"number","description":"Approval Rate"},"exceptionRate":{"type":"number","description":"Exception Rate"},"estimatedOpportunity":{"type":"string","description":"Estimated Opportunity"}},"required":["process"]},
"SlaEscalationBottleneckMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_instance, whose SLA and reminder timestamps it lists (data model for the agreed operations, 29 September)","description":"**What SLA, Escalation & Bottleneck Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflow":{"type":"string","description":"Workflow"},"instance":{"type":"string","description":"Instance"},"currentStep":{"type":"string","description":"Current Step"},"owner":{"type":"string","description":"Owner"},"started":{"type":"string","format":"date-time","description":"Started"},"target":{"type":"string","format":"date-time","description":"SLA deadline"},"timeRemaining":{"type":"integer","description":"Minutes until breach; negative once breached"},"risk":{"type":"string","description":"Risk"},"escalationLevel":{"type":"string","description":"Escalation Level"},"firstReminder":{"type":"string","format":"date-time","description":"First Reminder"},"secondReminder":{"type":"string","format":"date-time","description":"Second Reminder"},"managerEscalation":{"type":"string","format":"date-time","description":"Manager Escalation"},"executiveEscalation":{"type":"string","format":"date-time","description":"Executive Escalation"},"finalOutcome":{"type":"string","description":"Final Outcome"}},"required":["instance"]},
"SlaEscalationBottleneckMonitorViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"withinSla":{"type":"integer","description":"Within SLA"},"atRisk":{"type":"integer","description":"At Risk"},"breached":{"type":"integer","description":"Breached"},"escalated":{"type":"integer","description":"Escalated"},"averageProcessingTime":{"type":"integer","description":"Minutes"},"averageApprovalTime":{"type":"integer","description":"Minutes"},"longestWaitingStep":{"type":"string","description":"Longest Waiting Step"}}},
"SuggestionBasis": {"type":"string","description":"**How the answer was reached, and this is the field the whole design exists for.**\nA venue must be able to see that today's price suggestion is a margin rule and next quarter's is a trained model — **the same operation, the same screen, a different basis** — and a screen that cannot say which is a screen that asks a manager to trust arithmetic it will not show.\n**Swapping a heuristic for a model is a provider change, not a contract change.** That is the point of the abstraction: the frontend, the audit record and the outcome capture all stay exactly as they are.\n","enum":["heuristic","statistical","model","hybrid","manual"]},
"WorkflowAnalyticsProcessPerformanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — aggregated from approvals.workflow_instance, workflow_step_execution, automation_execution, request, decision and escalation (data model for the agreed operations, 29 September)","description":"**What Workflow Analytics & Process Performance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowVolume":{"type":"integer","description":"Workflow Volume"},"completionRate":{"type":"number","description":"Completion Rate"},"failureRate":{"type":"number","description":"Failure Rate"},"averageCompletionTime":{"type":"integer","description":"Minutes"},"approvalTime":{"type":"integer","description":"Minutes"},"automationRate":{"type":"number","description":"Automation Rate"},"escalationRate":{"type":"number","description":"Escalation Rate"},"rejectionRate":{"type":"number","description":"Rejection Rate"},"reworkRate":{"type":"number","description":"Rework Rate"},"slaCompliance":{"type":"number","description":"Percent within SLA"},"averageApprovalTime":{"type":"integer","description":"Minutes"},"approvalRate":{"type":"number","description":"Approval Rate"},"requestChangesRate":{"type":"number","description":"Request Changes Rate"},"delegationRate":{"type":"number","description":"Delegation Rate"},"manualStepsRemoved":{"type":"integer","description":"Manual Steps Removed"},"processingTimeSaved":{"type":"integer","description":"Minutes"},"workloadReduced":{"type":"number","description":"Staff hours"},"costSavingWhereMeasurable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost Saving where measurable"}}},
"WorkflowExceptionFailureRecoveryCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_exception (schema WorkflowException) (data model for the agreed operations, 29 September)","description":"**What Workflow Exception, Failure & Recovery Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"errorType":{"type":"string","enum":["businessRuleFailure","missingData","missingApprover","permissionFailure","integrationFailure","timeout","actionFailure","invalidState","duplicateEvent","serviceUnavailable","configurationError"],"description":"Kind of failure"},"exceptionId":{"type":"string","description":"Exception ID"},"workflow":{"type":"string","description":"Workflow"},"instance":{"type":"string","description":"Instance"},"module":{"type":"string","description":"Module"},"failedStep":{"type":"string","description":"Step that failed"},"time":{"type":"string","format":"date-time","description":"Time"},"businessImpact":{"type":"string","description":"Business Impact"},"priority":{"type":"string","description":"Priority"},"owner":{"type":"string","description":"Owner"},"retryCount":{"type":"integer","description":"Retry count"}},"required":["exceptionId"]},
"WorkflowInstance": {"type":"object","x-ticvai-persistence":"approvals.workflow_instance","description":"**One running workflow** (pack 13.2.1, 13.2.3 and 13.2.5; data model for the agreed operations, 29 September). Started by a `WorkflowTrigger`, on the version in force at that moment and kept on it to the end (audit R129). Its steps are `WorkflowStepExecution` rows, keyed by the same `correlationId` the participating services trace with. **The SLA clock and its reminder and escalation timestamps are held here**, not in a table of their own: there is one clock per instance, and the SLA, Escalation & Bottleneck Monitor lists instances. Lifecycle in `states/workflow-instance.yaml`. The engine writes this row; an operator changes it only through `actOnWorkflowInstance`, which keeps each change as a `WorkflowIntervention` (decided 29 September, writers pass).","required":["id","workflowDefinitionId","workflowVersionId","sourceModule","status","correlationId","startedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"workflowDefinitionId":{"type":"string","format":"uuid"},"workflowVersionId":{"type":"string","format":"uuid","description":"The version the instance started on; never changes"},"workflowTriggerId":{"type":"string","format":"uuid","nullable":true},"sourceModule":{"$ref":"#/components/schemas/WorkflowModule"},"businessObjectType":{"type":"string","maxLength":100,"nullable":true},"businessObjectId":{"type":"string","nullable":true,"description":"**A reference, never a copy**, as `ApprovalRequest.subjectId`"},"initiatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Null when a system event or schedule started it"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"priority":{"type":"string","maxLength":30,"nullable":true},"currentNodeId":{"type":"string","nullable":true,"description":"The node of the version's graph the instance is at"},"status":{"$ref":"#/components/schemas/WorkflowInstanceStatus"},"correlationId":{"type":"string","maxLength":100,"description":"The shared correlation id every participating service logs, for distributed tracing"},"slaPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The `ApprovalSlaPolicy` whose clock runs on this instance"},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean","default":false},"escalationLevel":{"type":"integer","minimum":0,"default":0},"firstReminderAt":{"type":"string","format":"date-time","nullable":true},"secondReminderAt":{"type":"string","format":"date-time","nullable":true},"managerEscalatedAt":{"type":"string","format":"date-time","nullable":true},"executiveEscalatedAt":{"type":"string","format":"date-time","nullable":true},"slaOutcome":{"type":"string","enum":["metWithinTarget","metAfterReminder","metAfterEscalation","breached"],"nullable":true,"description":"How the instance finished against its SLA; set on completion (the monitor's Final Outcome)"},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"The partition key (ADR-0005). Written at venue scope"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WorkflowInstanceActionInput": {"type":"object","x-ticvai-persistence":"none — request only; writes approvals.workflow_intervention (schema WorkflowIntervention) (decided 29 September, writers pass)","description":"One operator action on a running workflow instance (decided 29 September, writers pass).","required":["action","reason"],"properties":{"action":{"$ref":"#/components/schemas/WorkflowInterventionAction"},"reason":{"type":"string","minLength":1,"maxLength":500,"description":"Mandatory for every action (pack 13.2.5, \"actions capture a mandatory reason\")"},"workflowStepExecutionId":{"type":"string","format":"uuid","nullable":true,"description":"The step acted on; for `retryStep` the step to retry from. Defaults to the instance's current step"},"workflowExceptionId":{"type":"string","format":"uuid","nullable":true,"description":"The exception the action is taken from; required for `escalateException`"},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Required for `reassign`, `addBackupApprover` and `escalateException`"},"alternativeNodeId":{"type":"string","nullable":true,"description":"For `skipStep`, the node to continue at instead of the next one (Use Approved Alternative)"},"correctedInput":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `resume`, the corrected input of the failed step (Correct Data)"},"extendByMinutes":{"type":"integer","minimum":1,"maximum":43200,"nullable":true,"description":"Required for `extendSla`"},"priority":{"type":"string","maxLength":30,"nullable":true,"description":"Required for `changePriority`"}}},
"WorkflowInstanceMonitorProcessTimelineView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_instance and approvals.workflow_step_execution (data model for the agreed operations, 29 September)","description":"**What Workflow Instance Monitor & Process Timeline displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowInstance":{"type":"string","description":"Workflow Instance"},"workflowName":{"type":"string","description":"Workflow Name"},"version":{"type":"string","description":"Version"},"sourceModule":{"type":"string","description":"Source Module"},"businessObject":{"type":"string","description":"Business Object"},"initiatedBy":{"type":"string","description":"Initiated By"},"startTime":{"type":"string","format":"date-time","description":"Start Time"},"currentStatus":{"type":"string","enum":["running","waitingApproval","waitingTask","waitingSystem","escalated","failed","completed","cancelled"],"description":"Current Status"},"currentStep":{"type":"string","description":"Current Step"},"sla":{"type":"string","description":"SLA"},"step":{"type":"string","description":"Step"},"type":{"type":"string","description":"Type"},"started":{"type":"string","format":"date-time","description":"Started"},"completed":{"type":"string","format":"date-time","description":"Completed"},"assignedTo":{"type":"string","description":"Assigned To"},"input":{"type":"string","description":"Input"},"output":{"type":"string","description":"Output"},"decision":{"type":"string","description":"Decision"},"duration":{"type":"integer","description":"Seconds"},"status":{"type":"string","description":"Status"},"ruleEvaluations":{"type":"integer","description":"Rule evaluations"},"assignments":{"type":"integer","description":"Assignments"},"approvals":{"type":"integer","description":"Approvals"},"rejections":{"type":"integer","description":"Rejections"},"escalations":{"type":"integer","description":"Escalations"},"notifications":{"type":"integer","description":"Notifications"},"apiCalls":{"type":"integer","description":"API calls"},"systemActions":{"type":"integer","description":"System actions"},"errors":{"type":"integer","description":"Errors"}},"required":["workflowInstance"]},
"WorkflowInstanceStatus": {"type":"string","description":"Where one running workflow stands (pack 13.2.1 and 13.2.3; decided 29 September, readiness close-out). Modelled in `states/workflow-instance.yaml`.","enum":["running","waitingApproval","waitingTask","waitingSystem","escalated","failed","completed","cancelled"]},
"WorkflowInterventionAction": {"type":"string","description":"What an operator did to a running workflow instance (pack 13.2.3, 13.2.4 and 13.2.5; decided 29 September, writers pass). The effect of each is on `actOnWorkflowInstance`.","enum":["reassign","retryStep","skipStep","resume","cancel","extendSla","addBackupApprover","changePriority","escalateException"]},
"WorkflowModule": {"type":"string","description":"The module a workflow, rule or automation belongs to and a workflow instance originates from. The same values as `WorkflowOperationsCommandCenterView.module` (decided 29 September, readiness close-out), named so the workflow engine's tables share one vocabulary (data model for the agreed operations, 29 September).","enum":["ticketing","pricing","finance","procurement","crm","resourceManagement","fnb","retail","groupSales","customerService","membership","wallet","waiver","subscriptionLicensing"]},
"WorkflowOperationsCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_instance (schema WorkflowInstance) (data model for the agreed operations, 29 September)","description":"**What Workflow Operations Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowInstanceId":{"type":"string","description":"Workflow Instance ID"},"workflow":{"type":"string","description":"Workflow"},"module":{"type":"string","enum":["ticketing","pricing","finance","procurement","crm","resourceManagement","fnb","retail","groupSales","customerService","membership","wallet","waiver","subscriptionLicensing"],"description":"Module the workflow originates from"},"businessObject":{"type":"string","description":"Business Object"},"initiatedBy":{"type":"string","description":"Initiated By"},"started":{"type":"string","format":"date-time","description":"Started"},"currentStep":{"type":"string","description":"Current Step"},"owner":{"type":"string","description":"Owner"},"priority":{"type":"string","description":"Priority"},"sla":{"type":"string","description":"SLA"},"status":{"type":"string","enum":["running","waitingApproval","waitingTask","waitingSystem","escalated","failed","completed","cancelled"],"description":"Status"}},"required":["workflowInstanceId"]},
"WorkflowOperationsCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"workflowsRunning":{"type":"integer","description":"Workflows Running"},"startedToday":{"type":"integer","description":"Started Today"},"completedToday":{"type":"integer","description":"Completed Today"},"pendingApprovals":{"type":"integer","description":"Pending Approvals"},"waitingTasks":{"type":"integer","description":"Waiting Tasks"},"slaAtRisk":{"type":"integer","description":"SLA At Risk"},"slaBreached":{"type":"integer","description":"SLA Breached"},"failedWorkflows":{"type":"integer","description":"Failed Workflows"},"escalated":{"type":"integer","description":"Escalated"},"automatedExecutions":{"type":"integer","description":"Automated Executions"},"averageCompletionTime":{"type":"integer","description":"Minutes"},"automationSuccessRate":{"type":"number","description":"Automation Success Rate"}}}
}
```
