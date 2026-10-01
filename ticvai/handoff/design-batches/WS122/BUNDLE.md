# WS122 — AI Governance board 2

**10 screens · 25 operations · 34 schemas · 8 permissions**

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

- **Every control that can be refused must be gated.** 8 permissions apply here:
  `AI_APPROVE, AI_AUDIT_VIEW, AI_CONFIGURE, AI_USE, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW`. A control nobody can use must say so,
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
| `ADM-529` | AI Human Oversight Command Center | B–D | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-530` | AI Approval Requirement & Routing Configuration | B–D | 24 | 20 | 6 | 55 | 1 | 3 | — | notStarted (—) |
| `ADM-531` | AI Approval Review Workspace | B–D | 2 | 0 | 6 | 1 | 2 | 3 | — | notStarted (—) |
| `ADM-532` | Conditional Approval & Approval Conditions | B–D | 0 | 60 | 6 | 7 | 2 | 3 | — | notStarted (—) |
| `ADM-533` | Human Review, Challenge & AI Clarification Workspace | B–D | 0 | 16 | 6 | 11 | 1 | 0 | — | notStarted (—) |
| `ADM-534` | Escalation, Delegation & Approval SLA Management | B–D | 25 | 46 | 6 | 4 | 2 | 3 | — | notStarted (—) |
| `ADM-535` | Live AI Execution Oversight & Human Intervention | B–D | 5 | 20 | 6 | 0 | 3 | 0 | — | notStarted (—) |
| `ADM-536` | Human Override & Manual Control Center | A | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-537` | Approval & Intervention History / Decision Timeline | B–D | 2 | 0 | 6 | 4 | 1 | 3 | — | notStarted (—) |
| `ADM-538` | Human Oversight Workflow Simulator & Readiness Center | B–D | 7 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-531, ADM-533, ADM-536, ADM-537 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-529` AI Human Oversight Command Center

**Provide one central operational view of all AI activities requiring human oversight across TICVAI. This should become the control room for AI actions waiting for human intervention.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Header KPIs) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/platform/ai-human-oversight-command-center-adm-529` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search human oversight | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, ai capability, module, risk, approver and 4 more — which are present is a decision the pack already made. | — |

#### Outputs: what the screen shows and produces

**Shown**

**Pending AI Approvals** (metric tile)

**High-Risk Reviews** (metric tile)

**Critical Reviews** (metric tile)

**Awaiting Additional Approver** (metric tile)

**Conditional Approvals** (metric tile)

**Requested Changes** (metric tile)

**Escalated Cases** (metric tile)

**Overdue Reviews** (metric tile)

**Active AI Executions Under Oversight** (metric tile)

**Human Interventions Today** (metric tile)

**Data it reads**: `listProposedActions` (onLoad, What the assistant has proposed and nobody has decided)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-530` AI Approval Requirement & Routing Configuration: *AI Approval Requirement & Routing Configuration*
- → `ADM-531` AI Approval Review Workspace: *AI Approval Review Workspace*; carries `planId`
- → `ADM-532` Conditional Approval & Approval Conditions: *Conditional Approval & Approval Conditions*; carries `planId`
- → `ADM-533` Human Review, Challenge & AI Clarification Workspace: *Human Review, Challenge & AI Clarification Workspace*
- → `ADM-534` Escalation, Delegation & Approval SLA Management: *Escalation, Delegation & Approval SLA Management*; carries `planId`
- → `ADM-535` Live AI Execution Oversight & Human Intervention: *Live AI Execution Oversight & Human Intervention*; carries `planId`
- → `ADM-536` Human Override & Manual Control Center: *Human Override & Manual Control Center*; carries `planId`
- → `ADM-537` Approval & Intervention History / Decision Timeline: *Approval & Intervention History / Decision Timeline*
- → `ADM-538` Human Oversight Workflow Simulator & Readiness Center: *Human Oversight Workflow Simulator & Readiness Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The human oversight list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the human oversight untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No human oversight yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the human oversight are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `listProposedActions` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-529` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-529`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 1: Opens AI Human Oversight Command Center → Provide one central operational view of all AI activities requiring human oversight across TICVAI. This should become the control room for AI actions waiting for human intervention.
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F231 branch at step 1 (expected): when Nothing has been set up on AI Human Oversight Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F231 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-529?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-002`, `ADM-530`, `ADM-531`, `ADM-532`, `ADM-533`, `ADM-534`, `ADM-535`, `ADM-536`, `ADM-537`, `ADM-538`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-530` AI Approval Requirement & Routing Configuration

**Translate Board 1 governance decisions into the correct human approval workflow.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW` (2 configure, 1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-approval-requirement-routing-configuration-adm-530` |

**Known gaps.** **The pack names 11 actions on this screen and the screen declares 0 operations.** Unserved: Single Approval, Sequential Approval, Parallel Approval, Conditional Approval, Risk-Based Approval, → … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Policy | picker: choose a policy | — | — | `listAiGovernancePolicyVersions` ?policyId |
| Status | radio group | — | Draft · Simulated · Published · Superseded | `listAiGovernancePolicyVersions` ?status |
| Kind | select | — | Action · Data · Scope · Autonomy · Approval · Environment | `listAiGovernancePolicyVersions` ?kind |
| Target contract | text field | — | — | `listAiTools` ?targetContract |
| Effect | segmented control | — | Read · Write · Destructive | `listAiTools` ?effect |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |

**Form: Save approval matrix** (modal, opened by *Save approval matrix*; *Save approval matrix* calls `setApprovalMatrix`, *Cancel* sends nothing)

**Collects the matrix for kind `aiRecommendation`** before `setApprovalMatrix` is called: levels, the value range each approver may approve, and the escalation above it. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | — | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. | `setApprovalMatrix` body |
| Scope level `scopeLevel` | segmented control | required | — | Tenant · Region · Venue | — | — | `setApprovalMatrix` body |
| Rules `rules` | repeatable rows | required | — | — | — | — | `setApprovalMatrix` body |
| Order `rules[].order` | number field | required | — | — | — | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about. | `setApprovalMatrix` body |
| Min amount `rules[].minAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setApprovalMatrix` body |
| Max amount `rules[].maxAmount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `setApprovalMatrix` body |
| Risk score above `rules[].riskScoreAbove` | number field | optional | — | — | — | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). | `setApprovalMatrix` body |
| Condition `rules[].condition` | text field | optional | — | — | — | 11.1.13. Evaluated against the attributes the caller supplied. | `setApprovalMatrix` body |
| Approver roles `rules[].approverRoleIds` | multi-picker: choose approver roles | required | — | at least 1 | — | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. | `setApprovalMatrix` body |
| Approver scope level `rules[].approverScopeLevel` | radio group | optional | — | Venue · Department · Region · Tenant | — | 11.1.39. Which organisational level the approver must sit at. | `setApprovalMatrix` body |
| Mode `rules[].mode` | radio group | required | — | Sequential · Parallel · Consensus · Majority | — | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. | `setApprovalMatrix` body |
| Levels `rules[].levels` | number field | optional | 1 | — | — | 11.1.3. Multi-level chains ask each level in turn. | `setApprovalMatrix` body |
| Requires MFA `rules[].requiresMfa` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Requires signature `rules[].requiresSignature` | toggle | optional | off | — | — | — | `setApprovalMatrix` body |
| Sla minutes `rules[].slaMinutes` | number field (minutes) | optional | — | — | — | 11.1.14. Null means no SLA, which is different from a long one. | `setApprovalMatrix` body |
| Escalate after minutes `rules[].escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setApprovalMatrix` body |
| Escalate to roles `rules[].escalateToRoleIds` | multi-picker: choose escalate to roles | optional | — | — | — | Role ids from `identity.listRoles`, as `approverRoleIds`. | `setApprovalMatrix` body |
| Expires after minutes `rules[].expiresAfterMinutes` | number field (minutes) | optional | — | — | — | 11.1.53. An unanswered request eventually stops waiting. | `setApprovalMatrix` body |
| External provider `rules[].externalProviderId` | picker: choose an external provider | optional | — | — | shows names, sends the id | 11.1.65 (29 September). This level is decided in an external workflow system (`ApprovalExternalProvider`) rather than by a person in TICVAI. | `setApprovalMatrix` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `setApprovalMatrix` body |

Errors to draw in the form: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem)

