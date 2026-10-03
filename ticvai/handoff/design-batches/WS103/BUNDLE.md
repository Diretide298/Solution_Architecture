# WS103 — Subscription Licensing AI Self Service board 6

**9 screens · 20 operations · 28 schemas · 11 permissions**

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

- **Every control that can be refused must be gated.** 11 permissions apply here:
  `PLATFORM_CELL_VIEW, PLATFORM_PLAN_MANAGE, PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_MANAGE, PLATFORM_TENANT_VIEW, REGION_CONFIGURE, SCOPE_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_VIEW, USER_MANAGE`. A control nobody can use must say so,
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
| `ADM-419` | Provisioning Command Center | B | 0 | 12 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-420` | Tenant & Organization Provisioning | B | 12 | 6 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-421` | Venue & Operational Structure Creation | B | 18 | 7 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-422` | Administrator & Security Initialization | B | 27 | 6 | 7 | 15 | 0 | 0 | — | notStarted (—) |
| `ADM-423` | License & Entitlement Activation | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `ADM-424` | Module Activation & Dependency Validation | A | 9 | 57 | 7 | 10 | 1 | 0 | configures | notStarted (—) |
| `ADM-425` | Venue Template Application | B | 6 | 13 | 7 | 1 | 0 | 0 | — | notStarted (—) |
| `ADM-426` | Initial Configuration & Regional Defaults | B | 114 | 66 | 7 | 18 | 1 | 0 | — | notStarted (—) |
| `ADM-427` | Provisioning Validation & Exception Management | B | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**ADM-419, ADM-423, ADM-427 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-419` Provisioning Command Center

