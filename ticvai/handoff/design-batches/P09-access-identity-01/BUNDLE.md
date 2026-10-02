# P09-access-identity-01 — P09 · Access & Identity

**4 screens · 24 operations · 24 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `PLATFORM_TENANT_ACCESS, PLATFORM_TENANT_VIEW, ROLE_MANAGE, USER_MANAGE`. A control nobody can use must say so,
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
| `ADM-001` | Platform Login / MFA | B–D | 16 | 51 | 10 | 6 | 0 | 0 | — | notStarted (generated) |
| `ADM-020` | Platform User Directory | B–D | 18 | 22 | 7 | 2 | 0 | 0 | — | notStarted (generated) |
| `ADM-021` | Platform Role Management | B–D | 11 | 22 | 7 | 1 | 1 | 5 | — | notStarted (generated) |
| `ADM-699` | My Account & Security | B–D | 10 | 16 | 7 | 1 | 0 | 0 | — | notStarted (generated) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `ADM-001` Platform Login / MFA

**Get a TICVAI platform operator into the TICVAI Console: username and password (or TICVAI's own SSO), then always the authentication code, then the Platform Dashboard.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Access & Identity · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai; in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | form (compact density): A sign-in: two fields, the organisation's SSO where configured, and the second-factor and role steps in place - a form, not a list to browse. |
| Offline | Not available, and the offline banner says why: signing in needs a connection. |
| Opens with | `challengeId` (navigation), `providerId` (deepLink), `methodId` (navigation) · cold entry: **Needs nothing; that is what makes it the door.** No workstation travels with a browser sign-in (CHG-DOOR-001). `providerId` arrives only on the identity … |
| Route | `/general/platform-login-mfa` |

**What the spec says about it.** **Rebuilt as a sign-in form on 2 October 2026 (CHG-DOOR-002/003; Chinmay, 2 October 2026: fix the Block A blockers now).** It was generated as a list over active sessions, MFA methods and SSO providers with Force logout and Revoke all sessions on the door, which a person who is not yet signed in can never use (platform-foundation process notes). The sequence is the same on every staff and partner door: credentials (or the organisation's SSO) -> the authentication code only when a permission demands it (R135) -> the role prompt when several roles are held (ADR-0003) -> the landing. Managing sessions moved to the staff directory (BO-053); managing MFA methods stays on each app's own security or profile screen. **Every platform operator holds a PLATFORM_* permission, so the code is always asked** and the first sign-in always enrols (F104). Platform operators' sessions are not listed here: a session list on the Console would call tenant-permission operations with no platform-staff grant (R098).

**Known gaps.** Removed 2 October 2026 (CHG-WIR-021): The Console sign-in carried tables of active sessions with Force logout and Revoke all sessions; a person signing in has no session and must see none of that. … Removed 2 October 2026 (CHG-WIR-021): The Console sign-in carried tables of active sessions with Force logout and Revoke all sessions; a person signing in has no session and must see none of that. … Removed 2 October 2026 (CHG-WIR-021): The Console sign-in carried tables of active sessions with Force logout and Revoke all sessions; a person signing in has no session and must see none of that. …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The TICVAI Console's door for platform operators: username and password, then always the authentication code, because every platform operator holds a PLATFORM_* permission. First sign-in enrols the authenticator app (email as fallback) and shows recovery codes once. After sign-in the operator lands on the Platform Dashboard; their own and others' active sessions are managed elsewhere.

**Fixed on main** (the package already carries these; draw what it says): Pattern listDetail with tables of every active session, every MFA method and every SSO provider, and Force logout / Revoke all sessions on … (CHG-WIR-021); The login form requires workstationId. (CHG-WIR-021); startSsoAuthorization and completeSsoAuthorization exist but are not declared on any staff door. (CHG-WIR-021); emptyNoAccess names SESSION_FORCE_LOGOUT. (CHG-DOOR-003); Calls tenant-permission operations with no tenant picker and no platform-staff grant: forceLogout (SESSION_FORCE_LOGOUT) … (CHG-WIR-021); Tables show every schema field, plumbing included: 'Every active session' drop sessionId, principalId, roleId, workstationId, venueId … (CHG-WIR-021).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Username | text field | — | — | — | — | Goes into `LoginRequest.username`. | — |
| Password | text field | — | — | — | — | Goes into `LoginRequest.credential` with `method: password`. Minimum 8, show/hide. **No workstation is sent: a browser is not a registered device** (CHG-DOOR-001), and no PIN is offered, because a … | — |
| Authentication code | text field | — | — | — | — | Shown only when the sign-in comes back `requiresMfa`: the person holds a permission in `PasswordPolicy.mfaRequiredForPermissions` (ROLE_MANAGE, LEDGER_APPROVE, every PLATFORM_* permission, or one the … | — |
| New password | text field | — | — | — | — | Only when the credential was reset and is temporary: a new one is set before anything else, twice, and the last five cannot be reused (audit R132). | — |

**Sent by *Sign in*** (`login`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Username `username` | text area | required | — | max length 256 | — | — | `login` body |
| Credential `credential` | text area | required | — | max length 512 | — | Password, PIN, card token or RFID token depending on `method`. | `login` body |
| Method `method` | radio group | optional | Password | Password · PIN · Card · RFID · Sso | — | `pin` is how a till is actually used. A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets … | `login` body |
| Workstation `workstationId` | picker: choose a workstation | optional | — | — | shows names, sends the id | Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. | `login` body |
| Device fingerprint `deviceFingerprint` | text area | optional | — | max length 256 | — | — | `login` body |

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

**Sent by *Set up the authenticator app*** (`enrolMfaMethod`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Totp · SMS OTP · Email OTP · Biometric · Hardware token | — | — | `enrolMfaMethod` body |
| Target `target` | text field | optional | — | — | — | Phone or email for OTP methods. | `enrolMfaMethod` body |

**Sent by *Choose role*** (`selectRole`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Role `roleId` | picker: choose a role | required | — | — | shows names, sends the id | — | `selectRole` body |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Username and password**: Password minimum 8; no workstation, no PIN, no role picker unless the operator holds several platform roles. *(source: R126; ADR-0003)*
- **Authentication code**: Six digits from the authenticator app; Email me a code instead as fallback; five wrong codes lock for the lockout minutes, never permanently. *(source: R135; R126; F104 step 2)*
- **Enrol first method**: Only authenticator app or email; the secret as QR and text; confirmed by the first code; recovery codes shown once with copy and download. *(source: contracts/spine/identity.yaml#enrolMfaMethod; contracts/spine/identity.yaml#verifyMfaEnrolment; F104 step 2)*

#### Outputs: what the screen shows and produces

**Shown**

**Sign in with your organisation** (card list, from `listSsoProviders`): One button per identity provider TICVAI uses for its own staff; **absent, not disabled, when there is none.** Read before sign-in, unauthenticated. When a provider `isEnforced` for this person, the password field is hidden and only this remains.

| Shows | Format | Notes |
|---|---|---|
| Display name | text | — |
| Protocol | chip: Oidc, Saml2 | — |
| Is enforced | yes / no (icon or chip) | True disables password login for principals covered by this provider. |

**Finishing sign-in with your organisation** (progress indicator, from `completeSsoAuthorization`): On the provider's redirect back (`code` and `state` from the redirect, never typed). Returns the same `LoginResponse` as `login`, so the second factor and the role prompt follow exactly as below. 403: the provider proved who this is and no group maps to a role in this tenant, which grants nothing.

| Shows | Format | Notes |
|---|---|---|
| Access token | text | JWT carrying `sid`, validated per request against the session registry. |
| Refresh token | text | — |
| Expires in | 1,234 | Seconds |
| Requires role selection | yes / no (icon or chip) | — |
| Requires MFA | yes / no (icon or chip) | True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). |
| Has MFA method | yes / no (icon or chip) | Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 … |
| MFA methods | list or chips (count when long) | The principal's active methods, so the client can offer the right one for the `signIn` challenge. |
| ID | the name it points at, never the id | — |
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is active | yes / no (icon or chip) | — |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |
| Available roles | list or chips (count when long) | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Name | text | — |
| Is primary | yes / no (icon or chip) | — |

**Recovery codes** (credential display, from `verifyMfaEnrolment`): The method is active once its first code is verified. Recovery codes are shown once, with copy and download, and never again.

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

**Signed in as** (banner, from `getCurrentSession`): Read once the sign-in is complete (after the code and the role, where asked): the person's name and role, then straight on. A platform operator lands on the Platform Dashboard (ADM-002).

| Shows | Format | Notes |
|---|---|---|
| Session | the name it points at, never the id | — |
| Principal | the name it points at, never the id | — |
| Role | the name it points at, never the id | — |
| Display name | text | — |
| Scope | list or chips (count when long) | Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. |
| ID | the name it points at, never the id | — |
| Level | chip: Tenant, Brand, Region, Venue, Department, Sub department… | The eight organisational levels, plus `subject`. Restored 24 August. |
| Path | text | Materialised ltree path. Prefix-comparable — `uae.dubai` contains `uae.dubai.marina`. |
| Code | text | — |
| Name | text | — |
| Effective permissions | list or chips (count when long) | Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. |
| Permissions by scope | list or chips (count when long) | Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves. |
| Permissions | list or chips (count when long) | — |
| Sale board | the name it points at, never the id | Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board. |
| Workstation | grouped details | — |
| ID | the name it points at, never the id | — |
| Code | text | — |
| Venue | the name it points at, never the id | — |
| Region | the name it points at, never the id | — |
| Access point | the name it points at, never the id | Inherited from the workstation, never selected by the operator. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Sign in (primary button) | `login` POST `/auth/login` | LoginRequest | LoginResponse | 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused. | — |
| Continue with your organisation (secondary button) | `startSsoAuthorization` GET `/auth/sso/{providerId}/authorize` | — | inline | — | — |
| Verify (primary button) | `verifyMfaChallenge` POST `/auth/mfa/challenge/{challengeId}/verify` | inline | inline | — | — |
| Email me a code instead (secondary button) | `createMfaChallenge` POST `/auth/mfa/challenge` | inline | inline | — | — |
| Set up the authenticator app (secondary button) | `enrolMfaMethod` POST `/auth/mfa/methods` | inline | MfaEnrolment | 403 A guest caller while no venue of the tenant has guest two-step verification on (rev 3 GAP-B1, per venue).; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest … | — |
| Choose role (secondary button) | `selectRole` POST `/auth/select-role` | inline | Session | 403 Authenticated but not permitted at the requested scope | — |

**What each action does** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Sign in with SSO (where TICVAI uses one)**: Redirects to the identity provider and back; an unmapped group grants nothing. *(source: contracts/spine/identity.yaml#startSsoAuthorization; contracts/spine/identity.yaml#completeSsoAuthorization)*

**Data it reads**: `listSsoProviders` (onLoad, Which identity providers this door offers; unauthenticated …); `completeSsoAuthorization` (background, Exchange the provider's code for the same LoginResponse as …)

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Platform Dashboard*
- → `ADM-004` Platform Audit Log: *Platform Audit Log*
- → `PTR-001` Partner Login / MFA: *A partner user signs in through the same door*; carries `challengeId`, `methodId`, `providerId`; calls `getCurrentSession`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Checking the credential. The form stays visible and disabled. |
| Empty, first run (`?state=emptyFirstRun`) | **Nobody signed in** - the normal state of a door. The form offers username and password and, where TICVAI uses one, its SSO. |
| Error (`?state=error`) | Identity could not be reached. **Says so rather than saying the password is wrong**, and keeps what was typed. |
| Denied (`?state=denied`) | The credential does not match, or the account is locked. One message for both, with the attempts left before the lock; a locked account says when to try again. |
| Permission denied (`?state=emptyNoAccess`) | Signed in, and the person holds no role in this app. Says who at the tenant grants access; distinct from a wrong password. A door has no permission of its own to name, because the person is not signed in until it succeeds. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listSsoProviders` takes no filter; a tenant with no identity provider shows no SSO buttons at all, and the form is the whole door. |
| Session held (`?state=sessionHeld`) | `login` answered 409: this person already holds a session elsewhere (audit R184, ADR-0004). Says where and since when; only a holder of SESSION_FORCE_LOGOUT ends it, on the staff directory (BO-053), and signing in never ends it by itself. |
| MFA required (`?state=mfaRequired`) | **Signed in, not yet through.** The principal holds a permission that requires MFA (ROLE_MANAGE, LEDGER_APPROVE, any PLATFORM_* permission, or one the tenant added), so the screen calls `createMfaChallenge` (`action: signIn`) and asks for the authentication code; `verifyMfaChallenge` completes the sign-in. **Email me a code instead** is the fallback. Five wrong codes lock step-up for the policy's lockout minutes and the screen says until when (audit R135, R126). A person without such a … |
| MFA enrolment required (`?state=mfaEnrolmentRequired`) | **First sign-in, no method yet.** A person who requires MFA and has no active method enrols the authenticator app (email as the fallback) with `enrolMfaMethod`, confirms it with the first code (`verifyMfaEnrolment`), sees the recovery codes once, then continues to the code step (audit R135, R126 (5)). |
| Offline (`?state=offline`) | Not available, and the offline banner says why: signing in needs a connection. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 An active session already exists for this principal on another device. Per §3.1.3 the new login is refused.; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest the same (rev 3 GAP-B1).; 422 The new credential fails the password policy, or matches the current one or any of the previous … |

#### Edge cases to draw

- **Locked after five wrong codes**: "Too many attempts. Try again at 10:42." The session is not ended; nothing else is offered. *(source: F104 step 2; contracts/spine/identity.yaml#createMfaChallenge)*
- **The operator is already signed in elsewhere**: Refused with where (device, time); only another holder of SESSION_FORCE_LOGOUT can end it. *(source: ADR-0004)*

#### Consistency with other screens

- Match `PTR-001`: Same form, same second-factor step and wording (F104 step 4).
- Match `SUP-001`: Same door for venue management (F104 step 5).

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
operator:
  name: Sara Khalil
  username: sara.khalil
  method: authenticator app
  codeExample: 193 027
recoveryCodes:
- 7KQ2-MX9P
- R4TD-81WN
- …8 more
```

#### Permissions

- `login` → no permission · anonymous, partner
- `listSsoProviders` → no permission · anonymous, partner
- `startSsoAuthorization` → no permission · anonymous
- `completeSsoAuthorization` → no permission · anonymous
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest
- `enrolMfaMethod` → no permission · staff, partner, guest
- `verifyMfaEnrolment` → no permission · staff, partner, guest
- `selectRole` → no permission · staff, partner
- `changeOwnCredential` → no permission · staff, partner
- `getCurrentSession` → no permission · staff, partner

**A refused user sees:** Signed in, and the person holds no role in this app. Says who at the tenant grants access; distinct from a wrong password. A door has no permission of its own to name, because the person is not signed in until it succeeds.

#### Requirements it meets

6 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 5.1.5 | The system should have the option to be used by several waiters at the same time. | F&B & Guest Management | CONTRACTED | `login` |
| 5.8.2 | The system should only allow one session per user. | F&B & Guest Management | CONTRACTED | `login` |
| 7.1.16 | The system shall support MFA using Email OTP, SMS OTP, Authenticator Apps, and future supported authentication mechanisms. | F&B POS | CONTRACTED | `enrolMfaMethod` |
| 7.1.4 | The system should be able to have a login override option for the supervisor level in order to login to the POS if the need arises and the previous user has not logged out. | F&B POS | CONTRACTED | `selectRole` |
| 3.3.28 | Authorization Caching - System shall support caching of authorization decisions. | Admission and Access | CONTRACTED | `getCurrentSession` |
| 7.1.50 | Cache authorization decisions securely to improve performance while ensuring policy changes invalidate outdated cache entries. | F&B POS | CONTRACTED | `getCurrentSession` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-001` · status **notStarted** · provenance generated
- Flow F104 *A platform operator signs in under MFA*, step 1: The operator signs in with username and password. → **Signed in, not yet through.** Every platform operator holds a `PLATFORM_*` permission, and MFA is required by permission (decided 28 September, audit R135), so the session is not usable yet.
- Flow F104 *A platform operator signs in under MFA*, step 2: The second factor is asked for and given. → **The authenticator code, or an emailed code as the fallback** (audit R126 (5)). `verifyMfaChallenge` completes the sign-in; five wrong codes lock step-up for the policy's lockout minutes (audit R126 …
- Flow F104 *A platform operator signs in under MFA*, step 3: The session opens with its cross-tenant reach. → The operator lands on the Platform Dashboard with their session. Active sessions are not listed on the door (CHG-DOOR-003); ending one is done from a signed-in screen.
- Flow F109 *A tenant gets its first administrator*, step 1: The platform operator signs in → A session scoped to the platform, not to any tenant
- Flow F104 branch at step 2 (high): when The operator has no MFA method enrolled yet., **Enrolled before they get in.** A platform operator cannot finish signing in without a method, so ADM-001 enrols an authenticator app (or email) with `enrolMfaMethod` and `verifyMfaEnrolment` first …
- Flow F104 branch at step 2 (medium): when Five wrong codes., **Step-up locks for the policy's lockout minutes, never permanently** (audit R126 (6)). The screen says so and when it lifts; a permanent lock is a denial of service anybody can run.
- Flow F104 branch at step 1 (medium): when The acting principal lacks the permission at this scope., **Refused at the first step, not the last.** ADR-0002 makes authorisation user-driven — a person who gets three steps in and then cannot finish has been told the wrong thing.
- Flow F109 branch at step 1 (abandonsFlow): when The seeded platform account cannot sign in, **There is no second door.** MFA unreachable or the identity provider down leaves nobody able to issue an identity to anybody. This is the single point at which the whole permission tree is …
- ADR-0003 *Conditional role selection at login* (`docs/adr/0003-conditional-role-selection-at-login.md`)
- ADR-0004 *Single session per user* (`docs/adr/0004-single-session-per-user.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400, 403, 409, 422).
- [ ] Every output is drawn (51 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-001?state=<state>`: loading, emptyFirstRun, error, denied, emptyNoAccess, emptyNoResults, sessionHeld, mfaRequired, mfaEnrolmentRequired, offline.
- [ ] Every action is wired with its success and its failure: Sign in, Continue with your organisation, Verify, Email me a code instead, Set up the authenticator app, Choose role.
- [ ] Every transition is wired: `ADM-002`, `ADM-004`, `PTR-001`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-020` Platform User Directory

**Find TICVAI's platform staff and manage their accounts.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Access & Identity · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `USER_MANAGE` (1 operate, 1 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listPrincipals` reads the population and `getPrincipal` reads one of them — list, select, act |
| Offline | online only |
| Opens with | `principalId` (session), `tenantId` (navigation) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/general/platform-user-directory` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listPrincipals` (USER_MANAGE), `createPrincipal` (USER_MANAGE), `getPrincipal` (USER_MANAGE), `updatePrincipal` (USER_MANAGE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** TICVAI's own operators: find, create and deactivate platform staff and set their platform roles. Every platform operator must hold an MFA method.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- Uses the tenant identity operations (USER_MANAGE). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): Purpose "Find the right one quickly, and act on it without opening it" is generic. (CHG-WIR-023); Calls tenant-permission operations with no tenant picker and no platform-staff grant: listPrincipals (USER_MANAGE), createPrincipal … (CHG-SBO-001); Tables show every schema field, plumbing included: 'Every principal' drop id, primaryRoleId. (CHG-SBO-004).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Tenant | picker: choose an id | optional | — | — | shows names, sends the id | **Pick a tenant first** (audit R098; decided 2 October 2026, Chinmay: console screens get the tenant picker and grant, CHG-SBO-001). This screen's operations run in that tenant's cell, and a platform … | `Tenant.id` |
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listPrincipals`. | `listPrincipals` ?scopePath |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listPrincipals`. | `listPrincipals` ?isActive |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | radio group | — | Onboarding · Active · Suspended · Terminating · Terminated | `listTenants` ?status |
| Plan | picker: choose a plan | — | — | `listTenants` ?planId |

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

**Form: Open access grant** (modal, opened by *Open access grant*; *Open access grant* calls `openPlatformStaffGrant`, *Cancel* sends nothing)

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `USER_MANAGE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

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

**Every principal** (data table, from `listPrincipals`)

| Shows | Format | Notes |
|---|---|---|
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
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
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Create principal (primary button) | `createPrincipal` POST `/principals` | CreatePrincipalRequest | Principal | 400 Validation failed; 409 Username already in use within this cell | opens modal first |
| Save principal (secondary button) | `updatePrincipal` PATCH `/principals/{principalId}` | inline | Principal | — | opens modal first |

**Data it reads**: `listPrincipals` (onLoad, from page inventory); `getPrincipal` (onLoad, Read a principal); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

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
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `USER_MANAGE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Username already in use within this cell |

#### Edge cases to draw

- **createPrincipal answers 409**: Show it as something the person can act on, not a failure: Username already in use within this cell *(source: contracts/spine/identity.yaml#createPrincipal)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
operators:
- name: Sara Khalil
  username: sara.khalil
  role: Platform Operations
  mfa: enrolled
  lastSignIn: 01/10/2026 08:01
- name: Vikram Rao
  username: vikram.rao
  role: Release Manager
  mfa: not enrolled (cannot sign in)
```

#### Permissions

- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner
- `createPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `getPrincipal` → `USER_MANAGE` (configure) · staff, partner
- `updatePrincipal` → `USER_MANAGE` (configure) · staff, partner
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.6 | The system should be able to create a new Back Office/POS user and Logon to back office/POS using new user. | F&B POS | CONTRACTED | `createPrincipal` |
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

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

- [ ] Every input above is drawn (18), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Create principal, Save principal.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 1 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-021` Platform Role Management

**Define the roles TICVAI's platform staff hold.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Access & Identity · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai staff holding `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `ROLE_MANAGE` (1 operate, 1 read, 1 configure); in the flows as platform admin |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): `listRoles` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `tenantId` (navigation) |
| Route | `/general/platform-role-management` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Tenant picker and platform-staff grant added 2 October 2026** (CHG-SBO-001; Chinmay, pre-apply round: console screens get the R098 tenant picker and grant, the ADM-412 pattern). The Console runs outside every cell; `listRoles` (ROLE_MANAGE), `createRole` (ROLE_MANAGE) are tenant operations, refused 403 to a platform token until a time-boxed, audited grant into the picked tenant is open. The tenant sees the grant and every action under it. **No default roles (decided 2 October 2026 by Chinmay, DEC-007; CHG-CSP-003):** roles start from per-module presets (All, Viewer, Mid-level) that fill an editable checklist; the role can be renamed. Created inside the picked tenant under the open grant.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Platform roles for TICVAI staff (operations, release, support, billing) and the PLATFORM_* permissions each holds.

**Fixed on main** (the package already carries these; draw what it says): Purpose "for this venue". (CHG-WIR-023); Calls tenant-permission operations with no tenant picker and no platform-staff grant: listRoles (ROLE_MANAGE), createRole (ROLE_MANAGE). (CHG-SBO-001); Tables show every schema field, plumbing included: 'Every role' drop id, inheritsFromRoleId. (CHG-SBO-004).

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

**Collects what `openPlatformStaffGrant` sends before it is called** (audit R098). Required: `id` (a client UUIDv7, generated silently), `permissions` (tenant permissions only; `ROLE_MANAGE` preselected for this screen), `reason`, `expiresAt` (at most 8 hours ahead, proposed). Optional: `ticketRef`. Requires step-up: the operator presents a second factor first. The tenant sees the grant and everything done under it. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| ID `id` | picker: choose an id | required | — | — | shows names, sends the id | Client-generated UUIDv7 for the grant. | `openPlatformStaffGrant` body |
| Permissions `permissions` | multi-select chips | required | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE …; at … | — | What the operator may do in this tenant while the grant is open. Tenant permissions only; a `PLATFORM_*` value is refused `400`. | `openPlatformStaffGrant` body |
| Reason `reason` | text area | required | — | min length 3; max length 500 | — | — | `openPlatformStaffGrant` body |
| Ticket ref `ticketRef` | text field | optional | — | max length 100 | — | The support case this access serves, where there is one. | `openPlatformStaffGrant` body |
| Expires at `expiresAt` | date and time picker | required | — | At most 8 hours after opening (proposed, client to correct). | 1 Oct 2026, 14:30 (venue time zone) | At most 8 hours after opening (proposed, client to correct). | `openPlatformStaffGrant` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Create role** (modal, opened by *Create role*; *Create role* calls `createRole`, *Cancel* sends nothing)

**Collects what `createRole` sends before it is called.** Required: `code`, `name`. Optional: `description`, `presetCodes`, `permissions`. `presetCodes` fills the checklist from the chosen presets; `permissions` is the edited result. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | max length 64; pattern `^[A-Za-z0-9_-]+$` | — | Unique within the tenant, compared case-insensitively (decided 28 September, audit R108). | `createRole` body |
| Name `name` | text field | required | — | max length 200 | — | — | `createRole` body |
| Description `description` | text area | optional | — | max length 500 | — | — | `createRole` body |
| Preset codes `presetCodes` | list of values (chips) | optional | — | — | — | Presets (`CapabilityTemplate.code`) whose permissions fill the new role's checklist; copied, never bound (CHG-CSP-003). | `createRole` body |
| Permissions `permissions` | multi-select chips | optional | — | SESSION FORCE LOGOUT · USER MANAGE · ROLE MANAGE · PERMISSION GRANT · PERMISSION VIEW · PERMISSION MANAGE · PLATFORM TENANT VIEW · PLATFORM TENANT MANAGE · PLATFORM TENANT TERMINATE · PLATFORM PLAN MANAGE · PLATFORM CELL VIEW · PLATFORM CELL MANAGE … | — | Permissions ticked on the checklist beyond the presets. Unioned with them. | `createRole` body |

Errors to draw in the form: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A preset code that does not exist (`unknown-preset`), or an initial permission set that breaches a segregation rule (`segregation-breach`, naming the rule and …

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

**Every role** (data table, from `listRoles`)

| Shows | Format | Notes |
|---|---|---|
| Code | text | Unique within the tenant (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. |
| Name | text | — |
| Description | text | — |
| Permissions | list or chips (count when long) | A role that grants no permissions is not a role. `Role` carried a code, a name and two counts until 18 August, and … |
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
| Open access grant (primary button) | `openPlatformStaffGrant` POST `/platform-staff-grants` | inline | PlatformStaffGrant | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | step-up: mfa (Opens a platform operator's access into a tenant's data.); opens modal first |
| Create role (primary button) | `createRole` POST `/roles` | inline | Role | 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A preset code that does not exist … | opens modal first |

**Data it reads**: `listRoles` (onLoad, from page inventory); `listTenants` (onLoad, The tenant picker: the operator picks a tenant before …)

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
| Grant required (`?state=grantRequired`) | **No access into this tenant yet.** A tenant is picked and no platform-staff grant into it is open, so every tenant action is disabled and the screen offers **Open access grant** (`openPlatformStaffGrant`: reason, permissions `ROLE_MANAGE`, expiry). The same state returns when the grant reaches `expiresAt` (audit R098; CHG-SBO-001). |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit …; 422 A preset code that does not exist (`unknown-preset`), or an initial permission set that breaches a segregation rule (`segregation-breach`, naming the rule and … |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every role:
- code: AQC-AUH
  name: AquaCove Abu Dhabi
  description: Guest charged twice at Main Gate Till 3
  principalCount: 12
  grantCount: 12
- code: AQC-DXB
  name: Main Gate Till 3
  description: Group of 40 from Desert Gate Tours
  principalCount: 3
  grantCount: 3
- code: AQC-MCT
  name: Lagoon Grill
  description: Annual pass upgrade for the Al Nuaimi family
  principalCount: 0
  grantCount: 0
```

#### Permissions

- `listRoles` → `ROLE_MANAGE` (configure) · staff
- `createRole` → `ROLE_MANAGE` (configure) · staff
- `listTenants` → `PLATFORM_TENANT_VIEW` (read) · staff
- `listOwnPlatformStaffGrants` → `PLATFORM_TENANT_ACCESS` (operate) · staff
- `openPlatformStaffGrant` → `PLATFORM_TENANT_ACCESS` (operate) · staff · step-up mfa

**A refused user sees:** Shown when the caller lacks `ROLE_MANAGE`, which `listRoles` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.6 | It is expected to have one webstore/application API for each venue. | Ticketing Sales | CONTRACTED | data `Tenant` |

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
- ADR-0051 *Every AI function ships on a baseline and learns per tenant; a model goes live only on evidence* (`docs/adr/0051-ai-ships-on-a-baseline-and-learns-per-tenant.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (400, 403, 409, 422).
- [ ] Every output is drawn (22 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-021?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, grantRequired, offline.
- [ ] Every action is wired with its success and its failure: Open access grant, Create role.
- [ ] Every transition is wired: `ADM-001`, `ADM-002`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_ACCESS`, `PLATFORM_TENANT_VIEW`, `ROLE_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `ADM-699` My Account & Security

**Let a platform operator manage their own sign-in: the authentication methods, the password and the sessions they hold, and sign any of those sessions out.**

| | |
|---|---|
| App · platform | TICVAI Control · P09 TICVAI Web (web) |
| Module | Access & Identity · wave 1 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | ticvai |
| Device and orientation | This is the TICVAI console on a desktop browser, 1440 wide: a left navigation rail, a top bar with the tenant switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): Two short lists the operator acts on, their own methods and their own sessions, with the account they are signed in as above them. |
| Offline | online only |
| Opens with | `challengeId` (navigation), `methodId` (navigation), `sessionId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/access-identity/my-account-security` |

**What the spec says about it.** **Added 2 October 2026** (Chinmay, door follow-ups: "Add 'My account & security'"; CHG-SBO-022, CHG-CSP-052). A platform operator's own second-factor methods and own sessions. The doors no longer manage them (CHG-DOOR-002, CHG-DOOR-003), and the staff session list (`listActiveSessions`) needs `SESSION_FORCE_LOGOUT`, which an operator should not need to see their own sessions. **Nothing here needs a permission**: every signed-in operator sees only their own account, and ending a session or removing a method asks for the authentication code first. **No tenant picker**: the operator's account is the Control Plane's, not a tenant's (R098 does not apply).

#### Inputs: what the user enters or picks

**Form: Add a method** (modal, opened by *Add a method*; *Add a method* calls `enrolMfaMethod`, *Cancel* sends nothing)

**Collects what `enrolMfaMethod` sends before it is called.** Required: `kind`. Optional: `target`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Totp · SMS OTP · Email OTP · Biometric · Hardware token | — | — | `enrolMfaMethod` body |
| Target `target` | text field | optional | — | — | — | Phone or email for OTP methods. | `enrolMfaMethod` body |

Errors to draw in the form: 403 A guest caller while no venue of the tenant has guest two-step verification on (rev 3 GAP-B1, per venue).; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest the same (rev 3 GAP-B1).

**Form: Confirm the code** (modal, opened by *Confirm the code*; *Confirm the code* calls `verifyMfaEnrolment`, *Cancel* sends nothing)

**Collects what `verifyMfaEnrolment` sends before it is called.** Required: `code`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `verifyMfaEnrolment` body |

**Form: Change password** (modal, opened by *Change password*; *Change password* calls `changeOwnCredential`, *Cancel* sends nothing)

**Collects what `changeOwnCredential` sends before it is called.** Required: `method`, `currentCredential`, `newCredential`. The current password is asked; the new one meets the password policy (minimum 8). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Method `method` | segmented control | required | — | Password · PIN | — | Which credential is being changed. Card, RFID and SSO are not secrets the principal holds, so they are not changed here. | `changeOwnCredential` body |
| Current credential `currentCredential` | text area | required | — | max length 512 | — | — | `changeOwnCredential` body |
| New credential `newCredential` | text area | required | — | max length 512 | — | — | `changeOwnCredential` body |

Errors to draw in the form: 400 Validation failed; 422 The new credential fails the password policy, or matches the current one or any of the previous `PasswordPolicy.reusePreventionCount` credentials (5 unless the …

**Form: Sign this session out** (confirmDialog, opened by *Sign this session out*; *Verify and sign out* calls `verifyMfaChallenge`, *Cancel* sends nothing)

Names the device and when the session started, then asks for the authentication code (`createMfaChallenge`, `verifyMfaChallenge`) before `endOwnSession` is sent. Dismissing sends nothing.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `verifyMfaChallenge` body |

**Form: Remove method** (confirmDialog, opened by *Remove method*; *Send the code* calls `createMfaChallenge`, *Cancel* sends nothing)

Names the method, asks for the authentication code first (`createMfaChallenge`), and is refused for the last method.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Action `action` | text field | required | — | — | — | What the step-up is for. Recorded in the audit trail. | `createMfaChallenge` body |
| Method `methodId` | picker: choose a method | optional | — | — | shows names, sends the id | — | `createMfaChallenge` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | For a guest, the venue whose `VenueSettings.identity.guestTwoStep` applies (sign-in venue, or the venue of the booking being acted on). | `createMfaChallenge` body |

#### Outputs: what the screen shows and produces

**Shown**

**This session** (detail panel, from `listOwnSessions`): The operator's own account and the session in use (marked in the list below); never another operator's.

| Shows | Format | Notes |
|---|---|---|
| Principal name | text | — |
| Role name | text | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |

**Authentication methods** (data table, from `listMfaMethods`): The authenticator app is the method; the emailed code is the fallback. Every platform operator holds a PLATFORM_* permission, so at least one method always stays: removing the last one is refused and the button is disabled with that reason.

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Totp, SMS OTP, Email OTP, Biometric, Hardware token | — |
| Label | text | — |
| Masked target | text | Partially masked destination, so a person can tell two methods apart. |
| Is primary | yes / no (icon or chip) | — |
| Enrolled at | 1 Oct 2026, 14:30 | — |
| Last used at | 1 Oct 2026, 14:30 | — |

**My sessions** (data table, from `listOwnSessions`): Every session this operator holds, this one marked "This session". Paged (`listOwnSessions`).

| Shows | Format | Notes |
|---|---|---|
| Device info | text | — |
| Ip address | text | — |
| Started at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |
| MFA satisfied | yes / no (icon or chip) | — |
| Status | chip: Active, Signed out, Terminated, Expired | A registry that only holds live sessions cannot answer why one ended. Kept on the record so a supervisor asking *what happened to till 4* … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add a method (primary button) | `enrolMfaMethod` POST `/auth/mfa/methods` | inline | MfaEnrolment | 403 A guest caller while no venue of the tenant has guest two-step verification on (rev 3 GAP-B1, per venue).; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest … | opens modal first |
| Confirm the code (secondary button) | `verifyMfaEnrolment` POST `/auth/mfa/methods/{methodId}` | inline | MfaMethod | — | opens modal first |
| Remove method (destructive button) | `removeMfaMethod` DELETE `/auth/mfa/methods/{methodId}` | — | — | 409 Last remaining method of a principal who holds a permission that requires MFA (audit R135) | — |
| Change password (secondary button) | `changeOwnCredential` POST `/auth/credential` | ChangeCredentialRequest | — | 400 Validation failed; 422 The new credential fails the password policy, or matches the current one or any of the previous `PasswordPolicy.reusePreventionCount` credentials (5 unless the … | opens modal first |
| Sign this session out (destructive button) | `endOwnSession` POST `/auth/sessions/mine/{sessionId}/end` | — | ActiveSession | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The session is the one in use (`use-logout`) or has already ended (`session-ended`). | step-up: mfa (Ending a session elsewhere is an account-security act; the second factor proves it is the owner at the keyboard.) |

**Data it reads**: `listMfaMethods` (onLoad, The operator's own authentication methods); `listOwnSessions` (onLoad, The operator's own sessions (CHG-CSP-052))

**Where the user goes next**

- → `ADM-002` Platform Dashboard: *Back to the Platform Dashboard*
- → `ADM-001` Platform Login / MFA: *Signing this session out returns to the door*; carries `challengeId`, `methodId`; calls `endOwnSession`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The account, its methods and its sessions. |
| Error (`?state=error`) | Could not load. Names which read failed (methods or sessions) and leaves the other in place. |
| Empty, first run (`?state=emptyFirstRun`) | **Never empty for methods**: the first sign-in enrols one (F104). With one session, the list shows only "This session" and says no other session is open. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: nothing on this screen filters. |
| Permission denied (`?state=emptyNoAccess`) | Never shown: every signed-in operator sees their own account; nothing here needs a permission. |
| Step up (`?state=stepUp`) | Ending a session and removing a method ask for the authentication code in the confirmation (`createMfaChallenge`, `verifyMfaChallenge`); five wrong codes lock step-up for the lockout minutes, never permanently. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Last remaining method of a principal who holds a permission that requires MFA (audit R135); 409 The session is the one in use (`use-logout`) or has already ended (`session-ended`).; 422 A kind the caller may not enrol. Staff use `totp`, with `emailOtp` as the fallback (audit R126); a guest the same (rev 3 GAP-B1). |

#### Permissions

- `listMfaMethods` → no permission · staff, partner, guest
- `listOwnSessions` → no permission · staff, partner
- `enrolMfaMethod` → no permission · staff, partner, guest
- `verifyMfaEnrolment` → no permission · staff, partner, guest
- `removeMfaMethod` → no permission · staff, partner, guest
- `changeOwnCredential` → no permission · staff, partner
- `endOwnSession` → no permission · staff, partner · step-up mfa
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest

**A refused user sees:** Never shown: every signed-in operator sees their own account; nothing here needs a permission.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 7.1.16 | The system shall support MFA using Email OTP, SMS OTP, Authenticator Apps, and future supported authentication mechanisms. | F&B POS | CONTRACTED | `enrolMfaMethod` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for all of P09, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P09 TICVAI Web.dc.html#adm-699` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (10), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#ADM-699?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, stepUp, offline.
- [ ] Every action is wired with its success and its failure: Add a method, Confirm the code, Remove method, Change password, Sign this session out.
- [ ] Every transition is wired: `ADM-002`, `ADM-001`.
- [ ] Sign-in is asked only where the spec asks for it.
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

**1 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"changeOwnCredential": {"method":"POST","path":"/auth/credential","contract":"identity","summary":"Change the caller's own password or PIN","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChangeCredentialRequest","responds":null},
"completeSsoAuthorization": {"method":"POST","path":"/auth/sso/{providerId}/callback","contract":"identity","summary":"Exchange an SSO code for a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LoginResponse"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createPrincipal": {"method":"POST","path":"/principals","contract":"identity","summary":"Create a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"CreatePrincipalRequest","responds":"Principal"},
"createRole": {"method":"POST","path":"/roles","contract":"identity","summary":"Create a role","permission":"ROLE_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Role"},
"endOwnSession": {"method":"POST","path":"/auth/sessions/mine/{sessionId}/end","contract":"identity","summary":"Sign one of the caller's own sessions out","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ActiveSession"},
"enrolMfaMethod": {"method":"POST","path":"/auth/mfa/methods","contract":"identity","summary":"Enrol an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MfaEnrolment"},
"getCurrentSession": {"method":"GET","path":"/auth/session","contract":"identity","summary":"Current session and effective permissions","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"workstation","parameters":[],"requestBody":null,"responds":"Session"},
"getPrincipal": {"method":"GET","path":"/principals/{principalId}","contract":"identity","summary":"Read a principal","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Principal"},
"listMfaMethods": {"method":"GET","path":"/auth/mfa/methods","contract":"identity","summary":"Enrolled MFA methods","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MfaMethod"},
"listOwnPlatformStaffGrants": {"method":"GET","path":"/platform-staff-grants/mine","contract":"identity","summary":"The calling platform operator's own grants into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"activeOnly","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOwnSessions": {"method":"GET","path":"/auth/sessions/mine","contract":"identity","summary":"The caller's own signed-in sessions","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPrincipals": {"method":"GET","path":"/principals","contract":"identity","summary":"List principals","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRoles": {"method":"GET","path":"/roles","contract":"identity","summary":"List roles","permission":"ROLE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listSsoProviders": {"method":"GET","path":"/auth/sso/providers","contract":"identity","summary":"Identity providers configured for this tenant","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"SsoProvider"},
"listTenants": {"method":"GET","path":"/tenants","contract":"subscription","summary":"List tenants","permission":"PLATFORM_TENANT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"status","in":"query","required":null},{"name":"planId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"login": {"method":"POST","path":"/auth/login","contract":"identity","summary":"Authenticate and open a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"LoginRequest","responds":"LoginResponse"},
"openPlatformStaffGrant": {"method":"POST","path":"/platform-staff-grants","contract":"identity","summary":"A platform operator opens a time-boxed grant into this tenant","permission":"PLATFORM_TENANT_ACCESS","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"PlatformStaffGrant"},
"removeMfaMethod": {"method":"DELETE","path":"/auth/mfa/methods/{methodId}","contract":"identity","summary":"Remove an MFA method","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"selectRole": {"method":"POST","path":"/auth/select-role","contract":"identity","summary":"Choose a role for a multi-role session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Session"},
"startSsoAuthorization": {"method":"GET","path":"/auth/sso/{providerId}/authorize","contract":"identity","summary":"Begin an SSO flow","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"redirectUri","in":"query","required":true}],"requestBody":null,"responds":null},
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
"ChangeCredentialRequest": {"type":"object","description":"Request only. The credential itself is stored hashed in `identity.principal_credential` and is never returned by any operation (`handoff/schema-storage-only.md`).\n","required":["method","currentCredential","newCredential"],"properties":{"method":{"type":"string","enum":["password","pin"],"description":"Which credential is being changed. Card, RFID and SSO are not secrets the principal holds, so they are not changed here."},"currentCredential":{"type":"string","maxLength":512,"writeOnly":true},"newCredential":{"type":"string","maxLength":512,"writeOnly":true}}},
"CreatePrincipalRequest": {"type":"object","required":["username","displayName"],"properties":{"username":{"type":"string","maxLength":256},"displayName":{"type":"string","maxLength":200},"initialCredential":{"type":"string","maxLength":512,"writeOnly":true},"mustChangeCredential":{"type":"boolean","default":true},"validTo":{"type":"string","format":"date-time"},"roleIds":{"type":"array","items":{"type":"string","format":"uuid"}}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"LoginRequest": {"type":"object","description":"**`workstationId` is required for a device door and absent from a browser door** (CHG-DOOR-001, 2 October 2026). It was required on every login, so no browser could sign in: the TICVAI Console (ADM-001), Venue Management (SUP-001) and the partner portal (PTR-001) have no workstation. Optional in the schema is additive against r1; the rule moved to where it belongs, the device-bound methods: `pin`, `card` and `rfid` without a `workstationId` are refused 400 (`workstation-required`). A `password` sign-in from a till, handheld or scanner still sends it, because the workstation decides the Sale Board, the hardware and the till identity (never a permission, ADR-0002).\n","required":["username","credential"],"properties":{"username":{"type":"string","maxLength":256},"credential":{"type":"string","description":"Password, PIN, card token or RFID token depending on `method`.\n","maxLength":512,"writeOnly":true},"method":{"type":"string","description":"**`pin` is how a till is actually used.** A cashier signs in at a shared terminal between guests, and a password on a touchscreen with somebody waiting is a password that gets shortened, shared or written on the drawer. The employee number goes in `username` and the PIN in `credential`, so the shape of the request does not change — only what the operator types.\n\n**A PIN is weaker than a password and the difference is bounded by the device, not by the secret.** A `pin` (like `card` and `rfid`) is accepted only with a `workstationId`, refused 400 `workstation-required` without one (CHG-DOOR-001), and the workstation is *NOT a permission source*: it says which till, and the till is on a venue network in a staff area. A PIN is a reasonable credential there and nowhere else, which is why this is an enum value and not a policy flag — a surface that wants it has to ask for it by name.\n\nAdded 10 September 2026 for `POS-000 Sign In`.\n","enum":["password","pin","card","rfid","sso"],"default":"password"},"workstationId":{"type":"string","format":"uuid","description":"Identifies the device. Determines Sale Board, connected hardware, till identity and Access Point inheritance. NOT a permission source.\n\n**Sent by a device door, never by a browser** (CHG-DOOR-001, 2 October 2026). Required in effect for the device-bound methods `pin`, `card` and `rfid` (400 `workstation-required` without it); absent on the TICVAI Console, Venue Management and partner portal sign-ins, which have no workstation.\n"},"deviceFingerprint":{"type":"string","maxLength":256}}},
"LoginResponse": {"x-ticvai-persistence":"none — computed","allOf":[{"$ref":"#/components/schemas/TokenPair"},{"type":"object","required":["requiresRoleSelection","requiresMfa"],"properties":{"requiresRoleSelection":{"type":"boolean"},"requiresMfa":{"type":"boolean","description":"True when the principal holds any permission listed in `PasswordPolicy.mfaRequiredForPermissions` (decided 28 September, audit R135). The session is not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge."},"hasMfaMethod":{"type":"boolean","description":"Whether the principal has an active MFA method. With `requiresMfa` true and this false, the client must enrol one first (audit R135, R126 (5))."},"mfaMethods":{"type":"array","description":"The principal's active methods, so the client can offer the right one for the `signIn` challenge. Empty when `requiresMfa` is false.","items":{"$ref":"#/components/schemas/MfaMethod"}},"availableRoles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"session":{"$ref":"#/components/schemas/Session"}}}]},
"MfaEnrolment": {"x-ticvai-persistence":"none — transient","type":"object","required":["methodId","kind"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"methodId":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"secret":{"type":"string","nullable":true,"description":"TOTP shared secret. Returned once, at enrolment, and never again."},"qrCodeUri":{"type":"string","nullable":true},"recoveryCodes":{"type":"array","description":"Returned once, in this enrolment response (`enrolMfaMethod` writes them, hashed, to `identity.mfa_recovery_code`). Not retrievable afterwards — `verifyMfaEnrolment` does not return them.\n","items":{"type":"string"}},"expiresAt":{"type":"string","format":"date-time"}}},
"MfaKind": {"type":"string","enum":["totp","smsOtp","emailOtp","biometric","hardwareToken"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Permission": {"type":"string","enum":["SESSION_FORCE_LOGOUT","USER_MANAGE","ROLE_MANAGE","PERMISSION_GRANT","PERMISSION_VIEW","PERMISSION_MANAGE","PLATFORM_TENANT_VIEW","PLATFORM_TENANT_MANAGE","PLATFORM_TENANT_TERMINATE","PLATFORM_PLAN_MANAGE","PLATFORM_CELL_VIEW","PLATFORM_CELL_MANAGE","PLATFORM_BILLING_VIEW","PLATFORM_AI_MANAGE","PLATFORM_BILLING_MANAGE","PLATFORM_RELEASE_VIEW","PLATFORM_RELEASE_MANAGE","PLATFORM_RELEASE_PROMOTE","PLATFORM_MIGRATION_VIEW","PLATFORM_MIGRATION_APPLY","PLATFORM_TENANT_ACCESS","TENANT_CONFIGURE","TENANT_VIEW","TENANT_PUBLISH","SCOPE_VIEW","SCOPE_MANAGE","REGION_CONFIGURE","WORKSTATION_CONFIGURE","PRODUCT_VIEW","PRODUCT_CONFIGURE","PRODUCT_APPROVE","PRODUCT_PUBLISH","PRICE_VIEW","PRICE_CONFIGURE","EVENT_CONFIGURE","PERFORMANCE_CONFIGURE","CAPACITY_CONFIGURE","ORDER_VIEW","ORDER_VIEW_OTHER","ORDER_CREATE","ORDER_MODIFY","ORDER_DISCOUNT","ORDER_CANCEL","ORDER_VOID","ORDER_REFUND","ORDER_REFUND_APPROVE","ORDER_REFUND_BULK","ORDER_EXCHANGE","ORDER_RESCHEDULE","ORDER_REPRINT","PRICE_OVERRIDE","DISCOUNT_APPLY","CREDIT_MANAGE","CREDIT_OVERRIDE","WALLET_VIEW","WALLET_OPERATE","WALLET_CONFIGURE","PAYMENT_VIEW","PAYMENT_CONFIGURE","PAYMENT_PROVIDER_MANAGE","PAYMENT_DISPUTE","SHIFT_OPEN","SHIFT_CLOSE","SHIFT_SUSPEND","SHIFT_CLOSE_OTHER","SHIFT_APPROVE_OPEN","SHIFT_APPROVE_CLOSE","SHIFT_REOPEN","CASH_LIFT","CASH_ADD","CASH_NO_SALE","DEPOSIT_BOX_MODIFY_OWN","DEPOSIT_BOX_MODIFY_OTHER","OVERSHORT_ACCEPT","ACCESS_VALIDATE","ACCESS_OVERRIDE","ACCESS_POINT_CONFIGURE","TURNSTILE_MODE_SET","TICKET_LOOKUP","ACCREDITATION_VIEW","ACCREDITATION_APPLY","ACCREDITATION_APPROVE","ACCREDITATION_ISSUE","ACCREDITATION_MANAGE","ACCREDITATION_CONFIGURE","REPORT_VIEW_OWN","REPORT_VIEW_WORKSTATION","REPORT_VIEW_VENUE","REPORT_VIEW_REGION","REPORT_VIEW_TENANT","REPORT_EXPORT","REPORT_EXPORT_PII","REPORT_MANAGE","REPORT_SCHEDULE","LEDGER_VIEW","LEDGER_POST","LEDGER_APPROVE","TAX_CONFIGURE","ACCOUNT_CONFIGURE","SETTLEMENT_VIEW","SETTLEMENT_RECONCILE","GUEST_VIEW","GUEST_VIEW_PII","GUEST_MANAGE","VENUE_MAP_VIEW","VENUE_MAP_MANAGE","VENUE_MAP_PUBLISH","RESOURCE_VIEW","RESOURCE_BOOK","RESOURCE_MANAGE","RESOURCE_CONFIGURE","RENTAL_VIEW","RENTAL_BOOK","RENTAL_OPERATE","RENTAL_MANAGE","RENTAL_CONFIGURE","RENTAL_PRICE","RENTAL_APPROVE","RENTAL_OVERRIDE","DEVELOPER_VIEW","DEVELOPER_MANAGE","DEVELOPER_ADMIN","LOYALTY_ACCRUE","LOYALTY_REDEEM","LOYALTY_ADJUST","MARKETING_VIEW","MARKETING_MANAGE","MARKETING_SEND","CASE_VIEW","CASE_MANAGE","ASSET_LIBRARY_VIEW","ASSET_LIBRARY_MANAGE","ASSET_LIBRARY_APPROVE","ASSET_LIBRARY_SHARE","QUEUE_VIEW","QUEUE_MANAGE","QUEUE_REDEEM","QUEUE_OVERRIDE","TRANSPORT_VIEW","TRANSPORT_MANAGE","TRANSPORT_PRICE","ASSET_VIEW","ASSET_MANAGE","WORK_ORDER_VIEW","WORK_ORDER_MANAGE","WORK_ORDER_VERIFY","INSPECTION_VIEW","INSPECTION_SUBMIT","INSPECTION_MANAGE","INCIDENT_REPORT","INCIDENT_VIEW","INCIDENT_MANAGE","KIOSK_ATTEND","DEVICE_VIEW","DEVICE_CONFIGURE","DEVICE_MANAGE","APPROVAL_ACT","APPROVAL_DELEGATE","AI_USE","AI_CONFIGURE","AI_APPROVE","AI_AUDIT_VIEW","RISK_REVIEW","RISK_INVESTIGATE","AUDIT_VIEW","APPROVAL_VIEW","APPROVAL_REQUEST","APPROVAL_DECIDE","APPROVAL_CONFIGURE","MAINTENANCE_EXECUTE","MAINTENANCE_APPROVE","WORKFORCE_VIEW","WORKFORCE_MANAGE","ATTENDANCE_RECORD","ANNOUNCEMENT_PUBLISH","ANNOUNCEMENT_EMERGENCY","PARTNER_VIEW","PARTNER_MANAGE","PARKING_CONFIGURE","PAYMENT_VOID","PROCUREMENT_VIEW","PROCUREMENT_REQUEST","PROCUREMENT_MANAGE","PROCUREMENT_RECEIVE","CORE_AI_PUBLISH","TICKETING_AI_PUBLISH","ACCESS_AI_PUBLISH","FNB_AI_PUBLISH","RETAIL_AI_PUBLISH","INVENTORY_AI_PUBLISH","SEATING_AI_PUBLISH","MEMBERSHIP_AI_PUBLISH","MARKETING_AI_PUBLISH","RESOURCES_AI_PUBLISH","QUEUE_AI_PUBLISH","TRANSPORT_AI_PUBLISH","GAMES_AI_PUBLISH","MAINTENANCE_AI_PUBLISH","ACCREDITATION_AI_PUBLISH","PARTNER_AI_PUBLISH","ANALYTICS_AI_PUBLISH","BIOMETRIC_IMAGE_VIEW","ACCESS_DIRECTION_SET","REPORT_GOVERNANCE_MANAGE"]},
"PlatformStaffGrant": {"type":"object","x-ticvai-persistence":"identity.platform_staff_grant","description":"**One platform operator's time-boxed access into this tenant** (decided 28 September, audit R098). Written by `openPlatformStaffGrant`, read by the tenant through `listPlatformStaffGrants`, and never edited: a grant ends at `expiresAt`, and a new need is a new grant.\n","required":["id","operatorPrincipalId","permissions","reason","openedAt","expiresAt"],"properties":{"id":{"type":"string","format":"uuid"},"operatorPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"The platform operator, from the Control Plane token. Set by the server."},"operatorDisplayName":{"type":"string","readOnly":true},"permissions":{"type":"array","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"reason":{"type":"string"},"ticketRef":{"type":"string","nullable":true},"openedAt":{"type":"string","format":"date-time","readOnly":true},"expiresAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"The tenant root. **Operations write it at `tenant` scope**; the server sets it."}}},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"Role": {"x-ticvai-persistence":"identity.role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique within the tenant** (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. Unique per tenant, not per venue, because a grant names a role anywhere in the tree; `createRole` refuses a duplicate with `409 duplicate-code`.\n"},"name":{"type":"string"},"description":{"type":"string"},"permissions":{"type":"array","description":"**A role that grants no permissions is not a role.** `Role` carried a code, a name and two counts until 18 August, and `identity.role_permission` derived from it with exactly one column — `role_id`. **A join table that joins to nothing**, found by Hrushikant in review and missed by the schema audit that ran the same day.\n**The audit asked whether every table had columns, a relationship and an owner, and this table had all three.** What it did not ask is whether a table with one column can do the job its name claims.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"inheritsFromRoleId":{"type":"string","format":"uuid","nullable":true,"description":"**Role composition, one level deep and no deeper.** A supervisor role that is a cashier plus three permissions is how venues actually describe them.\n**Cycles are refused and depth is capped at one**, because a permission set nobody can read off the screen is a permission set nobody audits.\n"},"isSystem":{"type":"boolean","default":false,"description":"**Seeded roles ship and are editable; deleting one is refused.** A venue that removes `cashier` and rebuilds it has two roles with one name in the audit log.\n**The seeded system roles are Cashier, Supervisor, Venue Manager, Finance and Tenant Admin** (proposed in `docs/active/seed-data-proposal.md` section 2, client to correct; audit R229).\n\n**Superseded 2 October 2026: no fixed default roles** (Chinmay; DEC-007; CHG-CSP-003). The five are presets (`CapabilityTemplate`, `isPreset`) a role starts from, not roles a tenant is given. The field stays for clients built at r1 and is false on every role created from 2 October.\n"},"presetCode":{"type":"string","nullable":true,"readOnly":true,"maxLength":64,"description":"**The preset this role was started from, for the record only** (decided 2 October 2026, Chinmay; DEC-007; CHG-CSP-003): the first of `createRole.presetCodes`, or null for a role ticked by hand. It binds nothing; a later edit of the preset never changes this role.\n"},"principalCount":{"type":"integer"},"grantCount":{"type":"integer"}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n\n**Optional since 2 October 2026: only a till session carries it** (Chinmay, door follow-ups; CHG-CSP-002; breaking change against r1 approved as BC-001 to BC-005 in `docs/active/breaking-changes.yaml`). A browser door (ADM-001, SUP-001, PTR-001) and a staff handheld (EMP-001) sign in with no workstation since CHG-DOOR-001, so they have no board to land on and the field is absent. On a till it is the workstation's effective board: the outlet's board unless the till overrides it (`tenancy.Workstation.saleBoardSource`; CHG-CSP-006). A client reads its landing from this field when present and from its own platform otherwise.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"SessionStatus": {"type":"string","description":"**The life of one signed-in session, which is not the life of a shift.** A shift holds the float and survives a break; a session holds the person and does not. `ShiftStatus.suspended` is where a break lives — *break cover; float intact, workstation released* — and the release of the workstation is exactly why the session ends rather than pausing: the next person opens their own.\n**One principal, one active session per workstation.** Enforced by the `ActiveSession` registry rather than by a state, because it is a fact about the set of sessions and not about any one of them.\n","enum":["active","signedOut","terminated","expired"]},
"SsoProtocol": {"type":"string","enum":["oidc","saml2"]},
"SsoProvider": {"x-ticvai-persistence":"identity.sso_provider","type":"object","required":["id","displayName","protocol"],"properties":{"id":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"protocol":{"$ref":"#/components/schemas/SsoProtocol"},"iconAssetRef":{"type":"string","nullable":true},"isEnforced":{"type":"boolean","description":"True disables password login for principals covered by this provider."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope**; the server sets it and ignores it in a request."}}},
"SuspensionMode": {"type":"string","description":"Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n","enum":["readOnly","noNewSales","fullLockout"]},
"Tenant": {"x-ticvai-persistence":"control.tenant","type":"object","required":["id","code","name","status","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"status":{"$ref":"#/components/schemas/TenantStatus"},"suspensionMode":{"$ref":"#/components/schemas/SuspensionMode"},"suspensionReason":{"type":"string","nullable":true},"suspensionEffectiveAt":{"type":"string","format":"date-time","nullable":true,"description":"When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."},"suspensionNoticeMessage":{"$ref":"#/components/schemas/LocalisedText","description":"The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."},"terminationScheduledAt":{"type":"string","format":"date-time","nullable":true,"description":"When `terminateTenant` started the retention window. Null when no termination is under way."},"terminationRetentionUntil":{"type":"string","format":"date-time","nullable":true,"description":"`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."},"terminationReason":{"type":"string","maxLength":1000,"nullable":true},"terminationRequestedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"planId":{"type":"string","format":"uuid","nullable":true},"planName":{"type":"string","nullable":true},"cellCount":{"type":"integer"},"venueCount":{"type":"integer"},"regionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"},"billingEmail":{"type":"string"},"billingAddress":{"type":"string","maxLength":500,"nullable":true,"description":"Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."},"accountManagerPrincipalId":{"type":"string","format":"uuid","nullable":true},"createdAt":{"type":"string","format":"date-time"},"activatedAt":{"type":"string","format":"date-time","nullable":true}}},
"TenantStatus": {"type":"string","enum":["onboarding","active","suspended","terminating","terminated"]},
"TokenPair": {"x-ticvai-persistence":"none — transient","type":"object","required":["accessToken","refreshToken","expiresIn"],"properties":{"accessToken":{"type":"string","description":"JWT carrying `sid`, validated per request against the session registry."},"refreshToken":{"type":"string"},"expiresIn":{"type":"integer","description":"Seconds"}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