**Sent by *Test a routing*** (`evaluateApprovalRequirement`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | select | required | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | — | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. | `evaluateApprovalRequirement` body |
| Scope path `scopePath` | text field | required | — | — | — | — | `evaluateApprovalRequirement` body |
| Amount `amount` | money field | optional | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `evaluateApprovalRequirement` body |
| Attributes `attributes` | key and value settings | optional | — | — | — | Whatever the conditional rules match on (11.1.13). | `evaluateApprovalRequirement` body |

#### Outputs: what the screen shows and produces

**Shown**

**Approval matrix for AI actions** (data table, from `listApprovalMatrices`): **AI actions route through the shared approval matrix** (18 September minutes, M18-02), kind `aiRecommendation`: an approver is authorised up to a limit and anything above it escalates.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Scope level | chip: Tenant, Region, Venue | — |
| Rules | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Order | 1,234 | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason … |
| Min amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Max amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Risk score above | 1,234.5 | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). |
| Condition | text | 11.1.13. Evaluated against the attributes the caller supplied. |
| Approver roles | list or chips (count when long) | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. |
| Approver scope level | chip: Venue, Department, Region, Tenant | 11.1.39. Which organisational level the approver must sit at. |
| Mode | chip: Sequential, Parallel, Consensus, Majority | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. |
| Levels | 1,234 | 11.1.3. Multi-level chains ask each level in turn. |
| Requires MFA | yes / no (icon or chip) | — |
| Requires signature | yes / no (icon or chip) | — |
| Sla minutes | 1,234 | 11.1.14. Null means no SLA, which is different from a long one. |
| Escalate after minutes | 1,234 | — |
| Escalate to roles | list or chips (count when long) | Role ids from `identity.listRoles`, as `approverRoleIds`. |
| Expires after minutes | 1,234 | 11.1.53. An unanswered request eventually stops waiting. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Single Approval (primary button) | navigation or local | — | — | — | — |
| Sequential Approval (secondary button) | navigation or local | — | — | — | — |
| Parallel Approval (secondary button) | navigation or local | — | — | — | — |
| Conditional Approval (secondary button) | navigation or local | — | — | — | — |
| Risk-Based Approval (secondary button) | navigation or local | — | — | — | — |
| → Commercial Manager (secondary button) | navigation or local | — | — | — | — |
| → Commercial Manager + General Manager (secondary button) | navigation or local | — | — | — | — |
| → Commercial Director + General Manager (secondary button) | navigation or local | — | — | — | — |
| Save approval matrix (primary button) | `setApprovalMatrix` PUT `/approval-matrices` | ApprovalMatrix | ApprovalMatrix | 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which … | opens modal first |
| Test a routing (secondary button) | `evaluateApprovalRequirement` POST `/approval-requests/evaluate` | inline | ApprovalRequirement | — | — |

**Data it reads**: `listAiGovernancePolicyVersions` (onLoad, Governance policies and their versions); `listAiTools` (onLoad, The tool registry); `listApprovalMatrices` (onLoad, The matrices AI actions route through)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval requirement routing list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval requirement routing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval requirement routing yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval requirement routing are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold … (ApprovalMatrixRefusedProblem) |

#### Permissions

- `createAiGovernancePolicyDraft` → `AI_CONFIGURE` (configure) · staff
- `listAiGovernancePolicyVersions` → `AI_USE` (operate) · staff
- `listAiTools` → `AI_USE` (operate) · staff
- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff
- `setApprovalMatrix` → `APPROVAL_CONFIGURE` (configure) · staff
- `evaluateApprovalRequirement` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

55 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 43 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI actions route through the shared approval matrix: the screen shows the approver's limit for the kind and amount and whether the action is within it or must escalate; escalation, delegation and SLA apply as to any approval. *(agreed · MoM 18 Sep 2026, M18-02 · DI-956)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-530` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-530`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 2: Works in AI Approval Requirement & Routing Configuration → Translate Board 1 governance decisions into the correct human approval workflow.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (24), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-530?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Single Approval, Sequential Approval, Parallel Approval, Conditional Approval, Risk-Based Approval, → Commercial Manager, → Commercial Manager + General Manager, → Commercial Director + General Manager, Save approval matrix, Test a routing.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-531` AI Approval Review Workspace

**Give the human approver enough information to make an informed decision without having to navigate across many TICVAI modules. This should be one of the strongest screens in the board.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration Current Proposed) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `actionId` (navigation), `planId` (navigation) |
| Route | `/platform/ai-approval-review-workspace-adm-531` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Adult Weekend Price AED 140 AED 150 | text field | — | — | — | — | — | — |
| Effective Date Current 1 Oct 2026 | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval review configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval review configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).; 409 The plan is executing or finished; simulate a rollback plan instead. |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `simulateActionPlan` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval is not binary: conditional approval lets an approver approve with restrictions, e.g. a commercial manager may approve price increases only up to a ceiling, anything higher escalates. An approver can also challenge a proposal and request evidence or alternatives. *(agreed · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-932)*
- The AI approval review workspace gives the approver everything needed to decide: current vs proposed value, impact, risk and affected objects (e.g. a weekend price increase shown with the channels it publishes to and whether future bookings are affected). *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-931)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-531` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-531`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 4: Works in AI Approval Review Workspace → Give the human approver enough information to make an informed decision without having to navigate across many TICVAI modules. This should be one of the strongest screens in the board.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-531?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-532` Conditional Approval & Approval Conditions

**Allow humans to approve an AI action subject to explicit conditions rather than treating approval as simply Yes/No.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW` (1 operate, 1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `actionId` (navigation), `planId` (navigation) |
| Route | `/platform/conditional-approval-approval-conditions-adm-532` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | `listApprovalMatrices` ?kind |
| Effective | toggle | off | — | `listApprovalMatrices` ?effective |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel, from `getActionPlan`): One record, read-only.

| Shows | Format | Notes |
|---|---|---|
| Plan | grouped details | A plan: plan, validate, simulate, approve, execute, with rollback (design 2.2 D, 3.8; AIC-086..107). |
| ID | the name it points at, never the id | — |
| Origin | chip: Configuration session, Generate configuration, Assistant, Risk case, Operational … | — |
| Origin ref | text | — |
| Summary | text | — |
| Status | chip: Draft, Validated, Simulated, Awaiting approval, Approved, Executing… | — |
| Autonomy level | 1,234 | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). |
| Approval tier | 1,234 | The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). |
| Approval request | the name it points at, never the id | The `approvals` request, where tier 2 or the matrix caught the plan. |
| Proposed action | the name it points at, never the id | The `ai.proposed_action` the plan is presented as for a decision. |
| Change set hash | text | — |
| Governance outcome | chip: Allow, Allow with conditions, Prepare only, Approval required, Escalate, Block | What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). |
| Policy version ref | text | The governance policy version that decided it. |
| Simulation | grouped details | Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4). |
| Partial completion allowed | yes / no (icon or chip) | Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134). |
| Rollback of plan | the name it points at, never the id | — |
| Requested by principal | the name it points at, never the id | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Steps | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |

**Approval condition for this action** (detail panel, from `evaluateApprovalRequirement`): **Conditional authority** (M18-02): the approver's limit for this kind and amount, and whether the action is within it or must escalate.

| Shows | Format | Notes |
|---|---|---|
| Is required | yes / no (icon or chip) | — |
| Matched rule | grouped details | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Order | 1,234 | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason … |
| Min amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Max amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Risk score above | 1,234.5 | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). |
| Condition | text | 11.1.13. Evaluated against the attributes the caller supplied. |
| Approver roles | list or chips (count when long) | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. |
| Approver scope level | chip: Venue, Department, Region, Tenant | 11.1.39. Which organisational level the approver must sit at. |
| Mode | chip: Sequential, Parallel, Consensus, Majority | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. |
| Levels | 1,234 | 11.1.3. Multi-level chains ask each level in turn. |
| Requires MFA | yes / no (icon or chip) | — |
| Requires signature | yes / no (icon or chip) | — |
| Sla minutes | 1,234 | 11.1.14. Null means no SLA, which is different from a long one. |
| Escalate after minutes | 1,234 | — |
| Escalate to roles | list or chips (count when long) | Role ids from `identity.listRoles`, as `approverRoleIds`. |
| Expires after minutes | 1,234 | 11.1.53. An unanswered request eventually stops waiting. |
| External provider | the name it points at, never the id | 11.1.65 (29 September). This level is decided in an external workflow system (`ApprovalExternalProvider`) rather than by a person in TICVAI. |
| Matrix version | 1,234 | — |