**Show the overall status of the customer's environment creation.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-419 |
| Who uses it | ticvai staff holding `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_MANAGE` (1 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `cellId` (navigation) |
| Route | `/tenants-licensing/provisioning-command-center-adm-419` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The state of a customer's environment creation: tenant, cell, organisation, venues, administrator, licences, each step done, running or failed, with retry.

**Fixed on main** (the package already carries these; draw what it says): Only createTenant; nothing reads provisioning progress. (CHG-WIR-021).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Provisioning progress** (data table, from `listCellJobs`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Cell | the name it points at, never the id | — |
| Kind | chip: Provision, Tier migration, Schema migration, Backup, Restore, Decommission | — |
| Status | chip: Queued, Running, Completed, Failed, Rolled back | — |
| Progress percent | 1,234 | — |
| Message | text | — |
| Error | text | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Completed at | 1 Oct 2026, 14:30 | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create tenant (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCellJobs` (onLoad, Provisioning jobs and how far each has got)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to Platform Dashboard*
- → `ADM-420` Tenant & Organization Provisioning: *Tenant & Organization Provisioning*; carries `tenantId`
- → `ADM-421` Venue & Operational Structure Creation: *Venue & Operational Structure Creation*; carries `tenantId`
- → `ADM-422` Administrator & Security Initialization: *Administrator & Security Initialization*
- → `ADM-423` License & Entitlement Activation: *License & Entitlement Activation*
- → `ADM-424` Module Activation & Dependency Validation: *Module Activation & Dependency Validation*; carries `tenantId`
- → `ADM-425` Venue Template Application: *Venue Template Application*; carries `tenantId`
- → `ADM-426` Initial Configuration & Regional Defaults: *Initial Configuration & Regional Defaults*; carries `regionId`, `tenantId`
- → `ADM-427` Provisioning Validation & Exception Management: *Provisioning Validation & Exception Management*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The provisioning list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the provisioning untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No provisioning yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the provisioning are still there. The pack's own statuses are Pending — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Code already in use |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
steps:
  tenant: done
  cell: running 60%
  organisation: pending
  venues: pending
  administrator: pending
```

#### Permissions

- `createTenant` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `listCellJobs` → `PLATFORM_CELL_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After contract, TICVAI provisions the tenant with a basic setup reflecting the tier and licensed modules (e.g. mobile app, B2C, B2B enabled as contracted) before handover; AI can assist initial product/event/ticket setup following the same process as manual setup. *(client request · MoM 10 Sep 2026, 4.12 Tenant Provisioning & Go-Live Setup · DI-833)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-419` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-419`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 6
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 1: Opens Provisioning Command Center → Show the overall status of the customer's environment creation.
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F212 branch at step 1 (expected): when Nothing has been set up on Provisioning Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F212 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-419?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create tenant, Cancel.
- [ ] Every transition is wired: `ADM-002`, `ADM-420`, `ADM-421`, `ADM-422`, `ADM-423`, `ADM-424`, `ADM-425`, `ADM-426`, `ADM-427`.
- [ ] Every gated control is gated: `PLATFORM_CELL_VIEW`, `PLATFORM_TENANT_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-420` Tenant & Organization Provisioning

**Create the customer's isolated TICVAI environment and primary organization structure.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-420 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`, `SCOPE_MANAGE` (1 operate, 2 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/tenants-licensing/tenant-organization-provisioning-adm-420` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `createOrgUnit` (SCOPE_MANAGE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Onboarding: create the customer's tenant and its top organisation units (brand, region). Region choice decides currency and cell placement.

**Fixed on main** (the package already carries these; draw what it says): Only createOrgUnit; the tenant itself is created by createTenant. (CHG-WIR-021).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Create tenant** (modal, opened by *Create tenant*; *Create tenant* calls `createTenant`, *Cancel* sends nothing)

**Collects what `createTenant` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[a-z0-9-]+$` | — | — | `createTenant` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createTenant` body |
| Billing email `billingEmail` | text field | required | — | — | — | — | `createTenant` body |
| Billing address `billingAddress` | text area | optional | — | max length 500 | — | — | `createTenant` body |
| Account manager principal `accountManagerPrincipalId` | picker: choose an account manager principal | optional | — | — | shows names, sends the id | — | `createTenant` body |
| Plan `planId` | picker: choose a plan | optional | — | — | shows names, sends the id | — | `createTenant` body |

Errors to draw in the form: 409 Code already in use

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `SCOPE_MANAGE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Create org unit (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Create tenant (secondary button) | `createTenant` POST `/tenants` | CreateTenantRequest | Tenant | 409 Code already in use | opens modal first |

**Data it reads**: `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-419` Provisioning Command Center: *Back to Provisioning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tenant organization provisioning list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tenant organization provisioning untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tenant organization provisioning yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the tenant organization provisioning are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `SCOPE_MANAGE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Code already in use; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
tenant: Marina Leisure Group
brand: AquaCove Waterparks
regions:
- UAE (AED)
- Oman (OMR)
```

#### Permissions

- `createOrgUnit` → `SCOPE_MANAGE` (configure) · staff
- `createTenant` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-420` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-420`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 6
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 2: Works in Tenant & Organization Provisioning → Create the customer's isolated TICVAI environment and primary organization structure.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-420?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Create org unit, Cancel, Create tenant.
- [ ] Every transition is wired: `ADM-419`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`, `SCOPE_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-421` Venue & Operational Structure Creation

**Automatically create the initial venue structure using information collected during onboarding.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-421 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `SCOPE_MANAGE` (1 operate, 1 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Venue Settings) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/tenants-licensing/venue-operational-structure-creation-adm-421` |

**Known gaps.** **Venue & Operational Structure Creation declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either … Removed 2 October 2026 (CHG-WIR-021): Venue structure creation declared createPrincipal and setPasswordPolicy (the administrator and security baseline, ADM-422's job) and nothing created a venue … Removed 2 October 2026 (CHG-WIR-021): Venue structure creation declared createPrincipal and setPasswordPolicy (the administrator and security baseline, ADM-422's job) and nothing created a venue …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Onboarding: create the first venues of a tenant from the onboarding answers, under a platform-staff grant.

**Fixed on main** (the package already carries these; draw what it says): Operations are createPrincipal and setPasswordPolicy; nothing creates a venue. (CHG-WIR-021).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (decided 28 September, audit R098). This screen's operations run in that tenant's cell, and a platform token carries no tenant permission there until a platform-staff grant … | `Tenant.id` |
| Venue Name | select field | — | — | — | — | — | — |
| Venue Type | select field | — | — | — | — | — | — |
| Address | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| Currency | select field | — | — | — | — | — | — |
| Operating Region | select field | — | — | — | — | — | — |
| Default Language | select field | — | — | — | — | — | — |
| Operating Model | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (decided 28 September, audit R098). Required: `id` (a client UUIDv7), `permissions` (tenant permissions only — the ones this screen's operations need, preselected), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Create venue structure** (modal, opened by *Create venue structure*; *Create venue structure* calls `createOrgUnit`, *Cancel* sends nothing)

**Collects what `createOrgUnit` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Level `level` | select | required | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | — | The eight organisational levels, plus `subject`. Restored 24 August. | `createOrgUnit` body |
| Parent `parentId` | picker: choose a parent | required | — | — | shows names, sends the id | Required for every level except tenant, which the cell creates at provisioning. | `createOrgUnit` body |
| Code `code` | text field | required | — | max length 64; pattern `^[a-z0-9_]+$` | — | Becomes the final ltree segment. Immutable once created. | `createOrgUnit` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createOrgUnit` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Open access grant (permissions, reason, expiry)**: Permissions preselected to exactly what this screen's tenant calls need (TENANT_CONFIGURE, USER_MANAGE), never PLATFORM_* (those ride on the platform token); reason required and shown to the tenant; expiry at most 8 hours ahead (proposed). The tenant must be picked first. *(source: R098; contracts/spine/identity.yaml#openPlatformStaffGrant)*
- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setPasswordPolicy: tenant-wide only, no region or venue override is offered. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/identity.yaml#setPasswordPolicy)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (detail panel, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (decided 28 September, audit R098): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Create venue structure (secondary button) | `createOrgUnit` POST `/org-units` | CreateScopeNodeRequest | OrgUnit | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. | opens modal first |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Open access grant**: Confirmation names the consequence first, then asks for the authentication code (authenticator app, or an emailed code as fallback); only a verified challenge sends openPlatformStaffGrant with its single-use stepUpToken. Wrong code: the action is not sent and nothing changes; five wrong codes lock step-up for the policy's lockout minutes and the screen says when it lifts. Why the control exists: Opens a platform operator's access into a tenant's data. *(source: contracts/spine/identity.yaml#openPlatformStaffGrant; R126; contracts/spine/identity.yaml#createMfaChallenge)*

**Data it reads**: `listTenants` (onLoad, The tenant picker — the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-419` Provisioning Command Center: *Back to Provisioning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue operational structure configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue operational structure untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue operational structure configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions, expiry). The same state returns when the grant reaches `expiresAt` (decided 28 September, audit R098). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Idempotency conflict or optimistic concurrency failure. Two causes, so two types. |

#### Edge cases to draw

- **The platform-staff grant expires while the operator is mid-edit**: Every tenant action disables at once, the grantRequired state returns with Open access grant, and anything typed is kept so it can be sent after a new grant; the countdown in the grant panel warns before expiry. *(source: R098; screens/P09-platform-admin-console.yaml#ADM-412)*
- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_TENANT_ACCESS for Open access grant; USER_MANAGE for createPrincipal; TENANT_CONFIGURE for setPasswordPolicy. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/spine/identity.yaml#openPlatformStaffGrant)*
- **createPrincipal answers 409**: Show it as something the person can act on, not a failure: Username already in use within this cell *(source: contracts/spine/identity.yaml#createPrincipal)*

#### Consistency with other screens

- Match `ADM-412`: Same tenant picker, grant panel and grantRequired state on every P09 screen that acts in a tenant (R098).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue:
  name: AquaCove Muscat
  type: Waterpark
  timeZone: Asia/Muscat
  currency: OMR (from region)
  language: Arabic
```

#### Permissions

- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `createOrgUnit` → `SCOPE_MANAGE` (configure) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-421` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-421`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 6
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 4: Works in Venue & Operational Structure Creation → Automatically create the initial venue structure using information collected during onboarding.

#### Acceptance for the design

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 403, 409).
- [ ] Every output is drawn (7 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-421?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Create venue structure.
- [ ] Every transition is wired: `ADM-419`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `SCOPE_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 3 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-422` Administrator & Security Initialization

**Create the initial authorized customer administrator and establish the tenant security baseline.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-422 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`, `TENANT_CONFIGURE`, `USER_MANAGE` (1 operate, 3 configure, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Security Setup) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `tenantId` (session) |
| Route | `/tenants-licensing/administrator-security-initialization-adm-422` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Create the customer's first administrator and the security baseline (password policy, MFA floor, audit on). The first administrator holds ROLE_MANAGE and so must enrol MFA at first sign-in.

**Fixed on main** (the package already carries these; draw what it says): Operations are getTenantLicences and addLicenceAddOn; nothing creates the administrator. (CHG-WIR-021); Fields are check-marked status lines ("✓ Administrator Account Created"). (CHG-SBO-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Create administrator** (modal, opened by *Create administrator*; *Create administrator* calls `createPrincipal`, *Cancel* sends nothing)

**Collects what `createPrincipal` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Username `username` | text area | required | — | max length 256 | — | — | `createPrincipal` body |
| Display name `displayName` | text field | required | — | max length 200 | — | — | `createPrincipal` body |
| Initial credential `initialCredential` | text area | optional | — | max length 512 | — | — | `createPrincipal` body |
| Must change credential `mustChangeCredential` | toggle | optional | on | — | — | — | `createPrincipal` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPrincipal` body |
| Roles `roleIds` | multi-picker: choose roles | optional | — | — | — | — | `createPrincipal` body |

Errors to draw in the form: 400 Validation failed; 409 Username already in use within this cell

**Form: Set security baseline** (modal, opened by *Set security baseline*; *Set security baseline* calls `setPasswordPolicy`, *Cancel* sends nothing)

**Collects what `setPasswordPolicy` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Min length `minLength` | number field | required | 12 | min 8 | — | A tenant may raise the length and never set it below 8 (decided 28 September, audit R126 (7)). | `setPasswordPolicy` body |
| Require breach check `requireBreachCheck` | toggle | optional | on | — | — | The single most effective rule. Refusing a password known to be breached stops more account takeovers than every composition rule combined. | `setPasswordPolicy` body |
| Max age days `maxAgeDays` | number field (days) | optional | — | — | — | Null is the recommended value. Forced rotation produces `Summer2026!` becoming `Summer2027!`, and it is offered because some tenants are contractually obliged to have it rather … | `setPasswordPolicy` body |
| Recovery methods `recoveryMethods` | multi-select chips | optional | — | Email · SMS · Security questions · In person verification · Support assisted | — | BL-132. A guest locked out had no path back — lockout existed and recovery did not, which turns a forgotten password into a support call. | `setPasswordPolicy` body |
| Max concurrent sessions `maxConcurrentSessions` | number field | optional | — | — | — | BL-145. Null, and that is the decision. | `setPasswordPolicy` body |
| Device restriction `deviceRestriction` | group | optional | — | — | — | BL-146. Device, browser, IP and location restriction on access. | `setPasswordPolicy` body |
| Allowed ip ranges `deviceRestriction.allowedIpRanges` | list of values (chips) | optional | — | — | — | — | `setPasswordPolicy` body |
| Allowed countries `deviceRestriction.allowedCountries` | list of values (chips) | optional | — | — | — | — | `setPasswordPolicy` body |
| Require registered device `deviceRestriction.requireRegisteredDevice` | toggle | optional | off | — | — | — | `setPasswordPolicy` body |
| On violation `deviceRestriction.onViolation` | segmented control | optional | Require step up | Warn · Require step up · Block | — | — | `setPasswordPolicy` body |
| Lockout after attempts `lockoutAfterAttempts` | number field | optional | 10 | — | — | — | `setPasswordPolicy` body |
| Lockout minutes `lockoutMinutes` | number field (minutes) | optional | 15 | — | — | A temporary lockout, not a permanent one. Permanent lockout on failed attempts is a denial-of-service anybody can run against a known username. | `setPasswordPolicy` body |
| Force change on first logon `forceChangeOnFirstLogon` | toggle | optional | on | — | — | — | `setPasswordPolicy` body |
| Reuse prevention count `reusePreventionCount` | stepper or slider | optional | 5 | min 0; max 24 | — | How many previous credentials a staff member may not reuse — the last 5 unless the tenant sets another (decided 28 September, audit R132). | `setPasswordPolicy` body |
| MFA required for permissions `mfaRequiredForPermissions` | multi-select chips | optional | ROLE MANAGE, LEDGER APPROVE, PLATFORM TENANT VIEW, PLATFORM TENANT MANAGE, PLATFORM TENANT TERMINATE, PLATFORM TENANT ACCESS, PLATFORM PLAN MANAGE, PLATFORM CELL VIEW, PLATFORM CELL MANAGE, PLATFORM BILLING VIEW, PLATFORM BILLING MANAGE, PLATFORM RELEASE VIEW, PLATFORM RELEASE MANAGE, PLATFORM RELEASE PROMOTE, PLATFORM MIGRATION VIEW, PLATFORM MIGRATION APPLY | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; A … | — | Step-up rather than blanket MFA. Requiring it for a refund approval and not for reading a rota is what stops people sharing devices to avoid it. | `setPasswordPolicy` body |

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Administrator Account Created** (progress indicator): A progress output of initialisation, not an input.

**Email Verified** (progress indicator): A progress output of initialisation, not an input.

**Tenant Access Assigned** (progress indicator): A progress output of initialisation, not an input.

**Default Role Applied** (progress indicator): A progress output of initialisation, not an input.

**Security Policy Applied** (progress indicator): A progress output of initialisation, not an input.

**Audit Logging Enabled** (progress indicator): A progress output of initialisation, not an input.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (secondary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Create administrator (secondary button) | `createPrincipal` POST `/principals` | CreatePrincipalRequest | Principal | 400 Validation failed; 409 Username already in use within this cell | opens modal first |
| Set security baseline (secondary button) | `setPasswordPolicy` PUT `/password-policy` | PasswordPolicy | PasswordPolicy | — | opens modal first |

**Data it reads**: `getTenantLicences` (onLoad, Licence and entitlement activation); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-419` Provisioning Command Center: *Back to Provisioning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The administrator security initialization configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the administrator security initialization untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No administrator security initialization configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `TENANT_CONFIGURE`, `USER_MANAGE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Username already in use within this cell |

#### Edge cases to draw

- **First administrator signs in**: Is taken to MFA enrolment before anything else (ROLE_MANAGE is in the floor). *(source: R135; F109 step 1)*
- **Can read but not change (holds PLATFORM_TENANT_VIEW only)**: Everything reads; the actions needing another permission are not offered as live buttons: PLATFORM_TENANT_MANAGE for addLicenceAddOn. Where the person would reasonably expect the action, it shows disabled with the permission named. The server refuses with 403 forbidden regardless. *(source: contracts/satellite/subscription.yaml#addLicenceAddOn)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  ✓ Administrator Account Created: 11
  ✓ Email Verified: 46
  ✓ Tenant Access Assigned: Arabian Trails
  ✓ Default Role Applied: 46
  ✓ Security Policy Applied: 233
  ✓ Audit Logging Enabled: 19
```

#### Permissions

- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `addLicenceAddOn` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `createPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `setPasswordPolicy` → `TENANT_CONFIGURE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.5.1 | License Generation - System shall generate subscription licenses. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.2 | License Assignment - System shall assign licenses to tenants. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.3 | License Validation - System shall validate licenses automatically. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.4 | License Enforcement - System shall enforce licensing restrictions. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.5 | License Expiration - System shall support license expiration management. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.6 | Grace Period Management - System shall support configurable grace periods. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.7 | License Renewal Management - System shall support license renewals. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.8 | License Audit Logs - System shall maintain license audit logs. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.4.1 | Marketplace Catalog - System shall provide a marketplace of available modules. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.2 | Module Discovery - System shall allow customers to browse modules. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.3 | Module Installation - System shall support self-service module installation. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| 20.4.4 | Module Activation - System shall support module activation. | Subscription & Licensing Management | CONTRACTED | `addLicenceAddOn` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-422` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-422`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 6
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 6: Works in Administrator & Security Initialization → Create the initial authorized customer administrator and establish the tenant security baseline.

#### Acceptance for the design

- [ ] Every input above is drawn (27), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-422?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Create administrator, Set security baseline.
- [ ] Every transition is wired: `ADM-419`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`, `TENANT_CONFIGURE`, `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-423` License & Entitlement Activation

**Translate the commercial subscription purchased in Board 5 into enforceable technical entitlements.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-423 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/license-entitlement-activation-adm-423` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Turn the purchased subscription into enforceable technical entitlements (modules, limits).

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Data it reads**: `listModuleCatalogue` (onLoad, Module activation and dependencies)

**Where the user goes next**

- → `ADM-419` Provisioning Command Center: *Back to Provisioning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The license entitlement activation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the license entitlement activation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No license entitlement activation yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the license entitlement activation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
listModuleCatalogue (ModuleListing):
- name: Growth plan
  description: Guest charged twice at Main Gate Till 3
  price: AED 1,250.00
- name: AquaCove Annual Pass Gold
  description: Group of 40 from Desert Gate Tours
  price: AED 48,000.00
```

#### Permissions

- `listModuleCatalogue` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After contract, TICVAI provisions the tenant with a basic setup reflecting the tier and licensed modules (e.g. mobile app, B2C, B2B enabled as contracted) before handover; AI can assist initial product/event/ticket setup following the same process as manual setup. *(client request · MoM 10 Sep 2026, 4.12 Tenant Provisioning & Go-Live Setup · DI-833)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-423` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-423`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 6
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 8: Works in License & Entitlement Activation → Translate the commercial subscription purchased in Board 5 into enforceable technical entitlements.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-423?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-419`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-424` Module Activation & Dependency Validation

**Activate the modules purchased in Board 4/5 and verify all required dependencies.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 1 · needs the `core` module |
| Block | Block A · task APP-WL-ADM-424 |
| Who uses it | ticvai staff holding `PLATFORM_PLAN_MANAGE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 operate, 1 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/tenants-licensing/module-activation-dependency-validation-adm-424` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-021): Module Activation was wired to listVenueTypeTemplates, which belongs to the next screen (ADM-425 Venue Template Application); activation reads licence data …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Activate purchased modules and check their dependencies.

**Fixed on main** (the package already carries these; draw what it says): Only listVenueTypeTemplates (TENANT_CONFIGURE). (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Activate modules** (modal, opened by *Activate modules*; *Activate modules* calls `setModuleEnablement`, *Cancel* sends nothing)

**Collects what `setModuleEnablement` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Modules `modules` | repeatable rows | required | — | — | — | — | `setModuleEnablement` body |
| Module key `modules[].moduleKey` | field | required | — | — | — | — | `setModuleEnablement` body |
| Is enabled `modules[].isEnabled` | toggle | required | — | — | — | — | `setModuleEnablement` body |

Errors to draw in the form: 400 Module not licensed, or still referenced by navigation or homepage (ModuleReferenceProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension mode | chip: Read only, No new sales, Full lockout | Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets. |
| Suspension reason | text | — |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Suspension notice message | in the reader's language | The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`. |
| Termination scheduled at | 1 Oct 2026, 14:30 | When `terminateTenant` started the retention window. Null when no termination is under way. |
| Termination retention until | 1 Oct 2026, 14:30 | `terminationScheduledAt` plus the request's `retentionDays`. Stored, not recomputed — the day count is client-supplied and exists nowhere … |
| Termination reason | text | — |
| Termination requested by principal | the name it points at, never the id | — |
| Plan | the name it points at, never the id | — |
| Plan name | text | — |
| Cell count | 1,234 | — |
| Venue count | 1,234 | — |
| Region | the name it points at, never the id | The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided … |
| Billing email | text | — |
| Billing address | text | Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent. |

**Licensed modules** (detail panel, from `getTenantLicences`)

| Shows | Format | Notes |
|---|---|---|
| Powered by removable | yes / no (icon or chip) | Whether the tenant's licence lets it switch "Powered by TICVAI" off (Chinmay, 2 October, workbook Q160 and the pre-apply round … |
| Plan | the name it points at, never the id | — |
| Licensed modules | list or chips (count when long) | Union of plan modules and add-ons. The White Label Builder reads this and cannot enable anything absent from it. |
| Module key | text | — |
| Display name | text | — |
| Source | chip: Plan, Add on | — |
| Valid to | 1 Oct 2026 | — |
| Limits | list or chips (count when long) | — |
| Metric | chip: Venues, Workstations, Active users, Devices, Branded apps, AI tokens… | — |
| Limit | 1,234 | Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure … |
| Overage allowed | yes / no (icon or chip) | — |
| Overage unit price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |

**Dependencies** (data table, from `listModuleCatalogue`)

| Shows | Format | Notes |
|---|---|---|
| Module code | text | — |
| Name | text | — |
| Description | text | — |
| Category | text | — |
| Requires modules | list or chips (count when long) | — |
| Incompatible with modules | list or chips (count when long) | — |
| Included in tiers | list or chips (count when long) | — |
| Price | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Pricing basis | chip: Included, Flat fee, Per venue, Per unit, Revenue share, Metered | — |
| Metered metric | chip: Venues, Workstations, Active users, Devices, Branded apps, AI tokens… | For `metered`, what is counted (`aiTokens` for the AI module). Null otherwise. |
| Metered unit size | 1,234 | For `metered`, how many units `price` buys (e.g. 1000 tokens). |
| Provisioning minutes | 1,234 | — |
| Requires professional services | yes / no (icon or chip) | — |
| Status | chip: Available, Beta, Deprecated, Withdrawn | — |

**Active modules** (data table, from `getModuleEnablement`)

| Shows | Format | Notes |
|---|---|---|
| Module key | text | — |
| Display name | text | — |
| Is licensed | yes / no (icon or chip) | From the tenant's subscription. False makes enablement impossible. |
| Is enabled | yes / no (icon or chip) | — |
| Referenced by | list or chips (count when long) | Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (secondary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Activate modules (secondary button) | `setModuleEnablement` PUT `/tenant-config/modules` | inline | ModuleEnablement[] | 400 Module not licensed, or still referenced by navigation or homepage (ModuleReferenceProblem) | opens modal first |

**Data it reads**: `listTenants` (onLoad, Pick the tenant whose modules are being activated (audit …); `getTenantLicences` (onLoad, The modules the tenant has bought); `listModuleCatalogue` (onLoad, Each module's dependencies, to validate before activation); `getModuleEnablement` (onLoad, Which modules are switched on now)

**Where the user goes next**

- → `ADM-419` Provisioning Command Center: *Back to Provisioning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The module activation dependency list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the module activation dependency untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No module activation dependency yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the module activation dependency are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `TENANT_CONFIGURE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Module not licensed, or still referenced by navigation or homepage (ModuleReferenceProblem); 400 Validation failed |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
modules:
- module: fnb
  dependsOn: pos
  ok: true
- module: membership
  dependsOn: ticketing, access
  ok: true
```

#### Permissions

- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `getTenantLicences` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listModuleCatalogue` → `PLATFORM_PLAN_MANAGE` (configure) · staff, guest, prospect
- `getModuleEnablement` → `TENANT_CONFIGURE` (configure) · staff
- `setModuleEnablement` → `TENANT_CONFIGURE` (configure) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 20.5.1 | License Generation - System shall generate subscription licenses. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.2 | License Assignment - System shall assign licenses to tenants. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.3 | License Validation - System shall validate licenses automatically. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.4 | License Enforcement - System shall enforce licensing restrictions. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.5 | License Expiration - System shall support license expiration management. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.6 | Grace Period Management - System shall support configurable grace periods. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.7 | License Renewal Management - System shall support license renewals. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 20.5.8 | License Audit Logs - System shall maintain license audit logs. | Subscription & Licensing Management | CONTRACTED | `getTenantLicences` |
| 19.1.13 | Module Enablement - System shall allow enabling and disabling application modules. | Guest Mobile App & Branding | CONTRACTED | `setModuleEnablement` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After contract, TICVAI provisions the tenant with a basic setup reflecting the tier and licensed modules (e.g. mobile app, B2C, B2B enabled as contracted) before handover; AI can assist initial product/event/ticket setup following the same process as manual setup. *(client request · MoM 10 Sep 2026, 4.12 Tenant Provisioning & Go-Live Setup · DI-833)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Modules (`modules.modules`) | — | — | every guest screen (web, app and kiosk) | — |
| Modules: module key (`modules.modules[].moduleKey`) | — | — | every guest screen (web, app and kiosk) | — |
| Modules: is enabled (`modules.modules[].isEnabled`) | — | — | every guest screen (web, app and kiosk) | — |

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-424` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-424`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 6
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 10: Works in Module Activation & Dependency Validation → Activate the modules purchased in Board 4/5 and verify all required dependencies.

#### Acceptance for the design

- [ ] Every input above is drawn (9), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (57 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-424?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Activate modules.
- [ ] Every transition is wired: `ADM-419`.
- [ ] Every gated control is gated: `PLATFORM_PLAN_MANAGE`, `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-425` Venue Template Application

**Apply an appropriate initial configuration template based on the venue assessment from Board 2.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-425 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `TENANT_CONFIGURE` (1 operate, 1 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/tenants-licensing/venue-template-application-adm-425` |

**What the spec says about it.** **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listVenueTypeTemplates` (TENANT_CONFIGURE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-021): Venue Template Application was wired to updateRegionSettings (region money and time settings), which is initial configuration (ADM-426); the template list …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Apply a configuration template to a new venue based on its assessment.

**Fixed on main** (the package already carries these; draw what it says): Only updateRegionSettings. (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `TENANT_CONFIGURE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: updateRegionSettings: set per region (money, tax, ledger); venues inherit and cannot override. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#updateRegionSettings)*

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Venue templates** (data table, from `listVenueTypeTemplates`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Venue kind | chip: Theme park, Water park, Museum, Theatre, Stadium, Arena… | — |
| Seeds product kinds | list or chips (count when long) | — |
| Seeds roles | list or chips (count when long) | — |
| Seeds admission profiles | list or chips (count when long) | — |
| Seeds reports | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |

**Data it reads**: `listVenueTypeTemplates` (onLoad, Starting configurations by venue kind, to pick from); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

**Where the user goes next**

- → `ADM-419` Provisioning Command Center: *Back to Provisioning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue template application list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue template application untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue template application yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue template application are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `TENANT_CONFIGURE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed |

#### Edge cases to draw

- **updateRegionSettings answers 409**: Show it as something the person can act on, not a failure: Currency or scale change rejected because transactions exist in this region. *(source: contracts/spine/tenancy.yaml#updateRegionSettings)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
template: Waterpark - large
appliedTo: AquaCove Muscat
sets:
- opening hours
- zones
- default products
```

#### Permissions

- `listVenueTypeTemplates` → `TENANT_CONFIGURE` (configure) · staff, public
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-425` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-425`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 6
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 12: Works in Venue Template Application → Apply an appropriate initial configuration template based on the venue assessment from Board 2.

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (400, 403).
- [ ] Every output is drawn (13 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-425?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant.
- [ ] Every transition is wired: `ADM-419`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-426` Initial Configuration & Regional Defaults

**Apply safe initial defaults using information already provided during onboarding.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-426 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`, `REGION_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE`… (1 operate, 3 configure, 3 read); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Low-risk settings such as; Business-critical settings such as) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `regionId` (navigation), `tenantId` (navigation) |
| Route | `/tenants-licensing/initial-configuration-regional-defaults-adm-426` |

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Safe initial defaults from onboarding answers (currency, time zone, language, tax, refund and payment rules).

**Fixed on main** (the package already carries these; draw what it says): Only runGoLiveValidation. (CHG-WIR-021); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Currency | select field | — | — | — | — | — | — |
| Time Zone | select field | — | — | — | — | — | — |
| Language | select field | — | — | — | — | — | — |
| Venue Type | select field | — | — | — | — | — | — |
| Ticket prices | select field | — | — | — | — | — | — |
| Tax | select field | — | — | — | — | — | — |
| Refund policy | select field | — | — | — | — | — | — |
| Payment rules | select field | — | — | — | — | — | — |
| Access rules | select field | — | — | — | — | — | — |
| Settlement | select field | — | — | — | — | — | — |
| Capacity | select field | — | — | — | — | — | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Apply defaults** (modal, opened by *Apply defaults*; *Apply defaults* calls `setVenueSettingsDefaults`, *Cancel* sends nothing)

**Collects what `setVenueSettingsDefaults` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Calendar day start hour `calendarDayStartHour` | stepper or slider | optional | 6 | min 0; max 23 | — | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in … | `setVenueSettingsDefaults` body |
| Support hours `supportHours` | group | optional | — | — | — | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. | `setVenueSettingsDefaults` body |
| Mode `supportHours.mode` | radio group | optional | — | Always on · Business hours · Custom · None | — | — | `setVenueSettingsDefaults` body |
| Timezone `supportHours.timezone` | text field | optional | — | — | — | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. | `setVenueSettingsDefaults` body |
| Windows `supportHours.windows` | repeatable rows | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Day `supportHours.windows[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettingsDefaults` body |
| From `supportHours.windows[].from` | text field | optional | — | — | — | Wall-clock time the desk opens. | `setVenueSettingsDefaults` body |
| To `supportHours.windows[].to` | text field | optional | — | — | — | Wall-clock time the desk closes. | `setVenueSettingsDefaults` body |
| Out of hours message `supportHours.outOfHoursMessage` | text field | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Quiet hours `quietHours` | group | optional | — | — | — | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. | `setVenueSettingsDefaults` body |
| From `quietHours.from` | text field | optional | — | — | — | Wall-clock time sending stops | `setVenueSettingsDefaults` body |
| To `quietHours.to` | text field | optional | — | — | — | Wall-clock time sending resumes | `setVenueSettingsDefaults` body |
| Biometrics `biometrics` | group | optional | — | — | — | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. | `setVenueSettingsDefaults` body |
| Is enabled `biometrics.isEnabled` | toggle | optional | off | Off by default, and turning it on is refused without the two fields below. | — | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — a DPIA nobody can … | `setVenueSettingsDefaults` body |
| Dpia reference `biometrics.dpiaReference` | text field | optional | — | max length 200 | — | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is … | `setVenueSettingsDefaults` body |
| Consent notice acknowledged at `biometrics.consentNoticeAcknowledgedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice … | `setVenueSettingsDefaults` body |
| Face tag purge minutes after close `biometrics.faceTagPurgeMinutesAfterClose` | number field (minutes) | optional | 0 | — | — | BL-106. How long a same-visit Face Tag survives past the close of the operating day, and zero is the default because that is what 3.2.44 describes. | `setVenueSettingsDefaults` body |
| Consent form `biometrics.consentFormId` | picker: choose a consent form | optional | — | Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access … | shows names, sends the id | The venue's own consent form, which every biometric capture is taken on (decided 2 October 2026, Chinmay, batch 4, BO-188: "Consent first, on the venue's consent form"; DEC-128 … | `setVenueSettingsDefaults` body |
| Allow minors `biometrics.allowMinors` | toggle | optional | on | Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method. | — | Whether this venue enrols minors at all (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: "Guardian consent on the venue's form; minor age per country; the … | `setVenueSettingsDefaults` body |
| Accreditation face matching `biometrics.accreditationFaceMatching` | group | optional | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables it, with applicant …; Enabling it is refused without `legalSignOffReference` … | — | Face matching to find duplicate accreditation applicants, off unless the venue enables it (decided 2 October 2026, Chinmay, critical set 3, BO-631: "Only where the venue enables … | `setVenueSettingsDefaults` body |
| Is enabled `biometrics.accreditationFaceMatching.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettingsDefaults` body |
| Legal sign off reference `biometrics.accreditationFaceMatching.legalSignOffReference` | text field | optional | — | max length 200 | — | The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when. | `setVenueSettingsDefaults` body |
| Segregated access `segregatedAccess` | group | optional | — | — | — | CF-130. Configured at venue level because it changes by region and the venue is where it is known — a Ladies Night, a family session, a prayer-time closure. | `setVenueSettingsDefaults` body |
| Is enabled `segregatedAccess.isEnabled` | toggle | optional | off | — | — | — | `setVenueSettingsDefaults` body |
| Applies to access points `segregatedAccess.appliesToAccessPointIds` | multi-picker: choose applies to access points | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Schedule `segregatedAccess.schedule` | repeatable rows | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Day `segregatedAccess.schedule[].day` | select | optional | — | Mon · Tue · Wed · Thu · Fri · Sat · Sun | — | — | `setVenueSettingsDefaults` body |
| From `segregatedAccess.schedule[].from` | text field | optional | — | — | — | Wall-clock time | `setVenueSettingsDefaults` body |
| To `segregatedAccess.schedule[].to` | text field | optional | — | — | — | Wall-clock time | `setVenueSettingsDefaults` body |
| Admits `segregatedAccess.schedule[].admits` | radio group | optional | — | All · Women · Women and children · Families · Members | — | — | `setVenueSettingsDefaults` body |
| Gender verification `segregatedAccess.genderVerification` | segmented control | optional | Off | Off · Staff assisted · Device assisted; Available only where the driver reports the capability, and the result is advisory to the steward rather than decisive at the turnstile (3. | — | `off` — the entitlement decides and a steward handles exceptions. The default, and what is contracted. | `setVenueSettingsDefaults` body |
| Override rate alert threshold `segregatedAccess.overrideRateAlertThreshold` | number field | optional | — | — | — | Where `deviceAssisted` is on. An override rate near zero means the steward has stopped deciding, and that is the number that says whether the human safeguard is working or … | `setVenueSettingsDefaults` body |
| Alerting `alerting` | group | optional | — | The panel is the default and email or WhatsApp only where the matrix names them — an operational alert that arrives by email is an alert nobody sees in time. | — | CF-134. On-platform notification, marked as read. | `setVenueSettingsDefaults` body |
| Channel `alerting.channel` | segmented control | optional | Dashboard panel | Dashboard panel · Dashboard and email · Dashboard and whatsapp | — | — | `setVenueSettingsDefaults` body |
| Acknowledgement required `alerting.acknowledgementRequired` | toggle | optional | on | — | — | — | `setVenueSettingsDefaults` body |
| Escalate after minutes `alerting.escalateAfterMinutes` | number field (minutes) | optional | — | — | — | — | `setVenueSettingsDefaults` body |
| Display currencies `displayCurrencies` | list of values (chips) | optional | — | A code the region has no rate for is refused `400`. | — | Which currencies this venue shows guests (decided 28 September, audit R120 (a)). | `setVenueSettingsDefaults` body |
| Charge currencies `chargeCurrencies` | list of values (chips) | optional | — | presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. | — | Which currencies a guest may select and pay in (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). | `setVenueSettingsDefaults` body |
| Cart lease seconds `cartLeaseSeconds` | number field (seconds) | optional | 900 | min 30; max 3600 | — | How long a cart holds capacity (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. | `setVenueSettingsDefaults` body |
| Cart hold extension minutes `cartHoldExtensionMinutes` | stepper or slider (minutes) | optional | 5 | min 1; max 30 | — | How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094). | `setVenueSettingsDefaults` body |
| Cart max extensions `cartMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). | `setVenueSettingsDefaults` body |
| Resale cutoff hours `resaleCutoffHours` | number field (hours) | optional | 24 | min 0; max 168 | — | Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). | `setVenueSettingsDefaults` body |
| Exchange cutoff hours `exchangeCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). | `setVenueSettingsDefaults` body |
| Reschedule cutoff hours `rescheduleCutoffHours` | number field (hours) | optional | 24 | min 0; max 720 | — | Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). | `setVenueSettingsDefaults` body |
| Reservation max extensions `reservationMaxExtensions` | stepper or slider | optional | 1 | min 0; max 5 | — | How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094). | `setVenueSettingsDefaults` body |
| … 34 more | | | | | | the rest are in `schemas.json` | `setVenueSettingsDefaults` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Save region settings** (modal, opened by *Save region settings*; *Save region settings* calls `updateRegionSettings`, *Cancel* sends nothing)

**Collects what `updateRegionSettings` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Country code `countryCode` | text field | required | — | pattern `^[A-Z]{2}$` | — | ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell. | `updateRegionSettings` body |
| Currency code `currencyCode` | text field | required | — | pattern `^[A-Z]{3}$` | — | — | `updateRegionSettings` body |
| Currency scale `currencyScale` | stepper or slider | required | — | min 0; max 4 | — | Decimal places for this region's currency. Varies by currency — some use 2, some use 3. | `updateRegionSettings` body |
| Time zone `timeZone` | text field | required | — | — | — | IANA zone, e.g. `Asia/Dubai`. | `updateRegionSettings` body |
| Date format `dateFormat` | text field | optional | dd/MM/yyyy | — | — | — | `updateRegionSettings` body |
| Number format `numberFormat` | text field | optional | #,##0.00 | — | — | — | `updateRegionSettings` body |
| Fiscal year start month `fiscalYearStartMonth` | stepper or slider | required | — | min 1; max 12 | — | Varies by country. | `updateRegionSettings` body |
| Allowed AI residencies `allowedAiResidencies` | list of values (chips) | optional | — | — | — | The region's compliance gate on AI providers (decided 28 September, audit R203; ADR-0009). | `updateRegionSettings` body |
| AI residency class `aiResidencyClass` | segmented control | optional | Uae only | Uae only · Global allowed · On prem; 5-122B, Falcon-H1 Arabic or Jais 2), only where the client asks for it (CHG-R1S-002).; Moving from `uaeOnly` to `globalAllowed` without `aiResidencyOptIn` is refused `422 residency-opt-in-required`; on a tenant … | — | The tenant's AI residency class (decided 2 October 2026, Chinmay, "AI residency: per-tenant residency class"; DEC-539; CHG-CSP-009; amends AI-D02 and ADR-0009 section 1). | `updateRegionSettings` body |
| AI residency opt in `aiResidencyOptIn` | group | optional | — | — | — | The evidence a `globalAllowed` opt-in needs under PDPL Article 23 (DEC-539; CHG-CSP-009): the tenant's references to its vendor contract, its DPIA and the notice guests see. | `updateRegionSettings` body |
| Vendor contract reference `aiResidencyOptIn.vendorContractReference` | text field | optional | — | max length 200 | — | — | `updateRegionSettings` body |
| Dpia reference `aiResidencyOptIn.dpiaReference` | text field | optional | — | max length 200 | — | — | `updateRegionSettings` body |
| Guest notice reference `aiResidencyOptIn.guestNoticeReference` | text field | optional | — | max length 200 | — | — | `updateRegionSettings` body |
| Local language name locales `localLanguageNameLocales` | list of values (chips) | optional | — | — | — | The languages an outlet name must also be given in, in this country (decided 2 October 2026, Chinmay, batch 2 #26: "English plus the local language where the country needs it" … | `updateRegionSettings` body |
| Required billing documents `requiredBillingDocuments` | repeatable rows | optional | {'document type': 'trade licence', 'required when': 'always'}, {'document type': 'vat certificate', 'required when': 'trn entered'} | — | — | Which documents a TICVAI customer's billing entity must upload, in this country (decided 2 October 2026, Chinmay, batch 6 set 7, ADM-411: "Trade licence always; VAT certificate … | `updateRegionSettings` body |
| Document type `requiredBillingDocuments[].documentType` | text field | optional | — | max length 64 | — | The document kind, as the subscription contract's `PartnerDocument` names it (`tradeLicence`, `vatCertificate`, ...). | `updateRegionSettings` body |
| Required when `requiredBillingDocuments[].requiredWhen` | segmented control | optional | — | Always · Trn entered | — | — | `updateRegionSettings` body |
| Minor age threshold `minorAgeThreshold` | stepper or slider | optional | 18 | min 0; max 21 | — | The age below which a guest is a minor here, set per country (decided 2 October 2026, Chinmay, critical set 1, BO-187: "Guardian consent on the venue's form; minor age per … | `updateRegionSettings` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Currency or scale change rejected because transactions exist in this region, or a change to `aiResidencyClass` on a tenant TICVAI locked to `uaeOnly` …; 422 `aiResidencyClass` `globalAllowed` without the three references of `aiResidencyOptIn` (`residency-opt-in-required`; PDPL Article 23; DEC-539; CHG-CSP-009).

#### Outputs: what the screen shows and produces

**Shown**

**Open grant into this tenant** (banner, from `listOwnPlatformStaffGrants`): **Always visible while the screen acts on a tenant** (audit R098, the ADM-412 pattern): which tenant, which permissions, why, and the time left to `expiresAt`. At expiry every tenant action is disabled and the screen returns to its grantRequired state; a new need is a new grant. The tenant sees the grant in its own audit log. Found again after a reload with `listOwnPlatformStaffGrants`.

| Shows | Format | Notes |
|---|---|---|
| Operator display name | text | — |
| Permissions | list or chips (count when long) | — |
| Reason | text | — |
| Ticket ref | text | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Tenant** (data table, from `listTenants`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Status | chip: Onboarding, Active, Suspended, Terminating, Terminated | — |
| Suspension mode | chip: Read only, No new sales, Full lockout | Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets. |
| Suspension reason | text | — |
| Suspension effective at | 1 Oct 2026, 14:30 | When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. A future value is a pending suspension: the tenant stays `active` … |
| Suspension notice message | in the reader's language | The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`. |
| Termination scheduled at | 1 Oct 2026, 14:30 | When `terminateTenant` started the retention window. Null when no termination is under way. |
| Termination retention until | 1 Oct 2026, 14:30 | `terminationScheduledAt` plus the request's `retentionDays`. Stored, not recomputed — the day count is client-supplied and exists nowhere … |
| Termination reason | text | — |
| Termination requested by principal | the name it points at, never the id | — |
| Plan | the name it points at, never the id | — |
| Plan name | text | — |
| Cell count | 1,234 | — |
| Venue count | 1,234 | — |
| Region | the name it points at, never the id | The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided … |
| Billing email | text | — |
| Billing address | text | Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent. |

**Venue defaults** (detail panel, from `getVenueSettingsDefaults`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Venue | the name it points at, never the id | From the path of `setVenueSettings`. |
| Calendar day start hour | 1,234 | Where the venue's calendar day starts (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar … |
| Currency code | text | `readOnly` is the freeze. `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the … |
| Currency scale | 1,234 | Scale travels with currency (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency … |
| Support hours | grouped details | CF-100. A venue decides whether its support desk is 24/7 or bounded, and the platform does not. |
| Mode | chip: Always on, Business hours, Custom, None | — |
| Timezone | text | IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract. |
| Windows | list or chips (count when long) | — |
| Day | chip: Mon, Tue, Wed, Thu, Fri, Sat… | — |
| From | text | Wall-clock time the desk opens. |
| To | text | Wall-clock time the desk closes. |
| Out of hours message | text | — |
| Quiet hours | grouped details | When the platform does not send. A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this. |
| From | text | Wall-clock time sending stops |
| To | text | Wall-clock time sending resumes |
| Biometrics | grouped details | CF-35, BL-096, BL-105, BL-106. The venue-level master switch, and the one place a person is asked whether the paperwork exists. |
| Is enabled | yes / no (icon or chip) | Off by default, and turning it on is refused without the two fields below. `setVenueSettings` answers 422 rather than accepting an enable … |
| Dpia reference | text | The venue's own reference for its Article 21 assessment. The platform does not hold the document and does not judge it; it records that one … |
| Consent notice acknowledged at | 1 Oct 2026, 14:30 | When somebody confirmed the consent forms are in place at the point of capture. A guest consenting in an app is a record; a guest … |

**Region settings** (detail panel, from `getRegionSettings`)

| Shows | Format | Notes |
|---|---|---|
| Country code | text | ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell. |
| Currency code | text | — |
| Currency scale | 1,234 | Decimal places for this region's currency. Varies by currency — some use 2, some use 3. |
| Time zone | text | IANA zone, e.g. `Asia/Dubai`. |
| Date format | text | — |
| Number format | text | — |
| Fiscal year start month | 1,234 | Varies by country. |
| Allowed AI residencies | list or chips (count when long) | The region's compliance gate on AI providers (decided 28 September, audit R203; ADR-0009). |
| AI residency class | chip: Uae only, Global allowed, On prem | The tenant's AI residency class (decided 2 October 2026, Chinmay, "AI residency: per-tenant residency class"; DEC-539; CHG-CSP-009; amends … |
| AI residency class locked | yes / no (icon or chip) | Set by TICVAI at onboarding for a government, bank or health tenant (DEC-539), which must stay `uaeOnly`. |
| Tenant category | chip: Private, Semi government, Government, Banking, Payments, Health… | What kind of organisation the tenant is, for AI residency (3 October 2026, CHG-R1S-016; the legal research … |
| AI residency opt in | grouped details | The evidence a `globalAllowed` opt-in needs under PDPL Article 23 (DEC-539; CHG-CSP-009): the tenant's references to its vendor contract … |
| Vendor contract reference | text | — |
| Dpia reference | text | — |
| Guest notice reference | text | — |
| Confirmed by principal | the name it points at, never the id | — |
| Confirmed at | 1 Oct 2026, 14:30 | — |
| Local language name locales | list or chips (count when long) | The languages an outlet name must also be given in, in this country (decided 2 October 2026, Chinmay, batch 2 #26: "English plus the local … |
| Required billing documents | list or chips (count when long) | Which documents a TICVAI customer's billing entity must upload, in this country (decided 2 October 2026, Chinmay, batch 6 set 7, ADM-411 … |
| Document type | text | The document kind, as the subscription contract's `PartnerDocument` names it (`tradeLicence`, `vatCertificate`, ...). |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Open access grant (secondary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Apply defaults (secondary button) | `setVenueSettingsDefaults` PUT `/venue-settings-defaults` | VenueSettings | VenueSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Save region settings (secondary button) | `updateRegionSettings` PUT `/regions/{regionId}/settings` | RegionSettings | RegionSettings | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `listTenants` (onLoad, Pick the tenant being configured (audit R098)); `getVenueSettingsDefaults` (onLoad, The tenant's default for every venue setting); `getRegionSettings` (onLoad, The region's currency, time zone and money settings)

**Where the user goes next**

- → `ADM-419` Provisioning Command Center: *Back to Provisioning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The initial regional defaults configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the initial regional defaults untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing saved yet.** The form opens on the values it inherits and Apply defaults (`setVenueSettingsDefaults`) saves the first version; offers no other create action. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `REGION_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Currency or scale change rejected because transactions exist in this region, or a change to `aiResidencyClass` on a tenant TICVAI locked to `uaeOnly` …; 422 `aiResidencyClass` `globalAllowed` without the three references of `aiResidencyOptIn` (`residency-opt-in-required`; PDPL Article 23; DEC-539; CHG-CSP-009). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
form example:
  Currency: 128
  Time Zone: 42 min
  Language: 42 min
  Venue Type: AquaCove Abu Dhabi
  Ticket prices: AED 12,400.00
  Tax: 128
  Refund policy: 74
  Payment rules: 42
  Access rules: 7
  Settlement: 74
  Capacity: 312
```

#### Permissions

- `runGoLiveValidation` → `PLATFORM_TENANT_MANAGE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa
- `getVenueSettingsDefaults` → `TENANT_VIEW` (read) · staff
- `setVenueSettingsDefaults` → `TENANT_CONFIGURE` (configure) · staff
- `getRegionSettings` → `SCOPE_VIEW` (read) · staff
- `updateRegionSettings` → `REGION_CONFIGURE` (configure) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |
| 3.2.45 | Face Pass and Face Tag should support automatic gender recognition and reject customers who do not match the designated gender segment. | Admission and Access | CONTRACTED_PARTIAL | data `VenueSettings` |
| 3.2.46 | Face Pass shouldt restrict male guests attempting to enter during Friday Ladies Night, which needs to be validated with rule-based facial recognition validation. | Admission and Access | CONTRACTED | data `VenueSettings` |
| 8.9.3 | System shall display queue lengths, estimated wait times, queue utilization, queue alerts, and queue prediction metrics. | Unified Operations Dashboard | CONTRACTED | data `VenueSettings` |
| 11.1.15 | Approval Breach Alerts - System shall notify users when approval SLA thresholds are exceeded. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.17 | Approval Notifications - System shall notify approvers when new approval requests are assigned. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.18 | Approval Reminder Notifications - System shall send reminder notifications for pending approvals. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 11.1.19 | Approval Outcome Notifications - System shall notify requestors when approvals are approved, rejected or escalated. | Approval Workflows & Governance | CONTRACTED | data `VenueSettings` |
| 15.1.32 | Overstock Alerts - System shall generate overstock alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.33 | Stock Shortage Alerts - System shall generate stock shortage alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 15.1.34 | Expiry Alerts - System shall generate expiry alerts. | Inventory Management | CONTRACTED | data `VenueSettings` |
| 16.4.23 | Device Alerts - System shall generate device alerts. | Device Management | CONTRACTED | data `VenueSettings` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- After contract, TICVAI provisions the tenant with a basic setup reflecting the tier and licensed modules (e.g. mobile app, B2C, B2B enabled as contracted) before handover; AI can assist initial product/event/ticket setup following the same process as manual setup. *(client request · MoM 10 Sep 2026, 4.12 Tenant Provisioning & Go-Live Setup · DI-833)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-426` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-426`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 6
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 14: Works in Initial Configuration & Regional Defaults → Apply safe initial defaults using information already provided during onboarding.

#### Acceptance for the design

- [ ] Every input above is drawn (114), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (66 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-426?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Apply defaults, Save region settings.
- [ ] Every transition is wired: `ADM-419`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_MANAGE`, `PLATFORM_TENANT_VIEW`, `REGION_CONFIGURE`, `SCOPE_VIEW`, `TENANT_CONFIGURE`, `TENANT_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-427` Provisioning Validation & Exception Management

**Validate that the environment has been created correctly before handing it to customer configuration.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Tenants & Licensing · wave 3 · needs the `core` module |
| Block | Block B · task APP-CONSOLE-ADM-427 |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/tenants-licensing/provisioning-validation-exception-management-adm-427` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Validate the created environment before handing it to the customer, with exceptions to fix.

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Data it reads**: `getGoLiveReadiness` (onLoad, Provisioning outcome)

**Where the user goes next**

- → `ADM-419` Provisioning Command Center: *Back to Provisioning Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The provisioning validation exception list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the provisioning validation exception untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No provisioning validation exception yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the provisioning validation exception are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
getGoLiveReadiness (GoLiveReadiness):
- runAt: 01/10/2026 09:14
  status: active
  blockers: 12
  warnings: 12
  signedOffAt: 01/10/2026 09:14
- runAt: 30/09/2026 18:02
  status: pending
  blockers: 3
  warnings: 3
  signedOffAt: 30/09/2026 18:02
```

#### Permissions

- `getGoLiveReadiness` → `PLATFORM_TENANT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Go-live readiness validates end-to-end: products set up correctly, pricing displays correctly, and a full test transaction completes in the target environment. *(client request · MoM 10 Sep 2026, 4.14 Go-Live Readiness Validation · DI-835)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-427` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS158 Subscription Licensing AI Self Service Board 6.dc.html#adm-427`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 6
- Flow F212 *Subscription Licensing AI Self Service board 6: Provisioning Command Center*, step 16: Works in Provisioning Validation & Exception Management → Validate that the environment has been created correctly before handing it to customer configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-427?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `ADM-419`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_MANAGE`.
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

**5 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addLicenceAddOn": {"method":"POST","path":"/tenants/{tenantId}/licences/add-ons","contract":"subscription","summary":"License a module outside the plan","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LicenceAddOn","responds":"LicencePosition"},
"createOrgUnit": {"method":"POST","path":"/org-units","contract":"tenancy","summary":"Create a scope node","permission":"SCOPE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"brand","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateScopeNodeRequest","responds":"OrgUnit"},
"createPrincipal": {"method":"POST","path":"/principals","contract":"identity","summary":"Create a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePrincipalRequest","responds":"Principal"},
"createTenant": {"method":"POST","path":"/tenants","contract":"subscription","summary":"Create a tenant","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateTenantRequest","responds":"Tenant"},
"getGoLiveReadiness": {"method":"GET","path":"/go-live-readiness","contract":"subscription","summary":"Everything that must pass before a tenant can sell","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":"tenantId","in":"query","required":true}],"requestBody":null,"responds":"GoLiveReadiness"},
"getModuleEnablement": {"method":"GET","path":"/tenant-config/modules","contract":"white-label","summary":"Read module enablement","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"ModuleEnablement"},
"getRegionSettings": {"method":"GET","path":"/regions/{regionId}/settings","contract":"tenancy","summary":"Read region settings","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"RegionSettings"},
"getTenantLicences": {"method":"GET","path":"/tenants/{tenantId}/licences","contract":"subscription","summary":"What a tenant is licensed to use","permission":"PLATFORM_TENANT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"LicencePosition"},
"getVenueSettingsDefaults": {"method":"GET","path":"/venue-settings-defaults","contract":"tenancy","summary":"The tenant's default for every venue setting","permission":"TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"VenueSettings"},
"listCellJobs": {"method":"GET","path":"/cells/{cellId}/jobs","contract":"subscription","summary":"Provisioning, migration and maintenance jobs","permission":"PLATFORM_CELL_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listModuleCatalogue": {"method":"GET","path":"/module-catalogue","contract":"subscription","summary":"Modules, their dependencies and their commercial treatment","permission":"PLATFORM_PLAN_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[],"requestBody":null,"responds":"ModuleListing"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listVenueTypeTemplates": {"method":"GET","path":"/venue-type-templates","contract":"subscription","summary":"Starting configurations by venue kind","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"VenueTypeTemplate"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"runGoLiveValidation": {"method":"POST","path":"/go-live-readiness/run","contract":"subscription","summary":"Run the validation plan against a tenant","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setModuleEnablement": {"method":"PUT","path":"/tenant-config/modules","contract":"white-label","summary":"Enable or disable modules","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ModuleEnablement"},
"setPasswordPolicy": {"method":"PUT","path":"/password-policy","contract":"identity","summary":"Length, breach check, lockout and step-up","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"PasswordPolicy","responds":"PasswordPolicy"},
"setVenueSettingsDefaults": {"method":"PUT","path":"/venue-settings-defaults","contract":"tenancy","summary":"Set the tenant's default for every venue setting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"},
"updateRegionSettings": {"method":"PUT","path":"/regions/{regionId}/settings","contract":"tenancy","summary":"Update region settings","permission":"REGION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RegionSettings","responds":"RegionSettings"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"CellJob": {"x-ticvai-persistence":"control.cell_job","type":"object","required":["id","cellId","kind","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"cellId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["provision","tierMigration","schemaMigration","backup","restore","decommission"]},"status":{"type":"string","enum":["queued","running","completed","failed","rolledBack"]},"progressPercent":{"type":"integer","minimum":0,"maximum":100},"message":{"type":"string","nullable":true},"error":{"type":"string","nullable":true},"scheduledFor":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true}}},
"CreatePrincipalRequest": {"type":"object","required":["username","displayName"],"properties":{"username":{"type":"string","maxLength":256},"displayName":{"type":"string","maxLength":200},"initialCredential":{"type":"string","maxLength":512,"writeOnly":true},"mustChangeCredential":{"type":"boolean","default":true},"validTo":{"type":"string","format":"date-time"},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"CreateScopeNodeRequest": {"type":"object","required":["level","parentId","code","name"],"properties":{"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","description":"Required for every level except tenant, which the cell creates at provisioning."},"code":{"type":"string","maxLength":64,"pattern":"^[a-z0-9_]+$","description":"Becomes the final ltree segment. Immutable once created."},"name":{"type":"string","maxLength":200}}},
"CreateTenantRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["code","name","billingEmail"],"properties":{"code":{"type":"string","maxLength":64,"pattern":"^[a-z0-9-]+$"},"name":{"type":"string","maxLength":200},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500},"accountManagerPrincipalId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid"}}},
"EntitlementLimit": {"type":"object","required":["metric","limit"],"properties":{"metric":{"$ref":"#/components/schemas/UsageMetric"},"limit":{"type":"integer","nullable":true,"x-ticvai-column":"limit_value","description":"Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`."},"overageAllowed":{"type":"boolean","default":false},"overageUnitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"GoLiveReadiness": {"type":"object","x-ticvai-persistence":"subscription.go_live_readiness","description":"Board 8. **The screen that stops a launch going wrong in public.**","properties":{"tenantId":{"type":"string","format":"uuid"},"runAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["notStarted","running","blocked","readyWithWarnings","ready"]},"groups":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["ticketingAndProducts","salesChannels","payment","ticketQrAccess","usersAndSecurity","integrations","communications","financialSetup"]},"label":{"type":"string"},"checks":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"outcome":{"type":"string","enum":["pass","warn","fail","skipped"]},"detail":{"type":"string","nullable":true},"remediation":{"type":"string","nullable":true}}}}}}},"blockers":{"type":"integer"},"warnings":{"type":"integer"},"signedOffBy":{"type":"string","format":"uuid","nullable":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true}}},
"LicenceAddOn": {"x-ticvai-persistence":"control.licence_add_on + control.licence_add_on_limit","x-ticvai-retired-columns":["plan_id"],"description":"**Belongs to the tenant, not the plan.** Add-ons survive a plan change unless explicitly removed (`addLicenceAddOn`), so a row keyed on `plan_id` would be lost, or silently re-applied to every tenant on that plan, at the first plan change. The tenant comes from the path. `limitOverrides` are child rows in `control.licence_add_on_limit`.","type":"object","required":["moduleKey"],"properties":{"tenantId":{"type":"string","format":"uuid","readOnly":true,"description":"The tenant the add-on was sold to — the `tenantId` in the path, never the body."},"moduleKey":{"type":"string"},"limitOverrides":{"type":"array","items":{"$ref":"#/components/schemas/EntitlementLimit"}},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"validFrom":{"type":"string","format":"date"},"validTo":{"type":"string","format":"date","nullable":true},"note":{"type":"string","maxLength":500}}},
"LicencePosition": {"x-ticvai-persistence":"none — union of the tenant's plan (control.tenant.plan_id -> subscription.plan_module, subscription.plan_limit) and its add-ons (control.licence_add_on, control.licence_add_on_limit by tenant_id)","type":"object","required":["tenantId","licensedModules","limits"],"properties":{"poweredByRemovable":{"type":"boolean","readOnly":true,"default":false,"description":"**Whether the tenant's licence lets it switch \"Powered by TICVAI\" off** (Chinmay, 2 October, workbook Q160 and the pre-apply round; CHG-CSA-036). False by default; true where TICVAI sold the tenant the add-on keyed `poweredByRemoval` (`addLicenceAddOn`). White label's `setBrandIdentity` refuses `showPoweredBy` false while this is false."},"tenantId":{"type":"string","format":"uuid"},"planId":{"type":"string","format":"uuid","nullable":true},"licensedModules":{"type":"array","description":"Union of plan modules and add-ons. The White Label Builder reads this and cannot enable anything absent from it.\n","items":{"type":"object","required":["moduleKey","source"],"properties":{"moduleKey":{"type":"string"},"displayName":{"type":"string"},"source":{"type":"string","enum":["plan","addOn"]},"validTo":{"type":"string","format":"date","nullable":true}}}},"limits":{"type":"array","items":{"$ref":"#/components/schemas/EntitlementLimit"}}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"ModuleEnablement": {"x-ticvai-persistence":"whitelabel.module_enablement","type":"object","required":["moduleKey","isLicensed","isEnabled"],"properties":{"moduleKey":{"$ref":"#/components/schemas/ModuleKey"},"displayName":{"type":"string"},"isLicensed":{"type":"boolean","description":"From the tenant's subscription. False makes enablement impossible."},"isEnabled":{"type":"boolean"},"referencedBy":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write.","items":{"type":"string"}}}},
"ModuleKey": {"$ref":"../shared/common.yaml#/components/schemas/ModuleKey"},
"ModuleListing": {"type":"object","x-ticvai-persistence":"subscription.module_listing","description":"Board 4.6. **A marketplace without a dependency graph sells combinations that cannot be provisioned.**\n**TICVAI configures each module's price here, and tenants are billed per module (decided 29 September, Chinmay).** A usage-priced module (the AI module's tokens) has `pricingBasis` `metered`: `price` is then per `meteredUnitSize` units of `meteredMetric`, and the invoice carries it as a `metered` line.\n","required":["moduleCode"],"properties":{"moduleCode":{"type":"string"},"name":{"type":"string"},"description":{"type":"string","nullable":true},"category":{"type":"string","nullable":true},"requiresModules":{"type":"array","items":{"type":"string"}},"incompatibleWithModules":{"type":"array","items":{"type":"string"}},"includedInTiers":{"type":"array","items":{"type":"string"}},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money"},"pricingBasis":{"type":"string","enum":["included","flatFee","perVenue","perUnit","revenueShare","metered"]},"meteredMetric":{"allOf":[{"$ref":"#/components/schemas/UsageMetric"}],"nullable":true,"description":"For `metered`, what is counted (`aiTokens` for the AI module). Null otherwise."},"meteredUnitSize":{"type":"integer","minimum":1,"nullable":true,"description":"For `metered`, how many units `price` buys (e.g. 1000 tokens). Null otherwise."},"provisioningMinutes":{"type":"integer","nullable":true},"requiresProfessionalServices":{"type":"boolean","default":false},"status":{"type":"string","enum":["available","beta","deprecated","withdrawn"]}}},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"PasswordPolicy": {"type":"object","x-ticvai-persistence":"identity.password_policy","description":"BL-144. **Written by `setPasswordPolicy`, which returns it**, at tenant scope. Before BL-144 the package had no password policy, no lockout and no forced change at first logon anywhere.\n**Modelled on NIST SP 800-63B rather than on habit.** Length beats composition, and forced rotation on a schedule makes passwords worse — people increment a digit. Rotation is here because some tenants are contractually required to have it, **not because it helps.**\n","required":["id","scopePath","minLength"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"Assigned by the server. Required in the response only; ignored if a request sends it."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005), written by the server from the caller's tenant (`x-ticvai-config-scope: tenant`). Required in the response only; ignored if a request sends it."},"minLength":{"type":"integer","default":12,"minimum":8,"description":"A tenant may raise the length and never set it below 8 (decided 28 September, audit R126 (7))."},"requireBreachCheck":{"type":"boolean","default":true,"description":"**The single most effective rule.** Refusing a password known to be breached stops more account takeovers than every composition rule combined.\n"},"maxAgeDays":{"type":"integer","nullable":true,"description":"**Null is the recommended value.** Forced rotation produces `Summer2026!` becoming `Summer2027!`, and it is offered because some tenants are contractually obliged to have it rather than because it works.\n"},"recoveryMethods":{"type":"array","description":"BL-132. **A guest locked out had no path back** — lockout existed and recovery did not, which turns a forgotten password into a support call.\n**Ordered by strength, and the venue chooses which it offers.** Email is weakest and universal; a verified phone is stronger; an in-person check at a desk is strongest and only available to a guest who is already at the venue.\n","items":{"type":"string","enum":["email","sms","securityQuestions","inPersonVerification","supportAssisted"]}},"maxConcurrentSessions":{"type":"integer","nullable":true,"description":"BL-145. **Null, and that is the decision.** A staff principal has one live session, full stop: ADR-0004 keeps a server-side session registry (the `sid` claim, `ActiveSession`), and §3.1.3 refuses a second sign-in rather than counting towards a limit (confirmed 28 September, audit R184). A number here would only ever mean 1.\nThe requirement asked for it configurable. **Configurable to null is still an answer.**\n"},"deviceRestriction":{"type":"object","nullable":true,"description":"BL-146. **Device, browser, IP and location restriction on access.** Applies to staff principals, not guests — a guest restricted to one device is a guest who cannot use their new phone.\n**Warn before block by default.** An IP restriction that blocks silently is a venue manager locked out on the day their ISP rotates an address.\n","properties":{"allowedIpRanges":{"type":"array","items":{"type":"string"}},"allowedCountries":{"type":"array","items":{"type":"string"}},"requireRegisteredDevice":{"type":"boolean","default":false},"onViolation":{"type":"string","enum":["warn","requireStepUp","block"],"default":"requireStepUp"}}},"lockoutAfterAttempts":{"type":"integer","default":10},"lockoutMinutes":{"type":"integer","default":15,"description":"**A temporary lockout, not a permanent one.** Permanent lockout on failed attempts is a denial-of-service anybody can run against a known username.\n"},"forceChangeOnFirstLogon":{"type":"boolean","default":true},"reusePreventionCount":{"type":"integer","default":5,"minimum":0,"maximum":24,"description":"**How many previous credentials a staff member may not reuse** — the last 5 unless the tenant sets another (decided 28 September, audit R132). `changeOwnCredential` refuses a match with `422`.\n"},"mfaRequiredForPermissions":{"type":"array","description":"**Step-up rather than blanket MFA.** Requiring it for a refund approval and not for reading a rota is what stops people sharing devices to avoid it.\n**MFA is required by permission, not by role** (decided 28 September, audit R135). A principal holding any permission listed here must keep an active method (`removeMfaMethod` refuses to remove the last one). **The default is the platform floor**: `ROLE_MANAGE`, `LEDGER_APPROVE` and every `PLATFORM_*` permission. A tenant may add to the list and never remove a floor entry; a body that drops one is refused `400`.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"},"default":["ROLE_MANAGE","LEDGER_APPROVE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_TENANT_ACCESS","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY"]}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"Placement": {"x-ticvai-persistence":"none — embedded in region_settings","type":"object","description":"Read-only here. Set by the Control Plane at provisioning.\nEvery region is its own logical cell. Placement determines the infrastructure backing it, which is how cost is controlled without varying the split rule: `shared` puts several regions' databases on one cluster; `dedicated` and `isolated` give a region its own. Regions in different countries MUST have placements in their respective jurisdictions.\n","readOnly":true,"required":["mode"],"properties":{"mode":{"type":"string","enum":["shared","dedicated","isolated","clientHosted"]},"cellName":{"type":"string"},"cloudRegion":{"type":"string"}}},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"RegionSettings": {"x-ticvai-persistence":"platform.region_settings","type":"object","required":["countryCode","currencyCode","currencyScale","timeZone","fiscalYearStartMonth"],"properties":{"countryCode":{"type":"string","pattern":"^[A-Z]{2}$","description":"ISO 3166-1 alpha-2. Determines the jurisdiction, and therefore the cell."},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"description":"Decimal places for this region's currency. Varies by currency — some use 2, some use 3. Money columns are numeric(18,4) and carry the scale explicitly, because a fixed 2-place type silently truncates 3-place currencies.\n"},"timeZone":{"type":"string","description":"IANA zone, e.g. `Asia/Dubai`."},"dateFormat":{"type":"string","default":"dd/MM/yyyy"},"numberFormat":{"type":"string","default":"#,##0.00"},"fiscalYearStartMonth":{"type":"integer","minimum":1,"maximum":12,"description":"Varies by country."},"allowedAiResidencies":{"type":"array","description":"**The region's compliance gate on AI providers** (decided 28 September, audit R203; ADR-0009). The `AiProvider.residency` values a tenant in this region may use; empty means no restriction. `ai.setAiProvider` refuses any other residency with `409 residency-refused`. A prompt carrying guest data that reaches a provider hosted elsewhere is a cross-border transfer, and this is where a region says which it allows.\n**Derived from `aiResidencyClass` since 2 October 2026** (CHG-CSP-009): the class names the residencies, and this list narrows them further where a region needs it; it never widens them.\n","default":[],"items":{"type":"string"}},"aiResidencyClass":{"type":"string","enum":["uaeOnly","globalAllowed","onPrem"],"default":"uaeOnly","description":"**The tenant's AI residency class** (decided 2 October 2026, Chinmay, \"AI residency: per-tenant residency class\"; DEC-539; CHG-CSP-009; amends AI-D02 and ADR-0009 section 1). Which AI endpoints the AI engine may route this tenant's calls to:\n- `uaeOnly` (the default, and mandatory for government, bank and health tenants): the small tier\n  is Core42 Compass GPT-4.1 mini (or Seraj if it wins the Arabic golden set), the strong tier\n  Compass GPT-5, reached through `AiProviderKind` `openaiCompatible`; fallback OpenAI UAE (no\n  in-cell model: we host none unless a client asks, CHG-R1S-002). No call leaves the UAE.\n- `globalAllowed`: a private venue that opts in under PDPL Article 23, with a vendor contract, a\n  DPIA and a notice to guests (`aiResidencyOptIn`). Azure gpt-5-mini and gpt-6-sol Global, or\n  the tenant's BYOK provider; fallback the `uaeOnly` chain. The tenant is listed in ADR-0009's\n  transfer register.\n- `onPrem`: models in the tenant's own estate (Qwen3.5 or gpt-oss; strong tier Qwen3.5-122B,\n  Falcon-H1 Arabic or Jais 2), only where the client asks for it (CHG-R1S-002).\n\n**Every LLM call is scrubbed of personal data in-cell first, whatever the class** (DEC-542): the class decides where a call may go, never whether personal data may travel. Moving from `uaeOnly` to `globalAllowed` without `aiResidencyOptIn` is refused `422 residency-opt-in-required`; on a tenant `aiResidencyClassLocked` holds, any change is refused `409 residency-class-locked`. The model choice per class is the AI engine's (ai `AiProvider`, ai-system-design 3.3), not a setting here.\n"},"aiResidencyClassLocked":{"type":"boolean","readOnly":true,"default":false,"description":"**Set by TICVAI at onboarding for a government, bank or health tenant** (DEC-539), which must stay `uaeOnly`. Read-only to the tenant.\n"},"tenantCategory":{"type":"string","readOnly":true,"default":"private","enum":["private","semiGovernment","government","banking","payments","health","difc","adgm"],"description":"**What kind of organisation the tenant is, for AI residency** (3 October 2026, CHG-R1S-016; the legal research `docs/active/research/openai-key-uae-3-october.md`, item 2, and Chinmay's per-tenant residency class, DEC-539). Recorded by TICVAI staff at onboarding, read-only to the tenant. **Only `private` may take `globalAllowed`**: a government or semi-government entity (DESC, ADISS and TDRA scope), a bank or payments firm, a health provider, or a DIFC or ADGM entity stays `uaeOnly` (or `onPrem` where it asks), and `updateRegionSettings` refuses the change `409 residency-category-refused`, naming the category. `aiResidencyClassLocked` stays as the per-tenant override TICVAI can set on any category.\n"},"aiResidencyOptIn":{"type":"object","nullable":true,"description":"**The evidence a `globalAllowed` opt-in needs under PDPL Article 23** (DEC-539; CHG-CSP-009): the tenant's references to its vendor contract, its DPIA and the notice guests see. The platform records that they were named, by whom and when; it does not hold or judge the documents. Null while the class is `uaeOnly` or `onPrem`.\n","properties":{"vendorContractReference":{"type":"string","maxLength":200},"dpiaReference":{"type":"string","maxLength":200},"guestNoticeReference":{"type":"string","maxLength":200},"confirmedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"confirmedAt":{"type":"string","format":"date-time","readOnly":true}}},"localLanguageNameLocales":{"type":"array","default":[],"description":"**The languages an outlet name must also be given in, in this country** (decided 2 October 2026, Chinmay, batch 2 #26: \"English plus the local language where the country needs it\"; DEC-031; CHG-CSP-005). ISO 639-1 codes; `[ar]` in the UAE. Empty asks for English only. `createOutlet` and `updateOutlet` refuse an outlet whose `nameTranslations` lacks one of them (`422 local-name-required`).\n","items":{"type":"string","pattern":"^[a-z]{2}$"}},"requiredBillingDocuments":{"x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","type":"array","description":"**Which documents a TICVAI customer's billing entity must upload, in this country** (decided 2 October 2026, Chinmay, batch 6 set 7, ADM-411: \"Trade licence always; VAT certificate when a TRN is entered; configurable per country\"; DEC-210; CHG-CSP-008). The default for every country is the two rows below; TICVAI staff change them per country. The subscription contract's billing entity and `PartnerDocument` read this list; a missing required document holds the entity in verification.\n","default":[{"documentType":"tradeLicence","requiredWhen":"always"},{"documentType":"vatCertificate","requiredWhen":"trnEntered"}],"items":{"type":"object","properties":{"documentType":{"type":"string","maxLength":64,"description":"The document kind, as the subscription contract's `PartnerDocument` names it (`tradeLicence`, `vatCertificate`, ...)."},"requiredWhen":{"type":"string","enum":["always","trnEntered"]}}}},"minorAgeThreshold":{"type":"integer","minimum":0,"maximum":21,"default":18,"description":"**The age below which a guest is a minor here, set per country** (decided 2 October 2026, Chinmay, critical set 1, BO-187: \"Guardian consent on the venue's form; minor age per country\"; DEC-237; CHG-CSP-019). A minor's biometric enrolment needs a guardian's consent on the venue's consent form (access `enrolFacePass`, `consent.guardianSubjectId`); a subject with no date of birth is treated as a minor (audit R126). The default 18 is the UAE's age of majority and is marked for counsel to confirm per country (R205); whether minors may enrol at all is the venue's switch (`VenueSettings.biometrics.allowMinors`).\n"},"placement":{"$ref":"#/components/schemas/Placement"},"cellName":{"type":"string","readOnly":true,"description":"The cell serving this region. One cell per tenant per region (ADR-0014).\n"}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"ScopeLevel": {"type":"string","description":"**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n","enum":["tenant","brand","region","venue","department","subDepartment","workstation","outlet","subject"]},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]},
"UsageMetric": {"type":"string","enum":["venues","workstations","activeUsers","devices","brandedApps","aiTokens","apiCalls","storageGb","transactions","guestProfiles"]},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's own consent form, which every biometric capture is taken on** (decided 2 October 2026, Chinmay, batch 4, BO-188: \"Consent first, on the venue's consent form\"; DEC-128, DEC-549; CHG-CSP-018). A form from the venue's consent-form builder in Venue Management (the one builder Face Pass, Face Tag, marketing and waivers share; marketing-crm `setDigitalWaiverForm`). Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access `enrolFacePass`, `enrolFaceTag`).\n"},"templatesHeldByTicvai":{"type":"boolean","readOnly":true,"description":"**True where TICVAI's platform stores this venue's biometric templates** (rather than the venue's own on-premises reader estate). Derived from the venue's access deployment. While true, Venue Management shows the venue a standing warning that every guest must accept the venue's consent form before capture, because the data sits with TICVAI as the venue's processor (decided 2 October 2026, Chinmay, batch 4, BO-188: \"If we store the data, highlight or notify the venue that the client must accept a consent form\"; DEC-128; CHG-CSP-018).\n"},"allowMinors":{"type":"boolean","default":true,"description":"**Whether this venue enrols minors at all** (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: \"Guardian consent on the venue's form; minor age per country; the venue can switch minors off\"; supersedes the GST-069 default; DEC-237; CHG-CSP-019). On: a minor (below `RegionSettings.minorAgeThreshold`) is enrolled only with a guardian's consent on the venue's consent form. Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method.\n"},"accreditationFaceMatching":{"type":"object","nullable":true,"description":"**Face matching to find duplicate accreditation applicants, off unless the venue enables it** (decided 2 October 2026, Chinmay, critical set 3, BO-631: \"Only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default\"; DEC-461; CHG-CSP-022). Enabling it is refused without `legalSignOffReference` (`422 legal-sign-off-required`); each applicant matched must have consented on the application (accreditation's own record). Null is off.\n","properties":{"isEnabled":{"type":"boolean","default":false},"legalSignOffReference":{"type":"string","nullable":true,"maxLength":200,"description":"The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"chargeCurrencies":{"type":"array","nullable":true,"description":"**Which currencies a guest may select and pay in** (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). A subset of `displayCurrencies`: each code must also be one the venue's payment provider can charge (`orders.PaymentProvider.presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. Null or empty: guests pay in the trading (base) currency only and the other display currencies stay approximate. The ledger is always in the base currency, with the rate recorded on every payment and refund.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The most cash a till drawer should hold before some is lifted to the safe** (decided 2 October 2026, Chinmay, batch 6 set 3, BO-042: \"Add drawer limit setting (warn + offer cash lift)\"; DEC-179; CHG-CSP-016; DI-274: on a busy day the cashier unloads excess cash mid-shift and it is reconciled at close). The venue default; a till may set its own (`Workstation.cashDrawerLimit`). When the cash a till has taken since its last count takes the drawer over it, the till warns and offers a cash lift (`shift.createCashMovement` kind `lift`) and BO-042 flags the box (`shift.DepositBox.overDrawerLimit`). A warning, never a block: a sale is not refused because the drawer is full. Null sets no limit. **No proposed default: the client's finance team sets it.**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"tableReservedLeadMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":240,"default":30,"deprecated":true,"description":"**Deprecated (2 October 2026, CHG-CLN-009): `fnb.FnbReservationPolicy.reservedLeadMinutes` is canonical.** The table state model reads the reservation policy (`states/table.yaml`); this venue setting is kept for compatibility, never read, and not drawn. Its former meaning: **How long before a pre-allocated booking its table shows Reserved** (decided 2 October 2026, Chinmay, batch 6 set 6b, EMP-052: \"Reserved when a booking names the table, or N minutes (venue-set) before a pre-allocated booking\"; DEC-202; CHG-CSP-017; DI-689, DI-336). A booking that names its table holds it as Reserved for the booking's whole slot; a booking the host pre-allocated shows its table Reserved from this many minutes before it. Zero shows Reserved only once the booking is due. The fnb table state model applies it (`states/table.yaml`, owned by fnb). Proposed default 30 minutes, client to correct.\n"},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"VenueTypeTemplate": {"type":"object","x-ticvai-persistence":"control.venue_type_template","description":"BL-165. **What a venue of this kind starts with.** Product kinds, price list structure, access profiles, roles, report set.\n**A template is a starting point and not a constraint** — everything it creates is editable the moment it lands, which is the difference between a template and a plan tier.\n","required":["id","name","venueKind"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"venueKind":{"type":"string","enum":["themePark","waterPark","museum","theatre","stadium","arena","zoo","aquarium","cinema","attraction","mixed"]},"seedsProductKinds":{"type":"array","items":{"type":"string"}},"seedsRoles":{"type":"array","items":{"type":"string"}},"seedsAdmissionProfiles":{"type":"array","items":{"type":"string"}},"seedsReports":{"type":"array","items":{"type":"string"}}}}
}
```
