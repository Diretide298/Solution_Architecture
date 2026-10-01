# P06-operations-01 — P06 · Operations (1 of 5)

**10 screens · 57 operations · 62 schemas · 26 permissions**

Platform P06 Venue Staff App · ships as **venue-staff-mobile** ·
staff audience · mobileApp ·
offline-capable

## Who this is for

**staff on mobileApp.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 26 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, ANNOUNCEMENT_PUBLISH, CASH_LIFT, CASH_NO_SALE, INCIDENT_MANAGE, INCIDENT_REPORT, INCIDENT_VIEW, MAINTENANCE_APPROVE, MAINTENANCE_EXECUTE, OVERSHORT_ACCEPT, PROCUREMENT_REQUEST`…. A control nobody can use must say so,
  not sit enabled and fail.
- **28 of these operations work offline**: acceptWorkOrder, acknowledgeAnnouncement, attachWorkOrderEvidence, completeWorkOrder, createCashMovement, createWorkOrder, getCurrentSession, getCurrentShift
  — and the rest do not. A surface that looks the same online and off is lying.
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
| `EMP-001` | Sign in | B–D | 10 | 33 | 6 | 4 | 3 | 0 | — | notStarted (generated) |
| `EMP-002` | Select venue & role | B–D | 1 | 42 | 6 | 3 | 1 | 5 | — | notStarted (generated) |
| `EMP-003` | Home — on duty | B–D | 70 | 100 | 6 | 16 | 3 | 0 | — | notStarted (generated) |
| `EMP-009` | End shift | B–D | 57 | 69 | 6 | 6 | 1 | 6 | — | notStarted (generated) |
| `EMP-010` | Scan — ready | B–D | 37 | 35 | 6 | 61 | 1 | 0 | — | notStarted (generated) |
| `EMP-004` | Task list | B–D | 45 | 44 | 6 | 24 | 6 | 0 | — | notStarted (generated) |
| `EMP-005` | Task detail | B–D | 54 | 47 | 6 | 24 | 4 | 0 | — | notStarted (generated) |
| `EMP-006` | Raise a task | B–D | 63 | 44 | 6 | 33 | 4 | 0 | — | notStarted (generated) |
| `EMP-007` | Handover notes | B–D | 12 | 29 | 6 | 4 | 0 | 0 | — | notStarted (generated) |
| `EMP-008` | Shift summary | B–D | 6 | 56 | 6 | 1 | 0 | 6 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `EMP-001` Sign in

**Get an employee onto a shared device fast.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listMfaMethods` reads the population and `getCurrentSession` reads one of them — list, select, act |
| Offline | Signs in against the cached principal list. A technician in a basement still needs their tasks |
| Opens with | `challengeId` (navigation) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/operations/sign-in` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Sign in.** A shared device between shifts shows nothing until somebody identifies themselves. **Declared 20 August** — `isEntryPoint` existed in the schema and five platforms used none, so every screen in them read as unreachable. **Removed 24 August**: forceLogout, listActiveSessions, revokeAllSessions. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**

**Known gaps.** **1 declared operation reaches no component on this screen**: listSsoProviders. Either the screen is missing what calls them, or the declaration is residue.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Authentication code | text field | — | — | — | — | Shown only in the mfaRequired state (audit R135). | — |

**Form: Login** (modal, opened by *Login*; *Login* calls `login`, *Cancel* sends nothing)

**Collects what `login` sends before it is called.** Required: `username`, `credential`, `workstationId`. Optional: `method`, `deviceFingerprint`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Username `username` | text area | required | — | max length 256 | — | — | `login` body |
| Credential `credential` | text area | required | — | max length 512 | — | Password, PIN, card token or RFID token depending on `method`. | `login` body |
| Method `method` | radio group | optional | Password | Password · PIN · Card · RFID · Sso | — | `pin` is how a till is actually used. A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets … | `login` body |
| Workstation `workstationId` | picker: choose a workstation | required | — | — | shows names, sends the id | Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. | `login` body |
| Device fingerprint `deviceFingerprint` | text area | optional | — | max length 256 | — | — | `login` body |

Errors to draw in the form: 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused.

**Sent by *Verify*** (`verifyMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `verifyMfaChallenge` body |

