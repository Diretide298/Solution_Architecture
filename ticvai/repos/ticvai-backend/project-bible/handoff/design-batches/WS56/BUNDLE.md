# WS56 — Rules  Workflow  Approval   Automation Engine board 2

**10 screens · 9 operations · 16 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `APPROVAL_ACT, APPROVAL_CONFIGURE, APPROVAL_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
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
| `ADM-248` | Workflow Operations Command Center | B | 0 | 254 | 6 | 0 | 1 | 0 | — | notStarted (generated) |
| `ADM-249` | Unified Approval Inbox & Decision Workspace | B | 0 | 18 | 6 | 7 | 1 | 3 | — | notStarted (generated) |
| `ADM-250` | Workflow Instance Monitor & Process Timeline | B | 9 | 20 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-251` | Workflow Exception, Failure & Recovery Center | B | 10 | 22 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-252` | SLA, Escalation & Bottleneck Monitor | B | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-253` | Automation Execution & Autonomous Action Monitor | B | 0 | 34 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-254` | Cross-Module Orchestration Monitor | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-255` | Workflow Analytics & Process Performance | B | 2 | 0 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-256` | Process Optimization & Automation Opportunity Center | B | 0 | 14 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-257` | AI Workflow Intelligence & Autonomous Governance Center | B | 0 | 22 | 6 | 0 | 1 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-249, ADM-253, ADM-254, ADM-256, ADM-257 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-248` Workflow Operations Command Center

**Provide administrators and operational managers with a real-time view of all workflow activity across TICVAI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task VM-ADM-248 |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-operations-command-center-adm-248` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Every running workflow instance with its current step, owner, priority and SLA; counts of started, completed, failed and escalated.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listWorkflow (APPROVAL_VIEW). (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

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
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Priority | text | Priority |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |

**The selected workflow operations** (detail panel): The pack groups this record's detail under its own headings: “Show activity originating from”, “Use”, “Refund Approval Workflow”.

| Shows | Format | Notes |
|---|---|---|
| Workflow | text | Workflow |
| Module | chip: Ticketing, Pricing, Finance, Procurement, Crm, Resource management… | Module the workflow originates from |
| Business object | text | Business Object |
| Initiated by | text | Initiated By |
| Started | 1 Oct 2026, 14:30 | Started |
| Current step | text | Current Step |
| Priority | text | Priority |
| Status | chip: Running, Waiting approval, Waiting task, Waiting system, Escalated, Failed… | Status |

**Data it reads**: `listWorkflow` (onLoad, Workflow Operations Command Center)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `ADM-249` Unified Approval Inbox & Decision Workspace: *Works in Unified Approval Inbox & Decision Workspace*; calls `listWorkflow`
- → `ADM-250` Workflow Instance Monitor & Process Timeline: *Works in Workflow Instance Monitor & Process Timeline*; calls `listWorkflow`
- → `ADM-251` Workflow Exception, Failure & Recovery Center: *Works in Workflow Exception, Failure & Recovery Center*; calls `listWorkflow`
- → `ADM-252` SLA, Escalation & Bottleneck Monitor: *Works in SLA, Escalation & Bottleneck Monitor*; calls `listWorkflow`
- → `ADM-253` Automation Execution & Autonomous Action Monitor: *Works in Automation Execution & Autonomous Action Monitor*; calls `listWorkflow`
- → `ADM-254` Cross-Module Orchestration Monitor: *Works in Cross-Module Orchestration Monitor*; calls `listWorkflow`
- → `ADM-255` Workflow Analytics & Process Performance: *Works in Workflow Analytics & Process Performance*; calls `listWorkflow`
- → `ADM-256` Process Optimization & Automation Opportunity Center: *Works in Process Optimization & Automation Opportunity Center*; calls `listWorkflow`
- → `ADM-257` AI Workflow Intelligence & Autonomous Governance Center: *Works in AI Workflow Intelligence & Autonomous Governance Center*; calls `listWorkflow`
- → `BO-391` Live Escalation Operations Center: *Works in SLA, Escalation & Bottleneck Monitor*; calls `listWorkflow`
- → `BO-084` Approval Inbox: *Works in Unified Approval Inbox & Decision Workspace*; calls `listWorkflow`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow operations list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow operations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow operations yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow operations are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Workflows Running: 128
  Started Today: 46
  Completed Today: 312
  Pending Approvals: 74
  Waiting Tasks: 42 min
  SLA At Risk: 1.8 s
  SLA Breached: 3 h 20 min
  Failed Workflows: 5
  Escalated: 128
  Automated Executions: 46
```

#### Permissions

- `listWorkflow` → `APPROVAL_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-248` · status **notStarted** · provenance generated
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
- [ ] Every output is drawn (254 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-248?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `ADM-249`, `ADM-250`, `ADM-251`, `ADM-252`, `ADM-253`, `ADM-254`, `ADM-255`, `ADM-256`, `ADM-257`, `BO-391`, `BO-084`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-249` Unified Approval Inbox & Decision Workspace

**Provide users with one approval inbox across all TICVAI modules. This is extremely important. A manager should not need to open Finance for one approval, Pricing for another, Procurement for another, and Customer Service for another. (merged into BO-084 Approval Inbox).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task VM-ADM-249 |
| Who uses it | venue |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `requestId` (navigation), `approvalRequestId` (navigation) |
| Route | `/platform/unified-approval-inbox-decision-workspace-adm-249` |

**What the spec says about it.** **Merged into BO-084 Approval Inbox** (decided 2 October 2026, Chinmay: DEC-100 and the pre-apply round, "duplicate screens: merge as proposed"; CHG-MOV-002). On one platform it declared the same operations as BO-084 (check-screen-wiring S-DUP-SCREEN). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-084, and nothing on it is built separately. **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** One approval inbox across every module for a manager, decided in place. The same queue as BO-084, offered on the Console only for a platform operator acting in a tenant.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every unified approval decision** (data table)

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
| Approve (primary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (amount)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Decide (Approve / Reject / Return / Request information)**: Four outcomes, not two: reject needs a reason the requester reads; return sends it back to amend; request information pauses the SLA clock. Approving records an authorisation and does not perform the action; on a multi-level chain the request moves to the next level. Where the rule demands MFA the decision carries a stepUpToken from the in-place challenge; where it demands a signature, the signature step comes first. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; F14 step 4)*

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*
- → `BO-084` Approval Inbox: *Open Approval Inbox*; carries `approvalRequestId`, `requestId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The unified approval decision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the unified approval decision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No unified approval decision yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the unified approval decision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-084 Approval Inbox requires; this id has no operation of its own since the merge, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_DECIDE for Approve. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 403**: Show it as something the person can act on, not a failure: The approver may not decide this request. **Always carries `refusedReason`**, one value per cause — the approver is the requester (`approverIsRequester`), is not in the resolved chain (`notInApproverChain`), lacks the permission the rule demands (`insufficientPermission`), gave no step-up token where the rule requires MFA (`mfaR... *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **decideApprovalRequest answers 409**: Show it as something the person can act on, not a failure: The request is no longer open for a decision. `refusedReason` says which: `alreadyDecided` (approved or rejected), `withdrawn`, `expired` or `cancelled`, and `currentStatus` carries the status it is in. *(source: contracts/spine/approvals.yaml#decideApprovalRequest)*
- **The approver raised the request, or sits outside the resolved chain**: Decide is refused 403 with refusedReason (approverIsRequester, notInApproverChain, missing permission or step-up); show the reason in words and who can decide instead. Segregation of duties survives delegation. *(source: contracts/spine/approvals.yaml#decideApprovalRequest; contracts/spine/approvals.yaml#createApprovalDelegation)*

#### Consistency with other screens

- Match `BO-084`: One queue.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every unified approval decision:
- kind: standard
  amount: AED 1,250.00
  requestedAt: 01/10/2026 09:14
  slaDueAt: 01/10/2026 09:14
  status: active
- kind: standard
  amount: AED 48,000.00
  requestedAt: 30/09/2026 18:02
  slaDueAt: 30/09/2026 18:02
  status: pending
- kind: override
  amount: OMR 48.500
  requestedAt: 28/09/2026 11:45
  slaDueAt: 28/09/2026 11:45
  status: suspended
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-084 Approval Inbox requires; this id has no operation of its own since the merge, so it names that screen's.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.10 | Out-of-Office Routing - System shall automatically reroute approvals when approvers are unavailable. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.28 | Mobile Approvals - System shall support approval actions through mobile applications. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.29 | Email-Based Approvals - System shall support approval actions through email links. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.54 | Approval Reopening - System shall support reopening previously completed approval requests. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.73 | AI Risk Assessment - System shall provide AI-generated risk assessments for approval requests. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.75 | AI Escalation Recommendations - System shall recommend escalation actions based on approval patterns. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |
| 11.1.78 | Shared Service Approval Centers - System shall support centralized approval processing teams. | Approval Workflows & Governance | CONTRACTED | data `ApprovalRequest` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval command centre/inbox shows all pending, validated and renewal requests and lets requests be assigned or reassigned to the relevant department or person. Approvals apply to any request type (new product, price change, website change). *(client request · MoM 8 Sep 2026, 4.12 Approval Workflow Recap - Inbox, SLA & Escalation · DI-723)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-249` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-249`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-249?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Approve.
- [ ] Every transition is wired: `ADM-248`, `BO-084`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 4 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-250` Workflow Instance Monitor & Process Timeline

**Allow administrators to inspect exactly what is happening inside an individual running workflow.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task VM-ADM-250 |
| Who uses it | venue staff holding `APPROVAL_ACT`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen both a metric directory (§Display) and a per-row directory (§For each step show) — counts over a population, then the population |
| Offline | online only |
| Opens with | `instanceId` (navigation) |
| Route | `/platform/workflow-instance-monitor-process-timeline-adm-250` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** One running workflow instance step by step: who, when, input, output, decision and duration; act on it (retry, skip, cancel).

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listWorkflowInstanceProcess (APPROVAL_VIEW) … (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

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
| Empty, first run (`?state=emptyFirstRun`) | No workflow instance process yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow instance process are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not … |

#### Edge cases to draw

- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_ACT for Act on workflow instance. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*
- **actOnWorkflowInstance answers 409**: Show it as something the person can act on, not a failure: The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step to skip is an approval node *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*
- **actOnWorkflowInstance answers 422**: Show it as something the person can act on, not a failure: A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not an allowed edge, or the assignee is the requester of the approval *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Workflow Instance: 128
  Workflow Name: 46
  Version: 312
  Source Module: 74
  Business Object: 19
  Initiated By: 233
  Start Time: 3 h 20 min
  Current Status: 11
  Current Step: 128
  SLA: 3 h 20 min
Every workflow instance process:
- type: standard
  assignedTo: 31/12/2026 23:59
- type: standard
  assignedTo: 15/10/2026 00:00
- type: override
  assignedTo: 01/11/2026 06:00
```

#### Permissions

- `listWorkflowInstanceProcess` → `APPROVAL_VIEW` (read) · staff
- `actOnWorkflowInstance` → `APPROVAL_ACT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-250` · status **notStarted** · provenance generated
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
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-251` Workflow Exception, Failure & Recovery Center

**Provide one controlled workspace for failed workflow executions.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task VM-ADM-251 |
| Who uses it | venue staff holding `APPROVAL_ACT`, `APPROVAL_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | `instanceId` (navigation) |
| Route | `/platform/workflow-exception-failure-recovery-center-adm-251` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack names 15 actions on this screen and the screen declares 1 operation.** Unserved: Business Rule Failure, Missing Data, Permission Failure, Integration Failure, Action Failure, Duplicate …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Failed workflow executions by error type with business impact; retry, resolve or escalate each.

**Fixed on main** (the package already carries these; draw what it says): Error types are drawn as buttons. (CHG-MOV-005); Calls tenant-permission operations with no tenant picker and no platform-staff grant: listWorkflowExceptionFailure (APPROVAL_VIEW) … (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Error type | select | optional | — | Business rule failure · Missing data · Missing approver · Permission failure · Integration failure · Timeout · Action failure · Invalid state · Duplicate event · Service unavailable · Configuration error | — | The pack's error types (Business Rule Failure, Missing Data, Permission Failure, Integration Failure, Action Failure, Duplicate Event, Service Unavailable, Configuration Error) filter the list by … | `WorkflowExceptionFailureRecoveryCenterView.errorType` |

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
| Act on workflow instance (secondary button) | `actOnWorkflowInstance` POST `/workflow-instances/{instanceId}/actions` | WorkflowInstanceActionInput | WorkflowInstance | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` … | gated `APPROVAL_ACT`; opens modal first |

**Data it reads**: `listWorkflowExceptionFailure` (onLoad, Workflow Exception, Failure & Recovery Center)

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `listWorkflowExceptionFailure`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow exception failure list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow exception failure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow exception failure yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow exception failure are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step …; 422 A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not … |

#### Edge cases to draw

- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_ACT for Act on workflow instance. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*
- **actOnWorkflowInstance answers 409**: Show it as something the person can act on, not a failure: The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step to skip is an approval node *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*
- **actOnWorkflowInstance answers 422**: Show it as something the person can act on, not a failure: A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not an allowed edge, or the assignee is the requester of the approval *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
exceptions:
- workflow: Group booking confirmation
  step: Issue tickets
  errorType: Integration failure
  retries: 3
  impact: 42 tickets not issued
```

#### Permissions

- `listWorkflowExceptionFailure` → `APPROVAL_VIEW` (read) · staff
- `actOnWorkflowInstance` → `APPROVAL_ACT` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-251` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-251`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 6: Works in Workflow Exception, Failure & Recovery Center → Provide one controlled workspace for failed workflow executions.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-251?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Act on workflow instance.
- [ ] Every transition is wired: `ADM-248`.
- [ ] Every gated control is gated: `APPROVAL_ACT`, `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-252` SLA, Escalation & Bottleneck Monitor

**Monitor workflows approaching or exceeding configured time limits. (merged into BO-391 Live Escalation Operations Center).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task VM-ADM-252 |
| Who uses it | venue |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | `instanceId` (navigation) |
| Route | `/platform/sla-escalation-bottleneck-monitor-adm-252` |

**What the spec says about it.** **Merged into BO-391 Live Escalation Operations Center** (decided 2 October 2026, Chinmay: DEC-100 and the pre-apply round, "duplicate screens: merge as proposed"; CHG-MOV-002). On one platform it declared the same operations as BO-391 (check-screen-wiring S-DUP-SCREEN). **One implementation, both ids kept**, as the M24-03 merges do: this id stays for traceability and routes to BO-391, and nothing on it is built separately. **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Workflows approaching or past their time limits, the longest-waiting steps and escalation levels.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Within SLA** (metric tile)

**At Risk** (metric tile)

**Breached** (metric tile)

**Escalated** (metric tile)

**Minutes** (metric tile)

**Minutes** (metric tile)

**Longest Waiting Step** (metric tile)

**Every sla escalation bottleneck** (data table)

| Shows | Format | Notes |
|---|---|---|
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Escalation level | text | Escalation Level |
| Final outcome | text | Final Outcome |

**The selected sla escalation bottleneck** (detail panel): The pack groups this record's detail under its own headings: “Purchase Order Approval”, “Breakdown”.

| Shows | Format | Notes |
|---|---|---|
| Workflow | text | Workflow |
| Instance | text | Instance |
| Current step | text | Current Step |
| Owner | text | Owner |
| Started | 1 Oct 2026, 14:30 | Started |
| Time remaining | 1,234 | Minutes until breach; negative once breached |
| Escalation level | text | Escalation Level |
| Final outcome | text | Final Outcome |

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** Reassign, Escalate, Extend SLA, Add Backup Approver, Change Priority. Each needs attaching to the control it gates, or the screen needs the control.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Act on workflow instance (primary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*
- → `BO-391` Live Escalation Operations Center: *Open Live Escalation Operations Center*; carries `instanceId`

**What opens over it**

- modal *Act on workflow instance*: **Collects what `actOnWorkflowInstance` sends before it is called.** Required: `action`, `reason`. Optional: `workflowStepExecutionId`, `workflowExceptionId`, `assigneePrincipalId`, `alternativeNodeId`, `correctedInput`, `extendByMinutes`, `priority`. Dismissing sends nothing; the screen behind is …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sla escalation bottleneck list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sla escalation bottleneck untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sla escalation bottleneck yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the sla escalation bottleneck are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-391 Live Escalation Operations Center requires; this id has no operation of its own since the merge, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds APPROVAL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_ACT for Act on workflow instance. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*
- **actOnWorkflowInstance answers 409**: Show it as something the person can act on, not a failure: The instance is completed or cancelled, the action does not apply in its current status (for example `resume` on an instance that has not failed), or the step to skip is an approval node *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*
- **actOnWorkflowInstance answers 422**: Show it as something the person can act on, not a failure: A field the action needs is missing (assigneePrincipalId, extendByMinutes, priority, workflowExceptionId), the node is not skippable or the alternative is not an allowed edge, or the assignee is the requester of the approval *(source: contracts/spine/approvals.yaml#actOnWorkflowInstance)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Within SLA: 3 h 20 min
  At Risk: 0
  Breached: 5
  Escalated: 74
  Minutes: 233
  Longest Waiting Step: 3 h 20 min
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-391 Live Escalation Operations Center requires; this id has no operation of its own since the merge, so it names that screen's.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-252` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-252`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-252?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Act on workflow instance.
- [ ] Every transition is wired: `ADM-248`, `BO-391`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-253` Automation Execution & Autonomous Action Monitor

**Provide visibility and governance over actions executed automatically by TICVAI. This becomes especially important as TICVAI becomes more AI-driven.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task VM-ADM-253 |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/automation-execution-autonomous-action-monitor-adm-253` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** Contract gap recorded 2 October 2026 (CHG-WIR-024): A read listing automated and autonomous action executions (what ran, when, on whose rule, outcome), paged; createAutomationAutonomouAction should …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Actions TICVAI executed automatically: successful, failed, needing human confirmation, reversed; with the governance to suspend an automation.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- The only operation creates an autonomous action; nothing lists executions. (CHG-WIR-024)

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: createAutomationAutonomouAction (APPROVAL_CONFIGURE). (CHG-MOV-001).

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

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
today:
  automatedActions: 1840
  failed: 6
  needingConfirmation: 12
  reversed: 1
```

#### Permissions

- `createAutomationAutonomouAction` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-253` · status **notStarted** · provenance generated
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
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task VM-ADM-254 |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/cross-module-orchestration-monitor-adm-254` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A workflow spanning several services (e.g. group booking confirmation) step by step across modules.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listCrossModuleOrchestration (APPROVAL_VIEW). (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

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
| Empty, first run (`?state=emptyFirstRun`) | No cross-module orchestration yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the cross-module orchestration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listCrossModuleOrchestration (CrossModuleOrchestrationMonitorView):
- status: active
  started: 01/10/2026 09:14
  completed: 01/10/2026 09:14
  duration: 12
  failureHandling: waits
- status: pending
  started: 30/09/2026 18:02
  completed: 30/09/2026 18:02
  duration: 3
  failureHandling: retries
```

#### Permissions

- `listCrossModuleOrchestration` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-254` · status **notStarted** · provenance generated
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
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task VM-ADM-255 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§Analyze; Measure; Compare) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-analytics-process-performance-adm-255` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Workflow performance: volume, completion, failure, automation, escalation, rework, SLA compliance.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listWorkflowProcessPerformance (REPORT_VIEW_VENUE). (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

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

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (Transaction Value)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. Across tenants or regions figures in different currencies are never summed into one total; group by currency, or label the converted figure with its rate and time. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `listWorkflowProcessPerformance` (onLoad, Workflow Analytics & Process Performance)

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `listWorkflowProcessPerformance`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow analytics process list; the counts above it resolve separately. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow analytics process untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow analytics process yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow analytics process are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Workflow Volume: 128
  Completion Rate: 87%
  Failure Rate: 71%
  Average Completion Time: 3 h 20 min
  Approval Time: 42 min
  Automation Rate: 71%
  Escalation Rate: 94%
  Rejection Rate: 87%
  Rework Rate: 71%
  SLA Compliance: 94%
```

#### Permissions

- `listWorkflowProcessPerformance` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-255` · status **notStarted** · provenance generated
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
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task VM-ADM-256 |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Identify; Display) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/process-optimization-automation-opportunity-center-adm-256` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Processes worth simplifying or automating, by volume, steps, duration and exception rate.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listProcessAutomationOpportunity (REPORT_VIEW_VENUE). (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

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
| Average duration | 1,234 | Minutes |
| Approval rate | 12.5% | Approval Rate |
| Exception rate | 12.5% | Exception Rate |

**The selected process optimization automation** (detail panel): The pack groups this record's detail under its own headings: “Low-Value Refund Approval”, “Before changing anything”, “Estimated result”.

| Shows | Format | Notes |
|---|---|---|
| Opportunity type | chip: Repetitive approval, Unnecessary approval, High manual work, Excessive rework, Long … | Kind of improvement opportunity |
| Duplicate steps | text | not in the schema: `Duplicate Steps` |
| Process | text | Process |
| Module | text | Module |
| Monthly volume | 1,234 | Monthly Volume |
| Average duration | 1,234 | Minutes |
| Approval rate | 12.5% | Approval Rate |
| Exception rate | 12.5% | Exception Rate |

**Data it reads**: `listProcessAutomationOpportunity` (onLoad, Process Optimization & Automation Opportunity Center)

**Where the user goes next**

- → `ADM-248` Workflow Operations Command Center: *Returns to the board's landing screen*; calls `listProcessAutomationOpportunity`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The process optimization automation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the process optimization automation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No process optimization automation yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the process optimization automation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listProcessAutomationOpportunity (ProcessOptimizationAutomationOpportunityCenterView):
- opportunityType: repetitiveApproval
  monthlyVolume: 12
  currentSteps: 12
  averageDuration: 12
  manualSteps: 12
  approvalRate: 12
- opportunityType: unnecessaryApproval
  monthlyVolume: 3
  currentSteps: 3
  averageDuration: 3
  manualSteps: 3
  approvalRate: 3
```

#### Permissions

- `listProcessAutomationOpportunity` → `REPORT_VIEW_VENUE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-256` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-256`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 16: Works in Process Optimization & Automation Opportunity Center → Identify business processes that should be simplified, redesigned or automated. This is where TICVAI moves beyond simply running workflows.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
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
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · task VM-ADM-257 |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Analyze) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/ai-workflow-intelligence-autonomous-governance-center-adm-257` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001). It configures a record the venue owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI observations across rules and workflows with recommendations that become draft changes, never applied directly.

**Fixed on main** (the package already carries these; draw what it says): The table has no columns. (CHG-MOV-005); Calls tenant-permission operations with no tenant picker and no platform-staff grant: listWorkflowAutonomouGovernance (APPROVAL_VIEW). (CHG-MOV-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-MOV-003).

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
| Use case | text | Use Case |
| AI service | text | AI Service |
| Autonomy level | chip: Observe, Recommend, Prepare, Governed automation, Autonomous low risk | Level 0 to 4; approval decisions are held at observe |
| Decision scope | text | Decision Scope |
| Confidence threshold | 1,234.5 | Confidence Threshold |
| Human approval requirement | text | Human Approval Requirement |
| Execution volume | 1,234 | Execution Volume |
| Exception rate | 12.5% | Exception Rate |
| Override rate | 12.5% | Override rate |
| Last review | 1 Oct 2026, 14:30 | Last Review |
| Owner | text | Owner |

**The selected workflow intelligence autonomous** (detail panel): The pack groups this record's detail under its own headings: “Natural-Language Questions”, “Actual common process”, “Automation”, “Approval Simplification”, “SLA”, “Workflow Redesign”.

| Shows | Format | Notes |
|---|---|---|
| Use case | text | Use Case |
| AI service | text | AI Service |
| Autonomy level | chip: Observe, Recommend, Prepare, Governed automation, Autonomous low risk | Level 0 to 4; approval decisions are held at observe |
| Decision scope | text | Decision Scope |
| Confidence threshold | 1,234.5 | Confidence Threshold |
| Human approval requirement | text | Human Approval Requirement |
| Execution volume | 1,234 | Execution Volume |
| Exception rate | 12.5% | Exception Rate |
| Override rate | 12.5% | Override rate |
| Last review | 1 Oct 2026, 14:30 | Last Review |
| Owner | text | Owner |

**Data it reads**: `listWorkflowAutonomouGovernance` (onLoad, AI Workflow Intelligence & Autonomous Governance Center)

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The workflow intelligence autonomous list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the workflow intelligence autonomous untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No workflow intelligence autonomous yet. Offers no create action: nothing on this screen creates one, so for a monitor or a queue an empty list is the good outcome. Distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the workflow intelligence autonomous are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listWorkflowAutonomouGovernance (AiWorkflowIntelligenceAutonomousGovernanceCenterView):
- autonomyLevel: observe
  confidenceThreshold: 12
  executionVolume: 12
- autonomyLevel: recommend
  confidenceThreshold: 3
  executionVolume: 3
```

#### Permissions

- `listWorkflowAutonomouGovernance` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI actions in progress are shown step by step in an AI action command center; if a process only partly completes (e.g. missing information) it rolls back rather than leaving a product half-configured, and a full change history records everything AI modified. *(client request · MoM 21 Sep 2026, 4.9 Core AI Platform — AI Tools, Agents & Action Orchestration · DI-965)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-257` · status **notStarted** · provenance generated
- Client workshop board: `wireframes/WS137 Rules  Workflow  Approval   Automation Engine Board 2.dc.html#adm-257`
- Workshop pack: Rules__Workflow__Approval___Automation_Engine_Reference.pdf board 2
- Flow F165 *Rules Workflow Approval Automation Engine board 2: Workflow Operations Command …*, step 18: Works in AI Workflow Intelligence & Autonomous Governance Center → Create the AI intelligence layer across TICVAI's entire rules, workflow and automation ecosystem. This is the management-level AI brain for Area 13.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-257?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] No transition is declared; back returns where the user came from.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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
"listCrossModuleOrchestration": {"method":"GET","path":"/cross-module-orchestration","contract":"approvals","summary":"Cross-Module Orchestration Monitor","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"correlationId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProcessAutomationOpportunity": {"method":"GET","path":"/process-automation-opportunity","contract":"approvals","summary":"Process Optimization & Automation Opportunity Center","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"opportunityType","in":"query","required":false},{"name":"module","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
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
"AiWorkflowIntelligenceAutonomousGovernanceCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over the AI use-case register, which belongs to the AI service (the AI design is under review, 29 September); not an approvals table and not read directly from here","description":"**What AI Workflow Intelligence & Autonomous Governance Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"useCaseId":{"type":"string","description":"AI use case identifier"},"aiModel":{"type":"string","description":"AI Model"},"aiService":{"type":"string","description":"AI Service"},"useCase":{"type":"string","description":"Use Case"},"autonomyLevel":{"type":"string","enum":["observe","recommend","prepare","governedAutomation","autonomousLowRisk"],"description":"Level 0 to 4; approval decisions are held at observe"},"decisionScope":{"type":"string","description":"Decision Scope"},"confidenceThreshold":{"type":"number","description":"Confidence Threshold"},"humanApprovalRequirement":{"type":"string","description":"Human Approval Requirement"},"executionVolume":{"type":"integer","description":"Execution Volume"},"exceptionRate":{"type":"number","description":"Exception Rate"},"lastReview":{"type":"string","format":"date-time","description":"Last Review"},"owner":{"type":"string","description":"Owner"},"overrideRate":{"type":"number","description":"Override rate"}},"required":["useCaseId"]},
"AutomationExecutionAutonomousActionMonitorInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; updates approvals.automation status (schema Automation) (data model for the agreed operations, 29 September)","description":"**What Automation Execution & Autonomous Action Monitor submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"command":{"type":"string","enum":["pause","resume","disable","killSwitch"],"description":"Control command"},"automationId":{"type":"string","description":"Automation to control"},"reason":{"type":"string","description":"Why the automation is being controlled"}},"required":["automationId","command"]},
"AutomationExecutionAutonomousActionMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.automation and approvals.automation_execution (data model for the agreed operations, 29 September)","description":"**What Automation Execution & Autonomous Action Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"command":{"type":"string","enum":["pause","resume","disable","killSwitch"],"description":"Control command"},"automationId":{"type":"string","description":"Automation to control"},"automatedActionsToday":{"type":"integer","description":"Automated Actions Today"},"successful":{"type":"integer","description":"Successful"},"failed":{"type":"integer","description":"Failed"},"humanConfirmationRequired":{"type":"integer","description":"Actions waiting for human confirmation"},"reversed":{"type":"integer","description":"Reversed"},"suspended":{"type":"integer","description":"Suspended"},"estimatedManualActionsAvoided":{"type":"integer","description":"Estimated Manual Actions Avoided"},"estimatedTimeSaved":{"type":"integer","description":"Minutes"},"automation":{"type":"string","description":"Automation"},"businessObject":{"type":"string","description":"Business Object"},"rule":{"type":"string","description":"Rule"},"action":{"type":"string","description":"Action"},"result":{"type":"string","description":"Result"},"confidenceWhereAiAssisted":{"type":"number","description":"Confidence of an AI-assisted non-approval action; never set for approve or reject"},"executionTime":{"type":"string","format":"date-time","description":"Execution Time"},"status":{"type":"string","enum":["active","paused","disabled","killSwitched"],"description":"Status"},"reason":{"type":"string","description":"Why the automation is being controlled"}},"required":["automationId","command"]},
"CrossModuleOrchestrationMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_step_execution joined to approvals.workflow_instance by correlation id (data model for the agreed operations, 29 September)","description":"**What Cross-Module Orchestration Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"service":{"type":"string","description":"Service"},"action":{"type":"string","description":"Action"},"status":{"type":"string","enum":["notStarted","running","waiting","successful","failed","compensated"],"description":"Status"},"started":{"type":"string","format":"date-time","description":"Started"},"completed":{"type":"string","format":"date-time","description":"Completed"},"duration":{"type":"integer","description":"Seconds"},"inputOutput":{"type":"string","description":"Input/Output"},"failureHandling":{"type":"string","enum":["waits","retries","rollsBack","continuesPartially","requiresHumanIntervention"],"description":"What the workflow does after this node fails"},"retries":{"type":"integer","description":"Retries"},"correlationId":{"type":"string","description":"a common correlation/workflow ID"}},"required":["correlationId","service"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ProcessOptimizationAutomationOpportunityCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — aggregated from approvals.workflow_instance and workflow_step_execution per process (data model for the agreed operations, 29 September)","description":"**What Process Optimization & Automation Opportunity Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"opportunityType":{"type":"string","enum":["repetitiveApproval","unnecessaryApproval","highManualWork","excessiveRework","longWaitingTime","duplicateSteps","highFailureRate","lowRiskManualAction","processBottleneck"],"description":"Kind of improvement opportunity"},"process":{"type":"string","description":"Process"},"module":{"type":"string","description":"Module"},"monthlyVolume":{"type":"integer","description":"Monthly Volume"},"currentSteps":{"type":"integer","description":"Current Steps"},"averageDuration":{"type":"integer","description":"Minutes"},"manualSteps":{"type":"integer","description":"Manual Steps"},"approvalRate":{"type":"number","description":"Approval Rate"},"exceptionRate":{"type":"number","description":"Exception Rate"},"estimatedOpportunity":{"type":"string","description":"Estimated Opportunity"}},"required":["process"]},
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
