# P09-infrastructure-resilienc-01 — P09 · Infrastructure & Resilience

**4 screens · 8 operations · 10 schemas · 2 permissions**

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

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW`. A control nobody can use must say so,
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
| `ADM-014` | Auto-Scaling Configuration | B | 0 | 43 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-030` | Infrastructure Sizing & Scaling Policy | B | 8 | 13 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-033` | Backup & DR Status | B | 0 | 22 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `ADM-034` | Archival Job Monitor | B | 0 | 7 | 6 | 0 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-030, ADM-033, ADM-034 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-014` Auto-Scaling Configuration

**See how each cell scales: its floors, ceilings and target utilisation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Infrastructure & Resilience · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-014 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW` (1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellCapacity` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/auto-scaling-configuration` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): The cell operations were copied onto the scaling screen; decommission stays on ADM-003 only and tier changes on ADM-003 and ADM-030 (design-notes corrections … Removed 2 October 2026 (CHG-WIR-021): The cell operations were copied onto the scaling screen; decommission stays on ADM-003 only and tier changes on ADM-003 and ADM-030 (design-notes corrections … Removed 2 October 2026 (CHG-WIR-021): The cell operations were copied onto the scaling screen; decommission stays on ADM-003 only and tier changes on ADM-003 and ADM-030 (design-notes corrections … Open: No contract — infrastructure, Terraform not API

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Auto-scaling settings per cell and where each value came from.

**Fixed on main** (the package already carries these; draw what it says): No scaling operation; the cell operations are copied. (CHG-WIR-023); Tables show every schema field, plumbing included: 'Every cell job' drop id. (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Window | radio group | Day | Hour · Day · Week · Month | `getCellCapacity` ?window |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every cell job** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Provision, Tier migration, Schema migration, Backup, Restore, Decommission | — |
| Status | chip: Queued, Running, Completed, Failed, Rolled back | — |
| Progress percent | 1,234 | — |
| Message | text | — |
| Error | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**The selected cell job** (detail panel, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Provision, Tier migration, Schema migration, Backup, Restore, Decommission | — |
| Status | chip: Queued, Running, Completed, Failed, Rolled back | — |
| Progress percent | 1,234 | — |
| Message | text | — |
| Error | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |
| Tier | chip: Shared, Dedicated, Isolated, Client hosted | — |
| Status | chip: Provisioning, Active, Migrating, Suspended, Decommissioning, Failed | — |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | yes / no (icon or chip) | — |
| Is schema behind | yes / no (icon or chip) | — |
| Database status | text | — |
| Replication lag seconds | 1,234.5 | — |
| Last backup at | 1 Oct 2026, 14:30 | — |
| Last restore drill at | 1 Oct 2026, 14:30 | — |
| Checked at | 1 Oct 2026, 14:30 | — |

**The scaling policy** (detail panel, from `getScalingPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Service | text | — |
| Replica floor | 1,234 | — |
| Replica ceiling | 1,234 | Null means no maximum, which is the correct setting for a burst cell. |
| Target utilisation pct | 1,234 | — |
| Scale step pct | 1,234 | — |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Tenant count | 1,234 | Reported, and deliberately not the sizing signal. Forty quiet tenants may load a cell less than three busy ones. |
| Is constrained | yes / no (icon or chip) | — |
| Constrained dimension | text | — |
| Dimensions | list or chips (count when long) | Per dimension, because the response differs. Short of connections and long on storage is a different problem from short of both. |
| Forecast breach at | 1 Oct 2026, 14:30 | When the constrained dimension is projected to run out at the current trend. Null where there is no trend to project — an honest null beats … |
| Measured at | 1 Oct 2026, 14:30 | — |

**Data it reads**: `getCellCapacity` (onLoad, Load against headroom); `getCell` (onLoad, Read a cell); `getCellHealth` (onLoad, Cell health and schema version); `listCellJobs` (onLoad, Provisioning, migration and maintenance jobs); `getScalingPolicy` (onLoad, Floors, ceilings and target utilisation)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The auto-scaling list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the auto-scaling untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No auto-scaling yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellCapacity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for Cancel decommission, Decommission cell, Save cell tier. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **cancelDecommission answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **decommissionCell answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#decommissionCell)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell job:
- kind: standard
  status: active
  progressPercent: 12.5
  scheduledFor: 31/12/2026 23:59
  completedAt: 01/10/2026 09:14
