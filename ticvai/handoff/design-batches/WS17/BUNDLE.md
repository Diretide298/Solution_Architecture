# WS17 — Approval Workflows and Governance board 5

**10 screens · 10 operations · 17 schemas · 5 permissions**

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

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `APPROVAL_ACT, APPROVAL_CONFIGURE, APPROVAL_DECIDE, APPROVAL_REQUEST, APPROVAL_VIEW`. A control nobody can use must say so,
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

## The processes these screens belong to

Written by the owner of each process (`handoff/design-notes/`). Read before any screen: it says how the process runs end to end and which words the screens must use.

### Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management)

Platform Foundation is everything the apps stand on. Five apps each have one door: the guest app and website (WEB-016, GST-042: a six-digit code to email or mobile, a password, Apple or Google, UAE Pass; never enterprise SSO), the till (POS-000: employee number and PIN, recent operators as tiles; the kitchen display is the same app), the staff handheld and scanner (EMP-001, SCN-001), Venue Management (SUP-001, the single door for the back office P08, the CMS P13, analytics P16 and the support desk P12) and TICVAI Control (ADM-001 for TICVAI's own platform operators, PTR-001 for partner users; the developer portal P14 and the sign-up P17 belong to this app too). A second factor is required by permission, not by role or device: ROLE_MANAGE, LEDGER_APPROVE and every PLATFORM_* permission, plus any the tenant adds; so a cashier never sees it and a platform operator always does. The factor is an authenticator app with an emailed code as fallback; five wrong codes lock step-up for the lockout minutes, never permanently. Guests get two-step verification only at a venue that switched it on. One person holds one session per workstation: a second sign-in is refused and only a supervisor ends the other session. Several roles mean a role prompt; one role goes straight in. The workstation decides the Sale Board, hardware and till identity, never what a person may do. Sensitive actions (refund approval, journal approval, credential reset, partner credit, commission rules, opening a platform-staff grant and 17 more) demand a fresh step-up on the operation itself, asked in place in the action's confirmation; the tenant may raise the strength, never remove it. Permission outcomes are three, never one word: self-authorised (proceeds, audited), escalated (a supervisor PIN in place), refused (the denied state, naming the permission); a missing permission is never an empty table, and a record outside the person's venues is "not found", indistinguishable from absent. The hierarchy is binding (tenant, brand, region, venue, department, sub-department, workstation; outlet beside department for F&B and retail); region owns currency, decimals, time zone, date format and fiscal year; configuration resolves nearest-ancestor across tenant, region and venue (outlet for F&B and retail), venue is the floor and a workstation is assigned a profile, never configured; every configuration screen says which level it writes and what it inherits. Venue Management is one tenant-level surface filtering across the venues in the session's scope. TICVAI's Console runs outside every cell: a platform operator picks a tenant and opens a time-boxed, audited platform-staff grant (with step-up) before any tenant action, and the tenant sees every action in its audit log (ADM-412 is the reference implementation). Approval workflows record authorisations and never perform the action; the requester cannot approve their own request; a venue may tighten and never loosen a rule from above; in-flight …
*(source: screens/P12-support-agent-console.yaml#SUP-001; R135; R126; R167; DI-1072; ADR-0002; ADR-0003; ADR-0004; R184; contracts/spine/identity.yaml#createMfaChallenge; contracts/spine/approvals.yaml#setStepUpPolicy; ADR-0011; ADR-0018; ADR-0029; R098; contracts/spine/approvals.yaml#decideApprovalRequest …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sign in / Sign out | Entering and leaving any app, staff or guest. | Login, Log in, Logon, Logout | screens/P04-point-of-sale.yaml#POS-000 … |
| Authentication code | The staff second factor from the authenticator app (or the emailed fallback). | OTP, 2FA code, token | screens/P09-platform-admin-console.yaml#ADM-001 |
| One-time code | The six-digit code a guest receives to sign in or prove a contact. | OTP, PIN, password | DI-1034; R167 |
| Two-step verification | The guest's optional second factor, asked only at venues that switched it on. | MFA, 2FA | DI-1072 |
| Tenant / Brand / Region / Venue / Department / Outlet | The binding hierarchy levels; region owns currency and dates; outlet is F&B or retail inside a venue. | Client, Customer, Org (for tenant), Site, Park, Property (for venue), Area, Territory (for region) | ADR-0011; ADR-0018 |
| Workstation (back office) / till (operator copy) | A configured device; decides Sale Board, hardware and till identity, never authorisation. | Terminal, Station, POS (for the device), till (for the Deposit Box) | ADR-0002; R156 |
| Sale Board | The configured front end a workstation loads (ticketing, F&B or retail). | Screen, Layout, Menu | ADR-0003 |
| Role | A named, fully configurable grouping of permissions; the seeded five are editable starting points. | Group, Profile | R229 |
| Staff member / Partner user / Platform operator | A tenant's staff principal; a partner's user; a TICVAI employee in the Console. | User (alone), Account, Agent (for venue staff) | F104 step 1; F104 step 4; F104 step 5 |
| Platform-staff grant | The time-boxed, audited access a platform operator opens into one tenant before acting in it. | Impersonation, Support login | R098 |
| Escalate / Refused | Escalate is supervisor approval captured in place; Refused is the denied state that names the permission. | Denied (for an action that can be escalated) | R197 |
| Approve / Reject / Return / Request information | The four decisions on an approval request; Withdraw is the requester's own act and never a rejection. | Accept, Decline, Cancel (for withdraw) | contracts/spine/approvals.yaml#decideApprovalRequest … |
| Subscription / Plan / Module / Licence | TICVAI's commercial relationship with a tenant, its plan, the modules it licenses and the limits. | Membership (that is the guest's pass) | R214 |
| Membership / Annual pass | A guest's pass product and its holder (BO-284 to BO-303). | Subscription (that is the tenant's TICVAI plan) | screens/P08-venue-back-office.yaml#BO-284 |
| Sandbox client / Production client | A developer's own test credential; a TICVAI-issued live credential after certification. | Test key, Live key, API key (without environment) | DI-927 |
| Asset (DAM) / Media (ticket) | A digital file in the library; ticket media is a wristband or card carrying entitlements. Never mix them. | Media (for a library asset) | contracts/satellite/assets.yaml#searchMedia … |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-384` | Delegation & Escalation Command Center | B–D | 9 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-385` | Delegation Management | B–D | 10 | 0 | 5 | 2 | 1 | 0 | — | notStarted (—) |
| `BO-386` | Temporary Delegation & Availability Calendar | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-387` | Out-of-Office & Substitute Routing | B–D | 7 | 0 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-388` | Approval SLA Policy Configuration | B–D | 8 | 0 | 5 | 0 | 1 | 3 | — | notStarted (—) |
| `BO-389` | Reminder & Breach Notification Rules | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-390` | Escalation Policy Builder | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-391` | Live Escalation Operations Center | B–D | 9 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `BO-392` | SLA & Escalation Performance Analytics | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-393` | AI SLA & Escalation Advisor | B–D | 2 | 20 | 6 | 9 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-386, BO-389, BO-390, BO-391, BO-392 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-384` Delegation & Escalation Command Center