**Sent by *Email me a code instead*** (`createMfaChallenge`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every MFA method** (data table, from `listMfaMethods`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |

**Every SSO provider** (data table, from `listSsoProviders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Display name | text | — |
| Protocol | chip: Oidc, Saml2 | — |
| Icon | the image or video | — |
| Is enforced | yes / no (icon or chip) | True disables password login for principals covered by this provider. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected MFA method** (detail panel, from `listMfaMethods`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |

**The session** (detail panel, from `getCurrentSession`)

| Shows | Format | Notes |
|---|---|---|
| Session | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Role | the name it points at, never the id | — |
| Display name | text | — |
| Scope | list or chips (count when long) | Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. |
| Effective permissions | list or chips (count when long) | Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. |
| Permissions by scope | list or chips (count when long) | Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves. |
| Sale board | the name it points at, never the id | Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board. |
| Workstation | grouped details | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Login (primary button) | `login` POST `/auth/login` | LoginRequest | LoginResponse | 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused. | opens modal first |
| Verify (primary button) | `verifyMfaChallenge` POST `/auth/mfa/challenge/{challengeId}/verify` | inline | inline | — | — |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |

**Data it reads**: `getCurrentSession` (onLoad, Current session and effective permissions); `listMfaMethods` (onLoad, Enrolled MFA methods); `listSsoProviders` (onLoad, Identity providers configured for this tenant)

**Where the user goes next**

- → `EMP-002` Select venue & role: *Selects venue and role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-048` Opening checklist: *Opening checklist*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sign list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sign untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sign yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listMfaMethods` takes no filter, so an empty list is always the first-run state above. |
| MFA required (`?state=mfaRequired`) | **Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any platform-staff permission, or one the tenant added), so after `login` the screen calls `createMfaChallenge` and asks for the authenticator code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says so. A principal with no enrolled method is sent to enrol first … |
| Offline (`?state=offline`) | Signs in against the cached principal list. A technician in a basement still needs their tasks |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused. |

#### Permissions

- `login` → no permission · anonymous, partner
- `getCurrentSession` → no permission · staff, partner
- `listMfaMethods` → no permission · staff, partner, guest
- `listSsoProviders` → no permission · anonymous, partner
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.5 | The system should have the option to be used by several waiters at the same time. | F&B & Guest Management | CONTRACTED | `login` |
| 5.8.2 | The system should only allow one session per user. | F&B & Guest Management | CONTRACTED | `login` |
| 3.3.28 | Authorization Caching - System shall support caching of authorization decisions. | Admission and Access | CONTRACTED | `getCurrentSession` |
| 7.1.50 | Cache authorization decisions securely to improve performance while ensuring policy changes invalidate outdated cache entries. | F&B POS | CONTRACTED | `getCurrentSession` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Employee app login by username/password or SSO. *(client request · MoM 10 Aug 2026, 5.1 Login, Roles & Dashboard · DI-225)*
- A user can hold several roles and switch between them at login (e.g. cashier vs supervisor). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-152)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-001` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 1: Signs in → Biometric or SSO
- Flow F64 *A steward signs in and takes a venue and a role*, step 1: They sign in. → **SSO where the venue uses it, MFA where the role demands it.** A gate steward and a finance controller do not need the same ceremony.
- Flow F64 branch at step 1 (high): when MFA is required and the phone is in a locker., **Refused, and the venue has a policy problem rather than a platform one.** A bypass here is a bypass for everybody.

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (33 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, mfaRequired, offline.
- [ ] Every action is wired with its success and its failure: Login, Verify, Email me a code instead.
- [ ] Every transition is wired: `EMP-002`, `EMP-003`, `EMP-048`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-002` Select venue & role

**Confirm which hat this person is wearing today.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ROLE_MANAGE` (1 configure); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listMfaMethods` reads the population and `getCurrentSession` reads one of them — list, select, act |
| Offline | Cached from the last session |
| Opens with | `sessionId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/operations/select-venue-role` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createRole, forceLogout, listActiveSessions, revokeAllSessions. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.** ** restored** — a role-select screen must read the roles. Over-stripped and caught by F08.

#### Inputs: what the user enters or picks

**Form: Select role** (modal, opened by *Select role*; *Select role* calls `selectRole`, *Cancel* sends nothing)

**Collects what `selectRole` sends before it is called.** Required: `roleId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Role `roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `selectRole` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Every MFA method** (data table, from `listMfaMethods`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |

**Every SSO provider** (data table, from `listSsoProviders`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Display name | text | — |
| Protocol | chip: Oidc, Saml2 | — |
| Icon | the image or video | — |
| Is enforced | yes / no (icon or chip) | True disables password login for principals covered by this provider. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Every role** (data table, from `listRoles`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | Unique within the tenant (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. |
| Name | text | — |
| Description | text | — |
| Permissions | list or chips (count when long) | A role that grants no permissions is not a role. `Role` carried a code, a name and two counts until 18 August, and … |
| Inherits from role | the name it points at, never the id | Role composition, one level deep and no deeper. A supervisor role that is a cashier plus three permissions is how venues actually describe … |
| Is system | yes / no (icon or chip) | Seeded roles ship and are editable; deleting one is refused. A venue that removes `cashier` and rebuilds it has two roles with one name in … |
| Principal count | 1,234 | — |
| Grant count | 1,234 | — |

**The selected MFA method** (detail panel, from `listMfaMethods`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |

**The session** (detail panel, from `getCurrentSession`)

| Shows | Format | Notes |
|---|---|---|
| Session | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Role | the name it points at, never the id | — |
| Display name | text | — |
| Scope | list or chips (count when long) | Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. |
| Effective permissions | list or chips (count when long) | Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. |
| Permissions by scope | list or chips (count when long) | Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves. |
| Sale board | the name it points at, never the id | Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board. |
| Workstation | grouped details | — |
| Opened at | 1 Oct 2026, 14:30 | — |
| Expires at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Select role (primary button) | `selectRole` POST `/auth/select-role` | inline | Session | 403 Authenticated but not permitted at the requested scope | opens modal first |

**Data it reads**: `getCurrentSession` (onLoad, Current session and effective permissions); `listMfaMethods` (onLoad, Enrolled MFA methods); `listSsoProviders` (onLoad, Identity providers configured for this tenant); `listRoles` (onLoad, Roles this principal may take)

**Where the user goes next**

- → `EMP-048` Opening checklist: *Works the opening checklist*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The select venue role list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the select venue role untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No select venue role yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listMfaMethods` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ROLE_MANAGE`, which `listRoles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cached from the last session |

#### Permissions

- `selectRole` → no permission · staff
- `getCurrentSession` → no permission · staff, partner
- `listMfaMethods` → no permission · staff, partner, guest
- `listSsoProviders` → no permission · anonymous, partner
- `listRoles` → `ROLE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ROLE_MANAGE`, which `listRoles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.4 | The system should be able to have a login override option for the supervisor level in order to login to the POS if the need arises and the previous user has not logged out. | F&B POS | CONTRACTED | `selectRole` |
| 3.3.28 | Authorization Caching - System shall support caching of authorization decisions. | Admission and Access | CONTRACTED | `getCurrentSession` |
| 7.1.50 | Cache authorization decisions securely to improve performance while ensuring policy changes invalidate outdated cache entries. | F&B POS | CONTRACTED | `getCurrentSession` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-002` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 2: Selects venue and role → A person may hold several roles; the shift needs one
- Flow F64 *A steward signs in and takes a venue and a role*, step 2: They pick a venue and a role for the shift. → **One person, several roles, one at a time** (ADR-0002). A supervisor covering a lane takes the steward role and loses the supervisor one until they change back.
- Flow F08 branch at step 2 (requiresStaff): when Emergency declared, EMP-047 emergency mode overrides the home screen entirely. This is the one screen that outranks everything.
- Flow F64 branch at step 2 (medium): when The principal has no role at this venue., Refused at role select, not at first action. **A person who signs in and then cannot do anything has been told the wrong thing.**
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Select role.
- [ ] Every transition is wired: `EMP-048`, `EMP-001`, `EMP-003`.
- [ ] Every gated control is gated: `ROLE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-003` Home — on duty

**The screen the device sits on between tasks.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASH_NO_SALE`, `INCIDENT_MANAGE`, `INCIDENT_REPORT`, `INCIDENT_VIEW`, `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`… (9 operate, 1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | approvalInbox (comfortable density): `approveShiftOpen` decides items that `listIncidents` queues — every row is waiting for a person, so the empty state is success |
| Offline | Last synced view, with its age. The pending count is always current because it is local |
| Opens with | `incidentId` (deepLink), `shiftId` (session) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/home-on-duty` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **createCashMovement removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Severity | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | Sends `?severity=` to `listIncidents`. | `listIncidents` ?severity |
| Status | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | Sends `?status=` to `listIncidents`. | `listIncidents` ?status |
| Is reportable | toggle | optional | — | — | — | Sends `?isReportable=` to `listIncidents`. | `listIncidents` ?isReportable |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listShifts` ?workstationId |
| Status | select | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | `listShifts` ?status |
| Opened from | date and time picker | — | — | `listShifts` ?openedFrom |
| Opened to | date and time picker | — | — | `listShifts` ?openedTo |

**Form: Accept shift variance** (modal, opened by *Accept shift variance*; *Accept shift variance* calls `acceptShiftVariance`, *Cancel* sends nothing)

**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | Retained for audit. The accepting principal is recorded. | `acceptShiftVariance` body |

Errors to draw in the form: 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type `shift-not-pending-variance`) — within tolerance, still open, or already accepted.

**Form: Approve shift open** (modal, opened by *Approve shift open*; *Approve shift open* calls `approveShiftOpen`, *Cancel* sends nothing)

**Collects what `approveShiftOpen` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | — | `approveShiftOpen` body |

Errors to draw in the form: 409 Shift is not `pendingApproval` (problem type `shift-not-awaiting-approval`)

**Form: Open shift** (modal, opened by *Open shift*; *Open shift* calls `openShift`, *Cancel* sends nothing)

**Collects what `openShift` sends before it is called.** Required: `workstationId`, `openingFloat`. Optional: `depositBoxCode`, `bagNumber`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Workstation `workstationId` | picker: choose a workstation | required | — | — | shows names, sends the id | — | `openShift` body |
| Opening float `openingFloat` | repeatable rows | required | — | at least 1 | — | A count is a list of lines and the line is the row. Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — … | `openShift` body |
| ID `openingFloat[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `openShift` body |
| Shift `openingFloat[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `openShift` body |
| Deposit box `openingFloat[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `openShift` body |
| Count kind `openingFloat[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `openShift` body |
| Cash movement `openingFloat[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `openShift` body |
| Denomination `openingFloat[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `openShift` body |
| Counted quantity `openingFloat[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `openShift` body |
| Counted value `openingFloat[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `openShift` body |
| Counted by `openingFloat[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `openShift` body |
| Counted at `openingFloat[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `openShift` body |
| Recount of `openingFloat[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `openShift` body |
| Deposit box code `depositBoxCode` | text field | optional | — | max length 64 | — | Physical container assigned to this shift. Required where the venue configures deposit box allocation. | `openShift` body |
| Bag number `bagNumber` | text field | optional | — | max length 64 | — | Required where the venue configures bag numbers as mandatory. | `openShift` body |
| Recorded at `recordedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the device recorded it. `openShift` is online-only (F32), so this differs from server receipt time only by transit; it is kept because the shift's other device writes are … | `openShift` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent (`required-device-absent`).

**Form: Record authority notification** (modal, opened by *Record authority notification*; *Record authority notification* calls `recordAuthorityNotification`, *Cancel* sends nothing)

**Collects what `recordAuthorityNotification` sends before it is called.** Required: `authority`, `notifiedAt`. Optional: `reference`, `notifiedByPrincipalId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Authority `authority` | text field | required | — | max length 200 | — | — | `recordAuthorityNotification` body |
| Reference `reference` | text field | optional | — | max length 128 | — | — | `recordAuthorityNotification` body |
| Notified at `notifiedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordAuthorityNotification` body |
| Notified by principal `notifiedByPrincipalId` | picker: choose a notified by principal | optional | — | — | shows names, sends the id | — | `recordAuthorityNotification` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `recordAuthorityNotification` body |

Errors to draw in the form: 409 The incident is not reportable (`isReportable` false, audit R106 (6)).

**Form: Record no sale** (modal, opened by *Record no sale*; *Record no sale* calls `recordNoSale`, *Cancel* sends nothing)

**Collects what `recordNoSale` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordNoSale` body |
| Reason `reason` | radio group | required | — | Change for guest · Correct float · Retrieve dropped cash · Till check · Other | — | — | `recordNoSale` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `recordNoSale` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordNoSale` body |

Errors to draw in the form: 409 Shift is not open (problem type `shift-not-open`)

**Form: Reopen shift** (modal, opened by *Reopen shift*; *Reopen shift* calls `reopenShift`, *Cancel* sends nothing)

**Collects what `reopenShift` sends before it is called.** Required: `reason`, `supervisorStepUp` {`principalId`, `credential`}: the supervisor enters their staff PIN on this device, and may not be the principal who closed the shift. Refused 403 `approver-is-closer` or `supervisor-step-up-refused` (decided 28 September, audit R144). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `reopenShift` body |
| Supervisor step up `supervisorStepUp` | group | required | — | — | — | The supervisor signing the reopen on this device (audit R144). Replaces the bare `approverPrincipalId`, which named an approver without proving they were there. | `reopenShift` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `reopenShift` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `reopenShift` body |

Errors to draw in the form: 403 The supervisor is the closing principal (problem type `approver-is-closer`), or the step-up failed: the PIN did not verify, or the principal does not hold …; 409 Shift is not closed (problem type `shift-not-closed`), or the fiscal period has closed over it (`fiscal-period-closed`)

**Form: Report incident** (modal, opened by *Report incident*; *Report incident* calls `reportIncident`, *Cancel* sends nothing)

**Collects what `reportIncident` sends before it is called.** Required: `id`, `kind`, `severity`, `venueId`, `description`, `occurredAt`, `recordedAt`. Optional: `assetId`, `locationDescription`, `involvedSubjectIds`, `involvedStaffPrincipalIds`, `witnessCount`, `firstAidGiven`, `emergencyServicesCalled`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `reportIncident` body |
| Kind `kind` | select | required | — | Guest injury · Staff injury · Near miss · Property damage · Equipment failure · Security incident · Fire or evacuation · Food safety · Environmental · Other | — | — | `reportIncident` body |
| Severity `severity` | radio group | required | — | Near miss · Minor · Moderate · Major · Critical | — | — | `reportIncident` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `reportIncident` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `reportIncident` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `reportIncident` body |
| Description `description` | text area | required | — | min length 3; max length 10000 | — | — | `reportIncident` body |
| Involved subjects `involvedSubjectIds` | multi-picker: choose involved subjects | optional | — | — | — | Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact. | `reportIncident` body |
| Involved staff principals `involvedStaffPrincipalIds` | multi-picker: choose involved staff principals | optional | — | — | — | — | `reportIncident` body |
| Witness count `witnessCount` | number field | optional | — | — | — | — | `reportIncident` body |
| First aid given `firstAidGiven` | toggle | optional | off | — | — | — | `reportIncident` body |
| Emergency services called `emergencyServicesCalled` | toggle | optional | off | — | — | — | `reportIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `reportIncident` body |
| Occurred at `occurredAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportIncident` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `reportIncident` body |

Errors to draw in the form: 400 Validation failed

**Form: Resume shift** (modal, opened by *Resume shift*; *Resume shift* calls `resumeShift`, *Cancel* sends nothing)

**Collects what `resumeShift` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `resumeShift` body |

Errors to draw in the form: 403 Not the principal who suspended it, and the caller does not hold SHIFT_CLOSE_OTHER (problem type `not-shift-holder`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this shift is not `suspended` (`shift-not-suspended`)

**Form: Save incident** (modal, opened by *Save incident*; *Save incident* calls `updateIncident`, *Cancel* sends nothing)

**Collects what `updateIncident` sends before it is called.** Nothing in the body is required. Optional: `status`, `severity`, `assignedToPrincipalId`, `investigationNote`, `rootCause`, `correctiveActions`, `correctiveWorkOrderId`, `attachmentRefs`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Status `status` | radio group | optional | — | Reported · Under investigation · Action required · Closed | — | — | `updateIncident` body |
| Severity `severity` | radio group | optional | — | Near miss · Minor · Moderate · Major · Critical | — | — | `updateIncident` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Investigation note `investigationNote` | text area | optional | — | max length 10000 | — | Appended as a new entry of `IncidentDetail.investigationNotes`, never overwriting the last (audit R106 (5)). | `updateIncident` body |
| Root cause `rootCause` | text area | optional | — | max length 2000 | — | — | `updateIncident` body |
| Corrective actions `correctiveActions` | text area | optional | — | max length 5000 | — | — | `updateIncident` body |
| Corrective work order `correctiveWorkOrderId` | picker: choose a corrective work order | optional | — | — | shows names, sends the id | — | `updateIncident` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `updateIncident` body |

Errors to draw in the form: 400 Closure attempted without findings or a corrective action

**Sent by *Close shift*** (`closeShift`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Counted cash `countedCash` | repeatable rows | required | — | at least 1; A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`. | — | The cashier's blind count, one line per denomination counted (decided 29 September, readiness close-out; our build plan). | `closeShift` body |
| Denomination `countedCash[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there. | `closeShift` body |
| Count `countedCash[].count` | number field | required | — | min 0; max 100000 | — | How many of this note or coin were counted. Zero is a line, not an omission: a denomination counted and found empty. | `closeShift` body |
| Total `countedCash[].total` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent. | `closeShift` body |
| Non cash declared `nonCashDeclared` | repeatable rows | optional | — | — | — | Declared totals per non-cash tender, for reconciliation against captured payments. | `closeShift` body |
| Tender `nonCashDeclared[].tender` | text field | required | — | — | — | — | `closeShift` body |
| Amount `nonCashDeclared[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeShift` body |
| Notes `notes` | text area | optional | — | max length 1000 | — | — | `closeShift` body |
| Release held leases `releaseHeldLeases` | toggle | optional | on | — | — | Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak. | `closeShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `closeShift` body |

**Sent by *Suspend shift*** (`suspendShift`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 200 | — | — | `suspendShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `suspendShift` body |

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Location description | text | — |
| Is reportable | yes / no (icon or chip) | Requires notification to an external authority within a statutory window. |
| Notification due at | 1 Oct 2026, 14:30 | — |
| Notified at | 1 Oct 2026, 14:30 | The earliest `notifiedAt` among this incident's authority notifications. Maintained on write by `recordAuthorityNotification`; each … |
| Assigned to principal | the name it points at, never the id | — |

**Every cash movement** (data table, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. |
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Shift | the name it points at, never the id | — |
| Deposit box | the name it points at, never the id | The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099). |
| Witness principal | the name it points at, never the id | The cashier who countersigned a withdrawal. Null on other movements. |
| Withdrawal reason | chip: Banking, Safe drop, Change order, Other | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |

**Every shift** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

**The selected incident** (detail panel, from `listIncidents`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Location description | text | — |
| Is reportable | yes / no (icon or chip) | Requires notification to an external authority within a statutory window. |
| Notification due at | 1 Oct 2026, 14:30 | — |
| Notified at | 1 Oct 2026, 14:30 | The earliest `notifiedAt` among this incident's authority notifications. Maintained on write by `recordAuthorityNotification`; each … |
| Assigned to principal | the name it points at, never the id | — |
| Reported by principal | the name it points at, never the id | — |
| Corrective work order | the name it points at, never the id | — |
| Occurred at | 1 Oct 2026, 14:30 | — |
| Recorded at | 1 Oct 2026, 14:30 | — |

**The incident** (detail panel, from `getIncident`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Incident number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Kind | chip: Guest injury, Staff injury, Near miss, Property damage, Equipment failure, Security … | — |
| Severity | chip: Near miss, Minor, Moderate, Major, Critical | — |
| Status | chip: Reported, Under investigation, Action required, Closed | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Location description | text | — |
| Is reportable | yes / no (icon or chip) | Requires notification to an external authority within a statutory window. |
| Notification due at | 1 Oct 2026, 14:30 | — |
| Notified at | 1 Oct 2026, 14:30 | The earliest `notifiedAt` among this incident's authority notifications. Maintained on write by `recordAuthorityNotification`; each … |
| Assigned to principal | the name it points at, never the id | — |
| Reported by principal | the name it points at, never the id | — |
| Corrective work order | the name it points at, never the id | — |
| Occurred at | 1 Oct 2026, 14:30 | — |
| Recorded at | 1 Oct 2026, 14:30 | — |

**The shift** (detail panel, from `getShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**The shift** (detail panel, from `getCurrentShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Accept shift variance (primary button) | `acceptShiftVariance` POST `/shifts/{shiftId}/accept-variance` | inline | Shift | 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type … | step-up: pin (A supervisor signs off a cashier's over/short at the till, in front of the drawer (audit R080 (e)).); opens modal first |
| Approve shift open (secondary button) | `approveShiftOpen` POST `/shifts/{shiftId}/approve-open` | inline | Shift | 409 Shift is not `pendingApproval` (problem type `shift-not-awaiting-approval`) | opens modal first |
| Close shift (destructive button) | `closeShift` POST `/shifts/{shiftId}/close` | CloseShiftRequest | ShiftCloseResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` or `suspended` — already closing or closed (problem type `shift-not-open`) — or open orders remain … | — |
| Open shift (secondary button) | `openShift` POST `/shifts` | OpenShiftRequest | Shift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent … | opens modal first |
| Record authority notification (secondary button) | `recordAuthorityNotification` POST `/incidents/{incidentId}/notify-authority` | inline | Incident | 409 The incident is not reportable (`isReportable` false, audit R106 (6)). | opens modal first |
| Record no sale (secondary button) | `recordNoSale` POST `/shifts/{shiftId}/no-sale` | inline | NoSaleEvent | 409 Shift is not open (problem type `shift-not-open`) | works offline; opens modal first |
| Reopen shift (secondary button) | `reopenShift` POST `/shifts/{shiftId}/reopen` | inline | Shift | 403 The supervisor is the closing principal (problem type `approver-is-closer`), or the step-up failed: the PIN did not verify, or the principal does not hold …; 409 Shift is not closed (problem type … | step-up: pin (Reopening a counted shift is a reversal; a supervisor signs it in place (audit R144).); opens modal first |
| Report incident (secondary button) | `reportIncident` POST `/incidents` | ReportIncidentRequest | Incident | 400 Validation failed | works offline; opens modal first |
| Resume shift (secondary button) | `resumeShift` POST `/shifts/{shiftId}/resume` | inline | Shift | 403 Not the principal who suspended it, and the caller does not hold SHIFT_CLOSE_OTHER (problem type `not-shift-holder`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this … | works offline; opens modal first |
| Suspend shift (destructive button) | `suspendShift` POST `/shifts/{shiftId}/suspend` | inline | Shift | 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` (problem type `shift-not-open`) | works offline |
| Save incident (secondary button) | `updateIncident` PATCH `/incidents/{incidentId}` | inline | Incident | 400 Closure attempted without findings or a corrective action | opens modal first |

**Data it reads**: `getCurrentShift` (onLoad, From the flow it appears in); `listIncidents` (onLoad, From the flow it appears in); `getShift` (onLoad, Read a shift); `listCashMovements` (onLoad, Lifts, adds and the opening float); `listShifts` (onLoad, List shifts)

**Where the user goes next**

- → `EMP-004` Task list: *Works the task list*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-051` Restaurant Service Command Center: *Restaurant Service Command Center*
- → `EMP-052` Floor Plan & Table Map: *Floor Plan & Table Map*
- → `EMP-053` Table & Seating Configuration: *Table & Seating Configuration*
- → `EMP-054` Reservation Calendar & Timeline: *Reservation Calendar & Timeline*
- → `EMP-055` Create / Edit Reservation: *Create / Edit Reservation*
- → `EMP-056` Walk-In & Waitlist Management: *Walk-In & Waitlist Management*
- → `EMP-057` Guest Profile & Dining History: *Guest Profile & Dining History*
- → `EMP-058` Live Table & Service Management: *Live Table & Service Management*
- → `EMP-059` Table Order, Bill & Payment Management: *Table Order, Bill & Payment Management*
- → `EMP-060` Reservation & Table Performance: *Reservation & Table Performance*
- → `EMP-061` Retail Inventory Command Center: *Retail Inventory Command Center*
- → `EMP-062` Store Stock & SKU Availability: *Store Stock & SKU Availability*
- → `EMP-063` Requisition & Smart Store Replenishment: *Requisition & Smart Store Replenishment*
- → `EMP-064` Store-to-Store & Warehouse Transfers: *Store-to-Store & Warehouse Transfers*
- → `EMP-065` Receiving & Store Put-Away: *Receiving & Store Put-Away*
- → `EMP-066` Stock Count & Cycle Count Management: *Stock Count & Cycle Count Management*
- → `EMP-067` Damage, Loss, Shrinkage & Stock Adjustment: *Damage, Loss, Shrinkage & Stock Adjustment*
- → `EMP-068` Reservation, Allocation & Omnichannel Inventory: *Reservation, Allocation & Omnichannel Inventory*
- → `EMP-069` Barcode, RFID, Serialized Stock & Traceability: *Barcode, RFID, Serialized Stock & Traceability*
- → `EMP-070` Inventory Exceptions, AI Replenishment & Action Center: *Inventory Exceptions, AI Replenishment & Action Center*
- → `EMP-071` Rental Checkout Command Center: *Rental Checkout Command Center*
- → `EMP-081` Active Rental Operations Command Center: *Active Rental Operations Command Center*
- → `EMP-091` Rental Return Command Center: *Rental Return Command Center*
- → `EMP-006` Raise a task: *Raise a task*
- → `EMP-014` Ticket lookup: *Ticket lookup*
- → `EMP-019` AI assistant — home: *AI assistant — home*
- → `EMP-021` Roster: *Roster*
- → `EMP-022` My rota: *My rota*
- → `EMP-024` Clock in / out: *Clock in / out*
- → `EMP-025` Break management: *Break management*
- → `EMP-026` Incident report: *Incident report*; carries `incidentId`
- → `EMP-028` Lost & found: *Lost & found*
- → `EMP-029` Guest assistance: *Guest assistance*; carries `incidentId`
- → `EMP-030` Venue map: *Venue map*
- → `EMP-031` Queue monitor: *Queue monitor*
- → `EMP-033` Capacity view: *Capacity view*
- → `EMP-034` Walk-up sale: *Walk-up sale*
- → `EMP-037` Notifications: *Notifications*
- → `EMP-038` Broadcast to team: *Broadcast to team*
- → `EMP-039` Announcements: *Announcements*
- → `EMP-047` Emergency mode: *Emergency mode*
- → `EMP-042` Profile: *Profile*

**What opens over it**

- confirmDialog *Close shift*: **Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A home duty this affects should be identified in the dialog, not just counted. **Collects what `closeShift` sends before it is called.** Required: `countedCash`, `recordedAt`. Optional …
- confirmDialog *Suspend shift*: **Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A home duty this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The home duty list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the home duty untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on severity, status, isReportable and the home duty are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Last synced view, with its age. The pending count is always current because it is local |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Closure attempted without findings or a corrective action; 400 Validation failed; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent (`required-device-absent`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this shift is not `suspended` (`shift-not-suspended`) |

#### Permissions

- `getCurrentShift` → `SHIFT_OPEN` (operate) · staff
- `listIncidents` → `INCIDENT_VIEW` (read) · staff
- `acceptShiftVariance` → `OVERSHORT_ACCEPT` (operate) · staff · step-up pin
- `approveShiftOpen` → `SHIFT_APPROVE_OPEN` (operate) · staff
- `closeShift` → `SHIFT_CLOSE` (operate) · staff
- `getIncident` → `INCIDENT_VIEW` (read) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `openShift` → `SHIFT_OPEN` (operate) · staff
- `recordAuthorityNotification` → `INCIDENT_MANAGE` (configure) · staff
- `recordNoSale` → `CASH_NO_SALE` (operate) · staff
- `reopenShift` → `SHIFT_REOPEN` (operate) · staff · step-up pin
- `reportIncident` → `INCIDENT_REPORT` (operate) · staff
- `resumeShift` → `SHIFT_OPEN` (operate) · staff
- `suspendShift` → `SHIFT_SUSPEND` (operate) · staff
- `updateIncident` → `INCIDENT_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

16 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 8.9.5 | System shall provide real-time visibility of incidents, hazards, complaints, emergencies, and operational disruptions. | Unified Operations Dashboard | CONTRACTED | `listIncidents` |
| 5.9.8 | The system should allow the option of configuring the requirement of a supervisor's approval for opening and closing a cashier's session. For example, to open a cashier’s session, the cashier details … | F&B & Guest Management | CONTRACTED | `approveShiftOpen` |
| 5.8.3 | The system should allow the cashier to enter a total amount counted, or to count by denomination. For denomination counts, the cashier counts and enters each denomination separately and each count is … | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.1 | The system should be able to manage end of day shift closing and provide the ability to close out each cash register. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.2 | The system should have the ability to do a "blind" cashier close-out. Over-shorts should be captured and recorded. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.5 | The system should allow automatic closing of a cashier's session after a configurable time period. The supervisor should be notified on closing of the session. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 17.5.3 | Hazard Reporting - System shall support hazard reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.4 | Incident Reporting - System shall support incident reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 17.5.5 | Near-Miss Reporting - System shall support near-miss reporting. | Maintenance & Safety Management | CONTRACTED | `reportIncident` |
| 18.4.1 | Hazard Reporting - Users shall submit hazard reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.2 | Incident Reporting - Users shall submit incident reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| 18.4.3 | Near-Miss Reporting - Users shall submit near-miss reports. | Employee Mobile App & AI Assistant | CONTRACTED | `reportIncident` |
| … 4 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Quick-create for maintenance, IT support, cleaning/safety/security, store, purchase and leave requests. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-230)*
- Role-based home shows task counts, work orders and inspections for the employee; the whole navigation set (approvals, inventory, etc.) is filtered by role/permissions. *(client request · MoM 10 Aug 2026, 5.1 Login, Roles & Dashboard · DI-227)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-003` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 4: Sees the home screen on duty → Today, at a glance
- Flow F64 *A steward signs in and takes a venue and a role*, step 4: They go on duty. → **Open incidents surface before anything else.** A steward starting a shift needs yesterday’s unresolved problem before today’s first task.
- Flow F08 branch at step 4 (recoverable): when Signal lost in a plant room or basement, Queues locally. The status strip shows pending count, and EMP-017 reconciles on return.
- ADR-0023 *— Personal data lives apart from the append-only ledger* (`docs/adr/0023-pii-separation.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (70), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (100 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Accept shift variance, Approve shift open, Close shift, Open shift, Record authority notification, Record no sale, Reopen shift, Report incident, Resume shift, Suspend shift, Save incident.
- [ ] Every transition is wired: `EMP-004`, `EMP-001`, `EMP-002`, `EMP-051`, `EMP-052`, `EMP-053`, `EMP-054`, `EMP-055`, `EMP-056`, `EMP-057`, `EMP-058`, `EMP-059`, `EMP-060`, `EMP-061`, `EMP-062`, `EMP-063`, `EMP-064`, `EMP-065`, `EMP-066`, `EMP-067`, `EMP-068`, `EMP-069`, `EMP-070`, `EMP-071`, `EMP-081`, `EMP-091`, `EMP-006`, `EMP-014`, `EMP-019`, `EMP-021`, `EMP-022`, `EMP-024`, `EMP-025`, `EMP-026`, `EMP-028`, `EMP-029`, `EMP-030`, `EMP-031`, `EMP-033`, `EMP-034`, `EMP-037`, `EMP-038`, `EMP-039`, `EMP-047`, `EMP-042`.
- [ ] Every gated control is gated: `CASH_NO_SALE`, `INCIDENT_MANAGE`, `INCIDENT_REPORT`, `INCIDENT_VIEW`, `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SHIFT_APPROVE_OPEN`, `SHIFT_CLOSE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-009` End shift

**Close out cleanly, including anything unsynced.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `CASH_LIFT`, `CASH_NO_SALE`, `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SHIFT_APPROVE_OPEN`, `SHIFT_CLOSE`… (9 operate); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | approvalInbox (comfortable density): `approveShiftOpen` decides items that `listCashMovements` queues — every row is waiting for a person, so the empty state is success |
| Offline | **Cannot close.** Closing needs the server total, and a locally computed variance is not a variance |
| Opens with | `shiftId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/operations/end-shift` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Workstation | picker: choose a workstation | — | — | `listShifts` ?workstationId |
| Status | select | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | `listShifts` ?status |
| Opened from | date and time picker | — | — | `listShifts` ?openedFrom |
| Opened to | date and time picker | — | — | `listShifts` ?openedTo |

**Form: Accept shift variance** (modal, opened by *Accept shift variance*; *Accept shift variance* calls `acceptShiftVariance`, *Cancel* sends nothing)

**Collects what `acceptShiftVariance` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | Retained for audit. The accepting principal is recorded. | `acceptShiftVariance` body |

Errors to draw in the form: 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type `shift-not-pending-variance`) — within tolerance, still open, or already accepted.

**Form: Approve shift open** (modal, opened by *Approve shift open*; *Approve shift open* calls `approveShiftOpen`, *Cancel* sends nothing)

**Collects what `approveShiftOpen` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 300 | — | — | `approveShiftOpen` body |

Errors to draw in the form: 409 Shift is not `pendingApproval` (problem type `shift-not-awaiting-approval`)

**Form: Create cash movement** (modal, opened by *Create cash movement*; *Create cash movement* calls `createCashMovement`, *Cancel* sends nothing)

**Collects what `createCashMovement` sends before it is called.** Required: `id`, `kind`, `amount`, `recordedAt`. Optional: `denominations`, `reference`, `reason`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. | `createCashMovement` body |
| Kind `kind` | segmented control | required | — | Opening float · Lift · Add | — | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`. | `createCashMovement` body |
| Amount `amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `createCashMovement` body |
| Denominations `denominations` | repeatable rows | optional | — | at least 1 | — | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. | `createCashMovement` body |
| ID `denominations[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Shift `denominations[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `createCashMovement` body |
| Deposit box `denominations[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Count kind `denominations[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `createCashMovement` body |
| Cash movement `denominations[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `createCashMovement` body |
| Denomination `denominations[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `createCashMovement` body |
| Counted quantity `denominations[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `createCashMovement` body |
| Counted value `denominations[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `createCashMovement` body |
| Counted by `denominations[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `createCashMovement` body |
| Counted at `denominations[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |
| Recount of `denominations[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `createCashMovement` body |
| Reference `reference` | text field | optional | — | max length 64 | — | Safe drop reference or bag number. | `createCashMovement` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `createCashMovement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createCashMovement` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since (`lift-exceeds-float`, audit R123 …

**Form: Open shift** (modal, opened by *Open shift*; *Open shift* calls `openShift`, *Cancel* sends nothing)

**Collects what `openShift` sends before it is called.** Required: `workstationId`, `openingFloat`. Optional: `depositBoxCode`, `bagNumber`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Workstation `workstationId` | picker: choose a workstation | required | — | — | shows names, sends the id | — | `openShift` body |
| Opening float `openingFloat` | repeatable rows | required | — | at least 1 | — | A count is a list of lines and the line is the row. Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — … | `openShift` body |
| ID `openingFloat[].id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `openShift` body |
| Shift `openingFloat[].shiftId` | picker: choose a shift | required | — | — | shows names, sends the id | A UUIDv7, as `Shift.id` and `orders.pos_shift.id` are. | `openShift` body |
| Deposit box `openingFloat[].depositBoxId` | picker: choose a deposit box | optional | — | — | shows names, sends the id | — | `openShift` body |
| Count kind `openingFloat[].countKind` | segmented control | optional | — | Opening float · Close · Movement | — | Which count this line belongs to — the opening float (`openShift`), the close (`closeShift`) or a lift or add (`createCashMovement`). | `openShift` body |
| Cash movement `openingFloat[].cashMovementId` | picker: choose a cash movement | optional | — | — | shows names, sends the id | The movement this line counts, where `countKind` is `movement`. How `listCashMovements` rebuilds each movement's `denominations`. | `openShift` body |
| Denomination `openingFloat[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` — face value, kind and sort order live there. | `openShift` body |
| Counted quantity `openingFloat[].countedQuantity` | number field | required | — | min 0 | — | How many of this note or coin were in the drawer. | `openShift` body |
| Counted value `openingFloat[].countedValue` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | Quantity times face value, stored. Derivable, and stored anyway: a denomination revalued or deactivated later would silently rewrite a historical count. | `openShift` body |
| Counted by `openingFloat[].countedBy` | picker: choose a counted by | optional | — | — | shows names, sends the id | — | `openShift` body |
| Counted at `openingFloat[].countedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `openShift` body |
| Recount of `openingFloat[].recountOf` | picker: choose a recount of | optional | — | — | shows names, sends the id | A recount points at what it replaces rather than overwriting it. `requestRecount` exists because a variance is a question before it is a fact. | `openShift` body |
| Deposit box code `depositBoxCode` | text field | optional | — | max length 64 | — | Physical container assigned to this shift. Required where the venue configures deposit box allocation. | `openShift` body |
| Bag number `bagNumber` | text field | optional | — | max length 64 | — | Required where the venue configures bag numbers as mandatory. | `openShift` body |
| Recorded at `recordedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the device recorded it. `openShift` is online-only (F32), so this differs from server receipt time only by transit; it is kept because the shift's other device writes are … | `openShift` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent (`required-device-absent`).

**Form: Record no sale** (modal, opened by *Record no sale*; *Record no sale* calls `recordNoSale`, *Cancel* sends nothing)

**Collects what `recordNoSale` sends before it is called.** Required: `id`, `reason`, `recordedAt`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordNoSale` body |
| Reason `reason` | radio group | required | — | Change for guest · Correct float · Retrieve dropped cash · Till check · Other | — | — | `recordNoSale` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `recordNoSale` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordNoSale` body |

Errors to draw in the form: 409 Shift is not open (problem type `shift-not-open`)

**Form: Reopen shift** (modal, opened by *Reopen shift*; *Reopen shift* calls `reopenShift`, *Cancel* sends nothing)

**Collects what `reopenShift` sends before it is called.** Required: `reason`, `supervisorStepUp` {`principalId`, `credential`}: the supervisor enters their staff PIN on this device, and may not be the principal who closed the shift. Refused 403 `approver-is-closer` or `supervisor-step-up-refused` (decided 28 September, audit R144). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `reopenShift` body |
| Supervisor step up `supervisorStepUp` | group | required | — | — | — | The supervisor signing the reopen on this device (audit R144). Replaces the bare `approverPrincipalId`, which named an approver without proving they were there. | `reopenShift` body |
| Principal `supervisorStepUp.principalId` | picker: choose a principal | required | — | — | shows names, sends the id | The supervisor signing. Recorded against the act. | `reopenShift` body |
| Credential `supervisorStepUp.credential` | text area | required | — | max length 512 | — | The supervisor's staff PIN, as they sign in at a till with it. A PIN, never a password (audit R123 (7)). | `reopenShift` body |

Errors to draw in the form: 403 The supervisor is the closing principal (problem type `approver-is-closer`), or the step-up failed: the PIN did not verify, or the principal does not hold …; 409 Shift is not closed (problem type `shift-not-closed`), or the fiscal period has closed over it (`fiscal-period-closed`)

**Form: Resume shift** (modal, opened by *Resume shift*; *Resume shift* calls `resumeShift`, *Cancel* sends nothing)

**Collects what `resumeShift` sends before it is called.** Required: `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `resumeShift` body |

Errors to draw in the form: 403 Not the principal who suspended it, and the caller does not hold SHIFT_CLOSE_OTHER (problem type `not-shift-holder`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this shift is not `suspended` (`shift-not-suspended`)

**Sent by *Close shift*** (`closeShift`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Counted cash `countedCash` | repeatable rows | required | — | at least 1; A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`. | — | The cashier's blind count, one line per denomination counted (decided 29 September, readiness close-out; our build plan). | `closeShift` body |
| Denomination `countedCash[].denominationId` | picker: choose a denomination | required | — | — | shows names, sends the id | References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there. | `closeShift` body |
| Count `countedCash[].count` | number field | required | — | min 0; max 100000 | — | How many of this note or coin were counted. Zero is a line, not an omission: a denomination counted and found empty. | `closeShift` body |
| Total `countedCash[].total` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | `count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent. | `closeShift` body |
| Non cash declared `nonCashDeclared` | repeatable rows | optional | — | — | — | Declared totals per non-cash tender, for reconciliation against captured payments. | `closeShift` body |
| Tender `nonCashDeclared[].tender` | text field | required | — | — | — | — | `closeShift` body |
| Amount `nonCashDeclared[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `closeShift` body |
| Notes `notes` | text area | optional | — | max length 1000 | — | — | `closeShift` body |
| Release held leases `releaseHeldLeases` | toggle | optional | on | — | — | Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak. | `closeShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `closeShift` body |

**Sent by *Suspend shift*** (`suspendShift`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 200 | — | — | `suspendShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `suspendShift` body |

#### Outputs: what the screen shows and produces

**Shown**

**Waiting for a decision** (data table, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. |
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Shift | the name it points at, never the id | — |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |
| Sequence | 1,234 | Monotonic within the shift. Preserves order across an offline batch. |
| Synced at | 1 Oct 2026, 14:30 | — |

**Every shift** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

**The selected cash movement** (detail panel, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. |
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Shift | the name it points at, never the id | — |
| Deposit box | the name it points at, never the id | The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099). |
| Witness principal | the name it points at, never the id | The cashier who countersigned a withdrawal. Null on other movements. |
| Withdrawal reason | chip: Banking, Safe drop, Change order, Other | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |
| Sequence | 1,234 | Monotonic within the shift. Preserves order across an offline batch. |
| Synced at | 1 Oct 2026, 14:30 | — |

**The shift** (detail panel, from `getShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**The shift** (detail panel, from `getCurrentShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Close shift (destructive button) | `closeShift` POST `/shifts/{shiftId}/close` | CloseShiftRequest | ShiftCloseResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` or `suspended` — already closing or closed (problem type `shift-not-open`) — or open orders remain … | — |
| Accept shift variance (secondary button) | `acceptShiftVariance` POST `/shifts/{shiftId}/accept-variance` | inline | Shift | 403 The caller lacks OVERSHORT_ACCEPT at this venue, or is the cashier whose shift it is (problem type `approver-is-cashier`) — a cashier signing off their own …; 409 Shift is not `pendingVariance` (problem type … | step-up: pin (A supervisor signs off a cashier's over/short at the till, in front of the drawer (audit R080 (e)).); opens modal first |
| Approve shift open (secondary button) | `approveShiftOpen` POST `/shifts/{shiftId}/approve-open` | inline | Shift | 409 Shift is not `pendingApproval` (problem type `shift-not-awaiting-approval`) | opens modal first |
| Create cash movement (secondary button) | `createCashMovement` POST `/shifts/{shiftId}/cash-movements` | CreateCashMovementRequest | CashMovement | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 Shift is not open (problem type `shift-not-open`), or the lift exceeds the float counted at the last count less lifts since … | works offline; opens modal first |
| Open shift (secondary button) | `openShift` POST `/shifts` | OpenShiftRequest | Shift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent … | opens modal first |
| Record no sale (secondary button) | `recordNoSale` POST `/shifts/{shiftId}/no-sale` | inline | NoSaleEvent | 409 Shift is not open (problem type `shift-not-open`) | works offline; opens modal first |
| Reopen shift (secondary button) | `reopenShift` POST `/shifts/{shiftId}/reopen` | inline | Shift | 403 The supervisor is the closing principal (problem type `approver-is-closer`), or the step-up failed: the PIN did not verify, or the principal does not hold …; 409 Shift is not closed (problem type … | step-up: pin (Reopening a counted shift is a reversal; a supervisor signs it in place (audit R144).); opens modal first |
| Resume shift (secondary button) | `resumeShift` POST `/shifts/{shiftId}/resume` | inline | Shift | 403 Not the principal who suspended it, and the caller does not hold SHIFT_CLOSE_OTHER (problem type `not-shift-holder`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this … | works offline; opens modal first |
| Suspend shift (destructive button) | `suspendShift` POST `/shifts/{shiftId}/suspend` | inline | Shift | 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` (problem type `shift-not-open`) | works offline |

**Data it reads**: `getCurrentShift` (onLoad, The open or suspended shift on the session's workstation); `getShift` (onLoad, Read a shift); `listCashMovements` (onLoad, Lifts, adds and the opening float); `listShifts` (onLoad, List shifts)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

**What opens over it**

- confirmDialog *Close shift*: **Names what `closeShift` changes and what it leaves alone**, in the consequence rather than the verb. A end shift this affects should be identified in the dialog, not just counted. **Collects what `closeShift` sends before it is called.** Required: `countedCash`, `recordedAt`. Optional …
- confirmDialog *Suspend shift*: **Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A end shift this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The end shift list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the end shift untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **Nothing is waiting, which is the good outcome.** An empty queue means every item has been decided; it offers no create action, because creating work is not what it needs. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCashMovements` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Cannot close.** Closing needs the server total, and a locally computed variance is not a variance |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A shift is already open on this workstation (problem type `shift-already-open`), or a required device is absent (`required-device-absent`).; 409 Another shift is now open on this workstation (problem type `shift-already-open`), or this shift is not `suspended` (`shift-not-suspended`); 409 Shift is not `open` (problem type `shift-not-open`) |

#### Permissions

- `closeShift` → `SHIFT_CLOSE` (operate) · staff
- `acceptShiftVariance` → `OVERSHORT_ACCEPT` (operate) · staff · step-up pin
- `approveShiftOpen` → `SHIFT_APPROVE_OPEN` (operate) · staff
- `createCashMovement` → `CASH_LIFT` (operate) · staff
- `getCurrentShift` → `SHIFT_OPEN` (operate) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `openShift` → `SHIFT_OPEN` (operate) · staff
- `recordNoSale` → `CASH_NO_SALE` (operate) · staff
- `reopenShift` → `SHIFT_REOPEN` (operate) · staff · step-up pin
- `resumeShift` → `SHIFT_OPEN` (operate) · staff
- `suspendShift` → `SHIFT_SUSPEND` (operate) · staff

**A refused user sees:** Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.8.3 | The system should allow the cashier to enter a total amount counted, or to count by denomination. For denomination counts, the cashier counts and enters each denomination separately and each count is … | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.1 | The system should be able to manage end of day shift closing and provide the ability to close out each cash register. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.2 | The system should have the ability to do a "blind" cashier close-out. Over-shorts should be captured and recorded. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.5 | The system should allow automatic closing of a cashier's session after a configurable time period. The supervisor should be notified on closing of the session. | F&B & Guest Management | CONTRACTED | `closeShift` |
| 5.9.8 | The system should allow the option of configuring the requirement of a supervisor's approval for opening and closing a cashier's session. For example, to open a cashier’s session, the cashier details … | F&B & Guest Management | CONTRACTED | `approveShiftOpen` |
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-009` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 8: Ends the shift → Tasks reassigned, notes handed over
- Flow F72 *A shift ends and the summary is read*, step 3: The supervisor closes it. → **Closing and accepting a variance are supervisor acts** and now live only here.
- Flow F08 branch at step 8 (recoverable): when Shift ends with tasks open, Reassigned or carried, never silently closed. An open task at handover is the thing handover exists for.
- Flow F08 branch at step 8 (recoverable): when Steward forgets to end the shift, Auto-closed after the venue limit, and recorded as autoClosed rather than closed — nobody counted it.

#### Acceptance for the design

- [ ] Every input above is drawn (57), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (69 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Close shift, Accept shift variance, Approve shift open, Create cash movement, Open shift, Record no sale, Reopen shift, Resume shift, Suspend shift.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `CASH_LIFT`, `CASH_NO_SALE`, `OVERSHORT_ACCEPT`, `REPORT_VIEW_WORKSTATION`, `SHIFT_APPROVE_OPEN`, `SHIFT_CLOSE`, `SHIFT_OPEN`, `SHIFT_REOPEN`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-010` Scan — ready

**The raised centre action, and the thing this app is for.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate) |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | **Keep working when the network does not.** The screen already had an `offline` state. |
| Opens with | nothing: it opens on its own |
| Route | `/operations/scan-ready` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Absorbed EMP-011, EMP-012, EMP-013, EMP-016 on 18 August.** A scanner is one screen the device sits on all day, and an outcome is a state of it — **routing to `/access/admitted` for something gone in 1.5 seconds is a page load per guest**, and at a gate doing 40 a minute that is the whole problem. Every absorbed screen kept its copy as a named state.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Access point id | picker: choose an access point (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?accessPointId=` to `listScans`. | `listScans` ?accessPointId |
| Ticket id | picker: choose a ticket (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ticketId=` to `listScans`. | `listScans` ?ticketId |
| Outcome | segmented control | optional | — | Admitted · Denied · Overridden | — | Sends `?outcome=` to `listScans`. | `listScans` ?outcome |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listScans`. | `listScans` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listScans`. | `listScans` ?recordedTo |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |

**Form: Sync scans** (modal, opened by *Sync scans*; *Sync scans* calls `syncScans`, *Cancel* sends nothing)

**Collects what `syncScans` sends before it is called.** Required: `deviceId`, `scans`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | Sequence numbers are monotonic per device, not globally. | `syncScans` body |
| Scans `scans` | repeatable rows | required | — | at least 1; at most 500 | — | — | `syncScans` body |
| ID `scans[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `syncScans` body |
| Media code `scans[].mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `syncScans` body |
| Media kind `scans[].mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive | — | — | `syncScans` body |
| Direction `scans[].direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `syncScans` body |
| Group size `scans[].groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `syncScans` body |
| Proximity token `scans[].proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `syncScans` body |
| Recorded at `scans[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `syncScans` body |
| Sequence `scans[].sequence` | number field | required | — | min 1 | — | Monotonic per device. The server processes in this order. | `syncScans` body |
| Local outcome `scans[].localOutcome` | segmented control | required | — | Admitted · Denied · Overridden | — | What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded. | `syncScans` body |
| Local deny reason `scans[].localDenyReason` | select | optional | — | Not found · Not yet valid · Expired · Already used · Reentry limit reached · Exit required before reentry · Wrong access point · Wrong performance · Outside admission window · Entitlement suspended · Blacklisted · Capacity reached … | — | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean. | `syncScans` body |
| Overridden by principal `scans[].overriddenByPrincipalId` | picker: choose an overridden by principal | optional | — | — | shows names, sends the id | — | `syncScans` body |
| Override reason `scans[].overrideReason` | text field | optional | — | — | — | — | `syncScans` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Validate access** (modal, opened by *Validate access*; *Validate access* calls `validateAccess`, *Cancel* sends nothing)

**Collects what `validateAccess` sends before it is called.** Required: `id`, `mediaCode`, `mediaKind`, `direction`, `recordedAt`. Optional: `groupSize`, `proximityToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key and dedupe key. | `validateAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life. | `validateAccess` body |
| Media kind `mediaKind` | select | required | — | Image · Video · Audio · Document · Vector · Font · Archive | — | — | `validateAccess` body |
| Direction `direction` | radio group | required | — | Entry · Exit · Reentry · Crossover | — | — | `validateAccess` body |
| Group size `groupSize` | number field | optional | — | min 1 | — | For group media admitting several holders on one read. | `validateAccess` body |
| Proximity token `proximityToken` | text field | optional | — | — | — | BLE proximity assertion where the venue requires the operator to be physically at the gate. | `validateAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time of the read. Authoritative for ordering, not for validity. | `validateAccess` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell

**Form: Validate group access** (modal, opened by *Validate group access*; *Validate group access* calls `validateGroupAccess`, *Cancel* sends nothing)

**Collects what `validateGroupAccess` sends before it is called.** Required: `id`, `mediaCode`, `admitCount`, `recordedAt`. Optional: `direction`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `validateGroupAccess` body |
| Media code `mediaCode` | text area | required | — | max length 256 | — | — | `validateGroupAccess` body |
| Admit count `admitCount` | number field | required | — | min 1 | — | — | `validateGroupAccess` body |
| Direction `direction` | radio group | optional | — | Entry · Exit · Reentry · Crossover | — | — | `validateGroupAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `validateGroupAccess` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance

**Sent by *Override access*** (`overrideAccess`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `overrideAccess` body |
| Scan `scanId` | picker: choose a scan | required | — | — | shows names, sends the id | The denied scan being overridden. | `overrideAccess` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `overrideAccess` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `overrideAccess` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every scan event** (data table, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The scan's client-generated UUIDv7, the key offline replay deduplicates on. |
| Access point | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Ticket | the name it points at, never the id | The `Entitlement.id` scanned; null where the media resolved to nothing. |
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Direction | chip: Entry, Exit, Reentry, Crossover | — |
| Operator principal | the name it points at, never the id | — |
| Device | the name it points at, never the id | — |
| Overrides scan | the name it points at, never the id | Set only on an override row, naming the denied scan it admits against (decided 28 September, audit R228). |

**The selected scan event** (detail panel, from `listScans`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | The scan's client-generated UUIDv7, the key offline replay deduplicates on. |
| Access point | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Ticket | the name it points at, never the id | The `Entitlement.id` scanned; null where the media resolved to nothing. |
| Media code | text | — |
| Outcome | chip: Admitted, Denied, Overridden | — |
| Deny reason | chip: Not found, Not yet valid, Expired, Already used, Reentry limit reached, Exit … | Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a … |
| Direction | chip: Entry, Exit, Reentry, Crossover | — |
| Operator principal | the name it points at, never the id | — |
| Device | the name it points at, never the id | — |
| Overrides scan | the name it points at, never the id | Set only on an override row, naming the denied scan it admits against (decided 28 September, audit R228). |
| Override reason | text | The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`. |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Synced at | 1 Oct 2026, 14:30 | Null while pending. Differs from recordedAt for offline scans. |

**The offline package** (detail panel, from `getOfflinePackage`)

| Shows | Format | Notes |
|---|---|---|
| Generated at | 1 Oct 2026, 14:30 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Access point | the name it points at, never the id | — |
| Entitlements | list or chips (count when long) | Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device … |
| Delegated rights | list or chips (count when long) | Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits … |
| Blacklist | list or chips (count when long) | Media codes to deny outright regardless of entitlement state. |
| Admission rules | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sync scans (primary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Data it reads**: `listScans` (onLoad, List scan events); `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A scan ready this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The scan ready list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the scan ready untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No scan ready yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the scan ready are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Keep working when the network does not.** The screen already had an `offline` state. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 No identifier supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance |

#### Permissions

- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff
- `verifyAccreditationCredential` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

61 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.58 | In park attendance figure per ticket time is calculated in real time. | Admission and Access | CONTRACTED | `listScans` |
| 5.3.28 | Maintain detailed access validation history including gate entries, exits, attraction validations, RFID scans, QR scans, and turnstile events. | F&B & Guest Management | CONTRACTED | `listScans` |
| 18.1.4 | Synchronization - System shall synchronize data when connectivity is restored. | Employee Mobile App & AI Assistant | CONTRACTED | `syncScans` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| … 49 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A separate dedicated scanner app for devices used only for scanning (e.g. mounted at turnstiles/gates) shows only scanning functions; the same validation is also embedded in the employee app. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-239)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-010` · status **notStarted** · provenance generated
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-010?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sync scans, Lookup ticket, Override access, Validate access, Validate group access.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-004` Task list

**See what is assigned, and what is overdue.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW` (3 operate, 1 configure, 1 read); in the flows as supervisor, technician |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act |
| Offline | Local queue. Tasks completed offline sync on return |
| Opens with | `workOrderId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/task-list` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: createWorkOrder. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listWorkOrders`. | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | optional | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | — | Sends `?status=` to `listWorkOrders`. | `listWorkOrders` ?status |
| Priority | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Sends `?priority=` to `listWorkOrders`. | `listWorkOrders` ?priority |
| Asset id | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Sends `?assetId=` to `listWorkOrders`. | `listWorkOrders` ?assetId |
| Overdue only | toggle | optional | off | — | — | Sends `?overdueOnly=` to `listWorkOrders`. | `listWorkOrders` ?overdueOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Form: Attach work order evidence** (modal, opened by *Attach work order evidence*; *Attach work order evidence* calls `attachWorkOrderEvidence`, *Cancel* sends nothing)

**Collects what `attachWorkOrderEvidence` sends before it is called.** Required: `kind`. Optional: `assetRef`, `text`, `capturedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Photo · Video · Document · Note · Signature | — | — | `attachWorkOrderEvidence` body |
| Asset ref `assetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | In the media store | `attachWorkOrderEvidence` body |
| Text `text` | text area | optional | — | max length 4000 | — | Where the kind is a note | `attachWorkOrderEvidence` body |
| Captured at `capturedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `attachWorkOrderEvidence` body |
| Stage `stage` | radio group | optional | — | Before · During · After · Sign off | — | — | `attachWorkOrderEvidence` body |

**Form: Complete work order** (modal, opened by *Complete work order*; *Complete work order* calls `completeWorkOrder`, *Cancel* sends nothing)

**Collects what `completeWorkOrder` sends before it is called.** Required: `resolution`, `recordedAt`. Optional: `resolutionCode`, `attachmentRefs`, `followUpRequired`, `followUpNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resolution `resolution` | text area | required | — | min length 3; max length 5000 | — | — | `completeWorkOrder` body |
| Resolution code `resolutionCode` | select | optional | — | Repaired · Part replaced · Adjusted · Cleaned · No fault found · Referred external · Replaced · Deferred | — | — | `completeWorkOrder` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `completeWorkOrder` body |
| Follow up required `followUpRequired` | toggle | optional | off | — | — | — | `completeWorkOrder` body |
| Follow up note `followUpNote` | text area | optional | — | max length 1000 | — | — | `completeWorkOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `completeWorkOrder` body |

Errors to draw in the form: 400 Completion photographs required for this category and none supplied

**Form: Pause work order** (modal, opened by *Pause work order*; *Pause work order* calls `pauseWorkOrder`, *Cancel* sends nothing)

**Collects what `pauseWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `requisitionId`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Awaiting parts · Awaiting permit · Awaiting outage window · Awaiting specialist · End of shift · Safety concern · Other | — | — | `pauseWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `pauseWorkOrder` body |
| Requisition `requisitionId` | picker: choose a requisition | optional | — | — | shows names, sends the id | Where a part was ordered, so the two are linked. | `pauseWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Record work order parts** (modal, opened by *Record work order parts*; *Record work order parts* calls `recordWorkOrderParts`, *Cancel* sends nothing)

**Collects what `recordWorkOrderParts` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `recordWorkOrderParts` body |
| Inventory item `lines[].inventoryItemId` | picker: choose an inventory item | required | — | — | shows names, sends the id | — | `recordWorkOrderParts` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `recordWorkOrderParts` body |
| Location `lines[].locationId` | picker: choose a location | optional | — | — | shows names, sends the id | — | `recordWorkOrderParts` body |

Errors to draw in the form: 409 Insufficient stock

**Form: Record work order time** (modal, opened by *Record work order time*; *Record work order time* calls `recordWorkOrderTime`, *Cancel* sends nothing)

**Collects what `recordWorkOrderTime` sends before it is called.** Required: `id`, `action`, `recordedAt`. Optional: `pauseReason`, `note`. **When the pause reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordWorkOrderTime` body |
| Action `action` | radio group | required | — | Start · Pause · Resume · Stop | — | — | `recordWorkOrderTime` body |
| Pause reason `pauseReason` | select | optional | — | Awaiting parts · Awaiting access · Awaiting approval · End of shift · Reassigned · Other | — | — | `recordWorkOrderTime` body |
| Note `note` | text area | optional | — | max length 500; Required where the pause reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the pause reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones … | `recordWorkOrderTime` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordWorkOrderTime` body |

Errors to draw in the form: 400 Validation failed; 409 Action inconsistent with the current timer state

**Form: Start work order** (modal, opened by *Start work order*; *Start work order* calls `startWorkOrder`, *Cancel* sends nothing)

**Collects what `startWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `startedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Started at `startedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time where the job began offline. The server records both. | `startWorkOrder` body |

**Form: Save work order** (modal, opened by *Save work order*; *Save work order* calls `updateWorkOrder`, *Cancel* sends nothing)

**Collects what `updateWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `assignedToPrincipalId`, `priority`, `dueAt`, `description`, `categoryId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | How the maintenance head confirms a `suggestWorkOrderAssignee` candidate (M17-13). | `updateWorkOrder` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | — | `updateWorkOrder` body |
| Required qualification codes `requiredQualificationCodes` | list of values (chips) | optional | — | at most 10 | — | — | `updateWorkOrder` body |
| Due at `dueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateWorkOrder` body |
| Description `description` | text area | optional | — | max length 5000 | — | — | `updateWorkOrder` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateWorkOrder` body |

**Form: Verify work order** (modal, opened by *Verify work order*; *Verify work order* calls `verifyWorkOrder`, *Cancel* sends nothing)

**Collects what `verifyWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | segmented control | required | — | Verified · Rejected | — | — | `verifyWorkOrder` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `verifyWorkOrder` body |

Errors to draw in the form: 403 Verifier is the technician who completed the work

**Sent by *Reject work order*** (`rejectWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Wrong skill · Not on shift · Wrong venue · Already in hand · Unsafe · Other | — | — | `rejectWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `rejectWorkOrder` body |

**Sent by *Cancel work order*** (`cancelWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | radio group | required | — | Raised in error · Duplicate · Superseded · No longer required | — | — | `cancelWorkOrder` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `cancelWorkOrder` body |
| Superseded by work order `supersededByWorkOrderId` | picker: choose a superseded by work order | optional | — | — | shows names, sends the id | — | `cancelWorkOrder` body |

**Sent by *Close work order*** (`closeWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Completed and verified · Not reproducible · Superseded by replacement · No longer applicable · Duplicate | — | — | `closeWorkOrder` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `closeWorkOrder` body |
| Duplicate of work order `duplicateOfWorkOrderId` | picker: choose a duplicate of work order | optional | — | — | shows names, sends the id | — | `closeWorkOrder` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every work order** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |

**The selected work order** (detail panel, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |
| Assigned to principal | the name it points at, never the id | — |
| Raised by principal | the name it points at, never the id | — |

**The work order** (detail panel, from `getWorkOrder`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |
| Assigned to principal | the name it points at, never the id | — |
| Raised by principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Accept work order (primary button) | `acceptWorkOrder` POST `/work-orders/{workOrderId}/accept` | — | WorkOrder | 409 Not assigned to this principal, or already accepted | works offline |
| Reject work order (destructive button) | `rejectWorkOrder` POST `/work-orders/{workOrderId}/reject` | inline | WorkOrder | 400 Validation failed | works offline |
| Attach work order evidence (secondary button) | `attachWorkOrderEvidence` POST `/work-orders/{workOrderId}/attachments` | inline | WorkOrderAttachment | — | works offline; opens modal first |
| Cancel work order (destructive button) | `cancelWorkOrder` POST `/work-orders/{workOrderId}/cancel` | inline | WorkOrder | 409 Work has started. | — |
| Close work order (destructive button) | `closeWorkOrder` POST `/work-orders/{workOrderId}/close` | inline | WorkOrder | — | — |
| Complete work order (secondary button) | `completeWorkOrder` POST `/work-orders/{workOrderId}/complete` | inline | WorkOrder | 400 Completion photographs required for this category and none supplied | works offline; opens modal first |
| Pause work order (secondary button) | `pauseWorkOrder` POST `/work-orders/{workOrderId}/pause` | inline | WorkOrder | 400 Validation failed | works offline; opens modal first |
| Record work order parts (secondary button) | `recordWorkOrderParts` POST `/work-orders/{workOrderId}/parts` | inline | WorkOrderDetail | 409 Insufficient stock | opens modal first |
| Record work order time (secondary button) | `recordWorkOrderTime` POST `/work-orders/{workOrderId}/time` | inline | WorkOrder | 400 Validation failed; 409 Action inconsistent with the current timer state | works offline; opens modal first |
| Resume work order (secondary button) | `resumeWorkOrder` POST `/work-orders/{workOrderId}/resume` | — | WorkOrder | — | works offline |
| Start work order (secondary button) | `startWorkOrder` POST `/work-orders/{workOrderId}/start` | inline | WorkOrder | — | works offline; opens modal first |
| Save work order (secondary button) | `updateWorkOrder` PATCH `/work-orders/{workOrderId}` | inline | WorkOrder | — | works offline; opens modal first |
| Verify work order (secondary button) | `verifyWorkOrder` POST `/work-orders/{workOrderId}/verify` | inline | WorkOrder | 403 Verifier is the technician who completed the work | opens modal first |

**Data it reads**: `listWorkOrders` (onLoad, List work orders)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-005` Task detail: *Completes a task*; carries `workOrderId`

**What opens over it**

- confirmDialog *Reject work order*: **Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task list this affects should be identified in the dialog, not just counted. **Collects what `rejectWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`.
- confirmDialog *Cancel work order*: **Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task list this affects should be identified in the dialog, not just counted. **Collects what `cancelWorkOrder` sends before it is called.** Required: `reason`. Optional: `note` …
- confirmDialog *Close work order*: **Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task list this affects should be identified in the dialog, not just counted. **Collects what `closeWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The task list list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the task list untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No task list yet. Offers Record work order parts (`recordWorkOrderParts`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the task list are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Local queue. Tasks completed offline sync on return |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Completion photographs required for this category and none supplied; 400 Validation failed; 409 Action inconsistent with the current timer state; 409 Insufficient stock |

#### Permissions

- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `acceptWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `rejectWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `attachWorkOrderEvidence` → `MAINTENANCE_EXECUTE` (operate) · staff
- `cancelWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `closeWorkOrder` → `MAINTENANCE_APPROVE` (operate) · staff
- `completeWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff
- `pauseWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `recordWorkOrderParts` → `WORK_ORDER_MANAGE` (configure) · staff
- `recordWorkOrderTime` → `WORK_ORDER_MANAGE` (configure) · staff
- `resumeWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `startWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `updateWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `verifyWorkOrder` → `WORK_ORDER_VERIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `WORK_ORDER_VIEW`, which `listWorkOrders` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 18.2.1 | Work Order Inbox - Users shall view assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.2 | Work Order Acceptance - Users shall accept assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.3 | Work Order Rejection - Users shall reject assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.4 | Work Order Start - Users shall start work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.5 | Work Order Pause - Users shall pause work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.6 | Work Order Completion - Users shall complete work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.7 | Work Order Closure - Authorized users shall close work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.5.1 | Photo Capture - Users shall capture photos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.2 | Video Capture - Users shall capture videos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.3 | Document Upload - Users shall upload documents. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.4 | Notes Management - Users shall record notes. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.5 | Signature Capture - Users shall capture signatures. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Work orders assigned to a technician must be visible on a technician-facing mobile app so field staff see assigned tasks and act directly from their device; execution shows a repair checklist, spare parts/tools consumed, a timeline (assigned, started, part requests) and a functional-test checklist before completion. *(client request · MoM 17 Sep 2026, 4.4 Work Order Management & Execution · DI-911)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*
- Employee mobile app: staff see their assigned bookings and tasks for the day, perform check-in/check-out and shift closing, and request swaps directly from the app — mirroring the booking info on their back-office profile. *(client request · MoM 26 Aug 2026, 4.5 Staff / Personnel; 4.9 AI Optimization, Mobile App & Analytics · DI-492)*
- Tasks are logged with priority and scheduled date/time; work order lifecycle Created → Assigned → In progress → Review → Closed with a timer showing resolution duration. *(client request · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-231)*
- Notifications categorised by type — action-required vs purely informational — and search across tasks and incidents. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-229)*
- In-system task assignment between staff (e.g. a cashier flagging something for a supervisor) without email or messaging apps. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-159)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-004` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 5: Works the task list → Assigned and available work
- Flow F12 *Asset fails and closes a queue*, step 2: Technician picks up the work order → Assigned, with the asset history attached
- Flow F65 *A task is raised, worked and handed over*, step 2: It appears on the list for whoever is free. → **Ordered by urgency and proximity**, not by arrival — a spill on the concourse outranks a bulb in a store room raised an hour earlier.

#### Acceptance for the design

- [ ] Every input above is drawn (45), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-004?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Accept work order, Reject work order, Attach work order evidence, Cancel work order, Close work order, Complete work order, Pause work order, Record work order parts, Record work order time, Resume work order, Start work order, Save work order, Verify work order.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-005`.
- [ ] Every gated control is gated: `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW`.
- [ ] The 6 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-005` Task detail

**Do the task and record that it was done.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `PROCUREMENT_REQUEST`, `PRODUCT_VIEW`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VERIFY`… (4 operate, 2 read, 1 configure); in the flows as supervisor, technician |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act |
| Offline | Editable offline. Findings and photos queue |
| Opens with | `workOrderId` (deepLink), `stockReservationId` (navigation) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/task-detail` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Cross-platform navigation removed 24 August**: BO-030, BO-078. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Removed 24 August**: createWorkOrder. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listWorkOrders`. | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | optional | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | — | Sends `?status=` to `listWorkOrders`. | `listWorkOrders` ?status |
| Priority | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Sends `?priority=` to `listWorkOrders`. | `listWorkOrders` ?priority |
| Asset id | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Sends `?assetId=` to `listWorkOrders`. | `listWorkOrders` ?assetId |
| Overdue only | toggle | optional | off | — | — | Sends `?overdueOnly=` to `listWorkOrders`. | `listWorkOrders` ?overdueOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Form: Start work order** (modal, opened by *Start work order*; *Start work order* calls `startWorkOrder`, *Cancel* sends nothing)

**Collects what `startWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `startedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Started at `startedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time where the job began offline. The server records both. | `startWorkOrder` body |

**Form: Pause work order** (modal, opened by *Pause work order*; *Pause work order* calls `pauseWorkOrder`, *Cancel* sends nothing)

**Collects what `pauseWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `requisitionId`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Awaiting parts · Awaiting permit · Awaiting outage window · Awaiting specialist · End of shift · Safety concern · Other | — | — | `pauseWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `pauseWorkOrder` body |
| Requisition `requisitionId` | picker: choose a requisition | optional | — | — | shows names, sends the id | Where a part was ordered, so the two are linked. | `pauseWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Complete work order** (modal, opened by *Complete work order*; *Complete work order* calls `completeWorkOrder`, *Cancel* sends nothing)

**Collects what `completeWorkOrder` sends before it is called.** Required: `resolution`, `recordedAt`. Optional: `resolutionCode`, `attachmentRefs`, `followUpRequired`, `followUpNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resolution `resolution` | text area | required | — | min length 3; max length 5000 | — | — | `completeWorkOrder` body |
| Resolution code `resolutionCode` | select | optional | — | Repaired · Part replaced · Adjusted · Cleaned · No fault found · Referred external · Replaced · Deferred | — | — | `completeWorkOrder` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `completeWorkOrder` body |
| Follow up required `followUpRequired` | toggle | optional | off | — | — | — | `completeWorkOrder` body |
| Follow up note `followUpNote` | text area | optional | — | max length 1000 | — | — | `completeWorkOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `completeWorkOrder` body |

Errors to draw in the form: 400 Completion photographs required for this category and none supplied

**Form: Attach work order evidence** (modal, opened by *Attach work order evidence*; *Attach work order evidence* calls `attachWorkOrderEvidence`, *Cancel* sends nothing)

**Collects what `attachWorkOrderEvidence` sends before it is called.** Required: `kind`. Optional: `assetRef`, `text`, `capturedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Photo · Video · Document · Note · Signature | — | — | `attachWorkOrderEvidence` body |
| Asset ref `assetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | In the media store | `attachWorkOrderEvidence` body |
| Text `text` | text area | optional | — | max length 4000 | — | Where the kind is a note | `attachWorkOrderEvidence` body |
| Captured at `capturedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `attachWorkOrderEvidence` body |
| Stage `stage` | radio group | optional | — | Before · During · After · Sign off | — | — | `attachWorkOrderEvidence` body |

**Form: Record work order parts** (modal, opened by *Record work order parts*; *Record work order parts* calls `recordWorkOrderParts`, *Cancel* sends nothing)

**Collects what `recordWorkOrderParts` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `recordWorkOrderParts` body |
| Inventory item `lines[].inventoryItemId` | picker: choose an inventory item | required | — | — | shows names, sends the id | — | `recordWorkOrderParts` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `recordWorkOrderParts` body |
| Location `lines[].locationId` | picker: choose a location | optional | — | — | shows names, sends the id | — | `recordWorkOrderParts` body |

Errors to draw in the form: 409 Insufficient stock

**Form: Record work order time** (modal, opened by *Record work order time*; *Record work order time* calls `recordWorkOrderTime`, *Cancel* sends nothing)

**Collects what `recordWorkOrderTime` sends before it is called.** Required: `id`, `action`, `recordedAt`. Optional: `pauseReason`, `note`. **When the pause reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordWorkOrderTime` body |
| Action `action` | radio group | required | — | Start · Pause · Resume · Stop | — | — | `recordWorkOrderTime` body |
| Pause reason `pauseReason` | select | optional | — | Awaiting parts · Awaiting access · Awaiting approval · End of shift · Reassigned · Other | — | — | `recordWorkOrderTime` body |
| Note `note` | text area | optional | — | max length 500; Required where the pause reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the pause reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones … | `recordWorkOrderTime` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordWorkOrderTime` body |

Errors to draw in the form: 400 Validation failed; 409 Action inconsistent with the current timer state

**Form: Save work order** (modal, opened by *Save work order*; *Save work order* calls `updateWorkOrder`, *Cancel* sends nothing)

**Collects what `updateWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `assignedToPrincipalId`, `priority`, `dueAt`, `description`, `categoryId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | How the maintenance head confirms a `suggestWorkOrderAssignee` candidate (M17-13). | `updateWorkOrder` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | — | `updateWorkOrder` body |
| Required qualification codes `requiredQualificationCodes` | list of values (chips) | optional | — | at most 10 | — | — | `updateWorkOrder` body |
| Due at `dueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateWorkOrder` body |
| Description `description` | text area | optional | — | max length 5000 | — | — | `updateWorkOrder` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateWorkOrder` body |

**Form: Verify work order** (modal, opened by *Verify work order*; *Verify work order* calls `verifyWorkOrder`, *Cancel* sends nothing)

**Collects what `verifyWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | segmented control | required | — | Verified · Rejected | — | — | `verifyWorkOrder` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `verifyWorkOrder` body |

Errors to draw in the form: 403 Verifier is the technician who completed the work

**Sent by *Cancel work order*** (`cancelWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | radio group | required | — | Raised in error · Duplicate · Superseded · No longer required | — | — | `cancelWorkOrder` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `cancelWorkOrder` body |
| Superseded by work order `supersededByWorkOrderId` | picker: choose a superseded by work order | optional | — | — | shows names, sends the id | — | `cancelWorkOrder` body |

**Sent by *Close work order*** (`closeWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Completed and verified · Not reproducible · Superseded by replacement · No longer applicable · Duplicate | — | — | `closeWorkOrder` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `closeWorkOrder` body |
| Duplicate of work order `duplicateOfWorkOrderId` | picker: choose a duplicate of work order | optional | — | — | shows names, sends the id | — | `closeWorkOrder` body |

**Sent by *Reject work order*** (`rejectWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Wrong skill · Not on shift · Wrong venue · Already in hand · Unsafe · Other | — | — | `rejectWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `rejectWorkOrder` body |

**Sent by *Reserve parts*** (`createStockReservation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | optional | — | — | shows names, sends the id | — | `createStockReservation` body |
| Item `itemId` | picker: choose an item | required | — | — | shows names, sends the id | — | `createStockReservation` body |
| Location `locationId` | picker: choose a location | required | — | — | shows names, sends the id | — | `createStockReservation` body |
| Quantity `quantity` | number field | required | — | more than 0 | — | — | `createStockReservation` body |
| Source type `sourceType` | radio group | required | — | Work order · Rental agreement · Order · Transfer · Other | — | What a stock reservation is for (decided 17 September, M17-02; `rentalAgreement` is the existing use from `rental.agreement_item`). | `createStockReservation` body |
| Source `sourceId` | picker: choose a source | required | — | — | shows names, sends the id | The id of what the stock is reserved for: a work order, a rental agreement or an order. | `createStockReservation` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockReservation` body |
| Released at `releasedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createStockReservation` body |

**Sent by *Release reserved parts*** (`releaseStockReservation`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 300 | — | — | `releaseStockReservation` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every work order** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |

**The selected work order** (detail panel, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |
| Assigned to principal | the name it points at, never the id | — |
| Raised by principal | the name it points at, never the id | — |

**The work order** (detail panel, from `getWorkOrder`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |
| Assigned to principal | the name it points at, never the id | — |
| Raised by principal | the name it points at, never the id | — |

**Parts reserved for this task** (data table, from `listStockReservations`): **Reserved in the general inventory** (decided 17 September, M17-02), `sourceType` workOrder. *Record work order parts* issues from the reservation first. Needs signal: stock depletes in real time, so the reserve action is hidden offline.

| Shows | Format | Notes |
|---|---|---|
| Item | the name it points at, never the id | — |
| Quantity | 1,234.5 | — |
| Status | chip: Active, Consumed, Released, Expired | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Start work order (primary button) | `startWorkOrder` POST `/work-orders/{workOrderId}/start` | inline | WorkOrder | — | works offline; opens modal first |
| Pause work order (secondary button) | `pauseWorkOrder` POST `/work-orders/{workOrderId}/pause` | inline | WorkOrder | 400 Validation failed | works offline; opens modal first |
| Complete work order (secondary button) | `completeWorkOrder` POST `/work-orders/{workOrderId}/complete` | inline | WorkOrder | 400 Completion photographs required for this category and none supplied | works offline; opens modal first |
| Accept work order (secondary button) | `acceptWorkOrder` POST `/work-orders/{workOrderId}/accept` | — | WorkOrder | 409 Not assigned to this principal, or already accepted | works offline |
| Attach work order evidence (secondary button) | `attachWorkOrderEvidence` POST `/work-orders/{workOrderId}/attachments` | inline | WorkOrderAttachment | — | works offline; opens modal first |
| Cancel work order (destructive button) | `cancelWorkOrder` POST `/work-orders/{workOrderId}/cancel` | inline | WorkOrder | 409 Work has started. | — |
| Close work order (destructive button) | `closeWorkOrder` POST `/work-orders/{workOrderId}/close` | inline | WorkOrder | — | — |
| Record work order parts (secondary button) | `recordWorkOrderParts` POST `/work-orders/{workOrderId}/parts` | inline | WorkOrderDetail | 409 Insufficient stock | opens modal first |
| Record work order time (secondary button) | `recordWorkOrderTime` POST `/work-orders/{workOrderId}/time` | inline | WorkOrder | 400 Validation failed; 409 Action inconsistent with the current timer state | works offline; opens modal first |
| Reject work order (destructive button) | `rejectWorkOrder` POST `/work-orders/{workOrderId}/reject` | inline | WorkOrder | 400 Validation failed | works offline |
| Resume work order (secondary button) | `resumeWorkOrder` POST `/work-orders/{workOrderId}/resume` | — | WorkOrder | — | works offline |
| Save work order (secondary button) | `updateWorkOrder` PATCH `/work-orders/{workOrderId}` | inline | WorkOrder | — | works offline; opens modal first |
| Verify work order (secondary button) | `verifyWorkOrder` POST `/work-orders/{workOrderId}/verify` | inline | WorkOrder | 403 Verifier is the technician who completed the work | opens modal first |
| Reserve parts (secondary button) | `createStockReservation` POST `/stock-reservations` | InventoryStockReservation | InventoryStockReservation | 400 Validation failed; 409 Not enough free stock at the location. | — |
| Release reserved parts (secondary button) | `releaseStockReservation` POST `/stock-reservations/{stockReservationId}/release` | inline | InventoryStockReservation | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The reservation is not `active`. | — |

**Data it reads**: `listWorkOrders` (onLoad, List work orders)

**Where the user goes next**

- → `EMP-007` Handover notes: *Writes handover notes*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `BO-078` Requisitions: *Raises a requisition against the work order*; calls `pauseWorkOrder`
- → `BO-030` Work Order Verification: *Supervisor verifies*; carries `workOrderId`; calls `completeWorkOrder`

**What opens over it**

- confirmDialog *Cancel work order*: **Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task this affects should be identified in the dialog, not just counted. **Collects what `cancelWorkOrder` sends before it is called.** Required: `reason`. Optional: `note` …
- confirmDialog *Close work order*: **Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task this affects should be identified in the dialog, not just counted. **Collects what `closeWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note` …
- confirmDialog *Reject work order*: **Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A task this affects should be identified in the dialog, not just counted. **Collects what `rejectWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The task list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the task untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No task yet. Offers Record work order parts (`recordWorkOrderParts`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the task are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORK_ORDER_VIEW`, which `getWorkOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Editable offline. Findings and photos queue |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Completion photographs required for this category and none supplied; 400 Validation failed; 409 Action inconsistent with the current timer state; 409 Insufficient stock |

#### Permissions

- `listStockReservations` → `PRODUCT_VIEW` (read) · staff
- `createStockReservation` → `PROCUREMENT_REQUEST` (operate) · staff
- `releaseStockReservation` → `PROCUREMENT_REQUEST` (operate) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff
- `startWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `pauseWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `completeWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `acceptWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `attachWorkOrderEvidence` → `MAINTENANCE_EXECUTE` (operate) · staff
- `cancelWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `closeWorkOrder` → `MAINTENANCE_APPROVE` (operate) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `recordWorkOrderParts` → `WORK_ORDER_MANAGE` (configure) · staff
- `recordWorkOrderTime` → `WORK_ORDER_MANAGE` (configure) · staff
- `rejectWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `resumeWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `updateWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `verifyWorkOrder` → `WORK_ORDER_VERIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `WORK_ORDER_VIEW`, which `getWorkOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

24 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 17.4.8 | Work Order Audit Trail - System shall maintain work order audit logs. | Maintenance & Safety Management | CONTRACTED | `getWorkOrder` |
| 18.2.1 | Work Order Inbox - Users shall view assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.2 | Work Order Acceptance - Users shall accept assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.3 | Work Order Rejection - Users shall reject assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.4 | Work Order Start - Users shall start work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.5 | Work Order Pause - Users shall pause work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.6 | Work Order Completion - Users shall complete work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.7 | Work Order Closure - Authorized users shall close work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.5.1 | Photo Capture - Users shall capture photos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.2 | Video Capture - Users shall capture videos. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.3 | Document Upload - Users shall upload documents. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| 18.5.4 | Notes Management - Users shall record notes. | Employee Mobile App & AI Assistant | CONTRACTED | `attachWorkOrderEvidence` |
| … 12 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Work-order parts are reserved in the general inventory; the reserve action is hidden offline, and a refusal for short stock names the part. *(agreed · MoM 17 Sep 2026, M17-02 · DI-925)*
- Work orders assigned to a technician must be visible on a technician-facing mobile app so field staff see assigned tasks and act directly from their device; execution shows a repair checklist, spare parts/tools consumed, a timeline (assigned, started, part requests) and a functional-test checklist before completion. *(client request · MoM 17 Sep 2026, 4.4 Work Order Management & Execution · DI-911)*
- Maintenance work orders are assigned to the relevant department/person and are visible on the staff mobile app; repair workspace tracks cost; annual maintenance history shows lifecycle cost per item. *(client request · MoM 9 Sep 2026, 4.10 Rental Maintenance, Asset Lifecycle & Command Center Reporting · DI-769)*
- Tasks are logged with priority and scheduled date/time; work order lifecycle Created → Assigned → In progress → Review → Closed with a timer showing resolution duration. *(client request · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-231)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-005` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 6: Completes a task → With findings, not just a tick
- Flow F12 *Asset fails and closes a queue*, step 3: Works and records findings → Parts and time recorded. Completed, not yet in service
- Flow F15 *A part is needed and ordered*, step 1: Pauses the work order, reason: awaiting parts → **The reason decides the state.** awaitingParts is chased by ordering; paused is chased by asking someone
- Flow F15 *A part is needed and ordered*, step 5: The technician resumes → The part is consumed and the movement posts
- Flow F65 *A task is raised, worked and handed over*, step 3: Someone accepts it and works it. → **Accepting is the lock.** Two stewards walking to the same task is the failure the list exists to prevent.
- Flow F65 *A task is raised, worked and handed over*, step 4: It is completed with evidence. → **A photograph closes a spill; a signature closes an inspection.** The evidence kind is the task kind.
- Flow F08 branch at step 6 (requiresStaff): when Task is a safety incident, EMP-026 and EMP-027. A different severity, a different escalation, and it must reach a supervisor rather than sit in a list.
- Flow F08 branch at step 6 (recoverable): when Task needs a part that is not in stock, Blocks on awaitingParts rather than paused. **The distinction matters** — one is a person, the other is supply, and only one is chased by ordering something.
- Flow F12 branch at step 3 (requiresStaff): when Part not in stock, Blocks on awaitingParts, and a requisition is raised. **The queue stays closed** — an asset waiting for a part is not an asset in service.
- Flow F12 branch at step 3 (recoverable): when Technician has no signal in the plant room, Findings queue locally. The work order state moves on sync, and the queue stays closed until it does.
- Flow F12 branch at step 3 (recoverable): when Second fault found during the work, A new work order linked to the first rather than expanding the original. The asset history has to show both.

#### Acceptance for the design

- [ ] Every input above is drawn (54), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (47 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-005?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Start work order, Pause work order, Complete work order, Accept work order, Attach work order evidence, Cancel work order, Close work order, Record work order parts, Record work order time, Reject work order, Resume work order, Save work order, Verify work order, Reserve parts, Release reserved parts.
- [ ] Every transition is wired: `EMP-007`, `EMP-001`, `EMP-002`, `EMP-003`, `BO-078`, `BO-030`.
- [ ] Every gated control is gated: `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `PROCUREMENT_REQUEST`, `PRODUCT_VIEW`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-006` Raise a task

**Report something without finding a manager.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 1 · needs the `maintenance` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW` (3 operate, 1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listWorkOrders` reads the population and `getWorkOrder` reads one of them — list, select, act |
| Offline | Queues locally. A task raised in a plant room must not need signal |
| Opens with | `workOrderId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/raise-a-task` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal id | picker: choose an assigned to principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?assignedToPrincipalId=` to `listWorkOrders`. | `listWorkOrders` ?assignedToPrincipalId |
| Status | select | optional | — | Open · Assigned · In progress · Paused · Awaiting parts · Completed · Verified · Closed · Cancelled | — | Sends `?status=` to `listWorkOrders`. | `listWorkOrders` ?status |
| Priority | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Sends `?priority=` to `listWorkOrders`. | `listWorkOrders` ?priority |
| Asset id | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | Sends `?assetId=` to `listWorkOrders`. | `listWorkOrders` ?assetId |
| Overdue only | toggle | optional | off | — | — | Sends `?overdueOnly=` to `listWorkOrders`. | `listWorkOrders` ?overdueOnly |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `listWorkOrders` ?from |
| To | date and time picker | — | — | `listWorkOrders` ?to |
| Category | picker: choose a category | — | — | `listWorkOrders` ?categoryId |

**Form: Create work order** (modal, opened by *Create work order*; *Create work order* calls `createWorkOrder`, *Cancel* sends nothing)

**Collects what `createWorkOrder` sends before it is called.** Required: `id`, `title`, `venueId`, `priority`, `recordedAt`. Optional: `description`, `assetId`, `locationDescription`, `kind`, `categoryId`, `assignedToPrincipalId`, `dueAt`, `attachmentRefs`, `takeAssetOutOfService`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Title `title` | text field | required | — | max length 200 | — | — | `createWorkOrder` body |
| Description `description` | text area | optional | — | max length 5000 | — | — | `createWorkOrder` body |
| Venue `venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Asset `assetId` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | `createWorkOrder` body |
| Location description `locationDescription` | text area | optional | — | max length 500 | — | — | `createWorkOrder` body |
| Kind `kind` | radio group | optional | Corrective | Corrective · Planned · Inspection follow up · Incident corrective · Improvement | — | — | `createWorkOrder` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | Optional since 29 September (M17-01). Sent, it is `manual` and wins. | `createWorkOrder` body |
| Fault assessment `faultAssessment` | group | optional | — | — | — | What the person raising a fault says about it, which the priority score reads (M17-01). | `createWorkOrder` body |
| Safety risk `faultAssessment.safetyRisk` | toggle | optional | off | — | — | — | `createWorkOrder` body |
| Guest impact `faultAssessment.guestImpact` | segmented control | optional | None | None · Degraded · Closed | — | — | `createWorkOrder` body |
| Required qualification codes `requiredQualificationCodes` | list of values (chips) | optional | — | at most 10 | — | Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13). | `createWorkOrder` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | — | `createWorkOrder` body |
| Due at `dueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createWorkOrder` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | Photo-first. Expected at creation, not added later from memory. | `createWorkOrder` body |
| Take asset out of service `takeAssetOutOfService` | toggle | optional | off | — | — | Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action. | `createWorkOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Attach work order evidence** (modal, opened by *Attach work order evidence*; *Attach work order evidence* calls `attachWorkOrderEvidence`, *Cancel* sends nothing)

**Collects what `attachWorkOrderEvidence` sends before it is called.** Required: `kind`. Optional: `assetRef`, `text`, `capturedAt`, `stage`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Photo · Video · Document · Note · Signature | — | — | `attachWorkOrderEvidence` body |
| Asset ref `assetRef` | upload, or pick from the media library | optional | — | — | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | In the media store | `attachWorkOrderEvidence` body |
| Text `text` | text area | optional | — | max length 4000 | — | Where the kind is a note | `attachWorkOrderEvidence` body |
| Captured at `capturedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `attachWorkOrderEvidence` body |
| Stage `stage` | radio group | optional | — | Before · During · After · Sign off | — | — | `attachWorkOrderEvidence` body |

**Form: Complete work order** (modal, opened by *Complete work order*; *Complete work order* calls `completeWorkOrder`, *Cancel* sends nothing)

**Collects what `completeWorkOrder` sends before it is called.** Required: `resolution`, `recordedAt`. Optional: `resolutionCode`, `attachmentRefs`, `followUpRequired`, `followUpNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Resolution `resolution` | text area | required | — | min length 3; max length 5000 | — | — | `completeWorkOrder` body |
| Resolution code `resolutionCode` | select | optional | — | Repaired · Part replaced · Adjusted · Cleaned · No fault found · Referred external · Replaced · Deferred | — | — | `completeWorkOrder` body |
| Attachment refs `attachmentRefs` | list of values (chips) | optional | — | — | — | — | `completeWorkOrder` body |
| Follow up required `followUpRequired` | toggle | optional | off | — | — | — | `completeWorkOrder` body |
| Follow up note `followUpNote` | text area | optional | — | max length 1000 | — | — | `completeWorkOrder` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `completeWorkOrder` body |

Errors to draw in the form: 400 Completion photographs required for this category and none supplied

**Form: Pause work order** (modal, opened by *Pause work order*; *Pause work order* calls `pauseWorkOrder`, *Cancel* sends nothing)

**Collects what `pauseWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`, `requisitionId`. **When the reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Awaiting parts · Awaiting permit · Awaiting outage window · Awaiting specialist · End of shift · Safety concern · Other | — | — | `pauseWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `pauseWorkOrder` body |
| Requisition `requisitionId` | picker: choose a requisition | optional | — | — | shows names, sends the id | Where a part was ordered, so the two are linked. | `pauseWorkOrder` body |

Errors to draw in the form: 400 Validation failed

**Form: Record work order parts** (modal, opened by *Record work order parts*; *Record work order parts* calls `recordWorkOrderParts`, *Cancel* sends nothing)

**Collects what `recordWorkOrderParts` sends before it is called.** Required: `lines`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Lines `lines` | repeatable rows | required | — | at least 1 | — | — | `recordWorkOrderParts` body |
| Inventory item `lines[].inventoryItemId` | picker: choose an inventory item | required | — | — | shows names, sends the id | — | `recordWorkOrderParts` body |
| Quantity `lines[].quantity` | number field | required | — | min 0 | — | — | `recordWorkOrderParts` body |
| Location `lines[].locationId` | picker: choose a location | optional | — | — | shows names, sends the id | — | `recordWorkOrderParts` body |

Errors to draw in the form: 409 Insufficient stock

**Form: Record work order time** (modal, opened by *Record work order time*; *Record work order time* calls `recordWorkOrderTime`, *Cancel* sends nothing)

**Collects what `recordWorkOrderTime` sends before it is called.** Required: `id`, `action`, `recordedAt`. Optional: `pauseReason`, `note`. **When the pause reason is Other, `note` is required** — the operation refuses 400 without it (decided 28 September, audit R222). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `recordWorkOrderTime` body |
| Action `action` | radio group | required | — | Start · Pause · Resume · Stop | — | — | `recordWorkOrderTime` body |
| Pause reason `pauseReason` | select | optional | — | Awaiting parts · Awaiting access · Awaiting approval · End of shift · Reassigned · Other | — | — | `recordWorkOrderTime` body |
| Note `note` | text area | optional | — | max length 500; Required where the pause reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the pause reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones … | `recordWorkOrderTime` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordWorkOrderTime` body |

Errors to draw in the form: 400 Validation failed; 409 Action inconsistent with the current timer state

**Form: Start work order** (modal, opened by *Start work order*; *Start work order* calls `startWorkOrder`, *Cancel* sends nothing)

**Collects what `startWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `startedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Started at `startedAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Device time where the job began offline. The server records both. | `startWorkOrder` body |

**Form: Save work order** (modal, opened by *Save work order*; *Save work order* calls `updateWorkOrder`, *Cancel* sends nothing)

**Collects what `updateWorkOrder` sends before it is called.** Nothing in the body is required. Optional: `assignedToPrincipalId`, `priority`, `dueAt`, `description`, `categoryId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Assigned to principal `assignedToPrincipalId` | picker: choose an assigned to principal | optional | — | — | shows names, sends the id | How the maintenance head confirms a `suggestWorkOrderAssignee` candidate (M17-13). | `updateWorkOrder` body |
| Priority `priority` | radio group | optional | — | Low · Normal · High · Urgent · Emergency | — | — | `updateWorkOrder` body |
| Required qualification codes `requiredQualificationCodes` | list of values (chips) | optional | — | at most 10 | — | — | `updateWorkOrder` body |
| Due at `dueAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updateWorkOrder` body |
| Description `description` | text area | optional | — | max length 5000 | — | — | `updateWorkOrder` body |
| Category `categoryId` | picker: choose a category | optional | — | — | shows names, sends the id | — | `updateWorkOrder` body |

**Form: Verify work order** (modal, opened by *Verify work order*; *Verify work order* calls `verifyWorkOrder`, *Cancel* sends nothing)

**Collects what `verifyWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | segmented control | required | — | Verified · Rejected | — | — | `verifyWorkOrder` body |
| Note `note` | text area | optional | — | max length 1000 | — | — | `verifyWorkOrder` body |

Errors to draw in the form: 403 Verifier is the technician who completed the work

**Sent by *Cancel work order*** (`cancelWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | radio group | required | — | Raised in error · Duplicate · Superseded · No longer required | — | — | `cancelWorkOrder` body |
| Note `note` | text area | optional | — | max length 300 | — | — | `cancelWorkOrder` body |
| Superseded by work order `supersededByWorkOrderId` | picker: choose a superseded by work order | optional | — | — | shows names, sends the id | — | `cancelWorkOrder` body |

**Sent by *Close work order*** (`closeWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Outcome `outcome` | radio group | required | — | Completed and verified · Not reproducible · Superseded by replacement · No longer applicable · Duplicate | — | — | `closeWorkOrder` body |
| Note `note` | text area | optional | — | max length 500 | — | — | `closeWorkOrder` body |
| Duplicate of work order `duplicateOfWorkOrderId` | picker: choose a duplicate of work order | optional | — | — | shows names, sends the id | — | `closeWorkOrder` body |

**Sent by *Reject work order*** (`rejectWorkOrder`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | select | required | — | Wrong skill · Not on shift · Wrong venue · Already in hand · Unsafe · Other | — | — | `rejectWorkOrder` body |
| Note `note` | text area | optional | — | max length 300; Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real reasons. | — | Required where the reason is `other` (decided 28 September, audit R222): `other` with no note is refused `400`, and the notes are reviewed quarterly so the common ones become real … | `rejectWorkOrder` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every work order** (data table, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |

**The selected work order** (detail panel, from `listWorkOrders`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |
| Assigned to principal | the name it points at, never the id | — |
| Raised by principal | the name it points at, never the id | — |

**The work order** (detail panel, from `getWorkOrder`)

| Shows | Format | Notes |
|---|---|---|
| Downtime minutes | 1,234 | Measured from out-of-service to back-in-service, not from work start to work end. |
| Root cause | chip: Wear and tear, Operator error, Guest damage, Manufacturing defect, Environmental … | Structured, because free text cannot be counted. *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault … |
| Root cause note | text | — |
| Escalated at | 1 Oct 2026, 14:30 | — |
| Escalation level | 1,234 | Escalation is a clock, not a decision. A work order on a ride nobody has accepted after twenty minutes escalates itself, because the … |
| ID | the name it points at, never the id | — |
| Work order number | text | Server-assigned: the venue prefix plus a sequence per venue (decided 28 September, audit R152). |
| Title | text | — |
| Venue | the name it points at, never the id | — |
| Asset | the image or video | — |
| Asset name | text | The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record … |
| Status | chip: Open, Assigned, In progress, Paused, Awaiting parts, Completed… | — |
| Priority | chip: Low, Normal, High, Urgent, Emergency | — |
| Kind | chip: Corrective, Planned, Inspection follow up, Incident corrective, Improvement | — |
| Assigned to principal | the name it points at, never the id | — |
| Raised by principal | the name it points at, never the id | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Confirm (confirm dialog) | navigation or local | — | — | — | — |
| Create work order (primary button) | `createWorkOrder` POST `/work-orders` | CreateWorkOrderRequest | WorkOrder | 400 Validation failed | works offline; opens modal first |
| Accept work order (secondary button) | `acceptWorkOrder` POST `/work-orders/{workOrderId}/accept` | — | WorkOrder | 409 Not assigned to this principal, or already accepted | works offline |
| Attach work order evidence (secondary button) | `attachWorkOrderEvidence` POST `/work-orders/{workOrderId}/attachments` | inline | WorkOrderAttachment | — | works offline; opens modal first |
| Cancel work order (destructive button) | `cancelWorkOrder` POST `/work-orders/{workOrderId}/cancel` | inline | WorkOrder | 409 Work has started. | — |
| Close work order (destructive button) | `closeWorkOrder` POST `/work-orders/{workOrderId}/close` | inline | WorkOrder | — | — |
| Complete work order (secondary button) | `completeWorkOrder` POST `/work-orders/{workOrderId}/complete` | inline | WorkOrder | 400 Completion photographs required for this category and none supplied | works offline; opens modal first |
| Pause work order (secondary button) | `pauseWorkOrder` POST `/work-orders/{workOrderId}/pause` | inline | WorkOrder | 400 Validation failed | works offline; opens modal first |
| Record work order parts (secondary button) | `recordWorkOrderParts` POST `/work-orders/{workOrderId}/parts` | inline | WorkOrderDetail | 409 Insufficient stock | opens modal first |
| Record work order time (secondary button) | `recordWorkOrderTime` POST `/work-orders/{workOrderId}/time` | inline | WorkOrder | 400 Validation failed; 409 Action inconsistent with the current timer state | works offline; opens modal first |
| Reject work order (destructive button) | `rejectWorkOrder` POST `/work-orders/{workOrderId}/reject` | inline | WorkOrder | 400 Validation failed | works offline |
| Resume work order (secondary button) | `resumeWorkOrder` POST `/work-orders/{workOrderId}/resume` | — | WorkOrder | — | works offline |
| Start work order (secondary button) | `startWorkOrder` POST `/work-orders/{workOrderId}/start` | inline | WorkOrder | — | works offline; opens modal first |
| Save work order (secondary button) | `updateWorkOrder` PATCH `/work-orders/{workOrderId}` | inline | WorkOrder | — | works offline; opens modal first |
| Verify work order (secondary button) | `verifyWorkOrder` POST `/work-orders/{workOrderId}/verify` | inline | WorkOrder | 403 Verifier is the technician who completed the work | opens modal first |

**Data it reads**: `listWorkOrders` (onLoad, List work orders)

**Where the user goes next**

- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*
- → `EMP-004` Task list: *It appears on the list for whoever is free*; carries `workOrderId`; calls `createWorkOrder`

**What opens over it**

- confirmDialog *Cancel work order*: **Names what `cancelWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted. **Collects what `cancelWorkOrder` sends before it is called.** Required: `reason`. Optional: `note` …
- confirmDialog *Close work order*: **Names what `closeWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted. **Collects what `closeWorkOrder` sends before it is called.** Required: `outcome`. Optional: `note` …
- confirmDialog *Reject work order*: **Names what `rejectWorkOrder` changes and what it leaves alone**, in the consequence rather than the verb. A raise task this affects should be identified in the dialog, not just counted. **Collects what `rejectWorkOrder` sends before it is called.** Required: `reason`. Optional: `note`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The raise task list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the raise task untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No raise task yet. Offers Create work order (`createWorkOrder`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on assignedToPrincipalId, status, priority, assetId, overdueOnly and the raise task are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORK_ORDER_VIEW`, which `getWorkOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Queues locally. A task raised in a plant room must not need signal |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Completion photographs required for this category and none supplied; 400 Validation failed; 409 Action inconsistent with the current timer state; 409 Insufficient stock |

#### Permissions

- `createWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `acceptWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `attachWorkOrderEvidence` → `MAINTENANCE_EXECUTE` (operate) · staff
- `cancelWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `closeWorkOrder` → `MAINTENANCE_APPROVE` (operate) · staff
- `completeWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `getWorkOrder` → `WORK_ORDER_VIEW` (read) · staff
- `listWorkOrders` → `WORK_ORDER_VIEW` (read) · staff
- `pauseWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `recordWorkOrderParts` → `WORK_ORDER_MANAGE` (configure) · staff
- `recordWorkOrderTime` → `WORK_ORDER_MANAGE` (configure) · staff
- `rejectWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `resumeWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `startWorkOrder` → `MAINTENANCE_EXECUTE` (operate) · staff
- `updateWorkOrder` → `WORK_ORDER_MANAGE` (configure) · staff
- `verifyWorkOrder` → `WORK_ORDER_VERIFY` (operate) · staff

**A refused user sees:** Shown when the caller lacks `WORK_ORDER_VIEW`, which `getWorkOrder` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

33 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 16.5.25 | Corrective Maintenance - System shall support corrective maintenance tracking. | Device Management | CONTRACTED | `createWorkOrder` |
| 16.5.26 | Maintenance Work Orders - System shall support device maintenance work orders. | Device Management | CONTRACTED | `createWorkOrder` |
| 17.3.1 | Maintenance Requests - System shall support maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.2 | Breakdown Management - System shall support equipment breakdown management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.3.3 | Emergency Maintenance - System shall support emergency maintenance requests. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.1 | Work Order Creation - System shall support work order creation. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.2 | Work Order Assignment - System shall support work order assignment. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.3 | Work Order Prioritization - System shall support work order prioritization. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 17.4.4 | Work Order Status Management - System shall support work order lifecycle management. | Maintenance & Safety Management | CONTRACTED | `createWorkOrder` |
| 18.2.1 | Work Order Inbox - Users shall view assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.2 | Work Order Acceptance - Users shall accept assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| 18.2.3 | Work Order Rejection - Users shall reject assigned work orders. | Employee Mobile App & AI Assistant | CONTRACTED | `acceptWorkOrder` |
| … 21 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Photo capture is the primary way to log faulty assets without barcodes (pipes, valves, lighting); barcode scan is secondary. *(agreed · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-232)*
- Tasks are logged with priority and scheduled date/time; work order lifecycle Created → Assigned → In progress → Review → Closed with a timer showing resolution duration. *(client request · MoM 10 Aug 2026, 5.3 Task, Work Order & Asset Management · DI-231)*
- Quick-create for maintenance, IT support, cleaning/safety/security, store, purchase and leave requests. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-230)*
- In-system task assignment between staff (e.g. a cashier flagging something for a supervisor) without email or messaging apps. *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-159)*

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-006` · status **notStarted** · provenance generated
- Flow F65 *A task is raised, worked and handed over*, step 1: A steward raises a task. → **Raised in seconds, from where the problem is.** A form that takes a minute is a spill somebody steps around instead.

#### Acceptance for the design

- [ ] Every input above is drawn (63), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (44 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-006?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Confirm, Create work order, Accept work order, Attach work order evidence, Cancel work order, Close work order, Complete work order, Pause work order, Record work order parts, Record work order time, Reject work order, Resume work order, Start work order, Save work order, Verify work order.
- [ ] Every transition is wired: `EMP-001`, `EMP-002`, `EMP-003`, `EMP-004`.
- [ ] Every gated control is gated: `MAINTENANCE_APPROVE`, `MAINTENANCE_EXECUTE`, `WORK_ORDER_MANAGE`, `WORK_ORDER_VERIFY`, `WORK_ORDER_VIEW`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-007` Handover notes

**Tell the next shift what they are walking into.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW` (1 configure, 1 read); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAnnouncements` reads the population and `getAnnouncementReach` reads one of them — list, select, act |
| Offline | Editable offline and synced at end of shift |
| Opens with | `announcementId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/operations/handover-notes` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Unacknowledged only | toggle | optional | — | — | — | Sends `?unacknowledgedOnly=` to `listAnnouncements`. | `listAnnouncements` ?unacknowledgedOnly |

**Form: Publish announcement** (modal, opened by *Publish announcement*; *Publish announcement* calls `publishAnnouncement`, *Cancel* sends nothing)

**Collects what `publishAnnouncement` sends before it is called.** Required: `title`, `body`, `kind`, `publishedAt`. Optional: `id`, `venueIds`, `departmentIds`, `roleIds`, `requiresAcknowledgement`, `expiresAt`, `publishedByPrincipalId`, `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text field | required | — | max length 140 | — | — | `publishAnnouncement` body |
| Body `body` | text area | required | — | max length 4000 | — | — | `publishAnnouncement` body |
| Kind `kind` | radio group | required | — | Operational · Safety · Emergency · Hr · Celebration | — | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission. | `publishAnnouncement` body |
| Venues `venueIds` | multi-picker: choose venues | optional | — | — | — | — | `publishAnnouncement` body |
| Departments `departmentIds` | multi-picker: choose departments | optional | — | — | — | — | `publishAnnouncement` body |
| Roles `roleIds` | multi-picker: choose roles | optional | — | — | — | — | `publishAnnouncement` body |
| Requires acknowledgement `requiresAcknowledgement` | toggle | optional | — | — | — | — | `publishAnnouncement` body |
| Delivery channels `deliveryChannels` | multi-select chips | optional | In app, Push | In app · Push | — | How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). | `publishAnnouncement` body |
| Expires at `expiresAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishAnnouncement` body |
| Published at `publishedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishAnnouncement` body |
| Locale `locale` | text field | optional | — | — | — | — | `publishAnnouncement` body |

Errors to draw in the form: 403 The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type …

#### Outputs: what the screen shows and produces

**Shown**

**Every announcement** (data table, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Venues | list or chips (count when long) | — |
| Departments | list or chips (count when long) | — |
| Roles | list or chips (count when long) | — |
| Requires acknowledgement | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Locale | text | — |

**The selected announcement** (detail panel, from `listAnnouncements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Title | text | — |
| Body | text | — |
| Kind | chip: Operational, Safety, Emergency, Hr, Celebration | `emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a … |
| Venues | list or chips (count when long) | — |
| Departments | list or chips (count when long) | — |
| Roles | list or chips (count when long) | — |
| Requires acknowledgement | yes / no (icon or chip) | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Locale | text | — |

**The announcement reach** (detail panel, from `getAnnouncementReach`)

| Shows | Format | Notes |
|---|---|---|
| Announcement | the name it points at, never the id | — |
| Targeted | 1,234 | — |
| Delivered | 1,234 | — |
| Acknowledged | 1,234 | — |
| Outstanding | list or chips (count when long) | The list that matters. For an operational notice it measures whether anyone read it; during an emergency it is the roll call. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Publish announcement (primary button) | `publishAnnouncement` POST `/announcements` | Announcement | Announcement | 403 The caller lacks `ANNOUNCEMENT_PUBLISH` at the target scope, or sent `kind` `emergency` without `ANNOUNCEMENT_EMERGENCY` (problem type … | opens modal first |
| Acknowledge announcement (secondary button) | `acknowledgeAnnouncement` POST `/announcements/{announcementId}/acknowledge` | — | — | — | works offline |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `listAnnouncements` (onLoad, What staff have been told)

**Where the user goes next**

- → `EMP-009` End shift: *Ends the shift*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The handover notes list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the handover notes untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No handover notes yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on unacknowledgedOnly and the handover notes are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Editable offline and synced at end of shift |

#### Permissions

- `listAnnouncements` → `WORKFORCE_VIEW` (read) · staff
- `publishAnnouncement` → `ANNOUNCEMENT_PUBLISH` (configure) · staff
- `acknowledgeAnnouncement` → `WORKFORCE_VIEW` (read) · staff
- `getAnnouncementReach` → `WORKFORCE_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `WORKFORCE_VIEW`, which `listAnnouncements` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.2.66 | System shall send assignment and schedule notifications. | Ticketing Catalogue | CONTRACTED | `publishAnnouncement` |
| 18.1.5 | Push Notifications - System shall support push notifications. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.3 | Announcements - Users shall receive announcements. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |
| 18.9.4 | Emergency Alerts - Users shall receive emergency notifications. | Employee Mobile App & AI Assistant | CONTRACTED | `publishAnnouncement` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-007` · status **notStarted** · provenance generated
- Flow F08 *Steward works a shift on the employee app*, step 7: Writes handover notes → What the next shift needs to know
- Flow F65 *A task is raised, worked and handed over*, step 5: Unfinished work is written into the handover. → **The handover is generated from open tasks, not typed.** A note somebody writes at the end of a tiring shift is a note that omits things.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (29 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish announcement, Acknowledge announcement, What publishing changes.
- [ ] Every transition is wired: `EMP-009`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `ANNOUNCEMENT_PUBLISH`, `WORKFORCE_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `EMP-008` Shift summary

**See what this person actually did today.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P06 Venue Staff App (mobile) |
| Module | Operations · wave 2 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `REPORT_VIEW_WORKSTATION`, `SHIFT_OPEN`, `SHIFT_SUSPEND` (3 operate); in the flows as supervisor |
| Device and orientation | This is a staff phone, 390 x 844, dark theme, bottom navigation Home, Tasks, Scan, AI, More, with the offline strip. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listShifts` reads the population and `getCurrentShift` reads one of them — list, select, act |
| Offline | Local totals, marked as unreconciled |
| Opens with | `shiftId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/operations/shift-summary` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Removed 24 August**: acceptShiftVariance, approveShiftOpen, closeShift, createCashMovement. **Bulk-attach residue, found by walking a journey.** A device-settings screen does not read guest loyalty, a venue map does not set a refund policy, a shift summary does not close the shift, and **a rota a steward can rewrite is not a rota.** **Removed 24 August**: openShift, recordNoSale, reopenShift, resumeShift. **Bulk-attach residue.** A device-settings screen does not merge guest profiles, a rota view does not author the rota, a shift summary does not open a shift, and **authority notification belongs where the incident is raised, not where it is read.**

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listShifts`. | `listShifts` ?workstationId |
| Status | select | optional | — | Pending approval · Open · Suspended · Pending variance · Pending closure · Closed · Auto closed | — | Sends `?status=` to `listShifts`. | `listShifts` ?status |
| Opened from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedFrom=` to `listShifts`. | `listShifts` ?openedFrom |
| Opened to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?openedTo=` to `listShifts`. | `listShifts` ?openedTo |

**Sent by *Suspend shift*** (`suspendShift`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | optional | — | max length 200 | — | — | `suspendShift` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `suspendShift` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every shift** (data table, from `listShifts`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |

**Every cash movement** (data table, from `listCashMovements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. |
| Kind | chip: Opening float, Lift, Add | `openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one … |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Denominations | list or chips (count when long) | Stored as `orders.cash_count_line` rows with `countKind: movement` and this movement's `cashMovementId`, not as a column. |
| Reference | text | Safe drop reference or bag number. |
| Reason | text | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Shift | the name it points at, never the id | — |
| Deposit box | the name it points at, never the id | The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099). |
| Witness principal | the name it points at, never the id | The cashier who countersigned a withdrawal. Null on other movements. |
| Withdrawal reason | chip: Banking, Safe drop, Change order, Other | Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records. |
| Authorised by principal | the name it points at, never the id | The principal who authorised the movement, recorded for audit. |

**The selected shift** (detail panel, from `getCurrentShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**The shift** (detail panel, from `getShift`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Client-generated UUIDv7. Also the idempotency key. |
| Workstation | the name it points at, never the id | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Principal | the name it points at, never the id | Who opened it. Cash reconciles to a person and a drawer. |
| Principal display name | text | — |
| Incidents | list or chips (count when long) | BL-097. A till has exceptions and there was nowhere to write them — a no-sale, a drawer opened without a transaction, a manager override, a … |
| Status | chip: Pending approval, Open, Suspended, Pending variance, Pending closure, Closed… | — |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Currency scale | 1,234 | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Deposit box code | text | — |
| Bag number | text | — |
| Opening float | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Sales total | AED 1,234.50 | What the till took in sales, as the guest paid it — tax included. |
| Refunds total | AED 1,234.50 | What the till paid back, as the guest was refunded it — tax included. |
| Lifts total | AED 1,234.50 | Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Suspend shift (destructive button) | `suspendShift` POST `/shifts/{shiftId}/suspend` | inline | Shift | 403 Authenticated but not permitted at the requested scope; 409 Shift is not `open` (problem type `shift-not-open`) | works offline |

**Data it reads**: `listShifts` (onLoad, List shifts); `getCurrentShift` (onLoad, The open or suspended shift on the session's workstation); `getShift` (onLoad, Read a shift); `listCashMovements` (onLoad, Lifts, adds and the opening float)

**Where the user goes next**

- → `EMP-017` Sync & reconciliation: *Anything unsynced is pushed first*
- → `EMP-001` Sign in: *Sign in*
- → `EMP-002` Select venue & role: *Select venue & role*
- → `EMP-003` Home — on duty: *Home — on duty*

**What opens over it**

- confirmDialog *Suspend shift*: **Names what `suspendShift` changes and what it leaves alone**, in the consequence rather than the verb. A shift summary this affects should be identified in the dialog, not just counted. **Collects what `suspendShift` sends before it is called.** Required: `recordedAt`. Optional: `reason`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The shift summary list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the shift summary untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No shift summary yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, status, openedFrom, openedTo and the shift summary are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Local totals, marked as unreconciled |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Shift is not `open` (problem type `shift-not-open`) |

#### Permissions

- `listShifts` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `getCurrentShift` → `SHIFT_OPEN` (operate) · staff
- `getShift` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `listCashMovements` → `REPORT_VIEW_WORKSTATION` (operate) · staff
- `suspendShift` → `SHIFT_SUSPEND` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_WORKSTATION`, which `listShifts` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P06 · Operations, 12 for all of P06, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A59** Cross-check the workstation/POS/till wireframes shared by Allam against the functionality matrix and consolidate/redesign dashboards where overlapping (e.g., shift-closing vs. till-closing screens) *(Chinmay Parab / Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'till')*
- **A77** Design cash/shift (till) management and the workstation/POS admin dashboard suite: blind cash-out reconciliation, supervisor shift-closure authorization, a configurable cash-drawer limit with mid-shift unload, automatic … *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 14 Aug 2026 · workshop tracker · keyword 'shift')*
- **A150** Manage personnel as a resource type (duty/leave status, skills and certification levels, certification expiry, shift templates, leave quotas, optional external HR integration) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A155** Build AI resource forecasting, the employee mobile app (bookings, check-in/out, shift close, swaps) and cost/revenue analytics by resource and event *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 26 Aug 2026 · workshop tracker · keyword 'shift')*
- **A269** POS: auto hardware check at shift start; cashier report visibility as a role toggle *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 9 Sep 2026 · workshop tracker · keyword 'shift')*
- **A272** Agree shift-close cash-variance approach (expected-sales visibility, no-supervisor fallback) *(Qossai / Allam · Medium · With client → 30 Sep: Closed, Moved to T10 (TICVAI to act) · 9 Sep 2026 · workshop tracker · keyword 'shift')*

#### References

- Wireframe frame: `wireframes/P06 Venue Staff App.dc.html#emp-008` · status **notStarted** · provenance generated
- Flow F72 *A shift ends and the summary is read*, step 1: The steward reads their shift summary. → **Read-only.** This screen could close the shift and accept a variance until 24 August — **the person being reviewed could sign off their own review.**

#### Acceptance for the design

- [ ] Every input above is drawn (6), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (56 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#EMP-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Suspend shift.
- [ ] Every transition is wired: `EMP-017`, `EMP-001`, `EMP-002`, `EMP-003`.
- [ ] Every gated control is gated: `REPORT_VIEW_WORKSTATION`, `SHIFT_OPEN`, `SHIFT_SUSPEND`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P06 reference designs** (from `handoff/design-batches/apps/4-staff-app/README.md`)

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the client's employee app reference: dark theme, Home, Tasks, Scan, AI, More.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P06 as a whole** (3: 0 open, 3 closed). Open first; a closed row says where it went on 30 September.

- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A49** Confirm scope: deliver a lightweight standalone ticket-validation app for dedicated scanner devices, in addition to the scan/validate function embedded in the full Staff Operations App *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A71** Design an offline-first, native ticket-scanning/access-control capability (local scan storage with sync-on-reconnect) for both the dedicated scanner app and the scanning function embedded in the Employee App *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 10 Aug 2026 · workshop tracker)*

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

### Across P06 Venue Staff App

- From the case screen agents act on the customer's bookings/tickets (date change, reschedule, resend tickets), initiate refunds/compensation, route for internal approval, or escalate to another department, which sees it on that department's mobile app. *(client request · MoM 31 Aug 2026, 4.1 Customer Service & Contact Center (Case Management) · DI-542)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- Approval screens offer Approve, Reject, Return and Request More Information, show an AI-generated approval summary beside the request, and a visible trail of who approved at each stage (e.g. IT → Ops Manager → Finance → CEO → IT publishes). *(client request · MoM 10 Aug 2026, 5.5 Multi-Stage Approval Workflow · DI-235)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Allam: the platform is device-agnostic (Android, iOS and web) so sales can continue on any available device. *(agreed · MoM 31 Jul 2026, 8. Point-of-Sale Data Sync Strategy · DI-068)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

### In P06 · Operations

- Employee app navigation: Work Orders, Task & Assets, Inventory/Safety/Inspections, Attendance, Approvals/Requests, Incidents, Communications, Venue Map; plus employee ID/profile and preferences. *(client request · MoM 10 Aug 2026, 5.2 Core Navigation & Modules · DI-228)*

**23 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"acceptShiftVariance": {"method":"POST","path":"/shifts/{shiftId}/accept-variance","contract":"shift","summary":"Accept an over/short beyond the threshold","permission":"OVERSHORT_ACCEPT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"acceptWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/accept","contract":"maintenance","summary":"The assignee takes the job","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"acknowledgeAnnouncement": {"method":"POST","path":"/announcements/{announcementId}/acknowledge","contract":"workforce","summary":"Confirm you have read it","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"approveShiftOpen": {"method":"POST","path":"/shifts/{shiftId}/approve-open","contract":"shift","summary":"Approve a shift opening outside tolerance","permission":"SHIFT_APPROVE_OPEN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"attachWorkOrderEvidence": {"method":"POST","path":"/work-orders/{workOrderId}/attachments","contract":"maintenance","summary":"Photo, video, document, note or signature","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrderAttachment"},
"cancelWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/cancel","contract":"maintenance","summary":"Cancel a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"closeShift": {"method":"POST","path":"/shifts/{shiftId}/close","contract":"shift","summary":"Blind close-out","permission":"SHIFT_CLOSE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CloseShiftRequest","responds":"ShiftCloseResult"},
"closeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/close","contract":"maintenance","summary":"Administratively closed","permission":"MAINTENANCE_APPROVE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"completeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/complete","contract":"maintenance","summary":"Complete a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"createCashMovement": {"method":"POST","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Record a cash lift or add","permission":"CASH_LIFT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateCashMovementRequest","responds":"CashMovement"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createStockReservation": {"method":"POST","path":"/stock-reservations","contract":"inventory","summary":"Reserve stock for a work order or another need","permission":"PROCUREMENT_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"InventoryStockReservation","responds":"InventoryStockReservation"},
"createWorkOrder": {"method":"POST","path":"/work-orders","contract":"maintenance","summary":"Raise a work order","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreateWorkOrderRequest","responds":"WorkOrder"},
"getAnnouncementReach": {"method":"GET","path":"/announcements/{announcementId}/reach","contract":"workforce","summary":"Who has acknowledged, and who has not","permission":"WORKFORCE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AnnouncementReach"},
"getCurrentSession": {"method":"GET","path":"/auth/session","contract":"identity","summary":"Current session and effective permissions","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Session"},
"getCurrentShift": {"method":"GET","path":"/shifts/current","contract":"shift","summary":"The open or suspended shift on the session's workstation","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Shift"},
"getIncident": {"method":"GET","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Read an incident","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"IncidentDetail"},
"getOfflinePackage": {"method":"GET","path":"/access/offline-package","contract":"access","summary":"Entitlement and rule set for offline validation","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"sinceVersion","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":"validFrom","in":"query","required":true},{"name":"validTo","in":"query","required":true},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"OfflinePackage"},
"getShift": {"method":"GET","path":"/shifts/{shiftId}","contract":"shift","summary":"Read a shift","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Shift"},
"getWorkOrder": {"method":"GET","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Read a work order","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"WorkOrderDetail"},
"listAnnouncements": {"method":"GET","path":"/announcements","contract":"workforce","summary":"What staff have been told","permission":"WORKFORCE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"unacknowledgedOnly","in":"query","required":null}],"requestBody":null,"responds":"Announcement"},
"listCashMovements": {"method":"GET","path":"/shifts/{shiftId}/cash-movements","contract":"shift","summary":"Lifts, adds and the opening float","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listIncidents": {"method":"GET","path":"/incidents","contract":"maintenance","summary":"List incidents","permission":"INCIDENT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"severity","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"isReportable","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMfaMethods": {"method":"GET","path":"/auth/mfa/methods","contract":"identity","summary":"Enrolled MFA methods","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MfaMethod"},
"listRoles": {"method":"GET","path":"/roles","contract":"identity","summary":"List roles","permission":"ROLE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listScans": {"method":"GET","path":"/access/scans","contract":"access","summary":"List scan events","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accessPointId","in":"query","required":null},{"name":"ticketId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listShifts": {"method":"GET","path":"/shifts","contract":"shift","summary":"List shifts","permission":"REPORT_VIEW_WORKSTATION","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"openedFrom","in":"query","required":null},{"name":"openedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSsoProviders": {"method":"GET","path":"/auth/sso/providers","contract":"identity","summary":"Identity providers configured for this tenant","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SsoProvider"},
"listStockReservations": {"method":"GET","path":"/stock-reservations","contract":"inventory","summary":"Soft holds on stock","permission":"PRODUCT_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"sourceType","in":"query","required":null},{"name":"sourceId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listWorkOrders": {"method":"GET","path":"/work-orders","contract":"maintenance","summary":"List work orders","permission":"WORK_ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"assignedToPrincipalId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"priority","in":"query","required":null},{"name":"assetId","in":"query","required":null},{"name":"overdueOnly","in":"query","required":null},{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"login": {"method":"POST","path":"/auth/login","contract":"identity","summary":"Authenticate and open a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LoginRequest","responds":"LoginResponse"},
"lookupTicket": {"method":"GET","path":"/access/lookup","contract":"access","summary":"Read-only validity check without admitting","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaCode","in":"query","required":null},{"name":"ticketId","in":"query","required":null}],"requestBody":null,"responds":"TicketStatus"},
"openShift": {"method":"POST","path":"/shifts","contract":"shift","summary":"Open a shift","permission":"SHIFT_OPEN","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"OpenShiftRequest","responds":"Shift"},
"overrideAccess": {"method":"POST","path":"/access/override","contract":"access","summary":"Admit against a failed validation","permission":"ACCESS_OVERRIDE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"pauseWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/pause","contract":"maintenance","summary":"Stopped, and why","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"publishAnnouncement": {"method":"POST","path":"/announcements","contract":"workforce","summary":"Tell staff something","permission":"ANNOUNCEMENT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"Announcement","responds":"Announcement"},
"recordAuthorityNotification": {"method":"POST","path":"/incidents/{incidentId}/notify-authority","contract":"maintenance","summary":"Record notification to an external authority","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"},
"recordNoSale": {"method":"POST","path":"/shifts/{shiftId}/no-sale","contract":"shift","summary":"Open the Deposit Box without a sale","permission":"CASH_NO_SALE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"NoSaleEvent"},
"recordWorkOrderParts": {"method":"POST","path":"/work-orders/{workOrderId}/parts","contract":"maintenance","summary":"Record parts consumed","permission":"WORK_ORDER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrderDetail"},
"recordWorkOrderTime": {"method":"POST","path":"/work-orders/{workOrderId}/time","contract":"maintenance","summary":"Start, pause or stop work","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"rejectWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/reject","contract":"maintenance","summary":"The assignee declines, with a reason","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"releaseStockReservation": {"method":"POST","path":"/stock-reservations/{stockReservationId}/release","contract":"inventory","summary":"Give reserved stock back","permission":"PROCUREMENT_REQUEST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"InventoryStockReservation"},
"reopenShift": {"method":"POST","path":"/shifts/{shiftId}/reopen","contract":"shift","summary":"Reopen a shift closed in error","permission":"SHIFT_REOPEN","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"reportIncident": {"method":"POST","path":"/incidents","contract":"maintenance","summary":"Report an incident","permission":"INCIDENT_REPORT","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ReportIncidentRequest","responds":"Incident"},
"resumeShift": {"method":"POST","path":"/shifts/{shiftId}/resume","contract":"shift","summary":"Resume a suspended shift","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"resumeWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/resume","contract":"maintenance","summary":"Back to work","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"selectRole": {"method":"POST","path":"/auth/select-role","contract":"identity","summary":"Choose a role for a multi-role session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Session"},
"startWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/start","contract":"maintenance","summary":"Work has begun","permission":"MAINTENANCE_EXECUTE","offlineCapable":true,"conflictPolicy":"lastWriterWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"suspendShift": {"method":"POST","path":"/shifts/{shiftId}/suspend","contract":"shift","summary":"Suspend a shift so another user can log in","permission":"SHIFT_SUSPEND","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Shift"},
"syncScans": {"method":"POST","path":"/access/scans","contract":"access","summary":"Replay scans recorded offline","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ScanSyncResult"},
"updateIncident": {"method":"PATCH","path":"/incidents/{incidentId}","contract":"maintenance","summary":"Investigate, escalate or close an incident","permission":"INCIDENT_MANAGE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Incident"},
"updateWorkOrder": {"method":"PATCH","path":"/work-orders/{workOrderId}","contract":"maintenance","summary":"Assign, reprioritise or amend","permission":"WORK_ORDER_MANAGE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"},
"validateAccess": {"method":"POST","path":"/access/validate","contract":"access","summary":"Validate media at an access point and admit or deny","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ValidateRequest","responds":"ValidationResult"},
"validateGroupAccess": {"method":"POST","path":"/access/group-validate","contract":"access","summary":"Admit a group on one read","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"verifyAccreditationCredential": {"method":"GET","path":"/accreditation-credentials/verify","contract":"accreditation","summary":"Who holds this credential, and where may they go","permission":"ACCESS_VALIDATE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"identifier","in":"query","required":true},{"name":"zoneId","in":"query","required":null}],"requestBody":null,"responds":"AccreditationCredentialVerification"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"verifyWorkOrder": {"method":"POST","path":"/work-orders/{workOrderId}/verify","contract":"maintenance","summary":"Supervisor verification","permission":"WORK_ORDER_VERIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WorkOrder"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessAccreditationCredential": {"type":"object","x-ticvai-persistence":"access.accreditation_credential","x-ticvai-agreed":"29 September: build pass (group OWN, from group RA's handoff; BL-181); the events accreditation.credentialIssued and accreditation.holderStatusChanged name access as their critical consumer","description":"**What a gate needs to admit an accredited person, kept by `access`** (29 September, build). Written only by the consumers of `accreditation.credentialIssued` (a row per credential; a replacement sets the replaced row's `admits` false) and `accreditation.holderStatusChanged` (every credential of the holder: `admits` false unless the holder is `active`, validity taken from the event). Read by `validateAccess` and shipped in the offline package. The record of truth stays in `accreditation`; this is a copy shaped for the gate, never edited by a person.","required":["id","holderId","encodedIdentifier","admits","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The accreditation credential's id (`credentialId` on the events)."},"holderId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","description":"printedBadge, mobileCredential, qr, nfcCard, rfidCard or wristband, as issued."},"encodedIdentifier":{"type":"string","x-ticvai-unique":"tenant","description":"What the gate reads from the credential. Never sent to webhook subscribers."},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"zoneIds":{"type":"array","description":"The holder's effective zones, from the event (`effectiveZones`).","items":{"type":"string","format":"uuid"}},"holderStatus":{"type":"string","enum":["active","suspended","revoked","expired","archived"],"description":"The holder's status as last published; only `active` admits."},"admits":{"type":"boolean","description":"False once the credential is replaced or the holder is not active."},"sourceChangedAt":{"type":"string","format":"date-time","description":"The `issuedAt` or `changedAt` of the event last applied; an older event arriving late is ignored."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), the accreditation programme's scope."}}},
"AccessDynamicPolicy": {"type":"object","x-ticvai-persistence":"access.dynamic_policy","description":"One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.authorisation_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Guest admission lives here and nowhere else** (ADR-0068, accepted 1 October). `validateAccess` online and the gate offline evaluate the same active version: `getOfflinePackage` carries it, and every `scan_event` records the policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`) and the set it was decided under (`policySetVersion`). The condition is `conditionRule`, a closed JSON format (`AdmissionRule`), not free text. Identity's staff-permission engine was renamed `AuthorisationPolicy` on the same day, so \"access policy\" means this.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AuthorisationPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAuthorisationPolicyEffectiveness` in identity.","required":["id","scopePath","name","policyType","conditionRule","result","status","currentVersion"],"properties":{"id":{"type":"string","format":"uuid","description":"The policyId"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node; where it applies further is access.policy_scope_assignment"},"name":{"type":"string","maxLength":200},"policyType":{"type":"string","enum":["guestAttribute","accreditation","occupancy","employee","risk","membership","timeEvent"]},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"nullable":true,"description":"Context/time/event policies (setContextTimeEvent)"},"identityType":{"type":"string","enum":["guest","member","annualPassHolder","employee","contractor","vendor","performer","media","vip","security","emergencyServices","eventStaff"],"nullable":true,"description":"Identity-based policies (listIdentityMembershipAccreditation)"},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`)."},"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"priority":{"type":"integer","nullable":true},"allowedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"deniedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"monitorThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Restrict"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"The grant expires automatically at validTo"},"status":{"type":"string","enum":["draft","pendingApproval","active","inactive","expired"],"default":"draft"},"currentVersion":{"type":"integer","minimum":1,"description":"The version in force (access.dynamic_policy_version)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccreditationCredentialVerification": {"type":"object","description":"18.8.3. **What a steward needs to believe the person in front of them**: the face, the name, the category and the zones, and whether any of it is valid now. Returned by `verifyAccreditationCredential`; not stored.\n","required":["outcome"],"properties":{"outcome":{"type":"string","enum":["valid","notYetValid","expired","suspended","revoked","credentialReplaced","credentialLost","credentialInactive"],"description":"`valid` only when the holder is `active`, today is inside the holder's validity, and the credential is `issued` or `active`"},"reason":{"type":"string","nullable":true},"credentialId":{"type":"string","format":"uuid"},"credentialKind":{"type":"string"},"credentialStatus":{"type":"string"},"holderId":{"type":"string","format":"uuid"},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"photoUrl":{"type":"string","nullable":true,"description":"Signed and short-lived, so the scan screen can show the face without a second call"},"organisationName":{"type":"string","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"categoryName":{"type":"string","nullable":true},"holderStatus":{"type":"string"},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"effectiveZones":{"type":"array","description":"The zones the holder may enter under their profiles and exceptions, today","items":{"type":"object","properties":{"zoneId":{"type":"string","format":"uuid"},"zoneName":{"type":"string"},"allowedNow":{"type":"boolean","description":"Inside the profile schedule (date, day, time, event phase) at this moment"}}}},"escortRequired":{"type":"boolean"},"zoneCheck":{"type":"object","nullable":true,"description":"Present when `zoneId` was given","properties":{"zoneId":{"type":"string","format":"uuid"},"allowed":{"type":"boolean"},"reason":{"type":"string","nullable":true}}},"checkedAt":{"type":"string","format":"date-time"}}},
"Announcement": {"type":"object","x-ticvai-persistence":"workforce.announcement","required":["title","body","kind","publishedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"title":{"type":"string","maxLength":140},"body":{"type":"string","maxLength":4000},"kind":{"$ref":"#/components/schemas/AnnouncementKind"},"venueIds":{"type":"array","items":{"type":"string","format":"uuid"}},"departmentIds":{"type":"array","items":{"type":"string","format":"uuid"}},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}},"requiresAcknowledgement":{"type":"boolean"},"deliveryChannels":{"type":"array","description":"How it reaches people (29 September, build, 18.1.5). `inApp` always; `push` to the targeted people's registered staff phones (tenancy `RegisteredDevice`, kind `mobileHandset`). `emergency` is sent by both whatever is set here.\n","items":{"type":"string","enum":["inApp","push"]},"default":["inApp","push"]},"expiresAt":{"type":"string","format":"date-time","nullable":true},"publishedByPrincipalId":{"type":"string","format":"uuid","readOnly":true},"publishedAt":{"type":"string","format":"date-time"},"locale":{"type":"string","nullable":true}}},
"AnnouncementKind": {"type":"string","description":"`emergency` is not a louder `operational`. It overrides the home screen, bypasses quiet hours, requires acknowledgement, and carries a separate permission.\n","enum":["operational","safety","emergency","hr","celebration"]},
"AnnouncementReach": {"type":"object","x-ticvai-persistence":"none — computed from workforce.announcement_receipt","properties":{"announcementId":{"type":"string","format":"uuid"},"targeted":{"type":"integer"},"delivered":{"type":"integer"},"acknowledged":{"type":"integer"},"outstanding":{"type":"array","description":"**The list that matters.** For an operational notice it measures whether anyone read it; during an emergency it is the roll call.\n","items":{"type":"object","properties":{"principalId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"onShift":{"type":"boolean"}}}}}},
"CashMovement": {"x-ticvai-persistence":"orders.cash_movement","allOf":[{"$ref":"#/components/schemas/CreateCashMovementRequest"},{"type":"object","required":["shiftId","authorisedByPrincipalId","sequence"],"properties":{"shiftId":{"type":"string","format":"uuid"},"depositBoxId":{"type":"string","format":"uuid","nullable":true,"description":"The box the cash moved in or out of. Set on every lift `withdrawFromDepositBox` records (26 September, pull audit R099).\n"},"witnessPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The cashier who countersigned a withdrawal. Null on other movements."},"withdrawalReason":{"allOf":[{"$ref":"#/components/schemas/WithdrawalReason"}],"nullable":true},"authorisedByPrincipalId":{"type":"string","format":"uuid","description":"The principal who authorised the movement, recorded for audit."},"sequence":{"type":"integer","description":"Monotonic within the shift. Preserves order across an offline batch."},"syncedAt":{"type":"string","format":"date-time","nullable":true}}}]},
"CashMovementKind": {"type":"string","enum":["openingFloat","lift","add"],"description":"`openingFloat` is written by `openShift`; `lift` by `createCashMovement` and by `withdrawFromDepositBox`, which is a lift from one cashier's box; `add` by `createCashMovement`.\n"},
"CloseShiftRequest": {"type":"object","required":["countedCash","recordedAt"],"properties":{"countedCash":{"type":"array","minItems":1,"description":"**The cashier's blind count, one line per denomination counted** (decided 29 September, readiness close-out; our build plan). The server writes each line as one `CashCountLine` (`countKind` close) against the shift, taking the face value from `platform.denomination`. A denomination may appear once; a repeat is refused with 422 `duplicate-denomination`.\n","items":{"$ref":"#/components/schemas/CountedDenominationLine"}},"nonCashDeclared":{"type":"array","description":"Declared totals per non-cash tender, for reconciliation against captured payments.\n","items":{"type":"object","required":["tender","amount"],"properties":{"tender":{"type":"string"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"notes":{"type":"string","maxLength":1000},"releaseHeldLeases":{"type":"boolean","default":true,"description":"Return unsold inventory leases held by this workstation (ADR-0013 C103). Closing without releasing strands capacity until TTL expiry, which is visible at a gate during peak.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"CountedDenominationLine": {"type":"object","x-ticvai-persistence":"none — request only; lands as `CashCountLine` rows","description":"**One line of a cash count as the cashier types it: which note or coin, how many, and what they come to** (decided 29 September, readiness close-out; our build plan). The shape of the blind count on close (`closeShift`) and of the count columns on the till screens (POS-007, POS-011). It is the request side of `CashCountLine`, which is the stored row and adds the shift, the count kind, who counted and when.\n**`total` is shown to the cashier and checked, not trusted**: the server recomputes `count` times the denomination's face value and refuses a line whose `total` disagrees with 422 `count-total-mismatch`. An inactive or unknown denomination is refused with 422 `unknown-denomination`.\n","required":["denominationId","count"],"properties":{"denominationId":{"type":"string","format":"uuid","description":"References `platform.denomination` (`Denomination.id`) — face value, kind and counting order live there."},"count":{"type":"integer","minimum":0,"maximum":100000,"description":"**How many of this note or coin were counted.** Zero is a line, not an omission: a denomination counted and found empty."},"total":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"`count` times the face value, in the denomination's currency. Optional on the way in (the server computes it) and checked when sent.\n"}}},
"CreateCashMovementRequest": {"type":"object","required":["id","kind","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7."},"kind":{"$ref":"#/components/schemas/CashMovementKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"denominations":{"$ref":"#/components/schemas/DenominationCount","x-ticvai-persisted":false,"description":"**Stored as `orders.cash_count_line` rows** with `countKind: movement` and this movement's `cashMovementId`, not as a column. The jsonb blob this used to land in is what `Denomination` was created to replace (26 September, pull audit R099).\n"},"reference":{"type":"string","maxLength":64,"description":"Safe drop reference or bag number."},"reason":{"type":"string","maxLength":500},"recordedAt":{"type":"string","format":"date-time"}}},
"CreateWorkOrderRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","title","venueId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"title":{"type":"string","maxLength":200},"description":{"type":"string","maxLength":5000},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"kind":{"allOf":[{"$ref":"#/components/schemas/WorkOrderKind"}],"default":"corrective"},"priority":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"description":"**Optional since 29 September** (M17-01). Sent, it is `manual` and wins. Absent, the asset's `priorityOverride` applies, and failing that the venue's `WorkOrderPriorityPolicy` scores the fault.\n"},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","maxItems":10,"items":{"type":"string"},"description":"Skills the job needs, as qualification codes; `suggestWorkOrderAssignee` ranks by them (M17-13)."},"categoryId":{"type":"string","format":"uuid"},"assignedToPrincipalId":{"type":"string","format":"uuid"},"dueAt":{"type":"string","format":"date-time"},"attachmentRefs":{"type":"array","description":"Photo-first. Expected at creation, not added later from memory.","items":{"type":"string"}},"takeAssetOutOfService":{"type":"boolean","default":false,"description":"Raise and immediately suspend the asset. For a fault found on a live ride, the two are one action.\n"},"recordedAt":{"type":"string","format":"date-time"}}},
"DenominationCount": {"type":"array","description":"**A count is a list of lines and the line is the row.** Until 24 August this array carried the persistence hint itself, so `orders.cash_count_line` derived a single column — `shift_id` — and a count line had no denomination, no quantity and no variance.\n**The array is the transport; `CashCountLine` is the row.**\n","items":{"$ref":"#/components/schemas/CashCountLine"},"minItems":1},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"Incident": {"x-ticvai-persistence":"maintenance.incident","type":"object","required":["id","incidentNumber","kind","severity","status","venueId","occurredAt","reportedByPrincipalId"],"properties":{"id":{"type":"string","format":"uuid"},"incidentNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"status":{"$ref":"#/components/schemas/IncidentStatus"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"locationDescription":{"type":"string","nullable":true},"isReportable":{"type":"boolean","description":"Requires notification to an external authority within a statutory window."},"notificationDueAt":{"type":"string","format":"date-time","nullable":true},"notifiedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `notifiedAt` among this incident's authority notifications. **Maintained on write** by `recordAuthorityNotification`; each notification itself is a row of `maintenance.incident_authority_notification`.\n"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"reportedByPrincipalId":{"type":"string","format":"uuid"},"correctiveWorkOrderId":{"type":"string","format":"uuid","nullable":true},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"closedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"IncidentAuthorityNotification": {"x-ticvai-persistence":"maintenance.incident_authority_notification","type":"object","description":"**One notification to an external authority, appended by `recordAuthorityNotification`.** An incident may be reported to more than one authority, or to the same one twice, and each is the evidence that an obligation was met — so each is a row, not an overwrite of `maintenance.incident.notified_at`.\n","required":["id","incidentId","authority","notifiedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"authority":{"type":"string","maxLength":200},"reference":{"type":"string","maxLength":128,"nullable":true},"notifiedAt":{"type":"string","format":"date-time"},"notifiedByPrincipalId":{"type":"string","format":"uuid"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentDetail": {"x-ticvai-persistence":"maintenance.incident","allOf":[{"$ref":"#/components/schemas/Incident"},{"type":"object","properties":{"description":{"type":"string","description":"The original report. Never edited — investigation adds to the record."},"investigationNote":{"type":"string","nullable":true,"readOnly":true,"description":"The latest entry of `investigationNotes`, kept for readers that show one line."},"investigationNotes":{"type":"array","readOnly":true,"description":"**Every investigation note, oldest first** (decided 28 September, audit R106 (5)). Read from `maintenance.incident_investigation_note`; appended by `updateIncident`.\n","items":{"$ref":"#/components/schemas/IncidentInvestigationNote"}},"rootCause":{"type":"string","nullable":true},"correctiveActions":{"type":"string","nullable":true},"firstAidGiven":{"type":"boolean"},"emergencyServicesCalled":{"type":"boolean"},"witnessCount":{"type":"integer"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"involvedParties":{"type":"array","description":"Who was involved, as given in `ReportIncidentRequest.involvedSubjectIds` and `involvedStaffPrincipalIds`. Read from `maintenance.incident_involved_party`.\n","items":{"$ref":"#/components/schemas/IncidentInvolvedParty"}},"authorityNotifications":{"type":"array","description":"Read from `maintenance.incident_authority_notification`, oldest first.","items":{"$ref":"#/components/schemas/IncidentAuthorityNotification"}}}}]},
"IncidentInvestigationNote": {"x-ticvai-persistence":"maintenance.incident_investigation_note","type":"object","description":"**One investigation note, appended by `updateIncident`** (decided 28 September, audit R106 (5)). A history rather than a field, so what an investigator thought on Tuesday survives what they found on Thursday.\n","required":["id","incidentId","note","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"note":{"type":"string","maxLength":10000},"writtenByPrincipalId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"}}},
"IncidentInvolvedParty": {"x-ticvai-persistence":"maintenance.incident_involved_party","type":"object","description":"**One person involved in an incident, by opaque reference.** A guest or member of the public is a `pii.subject` id — personal details live there, the erasable store of ADR-0023, so the incident record survives an erasure request intact. A member of staff is a principal id. Exactly one of the two is set, as `kind` says.\n","required":["id","incidentId","kind"],"properties":{"id":{"type":"string","format":"uuid"},"incidentId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["subject","staff"]},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"A `pii.subject` id where `kind` is `subject`."},"principalId":{"type":"string","format":"uuid","nullable":true,"description":"The staff principal where `kind` is `staff`."}}},
"IncidentKind": {"type":"string","enum":["guestInjury","staffInjury","nearMiss","propertyDamage","equipmentFailure","securityIncident","fireOrEvacuation","foodSafety","environmental","other"]},
"IncidentSeverity": {"type":"string","enum":["nearMiss","minor","moderate","major","critical"]},
"IncidentStatus": {"type":"string","enum":["reported","underInvestigation","actionRequired","closed"]},
"InventoryStockReservation": {"type":"object","x-ticvai-persistence":"inventory.stock_reservation","description":"**Taken from the backend workbook, 20 September.** Temporarily reserves stock for an order or operational requirement so it cannot be allocated elsewhere.","required":["itemId","locationId","quantity","sourceType","sourceId","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"itemId":{"type":"string","format":"uuid"},"locationId":{"type":"string","format":"uuid"},"quantity":{"type":"number","exclusiveMinimum":0},"sourceType":{"$ref":"#/components/schemas/StockReservationSourceType"},"sourceId":{"type":"string","format":"uuid","description":"The id of what the stock is reserved for: a work order, a rental agreement or an order. A uuid, as every id is (ADR-0056); it was text from 29 September to 30 September because a work order id was then 26-character text (M17-02)."},"status":{"type":"string","enum":["active","consumed","released","expired"],"readOnly":true},"expiresAt":{"type":"string","format":"date-time","nullable":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"releasedAt":{"type":"string","format":"date-time","nullable":true}}},
"LoginRequest": {"type":"object","required":["username","credential","workstationId"],"properties":{"username":{"type":"string","maxLength":256},"credential":{"type":"string","description":"Password, PIN, card token or RFID token depending on `method`.\n","maxLength":512,"writeOnly":true},"method":{"type":"string","description":"**`pin` is how a till is actually used.** A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets shortened, shared or written on the drawer. The employee number goes in `username` and the PIN in `credential`, so the shape of the request does not change — only what the operator types.\n\n**A PIN is weaker than a password and the difference is bounded by the device, not by the secret.** `workstationId` is required on every login and is *NOT a permission source*: it says which till, and the till is on a venue network in a staff area. A PIN is a reasonable credential there and nowhere else, which is why this is an enum value and not a policy flag — a surface that wants it has to ask for it by name.\n\nAdded 10 September 2026 for `POS-000 Sign In`.\n","enum":["password","pin","card","rfid","sso"],"default":"password"},"workstationId":{"type":"string","format":"uuid","description":"Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. NOT a permission source.\n"},"deviceFingerprint":{"type":"string","maxLength":256}}},
"LoginResponse": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/TokenPair"},{"type":"object","required":["requiresRoleSelection","requiresMfa"],"properties":{"requiresRoleSelection":{"type":"boolean"},"requiresMfa":{"type":"boolean","description":"True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). The session is not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge."},"hasMfaMethod":{"type":"boolean","description":"Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 (5))."},"mfaMethods":{"type":"array","description":"The principal's active methods, so the client can offer the right one for the `signIn` challenge. Empty when `requiresMfa` is false.","items":{"$ref":"#/components/schemas/MfaMethod"}},"availableRoles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"session":{"$ref":"#/components/schemas/Session"}}}]},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MfaKind": {"type":"string","enum":["totp","smsOtp","emailOtp","biometric","hardwareToken"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"NoSaleEvent": {"type":"object","x-ticvai-persistence":"orders.no_sale_event","required":["id","shiftId","reason","principalId","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"reason":{"type":"string"},"note":{"type":"string","nullable":true},"principalId":{"type":"string","format":"uuid"},"recordedAt":{"type":"string","format":"date-time"},"countThisShift":{"type":"integer","description":"Running count. Returned so the terminal can show it — a cashier who can see they are on their ninth no-sale behaves differently from one who cannot.\n"}}},
"OfflinePackage": {"x-ticvai-persistence":"none — generated artefact in object storage","type":"object","required":["etag","generatedAt","validFrom","validTo","accessPointId","entitlements"],"properties":{"etag":{"type":"string"},"generatedAt":{"type":"string","format":"date-time"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"accessPointId":{"type":"string","format":"uuid"},"entitlementsVersion":{"type":"integer","description":"The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."},"policySetVersion":{"type":"string","description":"**The active admission policy version the package carries** (ADR-0068, 1 October): a fingerprint of the `(id, currentVersion)` of every policy in `dynamicPolicies`, computed the same way by `validateAccess` online. Every scan the gate records carries it (`ScanEvent.policySetVersion`), so a scan decided offline under a set that has since changed is visible at sync rather than assumed equal."},"dynamicPolicies":{"type":"array","description":"The active guest-admission dynamic policies for this access point's zones (SD-052), each at its active version with its `conditionRule` (ADR-0068), so an offline gate applies the same rules as an online one.","items":{"$ref":"#/components/schemas/AccessDynamicPolicy"}},"entitlements":{"type":"array","description":"Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.","items":{"type":"object","required":["ticketId","mediaCodes","validFrom","validTo","entriesAllowed","reentryAllowed"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id`."},"mediaCodes":{"type":"array","items":{"type":"string"},"description":"A ticket may carry several media over its life."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesAllowed":{"type":"integer","nullable":true},"entriesUsed":{"type":"integer"},"reentryAllowed":{"type":"boolean"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"delegatedRights":{"type":"array","description":"Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n","items":{"type":"object","required":["rightId","ticketId","issuingCellId","validFrom","validTo","entriesAllowed","entriesConsumed"],"properties":{"rightId":{"type":"string"},"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id` in the issuing cell."},"issuingCellId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"entriesAllowed":{"type":"integer","nullable":true},"entriesConsumed":{"type":"integer"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"blacklist":{"type":"array","items":{"type":"string"},"description":"Media codes to deny outright regardless of entitlement state."},"admissionRules":{"type":"array","items":{"type":"object","required":["id","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid"},"openMinutesBefore":{"type":"integer"},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean"}}}},"accreditationCredentials":{"type":"array","description":"Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.","items":{"$ref":"#/components/schemas/AccessAccreditationCredential"}}}},
"OfflineScan": {"x-ticvai-persistence":"none — client-side journal","allOf":[{"$ref":"#/components/schemas/ValidateRequest"},{"type":"object","required":["sequence","localOutcome"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. The server processes in this order."},"localOutcome":{"allOf":[{"$ref":"#/components/schemas/ScanOutcome"}],"description":"What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"},"localDenyReason":{"$ref":"#/components/schemas/DenyReason"},"overriddenByPrincipalId":{"type":"string","format":"uuid","nullable":true},"overrideReason":{"type":"string","nullable":true}}}]},
"OpenShiftRequest": {"type":"object","required":["workstationId","openingFloat"],"properties":{"workstationId":{"type":"string","format":"uuid"},"openingFloat":{"$ref":"#/components/schemas/DenominationCount"},"depositBoxCode":{"type":"string","maxLength":64,"description":"Physical container assigned to this shift. Required where the venue configures deposit box allocation.\n"},"bagNumber":{"type":"string","maxLength":64,"description":"Required where the venue configures bag numbers as mandatory."},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded it. `openShift` is online-only (F32), so this differs from server receipt time only by transit; it is kept because the shift's other device writes are ordered against it.\n"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"ReportIncidentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["id","kind","severity","venueId","description","occurredAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/IncidentKind"},"severity":{"$ref":"#/components/schemas/IncidentSeverity"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"description":{"type":"string","minLength":3,"maxLength":10000},"involvedSubjectIds":{"type":"array","description":"Opaque references. Personal details live in the erasable store, so the incident record survives an erasure request intact.\n","items":{"type":"string","format":"uuid"}},"involvedStaffPrincipalIds":{"type":"array","items":{"type":"string","format":"uuid"}},"witnessCount":{"type":"integer"},"firstAidGiven":{"type":"boolean","default":false},"emergencyServicesCalled":{"type":"boolean","default":false},"attachmentRefs":{"type":"array","items":{"type":"string"}},"occurredAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"}}},
"ResolutionCode": {"type":"string","enum":["repaired","partReplaced","adjusted","cleaned","noFaultFound","referredExternal","replaced","deferred"]},
"Role": {"x-ticvai-persistence":"identity.role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique within the tenant** (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. Unique per tenant, not per venue, because a grant names a role anywhere in the tree; `createRole` refuses a duplicate with `409 duplicate-code`.\n"},"name":{"type":"string"},"description":{"type":"string"},"permissions":{"type":"array","description":"**A role that grants no permissions is not a role.** `Role` carried a code, a name and two counts until 18 August, and `identity.role_permission` derived from it with exactly one column — `role_id`. **A join table that joins to nothing**, found by Hrushikant in review and missed by the schema audit that ran the same day.\n**The audit asked whether every table had columns, a relationship and an owner, and this table had all three.** What it did not ask is whether a table with one column can do the job its name claims.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"inheritsFromRoleId":{"type":"string","format":"uuid","nullable":true,"description":"**Role composition, one level deep and no deeper.** A supervisor role that is a cashier plus three permissions is how venues actually describe them.\n**Cycles are refused and depth is capped at one**, because a permission set nobody can read off the screen is a permission set nobody audits.\n"},"isSystem":{"type":"boolean","default":false,"description":"**Seeded roles ship and are editable; deleting one is refused.** A venue that removes `cashier` and rebuilds it has two roles with one name in the audit log.\n**The seeded system roles are Cashier, Supervisor, Venue Manager, Finance and Tenant Admin** (proposed in `docs/active/seed-data-proposal.md` section 2, client to correct; audit R229).\n"},"principalCount":{"type":"integer"},"grantCount":{"type":"integer"}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"ScanEvent": {"x-ticvai-append-only":"recordedAt","x-ticvai-persistence":"access.scan_event","type":"object","required":["id","accessPointId","venueId","outcome","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The scan's client-generated UUIDv7, the key offline replay deduplicates on."},"accessPointId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"The `Entitlement.id` scanned; null where the media resolved to nothing."},"mediaCode":{"type":"string","nullable":true},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"direction":{"$ref":"#/components/schemas/Direction"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"overridesScanId":{"type":"string","format":"uuid","nullable":true,"description":"**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"},"overrideReason":{"type":"string","nullable":true,"description":"The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."},"dynamicPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."},"dynamicPolicyVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version of that policy in force at the scan, so a report spanning a change counts each version apart."},"dynamicPolicyResult":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"nullable":true,"description":"What the policy decided, which for a step-up is not the same as the scan's outcome."},"quantity":{"type":"integer","minimum":1,"default":1,"description":"Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."},"localSequence":{"type":"integer","nullable":true,"description":"The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."},"policySetVersion":{"type":"string","nullable":true,"description":"The admission policy set the scan was decided under (`OfflinePackage.policySetVersion`, or the same fingerprint computed online by `validateAccess`), beside the one policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`). ADR-0068, 1 October."},"packageVersion":{"type":"string","nullable":true,"description":"The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while pending. Differs from recordedAt for offline scans."}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"ScanSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer","description":"Entries processed before any stop."},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string"},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","reconciled","rejected"]},"serverOutcome":{"$ref":"#/components/schemas/ScanOutcome"},"divergence":{"type":"string","nullable":true,"description":"Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions","saleBoardId"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"Shift": {"x-ticvai-persistence":"orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident","description":"**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n","type":"object","required":["id","workstationId","venueId","scopePath","principalId","status","currency","currencyScale","openedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"workstationId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"principalId":{"type":"string","format":"uuid","description":"Who opened it. Cash reconciles to a person and a drawer."},"principalDisplayName":{"type":"string"},"incidents":{"type":"array","description":"BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["noSale","drawerOpen","override","voidAfterPayment","guestDispute","tillJam","priceQuery","other"]},"at":{"type":"string","format":"date-time"},"principalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}}},"status":{"$ref":"#/components/schemas/ShiftStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"depositBoxCode":{"type":"string","nullable":true},"bagNumber":{"type":"string","nullable":true},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"salesTotal":{"x-ticvai-column":"gross_sales_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till took in sales, as the guest paid it — tax included."},"refundsTotal":{"x-ticvai-column":"gross_refunded_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till paid back, as the guest was refunded it — tax included."},"liftsTotal":{"x-ticvai-column":"lifted_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."},"expectedCash":{"x-ticvai-column":"expected_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept.\n"},"countedCash":{"x-ticvai-column":"counted_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"What the close count found. Null until the shift is counted."},"variance":{"x-ticvai-column":"variance_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"Counted minus expected, as `ShiftCloseResult.variance`. Negative is short."},"heldLeaseCount":{"type":"integer","description":"Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"},"openedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded the open. `openedAt` is the server's time."},"suspendedAt":{"type":"string","format":"date-time","nullable":true},"suspendReason":{"type":"string","maxLength":200,"nullable":true,"description":"The `reason` given to `suspendShift`. Cleared on resume."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while the shift has unsynced operations."},"approvals":{"type":"array","items":{"type":"object","required":["kind","principalId","at"],"properties":{"kind":{"type":"string","enum":["open","close","variance"],"description":"`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string"}}}}}},
"ShiftCloseResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["shift","expectedCash","countedCash","variance","requiresAcceptance"],"properties":{"shift":{"$ref":"#/components/schemas/Shift"},"expectedCash":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"countedCash":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Counted minus expected. Negative is short."},"requiresAcceptance":{"type":"boolean","description":"True when the variance exceeds the venue's `shiftVarianceThreshold` (audit R094). The shift is then `pendingVariance` and only `acceptShiftVariance` finalises it (audit R080 (e)).\n"},"nonCashVariances":{"type":"array","items":{"type":"object","required":["tender","declared","captured","variance"],"properties":{"tender":{"type":"string"},"declared":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"captured":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"variance":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}}}},
"ShiftStatus": {"type":"string","enum":["pendingApproval","open","suspended","pendingVariance","pendingClosure","closed","autoClosed"]},
"SsoProtocol": {"type":"string","enum":["oidc","saml2"]},
"SsoProvider": {"x-ticvai-persistence":"identity.sso_provider","type":"object","required":["id","displayName","protocol"],"properties":{"id":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"protocol":{"$ref":"#/components/schemas/SsoProtocol"},"iconAssetRef":{"type":"string","nullable":true},"isEnforced":{"type":"boolean","description":"True disables password login for principals covered by this provider."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."}}},
"StockReservationSourceType": {"type":"string","enum":["workOrder","rentalAgreement","order","transfer","other"],"description":"What a stock reservation is for (decided 17 September, M17-02; `rentalAgreement` is the existing use from `rental.agreement_item`)."},
"SupervisorStepUp": {"type":"object","description":"**A supervisor signs the act in place, on the device making the call** (decided 28 September, audit R144). Used where the decision is a same-device step-up rather than an approval request: reopening a shift, recounting a stock count, a retail return above the venue threshold, and (proposed by the coordinator, client to confirm) closing a stock transfer short and cancelling a performance.\n\n**The verification rule, the same on every operation that takes it:** the server checks `credential` against `principalId`; that principal must hold the operation's `x-ticvai-permission` at the operation's scope, must be active at that venue, and must not be the person whose act is being reversed where the operation says so. Any failure is a `403` (`supervisor-step-up-refused`) and nothing is written. **No approval request is raised**, and the operation declares `x-ticvai-step-up: pin`.\n","required":["principalId","credential"],"properties":{"principalId":{"type":"string","format":"uuid","description":"The supervisor signing. Recorded against the act."},"credential":{"type":"string","maxLength":512,"writeOnly":true,"description":"The supervisor's staff PIN, as they sign in at a till with it. **A PIN, never a password** (audit R123 (7)). Never stored or returned."}}},
"TicketStatus": {"x-ticvai-persistence":"none — computed from entitlement and scans","description":"**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n","type":"object","required":["ticketId","isValid"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"Stable for the life of the ticket, independent of the media carrying it."},"mediaCode":{"type":"string","nullable":true},"productName":{"type":"string"},"holderName":{"type":"string","nullable":true,"description":"Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"},"isValid":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"reentryAllowed":{"type":"boolean"},"isInsideVenue":{"type":"boolean","description":"Derived from the last scan. Drives anti-passback evaluation."},"issuingCellId":{"type":"string","nullable":true,"description":"Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"},"guestLinkId":{"type":"string","nullable":true,"description":"Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"},"admissionRulesId":{"type":"string","format":"uuid"},"denyReason":{"$ref":"#/components/schemas/DenyReason"}}},
"TokenPair": {"x-ticvai-persistence":"none — transient","type":"object","required":["accessToken","refreshToken","expiresIn"],"properties":{"accessToken":{"type":"string","description":"JWT carrying `sid`, validated per request against the session registry."},"refreshToken":{"type":"string"},"expiresIn":{"type":"integer","description":"Seconds"}}},
"ValidateRequest": {"type":"object","required":["id","mediaCode","mediaKind","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key and dedupe key."},"mediaCode":{"type":"string","maxLength":256,"description":"What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"},"mediaKind":{"$ref":"#/components/schemas/MediaKind"},"direction":{"$ref":"#/components/schemas/Direction"},"groupSize":{"type":"integer","minimum":1,"description":"For group media admitting several holders on one read."},"proximityToken":{"type":"string","description":"BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"},"recordedAt":{"type":"string","format":"date-time","description":"Device time of the read. Authoritative for ordering, not for validity."}}},
"ValidationResult": {"x-ticvai-persistence":"none — computed, persisted as scan_event","type":"object","required":["scanId","outcome","accessPointId","recordedAt"],"properties":{"scanId":{"type":"string","format":"uuid"},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"denyDetail":{"type":"string","description":"Human-readable, localised. For operator display, never for logic."},"accessPointId":{"type":"string","format":"uuid"},"ticket":{"$ref":"#/components/schemas/TicketStatus"},"admittedCount":{"type":"integer","description":"Holders admitted on this read. Differs from groupSize on partial admission."},"recordedAt":{"type":"string","format":"date-time"},"serverEvaluatedAt":{"type":"string","format":"date-time"},"advisory":{"type":"object","nullable":true,"description":"BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n","properties":{"genderClassification":{"type":"string","enum":["women","men","undetermined"],"description":"**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"},"confidence":{"type":"number","minimum":0,"maximum":1,"description":"**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"},"reportedByDeviceId":{"type":"string","format":"uuid","description":"**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"}}}}},
"WithdrawalReason": {"type":"string","description":"Why a supervisor took cash out of a box. Set only on lifts `withdrawFromDepositBox` records.","enum":["banking","safeDrop","changeOrder","other"]},
"WorkOrder": {"x-ticvai-persistence":"maintenance.work_order","x-ticvai-retired-columns":["is_overdue"],"type":"object","required":["id","workOrderNumber","title","venueId","status","priority","kind","createdAt"],"properties":{"downtimeMinutes":{"type":"integer","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**Measured from out-of-service to back-in-service, not from work start to work end.** A ride down for six hours of which two were spent working is down six hours, and the gap between the two numbers is the thing worth managing.\n**Maintained on write**: set when the asset returns to service, as the minutes from the `maintenance.asset_status_change` row that took it out carrying this work order's id to the asset's next change back to `inService`. Null while the asset is still out, and for a work order that never took it out.\n"},"rootCause":{"type":"string","nullable":true,"enum":["wearAndTear","operatorError","guestDamage","manufacturingDefect","environmental","softwareFault","powerFailure","deferredMaintenance","unknown"],"description":"**Structured, because free text cannot be counted.** *Deferred maintenance* is the value a venue least wants to see and most needs to — a fault caused by work that was postponed is an argument for a budget.\n"},"rootCauseNote":{"type":"string","nullable":true},"escalatedAt":{"type":"string","format":"date-time","nullable":true},"escalationLevel":{"type":"integer","default":0,"description":"**Escalation is a clock, not a decision.** A work order on a ride nobody has accepted after twenty minutes escalates itself, because the alternative is somebody noticing.\n"},"id":{"type":"string","format":"uuid"},"workOrderNumber":{"type":"string","readOnly":true,"description":"**Server-assigned: the venue prefix plus a sequence per venue** (decided 28 September, audit R152). Not gapless; only tax invoices are gapless, per legal entity.\n"},"title":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"assetId":{"type":"string","format":"uuid","nullable":true},"assetName":{"type":"string","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The asset's name, copied when the work order is raised or its asset changes, and not updated when the asset is later renamed — the record reads as it was raised.\n"},"status":{"$ref":"#/components/schemas/WorkOrderStatus"},"priority":{"$ref":"#/components/schemas/WorkOrderPriority"},"priorityScore":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"readOnly":true,"description":"The score the venue's policy gave the fault when raised; null when a person or the asset set the priority (M17-01)."},"prioritySource":{"type":"string","enum":["scored","assetOverride","manual"],"readOnly":true,"description":"Where `priority` came from (M17-01). A change through `updateWorkOrder` makes it `manual`."},"faultAssessment":{"$ref":"#/components/schemas/WorkOrderFaultAssessment"},"requiredQualificationCodes":{"type":"array","items":{"type":"string"},"description":"Skills the job needs (M17-13)."},"kind":{"$ref":"#/components/schemas/WorkOrderKind"},"assignedToPrincipalId":{"type":"string","format":"uuid","nullable":true},"raisedByPrincipalId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"As raised in `CreateWorkOrderRequest.categoryId`, amendable by `updateWorkOrder`. The category is what `completeWorkOrder` reads to decide whether completion photographs are required.\n"},"locationDescription":{"type":"string","maxLength":500,"nullable":true,"description":"Where the fault is, as raised. Needed where there is no asset — a broken tile, a leak in a corridor.\n"},"elapsedMinutes":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Labour minutes accumulated up to the last pause or stop. **Maintained on write** by `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`; while `isTimerRunning` is true the interval since the last start is not yet included.\n"},"isTimerRunning":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Maintained on write by `startWorkOrder`, `resumeWorkOrder`, `recordWorkOrderTime`, `pauseWorkOrder` and `completeWorkOrder`.\n"},"dueAt":{"type":"string","format":"date-time","nullable":true},"isOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`dueAt` is in the past and the status is still `open`, `assigned`, `inProgress`, `paused` or `awaitingParts`. **Computed on read and not stored** — it depends on the clock. `listWorkOrders?overdueOnly` applies the same test to `due_at`.\n"},"requiresVerification":{"type":"boolean"},"sourcePlanId":{"type":"string","format":"uuid","nullable":true},"sourceInspectionId":{"type":"string","format":"uuid","nullable":true},"sourceIncidentId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"completedAt":{"type":"string","format":"date-time","nullable":true},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderAttachment": {"type":"object","x-ticvai-persistence":"maintenance.work_order_attachment","required":["id","workOrderId","kind","capturedAt"],"properties":{"id":{"type":"string","format":"uuid"},"workOrderId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["photo","video","document","note","signature"]},"assetRef":{"type":"string","format":"uuid","nullable":true},"text":{"type":"string","nullable":true},"stage":{"type":"string","enum":["before","during","after","signOff"],"nullable":true},"capturedByPrincipalId":{"type":"string","format":"uuid"},"capturedAt":{"type":"string","format":"date-time","description":"Device time. **Distinct from when it synced** — a photo taken at 09:14 in a basement and uploaded at 11:40 is evidence of the first, not the second.\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"WorkOrderDetail": {"x-ticvai-persistence":"maintenance.work_order","allOf":[{"$ref":"#/components/schemas/WorkOrder"},{"type":"object","properties":{"description":{"type":"string","nullable":true},"resolution":{"type":"string","nullable":true},"resolutionCode":{"$ref":"#/components/schemas/ResolutionCode"},"attachmentRefs":{"type":"array","items":{"type":"string"}},"timeEntries":{"type":"array","items":{"type":"object","properties":{"action":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"pauseReason":{"type":"string","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}}},"parts":{"type":"array","items":{"type":"object","properties":{"inventoryItemId":{"type":"string","format":"uuid"},"itemName":{"type":"string"},"quantity":{"type":"number"},"reservedQuantity":{"type":"number","description":"Still reserved for this work order and not yet issued (M17-02)."},"cost":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"labourCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"partsCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"totalCost":{"$ref":"../shared/common.yaml#/components/schemas/Money","x-ticvai-column":"net_cost_amount"},"completedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who called `completeWorkOrder`. **What `verifyWorkOrder` compares against** — the verifier may not be the technician who completed the work, and the assignee is not necessarily that person.\n"},"followUpRequired":{"type":"boolean","default":false},"followUpNote":{"type":"string","maxLength":1000,"nullable":true},"verificationOutcome":{"type":"string","enum":["verified","rejected"],"nullable":true,"description":"The latest `verifyWorkOrder` outcome."},"verificationNote":{"type":"string","maxLength":1000,"nullable":true},"verifiedAt":{"type":"string","format":"date-time","nullable":true},"verifiedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"cancelReason":{"type":"string","enum":["raisedInError","duplicate","superseded","noLongerRequired"],"nullable":true},"cancelNote":{"type":"string","maxLength":300,"nullable":true},"supersededByWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `cancelWorkOrder` where the reason is `superseded`."},"cancelledAt":{"type":"string","format":"date-time","nullable":true},"closeOutcome":{"type":"string","enum":["completedAndVerified","notReproducible","supersededByReplacement","noLongerApplicable","duplicate"],"nullable":true},"closeNote":{"type":"string","maxLength":500,"nullable":true},"duplicateOfWorkOrderId":{"type":"string","format":"uuid","nullable":true,"description":"Set by `closeWorkOrder` where the outcome is `duplicate`."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true}}}]},
"WorkOrderFaultAssessment": {"x-ticvai-persistence":"none — columns on maintenance.work_order","type":"object","description":"What the person raising a fault says about it, which the priority score reads (M17-01).","properties":{"safetyRisk":{"type":"boolean","default":false},"guestImpact":{"type":"string","enum":["none","degraded","closed"],"default":"none"}}},
"WorkOrderKind": {"type":"string","enum":["corrective","planned","inspectionFollowUp","incidentCorrective","improvement"]},
"WorkOrderPriority": {"type":"string","enum":["low","normal","high","urgent","emergency"]},
"WorkOrderStatus": {"type":"string","enum":["open","assigned","inProgress","paused","awaitingParts","completed","verified","closed","cancelled"]},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
