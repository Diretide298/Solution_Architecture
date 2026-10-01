# P07-access-01 — P07 · Access (1 of 2)

**10 screens · 27 operations · 44 schemas · 10 permissions**

Platform P07 Venue Scanner · ships as **venue-staff-mobile** ·
staff audience · handheld ·
offline-capable

## Who this is for

**staff on handheld.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `ACCESS_OVERRIDE, ACCESS_VALIDATE, ORDER_CREATE, ORDER_VIEW, PERMISSION_VIEW, REPORT_VIEW_VENUE, SCOPE_VIEW, SHIFT_OPEN, TICKET_LOOKUP, TURNSTILE_MODE_SET`. A control nobody can use must say so,
  not sit enabled and fail.
- **14 of these operations work offline**: consumeCrossRegionEntitlement, endPodiumShift, getAccessPoint, getCrossRegionEntitlement, getCurrentSession, getCurrentShift, listAccessPoints, listBlacklist
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
| `SCN-001` | Sign in | B–D | 14 | 49 | 7 | 10 | 0 | 0 | — | notStarted (generated) |
| `SCN-002` | Access point & direction | B–D | 8 | 26 | 6 | 9 | 0 | 0 | — | notStarted (generated) |
| `SCN-003` | Ready to scan | B–D | 41 | 41 | 10 | 62 | 8 | 0 | — | notStarted (generated) |
| `SCN-007` | Group admission | B–D | 37 | 35 | 6 | 60 | 2 | 0 | — | notStarted (generated) |
| `SCN-008` | Manual entry | B–D | 37 | 35 | 6 | 60 | 1 | 0 | — | notStarted (generated) |
| `SCN-009` | Ticket lookup | B–D | 37 | 35 | 6 | 60 | 4 | 0 | — | notStarted (generated) |
| `SCN-011` | Delegated right | B–D | 4 | 16 | 5 | 0 | 0 | 0 | — | notStarted (generated) |
| `SCN-013` | Offline journal | B–D | 37 | 35 | 6 | 60 | 2 | 0 | — | notStarted (generated) |
| `SCN-014` | Sync & reconciliation | B–D | 74 | 40 | 6 | 62 | 3 | 0 | — | notStarted (generated) |
| `SCN-015` | Offline package | B–D | 37 | 35 | 6 | 60 | 0 | 0 | — | notStarted (generated) |

## Thin screens in this batch

**SCN-011 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `SCN-001` Sign in

**PIN or badge. Session carries the workstation.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PERMISSION_VIEW`, `SHIFT_OPEN` (1 read, 1 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listMfaMethods` reads the population and `getCurrentShift` reads one of them — list, select, act |
| Offline | **Signs in against the cached principal list from the last bundle.** A steward locked out at 08:00 because the venue wifi is down is a gate that does not open |
| Opens with | `shiftId` (session), `challengeId` (navigation) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/access/sign-in` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **createCashMovement removed 18 August** — attached by module resemblance, not by what this screen does. A screen that does not handle money should not be able to move it (CF-87's class). **Sign in.** The session carries the workstation, so the device cannot scan before it knows who is holding it. **Declared 20 August** — `isEntryPoint` existed in the schema and five platforms used none, so every screen in them read as unreachable. **`selectRole` and `resolvePermissions` wired 24 August.** ADR-0002 makes authorisation user-driven and **a sign-in screen that does not resolve a role is a sign-in that grants nothing** — found by walking F61. **Removed 24 August**: acceptShiftVariance, approveShiftOpen, closeShift, forceLogout, getShift, listActiveSessions, listCashMovements, listShifts, openShift, recordNoSale, reopenShift, resumeShift, revokeAllSessions, suspendShift. **Bulk-attach residue** — the 18 August defect that put identical operation sets on unrelated screens. A till does not cancel a performance, a staff app does not create roles, and **a scanner does not run a cash shift.**

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

**Form: Select role** (modal, opened by *Select role*; *Select role* calls `selectRole`, *Cancel* sends nothing)

**Collects what `selectRole` sends before it is called.** Required: `roleId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Role `roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `selectRole` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope

**Form: Resolve permissions** (modal, opened by *Resolve permissions*; *Resolve permissions* calls `resolvePermissions`, *Cancel* sends nothing)

**Collects what `resolvePermissions` sends before it is called.** Required: `principalId`, `roleId`. Optional: `atScopePath`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Principal `principalId` | picker: choose a principal | required | — | — | shows names, sends the id | — | `resolvePermissions` body |
| Role `roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `resolvePermissions` body |
| At scope path `atScopePath` | text field | optional | — | — | — | Optional. When supplied, the response also carries `decisionsAtScope`: PERMIT or DENY per permission at that node. | `resolvePermissions` body |

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
| Login (primary button) | `login` POST `/auth/login` | LoginRequest | LoginResponse | 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused. | opens modal first |
| Verify (primary button) | `verifyMfaChallenge` POST `/auth/mfa/challenge/{challengeId}/verify` | inline | inline | — | — |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |
| Select role (secondary button) | `selectRole` POST `/auth/select-role` | inline | Session | 403 Authenticated but not permitted at the requested scope | opens modal first |
| Resolve permissions (secondary button) | `resolvePermissions` POST `/permissions/resolve` | inline | inline | — | opens modal first |

**Data it reads**: `getCurrentShift` (onLoad, From the flow it appears in); `getCurrentSession` (onLoad, Current session and effective permissions); `listMfaMethods` (onLoad, Enrolled MFA methods); `listSsoProviders` (onLoad, Identity providers configured for this tenant)

**Where the user goes next**