**Threshold ranges** (data table, from `listApprovalMatrices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Refund, Price override, Discount override, Complimentary ticket, Membership … | 11.1.7 and 11.1.30–11.1.37. The first four already exist as bespoke implementations and this contract is what they collapse into. |
| Scope level | chip: Tenant, Region, Venue | — |
| Rules | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Order | 1,234 | First match wins. Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason … |
| Min amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Max amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Risk score above | 1,234.5 | 11.1.12. Not matched against the AI risk score (29 September, build pass, group G2). |
| Condition | text | 11.1.13. Evaluated against the attributes the caller supplied. |
| Approver roles | list or chips (count when long) | Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. |
| Approver scope level | chip: Venue, Department, Region, Tenant | 11.1.39. Which organisational level the approver must sit at. |
| Mode | chip: Sequential, Parallel, Consensus, Majority | 11.1.43–11.1.46. Sequential asks one at a time, parallel asks everyone at once, consensus needs all of them, majority needs more than half. |
| Levels | 1,234 | 11.1.3. Multi-level chains ask each level in turn. |
| Requires MFA | yes / no (icon or chip) | — |
| Requires signature | yes / no (icon or chip) | — |
| Sla minutes | 1,234 | 11.1.14. Null means no SLA, which is different from a long one. |
| Escalate after minutes | 1,234 | — |
| Escalate to roles | list or chips (count when long) | Role ids from `identity.listRoles`, as `approverRoleIds`. |
| Expires after minutes | 1,234 | 11.1.53. An unanswered request eventually stops waiting. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps); `evaluateApprovalRequirement` (onLoad, Whether this action is within the approver's limit); `listApprovalMatrices` (onLoad, The threshold ranges)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The conditional approval approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the conditional approval approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No conditional approval approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the conditional approval approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213). |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff
- `evaluateApprovalRequirement` → `APPROVAL_VIEW` (read) · staff
- `listApprovalMatrices` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.4 | Approval Before Execution AI recommendations affecting pricing or financial operations shall require approval before execution | Unified Operations Dashboard | CONTRACTED | `decideProposedAction` |
| 2.7.39 | The system should support: - Multiple credit terms and approval routing processes which can prevent order fulfilment prior to obtaining necessary approvals by client. - Supervisor level authorization … | Ticketing Sales | CONTRACTED | `evaluateApprovalRequirement` |
| 2.9.19 | Price creation, modification, activation, and publication shall support configurable approval workflows with audit trails and role-based authorization. | Ticketing Sales | CONTRACTED | `evaluateApprovalRequirement` |
| 3.6.38 | Promotion creation, modification, activation, and deactivation shall support configurable approval workflows with multi-level authorization and audit tracking. | Admission and Access | CONTRACTED | `evaluateApprovalRequirement` |
| 4.8.10 | Require approval before recipe changes become active. | Bundles and Promotions | CONTRACTED | `evaluateApprovalRequirement` |
| 4.8.11 | Track all recipe creation, modification and approval activities. | Bundles and Promotions | CONTRACTED | `evaluateApprovalRequirement` |
| 5.12.79 | Approval workflow for financial rule changes. | F&B & Guest Management | CONTRACTED | `evaluateApprovalRequirement` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI actions route through the shared approval matrix: the screen shows the approver's limit for the kind and amount and whether the action is within it or must escalate; escalation, delegation and SLA apply as to any approval. *(agreed · MoM 18 Sep 2026, M18-02 · DI-956)*
- Approval is not binary: conditional approval lets an approver approve with restrictions, e.g. a commercial manager may approve price increases only up to a ceiling, anything higher escalates. An approver can also challenge a proposal and request evidence or alternatives. *(agreed · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-932)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-532` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-532`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 6: Works in Conditional Approval & Approval Conditions → Allow humans to approve an AI action subject to explicit conditions rather than treating approval as simply Yes/No.
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (60 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-532?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-533` Human Review, Challenge & AI Clarification Workspace

**Allow the approver to question the AI proposal before making a decision. Human oversight should not mean simply clicking Approve.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_AUDIT_VIEW`, `AI_USE` (2 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `conversationId` (navigation), `decisionRecordId` (navigation) |
| Route | `/platform/human-review-challenge-ai-clarification-workspace-adm-533` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Depth | segmented control | Business | Business · Governance · Technical | `getAiDecisionTrace` ?depth |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every human review challenge** (data table)

| Shows | Format | Notes |
|---|---|---|
| Proposed action | text | not in the schema: `Proposed Action` |
| Business context | text | not in the schema: `Business Context` |
| Risk | text | not in the schema: `Risk` |
| Impact | text | not in the schema: `Impact` |
| AI recommendation | text | not in the schema: `AI Recommendation` |
| Validation | text | not in the schema: `Validation` |
| Alternatives | text | not in the schema: `Alternatives` |
| Ask AI | text | not in the schema: `Ask AI` |

**The selected human review challenge** (detail panel): The pack groups this record's detail under its own headings: “Other Example Questions”, “Important Requirement”, “If evidence is unavailable”.

| Shows | Format | Notes |
|---|---|---|
| Proposed action | text | not in the schema: `Proposed Action` |
| Business context | text | not in the schema: `Business Context` |
| Risk | text | not in the schema: `Risk` |
| Impact | text | not in the schema: `Impact` |
| AI recommendation | text | not in the schema: `AI Recommendation` |
| Validation | text | not in the schema: `Validation` |
| Alternatives | text | not in the schema: `Alternatives` |
| Ask AI | text | not in the schema: `Ask AI` |

**Data it reads**: `getAiDecisionTrace` (onLoad, The full trace of a decision)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The human review challenge list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the human review challenge untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No human review challenge yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the human review challenge are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `overrideAiDecision` → `AI_APPROVE` (operate) · staff
- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff
- `sendAiMessage` → `AI_USE` (operate) · staff, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.5 | Explainability System shall provide reasoning and confidence indicators where available. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.19 | System shall support AI-powered ticketing assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 8.4.20 | System shall support AI-powered support assistance. | Unified Operations Dashboard | CONTRACTED | `sendAiMessage` |
| 18.10.1 | AI Assistant - System shall provide an AI assistant for employees. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.3 | Operational Queries - Users shall retrieve operational information through AI. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.4 | Work Order Assistance - AI shall assist users with work order activities. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 18.10.5 | Knowledge Base Assistance - AI shall provide access to operational knowledge and procedures. | Employee Mobile App & AI Assistant | CONTRACTED | `sendAiMessage` |
| 22.8.4 | AI Chatbot Assistant | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.13 | AI Intent Recognition | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.14 | AI Knowledge Base Integration | Marketing & CRM | CONTRACTED | `sendAiMessage` |
| 22.8.15 | AI Product Recommendations | Marketing & CRM | CONTRACTED | `sendAiMessage` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval is not binary: conditional approval lets an approver approve with restrictions, e.g. a commercial manager may approve price increases only up to a ceiling, anything higher escalates. An approver can also challenge a proposal and request evidence or alternatives. *(agreed · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-932)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-533` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-533`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 8: Works in Human Review, Challenge & AI Clarification Workspace → Allow the approver to question the AI proposal before making a decision. Human oversight should not mean simply clicking Approve.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-533?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_AUDIT_VIEW`, `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-534` Escalation, Delegation & Approval SLA Management

**Ensure AI approvals do not remain indefinitely pending and provide controlled routing when approvers are unavailable or additional authority is required.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `APPROVAL_VIEW` (3 operate, 1 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation), `requestId` (navigation) |
| Route | `/platform/escalation-delegation-approval-sla-management-adm-534` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Sent by *Escalate*** (`escalateApprovalRequest`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 300 | — | — | `escalateApprovalRequest` body |

**Sent by *Delegate*** (`createApprovalDelegation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Delegator principal `delegatorPrincipalId` | picker: choose a delegator principal | required | — | — | shows names, sends the id | A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and … | `createApprovalDelegation` body |
| Delegate principal `delegatePrincipalId` | picker: choose a delegate principal | required | — | — | shows names, sends the id | A principal id, resolved to a name the same way as `delegatorPrincipalId`. | `createApprovalDelegation` body |
| Kinds `kinds` | multi-select chips | optional | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | — | Absent means everything the delegator may approve. | `createApprovalDelegation` body |
| Max amount `maxAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | A delegate may be given less authority than the delegator, never more. | `createApprovalDelegation` body |
| From `from` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createApprovalDelegation` body |
| To `to` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Required. An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it. | `createApprovalDelegation` body |
| Reason `reason` | text area | optional | — | — | — | — | `createApprovalDelegation` body |
| Scope path `scopePath` | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row … | `createApprovalDelegation` body |

**Sent by *Save approval SLA*** (`setApprovalSlaPolicy`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `setApprovalSlaPolicy` body |
| Code `code` | text field | required | — | — | — | — | `setApprovalSlaPolicy` body |
| Applies to request kinds `appliesToRequestKinds` | multi-select chips | optional | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry … | — | — | `setApprovalSlaPolicy` body |
| Target minutes `targetMinutes` | number field (minutes) | optional | — | — | — | — | `setApprovalSlaPolicy` body |
| Business hours only `businessHoursOnly` | toggle | optional | on | — | — | A four-hour SLA starting at five in the afternoon is breached by nine the next morning with nobody having done anything wrong. | `setApprovalSlaPolicy` body |
| Calendar `calendarId` | picker: choose a calendar | optional | — | — | shows names, sends the id | — | `setApprovalSlaPolicy` body |
| Reminders `reminders` | repeatable rows | optional | — | — | — | — | `setApprovalSlaPolicy` body |
| At percent of target `reminders[].atPercentOfTarget` | number field | optional | — | — | — | — | `setApprovalSlaPolicy` body |
| Notify `reminders[].notify` | radio group | optional | — | Approver · Approver manager · Requester · Escalation group | — | — | `setApprovalSlaPolicy` body |
| First reminder at percent `firstReminderAtPercent` | stepper or slider | optional | — | min 1; max 100 | — | Percent of `targetMinutes` at which the first reminder goes (decided 29 September, readiness close-out: the reminder steps are percentages of target). | `setApprovalSlaPolicy` body |
| Second reminder at percent `secondReminderAtPercent` | stepper or slider | optional | — | min 1; max 100 | — | Percent of `targetMinutes` at which the second reminder goes; above `firstReminderAtPercent` | `setApprovalSlaPolicy` body |
| Escalate at percent `escalateAtPercent` | stepper or slider | optional | — | min 1; max 100 | — | Percent of `targetMinutes` at which the request or workflow escalates; at or above `secondReminderAtPercent` | `setApprovalSlaPolicy` body |
| On breach `onBreach` | radio group | optional | Escalate | Notify only · Escalate · Auto approve · Auto reject | — | — | `setApprovalSlaPolicy` body |
| Auto action allowed `autoActionAllowed` | toggle | optional | off | — | — | Auto-approval on breach is off unless somebody says otherwise, in writing. A queue that approves itself when nobody looks is not an approval process. | `setApprovalSlaPolicy` body |
| Escalation group `escalationGroupId` | picker: choose an escalation group | optional | — | — | shows names, sends the id | — | `setApprovalSlaPolicy` body |
| Scope path `scopePath` | text field | optional | — | — | — | — | `setApprovalSlaPolicy` body |

#### Outputs: what the screen shows and produces

**Shown**

**Detail panel** (detail panel, from `getActionPlan`): One record, read-only.

| Shows | Format | Notes |
|---|---|---|
| Plan | grouped details | A plan: plan, validate, simulate, approve, execute, with rollback (design 2.2 D, 3.8; AIC-086..107). |
| ID | the name it points at, never the id | — |
| Origin | chip: Configuration session, Generate configuration, Assistant, Risk case, Operational … | — |
| Origin ref | text | — |
| Summary | text | — |
| Status | chip: Draft, Validated, Simulated, Awaiting approval, Approved, Executing… | — |
| Autonomy level | 1,234 | One autonomy scale for every capability (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). |
| Approval tier | 1,234 | The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). |
| Approval request | the name it points at, never the id | The `approvals` request, where tier 2 or the matrix caught the plan. |
| Proposed action | the name it points at, never the id | The `ai.proposed_action` the plan is presented as for a decision. |
| Change set hash | text | — |
| Governance outcome | chip: Allow, Allow with conditions, Prepare only, Approval required, Escalate, Block | What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). |
| Policy version ref | text | The governance policy version that decided it. |
| Simulation | grouped details | Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4). |
| Partial completion allowed | yes / no (icon or chip) | Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134). |
| Rollback of plan | the name it points at, never the id | — |
| Requested by principal | the name it points at, never the id | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Steps | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |

**Data table** (data table, from `listProposedActions`): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Interaction | the name it points at, never the id | — |
| Kind | chip: Pricing, Promotion, Operational, Financial, Configuration, Content… | `content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from … |
| Target contract | text | Which contract would perform it. The assistant never performs it itself. |
| Target operation | text | — |
| Payload | grouped details | The request body a person would submit, ready to review. Open on purpose: its shape is the request body of `targetOperation` in … |
| Summary | text | — |
| Status | chip: Proposed, Approved, Rejected, Applied, Expired | Expiry (decided 28 September, audit R213): a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires … |
| Expires at | 1 Oct 2026, 14:30 | When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once … |
| Approval level | 1,234 | 8.3.65. Multi-level, because a discount and a pricing change differ in authority. |
| Decided by principal | the name it points at, never the id | — |
| Decision reason | text | Required on rejection. The only signal the assistant is proposing badly, and without it a poor model degrades silently. |
| Proposed at | 1 Oct 2026, 14:30 | — |
| Decided at | 1 Oct 2026, 14:30 | — |
| Plan | the name it points at, never the id | The plan this action presents for a decision (AI design 2.2 D, 3.8). |
| Approval request | the name it points at, never the id | The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3). |
| Change set hash | text | Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181). |

**Delegations in force** (data table, from `listApprovalDelegations`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Delegator principal | the name it points at, never the id | A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from … |
| Delegate principal | the name it points at, never the id | A principal id, resolved to a name the same way as `delegatorPrincipalId`. |
| Kinds | list or chips (count when long) | Absent means everything the delegator may approve. |
| Max amount | AED 1,234.50 | A delegate may be given less authority than the delegator, never more. |
| From | 1 Oct 2026, 14:30 | — |
| To | 1 Oct 2026, 14:30 | Required. An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it. |
| Reason | text | — |
| Is active | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Escalate (secondary button) | `escalateApprovalRequest` POST `/approval-requests/{requestId}/escalate` | inline | ApprovalRequest | — | — |
| Delegate (secondary button) | `createApprovalDelegation` POST `/delegations` | ApprovalDelegation | ApprovalDelegation | 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem); 403 The delegation would hand … | — |
| Save approval SLA (secondary button) | `setApprovalSlaPolicy` PUT `/approval-sla-policies` | ApprovalSlaPolicy | ApprovalSlaPolicy | — | — |

**Data it reads**: `listProposedActions` (onLoad, What the assistant has proposed and nobody has decided); `listApprovalDelegations` (onLoad, Who is acting for whom)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The escalation delegation approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the escalation delegation approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No escalation delegation approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the escalation delegation approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem) |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `listProposedActions` → `AI_USE` (operate) · staff
- `listApprovalDelegations` → `APPROVAL_VIEW` (read) · staff
- `escalateApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff
- `createApprovalDelegation` → `APPROVAL_DECIDE` (operate) · staff
- `setApprovalSlaPolicy` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.47 | Multi-Level Escalation - System shall support escalation through multiple organizational levels. | Approval Workflows & Governance | CONTRACTED | `escalateApprovalRequest` |
| 11.1.48 | Escalation History - System shall maintain complete escalation history. | Approval Workflows & Governance | CONTRACTED | `escalateApprovalRequest` |
| 11.1.8 | Approval Delegation - System shall allow approvers to delegate approval authority to designated users. | Approval Workflows & Governance | CONTRACTED | `createApprovalDelegation` |
| 11.1.9 | Temporary Delegation - System shall support delegation periods with automatic expiration. | Approval Workflows & Governance | CONTRACTED | `createApprovalDelegation` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI actions route through the shared approval matrix: the screen shows the approver's limit for the kind and amount and whether the action is within it or must escalate; escalation, delegation and SLA apply as to any approval. *(agreed · MoM 18 Sep 2026, M18-02 · DI-956)*
- SLA rules set how fast a request must be approved (e.g. within one day); if not actioned it auto-escalates to the next level so someone can investigate (e.g. approver on leave) and reassign. *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-724)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-534` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-534`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 10: Works in Escalation, Delegation & Approval SLA Management → Ensure AI approvals do not remain indefinitely pending and provide controlled routing when approvers are unavailable or additional authority is required.

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-534?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Escalate, Delegate, Save approval SLA.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_USE`, `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_REQUEST`, `APPROVAL_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-535` Live AI Execution Oversight & Human Intervention

