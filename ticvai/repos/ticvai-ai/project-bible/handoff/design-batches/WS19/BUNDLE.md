# WS19 — Approval Workflows and Governance board 7

**10 screens · 13 operations · 15 schemas · 6 permissions**

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
| `ADM-349` | Approval Integration Command Center | B | 0 | 0 | 6 | 0 | 0 | 3 | — | notStarted (—) |
| `ADM-350` | Module Integration Registry | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-351` | Approval API Management | B | 9 | 37 | 5 | 21 | 0 | 3 | — | notStarted (—) |
| `ADM-352` | Workflow Event Framework | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `ADM-353` | Webhook Configuration & Subscription Manager | B–D | 5 | 0 | 5 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-354` | External Workflow System Integration | A | 22 | 16 | 5 | 1 | 1 | 0 | — | notStarted (—) |
| `ADM-355` | Data & Workflow Mapping Studio | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-356` | Integration Security & Access Control | B | 2 | 34 | 6 | 18 | 0 | 0 | — | notStarted (—) |
| `ADM-357` | Integration Monitoring, Error & Retry Center | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-358` | Integration Analytics & AI Health Advisor | B | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-350, ADM-352, ADM-355, ADM-357, ADM-358 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-349` Approval Integration Command Center

**Provide administrators and technical teams with a centralized overview of all systems connected to the Approval Engine.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29485 (VM-ADM-349) |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | commandCentre (compact density): the pack gives this screen a metric directory (§KPI Cards) and no per-row directory — measures over a population the screen does not itself list. The tiles are the pack's, not a tenant licence's |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-integration-command-center-adm-349` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Systems connected to the approval engine: modules, external providers, dispatches, failures.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listCrossModuleOrchestration (APPROVAL_VIEW) … (CHG-SBO-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

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

- → `BO-100` Venue Home: *Back to Venue Home*
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
| Empty, first run (`?state=emptyFirstRun`) | **Nothing to show yet**: the figures fill as activity is recorded. Offers no create action — a monitor creates nothing — and says so rather than showing empty tiles. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the approval integration are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
metric tiles:
  Connected TICVAI Modules: 128
  External Integrations: 46
  API Requests Today: 312
  Workflow Events: 74
  Active Webhooks: 19
  Failed Requests: 2
  Integration Errors: 0
  Average Response Time: 42 min
```

#### Permissions

- `listCrossModuleOrchestration` → `APPROVAL_VIEW` (read) · staff
- `listApprovalExternalProviders` → `APPROVAL_VIEW` (read) · staff
- `listApprovalExternalDispatches` → `APPROVAL_VIEW` (read) · staff

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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-349` · status **notStarted** · provenance —
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
- [ ] Every transition is wired: `BO-100`, `ADM-358`, `ADM-350`, `ADM-351`, `ADM-352`, `ADM-353`, `ADM-354`, `ADM-355`, `ADM-356`, `ADM-357`.
- [ ] Every gated control is gated: `APPROVAL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-350` Module Integration Registry

**Define which TICVAI modules are allowed to initiate and consume approval workflows.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29480 (VM-ADM-350) |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/module-integration-registry-adm-350` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Which modules may start and consume approval workflows.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listCrossModuleOrchestration (APPROVAL_VIEW). (CHG-SBO-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

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
| Empty, first run (`?state=emptyFirstRun`) | No module integration registry yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the module integration registry are still there. Names the active filter and offers to clear it. |
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-350` · status **notStarted** · provenance —
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
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29572 (VM-ADM-351) |
| Who uses it | venue staff holding `DEVELOPER_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§API Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/approval-api-management-adm-351` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Approval API Management configures and monitors the APIs that create, read and process approval requests; it was wired to listApprovalRequests, the approval …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The approval API as configured for external callers: endpoint, version, authentication, limits.

**Fixed on main** (the package already carries these; draw what it says): Only listApprovalRequests. (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

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
| Module | field | — | — | `listApiScopes` ?module |
| From | date picker | — | — | `getApiUsage` ?from |
| To | date picker | — | — | `getApiUsage` ?to |

#### Outputs: what the screen shows and produces

**Shown**

**Approval API scopes** (data table, from `listApiScopes`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| Scope | text | e.g. `ticketing.read`. |
| Module | text | — |
| Access | chip: Read, Write | — |
| Description | text | — |
| Operations | list or chips (count when long) | — |
| Contract | text | — |
| Operation | text | — |
| Licensed | yes / no (icon or chip) | Whether the caller's tenant licenses the module (`ApiLicence.licensedModules`). |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Clients** (data table, from `listApiClients`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Developer | the name it points at, never the id | — |
| Name | text | — |
| Client | text | — |
| Environment | chip: Sandbox, Production | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. |
| Scopes | list or chips (count when long) | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the … |
| Issued by | chip: Partner, Ticvai | Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`. |
| Certification listing | the name it points at, never the id | For a production client, the certified integration it was issued against. |
| Credential ttl days | 1,234 | Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry). |
| Expires at | 1 Oct 2026, 14:30 | When the key stops working unless rotated. No token is issued after it. |
| Allowed tenants | list or chips (count when long) | 13.1.46. Which tenants this client may act for. |
| Ip allow list | list or chips (count when long) | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the … |
| Status | chip: Active, Suspended, Revoked | — |
| Last used at | 1 Oct 2026, 14:30 | A credential unused for a year is a credential nobody will notice being stolen. |

**Usage** (detail panel, from `getApiUsage`)

| Shows | Format | Notes |
|---|---|---|
| Total calls | 1,234 | — |
| Success rate | 12.5% | — |
| Client error rate | 12.5% | 4xx — the integrator's problem. Separated because a single error rate lets both sides blame the other. |
| Server error rate | 12.5% | 5xx — TICVAI's problem. |
| P50 latency ms | 1,234.5 | — |
| P95 latency ms | 1,234.5 | — |
| P99 latency ms | 1,234.5 | — |
| Quota breaches | 1,234 | — |
| By operation | list or chips (count when long) | — |
| Operation | text | — |
| Calls | 1,234 | — |
| Error rate | 12.5% | — |

**Data it reads**: `listApiScopes` (onLoad, The approval scopes the API exposes, read and write); `listApiClients` (onLoad, The integrations that hold approval scopes); `getApiUsage` (onLoad, Calls, errors, latency and success rate of the approval API)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The approval api configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the approval api untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No approval api configured yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Endpoint: 128
  API version: 19
  Authentication: 128
  tenant context: Marina Leisure Group
  request schema: 312
  response schema: 19
  retry policy: 74
  rate limit: OMR 48.500
```

#### Permissions

- `listApiScopes` → `DEVELOPER_VIEW` (read) · public, staff, partner
- `listApiClients` → `DEVELOPER_VIEW` (read) · staff, partner
- `getApiUsage` → `DEVELOPER_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

21 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.24 | To provide the ability to enable license for the API only for the specific module. Example. APIs are exposed only for ticketing excluding resource management, Seating Module, etc | Developer & API Management | CONTRACTED | `listApiScopes` |
| 2.7.52 | System shall allow approved B2B partners to request, generate, manage, rotate, and revoke API credentials. Access shall be restricted by partner permissions, products, quotas, rate limits, IP … | Ticketing Sales | CONTRACTED | data `ApiClient` |
| 7.1.25 | The system shall support dedicated API users, integration users, service accounts, API keys, credential rotation, expiry controls, IP restrictions, and audit logging. | F&B POS | CONTRACTED | data `ApiClient` |
| 13.1.11 | API Key Management - System shall support API key generation and management. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.13 | OAuth Support - System shall support OAuth authentication. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.14 | Token Management - System shall support access token management. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.15 | Credential Revocation - System shall support credential revocation. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.21 | API Explorer - System shall provide interactive API testing tools. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.22 | SDK Availability - System shall provide SDKs for supported platforms. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.23 | Code Samples - System shall provide implementation examples. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.24 | Postman Collections - System shall provide Postman collections. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.38 | IP Whitelisting - System shall support IP whitelisting. | Developer & API Management | CONTRACTED | data `ApiClient` |
| … 9 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-351` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-351`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 4: Works in Approval API Management → Configure and monitor APIs used to create, retrieve and process approval requests. The matrix explicitly requires approval workflows to be exposed through APIs.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state.
- [ ] Every output is drawn (37 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-351?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `DEVELOPER_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-352` Workflow Event Framework

**Configure the business events published by the Approval Engine. The matrix requires workflow events to be published through the platform event framework.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29481 (VM-ADM-352) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `DEVELOPER_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/workflow-event-framework-adm-352` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The business events the approval engine publishes, with their schemas.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: setTriggerActionCross (APPROVAL_CONFIGURE) … (CHG-SBO-001).

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

#### Edge cases to draw

- **Can read but not change (holds DEVELOPER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_CONFIGURE for setTriggerActionCross. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#setTriggerActionCross)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listWebhookEventTypes (WebhookEventCatalogueEntry):
- name: Refund above AED 500 - Abu Dhabi
  version: 12
  description: Guest charged twice at Main Gate Till 3
- name: Group discount approval
  version: 3
  description: Group of 40 from Desert Gate Tours
```

#### Permissions

- `setTriggerActionCross` → `APPROVAL_CONFIGURE` (configure) · staff
- `listWebhookEventTypes` → `DEVELOPER_VIEW` (read) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-352` · status **notStarted** · provenance —
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
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-353` Webhook Configuration & Subscription Manager

**Allow external or internal systems to subscribe to approval events. The source explicitly requires webhook notifications for approval events. (merged into BO-1074 Webhook Configuration).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Delivery Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/webhook-configuration-subscription-manager-adm-353` |

**What the spec says about it.** **Merged into BO-1074 Webhook Configuration** (decided 2 October 2026, Chinmay: "duplicate screens: merge as proposed"; CHG-CLN-003). On P08 it declared the same operations as BO-1074 (check-screen-wiring S-DUP-SCREEN). One implementation, both ids kept: this id stays for traceability and routes to BO-1074. **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **Webhook Configuration & Subscription Manager declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Webhook subscriptions to approval events: endpoint, events, timeout, retries, failure action and auto-disable threshold.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: createWebhookSubscription (DEVELOPER_MANAGE) … (CHG-SBO-001).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Timeout | select field | — | — | — | — | — | — |
| Retry count | select field | — | — | — | — | — | — |
| Retry interval | select field | — | — | — | — | — | — |
| failure action | select field | — | — | — | — | — | — |
| disable threshold | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*
- → `BO-1074` Webhook Configuration: *Open Webhook Configuration*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The webhook subscription configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the webhook subscription untouched. |
| Empty, first run (`?state=emptyFirstRun`) | Nothing set up yet. The create action is BO-1074's; this anchor offers none of its own. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks the permission BO-1074 Webhook Configuration requires; this id has no operation of its own since the merge, so it names that screen's. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds DEVELOPER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: DEVELOPER_MANAGE for createWebhookSubscription. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/public-api.yaml#createWebhookSubscription)*
- **createWebhookSubscription answers 422**: Show it as something the person can act on, not a failure: An entry in `eventTypes` is not in the webhook event catalogue. *(source: contracts/satellite/public-api.yaml#createWebhookSubscription)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
subscription:
  endpoint: https://hooks.marinaleisure.ae/approvals
  events:
  - approval.decided
  - approval.escalated
  timeoutSeconds: 10
  retries: 5
  disableAfterFailures: 20
```

#### Permissions

**A refused user sees:** Shown when the caller lacks the permission BO-1074 Webhook Configuration requires; this id has no operation of its own since the merge, so it names that screen's.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-353` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-353`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 8: Works in Webhook Configuration & Subscription Manager → Allow external or internal systems to subscribe to approval events. The source explicitly requires webhook notifications for approval events.

#### Acceptance for the design

- [ ] Every input above is drawn (5), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-353?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-349`, `BO-1074`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-354` External Workflow System Integration

**Allow TICVAI to integrate with third-party workflow/governance platforms when a client already operates an enterprise approval environment. The matrix specifically requires integration with third-party workflow systems.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 1 · needs the `core` module |
| Block | Block A · ticket #27937 (APP-SETUP-ADM-354) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE`, `APPROVAL_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/external-workflow-system-integration-adm-354` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): listApiClients was used as "External workflow systems"; API clients are developer integrations, and the providers are listApprovalExternalProviders (declared). … Integration direction, user and role mapping and synchronisation mode have no field on ApprovalExternalProvider; the screen binds what the provider record holds.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Connect a tenant's existing enterprise approval system (ServiceNow-style) so approval requests are sent out and decisions come back: the provider, direction, authentication, the mapping of kinds, people and statuses, retries and sync mode, and the dispatch log for resending what the other side never received.

**Fixed on main** (the package already carries these; draw what it says): listApiClients is used as "External workflow systems". (CHG-WIR-021); Eight selectFields with no binding (system name, direction, authentication, mappings, error handling, sync mode). (CHG-SBO-011); listApprovalExternalDispatches and recordExternalApprovalDecision exist and are not declared. (CHG-WIR-021); Calls tenant-permission operations with no tenant picker and no platform-staff grant: listApiClients (DEVELOPER_VIEW) … (CHG-WIR-021).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| System name | text field | optional | — | — | — | — | `ApprovalExternalProvider.name` |
| Authentication | radio group | optional | Oauth client credentials | Bearer token · Basic · Oauth client credentials · Mutual tls | — | — | `ApprovalExternalProvider.outboundAuth` |
| Workflow mapping | repeatable rows | optional | — | — | — | Stored whole on the provider row (`request_mapping`, jsonb; 3 October 2026, CHG-R1S-020: the r1 gate found no column held it). | `ApprovalExternalProvider.requestMapping` |
| Status mapping | repeatable rows | optional | — | at least 2 | — | The provider's outcome values and the decision each means. At least one maps to `approve` and one to `reject`. | `ApprovalExternalProvider.decisionMapping` |
| Error handling | segmented control | optional | Fall back to roles | Fall back to roles · Escalate · Reject | — | — | `ApprovalExternalProvider.onTimeout` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | segmented control | — | Active · Paused · Disabled | `listApprovalExternalProviders` ?status |
| Provider | picker: choose a provider | — | — | `listApprovalExternalDispatches` ?providerId |
| Request | picker: choose a request | — | — | `listApprovalExternalDispatches` ?requestId |
| Status | select | — | Pending · Sent · Failed · Decided · Timed out · Cancelled | `listApprovalExternalDispatches` ?status |

**Form: Save provider** (modal, opened by *Save provider*; *Save provider* calls `setApprovalExternalProvider`, *Cancel* sends nothing)

**Collects what `setApprovalExternalProvider` sends before it is called.** Required: `code`, `name`, `endpointUrl`, `apiClientId`, `decisionMapping`. Optional: `outboundAuth`, `outboundCredential`, `signingSecret`, `requestMapping`, `timeoutMinutes`, `onTimeout`, `maxAttempts`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | The provider's stable name, and the key `setApprovalExternalProvider` upserts on. | `setApprovalExternalProvider` body |
| Name `name` | text field | required | — | — | — | — | `setApprovalExternalProvider` body |
| Endpoint URL `endpointUrl` | text field | required | — | — | — | `https` only. Where a request level is sent. | `setApprovalExternalProvider` body |
| Outbound auth `outboundAuth` | radio group | optional | Oauth client credentials | Bearer token · Basic · Oauth client credentials · Mutual tls | — | — | `setApprovalExternalProvider` body |
| Outbound credential `outboundCredential` | text field | optional | — | — | — | The credential TICVAI presents to the provider. Write-only, never returned, kept on a replace that omits it. | `setApprovalExternalProvider` body |
| Signing secret `signingSecret` | text field | optional | — | — | — | Signs every request TICVAI sends, as webhook deliveries are signed, so the provider can tell it came from TICVAI. | `setApprovalExternalProvider` body |
| API client `apiClientId` | picker: choose an api client | required | — | It must hold `APPROVAL_DECIDE`; `recordExternalApprovalDecision` from any other client is refused. | shows names, sends the id | The public-api client the provider calls back as. It must hold `APPROVAL_DECIDE`; `recordExternalApprovalDecision` from any other client is refused. | `setApprovalExternalProvider` body |
| Request mapping `requestMapping` | repeatable rows | optional | — | — | — | Stored whole on the provider row (`request_mapping`, jsonb; 3 October 2026, CHG-R1S-020: the r1 gate found no column held it). | `setApprovalExternalProvider` body |
| From `requestMapping[].from` | text field | required | — | — | — | A field of `ApprovalRequest`, e.g. `amount`, `kind`, `subjectId`, `requestedByPrincipalId`. | `setApprovalExternalProvider` body |
| To `requestMapping[].to` | text field | required | — | — | — | The provider's field name. | `setApprovalExternalProvider` body |
| Decision mapping `decisionMapping` | repeatable rows | required | — | at least 2 | — | The provider's outcome values and the decision each means. At least one maps to `approve` and one to `reject`. | `setApprovalExternalProvider` body |
| External value `decisionMapping[].externalValue` | text field | required | — | — | — | — | `setApprovalExternalProvider` body |
| Decision `decisionMapping[].decision` | radio group | required | — | Approve · Reject · Return · Request information | — | — | `setApprovalExternalProvider` body |
| Timeout minutes `timeoutMinutes` | number field (minutes) | optional | 1440 | — | — | How long a level waits for the provider before `onTimeout` applies. | `setApprovalExternalProvider` body |
| On timeout `onTimeout` | segmented control | optional | Fall back to roles | Fall back to roles · Escalate · Reject | — | — | `setApprovalExternalProvider` body |
| Max attempts `maxAttempts` | number field | optional | 5 | — | — | Delivery attempts, with backoff, before a dispatch is `failed` and the level falls back as on timeout. | `setApprovalExternalProvider` body |
| Status `status` | segmented control | optional | Active | Active · Paused · Disabled | — | `paused` sends nothing and every level that names it falls back at once; the platform sets `disabled` after repeated failures, as it disables a failing webhook. | `setApprovalExternalProvider` body |

Errors to draw in the form: 422 The endpoint is not `https`, the API client is not an active client of the tenant, or the decision mapping has no value for `approve` or for `reject`

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Provider**: Bound to the ApprovalExternalProvider schema; a secret is entered once and stored as a reference, never shown again. *(source: contracts/spine/approvals.yaml#setApprovalExternalProvider)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setApprovalExternalProvider: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/approvals.yaml#setApprovalExternalProvider)*

#### Outputs: what the screen shows and produces

**Shown**

**Dispatches** (data table, from `listApprovalExternalDispatches`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Request | the name it points at, never the id | — |
| Provider | the name it points at, never the id | — |
| Level | 1,234 | — |
| Status | chip: Pending, Sent, Failed, Decided, Timed out, Cancelled | — |
| Attempt count | 1,234 | — |
| External reference | text | The provider's own id for the item, as it acknowledged or called back with. |
| Last response code | 1,234 | — |
| Last error | text | — |
| Sent at | 1 Oct 2026, 14:30 | — |
| Answered at | 1 Oct 2026, 14:30 | — |
| External outcome | text | The provider's own outcome value, before mapping. |
| External approver ref | text | Who decided in the provider's system, as it named them. |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save provider (primary button) | `setApprovalExternalProvider` PUT `/approval-external-providers` | ApprovalExternalProvider | ApprovalExternalProvider | 422 The endpoint is not `https`, the API client is not an active client of the tenant, or the decision mapping has no value for `approve` or for `reject` | opens modal first |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Dispatch log**: Each request sent, its status, attempts and last error; failed ones offer Resend. *(source: contracts/spine/approvals.yaml#listApprovalExternalDispatches; DI-733)*

**Data it reads**: `listApprovalExternalProviders` (onLoad, Registered external workflow systems); `listApprovalExternalDispatches` (onLoad, What was sent to each external workflow system, and what …)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The external workflow system configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the external workflow system untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No external workflow system configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 422 The endpoint is not `https`, the API client is not an active client of the tenant, or the decision mapping has no value for `approve` or for `reject` |

#### Edge cases to draw

- **Can read but not change (holds APPROVAL_VIEW, DEVELOPER_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: APPROVAL_CONFIGURE for setApprovalExternalProvider. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/approvals.yaml#setApprovalExternalProvider)*
- **setApprovalExternalProvider answers 422**: Show it as something the person can act on, not a failure: The endpoint is not `https`, the API client is not an active client of the tenant, or the decision mapping has no value for `approve` or for `reject` *(source: contracts/spine/approvals.yaml#setApprovalExternalProvider)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
provider:
  name: Marina Group ServiceNow
  direction: bidirectional
  auth: oauth2
  syncMode: webhook
  kindsMapped: 4
```

#### Permissions

- `listApprovalExternalProviders` → `APPROVAL_VIEW` (read) · staff
- `setApprovalExternalProvider` → `APPROVAL_CONFIGURE` (configure) · staff
- `listApprovalExternalDispatches` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 11.1.65 | External Workflow Integration - System shall support integration with third-party workflow systems. | Approval Workflows & Governance | CONTRACTED | `setApprovalExternalProvider` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-354` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-354`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 10: Works in External Workflow System Integration → Allow TICVAI to integrate with third-party workflow/governance platforms when a client already operates an enterprise approval environment. The matrix specifically requires integration with …

#### Acceptance for the design

- [ ] Every input above is drawn (22), with its required mark, default, format and its error state (422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-354?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save provider.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `APPROVAL_CONFIGURE`, `APPROVAL_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-355` Data & Workflow Mapping Studio

**Map external system data to TICVAI's approval data model without requiring custom development for every integration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29482 (VM-ADM-355) |
| Who uses it | venue staff holding `APPROVAL_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/data-workflow-mapping-studio-adm-355` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **Data & Workflow Mapping Studio declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Map an external system's approval data to TICVAI's model.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: setTriggerActionCross (APPROVAL_CONFIGURE). (CHG-SBO-001).

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

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
external: ServiceNow u_amount
ticvai: amount
transform: minor units to AED 2 decimals
```

#### Permissions

- `setTriggerActionCross` → `APPROVAL_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-355` · status **notStarted** · provenance —
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
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29571 (VM-ADM-356) |
| Who uses it | venue staff holding `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`, `PERMISSION_VIEW` (1 configure, 2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `clientId` (navigation) |
| Route | `/platform/integration-security-access-control-adm-356` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Which applications and external systems may call the approval engine, under which policies.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Only listAuthorisationPolicies and an empty table. (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Draft · Pending approval · Active · Suspended · Retired | `listAuthorisationPolicies` ?status |
| Scope path | text field | — | — | `listAuthorisationPolicies` ?scopePath |

**Form: Suspend or reactivate** (modal, opened by *Suspend or reactivate*; *Suspend or reactivate* calls `setApiClientStatus`, *Cancel* sends nothing)

**Collects what `setApiClientStatus` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | segmented control | required | — | Active · Suspended | — | — | `setApiClientStatus` body |
| Reason `reason` | text area | optional | — | max length 500 | — | Required with `suspended`. | `setApiClientStatus` body |

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The client is `revoked`, which is terminal.; 422 `suspended` without a `reason`.

#### Outputs: what the screen shows and produces

**Shown**

**Permissions this screen separates** (banner): **The pack separates these permissions and no action on the screen claims them yet:** ☑ Create Approval Request, ☑ Read Status, ☑ Read History, ☐ Submit Approval Decision, ☐ Modify Workflow. Each needs attaching to the control it gates, or the screen needs the control.

**Integrations with access** (data table, from `listApiClients`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Developer | the name it points at, never the id | — |
| Name | text | — |
| Client | text | — |
| Environment | chip: Sandbox, Production | Bound to one, stated on the object rather than by naming convention. A key that works in both is a key somebody will use in the wrong one. |
| Scopes | list or chips (count when long) | Resolved against the tenant's licence at token issue (13.3.24). A scope granted here and not licensed there produces no token — and the … |
| Issued by | chip: Partner, Ticvai | Who generated the key (M17-06): a developer for a sandbox key, TICVAI for a production key issued on an approved `requestProductionAccess`. |
| Certification listing | the name it points at, never the id | For a production client, the certified integration it was issued against. |
| Credential ttl days | 1,234 | Key lifetime. Default 365 for production, 90 for sandbox (M17-06, configurable expiry). |
| Expires at | 1 Oct 2026, 14:30 | When the key stops working unless rotated. No token is issued after it. |
| Allowed tenants | list or chips (count when long) | 13.1.46. Which tenants this client may act for. |
| Ip allow list | list or chips (count when long) | 13.1.38. Required on a production client (17 September minutes, M17-07: endpoints are protected by IP allow-listing, not left open to the … |
| Status | chip: Active, Suspended, Revoked | — |
| Last used at | 1 Oct 2026, 14:30 | A credential unused for a year is a credential nobody will notice being stolen. |

**Authorisation policies** (data table, from `listAuthorisationPolicies`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Assigned by the server on `createAuthorisationPolicy`; the path names the policy on update. |
| Code | text | — |
| Name | text | — |
| Description | text | — |
| Is template | yes / no (icon or chip) | — |
| Permissions | list or chips (count when long) | Which permissions this policy speaks to. A policy with an empty list speaks to all of them, which is powerful enough that it is worth being … |
| Conditions | list or chips (count when long) | — |
| Attribute | chip: User.attribute, Employee.attribute, Employee.on shift, Membership.tier … | — |
| Key | text | For the `*.attribute` forms — which attribute, by code. |
| Operator | chip: Equals, Not equals, In, Not in, Greater than, Less than… | — |
| Value | text | The single comparand for `equals`, `notEquals`, `greaterThan`, `lessThan`, `contains` and `startsWith` — a string, number or boolean, by … |
| Values | list or chips (count when long) | — |
| Combining | chip: All must match, Any may match | — |
| Effect | chip: Permit, Deny | Deny wins over permit when two policies disagree. 3.3.32 asks for least-privilege, and a permit that can override a deny is not … |
| Priority | 1,234 | — |
| Applies to roles | list or chips (count when long) | — |
| Status | chip: Draft, Pending approval, Active, Suspended, Retired | Moved only by `setAuthorisationPolicyState`. A policy is created as a `draft`, and a status sent in a create or update body is ignored — … |
| Effective from | 1 Oct 2026, 14:30 | — |
| Effective to | 1 Oct 2026, 14:30 | — |
| Delegated admin roles | list or chips (count when long) | 3.3.35. Who may edit this policy without being a platform administrator. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Suspend or reactivate (secondary button) | `setApiClientStatus` POST `/api-clients/{clientId}/status` | inline | ApiClient | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The client is `revoked`, which is terminal.; 422 `suspended` without a `reason`. | opens modal first |

**Data it reads**: `listAuthorisationPolicies` (onLoad, Integration access control); `listApiClients` (onLoad, The applications and systems that can call the Approval …)

**Where the user goes next**

- → `ADM-349` Approval Integration Command Center: *Back to Approval Integration Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The integration security access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the integration security access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No integration security access yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration security access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The client is `revoked`, which is terminal.; 422 `suspended` without a `reason`. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listAuthorisationPolicies (AuthorisationPolicy):
- code: AQC-AUH
  name: AquaCove Abu Dhabi
  description: Guest charged twice at Main Gate Till 3
  isTemplate: true
  combining: allMustMatch
  effect: permit
- code: AQC-DXB
  name: Main Gate Till 3
  description: Group of 40 from Desert Gate Tours
  isTemplate: false
  combining: anyMayMatch
  effect: deny
```

#### Permissions

- `listAuthorisationPolicies` → `PERMISSION_VIEW` (read) · staff
- `listApiClients` → `DEVELOPER_VIEW` (read) · staff, partner
- `setApiClientStatus` → `DEVELOPER_MANAGE` (configure) · staff, partner

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.7.52 | System shall allow approved B2B partners to request, generate, manage, rotate, and revoke API credentials. Access shall be restricted by partner permissions, products, quotas, rate limits, IP … | Ticketing Sales | CONTRACTED | data `ApiClient` |
| 7.1.25 | The system shall support dedicated API users, integration users, service accounts, API keys, credential rotation, expiry controls, IP restrictions, and audit logging. | F&B POS | CONTRACTED | data `ApiClient` |
| 13.1.11 | API Key Management - System shall support API key generation and management. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.13 | OAuth Support - System shall support OAuth authentication. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.14 | Token Management - System shall support access token management. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.15 | Credential Revocation - System shall support credential revocation. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.21 | API Explorer - System shall provide interactive API testing tools. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.22 | SDK Availability - System shall provide SDKs for supported platforms. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.23 | Code Samples - System shall provide implementation examples. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.24 | Postman Collections - System shall provide Postman collections. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.38 | IP Whitelisting - System shall support IP whitelisting. | Developer & API Management | CONTRACTED | data `ApiClient` |
| 13.1.40 | Security Monitoring - System shall monitor API security events. | Developer & API Management | CONTRACTED | data `ApiClient` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-356` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS36 Approval Workflows and Governance Board 7.dc.html#adm-356`
- Workshop pack: Approval_Workflows_and_Governance_Reference.pdf board 7
- Flow F129 *Approval Workflows and Governance board 7: Approval Integration Command Center*, step 14: Works in Integration Security & Access Control → Govern which applications and external systems can access the Approval Engine.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (404, 409, 422).
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-356?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Suspend or reactivate.
- [ ] Every transition is wired: `ADM-349`.
- [ ] Every gated control is gated: `DEVELOPER_MANAGE`, `DEVELOPER_VIEW`, `PERMISSION_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-357` Integration Monitoring, Error & Retry Center

**Provide technical teams with real-time monitoring of integration failures.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29528 (VM-ADM-357) |
| Who uses it | venue staff holding `APPROVAL_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/integration-monitoring-error-retry-center-adm-357` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Integration failures in real time with retry.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listWorkflowExceptionFailure (APPROVAL_VIEW) … (CHG-SBO-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

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
| Empty, first run (`?state=emptyFirstRun`) | No integration monitoring error yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration monitoring error are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listApprovalExternalDispatches (ApprovalExternalDispatch):
- level: 12
  status: active
  attemptCount: 12
  lastResponseCode: 12
  sentAt: 01/10/2026 09:14
  answeredAt: 01/10/2026 09:14
- level: 3
  status: pending
  attemptCount: 3
  lastResponseCode: 3
  sentAt: 30/09/2026 18:02
  answeredAt: 30/09/2026 18:02
```

#### Permissions

- `listWorkflowExceptionFailure` → `APPROVAL_VIEW` (read) · staff
- `listApprovalExternalDispatches` → `APPROVAL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Approval integration screens cover API/webhook/external workflow connections with data mapping and retry handling (e.g. resending a request the external system did not receive). *(client request · MoM 8 Sep 2026, 4.18 API/Integration for the Approval Workflow · DI-733)*

Also apply: 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-357` · status **notStarted** · provenance —
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
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Platform · wave 3 · needs the `core` module |
| Block | Block B · ticket #29529 (VM-ADM-358) |
| Who uses it | venue staff holding `REPORT_VIEW_VENUE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/platform/integration-analytics-ai-health-advisor-adm-358` |

**What the spec says about it.** **Moved to Venue Management (P08) on 2 October 2026** (Chinmay, 2 October: the approvals workflow and matrix screens and the communication service screens move to Venue Management; CHG-CLN-003). It configures a record the tenant owns, so the venue's own staff use it here, inside the tenant's cell; TICVAI staff reach it only under a platform-staff grant into the tenant (R098), never from the console directly. The console's tenant picker and grant (CHG-SBO-001) came off with the move. The id is kept, so its tickets keep their keys.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Integration performance analytics for the approval engine.

**Fixed on main** (the package already carries these; draw what it says): Calls tenant-permission operations with no tenant picker and no platform-staff grant: listWorkflowProcessPerformance (REPORT_VIEW_VENUE). (CHG-SBO-001); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

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
| Empty, first run (`?state=emptyFirstRun`) | No integration analytics health yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the integration analytics health are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listWorkflowProcessPerformance (WorkflowAnalyticsProcessPerformanceView):
- workflowVolume: 12
  completionRate: 12
  failureRate: 12
  averageCompletionTime: 12
  approvalTime: 12
  automationRate: 12
  escalationRate: 12
  rejectionRate: 12
- workflowVolume: 3
  completionRate: 3
  failureRate: 3
  averageCompletionTime: 3
  approvalTime: 3
  automationRate: 3
  escalationRate: 3
  rejectionRate: 3
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

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#adm-358` · status **notStarted** · provenance —
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

**4 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getApiUsage": {"method":"GET","path":"/api-usage","contract":"public-api","summary":"Calls, errors, latency and success rate","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null}],"requestBody":null,"responds":"ApiUsageSummary"},
"listApiClients": {"method":"GET","path":"/api-clients","contract":"public-api","summary":"Registered clients for this developer","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ApiClient"},
"listApiScopes": {"method":"GET","path":"/api-scopes","contract":"public-api","summary":"The scope catalogue, one read and one write scope per module","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"module","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listApprovalExternalDispatches": {"method":"GET","path":"/approval-external-dispatches","contract":"approvals","summary":"What was sent to external workflow systems, and what came back","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"providerId","in":"query","required":false},{"name":"requestId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listApprovalExternalProviders": {"method":"GET","path":"/approval-external-providers","contract":"approvals","summary":"The external workflow systems approval levels may be sent to","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listAuthorisationPolicies": {"method":"GET","path":"/authorisation-policies","contract":"identity","summary":"Attribute-based authorisation policies","permission":"PERMISSION_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"scopePath","in":"query","required":null}],"requestBody":null,"responds":"AuthorisationPolicy"},
"listCrossModuleOrchestration": {"method":"GET","path":"/cross-module-orchestration","contract":"approvals","summary":"Cross-Module Orchestration Monitor","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"correlationId","in":"query","required":false},{"name":"status","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWebhookEventTypes": {"method":"GET","path":"/webhook-event-types","contract":"public-api","summary":"The events a webhook may subscribe to","permission":"DEVELOPER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"publisher","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkflowExceptionFailure": {"method":"GET","path":"/workflow-exception-failure","contract":"approvals","summary":"Workflow Exception, Failure & Recovery Center","permission":"APPROVAL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"errorType","in":"query","required":false},{"name":"module","in":"query","required":false},{"name":"priority","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkflowProcessPerformance": {"method":"GET","path":"/workflow-process-performance","contract":"approvals","summary":"Workflow Analytics & Process Performance","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workflow","in":"query","required":false},{"name":"module","in":"query","required":false},{"name":"venue","in":"query","required":false},{"name":"brand","in":"query","required":false},{"name":"businessProcess","in":"query","required":false},{"name":"department","in":"query","required":false},{"name":"approver","in":"query","required":false},{"name":"user","in":"query","required":false},{"name":"from","in":"query","required":false},{"name":"to","in":"query","required":false},{"name":"minTransactionValue","in":"query","required":false},{"name":"maxTransactionValue","in":"query","required":false}],"requestBody":null,"responds":"WorkflowAnalyticsProcessPerformanceView"},
"setApiClientStatus": {"method":"POST","path":"/api-clients/{clientId}/status","contract":"public-api","summary":"Suspend or reactivate an integration, reversibly","permission":"DEVELOPER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ApiClient"},
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
"ApiScope": {"type":"object","x-ticvai-persistence":"none — generated at release from x-ticvai-api-scope on each partner-callable operation","description":"**One module scope** (17 September minutes, M17-05): `{module}.read` or `{module}.write`, and the operations it opens.\n**A write scope never opens a catalogue write** (M17-04): `ticketing.write` opens carts, orders and holds for a partner or developer client, and no product, price list, price, channel capacity, lifecycle or alternative-code write, since those operations are not partner-callable and carry no `x-ticvai-api-scope`. Only a platform-staff `ApiLicence.catalogueWriteException` opens one, for one named client.\n","required":["scope","module","access"],"properties":{"scope":{"type":"string","description":"e.g. `ticketing.read`."},"module":{"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},"access":{"type":"string","enum":["read","write"]},"description":{"type":"string"},"operations":{"type":"array","items":{"type":"object","properties":{"contract":{"type":"string"},"operationId":{"type":"string"}}}},"licensed":{"type":"boolean","description":"Whether the caller's tenant licenses the module (`ApiLicence.licensedModules`)."}}},
"ApiUsageSummary": {"type":"object","description":"13.1.16 to 13.1.20, 13.1.41 to 13.1.45. **One endpoint because they are one question asked five ways.**\n","properties":{"totalCalls":{"type":"integer"},"successRate":{"type":"number"},"clientErrorRate":{"type":"number","description":"**4xx — the integrator's problem.** Separated because a single error rate lets both sides blame the other.\n"},"serverErrorRate":{"type":"number","description":"5xx — TICVAI's problem."},"p50LatencyMs":{"type":"number"},"p95LatencyMs":{"type":"number"},"p99LatencyMs":{"type":"number"},"quotaBreaches":{"type":"integer"},"byOperation":{"type":"array","items":{"type":"object","properties":{"operationId":{"type":"string"},"calls":{"type":"integer"},"errorRate":{"type":"number"}}}}}},
"ApprovalExternalDispatch": {"type":"object","x-ticvai-persistence":"approvals.external_dispatch","description":"11.1.65 (29 September, build pass). **One request level sent to an external workflow system**, and what became of it. Written by the platform when a level that names a provider is reached, and closed by `recordExternalApprovalDecision` or by the timeout.\n","required":["id","requestId","providerId","level","status"],"properties":{"id":{"type":"string","format":"uuid"},"requestId":{"type":"string","format":"uuid"},"providerId":{"type":"string","format":"uuid"},"level":{"type":"integer"},"status":{"type":"string","enum":["pending","sent","failed","decided","timedOut","cancelled"]},"attemptCount":{"type":"integer","default":0},"externalReference":{"type":"string","nullable":true,"description":"The provider's own id for the item, as it acknowledged or called back with."},"lastResponseCode":{"type":"integer","nullable":true},"lastError":{"type":"string","nullable":true},"sentAt":{"type":"string","format":"date-time","nullable":true},"answeredAt":{"type":"string","format":"date-time","nullable":true},"externalOutcome":{"type":"string","nullable":true,"description":"The provider's own outcome value, before mapping."},"externalApproverRef":{"type":"string","nullable":true,"description":"Who decided in the provider's system, as it named them."},"scopePath":{"type":"string"}}},
"ApprovalExternalProvider": {"type":"object","x-ticvai-persistence":"approvals.external_provider","description":"11.1.65 (29 September, build pass). **A third-party workflow system registered to decide approval levels**: where TICVAI sends a request, how its fields are mapped, how the answer comes back and what happens when it does not.\n","required":["code","name","endpointUrl","apiClientId","decisionMapping"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"code":{"type":"string","x-ticvai-unique":"tenant","description":"The provider's stable name, and the key `setApprovalExternalProvider` upserts on."},"name":{"type":"string"},"endpointUrl":{"type":"string","description":"`https` only. Where a request level is sent."},"outboundAuth":{"type":"string","enum":["bearerToken","basic","oauthClientCredentials","mutualTls"],"default":"oauthClientCredentials"},"outboundCredential":{"type":"string","format":"password","writeOnly":true,"nullable":true,"description":"The credential TICVAI presents to the provider. Write-only, never returned, kept on a replace that omits it. **Held in Key Vault**; the row's `outbound_credential` column keeps the secret's reference, never the value (CHG-R1S-020)."},"signingSecret":{"type":"string","format":"password","writeOnly":true,"nullable":true,"description":"Signs every request TICVAI sends, as webhook deliveries are signed, so the provider can tell it came from TICVAI. Write-only. **Held in Key Vault**; the `signing_secret` column keeps the secret's reference, never the value (CHG-R1S-020).\n"},"apiClientId":{"type":"string","format":"uuid","description":"The public-api client the provider calls back as. It must hold `APPROVAL_DECIDE`; `recordExternalApprovalDecision` from any other client is refused.\n"},"requestMapping":{"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Stored whole on the provider row (`request_mapping`, jsonb; 3 October 2026, CHG-R1S-020: the r1 gate found no column held it). Which request fields go to the provider, under which names. **Only mapped fields leave TICVAI** — a provider receives the amount and the subject it needs, not the whole request.\n","items":{"type":"object","required":["from","to"],"properties":{"from":{"type":"string","description":"A field of `ApprovalRequest`, e.g. `amount`, `kind`, `subjectId`, `requestedByPrincipalId`."},"to":{"type":"string","description":"The provider's field name."}}}},"decisionMapping":{"type":"array","minItems":2,"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"The provider's outcome values and the decision each means. At least one maps to `approve` and one to `reject`. Stored whole on the provider row (`decision_mapping`, jsonb; CHG-R1S-020).","items":{"type":"object","required":["externalValue","decision"],"properties":{"externalValue":{"type":"string"},"decision":{"type":"string","enum":["approve","reject","return","requestInformation"]}}}},"timeoutMinutes":{"type":"integer","default":1440,"description":"How long a level waits for the provider before `onTimeout` applies."},"onTimeout":{"type":"string","enum":["fallBackToRoles","escalate","reject"],"default":"fallBackToRoles"},"maxAttempts":{"type":"integer","default":5,"description":"Delivery attempts, with backoff, before a dispatch is `failed` and the level falls back as on timeout."},"status":{"type":"string","enum":["active","paused","disabled"],"default":"active","description":"`paused` sends nothing and every level that names it falls back at once; the platform sets `disabled` after repeated failures, as it disables a failing webhook.\n"},"lastSuccessAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true}}},
"AuthorisationPolicy": {"type":"object","x-ticvai-persistence":"identity.authorisation_policy","description":"3.3. **Conditions and an effect, evaluated by one engine.** A role says who you are; a policy says under what circumstances that is enough.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). The package has two: this one, and the access contract's `AccessDynamicPolicy` (`access.dynamic_policy`). **This one governs who may do what in the software**: a principal's permissions on operations and screens (`permissions` names them), narrowed or extended by who, where, when and on what device, and decided by `evaluateAccess`. **`AccessDynamicPolicy` governs who may pass which gate**: a guest's, holder's or employee's admission at an access point, decided in the gate's validation with results such as `requireId` or `requireSupervisor` that mean nothing to a permission check. A staff member's badge opening a staff door is a gate decision (access); the same staff member approving a refund is a permission decision (here).\n**Settled by ADR-0068 (accepted 1 October): guest admission lives in Access only.** This engine keeps staff authorisation and was renamed to say so: `identity.access_policy` became `identity.authorisation_policy`, its versions `identity.authorisation_policy_version`, and its operations `*AuthorisationPolicy*`. \"Access policy\" now means `AccessDynamicPolicy` and nothing else.\n","required":["code","name","effect"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server on `createAuthorisationPolicy`; the path names the policy on update."},"code":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"isTemplate":{"type":"boolean","default":false},"permissions":{"type":"array","items":{"type":"string"},"description":"**Which permissions this policy speaks to.** A policy with an empty list speaks to all of them, which is powerful enough that it is worth being explicit about.\n"},"conditions":{"type":"array","x-ticvai-persistence-column":"jsonb","items":{"$ref":"#/components/schemas/AccessCondition"}},"combining":{"type":"string","enum":["allMustMatch","anyMayMatch"],"default":"allMustMatch"},"effect":{"type":"string","enum":["permit","deny"],"description":"**Deny wins over permit when two policies disagree.** 3.3.32 asks for least-privilege, and a permit that can override a deny is not least-privilege by any reading — it is the union of every mistake anybody has made.\n"},"priority":{"type":"integer","default":0},"scopePath":{"type":"string","description":"3.3.40 to 3.3.43. **Tenant, venue and cross-venue policies are one mechanism**, because `scope_path` is prefix-comparable — `uae.dubai` contains `uae.dubai.marina` — and inheritance is the prefix walk rather than a second table.\n"},"appliesToRoleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"status":{"type":"string","readOnly":true,"description":"**Moved only by `setAuthorisationPolicyState`.** A policy is created as a `draft`, and a status sent in a create or update body is ignored — otherwise a write could skip the approval 3.3.26 requires.\n","enum":["draft","pendingApproval","active","suspended","retired"]},"version":{"type":"integer","default":1,"readOnly":true,"description":"Set by the server; every `updateAuthorisationPolicy` writes a new version."},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true},"delegatedAdminRoleIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"3.3.35. **Who may edit this policy without being a platform administrator.** A venue manager tuning their own opening-hours rule should not need someone who can edit every tenant's.\n"}}},
"CrossModuleOrchestrationMonitorView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_step_execution joined to approvals.workflow_instance by correlation id (data model for the agreed operations, 29 September)","description":"**What Cross-Module Orchestration Monitor displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"service":{"type":"string","description":"Service"},"action":{"type":"string","description":"Action"},"status":{"type":"string","enum":["notStarted","running","waiting","successful","failed","compensated"],"description":"Status"},"started":{"type":"string","format":"date-time","description":"Started"},"completed":{"type":"string","format":"date-time","description":"Completed"},"duration":{"type":"integer","description":"Seconds"},"inputOutput":{"type":"string","description":"Input/Output"},"failureHandling":{"type":"string","enum":["waits","retries","rollsBack","continuesPartially","requiresHumanIntervention"],"description":"What the workflow does after this node fails"},"retries":{"type":"integer","description":"Retries"},"correlationId":{"type":"string","description":"a common correlation/workflow ID"}},"required":["correlationId","service"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"TriggerActionCrossModuleOrchestrationConfigurationInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; writes approvals.workflow_trigger (schema WorkflowTrigger) (data model for the agreed operations, 29 September)","description":"**What Trigger, Action & Cross-Module Orchestration Configuration submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"triggerType":{"type":"string","enum":["event","dataCondition","schedule","manual"],"description":"What starts the workflow"},"workflowId":{"type":"string","description":"Workflow this trigger and action set belongs to"},"allowedActions":{"type":"array","items":{"type":"string","enum":["createApproval","createTask","updateStatus","applyHold","releaseHold","createNotification","generateDocument","executeRefund","updateAllocation","activateMembership","suspendPartner","callApprovedApi","callApprovedService","startSubWorkflow"]},"description":"Actions this workflow may call"},"onFailure":{"type":"string","enum":["retry","rollback","compensate","exceptionQueue","humanIntervention"],"description":"What happens when an action fails"},"triggerDefinition":{"type":"string","description":"Event name, data condition (e.g. Balance > Limit) or schedule"},"maxRetries":{"type":"integer","description":"Retries before the failure handling applies"}},"required":["workflowId","triggerType"]},
"TriggerActionCrossModuleOrchestrationConfigurationView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_trigger (schema WorkflowTrigger) (data model for the agreed operations, 29 September)","description":"**What Trigger, Action & Cross-Module Orchestration Configuration displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"triggerType":{"type":"string","enum":["event","dataCondition","schedule","manual"],"description":"What starts the workflow"},"workflowId":{"type":"string","description":"Workflow this trigger and action set belongs to"},"allowedActions":{"type":"array","items":{"type":"string","enum":["createApproval","createTask","updateStatus","applyHold","releaseHold","createNotification","generateDocument","executeRefund","updateAllocation","activateMembership","suspendPartner","callApprovedApi","callApprovedService","startSubWorkflow"]},"description":"Actions this workflow may call"},"onFailure":{"type":"string","enum":["retry","rollback","compensate","exceptionQueue","humanIntervention"],"description":"What happens when an action fails"},"triggerDefinition":{"type":"string","description":"Event name, data condition (e.g. Balance > Limit) or schedule"},"maxRetries":{"type":"integer","description":"Retries before the failure handling applies"}},"required":["workflowId","triggerType"]},
"WebhookEventCatalogueEntry": {"type":"object","x-ticvai-persistence":"none — read from the event catalogue (events/*.yaml) shipped with the release","description":"One event a webhook may subscribe to, as the event catalogue declares it. What a receiver needs to write a handler: the name, the version in the payload, who publishes it, what it is about and when, and the payload fields.\n","required":["name","version","publisher"],"properties":{"name":{"$ref":"#/components/schemas/WebhookEventType"},"version":{"type":"integer","minimum":1},"publisher":{"type":"string","description":"The one context that publishes it."},"aggregate":{"type":"string","description":"What the event is about. Delivery is ordered within one instance of it."},"description":{"type":"string"},"emittedWhen":{"type":"string","nullable":true},"payload":{"type":"array","items":{"type":"object","required":["field","type"],"properties":{"field":{"type":"string"},"type":{"type":"string"},"required":{"type":"boolean","default":true},"notes":{"type":"string","nullable":true}}}}}},
"WebhookEventType": {"type":"string","description":"**The webhook event catalogue: every event a subscription may name** (29 September, build pass). Each value is the `name` of an event in `events/` — `aggregate.pastTenseFact`, published through `platform.outbox` by exactly one context. A name is added here in the same change that adds its event file, and never before.\n**Added 29 September**, each closing a requirement that had the webhook mechanism and nothing to subscribe to:\n| Events | Publisher | Requirement | |---|---|---| | `device.statusChanged`, `device.tamperDetected`, `device.enrolmentChanged`, `device.firmwareReleased`, `device.firmwareRolloutCompleted` | tenancy | 16.9.56 | | `accreditation.applicationDecided`, `accreditation.holderStatusChanged`, `accreditation.credentialIssued`, `accreditation.renewalDue` | accreditation | 12.1.53 | | `approval.requested`, `approval.escalated`, `approval.stepCompleted`, `approval.expired` | approvals | 11.1.64, 11.1.66 | | `seat.held`, `seat.released`, `seat.blocked`, `seatMap.published` | seating | 21.13.4 | | `consent.deviceConsentRecorded`, `consent.deviceConsentClaimed` | marketing | 2.6.65 | | `order.chargebackRecorded` | orders | 8.3.11 to 8.3.15 (a tenant's own finance or fraud tooling) | | `entitlement.expiringSoon` | access | 5.5.30 (a tenant's own CRM) | | `apiClient.anomalyDetected` | public-api | 17 September minutes M17-07 (added 30 September with its event file) |\n**Deprecated** (1 October, ADR-0067 amendment): `device.enrolmentChanged` is still offered but nothing inside the platform consumes it any more; it is removed at the next major version of this API. Subscribers are told in the release note.\n**Published and deliberately not offered** (29 September, build pass, group G2): `identity.credentialResetRequested` and `identity.loginRecorded` are security signals, and a stream of them to an outside receiver is a map of which accounts are under attack; `storefront.sessionEvent` is high-volume fraud telemetry, not a business fact a receiver acts on.\n","x-ticvai-deprecated-values":["device.enrolmentChanged"],"enum":["access.validated","accreditation.applicationDecided","accreditation.credentialIssued","accreditation.holderStatusChanged","accreditation.renewalDue","ai.ceilingApproaching","apiClient.anomalyDetected","approval.escalated","approval.expired","approval.granted","approval.rejected","approval.requested","approval.stepCompleted","assets.documentIndexed","cart.abandoned","catalogue.productPublished","consent.deviceConsentClaimed","consent.deviceConsentRecorded","conversation.handedOver","device.enrolmentChanged","device.firmwareReleased","device.firmwareRolloutCompleted","device.statusChanged","device.tamperDetected","entitlement.expiringSoon","entitlement.issued","entitlement.statusChanged","fnb.menuPublished","fnb.orderReady","inventory.purchaseOrderReceived","ledger.journalPosted","ledger.periodClosed","maintenance.assetReturnedToService","maintenance.templatePublished","maintenance.workOrderCompleted","marketing.caseClosed","order.chargebackRecorded","order.completed","order.paid","order.refunded","performance.cancelled","reporting.definitionPublished","retail.merchandisePublished","seat.blocked","seat.held","seat.released","seat.sold","seatMap.published","shift.closed","stock.depleted","tenant.suspended","whitelabel.contentPublished"]},
"WorkflowAnalyticsProcessPerformanceView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — aggregated from approvals.workflow_instance, workflow_step_execution, automation_execution, request, decision and escalation (data model for the agreed operations, 29 September)","description":"**What Workflow Analytics & Process Performance displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"workflowVolume":{"type":"integer","description":"Workflow Volume"},"completionRate":{"type":"number","description":"Completion Rate"},"failureRate":{"type":"number","description":"Failure Rate"},"averageCompletionTime":{"type":"integer","description":"Minutes"},"approvalTime":{"type":"integer","description":"Minutes"},"automationRate":{"type":"number","description":"Automation Rate"},"escalationRate":{"type":"number","description":"Escalation Rate"},"rejectionRate":{"type":"number","description":"Rejection Rate"},"reworkRate":{"type":"number","description":"Rework Rate"},"slaCompliance":{"type":"number","description":"Percent within SLA"},"averageApprovalTime":{"type":"integer","description":"Minutes"},"approvalRate":{"type":"number","description":"Approval Rate"},"requestChangesRate":{"type":"number","description":"Request Changes Rate"},"delegationRate":{"type":"number","description":"Delegation Rate"},"manualStepsRemoved":{"type":"integer","description":"Manual Steps Removed"},"processingTimeSaved":{"type":"integer","description":"Minutes"},"workloadReduced":{"type":"number","description":"Staff hours"},"costSavingWhereMeasurable":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cost Saving where measurable"}}},
"WorkflowExceptionFailureRecoveryCenterView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over approvals.workflow_exception (schema WorkflowException) (data model for the agreed operations, 29 September)","description":"**What Workflow Exception, Failure & Recovery Center displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"errorType":{"type":"string","enum":["businessRuleFailure","missingData","missingApprover","permissionFailure","integrationFailure","timeout","actionFailure","invalidState","duplicateEvent","serviceUnavailable","configurationError"],"description":"Kind of failure"},"exceptionId":{"type":"string","description":"Exception ID"},"workflow":{"type":"string","description":"Workflow"},"instance":{"type":"string","description":"Instance"},"module":{"type":"string","description":"Module"},"failedStep":{"type":"string","description":"Step that failed"},"time":{"type":"string","format":"date-time","description":"Time"},"businessImpact":{"type":"string","description":"Business Impact"},"priority":{"type":"string","description":"Priority"},"owner":{"type":"string","description":"Owner"},"retryCount":{"type":"integer","description":"Retry count"}},"required":["exceptionId"]}
}
```