- kind: standard
  status: pending
  progressPercent: 8.0
  scheduledFor: 15/10/2026 00:00
  completedAt: 30/09/2026 18:02
- kind: override
  status: suspended
  progressPercent: 15.0
  scheduledFor: 01/11/2026 06:00
  completedAt: 28/09/2026 11:45
```

#### Permissions

- `getCellCapacity` → `PLATFORM_CELL_VIEW` (read) · staff
- `getCell` → `PLATFORM_CELL_VIEW` (read) · staff
- `getCellHealth` → `PLATFORM_CELL_VIEW` (read) · staff
- `listCellJobs` → `PLATFORM_CELL_VIEW` (read) · staff
- `getScalingPolicy` → `PLATFORM_CELL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellCapacity` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Infrastructure & Resilience, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-014` · status **notStarted** · provenance generated
- Flow F97 *A cell is capacity-checked and a tenant is placed on it*, step 3: Auto-Scaling Configuration. → 7 operations, 7 of them previously unwalked.
- ADR-0035 *A flash sale gets its own environment, and it cannot be deleted until it has been reconciled* (`docs/adr/0035-burst-environments.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (43 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-030` Infrastructure Sizing & Scaling Policy

**Set each cell's size and the policy it scales on.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Infrastructure & Resilience · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-030 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW` (1 configure, 1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellCapacity` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/infrastructure-sizing-and-scaling-policy` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Copied cell operations; decommission stays on ADM-003 only. The tier change stays here as sizing, beside the scaling policy (getScalingPolicy/setScalingPolicy) … Removed 2 October 2026 (CHG-WIR-021): Copied cell operations; decommission stays on ADM-003 only. The tier change stays here as sizing, beside the scaling policy (getScalingPolicy/setScalingPolicy) … Copied cell operations are not part of this screen (design-note correction platform-foundation ADM-030, CHG-SBO-015). Open: No contract — Terraform

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Sizing and scaling policy for cells.

**Fixed on main** (the package already carries these; draw what it says): Copied cell operations; "Save scaling policy" has no operation. (CHG-SBO-015); formSetScalingPolicy asks the person for id. (CHG-SBO-004); Tables show every schema field, plumbing included: 'Every cell job' drop id. (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003).

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Window | radio group | Day | Hour · Day · Week · Month | `getCellCapacity` ?window |

**Form: Save scaling policy** (modal, opened by *Save scaling policy*; *Save scaling policy* calls `setScalingPolicy`, *Cancel* sends nothing)

**Collects what `setScalingPolicy` sends before it is called.** Nothing in the body is required. Optional: `service`, `replicaFloor`, `replicaCeiling`, `targetUtilisationPct`, `scaleStepPct`. **Not asked:** `id` is a client UUIDv7 generated silently (design-note correction, 2 October 2026). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `setScalingPolicy` body |
| Cell `cellId` | picker: choose a cell | optional | — | — | shows names, sends the id | — | `setScalingPolicy` body |
| Service `service` | text field | optional | — | — | — | — | `setScalingPolicy` body |
| Replica floor `replicaFloor` | number field | optional | — | — | — | — | `setScalingPolicy` body |
| Replica ceiling `replicaCeiling` | number field | optional | — | — | — | Null means no maximum, which is the correct setting for a burst cell. | `setScalingPolicy` body |
| Target utilisation pct `targetUtilisationPct` | number field (%) | optional | — | — | — | — | `setScalingPolicy` body |
| Scale step pct `scaleStepPct` | number field (%) | optional | — | — | — | — | `setScalingPolicy` body |
| Updated at `updatedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `setScalingPolicy` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setScalingPolicy: set per region (money, tax, ledger); venues inherit and cannot override. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/satellite/platform-ops.yaml#setScalingPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**The scaling policy** (detail panel, from `getScalingPolicy`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Service | text | — |
| Replica floor | 1,234 | — |
| Replica ceiling | 1,234 | Null means no maximum, which is the correct setting for a burst cell. |
| Target utilisation pct | 1,234 | — |
| Scale step pct | 1,234 | — |

**The cell capacity** (detail panel, from `getCellCapacity`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Tenant count | 1,234 | Reported, and deliberately not the sizing signal. Forty quiet tenants may load a cell less than three busy ones. |
| Is constrained | yes / no (icon or chip) | — |
| Constrained dimension | text | — |
| Dimensions | list or chips (count when long) | Per dimension, because the response differs. Short of connections and long on storage is a different problem from short of both. |
| Forecast breach at | 1 Oct 2026, 14:30 | When the constrained dimension is projected to run out at the current trend. Null where there is no trend to project — an honest null beats … |
| Measured at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save scaling policy (secondary button) | `setScalingPolicy` PUT `/scaling-policies` | ScalingPolicy | ScalingPolicy | — | opens modal first |

**Data it reads**: `getCellCapacity` (onLoad, Load against headroom); `getScalingPolicy` (onLoad, The policy as it stands)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The infrastructure sizing scaling list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the infrastructure sizing scaling untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No infrastructure sizing scaling yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellCapacity` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_CELL_MANAGE` for `setScalingPolicy`. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for Cancel decommission, Decommission cell, Save cell tier. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **cancelDecommission answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **decommissionCell answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#decommissionCell)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell job:
- kind: standard
  status: active
  progressPercent: 12.5
  scheduledFor: 31/12/2026 23:59
  completedAt: 01/10/2026 09:14
- kind: standard
  status: pending
  progressPercent: 8.0
  scheduledFor: 15/10/2026 00:00
  completedAt: 30/09/2026 18:02
- kind: override
  status: suspended
  progressPercent: 15.0
  scheduledFor: 01/11/2026 06:00
  completedAt: 28/09/2026 11:45
```

#### Permissions

- `getCellCapacity` → `PLATFORM_CELL_VIEW` (read) · staff
- `getScalingPolicy` → `PLATFORM_CELL_VIEW` (read) · staff
- `setScalingPolicy` → `PLATFORM_CELL_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellCapacity` requires to show this screen, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. A caller who can see the screen but lacks what an action needs sees that action disabled, naming its permission: `PLATFORM_CELL_MANAGE` for `setScalingPolicy`.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Infrastructure & Resilience, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-030` · status **notStarted** · provenance generated
- ADR-0035 *A flash sale gets its own environment, and it cannot be deleted until it has been reconciled* (`docs/adr/0035-burst-environments.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-030?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save scaling policy.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_MANAGE`, `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-033` Backup & DR Status

**See each cell's backups and how old the newest one is.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Infrastructure & Resilience · wave 2 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-033 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW` (1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/backup-and-dr-status` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Copied cell actions (decommission, tier) are not part of backup status; decommission stays on ADM-003 only (design-notes corrections platform-foundation ADM-033 … Removed 2 October 2026 (CHG-WIR-021): Copied cell actions (decommission, tier) are not part of backup status; decommission stays on ADM-003 only (design-notes corrections platform-foundation ADM-033 … Removed 2 October 2026 (CHG-WIR-021): Copied cell actions (decommission, tier) are not part of backup status; decommission stays on ADM-003 only (design-notes corrections platform-foundation ADM-033 …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Backup runs and restore drills per cell, with failures and last tested restore.

**Fixed on main** (the package already carries these; draw what it says): Copied cell actions (decommission, tier). (CHG-SBO-015); Tables show every schema field, plumbing included: 'Every cell job' drop id; 'Every backup run' drop id. (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every backup run** (data table, from `listBackupRuns`)

| Shows | Format | Notes |
|---|---|---|
| Scope | chip: Cell, Tenant | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| State | chip: Running, Succeeded, Failed | — |
| Size bytes | 1,234 | — |
| Restore tested at | 1 Oct 2026, 14:30 | A backup nobody has restored is a hypothesis. |
| Error | text | — |

**The cell** (detail panel, from `getCell`)

| Shows | Format | Notes |
|---|---|---|
| Name | text | — |
| Kind | chip: Shared, Dedicated, On premise isolated, On premise connected, Control plane, Burst | Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law … |
| Last contact at | 1 Oct 2026, 14:30 | When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first. |
| Licence expires at | 1 Oct 2026, 14:30 | On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. |
| Region name | text | — |
| Country code | text | — |
| Tier | chip: Shared, Dedicated, Isolated, Client hosted | — |
| Status | chip: Provisioning, Active, Migrating, Suspended, Decommissioning, Failed | — |

**The cell health** (detail panel, from `getCellHealth`)

| Shows | Format | Notes |
|---|---|---|
| Is healthy | yes / no (icon or chip) | — |
| Is schema behind | yes / no (icon or chip) | — |
| Database status | text | — |
| Replication lag seconds | 1,234.5 | — |
| Last backup at | 1 Oct 2026, 14:30 | — |
| Last restore drill at | 1 Oct 2026, 14:30 | — |
| Checked at | 1 Oct 2026, 14:30 | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Backups**: Last successful backup and last restore test per cell; older than the target shown amber. *(source: ADR-0060)*

**Data it reads**: `getCellHealth` (onLoad, from page inventory); `getCell` (onLoad, Read a cell); `listBackupRuns` (onLoad, Backups taken and how old the newest is)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The backup status list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the backup status untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No backup status yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for Cancel decommission, Decommission cell, Save cell tier. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **cancelDecommission answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **decommissionCell answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#decommissionCell)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell job:
- kind: standard
  status: active
  progressPercent: 12.5
  scheduledFor: 31/12/2026 23:59
  completedAt: 01/10/2026 09:14
- kind: standard
  status: pending
  progressPercent: 8.0
  scheduledFor: 15/10/2026 00:00
  completedAt: 30/09/2026 18:02
- kind: override
  status: suspended
  progressPercent: 15.0
  scheduledFor: 01/11/2026 06:00
  completedAt: 28/09/2026 11:45
```

#### Permissions

- `getCellHealth` → `PLATFORM_CELL_VIEW` (read) · staff
- `getCell` → `PLATFORM_CELL_VIEW` (read) · staff
- `listBackupRuns` → `PLATFORM_CELL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Infrastructure & Resilience, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-033` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-033?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-034` Archival Job Monitor

**Watch the archival and retention jobs across the cells.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Infrastructure & Resilience · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-034 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW` (1 read) |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listCellJobs` reads the population and `getCell` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `cellId` (deepLink) · cold entry: **A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the … |
| Route | `/general/archival-job-monitor` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): Copied cell actions are not part of archival; decommission stays on ADM-003 only (ADR-0047; design-notes corrections platform-foundation ADM-034, ADM-013). Removed 2 October 2026 (CHG-WIR-021): Copied cell actions are not part of archival; decommission stays on ADM-003 only (ADR-0047; design-notes corrections platform-foundation ADM-034, ADM-013). Removed 2 October 2026 (CHG-WIR-021): Copied cell actions are not part of archival; decommission stays on ADM-003 only (ADR-0047; design-notes corrections platform-foundation ADM-034, ADM-013). Open: No contract — retention not specified

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Archival jobs per cell: rows archived and purged under each retention policy.

**Fixed on main** (the package already carries these; draw what it says): Copied cell actions. (CHG-SBO-015); Tables show every schema field, plumbing included: 'Every cell job' drop id; 'Every archival job' drop id. (CHG-SBO-004); requiresModule is 'membership' on a TICVAI Console screen. (CHG-SBO-003); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every archival job** (data table, from `listArchivalJobs`)

| Shows | Format | Notes |
|---|---|---|
| Policy name | text | — |
| Target table | text | — |
| Rows archived | 1,234 | — |
| Rows purged | 1,234 | — |
| State | chip: Scheduled, Running, Succeeded, Failed | — |
| Run at | 1 Oct 2026, 14:30 | — |
| Error | text | — |

**Data it reads**: `listArchivalJobs` (onLoad, Archival and retention jobs)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-003` Cross-Tenant Health Dashboard: *Cross-Tenant Health Dashboard*; carries `cellId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The archival job list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the archival job untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No archival job yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listCellJobs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Edge cases to draw

- **Can read but not change (holds PLATFORM_CELL_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_CELL_MANAGE for Cancel decommission, Decommission cell, Save cell tier. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **cancelDecommission answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#cancelDecommission)*
- **decommissionCell answers 409**: Show it as something the person can act on, not a failure: Not in a state that permits this *(source: contracts/satellite/subscription.yaml#decommissionCell)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every cell job:
- kind: standard
  status: active
  progressPercent: 12.5
  scheduledFor: 31/12/2026 23:59
  completedAt: 01/10/2026 09:14
- kind: standard
  status: pending
  progressPercent: 8.0
  scheduledFor: 15/10/2026 00:00
  completedAt: 30/09/2026 18:02
- kind: override
  status: suspended
  progressPercent: 15.0
  scheduledFor: 01/11/2026 06:00
  completedAt: 28/09/2026 11:45
```

#### Permissions

- `listArchivalJobs` → `PLATFORM_CELL_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listCellJobs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 1 for P09 · Infrastructure & Resilience, 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-034` · status **notStarted** · provenance generated
- ADR-0047 *How long data is kept, and where it goes next* (`docs/adr/0047-how-long-data-is-kept-and-where-it-goes-next.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-034?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`, `ADM-003`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
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

### In P09 · Infrastructure & Resilience

- **Open question.** Open (Chinmay): should server/infrastructure monitoring and management be a dedicated module inside the TICVAI platform, or stay in Softlabs' own tooling (e.g. Terraform) outside the product? Input from Tejesh pending. *(open · MoM 10 Sep 2026, 4.18 Other Discussion · DI-841)*

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"getCell": {"method":"GET","path":"/cells/{cellId}","contract":"subscription","summary":"Read a cell","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"CellDetail"},
"getCellCapacity": {"method":"GET","path":"/cells/{cellId}/capacity","contract":"subscription","summary":"Load against headroom","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"window","in":"query","required":null}],"requestBody":null,"responds":"CellCapacity"},
"getCellHealth": {"method":"GET","path":"/cells/{cellId}/health","contract":"subscription","summary":"Cell health and schema version","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"CellHealth"},
"getScalingPolicy": {"method":"GET","path":"/scaling-policies","contract":"platform-ops","summary":"The floors, ceilings and target utilisation a cell scales on","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"ScalingPolicy"},
"listArchivalJobs": {"method":"GET","path":"/archival-jobs","contract":"platform-ops","summary":"Archival and retention jobs","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"ArchivalJob"},
"listBackupRuns": {"method":"GET","path":"/backup-runs","contract":"platform-ops","summary":"Backups taken and what they cover","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"BackupRun"},
"listCellJobs": {"method":"GET","path":"/cells/{cellId}/jobs","contract":"subscription","summary":"Provisioning, migration and maintenance jobs","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setScalingPolicy": {"method":"PUT","path":"/scaling-policies","contract":"platform-ops","summary":"Change the scaling policy","permission":"PLATFORM_CELL_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ScalingPolicy","responds":"ScalingPolicy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ArchivalJob": {"type":"object","x-ticvai-persistence":"control.archival_job","description":"**Drafted 4 September.** One archival or retention run. Retention is a legal obligation, so a stalled job is a compliance failure rather than a housekeeping one.","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"policyName":{"type":"string"},"targetTable":{"type":"string"},"rowsArchived":{"type":"integer"},"rowsPurged":{"type":"integer"},"state":{"type":"string","enum":["scheduled","running","succeeded","failed"]},"runAt":{"type":"string","format":"date-time"},"error":{"type":"string"}}},
"BackupRun": {"type":"object","x-ticvai-persistence":"control.backup_run","description":"**Drafted 4 September.** One backup run. The question this answers is not *did it run* but *how old is the newest restorable copy* - a job that succeeds nightly against an empty database succeeds forever.","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"scope":{"type":"string","enum":["cell","tenant"]},"startedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time"},"state":{"type":"string","enum":["running","succeeded","failed"]},"sizeBytes":{"type":"integer"},"restoreTestedAt":{"type":"string","format":"date-time","description":"**A backup nobody has restored is a hypothesis.**"},"error":{"type":"string"}}},
"Cell": {"x-ticvai-persistence":"control.cell","x-ticvai-retired-columns":["tenant_id"],"type":"object","required":["id","name","regionId","countryCode","tier","status"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"$ref":"#/components/schemas/CellKind"},"clusterId":{"type":"string","format":"uuid","nullable":true},"isReachable":{"type":"boolean","default":true,"description":"False for `onPremiseIsolated`, true for `onPremiseConnected` (ADR-0046). When false, the Control Plane holds the record for licensing and support and **cannot reach the installation** — it may sit behind a firewall with no inbound route. Every operation assuming reachability must handle absence rather than timing out, and a cell that has not called home for a month is not necessarily broken.\n"},"lastContactAt":{"type":"string","format":"date-time","nullable":true,"description":"When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first.\n"},"licenceExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. **An expired licence degrades rather than stops** — a venue whose gates refuse entry because a licence lapsed over a weekend is worse than one running unlicensed until Monday.\n"},"participatesInCrossCell":{"type":"boolean","default":true,"description":"False by default for `onPremiseIsolated`, available for `onPremiseConnected` (ADR-0046). Redeeming a pass issued elsewhere requires reaching the issuing cell at that moment, and an on-premise site may not be able to. Exclusion is the honest default; local-then-reconcile carries a double-redemption risk that needs a decision rather than an assumption.\n"},"regionId":{"type":"string","format":"uuid"},"regionName":{"type":"string"},"countryCode":{"type":"string"},"tier":{"$ref":"#/components/schemas/CellTier"},"status":{"$ref":"#/components/schemas/CellStatus"},"cloudProvider":{"type":"string","nullable":true},"cloudRegion":{"type":"string","nullable":true},"apiEndpoint":{"type":"string","nullable":true},"venueCount":{"type":"integer"},"provisionedAt":{"type":"string","format":"date-time","nullable":true},"deploymentRef":{"type":"string","nullable":true,"description":"**A pointer to where this cell runs, not a description of it.** A Kubernetes namespace, an ECS cluster ARN, a stack name — whatever the orchestrator calls the thing.\n\n**The platform does not model instances, nodes or shards** (31 August). Kubernetes already holds instance counts and they change by the second; a table copying them drifts within minutes and the copy would win.\n\n**The line is: routing decisions belong to the platform, provisioning facts belong to the orchestrator.** Qdrant is the proof — ADR-0021 makes the tenant *the* shard key, so nine operations route without a lookup and **a stored shard assignment would be a second copy of something derivable.**\n\n**CF-161 needed a table after all, and this said it did not.** The claim here was that one database per cell or one per service is a build-time decision and the DDL is identical either way. **ADR-0038 answered it per tenant**, which drops `Cell.tenantId`, adds `CellTenant`, `RolloutTenant` and a per-tenant migration row, and takes `control` out of the tenant template. `tools/derive-ddl.py` carried the same claim in its docstring.\n\n**A claim that a question cannot affect your artefact is the one most likely to be left standing after it does**, which is why the correction is recorded here rather than the sentence simply deleted."}}},
"CellCapacity": {"type":"object","x-ticvai-persistence":"none — measured, not stored","required":["cellId","isConstrained","dimensions","measuredAt"],"properties":{"cellId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/CellKind"},"tenantCount":{"type":"integer","description":"Reported, and **deliberately not the sizing signal.** Forty quiet tenants may load a cell less than three busy ones.\n"},"isConstrained":{"type":"boolean"},"constrainedDimension":{"type":"string","nullable":true},"dimensions":{"type":"array","description":"Per dimension, because the response differs. Short of connections and long on storage is a different problem from short of both.\n","items":{"type":"object","required":["dimension","used","headroom"],"properties":{"dimension":{"type":"string","enum":["concurrentUsers","transactionsPerSecond","scansPerSecond","databaseConnections","storageGb","replicationLag","cpu"]},"used":{"type":"number"},"limit":{"type":"number"},"headroom":{"type":"number","description":"Fraction remaining. Negative means already over."},"peakAt":{"type":"string","format":"date-time","nullable":true}}}},"forecastBreachAt":{"type":"string","format":"date-time","nullable":true,"description":"When the constrained dimension is projected to run out at the current trend. Null where there is no trend to project — an honest null beats an invented date.\n"},"measuredAt":{"type":"string","format":"date-time"}}},
"CellDetail": {"x-ticvai-persistence":"control.cell","allOf":[{"$ref":"#/components/schemas/Cell"},{"type":"object","properties":{"health":{"$ref":"#/components/schemas/CellHealth"},"activeJobs":{"type":"array","items":{"$ref":"#/components/schemas/CellJob"}}}}]},
"CellHealth": {"x-ticvai-persistence":"none — polled, not stored","type":"object","required":["cellId","isHealthy","schemaVersion","checkedAt"],"properties":{"cellId":{"type":"string","format":"uuid"},"isHealthy":{"type":"boolean"},"schemaVersion":{"type":"string","description":"From the cell's version register. Skew across a tenant's cells is expected during rollout; unexplained skew is a defect.\n"},"isSchemaBehind":{"type":"boolean"},"databaseStatus":{"type":"string"},"replicationLagSeconds":{"type":"number","nullable":true},"lastBackupAt":{"type":"string","format":"date-time","nullable":true},"lastRestoreDrillAt":{"type":"string","format":"date-time","nullable":true},"checkedAt":{"type":"string","format":"date-time"}}},
"CellJob": {"x-ticvai-persistence":"control.cell_job","type":"object","required":["id","cellId","kind","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["provision","tierMigration","schemaMigration","backup","restore","decommission"]},"status":{"type":"string","enum":["queued","running","completed","failed","rolledBack"]},"progressPercent":{"type":"integer","minimum":0,"maximum":100},"message":{"type":"string","nullable":true},"error":{"type":"string","nullable":true},"scheduledFor":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"CellKind": {"type":"string","description":"Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law requires it.\n\n**On-premise is two configurations, not one (ADR-0046).** `onPremiseIsolated` keeps no channel to TICVAI — updates are pull-initiated or physically delivered, licensing is a signed file, support is blind. `onPremiseConnected` keeps an outbound control channel and is reachable, updatable and licensable in the ordinary way. The channel carries control traffic only and no natural person (ADR-0043); **AI inference is data, not control**, so connectivity alone does not grant the assistant.\n\nThere is no `hybrid`. The RFP's third model is answered by `onPremiseConnected`; a genuine split workload has never been asked for and would be a new decision.\n\n\n**`burst` added 31 August.** An environment stood up for one on-sale and torn down after (CF-162 scenario c). **It is not a jurisdiction and it is not permanent** — it holds a catalogue snapshot, three services of sixteen, and 17 tables of 380.\n\n**The other four are places data lives. This one is a place data passes through**, which is why it has its own lifecycle and a reconciliation obligation the others do not.","enum":["shared","dedicated","onPremiseIsolated","onPremiseConnected","controlPlane","burst"]},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ScalingPolicy": {"type":"object","x-ticvai-persistence":"control.scaling_policy","description":"**Drafted 4 September.** What a cell scales on. **A floor and a ceiling are not symmetric** - the floor is the size the environment is stood up at before traffic arrives, and the ceiling is a cap on absorbing a peak nobody predicted (ADR-0035).","required":["id"],"properties":{"id":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"service":{"type":"string"},"replicaFloor":{"type":"integer"},"replicaCeiling":{"type":"integer","description":"Null means no maximum, which is the correct setting for a burst cell."},"targetUtilisationPct":{"type":"integer"},"scaleStepPct":{"type":"integer"},"updatedAt":{"type":"string","format":"date-time"}}}
}
```