**Provide administrators and managers with a real-time overview of delegation, SLA and escalation conditions across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_ACT`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | `instanceId` (navigation) |
| Route | `/venue-operations/delegation-escalation-command-center-bo-384` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Delegations, unavailable approvers, SLA at risk and escalations across the venues in scope, with intervention.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

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

**Active Delegations** (metric tile)

**Approvers Unavailable** (metric tile)

**Pending Approvals** (metric tile)

**SLA At Risk** (metric tile)

**SLA Breached** (metric tile)

**Escalated Today** (metric tile)

**Unassigned Requests** (metric tile)

**Critical Escalations** (metric tile)

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Act on workflow instance (primary button) | `actOnWorkflowInstance` POST `/workflow-instances/{instanceId}/actions` | WorkflowInstanceActionInput | WorkflowInstance | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` … | gated `APPROVAL_ACT`; opens modal first |

**Data it reads**: `listApprovalDelegations` (onLoad, Delegations in force); `listSlaEscalationBottleneck` (onLoad, Live escalations)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-393` AI SLA & Escalation Advisor: *AI SLA & Escalation Advisor*
- → `BO-385` Delegation Management: *Delegation Management*
- → `BO-386` Temporary Delegation & Availability Calendar: *Temporary Delegation & Availability Calendar*
- → `BO-387` Out-of-Office & Substitute Routing: *Out-of-Office & Substitute Routing*
- → `BO-388` Approval SLA Policy Configuration: *Approval SLA Policy Configuration*
- → `BO-389` Reminder & Breach Notification Rules: *Reminder & Breach Notification Rules*
- → `BO-390` Escalation Policy Builder: *Escalation Policy Builder*
- → `BO-391` Live Escalation Operations Center: *Live Escalation Operations Center*; carries `instanceId`
- → `BO-392` SLA & Escalation Performance Analytics: *SLA & Escalation Performance Analytics*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delegation escalation list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delegation escalation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing to show yet**: the figures fill as activity is recorded. Offers no create action — a monitor creates nothing — and says so rather than showing empty tiles. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the delegation escalation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not … |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_ACT for Act on workflow instance. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*
- **actOnWorkflowInstance answers 409**: Show it as something the person can act on, not a failure: The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step to skip is an approval node *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*
- **actOnWorkflowInstance answers 422**: Show it as something the person can act on, not a failure: A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not an allowed edge, or the assignee is the requester of the approval *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Active Delegations: 128
  Approvers Unavailable: 46
  Pending Approvals: 312
  SLA At Risk: 3 h 20 min
  SLA Breached: 42 min
  Escalated Today: 233
  Unassigned Requests: 0
  Critical Escalations: 5
```

#### Permissions

- `listApprovalDelegations` → `APPROVAL_VIEW` (read) · staff
- `listSlaEscalationBottleneck` → `APPROVAL_VIEW` (read) · staff
- `actOnWorkflowInstance` → `APPROVAL_ACT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-384` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-384`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 5
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 1: Opens Delegation & Escalation Command Center → Provide administrators and managers with a real-time overview of delegation, SLA and escalation conditions across TICVAI.
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F127 branch at step 1 (expected): when Nothing has been set up on Delegation & Escalation Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F127 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-384?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Act on workflow instance.
- [ ] Every transition is wired: `BO-100`, `BO-393`, `BO-385`, `BO-386`, `BO-387`, `BO-388`, `BO-389`, `BO-390`, `BO-391`, `BO-392`.
- [ ] Every gated control is gated: `APPROVAL_ACT`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-385` Delegation Management

