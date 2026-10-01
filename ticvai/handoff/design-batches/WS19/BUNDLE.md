# WS19 — Approval Workflows and Governance board 7

**10 screens · 13 operations · 19 schemas · 6 permissions**

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

- **Every control that can be refused must be gated.** 6 permissions apply here:
  `APPROVAL_CONFIGURE, APPROVAL_VIEW, DEVELOPER_MANAGE, DEVELOPER_VIEW, PERMISSION_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `ADM-349` | Approval Integration Command Center | B–D | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |
| `ADM-350` | Module Integration Registry | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-351` | Approval API Management | B–D | 9 | 0 | 5 | 7 | 0 | 3 | — | notStarted (—) |
| `ADM-352` | Workflow Event Framework | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-353` | Webhook Configuration & Subscription Manager | B–D | 5 | 0 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-354` | External Workflow System Integration | A | 8 | 0 | 5 | 1 | 1 | 0 | — | notStarted (—) |
| `ADM-355` | Data & Workflow Mapping Studio | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-356` | Integration Security & Access Control | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-357` | Integration Monitoring, Error & Retry Center | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-358` | Integration Analytics & AI Health Advisor | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-350, ADM-352, ADM-355, ADM-356, ADM-357, ADM-358 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-349` Approval Integration Command Center

**Provide administrators and technical teams with a centralized overview of all systems connected to the Approval Engine.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-integration-command-center-adm-349` |

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Correlation | text field | — | — | `listCrossModuleOrchestration` ?correlationId |
| Status | text field | — | — | `listCrossModuleOrchestration` ?status |
| Status | segmented control | — | Active · Paused · Disabled | `listApprovalExternalProviders` ?status |
| Provider | picker: choose a provider | — | — | `listApprovalExternalDispatches` ?providerId |
| Request | picker: choose a request | — | — | `listApprovalExternalDispatches` ?requestId |
| Status | select | — | Pending · Sent · Failed · Decided · Timed out · Cancelled | `listApprovalExternalDispatches` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Connected TICVAI Modules** (metric tile)

**External Integrations** (metric tile)

**API Requests Today** (metric tile)

**Workflow Events** (metric tile)

**Active Webhooks** (metric tile)

**Failed Requests** (metric tile)

**Integration Errors** (metric tile)

**Average Response Time** (metric tile)

**Data it reads**: `listCrossModuleOrchestration` (onLoad, Which modules raise approvals); `listApprovalExternalProviders` (onLoad, External providers and their health); `listApprovalExternalDispatches` (onLoad, Levels waiting on or failed in external systems)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-358` Integration Analytics & AI Health Advisor: *Integration Analytics & AI Health Advisor*
- → `ADM-350` Module Integration Registry: *Module Integration Registry*
- → `ADM-351` Approval API Management: *Approval API Management*
- → `ADM-352` Workflow Event Framework: *Workflow Event Framework*
- → `ADM-353` Webhook Configuration & Subscription Manager: *Webhook Configuration & Subscription Manager*
- → `ADM-354` External Workflow System Integration: *External Workflow System Integration*
- → `ADM-355` Data & Workflow Mapping Studio: *Data & Workflow Mapping Studio*
- → `ADM-356` Integration Security & Access Control: *Integration Security & Access Control*
- → `ADM-357` Integration Monitoring, Error & Retry Center: *Integration Monitoring, Error & Retry Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval integration list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval integration untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval integration yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listCrossModuleOrchestration` → `APPROVAL_VIEW` (read) · staff
- `listApprovalExternalProviders` → `APPROVAL_VIEW` (read) · staff
- `listApprovalExternalDispatches` → `APPROVAL_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-349` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-349`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 1: Opens Approval Integration Command Center → Provide administrators and technical teams with a centralized overview of all systems connected to the Approval Engine.
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F129 branch at step 1 (expected): when Nothing has been set up on Approval Integration Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F129 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-349?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-358`, `ADM-350`, `ADM-351`, `ADM-352`, `ADM-353`, `ADM-354`, `ADM-355`, `ADM-356`, `ADM-357`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-350` Module Integration Registry

**Define which TICVAI modules are allowed to initiate and consume approval workflows.**

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
| Route | `/platform/module-integration-registry-adm-350` |

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

