# P09-access-identity-01 — P09 · Access & Identity

**3 screens · 18 operations · 17 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `ROLE_MANAGE, SESSION_FORCE_LOGOUT, USER_MANAGE`. A control nobody can use must say so,
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
| `ADM-001` | Platform Login / MFA | B–D | 21 | 52 | 8 | 6 | 0 | 0 | — | notStarted (generated) |
| `ADM-020` | Platform User Directory | B–D | 12 | 18 | 6 | 1 | 0 | 0 | — | notStarted (generated) |
| `ADM-021` | Platform Role Management | B–D | 3 | 18 | 6 | 0 | 1 | 5 | — | notStarted (generated) |

## Thin screens in this batch

**ADM-021 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-001` Platform Login / MFA

**Get someone into the app, fast, on a device that may be shared.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Access & Identity · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `SESSION_FORCE_LOGOUT` (1 operate); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listActiveSessions` reads the population and `getCurrentSession` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `challengeId` (navigation), `methodId` (navigation) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/platform-login-mfa` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue id | picker: choose a venue (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?venueId=` to `listActiveSessions`. | `listActiveSessions` ?venueId |
| Principal id | picker: choose a principal (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?principalId=` to `listActiveSessions`. | `listActiveSessions` ?principalId |
| Workstation id | picker: choose a workstation (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | Sends `?workstationId=` to `listActiveSessions`. | `listActiveSessions` ?workstationId |
| Authentication code | text field | — | — | — | — | Shown only in the mfaRequired state, after `login`, for the authenticator-app code or the emailed code (decided 28 September, audit R135, R126 (5)). | — |

**Form: Enrol MFA method** (modal, opened by *Enrol MFA method*; *Enrol* calls `enrolMfaMethod`, *Cancel* sends nothing)

**Collects what `enrolMfaMethod` sends before it is called.** Required: `kind` — the authenticator app (`totp`) or email (`emailOtp`) only (decided 28 September, audit R126 (5)). Optional: `target` (the email address for `emailOtp`). The response carries the secret or QR for the app and the recovery codes, shown once. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Totp · SMS OTP · Email OTP · Biometric · Hardware token | — | — | `enrolMfaMethod` body |
| Target `target` | text field | optional | — | — | — | Phone or email for OTP methods. | `enrolMfaMethod` body |

Errors to draw in the form: 403 A guest caller while no venue of the tenant has guest two-step verification on (rev 3 GAP-B1, per venue).; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest the same (rev 3 GAP-B1).

**Form: Confirm enrolment** (modal, opened by *Confirm enrolment*; *Confirm enrolment* calls `verifyMfaEnrolment`, *Cancel* sends nothing)

**Collects what `verifyMfaEnrolment` sends before it is called.** Required: `code`, the first code from the new method. The method is active only after this. Dismissing sends nothing; the method stays pending.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `verifyMfaEnrolment` body |

**Form: Remove MFA method** (confirmDialog, opened by *Remove MFA method*; *Remove* calls `removeMfaMethod`, *Cancel* sends nothing)

**Names the method being removed and what remains.** Removing the last active method is refused 409 while the principal holds a permission that requires MFA (decided 28 September, audit R135); the dialog says so before it is sent rather than after.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 409 Last remaining method of a principal who holds a permission that requires MFA (audit R135)

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

**Sent by *Force logout*** (`forceLogout`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `forceLogout` body |

**Sent by *Revoke all sessions*** (`revokeAllSessions`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `revokeAllSessions` body |
| Step up token `stepUpToken` | text field | required | — | — | — | — | `revokeAllSessions` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | — | `revokeAllSessions` body |
| Exclude self `excludeSelf` | toggle | optional | on | — | — | — | `revokeAllSessions` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every active session** (data table, from `listActiveSessions`)

| Shows | Format | Notes |
|---|---|---|
| Session | text | — |
| Principal | the name it points at, never the id | — |
| Principal name | text | — |
| Role | the name it points at, never the id | — |
| Role name | text | — |
| Workstation | the name it points at, never the id | — |
| Workstation name | text | — |
| Venue | the name it points at, never the id | — |
| Ip address | text | — |
| Device info | text | — |
| Has open shift | yes / no (icon or chip) | Revoking this session leaves cash unreconciled. |
| MFA satisfied | yes / no (icon or chip) | — |

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

**The selected active session** (detail panel, from `listActiveSessions`)

| Shows | Format | Notes |
|---|---|---|
| Status | chip: Active, Signed out, Terminated, Expired | A registry that only holds live sessions cannot answer why one ended. Kept on the record so a supervisor asking *what happened to till 4* … |
| Session | text | — |
| Principal | the name it points at, never the id | — |
| Principal name | text | — |
| Role | the name it points at, never the id | — |
| Role name | text | — |
| Workstation | the name it points at, never the id | — |
| Workstation name | text | — |
| Venue | the name it points at, never the id | — |
| Ip address | text | — |
| Device info | text | — |
| Has open shift | yes / no (icon or chip) | Revoking this session leaves cash unreconciled. |
| MFA satisfied | yes / no (icon or chip) | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |

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
| Enrol MFA method (secondary button) | `enrolMfaMethod` POST `/auth/mfa/methods` | inline | MfaEnrolment | 403 A guest caller while no venue of the tenant has guest two-step verification on (rev 3 GAP-B1, per venue).; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest … | opens modal first |
| Confirm enrolment (secondary button) | `verifyMfaEnrolment` POST `/auth/mfa/methods/{methodId}` | inline | MfaMethod | — | opens modal first |
| Remove MFA method (destructive button) | `removeMfaMethod` DELETE `/auth/mfa/methods/{methodId}` | — | — | 409 Last remaining method of a principal who holds a permission that requires MFA (audit R135) | opens confirmDialog first |
| Force logout (destructive button) | `forceLogout` POST `/auth/sessions/{sessionId}/force-logout` | inline | — | 403 Authenticated but not permitted at the requested scope | — |
| Revoke all sessions (destructive button) | `revokeAllSessions` POST `/auth/sessions/revoke-all` | inline | inline | 403 Step-up token missing, expired or issued for a different action | — |

**Data it reads**: `getCurrentSession` (onLoad, Current session and effective permissions); `listActiveSessions` (onLoad, List active sessions); `listMfaMethods` (onLoad, Enrolled MFA methods); `listSsoProviders` (onLoad, Identity providers configured for this tenant)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-004` Platform Audit Log: *Platform Audit Log*
- → `PTR-001` Partner Login / MFA: *A partner user signs in through the same door*; carries `challengeId`

**What opens over it**

- confirmDialog *Force logout*: **Names what `forceLogout` changes and what it leaves alone**, in the consequence rather than the verb. A platform login mfa this affects should be identified in the dialog, not just counted. **Collects what `forceLogout` sends before it is called.** Required: `reason`.
- confirmDialog *Revoke all sessions*: **Names what `revokeAllSessions` changes and what it leaves alone**, in the consequence rather than the verb. A platform login mfa this affects should be identified in the dialog, not just counted. **Collects what `revokeAllSessions` sends before it is called.** Required: `reason`, `stepUpToken`. …

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform login mfa list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform login mfa untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform login mfa yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on venueId, principalId, workstationId and the platform login mfa are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `SESSION_FORCE_LOGOUT`, which `listActiveSessions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| MFA required (`?state=mfaRequired`) | **Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any platform-staff permission, or one the tenant added), so after `login` the screen calls `createMfaChallenge` and asks for the authenticator code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says so. A principal with no enrolled method is sent to enrol first … |
| MFA enrolment required (`?state=mfaEnrolmentRequired`) | **First sign-in, no method yet.** A platform operator always requires MFA (every `PLATFORM_*` permission is in the floor), so one with no enrolled method cannot finish signing in: the screen enrols the authenticator app (`enrolMfaMethod`, email as the fallback), confirms it with the first code (`verifyMfaEnrolment`), then continues to the mfaRequired step (decided 28 September, audit R135, R126 (5)). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused.; 409 Last remaining method of a principal who holds a permission that requires MFA (audit R135); 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest the same (rev 3 GAP-B1). |

#### Permissions

- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest
- `enrolMfaMethod` → no permission · staff, partner, guest
- `verifyMfaEnrolment` → no permission · staff, partner, guest
- `removeMfaMethod` → no permission · staff, partner, guest
- `login` → no permission · anonymous, partner
- `forceLogout` → `SESSION_FORCE_LOGOUT` (operate) · staff, partner
- `getCurrentSession` → no permission · staff, partner
- `listActiveSessions` → `SESSION_FORCE_LOGOUT` (operate) · staff, partner
- `listMfaMethods` → no permission · staff, partner, guest
- `listSsoProviders` → no permission · anonymous, partner
- `revokeAllSessions` → `SESSION_FORCE_LOGOUT` (operate) · staff, partner

**A refused user sees:** Shown when the caller lacks `SESSION_FORCE_LOGOUT`, which `listActiveSessions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.16 | The system shall support MFA using Email OTP, SMS OTP, Authenticator Apps, and future supported authentication mechanisms. | F&B POS | CONTRACTED | `enrolMfaMethod` |
| 5.1.5 | The system should have the option to be used by several waiters at the same time. | F&B & Guest Management | CONTRACTED | `login` |
| 5.8.2 | The system should only allow one session per user. | F&B & Guest Management | CONTRACTED | `login` |
| 3.3.28 | Authorization Caching - System shall support caching of authorization decisions. | Admission and Access | CONTRACTED | `getCurrentSession` |
| 7.1.50 | Cache authorization decisions securely to improve performance while ensuring policy changes invalidate outdated cache entries. | F&B POS | CONTRACTED | `getCurrentSession` |
| 7.1.20 | The system shall allow administrators to view active sessions, force logout users, revoke sessions, configure inactivity timeouts, and control concurrent session limits. | F&B POS | CONTRACTED | `listActiveSessions` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-001` · status **notStarted** · provenance generated
- Flow F104 *A platform operator signs in under MFA*, step 1: The operator signs in with username and password. → **Signed in, not yet through.** Every platform operator holds a `PLATFORM_*` permission, and MFA is required by permission (decided 28 September, audit R135), so the session is not usable yet.
- Flow F104 *A platform operator signs in under MFA*, step 2: The second factor is asked for and given. → **The authenticator code, or an emailed code as the fallback** (audit R126 (5)). `verifyMfaChallenge` completes the sign-in; five wrong codes lock step-up for the policy's lockout minutes (audit R126 …
- Flow F104 *A platform operator signs in under MFA*, step 3: The session opens with its cross-tenant reach. → The operator sees their session and every other active one they may end.
- Flow F109 *A tenant gets its first administrator*, step 1: The platform operator signs in → A session scoped to the platform, not to any tenant
- Flow F104 branch at step 2 (high): when The operator has no MFA method enrolled yet., **Enrolled before they get in.** A platform operator cannot finish signing in without a method, so ADM-001 enrols an authenticator app (or email) with `enrolMfaMethod` and `verifyMfaEnrolment` first …
- Flow F104 branch at step 2 (medium): when Five wrong codes., **Step-up locks for the policy's lockout minutes, never permanently** (audit R126 (6)). The screen says so and when it lifts; a permanent lock is a denial of service anybody can run.
- Flow F104 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.
- Flow F109 branch at step 1 (abandonsFlow): when The seeded platform account cannot sign in, **There is no second door.** MFA unreachable or the identity provider down leaves nobody able to issue an identity to anybody. This is the single point at which the whole permission tree is …

#### Acceptance for the design

- [ ] Every input above is drawn (21), with its required mark, default, format and its error state (400, 403, 409, 422).
- [ ] Every output is drawn (52 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-001?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, mfaRequired, mfaEnrolmentRequired, offline.
- [ ] Every action is wired with its success and its failure: Login, Verify, Email me a code instead, Enrol MFA method, Confirm enrolment, Remove MFA method, Force logout, Revoke all sessions.
- [ ] Every transition is wired: `ADM-002`, `ADM-004`, `PTR-001`.
- [ ] Every gated control is gated: `SESSION_FORCE_LOGOUT`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-020` Platform User Directory

**Find the right one quickly, and act on it without opening it.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Access & Identity · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `USER_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPrincipals` reads the population and `getPrincipal` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `principalId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/platform-user-directory` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listPrincipals`. | `listPrincipals` ?scopePath |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listPrincipals`. | `listPrincipals` ?isActive |

**Form: Create principal** (modal, opened by *Create principal*; *Create principal* calls `createPrincipal`, *Cancel* sends nothing)

**Collects what `createPrincipal` sends before it is called.** Required: `username`, `displayName`. Optional: `initialCredential`, `mustChangeCredential`, `validTo`, `roleIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Username `username` | text area | required | — | max length 256 | — | — | `createPrincipal` body |
| Display name `displayName` | text field | required | — | max length 200 | — | — | `createPrincipal` body |
| Initial credential `initialCredential` | text area | optional | — | max length 512 | — | — | `createPrincipal` body |
| Must change credential `mustChangeCredential` | toggle | optional | on | — | — | — | `createPrincipal` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `createPrincipal` body |
| Roles `roleIds` | multi-picker: choose roles | optional | — | — | — | — | `createPrincipal` body |

Errors to draw in the form: 400 Validation failed; 409 Username already in use within this cell

**Form: Save principal** (modal, opened by *Save principal*; *Save principal* calls `updatePrincipal`, *Cancel* sends nothing)

**Collects what `updatePrincipal` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `isActive`, `validTo`, `primaryRoleId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Display name `displayName` | text field | optional | — | max length 200 | — | — | `updatePrincipal` body |
| Is active `isActive` | toggle | optional | — | — | — | — | `updatePrincipal` body |
| Valid to `validTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `updatePrincipal` body |
| Primary role `primaryRoleId` | picker: choose a primary role | optional | — | — | shows names, sends the id | — | `updatePrincipal` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every principal** (data table, from `listPrincipals`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Primary role | the name it points at, never the id | Determines the landing screen when the principal holds several roles and picks one at login. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**The selected principal** (detail panel, from `getPrincipal`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Primary role | the name it points at, never the id | Determines the landing screen when the principal holds several roles and picks one at login. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create principal (primary button) | `createPrincipal` POST `/principals` | CreatePrincipalRequest | Principal | 400 Validation failed; 409 Username already in use within this cell | opens modal first |
| Save principal (secondary button) | `updatePrincipal` PATCH `/principals/{principalId}` | inline | Principal | — | opens modal first |

**Data it reads**: `listPrincipals` (onLoad, from page inventory); `getPrincipal` (onLoad, Read a principal)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform user list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform user untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform user yet. Offers Create principal (`createPrincipal`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on scopePath, isActive and the platform user are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Username already in use within this cell |

#### Permissions

- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner
- `createPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `getPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `updatePrincipal` → `USER_MANAGE` (configure) · staff, partner

**A refused user sees:** Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.6 | The system should be able to create a new Back Office/POS user and Logon to back office/POS using new user. | F&B POS | CONTRACTED | `createPrincipal` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-020` · status **notStarted** · provenance generated
- Flow F109 *A tenant gets its first administrator*, step 5: Creates the first principal and grants it the role → One identity inside the tenant that can now create every other one
- Flow F16 *A venue opens for the first time*, step 7: Creates the first venue manager → Who then does everything else
- Flow F109 branch at step 5 (recoverable): when The principal is created but the role was never attached, An identity that can sign in and do nothing. It reads as success on this screen and fails on the tenant's first real action, which is the worst place to discover it.
- Flow F16 branch at step 7 (requiresStaff): when The first manager cannot sign in, SSO not configured, or the identity provider unreachable. There is no second path in — **this is why a break-glass local account exists**.

#### Acceptance for the design

- [ ] Every input above is drawn (12), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create principal, Save principal.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-021` Platform Role Management

**Find platform role management for this venue.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Access & Identity · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `ROLE_MANAGE` (1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRoles` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/general/platform-role-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement.

#### Inputs: what the user enters or picks

**Form: Create role** (modal, opened by *Create role*; *Create role* calls `createRole`, *Cancel* sends nothing)

**Collects what `createRole` sends before it is called.** Required: `code`, `name`. Optional: `description`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[A-Za-z0-9_-]+$` | — | Unique within the tenant, compared case-insensitively (decided 28 September, audit R108). | `createRole` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createRole` body |
| Description `description` | text area | optional | — | max length 500 | — | — | `createRole` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …

#### Outputs: what the screen shows and produces

**Shown**

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

**The selected role** (detail panel, from `listRoles`)

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

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Create role (primary button) | `createRole` POST `/roles` | inline | Role | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … | opens modal first |

**Data it reads**: `listRoles` (onLoad, from page inventory)

**Where the user goes next**

- → `ADM-001` Platform Login / MFA: *Platform Login / MFA*
- → `ADM-002` Platform Dashboard: *Platform Dashboard*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The platform role list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the platform role untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No platform role yet. Offers Create role (`createRole`). |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listRoles` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `ROLE_MANAGE`, which `listRoles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … |

#### Permissions

- `listRoles` → `ROLE_MANAGE` (configure) · staff
- `createRole` → `ROLE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `ROLE_MANAGE`, which `listRoles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Allam: add a "roles comparison" view letting an admin compare two roles side by side (e.g. confirm a cashier role lacks the refund/void permissions a supervisor role has). *(agreed · MoM 7 Aug 2026, 4. Roles & User Management · DI-153)*

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S2** Role-based access control: role and permission matrix *(Chinmay Parab · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'permission matrix')*
- **A48** Update Employee App wireframe: remove the manual role-selection screen — role and home dashboard should be determined automatically from backend RBAC configuration immediately after login *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'rbac')*
- **A63** Design RBAC enhancements: a roles-comparison view for side-by-side permission auditing, and the POS session model (one user per workstation session, fully role-driven access with automatic front-end/"sales board" … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 12 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A97** Document the RBAC role-permission matrix (edit/view · view-only · hidden, per role per module, sub-permissions, default templates) *(Chinmay Parab · High · Ongoing → 30 Sep: Closed, Rolled into S2 · 20 Aug 2026 · workshop tracker · keyword 'rbac')*
- **A130** Enforce venue-level admission capacity as superseding event capacity, with a blocking validation and an RBAC-gated override *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S2 · 25 Aug 2026 · workshop tracker · keyword 'rbac')*

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-021` · status **notStarted** · provenance generated
- Flow F109 *A tenant gets its first administrator*, step 3: Defines the role the first administrator will hold → A role carrying the permissions a tenant administrator needs
- Flow F109 branch at step 3 (expected): when No role exists yet for this tenant, ADM-021 shows `emptyFirstRun` rather than `emptyNoResults`. **The distinction matters here more than anywhere** — an empty role list on a brand-new tenant is the expected state, and an empty one on …
- Flow F109 branch at step 3 (requiresStaff): when The operator holds no key that satisfies ROLE_MANAGE, The screen shows `emptyNoAccess`. **On the package as written this is every operator**, because no role grants the key. Until the two permission vocabularies are joined, this branch is the happy path.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Create role.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `ROLE_MANAGE`.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createPrincipal": {"method":"POST","path":"/principals","contract":"identity","summary":"Create a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePrincipalRequest","responds":"Principal"},
"createRole": {"method":"POST","path":"/roles","contract":"identity","summary":"Create a role","permission":"ROLE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Role"},
"enrolMfaMethod": {"method":"POST","path":"/auth/mfa/methods","contract":"identity","summary":"Enrol an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaEnrolment"},
"forceLogout": {"method":"POST","path":"/auth/sessions/{sessionId}/force-logout","contract":"identity","summary":"Supervisor termination of an abandoned session","permission":"SESSION_FORCE_LOGOUT","offlineCapable":false,"conflictPolicy":"append","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"sessionId","in":"path","required":true}],"requestBody":null,"responds":null},
"getCurrentSession": {"method":"GET","path":"/auth/session","contract":"identity","summary":"Current session and effective permissions","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Session"},
"getPrincipal": {"method":"GET","path":"/principals/{principalId}","contract":"identity","summary":"Read a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Principal"},
"listActiveSessions": {"method":"GET","path":"/auth/sessions","contract":"identity","summary":"List active sessions","permission":"SESSION_FORCE_LOGOUT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"principalId","in":"query","required":null},{"name":"workstationId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMfaMethods": {"method":"GET","path":"/auth/mfa/methods","contract":"identity","summary":"Enrolled MFA methods","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MfaMethod"},
"listPrincipals": {"method":"GET","path":"/principals","contract":"identity","summary":"List principals","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRoles": {"method":"GET","path":"/roles","contract":"identity","summary":"List roles","permission":"ROLE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSsoProviders": {"method":"GET","path":"/auth/sso/providers","contract":"identity","summary":"Identity providers configured for this tenant","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SsoProvider"},
"login": {"method":"POST","path":"/auth/login","contract":"identity","summary":"Authenticate and open a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LoginRequest","responds":"LoginResponse"},
"removeMfaMethod": {"method":"DELETE","path":"/auth/mfa/methods/{methodId}","contract":"identity","summary":"Remove an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"revokeAllSessions": {"method":"POST","path":"/auth/sessions/revoke-all","contract":"identity","summary":"Revoke every session in scope","permission":"SESSION_FORCE_LOGOUT","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updatePrincipal": {"method":"PATCH","path":"/principals/{principalId}","contract":"identity","summary":"Update or deactivate a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Principal"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"verifyMfaEnrolment": {"method":"POST","path":"/auth/mfa/methods/{methodId}","contract":"identity","summary":"Complete enrolment","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaMethod"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"ActiveSession": {"x-ticvai-persistence":"none — Redis session registry","type":"object","required":["sessionId","principalId","status","startedAt","lastSeenAt"],"properties":{"status":{"allOf":[{"$ref":"#/components/schemas/SessionStatus"}],"description":"**A registry that only holds live sessions cannot answer why one ended.** Kept on the record so a supervisor asking *what happened to till 4* gets `terminated` or `expired` rather than an absence.\n"},"sessionId":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"principalName":{"type":"string"},"roleId":{"type":"string","format":"uuid","nullable":true},"roleName":{"type":"string","nullable":true},"workstationId":{"type":"string","format":"uuid","nullable":true},"workstationName":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"ipAddress":{"type":"string","nullable":true},"deviceInfo":{"type":"string","nullable":true},"hasOpenShift":{"type":"boolean","description":"Revoking this session leaves cash unreconciled."},"mfaSatisfied":{"type":"boolean"},"startedAt":{"type":"string","format":"date-time"},"lastSeenAt":{"type":"string","format":"date-time"}}},
"CreatePrincipalRequest": {"type":"object","required":["username","displayName"],"properties":{"username":{"type":"string","maxLength":256},"displayName":{"type":"string","maxLength":200},"initialCredential":{"type":"string","maxLength":512,"writeOnly":true},"mustChangeCredential":{"type":"boolean","default":true},"validTo":{"type":"string","format":"date-time"},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"LoginRequest": {"type":"object","required":["username","credential","workstationId"],"properties":{"username":{"type":"string","maxLength":256},"credential":{"type":"string","description":"Password, PIN, card token or RFID token depending on `method`.\n","maxLength":512,"writeOnly":true},"method":{"type":"string","description":"**`pin` is how a till is actually used.** A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets shortened, shared or written on the drawer. The employee number goes in `username` and the PIN in `credential`, so the shape of the request does not change — only what the operator types.\n\n**A PIN is weaker than a password and the difference is bounded by the device, not by the secret.** `workstationId` is required on every login and is *NOT a permission source*: it says which till, and the till is on a venue network in a staff area. A PIN is a reasonable credential there and nowhere else, which is why this is an enum value and not a policy flag — a surface that wants it has to ask for it by name.\n\nAdded 10 September 2026 for `POS-000 Sign In`.\n","enum":["password","pin","card","rfid","sso"],"default":"password"},"workstationId":{"type":"string","format":"uuid","description":"Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. NOT a permission source.\n"},"deviceFingerprint":{"type":"string","maxLength":256}}},
"LoginResponse": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/TokenPair"},{"type":"object","required":["requiresRoleSelection","requiresMfa"],"properties":{"requiresRoleSelection":{"type":"boolean"},"requiresMfa":{"type":"boolean","description":"True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). The session is not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge."},"hasMfaMethod":{"type":"boolean","description":"Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 (5))."},"mfaMethods":{"type":"array","description":"The principal's active methods, so the client can offer the right one for the `signIn` challenge. Empty when `requiresMfa` is false.","items":{"$ref":"#/components/schemas/MfaMethod"}},"availableRoles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"session":{"$ref":"#/components/schemas/Session"}}}]},
"MfaEnrolment": {"x-ticvai-persistence":"none — transient","type":"object","required":["methodId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"methodId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"secret":{"type":"string","nullable":true,"description":"TOTP shared secret. Returned once, at enrolment, and never again."},"qrCodeUri":{"type":"string","nullable":true},"recoveryCodes":{"type":"array","description":"Returned once, in this enrolment response (`enrolMfaMethod` writes them, hashed, to `identity.mfa_recovery_code`). Not retrievable afterwards — `verifyMfaEnrolment` does not return them.\n","items":{"type":"string"}},"expiresAt":{"type":"string","format":"date-time"}}},
"MfaKind": {"type":"string","enum":["totp","smsOtp","emailOtp","biometric","hardwareToken"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"Role": {"x-ticvai-persistence":"identity.role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique within the tenant** (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. Unique per tenant, not per venue, because a grant names a role anywhere in the tree; `createRole` refuses a duplicate with `409 duplicate-code`.\n"},"name":{"type":"string"},"description":{"type":"string"},"permissions":{"type":"array","description":"**A role that grants no permissions is not a role.** `Role` carried a code, a name and two counts until 18 August, and `identity.role_permission` derived from it with exactly one column — `role_id`. **A join table that joins to nothing**, found by Hrushikant in review and missed by the schema audit that ran the same day.\n**The audit asked whether every table had columns, a relationship and an owner, and this table had all three.** What it did not ask is whether a table with one column can do the job its name claims.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"inheritsFromRoleId":{"type":"string","format":"uuid","nullable":true,"description":"**Role composition, one level deep and no deeper.** A supervisor role that is a cashier plus three permissions is how venues actually describe them.\n**Cycles are refused and depth is capped at one**, because a permission set nobody can read off the screen is a permission set nobody audits.\n"},"isSystem":{"type":"boolean","default":false,"description":"**Seeded roles ship and are editable; deleting one is refused.** A venue that removes `cashier` and rebuilds it has two roles with one name in the audit log.\n**The seeded system roles are Cashier, Supervisor, Venue Manager, Finance and Tenant Admin** (proposed in `docs/active/seed-data-proposal.md` section 2, client to correct; audit R229).\n"},"principalCount":{"type":"integer"},"grantCount":{"type":"integer"}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions","saleBoardId"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"SessionStatus": {"type":"string","description":"**The life of one signed-in session, which is not the life of a shift.** A shift holds the float and survives a break; a session holds the person and does not. `ShiftStatus.suspended` is where a break lives — *break cover; float intact, workstation released* — and the release of the workstation is exactly why the session ends rather than pausing: the next person opens their own.\n**One principal, one active session per workstation.** Enforced by the `ActiveSession` registry rather than by a state, because it is a fact about the set of sessions and not about any one of them.\n","enum":["active","signedOut","terminated","expired"]},
"SsoProtocol": {"type":"string","enum":["oidc","saml2"]},
"SsoProvider": {"x-ticvai-persistence":"identity.sso_provider","type":"object","required":["id","displayName","protocol"],"properties":{"id":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"protocol":{"$ref":"#/components/schemas/SsoProtocol"},"iconAssetRef":{"type":"string","nullable":true},"isEnforced":{"type":"boolean","description":"True disables password login for principals covered by this provider."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."}}},
"TokenPair": {"x-ticvai-persistence":"none — transient","type":"object","required":["accessToken","refreshToken","expiresIn"],"properties":{"accessToken":{"type":"string","description":"JWT carrying `sid`, validated per request against the session registry."},"refreshToken":{"type":"string"},"expiresIn":{"type":"integer","description":"Seconds"}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