**Allow authorized humans to monitor and intervene after an AI-driven action has been approved and entered execution. This is different from approval.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_USE` (2 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§High-impact intervention should show) and no metric row |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/platform/live-ai-execution-oversight-human-intervention-adm-535` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Sent by *Pause*** (`pauseActionPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `pauseActionPlan` body |

**Sent by *Resume*** (`resumeActionPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 1000 | — | — | `resumeActionPlan` body |

**Sent by *Cancel plan*** (`cancelActionPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `cancelActionPlan` body |

**Sent by *Roll back*** (`rollbackActionPlan`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | max length 1000 | — | — | `rollbackActionPlan` body |
| Prefer forward fix `preferForwardFix` | toggle | optional | off | — | — | — | `rollbackActionPlan` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every live execution oversight** (data table, from `getActionPlan`)

| Shows | Format | Notes |
|---|---|---|
| Impact of pausing | text | not in the schema: `Impact of Pausing` |
| Completed objects remain | text | not in the schema: `Completed objects remain` |
| 4 actions will remain pending | text | not in the schema: `4 actions will remain pending` |
| No active transaction affected | text | not in the schema: `No active transaction affected` |
| Emergency stop | text | not in the schema: `Emergency Stop` |
| Emergency stop AI execution | text | not in the schema: `Emergency Stop AI Execution` |
| Authorized role | text | not in the schema: `Authorized Role` |
| Reason | text | not in the schema: `Reason` |
| Confirmation | text | not in the schema: `Confirmation` |
| Audit record | text | not in the schema: `Audit Record` |

**The selected live execution oversight** (detail panel, from `getActionPlan`): The pack groups this record's detail under its own headings: “Approval answers”, “Step Action Module Status”, “Administrator notices”.

| Shows | Format | Notes |
|---|---|---|
| Impact of pausing | text | not in the schema: `Impact of Pausing` |
| Completed objects remain | text | not in the schema: `Completed objects remain` |
| 4 actions will remain pending | text | not in the schema: `4 actions will remain pending` |
| No active transaction affected | text | not in the schema: `No active transaction affected` |
| Emergency stop | text | not in the schema: `Emergency Stop` |
| Emergency stop AI execution | text | not in the schema: `Emergency Stop AI Execution` |
| Authorized role | text | not in the schema: `Authorized Role` |
| Reason | text | not in the schema: `Reason` |
| Confirmation | text | not in the schema: `Confirmation` |
| Audit record | text | not in the schema: `Audit Record` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Pause (secondary button) | `pauseActionPlan` POST `/action-plans/{planId}/pause` | inline | AiActionPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The plan is not executing. | — |
| Resume (secondary button) | `resumeActionPlan` POST `/action-plans/{planId}/resume` | inline | AiActionPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not resumable: the plan is not paused (`plan-not-paused`), or a target object changed since planning … | — |
| Cancel plan (destructive button) | `cancelActionPlan` POST `/action-plans/{planId}/cancel` | inline | AiActionPlan | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The plan is already finished. | — |
| Roll back (destructive button) | `rollbackActionPlan` POST `/action-plans/{planId}/rollback` | inline | AiActionPlanDetail | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Nothing to roll back: the plan has no completed step (`plan-not-applied`). | — |

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

**What opens over it**

- confirmDialog *Cancel plan*: **Names the plan, the steps already executed and what stays applied**: cancelling stops the remaining steps; it does not undo the executed ones (that is Roll back).
- confirmDialog *Roll back*: **Names each executed step and its compensation**, and that the rollback plan goes for approval before it runs.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live execution oversight list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live execution oversight untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live execution oversight yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live execution oversight are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not resumable: the plan is not paused (`plan-not-paused`), or a target object changed since planning (`plan-drifted`).; 409 Nothing to roll back: the plan has no completed step (`plan-not-applied`).; 409 The plan is already finished.; 409 The plan is not executing. |

#### Permissions

- `getActionPlan` → `AI_USE` (operate) · staff
- `pauseActionPlan` → `AI_APPROVE` (operate) · staff
- `resumeActionPlan` → `AI_APPROVE` (operate) · staff
- `cancelActionPlan` → `AI_USE` (operate) · staff
- `rollbackActionPlan` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Roll back on partial failure: plans the compensating steps in reverse dependency order, approved like any plan. *(agreed · MoM 21 Sep 2026, M21-12 · DI-972)*
- AI actions in progress are shown step by step in an AI action command center; if a process only partly completes (e.g. missing information) it rolls back rather than leaving a product half-configured, and a full change history records everything AI modified. *(client request · MoM 21 Sep 2026, 4.9 Core AI Platform — AI Tools, Agents & Action Orchestration · DI-965)*
- Live AI execution oversight lets a user watch an in-progress AI process step by step (e.g. the configuration assistant creating a venue, then products, then performances), and an authorised person can reject, modify or replace an AI decision at any point, with full intervention history. *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-933)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-535` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-535`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 12: Works in Live AI Execution Oversight & Human Intervention → Allow authorized humans to monitor and intervene after an AI-driven action has been approved and entered execution. This is different from approval.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-535?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Pause, Resume, Cancel plan, Roll back.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_USE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-536` Human Override & Manual Control Center

**Provide controlled mechanisms for humans to override an AI recommendation or take control when AI output is inappropriate. Human override should always be possible where governance requires it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | Block A · ticket #20754 (APP-SETUP-ADM-536) |
| Who uses it | ticvai staff holding `AI_APPROVE`, `AI_CONFIGURE` (1 operate, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `capabilityKey` (navigation), `decisionRecordId` (navigation), `planId` (navigation) |
| Route | `/platform/human-override-manual-control-center-adm-536` |

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

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The human override manual list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the human override manual untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No human override manual yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the human override manual are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already paused.; 409 Not paused.; 409 The plan is not executing. |

#### Permissions

- `pauseAiCapability` → `AI_CONFIGURE` (configure) · staff
- `resumeAiCapability` → `AI_APPROVE` (operate) · staff
- `pauseActionPlan` → `AI_APPROVE` (operate) · staff
- `overrideAiDecision` → `AI_APPROVE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live AI execution oversight lets a user watch an in-progress AI process step by step (e.g. the configuration assistant creating a venue, then products, then performances), and an authorised person can reject, modify or replace an AI decision at any point, with full intervention history. *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-933)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-536` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-536`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 14: Works in Human Override & Manual Control Center → Provide controlled mechanisms for humans to override an AI recommendation or take control when AI output is inappropriate. Human override should always be possible where governance requires it.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-536?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_APPROVE`, `AI_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-537` Approval & Intervention History / Decision Timeline

**Provide complete operational history of human involvement in AI activity. This is the human-oversight timeline; Board 3 will later provide deeper enterprise AI explainability and audit.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_AUDIT_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `decisionRecordId` (navigation) |
| Route | `/platform/approval-intervention-history-decision-timeline-adm-537` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search approval intervention history | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by ai capability, user, approver, module, decision, risk and 3 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Capability key | text field | — | — | `searchAiDecisions` ?capabilityKey |
| Outcome | select | — | Answered · Refused · Allowed · Blocked · Executed · Failed · Approved then failed · Published · Suggested | `searchAiDecisions` ?outcome |
| Subject ref | text field | — | — | `searchAiDecisions` ?subjectRef |
| Trace | text field | — | — | `searchAiDecisions` ?traceId |
| Policy version | text field | — | — | `searchAiDecisions` ?policyVersion |
| Model version | text field | — | — | `searchAiDecisions` ?modelVersion |
| From | date and time picker | — | — | `searchAiDecisions` ?from |
| To | date and time picker | — | — | `searchAiDecisions` ?to |

#### Outputs: what the screen shows and produces

**Data it reads**: `searchAiDecisions` (onLoad, Find AI decisions)

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval intervention history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval intervention history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval intervention history yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval intervention history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `searchAiDecisions` → `AI_AUDIT_VIEW` (read) · staff
- `getAiDecisionTrace` → `AI_AUDIT_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.1.6 | AI-based Dynamic Pricing Promotion | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.2.58 | System shall maintain forecasting audit logs. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.3.53 | System shall maintain fraud audit trails. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |
| 8.6.29 | System shall support recommendation audit trails. | Unified Operations Dashboard | CONTRACTED | `searchAiDecisions` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Live AI execution oversight lets a user watch an in-progress AI process step by step (e.g. the configuration assistant creating a venue, then products, then performances), and an authorised person can reject, modify or replace an AI decision at any point, with full intervention history. *(client request · MoM 18 Sep 2026, 4.2 AI Governance — Approval, Human Oversight & Intervention · DI-933)*

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-537` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-537`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 16: Works in Approval & Intervention History / Decision Timeline → Provide complete operational history of human involvement in AI activity. This is the human-oversight timeline; Board 3 will later provide deeper enterprise AI explainability and audit.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-537?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_AUDIT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-538` Human Oversight Workflow Simulator & Readiness Center

**Allow Soft Labs/TICVAI administrators to test the entire human-in-the-loop workflow before activating it in production.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Platform · wave 3 · needs the `ai` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `AI_CONFIGURE`, `AI_USE` (1 configure, 1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Board 1 defines) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `planId` (navigation), `versionId` (navigation) |
| Route | `/platform/human-oversight-workflow-simulator-readiness-center-adm-538` |

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 0 operations.** Unserved: but Operations Assistant lacks Pricing approval rights,. Each needs an operation, or needs removing from …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Risk | select field | — | — | — | — | — | — |
| Autonomy | select field | — | — | — | — | — | — |
| AI permissions | select field | — | — | — | — | — | — |
| Data usage | select field | — | — | — | — | — | — |
| Policy | select field | — | — | — | — | — | — |
| Governance decision | select field | — | — | — | — | — | — |
| Important Boundary — Owning Modules | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| but Operations Assistant lacks Pricing approval rights, (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-529` AI Human Oversight Command Center: *Back to AI Human Oversight Command Center*; carries `planId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The human oversight workflow configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the human oversight workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No human oversight workflow configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The plan is executing or finished; simulate a rollback plan instead.; 409 The version is not a draft (already published or superseded). |

#### Permissions

- `simulateAiGovernancePolicy` → `AI_CONFIGURE` (configure) · staff
- `simulateActionPlan` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Platform, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-538` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS15 AI Governance Board 2.dc.html#adm-538`
- Workshop pack: AI_Governance_Reference.pdf board 2
- Flow F231 *AI Governance board 2: AI Human Oversight Command Center*, step 18: Works in Human Oversight Workflow Simulator & Readiness Center → Allow Soft Labs/TICVAI administrators to test the entire human-in-the-loop workflow before activating it in production.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-538?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: but Operations Assistant lacks Pricing ….
- [ ] Every transition is wired: `ADM-529`.
- [ ] Every gated control is gated: `AI_CONFIGURE`, `AI_USE`.
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

**13 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"cancelActionPlan": {"method":"POST","path":"/action-plans/{planId}/cancel","contract":"ai","summary":"Cancel a plan","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"createAiGovernancePolicyDraft": {"method":"POST","path":"/governance/policy-drafts","contract":"ai","summary":"Draft a governance policy, or a new version of one","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiGovernancePolicyVersion"},
"createApprovalDelegation": {"method":"POST","path":"/delegations","contract":"approvals","summary":"Delegate approval authority","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalDelegation","responds":"ApprovalDelegation"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"escalateApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/escalate","contract":"approvals","summary":"Move it up a level","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"evaluateApprovalRequirement": {"method":"POST","path":"/approval-requests/evaluate","contract":"approvals","summary":"Does this need approval, and from whom","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequirement"},
"getActionPlan": {"method":"GET","path":"/action-plans/{planId}","contract":"ai","summary":"A plan with its steps","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiActionPlanDetail"},
"getAiDecisionTrace": {"method":"GET","path":"/decision-records/{decisionRecordId}/trace","contract":"ai","summary":"The full trace of a decision","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"depth","in":"query","required":null}],"requestBody":null,"responds":"AiDecisionTrace"},
"listAiGovernancePolicyVersions": {"method":"GET","path":"/governance/policy-versions","contract":"ai","summary":"Governance policies and their versions","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"policyId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAiTools": {"method":"GET","path":"/tools","contract":"ai","summary":"The tool registry","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"targetContract","in":"query","required":null},{"name":"effect","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listApprovalDelegations": {"method":"GET","path":"/delegations","contract":"approvals","summary":"Who is standing in for whom","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ApprovalDelegation"},
"listApprovalMatrices": {"method":"GET","path":"/approval-matrices","contract":"approvals","summary":"What requires approval here","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"effective","in":"query","required":null}],"requestBody":null,"responds":"ApprovalMatrix"},
"listProposedActions": {"method":"GET","path":"/proposed-actions","contract":"ai","summary":"What the assistant has proposed and nobody has decided","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProposedAction"},
"overrideAiDecision": {"method":"POST","path":"/decision-records/{decisionRecordId}/override","contract":"ai","summary":"Override an AI decision","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiIntervention"},
"pauseActionPlan": {"method":"POST","path":"/action-plans/{planId}/pause","contract":"ai","summary":"Pause an executing plan","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"pauseAiCapability": {"method":"POST","path":"/governance/capabilities/{capabilityKey}/pause","contract":"ai","summary":"Stop a capability now","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiCapabilityRegistration"},
"resumeActionPlan": {"method":"POST","path":"/action-plans/{planId}/resume","contract":"ai","summary":"Resume a paused plan","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlan"},
"resumeAiCapability": {"method":"POST","path":"/governance/capabilities/{capabilityKey}/resume","contract":"ai","summary":"Resume a paused capability","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiCapabilityRegistration"},
"rollbackActionPlan": {"method":"POST","path":"/action-plans/{planId}/rollback","contract":"ai","summary":"Plan a rollback","permission":"AI_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"searchAiDecisions": {"method":"GET","path":"/decision-records","contract":"ai","summary":"Find AI decisions","permission":"AI_AUDIT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"capabilityKey","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"subjectRef","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"traceId","in":"query","required":null},{"name":"policyVersion","in":"query","required":null},{"name":"modelVersion","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"sendAiMessage": {"method":"POST","path":"/conversations/{conversationId}/messages","contract":"ai","summary":"Ask","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiMessage"},
"setApprovalMatrix": {"method":"PUT","path":"/approval-matrices","contract":"approvals","summary":"Configure what requires approval","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalMatrix","responds":"ApprovalMatrix"},
"setApprovalSlaPolicy": {"method":"PUT","path":"/approval-sla-policies","contract":"approvals","summary":"How long a decision may take, and what happens when it does not","permission":"APPROVAL_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalSlaPolicy","responds":"ApprovalSlaPolicy"},
"simulateActionPlan": {"method":"POST","path":"/action-plans/{planId}/simulate","contract":"ai","summary":"Validate and simulate a plan without changing anything","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiActionPlanDetail"},
"simulateAiGovernancePolicy": {"method":"POST","path":"/governance/policy-versions/{versionId}/simulate","contract":"ai","summary":"Test a draft policy before it is published","permission":"AI_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AiPolicySimulation"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiActionPlan": {"type":"object","x-ticvai-persistence":"ai.action_plan","description":"**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).","required":["origin","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"origin":{"type":"string","enum":["configurationSession","generateConfiguration","assistant","riskCase","operationalRequirement","rollback"]},"originRef":{"type":"string","nullable":true},"summary":{"type":"string"},"status":{"type":"string","enum":["draft","validated","simulated","awaitingApproval","approved","executing","paused","completed","partiallyCompleted","failed","compensated","cancelled","rolledBack"],"readOnly":true},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"approvalTier":{"type":"integer","minimum":1,"maximum":2,"description":"The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request, where tier 2 or the matrix caught the plan."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.proposed_action","description":"The `ai.proposed_action` the plan is presented as for a decision."},"changeSetHash":{"type":"string","readOnly":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"readOnly":true},"policyVersionRef":{"type":"string","readOnly":true,"description":"The governance policy version that decided it."},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."},"partialCompletionAllowed":{"type":"boolean","default":false,"description":"Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."},"rollbackOfPlanId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.action_plan"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiActionPlanDetail": {"type":"object","x-ticvai-persistence":"none — ai.action_plan with its ai.action_step rows","description":"A plan with its steps in DAG order.","required":["plan","steps"],"properties":{"plan":{"$ref":"#/components/schemas/AiActionPlan"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/AiActionStep"}}}},
"AiActionStep": {"type":"object","x-ticvai-persistence":"ai.action_step","description":"One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).","required":["planId","stepNumber","toolKey","targetContract","targetOperation","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","x-ticvai-references":"ai.action_plan"},"stepNumber":{"type":"integer","minimum":1},"dependsOn":{"type":"array","items":{"type":"integer","minimum":1},"description":"Step numbers that must succeed first. The plan is a DAG."},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body of `targetOperation`, validated against it before the plan is approved."},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"idempotencyKey":{"type":"string","readOnly":true},"targetObjectRef":{"type":"string","nullable":true},"targetObjectVersion":{"type":"string","nullable":true,"description":"The version the step was planned against. A different version at execution is drift."},"reversible":{"type":"boolean"},"compensation":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["pending","validated","running","succeeded","failed","compensated","skipped","paused"],"readOnly":true},"attempts":{"type":"integer","minimum":0,"maximum":3,"readOnly":true,"description":"Bounded at 3 (AIC-135)."},"lastError":{"type":"string","nullable":true,"readOnly":true},"resultRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning service's response: success is its answer, not a model's judgement (AIC-097)."},"startedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"AiAutonomyLevel": {"type":"integer","minimum":0,"maximum":4,"description":"**One autonomy scale for every capability** (design 3.8 and 5.5, GOV 0 to 4; ADR-0050). 0 disabled; 1 advisory (explains and recommends, nothing is drafted to run); 2 prepare (drafts a proposal a person applies in the owning screen); 3 execute with approval (the plan runs after approval, through owning APIs); 4 controlled auto (runs without approval, only for listed low-risk reversible actions inside pre-approved ranges). **Not the approval tier**: `ProposedAction.approvalLevel` is the tier."},
"AiCapabilityFamily": {"type":"string","enum":["gatewayAndModels","governance","actionPipeline","knowledgeRetrieval","assistants","analyticsInsights","configurationAssistant","forecasting","anomalyDetection","riskIntelligence","recommendations","decisionRecords","operationsEvaluation","residencyPrivacy"],"description":"The fourteen capabilities of the AI system design (section 1.1), C1 to C14 in order: gateway and model registry, governance decision point, action pipeline and human oversight, knowledge and retrieval, assistants, analytics assistant and insights, configuration assistant, forecasting and operational requirements, anomaly detection, fraud and risk intelligence, recommendation and upsell engine, decision records and audit, operations/evaluation/cost, residency/privacy/tenancy. **Every registered capability belongs to exactly one**, which is what `AiPolicy.enabledCapabilities` and the usage report group by."},
"AiCapabilityRegistration": {"type":"object","x-ticvai-persistence":"ai.capability","description":"**An entry in the capability registry** (design 3.1 Registry, AIC-144, AIC-145; ADM-520). Nothing becomes an operational AI capability without a row here: owner, function, risk class, autonomy, data categories and lifecycle per environment. `autonomyCeiling` is the platform ceiling for the tenant; a tenant or venue may lower `autonomyLevel`, never raise it (AIC-151).","required":["capabilityKey","family","riskClass","autonomyLevel"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"capabilityKey":{"type":"string","description":"Stable key, unique per tenant: `assistant.guest`, `forecast.attendance`, `risk.transaction`, `config.assistant`, `recommend.checkout`."},"family":{"$ref":"#/components/schemas/AiCapabilityFamily"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"identity.principal","description":"The accountable business owner (AIC-144)."},"businessFunction":{"type":"string","nullable":true},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"autonomyCeiling":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"readOnly":true,"description":"The first-release ceiling for this capability (design 3.8 table). Read-only to a tenant."},"autonomyLevel":{"allOf":[{"$ref":"#/components/schemas/AiAutonomyLevel"}],"description":"The level in force at this scope. At most `autonomyCeiling`."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories the capability reads (ADM-524)."},"lifecycle":{"type":"object","description":"Lifecycle per environment (AIC-145): a capability or model can be live in staging and still a draft in production.","properties":{"development":{"type":"string","enum":["draft","pilot","active","retired"]},"staging":{"type":"string","enum":["draft","pilot","active","retired"]},"production":{"type":"string","enum":["draft","pilot","active","retired"]}}},"degradationMode":{"type":"string","enum":["rulesOnly","searchOnly","humanHandoff","hidden","failOpen","lastPublished"],"description":"What the capability does when its model or the service is unavailable (design 3.7, AIC-241)."},"status":{"type":"string","enum":["active","paused"],"readOnly":true,"description":"Paused by `pauseAiCapability`: the capability answers from its degradation mode until resumed."},"pausedReason":{"type":"string","nullable":true,"readOnly":true},"pausedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiDecisionRecord": {"type":"object","x-ticvai-persistence":"ai.decision_record","description":"**The standard record for every governed decision** (design 3.9, C12; AIC-193..209): a recommendation summary, a risk assessment, a forecast publication, a plan step, an assistant answer at significant depth, a governance block, a Help me choose suggestion. **Append-only; corrections are annotations; hash-chained per tenant** so tampering is detectable (AIC-203, AIC-204). **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.","required":["traceId","capabilityKey","outcome","recordHash"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"traceId":{"type":"string"},"capabilityKey":{"type":"string"},"task":{"type":"string","nullable":true},"subjectKind":{"type":"string","nullable":true},"subjectRef":{"type":"string","nullable":true},"inputsRef":{"type":"string","nullable":true,"description":"Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself."},"evidence":{"$ref":"#/components/schemas/AiEvidenceItemList"},"producer":{"type":"string","nullable":true},"modelVersion":{"type":"string","nullable":true},"promptTemplateVersion":{"type":"string","nullable":true},"featureSetVersion":{"type":"string","nullable":true},"knowledgeVersion":{"type":"string","nullable":true},"ruleVersions":{"type":"object","additionalProperties":true,"nullable":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"nullable":true},"policyVersion":{"type":"string","nullable":true},"approvals":{"type":"object","additionalProperties":true,"nullable":true,"description":"Approval requests and their decisions."},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true,"description":"Override or intervention, where a person changed the outcome."},"executionResult":{"type":"object","additionalProperties":true,"nullable":true},"outcomeRef":{"type":"string","nullable":true,"description":"The business outcome it links to (an order, a published version, a closed case)."},"outcome":{"type":"string","enum":["answered","refused","allowed","blocked","executed","failed","approvedThenFailed","published","suggested"],"description":"`approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit)."},"annotations":{"type":"array","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"byPrincipalId":{"type":"string","format":"uuid"},"note":{"type":"string"}}},"readOnly":true,"description":"Corrections, appended; the original fields are never edited."},"previousHash":{"type":"string","readOnly":true},"recordHash":{"type":"string","readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiDecisionTrace": {"type":"object","x-ticvai-persistence":"none — ai.decision_record with the rows it references","description":"**The full trace of one decision** (ADM-540..546): record, evidence, candidates and rules, model and runtime, governance and approvals, execution and business outcome. Depth is gated by permission (AIC-195).","required":["record"],"properties":{"record":{"$ref":"#/components/schemas/AiDecisionRecord"},"depth":{"type":"string","enum":["business","governance","technical"]},"explanation":{"type":"string","description":"Built from structured evidence, never a model's chain of thought (AIC-192)."},"activity":{"type":"array","items":{"$ref":"#/components/schemas/AiInteraction"},"description":"The model calls behind it (`technical` depth)."},"plan":{"allOf":[{"$ref":"#/components/schemas/AiActionPlanDetail"}],"nullable":true},"interventions":{"type":"array","items":{"$ref":"#/components/schemas/AiIntervention"}},"chainVerified":{"type":"boolean","description":"The hash chain around this record verifies."}}},
"AiEvidenceItemList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The evidence of one decision record, stored with it.","items":{"$ref":"#/components/schemas/AiEvidenceItem"}},
"AiGovernanceOutcome": {"type":"string","enum":["allow","allowWithConditions","prepareOnly","approvalRequired","escalate","block"],"description":"What the governance decision point returns (design 3.8, AIC-166). Conflicts resolve to the more restrictive (AIC-161). `block` is an answer, not an error, and is logged as outcome `refused`."},
"AiGovernancePolicyVersion": {"type":"object","x-ticvai-persistence":"ai.governance_policy_version","description":"One version of a governance policy. **Published versions are never edited**: a change is a new version, and the previous one becomes `superseded` in the same transaction (AIC-165).","required":["policyId","version","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"policyId":{"type":"string","format":"uuid","x-ticvai-references":"ai.governance_policy"},"version":{"type":"integer","minimum":1},"status":{"type":"string","enum":["draft","simulated","published","superseded"]},"rules":{"$ref":"#/components/schemas/AiGovernanceRuleList"},"changeNote":{"type":"string","nullable":true},"simulationSummary":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"The last `simulateAiGovernancePolicy` result: decisions that would change, by outcome."},"draftedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"publishedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"identity.principal"},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"supersededAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiGovernanceRule": {"type":"object","x-ticvai-persistence":"none — held in the jsonb rules column of ai.governance_policy_version, through AiGovernanceRuleList","description":"One rule of a governance policy version: which actions on which data, under which conditions, get which outcome (AIC-147..160).","required":["effect"],"properties":{"effect":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKeys":{"type":"array","items":{"type":"string"},"description":"Registered capabilities it applies to. Empty means every capability the policy names."},"actions":{"type":"array","items":{"type":"string","enum":["read","analyze","recommend","generate","prepare","create","modify","publish","execute","delete"]},"description":"ADM-523: what AI may do, from reading to executing."},"dataCategories":{"type":"array","items":{"type":"string"},"description":"Data categories (ADM-524), e.g. `customerContact`, `payment`, `financial`, `operational`."},"purposes":{"type":"array","items":{"type":"string"},"description":"Permitted purposes for those categories (AIC-156, AIR-182)."},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Above this value the effect escalates one step (for example to `approvalRequired`)."},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"Roles the rule applies to; empty means every role."},"environments":{"type":"array","items":{"type":"string","enum":["development","sandbox","staging","production"]},"description":"ADM-525. Empty means every environment. **`sandbox`** (18 September minutes, M18-01): the developer sandbox and a tenant's trial environment, governed apart from staging so a rule can allow in sandbox what it blocks in production."},"conditions":{"type":"object","additionalProperties":true,"nullable":true,"description":"Conditions attached to an `allowWithConditions` effect, for example `maskFields` or `requireCitation`."}}},
"AiGovernanceRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The rules of one policy version, stored with the version as one `jsonb` column.","items":{"$ref":"#/components/schemas/AiGovernanceRule"}},
"AiInteraction": {"type":"object","x-ticvai-persistence":"ai.activity","required":["id","principalId","capability","outcome","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid","nullable":true},"principalId":{"type":"string","format":"uuid"},"audience":{"type":"string","enum":["staff","guest"],"description":"**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"},"billableToTenantId":{"type":"string","format":"uuid","description":"Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"},"scopePath":{"type":"string"},"capability":{"type":"string"},"prompt":{"type":"string"},"response":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"outcome":{"type":"string","enum":["answered","refused","applied","rejected","failed"]},"refusalReason":{"type":"string","nullable":true},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"cost":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"x-ticvai-column":"cost_amount","description":"What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"},"latencyMs":{"type":"integer"},"maskedFieldCount":{"type":"integer","description":"How many fields were redacted. Zero on a prompt touching guest data is a defect."},"traceId":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"description":"The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."},"cacheLayer":{"type":"string","nullable":true,"enum":["guardrail","semantic","exact","negative","analytics"],"description":"Which cache answered, where one did (AI design 3.6). Null for a model call."},"createdAt":{"type":"string","format":"date-time"}}},
"AiIntervention": {"type":"object","x-ticvai-persistence":"ai.intervention","description":"**A person stepping in** (AIC-187, ADM-535, ADM-536): an override, pause, resume, stop, retry or rollback, with the original AI decision and the human one side by side.","required":["kind","targetKind","targetRef"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"type":"string","enum":["override","pause","resume","cancel","retry","rollback","capabilityPause","capabilityResume"]},"targetKind":{"type":"string","enum":["plan","step","decision","capability"]},"targetRef":{"type":"string"},"decisionRecordId":{"type":"string","format":"uuid","nullable":true},"originalDecision":{"type":"object","additionalProperties":true,"nullable":true},"humanDecision":{"type":"object","additionalProperties":true,"nullable":true},"reason":{"type":"string","maxLength":2000},"principalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiMessage": {"type":"object","x-ticvai-persistence":"ai.message","required":["id","conversationId","role","content","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"conversationId":{"type":"string","format":"uuid"},"role":{"type":"string","enum":["user","assistant","system"]},"content":{"type":"string"},"sources":{"$ref":"#/components/schemas/AiSourceList"},"confidence":{"type":"number","nullable":true,"description":"8.1.5, 8.3.67. **Nullable on purpose** — a provider that does not report confidence must yield null rather than an invented number, and an interface showing 0.9 because the code defaulted it is worse than showing nothing.\n"},"rationale":{"type":"string","nullable":true,"description":"8.3.68, 8.3.69."},"proposedAction":{"allOf":[{"$ref":"#/components/schemas/ProposedAction"}],"nullable":true,"description":"Present where the answer suggests a change. **A draft, never applied here.**"},"traceId":{"type":"string"},"provider":{"$ref":"#/components/schemas/AiProviderKind"},"model":{"type":"string"},"promptTokens":{"type":"integer"},"completionTokens":{"type":"integer"},"latencyMs":{"type":"integer"},"createdAt":{"type":"string","format":"date-time"}}},
"AiPolicySimulation": {"type":"object","x-ticvai-persistence":"none — computed; summary kept on ai.governance_policy_version.simulationSummary","description":"What a draft policy version would have decided over recorded decisions and the test cases (ADM-527).","required":["evaluated"],"properties":{"evaluated":{"type":"integer"},"wouldChange":{"type":"integer"},"byOutcome":{"type":"object","additionalProperties":true,"description":"Counts per outcome, current against draft."},"examples":{"type":"array","items":{"type":"object","properties":{"decisionRecordId":{"type":"string","format":"uuid"},"current":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"draft":{"$ref":"#/components/schemas/AiGovernanceOutcome"},"capabilityKey":{"type":"string"}}}}}},
"AiProviderKind": {"type":"string","enum":["openai","gemini","anthropic","azureOpenai","localLlm","openaiCompatible"],"description":"`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"},
"AiRiskClass": {"type":"string","enum":["low","medium","high","critical"],"description":"Business, customer, financial, operational, security and compliance impact of a capability or action type (AIC-144, ADM-521). The governance decision point scores against it."},
"AiSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n","items":{"$ref":"#/components/schemas/AiSource"}},
"AiTool": {"type":"object","x-ticvai-persistence":"ai.tool","description":"**The tool registry** (design 3.1 Registry, 3.8; AIC-088, AIC-089). The executor calls owning modules only for tools registered here: each names its target operation at a contract version, whether it reads, writes or destroys, its risk, the permission it needs, its compensation and timeout. Platform rows, replicated read-only into each tenant database with the tenant root as `scopePath`; written only by `setAiTool` (`PLATFORM_AI_MANAGE`).","x-ticvai-registered-tools-note":"Registrations the release seeds through `setAiTool` for the resources and white-label assistants (29 September, build; 1.2.59, 2.6.50), so a conversational command or a configuration plan can change a resource schedule, a booking, an allocation or the storefront theme, fonts, header, navigation, homepage and pages. Each owner operation accepts `Prefer: validate-only` (added by its owner the same day). `white-label.publishTenantConfig` is deliberately not a tool: the assistant prepares, a person publishes.","x-ticvai-registered-tools":[{"toolKey":"resources.setResourceSchedule","targetContract":"resources","targetOperation":"setResourceSchedule","effect":"write","riskClass":"medium","permission":"RESOURCE_CONFIGURE","reversible":true,"compensationOperation":"setResourceSchedule","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"resources.updateResourceBooking","targetContract":"resources","targetOperation":"updateResourceBooking","effect":"write","riskClass":"medium","permission":"RESOURCE_BOOK","reversible":true,"compensationOperation":"updateResourceBooking","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"resources.allocateResources","targetContract":"resources","targetOperation":"allocateResources","effect":"write","riskClass":"medium","permission":"RESOURCE_BOOK","reversible":true,"compensationOperation":"replaceResourceAllocation","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setTheme","targetContract":"white-label","targetOperation":"setTheme","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setFonts","targetContract":"white-label","targetOperation":"setFonts","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setHeader","targetContract":"white-label","targetOperation":"setHeader","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setNavigation","targetContract":"white-label","targetOperation":"setNavigation","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.setHomepageLayout","targetContract":"white-label","targetOperation":"setHomepageLayout","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"restoreConfigVersion","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"white-label.createContentPage","targetContract":"white-label","targetOperation":"createContentPage","effect":"write","riskClass":"low","permission":"TENANT_CONFIGURE","reversible":true,"compensationOperation":"deleteContentPage","timeoutMs":5000,"idempotent":true,"validateOnly":true},{"toolKey":"venue-map.generateVisitPlan","targetContract":"venue-map","targetOperation":"generateVisitPlan","effect":"write","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":null,"timeoutMs":3000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.getVisitPlan","targetContract":"venue-map","targetOperation":"getVisitPlan","effect":"read","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":null,"timeoutMs":2000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.listVisitPlanAlternatives","targetContract":"venue-map","targetOperation":"listVisitPlanAlternatives","effect":"read","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":null,"timeoutMs":2000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.updateVisitPlan","targetContract":"venue-map","targetOperation":"updateVisitPlan","effect":"write","riskClass":"low","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":"updateVisitPlan","timeoutMs":3000,"idempotent":true,"validateOnly":false,"agent":"planner.guest"},{"toolKey":"venue-map.bookVisitPlan","targetContract":"venue-map","targetOperation":"bookVisitPlan","effect":"write","riskClass":"medium","permission":null,"callerAudience":"guest","reversible":true,"compensationOperation":"orders.removeCartLine","timeoutMs":5000,"idempotent":true,"validateOnly":false,"agent":"planner.guest","requiresGuestConfirmation":true}],"x-ticvai-registered-tools-planner-note":"**The planner agent's tools** (29 September, MOB-6; the assistant profile `planner.guest`, audience guest, `guestCapabilityScope` `visitPlanning`). The agent refines a rules plan by chat on GST-054 through these five `venue-map` operations, **always called as the guest whose plan it is** (permission null, the guest session's own plan), so every change is a plan version the guest can undo. `bookVisitPlan` needs the guest to press Book in the app; the agent may prepare it and never checks out. AI writes nothing outside `ai.*` (ADR-0020): the plan tables are written by the venue-map service these tools call. **Grounding** (30 September client meeting, MoM 4.7): the agent's candidates are only what these tools return for a day, i.e. the rides, dining and retail points (shops and kiosks) on the published map of that day's venue; it never proposes a point from another venue or from general knowledge, and says so when a preference is not met there (`VisitPlan.unmatchedPreferences`).","required":["toolKey","targetContract","targetOperation","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"effect":{"type":"string","enum":["read","write","destructive"]},"riskClass":{"$ref":"#/components/schemas/AiRiskClass"},"permission":{"type":"string","description":"The permission the requester must hold for the executor to call it on their behalf."},"reversible":{"type":"boolean","description":"Non-reversible steps (a refund, a publish) need the stronger approval tier (AIC-099)."},"compensationOperation":{"type":"string","nullable":true},"timeoutMs":{"type":"integer","minimum":1},"idempotent":{"type":"boolean","default":true},"validateOnly":{"type":"boolean","default":false,"description":"The owner accepts `Prefer: validate-only` on it (design 2.3)."},"status":{"type":"string","enum":["active","disabled"]},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalDelegation": {"type":"object","x-ticvai-persistence":"approvals.delegation","required":["delegatorPrincipalId","delegatePrincipalId","from","to"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"delegatorPrincipalId":{"type":"string","format":"uuid","description":"A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and `identity.getPrincipal`.\n"},"delegatePrincipalId":{"type":"string","format":"uuid","description":"A principal id, resolved to a name the same way as `delegatorPrincipalId`."},"kinds":{"type":"array","description":"Absent means everything the delegator may approve.","items":{"$ref":"#/components/schemas/ApprovalKind"}},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"A delegate may be given less authority than the delegator, never more."},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time","description":"**Required.** An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it.\n"},"reason":{"type":"string"},"isActive":{"type":"boolean","readOnly":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalRequirement": {"type":"object","x-ticvai-persistence":"none — computed","description":"The answer to \"does this need approval\", returned before the action.","required":["isRequired"],"properties":{"isRequired":{"type":"boolean"},"matchedRule":{"allOf":[{"$ref":"#/components/schemas/ApprovalRule"}],"nullable":true},"matrixVersion":{"type":"integer","nullable":true},"approvers":{"type":"array","description":"Resolved, with delegations applied. **Named so the caller can say \"this needs Sara\"** rather than \"this needs approval\".\n","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"level":{"type":"integer"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true}}}},"slaMinutes":{"type":"integer","nullable":true},"noApproverAvailable":{"type":"boolean","description":"**The case that must not fail silently.** A rule requiring a role nobody at this venue holds means the action is blocked forever, and the caller needs to know that now rather than after raising a request nobody can decide.\n"}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"}}},
"ApprovalSlaPolicy": {"type":"object","x-ticvai-persistence":"approvals.sla_policy","description":"Approvals boards 5.5 and 5.6. **A target with no consequence is a number in a table**, so the reminder and breach behaviour are part of the policy.\n","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"targetMinutes":{"type":"integer"},"businessHoursOnly":{"type":"boolean","default":true,"description":"**A four-hour SLA starting at five in the afternoon is breached by nine the next morning with nobody having done anything wrong.**\n"},"calendarId":{"type":"string","format":"uuid","nullable":true},"reminders":{"type":"array","items":{"type":"object","properties":{"atPercentOfTarget":{"type":"integer"},"notify":{"type":"string","enum":["approver","approverManager","requester","escalationGroup"]}}}},"firstReminderAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"**Percent of `targetMinutes` at which the first reminder goes** (decided 29 September, readiness close-out: the reminder steps are percentages of target). A column so the SLA, Escalation, Reminder & Timeout Rules screen reads it rather than unpacking `reminders`; the reminder in `reminders` at this percentage says whom it notifies (data model for the agreed operations, 29 September)."},"secondReminderAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Percent of `targetMinutes` at which the second reminder goes; above `firstReminderAtPercent`"},"escalateAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Percent of `targetMinutes` at which the request or workflow escalates; at or above `secondReminderAtPercent`"},"onBreach":{"type":"string","enum":["notifyOnly","escalate","autoApprove","autoReject"],"default":"escalate"},"autoActionAllowed":{"type":"boolean","default":false,"description":"**Auto-approval on breach is off unless somebody says otherwise, in writing.** A queue that approves itself when nobody looks is not an approval process.\n"},"escalationGroupId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"Money": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"numeric(18,4)","description":"**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n","required":["amount","currency","scale"],"properties":{"amount":{"type":"string","description":"Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n","pattern":"^-?\\d+(\\.\\d{1,4})?$"},"currency":{"type":"string","description":"**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n","pattern":"^[A-Z]{3}$"},"scale":{"type":"integer","description":"Resolved from the region alongside `currency`.","minimum":0,"maximum":4}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}}
}
```
