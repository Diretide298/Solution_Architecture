# WS55 — Rules  Workflow  Approval   Automation Engine board 1

**10 screens · 14 operations · 22 schemas · 3 permissions**

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
| `ADM-238` | Rules & Workflow Command Center | B–D | 0 | 14 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-239` | Visual Business Rule Builder | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-240` | Conditions, Decision Logic & Decision Tables | B–D | 0 | 0 | 6 | 0 | 0 | 1 | — | notStarted (generated) |
| `ADM-241` | Visual Workflow Designer | B–D | 21 | 12 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-242` | Approval Matrix & Multi-Level Approval Configuration | B–D | 7 | 0 | 5 | 0 | 0 | 3 | — | notStarted (generated) |
| `ADM-243` | Roles, Authority, Delegation & Approval Limits | A | 14 | 0 | 5 | 51 | 0 | 6 | — | notStarted (generated) |
| `ADM-244` | SLA, Escalation, Reminder & Timeout Rules | B–D | 21 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-245` | Trigger, Action & Cross-Module Orchestration Configuration | B–D | 12 | 0 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-246` | Workflow Testing, Simulation & Impact Analysis | B–D | 0 | 16 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-247` | Versioning, Governance, Approval & Publication | B–D | 25 | 20 | 6 | 0 | 0 | 3 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-239, ADM-240 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-238` Rules & Workflow Command Center

**Provide administrators with a centralized portfolio of all business rules, workflows, approvals and automations configured across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§Each configuration should show) — counts over a population, then the population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/rules-workflow-command-center-adm-238` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The rules and workflow board's hub: every business rule, workflow, approval and automation with its module, version, owner, effective date and status; counts of drafts, pending approval, scheduled changes, errors and warnings.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listRuleWorkflow (APPROVAL_VIEW). (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

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
| Name | text | Name |
| Type | chip: Business rule, Approval workflow, Operational workflow, Decision rule, Validation … | Kind of configuration |
| Source module | text | Source Module |
| Business process | text | Business Process |
| Effective date | 1 Oct 2026, 14:30 | Effective Date |
| Status | chip: Draft, Testing, Review, Pending approval, Approved, Scheduled… | Lifecycle status |

**The selected rules workflow** (detail panel): The pack groups this record's detail under its own headings: “Classify as”.