**Allow an authorized approver or administrator to delegate approval authority to another eligible user. The source specifically requires approvers to be able to delegate their approval authority.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_DECIDE`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Delegation Setup) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `delegationId` (navigation) · cold entry: **Reached from the list that owns it**, so the identifier arrives with the navigation. Opened cold without one, the screen says what is missing and offers that … |
| Route | `/venue-operations/delegation-management-bo-385` |

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): listDelegations (GUEST_VIEW) lists who may act for a guest; approval delegation is listApprovalDelegations, already declared (design-notes correction …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** An approver delegates authority to an eligible colleague for a period; the same function as BO-087.

**Fixed on main** (the package already carries these; draw what it says): listDelegations (GUEST_VIEW) is the guest delegation operation. (CHG-WIR-021); Fields are prefilled with sample names ("Delegator Ahmed Raza", "Delegate To Sara Khan"). (CHG-SBO-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Delegator | select field | — | — | — | — | A pick list of people by name; sample names belong in the sample data. | — |
| Delegate to | select field | — | — | — | — | — | — |

**Form: Activate delegation** (modal, opened by *Activate delegation*; *Activate delegation* calls `createApprovalDelegation`, *Cancel* sends nothing)

**Collects what `createApprovalDelegation` sends before it is called.** Required: `delegatorPrincipalId`, `delegatePrincipalId`, `from`, `to`. Optional: `kinds`, `maxAmount`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

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

Errors to draw in the form: 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem); 403 The delegation would hand over authority that is not there. `refusedReason` is `delegateLacksPermission` where the delegate does not hold the permission being … (DelegationRefusedProblem)

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Delegation window and limits**: Always time-bounded: 'to' must follow 'from' (refused invalidWindow); the delegate cannot exceed the delegator's kinds or maxAmount and must hold the permission (exceedsDelegatorAuthority, delegateLacksPermission); a delegate never approves a request the delegator raised. *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Activate delegation (primary button) | `createApprovalDelegation` POST `/delegations` | ApprovalDelegation | ApprovalDelegation | 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem); 403 The delegation would hand … | opens modal first |
| Cancel delegation (destructive button) | `revokeApprovalDelegation` DELETE `/delegations/{delegationId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |

**Data it reads**: `listApprovalDelegations` (onLoad, List approval delegations (screen currently binds guest …)

**Where the user goes next**

- → `BO-384` Delegation & Escalation Command Center: *Back to Delegation & Escalation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delegation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delegation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No delegation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem) |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW, GUEST_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_DECIDE for createApprovalDelegation, revokeApprovalDelegation. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*
- **createApprovalDelegation answers 403**: Show it as something the person can act on, not a failure: The delegation would hand over authority that is not there. `refusedReason` is `delegateLacksPermission` where the delegate does not hold the permission being delegated, or `exceedsDelegatorAuthority` where `kinds` or `maxAmount` go beyond what the delegator may approve. The shared `Forbidden`, with no `refusedReason`, is the ca... *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Consistency with other screens

- Match `BO-087`: One delegation editor.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listApprovalDelegations (ApprovalDelegation):
- maxAmount: AED 1,250.00
  from: 01/10/2026 09:14
  to: 01/10/2026 09:14
  reason: Guest charged twice at Main Gate Till 3
  isActive: true
- maxAmount: AED 48,000.00
  from: 30/09/2026 18:02
  to: 30/09/2026 18:02
  reason: Group of 40 from Desert Gate Tours
  isActive: true
```

#### Permissions

- `createApprovalDelegation` → `APPROVAL_DECIDE` (operate) · staff
- `listApprovalDelegations` → `APPROVAL_VIEW` (read) · staff
- `revokeApprovalDelegation` → `APPROVAL_DECIDE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.8 | Approval Delegation - System shall allow approvers to delegate approval authority to designated users. | Approval Workflows & Governance | CONTRACTED | `createApprovalDelegation` |
| 11.1.9 | Temporary Delegation - System shall support delegation periods with automatic expiration. | Approval Workflows & Governance | CONTRACTED | `createApprovalDelegation` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Delegation/availability management defines a substitute approver so requests don't stall when an approver is unavailable. *(client request · MoM 8 Sep 2026, 4.16 Delegation, Substitute Approval & SLA Monitoring · DI-730)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-385` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-385`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 5
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 2: Works in Delegation Management → Allow an authorized approver or administrator to delegate approval authority to another eligible user. The source specifically requires approvers to be able to delegate their approval authority.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-385?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Activate delegation, Cancel delegation.
- [ ] Every transition is wired: `BO-384`.
- [ ] Every gated control is gated: `APPROVAL_DECIDE`, `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-386` Temporary Delegation & Availability Calendar

**Manage time-limited delegation caused by annual leave, business travel, training, sickness, or other planned absence. The matrix requires temporary delegation periods with automatic expiration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_DECIDE`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/temporary-delegation-availability-calendar-bo-386` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** An approver's availability calendar (leave, travel, training) with the delegation that covers each absence and its automatic end.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save approver availability (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listApprovalDelegations` (onLoad, Existing delegations)

**Where the user goes next**

- → `BO-384` Delegation & Escalation Command Center: *Back to Delegation & Escalation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The temporary delegation availability list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the temporary delegation availability untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No temporary delegation availability yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the temporary delegation availability are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_DECIDE for setApproverAvailability. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#setApproverAvailability)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listApprovalDelegations (ApprovalDelegation):
- maxAmount: AED 1,250.00
  from: 01/10/2026 09:14
  to: 01/10/2026 09:14
  reason: Guest charged twice at Main Gate Till 3
  isActive: true
- maxAmount: AED 48,000.00
  from: 30/09/2026 18:02
  to: 30/09/2026 18:02
  reason: Group of 40 from Desert Gate Tours
  isActive: true
```

#### Permissions

- `setApproverAvailability` → `APPROVAL_DECIDE` (operate) · staff
- `listApprovalDelegations` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Delegation/availability management defines a substitute approver so requests don't stall when an approver is unavailable. *(client request · MoM 8 Sep 2026, 4.16 Delegation, Substitute Approval & SLA Monitoring · DI-730)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-386` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-386`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 5
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 4: Works in Temporary Delegation & Availability Calendar → Manage time-limited delegation caused by annual leave, business travel, training, sickness, or other planned absence. The matrix requires temporary delegation periods with automatic expiration.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-386?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save approver availability, Cancel.
- [ ] Every transition is wired: `BO-384`.
- [ ] Every gated control is gated: `APPROVAL_DECIDE`, `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-387` Out-of-Office & Substitute Routing

**Configure automatic routing when the primary approver is unavailable. The matrix specifically requires automatic rerouting when approvers are unavailable.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_DECIDE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/out-of-office-substitute-routing-bo-387` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What happens when the approver is unavailable: reroute immediately or after a wait, to a deputy, manager or shared queue, or escalate; the original approver kept informed.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Immediate rerouting | select field | — | — | — | — | — | — |
| Wait X minutes | select field | — | — | — | — | — | — |
| Route to deputy | select field | — | — | — | — | — | — |
| Route to manager | select field | — | — | — | — | — | — |
| Route to shared queue | text field | — | — | — | — | — | — |
| Escalate | select field | — | — | — | — | — | — |
| Keep original approver informed | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-384` Delegation & Escalation Command Center: *Back to Delegation & Escalation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The out-of-office substitute routing configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the out-of-office substitute routing untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No out-of-office substitute routing configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
routing:
  when: approver out of office
  after: 15 min
  routeTo: deputy
  keepOriginalInformed: true
```

#### Permissions

- `setApproverAvailability` → `APPROVAL_DECIDE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Delegation/availability management defines a substitute approver so requests don't stall when an approver is unavailable. *(client request · MoM 8 Sep 2026, 4.16 Delegation, Substitute Approval & SLA Monitoring · DI-730)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-387` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-387`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 5
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 6: Works in Out-of-Office & Substitute Routing → Configure automatic routing when the primary approver is unavailable. The matrix specifically requires automatic rerouting when approvers are unavailable.

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-387?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-384`.
- [ ] Every gated control is gated: `APPROVAL_DECIDE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-388` Approval SLA Policy Configuration

**Define how quickly different approval types must be processed. The matrix explicitly requires configurable approval response-time targets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/approval-sla-policy-configuration-bo-388` |

**What the spec says about it.** **One SLA policy screen (decided 2 October 2026, merge as proposed; CHG-SBO-021):** reminders and breach notifications (BO-389) and the escalation policy (BO-390) are sections of this one policy object.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Response-time targets per approval kind, with business or calendar hours, weekends, holidays and priority or risk variants.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| SLA duration | select field | — | — | — | — | — | — |
| Business hours / calendar hours | text field | — | — | — | — | — | — |
| Working days | select field | — | — | — | — | — | — |
| Weekends | select field | — | — | — | — | — | — |
| Public holidays | select field | — | — | — | — | — | — |
| Venue operating hours | select field | — | — | — | — | — | — |
| Priority-based SLA | select field | — | — | — | — | — | — |
| Risk-based SLA | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApprovalSlaPolicy: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setApprovalSlaPolicy)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-384` Delegation & Escalation Command Center: *Back to Delegation & Escalation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval sla policy configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval sla policy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval sla policy configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
sla:
  kind: Refund above threshold
  duration: 30 min
  hours: venue operating hours
  weekends: included
```

#### Permissions

- `setApprovalSlaPolicy` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- SLA rules set how fast a request must be approved (e.g. within one day); if not actioned it auto-escalates to the next level so someone can investigate (e.g. approver on leave) and reassign. *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-724)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-388` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-388`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 5
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 8: Works in Approval SLA Policy Configuration → Define how quickly different approval types must be processed. The matrix explicitly requires configurable approval response-time targets.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-388?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-384`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-389` Reminder & Breach Notification Rules

**Configure proactive notifications before and after SLA breaches. The source requires reminders for pending approvals and alerts when SLA thresholds are exceeded (merged into BO-388 Approval SLA Policy Configuration).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/reminder-breach-notification-rules-bo-389` |

**What the spec says about it.** **Merged into BO-388** (decided 2 October 2026, Chinmay: duplicate screens merged as proposed; CHG-SBO-021). Reminders, breach notifications and escalation are parts of the one approval SLA policy (`setApprovalSlaPolicy`), edited on BO-388 (design-note correction platform-foundation BO-389). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-388, and nothing on it is built separately.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Reminders before an SLA breach and alerts after, to whom and through which channel.

**Fixed on main** (the package already carries these; draw what it says): Shares setApprovalSlaPolicy with BO-388 and BO-390 and has no fields. (CHG-SBO-021).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApprovalSlaPolicy: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setApprovalSlaPolicy)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-384` Delegation & Escalation Command Center: *Back to Delegation & Escalation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Routes to BO-388 while it opens. |
| Error (`?state=error`) | Could not open BO-388; says so and offers to retry. |
| Empty, first run (`?state=emptyFirstRun`) | Never shown: this id routes to BO-388, whose empty states apply. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: this id routes to BO-388. |
| Permission denied (`?state=emptyNoAccess`) | As BO-388: shown when the caller lacks the access BO-388 requires, named in words. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kind: Refund above threshold
remindAt: 50% and 80% of SLA
breachAlertTo:
- Venue Manager
- Duty Manager
channel:
- in-app
- email
```