- → `SCN-002` Access point & direction: *Confirms access point and direction*
- → `SCN-003` Ready to scan: *Ready to scan*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sign list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sign untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sign yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listMfaMethods` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| MFA required (`?state=mfaRequired`) | **Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any platform-staff permission, or one the tenant added), so after `login` the screen calls `createMfaChallenge` and asks for the authenticator code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says so. A principal with no enrolled method is sent to enrol first … |
| Offline (`?state=offline`) | **Signs in against the cached principal list from the last bundle.** A steward locked out at 08:00 because the venue wifi is down is a gate that does not open |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused. |

#### Permissions

- `login` → no permission · anonymous, partner
- `getCurrentShift` → `SHIFT_OPEN` (operate) · staff
- `getCurrentSession` → no permission · staff, partner
- `listMfaMethods` → no permission · staff, partner, guest
- `listSsoProviders` → no permission · anonymous, partner
- `selectRole` → no permission · staff
- `resolvePermissions` → `PERMISSION_VIEW` (read) · staff
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest

**A refused user sees:** Shown when the caller lacks `SHIFT_OPEN`, which `getCurrentShift` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.5 | The system should have the option to be used by several waiters at the same time. | F&B & Guest Management | CONTRACTED | `login` |
| 5.8.2 | The system should only allow one session per user. | F&B & Guest Management | CONTRACTED | `login` |
| 3.3.28 | Authorization Caching - System shall support caching of authorization decisions. | Admission and Access | CONTRACTED | `getCurrentSession` |
| 7.1.50 | Cache authorization decisions securely to improve performance while ensuring policy changes invalidate outdated cache entries. | F&B POS | CONTRACTED | `getCurrentSession` |
| 7.1.4 | The system should be able to have a login override option for the supervisor level in order to login to the POS if the need arises and the previous user has not logged out. | F&B POS | CONTRACTED | `selectRole` |
| 3.3.27 | Real-Time Authorization - System shall evaluate access decisions in real time. | Admission and Access | CONTRACTED | `resolvePermissions` |
| 7.1.15 | The system shall support inheritance of permissions from parent roles, groups, departments, venues, or business structures while allowing controlled overrides. | F&B POS | CONTRACTED | `resolvePermissions` |
| 7.1.31 | The system shall restrict access to guest profiles, CRM data, financial data, wallet data, loyalty data, membership data, inventory costs, and marketing data based on permissions. | F&B POS | CONTRACTED | `resolvePermissions` |
| 7.1.51 | Evaluate authorization decisions in real time for every protected transaction, screen, API call or business action. | F&B POS | CONTRACTED | `resolvePermissions` |
| 2.13.44 | Incident & Exception Logging | Ticketing Sales | CONTRACTED | data `Shift` |

#### Client meeting inputs

None names this screen.

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-001` · status **notStarted** · provenance generated
- Flow F06 *Guest enters the venue*, step 1: Steward signs in with PIN or badge → Session carries the workstation, so every scan is attributable
- Flow F61 *A gate opens, a steward signs in, and a group is admitted*, step 1: The steward signs in and takes a role for the session. → **The person carries the authority, not the device** (ADR-0002). A handheld passed to a colleague at a break carries nothing with it, which is the property that makes a shared device safe.
- Flow F61 branch at step 1 (medium): when The steward has no role at this venue., Refused at sign-in rather than at first scan. **A person who reaches the lane and then cannot scan has already formed a queue behind them.**
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (14), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (49 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, mfaRequired, offline.
- [ ] Every action is wired with its success and its failure: Login, Verify, Email me a code instead, Select role, Resolve permissions.
- [ ] Every transition is wired: `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `PERMISSION_VIEW`, `SHIFT_OPEN`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-002` Access point & direction

**Confirm what this device is doing before it does it.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `SCOPE_VIEW`, `TURNSTILE_MODE_SET` (1 read, 1 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listAccessPoints` reads the population and `getAccessPoint` reads one of them — list, select, act |
| Offline | Fully offline. The access point list is in the bundle |
| Opens with | `accessPointId` (deepLink), `podiumId` (session), `shiftId` (session) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/access/access-point-direction` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Authoring operations removed 24 August**: createAccessPoint, setAccessPointGeofence, updateAccessPoint. **A scanner reads the gate configuration; it does not write it.** An access point is created in the back office and a geofence is a venue decision — a handheld at a lane that can redefine the lane is a handheld that can admit anywhere. **`setTurnstileMode` belongs here and flow F06 is why.** It was taken off on 4 September on the reasoning that this screen only reads — but F06 *guest enters the venue* step 2 is 'confirms access point and direction'. **Since 28 September (audit R221) confirming the direction is not setting the mode**: the direction is fixed per access point and shown here read-only; what the operator sets is the operating mode (required), with the turnstile mode (freeRotation or closed) as an optional narrowing under normal or podium only.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listAccessPoints`. | `listAccessPoints` ?venueId |

**Form: Save gate mode** (modal, opened by *Save gate mode*; *Save gate mode* calls `setTurnstileMode`, *Cancel* sends nothing)

**Collects what `setTurnstileMode` sends before it is called.** Required: `operatingMode` (normal, freeFlow, dropArm, closed, podium, maintenance). Optional: `mode` (freeRotation or closed), offered only with normal or podium, since the other four already decide the arm and the server refuses it 400; and `reason`. **Direction is not on this form**: it is fixed per access point and set in the back office (BO-064) with createAccessPoint/updateAccessPoint (decided 28 September, audit R221). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Operating mode `operatingMode` | select | required | — | Normal · Free flow · Drop arm · Closed · Podium · Maintenance | — | BL-107 and BL-109. What the gate does, and what the podium sets (`setTurnstileMode`, decided 28 September, audit R221). | `setTurnstileMode` body |
| Mode `mode` | segmented control | optional | — | Free rotation · Closed | — | Optional narrowing within `normal` or `podium`: `freeRotation` or `closed`. Null or absent, the turnstile validates in the access point's fixed direction. | `setTurnstileMode` body |
| Reason `reason` | text area | optional | — | max length 200 | — | — | `setTurnstileMode` body |
| Effective at `effectiveAt` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | When the change takes effect. | `setTurnstileMode` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: Start podium shift** (modal, opened by *Start podium shift*; *Start podium shift* calls `startPodiumShift`, *Cancel* sends nothing)

**Collects what `startPodiumShift` sends before it is called.** Nothing in the body is required. Optional: `role`, `accessDeviceId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Role `role` | text field | optional | — | max length 64 | — | Role the operator acts in on this podium | `startPodiumShift` body |
| Access device `accessDeviceId` | picker: choose an access device | optional | — | — | shows names, sends the id | The handheld or unit the operator signs in on, where it is not the podium itself | `startPodiumShift` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

**Form: End podium shift** (modal, opened by *End podium shift*; *End podium shift* calls `endPodiumShift`, *Cancel* sends nothing)

**Collects what `endPodiumShift` sends before it is called.** Nothing in the body is required. Optional: `handoverNote`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Handover note `handoverNote` | text area | optional | — | max length 1000 | — | — | `endPodiumShift` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 `shift-ended`: the shift is already ended.

#### Outputs: what the screen shows and produces

**Shown**

**Every access point** (data table, from `listAccessPoints`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| External credential sources | list or chips (count when long) | BL-108. A hotel room card admitting a guest to a water park — externally issued, and the platform validates it without having sold it. |
| Scan anomaly rules | list or chips (count when long) | BL-104. Rule-based scan anomalies, separated from the parked model-based engine — device sharing, simultaneous entries at two gates, an … |
| Operating mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Set by the podium with `setTurnstileMode`, and it wins (audit R221). BL-107 and BL-109. |
| Vehicle location capture | yes / no (icon or chip) | BL-023. Nothing helped a guest find their vehicle. |
| Mode | chip: Free rotation, Closed | Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates … |
| Direction | chip: Entry, Exit, Reentry, Crossover | Fixed per access point (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium. |
| Anti passback enabled | yes / no (icon or chip) | — |

**The selected access point** (detail panel, from `getAccessPoint`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| External credential sources | list or chips (count when long) | BL-108. A hotel room card admitting a guest to a water park — externally issued, and the platform validates it without having sold it. |
| Scan anomaly rules | list or chips (count when long) | BL-104. Rule-based scan anomalies, separated from the parked model-based engine — device sharing, simultaneous entries at two gates, an … |
| Operating mode | chip: Normal, Free flow, Drop arm, Closed, Podium, Maintenance | Set by the podium with `setTurnstileMode`, and it wins (audit R221). BL-107 and BL-109. |
| Vehicle location capture | yes / no (icon or chip) | BL-023. Nothing helped a guest find their vehicle. |
| Mode | chip: Free rotation, Closed | Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates … |
| Direction | chip: Entry, Exit, Reentry, Crossover | Fixed per access point (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium. |
| Anti passback enabled | yes / no (icon or chip) | — |
| Is active | yes / no (icon or chip) | — |
| Last heartbeat at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save gate mode (primary button) | `setTurnstileMode` PUT `/access-points/{accessPointId}/mode` | inline | AccessPoint | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; opens modal first |
| Start podium shift (secondary button) | `startPodiumShift` POST `/podiums/{podiumId}/shifts` | inline | AccessPodiumShift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; gated `TURNSTILE_MODE_SET`; opens modal first |
| End podium shift (secondary button) | `endPodiumShift` POST `/podium-shifts/{shiftId}/end` | inline | AccessPodiumShift | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; gated `TURNSTILE_MODE_SET`; opens modal first |

**Data it reads**: `listAccessPoints` (onLoad, From the flow it appears in)

**Where the user goes next**

- → `SCN-015` Offline package: *Loads the offline package*
- → `SCN-001` Sign in: *Sign in*
- → `SCN-003` Ready to scan: *Ready to scan*
- → `SCN-016` Gate mode: *Gate mode*; carries `accessPointId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The access point direction list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the access point direction untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No access point direction yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId and the access point direction are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SCOPE_VIEW`, which `listAccessPoints` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Fully offline. The access point list is in the bundle |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 `shift-ended`: the shift is already ended. |

#### Permissions

- `listAccessPoints` → `SCOPE_VIEW` (read) · staff
- `getAccessPoint` → `SCOPE_VIEW` (read) · staff
- `setTurnstileMode` → `TURNSTILE_MODE_SET` (operate) · staff
- `startPodiumShift` → `TURNSTILE_MODE_SET` (operate) · staff
- `endPodiumShift` → `TURNSTILE_MODE_SET` (operate) · staff

**A refused user sees:** Shown when the caller lacks `SCOPE_VIEW`, which `listAccessPoints` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

9 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.27 | The system should have the ability to customize / configure / manage software on turnstiles and making it behave differently depending on type of card used. There should be the possibility to add … | Admission and Access | CONTRACTED | `setTurnstileMode` |
| 3.2.28 | The system should support turnstiles of multiple sizes. For example, larger turnstiles for buggies. | Admission and Access | CONTRACTED | `setTurnstileMode` |
| 3.2.56 | It is expected to have the possibility to set the access control on Free spin mode, meaning that no ticket is read at access control point, still the turnstile shall be able to count how many times … | Admission and Access | CONTRACTED | `setTurnstileMode` |
| 19.2.77 | Parking Locator - System shall help guests locate vehicles. | Guest Mobile App & Branding | CONTRACTED | data `AccessPoint` |
| 3.1.8 | The system shall detect suspicious QR usage patterns including device sharing, multiple simultaneous sessions, excessive activations, and abnormal access attempts, with configurable security … | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.32 | Real-time fraud-monitoring & unified identity lock (one media per visit, Face-change audit, POD/Nanny linkage) | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.57 | In case of emergency, a drop arm mode can be activated at turnstiles. No scan and no count are being performed. | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.61 | It is possible for the system to integrate with hotels room card management system in order to read the room card at access control points and have the ability to interface to the hotels property … | Admission and Access | CONTRACTED | data `AccessPoint` |
| 3.2.73 | The access control can support a Podium feature with functions such as but not limited to: -podium is either in the form of a keyboard interface on the turnstile or a handheld tablet operated by the … | Admission and Access | CONTRACTED | data `AccessPoint` |

#### Client meeting inputs

None names this screen.

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-002` · status **notStarted** · provenance generated
- Flow F06 *Guest enters the venue*, step 2: Confirms access point and direction → The device knows what it is doing before it does it
- Flow F61 *A gate opens, a steward signs in, and a group is admitted*, step 2: They pick an access point and a direction. → **Direction is a choice and not an inference.** The same lane runs entry in the morning and exit at close, and a scanner that guesses will count a departure as an arrival.

#### Acceptance for the design

- [ ] Every input above is drawn (8), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (26 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-002?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save gate mode, Start podium shift, End podium shift.
- [ ] Every transition is wired: `SCN-015`, `SCN-001`, `SCN-003`, `SCN-016`.
- [ ] Every gated control is gated: `SCOPE_VIEW`, `TURNSTILE_MODE_SET`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-003` Ready to scan

**The screen the device sits on all day.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `SCOPE_VIEW`, `TICKET_LOOKUP` (4 operate, 1 read); in the flows as contractor, gate operator, guest, partner |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | **Same loop, different truth. Amber says so.** Was a separate screen until 18 August, and the screen already had an `offline` state — two places describing one condition is two places to disagree. |
| Opens with | `mediaCode` (deepLink), `rightId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/access/ready-to-scan` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Absorbed SCN-004, SCN-005, SCN-006, SCN-010, SCN-012 on 18 August.** A scanner is one screen the device sits on all day, and an outcome is a state of it — **routing to `/access/admitted` for something gone in 1.5 seconds is a page load per guest**, and at a gate doing 40 a minute that is the whole problem. Every absorbed screen kept its copy as a named state. **Authoring operations removed 24 August**: addBlacklistEntry, removeBlacklistEntry. **A scanner reads the gate configuration; it does not write it.** An access point is created in the back office and a geofence is a venue decision — a handheld at a lane that can redefine the lane is a handheld that can admit anywhere.

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

**Form: Consume cross region entitlement** (modal, opened by *Consume cross region entitlement*; *Consume cross region entitlement* calls `consumeCrossRegionEntitlement`, *Cancel* sends nothing)

**Collects what `consumeCrossRegionEntitlement` sends before it is called.** Required: `id`, `entries`, `scanId`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `consumeCrossRegionEntitlement` body |
| Entries `entries` | number field | required | — | min 1 | — | — | `consumeCrossRegionEntitlement` body |
| Scan `scanId` | picker: choose a scan | required | — | — | shows names, sends the id | — | `consumeCrossRegionEntitlement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `consumeCrossRegionEntitlement` body |

Errors to draw in the form: 409 Entries exhausted, or the right is revoked or outside its window

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

**Every blacklist entry** (data table, from `listBlacklist`)

| Shows | Format | Notes |
|---|---|---|
| Media code | text | Unique within the tenant (decided 28 September, audit R108): one entry per code. |
| Reason | text | — |
| Added at | 1 Oct 2026, 14:30 | — |
| Added by principal | the name it points at, never the id | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

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
| Consume cross region entitlement (secondary button) | `consumeCrossRegionEntitlement` POST `/cross-region-entitlements/{rightId}/consume` | inline | CrossRegionEntitlement | 409 Entries exhausted, or the right is revoked or outside its window | works offline; opens modal first |

**Data it reads**: `listScans` (onLoad, List scan events); `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation); `listBlacklist` (onLoad, From the flow it appears in)

**Where the user goes next**

- → `SCN-007` Group admission: *A school party of forty arrives on one booking*
- → `SCN-014` Sync & reconciliation: *Syncs the journal when signal returns*
- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *Ready to scan*; carries `mediaCode`, `rightId`
- → `PTR-015` Order History: *Reviews usage*; calls `validateAccess`
- → `SCN-011` Delegated right: *Delegated right*; carries `rightId`

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A ready scan this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ready scan list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ready scan untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ready scan yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the ready scan are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Same loop, different truth. Amber says so.** Was a separate screen until 18 August, and the screen already had an `offline` state — two places describing one condition is two places to disagree. |
| Admitted (`?state=admitted`) | **Green, and gone in 1.5 seconds.** The absorbed SCN-004. Shows what was admitted and against which right; at a gate doing 40 a minute this is the state the device is in most of the time. |
| Denied (`?state=denied`) | Denied with the reason and the time of the previous scan. **The reason matters more than the refusal** — a steward has to explain it to somebody standing in front of them. The absorbed SCN-005. |
| Override required (`?state=overrideRequired`) | A supervisor override, which requires a permission a steward may not hold, and records who, why and when. The absorbed SCN-006. |
| Blocked (`?state=blocked`) | Blacklisted or otherwise barred. **No override is offered on the device** — this is not a judgement a steward makes at a lane. The absorbed SCN-010. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 No identifier supplied; 400 Validation failed; 409 Entries exhausted, or the right is revoked or outside its window |

#### Permissions

- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff
- `consumeCrossRegionEntitlement` → `ACCESS_VALIDATE` (operate) · staff
- `listBlacklist` → `SCOPE_VIEW` (read) · staff
- `verifyAccreditationCredential` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

62 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

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
| … 50 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Qossai: walk-in, virtual-queue and VIP guests must be distinguished at the ride; VQ guests are never merged into the VIP line (would erode paid value); VQ arrivals need their own handling, e.g. a separate line or a QR scan within the arrival window. *(agreed · MoM 7 Sep 2026, 4.15 Virtual Queue - Three-Tier Guest Model · DI-678)*
- Access decisions consider who, ticket type, where, when and context; e.g. an otherwise valid unused ticket is denied once the venue's maximum live occupancy is reached, until guests exit. Scanners need a venue-full denial state. *(agreed · MoM 2 Sep 2026, 4.16 Attribute-Based Access Control · DI-650)*
- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*
- A successful scan marks the ticket used even if the guest did not pass (stroller, turnstile re-locked). Genuine cases are resolved manually by security from the ticket's scan-history log, so scanner lookup must show it. *(agreed · MoM 2 Sep 2026, 4.3 Decision (scan without physical passage) · DI-627)*
- Qossai: where a waiver is required before entry, an incomplete waiver can block ticket download, activation, check-in or access; ticket and scan screens need a waiver-incomplete state. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-574)*
- If a guest exits without a matching checkout scan (e.g. a manually opened door), the system flags it and blocks the next re-entry scan until check-in/check-out is reconciled. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-461)*
- Entitlements go beyond admission — e.g. a combo of park admission + an F&B item + a retail item, each redeemed by QR scan at its counter. Admission entitlements cap entries per ticket (e.g. max 2); product entitlements give a time-bound window (e.g. 60 minutes from first scan). *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-458)*
- **Open question.** Access-control scan result screens show customer photo, ticket information and validity status; details deferred to a future workshop. *(open · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-129)*

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-003` · status **notStarted** · provenance generated
- Flow F06 *Guest enters the venue*, step 4: Waits at the ready screen → The loop. The device sits here all day **Calls nothing** — the ready screen is idle by design, which is what makes the next scan instant.
- Flow F06 *Guest enters the venue*, step 5: Scans and admits → Green, party size, and the entitlement is consumed locally
- Flow F10 *Partner books, uses and settles*, step 4: A customer arrives and is admitted → The voucher is redeemed at a gate, possibly offline
- Flow F19 *A membership works in another country*, step 3: Guest scans at the other venue → Validated against the propagated right in the local bundle
- Flow F23 *A contractor gets a badge and uses it*, step 4: A steward scans it at a service gate → Against an admission profile with zones and hours
- Flow F23 *A contractor gets a badge and uses it*, step 5: Revoked immediately when the contract ends → **The blacklist is in the bundle**, so revocation works offline
- Flow F61 *A gate opens, a steward signs in, and a group is admitted*, step 4: A guest presents a ticket and it scans. → **Decided locally against the package**, in under 300ms. `frozenDays` is held rather than replayed precisely because the gate cannot afford the arithmetic.
- Flow F61 *A gate opens, a steward signs in, and a group is admitted*, step 7: The session ends and the device syncs. → Scans posted in sequence. **A duplicate scan across two devices is resolved on sync, not at the gate** — refusing a guest because another lane might have seen them is a queue nobody accepts.
- … and 1 more flow steps (`flows/`)
- Flow F06 branch at step 5 (recoverable): when Entitlement already fully consumed, SCN-003 shows denied with the reason and the time of the previous scan. **The reason matters more than the denial** — a steward facing a guest needs to say what happened, not just no.
- Flow F06 branch at step 5 (requiresStaff): when Guest is blacklisted, SCN-003, handled differently from an ordinary denial: no override offered on the device, and a supervisor is summoned.
- Flow F06 branch at step 5 (recoverable): when Media unreadable — damaged QR, dead phone, SCN-008 manual entry by reference, or SCN-009 lookup by name. Both are slower and both are necessary.
- Flow F06 branch at step 5 (recoverable): when Party larger than the entitlement, SCN-007 group admission admits what is valid and states the shortfall, rather than refusing the whole party at a gate with a queue behind it.
- Flow F06 branch at step 5 (requiresStaff): when Steward believes the denial is wrong, Supervisor override on SCN-003, which requires a permission a steward may not hold and records who, why and against which scan.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (41), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (41 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-003?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline, admitted, denied, overrideRequired, blocked.
- [ ] Every action is wired with its success and its failure: Sync scans, Lookup ticket, Override access, Validate access, Validate group access, Consume cross region entitlement.
- [ ] Every transition is wired: `SCN-007`, `SCN-014`, `SCN-001`, `SCN-002`, `SCN-003`, `PTR-015`, `SCN-011`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `SCOPE_VIEW`, `TICKET_LOOKUP`.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-007` Group admission

**Partial admission is the normal case, not the error.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Fully offline. Admits what is valid and states the shortfall |
| Opens with | nothing: it opens on its own |
| Route | `/access/group-admission` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

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
| Validate group access (primary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |
| Lookup ticket (secondary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Sync scans (secondary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |

**Data it reads**: `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation); `listScans` (onLoad, List scan events)

**Where the user goes next**

- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *The session ends and the device syncs*; carries `mediaCode`, `rightId`; calls `listScans`

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A group admission this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The group admission list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the group admission untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No group admission yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the group admission are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Fully offline. Admits what is valid and states the shortfall |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Permissions

- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

60 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.120 | Group entry validation | Ticketing Catalogue | CONTRACTED | `validateGroupAccess` |
| 3.2.13 | The system should be able to indicate the exact number of people in the group to the control agent upon verification of a group ticket, and support the entry of actual attendants in the scanner to … | Admission and Access | CONTRACTED | `validateGroupAccess` |
| 3.2.33 | Entrance flow and queuing need improvement, especially for large B2B groups. B2B group leaders need a faster way to validate multiple tickets stored on one device. | Admission and Access | CONTRACTED | `validateGroupAccess` |
| 3.7.2 | The system should be able to allow faster entry process for external Tour operators handling huge groups with one external ticketing media (group of ten guests visiting the park with one ticket … | Admission and Access | CONTRACTED | `validateGroupAccess` |
| 7.4.28 | For each PLU, it is possible to manage Ticket valid for one guest or more than one guest | F&B POS | CONTRACTED | `validateGroupAccess` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |
| … 48 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Group ticket QR options: one QR valid for a defined headcount, individual QR per member, or a single rotating/multi-use QR scanned until the headcount is exhausted. *(client request · MoM 31 Aug 2026, 4.8 Group Operations, Payment Links & Check-In · DI-569)*
- Group tickets can carry one shared QR code or individual QR codes, with partial check-in tracking; family tickets bundle adult/child pricing. *(agreed · MoM 5 Aug 2026, 4. Ticket Catalogue & Product Types · DI-137)*

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-007` · status **notStarted** · provenance generated
- Flow F61 *A gate opens, a steward signs in, and a group is admitted*, step 5: A school party of forty arrives on one booking. → **One credential, forty admissions, counted individually.** A group scanned as a single event is a group the venue cannot evacuate — occupancy needs the count, not the booking.
- Flow F61 *A gate opens, a steward signs in, and a group is admitted*, step 6: Thirty-eight go through and two are missing. → **The group stays open and the remaining two can arrive later.** A group closed at the first scan forces two children to be refused at the gate their teacher just walked through.
- Flow F61 branch at step 5 (high): when The group is larger than the booking., **Admitted up to the booking and the excess is an override.** A steward at a gate with a teacher and two extra children needs a decision recorded, not a refusal — and `overrideAccess` records who …
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-007?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Validate group access, Lookup ticket, Override access, Sync scans, Validate access.
- [ ] Every transition is wired: `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-008` Manual entry

**Damaged media, dead phone battery, printed slip.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Searches the bundle only. A reference issued after the last sync will not be found, and the screen says so rather than denying |
| Opens with | nothing: it opens on its own |
| Route | `/access/manual-entry` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Access point id | picker: choose an access point (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?accessPointId=` to `listScans`. | `listScans` ?accessPointId |
| Ticket id | picker: choose a ticket (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ticketId=` to `listScans`. | `listScans` ?ticketId |
| Outcome | segmented control | optional | — | Admitted · Denied · Overridden | — | Sends `?outcome=` to `listScans`. | `listScans` ?outcome |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listScans`. | `listScans` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listScans`. | `listScans` ?recordedTo |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |

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
| Lookup ticket (primary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Sync scans (secondary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Data it reads**: `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation); `listScans` (onLoad, List scan events)

**Where the user goes next**

- → `SCN-009` Ticket lookup: *The ticket is found and its history read*; calls `lookupTicket`
- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *Ready to scan*; carries `mediaCode`, `rightId`

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A manual entry this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason`, `recordedAt`.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The manual entry list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the manual entry untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No manual entry yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the manual entry are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Searches the bundle only. A reference issued after the last sync will not be found, and the screen says so rather than denying |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Permissions

- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

60 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.17 | The system should have the ability to scan a ticket into a POS terminal and display record of ticket’s history: transaction time, clerk, payment method, etc. | Admission and Access | CONTRACTED | `lookupTicket` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| … 48 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-008` · status **notStarted** · provenance generated
- Flow F62 *A ticket will not scan*, step 1: The steward types the reference by hand. → **Typed, not guessed.** A lookup that fuzzy-matches will admit the wrong guest at a gate.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-008?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket, Override access, Sync scans, Validate access, Validate group access.
- [ ] Every transition is wired: `SCN-009`, `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-009` Ticket lookup

**Reads. Does not admit, does not decrement.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Bundle only, and the bundle age is shown beside the results |
| Opens with | nothing: it opens on its own |
| Route | `/access/ticket-lookup` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Access point id | picker: choose an access point (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?accessPointId=` to `listScans`. | `listScans` ?accessPointId |
| Ticket id | picker: choose a ticket (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?ticketId=` to `listScans`. | `listScans` ?ticketId |
| Outcome | segmented control | optional | — | Admitted · Denied · Overridden | — | Sends `?outcome=` to `listScans`. | `listScans` ?outcome |
| Recorded from | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedFrom=` to `listScans`. | `listScans` ?recordedFrom |
| Recorded to | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Sends `?recordedTo=` to `listScans`. | `listScans` ?recordedTo |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |

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
| Lookup ticket (primary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Sync scans (secondary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Data it reads**: `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation); `listScans` (onLoad, List scan events)

**Where the user goes next**

- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *It is valid*; carries `mediaCode`, `rightId`

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A ticket lookup this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The ticket lookup list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the ticket lookup untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No ticket lookup yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the ticket lookup are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Bundle only, and the bundle age is shown beside the results |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Permissions

- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

60 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 3.2.17 | The system should have the ability to scan a ticket into a POS terminal and display record of ticket’s history: transaction time, clerk, payment method, etc. | Admission and Access | CONTRACTED | `lookupTicket` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| … 48 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Ticket lookup shows the complete scan history: purchaser, gate and timestamp for every attempt. Security can manually override to admit a guest despite a scan issue; every override is logged against the visitor's record. *(client request · MoM 2 Sep 2026, 4.16 Ticket Lookup & Manual Override · DI-649)*
- A successful scan marks the ticket used even if the guest did not pass (stroller, turnstile re-locked). Genuine cases are resolved manually by security from the ticket's scan-history log, so scanner lookup must show it. *(agreed · MoM 2 Sep 2026, 4.3 Decision (scan without physical passage) · DI-627)*
- Ticket look-up shows the ticket's full consumption history: transaction date/time, number of scans, expiry, and (if applicable) wallet balance and F&B/retail spend against that ticket. *(client request · MoM 25 Aug 2026, 4.7 Entitlements & Access Control · DI-462)*
- **Open question.** Access-control scan result screens show customer photo, ticket information and validity status; details deferred to a future workshop. *(open · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-129)*

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-009` · status **notStarted** · provenance generated
- Flow F62 *A ticket will not scan*, step 2: The ticket is found and its history read. → **When and where it was used, if it was.** *Already scanned* with no detail is an argument; *scanned at North Gate at 10:14* is an answer.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-009?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket, Override access, Sync scans, Validate access, Validate group access.
- [ ] Every transition is wired: `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-011` Delegated right

**A ticket issued in another cell, redeemed here.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_VALIDATE`, `TICKET_LOOKUP` (2 operate) |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | statusTracker (comfortable density): `getCrossRegionEntitlement` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | **Not available offline.** A delegated right issued in another region cannot be verified from a local bundle, and admitting on trust is how a pass gets used twice in two countries |
| Opens with | `rightId` (deepLink) · cold entry: **A staff link opened cold resolves the thing or says plainly that it is gone.** No silent redirect — a supervisor following a link from an alert needs to know … |
| Route | `/access/delegated-right` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

#### Inputs: what the user enters or picks

**Form: Consume cross region entitlement** (modal, opened by *Consume cross region entitlement*; *Consume cross region entitlement* calls `consumeCrossRegionEntitlement`, *Cancel* sends nothing)

**Collects what `consumeCrossRegionEntitlement` sends before it is called.** Required: `id`, `entries`, `scanId`, `recordedAt`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | — | `consumeCrossRegionEntitlement` body |
| Entries `entries` | number field | required | — | min 1 | — | — | `consumeCrossRegionEntitlement` body |
| Scan `scanId` | picker: choose a scan | required | — | — | shows names, sends the id | — | `consumeCrossRegionEntitlement` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `consumeCrossRegionEntitlement` body |

Errors to draw in the form: 409 Entries exhausted, or the right is revoked or outside its window

#### Outputs: what the screen shows and produces

**Shown**

**The cross region entitlement** (detail panel, from `getCrossRegionEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Right | the name it points at, never the id | — |
| Ticket | text | — |
| Guest link | text | — |
| Issuing cell name | text | — |
| Consuming cell name | text | — |
| Media codes | list or chips (count when long) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | — |
| Admission rules | the name it points at, never the id | — |
| Venue | the name it points at, never the id | Null where the right is valid at any venue in the consuming cell. |
| Entries allowed | 1,234 | Null means unlimited. |
| Entries consumed | 1,234 | — |
| Status | chip: Active, Exhausted, Revoked, Expired | — |
| Last consumed at | 1 Oct 2026, 14:30 | — |
| Last reconciled at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Consume cross region entitlement (primary button) | `consumeCrossRegionEntitlement` POST `/cross-region-entitlements/{rightId}/consume` | inline | CrossRegionEntitlement | 409 Entries exhausted, or the right is revoked or outside its window | works offline; opens modal first |

**Data it reads**: `getCrossRegionEntitlement` (onLoad, From the flow it appears in)

**Where the user goes next**

- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*
- → `SCN-003` Ready to scan: *Ready to scan*; carries `rightId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The delegated right, read by `getCrossRegionEntitlement`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the delegated right untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No delegated right yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TICKET_LOOKUP`, which `getCrossRegionEntitlement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | **Not available offline.** A delegated right issued in another region cannot be verified from a local bundle, and admitting on trust is how a pass gets used twice in two countries |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Entries exhausted, or the right is revoked or outside its window |

#### Permissions

- `getCrossRegionEntitlement` → `TICKET_LOOKUP` (operate) · staff
- `consumeCrossRegionEntitlement` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `TICKET_LOOKUP`, which `getCrossRegionEntitlement` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-011` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-011?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Consume cross region entitlement.
- [ ] Every transition is wired: `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_VALIDATE`, `TICKET_LOOKUP`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-013` Offline journal

**What the device decided, before anyone confirmed it.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | The journal is the offline record. It is why an offline admit is recoverable |
| Opens with | nothing: it opens on its own |
| Route | `/access/offline-journal` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

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
| Lookup ticket (primary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Sync scans (secondary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Data it reads**: `listScans` (onLoad, From the flow it appears in); `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation)

**Where the user goes next**

- → `SCN-014` Sync & reconciliation: *The network returns and the journal posts*; calls `listScans`
- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *Ready to scan*; carries `mediaCode`, `rightId`

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A offline journal this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline journal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline journal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline journal yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the offline journal are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | The journal is the offline record. It is why an offline admit is recoverable |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Permissions

- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `REPORT_VIEW_VENUE`, which `listScans` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

60 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.58 | In park attendance figure per ticket time is calculated in real time. | Admission and Access | CONTRACTED | `listScans` |
| 5.3.28 | Maintain detailed access validation history including gate entries, exits, attraction validations, RFID scans, QR scans, and turnstile events. | F&B & Guest Management | CONTRACTED | `listScans` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| … 48 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*
- Scanning must be native/installable and work fully offline, storing scans locally and syncing when connectivity returns. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-240)*

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-013` · status **notStarted** · provenance generated
- Flow F63 *A gate goes offline and reconciles*, step 2: Scans journal locally while the network is gone. → **Every scan is kept, including the refusals.** A refusal offline is as much a record as an admission.
- Flow F63 branch at step 2 (medium): when The same guest is scanned at two lanes, both offline., **Both post and the duplicate is a reconciliation task.** The guest is inside either way; the question is which lane counted them, and occupancy was wrong for a period.
- Flow F63 branch at step 2 (high): when The offline window exceeds the venue policy., **The gate keeps admitting.** Unlike a till, a gate that stops is a crowd — `maxOfflineHours` warns here rather than blocking.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-013?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket, Override access, Sync scans, Validate access, Validate group access.
- [ ] Every transition is wired: `SCN-014`, `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-014` Sync & reconciliation

**The screen nobody designs and everybody needs.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `ORDER_CREATE`, `ORDER_VIEW`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (5 operate, 1 read); in the flows as gate operator, guest |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listSyncRejections` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Not applicable. This screen exists to end the offline period |
| Opens with | nothing: it opens on its own |
| Route | `/access/sync-reconciliation` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. **Cross-platform navigation removed 24 August**: ADM-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listSyncRejections`. | `listSyncRejections` ?workstationId |
| Kind | radio group | optional | — | Order · Payment · Refund · Void · Scan | — | Sends `?kind=` to `listSyncRejections`. | `listSyncRejections` ?kind |
| Resolved | toggle | optional | — | — | — | Sends `?resolved=` to `listSyncRejections`. | `listSyncRejections` ?resolved |
|  | scan target | — | — | — | — | **A screen that validates a credential needs somewhere to point the camera.** `denied` and `hardwareError` look different because an operator facing a guest needs to know whether to try again or … | — |
| Search | search field | — | — | — | — | A search that returns nothing must say so differently from a search not yet run. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Since version | number field | — | — | `getOfflinePackage` ?sinceVersion |
| Valid from | date and time picker | — | — | `getOfflinePackage` ?validFrom |
| Valid to | date and time picker | — | — | `getOfflinePackage` ?validTo |
| Access point | picker: choose an access point | — | — | `listScans` ?accessPointId |
| Ticket | picker: choose a ticket | — | — | `listScans` ?ticketId |
| Outcome | segmented control | — | Admitted · Denied · Overridden | `listScans` ?outcome |
| Recorded from | date and time picker | — | — | `listScans` ?recordedFrom |
| Recorded to | date and time picker | — | — | `listScans` ?recordedTo |

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

**Form: Sync orders** (modal, opened by *Sync orders*; *Sync orders* calls `syncOrders`, *Cancel* sends nothing)

**Collects what `syncOrders` sends before it is called.** Required: `deviceId`, `orders`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Device `deviceId` | picker: choose a device | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Orders `orders` | repeatable rows | required | — | at least 1; at most 200 | — | — | `syncOrders` body |
| ID `orders[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. | `syncOrders` body |
| Venue `orders[].venueId` | picker: choose a venue | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Channel `orders[].channel` | select | required | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `syncOrders` body |
| Shift `orders[].shiftId` | picker: choose a shift | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Subject `orders[].subjectId` | picker: choose a subject | optional | — | — | shows names, sends the id | Null for an anonymous sale. Identity and entitlement are separate. | `syncOrders` body |
| Guest link `orders[].guestLinkId` | text field | optional | — | — | — | Present where the guest is linked across cells. | `syncOrders` body |
| Catalogue bundle version `orders[].catalogueBundleVersion` | text field | optional | — | — | — | The bundle the client priced from. Lets the server explain a variance rather than merely report one. | `syncOrders` body |
| Lines `orders[].lines` | repeatable rows | required | — | at least 1 | — | — | `syncOrders` body |
| ID `orders[].lines[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the line. `lineIds` everywhere in this contract are these. | `syncOrders` body |
| Variant `orders[].lines[].variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Recommendation `orders[].lines[].recommendationId` | picker: choose a recommendation | optional | — | — | shows names, sends the id | The `trackingId` of the ai `decideRecommendations` item this line came from (29 September, build, AI system design 2.2 A step 8), so a purchase is attributed to the recommendation … | `syncOrders` body |
| Performance `orders[].lines[].performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Booked window `orders[].lines[].bookedWindow` | group | optional | — | `endsAt` minus `startsAt` must equal the chosen variant's length (its `length` dimension value's `durationMinutes`), or the line is refused 422 `windowLengthMismatch`. | — | The booked time window of an hourly product, such as a meeting room (decided 29 September, rev 3 REV3-13: meeting rooms by the hour are in scope). | `syncOrders` body |
| Inventory hold `orders[].lines[].inventoryHoldId` | text field | optional | — | — | — | Lease the units were drawn from — a `catalogue.InventoryHold.id`. Absent for uncontended products. | `syncOrders` body |
| Seats `orders[].lines[].seatIds` | multi-picker: choose seats | optional | — | at most 50; At most `VenueSettings.; maxSeatsPerGuestOrder` seats per booking on a guest channel (default 10, bounds 1 to 50, decided 29 September, rev 3 REV3-7); at most 10 per sale on staff and POS (audit R080 (c)), across all the … | — | Seated products only, as `seating.Seat.id`. Not available offline. | `syncOrders` body |
| Resource hold `orders[].lines[].resourceHoldId` | picker: choose a resource hold | optional | — | — | shows names, sends the id | A `resources.ResourceHold` on a resource the guest picked on a venue map (decided 29 September, rev 3 REV3-15); `variantId` is the placed resource's price-band variant. | `syncOrders` body |
| Attributes `orders[].lines[].attributes` | group | optional | — | — | — | Open attributes of a line, kept from the cart to the order line. `transport` is the one with a defined shape (decided 29 September, rev 3 REV3-21); other keys are free. | `syncOrders` body |
| Quantity `orders[].lines[].quantity` | number field | required | — | min 1 | — | — | `syncOrders` body |
| Eligibility declaration `orders[].lines[].eligibilityDeclaration` | repeatable rows | optional | — | — | — | What was declared for each guest on this line, kept as the record staff check at the gate. | `syncOrders` body |
| Quoted unit price `orders[].lines[].quotedUnitPrice` | money field | required | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the client charged, from its local bundle. | `syncOrders` body |
| Holder name `orders[].lines[].holderName` | text field | optional | — | — | — | — | `syncOrders` body |
| Data mask values `orders[].lines[].dataMaskValues` | key and value settings | optional | — | — | — | Deliberately open. Custom fields keyed by the venue's data mask: the field definitions travel in the catalogue bundle (`catalogue.CatalogueBundle.payload`), so the keys are the … | `syncOrders` body |
| Recorded at `orders[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `syncOrders` body |
| Sequence `orders[].sequence` | number field | required | — | min 1 | — | Monotonic per device. Processed in this order. | `syncOrders` body |
| Payments `orders[].payments` | repeatable rows | required | — | — | — | — | `syncOrders` body |
| ID `orders[].payments[].id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header. | `syncOrders` body |
| Order `orders[].payments[].orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `syncOrders` body |
| Tender `orders[].payments[].tender` | select | required | — | Cash · Card · Wallet · Voucher · Bank transfer · Hotel charge · Installment · Gift card · Complimentary | — | `wallet` is a digital wallet (Apple Pay, Google Pay and the like, taken through the gateway), the value the guest channels accept beside `card` (decided 28 September, audit R080 … | `syncOrders` body |
| Amount `orders[].payments[].amount` | money field | required | — | A jsonb price cannot be summed in SQL. | AED, 2 decimals shown (up to 4 accepted), currency from the … | On the wire this is three fields; in the database it is one column. 24 August. | `syncOrders` body |
| Tender currency `orders[].payments[].tenderCurrency` | text field | optional | — | pattern `^[A-Z]{3}$` | — | The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. | `syncOrders` body |
| Tender amount `orders[].payments[].tenderAmount` | money field | optional | — | — | AED, 2 decimals shown (up to 4 accepted), currency from the … | What the guest handed over, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). | `syncOrders` body |
| Wallet authorisation `orders[].payments[].walletAuthorisationId` | text field | optional | — | — | — | Cross-cell wallet hold, where the guest's home cell is elsewhere. | `syncOrders` body |
| Wallet hold `orders[].payments[].walletHoldId` | picker: choose a wallet hold | optional | — | — | shows names, sends the id | For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table. | `syncOrders` body |
| Return URL `orders[].payments[].returnUrl` | URL field | optional | — | — | https:// | Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). | `syncOrders` body |
| Terminal `orders[].payments[].terminalId` | picker: choose a terminal | optional | — | — | shows names, sends the id | The card terminal to instruct, for a card payment at a till (ECR flow, SD-034). | `syncOrders` body |
| Device `orders[].payments[].deviceId` | picker: choose a device | optional | — | — | shows names, sends the id | — | `syncOrders` body |
| Recorded at `orders[].payments[].recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `syncOrders` body |

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

**Every sync rejection** (data table, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | — |
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Payload | grouped details | Deliberately open: the journal entry exactly as the till sent it. Its shape is the request schema for `kind` — an `OfflineOrder` for … |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolved by principal | the name it points at, never the id | — |

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

**The selected sync rejection** (detail panel, from `listSyncRejections`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Workstation | the name it points at, never the id | — |
| Kind | chip: Order, Payment, Refund, Void, Scan | — |
| Recorded at | 1 Oct 2026, 14:30 | — |
| Rejected at | 1 Oct 2026, 14:30 | — |
| Problem | grouped details | RFC 9457 problem details. Every error response uses this shape. |
| Payload | grouped details | Deliberately open: the journal entry exactly as the till sent it. Its shape is the request schema for `kind` — an `OfflineOrder` for … |
| Resolved at | 1 Oct 2026, 14:30 | — |
| Resolved by principal | the name it points at, never the id | — |
| Resolution | chip: Posted, Voided, Refunded | What `resolveSyncRejection` recorded. Null while the rejection waits. |
| Resolved record | the name it points at, never the id | The order, void or refund the resolution produced — what stops the entry being posted twice. |

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
| Sync orders (secondary button) | `syncOrders` POST `/sync/orders` | inline | OrderSyncResult | — | emits `order.paid`, `sync.rejectionRaised`; opens modal first |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Data it reads**: `listSyncRejections` (onLoad, From the flow it appears in); `getOfflinePackage` (onLoad, Entitlement and rule set for offline validation); `listScans` (onLoad, List scan events)

**Where the user goes next**

- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *Ready to scan*; carries `mediaCode`, `rightId`
- → `ADM-003` Cross-Tenant Health Dashboard: *Reconciliation confirms it*; calls `syncScans`

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A sync reconciliation this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The sync reconciliation list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the sync reconciliation untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No sync reconciliation yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on workstationId, kind, resolved and the sync reconciliation are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Not applicable. This screen exists to end the offline period |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Permissions

- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `listSyncRejections` → `ORDER_VIEW` (read) · staff
- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `syncOrders` → `ORDER_CREATE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ORDER_VIEW`, which `listSyncRejections` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

62 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 18.1.4 | Synchronization - System shall synchronize data when connectivity is restored. | Employee Mobile App & AI Assistant | CONTRACTED | `syncScans` |
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| … 50 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Handheld scanners read QR, RFID or other supported media. Offline, devices validate locally from data embedded in the credential, queue the transactions and auto-sync when connectivity returns. *(agreed · MoM 2 Sep 2026, 4.13 / 4.14 Handheld Scanners & Offline Mode · DI-646)*
- Scanning must be native/installable and work fully offline, storing scans locally and syncing when connectivity returns. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-240)*
- After reconnection, offline records sync in batches in the order events occurred, tagged with both the original recorded time and the sync time; syncing must not slow gate entry. *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-065)*

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-014` · status **notStarted** · provenance generated
- Flow F06 *Guest enters the venue*, step 6: Syncs the journal when signal returns → The server accepts most and may reject some
- Flow F19 *A membership works in another country*, step 4: The redemption syncs back → **Both cells must agree the pass was used**
- Flow F63 *A gate goes offline and reconciles*, step 3: The network returns and the journal posts. → **In sequence, not by timestamp.** Two handhelds with clocks a minute apart produce an order nobody can reconstruct.
- Flow F06 branch at step 6 (requiresStaff): when Server rejects a scan the device already admitted, SCN-014 reconciliation. The guest is already inside. This is a revenue and audit event, not a gate event, and it is why the journal exists.
- Flow F06 branch at step 6 (recoverable): when Journal too large to sync in one pass, Batched. The device keeps journalling while it syncs — a device that stops scanning to sync is a closed gate.
- Flow F19 branch at step 4 (requiresStaff): when Both cells think the pass was used once, at the same time, A single-entry pass redeemed in two countries in one day is either fraud or a clock. **The scan timestamps decide**, and both are retained with recordedAt and syncedAt for exactly this.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (74), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (40 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-014?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Sync scans, Lookup ticket, Override access, Sync orders, Validate access, Validate group access.
- [ ] Every transition is wired: `SCN-001`, `SCN-002`, `SCN-003`, `ADM-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `ORDER_CREATE`, `ORDER_VIEW`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `SCN-015` Offline package

**Rule changes land here, not instantly.**

| | |
|---|---|
| App · platform | TICVAI Venue Staff · P07 Venue Scanner (handheld) |
| Module | Access · wave 1 · needs the `access` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP` (4 operate); in the flows as gate operator |
| Device and orientation | This is a rugged handheld, 360 x 720, very large pass and fail states, readable in sunlight. · LTR and RTL · light theme |
| Pattern | listDetail (comfortable density): `listScans` reads the population and `getOfflinePackage` reads one of them — list, select, act |
| Offline | Cannot refresh. The existing bundle continues to be used and its age is shown |
| Opens with | nothing: it opens on its own |
| Route | `/access/offline-package` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written.

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
| Lookup ticket (primary button) | `lookupTicket` GET `/access/lookup` | — | TicketStatus | 400 Neither mediaCode nor ticketId supplied; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | works offline; produces a document or message: Read-only validity check without admitting |
| Override access (destructive button) | `overrideAccess` POST `/access/override` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 The scan was not a denial, or has already been overridden | works offline |
| Sync scans (secondary button) | `syncScans` POST `/access/scans` | inline | ScanSyncResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Validate access (secondary button) | `validateAccess` POST `/access/validate` | ValidateRequest | ValidationResult | 400 Validation failed; 403 Authenticated but not permitted at the requested scope; 404 Media not recognised in this cell | works offline; opens modal first |
| Validate group access (secondary button) | `validateGroupAccess` POST `/access/group-validate` | inline | ValidationResult | 403 Authenticated but not permitted at the requested scope; 409 Requested count exceeds the remaining group allowance | works offline; opens modal first |

**Data it reads**: `getOfflinePackage` (onLoad, From the flow it appears in); `listScans` (onLoad, List scan events)

**Where the user goes next**

- → `SCN-013` Offline journal: *Scans journal locally while the network is gone*; calls `getOfflinePackage`
- → `SCN-001` Sign in: *Sign in*
- → `SCN-002` Access point & direction: *Access point & direction*; carries `accessPointId`
- → `SCN-003` Ready to scan: *Waits at the ready screen*; carries `mediaCode`, `rightId`; calls `getOfflinePackage`

**What opens over it**

- confirmDialog *Override access*: **Names what `overrideAccess` changes and what it leaves alone**, in the consequence rather than the verb. A offline package this affects should be identified in the dialog, not just counted. **Collects what `overrideAccess` sends before it is called.** Required: `id`, `scanId`, `reason` …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The offline package list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the offline package untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No offline package yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on accessPointId, ticketId, outcome, recordedFrom, recordedTo and the offline package are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | Cannot refresh. The existing bundle continues to be used and its age is shown |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Neither mediaCode nor ticketId supplied; 400 Validation failed; 409 Requested count exceeds the remaining group allowance; 409 The scan was not a denial, or has already been overridden |

#### Permissions

- `getOfflinePackage` → `ACCESS_VALIDATE` (operate) · staff
- `listScans` → `REPORT_VIEW_VENUE` (operate) · staff
- `lookupTicket` → `TICKET_LOOKUP` (operate) · staff
- `overrideAccess` → `ACCESS_OVERRIDE` (operate) · staff
- `syncScans` → `ACCESS_VALIDATE` (operate) · staff
- `validateAccess` → `ACCESS_VALIDATE` (operate) · staff
- `validateGroupAccess` → `ACCESS_VALIDATE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `ACCESS_VALIDATE`, which `getOfflinePackage` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

60 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.13.38 | Offline Access Validation | Ticketing Sales | CONTRACTED | `getOfflinePackage` |
| 3.1.5 | Access control devices shall validate dynamic QR codes using secure offline cryptographic validation without requiring continuous connectivity to the central platform. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.1.10 | System shall support embedding entitlement information within secure QR, RFID, NFC, mobile wallet, and digital credential tokens. Embedded information may include ticket type, seat assignment, event … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.49 | The validity check logic allows offline validity check. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.2.75 | The access control can be operated in offline mode. Turnstiles can perform access control in absence of database access (database unavailable or not reachable). Key access control criteria can be … | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 3.3.30 | Distributed Policy Evaluation - System shall support local policy evaluation when offline. | Admission and Access | CONTRACTED | `getOfflinePackage` |
| 18.1.3 | Offline Mode - System shall support offline operation. | Employee Mobile App & AI Assistant | CONTRACTED | `getOfflinePackage` |
| 1.1.63 | Entitlement audit reporting | Ticketing Catalogue | CONTRACTED | `listScans` |
| 3.1.6 | The system shall maintain complete scan history including gate, location, timestamp, device ID, operator, validation result, and entry attempts. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.21 | The system should keep track of the count of people passing through an access control device. Multiple Access Control System can be grouped together to give the capacity count of a specific … | Admission and Access | CONTRACTED | `listScans` |
| 3.2.54 | If access control reading is valid, the attendance counter is increased by the number or Guests associated to the ticket. | Admission and Access | CONTRACTED | `listScans` |
| 3.2.55 | All Guests are invited use the turnstiles when leaving the park. It is expected that the system counts the number of exits. Scan can be required at exit. | Admission and Access | CONTRACTED | `listScans` |
| … 48 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 14 for all of P07, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P07 Venue Scanner.dc.html#scn-015` · status **notStarted** · provenance generated
- Flow F06 *Guest enters the venue*, step 3: Loads the offline package → Entitlements, blacklist and admission profiles are local from here
- Flow F61 *A gate opens, a steward signs in, and a group is admitted*, step 3: The device pulls its offline package for the session. → Entitlements valid for this point and this window, held locally. **Pulled before the session because a gate that fetches at first scan has already queued.**
- Flow F63 *A gate goes offline and reconciles*, step 1: The package is already on the device from before the session. → **Pulled before, not during.** A gate that fetches at first scan has already queued.
- ADR-0068 *Guest admission policy lives in Access only, and the offline package carries it* (`docs/adr/0068-guest-admission-policy-lives-in-access-only.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (37), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (35 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#SCN-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Lookup ticket, Override access, Sync scans, Validate access, Validate group access.
- [ ] Every transition is wired: `SCN-013`, `SCN-001`, `SCN-002`, `SCN-003`.
- [ ] Every gated control is gated: `ACCESS_OVERRIDE`, `ACCESS_VALIDATE`, `REPORT_VIEW_VENUE`, `TICKET_LOOKUP`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P07 reference designs** (from `handoff/design-batches/apps/3-scanner/README.md`)

- `sources/designs/TICVAI_Employee_App_UI_Reference_1.pdf`: the employee app reference. The scanner shares its look and its offline strip.
- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for density.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-035, DI-036, DI-037, DI-038, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P07 as a whole** (1: 0 open, 1 closed). Open first; a closed row says where it went on 30 September.

- **A229** Build turnstile and handheld scanner configuration (connection details, light and sound feedback by ticket type, custom welcome messaging and branding, compatibility testing and deployment) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S7 (HLD/LLD) · 2 Sep 2026 · workshop tracker)*

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

### Across P07 Venue Scanner

- Staff-facing POS and tablet UIs always carry TICVAI branding, not client branding. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-296)*
- A separate dedicated scanner app for devices used only for scanning (e.g. mounted at turnstiles/gates) shows only scanning functions; the same validation is also embedded in the employee app. *(agreed · MoM 10 Aug 2026, 5.7 Ticket Scanning / Access Control App · DI-239)*
- Two separate apps: an access-control app (handhelds or fixed terminals) scoped purely to entry validation/scanning, and an employee app (approvals, alerts/messages, matrix features) that may include a basic ticket-validity lookup but not full scanning. *(agreed · MoM 3 Aug 2026, 12. Mobile Application Strategy · DI-128)*
- Offline state must be clearly visible in the UI, e.g. a visible mode indicator or greyed-out unavailable functions; exact visual treatment to be settled in the UI/UX session. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-072)*
- Allam: the app detects loss of connectivity and switches to offline mode automatically, without cashier action, then restores online mode and syncs pending transactions automatically. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-071)*
- Offline capability applies to POS terminals, handheld/validation devices (turnstiles, scanners), and staff and customer mobile apps. *(agreed · MoM 31 Jul 2026, 11. Offline Functionality Scope · DI-070)*
- Validation works fully offline, with optional local BLE verification (Bluetooth must be on) to confirm the staff member is physically at the gate; BLE is configurable per venue. *(agreed · MoM 31 Jul 2026, 7. Ticket Validation & Offline Architecture · DI-063)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- POS: sell tickets, memberships, F&B, retail and services from one unified cashier experience. Access Control: real-time entry validation, occupancy monitoring, offline mode and gate management. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) - 04 Point of Sale; 03 Access Control · DI-035)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*
- During an outage the handheld validates tickets against a secure local database, stores scans locally and synchronises when connectivity returns; validation by QR format alone is not acceptable (fraud risk). *(agreed · MoM 28 Jul 2026, 15. Offline POS and Access-Control Operations · DI-013)*
- POS must keep selling general admission tickets during an internet outage, and access-control apps must keep scanning and validating tickets during a connectivity failure. *(agreed · MoM 28 Jul 2026, 15. Offline POS and Access-Control Operations · DI-012)*

**20 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"consumeCrossRegionEntitlement": {"method":"POST","path":"/cross-region-entitlements/{rightId}/consume","contract":"cross-region","summary":"Consume entries against a right, locally authoritative","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CrossRegionEntitlement"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"endPodiumShift": {"method":"POST","path":"/podium-shifts/{shiftId}/end","contract":"access","summary":"End an operator shift on a podium","permission":"TURNSTILE_MODE_SET","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPodiumShift"},
"getAccessPoint": {"method":"GET","path":"/access-points/{accessPointId}","contract":"access","summary":"Read an access point","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AccessPoint"},
"getCrossRegionEntitlement": {"method":"GET","path":"/cross-region-entitlements/{rightId}","contract":"cross-region","summary":"Read a redemption right","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"CrossRegionEntitlement"},
"getCurrentSession": {"method":"GET","path":"/auth/session","contract":"identity","summary":"Current session and effective permissions","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Session"},
"getCurrentShift": {"method":"GET","path":"/shifts/current","contract":"shift","summary":"The open or suspended shift on the session's workstation","permission":"SHIFT_OPEN","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Shift"},
"getOfflinePackage": {"method":"GET","path":"/access/offline-package","contract":"access","summary":"Entitlement and rule set for offline validation","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[{"name":"sinceVersion","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":"validFrom","in":"query","required":true},{"name":"validTo","in":"query","required":true},{"name":"If-None-Match","in":"header","required":null}],"requestBody":null,"responds":"OfflinePackage"},
"listAccessPoints": {"method":"GET","path":"/access-points","contract":"access","summary":"List access points","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBlacklist": {"method":"GET","path":"/blacklist","contract":"access","summary":"List blacklisted media","permission":"SCOPE_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMfaMethods": {"method":"GET","path":"/auth/mfa/methods","contract":"identity","summary":"Enrolled MFA methods","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MfaMethod"},
"listScans": {"method":"GET","path":"/access/scans","contract":"access","summary":"List scan events","permission":"REPORT_VIEW_VENUE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"accessPointId","in":"query","required":null},{"name":"ticketId","in":"query","required":null},{"name":"outcome","in":"query","required":null},{"name":"recordedFrom","in":"query","required":null},{"name":"recordedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSsoProviders": {"method":"GET","path":"/auth/sso/providers","contract":"identity","summary":"Identity providers configured for this tenant","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SsoProvider"},
"listSyncRejections": {"method":"GET","path":"/sync/rejections","contract":"orders","summary":"Entries the server refused","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"workstationId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"resolved","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"login": {"method":"POST","path":"/auth/login","contract":"identity","summary":"Authenticate and open a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LoginRequest","responds":"LoginResponse"},
"lookupTicket": {"method":"GET","path":"/access/lookup","contract":"access","summary":"Read-only validity check without admitting","permission":"TICKET_LOOKUP","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"mediaCode","in":"query","required":null},{"name":"ticketId","in":"query","required":null}],"requestBody":null,"responds":"TicketStatus"},
"overrideAccess": {"method":"POST","path":"/access/override","contract":"access","summary":"Admit against a failed validation","permission":"ACCESS_OVERRIDE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"resolvePermissions": {"method":"POST","path":"/permissions/resolve","contract":"identity","summary":"Simulate a principal's effective permissions","permission":"PERMISSION_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"selectRole": {"method":"POST","path":"/auth/select-role","contract":"identity","summary":"Choose a role for a multi-role session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Session"},
"setTurnstileMode": {"method":"PUT","path":"/access-points/{accessPointId}/mode","contract":"access","summary":"Set the operating mode of an access point","permission":"TURNSTILE_MODE_SET","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPoint"},
"startPodiumShift": {"method":"POST","path":"/podiums/{podiumId}/shifts","contract":"access","summary":"Start an operator shift on a podium","permission":"TURNSTILE_MODE_SET","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"AccessPodiumShift"},
"syncOrders": {"method":"POST","path":"/sync/orders","contract":"orders","summary":"Replay orders recorded offline","permission":"ORDER_CREATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"OrderSyncResult"},
"syncScans": {"method":"POST","path":"/access/scans","contract":"access","summary":"Replay scans recorded offline","permission":"ACCESS_VALIDATE","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ScanSyncResult"},
"validateAccess": {"method":"POST","path":"/access/validate","contract":"access","summary":"Validate media at an access point and admit or deny","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ValidateRequest","responds":"ValidationResult"},
"validateGroupAccess": {"method":"POST","path":"/access/group-validate","contract":"access","summary":"Admit a group on one read","permission":"ACCESS_VALIDATE","offlineCapable":true,"conflictPolicy":"append","scopeLevel":"workstation","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ValidationResult"},
"verifyAccreditationCredential": {"method":"GET","path":"/accreditation-credentials/verify","contract":"accreditation","summary":"Who holds this credential, and where may they go","permission":"ACCESS_VALIDATE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"identifier","in":"query","required":true},{"name":"zoneId","in":"query","required":null}],"requestBody":null,"responds":"AccreditationCredentialVerification"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessAccreditationCredential": {"type":"object","x-ticvai-persistence":"access.accreditation_credential","x-ticvai-agreed":"29 September: build pass (group OWN, from group RA's handoff; BL-181); the events accreditation.credentialIssued and accreditation.holderStatusChanged name access as their critical consumer","description":"**What a gate needs to admit an accredited person, kept by `access`** (29 September, build). Written only by the consumers of `accreditation.credentialIssued` (a row per credential; a replacement sets the replaced row's `admits` false) and `accreditation.holderStatusChanged` (every credential of the holder: `admits` false unless the holder is `active`, validity taken from the event). Read by `validateAccess` and shipped in the offline package. The record of truth stays in `accreditation`; this is a copy shaped for the gate, never edited by a person.","required":["id","holderId","encodedIdentifier","admits","scopePath"],"properties":{"id":{"type":"string","format":"uuid","description":"The accreditation credential's id (`credentialId` on the events)."},"holderId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid","nullable":true},"kind":{"type":"string","description":"printedBadge, mobileCredential, qr, nfcCard, rfidCard or wristband, as issued."},"encodedIdentifier":{"type":"string","x-ticvai-unique":"tenant","description":"What the gate reads from the credential. Never sent to webhook subscribers."},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"zoneIds":{"type":"array","description":"The holder's effective zones, from the event (`effectiveZones`).","items":{"type":"string","format":"uuid"}},"holderStatus":{"type":"string","enum":["active","suspended","revoked","expired","archived"],"description":"The holder's status as last published; only `active` admits."},"admits":{"type":"boolean","description":"False once the credential is replaced or the holder is not active."},"sourceChangedAt":{"type":"string","format":"date-time","description":"The `issuedAt` or `changedAt` of the event last applied; an older event arriving late is ignored."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005), the accreditation programme's scope."}}},
"AccessDynamicPolicy": {"type":"object","x-ticvai-persistence":"access.dynamic_policy","description":"One guest-admission dynamic (attribute-based) policy with its current content - type, context or identity it tests, condition expression, result, priority, zones, validity, status and current version. Not identity.authorisation_policy, which is staff permission (declared 29 September, data-model close-out DM1).\n\n**Guest admission lives here and nowhere else** (ADR-0068, accepted 1 October). `validateAccess` online and the gate offline evaluate the same active version: `getOfflinePackage` carries it, and every `scan_event` records the policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`) and the set it was decided under (`policySetVersion`). The condition is `conditionRule`, a closed JSON format (`AdmissionRule`), not free text. Identity's staff-permission engine was renamed `AuthorisationPolicy` on the same day, so \"access policy\" means this.\n\n**Which of the two policy engines this is** (stated 29 September, build pass). **This one governs who may pass which gate**: admission of a guest, pass holder, accreditation holder or employee at an access point, decided in validation with results a gate acts on (allow, deny, review, requireId, requireBiometric, requireCompanion, requireSupervisor). **identity `AuthorisationPolicy` governs who may do what in the software**: a principal's permissions on operations and screens, decided by identity `evaluateAccess`. An employee's badge opening a staff door is decided here; the same employee approving a refund is decided in identity. Effectiveness is reported per engine: `listDynamicPolicyEffectiveness` here, `listAuthorisationPolicyEffectiveness` in identity.","required":["id","scopePath","name","policyType","conditionRule","result","status","currentVersion"],"properties":{"id":{"type":"string","format":"uuid","description":"The policyId"},"venueId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node; where it applies further is access.policy_scope_assignment"},"name":{"type":"string","maxLength":200},"policyType":{"type":"string","enum":["guestAttribute","accreditation","occupancy","employee","risk","membership","timeEvent"]},"contextType":{"type":"string","enum":["date","day","time","season","event","performance","specialEvent","holiday","operatingCalendar","occupancy","attractionStatus"],"nullable":true,"description":"Context/time/event policies (setContextTimeEvent)"},"identityType":{"type":"string","enum":["guest","member","annualPassHolder","employee","contractor","vendor","performer","media","vip","security","emergencyServices","eventStaff"],"nullable":true,"description":"Identity-based policies (listIdentityMembershipAccreditation)"},"conditionRule":{"$ref":"#/components/schemas/AdmissionRule","description":"The condition, in the closed JSON rule format evaluated the same way online and at the gate (ADR-0068; replaces the free-text `conditionExpression`)."},"result":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"]},"priority":{"type":"integer","nullable":true},"allowedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"deniedZoneIds":{"type":"array","items":{"type":"string","format":"uuid"}},"monitorThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Monitor"},"restrictThresholdPercent":{"type":"integer","minimum":0,"maximum":100,"nullable":true,"description":"Occupancy policies. Percent at which the band becomes Restrict"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"The grant expires automatically at validTo"},"status":{"type":"string","enum":["draft","pendingApproval","active","inactive","expired"],"default":"draft"},"currentVersion":{"type":"integer","minimum":1,"description":"The version in force (access.dynamic_policy_version)"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"AccessPodiumShift": {"type":"object","x-ticvai-persistence":"access.podium_shift","description":"One operator session on a podium or device: who, in what role, where, and login and logout times. Logout is null while the shift is open (declared 29 September, data-model close-out DM1) Written by startPodiumShift and endPodiumShift; an identity sign-out ends the open shift (decided 29 September, writers pass).","required":["id","venueId","operatorPrincipalId","loginAt","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid"},"role":{"type":"string","nullable":true},"podiumId":{"type":"string","format":"uuid","nullable":true},"accessDeviceId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"platform.device","description":"Device used, from the one device register (platform.device, ADR-0067)"},"loginAt":{"type":"string","format":"date-time"},"logoutAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"ltree of the owning scope node (ADR-0005)"}}},
"AccessPoint": {"x-ticvai-persistence":"access.access_point","type":"object","required":["id","code","name","venueId","operatingMode","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"externalCredentialSources":{"allOf":[{"$ref":"#/components/schemas/ExternalCredentialSourceList"}],"description":"BL-108. **A hotel room card admitting a guest to a water park** — externally issued, and the platform validates it without having sold it.\n**The entitlement is created on first use, not on check-in.** A hotel with 400 rooms does not want 400 entitlements a night for guests who never visit.\n"},"scanAnomalyRules":{"allOf":[{"$ref":"#/components/schemas/ScanAnomalyRuleList"}],"description":"BL-104. **Rule-based scan anomalies, separated from the parked model-based engine** — device sharing, simultaneous entries at two gates, an impossible walking time between them.\n**These are deterministic and need no model**, which is why they are here and not in `ai`: two entries eight seconds apart at gates four hundred metres apart is arithmetic.\n"},"operatingMode":{"allOf":[{"$ref":"#/components/schemas/AccessPointOperatingMode"}],"default":"normal","description":"**Set by the podium with `setTurnstileMode`, and it wins** (audit R221). BL-107 and BL-109. **A closed turnstile and one in emergency drop-arm mode look the same in the model and are opposite in meaning.** Closed refuses everybody; drop-arm lets everybody through, and it is the state that exists for an evacuation.\n**`podium` is a supervised validation position** — a member of staff directing a group through a lane, validating by eye against a list. It scans nothing and it is how school parties actually enter.\n**`freeFlow` counts without validating.** Useful at a free event, and a mode that must be visibly distinct from a broken reader.\n"},"vehicleLocationCapture":{"type":"boolean","default":false,"description":"BL-023. **Nothing helped a guest find their vehicle.** Where the access point is a car park entry, the level and zone are captured against the visit so the app can answer it — **the guest who cannot find their car at 11pm is the last impression of the day.**\n"},"mode":{"allOf":[{"$ref":"#/components/schemas/TurnstileMode"}],"nullable":true,"description":"Narrows `operatingMode` only: `freeRotation` or `closed` within `normal` or `podium`, null otherwise and whenever the turnstile validates in its fixed `direction` (audit R221).\n"},"direction":{"allOf":[{"$ref":"#/components/schemas/Direction"}],"description":"**Fixed per access point** (audit R221): set in the back office by `createAccessPoint` and `updateAccessPoint`, never by the podium.\n"},"antiPassbackEnabled":{"type":"boolean"},"requiresExitBeforeReentry":{"type":"boolean","default":false,"description":"Written by `createAccessPoint` and `updateAccessPoint`, and returned so the edit form reads back what it wrote."},"driver":{"type":"string","nullable":true,"description":"Driver identifier for the controller behind this access point, as written by `createAccessPoint` and `updateAccessPoint`. Where the reader speaks OSDP the driver is standards-based; the controller layer above it is vendor-specific.\n"},"geofence":{"allOf":[{"$ref":"#/components/schemas/AccessPointGeofence"}],"nullable":true,"description":"Written by `setAccessPointGeofence`; null until one is set. **One `jsonb` column on the access point row** (`access.access_point.geofence`), read with the point when a handheld validates against it.\n"},"isActive":{"type":"boolean"},"lastHeartbeatAt":{"type":"string","format":"date-time","nullable":true}}},
"AccessPointGeofence": {"type":"object","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"Where a handheld may validate for one access point, and what happens outside it. The body of `setAccessPointGeofence` and the value of `AccessPoint.geofence`.\n","required":["enforcement"],"properties":{"latitude":{"type":"number"},"longitude":{"type":"number"},"radiusMetres":{"type":"integer","minimum":5,"maximum":5000},"enforcement":{"type":"string","enum":["off","warn","deny"],"description":"`off` keeps the fence on record and checks nothing; `warn` lets a validation from outside the fence through with a warning; `deny` refuses it.\n"},"allowProximityBeacon":{"type":"boolean","description":"Accept a BLE proximity assertion in place of GPS. Better indoors."}}},
"AccessPointOperatingMode": {"type":"string","description":"BL-107 and BL-109. **What the gate does, and what the podium sets** (`setTurnstileMode`, decided 28 September, audit R221). `closed` refuses everybody; `dropArm` lets everybody through and exists for an evacuation; `podium` is supervised validation by eye; `freeFlow` counts without validating; `maintenance` takes the lane out of use.\n","enum":["normal","freeFlow","dropArm","closed","podium","maintenance"]},
"AccreditationCredentialVerification": {"type":"object","description":"18.8.3. **What a steward needs to believe the person in front of them**: the face, the name, the category and the zones, and whether any of it is valid now. Returned by `verifyAccreditationCredential`; not stored.\n","required":["outcome"],"properties":{"outcome":{"type":"string","enum":["valid","notYetValid","expired","suspended","revoked","credentialReplaced","credentialLost","credentialInactive"],"description":"`valid` only when the holder is `active`, today is inside the holder's validity, and the credential is `issued` or `active`"},"reason":{"type":"string","nullable":true},"credentialId":{"type":"string","format":"uuid"},"credentialKind":{"type":"string"},"credentialStatus":{"type":"string"},"holderId":{"type":"string","format":"uuid"},"accreditationNumber":{"type":"string"},"fullName":{"type":"string"},"photoAssetId":{"type":"string","format":"uuid","nullable":true},"photoUrl":{"type":"string","nullable":true,"description":"Signed and short-lived, so the scan screen can show the face without a second call"},"organisationName":{"type":"string","nullable":true},"affiliationRole":{"type":"string","nullable":true},"programmeId":{"type":"string","format":"uuid"},"categoryCode":{"type":"string","nullable":true},"categoryName":{"type":"string","nullable":true},"holderStatus":{"type":"string"},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"effectiveZones":{"type":"array","description":"The zones the holder may enter under their profiles and exceptions, today","items":{"type":"object","properties":{"zoneId":{"type":"string","format":"uuid"},"zoneName":{"type":"string"},"allowedNow":{"type":"boolean","description":"Inside the profile schedule (date, day, time, event phase) at this moment"}}}},"escortRequired":{"type":"boolean"},"zoneCheck":{"type":"object","nullable":true,"description":"Present when `zoneId` was given","properties":{"zoneId":{"type":"string","format":"uuid"},"allowed":{"type":"boolean"},"reason":{"type":"string","nullable":true}}},"checkedAt":{"type":"string","format":"date-time"}}},
"BlacklistEntry": {"x-ticvai-persistence":"access.blacklist","type":"object","required":["mediaCode","reason","addedAt","addedByPrincipalId"],"properties":{"mediaCode":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique within the tenant** (decided 28 September, audit R108): one entry per code. `addBlacklistEntry` refuses a second entry with `409 duplicate-code`. **One code space for both lists** (decided 29 September, writers pass): a code on the blacklist cannot also be whitelisted; adding it to the other list is the same `409 duplicate-code`. Move a code between lists by removing and re-adding it."},"reason":{"type":"string"},"addedAt":{"type":"string","format":"date-time"},"addedByPrincipalId":{"type":"string","format":"uuid"},"expiresAt":{"type":"string","format":"date-time","nullable":true},"listType":{"type":"string","enum":["blacklist","whitelist"],"default":"blacklist","description":"A blacklist entry refuses the media; a whitelist entry is an approved exception to a restriction (added 29 September, data-model close-out DM1)."},"disableScope":{"type":"string","enum":["entireCredential","venueAccess","attractionAccess","reEntry","fastPass","specificEntitlement"],"default":"entireCredential","description":"What the entry disables (added 29 September, data-model close-out DM1)."},"distributedTo":{"type":"array","items":{"type":"string","enum":["centralPlatform","venueEdge","onlineGates","offlineRevocationPackage"]},"description":"Where the restriction has been distributed so far, as `listCredentialDisableBlacklist` returns it (added 29 September, data-model close-out DM1)."},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"CreateOrderRequest": {"type":"object","required":["id","venueId","channel","lines","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key: it must equal the `Idempotency-Key` header, and a replay or a mismatch follows `IdempotencyKey` in `shared/common.yaml`. Offline replay through `syncOrders` carries no header, and this id alone deduplicates there.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"#/components/schemas/Channel"},"shiftId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null for an anonymous sale. Identity and entitlement are separate."},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells."},"catalogueBundleVersion":{"type":"string","description":"The bundle the client priced from. Lets the server explain a variance rather than merely report one.\n"},"lines":{"type":"array","minItems":1,"items":{"$ref":"#/components/schemas/CreateOrderLine"}},"recordedAt":{"type":"string","format":"date-time"}}},
"CreatePaymentRequest": {"type":"object","required":["id","orderId","tender","amount","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7 of the payment, and its idempotency key — it must equal the `Idempotency-Key` header."},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"The currency the guest handed over, where it is not the venue's — becomes `Payment.tenderCurrency`. Omit for a payment in the venue's own currency."},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"**What the guest handed over**, in `tenderCurrency` — becomes `Payment.tenderAmount`, one name for one concept (renamed from `tenderedAmount` on 26 September). For cash, change is the difference.\n"},"walletAuthorisationId":{"type":"string","nullable":true,"description":"Cross-cell wallet hold, where the guest's home cell is elsewhere."},"walletHoldId":{"type":"string","format":"uuid","nullable":true,"description":"For a `wallet` tender, the hold `wallet.holdWalletFunds` placed (SD-027). Capture debits it; the order service writes no wallet table."},"returnUrl":{"type":"string","format":"uri","nullable":true,"description":"Where the provider returns the guest after a 3-D Secure challenge or hosted page (SD-034). Required for a card payment from the guest web or app."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal to instruct, for a card payment at a till (ECR flow, SD-034)."},"deviceId":{"type":"string","format":"uuid","nullable":true},"recordedAt":{"type":"string","format":"date-time"}}},
"CrossRegionEntitlement": {"x-ticvai-persistence":"platform.cross_region_entitlement","type":"object","required":["rightId","ticketId","issuingCellName","consumingCellName","validFrom","validTo","entriesAllowed","entriesConsumed","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"rightId":{"type":"string","format":"uuid"},"ticketId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"issuingCellName":{"type":"string"},"consumingCellName":{"type":"string"},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"admissionRulesId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid","nullable":true,"description":"Null where the right is valid at any venue in the consuming cell."},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"entriesConsumed":{"type":"integer"},"status":{"type":"string","enum":["active","exhausted","revoked","expired"]},"lastConsumedAt":{"type":"string","format":"date-time","nullable":true},"lastReconciledAt":{"type":"string","format":"date-time","nullable":true}}},
"DenyReason": {"type":"string","description":"Enumerated so the client can render an appropriate operator prompt. A gate operator facing a queue needs a reason and a next action, not a boolean.\n","enum":["notFound","notYetValid","expired","alreadyUsed","reentryLimitReached","exitRequiredBeforeReentry","wrongAccessPoint","wrongPerformance","outsideAdmissionWindow","entitlementSuspended","blacklisted","capacityReached","waiverRequired","accompanimentRequired","mediaDeactivated","unpaid","delegatedRightExhausted","delegatedRightRevoked","journeyNotCovered"]},
"Direction": {"type":"string","enum":["entry","exit","reentry","crossover"]},
"ExternalCredentialSourceList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.external_credential_sources`). Read with the access point when a credential is presented; a source is never queried on its own.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["hotelRoomCard","corporateBadge","cityPass","transitCard","partnerToken"]},"providerName":{"type":"string"},"endpoint":{"type":"string"},"credentialRef":{"type":"string"},"grantsProductId":{"type":"string","format":"uuid"}}}},
"LoginRequest": {"type":"object","required":["username","credential","workstationId"],"properties":{"username":{"type":"string","maxLength":256},"credential":{"type":"string","description":"Password, PIN, card token or RFID token depending on `method`.\n","maxLength":512,"writeOnly":true},"method":{"type":"string","description":"**`pin` is how a till is actually used.** A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets shortened, shared or written on the drawer. The employee number goes in `username` and the PIN in `credential`, so the shape of the request does not change — only what the operator types.\n\n**A PIN is weaker than a password and the difference is bounded by the device, not by the secret.** `workstationId` is required on every login and is *NOT a permission source*: it says which till, and the till is on a venue network in a staff area. A PIN is a reasonable credential there and nowhere else, which is why this is an enum value and not a policy flag — a surface that wants it has to ask for it by name.\n\nAdded 10 September 2026 for `POS-000 Sign In`.\n","enum":["password","pin","card","rfid","sso"],"default":"password"},"workstationId":{"type":"string","format":"uuid","description":"Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. NOT a permission source.\n"},"deviceFingerprint":{"type":"string","maxLength":256}}},
"LoginResponse": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/TokenPair"},{"type":"object","required":["requiresRoleSelection","requiresMfa"],"properties":{"requiresRoleSelection":{"type":"boolean"},"requiresMfa":{"type":"boolean","description":"True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). The session is not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge."},"hasMfaMethod":{"type":"boolean","description":"Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 (5))."},"mfaMethods":{"type":"array","description":"The principal's active methods, so the client can offer the right one for the `signIn` challenge. Empty when `requiresMfa` is false.","items":{"$ref":"#/components/schemas/MfaMethod"}},"availableRoles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"session":{"$ref":"#/components/schemas/Session"}}}]},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MfaKind": {"type":"string","enum":["totp","smsOtp","emailOtp","biometric","hardwareToken"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"OfflineOrder": {"x-ticvai-persistence":"none — client-side journal, not server storage","allOf":[{"$ref":"#/components/schemas/CreateOrderRequest"},{"type":"object","required":["sequence","payments"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. Processed in this order."},"payments":{"type":"array","items":{"$ref":"#/components/schemas/CreatePaymentRequest"}}}}]},
"OfflinePackage": {"x-ticvai-persistence":"none — generated artefact in object storage","type":"object","required":["etag","generatedAt","validFrom","validTo","accessPointId","entitlements"],"properties":{"etag":{"type":"string"},"generatedAt":{"type":"string","format":"date-time"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"accessPointId":{"type":"string","format":"uuid"},"entitlementsVersion":{"type":"integer","description":"The highest `access.entitlement` change included (SD-052, 29 September). A refresh sends it as `sinceVersion` and receives only what changed after it, so a 60,000-guest venue is not re-sent whole."},"policySetVersion":{"type":"string","description":"**The active admission policy version the package carries** (ADR-0068, 1 October): a fingerprint of the `(id, currentVersion)` of every policy in `dynamicPolicies`, computed the same way by `validateAccess` online. Every scan the gate records carries it (`ScanEvent.policySetVersion`), so a scan decided offline under a set that has since changed is visible at sync rather than assumed equal."},"dynamicPolicies":{"type":"array","description":"The active guest-admission dynamic policies for this access point's zones (SD-052), each at its active version with its `conditionRule` (ADR-0068), so an offline gate applies the same rules as an online one.","items":{"$ref":"#/components/schemas/AccessDynamicPolicy"}},"entitlements":{"type":"array","description":"Read from `access.entitlement` (SD-052). With `sinceVersion`, only the rows changed after it, including ones now void or used, so a device removes them.","items":{"type":"object","required":["ticketId","mediaCodes","validFrom","validTo","entriesAllowed","reentryAllowed"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id`."},"mediaCodes":{"type":"array","items":{"type":"string"},"description":"A ticket may carry several media over its life."},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesAllowed":{"type":"integer","nullable":true},"entriesUsed":{"type":"integer"},"reentryAllowed":{"type":"boolean"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"delegatedRights":{"type":"array","description":"Redemption rights issued by other cells and valid at this access point. Included in the package so a cross-region entitlement still admits when the inter-cell link is down — the same reason locally issued entitlements are included.\n","items":{"type":"object","required":["rightId","ticketId","issuingCellId","validFrom","validTo","entriesAllowed","entriesConsumed"],"properties":{"rightId":{"type":"string"},"ticketId":{"type":"string","format":"uuid","description":"The `Entitlement.id` in the issuing cell."},"issuingCellId":{"type":"string"},"guestLinkId":{"type":"string","nullable":true},"mediaCodes":{"type":"array","items":{"type":"string"}},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time"},"entriesAllowed":{"type":"integer","nullable":true},"entriesConsumed":{"type":"integer"},"admissionRulesId":{"type":"string","format":"uuid"}}}},"blacklist":{"type":"array","items":{"type":"string"},"description":"Media codes to deny outright regardless of entitlement state."},"admissionRules":{"type":"array","items":{"type":"object","required":["id","openMinutesBefore","closeMinutesAfter"],"properties":{"id":{"type":"string","format":"uuid"},"openMinutesBefore":{"type":"integer"},"closeMinutesAfter":{"type":"integer"},"maxDurationMinutes":{"type":"integer","nullable":true},"requiresExitBeforeReentry":{"type":"boolean"}}}},"accreditationCredentials":{"type":"array","description":"Accreditation credentials that admit at this access point, from access.accreditation_credential (29 September, build; BL-181). Only rows that admit are included; a credential dropped from one package to the next no longer admits.","items":{"$ref":"#/components/schemas/AccessAccreditationCredential"}}}},
"OfflineScan": {"x-ticvai-persistence":"none — client-side journal","allOf":[{"$ref":"#/components/schemas/ValidateRequest"},{"type":"object","required":["sequence","localOutcome"],"properties":{"sequence":{"type":"integer","minimum":1,"description":"Monotonic per device. The server processes in this order."},"localOutcome":{"allOf":[{"$ref":"#/components/schemas/ScanOutcome"}],"description":"What the device decided offline. The server is authoritative and may disagree; disagreements are returned for reconciliation, not discarded.\n"},"localDenyReason":{"$ref":"#/components/schemas/DenyReason"},"overriddenByPrincipalId":{"type":"string","format":"uuid","nullable":true},"overrideReason":{"type":"string","nullable":true}}}]},
"OrderSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer"},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"First entry that hit a **transient** failure (SD-028, 29 September): a refusal on the merits no longer stops the batch. Null when every entry was accepted, duplicate or quarantined. The client retries from here and never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string","format":"uuid","description":"The `OfflineOrder.id` this result is about."},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","rejected","blockedByRejection"],"description":"`rejected`: refused on its merits and quarantined in `sync.rejection`; the batch continues. `blockedByRejection`: depends on a rejected entry for the same order (a void, a refund, a later payment) and is quarantined with it (SD-028, 29 September)."},"orderNumber":{"type":"string","nullable":true},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Posted to the variance account. Not surfaced to the cashier."},"varianceExceedsThreshold":{"type":"boolean","description":"True when review is required per the venue's variance threshold."},"rejectionId":{"type":"string","nullable":true,"description":"For a `rejected` or `blockedByRejection` entry, the `sync.rejection` row it was quarantined into (SD-028). The batch carried on past it."},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE"]},
"PermissionSet": {"type":"array","items":{"$ref":"#/components/schemas/Permission"},"uniqueItems":true},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"ScanAnomalyRuleList": {"type":"array","x-ticvai-persistence-kind":"valueObject","x-ticvai-persistence-column":"jsonb","description":"**One `jsonb` column on the access point row** (`access.access_point.scan_anomaly_rules`). Read with the access point at validation, and a rule is never queried on its own.\n","items":{"type":"object","properties":{"rule":{"type":"string","enum":["simultaneousEntry","impossibleTravelTime","rapidReentry","sharedDevice","velocityBreach"]},"action":{"type":"string","enum":["log","flag","requireSupervisor","deny"]},"thresholdSeconds":{"type":"integer","nullable":true}}}},
"ScanEvent": {"x-ticvai-append-only":"recordedAt","x-ticvai-persistence":"access.scan_event","type":"object","required":["id","accessPointId","venueId","outcome","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The scan's client-generated UUIDv7, the key offline replay deduplicates on."},"accessPointId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"ticketId":{"type":"string","format":"uuid","nullable":true,"description":"The `Entitlement.id` scanned; null where the media resolved to nothing."},"mediaCode":{"type":"string","nullable":true},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"direction":{"$ref":"#/components/schemas/Direction"},"operatorPrincipalId":{"type":"string","format":"uuid","nullable":true},"deviceId":{"type":"string","format":"uuid","nullable":true},"overridesScanId":{"type":"string","format":"uuid","nullable":true,"description":"**Set only on an override row**, naming the denied scan it admits against (decided 28 September, audit R228). The denied scan itself is never updated: the denial and the override are two rows, and at most one override row names any scan. Null on every other scan.\n"},"overrideReason":{"type":"string","nullable":true,"description":"The supervisor's justification, on the override row only. The overriding principal is that row's `operatorPrincipalId`."},"dynamicPolicyId":{"type":"string","format":"uuid","nullable":true,"description":"The dynamic access policy (`access.dynamic_policy`) whose result decided this scan; null when no dynamic policy matched and the entitlement alone decided (added 29 September, build pass, 3.3.48). `listDynamicPolicyEffectiveness` counts from it."},"dynamicPolicyVersion":{"type":"integer","minimum":1,"nullable":true,"description":"The version of that policy in force at the scan, so a report spanning a change counts each version apart."},"dynamicPolicyResult":{"type":"string","enum":["allow","deny","review","requireId","requireBiometric","requireCompanion","requireSupervisor"],"nullable":true,"description":"What the policy decided, which for a step-up is not the same as the scan's outcome."},"quantity":{"type":"integer","minimum":1,"default":1,"description":"Admissions this scan counted. More than one only for a group wave (`validateGroupAccess`) or a quantity entitlement consumed in one pass (added 29 September, data-model close-out DM1)."},"localSequence":{"type":"integer","nullable":true,"description":"The device-local sequence number of a scan recorded offline; null for an online scan (added 29 September, data-model close-out DM1)."},"policySetVersion":{"type":"string","nullable":true,"description":"The admission policy set the scan was decided under (`OfflinePackage.policySetVersion`, or the same fingerprint computed online by `validateAccess`), beside the one policy and version that decided it (`dynamicPolicyId`, `dynamicPolicyVersion`). ADR-0068, 1 October."},"packageVersion":{"type":"string","nullable":true,"description":"The offline package (`access.edge_package`) the device validated against; null for an online scan (added 29 September, data-model close-out DM1)."},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while pending. Differs from recordedAt for offline scans."}}},
"ScanOutcome": {"type":"string","enum":["admitted","denied","overridden"]},
"ScanSyncResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["accepted","results"],"properties":{"accepted":{"type":"integer","description":"Entries processed before any stop."},"stoppedAtSequence":{"type":"integer","nullable":true,"description":"Sequence of the first entry that could not be processed. Null when the whole batch succeeded. The client retries from here — never past it.\n"},"results":{"type":"array","items":{"type":"object","required":["id","sequence","status"],"properties":{"id":{"type":"string"},"sequence":{"type":"integer"},"status":{"type":"string","enum":["accepted","duplicate","reconciled","rejected"]},"serverOutcome":{"$ref":"#/components/schemas/ScanOutcome"},"divergence":{"type":"string","nullable":true,"description":"Present when `reconciled` — the device admitted and the server would have denied, or vice versa. Surfaced to the operator, not swallowed.\n"},"error":{"$ref":"../shared/common.yaml#/components/schemas/Problem"}}}}}},
"ScopedPermissions": {"type":"object","description":"Permissions effective at a given scope path, after deny resolution. Clients filter navigation on this and never compute permissions themselves.\n","required":["scopePath","permissions"],"properties":{"scopePath":{"type":"string","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"permissions":{"$ref":"#/components/schemas/PermissionSet"}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions","saleBoardId"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"Shift": {"x-ticvai-persistence":"orders.pos_shift + orders.pos_shift_approval + orders.pos_shift_incident","description":"**`approvals` and `incidents` are child rows** (26 September, pull audit R099): `orders.pos_shift_approval` and `orders.pos_shift_incident`, one row per item, keyed to the shift. Until then the contract carried both and `orders.pos_shift` had nowhere to put either.\n","type":"object","required":["id","workstationId","venueId","scopePath","principalId","status","currency","currencyScale","openedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key."},"workstationId":{"type":"string","format":"uuid"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"principalId":{"type":"string","format":"uuid","description":"Who opened it. Cash reconciles to a person and a drawer."},"principalDisplayName":{"type":"string"},"incidents":{"type":"array","description":"BL-097. **A till has exceptions and there was nowhere to write them** — a no-sale, a drawer opened without a transaction, a manager override, a guest dispute.\n**This is the log a cash-up investigation starts from**, and a shift that balances with four unexplained no-sales is not a shift that balanced.\n","items":{"type":"object","properties":{"kind":{"type":"string","enum":["noSale","drawerOpen","override","voidAfterPayment","guestDispute","tillJam","priceQuery","other"]},"at":{"type":"string","format":"date-time"},"principalId":{"type":"string","format":"uuid"},"note":{"type":"string","nullable":true}}}},"status":{"$ref":"#/components/schemas/ShiftStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"depositBoxCode":{"type":"string","nullable":true},"bagNumber":{"type":"string","nullable":true},"openingFloat":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"salesTotal":{"x-ticvai-column":"gross_sales_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till took in sales, as the guest paid it — tax included."},"refundsTotal":{"x-ticvai-column":"gross_refunded_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"What the till paid back, as the guest was refunded it — tax included."},"liftsTotal":{"x-ticvai-column":"lifted_amount","$ref":"../shared/common.yaml#/components/schemas/Money","description":"Cash taken out mid-shift by lifts and withdrawals. Cash, so neither gross nor net."},"expectedCash":{"x-ticvai-column":"expected_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"26 September, pull audit R207. **The figure the blind count was measured against**, revealed once the count is in — null until then. Until this date only `ShiftCloseResult` carried it, returned once by `closeShift`, so BO-040 could not show the over/short it exists to accept.\n"},"countedCash":{"x-ticvai-column":"counted_cash_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"What the close count found. Null until the shift is counted."},"variance":{"x-ticvai-column":"variance_amount","allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"readOnly":true,"nullable":true,"description":"Counted minus expected, as `ShiftCloseResult.variance`. Negative is short."},"heldLeaseCount":{"type":"integer","description":"Inventory leases currently held by this workstation. Surfaced so an operator closing a shift can see what will be returned.\n"},"openedAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time","description":"When the device recorded the open. `openedAt` is the server's time."},"suspendedAt":{"type":"string","format":"date-time","nullable":true},"suspendReason":{"type":"string","maxLength":200,"nullable":true,"description":"The `reason` given to `suspendShift`. Cleared on resume."},"closedAt":{"type":"string","format":"date-time","nullable":true},"closedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"Who submitted the close count. `reopenShift` refuses an approver who is this principal, and until 26 September there was nothing to compare against (pull audit R099).\n"},"syncedAt":{"type":"string","format":"date-time","nullable":true,"description":"Null while the shift has unsynced operations."},"approvals":{"type":"array","items":{"type":"object","required":["kind","principalId","at"],"properties":{"kind":{"type":"string","enum":["open","close","variance"],"description":"`open` from `approveShiftOpen`, `close` from `approveShiftClose`, `variance` from `acceptShiftVariance`.\n"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"},"reason":{"type":"string"}}}}}},
"ShiftStatus": {"type":"string","enum":["pendingApproval","open","suspended","pendingVariance","pendingClosure","closed","autoClosed"]},
"SsoProtocol": {"type":"string","enum":["oidc","saml2"]},
"SsoProvider": {"x-ticvai-persistence":"identity.sso_provider","type":"object","required":["id","displayName","protocol"],"properties":{"id":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"protocol":{"$ref":"#/components/schemas/SsoProtocol"},"iconAssetRef":{"type":"string","nullable":true},"isEnforced":{"type":"boolean","description":"True disables password login for principals covered by this provider."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."}}},
"SyncRejection": {"x-ticvai-persistence":"sync.rejection","type":"object","required":["id","workstationId","kind","rejectedAt","problem"],"properties":{"id":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["order","payment","refund","void","scan"]},"recordedAt":{"type":"string","format":"date-time"},"rejectedAt":{"type":"string","format":"date-time"},"problem":{"$ref":"../shared/common.yaml#/components/schemas/Problem"},"payload":{"type":"object","additionalProperties":true,"description":"**Deliberately open: the journal entry exactly as the till sent it.** Its shape is the request schema for `kind` — an `OfflineOrder` for `order`, a `CreatePaymentRequest` for `payment` — kept verbatim so the supervisor resolves what was actually recorded, not a re-typed copy.\n"},"resolvedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"resolvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"resolution":{"type":"string","nullable":true,"readOnly":true,"enum":["posted","voided","refunded"],"description":"What `resolveSyncRejection` recorded. Null while the rejection waits."},"resolvedRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The order, void or refund the resolution produced — what stops the entry being posted twice."}}},
"TicketStatus": {"x-ticvai-persistence":"none — computed from entitlement and scans","description":"**A validation result, not a lifecycle**, despite the name. Computed at scan time from the entitlement and its scan history — `isValid`, `entriesUsed`, `isInsideVenue`.\n**The name misled a state model into anchoring on it** (`states/entitlement.yaml`, removed 18 August): six lifecycle states were checked against an object with no values, and `check-states` warned about it for a day before anyone read the schema.\nThe entitlement's lifecycle is `orders.EntitlementStatus`. **This is what a gate learns when it scans**, which is a different question with a similar name.\n","type":"object","required":["ticketId","isValid"],"properties":{"ticketId":{"type":"string","format":"uuid","description":"Stable for the life of the ticket, independent of the media carrying it."},"mediaCode":{"type":"string","nullable":true},"productName":{"type":"string"},"holderName":{"type":"string","nullable":true,"description":"Present only where the entitlement is name-bound. Identity and entitlement are separate concerns; most entitlements carry no holder.\n"},"isValid":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true},"performanceId":{"type":"string","format":"uuid","nullable":true},"entriesUsed":{"type":"integer"},"entriesAllowed":{"type":"integer","nullable":true,"description":"Null means unlimited."},"reentryAllowed":{"type":"boolean"},"isInsideVenue":{"type":"boolean","description":"Derived from the last scan. Drives anti-passback evaluation."},"issuingCellId":{"type":"string","nullable":true,"description":"Present when this entitlement was issued in a different cell and is being redeemed here as a delegated right (ADR-0010). Null for locally issued tickets.\n"},"guestLinkId":{"type":"string","nullable":true,"description":"Pseudonymous cross-region guest reference. Present only on delegated rights. Carries no personal data.\n"},"admissionRulesId":{"type":"string","format":"uuid"},"denyReason":{"$ref":"#/components/schemas/DenyReason"}}},
"TokenPair": {"x-ticvai-persistence":"none — transient","type":"object","required":["accessToken","refreshToken","expiresIn"],"properties":{"accessToken":{"type":"string","description":"JWT carrying `sid`, validated per request against the session registry."},"refreshToken":{"type":"string"},"expiresIn":{"type":"integer","description":"Seconds"}}},
"TurnstileMode": {"type":"string","description":"**Reduced to two values — decided 28 September, audit R221.** Entry, exit, re-entry and crossover were the access point's `Direction` under another name, and two fields that could disagree left the gate to guess. Direction is fixed per access point; within `normal` or `podium` operation the turnstile may only be let spin free or held closed.\n","enum":["freeRotation","closed"]},
"ValidateRequest": {"type":"object","required":["id","mediaCode","mediaKind","direction","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"Client-generated UUIDv7. Also the idempotency key and dedupe key."},"mediaCode":{"type":"string","maxLength":256,"description":"What was read from the media. NOT the ticket id — media can be re-linked over a ticket's life.\n"},"mediaKind":{"$ref":"#/components/schemas/MediaKind"},"direction":{"$ref":"#/components/schemas/Direction"},"groupSize":{"type":"integer","minimum":1,"description":"For group media admitting several holders on one read."},"proximityToken":{"type":"string","description":"BLE proximity assertion where the venue requires the operator to be physically at the gate. Absent where not configured.\n"},"recordedAt":{"type":"string","format":"date-time","description":"Device time of the read. Authoritative for ordering, not for validity."}}},
"ValidationResult": {"x-ticvai-persistence":"none — computed, persisted as scan_event","type":"object","required":["scanId","outcome","accessPointId","recordedAt"],"properties":{"scanId":{"type":"string","format":"uuid"},"outcome":{"$ref":"#/components/schemas/ScanOutcome"},"denyReason":{"$ref":"#/components/schemas/DenyReason"},"denyDetail":{"type":"string","description":"Human-readable, localised. For operator display, never for logic."},"accessPointId":{"type":"string","format":"uuid"},"ticket":{"$ref":"#/components/schemas/TicketStatus"},"admittedCount":{"type":"integer","description":"Holders admitted on this read. Differs from groupSize on partial admission."},"recordedAt":{"type":"string","format":"date-time"},"serverEvaluatedAt":{"type":"string","format":"date-time"},"advisory":{"type":"object","nullable":true,"description":"BL-179, CF-130. **What a device observed, for the steward, never for the gate.** Present only where an access point's device reports the matching `DeviceCapability` and the venue has turned the corresponding setting on.\n**Never persisted.** This schema is computed and stored as `access.scan_event`, and the advisory is deliberately not part of what is stored: an inferred classification kept against a guest is sensitive personal data with no consent behind it. **A guest agreed to be admitted, not to be classified** — Face Pass and Face Tag carry `consent_purpose_id` and `consent_given_at` because somebody enrolled, and nobody enrols in being looked at by a turnstile. `scan_event` records that an override happened and never what the device thought, which keeps `overrideRateAlertThreshold` working without building a register nobody agreed to.\n**It cannot reach `outcome` or `denyReason`.** Those are decisive and `entitlementGated` is `true` and read-only: the gate admits on the entitlement, and everything here sits on top of that without replacing any of it.\n","properties":{"genderClassification":{"type":"string","enum":["women","men","undetermined"],"description":"**`undetermined` is a real answer and the most common one to design for.** A classifier that never returns it is one that has been tuned to look confident.\n"},"confidence":{"type":"number","minimum":0,"maximum":1,"description":"**Required reading for the steward, not decoration.** An advisory with no confidence is read as a fact, and `overrideRateAlertThreshold` exists to catch exactly the failure that produces — *an override rate near zero means the steward has stopped deciding.* That number only means anything if the steward could see how sure the device was.\n"},"reportedByDeviceId":{"type":"string","format":"uuid","description":"**Which device said it.** A classifier that degrades is one camera, not a venue, and an advisory nobody can trace to hardware cannot be investigated or switched off alone.\n"}}}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