| Shows | Format | Notes |
|---|---|---|
| Name | text | Name |
| Type | chip: Business rule, Approval workflow, Operational workflow, Decision rule, Validation … | Kind of configuration |
| Source module | text | Source Module |
| Business process | text | Business Process |
| Owner | text | Owner |
| Effective date | 1 Oct 2026, 14:30 | Effective Date |
| Status | chip: Draft, Testing, Review, Pending approval, Approved, Scheduled… | Lifecycle status |
| Last modified | 1 Oct 2026, 14:30 | Last Modified |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Status**: Draft, pending approval, scheduled, active, suspended, retired; errors and warnings counted and filterable. *(source: contracts/spine/approvals.yaml#listRuleWorkflow)*

**Data it reads**: `listRuleWorkflow` (onLoad, Rules & Workflow Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-239` Visual Business Rule Builder: *Works in Visual Business Rule Builder*; calls `listRuleWorkflow`
- → `ADM-240` Conditions, Decision Logic & Decision Tables: *Works in Conditions, Decision Logic & Decision Tables*; calls `listRuleWorkflow`
- → `ADM-241` Visual Workflow Designer: *Works in Visual Workflow Designer*; calls `listRuleWorkflow`
- → `ADM-242` Approval Matrix & Multi-Level Approval Configuration: *Works in Approval Matrix & Multi-Level Approval Configuration*; calls `listRuleWorkflow`
- → `ADM-243` Roles, Authority, Delegation & Approval Limits: *Works in Roles, Authority, Delegation & Approval Limits*; calls `listRuleWorkflow`
- → `ADM-244` SLA, Escalation, Reminder & Timeout Rules: *Works in SLA, Escalation, Reminder & Timeout Rules*; calls `listRuleWorkflow`
- → `ADM-245` Trigger, Action & Cross-Module Orchestration Configuration: *Works in Trigger, Action & Cross-Module Orchestration Configuration*; calls `listRuleWorkflow`
- → `ADM-246` Workflow Testing, Simulation & Impact Analysis: *Works in Workflow Testing, Simulation & Impact Analysis*; calls `listRuleWorkflow`
- → `ADM-247` Versioning, Governance, Approval & Publication: *Works in Versioning, Governance, Approval & Publication*; calls `listRuleWorkflow`
- → `BO-086` Approval Matrix: *Works in Approval Matrix & Multi-Level Approval Configuration*; calls `listRuleWorkflow`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rules workflow list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rules workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rules workflow yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rules workflow are still there. The pack's own statuses are Suspended → Retired — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Active Rules: 128
  Active Workflows: 46
  Approval Workflows: 312
  Draft Configurations: 74
  Pending Approval: 19
  Scheduled Changes: 233
  Rules With Errors: 0
  Workflows With Warnings: 5
  Recently Modified: 128
  Modules Covered: 46
Every rules workflow:
- name: Refund above AED 500 - Abu Dhabi
  type: standard
  effectiveDate: 01/10/2026 09:14
  status: active
- name: Group discount approval
  type: standard
  effectiveDate: 30/09/2026 18:02
  status: pending
- name: Purchase order over AED 10,000
  type: override
  effectiveDate: 28/09/2026 11:45
  status: suspended
```

#### Permissions

- `listRuleWorkflow` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Workshop packs group screens ten to a board, each opened by a command centre; that grouping is the navigation: the nine detail screens are reached from the board's hub and return to it. *(agreed · screen note 4 Sep 2026, BO-144 and the other board hubs · DI-653)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-238` · status **notStarted** · provenance generated
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
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-238?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-239`, `ADM-240`, `ADM-241`, `ADM-242`, `ADM-243`, `ADM-244`, `ADM-245`, `ADM-246`, `ADM-247`, `BO-086`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-239` Visual Business Rule Builder

**Allow administrators to create business rules without software development.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/visual-business-rule-builder-adm-239` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Build an IF/THEN business rule without code: condition groups on business fields, then actions; tested in the simulator before publication.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: setVisualBusinessRule (APPROVAL_CONFIGURE). (CHG-MOV-001).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setVisualBusinessRule: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setVisualBusinessRule)*

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

#### Consistency with other screens

- Match `ADM-246`: Every rule is tested there before publishing.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
rule: Large refund needs manager
when: refund amount > AED 500 AND channel = POS
then: create approval request (Venue Manager)
```

#### Permissions

- `setVisualBusinessRule` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-239` · status **notStarted** · provenance generated
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
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/conditions-decision-logic-decision-tables-adm-240` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Decision tables and compound conditions where a simple rule is not enough; rows evaluated in order, first match wins.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listConditionDecisionLogic (APPROVAL_VIEW). (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

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
| Empty, first run (`?state=emptyFirstRun`) | No conditions decision logic yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the conditions decision logic are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listConditionDecisionLogic (ConditionsDecisionLogicDecisionTablesView):
- name: Refund above AED 500 - Abu Dhabi
  resolutionStrategy: priority
  onMatch: stopProcessing
- name: Group discount approval
  resolutionStrategy: sequence
  onMatch: continueEvaluation
```

#### Permissions

- `listConditionDecisionLogic` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A85** Design the table management module for fine dining: visual floor/table map with VIP tagging, table status flow (Available → Ordered → Table Closed → Reserved), reservations with deposit and waitlist, a per-table … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'table management')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-240` · status **notStarted** · provenance generated
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
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/visual-workflow-designer-adm-241` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Design a whole workflow on a canvas: trigger, steps, approvals, actions, branches; name, module, owner, version, priority and effective dates.

**Fixed on main** (the package already carries these; draw what it says): No canvas component is declared; only form fields. (CHG-SBO-023); Calls tenant-permission operations with no tenant picker and no platform-staff grant: setVisualWorkflow (APPROVAL_CONFIGURE). (CHG-MOV-001); Fields drawn as drop-downs that cannot be choices: text field: Workflow Name, Module, Business Process, Owner, Version, Priority, Effective … (CHG-MOV-005).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workflow Name | text field | optional | — | — | — | Workflow Name | `VisualWorkflowDesignerInput.workflowName` |
| Module | text field | optional | — | — | — | Module | `VisualWorkflowDesignerInput.module` |
| Business Process | text field | optional | — | — | — | Business Process | `VisualWorkflowDesignerInput.businessProcess` |
| Owner | text field | optional | — | — | — | Owner | `VisualWorkflowDesignerInput.owner` |
| Trigger | select field | — | — | — | — | — | — |
| Version | text field | optional | — | — | — | Version | `VisualWorkflowDesignerInput.version` |
| Priority | text field | optional | — | — | — | Priority | `VisualWorkflowDesignerInput.priority` |
| Effective Dates | text field | optional | — | — | — | From and to: effectiveFrom and effectiveTo on VisualWorkflowDesignerInput. | `VisualWorkflowDesignerInput.effectiveFrom` |

**Sent by *Save changes*** (`setVisualWorkflow`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Definition `definition` | text field | required | — | — | — | The workflow graph (nodes and connections) as a JSON document | `setVisualWorkflow` body |
| Node types `nodeTypes` | multi-select chips | optional | — | Start · Trigger · Task · Decision · Approval · System action · Notification · Wait · Timer · Parallel branch · Merge · Escalation … | — | Node kinds used in this workflow | `setVisualWorkflow` body |
| Workflow name `workflowName` | text field | required | — | — | — | Workflow Name | `setVisualWorkflow` body |
| Module `module` | text field | required | — | — | — | Module | `setVisualWorkflow` body |
| Business process `businessProcess` | text field | optional | — | — | — | Business Process | `setVisualWorkflow` body |
| Owner `owner` | text field | optional | — | — | — | Owner | `setVisualWorkflow` body |
| Version `version` | text field | optional | — | — | — | Version | `setVisualWorkflow` body |
| Priority `priority` | text field | optional | — | — | — | Priority | `setVisualWorkflow` body |
| Effective from `effectiveFrom` | text field | optional | — | — | — | Effective Dates | `setVisualWorkflow` body |
| Validation issues `validationIssues` | multi-select chips | optional | — | Dead ends · Missing outcomes · Circular loops · Missing assignee · Invalid actions | — | Design problems the designer found (read-only) | `setVisualWorkflow` body |
| Workflow `workflowId` | text field | optional | — | — | — | Workflow identifier; absent on input to create a new workflow | `setVisualWorkflow` body |
| Trigger `trigger` | text field | optional | — | — | — | What starts the workflow | `setVisualWorkflow` body |
| Effective to `effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Effective to | `setVisualWorkflow` body |

#### Outputs: what the screen shows and produces

**Shown**

**Workflow canvas** (canvas, from `setVisualWorkflow`): Steps, decisions and connections of `definition` on a node-and-edge editor with the `nodeTypes` palette and a properties panel (CHG-SOT-020); the fields above are the workflow's header.

| Shows | Format | Notes |
|---|---|---|
| Definition | text | The workflow graph (nodes and connections) as a JSON document |
| Node types | list or chips (count when long) | Node kinds used in this workflow |
| Workflow name | text | Workflow Name |
| Module | text | Module |
| Business process | text | Business Process |
| Owner | text | Owner |
| Priority | text | Priority |
| Effective from | text | Effective Dates |
| Validation issues | list or chips (count when long) | Design problems the designer found (read-only) |
| Workflow | text | Workflow identifier; absent on input to create a new workflow |
| Trigger | text | What starts the workflow |
| Effective to | 1 Oct 2026, 14:30 | Effective to |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save changes (primary button) | `setVisualWorkflow` PUT `/visual-workflow` | VisualWorkflowDesignerInput | VisualWorkflowDesignerView | — | — |

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

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Workflow Name: 233
  Module: 11
  Business Process: 312
  Owner: Rahul Menon
  Trigger: 74
  Version: 19
  Priority: 57
  Effective Dates: 57
```

#### Permissions

- `setVisualWorkflow` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-241` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-241`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 6: Works in Visual Workflow Designer → Allow administrators to visually design complete business processes.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-241?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save changes.
- [ ] Every transition is wired: `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-242` Approval Matrix & Multi-Level Approval Configuration

**Configure when approvals are required and who must approve. (merged into BO-086 Approval Matrix).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-matrix-multi-level-approval-configuration-adm-242` |

**What the spec says about it.** **Merged into BO-086 Approval Matrix** (decided 2 October 2026, Chinmay: DEC-100 and the pre-apply round, "duplicate screens: merge as proposed"; CHG-MOV-002). On one platform it declared the same operations as BO-086 (check-screen-wiring S-DUP-SCREEN). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-086, and nothing on it is built separately. **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 6 actions on this screen and the screen declares 1 operation.** Unserved: Single Approval, Sequential Approval, Parallel Approval, Any-One Approval, Conditional Approval, Multi-Level …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** When approvals are required and who approves: single, sequential, parallel, any-one, conditional and multi-level routes with minimum approvals and rejection behaviour. Tighten-never-loosen applies across levels.

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

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApprovalMatrix: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setApprovalMatrix)*
- **Approval matrix rules**: Ordered; the first matching rule wins. A venue may tighten and never loosen a rule from above: a higher threshold, fewer approvers or a different approver role are each loosening and refused 409 loosensParentRule. Saving creates a new version; requests in flight keep the version they were raised under. *(source: contracts/spine/approvals.yaml#setApprovalMatrix; R129; R183)*

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

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*
- → `BO-086` Approval Matrix: *Open Approval Matrix*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval multi-level approval configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval multi-level approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval multi-level approval configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-086 Approval Matrix requires; this id has no operation of its own since the merge, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **setApprovalMatrix answers 409**: Show it as something the person can act on, not a failure: Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold, fewer approvers or a different approver role; audit R129); or `unreachableRule` — a rule can never match because an earlier one always does. `ruleOrder` names the offending r... *(source: contracts/spine/approvals.yaml#setApprovalMatrix)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Sequential/Parallel: 74
  Minimum Approvals: 42
  Rejection Behavior: 19
  Request Changes: 128
  Delegate: 19
  Reassign: 233
  Skip Conditions: 233
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-086 Approval Matrix requires; this id has no operation of its own since the merge, so it names that screen's.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-242` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-242`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1

#### Acceptance for the design

- [ ] Every input above is drawn (7), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-242?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Single Approval, Sequential Approval, Parallel Approval, Any-One Approval, Conditional Approval, Multi-Level Approval.
- [ ] Every transition is wired: `ADM-238`, `BO-086`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-243` Roles, Authority, Delegation & Approval Limits

**Define who has authority to perform or approve specific actions. This should work with TICVAI RBAC/PBAC rather than replace it. (a section of BO-087 Approval Delegations since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 1 · needs the `core` module |
| Block | Block A · task APP-SETUP-ADM-243 |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_VIEW` (1 configure, 1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Define by; Capture) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/approvals/approval-delegations/roles-authority-delegation-approval-limits-adm-243` |

**What the spec says about it.** **Merged into BO-087 Approval Delegations as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-087: it renders inside BO-087's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Event operations. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Who has authority to approve what, up to which limit, and who stands in for whom, working with roles rather than replacing them.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listApprovalDelegations (APPROVAL_VIEW) … (CHG-MOV-001).

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

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApprovalMatrix: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setApprovalMatrix)*
- **Approval matrix rules**: Ordered; the first matching rule wins. A venue may tighten and never loosen a rule from above: a higher threshold, fewer approvers or a different approver role are each loosening and refused 409 loosensParentRule. Saving creates a new version; requests in flight keep the version they were raised under. *(source: contracts/spine/approvals.yaml#setApprovalMatrix; R129; R183)*
- **Delegation window and limits**: Always time-bounded: 'to' must follow 'from' (refused invalidWindow); the delegate cannot exceed the delegator's kinds or maxAmount and must hold the permission (exceedsDelegatorAuthority, delegateLacksPermission); a delegate never approves a request the delegator raised. *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Event operations (primary button) | navigation or local | — | — | — | — |

**Data it reads**: `listApprovalDelegations` (onLoad, Delegations in force)

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*
- → `BO-087` Approval Delegations: *Open Approval Delegations*; carries `delegationId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The roles authority delegation configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the roles authority delegation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No roles authority delegation configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The delegation is malformed. `refusedReason` is `invalidWindow` where `to` is not after `from`, or `delegateIsDelegator` where both principals are the same … (DelegationRefusedProblem); 400 Validation failed. Includes a `scopeLevel` that is not the level of the scope node the caller acts at (audit R183); `errors[]` names `scopeLevel`.; 409 Refused, and nothing is stored. `refusedReason` says … |

#### Edge cases to draw

- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_DECIDE for createApprovalDelegation; APPROVAL_CONFIGURE for setApprovalMatrix. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*
- **createApprovalDelegation answers 403**: Show it as something the person can act on, not a failure: The delegation would hand over authority that is not there. `refusedReason` is `delegateLacksPermission` where the delegate does not hold the permission being delegated, or `exceedsDelegatorAuthority` where `kinds` or `maxAmount` go beyond what the delegator may approve. The shared `Forbidden`, with no `refusedReason`, is the ca... *(source: contracts/spine/approvals.yaml#createApprovalDelegation)*
- **setApprovalMatrix answers 409**: Show it as something the person can act on, not a failure: Refused, and nothing is stored. `refusedReason` says which: `loosensParentRule` — the matrix would loosen a rule set at a higher scope (a higher threshold, fewer approvers or a different approver role; audit R129); or `unreachableRule` — a rule can never match because an earlier one always does. `ruleOrder` names the offending r... *(source: contracts/spine/approvals.yaml#setApprovalMatrix)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  User: 19
  Role: 233
  Position: 312
  Department: Ticketing
  Venue: AquaCove Dubai
  Business Unit: 312
  Legal Entity: 312
  Region: 233
  Delegator: 46
  Delegate: 46
  Scope: 11
  Start: 128
  End: 11
  Reason: 74
```

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

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-243` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-243`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 10: Works in Roles, Authority, Delegation & Approval Limits → Define who has authority to perform or approve specific actions. This should work with TICVAI RBAC/PBAC rather than replace it.

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-243?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Event operations.
- [ ] Every transition is wired: `ADM-238`, `BO-087`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `APPROVAL_DECIDE`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-244` SLA, Escalation, Reminder & Timeout Rules

**Define how workflows behave when people or systems do not act within the expected time. (a section of BO-388 Approval SLA Policy Configuration since 2 October 2026).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `APPROVAL_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/venue-operations/approval-sla-policy-configuration-bo-388/sla-escalation-reminder-timeout-rules-adm-244` |

**What the spec says about it.** **Merged into BO-388 Approval SLA Policy Configuration as a section of it** (decided 2 October 2026, Chinmay: DEC-100, "merge them with BO-008 to BO-011 so one surface edits each record", and the pre-apply round; CHG-MOV-002). It edits the same record as BO-388: it renders inside BO-388's component, under its route, and keeps its own operations, because the first-release slice and its ticket name them. Whether those duplicate writers retire in favour of the venue screen's is a contract and plan question (CHG-MOV-008). **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 1 actions on this screen and the screen declares 1 operation.** Unserved: Venue Calendar. Each needs an operation, or needs removing from the screen; this is the Phase 3 …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Response, approval, task and resolution SLAs and system timeouts per workflow, measured on the venue calendar.

**Fixed on main** (the package already carries these; draw what it says): Only a read (listSlaEscalationReminder); nothing saves. (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Response SLA | select field | — | — | — | — | — | — |
| Approval SLA | select field | — | — | — | — | — | — |
| Task SLA | select field | — | — | — | — | — | — |
| Resolution SLA | select field | — | — | — | — | — | — |
| System Action Timeout | select field | — | — | — | — | — | — |

**Form: Save SLA rules** (modal, opened by *Save SLA rules*; *Save SLA rules* calls `setApprovalSlaPolicy`, *Cancel* sends nothing)

**Collects what `setApprovalSlaPolicy` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Venue Calendar (primary button) | navigation or local | — | — | — | — |
| Save SLA rules (secondary button) | `setApprovalSlaPolicy` PUT `/approval-sla-policies` | ApprovalSlaPolicy | ApprovalSlaPolicy | — | opens modal first |

**Data it reads**: `listSlaEscalationReminder` (onLoad, SLA, Escalation, Reminder & Timeout Rules)

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*; calls `listSlaEscalationReminder`
- → `BO-388` Approval SLA Policy Configuration: *Open Approval SLA Policy Configuration*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sla escalation reminder configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sla escalation reminder untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sla escalation reminder configured yet. Offers no create action (nothing on this screen creates one) and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Response SLA: 3 h 20 min
  Approval SLA: 42 min
  Task SLA: 42 min
  Resolution SLA: 1.8 s
  System Action Timeout: 42 min
```

#### Permissions

- `listSlaEscalationReminder` → `APPROVAL_VIEW` (read) · staff
- `setApprovalSlaPolicy` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-244` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-244`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 12: Works in SLA, Escalation, Reminder & Timeout Rules → Define how workflows behave when people or systems do not act within the expected time.

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-244?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Venue Calendar, Save SLA rules.
- [ ] Every transition is wired: `ADM-238`, `BO-388`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-245` Trigger, Action & Cross-Module Orchestration Configuration

**Define what starts a workflow and what TICVAI services may be called during execution.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/trigger-action-cross-module-orchestration-configuration-adm-245` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 13 actions on this screen and the screen declares 1 operation.** Unserved: Create Approval, Create Task, Update Status, Apply Hold, Release Hold, Create Notification, Generate …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** What starts a workflow and which TICVAI actions it may call (create approval, task, hold, notification, document, refund), with retry, compensation and the exception queue.

**Fixed on main** (the package already carries these; draw what it says): Action types (Execute Refund, Apply Hold) are drawn as buttons. (CHG-MOV-005); Calls tenant-permission operations with no tenant picker and no platform-staff grant: setTriggerActionCross (APPROVAL_CONFIGURE). (CHG-MOV-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Retry | select field | — | — | — | — | — | — |
| Rollback where supported | select field | — | — | — | — | — | — |
| Compensation Action | select field | — | — | — | — | — | — |
| Exception Queue | select field | — | — | — | — | — | — |
| Human Intervention | select field | — | — | — | — | — | — |
| Allowed actions | multi-select chips | optional | — | Create approval · Create task · Update status · Apply hold · Release hold · Create notification · Generate document · Execute refund · Update allocation · Activate membership · Suspend partner · Call approved API … | — | The pack's action types (Create Approval, Create Task, Update Status, Apply Hold, Release Hold, Create Notification, Generate Document, Execute Refund) are options of allowedActions, not buttons … | `TriggerActionCrossModuleOrchestrationConfigurationInput.allowedActions` |

**Sent by *Save orchestration*** (`setTriggerActionCross`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Trigger type `triggerType` | radio group | required | — | Event · Data condition · Schedule · Manual | — | What starts the workflow | `setTriggerActionCross` body |
| Workflow `workflowId` | text field | required | — | — | — | Workflow this trigger and action set belongs to | `setTriggerActionCross` body |
| Allowed actions `allowedActions` | multi-select chips | optional | — | Create approval · Create task · Update status · Apply hold · Release hold · Create notification · Generate document · Execute refund · Update allocation · Activate membership · Suspend partner · Call approved API … | — | Actions this workflow may call | `setTriggerActionCross` body |
| On failure `onFailure` | radio group | optional | — | Retry · Rollback · Compensate · Exception queue · Human intervention | — | What happens when an action fails | `setTriggerActionCross` body |
| Trigger definition `triggerDefinition` | text field | optional | — | — | — | Event name, data condition (e.g. | `setTriggerActionCross` body |
| Max retries `maxRetries` | number field | optional | — | — | — | Retries before the failure handling applies | `setTriggerActionCross` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save orchestration (primary button) | `setTriggerActionCross` PUT `/trigger-action-cross` | TriggerActionCrossModuleOrchestrationConfigurationInput | TriggerActionCrossModuleOrchestrationConfigurationView | — | — |

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

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Retry: 233
  Rollback where supported: 46
  Compensation Action: 233
  Exception Queue: 1
  Human Intervention: 57
```

#### Permissions

- `setTriggerActionCross` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-245` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-245`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 14: Works in Trigger, Action & Cross-Module Orchestration Configuration → Define what starts a workflow and what TICVAI services may be called during execution.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-245?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save orchestration.
- [ ] Every transition is wired: `ADM-238`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-246` Workflow Testing, Simulation & Impact Analysis

**Allow administrators to test rules and workflows before they affect live operations. This is a critical screen.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-testing-simulation-impact-analysis-adm-246` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Manual Test Case, Sample Transaction, Historical Replay, Scenario Simulation, Batch Test. Each needs an …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Test rules and workflows before they affect live operations: a manual case, a sample transaction, historical replay or a batch; shows rules evaluated, approval path, actions and expected outcome. Nothing is executed.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: simulateWorkflowTestingImpact (APPROVAL_CONFIGURE). (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

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

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Simulation result**: Labelled "Simulation — nothing was changed"; differences from the current live version highlighted. *(source: contracts/spine/approvals.yaml#simulateWorkflowTestingImpact)*

**Where the user goes next**

- → `ADM-238` Rules & Workflow Command Center: *Returns to the board's landing screen*; calls `simulateWorkflowTestingImpact`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow testing simulation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow testing simulation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow testing simulation yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow testing simulation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
case: Refund AED 750 at Main Gate Till 3
rulesEvaluated: 4
approvalPath: Supervisor then Venue Manager
outcome: approval required
changed: nothing (simulation)
```

#### Permissions

- `simulateWorkflowTestingImpact` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-246` · status **notStarted** · provenance generated
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
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show) and no metric row |
| Offline | online only |
| Opens with | `challengeId` (navigation) |
| Route | `/platform/versioning-governance-approval-publication-adm-247` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 1 operation.** Unserved: Publish Now, Schedule, Selected Tenant, Selected Venue, Selected Brand. Each needs an operation, or needs …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Move a rule or workflow version from draft to production: review, approve with a second factor, publish now or schedule, for a tenant, brand or venue.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: approveVersioningGovernance (APPROVAL_CONFIGURE). (CHG-MOV-001); Reaches approveVersioningGovernance (step-up mfa) and declares no way to raise the challenge. (CHG-MOV-006); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Authentication code | text field | — | — | — | — | Asked in place inside the Publish confirmation; its result is the stepUpToken approveVersioningGovernance needs (audit R126). | — |

**Form: Publish Now** (confirmDialog, opened by *Publish Now*; *Publish* calls `approveVersioningGovernance`, *Cancel* sends nothing)

**Says which workflow version goes live, where (rolloutScope) and from when.** Collects what `approveVersioningGovernance` sends and asks for the authentication code in place, because the operation demands step-up (mfa) and refuses without a fresh stepUpToken (CHG-MOV-006). Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Workflow `workflowId` | text field | required | — | — | — | Rule or workflow the version belongs to | `approveVersioningGovernance` body |
| Version `version` | text field | required | — | — | — | Version | `approveVersioningGovernance` body |
| Changed by `changedBy` | text field | optional | — | — | — | Changed By | `approveVersioningGovernance` body |
| Change date `changeDate` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Change Date | `approveVersioningGovernance` body |
| Change reason `changeReason` | text field | optional | — | — | — | Change Reason | `approveVersioningGovernance` body |
| Business owner `businessOwner` | text field | optional | — | — | — | Business Owner | `approveVersioningGovernance` body |
| Technical owner `technicalOwner` | text field | optional | — | — | — | Technical Owner | `approveVersioningGovernance` body |
| Risk classification `riskClassification` | text field | optional | — | — | — | Risk Classification | `approveVersioningGovernance` body |
| Test results `testResults` | text field | optional | — | — | — | Test Results | `approveVersioningGovernance` body |
| Approval `approval` | text field | optional | — | — | — | Approval request id for this version | `approveVersioningGovernance` body |
| Changed areas `changedAreas` | multi-select chips | optional | — | Conditions · Thresholds · Approvers · Actions · Sla · Escalation · Integrations | — | Areas that differ from the compared version (read-only) | `approveVersioningGovernance` body |
| Rollout scope `rolloutScope` | radio group | optional | — | All scopes · Selected tenant · Selected venue · Selected brand · Controlled rollout | — | Where the version is published | `approveVersioningGovernance` body |
| Who created `whoCreated` | text field | optional | — | — | — | User who created the version | `approveVersioningGovernance` body |
| Who changed `whoChanged` | text field | optional | — | — | — | Who changed | `approveVersioningGovernance` body |
| Who tested `whoTested` | text field | optional | — | — | — | Who tested | `approveVersioningGovernance` body |
| Who approved `whoApproved` | text field | optional | — | — | — | Who approved | `approveVersioningGovernance` body |
| Who published `whoPublished` | text field | optional | — | — | — | Who published | `approveVersioningGovernance` body |
| What changed `whatChanged` | text field | optional | — | — | — | What changed | `approveVersioningGovernance` body |
| Lifecycle status `lifecycleStatus` | select | optional | — | Draft · Tested · Business review · Technical validation · Approval · Scheduled · Active · Suspended · Retired | — | Version lifecycle status | `approveVersioningGovernance` body |
| Scopes `scopeIds` | list of values (chips) | optional | — | — | — | Tenant, venue or brand ids for a selected rollout | `approveVersioningGovernance` body |
| Effective from `effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Scheduled activation; absent means publish now | `approveVersioningGovernance` body |

**Sent by *Email me a code instead*** (`createMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

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
| Publish Now (primary button) | `approveVersioningGovernance` PUT `/versioning-governance` | VersioningGovernanceApprovalPublicationInput | VersioningGovernanceApprovalPublicationView | — | step-up: mfa (Publishes a governed version. What everyone downstream then treats as current.); opens confirmDialog first |
| Schedule (secondary button) | navigation or local | — | — | — | — |
| Selected Tenant (secondary button) | navigation or local | — | — | — | — |
| Selected Venue (secondary button) | navigation or local | — | — | — | — |
| Selected Brand (secondary button) | navigation or local | — | — | — | — |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Publish now / Schedule**: Separate from approval; the gate names which tenants, brands or venues the version goes live in. *(source: screens/_components.yaml#publishGate)*
- **approveVersioningGovernance**: Confirmation names the consequence first, then asks for the authentication code (authenticator app, or an emailed code as fallback); only a verified challenge sends approveVersioningGovernance with its single-use stepUpToken. Wrong code: the action is not sent and nothing changes; five wrong codes lock step-up for the policy's lockout minutes and the screen says when it lifts. Why the control exists: Publishes a governed version. What everyone downstream then treats as current. *(source: contracts/spine/approvals.yaml#approveVersioningGovernance; R126; contracts/spine/identity.yaml#createMfaChallenge)*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The versioning governance approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the versioning governance approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No versioning governance approval yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the versioning governance approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
item: Refund approval workflow v5
status: approved, awaiting publication
publish: scheduled 05/10/2026 05:00
scope: AquaCove Abu Dhabi
```

#### Permissions

- `approveVersioningGovernance` → `APPROVAL_CONFIGURE` (configure) · staff · step-up mfa
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-247` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS136 Rules  Workflow  Approval   Automation Engine Board 1.dc.html#adm-247`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 1
- Flow F164 *Rules Workflow Approval Automation Engine board 1: Rules & Workflow Command …*, step 18: Works in Versioning, Governance, Approval & Publication → Control how rules and workflows move safely from configuration into production. Board 1 configured the rules and workflows. Board 2 is the live operational layer where TICVAI executes, monitors …

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state.
- [ ] Every output is drawn (20 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-247?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Publish Now, Schedule, Selected Tenant, Selected Venue, Selected Brand, Email me a code instead.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`.
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
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listApprovalDelegations": {"method":"GET","path":"/delegations","contract":"approvals","summary":"Who is standing in for whom","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ApprovalDelegation"},
"listConditionDecisionLogic": {"method":"GET","path":"/condition-decision-logic","contract":"approvals","summary":"Conditions, Decision Logic & Decision Tables","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ConditionsDecisionLogicDecisionTablesView"},
"listRuleWorkflow": {"method":"GET","path":"/rule-workflow","contract":"approvals","summary":"Rules & Workflow Command Center","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"type","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":"sourceModule","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSlaEscalationReminder": {"method":"GET","path":"/sla-escalation-reminder","contract":"approvals","summary":"SLA, Escalation, Reminder & Timeout Rules","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"SlaEscalationReminderTimeoutRulesView"},
"setApprovalMatrix": {"method":"PUT","path":"/approval-matrices","contract":"approvals","summary":"Configure what requires approval","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalMatrix","responds":"ApprovalMatrix"},
"setApprovalSlaPolicy": {"method":"PUT","path":"/approval-sla-policies","contract":"approvals","summary":"How long a decision may take, and what happens when it does not","permission":"APPROVAL_CONFIGURE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ApprovalSlaPolicy","responds":"ApprovalSlaPolicy"},
"setTriggerActionCross": {"method":"PUT","path":"/trigger-action-cross","contract":"approvals","summary":"Trigger, Action & Cross-Module Orchestration Configuration","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"TriggerActionCrossModuleOrchestrationConfigurationInput","responds":"TriggerActionCrossModuleOrchestrationConfigurationView"},
"setVisualBusinessRule": {"method":"PUT","path":"/visual-business-rule","contract":"approvals","summary":"Visual Business Rule Builder","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualBusinessRuleBuilderInput","responds":"VisualBusinessRuleBuilderView"},
"setVisualWorkflow": {"method":"PUT","path":"/visual-workflow","contract":"approvals","summary":"Visual Workflow Designer","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VisualWorkflowDesignerInput","responds":"VisualWorkflowDesignerView"},
"simulateWorkflowTestingImpact": {"method":"PUT","path":"/workflow-testing-impact","contract":"approvals","summary":"Workflow Testing, Simulation & Impact Analysis","permission":"APPROVAL_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"WorkflowTestingSimulationImpactAnalysisInput","responds":"WorkflowTestingSimulationImpactAnalysisView"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ApprovalDelegation": {"type":"object","x-ticvai-persistence":"approvals.delegation","required":["delegatorPrincipalId","delegatePrincipalId","from","to"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"delegatorPrincipalId":{"type":"string","format":"uuid","description":"A principal id (`identity.Principal.id`). This contract stores the id only; the name to show, and the people to pick from, come from `identity.listPrincipals` and `identity.getPrincipal`.\n"},"delegatePrincipalId":{"type":"string","format":"uuid","description":"A principal id, resolved to a name the same way as `delegatorPrincipalId`."},"kinds":{"type":"array","description":"Absent means everything the delegator may approve.","items":{"$ref":"#/components/schemas/ApprovalKind"}},"maxAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"A delegate may be given less authority than the delegator, never more."},"from":{"type":"string","format":"date-time"},"to":{"type":"string","format":"date-time","description":"**Required.** An open-ended delegation is an approver who quietly stopped approving and a delegate who does not know they still hold it.\n"},"reason":{"type":"string"},"isActive":{"type":"boolean","readOnly":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ApprovalKind": {"type":"string","description":"11.1.7 and 11.1.30–11.1.37. **The first four already exist as bespoke implementations** and this contract is what they collapse into.\n**Which actions route here — decided 28 September, audit R144.** Finance and procurement acts go through this engine to a **finance approver**: closing a fiscal period (`periodClose`), reopening one (`periodReopen`), cancelling a purchase order (`purchaseOrderCancel`) and closing one short (`purchaseOrderShortClose`). The tenant default matrix for each of these names the finance approver role; a venue may tighten it and never loosen it. Starting a release rollout routes through `releasePromotion` to the platform release manager (a holder of `PLATFORM_RELEASE_PROMOTE`). **Not every `requiresApproval` goes here:** reopening a shift, recounting a stock count and a retail return above the venue threshold take a supervisor's step-up on the same device instead, and never raise a request.\n**Catalogue change requests route through `productChange` and `pricingChange`** (decided 29 September, writers pass): a product change and a price or pricing change raised in `catalogue` ask for approval under these two kinds, so a venue can route product edits and price edits to different approvers.\n\n**Optional review steps a venue switches on, decided 2 October 2026** (Chinmay; CHG-CSP-036, CHG-CSP-028, CHG-CSP-031). Each is an existing kind narrowed by the rule's `subjectTypes`, so no kind is added (a new value here would be a breaking change against r1) and each is off until the venue saves an active matrix for it:\n- **A purchase order** (`requisition`, subject `purchaseOrder`; Chinmay, 3 October 2026, Block A business rules; CHG-RUL-004): the PO approval matrix. Blanket and RFQ-award orders are raised without a requisition and are approved here instead; `inventory.createPurchaseOrder` asks for every order, by kind and value. - **Publishing white-label content** (`configurationChange`, subject `whiteLabelPublication`): simulate, then a single publish by a holder of the permission; a review step only where the venue sets one up (batch 1, CMS-014; DEC-156). - **Recording F&B waste above a value** (`stockWriteOff`, subject `fnbWaste`): the venue's waste-approval policy, value bands as `minAmount` and `maxAmount`, photo evidence above a value held by fnb (batch 6 #192, BO-139; DEC-192; R144). - **Publishing an access topology** (`configurationChange`, subject `topologyPublication`): second-person approval when the venue switches it on (batch 6 #230, BO-153; DEC-230). - **A permanent identity lock, a whitelist entry, or releasing a full-identity or permanent lock** (`accessPermissionChange`, subjects `identityLock`, `whitelistEntry`, `identityLockRelease`): always a second approver, never for an until-end-of-day lock (critical set 1, BO-229 and BO-247; DEC-254, DEC-260); the tenant default matrix names the security approver role and a venue may tighten it, never remove it.\n","enum":["refund","priceOverride","discountOverride","complimentaryTicket","membershipCancellation","accessPermissionChange","configurationChange","aiRecommendation","releasePromotion","requisition","stockWriteOff","journalEntry","periodClose","periodReopen","purchaseOrderCancel","purchaseOrderShortClose","tenantMigration","productChange","pricingChange"]},
"ApprovalMatrix": {"type":"object","x-ticvai-persistence":"approvals.matrix","required":["kind","scopeLevel","rules"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ApprovalKind"},"scopeLevel":{"type":"string","enum":["tenant","region","venue"]},"scopePath":{"type":"string","readOnly":true},"version":{"type":"integer","readOnly":true,"description":"11.1.80. **A request is decided by the rules it was raised under.** Changing the matrix mid-flight would mean an approver answering a question that changed while they read it.\n**(`kind`, `scopePath`, `version`) is unique**, and a stored version is never edited: a request's `matrixVersion` names exactly one rule set (decided 28 September, audit R129 (2)).\n"},"rules":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalRule"}},"isActive":{"type":"boolean"}}},
"ApprovalRule": {"type":"object","x-ticvai-persistence":"approvals.rule","required":["order","approverRoleIds","mode"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"order":{"type":"integer","description":"**First match wins.** Explicit ordering is what makes a matrix reviewable — an unordered set of overlapping rules is one nobody can reason about.\n"},"minAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"maxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"riskScoreAbove":{"type":"number","nullable":true,"description":"11.1.12. **Not matched against the AI risk score** (29 September, build pass, group G2). The AI assessment on a request (`ApprovalRequest.aiAssessment`, from `ai.scoreApprovalRequest`) is context for the reviewer only (MoM 8 September: AI never influences approve or reject), and routing a request to more approvers because of it would be influence. A rule with this set matches only a `riskScore` the requesting contract passes in `attributes` from its own deterministic rules (a payment's rule score, for example). Using the AI score here needs the client to say so.\n"},"condition":{"type":"string","nullable":true,"description":"11.1.13. Evaluated against the attributes the caller supplied.\n\n**No condition language is defined yet** (pull audit R104, 26 September): the grammar, the attributes it may name and how two conditions are compared for `unreachableRule` are an open decision, not something to infer from this field.\n"},"approverRoleIds":{"type":"array","minItems":1,"description":"Role ids from `identity.listRoles` (`Role.id`), which is where an editor gets the names to show and pick from. This contract stores the ids only.\n","items":{"type":"string","format":"uuid"}},"approverScopeLevel":{"type":"string","enum":["venue","department","region","tenant"],"description":"11.1.39. Which organisational level the approver must sit at."},"mode":{"$ref":"#/components/schemas/ApprovalMode"},"levels":{"type":"integer","default":1,"description":"11.1.3. Multi-level chains ask each level in turn."},"requiresMfa":{"type":"boolean","default":false},"requiresSignature":{"type":"boolean","default":false},"slaMinutes":{"type":"integer","nullable":true,"description":"11.1.14. Null means no SLA, which is different from a long one."},"escalateAfterMinutes":{"type":"integer","nullable":true},"escalateToRoleIds":{"type":"array","description":"Role ids from `identity.listRoles`, as `approverRoleIds`.","items":{"type":"string","format":"uuid"}},"expiresAfterMinutes":{"type":"integer","nullable":true,"description":"11.1.53. An unanswered request eventually stops waiting."},"subjectTypes":{"type":"array","description":"**Which subjects of the kind this rule matches** (decided 2 October 2026, Chinmay; CHG-CSP-028, CHG-CSP-036, CHG-CSP-031): the `CreateApprovalRequest.subjectType` values, for example `topologyPublication` or `whiteLabelPublication` under `configurationChange`. Empty matches every subject of the kind. It is how a venue switches an optional review step on for one kind of act without routing every act of the kind.","items":{"type":"string","maxLength":64}},"signatureMethods":{"type":"array","description":"**The signature methods this level accepts, where `requiresSignature` is true** (design-notes correction on ADM-344, Block B: \"Configuring which stages need a signature is a policy write\"; CHG-CSP-045). Values of `ApprovalSignature.method`. Empty accepts any of them. With `requiresSignature` this makes the rule the signature policy: which levels of which kinds need a signature, and how it is given; `signApprovalDecision` refuses a method the level does not accept.","items":{"type":"string","enum":["platformKey","uaePass","externalCertificate","drawnSignature"]}},"externalProviderId":{"type":"string","format":"uuid","nullable":true,"description":"11.1.65 (29 September). **This level is decided in an external workflow system** (`ApprovalExternalProvider`) rather than by a person in TICVAI. `approverRoleIds` stay required: they are who decides if the provider does not answer in time and its `onTimeout` is `fallBackToRoles`.\n"}}},
"ApprovalSlaPolicy": {"type":"object","x-ticvai-persistence":"approvals.sla_policy","description":"Approvals boards 5.5 and 5.6. **A target with no consequence is a number in a table**, so the reminder and breach behaviour are part of the policy.\n","required":["code"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"appliesToRequestKinds":{"type":"array","items":{"$ref":"#/components/schemas/ApprovalKind"}},"targetMinutes":{"type":"integer"},"businessHoursOnly":{"type":"boolean","default":true,"description":"**A four-hour SLA starting at five in the afternoon is breached by nine the next morning with nobody having done anything wrong.**\n"},"calendarId":{"type":"string","format":"uuid","nullable":true},"reminders":{"type":"array","items":{"type":"object","properties":{"atPercentOfTarget":{"type":"integer"},"notify":{"type":"string","enum":["approver","approverManager","requester","escalationGroup"]}}}},"firstReminderAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"**Percent of `targetMinutes` at which the first reminder goes** (decided 29 September, readiness close-out: the reminder steps are percentages of target). A column so the SLA, Escalation, Reminder & Timeout Rules screen reads it rather than unpacking `reminders`; the reminder in `reminders` at this percentage says whom it notifies (data model for the agreed operations, 29 September)."},"secondReminderAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Percent of `targetMinutes` at which the second reminder goes; above `firstReminderAtPercent`"},"escalateAtPercent":{"type":"integer","minimum":1,"maximum":100,"nullable":true,"description":"Percent of `targetMinutes` at which the request or workflow escalates; at or above `secondReminderAtPercent`"},"onBreach":{"type":"string","enum":["notifyOnly","escalate","autoApprove","autoReject"],"default":"escalate"},"autoActionAllowed":{"type":"boolean","default":false,"description":"**Auto-approval on breach is off unless somebody says otherwise, in writing.** A queue that approves itself when nobody looks is not an approval process.\n"},"escalationGroupId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"}}},
"ConditionsDecisionLogicDecisionTablesView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.decision_table and decision_table_row (schema DecisionTable) (data model for the agreed operations, 29 September)","description":"**What Conditions, Decision Logic & Decision Tables displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"name":{"type":"string","description":"Name"},"decisionTableId":{"type":"string","description":"Decision table or condition set identifier"},"resolutionStrategy":{"type":"string","enum":["priority","sequence","specificity"],"description":"How to choose when multiple rules apply"},"onMatch":{"type":"string","enum":["stopProcessing","continueEvaluation"],"description":"Whether evaluation stops at the first match"},"conflicts":{"type":"array","items":{"type":"string","enum":["contradictoryRules","overlappingConditions","unreachableOutcomes","circularLogic","missingOutcomes"]},"description":"Conflicts detected in this decision logic (read-only)"}},"required":["decisionTableId","name"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"RulesWorkflowCommandCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_definition, workflow_version, business_rule, decision_table, automation, matrix and rule; one row per configuration (data model for the agreed operations, 29 September)","description":"**What Rules & Workflow Command Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"ruleWorkflowId":{"type":"string","description":"Rule/Workflow ID"},"name":{"type":"string","description":"Name"},"type":{"type":"string","enum":["businessRule","approvalWorkflow","operationalWorkflow","decisionRule","validationRule","escalationRule","automation","crossModuleWorkflow"],"description":"Kind of configuration"},"sourceModule":{"type":"string","description":"Source Module"},"businessProcess":{"type":"string","description":"Business Process"},"version":{"type":"string","description":"Version"},"owner":{"type":"string","description":"Owner"},"effectiveDate":{"type":"string","format":"date-time","description":"Effective Date"},"status":{"type":"string","enum":["draft","testing","review","pendingApproval","approved","scheduled","active","suspended","retired"],"description":"Lifecycle status"},"lastModified":{"type":"string","format":"date-time","description":"Last Modified"},"usage":{"type":"string","description":"Usage"}},"required":["ruleWorkflowId"]},
"RulesWorkflowCommandCenterViewSummary": {"type":"object","x-ticvai-persistence":"none - aggregate computed at read time over the rows the page lists","description":"The KPI tiles shown above the list on this screen. Computed over the whole filtered set, not the current page (decided 29 September, readiness close-out).","properties":{"activeRules":{"type":"integer","description":"Active Rules"},"activeWorkflows":{"type":"integer","description":"Active Workflows"},"approvalWorkflows":{"type":"integer","description":"Approval Workflows"},"draftConfigurations":{"type":"integer","description":"Draft Configurations"},"pendingApproval":{"type":"integer","description":"Pending Approval"},"scheduledChanges":{"type":"integer","description":"Scheduled Changes"},"rulesWithErrors":{"type":"integer","description":"Rules With Errors"},"workflowsWithWarnings":{"type":"integer","description":"Workflows With Warnings"},"recentlyModified":{"type":"integer","description":"Configurations modified in the recent period"},"modulesCovered":{"type":"integer","description":"Number of modules using configured rules and workflows"}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
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
"WorkflowTestingSimulationImpactAnalysisView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — computed by simulation over approvals.workflow_version and the rules it calls; never executes actions (data model for the agreed operations, 29 September)","description":"**What Workflow Testing, Simulation & Impact Analysis displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowId":{"type":"string","description":"Workflow under test"},"testMode":{"type":"string","enum":["manualTestCase","sampleTransaction","historicalReplay","scenarioSimulation","batchTest"],"description":"How the workflow is tested"},"rulesEvaluated":{"type":"integer","description":"Rules Evaluated"},"conditionsMatched":{"type":"integer","description":"Conditions Matched"},"decisions":{"type":"integer","description":"Decisions"},"approvalPath":{"type":"string","description":"Approval Path"},"actions":{"type":"integer","description":"Actions"},"notifications":{"type":"integer","description":"Notifications"},"sla":{"type":"string","description":"SLA"},"expectedOutcome":{"type":"string","description":"Expected Outcome"},"version":{"type":"string","description":"Version under test"},"compareWithVersion":{"type":"string","description":"Existing version to compare against for regression"},"inputPayload":{"type":"string","description":"Sample transaction as a JSON document, for manual and sample tests"},"replayFrom":{"type":"string","format":"date","description":"Historical replay start"},"replayTo":{"type":"string","format":"date","description":"Historical replay end"}},"required":["workflowId","testMode"]},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