#### Permissions

**A refused user sees:** As BO-388: shown when the caller lacks the access BO-388 requires, named in words.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- SLA reminders notify the approver (e.g. by email) as the deadline approaches; a workload view shows how many pending requests each approver currently carries. *(client request · MoM 8 Sep 2026, 4.16 Delegation, Substitute Approval & SLA Monitoring · DI-731)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-389` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-389`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 5
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 10: Works in Reminder & Breach Notification Rules → Configure proactive notifications before and after SLA breaches. The source requires reminders for pending approvals and alerts when SLA thresholds are exceeded.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-389?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-384`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-390` Escalation Policy Builder

**Define what TICVAI should do when an approval remains unresolved or meets another escalation condition (merged into BO-388 Approval SLA Policy Configuration).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/escalation-policy-builder-bo-390` |

**What the spec says about it.** **Merged into BO-388** (decided 2 October 2026, Chinmay: duplicate screens merged as proposed; CHG-SBO-021). Reminders, breach notifications and escalation are parts of the one approval SLA policy (`setApprovalSlaPolicy`), edited on BO-388 (design-note correction platform-foundation BO-390). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-388, and nothing on it is built separately.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What happens when an approval stays unresolved: escalation levels, timing and targets.

**Fixed on main** (the package already carries these; draw what it says): No fields; shares setApprovalSlaPolicy. (CHG-SBO-021).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApprovalSlaPolicy: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setApprovalSlaPolicy)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-384` Delegation & Escalation Command Center: *Back to Delegation & Escalation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Routes to BO-388 while it opens. |
| Error (`?state=error`) | Could not open BO-388; says so and offers to retry. |
| Empty, first run (`?state=emptyFirstRun`) | Never shown: this id routes to BO-388, whose empty states apply. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: this id routes to BO-388. |
| Permission denied (`?state=emptyNoAccess`) | As BO-388: shown when the caller lacks the access BO-388 requires, named in words. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
kind: Purchase order
levels:
- 'after 4 h: department head'
- 'after 24 h: venue manager'
- 'after 48 h: regional director'
```

#### Permissions

**A refused user sees:** As BO-388: shown when the caller lacks the access BO-388 requires, named in words.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- SLA rules set how fast a request must be approved (e.g. within one day); if not actioned it auto-escalates to the next level so someone can investigate (e.g. approver on leave) and reassign. *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-724)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-390` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-390`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 5
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 12: Works in Escalation Policy Builder → Define what TICVAI should do when an approval remains unresolved or meets another escalation condition.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-390?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-384`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-391` Live Escalation Operations Center

**Allow managers to monitor and intervene in currently escalated approvals.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_ACT`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `instanceId` (navigation) |
| Route | `/venue-operations/live-escalation-operations-center-bo-391` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Live view of escalated approvals for managers to intervene (reassign, decide, extend).

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

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

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Act on workflow instance (primary button) | `actOnWorkflowInstance` POST `/workflow-instances/{instanceId}/actions` | WorkflowInstanceActionInput | WorkflowInstance | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` … | gated `APPROVAL_ACT`; opens modal first |

**Data it reads**: `listSlaEscalationBottleneck` (onLoad, What is escalating now)

**Where the user goes next**

- → `BO-384` Delegation & Escalation Command Center: *Back to Delegation & Escalation Command Center*; carries `instanceId`
- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `listSlaEscalationBottleneck`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The live escalation operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the live escalation operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No live escalation operations yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the live escalation operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not … |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_ACT for Act on workflow instance. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*
- **actOnWorkflowInstance answers 409**: Show it as something the person can act on, not a failure: The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step to skip is an approval node *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*
- **actOnWorkflowInstance answers 422**: Show it as something the person can act on, not a failure: A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not an allowed edge, or the assignee is the requester of the approval *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listSlaEscalationBottleneck (SlaEscalationBottleneckMonitorView):
- started: 01/10/2026 09:14
  target: 01/10/2026 09:14
  timeRemaining: 12
- started: 30/09/2026 18:02
  target: 30/09/2026 18:02
  timeRemaining: 3
```

#### Permissions