**Data it reads**: `listCrossModuleOrchestration` (onLoad, The integration registry)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The module integration registry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the module integration registry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No module integration registry yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the module integration registry are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-350` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-350`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 2: Works in Module Integration Registry → Define which TICVAI modules are allowed to initiate and consume approval workflows.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-350?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-351` Approval API Management

**Configure and monitor APIs used to create, retrieve and process approval requests. The matrix explicitly requires approval workflows to be exposed through APIs.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§API Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-api-management-adm-351` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Endpoint | select field | — | — | — | — | — | — |
| API version | select field | — | — | — | — | — | — |
| Authentication | select field | — | — | — | — | — | — |
| tenant context | select field | — | — | — | — | — | — |
| request schema | select field | — | — | — | — | — | — |
| response schema | select field | — | — | — | — | — | — |
| timeout | select field | — | — | — | — | — | — |
| retry policy | select field | — | — | — | — | — | — |
| rate limit | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

#### Outputs: what the screen shows and produces

**Data it reads**: `listApprovalRequests` (onLoad, What the API exposes)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval api configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval api untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval api configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-351` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-351`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 4: Works in Approval API Management → Configure and monitor APIs used to create, retrieve and process approval requests. The matrix explicitly requires approval workflows to be exposed through APIs.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-351?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-352` Workflow Event Framework

**Configure the business events published by the Approval Engine. The matrix requires workflow events to be published through the platform event framework.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE`, `DEVELOPER_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-event-framework-adm-352` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Publisher | text field | — | — | `listWebhookEventTypes` ?publisher |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save trigger action cross (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listWebhookEventTypes` (onLoad, Workflow events published through the event framework …)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow event framework list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow event framework untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow event framework yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow event framework are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setTriggerActionCross` → `APPROVAL_CONFIGURE` (configure) · staff
- `listWebhookEventTypes` → `DEVELOPER_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-352` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-352`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 6: Works in Workflow Event Framework → Configure the business events published by the Approval Engine. The matrix requires workflow events to be published through the platform event framework.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-352?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save trigger action cross, Cancel.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `DEVELOPER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-353` Webhook Configuration & Subscription Manager

**Allow external or internal systems to subscribe to approval events. The source explicitly requires webhook notifications for approval events.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW` (1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Delivery Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/webhook-configuration-subscription-manager-adm-353` |

**Known gaps.** **Webhook Configuration & Subscription Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Timeout | select field | — | — | — | — | — | — |
| Retry count | select field | — | — | — | — | — | — |
| Retry interval | select field | — | — | — | — | — | — |
| failure action | select field | — | — | — | — | — | — |
| disable threshold | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Publisher | text field | — | — | `listWebhookEventTypes` ?publisher |
| Client | picker: choose a client | — | — | `listWebhookSubscriptions` ?clientId |

#### Outputs: what the screen shows and produces

**Data it reads**: `listWebhookEventTypes` (onLoad, Events a subscription can take); `listWebhookSubscriptions` (onLoad, Existing subscriptions)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The webhook subscription configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the webhook subscription untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No webhook subscription configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 An entry in `eventTypes` is not in the webhook event catalogue. |

#### Permissions

- `createWebhookSubscription` → `DEVELOPER_MANAGE` (configure) · staff, partner
- `listWebhookEventTypes` → `DEVELOPER_VIEW` (read) · staff, partner
- `listWebhookSubscriptions` → `DEVELOPER_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-353` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-353`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 8: Works in Webhook Configuration & Subscription Manager → Allow external or internal systems to subscribe to approval events. The source explicitly requires webhook notifications for approval events.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-353?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-354` External Workflow System Integration

**Allow TICVAI to integrate with third-party workflow/governance platforms when a client already operates an enterprise approval environment. The matrix specifically requires integration with third-party workflow systems.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block A · ticket #20610 (APP-SETUP-ADM-354) |
| Who uses it | ticvai staff holding `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`, `DEVELOPER_VIEW` (1 configure, 2 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/external-workflow-system-integration-adm-354` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| System name | select field | — | — | — | — | — | — |
| integration direction | select field | — | — | — | — | — | — |
| authentication | select field | — | — | — | — | — | — |
| workflow mapping | select field | — | — | — | — | — | — |
| user/role mapping | select field | — | — | — | — | — | — |
| status mapping | select field | — | — | — | — | — | — |
| error handling | select field | — | — | — | — | — | — |
| synchronization mode | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | segmented control | — | Active · Paused · Disabled | `listApprovalExternalProviders` ?status |

#### Outputs: what the screen shows and produces

**Data it reads**: `listApiClients` (onLoad, External workflow systems); `listApprovalExternalProviders` (onLoad, Registered external workflow systems)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The external workflow system configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the external workflow system untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No external workflow system configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The endpoint is not `https`, the API client is not an active client of the tenant, or the decision mapping has no value for `approve` or for `reject` |

#### Permissions

- `listApiClients` → `DEVELOPER_VIEW` (read) · staff, partner
- `listApprovalExternalProviders` → `APPROVAL_VIEW` (read) · staff
- `setApprovalExternalProvider` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.65 | External Workflow Integration - System shall support integration with third-party workflow systems. | Approval Workflows & Governance | CONTRACTED | `setApprovalExternalProvider` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-354` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-354`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 10: Works in External Workflow System Integration → Allow TICVAI to integrate with third-party workflow/governance platforms when a client already operates an enterprise approval environment. The matrix specifically requires integration with …

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-354?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`, `DEVELOPER_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-355` Data & Workflow Mapping Studio

**Map external system data to TICVAI's approval data model without requiring custom development for every integration.**

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
| Route | `/platform/data-workflow-mapping-studio-adm-355` |

**Known gaps.** **Data & Workflow Mapping Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save trigger action cross (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The data workflow mapping list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the data workflow mapping untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No data workflow mapping yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the data workflow mapping are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setTriggerActionCross` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-355` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-355`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 12: Works in Data & Workflow Mapping Studio → Map external system data to TICVAI's approval data model without requiring custom development for every integration.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-355?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save trigger action cross, Cancel.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-356` Integration Security & Access Control

**Govern which applications and external systems can access the Approval Engine.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PERMISSION_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/integration-security-access-control-adm-356` |

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

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** ☑ Create Approval Request, ☑ Read Status, ☑ Read History, ☐ Submit Approval Decision, ☐ Modify Workflow. Each needs attaching to the control it gates, or the screen needs the control.

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listAuthorisationPolicies` (onLoad, Integration access control)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration security access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration security access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration security access yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration security access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAuthorisationPolicies` → `PERMISSION_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-356` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-356`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 14: Works in Integration Security & Access Control → Govern which applications and external systems can access the Approval Engine.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-356?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `PERMISSION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-357` Integration Monitoring, Error & Retry Center

**Provide technical teams with real-time monitoring of integration failures.**

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
| Route | `/platform/integration-monitoring-error-retry-center-adm-357` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Error type | text field | — | — | `listWorkflowExceptionFailure` ?errorType |
| Module | text field | — | — | `listWorkflowExceptionFailure` ?module |
| Priority | text field | — | — | `listWorkflowExceptionFailure` ?priority |
| Provider | picker: choose a provider | — | — | `listApprovalExternalDispatches` ?providerId |
| Request | picker: choose a request | — | — | `listApprovalExternalDispatches` ?requestId |
| Status | select | — | Pending · Sent · Failed · Decided · Timed out · Cancelled | `listApprovalExternalDispatches` ?status |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listWorkflowExceptionFailure` (onLoad, Errors and retries); `listApprovalExternalDispatches` (onLoad, External dispatch errors and retries)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration monitoring error list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration monitoring error untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration monitoring error yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration monitoring error are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listWorkflowExceptionFailure` → `APPROVAL_VIEW` (read) · staff
- `listApprovalExternalDispatches` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-357` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-357`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 16: Works in Integration Monitoring, Error & Retry Center → Provide technical teams with real-time monitoring of integration failures.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-357?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-358` Integration Analytics & AI Health Advisor

**Provide technical and business teams with analytics on Approval Engine integration performance.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/integration-analytics-ai-health-advisor-adm-358` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

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

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listWorkflowProcessPerformance` (onLoad, Integration health)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration analytics health list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration analytics health untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration analytics health yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration analytics health are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-358` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-358`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 18: Works in Integration Analytics & AI Health Advisor → Provide technical and business teams with analytics on Approval Engine integration performance.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-358?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `REPORT_VIEW_VENUE`.
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createWebhookSubscription": {"method":"POST","path":"/webhook-subscriptions","contract":"public-api","summary":"Subscribe to business events","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WebhookSubscription","responds":"WebhookSubscription"},
"listApiClients": {"method":"GET","path":"/api-clients","contract":"public-api","summary":"Registered clients for this developer","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApiClient"},
"listApprovalExternalDispatches": {"method":"GET","path":"/approval-external-dispatches","contract":"approvals","summary":"What was sent to external workflow systems, and what came back","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"providerId","in":"query","required":false},{"name":"requestId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listApprovalExternalProviders": {"method":"GET","path":"/approval-external-providers","contract":"approvals","summary":"The external workflow systems approval levels may be sent to","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listApprovalRequests": {"method":"GET","path":"/approval-requests","contract":"approvals","summary":"Requests awaiting a decision, or already decided","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToMe","in":"query","required":null},{"name":"raisedByMe","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"breachingWithinMinutes","in":"query","required":null},{"name":"sort","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuthorisationPolicies": {"method":"GET","path":"/authorisation-policies","contract":"identity","summary":"Attribute-based authorisation policies","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"scopePath","in":"query","required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"listCrossModuleOrchestration": {"method":"GET","path":"/cross-module-orchestration","contract":"approvals","summary":"Cross-Module Orchestration Monitor","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"correlationId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWebhookEventTypes": {"method":"GET","path":"/webhook-event-types","contract":"public-api","summary":"The events a webhook may subscribe to","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"publisher","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWebhookSubscriptions": {"method":"GET","path":"/webhook-subscriptions","contract":"public-api","summary":"The tenant's webhook subscriptions, filterable by API client","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"clientId","in":"query","required":false}],"requestBody":null,"responds":"WebhookSubscription"},
"listWorkflowExceptionFailure": {"method":"GET","path":"/workflow-exception-failure","contract":"approvals","summary":"Workflow Exception, Failure & Recovery Center","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"errorType","in":"query","required":false},{"name":"module","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkflowProcessPerformance": {"method":"GET","path":"/workflow-process-performance","contract":"approvals","summary":"Workflow Analytics & Process Performance","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workflow","in":"query","required":false},{"name":"module","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"brand","in":"query","required":false},{"name":"businessProcess","in":"query","required":false},{"name":"department","in":"query","required":false},{"name":"approver","in":"query","required":false},{"name":"user","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"minTransactionValue","in":"query","required":false},{"name":"maxTransactionValue","in":"query","required":false}],"requestBody":null,"responds":"WorkflowAnalyticsProcessPerformanceView"},
"setApprovalExternalProvider": {"method":"PUT","path":"/approval-external-providers","contract":"approvals","summary":"Register a third-party workflow system as an approver","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalExternalProvider","responds":"ApprovalExternalProvider"},
"setTriggerActionCross": {"method":"PUT","path":"/trigger-action-cross","contract":"approvals","summary":"Trigger, Action & Cross-Module Orchestration Configuration","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TriggerActionCrossModuleOrchestrationConfigurationInput","responds":"TriggerActionCrossModuleOrchestrationConfigurationView"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessCondition": {"type":"object","description":"**One attribute, one operator, one value** — and the attribute names are an enum rather than free text, because a policy that reads `venu.type` silently never matches.\nThe enum is the matrix, row by row: user (3.3.7), employee (3.3.8), membership (3.3.9), accreditation (3.3.10), customer segment (3.3.11), resource classification (3.3.12), venue (3.3.13), attraction (3.3.14), device (3.3.15), day of week (3.3.16), season (3.3.17), event (3.3.18), capacity (3.3.19), occupancy (3.3.20), risk score (3.3.21), location (3.3.2) and time (3.3.3).\n","required":["attribute","operator"],"properties":{"attribute":{"type":"string","enum":["user.attribute","employee.attribute","employee.onShift","membership.tier","membership.status","accreditation.type","accreditation.status","customer.segment","resource.classification","venue.attribute","venue.id","attraction.attribute","device.kind","device.id","device.trusted","time.ofDay","time.dayOfWeek","time.season","time.withinOperatingHours","event.id","event.status","capacity.utilisationPercent","occupancy.level","risk.score","ticket.status","location.scopePath"]},"key":{"type":"string","nullable":true,"description":"For the `*.attribute` forms — which attribute, by code."},"operator":{"type":"string","enum":["equals","notEquals","in","notIn","greaterThan","lessThan","between","contains","startsWith","exists"]},"value":{"nullable":true,"description":"The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by the attribute. Null for `exists`; `in`, `notIn` and `between` use `values`.\n"},"values":{"type":"array","items":{"type":"string"}}}},
"ApiClient": {"type":"object","x-ticvai-persistence":"control.api_client","description":"CF-135a. **The one credential model.** 2.7.52, 7.1.25 and 7.1.30 each asserted their own, so a partner API key, a POS integration credential and a webstore credential were three unrelated things with three lifecycles.\n","required":["id","developerId","name","environment","scopes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"developerId":{"type":"string","format":"uuid"},"name":{"type":"string"},"clientId":{"type":"string","readOnly":true},"environment":{"type":"string","enum":["sandbox","production"],"description":"**Bound to one, stated on the object rather than by naming convention.** A key that works in both is a key somebody will use in the wrong one.\n"},"scopes":{"type":"array","description":"**Resolved against the tenant's licence at token issue** (13.3.24). A scope granted here and not licensed there produces no token — and the refusal is at issue rather than at call time, so an integrator finds out in testing. **Module scopes** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, one of `listApiScopes`.\n","items":{"type":"string","pattern":"^[a-zA-Z]+\\.(read|write)$"}},"issuedBy":{"type":"string","enum":["partner","ticvai"],"readOnly":true,"description":"Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`.\n"},"certificationListingId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"control.integration_listing","description":"For a production client, the certified integration it was issued against."},"credentialTtlDays":{"type":"integer","minimum":1,"maximum":730,"nullable":true,"description":"Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry)."},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the key stops working unless rotated. No token is issued after it."},"allowedTenantIds":{"type":"array","description":"13.1.46. **Which tenants this client may act for.** A developer integrating for one venue must not reach another, and a client with an empty list reaches none.\n","items":{"type":"string","format":"uuid"}},"ipAllowList":{"type":"array","description":"13.1.38. **Required on a production client** (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the internet); optional in the sandbox. CIDR ranges. Checked at token issue and on every call.\n","items":{"type":"string"}},"status":{"type":"string","enum":["active","suspended","revoked"],"readOnly":true},"lastUsedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"**A credential unused for a year is a credential nobody will notice being stolen.**\n"}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalExternalDispatch": {"type":"object","x-ticvai-persistence":"approvals.external_dispatch","description":"11.1.65 (29 September, build pass). **One request level sent to an external workflow system**, and what became of it. Written by the platform when a level that names a provider is reached, and closed by `recordExternalApprovalDecision` or by the timeout.\n","required":["id","requestId","providerId","level","status"],"properties":{"id":{"type":"string","format":"uuid"},"requestId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid"},"level":{"type":"integer"},"status":{"type":"string","enum":["pending","sent","failed","decided","timedOut","cancelled"]},"attemptCount":{"type":"integer","default":0},"externalReference":{"type":"string","nullable":true,"description":"The provider's own id for the item, as it acknowledged or called back with."},"lastResponseCode":{"type":"integer","nullable":true},"lastError":{"type":"string","nullable":true},"sentAt":{"type":"string","format":"date-time","nullable":true},"answeredAt":{"type":"string","format":"date-time","nullable":true},"externalOutcome":{"type":"string","nullable":true,"description":"The provider's own outcome value, before mapping."},"externalApproverRef":{"type":"string","nullable":true,"description":"Who decided in the provider's system, as it named them."},"scopePath":{"type":"string"}}},
"ApprovalExternalProvider": {"type":"object","x-ticvai-persistence":"approvals.external_provider","description":"11.1.65 (29 September, build pass). **A third-party workflow system registered to decide approval levels**: where TICVAI sends a request, how its fields are mapped, how the answer comes back and what happens when it does not.\n","required":["code","name","endpointUrl","apiClientId","decisionMapping"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","x-ticvai-unique":"tenant","description":"The provider's stable name, and the key `setApprovalExternalProvider` upserts on."},"name":{"type":"string"},"endpointUrl":{"type":"string","description":"`https` only. Where a request level is sent."},"outboundAuth":{"type":"string","enum":["bearerToken","basic","oauthClientCredentials","mutualTls"],"default":"oauthClientCredentials"},"outboundCredential":{"type":"string","format":"password","writeOnly":true,"nullable":true,"description":"The credential TICVAI presents to the provider. Write-only, never returned, kept on a replace that omits it."},"signingSecret":{"type":"string","format":"password","writeOnly":true,"nullable":true,"description":"Signs every request TICVAI sends, as webhook deliveries are signed, so the provider can tell it came from TICVAI. Write-only.\n"},"apiClientId":{"type":"string","format":"uuid","description":"The public-api client the provider calls back as. It must hold `APPROVAL_DECIDE`; `recordExternalApprovalDecision` from any other client is refused.\n"},"requestMapping":{"type":"array","description":"Which request fields go to the provider, under which names. **Only mapped fields leave TICVAI** — a provider receives the amount and the subject it needs, not the whole request.\n","items":{"type":"object","required":["from","to"],"properties":{"from":{"type":"string","description":"A field of `ApprovalRequest`, e.g. `amount`, `kind`, `subjectId`, `requestedByPrincipalId`."},"to":{"type":"string","description":"The provider's field name."}}}},"decisionMapping":{"type":"array","minItems":2,"description":"The provider's outcome values and the decision each means. At least one maps to `approve` and one to `reject`.","items":{"type":"object","required":["externalValue","decision"],"properties":{"externalValue":{"type":"string"},"decision":{"type":"string","enum":["approve","reject","return","requestInformation"]}}}},"timeoutMinutes":{"type":"integer","default":1440,"description":"How long a level waits for the provider before `onTimeout` applies."},"onTimeout":{"type":"string","enum":["fallBackToRoles","escalate","reject"],"default":"fallBackToRoles"},"maxAttempts":{"type":"integer","default":5,"description":"Delivery attempts, with backoff, before a dispatch is `failed` and the level falls back as on timeout."},"status":{"type":"string","enum":["active","paused","disabled"],"default":"active","description":"`paused` sends nothing and every level that names it falls back at once; the platform sets `disabled` after repeated failures, as it disables a failing webhook.\n"},"lastSuccessAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"AuthorisationPolicy": {"type":"object","x-ticvai-persistence":"identity.authorisation_policy","description":"3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here).\n**Settled by ADR-0068 (accepted 1 October): guest admission lives in Access only.** This engine keeps staff authorisation and was renamed to say so: `identity.access_policy` became `identity.authorisation_policy`, its versions `identity.authorisation_policy_version`, and its operations `*AuthorisationPolicy*`. \"Access policy\" now means `AccessDynamicPolicy` and nothing else.\n","required":["code","name","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on `createAuthorisationPolicy`; the path names the policy on update."},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"isTemplate":{"type":"boolean","default":false},"permissions":{"type":"array","items":{"type":"string"},"description":"**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"},"conditions":{"type":"array","items":{"$ref":"#/components/schemas/AccessCondition"}},"combining":{"type":"string","enum":["allMustMatch","anyMayMatch"],"default":"allMustMatch"},"effect":{"type":"string","enum":["permit","deny"],"description":"**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"},"priority":{"type":"integer","default":0},"scopePath":{"type":"string","description":"3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"},"appliesToRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"status":{"type":"string","readOnly":true,"description":"**Moved only by `setAuthorisationPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n","enum":["draft","pendingApproval","active","suspended","retired"]},"version":{"type":"integer","default":1,"readOnly":true,"description":"Set by the server; every `updateAuthorisationPolicy` writes a new version."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"delegatedAdminRoleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"}}},
"CrossModuleOrchestrationMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_step_execution joined to approvals.workflow_instance by correlation id (data model for the agreed operations, 29 September)","description":"**What Cross-Module Orchestration Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"service":{"type":"string","description":"Service"},"action":{"type":"string","description":"Action"},"status":{"type":"string","enum":["notStarted","running","waiting","successful","failed","compensated"],"description":"Status"},"started":{"type":"string","format":"date-time","description":"Started"},"completed":{"type":"string","format":"date-time","description":"Completed"},"duration":{"type":"integer","description":"Seconds"},"inputOutput":{"type":"string","description":"Input/Output"},"failureHandling":{"type":"string","enum":["waits","retries","rollsBack","continuesPartially","requiresHumanIntervention"],"description":"What the workflow does after this node fails"},"retries":{"type":"integer","description":"Retries"},"correlationId":{"type":"string","description":"a common correlation/workflow ID"}},"required":["correlationId","service"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"TriggerActionCrossModuleOrchestrationConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.workflow_trigger (schema WorkflowTrigger) (data model for the agreed operations, 29 September)","description":"**What Trigger, Action & Cross-Module Orchestration Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"triggerType":{"type":"string","enum":["event","dataCondition","schedule","manual"],"description":"What starts the workflow"},"workflowId":{"type":"string","description":"Workflow this trigger and action set belongs to"},"allowedActions":{"type":"array","items":{"type":"string","enum":["createApproval","createTask","updateStatus","applyHold","releaseHold","createNotification","generateDocument","executeRefund","updateAllocation","activateMembership","suspendPartner","callApprovedApi","callApprovedService","startSubWorkflow"]},"description":"Actions this workflow may call"},"onFailure":{"type":"string","enum":["retry","rollback","compensate","exceptionQueue","humanIntervention"],"description":"What happens when an action fails"},"triggerDefinition":{"type":"string","description":"Event name, data condition (e.g. Balance > Limit) or schedule"},"maxRetries":{"type":"integer","description":"Retries before the failure handling applies"}},"required":["workflowId","triggerType"]},
"TriggerActionCrossModuleOrchestrationConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_trigger (schema WorkflowTrigger) (data model for the agreed operations, 29 September)","description":"**What Trigger, Action & Cross-Module Orchestration Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"triggerType":{"type":"string","enum":["event","dataCondition","schedule","manual"],"description":"What starts the workflow"},"workflowId":{"type":"string","description":"Workflow this trigger and action set belongs to"},"allowedActions":{"type":"array","items":{"type":"string","enum":["createApproval","createTask","updateStatus","applyHold","releaseHold","createNotification","generateDocument","executeRefund","updateAllocation","activateMembership","suspendPartner","callApprovedApi","callApprovedService","startSubWorkflow"]},"description":"Actions this workflow may call"},"onFailure":{"type":"string","enum":["retry","rollback","compensate","exceptionQueue","humanIntervention"],"description":"What happens when an action fails"},"triggerDefinition":{"type":"string","description":"Event name, data condition (e.g. Balance > Limit) or schedule"},"maxRetries":{"type":"integer","description":"Retries before the failure handling applies"}},"required":["workflowId","triggerType"]},
"WebhookEventCatalogueEntry": {"type":"object","x-ticvai-persistence":"none — read from the event catalogue (events/*.yaml) shipped with the release","description":"One event a webhook may subscribe to, as the event catalogue declares it. What a receiver needs to write a handler: the name, the version in the payload, who publishes it, what it is about and when, and the payload fields.\n","required":["name","version","publisher"],"properties":{"name":{"$ref":"#/components/schemas/WebhookEventType"},"version":{"type":"integer","minimum":1},"publisher":{"type":"string","description":"The one context that publishes it."},"aggregate":{"type":"string","description":"What the event is about. Delivery is ordered within one instance of it."},"description":{"type":"string"},"emittedWhen":{"type":"string","nullable":true},"payload":{"type":"array","items":{"type":"object","required":["field","type"],"properties":{"field":{"type":"string"},"type":{"type":"string"},"required":{"type":"boolean","default":true},"notes":{"type":"string","nullable":true}}}}}},
"WebhookEventType": {"type":"string","description":"**The webhook event catalogue: every event a subscription may name** (29 September, build pass). Each value is the `name` of an event in `events/` — `aggregate.pastTenseFact`, published through `platform.outbox` by exactly one context. A name is added here in the same change that adds its event file, and never before.\n**Added 29 September**, each closing a requirement that had the webhook mechanism and nothing to subscribe to:\n| Events | Publisher | Requirement | |---|---|---| | `device.statusChanged`, `device.tamperDetected`, `device.enrolmentChanged`, `device.firmwareReleased`, `device.firmwareRolloutCompleted` | tenancy | 16.9.56 | | `accreditation.applicationDecided`, `accreditation.holderStatusChanged`, `accreditation.credentialIssued`, `accreditation.renewalDue` | accreditation | 12.1.53 | | `approval.requested`, `approval.escalated`, `approval.stepCompleted`, `approval.expired` | approvals | 11.1.64, 11.1.66 | | `seat.held`, `seat.released`, `seat.blocked`, `seatMap.published` | seating | 21.13.4 | | `consent.deviceConsentRecorded`, `consent.deviceConsentClaimed` | marketing | 2.6.65 | | `order.chargebackRecorded` | orders | 8.3.11 to 8.3.15 (a tenant's own finance or fraud tooling) | | `entitlement.expiringSoon` | access | 5.5.30 (a tenant's own CRM) | | `apiClient.anomalyDetected` | public-api | 17 September minutes M17-07 (added 30 September with its event file) |\n**Deprecated** (1 October, ADR-0067 amendment): `device.enrolmentChanged` is still offered but nothing inside the platform consumes it any more; it is removed at the next major version of this API. Subscribers are told in the release note.\n**Published and deliberately not offered** (29 September, build pass, group G2): `identity.credentialResetRequested` and `identity.loginRecorded` are security signals, and a stream of them to an outside receiver is a map of which accounts are under attack; `storefront.sessionEvent` is high-volume fraud telemetry, not a business fact a receiver acts on.\n","x-ticvai-deprecated-values":["device.enrolmentChanged"],"enum":["access.validated","accreditation.applicationDecided","accreditation.credentialIssued","accreditation.holderStatusChanged","accreditation.renewalDue","ai.ceilingApproaching","apiClient.anomalyDetected","approval.escalated","approval.expired","approval.granted","approval.rejected","approval.requested","approval.stepCompleted","assets.documentIndexed","cart.abandoned","catalogue.productPublished","consent.deviceConsentClaimed","consent.deviceConsentRecorded","conversation.handedOver","device.enrolmentChanged","device.firmwareReleased","device.firmwareRolloutCompleted","device.statusChanged","device.tamperDetected","entitlement.expiringSoon","entitlement.issued","entitlement.statusChanged","fnb.menuPublished","fnb.orderReady","inventory.purchaseOrderReceived","ledger.journalPosted","ledger.periodClosed","maintenance.assetReturnedToService","maintenance.templatePublished","maintenance.workOrderCompleted","marketing.caseClosed","order.chargebackRecorded","order.completed","order.paid","order.refunded","performance.cancelled","reporting.definitionPublished","retail.merchandisePublished","seat.blocked","seat.held","seat.released","seat.sold","seatMap.published","shift.closed","stock.depleted","tenant.suspended","whitelabel.contentPublished"]},
"WebhookSubscription": {"type":"object","x-ticvai-persistence":"control.webhook_subscription","description":"13.1.26, 13.3.18 and 13.3.22. **The 29 events already exist and nothing outside could receive one.**\n","required":["id","clientId","endpointUrl","eventTypes","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"clientId":{"type":"string","format":"uuid"},"endpointUrl":{"type":"string"},"eventTypes":{"type":"array","description":"**Filtered at subscription, not at delivery.** A subscriber taking every event and discarding 99% is a subscriber the platform pays to talk to. Each entry is a name from the webhook event catalogue (`WebhookEventType`).\n","items":{"$ref":"#/components/schemas/WebhookEventType"}},"filters":{"type":"object","nullable":true,"description":"13.3.22. Tenant, venue, or a business condition on the payload.","additionalProperties":true},"signingSecret":{"type":"string","format":"password","writeOnly":true,"description":"**How the receiver knows it was TICVAI.** Without a signature an endpoint accepts a ticket-sale event from anybody who learns the URL.\n**Write-only: accepted on create, never returned.** The same rule as `clientSecret` — a system that can show you a secret later is a system that hands it to whoever reads the subscription.\n"},"status":{"type":"string","enum":["pendingVerification","active","paused","failing","disabled"],"readOnly":true},"consecutiveFailures":{"type":"integer","readOnly":true},"disabledReason":{"type":"string","nullable":true,"readOnly":true,"description":"13.1.29. **An endpoint failing for days is disabled rather than retried forever**, and the developer is told — a queue growing against a dead endpoint is a cost the platform carries silently.\n"}}},
"WorkflowAnalyticsProcessPerformanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — aggregated from approvals.workflow_instance, workflow_step_execution, automation_execution, request, decision and escalation (data model for the agreed operations, 29 September)","description":"**What Workflow Analytics & Process Performance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowVolume":{"type":"integer","description":"Workflow Volume"},"completionRate":{"type":"number","description":"Completion Rate"},"failureRate":{"type":"number","description":"Failure Rate"},"averageCompletionTime":{"type":"integer","description":"Minutes"},"approvalTime":{"type":"integer","description":"Minutes"},"automationRate":{"type":"number","description":"Automation Rate"},"escalationRate":{"type":"number","description":"Escalation Rate"},"rejectionRate":{"type":"number","description":"Rejection Rate"},"reworkRate":{"type":"number","description":"Rework Rate"},"slaCompliance":{"type":"number","description":"Percent within SLA"},"averageApprovalTime":{"type":"integer","description":"Minutes"},"approvalRate":{"type":"number","description":"Approval Rate"},"requestChangesRate":{"type":"number","description":"Request Changes Rate"},"delegationRate":{"type":"number","description":"Delegation Rate"},"manualStepsRemoved":{"type":"integer","description":"Manual Steps Removed"},"processingTimeSaved":{"type":"integer","description":"Minutes"},"workloadReduced":{"type":"number","description":"Staff hours"},"costSavingWhereMeasurable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost Saving where measurable"}}},
"WorkflowExceptionFailureRecoveryCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_exception (schema WorkflowException) (data model for the agreed operations, 29 September)","description":"**What Workflow Exception, Failure & Recovery Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"errorType":{"type":"string","enum":["businessRuleFailure","missingData","missingApprover","permissionFailure","integrationFailure","timeout","actionFailure","invalidState","duplicateEvent","serviceUnavailable","configurationError"],"description":"Kind of failure"},"exceptionId":{"type":"string","description":"Exception ID"},"workflow":{"type":"string","description":"Workflow"},"instance":{"type":"string","description":"Instance"},"module":{"type":"string","description":"Module"},"failedStep":{"type":"string","description":"Step that failed"},"time":{"type":"string","format":"date-time","description":"Time"},"businessImpact":{"type":"string","description":"Business Impact"},"priority":{"type":"string","description":"Priority"},"owner":{"type":"string","description":"Owner"},"retryCount":{"type":"integer","description":"Retry count"}},"required":["exceptionId"]}
}
```