- `listSlaEscalationBottleneck` → `APPROVAL_VIEW` (read) · staff
- `actOnWorkflowInstance` → `APPROVAL_ACT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- SLA rules set how fast a request must be approved (e.g. within one day); if not actioned it auto-escalates to the next level so someone can investigate (e.g. approver on leave) and reassign. *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-724)*

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-391` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-391`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 5
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 14: Works in Live Escalation Operations Center → Allow managers to monitor and intervene in currently escalated approvals.
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 8: Works in SLA, Escalation & Bottleneck Monitor → Monitor workflows approaching or exceeding configured time limits.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-391?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Act on workflow instance.
- [ ] Every transition is wired: `BO-384`, `ADM-248`.
- [ ] Every gated control is gated: `APPROVAL_ACT`, `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-392` SLA & Escalation Performance Analytics

**Provide management with analytics about where approval delays and escalations occur. The source explicitly requires escalation reporting and escalation trend analytics.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Identify) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/sla-escalation-performance-analytics-bo-392` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Where approval delays and escalations occur: slowest approvers, stages, workflows, venues, peak periods.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The table's columns are the workshop pack's labels with no bound response field (0 of 6 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every sla escalation performance** (data table)

| Shows | Format | Notes |
|---|---|---|
| Slowest approvers | text | not in the schema: `Slowest approvers` |
| Slowest stages | text | not in the schema: `Slowest stages` |
| Slowest workflows | text | not in the schema: `Slowest workflows` |
| High escalation venues | text | not in the schema: `High-escalation venues` |
| High escalation departments | text | not in the schema: `High-escalation departments` |
| Peak approval periods | text | not in the schema: `Peak approval periods` |

**The selected sla escalation performance** (detail panel): The pack groups this record's detail under its own headings: “SLA Compliance”, “Average Response”, “Escalation Rate”, “Breach Rate”, “SLA by Department”, “Escalations by Reason”.

| Shows | Format | Notes |
|---|---|---|
| Slowest approvers | text | not in the schema: `Slowest approvers` |
| Slowest stages | text | not in the schema: `Slowest stages` |
| Slowest workflows | text | not in the schema: `Slowest workflows` |
| High escalation venues | text | not in the schema: `High-escalation venues` |
| High escalation departments | text | not in the schema: `High-escalation departments` |
| Peak approval periods | text | not in the schema: `Peak approval periods` |

**Data it reads**: `getApprovalAnalytics` (onLoad, SLA and escalation performance)

**Where the user goes next**

- → `BO-384` Delegation & Escalation Command Center: *Back to Delegation & Escalation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sla escalation performance list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sla escalation performance untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sla escalation performance yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sla escalation performance are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every sla escalation performance:
- Slowest approvers: Rahul Menon
  Slowest stages: 1.8 s
  Slowest workflows: 128
  High-escalation venues: 128
  High-escalation departments: Ticketing
  Peak approval periods: 233
- Slowest approvers: Fatima Al Mansoori
  Slowest stages: 3 h 20 min
  Slowest workflows: 42
  High-escalation venues: 42
  High-escalation departments: F&B
  Peak approval periods: 57
- Slowest approvers: Omar Haddad
  Slowest stages: 42 min
  Slowest workflows: 7
  High-escalation venues: 7
  High-escalation departments: Retail
  Peak approval periods: 11
```

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-392` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-392`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 5
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 16: Works in SLA & Escalation Performance Analytics → Provide management with analytics about where approval delays and escalations occur. The source explicitly requires escalation reporting and escalation trend analytics.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-392?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-384`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-393` AI SLA & Escalation Advisor

**Use AI to predict approval bottlenecks and recommend preventive actions before SLAs are breached. The matrix specifically requires AI escalation recommendations.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Venue Operations · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_REQUEST`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `requestId` (navigation) |
| Route | `/venue-operations/ai-sla-escalation-advisor-bo-393` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI predictions of approval bottlenecks with recommended preventive actions; a recommendation becomes a draft change that goes for approval, never applied directly.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Analyse from | date picker | — | — | — | — | Sends `?from=`; the window runs to now. | — |
| Group by | select field | — | — | — | — | Sends `?groupBy=` (kind, approver, venue, day, week). The pack's slowest stages, workflows, venues and departments (page 47) are these groupings; stage and department are not among them. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date picker | — | — | `getApprovalAnalytics` ?from |
| Group by | radio group | — | Kind · Approver · Venue · Day · Week | `getApprovalAnalytics` ?groupBy |
| Assigned to me | toggle | — | — | `listApprovalRequests` ?assignedToMe |
| Raised by me | toggle | — | — | `listApprovalRequests` ?raisedByMe |
| Status | select | — | Draft · Pending · Escalated · Returned · Information requested · Approved · Rejected · Withdrawn · Expired · Cancelled | `listApprovalRequests` ?status |
| Kind | select | — | Refund · Price override · Discount override · Complimentary ticket · Membership cancellation · Access permission change · Configuration change · AI recommendation · Release promotion · Requisition · Stock write off · Journal entry …; Each is an existing kind … | `listApprovalRequests` ?kind |
| Breaching within minutes | number field (minutes) | — | — | `listApprovalRequests` ?breachingWithinMinutes |
| Sort | segmented control | Sla proximity | Sla proximity · AI priority | `listApprovalRequests` ?sort |

#### Outputs: what the screen shows and produces

**Shown**

**SLA breaches** (metric tile, from `getApprovalAnalytics`): Summed across the returned rows.

| Shows | Format | Notes |
|---|---|---|
| Sla breached | 1,234 | — |

**Escalated** (metric tile, from `getApprovalAnalytics`): Summed across the returned rows.

| Shows | Format | Notes |
|---|---|---|
| Escalated | 1,234 | — |

**Predicted SLA breaches (next 60 min)** (metric tile): The pack's headline prediction ("16 requests likely to breach"); nothing in the contract forecasts breaches.

| Shows | Format | Notes |
|---|---|---|
| Predicted SLA breaches (next 60 min) | text | not in the schema: `Predicted SLA breaches (next 60 min)` |

**Predicted average wait time** (metric tile): The pack's expected-impact figure (48 min to 27 min); the contract reports only observed median and p95.

| Shows | Format | Notes |
|---|---|---|
| Predicted average wait time | text | not in the schema: `Predicted average wait time` |

**Approval throughput by group** (data table, from `getApprovalAnalytics`): One row per `groupBy` key; the advisor ranks the slowest first.

| Shows | Format | Notes |
|---|---|---|
| Key | text | — |
| Raised | 1,234 | — |
| Approved | 1,234 | — |
| Rejected | 1,234 | — |
| Withdrawn | 1,234 | — |
| Expired | 1,234 | Requests nobody answered. Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person. |
| Escalated | 1,234 | — |
| Sla breached | 1,234 | — |
| Median minutes | 1,234.5 | — |
| P95 minutes | 1,234.5 | — |

**The selected AI recommendation** (detail panel): No operation returns AI recommendations; every field here is a pack label.

| Shows | Format | Notes |
|---|---|---|
| Predicted SLA risk | text | not in the schema: `Predicted SLA risk` |
| Pending approvals | text | not in the schema: `Pending approvals` |
| Predicted breaches | text | not in the schema: `Predicted breaches` |
| Recommendation | text | not in the schema: `Recommendation` |
| Expected impact: predicted breaches | text | not in the schema: `Expected impact: predicted breaches` |
| Expected impact: average wait time | text | not in the schema: `Expected impact: average wait time` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Simulate recommendation (secondary button) | navigation or local | — | — | — | — |
| Create draft change (secondary button) | navigation or local | — | — | — | — |
| Send for approval (primary button) | navigation or local | — | — | — | — |
| Dismiss (destructive button) | navigation or local | — | — | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Create draft change / Send for approval**: Creates a draft; nothing changes until approved. *(source: ADR-0050)*

**Data it reads**: `getApprovalAnalytics` (onLoad, Where the SLA is failing); `listApprovalRequests` (onLoad, Pending requests with AI escalation suggestions …)

**Where the user goes next**

- → `BO-384` Delegation & Escalation Command Center: *Back to Delegation & Escalation Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sla escalation advisor list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sla escalation advisor untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sla escalation advisor yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sla escalation advisor are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_REQUEST for escalateApprovalRequest. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#escalateApprovalRequest)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  SLA breaches: 3 h 20 min
  Escalated: 46
  Predicted SLA breaches (next 60 min): 1.8 s
  Predicted average wait time: 3 h 20 min
```

#### Permissions

- `getApprovalAnalytics` → `APPROVAL_VIEW` (read) · staff
- `listApprovalRequests` → `APPROVAL_VIEW` (read) · staff, public
- `escalateApprovalRequest` → `APPROVAL_REQUEST` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.55 | Regulatory Audit Support - System shall provide approval records suitable for regulatory audits. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.56 | Immutable Approval Records - System shall prevent modification of completed approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.62 | Approval Tamper Detection - System shall detect unauthorized modification attempts on approval records. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 11.1.74 | AI Priority Scoring - System shall prioritize approval requests using AI scoring. | Approval Workflows & Governance | CONTRACTED | `listApprovalRequests` |
| 18.6.1 | Approval Inbox - Users shall view pending approvals. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.2 | Approval Actions - Authorized users shall approve or reject requests. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 18.6.3 | Approval Comments - Users shall submit approval comments. | Employee Mobile App & AI Assistant | CONTRACTED | `listApprovalRequests` |
| 11.1.47 | Multi-Level Escalation - System shall support escalation through multiple organizational levels. | Approval Workflows & Governance | CONTRACTED | `escalateApprovalRequest` |
| 11.1.48 | Escalation History - System shall maintain complete escalation history. | Approval Workflows & Governance | CONTRACTED | `escalateApprovalRequest` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P08 · Venue Operations, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-393` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS34 Approval Workflows and Governance Board 5.dc.html#bo-393`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 5
- Flow F127 *Approval Workflows and Governance board 5: Delegation & Escalation Command …*, step 18: Works in AI SLA & Escalation Advisor → Use AI to predict approval bottlenecks and recommend preventive actions before SLAs are breached. The matrix specifically requires AI escalation recommendations.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-393?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Simulate recommendation, Create draft change, Send for approval, Dismiss.
- [ ] Every transition is wired: `BO-384`.
- [ ] Every gated control is gated: `APPROVAL_REQUEST`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
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

### In P08 · Venue Operations

- Allam/Qossai: the workstation/till/POS wireframes are reference only (partly ChatGPT-generated, with errors) and not to be replicated; Softlabs may consolidate dashboards freely and must cross-check the functionality matrix for missing items. *(agreed · MoM 14 Aug 2026, 11. Wireframe Walkthrough — Workstation, Till & POS Management · DI-312)*

**7 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"actOnWorkflowInstance": {"method":"POST","path":"/workflow-instances/{instanceId}/actions","contract":"approvals","summary":"An operator's intervention in a running workflow","permission":"APPROVAL_ACT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkflowInstanceActionInput","responds":"WorkflowInstance"},
"createApprovalDelegation": {"method":"POST","path":"/delegations","contract":"approvals","summary":"Delegate approval authority","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalDelegation","responds":"ApprovalDelegation"},
"escalateApprovalRequest": {"method":"POST","path":"/approval-requests/{requestId}/escalate","contract":"approvals","summary":"Move it up a level","permission":"APPROVAL_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApprovalRequest"},
"getApprovalAnalytics": {"method":"GET","path":"/approval-analytics","contract":"approvals","summary":"Volumes, times, rejections and bottlenecks","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"from","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"ApprovalAnalytics"},
"listApprovalDelegations": {"method":"GET","path":"/delegations","contract":"approvals","summary":"Who is standing in for whom","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ApprovalDelegation"},
"listApprovalRequests": {"method":"GET","path":"/approval-requests","contract":"approvals","summary":"Requests awaiting a decision, or already decided","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToMe","in":"query","required":null},{"name":"raisedByMe","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"breachingWithinMinutes","in":"query","required":null},{"name":"sort","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSlaEscalationBottleneck": {"method":"GET","path":"/sla-escalation-bottleneck","contract":"approvals","summary":"SLA, Escalation & Bottleneck Monitor","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workflow","in":"query","required":false},{"name":"risk","in":"query","required":false},{"name":"escalationLevel","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"revokeApprovalDelegation": {"method":"DELETE","path":"/delegations/{delegationId}","contract":"approvals","summary":"End a delegation early","permission":"APPROVAL_DECIDE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setApprovalSlaPolicy": {"method":"PUT","path":"/approval-sla-policies","contract":"approvals","summary":"How long a decision may take, and what happens when it does not","permission":"APPROVAL_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalSlaPolicy","responds":"ApprovalSlaPolicy"},
"setApproverAvailability": {"method":"PUT","path":"/approval-delegations/availability","contract":"approvals","summary":"Out of office, and who decides instead","permission":"APPROVAL_DECIDE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApproverAvailability","responds":"ApproverAvailability"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalAnalytics": {"type":"object","x-ticvai-persistence":"none — aggregated from approvals.request","properties":{"from":{"type":"string","format":"date"},"to":{"type":"string","format":"date"},"groupBy":{"type":"string","description":"The grouping asked for, as the `groupBy` query parameter; each row's `key` is one value of it.","enum":["kind","approver","venue","day","week"]},"rows":{"type":"array","items":{"type":"object","properties":{"key":{"type":"string"},"raised":{"type":"integer"},"approved":{"type":"integer"},"rejected":{"type":"integer"},"withdrawn":{"type":"integer"},"expired":{"type":"integer","description":"**Requests nobody answered.** Usually a routing defect rather than a busy approver, and the number that says the matrix names the wrong person.\n"},"escalated":{"type":"integer"},"slaBreached":{"type":"integer"},"medianMinutes":{"type":"number"},"p95Minutes":{"type":"number"}}}}}},
"ApprovalDecision": {"type":"object","x-ticvai-persistence":"approvals.decision","required":["level","principalId","decision","decidedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"level":{"type":"integer"},"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"},"delegatedFrom":{"type":"string","format":"uuid","nullable":true},"decision":{"type":"string","enum":["approve","reject"]},"comment":{"type":"string","nullable":true},"reason":{"type":"string","nullable":true},"usedMfa":{"type":"boolean"},"signatureRef":{"type":"string","nullable":true},"decidedAt":{"type":"string","format":"date-time"}}},
"ApprovalDelegation": {"type":"object","x-ticvai-persistence":"approvals.delegation","required":["delegatorPrincipalId","delegatePrincipalId","from","to"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"delegatorPrincipalId":{"type":"string","format":"uuid","description":"A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and `identity.getPrincipal`.\n"},"delegatePrincipalId":{"type":"string","format":"uuid","description":"A principal id, resolved to a name the same way as `delegatorPrincipalId`."},"kinds":{"type":"array","description":"Absent means everything the delegator may approve.","items":{"$ref":"#/components/schemas/ApprovalKind"}},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"A delegate may be given less authority than the delegator, never more."},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time","description":"**Required.** An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it.\n"},"reason":{"type":"string"},"isActive":{"type":"boolean","readOnly":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMode": {"type":"string","description":"11.1.43–11.1.46. **Sequential** asks one at a time, **parallel** asks everyone at once, **consensus** needs all of them, **majority** needs more than half.\nParallel and consensus differ in when it completes: parallel completes on the first approval, consensus waits for all. Conflating them is how a four-eyes rule turns into a one-eye rule.\n","enum":["sequential","parallel","consensus","majority"]},
"ApprovalRequest": {"type":"object","x-ticvai-persistence":"approvals.request","required":["id","kind","status","requestedByPrincipalId","requestedAt"],"properties":{"id":{"type":"string"},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"rerouteOnNoApprover":{"type":"boolean","default":true,"description":"BL-154. **An approver on leave is an approval that waits for them to come back.** Reroutes to the next in the chain rather than stalling — `workforce` already knows who is on leave, and an approval queue nobody is watching is the thing that stops a venue.\n"},"outOfOfficeDelegateId":{"type":"string","format":"uuid","nullable":true},"allowEmailApproval":{"type":"boolean","default":false,"description":"**Approving from an email link with no second factor is the weakest path in the system**, so it is off by default and available only below a configured value.\n"},"reopenedFrom":{"type":"string","format":"uuid","nullable":true,"description":"**Reopening a decided approval creates a new one that points back.** Editing a decision in place destroys the record of what was originally approved, which is the only thing an audit wants.\n"},"status":{"$ref":"#/components/schemas/ApprovalStatus"},"subjectContract":{"type":"string"},"subjectType":{"type":"string"},"subjectId":{"type":"string"},"scopePath":{"type":"string"},"summary":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"justification":{"type":"string","nullable":true},"requestedByPrincipalId":{"type":"string","format":"uuid"},"matrixVersion":{"type":"integer"},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"currentLevel":{"type":"integer"},"totalLevels":{"type":"integer"},"pendingApprovers":{"type":"array","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"isDelegate":{"type":"boolean"}}}},"decisions":{"type":"array","description":"Every decision at every level, in order. **Immutable once the request completes** (11.1.56) — an approval is evidence, and amending one is a different fact.\n","items":{"$ref":"#/components/schemas/ApprovalDecision"}},"escalations":{"type":"array","description":"11.1.48. Who was asked, when, and why it moved up. **Escalation adds an approver rather than replacing one**, so the original stays in the record.\n","items":{"type":"object","properties":{"at":{"type":"string","format":"date-time"},"reason":{"type":"string"},"fromLevel":{"type":"integer"},"toLevel":{"type":"integer"},"wasAutomatic":{"type":"boolean"}}}},"resubmittedFromId":{"type":"string","nullable":true},"reopenedFromId":{"type":"string","nullable":true},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Who claimed or was assigned the request in a shared queue (`assignApprovalRequest`; DI-723; CHG-CSP-042). Null while it sits in the queue."},"assignedToDepartmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The department queue it was assigned to, where it went to a department rather than a person (CHG-CSP-042)."},"assignedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"requestedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"aiAssessment":{"type":"object","nullable":true,"readOnly":true,"description":"**AI context for the reviewer, never an input to the decision** (11.1.73 to 11.1.75; MoM 8 September; 29 September, build pass, group G2). Written by approvals from `ai.scoreApprovalRequest` on submit and on each SLA tick; null where AI is off or has not answered. Shown on the request labelled as AI; orders the inbox only when `sort=aiPriority` is asked for.","properties":{"riskScore":{"type":"integer","minimum":0,"maximum":100},"riskBand":{"type":"string","enum":["low","medium","high","critical"]},"priorityScore":{"type":"integer","minimum":0,"maximum":100},"escalationSuggestion":{"type":"object","description":"A suggestion a person may act on through `escalateApprovalRequest`, or the tenant's own SLA policy may; nothing escalates because of it.","properties":{"action":{"type":"string","enum":["escalate","addBackupApprover","none"]},"reason":{"type":"string","nullable":true}}},"signals":{"type":"array","maxItems":10,"description":"The signals behind the scores, largest first, as `ai.AiApprovalRequestScore.signals`.","items":{"type":"object","properties":{"code":{"type":"string"},"contribution":{"type":"number"},"detail":{"type":"string","nullable":true}}}},"scoreId":{"type":"string","format":"uuid","description":"The `ai.approval_request_score` row it was copied from; `ai.getApprovalRequestScore` gives the full context. Not a foreign key (the score lives in the AI service)."},"decisionRecordId":{"type":"string","description":"The ai decision record, for the audit of what the AI said and why."},"assessedAt":{"type":"string","format":"date-time"}}}}},
"ApprovalSlaPolicy": {"type":"object","x-ticvai-persistence":"approvals.sla_policy","description":"Approvals boards 5.5 and 5.6. **A target with no consequence is a number in a table**, so the reminder and breach behaviour are part of the policy.\n","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"targetMinutes":{"type":"integer"},"businessHoursOnly":{"type":"boolean","default":true,"description":"**A four-hour SLA starting at five in the afternoon is breached by nine the next morning with nobody having done anything wrong.**\n"},"calendarId":{"type":"string","format":"uuid","nullable":true},"reminders":{"type":"array","items":{"type":"object","properties":{"atPercentOfTarget":{"type":"integer"},"notify":{"type":"string","enum":["approver","approverManager","requester","escalationGroup"]}}}},"firstReminderAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"**Percent of `targetMinutes` at which the first reminder goes** (decided 29 September, readiness close-out: the reminder steps are percentages of target). A column so the SLA, Escalation, Reminder & Timeout Rules screen reads it rather than unpacking `reminders`; the reminder in `reminders` at this percentage says whom it notifies (data model for the agreed operations, 29 September)."},"secondReminderAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Percent of `targetMinutes` at which the second reminder goes; above `firstReminderAtPercent`"},"escalateAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Percent of `targetMinutes` at which the request or workflow escalates; at or above `secondReminderAtPercent`"},"onBreach":{"type":"string","enum":["notifyOnly","escalate","autoApprove","autoReject"],"default":"escalate"},"autoActionAllowed":{"type":"boolean","default":false,"description":"**Auto-approval on breach is off unless somebody says otherwise, in writing.** A queue that approves itself when nobody looks is not an approval process.\n"},"escalationGroupId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"ApprovalStatus": {"type":"string","enum":["draft","pending","escalated","returned","informationRequested","approved","rejected","withdrawn","expired","cancelled"]},
"ApproverAvailability": {"type":"object","x-ticvai-persistence":"approvals.approver_availability","description":"Approvals boards 5.3 and 5.4. **Dated, so nobody has to remember to turn it off.**","properties":{"id":{"type":"string","format":"uuid","description":"One period of absence. The key `setApproverAvailability` replaces by; absent on input to record a new period. Already the table's key (`approvals.approver_availability.id`), and until 26 September missing from the wire, so no period could be addressed.\n"},"principalId":{"type":"string","format":"uuid"},"unavailableFrom":{"type":"string","format":"date-time"},"unavailableTo":{"type":"string","format":"date-time"},"substitutePrincipalId":{"type":"string","format":"uuid","nullable":true},"delegationId":{"type":"string","format":"uuid","nullable":true},"reason":{"type":"string","nullable":true},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"scopePath":{"type":"string"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SlaEscalationBottleneckMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_instance, whose SLA and reminder timestamps it lists (data model for the agreed operations, 29 September)","description":"**What SLA, Escalation & Bottleneck Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflow":{"type":"string","description":"Workflow"},"instance":{"type":"string","description":"Instance"},"currentStep":{"type":"string","description":"Current Step"},"owner":{"type":"string","description":"Owner"},"started":{"type":"string","format":"date-time","description":"Started"},"target":{"type":"string","format":"date-time","description":"SLA deadline"},"timeRemaining":{"type":"integer","description":"Minutes until breach; negative once breached"},"risk":{"type":"string","description":"Risk"},"escalationLevel":{"type":"string","description":"Escalation Level"},"firstReminder":{"type":"string","format":"date-time","description":"First Reminder"},"secondReminder":{"type":"string","format":"date-time","description":"Second Reminder"},"managerEscalation":{"type":"string","format":"date-time","description":"Manager Escalation"},"executiveEscalation":{"type":"string","format":"date-time","description":"Executive Escalation"},"finalOutcome":{"type":"string","description":"Final Outcome"}},"required":["instance"]},
"SlaEscalationBottleneckMonitorViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"withinSla":{"type":"integer","description":"Within SLA"},"atRisk":{"type":"integer","description":"At Risk"},"breached":{"type":"integer","description":"Breached"},"escalated":{"type":"integer","description":"Escalated"},"averageProcessingTime":{"type":"integer","description":"Minutes"},"averageApprovalTime":{"type":"integer","description":"Minutes"},"longestWaitingStep":{"type":"string","description":"Longest Waiting Step"}}},
"WorkflowInstance": {"type":"object","x-ticvai-persistence":"approvals.workflow_instance","description":"**One running workflow** (pack 13.2.1, 13.2.3 and 13.2.5; data model for the agreed operations, 29 September). Started by a `WorkflowTrigger`, on the version in force at that moment and kept on it to the end (audit R129). Its steps are `WorkflowStepExecution` rows, keyed by the same `correlationId` the participating services trace with. **The SLA clock and its reminder and escalation timestamps are held here**, not in a table of their own: there is one clock per instance, and the SLA, Escalation & Bottleneck Monitor lists instances. Lifecycle in `states/workflow-instance.yaml`. The engine writes this row; an operator changes it only through `actOnWorkflowInstance`, which keeps each change as a `WorkflowIntervention` (decided 29 September, writers pass).","required":["id","workflowDefinitionId","workflowVersionId","sourceModule","status","correlationId","startedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"workflowDefinitionId":{"type":"string","format":"uuid"},"workflowVersionId":{"type":"string","format":"uuid","description":"The version the instance started on; never changes"},"workflowTriggerId":{"type":"string","format":"uuid","nullable":true},"sourceModule":{"$ref":"#/components/schemas/WorkflowModule"},"businessObjectType":{"type":"string","maxLength":100,"nullable":true},"businessObjectId":{"type":"string","nullable":true,"description":"**A reference, never a copy**, as `ApprovalRequest.subjectId`"},"initiatedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Null when a system event or schedule started it"},"ownerPrincipalId":{"type":"string","format":"uuid","nullable":true},"priority":{"type":"string","maxLength":30,"nullable":true},"currentNodeId":{"type":"string","nullable":true,"description":"The node of the version's graph the instance is at"},"status":{"$ref":"#/components/schemas/WorkflowInstanceStatus"},"correlationId":{"type":"string","maxLength":100,"description":"The shared correlation id every participating service logs, for distributed tracing"},"slaPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The `ApprovalSlaPolicy` whose clock runs on this instance"},"slaDueAt":{"type":"string","format":"date-time","nullable":true},"slaBreached":{"type":"boolean","default":false},"escalationLevel":{"type":"integer","minimum":0,"default":0},"firstReminderAt":{"type":"string","format":"date-time","nullable":true},"secondReminderAt":{"type":"string","format":"date-time","nullable":true},"managerEscalatedAt":{"type":"string","format":"date-time","nullable":true},"executiveEscalatedAt":{"type":"string","format":"date-time","nullable":true},"slaOutcome":{"type":"string","enum":["metWithinTarget","metAfterReminder","metAfterEscalation","breached"],"nullable":true,"description":"How the instance finished against its SLA; set on completion (the monitor's Final Outcome)"},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"The partition key (ADR-0005). Written at venue scope"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"WorkflowInstanceActionInput": {"type":"object","x-ticvai-persistence":"none — request only; writes approvals.workflow_intervention (schema WorkflowIntervention) (decided 29 September, writers pass)","description":"One operator action on a running workflow instance (decided 29 September, writers pass).","required":["action","reason"],"properties":{"action":{"$ref":"#/components/schemas/WorkflowInterventionAction"},"reason":{"type":"string","minLength":1,"maxLength":500,"description":"Mandatory for every action (pack 13.2.5, \"actions capture a mandatory reason\")"},"workflowStepExecutionId":{"type":"string","format":"uuid","nullable":true,"description":"The step acted on; for `retryStep` the step to retry from. Defaults to the instance's current step"},"workflowExceptionId":{"type":"string","format":"uuid","nullable":true,"description":"The exception the action is taken from; required for `escalateException`"},"assigneePrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Required for `reassign`, `addBackupApprover` and `escalateException`"},"alternativeNodeId":{"type":"string","nullable":true,"description":"For `skipStep`, the node to continue at instead of the next one (Use Approved Alternative)"},"correctedInput":{"type":"object","additionalProperties":true,"nullable":true,"description":"For `resume`, the corrected input of the failed step (Correct Data)"},"extendByMinutes":{"type":"integer","minimum":1,"maximum":43200,"nullable":true,"description":"Required for `extendSla`"},"priority":{"type":"string","maxLength":30,"nullable":true,"description":"Required for `changePriority`"}}},
"WorkflowInstanceStatus": {"type":"string","description":"Where one running workflow stands (pack 13.2.1 and 13.2.3; decided 29 September, readiness close-out). Modelled in `states/workflow-instance.yaml`.","enum":["running","waitingApproval","waitingTask","waitingSystem","escalated","failed","completed","cancelled"]},
"WorkflowInterventionAction": {"type":"string","description":"What an operator did to a running workflow instance (pack 13.2.3, 13.2.4 and 13.2.5; decided 29 September, writers pass). The effect of each is on `actOnWorkflowInstance`.","enum":["reassign","retryStep","skipStep","resume","cancel","extendSla","addBackupApprover","changePriority","escalateException"]},
"WorkflowModule": {"type":"string","description":"The module a workflow, rule or automation belongs to and a workflow instance originates from. The same values as `WorkflowOperationsCommandCenterView.module` (decided 29 September, readiness close-out), named so the workflow engine's tables share one vocabulary (data model for the agreed operations, 29 September).","enum":["ticketing","pricing","finance","procurement","crm","resourceManagement","fnb","retail","groupSales","customerService","membership","wallet","waiver","subscriptionLicensing"]}
}
```
